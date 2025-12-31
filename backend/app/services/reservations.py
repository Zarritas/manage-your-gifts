"""Gift reservation service."""

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Gift, GiftReservation


class ReservationService:
    """Service for gift reservation operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def _get_gift(self, gift_id: str) -> Gift | None:
        """Get gift by ID."""
        result = await self.session.exec(
            select(Gift).where(Gift.id == gift_id)
        )
        return result.first()
    
    async def _get_reservation(self, gift_id: str) -> GiftReservation | None:
        """Get reservation for a gift."""
        result = await self.session.exec(
            select(GiftReservation).where(GiftReservation.gift_id == gift_id)
        )
        return result.first()
    
    async def reserve_gift(self, gift_id: str, user_id: str) -> tuple[bool, str]:
        """
        Reserve a gift.
        
        Steps:
        1. Ensure current user != gift.owner_user_id
        2. Ensure no active reservation exists
        3. Create GiftReservation (status = reserved)
        """
        gift = await self._get_gift(gift_id)
        if not gift:
            return False, "Gift not found"
        
        if gift.owner_user_id == user_id:
            return False, "Cannot reserve your own gift"
        
        # Check existing reservation
        existing = await self._get_reservation(gift_id)
        if existing:
            return False, "Gift is already reserved"
        
        reservation = GiftReservation(
            gift_id=gift_id,
            reserved_by_user_id=user_id,
            status="reserved"
        )
        self.session.add(reservation)
        
        return True, "Gift reserved"
    
    async def unreserve_gift(self, gift_id: str, user_id: str) -> tuple[bool, str]:
        """
        Cancel a gift reservation.
        
        Steps:
        1. Ensure reserved_by_user_id == current user
        2. Delete GiftReservation
        """
        reservation = await self._get_reservation(gift_id)
        if not reservation:
            return False, "No reservation found"
        
        if reservation.reserved_by_user_id != user_id:
            return False, "Not your reservation"
        
        await self.session.delete(reservation)
        
        return True, "Reservation cancelled"
    
    async def mark_purchased(self, gift_id: str, user_id: str) -> tuple[bool, str]:
        """
        Mark a gift as purchased.
        
        Steps:
        1. Ensure reserved_by_user_id == current user
        2. Update GiftReservation status = purchased
        """
        reservation = await self._get_reservation(gift_id)
        if not reservation:
            return False, "No reservation found"
        
        if reservation.reserved_by_user_id != user_id:
            return False, "Not your reservation"
        
        reservation.status = "purchased"
        self.session.add(reservation)
        
        return True, "Marked as purchased"
