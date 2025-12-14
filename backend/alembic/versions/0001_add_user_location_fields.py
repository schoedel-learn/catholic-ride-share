"""Add user location tracking fields.

Revision ID: 0001_add_user_location_fields
Revises:
Create Date: 2025-11-21
"""

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geography

# revision identifiers, used by Alembic.
revision = "0001_add_user_location_fields"
down_revision = "0000_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add last_known_location and last_location_updated_at columns to users."""
    op.add_column(
        "users",
        sa.Column(
            "last_known_location",
            Geography(geometry_type="POINT", srid=4326),
            nullable=True,
        ),
    )
    op.add_column(
        "users",
        sa.Column("last_location_updated_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Remove user location tracking columns."""
    op.drop_column("users", "last_location_updated_at")
    op.drop_column("users", "last_known_location")
