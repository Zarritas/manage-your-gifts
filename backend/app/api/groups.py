"""Groups API routes."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.schemas.groups import (
    CreateGroupRequest,
    GroupResponse,
    GroupDetailResponse,
)
from app.services.groups import GroupService
from app.middleware import get_current_user
from app.models import User
from app.websockets import manager

router = APIRouter(prefix="/api/groups", tags=["Groups"])


@router.get("", response_model=list[GroupResponse])
async def list_groups(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """List all groups the user is a member of."""
    group_service = GroupService(session)
    groups = await group_service.get_user_groups(current_user.id)
    return groups


@router.post("", response_model=GroupResponse)
async def create_group(
    request: CreateGroupRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new group."""
    group_service = GroupService(session)
    group = await group_service.create_group(
        current_user.id,
        request.name,
        request.description
    )
    
    return GroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        status=group.status,
        admin_user_id=group.admin_user_id,
        created_at=group.created_at,
        member_count=1
    )


@router.get("/{group_id}", response_model=GroupDetailResponse)
async def get_group(
    group_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get group details with members."""
    group_service = GroupService(session)
    
    # Check membership
    membership = await group_service.get_membership(group_id, current_user.id)
    if not membership or membership.status != "accepted":
        raise HTTPException(status_code=403, detail="Not a member of this group")
    
    group = await group_service.get_group_detail(group_id, current_user.id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return group


@router.post("/{group_id}/join")
async def join_group(
    group_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Request to join a group."""
    group_service = GroupService(session)
    success, message = await group_service.join_group(group_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # Broadcast to group (so admin sees pending request)
    background_tasks.add_task(
        manager.broadcast_to_group,
        group_id,
        {
            "type": "MEMBER_UPDATE", 
            "group_id": group_id, 
            "action": "join_request",
            "user_id": current_user.id
        }
    )

    return {"success": True, "message": message}


@router.post("/{group_id}/members/{user_id}/accept")
async def accept_member(
    group_id: str,
    user_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Accept a pending member."""
    group_service = GroupService(session)
    success, message = await group_service.accept_user(group_id, user_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # Broadcast to group
    background_tasks.add_task(
        manager.broadcast_to_group,
        group_id,
        {
            "type": "MEMBER_UPDATE", 
            "group_id": group_id, 
            "action": "accepted",
            "user_id": user_id
        }
    )
    
    return {"success": True, "message": message}


@router.post("/{group_id}/members/{user_id}/reject")
async def reject_member(
    group_id: str,
    user_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Reject a pending member."""
    group_service = GroupService(session)
    success, message = await group_service.reject_user(group_id, user_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # Broadcast to group
    background_tasks.add_task(
        manager.broadcast_to_group,
        group_id,
        {
            "type": "MEMBER_UPDATE", 
            "group_id": group_id, 
            "action": "rejected",
            "user_id": user_id
        }
    )
    
    return {"success": True, "message": message}


@router.delete("/{group_id}/members/{user_id}")
async def remove_member(
    group_id: str,
    user_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Remove a member from the group."""
    group_service = GroupService(session)
    success, message = await group_service.remove_user(group_id, user_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # Broadcast to group
    background_tasks.add_task(
        manager.broadcast_to_group,
        group_id,
        {
            "type": "MEMBER_UPDATE", 
            "group_id": group_id, 
            "action": "removed",
            "user_id": user_id
        }
    )
    
    return {"success": True, "message": message}


@router.post("/{group_id}/close")
async def close_group(
    group_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Close a group (admin only)."""
    group_service = GroupService(session)
    success, message = await group_service.close_group(group_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"success": True, "message": message}
