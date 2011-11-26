#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**getDependenciesInformations.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Get dependencies informations.

**Others:**

"""
#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import subprocess
import sys
from collections import OrderedDict

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
from foundations.io import File
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

LOGGING_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
LOGGING_CONSOLE_HANDLER.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
LOGGER.addHandler(LOGGING_CONSOLE_HANDLER)

core.setVerbosityLevel(3)

GIT_EXECUTABLE = "/usr/local/git/bin/git"
FOUNDATIONS_DIRECTORY = "../../Foundations"
MANAGER_DIRECTORY = "../../Manager"
TEMPLATES_DIRECTORY = "../../sIBL_GUI_Templates"
DEPENDENCIES = OrderedDict((("Foundations", FOUNDATIONS_DIRECTORY),
							("Manager", MANAGER_DIRECTORY), ("sIBL_GUI_Templates", TEMPLATES_DIRECTORY)))
DEPENDENCIES_FILE = "../releases/sIBL_GUI_Dependencies.rc"

#**********************************************************************************************************************
#***	Main Python code.
#**********************************************************************************************************************
def getDependenciesInformations():
	"""
	This definition gets sIBL_GUI dependencies informations file.
	"""

	content = ["[Dependencies]\n"]
	for dependency, path in DEPENDENCIES.items():
		release = subprocess.Popen("cd {0} &&  {1} describe".format(path, GIT_EXECUTABLE),
									shell=True,
									stdout=subprocess.PIPE,
									stderr=subprocess.PIPE).communicate()[0]
		LOGGER.info("{0} | '{1}': '{2}'.".format(getDependenciesInformations.__name__, dependency, release.strip()))
		content.append("{0}={1}".format(dependency, release))
	file = File(DEPENDENCIES_FILE)
	file.content = content
	file.write()

if __name__ == "__main__":
	getDependenciesInformations()
