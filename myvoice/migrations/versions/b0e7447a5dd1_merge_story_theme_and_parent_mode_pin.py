"""merge story_theme and parent_mode_pin

Revision ID: b0e7447a5dd1
Revises: a1b2c3d4e5f6, bcd244f29f1e
Create Date: 2026-03-24 20:38:46.849032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0e7447a5dd1'
down_revision: Union[str, None] = ('a1b2c3d4e5f6', 'bcd244f29f1e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
