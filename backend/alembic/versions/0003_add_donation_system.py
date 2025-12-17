"""Add donation + review system.

Revision ID: 0003_add_donation_system
Revises: 0002_add_core_domain_tables
Create Date: 2025-12-14
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0003_add_donation_system"
down_revision = "0002_add_core_domain_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add donation and review tables + user donation preferences."""
    # Users: Stripe + donation preferences
    op.add_column("users", sa.Column("stripe_customer_id", sa.String(), nullable=True))
    op.create_index(
        "ix_users_stripe_customer_id",
        "users",
        ["stripe_customer_id"],
        unique=True,
    )

    op.add_column(
        "users",
        sa.Column(
            "auto_donation_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "auto_donation_type",
            sa.Enum("fixed", "distance_based", name="autodonationtype"),
            nullable=False,
            server_default="fixed",
        ),
    )
    op.add_column("users", sa.Column("auto_donation_amount_cents", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("auto_donation_multiplier", sa.Float(), nullable=True))

    # Donations
    op.create_table(
        "donations",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("ride_id", sa.Integer(), sa.ForeignKey("rides.id"), nullable=False, index=True),
        sa.Column("donor_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column(
            "recipient_id",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            nullable=True,
            index=True,
        ),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False, server_default="USD"),
        sa.Column(
            "stripe_payment_intent_id",
            sa.String(),
            nullable=False,
            unique=True,
            index=True,
        ),
        sa.Column("stripe_client_secret", sa.String(), nullable=True),
        sa.Column("stripe_charge_id", sa.String(), nullable=True),
        sa.Column(
            "stripe_status",
            sa.String(),
            nullable=False,
            server_default="pending",
            index=True,
        ),
        sa.Column("stripe_fee_cents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("net_amount_cents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )

    # Reviews
    op.create_table(
        "ride_reviews",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "ride_id",
            sa.Integer(),
            sa.ForeignKey("rides.id"),
            nullable=False,
            unique=True,
            index=True,
        ),
        sa.Column(
            "reviewer_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True
        ),
        sa.Column(
            "reviewee_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True
        ),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("idx_driver_reviews", "ride_reviews", ["reviewee_id", "rating"])


def downgrade() -> None:
    """Remove donation and review system."""
    op.drop_index("idx_driver_reviews", table_name="ride_reviews")
    op.drop_table("ride_reviews")
    op.drop_table("donations")

    op.drop_column("users", "auto_donation_multiplier")
    op.drop_column("users", "auto_donation_amount_cents")
    op.drop_column("users", "auto_donation_type")
    op.drop_column("users", "auto_donation_enabled")

    op.drop_index("ix_users_stripe_customer_id", table_name="users")
    op.drop_column("users", "stripe_customer_id")

    # Drop enum to allow clean rollback
    op.execute("DROP TYPE IF EXISTS autodonationtype")
