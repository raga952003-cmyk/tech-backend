from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.schemas import ProgressUpdate, ProgressResponse
from app.models import Progress, User, LearningPath
from app.utils.auth import get_current_user
from app.services.email_service import send_task_completion_email
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=ProgressResponse)
def update_progress(
    progress_data: ProgressUpdate,
    learning_path_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.learning_path_id == learning_path_id,
        Progress.day_number == progress_data.day_number
    ).first()
    
    # Track if this is a new completion
    is_new_completion = False
    
    if progress:
        # Check if this is newly completed
        if not progress.completed and progress_data.completed:
            is_new_completion = True
        
        progress.completed = progress_data.completed
        progress.notes = progress_data.notes
        if progress_data.completed:
            progress.completion_date = datetime.utcnow()
    else:
        is_new_completion = progress_data.completed
        progress = Progress(
            user_id=current_user.id,
            learning_path_id=learning_path_id,
            day_number=progress_data.day_number,
            topic=progress_data.topic,
            completed=progress_data.completed,
            notes=progress_data.notes,
            completion_date=datetime.utcnow() if progress_data.completed else None
        )
        db.add(progress)
    
    db.commit()
    db.refresh(progress)
    
    # Send completion email if enabled and task was just completed
    if is_new_completion and settings.ENABLE_EMAIL_NOTIFICATIONS:
        try:
            # Get learning path details
            learning_path = db.query(LearningPath).filter(
                LearningPath.id == learning_path_id
            ).first()
            
            if learning_path:
                send_task_completion_email(
                    current_user.email,
                    current_user.full_name,
                    progress_data.day_number,
                    progress_data.topic,
                    learning_path.technology
                )
                logger.info(f"Sent completion email to {current_user.email} for Day {progress_data.day_number}")
        except Exception as e:
            logger.error(f"Failed to send completion email: {str(e)}")
            # Don't fail the request if email fails
    
    return progress

@router.get("/{learning_path_id}", response_model=List[ProgressResponse])
def get_progress(
    learning_path_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.learning_path_id == learning_path_id
    ).all()
