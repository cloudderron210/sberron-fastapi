from httpx import AsyncClient
import pytest
from core.models import User
from tests.user.fixtures import USER_TEST_DATA

pytest_plugins = ('pytest_asyncio',)
   

@pytest.mark.asyncio
async def test_create_user_success(test_client: AsyncClient):
    data = USER_TEST_DATA.copy()
    response = await test_client.post(
        '/api/v1/user',
        json=data
    )
    assert response.status_code == 200 
    
@pytest.mark.asyncio
async def test_get_users(existing_user: User, test_client: AsyncClient):
    response = await test_client.get(
        '/api/v1/user',
    )
    assert response.status_code == 200 
    assert type(response.json()) == list
    assert response.json() 

@pytest.mark.asyncio
async def test_docrecs_exists_post(existing_user: User, test_client: AsyncClient):
    data = USER_TEST_DATA.copy()
    data['docRequisites'] = existing_user.doc_requisites
    
    response = await test_client.post('/api/v1/user',json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'docRequisites exists'

@pytest.mark.asyncio
async def test_docrecs_exists_patch(existing_user: User, existing_user2: User, test_client: AsyncClient):
    data = {'docRequisites': existing_user.doc_requisites}
    
    response = await test_client.patch(f'/api/v1/user/{existing_user2.id}',json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'docRequisites exists'
    
    
@pytest.mark.asyncio
async def test_telephone_exists_post(existing_user: User, test_client: AsyncClient):
    data = USER_TEST_DATA.copy()
    data['telephone'] = existing_user.telephone
    
    response = await test_client.post('/api/v1/user',json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'telephone exists'

@pytest.mark.asyncio
async def test_telephone_exists_patch(existing_user: User, existing_user2: User, test_client: AsyncClient):
    data = {'telephone': existing_user.telephone}
    
    response = await test_client.patch(f'/api/v1/user/{existing_user2.id}',json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'telephone exists'


@pytest.mark.asyncio
async def test_invalid_birthday_future(test_client: AsyncClient):
    data = USER_TEST_DATA.copy()
    data['birthday'] = '2025-10-10'
    response = await test_client.post('/api/v1/user',json=data)
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
    data = USER_TEST_DATA.copy()
    data["birthday"] = invalid_birthday
    response = await test_client.post('/api/v1/user',json=data)
    validate_birthday(response, expected_error_type, expected_msg)
    
    
@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_birthday, expected_error_type, expected_msg", [
    ("20241010", "date_from_datetime_inexact", "Datetimes provided to dates should have zero time"),
    ("10-10-2024", "date_from_datetime_parsing", "invalid character in year"),
    ("2024", "date_from_datetime_inexact", "Datetimes provided to dates should have zero time"),
    ("2024-10-1", "date_from_datetime_parsing", "Input should be a valid date or datetime, input is too short"),
])
async def test_invalid_birthday_formats_patch(existing_user: User,test_client: AsyncClient, invalid_birthday, expected_error_type, expected_msg):
    data = {'birthday': invalid_birthday}
    response = await test_client.patch(f'/api/v1/user/{existing_user.id}' ,json=data)
    validate_birthday(response, expected_error_type, expected_msg)


def validate_birthday(response, expected_error_type, expected_msg):
    
    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "birthday"]
    assert expected_error_type == error["type"] 
    assert expected_msg in error["msg"]   
    
    
@pytest.mark.asyncio
async def test_invalid_document(test_client: AsyncClient):
    data = USER_TEST_DATA.copy()
    data['document'] = 'wrong_document'
    response = await test_client.post('/api/v1/user',json=data)

    error = response.json()['detail'][0]

    assert error['loc'] == ['body', 'document']
    assert error['type'] == 'enum'
    assert error['msg'] == "Input should be 'passport' or 'international passport'"



