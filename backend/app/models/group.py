"""Group and membership models."""

from datetime import datetime
from uuid import uuid4
from typing import Optional
from sqlmodel import SQLModel, Field


class Group(SQLModel, table=True):
    """Gift sharing group."""
    
    __tablename__ = "groups"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    admin_user_id: str = Field(foreign_key="users.id", index=True)
    status: str = Field(default="active")  # active | closed
    created_at: datetime = Field(default_factory=datetime.utcnow)


class GroupUser(SQLModel, table=True):
    """Group membership."""
    
    __tablename__ = "group_users"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    group_id: str = Field(foreign_key="groups.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    status: str = Field(default="pending")  # pending | accepted | rejected
    joined_at: Optional[datetime] = Field(default=None)
