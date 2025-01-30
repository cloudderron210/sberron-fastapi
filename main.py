from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query 
import settings
from sql.engine import SessionDep, create_db_and_tables
from routers.client import client_router
from routers.account import account_router
from routers.move_money import money_router
from routers.user import user_router
from api_v1.client.views import router as client_router
from api_v1.account.views import router as account_router
from api_v1 import router as router_v1
from contextlib import asynccontextmanager
from core.models import Base, db_helper
from core.config import settings





@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    
app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.apiv1_prefix)
# app.include_router(client_router)
# app.include_router(account_router)
# app.include_router(money_router)
# app.include_router(user_router)
    



