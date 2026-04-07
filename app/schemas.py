from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    skill_level: Optional[str] = "beginner"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    skill_level: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Learning Path schemas
class LearningPathCreate(BaseModel):
    technology: str
    skill_level: str = "beginner"

class LearningPathResponse(BaseModel):
    id: int
    technology: str
    subtopics: List[Dict[str, Any]]
    daily_plan: List[Dict[str, Any]]
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

# Progress schemas
class ProgressUpdate(BaseModel):
    day_number: int
    topic: str
    completed: bool
    notes: Optional[str] = None

class ProgressResponse(BaseModel):
    id: int
    day_number: int
    topic: str
    completed: bool
    completion_date: Optional[datetime]
    
    class Config:
        from_attributes = True

# Quiz schemas
class QuizCreate(BaseModel):
    topic: str
    difficulty: str = "medium"

class QuizResponse(BaseModel):
    id: int
    topic: str
    questions: List[Dict[str, Any]]
    difficulty: str
    
    class Config:
        from_attributes = True

class QuizSubmit(BaseModel):
    quiz_id: int
    answers: Dict[int, int]  # Changed to int for option indices

class QuizResultResponse(BaseModel):
    score: float
    weak_areas: List[str]
    feedback: str
