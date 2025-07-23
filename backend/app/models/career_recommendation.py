from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON, Enum, Float
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base, TimestampMixin


class CareerType(str, enum.Enum):
    CORPORATE = "corporate"  # 企業転職
    FREELANCE = "freelance"  # フリーランス
    ENTREPRENEURSHIP = "entrepreneurship"  # 起業


class CareerRecommendation(Base, TimestampMixin):
    __tablename__ = "career_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    
    # Recommendation details
    career_type = Column(Enum(CareerType), nullable=False)
    title = Column(String, nullable=False)  # Job title or business idea
    description = Column(Text, nullable=False)
    
    # Requirements and gaps
    required_skills = Column(JSON, nullable=False)  # List of required skills
    skill_match_percentage = Column(Float, nullable=False)  # 0-100
    skill_gaps = Column(JSON, nullable=True)  # Skills user needs to acquire
    
    # Market data
    salary_range_min = Column(Integer, nullable=True)  # In JPY
    salary_range_max = Column(Integer, nullable=True)  # In JPY
    market_demand = Column(String, nullable=True)  # High, Medium, Low
    
    # Learning path
    recommended_courses = Column(JSON, nullable=True)  # Course recommendations
    estimated_preparation_time = Column(Integer, nullable=True)  # In weeks
    
    # Additional insights
    pros = Column(JSON, nullable=True)  # List of advantages
    cons = Column(JSON, nullable=True)  # List of challenges
    next_steps = Column(JSON, nullable=True)  # Actionable next steps
    
    # Confidence
    confidence_score = Column(Float, nullable=False)  # 0-1
    
    # Relationships
    analysis = relationship("Analysis", back_populates="career_recommendations")