from fastapi import HTTPException
from sqlmodel import select
from sql.engine import SessionDep
from sql.models import Client

from client.schemas import AddClient


async def add_client(client_data: AddClient, session: SessionDep):

    client_telephone = session.exec(
        select(Client).where(Client.telephone == client_data.telephone)
    ).first()
    if client_telephone:
        raise HTTPException(400, f"telephone exists")

    client_req = session.exec(
        select(Client).where(Client.docRequisites == client_data.docRequisites)
    ).first()
    if client_req:
        raise HTTPException(400, "docRequisites exists")

    new_client = Client(**client_data.model_dump())
    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    return new_client
