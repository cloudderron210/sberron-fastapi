from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import settings



engine = create_async_engine

