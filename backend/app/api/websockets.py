"""WebSocket API routes."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from app.websockets import manager
from app.services.auth import AuthService
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from jose import jwt, JWTError
from app.config import get_settings

router = APIRouter(tags=["WebSockets"])
settings = get_settings()

async def get_user_from_token(token: str, session: AsyncSession) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        return user_id
    except JWTError:
        return None

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    session: AsyncSession = Depends(get_session)
):
    user_id = await get_user_from_token(token, session)
    if not user_id:
        await websocket.close(code=4003)
        return

    await manager.connect(websocket, user_id)
    try:
        while True:
            # Keep connection alive, maybe handle heartbeats
            # For this simple app, we just listen (client mainly listens too)
            data = await websocket.receive_text()
            # We can handle ping/pong if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
