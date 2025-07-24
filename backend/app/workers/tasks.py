import logging
from datetime import datetime
from celery import Task
from app.workers.celery_app import celery_app
from app.core.database import SessionLocal
# Import all models to ensure they're loaded before using relationships
from app.models.user import User  # Import User model first
from app.models.document import Document
from app.models.analysis import Analysis, AnalysisStatus
from app.models.career_recommendation import CareerRecommendation, CareerType
from app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class CallbackTask(Task):
    """Task with database session management."""
    
    def on_success(self, retval, task_id, args, kwargs):
        """Success callback."""
        pass
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Failure callback."""
        logger.error(f"Task {task_id} failed: {str(exc)}")


@celery_app.task(base=CallbackTask, bind=True, max_retries=3)
def process_analysis_task(self, analysis_id: int):
    """Process career analysis asynchronously."""
    
    db = SessionLocal()
    
    try:
        # Get analysis
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            raise ValueError(f"Analysis {analysis_id} not found")
        
        # Update status
        analysis.status = AnalysisStatus.PROCESSING
        db.commit()
        
        start_time = datetime.utcnow()
        
        # Get document
        document = db.query(Document).filter(Document.id == analysis.document_id).first()
        if not document:
            raise ValueError(f"Document {analysis.document_id} not found")
        
        # Call Gemini API (synchronous version for Celery)
        # Create a new instance for each task to avoid connection reuse issues
        gemini_service = GeminiService()
        result = gemini_service.analyze_resume_sync(
            document.raw_text,
            document.document_type.value
        )
        
        # Update analysis with results
        analysis.status = AnalysisStatus.COMPLETED
        analysis.processing_time = (datetime.utcnow() - start_time).total_seconds()
        analysis.gemini_response = result["data"]
        analysis.career_paths = result["data"].get("career_paths", [])
        analysis.skill_gaps = []
        
        # Extract all skill gaps
        all_skill_gaps = set()
        
        # Create career recommendations
        for path in result["data"].get("career_paths", []):
            # Collect skill gaps
            path_skill_gaps = path.get("skill_gaps", [])
            all_skill_gaps.update(path_skill_gaps)
            
            recommendation = CareerRecommendation(
                analysis_id=analysis.id,
                career_type=CareerType(path["type"]),
                title=path["title"],
                description=path["description"],
                required_skills=path.get("required_skills", []),
                skill_match_percentage=path.get("skill_match_percentage", 0),
                skill_gaps=path_skill_gaps,
                salary_range_min=path.get("salary_range", {}).get("min"),
                salary_range_max=path.get("salary_range", {}).get("max"),
                market_demand=path.get("market_demand"),
                confidence_score=path.get("confidence_score", 0.5),
                next_steps=path.get("next_steps", [])
            )
            db.add(recommendation)
        
        # Update overall skill gaps
        analysis.skill_gaps = list(all_skill_gaps)
        
        db.commit()
        
        logger.info(f"Analysis {analysis_id} completed successfully")
        return {"status": "success", "analysis_id": analysis_id}
        
    except Exception as e:
        logger.error(f"Analysis {analysis_id} failed: {str(e)}")
        
        # Update analysis status
        if 'analysis' in locals():
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = str(e)
            db.commit()
        
        # Retry the task
        raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
        
    finally:
        db.close()