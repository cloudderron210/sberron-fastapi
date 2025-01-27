from fastapi import  APIRouter
from fastapi.responses import JSONResponse
from sql.engine import SessionDep

from client.schemas import AddClient
from client import crud


router = APIRouter(prefix='/client', tags=['Client'])

@router.post('/add')
async def add_client(client_data: AddClient, session: SessionDep):

    new_client = await crud.add_client(client_data, session)
    new_client = new_client.model_dump()
    new_client['createdAt'] = new_client['createdAt'].isoformat()

    return JSONResponse({'result': True, 'new_client': new_client}) 
