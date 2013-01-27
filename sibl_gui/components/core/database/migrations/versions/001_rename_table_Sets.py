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
import sibl_gui.components.core.database.operations

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

__all__ = ["LOGGER", "renameTable", "upgrade", "downgrade"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def renameTable(databaseEngine, currrentName, newName):
	"""
	This definition renames given Database table name to given new name.

	:param databaseEngine: Database engine. ( Object )
	:param currrentName: Source table name. ( String )
	:param newName: Target table name. ( String )
	:return: Method success. ( Boolean )
	"""

	LOGGER.info("{0} | SQLAlchemy Migrate: Upgrading Database!".format(__name__))

	metadata = sqlalchemy.MetaData()
	metadata.bind = databaseEngine
	metadata.reflect(databaseEngine)

	if currrentName in metadata.tables:
		LOGGER.info("{0} | SQLAlchemy Migrate: Renaming '{1}' table to '{2}'!".format(__name__, currrentName, newName))
		table = sqlalchemy.Table(currrentName, metadata, autoload=True, autoload_with=databaseEngine)
		table.rename(newName)

		sessionMaker = sqlalchemy.orm.sessionmaker(bind=databaseEngine)
		session = sessionMaker()

		for collection in sibl_gui.components.core.database.operations.getCollectionsByType(currrentName, session):
			LOGGER.info("{0} | SQLAlchemy Migrate: Changing '{1}' Collection type to '{2}'!".format(
			__name__, collection.name, newName))
			collection.type = newName
		sibl_gui.components.core.database.operations.commit(session)
		session.close()
	else:
		LOGGER.info("{0} | SQLAlchemy Migrate: '{1}' table name is already up to date!".format(__name__, newName))
	return True

def upgrade(databaseEngine):
	"""
	This definition upgrades the Database.

	:param databaseEngine: Database engine. ( Object )
	"""

	renameTable(databaseEngine, "Sets", "IblSets")

def downgrade(databaseEngine):
	"""
	This definition downgrades the Database.

	:param databaseEngine: Database engine. ( Object )
	"""

	renameTable(databaseEngine, "IblSets", "Sets")
