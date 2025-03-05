from fastapi import APIRouter, HTTPException, Request, status
import jwt
from api_v1.currencies import crud

from api_v1.currencies.schemas import AddCurrency, CurrencyResponse
from api_v1.dependencies import AuthorisedUser
from api_v1.users.schemas import User
from core.config import settings
from core.models.helper import AsyncSessionDep

router = APIRouter(tags=['Currency'])


@router.get("", response_model=list[CurrencyResponse])
async def get_accounts(authorised_user: AuthorisedUser, session: AsyncSessionDep):
    if authorised_user['permissions'] == 0:
        result = await crud.get_currencies(session)
        return result
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Not allowed')



@router.post("", response_model=CurrencyResponse)
async def add_account(authorised_user: AuthorisedUser, account_data: AddCurrency, session: AsyncSessionDep):
    if authorised_user['permissions'] == 0:
        new_account = await crud.add(account_data, session)
        return new_account 
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Not allowed')

    
