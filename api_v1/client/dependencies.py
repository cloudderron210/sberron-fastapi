from typing import Annotated
from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.client import Client
from api_v1.client import crud
from core.models import db_helper


async def get_client_dep(client_id: Annotated[int, Path],
                         session: AsyncSession = Depends(db_helper.session_dependency)) -> Client:
    client = await crud.get_client_by_id(client_id=client_id, session=session) 
    if client is not None:
        return client
    else:
        raise HTTPException(404, f'Client with id {client_id} not found')


ClientDepId = Annotated[Client, Depends(get_client_dep)]
        
        
        
    
