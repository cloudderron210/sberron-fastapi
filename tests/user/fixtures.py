
from datetime import date
import logging
import random
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.users.clients.crud import login_client, register_client
from api_v1.users.clients.schemas import AddClient
from api_v1.users.crud import add_user
from api_v1.users.schemas import AddUser
from core.models import User
from core.models import Client



USER_TEST_DATA ={
    "name": "lololoshka",
    "surname": "test2name",
    "birthday": "2024-09-16",
    "sex": "male",
    "document": "passport",
    "docRequisites": "12345",
    "docIssuedBy": "1234",
    "telephone": "+12345", 
    "patronymic": "666",
    "serviceEndDate": None
    }



CLIENT_USER_TEST_DATA = {
    "login": "testlogin",
     "password": "Testpassword210",
     **USER_TEST_DATA
}
USER_URL = '/api/v1/user'
CLIENT_URL = f'{USER_URL}/client'

@pytest_asyncio.fixture
async def test_jwt(existing_client: Client, db_session: AsyncSession) -> str | None:
    result = await login_client(existing_client, db_session)
    if result:
        return result['jwt']
    else:
        return

@pytest_asyncio.fixture
async def auth_headers(test_jwt: str) -> dict:
    headers = {
        'Authorization': f'Bearer {test_jwt}'
    }
    return headers

@pytest_asyncio.fixture
async def test_jwt_user2(existing_client: Client, db_session: AsyncSession) -> str | None:
    result = await login_client(existing_client, db_session)
    if result:
        return result['jwt']
    else:
        return

@pytest_asyncio.fixture
async def auth_headers_user2(test_jwt: str) -> dict:
    headers = {
        'Authorization': f'Bearer {test_jwt}'
    }
    return headers

@pytest_asyncio.fixture
async def existing_client(db_session: AsyncSession) -> Client:
    data = CLIENT_USER_TEST_DATA.copy()
    data['telephone'] = '+796012300001'
    data['docRequisites'] = '123400001'
    client_data = AddClient(**data)
    new_client = await register_client(client_data, db_session)
    return new_client

@pytest_asyncio.fixture
async def existing_client_login(existing_client: Client) -> str:
    return existing_client.login

@pytest_asyncio.fixture
async def existing_client2(db_session: AsyncSession) -> Client:
    data = CLIENT_USER_TEST_DATA.copy()
    data['telephone'] = '+796012300002'
    data['docRequisites'] = '123400002'
    client_data = AddClient(**data)
    new_client = await register_client(client_data, db_session) 
    return new_client

@pytest_asyncio.fixture
async def existing_client2_login(existing_client: Client) -> str:
    return existing_client.login

@pytest_asyncio.fixture
async def existing_user(existing_client: Client):
    return existing_client.user

@pytest_asyncio.fixture
async def existing_user2(existing_client2: Client):
    return existing_client2.user


@pytest_asyncio.fixture
async def register_1000_clients(db_session: AsyncSession):
    data = CLIENT_USER_TEST_DATA.copy()
    def generate_unique_numbers(count):
        uniqe_numbers = set()
        while len(uniqe_numbers) < count:
            number = random.randint(10**5, 10**6-1)
            uniqe_numbers.add(number)
        return list(uniqe_numbers)
    
    unique_telephone_numbers = generate_unique_numbers(1000)
    unique_doc_reqs = generate_unique_numbers(1000)
    for i in range(len(unique_telephone_numbers)):
        data['telephone'] = str(unique_telephone_numbers[i])
        data['docRequisites'] = str(unique_doc_reqs[i])
        client_data = AddClient(**data)
        new_client = await register_client(client_data, db_session) 
    return
        
