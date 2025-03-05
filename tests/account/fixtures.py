import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.account.crud import add
from core.models.account import Account
from core.models.currency import Currency
from core.models.user import User
from tests.test_engine import setup_db, db_session, test_client
from api_v1.account.schemas import AddAccount, BaseAccount


TEST_ACCOUNT_DATA = {
    "userId": 1,
    "currencyId": 810,
    "balNum": "12345",
    "description": "set",
    "isActive": True 
}

TEST_CURRENCY_DATA = {
    "id": 810,
}

@pytest_asyncio.fixture
async def existing_currency(db_session: AsyncSession) -> Currency:
    new_currency = Currency(id=810, str_code='RUB', name='Rubles')
    db_session.add(new_currency)
    await db_session.commit()
    await db_session.refresh(new_currency)
    return new_currency

async def create_account(db_session: AsyncSession, is_active: bool, owner: User) -> Account:
    data = TEST_ACCOUNT_DATA.copy()
    data['userId'] = owner.id
    data['isActive'] = is_active
    account_data = AddAccount(**data)
    new_account = await add(account_data, db_session)
    return new_account
    

@pytest_asyncio.fixture
async def existing_account(existing_currency: Currency, existing_user: User, db_session: AsyncSession) -> Account:
    new_account = await create_account(db_session, is_active=True, owner=existing_user)
    return new_account


@pytest_asyncio.fixture
async def existing_account_passive(existing_user: User, db_session: AsyncSession) -> Account:
    new_account = await create_account(db_session, is_active=False, owner=existing_user)
    return new_account


@pytest_asyncio.fixture
async def existing_account_2(existing_user: User, db_session: AsyncSession) -> Account:
    new_account = await create_account(db_session, is_active=True, owner=existing_user)
    return new_account

    
@pytest_asyncio.fixture
async def existing_account_passive_2(existing_user: User, db_session: AsyncSession) -> Account:
    new_account = await create_account(db_session, is_active=False, owner=existing_user)
    return new_account
    
@pytest_asyncio.fixture
async def active_account_for_user1(existing_user: User, db_session: AsyncSession) -> Account:
    new_account = await create_account(db_session, is_active=True, owner=existing_user)
    return new_account

@pytest_asyncio.fixture
async def passive_account_for_user2(existing_currency: Currency, existing_user2: User, db_session: AsyncSession) -> Account:
    new_account = await create_account(db_session, is_active=False, owner=existing_user2)
    return new_account











    
    
    
