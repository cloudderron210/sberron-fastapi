from pydantic import BaseModel, Field, field_validator
from pydantic.alias_generators import to_snake


class ValidatorMixin:
    
    @field_validator('balNum')
    def validate_balnum(cls, value: str):
        if not value.isdigit():
            raise ValueError('must contain only digits')
        return value
    

class BaseAccount(BaseModel):
    clientId: int = Field(...)
    currencyId: int = Field(...)
    balNum: str = Field(..., max_length=5, min_length=5)
    description: str = Field(...)
    isActive: bool = Field(...)
    
    class Config:
        alias_generator = to_snake
        populate_by_name = True

class AddAccount(BaseAccount):
    pass

class PatchAccount():
    clientId: int | None= Field(...)
    currencyId: int | None= Field(...)
    balNum: str | None= Field(..., max_length=5, min_length=5)
    description: str | None= Field(...)
    isActive: bool | None= Field(...)

# class Account(Base)


class Account(BaseModel):
    id: int
    clientId: int 
    currencyId: int 
    description: str 
    isActive: bool 
    num_account: str
    class Config:
        alias_generator = to_snake
        populate_by_name = True
    
