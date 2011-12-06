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

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
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

UID = "6476c4d6da7ea194cc25a6b4b5efb06f"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def apply():
	"""
	This definition is called by the Application and triggers the patch execution.

	:return: Definition success. ( Boolean )
	"""

	userApplicationDataDirectory = RuntimeGlobals.userApplicationDataDirectory
	if foundations.common.pathExists(userApplicationDataDirectory):
		legacySettingsFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
												Constants.settingsDirectory,
												"sIBL_Settings.rc")
		if foundations.common.pathExists(legacySettingsFile):
			LOGGER.warning("!> {0} | Removing deprecated '{1}' settings file!".format(
			core.getModule(apply).__name__, legacySettingsFile))
			os.remove(legacySettingsFile)

		legacyLoggingFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
												Constants.loggingDirectory,
												"sIBL_Logging.log")
		if foundations.common.pathExists(legacyLoggingFile):
			LOGGER.warning("!> {0} | Removing deprecated '{1}' logging file!".format(
			core.getModule(apply).__name__, legacyLoggingFile))
			os.remove(legacyLoggingFile)

		legacyDatabaseFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
												Constants.databaseDirectory,
												"sIBL_Database.sqlite")
		if foundations.common.pathExists(legacyDatabaseFile):
			LOGGER.warning("!> {0} | Renaming '{1}' database file!".format(
			core.getModule(apply).__name__, legacyDatabaseFile))
			os.rename(legacyDatabaseFile, os.path.join(os.path.dirname(legacyDatabaseFile), Constants.databaseFile))

	return True
