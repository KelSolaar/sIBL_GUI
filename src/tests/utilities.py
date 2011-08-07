#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**utilities.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Tests utilities Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import sys

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
from umbra.globals.constants import Constants
from umbra.globals.runtimeConstants import RuntimeConstants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

# Starting the console handler.
RuntimeConstants.loggingConsoleHandler = logging.StreamHandler(sys.__stdout__)
RuntimeConstants.loggingConsoleHandler.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
LOGGER.addHandler(RuntimeConstants.loggingConsoleHandler)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
