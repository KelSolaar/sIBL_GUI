#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**001_table_Sets_sqlalchemy.Column_previewImage.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Database migration Module.

**Others:**

"""

#***********************************************************************************************
#*** External imports
#***********************************************************************************************
import sqlalchemy
from migrate import *
import logging

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
def upgrade(dbEngine):
	"""
	This definition upgrades the Database.

	:param dbEngine: Database engine. ( Object )
	"""

	LOGGER.info("{0} | SQLAlchemy Migrate: Upgrading Database!".format(__name__))

	metadata = sqlalchemy.MetaData()
	metadata.bind = dbEngine
	table = sqlalchemy.Table("Sets", metadata, autoload=True, autoload_with=dbEngine)

	columnName = "previewImage"
	if columnName not in table.columns:
		LOGGER.info("{0} | SQLAlchemy Migrate: Adding '{1}' column to '{2}' table!".format(__name__, columnName, table))
		column = sqlalchemy.Column(columnName, sqlalchemy.String)
		column.create(table)
	else:
		LOGGER.info("{0} | SQLAlchemy Migrate: Column '{1}' already exists in '{2}' table!".format(__name__, columnName, table))

def downgrade(dbEngine):
	"""
	This definition downgrades the Database.

	:param dbEngine: Database engine. ( Object )
	"""

	pass

