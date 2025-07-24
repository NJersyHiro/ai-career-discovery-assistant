from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.config import settings
from app.services.gemini_service import gemini_service
from app.models.document import Document
from app.models.analysis import Analysis, AnalysisStatus
from app.models.career_recommendation import CareerRecommendation, CareerType
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisResponse,
    AnalysisListResponse,
    CareerPathResponse
)
from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.workers.tasks import process_analysis_task
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=AnalysisResponse)
async def create_analysis(
    analysis_data: AnalysisCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new career analysis for a document."""
    
    # Verify document exists and belongs to user
    document = db.query(Document).filter(
        Document.id == analysis_data.document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if not document.raw_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document has no extracted text"
        )
    
    # Create analysis record
    db_analysis = Analysis(
        user_id=current_user.id,
        document_id=document.id,
        status=AnalysisStatus.PENDING
    )
    
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    # Queue Celery task for analysis
    from app.workers.tasks import process_analysis_task
    process_analysis_task.delay(db_analysis.id)
    
    return AnalysisResponse.from_orm(db_analysis)


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analysis details."""
    
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return AnalysisResponse.from_orm(analysis)


@router.get("/", response_model=List[AnalysisListResponse])
async def list_analyses(
    skip: int = 0,
    limit: int = 20,
    document_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's analyses."""
    
    from sqlalchemy.orm import joinedload
    
    query = db.query(Analysis).filter(Analysis.user_id == current_user.id)
    
    if document_id:
        query = query.filter(Analysis.document_id == document_id)
    
    # Join with document and career_recommendations
    analyses = query.options(
        joinedload(Analysis.document),
        joinedload(Analysis.career_recommendations)
    ).order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    
    # Convert to response format with document info
    result = []
    for analysis in analyses:
        analysis_dict = {
            "id": analysis.id,
            "document_id": analysis.document_id,
            "status": analysis.status,
            "created_at": analysis.created_at,
            "processing_time": analysis.processing_time
        }
        
        # Add document info if available
        if analysis.document:
            analysis_dict["document"] = {
                "filename": analysis.document.filename,
                "document_type": analysis.document.document_type
            }
        
        # Add career recommendations if completed
        if analysis.status == AnalysisStatus.COMPLETED and analysis.career_recommendations:
            analysis_dict["career_recommendations"] = [
                {
                    "career_type": rec.career_type.value,
                    "title": rec.title,
                    "skill_match_percentage": rec.skill_match_percentage,
                    "salary_range_min": rec.salary_range_min,
                    "salary_range_max": rec.salary_range_max
                }
                for rec in analysis.career_recommendations
            ]
        
        result.append(AnalysisListResponse(**analysis_dict))
    
    return result


@router.post("/{analysis_id}/process")
async def process_analysis_now(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process analysis immediately (for testing)."""
    
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    if analysis.status != AnalysisStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Analysis is already {analysis.status}"
        )
    
    try:
        # Update status
        analysis.status = AnalysisStatus.PROCESSING
        db.commit()
        
        start_time = datetime.utcnow()
        
        # Get document
        document = db.query(Document).filter(Document.id == analysis.document_id).first()
        
        # Call Gemini API
        result = await gemini_service.analyze_resume(
            document.raw_text,
            document.document_type.value
        )
        
        # Update analysis with results
        analysis.status = AnalysisStatus.COMPLETED
        analysis.processing_time = (datetime.utcnow() - start_time).total_seconds()
        analysis.gemini_response = result["data"]
        analysis.career_paths = result["data"].get("career_paths", [])
        analysis.skill_gaps = result["data"].get("skill_gaps", [])
        
        # Create career recommendations
        for path in result["data"].get("career_paths", []):
            recommendation = CareerRecommendation(
                analysis_id=analysis.id,
                career_type=CareerType(path["type"]),
                title=path["title"],
                description=path["description"],
                required_skills=path.get("required_skills", []),
                skill_match_percentage=path.get("skill_match_percentage", 0),
                skill_gaps=path.get("skill_gaps", []),
                salary_range_min=path.get("salary_range", {}).get("min"),
                salary_range_max=path.get("salary_range", {}).get("max"),
                market_demand=path.get("market_demand"),
                confidence_score=path.get("confidence_score", 0.5),
                next_steps=path.get("next_steps", [])
            )
            db.add(recommendation)
        
        db.commit()
        
        return {"message": "Analysis completed successfully", "analysis_id": analysis.id}
        
    except Exception as e:
        logger.error(f"Analysis processing failed: {str(e)}")
        analysis.status = AnalysisStatus.FAILED
        analysis.error_message = str(e)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/{analysis_id}/career-paths", response_model=List[CareerPathResponse])
async def get_career_paths(
    analysis_id: int,
    career_type: Optional[CareerType] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get career path recommendations from analysis."""
    
    # Verify analysis belongs to user
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    query = db.query(CareerRecommendation).filter(
        CareerRecommendation.analysis_id == analysis_id
    )
    
    if career_type:
        query = query.filter(CareerRecommendation.career_type == career_type)
    
    recommendations = query.all()
    
    return [CareerPathResponse.from_orm(rec) for rec in recommendations]