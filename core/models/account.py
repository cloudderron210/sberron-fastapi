
from datetime import datetime, date
from sqlalchemy import TIMESTAMP, DateTime, String, func, Column, text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Account(Base):
    __tablename__ = 'account'
    numAccount: Mapped[str] = mapped_column(String(50))
    dateOpen: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    dateClosed: Mapped[datetime | None ]
    description: Mapped[str] = mapped_column(String(100))
    isActive: Mapped[bool] 
    status: Mapped[bool] = mapped_column(default=True)  
