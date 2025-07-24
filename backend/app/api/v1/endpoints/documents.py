from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import aiofiles
import os
from app.core.config import settings
from app.services.document_processor import document_processor
from app.services.s3_service import s3_service
from app.models.document import Document, DocumentStatus
from app.models.analysis import Analysis, AnalysisStatus
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentList
from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.workers.tasks import process_analysis_task
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a resume or CV document."""
    
    # Validate file extension
    file_extension = file.filename.split('.')[-1].lower()
    allowed_extensions = settings.ALLOWED_EXTENSIONS or ["pdf", "docx", "doc"]
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Validate file size
    file_size = 0
    contents = await file.read()
    file_size = len(contents)
    
    if file_size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE_MB}MB"
        )
    
    try:
        # Extract text from document
        logger.info(f"Processing {file.filename} ({file_size} bytes, type: {file_extension})")
        text = await document_processor.extract_text(contents, file_extension)
        
        if not text or len(text.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ドキュメントからテキストを抽出できませんでした。PDFが空か、スキャンされた画像の可能性があります。"
            )
        
        logger.info(f"Successfully extracted {len(text)} characters from {file.filename}")
        
        # Detect document type
        doc_type = document_processor.detect_document_type(text, file.filename)
        
        # Upload to S3
        s3_key = f"documents/{current_user.id}/{file.filename}"
        await s3_service.upload_file(contents, s3_key, file.content_type)
        
        # Create database record
        db_document = Document(
            user_id=current_user.id,
            filename=file.filename,
            file_type=file_extension,
            document_type=doc_type,
            file_size=file_size,
            s3_key=s3_key,
            status=DocumentStatus.PROCESSED,
            raw_text=text
        )
        
        # Parse structured data based on document type
        if doc_type == "resume":
            db_document.structured_data = document_processor.parse_japanese_resume(text)
        elif doc_type == "cv":
            db_document.structured_data = document_processor.parse_japanese_cv(text)
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Create analysis record automatically
        db_analysis = Analysis(
            user_id=current_user.id,
            document_id=db_document.id,
            status=AnalysisStatus.PENDING
        )
        
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Queue background task for analysis
        background_tasks.add_task(
            process_analysis_task,
            analysis_id=db_analysis.id
        )
        
        # Return document response with analysis_id
        response = DocumentResponse.from_orm(db_document)
        response_dict = response.dict()
        response_dict['analysis_id'] = db_analysis.id
        
        return response_dict
        
    except Exception as e:
        logger.error(f"Document upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )


@router.get("/", response_model=List[DocumentList])
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's uploaded documents."""
    
    documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return [DocumentList.from_orm(doc) for doc in documents]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get document details."""
    
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return DocumentResponse.from_orm(document)


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete from S3
    try:
        await s3_service.delete_file(document.s3_key)
    except Exception as e:
        logger.error(f"Failed to delete S3 file: {str(e)}")
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}