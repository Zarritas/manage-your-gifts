"""Application configuration settings."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App
    APP_NAME: str = "Gift Sharing App"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production-use-a-real-secret-key"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./gifts.db"
    
    # Email (Resend)
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@example.com"
    
    # OTP Settings
    OTP_EXPIRE_MINUTES: int = 10
    OTP_LENGTH: int = 6
    
    # Session
    SESSION_EXPIRE_HOURS: int = 24 * 7  # 1 week
    
    # Frontend URL (for CORS)
    FRONTEND_URL: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
