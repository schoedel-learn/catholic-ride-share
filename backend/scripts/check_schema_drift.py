"""Fail if SQLAlchemy models drift from the live database schema.

This is a safety rail to preserve the rule: "no model changes without Alembic migrations".

It compares `app.db.session.Base.metadata` against the connected database using Alembic's
autogenerate diff engine (without writing any migration files).

Usage (Docker):
  docker-compose run --rm backend python scripts/check_schema_drift.py

Exit codes:
  0 - no drift detected
  1 - drift detected (you probably forgot to create/apply a migration)
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import create_engine

# Ensure `import app` works when running as a script (e.g., `python scripts/...`).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings
from app.db.session import Base
from app import models as _models  # noqa: F401  # ensure models are imported and registered


EXCLUDED_SCHEMAS = {"tiger", "topology"}
EXCLUDED_TABLES = {
    "spatial_ref_sys",
    "geometry_columns",
    "geography_columns",
    "raster_columns",
    "raster_overviews",
}


def include_object(object_: Any, name: str | None, type_: str, reflected: bool, compare_to: Any) -> bool:
    """Match Alembic env.py behavior: only manage app-owned metadata objects."""
    schema = getattr(object_, "schema", None) or "public"

    # Ignore DB-only objects (extensions, etc.) so we don't flag them as drift.
    if reflected and compare_to is None:
        return False

    if schema in EXCLUDED_SCHEMAS:
        return False

    if type_ == "table" and name in EXCLUDED_TABLES:
        return False

    return True


def main() -> int:
    """Run drift detection against the configured database."""
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        mc = MigrationContext.configure(
            connection,
            opts={
                "include_schemas": True,
                "include_object": include_object,
                "compare_type": True,
                "compare_server_default": True,
            },
        )
        diffs = compare_metadata(mc, Base.metadata)

    if not diffs:
        print("No schema drift detected.")
        return 0

    print("Schema drift detected between SQLAlchemy models and the live database.")
    print("Create/apply an Alembic migration before merging changes.\n")
    for diff in diffs:
        print(diff)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())


