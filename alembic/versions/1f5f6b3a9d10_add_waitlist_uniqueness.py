"""Enforce one waitlist entry per user and edition.

Revision ID: 1f5f6b3a9d10
Revises: ed6ef11eef8a
"""
from alembic import op


revision = "1f5f6b3a9d10"
down_revision = "ed6ef11eef8a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_waitlist_user_edition",
        "waitlist",
        ["user_id", "edition_id"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_waitlist_user_edition", "waitlist", type_="unique")
