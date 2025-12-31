"""Group management service."""

from datetime import datetime
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Group, GroupUser, GiftReservation, Gift


class GroupService:
    """Service for group operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user_groups(self, user_id: str) -> list[dict]:
        """Get all groups where user is a member (accepted)."""
        result = await self.session.exec(
            select(Group, GroupUser)
            .join(GroupUser, Group.id == GroupUser.group_id)
            .where(GroupUser.user_id == user_id)
            .where(GroupUser.status == "accepted")
        )
        
        groups = []
        for group, membership in result.all():
            # Count members
            count_result = await self.session.exec(
                select(func.count(GroupUser.id))
                .where(GroupUser.group_id == group.id)
                .where(GroupUser.status == "accepted")
            )
            member_count = count_result.first() or 0
            
            groups.append({
                "id": group.id,
                "name": group.name,
                "description": group.description,
                "status": group.status,
                "admin_user_id": group.admin_user_id,
                "created_at": group.created_at,
                "member_count": member_count,
                "is_admin": group.admin_user_id == user_id
            })
        
        return groups
    
    async def create_group(self, user_id: str, name: str, description: str | None) -> Group:
        """
        Create a new group.
        
        Steps:
        1. Validate name
        2. Create Group (admin_user_id = current user)
        3. Create GroupUser (status = accepted)
        """
        # Create group
        group = Group(
            name=name.strip(),
            description=description.strip() if description else None,
            admin_user_id=user_id
        )
        self.session.add(group)
        await self.session.flush()
        
        # Add creator as accepted member
        member = GroupUser(
            group_id=group.id,
            user_id=user_id,
            status="accepted",
            joined_at=datetime.utcnow()
        )
        self.session.add(member)
        
        return group
    
    async def get_group(self, group_id: str) -> Group | None:
        """Get group by ID."""
        result = await self.session.exec(
            select(Group).where(Group.id == group_id)
        )
        return result.first()
    
    async def get_group_detail(self, group_id: str, current_user_id: str) -> dict | None:
        """Get group with members."""
        group = await self.get_group(group_id)
        if not group:
            return None
        
        # Get members with user info
        from app.models import User
        result = await self.session.exec(
            select(GroupUser, User)
            .join(User, GroupUser.user_id == User.id)
            .where(GroupUser.group_id == group_id)
        )
        
        members = []
        for gu, user in result.all():
            members.append({
                "id": gu.id,
                "user_id": gu.user_id,
                "email": user.email,
                "status": gu.status,
                "joined_at": gu.joined_at,
                "is_admin": group.admin_user_id == gu.user_id
            })
        
        return {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "status": group.status,
            "admin_user_id": group.admin_user_id,
            "created_at": group.created_at,
            "members": members,
            "is_admin": group.admin_user_id == current_user_id
        }
    
    async def get_membership(self, group_id: str, user_id: str) -> GroupUser | None:
        """Get user's membership in a group."""
        result = await self.session.exec(
            select(GroupUser)
            .where(GroupUser.group_id == group_id)
            .where(GroupUser.user_id == user_id)
        )
        return result.first()
    
    async def join_group(self, group_id: str, user_id: str) -> tuple[bool, str]:
        """
        Request to join a group.
        
        Steps:
        1. Require authentication (done by middleware)
        2. If group.status == closed → error
        3. If GroupUser already exists → redirect
        4. Create GroupUser (status = pending)
        """
        group = await self.get_group(group_id)
        if not group:
            return False, "Group not found"
        
        if group.status == "closed":
            return False, "Group is closed"
        
        # Check existing membership
        existing = await self.get_membership(group_id, user_id)
        if existing:
            if existing.status == "accepted":
                return True, "Already a member"
            elif existing.status == "pending":
                return True, "Request already pending"
            else:  # rejected - allow re-request
                existing.status = "pending"
                self.session.add(existing)
                return True, "Request sent"
        
        # Create pending membership
        member = GroupUser(
            group_id=group_id,
            user_id=user_id,
            status="pending"
        )
        self.session.add(member)
        
        return True, "Request sent"
    
    async def accept_user(self, group_id: str, user_id: str, admin_id: str) -> tuple[bool, str]:
        """
        Accept a pending member.
        
        Steps:
        1. Ensure current user is group admin
        2. Update GroupUser status = accepted
        """
        group = await self.get_group(group_id)
        if not group:
            return False, "Group not found"
        
        if group.admin_user_id != admin_id:
            return False, "Not authorized"
        
        membership = await self.get_membership(group_id, user_id)
        if not membership:
            return False, "User not found"
        
        if membership.status != "pending":
            return False, "User is not pending"
        
        membership.status = "accepted"
        membership.joined_at = datetime.utcnow()
        self.session.add(membership)
        
        return True, "User accepted"
    
    async def reject_user(self, group_id: str, user_id: str, admin_id: str) -> tuple[bool, str]:
        """
        Reject a pending member.
        
        Steps:
        1. Ensure admin
        2. Update GroupUser status = rejected
        """
        group = await self.get_group(group_id)
        if not group:
            return False, "Group not found"
        
        if group.admin_user_id != admin_id:
            return False, "Not authorized"
        
        membership = await self.get_membership(group_id, user_id)
        if not membership:
            return False, "User not found"
        
        membership.status = "rejected"
        self.session.add(membership)
        
        return True, "User rejected"
    
    async def remove_user(self, group_id: str, user_id: str, admin_id: str) -> tuple[bool, str]:
        """
        Remove a member from group.
        
        Steps:
        1. Ensure admin
        2. Delete GroupUser
        3. Delete GiftReservations by that user in the group
        """
        group = await self.get_group(group_id)
        if not group:
            return False, "Group not found"
        
        if group.admin_user_id != admin_id:
            return False, "Not authorized"
        
        if user_id == admin_id:
            return False, "Cannot remove yourself"
        
        membership = await self.get_membership(group_id, user_id)
        if not membership:
            return False, "User not found"
        
        # Delete reservations by this user in this group
        gifts_result = await self.session.exec(
            select(Gift).where(Gift.group_id == group_id)
        )
        gift_ids = [g.id for g in gifts_result.all()]
        
        if gift_ids:
            reservations_result = await self.session.exec(
                select(GiftReservation)
                .where(GiftReservation.gift_id.in_(gift_ids))
                .where(GiftReservation.reserved_by_user_id == user_id)
            )
            for reservation in reservations_result.all():
                await self.session.delete(reservation)
        
        # Delete membership
        await self.session.delete(membership)
        
        return True, "User removed"
    
    async def close_group(self, group_id: str, admin_id: str) -> tuple[bool, str]:
        """
        Close a group.
        
        Steps:
        1. Ensure admin
        2. Update Group status = closed
        3. Disable all write actions
        """
        group = await self.get_group(group_id)
        if not group:
            return False, "Group not found"
        
        if group.admin_user_id != admin_id:
            return False, "Not authorized"
        
        group.status = "closed"
        self.session.add(group)
        
        return True, "Group closed"
