from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./techstudy.db"
    SECRET_KEY: str = "your-secret-key-change-in-production-09876543210"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPENAI_API_KEY: Optional[str] = ""
    MISTRAL_API_KEY: Optional[str] = ""
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = ""
    SMTP_PASSWORD: Optional[str] = ""
    SMTP_FROM_EMAIL: Optional[str] = ""
    
    # Email Notification Settings
    DAILY_REMINDER_TIME: str = "09:00"  # Time to send daily reminders (24-hour format)
    ENABLE_EMAIL_NOTIFICATIONS: bool = False  # Set to True to enable emails
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()
