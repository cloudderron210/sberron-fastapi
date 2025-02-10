import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.account import Account
from core.models.currency import Currency
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

async def get_account(num_account:str , db_session: AsyncSession, is_active: bool):
    data = TEST_ACCOUNT_DATA.copy()
    account_data = BaseAccount(**data).model_dump(by_alias=True)
    account_data['num_account'] = num_account
    account_data['is_active'] = is_active
    account_data.pop('bal_num')
    new_account = Account(**account_data)
    

    
    db_session.add(new_account)
    await db_session.commit()
    await db_session.refresh(new_account)
    return new_account


@pytest_asyncio.fixture
async def existing_account(db_session: AsyncSession) -> Account:
    num_account = '12345810444440000002'
    new_account = await get_account(num_account, db_session, is_active=True)
    return new_account


@pytest_asyncio.fixture
async def existing_account_passive(db_session: AsyncSession) -> Account:
    num_account = '12345810444440000001'
    new_account = await get_account(num_account, db_session, is_active=False)
    return new_account


@pytest_asyncio.fixture
async def existing_account_2(db_session: AsyncSession) -> Account:
    num_account = '12345810444440000003'
    new_account = await get_account(num_account, db_session, is_active=True)
    return new_account

    
@pytest_asyncio.fixture
async def existing_account_passive_2(db_session: AsyncSession) -> Account:
    num_account = '12345810444440000004'
    new_account = await get_account(num_account, db_session, is_active=False)
    return new_account
    










    
    
    
