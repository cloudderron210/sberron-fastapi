from pydantic import BaseModel, ConfigDict, constr, field_validator, Field


from api_v1.users.schemas import AddUser



class ClientCredentials():
    login: str = Field(max_length=20)
    password: str = Field(min_length=6, max_length=20)


    @field_validator('login')
    def validate_login(cls, value: str):
        if value.isdigit():
            raise ValueError('Invalid login')
        return value
    
    @field_validator('password')
    def validate_password(cls, value: str):
        if not any(c.isupper() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError('Invalid password, must contain at least 1 uppercase letter and 1 digit')
        return value
    

class AddClient(ClientCredentials,AddUser):
    pass
    
class LoginClient(ClientCredentials, BaseModel):
    pass

class JwtResponse(BaseModel):
    jwt: str



