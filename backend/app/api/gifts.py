"""Gifts API routes."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.schemas.gifts import CreateGiftRequest, GiftWithReservationResponse
from app.services.gifts import GiftService
from app.services.groups import GroupService
from app.middleware import get_current_user
from app.models import User
from app.websockets import manager

router = APIRouter(prefix="/api", tags=["Gifts"])


@router.get("/groups/{group_id}/gifts", response_model=list[GiftWithReservationResponse])
async def list_gifts(
    group_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """List all gifts in a group with visibility rules applied."""
    group_service = GroupService(session)
    
    # Check membership
    membership = await group_service.get_membership(group_id, current_user.id)
    if not membership or membership.status != "accepted":
        raise HTTPException(status_code=403, detail="Not a member of this group")
    
    gift_service = GiftService(session)
    gifts = await gift_service.get_group_gifts(group_id, current_user.id)
    
    return gifts


@router.post("/groups/{group_id}/gifts", response_model=GiftWithReservationResponse)
async def create_gift(
    group_id: str,
    request: CreateGiftRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new gift."""
    service = GiftService(session)
    success, message, gift = await service.create_gift(
        group_id=group_id,
        user_id=current_user.id,
        title=request.title,
        description=request.description,
        image_url=request.image_url,
        price=request.price,
        link=request.link
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
        
    # Broadcast to group in background
    background_tasks.add_task(
        manager.broadcast_to_group,
        group_id,
        {
            "type": "GIFT_UPDATE", 
            "gift_id": gift.id, 
            "action": "created",
            "group_id": group_id
        }
    )
    
    return GiftWithReservationResponse(
        id=gift.id,
        group_id=gift.group_id,
        owner_user_id=gift.owner_user_id,
        owner_email=current_user.email,
        title=gift.title,
        description=gift.description,
        image_url=gift.image_url,
        price=gift.price,
        link=gift.link,
        created_at=gift.created_at,
        is_own=True,
        reservation_status=None,
        reserved_by_me=False
    )


@router.delete("/groups/{group_id}/gifts/{gift_id}")
async def delete_gift(
    group_id: str,
    gift_id: str,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a gift."""
    gift = await session.get(Gift, gift_id)
    if not gift or gift.group_id != group_id:
        raise HTTPException(status_code=404, detail="Gift not found")
    
    if gift.owner_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this gift")
    
    # Check if there are reservations? Maybe prevent delete? 
    # For now allow delete.
    
    await session.delete(gift)
    await session.commit()
    
    # Broadcast update in background
    background_tasks.add_task(
        manager.broadcast_to_group,
        group_id,
        {
            "type": "GIFT_UPDATE",
            "gift_id": gift_id,
            "action": "deleted",
            "group_id": group_id
        }
    )
    
    return {"success": True, "message": "Gift deleted successfully"}

