"""client table added

Revision ID: bca9ba5394d4
Revises: 50dcb95ce54b
Create Date: 2025-02-12 18:19:14.316822

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bca9ba5394d4"
down_revision: Union[str, None] = "50dcb95ce54b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "clients",
        sa.Column(
            "state",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("login", sa.String(length=20), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("salt", sa.String(), nullable=False),
        sa.Column(
            "date_register",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("time_last_login", sa.DateTime(), nullable=True),
        sa.Column("last_login_ip", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("clients")
    # ### end Alembic commands ###
