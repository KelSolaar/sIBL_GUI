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
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Resources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**001_table_Sets_sqlalchemy.Column_previewImage.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Database Migration Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin.
#***********************************************************************************************

#***********************************************************************************************
#*** External Imports
#***********************************************************************************************
import sqlalchemy
from migrate import *
import logging

#***********************************************************************************************
#***	Internal Imports.
#***********************************************************************************************
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions.
#***********************************************************************************************
def upgrade(dbEngine):
	"""
	This Definition Upgrades The Database.

	@param dbEngine: Database Engine. ( Object )
	"""

	LOGGER.info("{0} | SQLAlchemy Migrate: Upgrading Database!".format(__name__))

	metadata = sqlalchemy.MetaData()
	metadata.bind = dbEngine
	table = sqlalchemy.Table("Sets", metadata, autoload=True, autoload_with=dbEngine)

	columnName = "previewImage"
	if columnName not in table.columns:
		LOGGER.info("{0} | SQLAlchemy Migrate: Adding '{1}' Column To '{2}' Table!".format(__name__, columnName, table))
		column = sqlalchemy.Column(columnName, sqlalchemy.String)
		column.create(table)
	else:
		LOGGER.info("{0} | SQLAlchemy Migrate: Column '{1}' Already Exists In '{2}' Table!".format(__name__, columnName, table))

def downgrade(dbEngine):
	"""
	This Definition Downgrades The Database.

	@param dbEngine: Database Engine. ( Object )
	"""

	pass

#***********************************************************************************************
#***	Python End.
#***********************************************************************************************
