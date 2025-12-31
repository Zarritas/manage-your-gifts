"""Authentication schemas."""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class SendCodeRequest(BaseModel):
    """Request to send OTP code."""
    email: EmailStr


class SendCodeResponse(BaseModel):
    """Response after sending OTP."""
    success: bool
    message: str


class VerifyCodeRequest(BaseModel):
    """Request to verify OTP code."""
    email: EmailStr
    code: str


class VerifyCodeResponse(BaseModel):
    """Response after verifying OTP."""
    success: bool
    message: str
    token: Optional[str] = None


class UserResponse(BaseModel):
    """User data response."""
    id: str
    email: str
    language: str
    search_stores: list[dict]
    created_at: datetime

    class Config:
        from_attributes = True
