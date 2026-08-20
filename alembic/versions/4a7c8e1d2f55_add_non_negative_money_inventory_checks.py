"""Protect wallet, inventory, and order amounts from invalid values.

Revision ID: 4a7c8e1d2f55
Revises: 3c9e7a2b1d44
"""
from alembic import op


revision = "4a7c8e1d2f55"
down_revision = "3c9e7a2b1d44"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_base_users_wallet_non_negative",
        "base_users",
        "wallet_amount >= 0",
    )
    op.create_check_constraint(
        "ck_editions_price_non_negative",
        "editions",
        "price >= 0",
    )
    op.create_check_constraint(
        "ck_editions_amount_non_negative",
        "editions",
        "amount >= 0",
    )
    op.create_check_constraint(
        "ck_transactions_amount_positive",
        "transactions",
        "amount > 0",
    )
    op.create_check_constraint(
        "ck_orders_final_price_non_negative",
        "orders",
        "final_price >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_orders_final_price_non_negative", "orders", type_="check")
    op.drop_constraint("ck_transactions_amount_positive", "transactions", type_="check")
    op.drop_constraint("ck_editions_amount_non_negative", "editions", type_="check")
    op.drop_constraint("ck_editions_price_non_negative", "editions", type_="check")
    op.drop_constraint("ck_base_users_wallet_non_negative", "base_users", type_="check")
