"""Poblar roles parte 2

Revision ID: 4bd53d4b510c
Revises: f6cf0da1c11b
Create Date: 2025-05-10 00:25:00.969965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bd53d4b510c'
down_revision: Union[str, None] = 'f6cf0da1c11b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO rol (nombre) VALUES ('usuario');")
    op.execute("INSERT INTO rol (nombre) VALUES ('admin');")



def downgrade() -> None:
    op.execute("DELETE FROM rol WHERE nombre IN ('usuario', 'admin');")

