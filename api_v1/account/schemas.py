from pydantic import BaseModel, Field, field_validator




class BaseAccount(BaseModel):
    owner_id: int = Field(...)
    currency_id: int = Field(...)
    balNum: str = Field(..., max_length=5, min_length=5)
    description: str = Field(...)
    isActive: bool = Field(...)

    @field_validator('balNum')
    def validate_balnum(cls, value: str):
        if not value.isdigit():
            raise ValueError('must contain only digits')
        return value

class AddAccount(BaseAccount):
    pass


# class Account(Base)


