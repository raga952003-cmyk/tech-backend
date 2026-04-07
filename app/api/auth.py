from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from app.database import get_db
from app.schemas import UserCreate, UserLogin, Token, UserResponse
from app.models import User
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.services.email_service import send_password_reset_email
from app.config import settings
import secrets
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        skill_level=user.skill_level
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(request: dict, db: Session = Depends(get_db)):
    """
    Send password reset email
    """
    email = request.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    user = db.query(User).filter(User.email == email).first()
    
    # Always return success to prevent email enumeration
    if not user:
        return {"message": "If the email exists, a password reset link has been sent"}
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    
    db.commit()
    
    # Send reset email
    try:
        if settings.ENABLE_EMAIL_NOTIFICATIONS:
            send_password_reset_email(user.email, user.full_name, reset_token)
            logger.info(f"Password reset email sent to {user.email}")
        else:
            logger.info(f"Password reset requested for {user.email}, but emails are disabled")
            logger.info(f"Reset token: {reset_token}")
    except Exception as e:
        logger.error(f"Failed to send password reset email: {str(e)}")
    
    return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/reset-password")
def reset_password(request: dict, db: Session = Depends(get_db)):
    """
    Reset password using token
    """
    token = request.get("token")
    new_password = request.get("new_password")
    
    if not token or not new_password:
        raise HTTPException(status_code=400, detail="Token and new password are required")
    
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    
    # Find user with this token
    user = db.query(User).filter(User.reset_token == token).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    # Check if token is expired
    if user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reset token has expired")
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    
    db.commit()
    
    logger.info(f"Password reset successful for {user.email}")
    
    return {"message": "Password reset successful"}
