from decimal import Decimal
import re
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from sqlmodel import func, select
from core.models.account import Account
from sql.engine import SessionDep
from sql.models import Client, Currency 
from core.models.money_move_order import MoneyMoveOrder as Mvo




money_router = APIRouter()
    
class MoveMoney(BaseModel):
    strAccDb: str = Field(...)
    strAccCr: str = Field(...)
    amount: Decimal = Field(...)
    execute: bool = Field(...)
    description: str = Field(...)

class Balance(BaseModel):
    idAccount: int = Field()

    
def check_balance(account: Account, session: SessionDep) -> dict:
    if account.is_active:
        executed_debits = (
            session.exec(
                select(func.sum(Mvo.amount)).where(
                    Mvo.id_acc_cr== account.id,
                    Mvo.is_executed == True
                )
            ).one()
        ) or 0
        executed_credits = (
            session.exec(
                select(func.sum(Mvo.amount)).where(
                    Mvo.id_acc_cr== account.id,
                    Mvo.is_executed == True
                )
            ).one()
        ) or 0
        pending_credits = (
            session.exec(
                select(func.sum(Mvo.amount)).where(
                    Mvo.id_acc_cr== account.id,
                    Mvo.is_executed == False 
                )
            ).one()
        ) or 0
        current = executed_debits - executed_credits
        available = executed_debits - executed_credits - pending_credits
    
    else:
        executed_debits = (
            session.exec(
                select(func.sum(Mvo.amount)).where(
                    Mvo.id_acc_cr== account.id,
                    Mvo.is_executed == True
                )
            ).one()
        ) or 0
        executed_credits = (
            session.exec(
                select(func.sum(Mvo.amount)).where(
                    Mvo.id_acc_cr== account.id,
                    Mvo.is_executed == True
                )
            ).one()
        ) or 0
        
        pending_credits = (
            session.exec(
                select(func.sum(Mvo.amount)).where(
                    Mvo.id_acc_cr== account.id,
                    Mvo.is_executed == False 
                )
            ).one()
        ) or 0
        
        current = executed_debits - executed_credits
        available = executed_debits - executed_credits - pending_credits
    return {'current': float(current), 'available': float(available)}
   

@money_router.post('/balance')
def balance(balance_data:Balance, session: SessionDep):
    account = session.exec(select(Account).where(Account.id == balance_data.idAccount)).first()
    if not account:
        raise HTTPException(400, 'account not found')

    balance = check_balance(account, session)

    return JSONResponse(balance)

    

@money_router.post('/moveMoney')
def move_money(move_money_data: MoveMoney, session: SessionDep):
    acc_db = session.exec(select(Account).where(Account.num_account== move_money_data.strAccDb)).first()
    acc_cr = session.exec(select(Account).where(Account.num_account== move_money_data.strAccCr)).first()

    if not acc_db:
        raise HTTPException(400, "no such acc_db")
    if not acc_cr:
        raise HTTPException(400, f"no such acc_cr {acc_db.num_account}")

    if acc_db.currency_id!= acc_cr.currency_id:
        raise HTTPException(400, 'currencys should be the same')

    if acc_db.num_account:
        acc_db_available = check_balance(acc_db, session)['available']
        if int(acc_db_available) < move_money_data.amount:
            raise HTTPException(400, 'insufficient amount on accDb')
    if not acc_cr.num_account:
        acc_cr_available = check_balance(acc_cr, session)['available']
        if int(acc_cr_available) < move_money_data.amount:
            raise HTTPException(400, 'balance cannot be lower than 0')

        
    data = move_money_data.model_dump()
    data['idAccCr'] = acc_cr.id
    data['idAccDb'] = acc_db.id
    data.pop('strAccCr')
    data.pop('strAccDb')
    data['is_executed'] = move_money_data.execute



    new_order = Mvo(**data)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    
    return JSONResponse({'result': True})
    
   
