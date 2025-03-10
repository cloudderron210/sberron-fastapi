
from datetime import datetime, date
from typing import TYPE_CHECKING
from sqlalchemy import TIMESTAMP,  text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .account import Account
    from .client import Client

class User(Base):
    __tablename__ = 'users'
    
    telephone: Mapped[str]
    name: Mapped[str] 
    surname: Mapped[str] 
    patronymic: Mapped[str | None ]
    created_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    service_end_date: Mapped[datetime | None ]
    birthday: Mapped[date] 
    sex: Mapped[str] 
    document: Mapped[str] 
    doc_requisites: Mapped[str] 
    doc_issued_by: Mapped[str] 

    
    client: Mapped['Client'] = relationship(secondary='user_client',back_populates='user')
    
    accounts: Mapped[list['Account']] = relationship(secondary='user_account', back_populates='users')

    
