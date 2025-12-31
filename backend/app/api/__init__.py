"""API routes package."""

from app.api.auth import router as auth_router
from app.api.groups import router as groups_router
from app.api.gifts import router as gifts_router
from app.api.reservations import router as reservations_router
from app.api.users import router as users_router
from app.api.websockets import router as websocket_router

__all__ = [
    "auth_router",
    "groups_router",
    "gifts_router",
    "reservations_router",
    "users_router",
    "websocket_router",
]
