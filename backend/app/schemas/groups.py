"""Group schemas."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateGroupRequest(BaseModel):
    """Request to create a new group."""
    name: str
    description: Optional[str] = None


class GroupResponse(BaseModel):
    """Basic group data response."""
    id: str
    name: str
    description: Optional[str]
    status: str
    admin_user_id: str
    created_at: datetime
    member_count: int = 0

    class Config:
        from_attributes = True


class GroupUserResponse(BaseModel):
    """Group member data response."""
    id: str
    user_id: str
    email: str
    status: str
    joined_at: Optional[datetime]
    is_admin: bool = False

    class Config:
        from_attributes = True


class GroupDetailResponse(BaseModel):
    """Detailed group data with members."""
    id: str
    name: str
    description: Optional[str]
    status: str
    admin_user_id: str
    created_at: datetime
    members: list[GroupUserResponse]
    is_admin: bool = False

    class Config:
        from_attributes = True
