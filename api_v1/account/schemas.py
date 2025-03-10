from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel, to_snake

# from api_v1.users.schemas import UserResponse


class ValidatorMixin:
    
    @field_validator('balNum')
    def validate_balnum(cls, value: str):
        if not value.isdigit():
            raise ValueError('must contain only digits')
        return value
    

class BaseAccount(BaseModel):
    userId: int | None = Field(None)
    currencyId: int | None = Field(None)
    balNum: str | None = Field(None, max_length=5, min_length=5)
    description: str | None = Field(None)
    isActive: bool | None = Field(None)

    model_config = ConfigDict(
        alias_generator=to_snake,
        populate_by_name=True
    )

class AddAccount(BaseModel, ValidatorMixin):
    userId: int = Field(...)
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
    user_id: int 
    currency_id: int 
    description: str  
    is_active: bool
    # users: list[UserResponse]

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel)
    

    

