
from datetime import datetime, date
from sqlalchemy import TIMESTAMP, DateTime, String, func, Column, text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Account(Base):
    __tablename__ = 'account'
    pass
    numAccount: Mapped[str] = mapped_column(String(100))
    
