#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**runtimeConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Runtime constants Module.

**Others:**

"""

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
class RuntimeConstants():
	"""
	This class is the **RuntimeConstants** class.
	"""

	parameters = None
	args = None

	loggingConsoleHandler = None
	loggingFileHandler = None
	loggingSessionHandler = None
	loggingSessionHandlerStream = None
	loggingFormatters = None
	loggingActiveFormatter = None

	verbosityLevel = None
	loggingFile = None

	application = None
	userApplicationDatasDirectory = None

	uiFile = None
	ui = None

	settingsFile = None
	settings = None

	splashscreenPicture = None
	splashscreen = None

