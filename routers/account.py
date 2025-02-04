from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from sqlmodel import select
from sql.engine import SessionDep
from sql.models import Account, Client, Currency


account_router = APIRouter()


class AddAccount(BaseModel):
    owner_id: int = Field(...)
    currency_id: int = Field(...)
    balNum: str = Field(..., max_length=5, min_length=5)
    description: str = Field(...)
    isActive: bool = Field(...)

    @field_validator('balNum')
    def validate_balnum(cls, value: str):
        if not value.isdigit():
            raise ValueError('must contain only digits')
        return value

@account_router.get('/getaccounts')
async def get_accounts(session: SessionDep):
    accs = session.exec(select(Account)).fetchall()
    result = [
        {
            "id": account.id,
            "numAccount": account.numAccount,
            "dateOpen": account.dateOpen.isoformat() if account.dateOpen else None,
            "dateClosed": account.dateClosed.isoformat() if account.dateClosed else None,
            "description": account.description,
            "isActive": account.isActive,
            "status": account.status,
            "owner": account.owner_id,
            "currency": account.currency_id,
        }
        for account in accs 
    ]
    return JSONResponse({'accs': result})
    

@account_router.post('/addaccount')
async def add_account(account_data: AddAccount, session: SessionDep):
    
    id_acc = session.exec(select(Client).where(Client.id == account_data.owner_id)).first()
    if not id_acc:
        raise HTTPException(400, 'there are no Client with such id')
        
    currency = session.exec(select(Currency).where(Currency.id == account_data.currency_id)).first()
    if not currency:
        raise HTTPException(400, 'no such currency')

    def generate_licnum():
        accs = session.exec(select(Account)).fetchall()
        if accs:
            num_accs = [int(acc.model_dump()['numAccount'][-2:]) for acc in accs]
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
    
    data = account_data.model_dump()
    licnum = generate_licnum()
    data['numAccount'] = account_data.balNum + str(account_data.currency_id)+ str(sum_c(account_data.balNum, licnum, str(account_data.currency_id))) + '4444' + licnum
    
    new_account = Account(**data)
    session.add(new_account)
    session.commit()
    session.refresh(new_account)
    new_account = new_account.model_dump()
    new_account['dateOpen'] = new_account['dateOpen'].isoformat()
    
    return JSONResponse({'success':True, 'new_account':new_account})
    



        
    
