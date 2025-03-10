from fastapi import APIRouter, Depends, HTTPException

from api_v1.account.schemas import AccountResponse
from api_v1.users.schemas import AddUser, User, PatchUser, UpdateUser, UserResponse
from api_v1.users import crud
from api_v1.users.dependencies import UserDepId
from api_v1.users.clients.views import router as client_router
from core.models.helper import AsyncSessionDep


router = APIRouter(tags=["User"])


@router.get("", response_model=list[UserResponse])
async def get_user(session: AsyncSessionDep):
    users = await crud.get_user(session)
    return users


@router.post("", response_model=User)
async def add_user(user_data: AddUser, session: AsyncSessionDep):
    return await crud.register_user(user_data, session)


@router.get("/{user_id}/accounts", response_model=list[AccountResponse])
async def get_accounts_by_user_id(user_id: int, session: AsyncSessionDep):
    result = await crud.get_accounts(user_id, session)
    return result

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user: UserDepId):
    return user

@router.put("/{user_id}")
async def put_user(user_update: UpdateUser, user: UserDepId, session: AsyncSessionDep):
    return await crud.update_user(session=session, user=user, user_update=user_update)


@router.patch("/{user_id}")
async def patch_user(user_patch: PatchUser, user: UserDepId, session: AsyncSessionDep):
    return await crud.patch_user(session=session, user=user, user_update=user_patch)
