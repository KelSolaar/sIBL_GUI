#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**003_migrate_4-x-x_to_4-0-3.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module migrates sIBL_GUI from 4.x.x to 4.0.3.

**Others:**

"""

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
import umbra.ui.widgets.messageBox
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UID", "apply"]

LOGGER = foundations.verbose.installLogger()

UID = "97DD5A8BEA1E9CA5F849754730C4EEB3"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def apply():
	"""
	This definition is called by the Application and triggers the patch execution.

	:return: Definition success. ( Boolean )
	"""

	umbra.ui.widgets.messageBox.messageBox("Information",
	"sIBL_GUI | Message",
	"Hello!\n\nUpon startup and from now on, sIBL_GUI will attempt to connect to \
https://www.crittercism.com/ to report unhandled exceptions whenever they occur!\n\nThis message will only display once!")

	defaultScriptEditorDirectory = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
														Constants.ioDirectory,
														"scriptEditor")
	defaultScriptEditorFile = os.path.join(defaultScriptEditorDirectory, "defaultScript.py")

	if foundations.common.pathExists(defaultScriptEditorFile):
		LOGGER.info("{0} | Removing deprecated '{1}' default script file!".format(__name__, defaultScriptEditorFile))
		os.remove(defaultScriptEditorFile)
	return True
