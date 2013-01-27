#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**002_add_table_Sets_Column_previewImage.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the *002* version Application Database migrations objects: :func:`upgrade`
	and :func:`downgrade` definitions.

**Others:**

"""

#**********************************************************************************************************************
#*** External imports
#**********************************************************************************************************************
import sqlalchemy

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "upgrade", "downgrade"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def upgrade(databaseEngine):
	"""
	This definition upgrades the Database.

	:param databaseEngine: Database engine. ( Object )
	"""

	LOGGER.info("{0} | SQLAlchemy Migrate: Upgrading Database!".format(__name__))

	metadata = sqlalchemy.MetaData()
	metadata.bind = databaseEngine

	tableName = "IblSets"

	table = sqlalchemy.Table(tableName, metadata, autoload=True, autoload_with=databaseEngine)

	columnName = "previewImage"
	if columnName not in table.columns:
		LOGGER.info("{0} | SQLAlchemy Migrate: Adding '{1}' column to '{2}' table!".format(__name__, columnName, table))
		column = sqlalchemy.Column(columnName, sqlalchemy.String)
		column.create(table)
	else:
		LOGGER.info("{0} | SQLAlchemy Migrate: Column '{1}' already exists in '{2}' table!".format(__name__,
																									columnName, table))
def downgrade(databaseEngine):
	"""
	This definition downgrades the Database.

	:param databaseEngine: Database engine. ( Object )
	"""

	pass
