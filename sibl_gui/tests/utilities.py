#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**utilities.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines tests suite logging configuration.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import sys

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER"]

LOGGER = logging.getLogger(Constants.logger)

# Starting the console handler.
RuntimeGlobals.loggingConsoleHandler = logging.StreamHandler(sys.__stdout__)
RuntimeGlobals.loggingConsoleHandler.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
LOGGER.addHandler(RuntimeGlobals.loggingConsoleHandler)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
