import hashlib
import secrets
from fastapi import HTTPException
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select
from api_v1.users.clients.schemas import AddClient
from api_v1.users.crud import add_user
from core.models import User, Client
from api_v1.users.schemas import AddUser, PatchUser, UpdateUser
from core.models.user_client import UserClient


def get_hash(paswd: str) -> dict:
    salt = secrets.token_bytes(16)
    combined = paswd.encode() + salt
    hash = hashlib.sha512(combined).hexdigest()
    salt = salt.hex()
    return {'hash': hash, 'salt': salt}

async def register_client(client_data: AddClient, session: AsyncSession):

    try:
        user_data = AddUser(**client_data.model_dump(exclude={'login', 'password'}, by_alias=True))
        new_user = await add_user(user_data, session)
        
        client_dict= client_data.model_dump(include={'login', 'password'}, by_alias=True)
        hash_data = get_hash(client_data.password)
        client_dict['password'] = hash_data['hash']
        client_dict['salt'] = hash_data['salt']
        new_client = Client(**client_dict)
        session.add(new_client)
        await session.commit()
        await session.refresh(new_client)

        new_user_client = UserClient(user_id=new_user.id, client_id=new_client.id)
        session.add(new_user_client)
        await session.commit()
        await session.refresh(new_user_client)
        
        return {'message': 'Client created successfully'}
        
    except Exception as e:
        await session.rollback()
        raise e
    
    
    
    
