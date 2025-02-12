from datetime import date, datetime
from enum import Enum
import re
from typing import TypeVar
from pydantic import BaseModel, ConfigDict, field_validator, Field

from pydantic.alias_generators import to_snake
from sqlalchemy import String

from api_v1.users.schemas import AddUser


class AddClient(AddUser):
    login: str = Field(max_length=20)
    password: str = Field(min_length=6, max_length=20)
    


