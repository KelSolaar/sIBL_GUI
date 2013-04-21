#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**004_migrate_4-x-x_to_4-0-7.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module migrates sIBL_GUI from 4.x.x to 4.0.7.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.schema import DropTable
from sqlalchemy.schema import MetaData
from sqlalchemy.schema import Table

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.verbose
import sibl_gui.components.core.database.operations
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UID", "apply"]

LOGGER = foundations.verbose.installLogger()

UID = "ddfd9d292ea73aa3450989af7d7ee945"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def apply():
	"""
	This definition is called by the Application and triggers the patch execution.

	:return: Definition success. ( Boolean )
	"""

	databaseDirectory = os.path.join(RuntimeGlobals.userApplicationDataDirectory, Constants.databaseDirectory)

	migrationsDirectory = os.path.join(databaseDirectory, "migrations")
	if foundations.common.pathExists(migrationsDirectory):
		foundations.io.remove(migrationsDirectory)

	databaseFile = os.path.join(databaseDirectory, Constants.databaseFile)
	engine = create_engine("sqlite:///{0}".format(databaseFile))
	connection = engine.connect()
	transaction = connection.begin()
	inspector = reflection.Inspector.from_engine(engine)
	metadata = MetaData()
	for name in inspector.get_table_names():
		if name in ("Migrate", "{{ locals().pop('version_table') }}"):
			connection.execute(DropTable(Table(name, metadata)))
	transaction.commit()

	return True
