from fastapi import  HTTPException
from sqlalchemy import Result
from sqlalchemy.orm import selectinload
from sqlmodel import select
from api_v1.account.schemas import AddAccount, BaseAccount
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from core.helpers import CustomValidationError
from core.models.account import Account
from core.models.client import Client
from core.models.currency import Currency
    

async def get_accounts(session: AsyncSession) -> list[Account]:
    stmt = select(Account).order_by(Account.id)
    result: Result = await session.execute(stmt)
    accounts = result.scalars().all()
    return list(accounts)


async def get_owner_by_id(account_id, session: AsyncSession):
    result = await session.execute(select(Account).options(selectinload(Account.client)).where(Account.id == account_id))
    account = result.scalar()
    if account:
        owner = account.client
        return owner
    else:
        raise HTTPException(404, detail="Account not found")

async def get_by_id(account_id: int, session: AsyncSession) -> Account|None:
    return await session.get(Account, account_id)
    

async def add(account_data: AddAccount, session: AsyncSession) -> Account:
    
    result: Result = await session.execute(select(Client).where(Client.id == account_data.clientId))
    existing_client = result.first()
    
    if not existing_client:
        raise CustomValidationError(
            status_code=400,
            detail='there are no Client with such id',
            type='client_not_found',
            loc=['body', 'clientId'],
            input=str(account_data.clientId)
        )
        
    result: Result = await session.execute(select(Currency).where(Currency.id == account_data.currencyId))
    currency = result.first()
    
    if not currency:
        raise CustomValidationError(
            status_code=400,
            detail='there are no currency with such id',
            type='currency_not_found',
            loc=['body', 'clientId'],
            input=str(account_data.currencyId)
        )

    async def generate_licnum():
        result: Result = await session.execute(select(Account))
        accs = result.scalars().all()
        if accs:
            num_accs = [int(acc.num_account[-2:]) for acc in accs]
            max_num = max(num_accs) + 1
            return f'{max_num:07}'
        else:
            return f'{1:07}'

    def sum_c(bal_num:str, lic:str, val:str):
        KOEFFICIENT = [7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1]
        BIK = '567'
        FILIAL = '4444'
        pred = [int(char) for char in (BIK + bal_num + val + '0' + FILIAL+ lic)]
        C = (sum(x * y for x, y in zip(KOEFFICIENT, pred))) % 10 * 3 % 10
        return C 

    data = account_data.model_dump(by_alias=True)
    licnum = await generate_licnum()
    data['num_account'] = account_data.balNum + str(account_data.currencyId)+ str(sum_c(account_data.balNum, licnum, str(account_data.currencyId))) + '4444' + licnum
    data.pop('bal_num')
    
    new_account = Account(**data)
    session.add(new_account)
    await session.commit()
    await session.refresh(new_account)
    
    return new_account


