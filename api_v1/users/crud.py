from fastapi import HTTPException
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select
from core.models import User

from api_v1.users.schemas import AddUser, PatchUser, UpdateUser


async def check_if_exists(
    session: AsyncSession,
    telephone: str | None = None,
    docRequisites: str | None = None,
    user_id: int | None = None,
):

    query = select(User).where(User.id != user_id)
    if telephone:
        query_tel = query.where(User.telephone == telephone)
        result: Result = await session.execute(query_tel)
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(400, f"telephone exists")
    if docRequisites:
        query_docs = query.where(User.doc_requisites == docRequisites)
        result: Result = await session.execute(query_docs)
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(400, f"docRequisites exists")


async def add_user(user_data: AddUser, session: AsyncSession) -> User:
    await check_if_exists(
        session=session,
        telephone=user_data.telephone,
        docRequisites=user_data.docRequisites,
    )
    new_user = User(**user_data.model_dump(by_alias=True))
    session.add(new_user)
    return new_user


async def register_user(user_data: AddUser, session: AsyncSession) -> User:
    new_user = await add_user(user_data, session)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_accounts(user_id: int, session: AsyncSession):
    stmt = select(User).options(joinedload(User.accounts)).where(User.id == user_id)
    result: Result = await session.execute(stmt)
    user = result.scalar()
    if user:
        accounts = user.accounts
        return accounts
    else:
        raise HTTPException(404, detail="user not found")


async def get_user(session: AsyncSession) -> list[User]:
    stmt = select(User).options(selectinload(User.accounts)).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.scalar(
        select(User).options(selectinload(User.accounts)).where(User.id == user_id)
    )

async def update_user(session: AsyncSession, user: User, user_update: UpdateUser):

    await check_if_exists(session, user.telephone, user.doc_requisites, user_id=user.id)

    for name, value in user_update.model_dump(by_alias=True).items():
        setattr(user, name, value)
    await session.commit()
    return user

async def patch_user(session: AsyncSession, user: User, user_update: PatchUser):

    update_data = user_update.model_dump(by_alias=True, exclude_unset=True)

    if "telephone" or "docRequisites" in update_data:
        await check_if_exists(
            session, user_update.telephone, user_update.docRequisites, user_id=user.id
        )

    for name, value in update_data.items():
        setattr(user, name, value)
    await session.commit()
    return user
