from os import getenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    apiv1_prefix: str = '/api/v1'
    db_url: str = 'postgresql+asyncpg://derron:Cloudderron210!@194.120.116.89/debug2' 
    db_echo: bool = True
    
    

settings = Settings()
