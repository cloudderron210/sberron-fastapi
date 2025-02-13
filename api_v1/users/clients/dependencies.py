import hashlib
from typing import Annotated
from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from api_v1.users.clients.schemas import AddClient, LoginClient
from core.models.client import Client
from core.models.helper import AsyncSessionDep
from core.helpers import CustomValidationError


async def get_client_dep(login_data: LoginClient,
                         session: AsyncSessionDep) -> Client:

    stmt = select(Client).where(Client.login == login_data.login)
    client = await session.scalar(stmt)
    if not client:
        raise CustomValidationError(
            status_code=404,
            detail="user with this login not found",
            type="invalid credentials",
            loc=["body", "login"],
            input=login_data.login
        )
    
    salt = bytes.fromhex(client.salt)
    combined = login_data.password.encode() + salt
    hash = hashlib.sha512(combined).hexdigest()
    
    if client.password != hash:
        raise CustomValidationError(
            status_code=404,
            detail="invalid password",
            type="invalid credentials",
            loc=["body", "password"],
            input=login_data.password
        )
    return client

ClientValidated = Annotated[Client, Depends(get_client_dep)]
        

async def validate_login(login_data: AddClient,
                         session: AsyncSessionDep) -> AddClient:
    
    stmt = select(Client).where(Client.login == login_data.login)
    client = await session.scalar(stmt)
    if client:
        raise CustomValidationError(
            status_code=404,
            detail="this login is alread in use",
            type="invalid credentials",
            loc=["body", "login"],
            input=login_data.login
        )
    return login_data

AddClientValidated = Annotated[AddClient, Depends(validate_login)]




