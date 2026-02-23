"""add unique constraint on processos numero_cnj + tribunal

Revision ID: 20260223_0001
Revises:
Create Date: 2026-02-23 00:01:00.000000
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260223_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_processos_numero_tribunal",
        "processos",
        ["numero_cnj", "tribunal"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_processos_numero_tribunal", "processos", type_="unique")
