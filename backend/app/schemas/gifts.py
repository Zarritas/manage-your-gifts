"""Gift schemas."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateGiftRequest(BaseModel):
    """Request to create a new gift."""
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    link: Optional[str] = None


class GiftResponse(BaseModel):
    """Basic gift data response (for owner view - no reservation info)."""
    id: str
    group_id: str
    owner_user_id: str
    title: str
    description: Optional[str]
    image_url: Optional[str]
    price: Optional[float]
    link: Optional[str]
    created_at: datetime
    is_own: bool = False

    class Config:
        from_attributes = True


class GiftWithReservationResponse(BaseModel):
    """Gift data with reservation info (for non-owner view)."""
    id: str
    group_id: str
    owner_user_id: str
    owner_email: str
    title: str
    description: Optional[str]
    image_url: Optional[str]
    price: Optional[float]
    link: Optional[str]
    created_at: datetime
    is_own: bool = False
    # Reservation info - ONLY shown to non-owners
    reservation_status: Optional[str] = None  # None = free, "reserved", "purchased"
    reserved_by_me: bool = False

    class Config:
        from_attributes = True
