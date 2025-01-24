import re
from fastapi import  APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator 
from sqlmodel import Field, select
from sql.engine import SessionDep
from sql.models import Client

client_router = APIRouter()

class AddClient(BaseModel):
    name: str = Field(..., max_length=100)
    telephone: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=30)
    patronymic: str | None = Field()
    birthday: str | None = Field()
    sex: str = Field(..., regex='^(male|female|other)$')
    document : str = Field(..., regex='^(passport|international passport)$')
    docRequisites: str = Field(..., max_length=100)
    docIssuedBy: str = Field(..., max_length=100)

    @field_validator("telephone")
    def validate_telephone(cls, value):
        if not re.match(r'^\+?\d{1,15}$', value):
            raise ValueError("Invalid telephone format")
        return value


async def add_client_helper(client_data: AddClient, session: SessionDep):

    client_telephone = session.exec(select(Client).where(Client.telephone == client_data.telephone)).first()
    if client_telephone:
        raise HTTPException(400, f'telephone exists')
    
    client_req = session.exec(select(Client).where(Client.docRequisites == client_data.docRequisites)).first()
    if client_req:
        raise HTTPException(400, 'docRequisites exists')
    
    new_client = Client(**client_data.model_dump())
    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    return new_client

@client_router.post('/addclient')
async def add_client(client_data: AddClient, session: SessionDep):

    new_client = await add_client_helper(client_data, session)
    new_client = new_client.model_dump()
    new_client['createdAt'] = new_client['createdAt'].isoformat()

    return JSONResponse({'result': True, 'new_client': new_client}) 
