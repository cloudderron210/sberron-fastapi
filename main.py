import re
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query 
from sql.engine import SessionDep, create_db_and_tables
# from sql.models import Client, Currency, Account
from routers.client import client_router
from routers.account import account_router
from routers.move_money import money_router
from routers.user import user_router
from client.views import router as client_router
from account.views import router as account_router





app = FastAPI()
app.include_router(client_router)
app.include_router(account_router)
app.include_router(money_router)
app.include_router(user_router)


@app.on_event('startup')
def on_startup():
    create_db_and_tables()




    
    



