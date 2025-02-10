from typing import Annotated
from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user import User
from api_v1.users import crud
from core.models import db_helper


async def get_user_dep(user_id: Annotated[int, Path],
                         session: AsyncSession = Depends(db_helper.session_dependency)) -> User:
    user = await crud.get_user_by_id(user_id=user_id, session=session) 
    if user is not None:
        return user
    else:
        raise HTTPException(404, f'User with id {user_id} not found')


UserDepId = Annotated[User, Depends(get_user_dep)]
        
        
        
    
