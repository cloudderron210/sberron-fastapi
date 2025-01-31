from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from core.models.base import Base

if TYPE_CHECKING:
    from .account import Account

class Currency(Base):
    __tablename__ = 'currencies'
    
    str_code: Mapped[str]
    name: Mapped[str]

    accounts: Mapped[list['Account']] = relationship(back_populates='currency')
