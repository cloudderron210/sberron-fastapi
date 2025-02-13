from pydantic import BaseModel, ConfigDict, field_validator, Field


from api_v1.users.schemas import AddUser



class ClientCredentials():
    login: str = Field(max_length=20)
    password: str = Field(min_length=6, max_length=20)


class AddClient(ClientCredentials,AddUser):
    pass
    
class LoginClient(ClientCredentials, BaseModel):
    pass


