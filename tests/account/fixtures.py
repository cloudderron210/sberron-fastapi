import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.currency import Currency
from tests.test_engine import setup_db, db_session, test_client


TEST_ACCOUNT_DATA = {
    "clientId": 1,
    "currencId": 810,
    "balNum": "12345",
    "description": "set",
    "isActive": True 
}

TEST_CURRENCY_DATA = {
    "id": 810,
}

@pytest_asyncio.fixture
async def existing_currency(db_session: AsyncSession):
    new_currency = Currency(id=810, str_code='RUB', name='Rubles')
    db_session.add(new_currency)
    await db_session.commit()
    await db_session.refresh(new_currency)
    return new_currency
    
    
