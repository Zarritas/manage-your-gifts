"""Reservation schemas."""

from pydantic import BaseModel
from datetime import datetime


class ReservationResponse(BaseModel):
    """Reservation data response."""
    id: str
    gift_id: str
    reserved_by_user_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
