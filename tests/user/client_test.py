# from tests.user.fixtures import CLIENT_TEST_DATA
from httpx import AsyncClient
import pytest
from core.models import User
from tests.user.fixtures import CLIENT_USER_TEST_DATA


pytest_plugins = ('pytest_asyncio',)





@pytest.mark.asyncio
async def test_client_created(test_client: AsyncClient):
    data = CLIENT_USER_TEST_DATA.copy()
    response = await test_client.post(
        '/api/v1/user/client/register',
        json=data
    )
    assert response.status_code == 201
    

@pytest.mark.asyncio
async def test_client_invalid_name(test_client: AsyncClient):
    pass
            
@pytest.mark.asyncio
async def test_session_rolled_back(test_client: AsyncClient):
    pass









