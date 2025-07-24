import io
import logging
from typing import List, Optional
from PIL import Image
import fitz  # PyMuPDF
from google.cloud import vision
from google.api_core import exceptions as gcp_exceptions
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)


class OCRService:
    """Service for OCR (Optical Character Recognition) of scanned PDFs."""
    
    def __init__(self):
        self.use_cloud_vision = False
        self.vision_client = None
        
        # Try to initialize Google Cloud Vision if credentials are available
        if hasattr(settings, 'GOOGLE_CLOUD_CREDENTIALS_PATH') and settings.GOOGLE_CLOUD_CREDENTIALS_PATH:
            try:
                self.vision_client = vision.ImageAnnotatorClient()
                self.use_cloud_vision = True
                logger.info("Google Cloud Vision API initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize Google Cloud Vision: {str(e)}")
        
        # Initialize Gemini for fallback OCR
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini API initialized for OCR fallback")
    
    async def extract_text_from_image_pdf(self, pdf_content: bytes) -> str:
        """Extract text from image-based PDF using OCR."""
        
        try:
            # Extract images from PDF
            images = self._extract_images_from_pdf(pdf_content)
            
            if not images:
                logger.error("No images found in PDF")
                return ""
            
            logger.info(f"Extracted {len(images)} images from PDF")
            
            # Perform OCR on each image
            all_text = []
            for i, image in enumerate(images):
                logger.info(f"Processing image {i+1}/{len(images)}")
                
                # Try Google Cloud Vision first
                if self.use_cloud_vision:
                    text = await self._ocr_with_cloud_vision(image)
                    if text:
                        all_text.append(text)
                        continue
                
                # Fallback to Gemini Vision
                text = await self._ocr_with_gemini(image)
                if text:
                    all_text.append(text)
            
            combined_text = "\n\n".join(all_text)
            logger.info(f"Total OCR extracted {len(combined_text)} characters")
            
            return combined_text
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return ""
    
    def _extract_images_from_pdf(self, pdf_content: bytes) -> List[bytes]:
        """Extract images from PDF pages."""
        
        images = []
        
        try:
            pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                
                # Convert page to image
                mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                images.append(img_data)
                
                logger.info(f"Converted page {page_num+1} to image ({len(img_data)} bytes)")
            
            pdf_document.close()
            
        except Exception as e:
            logger.error(f"Failed to extract images from PDF: {str(e)}")
        
        return images
    
    async def _ocr_with_cloud_vision(self, image_bytes: bytes) -> Optional[str]:
        """Perform OCR using Google Cloud Vision API."""
        
        if not self.vision_client:
            return None
        
        try:
            image = vision.Image(content=image_bytes)
            
            # Perform OCR with Japanese language hint
            response = self.vision_client.document_text_detection(
                image=image,
                image_context={"language_hints": ["ja", "en"]}
            )
            
            if response.error.message:
                logger.error(f"Cloud Vision API error: {response.error.message}")
                return None
            
            text = response.full_text_annotation.text
            logger.info(f"Cloud Vision extracted {len(text)} characters")
            
            return text
            
        except gcp_exceptions.GoogleAPIError as e:
            logger.error(f"Cloud Vision API error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Cloud Vision OCR failed: {str(e)}")
            return None
    
    async def _ocr_with_gemini(self, image_bytes: bytes) -> Optional[str]:
        """Perform OCR using Gemini Vision API as fallback."""
        
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            prompt = """この画像は日本語の職務経歴書または履歴書のスキャンです。
画像内のすべてのテキストを正確に読み取って、元のフォーマットを保持しながらテキストとして出力してください。
表形式のデータは適切に整形してください。"""
            
            # Send image to Gemini
            response = self.gemini_model.generate_content([prompt, image])
            
            if response.text:
                logger.info(f"Gemini OCR extracted {len(response.text)} characters")
                return response.text
            else:
                logger.warning("Gemini OCR returned empty response")
                return None
                
        except Exception as e:
            logger.error(f"Gemini OCR failed: {str(e)}")
            return None


# Singleton instance
ocr_service = OCRService()