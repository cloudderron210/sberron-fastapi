from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class UserClient(Base):

    __tablename__ = 'user_client'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
