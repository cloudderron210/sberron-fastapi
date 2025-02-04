from httpx import AsyncClient
import pytest
from core.models.client import Client
from core.models.currency import Currency
from tests.account.fixtures import TEST_ACCOUNT_DATA, existing_currency
from tests.test_engine import setup_db, db_session, test_client
from tests.client.fixtures import existing_client

@pytest.mark.asyncio
async def test_get_accounts(test_client: AsyncClient):
    response = await test_client.get('/api/v1/account')
    assert response.status_code == 200
    assert type(response.json()) == list
    


    
@pytest.mark.asyncio
async def test_add_account(existing_currency: Currency, existing_client: Client, test_client: AsyncClient):
    data = TEST_ACCOUNT_DATA.copy()
    data['clientId'] = existing_client.id
    data['currencyId'] = existing_currency.id
    response = await test_client.post('/api/v1/account', json=data)
    assert response.status_code == 200 
    # assert response.json()['detail'] == []
