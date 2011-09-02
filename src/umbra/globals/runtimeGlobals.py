#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**RuntimeGlobals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Umbra** package runtime constants through the :class:`RuntimeGlobals` class.

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
class RuntimeGlobals():
	"""
	This class provides **Umbra** package runtime constants.
	"""

	parameters = None
	"""Application startup parameters."""
	args = None
	"""Application startup arguments."""

	loggingConsoleHandler = None
	"""Logging console handler instance."""
	loggingFileHandler = None
	"""Logging file handler instance."""
	loggingSessionHandler = None
	"""Logging session handler instance."""
	loggingSessionHandlerStream = None
	"""Logging session handler stream."""
	loggingFormatters = None
	"""Logging formatters."""
	loggingActiveFormatter = None
	"""Logging current formatter."""

	verbosityLevel = None
	"""Logging current verbosity level."""
	loggingFile = None
	"""Application logging file."""

	application = None
	"""Application instance."""
	userApplicationDatasDirectory = None
	"""Application user datas directory."""

	resourcesPaths = []
	"""Resources paths."""

	uiFile = None
	"""Application ui file."""
	ui = None
	"""Application ui instance."""

	settingsFile = None
	"""Application settings file."""
	settings = None
	"""Application settings instance."""

	splashscreenImage = None
	"""Application splashscreen picture."""
	splashscreen = None
	"""Application splashscreen instance."""
