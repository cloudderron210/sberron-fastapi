from os import getenv

from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    apiv1_prefix: str = '/api/v1'
    db_url: str 
    db_echo: bool = True
    jwt_secret_key: str
    jwt_algorith: str = "HS256"

    model_config = SettingsConfigDict(
        env_file = ".env"
    )

settings = Settings() 


