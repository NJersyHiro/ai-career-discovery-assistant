from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.document import DocumentType, DocumentStatus


class DocumentBase(BaseModel):
    filename: str
    file_type: str
    document_type: DocumentType
    file_size: int


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime
    raw_text: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None
    extracted_skills: Optional[List[str]] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class DocumentList(BaseModel):
    id: int
    filename: str
    document_type: DocumentType
    status: DocumentStatus
    created_at: datetime
    file_size: int
    
    class Config:
        from_attributes = True