from fastapi import  HTTPException
from sqlalchemy import Result
from sqlalchemy.orm import selectinload
from sqlmodel import select
from api_v1.account.schemas import AddAccount, BaseAccount
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from api_v1.currencies.schemas import AddCurrency
from core.helpers import CustomValidationError
from core.models.account import Account
from core.models.user import User 
from core.models.currency import Currency
    

async def get_currencies(session: AsyncSession) -> list[Currency]:
    stmt = select(Currency).order_by(Currency.id)
    result: Result = await session.execute(stmt)
    currencies = result.scalars().all()
    return list(currencies)



async def add(currency_data: AddCurrency, session: AsyncSession) -> Currency:

    data = currency_data.model_dump(by_alias=True)
    new_currency = Currency(**data)
    session.add(new_currency)
    await session.commit()
    await session.refresh(new_currency)
    
    return new_currency


