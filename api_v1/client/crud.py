from fastapi import HTTPException
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from core.models import Client

from api_v1.client.schemas import AddClient, PatchClient, UpdateClient

async def check_if_exists(session: AsyncSession, 
                          telephone: str | None = None, 
                          docRequisites: str | None= None,  
                          client_id: int | None = None):
    
    # client_telephone: Result = await session.execute(
    #     select(Client).where(Client.id != client_id).where(Client.telephone == telephone)
    # )
    # ct = client_telephone.first()
    # if ct:
    #     raise HTTPException(400, f"telephone exists")
    #
    # client_req: Result = await session.execute(
    #     select(Client).where(Client.id != client_id).where(Client.doc_requisites == docRequisites)
    # )
    # reqs = client_req.first()
    # if reqs:
    #     raise HTTPException(400, f"docRequisites exists")
    #     
    
    query = select(Client).where(Client.id != client_id)
    if telephone:
        query_tel = query.where(Client.telephone == telephone)
        result: Result = await session.execute(query_tel)
        existing_client = result.scalars().first()
        if existing_client:
            raise HTTPException(400, f"telephone exists")
    if docRequisites:
        query_docs = query.where(Client.doc_requisites == docRequisites)
        result: Result = await session.execute(query_docs)
        existing_client = result.scalars().first()
        if existing_client:
            raise HTTPException(400, f"docRequisites exists")

 

async def add_client(client_data: AddClient, session: AsyncSession) -> Client:

    await check_if_exists(session=session, 
                          telephone=client_data.telephone,
                          docRequisites=client_data.docRequisites)

    new_client = Client(**client_data.model_dump(by_alias=True))
    session.add(new_client)
    await session.commit()
    await session.refresh(new_client)
    return new_client



async def get_client(session: AsyncSession) -> list[Client]:
    stmt = select(Client).order_by(Client.id)
    result: Result = await session.execute(stmt)
    clients = result.scalars().all()
    return list(clients)


async def get_client_by_id(session: AsyncSession, client_id: int) -> Client | None:
    return await session.get(Client, client_id)


async def update_client(session: AsyncSession, 
                        client: Client, 
                        client_update: UpdateClient):
    
    await check_if_exists(session, client.telephone, client.doc_requisites,  client_id=client.id)
    
    for (name, value) in client_update.model_dump(by_alias=True).items():
        setattr(client, name, value)
    await session.commit()
    return client
    
async def patch_client(session: AsyncSession, 
                        client: Client, 
                        client_update: PatchClient):
    
    update_data = client_update.model_dump(by_alias=True, exclude_unset=True)
    
    if 'telephone' or 'docRequisites' in update_data:
        await check_if_exists(session, client_update.telephone, client_update.docRequisites,  client_id=client.id)
    
    for (name, value) in update_data.items():
        setattr(client, name, value)
    await session.commit()
    return client
    
    
