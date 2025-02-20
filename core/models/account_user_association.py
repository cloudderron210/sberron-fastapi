
from sqlalchemy import Column, ForeignKey, Table

from core.models.base import Base


user_account = Table(
    'user_account',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('account_id', ForeignKey('accounts.id'), primary_key=True),
)
