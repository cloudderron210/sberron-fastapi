from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

if TYPE_CHECKING:
    from .account import Account

class Currency(Base):
    __tablename__ = 'currencies'
    
    id: Mapped[int] = mapped_column(autoincrement=False ,primary_key=True) 
    str_code: Mapped[str]
    name: Mapped[str]

    accounts: Mapped[list['Account']] = relationship(back_populates='currency')
