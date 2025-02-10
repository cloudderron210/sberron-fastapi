from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

if TYPE_CHECKING:
    from .client import Client

class ClientRelationMixin(declared_attr):
    _client_back_populates: str | None = None


    @declared_attr
    def client_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey('clients.id'))

    
    @declared_attr
    def client(cls) -> Mapped['Client']:
        return relationship('Client', back_populates=cls._client_back_populates)
