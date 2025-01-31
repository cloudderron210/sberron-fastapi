from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.client.schemas import AddClient, Client, PatchClient, UpdateClient
from api_v1.client import crud
from api_v1.client.dependencies import ClientDepId, get_client_dep
from core.models import db_helper
from core.models.helper import AsyncSessionDep


router = APIRouter(tags=['Client'])


@router.get('', response_model=list[Client])
async def get_client(session: AsyncSessionDep):
    clients = await crud.get_client(session)
    return clients


@router.post('', response_model=Client)
async def add_client(client_data: AddClient, session: AsyncSessionDep):
    return await crud.add_client(client_data, session)

    
@router.get('/{client_id}', response_model=Client)
async def get_client_by_id(client: ClientDepId):
    return client
        
        


@router.put('/{client_id}')
async def put_client(client_update: UpdateClient,
                     client: ClientDepId,
                     session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.update_client(
        session=session, 
        client=client, 
        client_update=client_update)

@router.patch('/{client_id}')
async def patch_client(client_patch: PatchClient, client: ClientDepId, session: AsyncSessionDep):
    return await crud.patch_client(
        session=session, 
        client=client, 
        client_update=client_patch)
        
    
    








    
