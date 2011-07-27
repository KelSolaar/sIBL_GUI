#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**001_table_Sets_sqlalchemy.Column_previewImage.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Database migration Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

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
#***	Overall variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
def upgrade(dbEngine):
	"""
	This definition upgrades the Database.

	@param dbEngine: Database engine. ( Object )
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

	@param dbEngine: Database engine. ( Object )
	"""

	pass

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
