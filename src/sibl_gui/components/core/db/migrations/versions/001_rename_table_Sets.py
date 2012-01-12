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
import logging
import sibl_gui.components.core.db.utilities.common as dbCommon

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "renameTable", "upgrade", "downgrade"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def renameTable(dbEngine, currrentName, newName):
	"""
	This definition renames given Database table name to given new name.

	:param dbEngine: Database engine. ( Object )
	:param currrentName: Source table name. ( String )
	:param newName: Target table name. ( String )
	:return: Method success. ( Boolean )
	"""

	LOGGER.info("{0} | SQLAlchemy Migrate: Upgrading Database!".format(__name__))

	metadata = sqlalchemy.MetaData()
	metadata.bind = dbEngine
	metadata.reflect(dbEngine)

	if currrentName in metadata.tables:
		LOGGER.info("{0} | SQLAlchemy Migrate: Renaming '{1}' table to '{2}'!".format(__name__, currrentName, newName))
		table = sqlalchemy.Table(currrentName, metadata, autoload=True, autoload_with=dbEngine)
		table.rename(newName)

		sessionMaker = sqlalchemy.orm.sessionmaker(bind=dbEngine)
		session = sessionMaker()

		for collection in dbCommon.getCollectionsByType(session, currrentName):
			LOGGER.info("{0} | SQLAlchemy Migrate: Changing '{1}' Collection type to '{2}'!".format(
			__name__, collection.name, newName))
			collection.type = newName
		dbCommon.commit(session)
		session.close()
	else:
		LOGGER.info("{0} | SQLAlchemy Migrate: '{1}' table name is already up to date!".format(__name__, newName))
	return True

def upgrade(dbEngine):
	"""
	This definition upgrades the Database.

	:param dbEngine: Database engine. ( Object )
	"""

	renameTable(dbEngine, "Sets", "IblSets")

def downgrade(dbEngine):
	"""
	This definition downgrades the Database.

	:param dbEngine: Database engine. ( Object )
	"""

	renameTable(dbEngine, "IblSets", "Sets")
