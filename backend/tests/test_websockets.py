import pytest
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta
from app.config import get_settings
from app.models import User, Group, GroupUser
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

settings = get_settings()

# Use the SAME test DB URL as conftest to share state
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_gifts.db"
engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

def create_token(user_id: str) -> str:
    """Create a valid JWT token for testing."""
    expire = datetime.utcnow() + timedelta(hours=1)
    data = {"sub": user_id, "exp": expire}
    return jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")

@pytest.mark.asyncio
async def test_websocket_broadcast(client: TestClient, db_session: AsyncSession):
    """
    Test authenticating via WebSocket and receiving a broadcast.
    """
    # 1. Setup Data directly in DB
    # Create User
    user = User(email="ws_test@example.com", language="en")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    user_id = user.id  # Cache ID while fresh
    
    # Create Group
    group = Group(name="WS Test Group", admin_user_id=user_id, status="active")
    db_session.add(group)
    await db_session.commit()
    await db_session.refresh(group)
    group_id = group.id # Cache ID while fresh
    
    # Add User to Group as accepted member
    group_user = GroupUser(
        group_id=group_id, 
        user_id=user_id, 
        status="accepted",
        joined_at=datetime.utcnow()
    )
    db_session.add(group_user)
    await db_session.commit()

    # 2. Connect WebSocket
    token = create_token(user_id)
    
    # Note: TestClient.websocket_connect is a context manager.
    with client.websocket_connect(f"/ws?token={token}") as websocket:
        # Connection established
        
        # 3. Trigger an action that broadcasts
        # We can use the HTTP client to trigger an action, e.g., create a gift.
        
        # Authenticate for HTTP API
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create a new gift via API
        gift_data = {
            "title": "Live Update Gift",
            "description": "Testing WS",
            "link": "http://example.com"
        }
        response = client.post(
            f"/api/groups/{group_id}/gifts",
            json=gift_data,
            headers=headers
        )
        assert response.status_code == 200, f"Response: {response.text}"
        
        # 4. Verify WebSocket received message
        data = websocket.receive_json()
        assert data["type"] == "GIFT_UPDATE"
        assert data["action"] == "created"
        assert data["group_id"] == group_id
