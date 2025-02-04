from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from routers.client import AddClient, add_client_helper
from sql.engine import SessionDep
from sql.models import User
import secrets, hashlib



user_router = APIRouter()

    
class UserModel(BaseModel):
    login: str = Field(..., description="логин")
    password: str = Field(..., description="пароль")
    name: str = Field(..., description="имя")
    telephone: str = Field(..., description="телефон")
    surname: str = Field(..., description="фамилия")
    patronymic: str | None = Field(None, description="отчество, может отсутствовать")
    birthdate: str = Field(..., description='дата рождения в формате "2020-01-02"')
    sex: str = Field(..., description="пол")
    document: str = Field(..., description="тип документа")
    docRequisites: str = Field(..., description="реквизиты документа")
    docIssuedBy: str = Field(..., description="орган, выдавший документ")


def get_hash(paswd: str) -> dict:
    salt = secrets.token_bytes(16)
    combined = paswd.encode() + salt
    hash = hashlib.sha512(combined).hexdigest()
    salt = salt.hex()
    return {'hash': hash, 'salt': salt}

    

@user_router.post('/userRegister')
async def register_user(user_data: UserModel, session: SessionDep):
    u_data = user_data.model_dump()
    hash_data = get_hash(user_data.password)
    u_data['state'] = True
    u_data['salt'] = hash_data['salt']
    u_data['password'] = hash_data['hash']


    try:
        client_data = AddClient(            
            name=user_data.name,
            telephone=user_data.telephone,
            surname=user_data.surname,
            patronymic=user_data.patronymic,
            birthday=user_data.birthdate,
            sex=user_data.sex,
            document=user_data.document,
            docRequisites=user_data.docRequisites,
            docIssuedBy=user_data.docIssuedBy)
        new_client = await add_client_helper(client_data, session)
        
        
        new_user = User(**data)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return JSONResponse({'result': True})
    except Exception as e:
        session.rollback()
        raise HTTPException(400,f'{e}')
    
    
    
    
    




