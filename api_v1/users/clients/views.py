from fastapi import  APIRouter

from api_v1.users.clients.dependencies import ClientDataValidated, ClientValidated
from api_v1.users.clients import crud
from api_v1.users.clients.schemas import ClientRegistered, JwtResponse
from core.models.helper import AsyncSessionDep

router = APIRouter(tags=['Client'])



@router.post('/register', status_code=201, response_model=ClientRegistered)
async def add_client(client_data: ClientDataValidated, session: AsyncSessionDep):
    return await crud.register_client(client_data,session)
    

@router.post('/login', response_model=JwtResponse)
async def login_client(client: ClientValidated, session: AsyncSessionDep):
    return await crud.login_client(client, session)


@router.get('/getuser/{id}')
async def get_user(id: int, session: AsyncSessionDep):
    return await crud.get_user(id, session)



