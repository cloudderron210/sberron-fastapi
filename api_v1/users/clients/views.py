from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.account.schemas import AccountResponse
from api_v1.users.clients.schemas import AddClient
from api_v1.users.schemas import AddUser, User, PatchUser, UpdateUser
from api_v1.users.clients import crud
from api_v1.users.dependencies import UserDepId, get_user_dep
from core.models import db_helper
from core.models.helper import AsyncSessionDep

router = APIRouter(tags=['Client'])



@router.post('', status_code=201)
async def add_client(client_data: AddClient, session: AsyncSessionDep):
    return await crud.register_client(client_data,session)
