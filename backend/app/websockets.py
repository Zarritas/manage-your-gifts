"""WebSocket connection manager."""

from typing import Dict, List
from fastapi import WebSocket
from app.services.groups import GroupService
from app.database import async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# Separate session maker for WebSocket events (since they happen outside request scope sometimes)
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class ConnectionManager:
    """Manages WebSocket connections and broadcasting."""
    
    def __init__(self):
        # Map user_id -> Active WebSocket connection
        # Note: A user might have multiple tabs open, so this should ideally be List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    # Connection might be dead
                    pass

    async def broadcast_to_group(self, group_id: str, message: dict, exclude_user_id: str = None, session: AsyncSession = None):
        """
        Broadcast message to all accepted members of a group.
        Currently simple implementation - triggers a re-fetch on frontend.
        """
        print(f"DEBUG: Broadcasting to group {group_id}")
        
        if session:
            await self._broadcast_with_session(session, group_id, message, exclude_user_id)
        else:
            async with async_session_maker() as new_session:
                await self._broadcast_with_session(new_session, group_id, message, exclude_user_id)

    async def _broadcast_with_session(self, session: AsyncSession, group_id: str, message: dict, exclude_user_id: str = None):
        from app.models import GroupUser, Group
        from sqlmodel import select
        
        result = await session.exec(
            select(GroupUser.user_id)
            .where(GroupUser.group_id == group_id)
            .where(GroupUser.status == "accepted")
        )
        member_ids = result.all()
        
        # Also notify admin if not in list (though admin should be member)
        group = await session.get(Group, group_id)
        if group and group.admin_user_id not in member_ids:
                # Cast result to list to modify it
                member_ids = list(member_ids)
                member_ids.append(group.admin_user_id)

        for user_id in member_ids:
            if exclude_user_id and user_id == exclude_user_id:
                continue
            await self.send_personal_message(message, user_id)

manager = ConnectionManager()
