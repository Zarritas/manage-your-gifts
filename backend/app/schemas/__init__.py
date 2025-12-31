"""API request/response schemas."""

from app.schemas.auth import (
    SendCodeRequest,
    SendCodeResponse,
    VerifyCodeRequest,
    VerifyCodeResponse,
    UserResponse,
)
from app.schemas.groups import (
    CreateGroupRequest,
    GroupResponse,
    GroupDetailResponse,
    GroupUserResponse,
)
from app.schemas.gifts import (
    CreateGiftRequest,
    GiftResponse,
    GiftWithReservationResponse,
)
from app.schemas.reservations import (
    ReservationResponse,
)

__all__ = [
    "SendCodeRequest",
    "SendCodeResponse",
    "VerifyCodeRequest",
    "VerifyCodeResponse",
    "UserResponse",
    "CreateGroupRequest",
    "GroupResponse",
    "GroupDetailResponse",
    "GroupUserResponse",
    "CreateGiftRequest",
    "GiftResponse",
    "GiftWithReservationResponse",
    "ReservationResponse",
]
