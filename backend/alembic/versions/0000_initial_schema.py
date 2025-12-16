"""Create initial schema with users table.

Revision ID: 0000_initial_schema
Revises:
Create Date: 2025-11-20
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0000_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create users table."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("email", sa.String(), unique=True, index=True, nullable=False),
        sa.Column("phone", sa.String(), unique=True, index=True, nullable=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column(
            "role",
            sa.Enum("rider", "driver", "both", "admin", name="userrole"),
            nullable=False,
            server_default="rider",
        ),
        sa.Column("parish_id", sa.Integer(), nullable=True),
        sa.Column("profile_photo_url", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    """Drop users table."""
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS userrole")
