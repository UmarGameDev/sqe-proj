import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.database import get_session
from backend.main import app
from backend.model import Property, table_registry


@pytest.fixture(scope='session')
def engine():
    _engine = create_async_engine('sqlite+aiosqlite:///:memory:', future=True)
    return _engine


@pytest.fixture
async def session(engine):
    TestingAsynSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=True,
        expire_on_commit=False,
        bind=engine,
        class_=AsyncSession,
    )

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

        async with TestingAsynSessionLocal() as session:
            yield session

        await conn.run_sync(table_registry.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def client(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    # FIXED: Use ASGITransport instead of app parameter
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url='http://test'
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def property(session):
    property = Property(
        description='test description',
        number_bedrooms='T0',
        price=456,
        area=456,
        location='test location',
    )

    async with session.begin():
        session.add(property)
        await session.commit()
        session.refresh(property)

    return property