from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from core.models.base import Base
from main import app
from core.models import db_helper
import pytest_asyncio



DATABASE_URL = 'sqlite+aiosqlite:///./test.db'


@pytest_asyncio.fixture(scope='function')
async def setup_db():
    async_engine = create_async_engine(DATABASE_URL, connect_args={'check_same_thread': False}) 
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  async_engine
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_engine.dispose()


# @pytest_asyncio.fixture(scope='function')
# async def db_session(setup_db):
#     async_session = AsyncSession(bind=setup_db) 
#     try:
#         yield async_session
#     finally:
#         await async_session.rollback()
#         await async_session.close()
    
@pytest_asyncio.fixture(scope='function')
async def db_session(setup_db):
    async_session = async_sessionmaker(bind=setup_db, expire_on_commit=False) 
    async with async_session() as session:
        yield session
        await session.rollback()
        
    
@pytest_asyncio.fixture(scope='function')
async def test_client(db_session):
    async def override_get_db():
        async with db_session as session:
            yield session
    app.dependency_overrides[db_helper.session_dependency] = override_get_db 
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client: 
        yield client
    app.dependency_overrides.clear()

        


    
        



