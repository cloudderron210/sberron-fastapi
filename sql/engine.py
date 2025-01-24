from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
import settings

engine = create_engine(settings.DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
    

# class DatabaseHelper:
#     def __init__(
#         self,
#         url: str,
#         echo: bool = False,
#         echo_pool: bool = False,
#         pool_size: int = 5,
#     ):
#         self.engine = create_engine(
#             url=url,
#             echo=echo,
#             echo_pool=echo_pool,
#             pool_size=pool_size
#         )


        
        
