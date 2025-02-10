from fastapi import APIRouter
from api_v1.account import crud
from api_v1.account.schemas import  AccountResponse, AddAccount, BaseAccount
from api_v1.account.dependencies import AccountById

from api_v1.client.schemas import Client
from core.models.helper import AsyncSessionDep

router = APIRouter(tags=['Account'])


@router.get("", response_model=list[AccountResponse])
async def get_accounts(session: AsyncSessionDep):
    result = await crud.get_accounts(session)
    return result


@router.get("/{account_id}", response_model=AccountResponse)
async def get_accounts_by_id(account: AccountById):
    return account

@router.get("/owner/{account_id}", response_model=Client)
async def get_owner(account_id: int, session: AsyncSessionDep):
    result = await crud.get_owner_by_id(account_id, session)
    return result



@router.post("", response_model=AccountResponse)
async def add_account(account_data: AddAccount, session: AsyncSessionDep):
    new_account = await crud.add(account_data, session)
    return new_account 

    
