from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from app.database import get_db
from app.schemas import QuizCreate, QuizResponse, QuizSubmit, QuizResultResponse
from app.models import Quiz, QuizAttempt, User, LearningPath
from app.utils.auth import get_current_user
from app.services.quiz_service import generate_quiz, evaluate_quiz

router = APIRouter()

@router.get("/learning-path/{path_id}/day/{day}", response_model=Dict)
def get_quiz_for_day(
    path_id: int,
    day: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a quiz for a specific day in a learning path"""
    # Get the learning path
    path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.user_id == current_user.id
    ).first()
    
    if not path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    # Find the day's topic
    day_plan = next((d for d in path.daily_plan if d['day'] == day), None)
    if not day_plan:
        raise HTTPException(status_code=404, detail="Day not found")
    
    # Generate quiz
    quiz_data = generate_quiz(
        topic=day_plan['topic'],
        technology=path.technology,
        difficulty='beginner',
        num_questions=10
    )
    
    # Store quiz in database
    quiz = Quiz(
        topic=day_plan['topic'],
        questions=quiz_data['questions'],
        difficulty=quiz_data['difficulty']
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    return {
        **quiz_data,
        "quiz_id": quiz.id,
        "day": day,
        "learning_path_id": path_id
    }

@router.post("/generate", response_model=Dict)
def create_quiz(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db)
):
    """Generate a quiz for a specific topic"""
    quiz_result = generate_quiz(
        topic=quiz_data.topic,
        technology=quiz_data.topic,
        difficulty=quiz_data.difficulty,
        num_questions=10
    )
    
    quiz = Quiz(
        topic=quiz_data.topic,
        questions=quiz_result['questions'],
        difficulty=quiz_data.difficulty
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    return {
        **quiz_result,
        "quiz_id": quiz.id
    }

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/submit", response_model=Dict)
def submit_quiz(
    submission: QuizSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit quiz answers and get results"""
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Prepare quiz data for evaluation
    quiz_data = {
        'questions': quiz.questions,
        'passing_score': 70
    }
    
    result = evaluate_quiz(quiz_data, submission.answers)
    
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=submission.quiz_id,
        answers=submission.answers,
        score=result["score"],
        weak_areas=result.get("weak_topics", [])
    )
    db.add(attempt)
    db.commit()
    
    return result
