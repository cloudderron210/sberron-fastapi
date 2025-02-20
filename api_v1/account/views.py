from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from api_v1.account import crud
from api_v1.account.schemas import AccountResponse, AddAccount
from api_v1.account.dependencies import AccountById

from api_v1.dependencies import AuthorisedUser, require_admin
from api_v1.users.schemas import User
from core.models.helper import AsyncSessionDep

router = APIRouter(tags=["Account"])


@router.get("", response_model=list[AccountResponse])
async def get_accounts(session: AsyncSessionDep, authorised_user: AuthorisedUser):
    authorised_user = await require_admin(authorised_user)
    result = await crud.get_accounts(session)
    return result


@router.get("/{account_id}", response_model=AccountResponse)
async def get_accounts_by_id(authorised_user: AuthorisedUser, account: AccountById):
    authorised_user = await require_admin(authorised_user)
    return account


@router.get("/owner/{account_id}", response_model=User)
async def get_owner(
    authorised_user: AuthorisedUser, account_id: int, session: AsyncSessionDep
):
    if authorised_user["permissions"] == 0:
        result = await crud.get_owner_by_id(account_id, session)
        return result
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")


@router.post("", response_model=AccountResponse)
async def add_account(
    authorised_user: AuthorisedUser, account_data: AddAccount, session: AsyncSessionDep
):
    if authorised_user["permissions"] == 0:
        new_account = await crud.add(account_data, session)
        return new_account
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")
