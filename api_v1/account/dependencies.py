from typing import Annotated
from fastapi import Depends, HTTPException, Path
from core.models.account import Account
from api_v1.account import crud
from core.models.helper import AsyncSessionDep


async def get_account_dep(account_id: Annotated[int, Path],
                         session: AsyncSessionDep) -> Account:
    account = await crud.get_by_id(account_id=account_id, session=session) 
    if account is not None:
        return account 
    else:
        raise HTTPException(404, f'User with id {account_id} not found')

AccountById = Annotated[Account, Depends(get_account_dep)]
        
        
        
    
