
from datetime import datetime, date
from typing import TYPE_CHECKING
from sqlalchemy import TIMESTAMP, DateTime, func, Column, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .account import Account

class Client(Base):
    __tablename__ = 'clients'
    
    telephone: Mapped[str]
    name: Mapped[str] 
    surname: Mapped[str] 
    patronymic: Mapped[str | None ]
    createdAt: Mapped[datetime | None] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    serviceEndDate: Mapped[datetime | None ]
    birthday: Mapped[date] 
    sex: Mapped[str] 
    document: Mapped[str] 
    docRequisites: Mapped[str] 
    docIssuedBy: Mapped[str] 

    accounts: Mapped[list['Account']] = relationship(back_populates='client')


