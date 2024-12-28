import re
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query 
import settings
from pydantic import BaseModel, field_validator, validator 
from typing import Annotated, Literal
from sqlmodel import CheckConstraint, SQLModel, create_engine, Session, Field, select
from datetime import datetime
from sql.engine import SessionDep, create_db_and_tables
from sql.models import Client, Currency, Account
from routers.client import client_router




app = FastAPI()
app.include_router(client_router)


@app.on_event('startup')
def on_startup():
    create_db_and_tables()








    
    



