from fastapi import  APIRouter, Depends, HTTPException

from api_v1.users.clients.dependencies import ClientValidated
from api_v1.users.clients.schemas import AddClient, LoginClient
from api_v1.users.clients import crud
from core.models.helper import AsyncSessionDep

router = APIRouter(tags=['Client'])



@router.post('/register', status_code=201)
async def add_client(client_data: AddClient, session: AsyncSessionDep):
    return await crud.register_client(client_data,session)
    

    

@router.post('/login')
async def login_client(client: ClientValidated, session: AsyncSessionDep):
    return await crud.login_client(client, session)




