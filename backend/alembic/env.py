"""Alembic migration environment."""

from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.db.session import Base
from app import models  # Import all models

# this is the Alembic Config object
config = context.config

# Override sqlalchemy.url with the one from our settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata


EXCLUDED_SCHEMAS = {"tiger", "topology"}
EXCLUDED_TABLES = {
    # PostGIS extension-managed objects (should not be managed by app migrations)
    "spatial_ref_sys",
    "geometry_columns",
    "geography_columns",
    "raster_columns",
    "raster_overviews",
}


def include_object(object_, name: str | None, type_: str, reflected: bool, compare_to) -> bool:
    """Filter objects included in Alembic autogenerate.

    This project uses PostGIS. The `postgis/postgis` Docker image enables extensions like
    `postgis_tiger_geocoder` and `postgis_topology`, which create many extension-managed tables
    in schemas like `tiger` and `topology` (and a few in `public` like `spatial_ref_sys`).

    Those objects must NOT be created/dropped by our app migrations.
    """
    schema = getattr(object_, "schema", None) or "public"

    # Ignore objects that exist in the database but are not represented in SQLAlchemy metadata.
    # This prevents Alembic from generating destructive "drop_*" operations for extension-managed
    # tables (PostGIS tiger/topology, etc.) and any other DB-owned objects.
    if reflected and compare_to is None:
        return False

    if schema in EXCLUDED_SCHEMAS:
        return False

    if type_ == "table" and name in EXCLUDED_TABLES:
        return False

    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_schemas=True,
        include_object=include_object,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
