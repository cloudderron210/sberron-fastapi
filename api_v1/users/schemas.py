from datetime import date, datetime
from enum import Enum
import re
from typing import TypeVar
from pydantic import BaseModel, ConfigDict, field_validator, Field

from pydantic.alias_generators import to_camel, to_snake

from api_v1.account.schemas import AccountResponse

class Sex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class Document(str, Enum):
    PASSPORT = 'passport'
    INTERNATIONAL_PASSPORT = 'international passport'


class ValidatorMixin():
    @field_validator('name')
    def validate_name(cls, value):
        if value is None and not re.match(r'\d', value):
            raise ValueError('Invalid name')
        return value
    

    @field_validator('telephone')
    def validate_telephone(cls, value):
        if value is not None and not re.match(r'^\+?\d{1,15}$', value):
            raise ValueError('Invalid telephone format')
        return value
    
    @field_validator('birthday')
    def validate_birthday(cls, value):
        if value > date.today():
            raise ValueError('Birthday cannot be in future')
        return value



class BaseUser(BaseModel):
    
    name: str | None = Field(None, max_length=100)
    telephone: str | None = Field(None, max_length=50)
    surname: str | None = Field(None, max_length=30)
    birthday: date | None = Field(None)
    sex: Sex | None = Field(None)
    document: Document | None = Field(None)
    patronymic: str | None = Field(None) 
    docRequisites: str | None = Field(None)
    docIssuedBy: str | None = Field(None)
    
    model_config = ConfigDict(
        alias_generator=to_snake,
        populate_by_name=True
    )
    
    
class PatchUser(BaseUser, ValidatorMixin):
    pass

class AddUser(BaseModel, ValidatorMixin):
    name: str = Field(..., max_length=100)
    telephone: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=30)
    birthday: date 
    sex: Sex 
    document: Document 
    patronymic: str | None = Field(None, max_length=20) 
    docRequisites: str = Field(..., max_length=100)
    docIssuedBy: str = Field(..., max_length=100)
    
    model_config = ConfigDict(
        alias_generator=to_snake,
        populate_by_name=True
    )
    
class UserResponse(BaseModel):
    id: int
    telephone:str
    name:str
    surname: str
    created_at: datetime
    document: str
    doc_requisites: str
    doc_issued_by: str
    accounts: list[AccountResponse]
    
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )

class UpdateUser(BaseUser):
    pass

class User(BaseUser):
    id:int



