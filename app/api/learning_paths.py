from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import LearningPathCreate, LearningPathResponse
from app.models import LearningPath, User, Progress
from app.utils.auth import get_current_user
from app.services.llm_service import generate_learning_path

router = APIRouter()

@router.post("/", response_model=LearningPathResponse)
def create_learning_path(
    path_data: LearningPathCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate learning path using LLM
    generated_path = generate_learning_path(path_data.technology, path_data.skill_level)
    
    learning_path = LearningPath(
        user_id=current_user.id,
        technology=path_data.technology,
        subtopics=generated_path["subtopics"],
        daily_plan=generated_path["daily_plan"]
    )
    db.add(learning_path)
    db.commit()
    db.refresh(learning_path)
    return learning_path

@router.get("/", response_model=List[LearningPathResponse])
def get_learning_paths(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(LearningPath).filter(LearningPath.user_id == current_user.id).all()

@router.get("/{path_id}", response_model=LearningPathResponse)
def get_learning_path(
    path_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.user_id == current_user.id
    ).first()
    if not path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return path

@router.delete("/{path_id}")
def delete_learning_path(
    path_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.user_id == current_user.id
    ).first()
    if not path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    # Delete associated progress records
    db.query(Progress).filter(Progress.learning_path_id == path_id).delete()
    
    # Delete the learning path
    db.delete(path)
    db.commit()
    
    return {"message": "Learning path deleted successfully"}
