from datetime import datetime
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
import jwt
from core.config import settings

    
async def authorize_jwt(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(401, 'missing Authorization header')

    if not auth_header.startswith('Bearer'):
        raise HTTPException(401, 'invalid Authorization header format')
    token = auth_header.split(' ')[1]
    
    try:
        decoded_token = jwt.decode(token,key=settings.jwt_secret_key, algorithms=['HS256'])
    except jwt.DecodeError:
        raise HTTPException(401, 'invalid token')
        
    time_expire = datetime.strptime(decoded_token.get('timeExpire'), '%Y-%m-%dT%H:%M:%S.%fZ')
    if time_expire < datetime.now():
        raise HTTPException(401, 'Token has expired')
        
    return decoded_token

AuthorisedUser = Annotated[dict, Depends(authorize_jwt)]

async def require_admin(authorised_user: AuthorisedUser):
    if authorised_user["permissions"] != 0:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")
    return authorised_user



