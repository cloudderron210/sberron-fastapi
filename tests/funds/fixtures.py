import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.account import Account
from core.models.money_move_order import MoneyMoveOrder

FUNDS_URL = "/api/v1/funds"


MOVE_MONEY_DATA_TEMPLATE = {
    "strAccDb": "12346810744440000002",
    "strAccCr": "12345810744440000003",
    "amount": 50,
    "execute": True,
    "description": "test",
}


@pytest_asyncio.fixture
async def exs_hundred_rub_passive_to_active(
    existing_account: Account, 
    existing_account_passive: Account, 
    db_session: AsyncSession
):

    data = MOVE_MONEY_DATA_TEMPLATE.copy()
    data["id_acc_cr"] = existing_account.id
    data["id_acc_db"] = existing_account_passive.id
    data["is_executed"] = data.pop("execute")
    data['amount'] = 100
    data.pop("strAccCr")
    data.pop("strAccDb")
    
    new_order = MoneyMoveOrder(**data)
    db_session.add(new_order)
    await db_session.commit()
    await db_session.refresh(new_order)

    return new_order
    
