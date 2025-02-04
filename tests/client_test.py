from datetime import date
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.client.schemas import AddClient
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
    client_data = AddClient(**test_data).model_dump(by_alias=True)
    
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
    
    data = test_data.copy()
    client_data = AddClient(**test_data).model_dump(by_alias=True)
    
    client_data['telephone'] = '12345001'
    client_data['doc_requisites'] = '12345001'
    client_data['birthday'] = date.fromisoformat(data['birthday'])
    new_client = Client(**client_data)
    
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
async def test_docrecs_exists_post(existing_client: Client, test_client: AsyncClient):
    data = test_data.copy()
    data['docRequisites'] = existing_client.doc_requisites
    
    response = await test_client.post('/api/v1/client',json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'docRequisites exists'

@pytest.mark.asyncio
async def test_docrecs_exists_patch(existing_client: Client, existing_client2: Client, test_client: AsyncClient):
    data = {'docRequisites': existing_client.doc_requisites}
    
    response = await test_client.patch(f'/api/v1/client/{existing_client2.id}',json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'docRequisites exists'
    
    
@pytest.mark.asyncio
async def test_telephone_exists_post(existing_client: Client, test_client: AsyncClient):
    data = test_data.copy()
    data['telephone'] = existing_client.telephone
    
    response = await test_client.post('/api/v1/client',json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'telephone exists'

@pytest.mark.asyncio
async def test_telephone_exists_patch(existing_client: Client, existing_client2: Client, test_client: AsyncClient):
    data = {'telephone': existing_client.telephone}
    
    response = await test_client.patch(f'/api/v1/client/{existing_client2.id}',json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'telephone exists'


@pytest.mark.asyncio
async def test_invalid_birthday_future(test_client: AsyncClient):
    data = test_data.copy()
    data['birthday'] = '2025-10-10'
    response = await test_client.post('/api/v1/client',json=data)
    assert response.status_code == 422
    assert 'Birthday cannot be in future' in response.json()['detail'][0]['msg']
    assert 'value_error' in response.json()['detail'][0]['type']
    assert response.json()['detail'][0]['loc'][0] == 'body'
    assert response.json()['detail'][0]['loc'][1] == 'birthday'

    
@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_birthday, expected_error_type, expected_msg", [
    ("20241010", "date_from_datetime_inexact", "Datetimes provided to dates should have zero time"),
    ("10-10-2024", "date_from_datetime_parsing", "invalid character in year"),
    ("2024", "date_from_datetime_inexact", "Datetimes provided to dates should have zero time"),
    ("2024-10-1", "date_from_datetime_parsing", "Input should be a valid date or datetime, input is too short"),
])
async def test_invalid_birthday_formats_post(test_client: AsyncClient, invalid_birthday, expected_error_type, expected_msg):
    data = test_data.copy()
    data["birthday"] = invalid_birthday
    response = await test_client.post('/api/v1/client',json=data)
    validate_birthday(response, expected_error_type, expected_msg)
    
    
@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_birthday, expected_error_type, expected_msg", [
    ("20241010", "date_from_datetime_inexact", "Datetimes provided to dates should have zero time"),
    ("10-10-2024", "date_from_datetime_parsing", "invalid character in year"),
    ("2024", "date_from_datetime_inexact", "Datetimes provided to dates should have zero time"),
    ("2024-10-1", "date_from_datetime_parsing", "Input should be a valid date or datetime, input is too short"),
])
async def test_invalid_birthday_formats_patch(existing_client: Client,test_client: AsyncClient, invalid_birthday, expected_error_type, expected_msg):
    data = {'birthday': invalid_birthday}
    response = await test_client.patch(f'/api/v1/client/{existing_client.id}' ,json=data)
    validate_birthday(response, expected_error_type, expected_msg)


    
    

def validate_birthday(response, expected_error_type, expected_msg):
    
    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "birthday"]
    assert expected_error_type == error["type"] 
    assert expected_msg in error["msg"]   
    

    
    
@pytest.mark.asyncio
async def test_invalid_document(test_client: AsyncClient):
    data = test_data.copy()
    data['document'] = 'wrong_document'
    response = await test_client.post('/api/v1/client',json=data)

    error = response.json()['detail'][0]

    assert error['loc'] == ['body', 'document']
    assert error['type'] == 'enum'
    assert error['msg'] == "Input should be 'passport' or 'international passport'"



