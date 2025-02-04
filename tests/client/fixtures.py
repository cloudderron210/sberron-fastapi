
from datetime import date
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.client.schemas import AddClient
from tests.test_engine import setup_db, db_session, test_client
from core.models import Client

TEST_DATA ={
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


@pytest_asyncio.fixture
async def existing_client(db_session: AsyncSession):
    
    data = TEST_DATA.copy()
    client_data = AddClient(**data).model_dump(by_alias=True)
    
    client_data['telephone'] = '12345000'
    client_data['doc_requisites'] = '12345000'
    client_data['birthday'] = date.fromisoformat(data['birthday'])
    new_client = Client(**client_data)
    
    db_session.add(new_client)
    await db_session.commit()
    await db_session.refresh(new_client)
    return new_client
        
    
@pytest_asyncio.fixture
async def existing_client2(db_session: AsyncSession):
    
    data = TEST_DATA.copy()
    client_data = AddClient(**data).model_dump(by_alias=True)
    
    client_data['telephone'] = '12345001'
    client_data['doc_requisites'] = '12345001'
    client_data['birthday'] = date.fromisoformat(data['birthday'])
    new_client = Client(**client_data)
    
    db_session.add(new_client)
    await db_session.commit()
    await db_session.refresh(new_client)
    return new_client

