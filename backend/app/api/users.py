"""Users API routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
import json

from app.database import get_session
from app.schemas.auth import UserResponse
from app.services.auth import AuthService
from app.middleware import get_current_user
from app.models import User

router = APIRouter(prefix="/api/users", tags=["Users"])


class UpdateLanguageRequest(BaseModel):
    language: str


class UpdateStoresRequest(BaseModel):
    stores: list[dict]


@router.patch("/me/language", response_model=UserResponse)
async def update_language(
    request: UpdateLanguageRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update user language preference."""
    auth_service = AuthService(session)
    success = await auth_service.update_user_language(current_user.id, request.language)
    
    if not success:
        raise HTTPException(status_code=400, detail="Invalid language")
    
    # Refetch user
    user = await auth_service.get_user_by_id(current_user.id)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        language=user.language,
        search_stores=json.loads(user.search_stores),
        created_at=user.created_at
    )


@router.patch("/me/stores", response_model=UserResponse)
async def update_search_stores(
    request: UpdateStoresRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update user search stores configuration."""
    auth_service = AuthService(session)
    success = await auth_service.update_user_stores(current_user.id, request.stores)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update stores")
    
    # Refetch user
    user = await auth_service.get_user_by_id(current_user.id)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        language=user.language,
        search_stores=json.loads(user.search_stores),
        created_at=user.created_at
    )
