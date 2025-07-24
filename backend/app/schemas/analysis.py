from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.analysis import AnalysisStatus
from app.models.career_recommendation import CareerType


class AnalysisCreate(BaseModel):
    document_id: int


class AnalysisResponse(BaseModel):
    id: int
    user_id: int
    document_id: int
    status: AnalysisStatus
    created_at: datetime
    updated_at: datetime
    processing_time: Optional[float] = None
    career_paths: Optional[List[Dict[str, Any]]] = None
    skill_gaps: Optional[List[str]] = None
    market_insights: Optional[Dict[str, Any]] = None
    confidence_scores: Optional[Dict[str, float]] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class DocumentInfo(BaseModel):
    filename: str
    document_type: str
    
    class Config:
        from_attributes = True


class AnalysisListResponse(BaseModel):
    id: int
    document_id: int
    status: AnalysisStatus
    created_at: datetime
    processing_time: Optional[float] = None
    document: Optional[DocumentInfo] = None
    career_recommendations: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        from_attributes = True


class CareerPathResponse(BaseModel):
    id: int
    career_type: CareerType
    title: str
    description: str
    required_skills: List[str]
    skill_match_percentage: float
    skill_gaps: Optional[List[str]] = None
    salary_range_min: Optional[int] = None
    salary_range_max: Optional[int] = None
    market_demand: Optional[str] = None
    recommended_courses: Optional[List[Dict[str, Any]]] = None
    estimated_preparation_time: Optional[int] = None
    pros: Optional[List[str]] = None
    cons: Optional[List[str]] = None
    next_steps: Optional[List[str]] = None
    confidence_score: float
    
    class Config:
        from_attributes = True