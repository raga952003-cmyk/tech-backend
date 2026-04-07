from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, LearningPath
from app.utils.auth import get_current_user
from app.services.interview_service import generate_viva_session

router = APIRouter()

@router.get("/{learning_path_id}/day/{day_number}")
def get_daily_interview(
    learning_path_id: int,
    day_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI interview questions for a specific day
    """
    # Get learning path
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == learning_path_id,
        LearningPath.user_id == current_user.id
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    # Find the day in the daily plan
    day_plan = None
    for day in learning_path.daily_plan:
        if day.get('day') == day_number:
            day_plan = day
            break
    
    if not day_plan:
        raise HTTPException(status_code=404, detail="Day not found")
    
    # Generate viva session
    viva_session = generate_viva_session(
        topic=day_plan.get('topic'),
        technology=learning_path.technology,
        day_number=day_number,
        skill_level=current_user.skill_level
    )
    
    return viva_session
