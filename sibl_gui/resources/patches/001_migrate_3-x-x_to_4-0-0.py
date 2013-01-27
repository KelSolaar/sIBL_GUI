#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**001_migrate_3-x-x_to_4-0-0.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module migrates sIBL_GUI from 3.x.x to 4.0.0.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import shutil
import sqlalchemy
from PyQt4.QtGui import QMessageBox

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core
import foundations.verbose
import sibl_gui.components.core.database.operations
import umbra.ui.widgets.messageBox
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

UID = "f23bedfa0def170bb6f70f24b4e1b047"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def apply():
	"""
	This definition is called by the Application and triggers the patch execution.

	:return: Definition success. ( Boolean )
	"""

	if RuntimeGlobals.parameters.databaseReadOnly:
		message = "sIBL_GUI is launched with '-r / --databaseReadOnly' parameter preventing database migration!\n\n\
In order to complete the migration, you will need to relaunch sIBL_GUI without the '-r / --databaseReadOnly' parameter!\n\n\
If you are using an already migrated shared database, you can ignore this message!\n\nWould like to continue?"
		if umbra.ui.widgets.messageBox.messageBox("Question",
													"sIBL_GUI | Question",
													message,
													buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
			foundations.core.exit(1)

	if RuntimeGlobals.parameters.databaseReadOnly:
		LOGGER.warning(
		"!> {0} | Database has been set read only by '{1}' command line parameter value!".format(__name__,
																								"databaseReadOnly"))
		return True

	if RuntimeGlobals.parameters.databaseDirectory:
		databaseDirectory = RuntimeGlobals.parameters.databaseDirectory
		legacyDatabaseFile = os.path.join(databaseDirectory, "sIBL_Database.sqlite")
	else:
		databaseDirectory = os.path.join(RuntimeGlobals.userApplicationDataDirectory, Constants.databaseDirectory)
		legacyDatabaseFile = os.path.normpath(os.path.join(RuntimeGlobals.userApplicationDataDirectory,
									"..",
									Constants.databaseDirectory,
									"sIBL_Database.sqlite"))

	if foundations.common.pathExists(legacyDatabaseFile):
		databaseFile = os.path.join(databaseDirectory, Constants.databaseFile)
		message = "A previous sIBL_GUI database file has been found: '{0}'!\n\n\
Would you like to migrate it toward sIBL_GUI 4.0.0?".format(
				legacyDatabaseFile)
		if umbra.ui.widgets.messageBox.messageBox("Question", "sIBL_GUI | Question",
														message,
														buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			try:
				LOGGER.info("{0} | Copying '{1}' database file to '{2}' destination!".format(__name__,
																							legacyDatabaseFile,
																							databaseFile))
				shutil.copyfile(legacyDatabaseFile, databaseFile)
			except:
				message = "{0} | Critical exception raised while copying '{1}' database file to '{2}' destination!\n\n\
sIBL_GUI will now exit!".format(__name__, legacyDatabaseFile, databaseFile)
				umbra.ui.widgets.messageBox.messageBox("Critical", "sIBL_GUI | Critical", message)
				foundations.core.exit(1)

			if RuntimeGlobals.parameters.databaseDirectory:
				deprecatedDatabaseDirectory = os.path.join(databaseDirectory, "backup", "deprecated")
				message = "The previous sIBL_GUI database file will be backuped into the following directory: '{0}'.".format(
				deprecatedDatabaseDirectory)
				umbra.ui.widgets.messageBox.messageBox("Information", "sIBL_GUI | Information", message)
				os.makedirs(deprecatedDatabaseDirectory)
				shutil.move(legacyDatabaseFile,
							os.path.join(deprecatedDatabaseDirectory, os.path.basename(legacyDatabaseFile)))

			databaseEngine = sqlalchemy.create_engine("sqlite:///{0}".format(databaseFile))
			databaseSessionMaker = sqlalchemy.orm.sessionmaker(bind=databaseEngine)
			databaseSession = databaseSessionMaker()
			for template in sibl_gui.components.core.database.operations.getTemplates(databaseSession):
				id = template.id
				LOGGER.info("{0} | Removing deprecated Template with '{1}' id from database!".format(__name__, id))
				sibl_gui.components.core.database.operations.removeTemplate(id, databaseSession)

	return True
