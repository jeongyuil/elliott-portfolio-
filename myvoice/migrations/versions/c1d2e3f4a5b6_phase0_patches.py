"""phase0_patches: idempotency_key, session_activity status default, activity columns

Revision ID: c1d2e3f4a5b6
Revises: 707faa12c1fd
Create Date: 2026-02-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1d2e3f4a5b6'
down_revision: Union[str, None] = '707faa12c1fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add idempotency_key to utterances for duplicate-request prevention
    op.add_column(
        'utterances',
        sa.Column('idempotency_key', sa.String(255), nullable=True),
    )
    op.create_index(
        'ix_utterances_idempotency_key',
        'utterances',
        ['idempotency_key'],
    )

    # Update existing session_activities records from 'pending' to 'idle'
    op.execute(
        "UPDATE session_activities SET status = 'idle' WHERE status = 'pending'"
    )

    # Add activity columns from ad-hoc scripts (idempotent via IF NOT EXISTS)
    op.execute(
        "ALTER TABLE activities ADD COLUMN IF NOT EXISTS image_path TEXT"
    )
    op.execute(
        "ALTER TABLE activities ADD COLUMN IF NOT EXISTS story_content TEXT"
    )
    op.execute(
        "ALTER TABLE activities ADD COLUMN IF NOT EXISTS key_expression VARCHAR(200)"
    )
    op.execute(
        "ALTER TABLE activities ADD COLUMN IF NOT EXISTS image_prompt TEXT"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE activities DROP COLUMN IF EXISTS image_prompt"
    )
    op.execute(
        "ALTER TABLE activities DROP COLUMN IF EXISTS key_expression"
    )
    op.execute(
        "ALTER TABLE activities DROP COLUMN IF EXISTS story_content"
    )
    op.execute(
        "ALTER TABLE activities DROP COLUMN IF EXISTS image_path"
    )
    op.execute(
        "UPDATE session_activities SET status = 'pending' WHERE status = 'idle'"
    )
    op.drop_index('ix_utterances_idempotency_key', table_name='utterances')
    op.drop_column('utterances', 'idempotency_key')
