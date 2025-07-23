from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.career_recommendation import CareerRecommendation, CareerType
from app.schemas.analysis import CareerPathResponse

router = APIRouter()


@router.get("/", response_model=List[CareerPathResponse])
async def list_all_career_paths(
    career_type: Optional[CareerType] = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all career paths for the current user across all analyses."""
    
    query = db.query(CareerRecommendation).join(
        CareerRecommendation.analysis
    ).filter(
        CareerRecommendation.analysis.has(user_id=current_user.id)
    )
    
    if career_type:
        query = query.filter(CareerRecommendation.career_type == career_type)
    
    recommendations = query.order_by(
        CareerRecommendation.confidence_score.desc()
    ).offset(skip).limit(limit).all()
    
    return [CareerPathResponse.from_orm(rec) for rec in recommendations]