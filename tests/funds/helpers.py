from httpx import AsyncClient
from tests.funds.fixtures import MOVE_MONEY_DATA_TEMPLATE


async def move_money(
    strAccDb: str, strAccCr: str, amount: int, test_client: AsyncClient
):
    data = MOVE_MONEY_DATA_TEMPLATE.copy()
    data["strAccDb"] = strAccDb
    data["strAccCr"] = strAccCr
    data["amount"] = amount
    response = await test_client.post(url="/api/v1/funds/move", json=data)
    return response
