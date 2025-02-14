from datetime import datetime
from pydantic import BaseModel, ConfigDict, constr, field_validator, Field
from pydantic.alias_generators import to_camel


from api_v1.users.schemas import AddUser



class ClientCredentials():
    login: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=6, max_length=20)


class ValidatorsMixin():
    @field_validator('login')
    def validate_login(cls, value: str):
        if value.isdigit():
            raise ValueError('Invalid login')
        return value
    
    @field_validator('password')
    def validate_password(cls, value: str):
        if not any(c.isupper() for c in value):
            raise ValueError('Invalid password, must contain at least 1 uppercase letter') 
        if not any(c.isdigit() for c in value):
            raise ValueError('Invalid password, must contain at least 1 digit') 
            
        return value
    

class AddClient(ClientCredentials,AddUser,ValidatorsMixin):
    pass
    
class LoginClient(ClientCredentials, BaseModel):
    pass

class JwtResponse(BaseModel):
    jwt: str


class ClientRegistered(BaseModel):
    login: str
    date_register: datetime
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel)
