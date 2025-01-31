
from datetime import datetime
from typing import TYPE_CHECKING 
from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .client import Client
    from .currency import Currency

class Account(Base):
    __tablename__ = 'accounts'
    
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'))
    numAccount: Mapped[str] = mapped_column(String(50))
    dateOpen: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    dateClosed: Mapped[datetime | None ]
    description: Mapped[str] = mapped_column(String(100))
    isActive: Mapped[bool] 
    status: Mapped[bool] = mapped_column(default=True)  

    client: Mapped['Client'] = relationship(back_populates='accounts')
    currency: Mapped['Currency'] = relationship(back_populates='accounts')
