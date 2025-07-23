import io
import logging
from typing import Dict, Any, Optional
import PyPDF2
import pdfplumber
from docx import Document as DocxDocument
from app.models.document import DocumentType

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Service for processing uploaded documents (PDF, Word)."""
    
    async def extract_text(self, file_content: bytes, file_type: str) -> str:
        """Extract text from document based on file type."""
        
        if file_type.lower() == 'pdf':
            return await self._extract_pdf_text(file_content)
        elif file_type.lower() in ['docx', 'doc']:
            return await self._extract_docx_text(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    async def _extract_pdf_text(self, file_content: bytes) -> str:
        """Extract text from PDF file."""
        
        text = ""
        
        # Try pdfplumber first (better for Japanese text)
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                logger.info(f"Extracted {len(text)} characters using pdfplumber")
                return text.strip()
        except Exception as e:
            logger.warning(f"pdfplumber failed: {str(e)}, trying PyPDF2")
        
        # Fallback to PyPDF2
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            logger.info(f"Extracted {len(text)} characters using PyPDF2")
            return text.strip()
        except Exception as e:
            logger.error(f"PDF extraction failed: {str(e)}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    async def _extract_docx_text(self, file_content: bytes) -> str:
        """Extract text from DOCX file."""
        
        try:
            doc = DocxDocument(io.BytesIO(file_content))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            # Also extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += "\n" + cell.text
            
            logger.info(f"Extracted {len(text)} characters from DOCX")
            return text.strip()
        except Exception as e:
            logger.error(f"DOCX extraction failed: {str(e)}")
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")
    
    def detect_document_type(self, text: str, filename: str) -> DocumentType:
        """Detect document type based on content and filename."""
        
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        # Check for resume indicators
        resume_indicators = ['履歴書', '氏名', '生年月日', '住所', '学歴', '職歴']
        if any(indicator in text for indicator in resume_indicators) or '履歴書' in filename_lower:
            return DocumentType.RESUME
        
        # Check for CV indicators
        cv_indicators = ['職務経歴書', '職務経歴', '業務内容', 'プロジェクト', '実績', 'スキル']
        if any(indicator in text for indicator in cv_indicators) or '職務経歴' in filename_lower:
            return DocumentType.CV
        
        # Check for skill sheet indicators
        skill_indicators = ['スキルシート', 'skill sheet', '技術スタック', '開発経験']
        if any(indicator in text_lower for indicator in skill_indicators):
            return DocumentType.SKILL_SHEET
        
        return DocumentType.OTHER
    
    def parse_japanese_resume(self, text: str) -> Dict[str, Any]:
        """Parse Japanese resume (履歴書) structure."""
        
        parsed = {
            "personal_info": {},
            "education": [],
            "work_history": [],
            "qualifications": [],
            "other_info": {}
        }
        
        # This is a simplified parser - in production, you'd use more sophisticated NLP
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if '学歴' in line:
                current_section = 'education'
            elif '職歴' in line:
                current_section = 'work_history'
            elif '資格' in line or '免許' in line:
                current_section = 'qualifications'
            elif current_section:
                # Add to appropriate section
                if current_section == 'education':
                    parsed['education'].append(line)
                elif current_section == 'work_history':
                    parsed['work_history'].append(line)
                elif current_section == 'qualifications':
                    parsed['qualifications'].append(line)
        
        return parsed
    
    def parse_japanese_cv(self, text: str) -> Dict[str, Any]:
        """Parse Japanese CV (職務経歴書) structure."""
        
        parsed = {
            "summary": "",
            "work_experience": [],
            "projects": [],
            "skills": [],
            "achievements": []
        }
        
        # This is a simplified parser - in production, you'd use more sophisticated NLP
        # You might want to integrate with Gemini API for better parsing
        
        return parsed


# Singleton instance
document_processor = DocumentProcessor()