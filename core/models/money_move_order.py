from datetime import datetime
from decimal import Decimal
from sqlalchemy import DECIMAL, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING 

from .base import Base

if TYPE_CHECKING:
    from .account import Account


class MoneyMoveOrder(Base):
    __tablename__= 'money_move_orders'

    id_acc_cr: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    id_acc_db: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    amount: Mapped[float] = mapped_column(DECIMAL(10,2))
    date_created: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    date_executed: Mapped[datetime|None] = mapped_column(nullable=True)
    is_executed: Mapped[bool] = mapped_column()
    description: Mapped[str] = mapped_column(String(100))
    
    # credit_account: Mapped['Account'] = relationship(back_populates='credit_orders')
    # debet_account: Mapped['Account'] = relationship(back_populates='debet_orders')
    

    
    
       
