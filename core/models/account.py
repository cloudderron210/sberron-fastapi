
from datetime import datetime, date
from sqlalchemy import TIMESTAMP, DateTime, func, Column, text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Account(Base):

    owner_id: Mapped[int] = Column(foreign_key='client.id')
    numAccount: Mapped[str] = Field(max_length=100)
    currency_id: Mapped[int] = Field(foreign_key='currency.id')
    dateOpen: Mapped[datetime] = Field(sa_column=Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")))
    dateClosed: datetime | None = Field()
    description: Mapped[str] = Field(max_length=100)
    isActive: Mapped[bool]= Field(default=True)  
    status: Mappped[bool] = Field(default=True)  

    owner: Client = Relationship(back_populates='accounts')
    currency: Currency = Relationship(back_populates='accounts')
    
