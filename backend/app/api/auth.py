"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.schemas.auth import (
    SendCodeRequest,
    SendCodeResponse,
    VerifyCodeRequest,
    VerifyCodeResponse,
    UserResponse,
)
from app.services.auth import AuthService
from app.middleware import get_current_user
from app.models import User
import json

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/send-code", response_model=SendCodeResponse)
async def send_login_code(
    request: SendCodeRequest,
    session: AsyncSession = Depends(get_session)
):
    """Send OTP code to email."""
    auth_service = AuthService(session)
    success, message = await auth_service.send_login_code(request.email)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return SendCodeResponse(success=True, message=message)


@router.post("/verify-code", response_model=VerifyCodeResponse)
async def verify_login_code(
    request: VerifyCodeRequest,
    session: AsyncSession = Depends(get_session)
):
    """Verify OTP code and return token."""
    auth_service = AuthService(session)
    success, message, token = await auth_service.verify_login_code(
        request.email, request.code
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return VerifyCodeResponse(success=True, message=message, token=token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user info."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        language=current_user.language,
        search_stores=json.loads(current_user.search_stores),
        created_at=current_user.created_at
    )


@router.post("/logout")
async def logout():
    """Logout (client-side token removal)."""
    return {"success": True, "message": "Logged out"}
