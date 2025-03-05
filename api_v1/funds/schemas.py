from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from sqlalchemy import DECIMAL, String






    
class MoveMoneyData(BaseModel):
    strAccDb: str
    strAccCr: str
    amount: Decimal
    execute: bool
    description: str = Field(..., max_length=100)
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class MovementResponse(BaseModel):
    id: int
    date_created: datetime
    amount: int
    is_executed: bool
    id_acc_cr: int 
    id_acc_db: int

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel)
    
class BalanceResponse(BaseModel):
    current: float
    available: float
