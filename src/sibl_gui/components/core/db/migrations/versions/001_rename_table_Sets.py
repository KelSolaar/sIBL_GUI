#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**001_rename_table_Sets.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the *001* version Application Database migrations objects: :func:`upgrade`
	and :func:`downgrade` definitions.

**Others:**

"""

#**********************************************************************************************************************
#*** External imports
#**********************************************************************************************************************
import sqlalchemy
from migrate import *
import logging

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "upgrade", "downgrade"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def upgrade(dbEngine):
	"""
	This definition upgrades the Database.

	:param dbEngine: Database engine. ( Object )
	"""

	LOGGER.info("{0} | SQLAlchemy Migrate: Upgrading Database!".format(__name__))

	metadata = sqlalchemy.MetaData()
	metadata.bind = dbEngine

	currentTableName = "Sets"
	tableName = "IblSets"

	if currentTableName in metadata.tables.keys():
		table = sqlalchemy.Table(currentTableName, metadata, autoload=True, autoload_with=dbEngine)

		LOGGER.info("{0} | SQLAlchemy Migrate: Renaming '{1}' table to '{2}'!".format(__name__, currentTableName, tableName))
		table.rename(tableName)
	else:
		LOGGER.info("{0} | SQLAlchemy Migrate: '{1}' table name is already up to date!".format(__name__, tableName))

def downgrade(dbEngine):
	"""
	This definition downgrades the Database.

	:param dbEngine: Database engine. ( Object )
	"""

	LOGGER.info("{0} | SQLAlchemy Migrate: Downgrading Database!".format(__name__))

	metadata = sqlalchemy.MetaData()
	metadata.bind = dbEngine

	currentTableName = "IblSets"
	tableName = "Sets"

	if currentTableName in metadata.tables.keys():
		table = sqlalchemy.Table(currentTableName, metadata, autoload=True, autoload_with=dbEngine)

		LOGGER.info("{0} | SQLAlchemy Migrate: Renaming '{1}' table to '{2}'!".format(__name__, currentTableName, tableName))
		table.rename(tableName)
