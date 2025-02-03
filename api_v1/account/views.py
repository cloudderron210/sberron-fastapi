from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from api_v1.account import crud
from api_v1.account.schemas import AddAccount
from api_v1.account.dependencies import AccountById

from core.models.helper import AsyncSessionDep

router = APIRouter(tags=['Account'])


@router.get("")
async def get_accounts(session: AsyncSessionDep):
    result = await crud.get_accounts(session)
    return result


@router.get("/{account_id}", )
async def get_accounts_by_id(account: AccountById):
    return account

@router.get("/owner/{account_id}", )
async def get_owner(account_id: int, session: AsyncSessionDep):
    result = await crud.get_owner_by_id(account_id, session)
    return result
                             



@router.post("")
async def add_account(account_data: AddAccount, session: AsyncSessionDep):

    new_account = await crud.add(account_data, session)

    return new_account

# @router.patch('{account_id}')
# async def patch_account(account_data: ,account: AccountById, session: AsyncSessionDep):
#     
    
    
