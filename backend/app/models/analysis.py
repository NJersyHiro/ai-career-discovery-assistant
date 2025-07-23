from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON, Enum, Float
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base, TimestampMixin


class AnalysisStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Analysis(Base, TimestampMixin):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Analysis metadata
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    error_message = Column(Text, nullable=True)
    processing_time = Column(Float, nullable=True)  # in seconds
    
    # Analysis results
    career_paths = Column(JSON, nullable=True)  # List of recommended career paths
    skill_gaps = Column(JSON, nullable=True)  # Identified skill gaps
    market_insights = Column(JSON, nullable=True)  # Market data and trends
    
    # Gemini API specific
    gemini_prompt = Column(Text, nullable=True)  # Prompt sent to Gemini
    gemini_response = Column(JSON, nullable=True)  # Raw response from Gemini
    
    # Scores and metrics
    confidence_scores = Column(JSON, nullable=True)  # Confidence for each recommendation
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    document = relationship("Document", back_populates="analyses")
    career_recommendations = relationship("CareerRecommendation", back_populates="analysis", cascade="all, delete-orphan")