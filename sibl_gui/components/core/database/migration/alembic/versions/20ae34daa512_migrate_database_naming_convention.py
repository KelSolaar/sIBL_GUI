#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**20ae34daa512_migrate_database_naming_convention.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Migrates database naming convention from *camelCase* to *underscore_case*.

**Others:**
    Revises: 10df7481424c
    Creation date: 2014-04-26 21:24:17.051461
"""

import sqlalchemy
from alembic import op

from sibl_gui.components.core.database.migration.alembic.common import rename_column

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["revision", "down_revision", "upgrade", "downgrade"]

revision = "20ae34daa512"
down_revision = "10df7481424c"

def upgrade():
    """
    Upgrade the database to current revision.
    """

    # Renaming tables.
    op.rename_table("Collections", "_Collections")
    op.rename_table("_Collections", "collections")

    op.rename_table("IblSets", "ibl_sets")

    op.rename_table("Templates", "_Templates")
    op.rename_table("_Templates", "templates")

    # Renaming columns.
    rename_column("ibl_sets", "osStats", "os_stats")
    rename_column("ibl_sets", "previewImage", "preview_image")
    rename_column("ibl_sets", "backgroundImage", "background_image")
    rename_column("ibl_sets", "lightingImage", "lighting_image")
    rename_column("ibl_sets", "reflectionImage", "reflection_image")

    rename_column("templates", "osStats", "os_stats")
    rename_column("templates", "helpFile", "help_file")
    rename_column("templates", "outputScript", "output_script")

    # Updating columns data.
    collections = sqlalchemy.sql.table("collections", sqlalchemy.sql.column("type", sqlalchemy.String))
    op.execute(collections.update().where(
        collections.c.type == op.inline_literal("IblSets")).values({"type": op.inline_literal("ibl_sets")}))
    op.execute(collections.update().where(
        collections.c.type == op.inline_literal("Templates")).values({"type": op.inline_literal("templates")}))

def downgrade():
    """
    Downgrade the database to previous revision.
    """

    # Renaming tables.
    op.rename_table("collections", "_Collections")
    op.rename_table("_Collections", "Collections")

    op.rename_table("ibl_sets", "IblSets")

    op.rename_table("templates", "_Templates")
    op.rename_table("_Templates", "Templates")

    # Renaming columns.
    rename_column("IblSets", "os_stats", "osStats")
    rename_column("IblSets", "preview_image", "previewImage")
    rename_column("IblSets", "background_image", "backgroundImage")
    rename_column("IblSets", "lighting_image", "lightingImage")
    rename_column("IblSets", "reflection_image", "reflectionImage")

    rename_column("Templates", "os_stats", "osStats")
    rename_column("Templates", "help_file", "helpFile")
    rename_column("Templates", "output_script", "outputScript")

    # Updating columns data.
    collections = sqlalchemy.sql.table("Collections", sqlalchemy.sql.column("type", sqlalchemy.String))
    op.execute(collections.update().where(
        collections.c.type == op.inline_literal("ibl_sets")).values({"type": op.inline_literal("IblSets")}))
    op.execute(collections.update().where(
        collections.c.type == op.inline_literal("templates")).values({"type": op.inline_literal("Templates")}))
