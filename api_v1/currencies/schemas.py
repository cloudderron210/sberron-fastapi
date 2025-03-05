from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel, to_snake


class ValidatorMixin:
    @field_validator('strCode')
    def validate_balnum(cls, value: str):
        if any(c.islower() for c in value):
            raise ValueError('must contain only uppercase letters')
        return value

class CurrencyBase(BaseModel):
    id: int  
    strCode: str = Field(min_length=3, max_length=3)
    name: str
    model_config = ConfigDict(
        alias_generator=to_snake,
        populate_by_name=True
    )

class CurrencyResponse(BaseModel):
    id: int 
    str_code: str 
    name: str
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class AddCurrency(CurrencyBase, ValidatorMixin):
    pass

class PatchCurrency(CurrencyBase, ValidatorMixin):
    pass

    

    

