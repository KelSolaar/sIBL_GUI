#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Umbra** package default constants through the :class:`Constants` class.

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
	This class provides **Umbra** package default constants.
	"""

	applicationName = "Umbra"
	"""Package Application name: '**Umbra**' ( String )"""
	releaseVersion = "1.0.0"
	"""Package release version: '**1.0.0**' ( String )"""

	logger = "Umbra_Logger"
	"""Package logger name: '**Umbra_Logger**' ( String )"""
	verbosityLevel = 3
	"""Default logging verbosity level: '**3**' ( Integer )"""
	verbosityLabels = ("Critical", "Error", "Warning", "Info", "Debug")
	"""Logging verbosity labels: ('**Critical**', '**Error**', '**Warning**', '**Info**', '**Debug**') ( Tuple )"""
	loggingDefaultFormatter = "Default"
	"""Default logging formatter name: '**Default**' ( String )"""
	loggingSeparators = "*" * 96
	"""Logging separators: '*' * 96 ( String )"""

	encodingFormat = "utf-8"
	"""Default encoding format: '**utf-8**' ( String )"""
	encodingError = "ignore"
	"""Default encoding error behavior: '**ignore**' ( String )"""

	applicationDirectory = "Umbra"
	"""Package Application directory: '**Umbra**' ( String )"""
	if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Darwin":
		providerDirectory = "HDRLabs"
		"""Package provider directory: '**HDRLabs** on Windows / Darwin, **.HDRLabs** on Linux' ( String )"""
	elif platform.system() == "Linux":
		providerDirectory = ".HDRLabs"
		"""Package provider directory: '**HDRLabs** on Windows / Darwin, **.HDRLabs** on Linux' ( String )"""

	settingsDirectory = "settings"
	"""Application settings directory: '**settings**' ( String )"""
	userComponentsDirectory = "components"
	"""Application user components directory: '**components**' ( String )"""
	loggingDirectory = "logging"
	"""Application logging directory: '**logging**' ( String )"""
	ioDirectory = "io"
	"""Application io directory: '**io**' ( String )"""

	preferencesDirectories = (settingsDirectory,
								userComponentsDirectory,
								loggingDirectory,
								ioDirectory)
	"""Application preferences directories ( Tuple )"""

	factoryComponentsDirectory = "components/factory"
	"""Application core components directory: '**components/factory**' ( String )"""

	settingsFile = "Umbra_Settings.rc"
	"""Application settings file: '**Umbra_Settings.rc**' ( String )"""
	loggingFile = "Umbra_Logging.log"
	"""Application logging file: '**Umbra_Logging.log**' ( String )"""

	librariesDirectory = "libraries"
	"""Application libraries directory: '**libraries**' ( String )"""
	if platform.system() == "Windows" or platform.system() == "Microsoft":
		freeImageLibrary = os.path.join(librariesDirectory, "freeImage/resources/FreeImage.dll")
		"""FreeImage library path: '**freeImage/resources/FreeImage.dll** on Windows, '**freeImage/resources/libfreeimage.dylib** on Darwin, **freeImage/resources/libfreeimage.so** on Linux' ( String )"""
	elif platform.system() == "Darwin":
		freeImageLibrary = os.path.join(librariesDirectory, "freeImage/resources/libfreeimage.dylib")
		"""FreeImage library path: '**freeImage/resources/FreeImage.dll** on Windows, '**freeImage/resources/libfreeimage.dylib** on Darwin, **freeImage/resources/libfreeimage.so** on Linux' ( String )"""
	elif platform.system() == "Linux":
		freeImageLibrary = os.path.join(librariesDirectory, "freeImage/resources/libfreeimage.so")
		"""FreeImage library path: '**freeImage/resources/FreeImage.dll** on Windows, '**freeImage/resources/libfreeimage.dylib** on Darwin, **freeImage/resources/libfreeimage.so** on Linux' ( String )"""

	defaultTimerCycle = 125
	"""Default timer cycle length in milliseconds: '**125**' ( Integer )"""
	nullObject = "None"
	"""Default null object string: '**None**' ( String )"""
