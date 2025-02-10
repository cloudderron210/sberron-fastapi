from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel, to_snake


class ValidatorMixin:
    
    @field_validator('balNum')
    def validate_balnum(cls, value: str):
        if not value.isdigit():
            raise ValueError('must contain only digits')
        return value
    

class BaseAccount(BaseModel):
    clientId: int | None = Field(None)
    currencyId: int | None = Field(None)
    balNum: str | None = Field(None, max_length=5, min_length=5)
    description: str | None = Field(None)
    isActive: bool | None = Field(None)

    model_config = ConfigDict(
        alias_generator=to_snake,
        populate_by_name=True
    )

class AddAccount(BaseModel, ValidatorMixin):
    clientId: int = Field(...)
    currencyId: int = Field(...)
    balNum: str = Field(..., max_length=5, min_length=5)
    description: str  = Field(...)
    isActive: bool = Field(...)
    
    model_config = ConfigDict(
        alias_generator=to_snake,
        populate_by_name=True
    )


class PatchAccount(BaseAccount, ValidatorMixin):
    pass


    
class AccountResponse(BaseModel):
    id: int
    num_account: str
    client_id: int 
    currency_id: int 
    description: str  
    is_active: bool

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel)
    

    

