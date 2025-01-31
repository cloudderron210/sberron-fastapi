from datetime import date
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, Session, create_engine
from main import app
from sql.engine import get_session
import pytest
from tests.test_engine import setup_db, db_session, test_client
from core.models import Client

pytest_plugins = ('pytest_asyncio',)

    
test_data ={
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
    data = test_data.copy()
    data['telephone'] = '12345000'
    data['docRequisites'] = '12345000'
    
    data['birthday'] = date.fromisoformat(data['birthday'])
    
    new_client = Client(**data)
    
    db_session.add(new_client)
    await db_session.commit()
    await db_session.refresh(new_client)

    return new_client
        

@pytest.mark.asyncio
async def test_create_client_success(test_client: AsyncClient):
    data = test_data.copy()
    response = await test_client.post(
        '/api/v1/client',
        json=data
    )
    assert response.status_code == 200 
    
@pytest.mark.asyncio
async def test_get_clients(existing_client: Client, test_client: AsyncClient):
    response = await test_client.get(
        '/api/v1/client',
    )
    assert response.status_code == 200 
    assert type(response.json()) == list
    assert response.json() 

@pytest.mark.asyncio
async def test_docrecs_exists(existing_client: Client, test_client: AsyncClient, db_session: AsyncSession):
    data = test_data.copy()
    data['docRequisites'] = existing_client.docRequisites
    
    response = await test_client.post('/api/v1/client',json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'docRequisites exists'

@pytest.mark.asyncio
async def test_telephone_exists(existing_client: Client, test_client: AsyncClient, db_session: AsyncSession):
    data = test_data.copy()
    data['telephone'] = existing_client.telephone
    response = await test_client.post('/api/v1/client',json=data.copy())
    assert response.status_code == 400
    assert response.json()['detail'] == 'telephone exists'






