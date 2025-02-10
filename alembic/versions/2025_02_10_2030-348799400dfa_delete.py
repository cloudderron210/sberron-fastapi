"""delete

Revision ID: 348799400dfa
Revises: d252ef0d816f
Create Date: 2025-02-10 20:30:14.615053

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "348799400dfa"
down_revision: Union[str, None] = "d252ef0d816f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_client")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_client",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "client_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"], ["clients.id"], name="user_client_client_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="user_client_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="user_client_pkey"),
    )
    # ### end Alembic commands ###
