import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from app.main import app
from app.database import get_session
# Import models to register them with SQLModel metadata
from app.models import User, Group, GroupUser, Gift, GiftReservation, EmailOTP

# Use a test database in shared memory to avoid file locking issues
TEST_DATABASE_URL = "sqlite+aiosqlite:///file:memdb1?mode=memory&cache=shared&uri=true"

engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

async def override_get_session() -> Generator:
    async with AsyncSession(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

# Patch the session maker used by background tasks (like ConnectionManager)
from sqlalchemy.orm import sessionmaker
import app.database as app_db
app_db.async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.fixture(scope="module")
def client(init_db):
    with TestClient(app) as c:
        yield c

@pytest.fixture
async def db_session(init_db):
    async with AsyncSession(engine) as session:
        yield session
