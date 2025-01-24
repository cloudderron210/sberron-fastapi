from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, CheckConstraint, Relationship
from sqlalchemy import TIMESTAMP, Column, func, text



class Client(SQLModel, table=True):
    
    __table_args__ = (
        CheckConstraint("sex IN ('male', 'female', 'other')", name="check_sex_valid_values"),
        CheckConstraint("document IN ('passport', 'international passport')", name="check_document_valid_values"),
    )
    
    id: int | None = Field(default=None, primary_key=True)
    telephone: str = Field(max_length=64, unique=True)
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    patronymic: str | None = Field(max_length=100)
    createdAt: datetime = Field(default_factory=datetime.now)
    serviceEndDate: datetime | None = Field()
    birthday: str = Field(max_length=100)
    sex: str = Field(max_length=10)
    document: str = Field(max_length=100)
    docRequisites: str = Field(max_length=100, unique=True)
    docIssuedBy: str = Field(max_length=100)

    accounts: list['Account'] = Relationship(back_populates='owner')
    
class Currency(SQLModel, table=True):
    id: int  = Field(sa_column_kwargs={'autoincrement': False} ,primary_key=True)
    str_code: str= Field(max_length=3)
    name: str = Field(max_length=20)

    accounts: list['Account'] = Relationship(back_populates='currency')

class Account(SQLModel, table=True):

    id: int | None = Field(primary_key=True)
    owner_id: int = Field(foreign_key='client.id')
    numAccount: str = Field(max_length=100)
    currency_id:int = Field(foreign_key='currency.id')
    # dateOpen: datetime = Field(default_factory=datetime.now)
    dateOpen: datetime = Field(sa_column=Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")))
    dateClosed: datetime | None = Field()
    description: str = Field(max_length=100)
    isActive: bool = Field(default=True)  
    status: bool = Field(default=True)  

    owner: Client = Relationship(back_populates='accounts')
    currency: Currency = Relationship(back_populates='accounts')

class MoveMoneyOrder(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    idAccCr: int = Field(foreign_key='account.numAccount')
    idAccDb: int = Field(foreign_key='account.numAccount')
    amount: Decimal = Field(decimal_places=5)
    dateCreated: datetime = Field(sa_column=Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")))
    dateExecuted: datetime | None = Field()
    is_executed: bool = Field()
    description: str = Field()


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    state: bool = Field()
    login: str = Field()
    password: str = Field()
    salt: str = Field()
    date_register: datetime = Field(sa_column=Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")))
    time_last_login: datetime | None = Field()
    last_login_ip: str = Field()

class UserClient(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    id_user: int = Field(foreign_key='user.id')
    id_client: int = Field(foreign_key='client.id')

    # user: User = Relationship(back_populates='userclient')
    # client: Client = Relationship(back_populates='userclient')
    

    
    


    
