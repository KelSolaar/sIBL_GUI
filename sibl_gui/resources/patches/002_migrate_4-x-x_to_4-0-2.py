#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**002_migrate_4-x-x_to_4-0-2.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Migrates sIBL_GUI from 4.x.x to 4.0.2.

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

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core
import foundations.verbose
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UID", "apply"]

LOGGER = foundations.verbose.install_logger()

UID = "00fd997f2a2c395b59aa31f1997f831b"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def apply():
	"""
	Triggers the patch execution.

	:return: Definition success.
	:rtype: bool
	"""

	default_script_editor_directory = os.path.join(RuntimeGlobals.user_application_data_directory,
														Constants.io_directory,
														"script_editor")
	default_script_editor_file = os.path.join(default_script_editor_directory, "default_script.py")

	if foundations.common.path_exists(default_script_editor_file):
		LOGGER.info("{0} | Removing deprecated '{1}' default script file!".format(__name__, default_script_editor_file))
		os.remove(default_script_editor_file)
	return True
