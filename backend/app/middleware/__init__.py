"""Authentication middleware."""

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.models import User
from app.services.auth import AuthService

settings = get_settings()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """Get the current authenticated user from JWT token."""
    
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_id(user_id)
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


async def get_optional_user(
    request: Request,
    session: AsyncSession = Depends(get_session)
) -> User | None:
    """Get the current user if authenticated, None otherwise."""
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.split(" ")[1]
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None
    
    auth_service = AuthService(session)
    return await auth_service.get_user_by_id(user_id)
