#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Constants Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import os
import platform

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Constants():
	"""
	This class is the Constants class.
	"""

	applicationName = "sIBL_GUI"
	releaseVersion = "4.0.0"

	logger = "sIBL_GUI_Logger"
	verbosityLevel = 3
	verbosityLabels = ("Critical", "Error", "Warning", "Info", "Debug")
	loggingDefaultFormatter = "Default"
	loggingSeparators = "*" * 96

	encodingFormat = "utf-8"
	encodingError = "ignore"

	applicationDirectory = "sIBL_GUI"
	if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Darwin":
		providerDirectory = "HDRLabs"
	elif platform.system() == "Linux":
		providerDirectory = ".HDRLabs"

	databaseDirectory = "database"
	databaseMigrationsDirectory = "migrations"
	databaseMigrationsFilesDirectory = "versions"
	databaseMigrationsTemplatesDirectory = "templates"
	settingsDirectory = "settings"
	userComponentsDirectory = "components"
	loggingDirectory = "logging"
	templatesDirectory = "templates"
	ioDirectory = "io"

	preferencesDirectories = (databaseDirectory,
								settingsDirectory,
								userComponentsDirectory,
								loggingDirectory,
								templatesDirectory,
								ioDirectory)
	coreComponentsDirectory = "components/core"
	addonsComponentsDirectory = "components/addons"

	databaseFile = "sIBL_Database.sqlite"
	settingsFile = "sIBL_Settings.rc"
	loggingFile = "sIBL_Logging.log"

	databaseMigrationsFilesExtension = "py"

	librariesDirectory = "libraries"
	if platform.system() == "Windows" or platform.system() == "Microsoft":
		freeImageLibrary = os.path.join(librariesDirectory, "freeImage/resources/FreeImage.dll")
	elif platform.system() == "Darwin":
		freeImageLibrary = os.path.join(librariesDirectory, "freeImage/resources/libfreeimage.dylib")
	elif platform.system() == "Linux":
		freeImageLibrary = os.path.join(librariesDirectory, "freeImage/resources/libfreeimage.so")

	defaultTimerCycle = 125
	nullObject = "None"

