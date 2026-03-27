"""add story_theme to curriculum_units and selected_story_theme to children

Revision ID: a1b2c3d4e5f6
Revises: f1a2b3c4d5e6
Create Date: 2026-03-24 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'f1a2b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'curriculum_units',
        sa.Column('story_theme', sa.String(50), nullable=False, server_default='earth_crew'),
    )
    op.add_column(
        'children',
        sa.Column('selected_story_theme', sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('children', 'selected_story_theme')
    op.drop_column('curriculum_units', 'story_theme')
