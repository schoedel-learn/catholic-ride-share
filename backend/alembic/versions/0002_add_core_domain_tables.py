"""Create core domain tables for rides, drivers, and parishes.

Revision ID: 0002_add_core_domain_tables
Revises: 0001_add_user_location_fields
Create Date: 2025-12-13
"""

import sqlalchemy as sa
from geoalchemy2 import Geography

from alembic import op

# revision identifiers, used by Alembic.
revision = "0002_add_core_domain_tables"
down_revision = "0001_add_user_location_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create core domain tables."""
    op.create_table(
        "parishes",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(), nullable=False, index=True),
        sa.Column("address_line1", sa.String(), nullable=False),
        sa.Column("address_line2", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("zip_code", sa.String(), nullable=False),
        sa.Column("location", Geography(geometry_type="POINT", srid=4326), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "driver_profiles",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), unique=True, nullable=False),
        sa.Column("vehicle_make", sa.String(), nullable=True),
        sa.Column("vehicle_model", sa.String(), nullable=True),
        sa.Column("vehicle_year", sa.Integer(), nullable=True),
        sa.Column("vehicle_color", sa.String(), nullable=True),
        sa.Column("license_plate", sa.String(), nullable=True),
        sa.Column("vehicle_capacity", sa.Integer(), nullable=False, server_default="4"),
        sa.Column(
            "insurance_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column("background_check_status", sa.String(), nullable=False, server_default="pending"),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("total_rides", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("average_rating", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ride_requests",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("rider_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column(
            "destination_type",
            sa.Enum(
                "mass", "confession", "prayer_event", "social", "other", name="destinationtype"
            ),
            nullable=False,
        ),
        sa.Column("parish_id", sa.Integer(), sa.ForeignKey("parishes.id"), nullable=True),
        sa.Column("pickup_location", Geography(geometry_type="POINT", srid=4326), nullable=False),
        sa.Column(
            "destination_location", Geography(geometry_type="POINT", srid=4326), nullable=False
        ),
        sa.Column("requested_datetime", sa.DateTime(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("passenger_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "accepted",
                "in_progress",
                "completed",
                "cancelled",
                name="riderequeststatus",
            ),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False, index=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "rides",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "ride_request_id",
            sa.Integer(),
            sa.ForeignKey("ride_requests.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("driver_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("rider_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("accepted_at", sa.DateTime(), nullable=False),
        sa.Column("pickup_time", sa.DateTime(), nullable=True),
        sa.Column("dropoff_time", sa.DateTime(), nullable=True),
        sa.Column(
            "actual_pickup_location", Geography(geometry_type="POINT", srid=4326), nullable=True
        ),
        sa.Column(
            "actual_dropoff_location", Geography(geometry_type="POINT", srid=4326), nullable=True
        ),
        sa.Column(
            "status",
            sa.Enum(
                "accepted",
                "driver_enroute",
                "arrived",
                "picked_up",
                "in_progress",
                "completed",
                "cancelled",
                name="ridestatus",
            ),
            nullable=False,
            server_default="accepted",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Drop core domain tables."""
    op.drop_table("rides")
    op.drop_table("ride_requests")
    op.drop_table("driver_profiles")
    op.drop_table("parishes")

    # Drop enums to allow clean rollback
    op.execute("DROP TYPE IF EXISTS destinationtype")
    op.execute("DROP TYPE IF EXISTS riderequeststatus")
    op.execute("DROP TYPE IF EXISTS ridestatus")
