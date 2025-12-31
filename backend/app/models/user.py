"""User and authentication models."""

from datetime import datetime
from uuid import uuid4
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """User account model."""
    
    __tablename__ = "users"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    language: str = Field(default="en")  # en | es
    search_stores: str = Field(default="[]")  # JSON array of store configs
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EmailOTP(SQLModel, table=True):
    """Email OTP for passwordless authentication."""
    
    __tablename__ = "email_otps"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    code_hash: str  # Hashed OTP code
    expires_at: datetime
    used: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
