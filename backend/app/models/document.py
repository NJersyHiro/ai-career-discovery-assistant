from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base, TimestampMixin


class DocumentType(str, enum.Enum):
    RESUME = "resume"  # 履歴書
    CV = "cv"  # 職務経歴書
    SKILL_SHEET = "skill_sheet"
    OTHER = "other"


class DocumentStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class Document(Base, TimestampMixin):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Document info
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, docx, etc.
    document_type = Column(Enum(DocumentType), default=DocumentType.OTHER)
    file_size = Column(Integer, nullable=False)  # in bytes
    s3_key = Column(String, nullable=False)  # S3 object key
    
    # Processing status
    status = Column(Enum(DocumentStatus), default=DocumentStatus.UPLOADED)
    error_message = Column(Text, nullable=True)
    
    # Extracted content
    raw_text = Column(Text, nullable=True)
    structured_data = Column(JSON, nullable=True)  # Parsed resume/CV data
    extracted_skills = Column(JSON, nullable=True)  # List of skills
    
    # Relationships
    user = relationship("User", back_populates="documents")
    analyses = relationship("Analysis", back_populates="document", cascade="all, delete-orphan")