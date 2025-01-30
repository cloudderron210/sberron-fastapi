from datetime import date, datetime
from enum import Enum
import re
from typing import TypeVar
from pydantic import BaseModel, ConfigDict, field_validator, Field


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



class BaseClient(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str | None = Field(None, max_length=100)
    telephone: str | None = Field(None, max_length=50)
    surname: str | None = Field(None, max_length=30)
    birthday: date | None
    sex: Sex | None 
    document: Document | None 
    patronymic: str | None 
    docRequisites: str | None = Field(None)
    docIssuedBy: str | None = Field(None)
    
class PatchClient(BaseClient):
    pass

class AddClient(BaseModel, ValidatorMixin):
    name: str = Field(..., max_length=100)
    telephone: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=30)
    birthday: date 
    sex: Sex 
    document: Document 
    patronymic: str | None 
    docRequisites: str = Field(..., max_length=100)
    docIssuedBy: str = Field(..., max_length=100)

class UpdateClient(BaseClient):
    pass

class Client(BaseClient):
    id:int



