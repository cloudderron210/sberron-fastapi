from typing import Any
from httpx import AsyncClient
import pytest
from core.models.client import Client
from core.models.currency import Currency
from tests.account.fixtures import TEST_ACCOUNT_DATA, existing_currency
from tests.test_engine import setup_db, db_session, test_client
from tests.client.fixtures import existing_client
from tests.helpers import validate_invalid_parameter
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")

ACCOUNT_URL = '/api/v1/account'

@pytest.mark.asyncio
async def test_get_accounts(test_client: AsyncClient):
    response = await test_client.get(ACCOUNT_URL)
    assert response.status_code == 200
    assert type(response.json()) == list


@pytest.mark.asyncio
async def test_add_account(
    existing_currency: Currency, existing_client: Client, test_client: AsyncClient
):
    data = TEST_ACCOUNT_DATA.copy()
    data["clientId"] = existing_client.id
    data["currencyId"] = existing_currency.id
    response = await test_client.post(ACCOUNT_URL, json=data)
    assert response.status_code == 200
    assert response.json()["client_id"] == existing_client.id


@pytest.mark.asyncio
async def test_no_such_currency(
    existing_currency: Currency, existing_client: Client, test_client: AsyncClient
):
    data = TEST_ACCOUNT_DATA.copy()
    data["currencyId"] = "811"
    data["clientId"] = existing_client.id
    await validate_invalid_parameter(
        data = data,
        parameter_name="currencyId",
        parameter_value='811',
        expected_error_message="no such currency",
        test_client=test_client,
        url=ACCOUNT_URL,
        method='post',
        expected_error_code=400
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_error_type, error_message, balNumInput",
    [
        ("string_too_long", "String should have at most 5 characters", "132456"),
        ("string_too_short", "String should have at least 5 characters", "1234"),
        ("string_type", "Input should be a valid string", 12345),
    ],
)
async def test_invalid_balnum(
    existing_currency: Currency,
    existing_client: Client,
    test_client: AsyncClient,
    expected_error_type: str,
    error_message: str,
    balNumInput: Any,
):
    data = TEST_ACCOUNT_DATA.copy()
    data["currencyId"] = existing_currency.id
    data["clientId"] = existing_client.id

    await validate_invalid_parameter(
        data=data,
        parameter_name='balNum',
        parameter_value=balNumInput,
        test_client=test_client,
        method='post',
        url=ACCOUNT_URL,
        expected_error_type=expected_error_type,
        expected_error_message=error_message,
        expected_error_code=422
    )
    
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_error_type, error_message, isActiveValue",
    [
        ("bool_type", "Input should be a valid boolean", None),
        ("bool_parsing", "Input should be a valid boolean, unable to interpret input", ""),
        ("bool_parsing", "Input should be a valid boolean, unable to interpret input", 3), 
    ],
)
async def test_invalid_is_active(
    existing_currency: Currency, 
    existing_client: Client, test_client: AsyncClient,
    expected_error_type: str,
    error_message: str,
    isActiveValue: Any,
    
):
    data = TEST_ACCOUNT_DATA.copy()
    data["currencyId"] = existing_currency.id
    data["clientId"] = existing_client.id

    await validate_invalid_parameter(
        data=data,
        parameter_name='isActive',
        parameter_value=isActiveValue,
        test_client=test_client,
        method='post',
        url='/api/v1/account',
        expected_error_type=expected_error_type,
        expected_error_message=error_message,
        expected_error_code=422
    )












    
    

