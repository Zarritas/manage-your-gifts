"""Reservations API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.services.reservations import ReservationService
from app.services.gifts import GiftService
from app.middleware import get_current_user
from app.models import User

from app.websockets import manager

router = APIRouter(prefix="/api/gifts", tags=["Reservations"])


@router.post("/{gift_id}/reserve")
async def reserve_gift(
    gift_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Reserve a gift."""
    reservation_service = ReservationService(session)
    success, message = await reservation_service.reserve_gift(gift_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # Broadcast update
    gift_service = GiftService(session)
    gift = await gift_service.get_gift(gift_id)
    if gift:
        await manager.broadcast_to_group(
            gift.group_id,
            {
                "type": "GIFT_UPDATE", 
                "gift_id": gift_id, 
                "action": "reserved",
                "group_id": gift.group_id
            }
        )
    
    return {"success": True, "message": message}


@router.delete("/{gift_id}/reserve")
async def unreserve_gift(
    gift_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Cancel a gift reservation."""
    reservation_service = ReservationService(session)
    success, message = await reservation_service.unreserve_gift(gift_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # Broadcast update
    gift_service = GiftService(session)
    gift = await gift_service.get_gift(gift_id)
    if gift:
        await manager.broadcast_to_group(
            gift.group_id,
            {
                "type": "GIFT_UPDATE", 
                "gift_id": gift_id, 
                "action": "unreserved",
                "group_id": gift.group_id
            }
        )
    
    return {"success": True, "message": message}


@router.post("/{gift_id}/purchased")
async def mark_gift_purchased(
    gift_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Mark a gift as purchased."""
    reservation_service = ReservationService(session)
    success, message = await reservation_service.mark_purchased(gift_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # Broadcast update
    gift_service = GiftService(session)
    gift = await gift_service.get_gift(gift_id)
    if gift:
        await manager.broadcast_to_group(
            gift.group_id,
            {
                "type": "GIFT_UPDATE", 
                "gift_id": gift_id, 
                "action": "purchased",
                "group_id": gift.group_id
            }
        )
    
    return {"success": True, "message": message}
