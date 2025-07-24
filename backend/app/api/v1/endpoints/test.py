from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_processor import document_processor
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/test-pdf")
async def test_pdf_extraction(file: UploadFile = File(...)):
    """Test PDF extraction without saving to database"""
    
    try:
        contents = await file.read()
        logger.info(f"Test PDF: {file.filename}, size: {len(contents)} bytes")
        
        file_extension = file.filename.split('.')[-1].lower()
        text = await document_processor.extract_text(contents, file_extension)
        
        return {
            "filename": file.filename,
            "file_size": len(contents),
            "extracted_text_length": len(text),
            "first_500_chars": text[:500] if text else None,
            "success": True
        }
    except Exception as e:
        logger.error(f"Test extraction failed: {str(e)}")
        return {
            "filename": file.filename,
            "file_size": len(contents),
            "error": str(e),
            "success": False
        }