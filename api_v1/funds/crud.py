from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from sqlalchemy.orm import selectinload

from api_v1.funds.schemas import MoveMoneyData
from core.helpers import CustomValidationError
from core.models.account import Account
from core.models.money_move_order import MoneyMoveOrder as Mmo


async def check_balance(account: Account, session: AsyncSession) -> dict:
    async def get_sum_of_funds(account_id, is_executed: bool):
        result = await session.execute(
            select(func.sum(Mmo.amount)).where(
                account_id == account.id, Mmo.is_executed == is_executed
            )
        )
        return result.scalar() or 0

    if account.is_active:
        executed_debits = await get_sum_of_funds(Mmo.id_acc_cr, is_executed=True) or 0
        executed_credits = await get_sum_of_funds(Mmo.id_acc_db, is_executed=True) or 0
        pending_credits = await get_sum_of_funds(Mmo.id_acc_db, is_executed=False) or 0

    else:
        executed_debits = await get_sum_of_funds(Mmo.id_acc_db, is_executed=True) or 0
        executed_credits = await get_sum_of_funds(Mmo.id_acc_cr, is_executed=True) or 0
        pending_credits = await get_sum_of_funds(Mmo.id_acc_cr, is_executed=False) or 0

    current = executed_debits - executed_credits
    available = executed_debits - executed_credits - pending_credits

    return {"current": current, "available": available}


async def move_money(user_validated: dict, movement_data: MoveMoneyData, session: AsyncSession):
    result = await session.execute(
        select(Account)
        .options(selectinload(Account.currency))
        .where(Account.num_account == movement_data.strAccDb)
    )
    acc_db = result.scalars().first()
    if not acc_db:
        raise CustomValidationError(
            status_code=404,
            detail="there is no such account for debet",
            type="account_missing",
            loc=["body", "strAccDb"],
            input=f"{movement_data.strAccDb}",
        )

    if user_validated['idUser'] != acc_db.user_id:
        raise CustomValidationError(
            status_code=404,
            detail="not allowed to move money from this account",
            type="not_allowed",
            loc=["body", "strAccDb"],
            input=f"{movement_data.strAccDb}",
        )


    result = await session.execute(
        select(Account)
        .options(selectinload(Account.currency))
        .where(Account.num_account == movement_data.strAccCr)
    )
    
    acc_cr = result.scalars().first()
    if not acc_cr:
        raise CustomValidationError(
            status_code=404,
            detail="there is no such account for credit",
            type="account_missing",
            loc=["body", "strAccCr"],
            input=f"{movement_data.strAccCr}",
        )

    if acc_db.currency != acc_cr.currency:
        raise CustomValidationError(
            status_code=400,
            detail="currencies should be the same",
            type="currencies_not_the_same",
            loc=["body", "strAccCr"],
            input=f"{movement_data.strAccCr}",
        )


    if acc_db.is_active:
        result = await check_balance(acc_db, session)
        logging.error(f'{result["available"]}')
        available = result["available"]
        if available < movement_data.amount:
            raise CustomValidationError(
                status_code=422,
                detail="insufficient funds",
                type="invalid_amount",
                loc=["body", "amount"],
                input=f"{movement_data.amount}",
            )

    if not acc_cr.is_active:
        result = await check_balance(acc_cr, session)
        available = result["available"]
        if available < movement_data.amount:
            raise CustomValidationError(
                status_code=422,
                detail="balance cannot be lower than 0",
                type="invalid_amount",
                loc=["body", "amount"],
                input=f"{movement_data.amount}",
            )

    data = movement_data.model_dump(by_alias=True)
    data["id_acc_cr"] = acc_cr.id
    data["id_acc_db"] = acc_db.id
    data["is_executed"] = data.pop("execute")
    data.pop("strAccCr")
    data.pop("strAccDb")
    new_order = Mmo(**data)
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)
    return new_order
