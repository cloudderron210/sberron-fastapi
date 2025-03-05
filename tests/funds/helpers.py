import logging
from httpx import AsyncClient
from tests.funds.fixtures import FUNDS_URL, MOVE_MONEY_DATA_TEMPLATE

async def move_money(
    strAccDb: str, strAccCr: str, amount: int, test_client: AsyncClient, headers: dict, user=None
):
    data = MOVE_MONEY_DATA_TEMPLATE.copy()
    data["strAccDb"] = strAccDb
    data["strAccCr"] = strAccCr
    data["amount"] = amount
    logging.error(f'++++++++++++++++++++++++++++++++++{data}')
    logging.error(f'+++++++++++++++USER+++++++++++++++++++{user}')
    response = await test_client.post(url=f"{FUNDS_URL}/move", json=data, headers=headers)
    
    logging.error(f"Response: {response.status_code} - {response.json()}")
    
    return response
