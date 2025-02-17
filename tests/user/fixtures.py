
from datetime import date
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.users.clients.crud import register_client
from api_v1.users.clients.schemas import AddClient
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
async def existing_client(db_session: AsyncSession) -> Client:
    data = CLIENT_USER_TEST_DATA.copy()
    client_data = AddClient(**data)
    new_client = await register_client(client_data, db_session)
    return new_client
    
@pytest_asyncio.fixture
async def existing_client_login(existing_client: Client) -> str:
    return existing_client.login

    

@pytest_asyncio.fixture
async def existing_user(db_session: AsyncSession):
    
    data = USER_TEST_DATA.copy()
    user_data = AddUser(**data).model_dump(by_alias=True)
    
    user_data['telephone'] = '12345000'
    user_data['doc_requisites'] = '12345000'
    user_data['birthday'] = date.fromisoformat(data['birthday'])
    new_user = User(**user_data)
    
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)
    return new_user
        
    
@pytest_asyncio.fixture
async def existing_user2(db_session: AsyncSession):
    
    data = USER_TEST_DATA.copy()
    user_data = AddUser(**data).model_dump(by_alias=True)
    
    user_data['telephone'] = '12345001'
    user_data['doc_requisites'] = '12345001'
    user_data['birthday'] = date.fromisoformat(data['birthday'])
    new_user = User(**user_data)
    
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)
    return new_user

