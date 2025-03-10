from datetime import datetime, timedelta
import hashlib
import logging
import secrets
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from api_v1.users.clients.schemas import AddClient
from api_v1.users.crud import add_user
from core.models import User, Client
from api_v1.users.schemas import AddUser
from core.models.user_client import UserClient
import jwt
from core.config import settings

logger = logging.getLogger("uvicorn.error")
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_hash(paswd: str) -> dict:
    salt = secrets.token_bytes(16)
    combined = paswd.encode() + salt
    hash = hashlib.sha512(combined).hexdigest()
    salt = salt.hex()
    return {"hash": hash, "salt": salt}

async def register_client(client_data: AddClient, session: AsyncSession) -> Client:
    """
    Registers a new client along with a linked user.
    """
    try:
        user_data = AddUser(
            **client_data.model_dump(exclude={"login", "password"}, by_alias=True)
        )
        new_user = await add_user(user_data, session)

        client_dict = client_data.model_dump(
            include={"login", "password"}, by_alias=True
        )
        hash_data = get_hash(client_data.password)

        client_dict["password"] = hash_data["hash"]
        client_dict["salt"] = hash_data["salt"]
        new_client = Client(**client_dict)
        session.add(new_client)
        await session.flush()

        new_user_client = UserClient(user_id=new_user.id, client_id=new_client.id)
        session.add(new_user_client)

        await session.commit()
        await session.refresh(new_client)

        new_client = await(session.scalar(select(Client).options(joinedload(Client.user)).where(Client.id == new_client.id)))
        
        return new_client

    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

    


async def login_client(client: Client, session: AsyncSession) -> dict | None:
    stmt = select(UserClient).where(UserClient.client_id == client.id)
    user_client = await session.scalar(stmt)
    if user_client:
        current_datetime_plus_20 = datetime.now() + timedelta(minutes=20)
        formatted_timestamp = current_datetime_plus_20.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        payload = {
            "idClient": user_client.client_id,
            "idUser": user_client.user_id,
            "permissions": 0,
            "timeExpire": formatted_timestamp,
        }
        token = jwt.encode(
            payload, key=settings.jwt_secret_key, algorithm=settings.jwt_algorith
        )
        
        return {"jwt": token}


async def get_user(id: int, session: AsyncSession):
    stmt = (
        select(User)
        .options(joinedload(User.accounts))
        .where(User.id == id)
    )
    user = await session.scalar(stmt)

    if user:
        return user.accounts
    else:
        return None

    
    





