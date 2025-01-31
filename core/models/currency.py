



from sqlalchemy.orm import Mapped
from core.models.base import Base


class Currency(Base):
    __tablename__ = 'currencies'
    
    str_code: Mapped[str]
    name: Mapped[str]
