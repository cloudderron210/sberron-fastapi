import re
from pydantic import BaseModel, field_validator 
from sqlmodel import Field

class AddClient(BaseModel):
    name: str = Field(..., max_length=100)
    telephone: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=30)
    patronymic: str | None = Field()
    birthday: str | None = Field()
    sex: str = Field(..., regex='^(male|female|other)$')
    document : str = Field(..., regex='^(passport|international passport)$')
    docRequisites: str = Field(..., max_length=100)
    docIssuedBy: str = Field(..., max_length=100)

    @field_validator("telephone")
    def validate_telephone(cls, value):
        if not re.match(r'^\+?\d{1,15}$', value):
            raise ValueError("Invalid telephone format")
        return value



