"""Poblar roles por defecto

Revision ID: f6cf0da1c11b
Revises: e2fe67794491
Create Date: 2025-05-10 00:20:42.288526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6cf0da1c11b'
down_revision: Union[str, None] = 'e2fe67794491'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO rol (nombre) VALUES ('usuario');")
    op.execute("INSERT INTO rol (nombre) VALUES ('admin');")


def downgrade() -> None:
    op.execute("DELETE FROM rol WHERE nombre IN ('usuario', 'admin');")
