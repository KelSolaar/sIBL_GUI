#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **sIBL_GUI** package default constants through the :class:`Constants` class.

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
import platform

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import sibl_gui

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["Constants"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Constants():
	"""
	Defines **sIBL_GUI** package default constants.
	"""

	applicationName = "sIBL_GUI"
	"""
	:param applicationName: Package Application name.
	:type applicationName: unicode
	"""
	majorVersion = "4"
	"""
	:param majorVersion: Package major version.
	:type majorVersion: unicode
	"""
	minorVersion = "0"
	"""
	:param minorVersion: Package minor version.
	:type minorVersion: unicode
	"""
	changeVersion = "8"
	"""
	:param changeVersion: Package change version.
	:type changeVersion: unicode
	"""
	version = ".".join((majorVersion, minorVersion, changeVersion))
	"""
	:param version: Package version.
	:type version: unicode
	"""

	logger = "sIBL_GUI_Logger"
	"""
	:param logger: Package logger name.
	:type logger: unicode
	"""

	defaultCodec = sibl_gui.DEFAULT_CODEC
	"""
	:param defaultCodec: Default codec.
	:type defaultCodec: unicode
	"""
	codecError = sibl_gui.CODEC_ERROR
	"""
	:param codecError: Default codec error behavior.
	:type codecError: unicode
	"""

	applicationDirectory = os.sep.join(("sIBL_GUI", ".".join((majorVersion, minorVersion))))
	"""
	:param applicationDirectory: Package Application directory.
	:type applicationDirectory: unicode
	"""
	if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Darwin":
		providerDirectory = "HDRLabs"
		"""
		:param providerDirectory: Package provider directory.
		:type providerDirectory: unicode
		"""
	elif platform.system() == "Linux":
		providerDirectory = ".HDRLabs"
		"""
		:param providerDirectory: Package provider directory.
		:type providerDirectory: unicode
		"""

	databaseDirectory = "database"
	"""
	:param databaseDirectory: Application Database directory.
	:type databaseDirectory: unicode
	"""
	patchesDirectory = "patches"
	"""
	:param patchesDirectory: Application patches directory.
	:type patchesDirectory: unicode
	"""
	settingsDirectory = "settings"
	"""
	:param settingsDirectory: Application settings directory.
	:type settingsDirectory: unicode
	"""
	userComponentsDirectory = "components"
	"""
	:param userComponentsDirectory: Application user components directory.
	:type userComponentsDirectory: unicode
	"""
	loggingDirectory = "logging"
	"""
	:param loggingDirectory: Application logging directory.
	:type loggingDirectory: unicode
	"""
	templatesDirectory = "templates"
	"""
	:param templatesDirectory: Application templates directory.
	:type templatesDirectory: unicode
	"""
	ioDirectory = "io"
	"""
	:param ioDirectory: Application io directory.
	:type ioDirectory: unicode
	"""

	preferencesDirectories = (databaseDirectory,
								patchesDirectory,
								settingsDirectory,
								userComponentsDirectory,
								loggingDirectory,
								templatesDirectory,
								ioDirectory)
	"""
	:param preferencesDirectories: Application preferences directories.
	:type preferencesDirectories: tuple
	"""

	coreComponentsDirectory = "components/core"
	"""
	:param coreComponentsDirectory: Application core components directory.
	:type coreComponentsDirectory: unicode
	"""
	addonsComponentsDirectory = "components/addons"
	"""
	:param addonsComponentsDirectory: Application addons components directory.
	:type addonsComponentsDirectory: unicode
	"""

	resourcesDirectory = "resources"
	"""
	:param resourcesDirectory: Application resources directory.
	:type resourcesDirectory: unicode
	"""

	patchesFile = "sIBL_GUI_Patches.rc"
	"""
	:param patchesFile: Application settings file.
	:type patchesFile: unicode
	"""
	databaseFile = "sIBL_GUI_Database.sqlite"
	"""
	:param databaseFile: Application Database file.
	:type databaseFile: unicode
	"""
	settingsFile = "sIBL_GUI_Settings.rc"
	"""
	:param settingsFile: Application settings file.
	:type settingsFile: unicode
	"""
	loggingFile = "sIBL_GUI_Logging_{0}.log"
	"""
	:param loggingFile: Application logging file.
	:type loggingFile: unicode
	"""

	databaseMigrationsFilesExtension = "py"
	"""
	:param databaseMigrationsFilesExtension: Application Database migrations files extension.
	:type databaseMigrationsFilesExtension: unicode
	"""

	librariesDirectory = "libraries"
	"""
	:param librariesDirectory: Application libraries directory.
	:type librariesDirectory: unicode
	"""
	if platform.system() == "Windows" or platform.system() == "Microsoft":
		freeImageLibrary = os.path.join(librariesDirectory, "freeImage/resources/FreeImage.dll")
		"""FreeImage library path: '**freeImage/resources/FreeImage.dll** on Windows,
		**freeImage/resources/libfreeimage.dylib** on Darwin,
		**freeImage/resources/libfreeimage.so** on Linux' ( String )"""
	elif platform.system() == "Darwin":
		freeImageLibrary = os.path.join(librariesDirectory, "freeImage/resources/libfreeimage.dylib")
		"""FreeImage library path: '**freeImage/resources/FreeImage.dll** on Windows,
		**freeImage/resources/libfreeimage.dylib** on Darwin,
		**freeImage/resources/libfreeimage.so** on Linux' ( String )"""
	elif platform.system() == "Linux":
		freeImageLibrary = os.path.join(librariesDirectory, "freeImage/resources/libfreeimage.so")
		"""FreeImage library path: '**freeImage/resources/FreeImage.dll** on Windows,
		**freeImage/resources/libfreeimage.dylib** on Darwin,
		**freeImage/resources/libfreeimage.so** on Linux' ( String )"""
