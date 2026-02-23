"""alter processos.data_ajuizamento from string to datetime

Revision ID: 20260223_0002
Revises: 20260223_0001
Create Date: 2026-02-23 00:02:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260223_0002"
down_revision: Union[str, None] = "20260223_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "processos",
        "data_ajuizamento",
        existing_type=sa.String(),
        type_=sa.DateTime(),
        existing_nullable=True,
        postgresql_using="data_ajuizamento::timestamp",
    )


def downgrade() -> None:
    op.alter_column(
        "processos",
        "data_ajuizamento",
        existing_type=sa.DateTime(),
        type_=sa.String(),
        existing_nullable=True,
        postgresql_using="data_ajuizamento::text",
    )
