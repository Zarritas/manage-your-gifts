"""Gift management service."""

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Gift, GiftReservation, Group, GroupUser, User


class GiftService:
    """Service for gift operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_group_gifts(self, group_id: str, current_user_id: str) -> list[dict]:
        """
        Get all gifts in a group with visibility rules applied.
        
        CRITICAL: If gift.owner_user_id == current_user, DO NOT show reservation info.
        """
        # Get all gifts with owner info
        result = await self.session.exec(
            select(Gift, User)
            .join(User, Gift.owner_user_id == User.id)
            .where(Gift.group_id == group_id)
            .order_by(Gift.created_at.desc())
        )
        
        gifts = []
        for gift, owner in result.all():
            is_own = gift.owner_user_id == current_user_id
            
            gift_data = {
                "id": gift.id,
                "group_id": gift.group_id,
                "owner_user_id": gift.owner_user_id,
                "owner_email": owner.email,
                "title": gift.title,
                "description": gift.description,
                "image_url": gift.image_url,
                "price": gift.price,
                "link": gift.link,
                "created_at": gift.created_at,
                "is_own": is_own,
            }
            
            # VISIBILITY RULE: Only show reservation info to non-owners
            if not is_own:
                reservation = await self._get_reservation(gift.id)
                if reservation:
                    gift_data["reservation_status"] = reservation.status
                    gift_data["reserved_by_me"] = reservation.reserved_by_user_id == current_user_id
                else:
                    gift_data["reservation_status"] = None
                    gift_data["reserved_by_me"] = False
            else:
                # Owner sees no reservation info at all
                gift_data["reservation_status"] = None
                gift_data["reserved_by_me"] = False
            
            gifts.append(gift_data)
        
        return gifts
    
    async def _get_reservation(self, gift_id: str) -> GiftReservation | None:
        """Get reservation for a gift."""
        result = await self.session.exec(
            select(GiftReservation).where(GiftReservation.gift_id == gift_id)
        )
        return result.first()
    
    async def get_gift(self, gift_id: str) -> Gift | None:
        """Get gift by ID."""
        result = await self.session.exec(
            select(Gift).where(Gift.id == gift_id)
        )
        return result.first()
    
    async def create_gift(
        self,
        group_id: str,
        user_id: str,
        title: str,
        description: str | None,
        image_url: str | None,
        price: float | None,
        link: str | None
    ) -> tuple[bool, str, Gift | None]:
        """
        Create a new gift.
        
        Steps:
        1. Ensure group.status == active
        2. Validate title
        3. Create Gift
        """
        # Get group
        result = await self.session.exec(
            select(Group).where(Group.id == group_id)
        )
        group = result.first()
        
        if not group:
            return False, "Group not found", None
        
        if group.status != "active":
            return False, "Group is closed", None
        
        # Check membership
        membership_result = await self.session.exec(
            select(GroupUser)
            .where(GroupUser.group_id == group_id)
            .where(GroupUser.user_id == user_id)
            .where(GroupUser.status == "accepted")
        )
        if not membership_result.first():
            return False, "Not a member of this group", None
        
        # Validate title
        if not title or not title.strip():
            return False, "Title is required", None
        
        # Create gift
        gift = Gift(
            group_id=group_id,
            owner_user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            image_url=image_url,
            price=price,
            link=link
        )
        self.session.add(gift)
        await self.session.flush()
        
        return True, "Gift created", gift
    
    async def delete_gift(self, gift_id: str, user_id: str) -> tuple[bool, str]:
        """
        Delete a gift.
        
        Steps:
        1. Ensure owner_user_id == current user
        2. Ensure no active GiftReservation exists
        3. Delete Gift
        """
        gift = await self.get_gift(gift_id)
        if not gift:
            return False, "Gift not found"
        
        if gift.owner_user_id != user_id:
            return False, "Not authorized"
        
        # Check for reservation
        reservation = await self._get_reservation(gift_id)
        if reservation:
            return False, "Cannot delete a reserved gift"
        
        await self.session.delete(gift)
        
        return True, "Gift deleted"
