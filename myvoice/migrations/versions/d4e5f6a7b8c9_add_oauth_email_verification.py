"""add_oauth_email_verification

Revision ID: d4e5f6a7b8c9
Revises: c1d2e3f4a5b6
Create Date: 2026-02-16 00:00:00.000000

Adds:
  - family_accounts: email_verified, email_verification_token,
    email_verification_expires, password_reset_token, password_reset_expires
  - oauth_accounts table (Google / Kakao / Apple)
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, None] = "e38fb29f43bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- family_accounts: new auth columns ---
    op.add_column(
        "family_accounts",
        sa.Column("email_verified", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "family_accounts",
        sa.Column("email_verification_token", sa.String(255), nullable=True),
    )
    op.add_column(
        "family_accounts",
        sa.Column("email_verification_expires", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "family_accounts",
        sa.Column("password_reset_token", sa.String(255), nullable=True),
    )
    op.add_column(
        "family_accounts",
        sa.Column("password_reset_expires", sa.DateTime(), nullable=True),
    )

    # --- oauth_accounts table ---
    op.create_table(
        "oauth_accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "family_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("family_accounts.family_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("provider", sa.String(20), nullable=False),
        sa.Column("provider_user_id", sa.String(255), nullable=False),
        sa.Column("provider_email", sa.String(255), nullable=True),
        sa.Column("access_token", sa.String(2048), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("provider", "provider_user_id", name="uq_oauth_provider_user"),
    )
    op.create_index("ix_oauth_accounts_family_id", "oauth_accounts", ["family_id"])


def downgrade() -> None:
    op.drop_index("ix_oauth_accounts_family_id", table_name="oauth_accounts")
    op.drop_table("oauth_accounts")

    op.drop_column("family_accounts", "password_reset_expires")
    op.drop_column("family_accounts", "password_reset_token")
    op.drop_column("family_accounts", "email_verification_expires")
    op.drop_column("family_accounts", "email_verification_token")
    op.drop_column("family_accounts", "email_verified")
