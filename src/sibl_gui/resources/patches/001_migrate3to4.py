#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**001_migrate3to4.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module migrates sIBL_GUI from 3.x.x to 4.0.0.

**Others:**

"""
#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import shutil
import sqlalchemy
from PyQt4.QtGui import QMessageBox

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import sibl_gui.components.core.db.utilities.common as dbCommon
import umbra.ui.widgets.messageBox
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UID", "apply"]

LOGGER = logging.getLogger(Constants.logger)

UID = "0c9b1019275b1f34bd0f7f578f56aa63"

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
		if umbra.ui.widgets.messageBox.standaloneMessageBox("Question",
																"sIBL_GUI | Question",
																message,
																buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
			foundations.common.exit(1)

	userApplicationDataDirectory = RuntimeGlobals.userApplicationDataDirectory
	if foundations.common.pathExists(userApplicationDataDirectory):
		# 'sIBL_Settings.rc' file.		
		legacySettingsFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
												Constants.settingsDirectory,
												"sIBL_Settings.rc")
		if foundations.common.pathExists(legacySettingsFile):
			LOGGER.info("{0} | Removing deprecated '{1}' settings file!".format(
			core.getModule(apply).__name__, legacySettingsFile))
			os.remove(legacySettingsFile)

		# 'sIBL_Logging.log' file.
		legacyLoggingFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
												Constants.loggingDirectory,
												"sIBL_Logging.log")
		if foundations.common.pathExists(legacyLoggingFile):
			LOGGER.info("{0} | Removing deprecated '{1}' logging file!".format(
			core.getModule(apply).__name__, legacyLoggingFile))
			os.remove(legacyLoggingFile)

	# 'sIBL_Database.sqlite' file.
	if RuntimeGlobals.parameters.databaseReadOnly:
		LOGGER.warning("!> {0} | Database has been set read only by '{1}' command line parameter value!".format(
		core.getModule(apply).__name__, "databaseReadOnly"))
		return True

	if RuntimeGlobals.parameters.databaseDirectory:
		databaseDirectory = RuntimeGlobals.parameters.databaseDirectory
	else:
		databaseDirectory = os.path.join(RuntimeGlobals.userApplicationDataDirectory, Constants.databaseDirectory)
	legacyDatabaseFile = os.path.join(databaseDirectory, "sIBL_Database.sqlite")
	backupDirectory = os.path.join(databaseDirectory, "backup")

	if foundations.common.pathExists(legacyDatabaseFile):
		LOGGER.info("{0} | Renaming '{1}' database file!".format(
		core.getModule(apply).__name__, legacyDatabaseFile))
		databaseFile = os.path.join(os.path.dirname(legacyDatabaseFile), Constants.databaseFile)
		os.rename(legacyDatabaseFile, databaseFile)

		if foundations.common.pathExists(backupDirectory):
			items = [os.path.join(backupDirectory, item) for item in os.listdir(backupDirectory)]
			for item in items:
				if not  os.path.isfile(item):
					continue

				LOGGER.info("{0} | Renaming '{1}' backup database file!".format(core.getModule(apply).__name__, item))
				os.rename(item, item.replace("sIBL_Database", "sIBL_GUI_Database"))

			deprecatedDatabaseDirectory = os.path.join(backupDirectory, "deprecated")
			os.makedirs(os.path.join(backupDirectory, deprecatedDatabaseDirectory))
			deprecatedDatabaseFile = os.path.join(deprecatedDatabaseDirectory, os.path.basename(databaseFile))
			message = "A deprecated database file has been found and will be backuped in the following directory: '{0}'.".format(
			deprecatedDatabaseDirectory)
			umbra.ui.widgets.messageBox.standaloneMessageBox("Information", "sIBL_GUI | Information", message)
			shutil.copyfile(databaseFile, deprecatedDatabaseFile)

		dbEngine = sqlalchemy.create_engine("sqlite:///{0}".format(databaseFile))
		dbSessionMaker = sqlalchemy.orm.sessionmaker(bind=dbEngine)
		dbSession = dbSessionMaker()
		for template in dbCommon.getTemplates(dbSession):
			id = template.id
			LOGGER.info("{0} | Removing deprecated Template with '{1}' id from database!".format(
			core.getModule(apply).__name__, id))
			dbCommon.removeTemplate(dbSession, id)

	return True
