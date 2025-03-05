
from datetime import datetime
from typing import TYPE_CHECKING 
from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.mixins import UserRelationMixin
from .money_move_order import MoneyMoveOrder

from .base import Base

if TYPE_CHECKING:
    from .currency import Currency
    from .user import User

class Account(Base):#, UserRelationMixin):
    __tablename__ = 'accounts'
    
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'))
    num_account: Mapped[str] = mapped_column(String(50))
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_open: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    date_closed: Mapped[datetime | None ]
    description: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] 
    status: Mapped[bool] = mapped_column(default=True)  

    currency: Mapped['Currency'] = relationship(back_populates='accounts')
    
    users: Mapped[list['User']] = relationship(secondary='user_account', back_populates='accounts')
    
    
    
    
    
