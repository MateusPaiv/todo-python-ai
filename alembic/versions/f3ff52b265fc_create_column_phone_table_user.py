"""create column phone table user

Revision ID: f3ff52b265fc
Revises: 
Create Date: 2025-03-03 21:25:44.070054

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f3ff52b265fc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("phone", sa.String(length=15), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "phone")
