from httpx import AsyncClient
import pytest
from api_v1.funds.schemas import MoveMoneyData
from core.models.account import Account
from core.models.client import Client
from tests.helpers import validate_invalid_parameter
from tests.test_engine import test_client
from tests.account.fixtures import existing_account, existing_account_passive
from core.models.money_move_order import MoneyMoveOrder
from tests.funds.fixtures import FUNDS_URL, MOVE_MONEY_DATA_TEMPLATE
import logging
from tests.funds.helpers import move_money


pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_from_passive_to_active_success(
    existing_account: Account,
    existing_account_passive: Account,
    test_client: AsyncClient,
    auth_headers: dict,
    existing_client: Client
):
    response = await move_money(
        strAccDb=existing_account_passive.num_account,
        strAccCr=existing_account.num_account,
        test_client=test_client,
        amount=100,
        headers=auth_headers,
        user=existing_client.user,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_from_active_to_active_success(
    existing_account: Account,
    existing_account_2: Account,
    exs_hundred_rub_passive_to_active: MoneyMoveOrder,
    test_client: AsyncClient,
    auth_headers: dict
):
    response = await move_money(
        strAccDb=existing_account.num_account,
        strAccCr=existing_account_2.num_account,
        test_client=test_client,
        amount=100,
        headers=auth_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_not_enough_funds(
    existing_account: Account,
    existing_account_2: Account,
    exs_hundred_rub_passive_to_active: MoneyMoveOrder,
    test_client: AsyncClient,
    auth_headers: dict
):

    data = MOVE_MONEY_DATA_TEMPLATE.copy()
    data['strAccDb'] = existing_account.num_account
    data['strAccCr'] = existing_account_2.num_account   
    
    await validate_invalid_parameter(
        data = data,
        parameter_name="amount",
        parameter_value=101,
        expected_error_message="insufficient funds",
        test_client=test_client,
        url=f'{FUNDS_URL}/move',
        method='post',
        expected_error_code=422,
        expected_error_type='invalid_amount',
        headers=auth_headers
    )
    
    


@pytest.mark.asyncio
async def test_balance_cannot_be_lower_zero(
    existing_account: Account,
    existing_account_passive_2: Account,
    exs_hundred_rub_passive_to_active: MoneyMoveOrder,
    test_client: AsyncClient,
    auth_headers: dict
):
    """
    Existing order: Passive_1 to Active_1 for 100 rubles -> passive_1 balance is 100, active_1 balance is 100
    trying to perform transfer from account_1 to passive_account_2 (balance=0)
    """

    data = MOVE_MONEY_DATA_TEMPLATE.copy()
    data['strAccDb'] = existing_account.num_account
    data['strAccCr'] = existing_account_passive_2.num_account   
    
    await validate_invalid_parameter(
        data = data,
        parameter_name="amount",
        parameter_value=99,
        expected_error_message="balance cannot be lower than 0",
        test_client=test_client,
        url=f'{FUNDS_URL}/move',
        method='post',
        expected_error_code=422,
        expected_error_type='invalid_amount',
        headers=auth_headers
    )

    
        
