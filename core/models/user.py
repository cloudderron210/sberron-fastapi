from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import TIMESTAMP, ForeignKey, String, sql,  text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base




class User(Base):
    __tablename__ = 'users'

    state: Mapped[bool] = mapped_column(server_default=sql.expression.true())
    login: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] 
    salt: Mapped[str]
    date_register: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    time_last_login: Mapped[datetime | None]
    last_login_ip: Mapped[str]
    
    
    
