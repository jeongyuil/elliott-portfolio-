"""add parent_mode_pin to family_accounts

Revision ID: bcd244f29f1e
Revises: d4e5f6a7b8c9
Create Date: 2026-03-20 03:19:19.117628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcd244f29f1e'
down_revision: Union[str, None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('family_accounts', sa.Column('parent_mode_pin', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('family_accounts', 'parent_mode_pin')
