from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select
from account import crud
from account.schemas import AddAccount
from sql.engine import SessionDep
from sql.models import Account, Client, Currency


router = APIRouter(prefix="/account")


@router.get("/get")
async def get_accounts(session: SessionDep):
    result = await crud.get(session)
    return JSONResponse({"accs": result})


@router.get("/get/{account_id}/")
async def get_accounts_by_id(account_id: int, session: SessionDep):
    result = await crud.get_by_id(account_id, session)
    return JSONResponse({"accs": result})


@router.post("/add")
async def add_account(account_data: AddAccount, session: SessionDep):

    new_account = await crud.add(account_data, session)

    return JSONResponse({"success": True, "new_account": new_account})
