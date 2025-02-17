from httpx import AsyncClient
import pytest
from pytest_lazy_fixtures import lf 
from core.models import User
from core.models.client import Client
from tests.helpers import validate_invalid_parameter
from tests.user.fixtures import CLIENT_USER_TEST_DATA, CLIENT_URL


pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_client_created(test_client: AsyncClient):
    data = CLIENT_USER_TEST_DATA.copy()
    response = await test_client.post("/api/v1/user/client/register", json=data)
    assert response.status_code == 201


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_error_code, expected_error_type, expected_error_message, login_input",
    [
        (422, "value_error", "Value error, Invalid login", "1234"),
        (422, "string_too_short", "String should have at least 4 characters", "a" * 3),
        (422, "string_too_long", "String should have at most 20 characters", "a" * 21),
        (404, "invalid credentials", "this login is already in use", lf('existing_client_login'),),
    ],
)
async def test_client_invalid_login(
    expected_error_code: int,
    expected_error_message: str,
    expected_error_type: str,
    login_input: str,
    test_client: AsyncClient,
):
    data = CLIENT_USER_TEST_DATA.copy()

    await validate_invalid_parameter(
        data=data,
        parameter_name="login",
        parameter_value=login_input,
        test_client=test_client,
        method="post",
        url=f'{CLIENT_URL}/register',
        expected_error_message=expected_error_message,
        expected_error_code=expected_error_code,
        expected_error_type=expected_error_type,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_error_code, expected_error_type, expected_error_message, password_input",
    [
        (422, "string_too_short", "String should have at least 6 characters", "A" * 5),
        (422, "string_too_long", "String should have at most 20 characters", "A" * 21),
        (422, "value_error", "must contain at least 1 uppercase", 'cloud210'),
        (422, "value_error", "must contain at least 1 digit", 'Cloudderron'),
    ],
)

@pytest.mark.asyncio
async def test_client_reg_invalid_password(
    expected_error_code: int,
    expected_error_message: str,
    expected_error_type: str,
    password_input: str,
    test_client: AsyncClient,
):

    data = CLIENT_USER_TEST_DATA.copy()

    await validate_invalid_parameter(
        data=data,
        parameter_name="password",
        parameter_value=password_input,
        test_client=test_client,
        method="post",
        url=f'{CLIENT_URL}/register',
        expected_error_message=expected_error_message,
        expected_error_code=expected_error_code,
        expected_error_type=expected_error_type,
    )



@pytest.mark.asyncio
async def test_client_login_invalid_password(existing_client: Client, test_client: AsyncClient):
    data = CLIENT_USER_TEST_DATA.copy()
    
    await validate_invalid_parameter(
        data=data,
        parameter_name="password",
        parameter_value="invalid",
        test_client=test_client,
        method="post",
        url=f'{CLIENT_URL}/login',
        expected_error_message='invalid password',
        expected_error_code=404,
        expected_error_type='invalid credentials'
    )
    

@pytest.mark.asyncio
async def test_client_login_success(existing_client: Client, test_client: AsyncClient):
    data = CLIENT_USER_TEST_DATA.copy()
    response = await test_client.post("/api/v1/user/client/login", json=data)
    assert response.status_code == 200
    
    
    


@pytest.mark.asyncio
async def test_client_reg_missing_fields(test_client: AsyncClient):
    pass


@pytest.mark.asyncio
async def test_client_login_missing_fields(test_client: AsyncClient):
    pass


@pytest.mark.asyncio
async def test_session_rolled_back(test_client: AsyncClient):
    pass
