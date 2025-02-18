from fastapi import  APIRouter

from api_v1.account.dependencies import AccountById
from api_v1.dependencies import AuthorisedUser
from api_v1.funds import crud
from api_v1.funds.schemas import BalanceResponse, MoveMoneyData, MovementResponse
from core.models.helper import AsyncSessionDep


router = APIRouter(tags=['Funds'])


@router.post('/move', response_model=MovementResponse)
async def move_money(user_validated:AuthorisedUser, data: MoveMoneyData, session: AsyncSessionDep):
    result = await crud.move_money(user_validated ,data , session)
    return result

    
@router.get('/balance/{account_id}', response_model=BalanceResponse)
async def balance(account: AccountById, session: AsyncSessionDep):
    return await crud.check_balance(account, session)
