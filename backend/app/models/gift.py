"""Gift and reservation models."""

from datetime import datetime
from uuid import uuid4
from typing import Optional
from sqlmodel import SQLModel, Field


class Gift(SQLModel, table=True):
    """Gift wishlist item - immutable after creation."""
    
    __tablename__ = "gifts"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    group_id: str = Field(foreign_key="groups.id", index=True)
    owner_user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    image_url: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None, ge=0)
    link: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class GiftReservation(SQLModel, table=True):
    """Gift reservation by a user."""
    
    __tablename__ = "gift_reservations"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    gift_id: str = Field(foreign_key="gifts.id", unique=True, index=True)
    reserved_by_user_id: str = Field(foreign_key="users.id", index=True)
    status: str = Field(default="reserved")  # reserved | purchased
    created_at: datetime = Field(default_factory=datetime.utcnow)
