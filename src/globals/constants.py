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
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
************************************************************************************************
***	constants.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Constants Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import os
import platform

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Constants():
	"""
	This Class Is The Constants Class.
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
								ioDirectory
							)
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

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
