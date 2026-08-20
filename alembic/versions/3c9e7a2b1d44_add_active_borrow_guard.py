"""Prevent multiple active borrows of the same edition by one user.

Revision ID: 3c9e7a2b1d44
Revises: 1f5f6b3a9d10
"""
from alembic import op
import sqlalchemy as sa


revision = "3c9e7a2b1d44"
down_revision = "1f5f6b3a9d10"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "uq_active_borrow_user_edition",
        "borrows",
        ["user_id", "edition_id"],
        unique=True,
        postgresql_where=sa.text("status = 'ACTIVE'"),
    )


def downgrade() -> None:
    op.drop_index("uq_active_borrow_user_edition", table_name="borrows")
