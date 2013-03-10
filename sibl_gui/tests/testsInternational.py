#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module runs the international tests suite.

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
import shutil
import subprocess
import tempfile

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import sibl_gui

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
		"INTERNATIONAL_TEST_SCRIPT_FILE",
		"USER_APPLICATION_DIRECTORY_PREFIX",
		"testsInternational"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
INTERNATIONAL_TEST_SCRIPT_FILE = os.path.join(RESOURCES_DIRECTORY, "internationalScript.py")
USER_APPLICATION_DIRECTORY_PREFIX = "标准"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def testsInternational():
	"""
	This definitions runs the international tests suite.
	
	:return: Definition success. ( Boolean )
	"""

	userApplicationDirectory = tempfile.mkdtemp(prefix=USER_APPLICATION_DIRECTORY_PREFIX)
	command = [os.path.join(sibl_gui.__path__[0], "../bin/sIBL_GUI"),
 			"-u", userApplicationDirectory,
			"-x", unicode(INTERNATIONAL_TEST_SCRIPT_FILE)]
	if subprocess.check_call(command) == 0:
		shutil.rmtree(userApplicationDirectory)

if __name__ == "__main__":
	testsInternational()
