from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.account.dependencies import AccountById
from api_v1.funds import crud
from api_v1.funds.schemas import MoveMoneyData, MovementResponse
from core.models import db_helper
from core.models.helper import AsyncSessionDep


router = APIRouter(tags=['Funds'])


@router.post('/move', response_model=MovementResponse)
async def move_money(data: MoveMoneyData, session: AsyncSessionDep):
    result = await crud.move_money(data, session)
    return result

    
@router.get('/balance/{account_id}')
async def balance(account: AccountById, session: AsyncSessionDep):
    return await crud.check_balance(account, session)
