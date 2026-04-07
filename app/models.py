from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    skill_level = Column(String)  # beginner, intermediate, advanced
    created_at = Column(DateTime, default=datetime.utcnow)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    
    learning_paths = relationship("LearningPath", back_populates="user")
    progress = relationship("Progress", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")

class LearningPath(Base):
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    technology = Column(String, nullable=False)
    subtopics = Column(JSON)  # List of subtopics
    daily_plan = Column(JSON)  # Calendar-based daily tasks
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="learning_paths")
    progress = relationship("Progress", back_populates="learning_path")

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    day_number = Column(Integer)
    topic = Column(String)
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime)
    notes = Column(Text)
    
    user = relationship("User", back_populates="progress")
    learning_path = relationship("LearningPath", back_populates="progress")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    questions = Column(JSON)  # List of questions with options
    difficulty = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    answers = Column(JSON)
    score = Column(Float)
    weak_areas = Column(JSON)
    attempted_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="quiz_attempts")
