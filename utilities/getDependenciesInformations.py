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
import subprocess
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
from foundations.io import File

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"GIT_EXECUTABLE",
		"FOUNDATIONS_DIRECTORY",
		"MANAGER_DIRECTORY",
		"UMBRA_DIRECTORY"
		"TEMPLATES_DIRECTORY",
		"DEPENDENCIES",
		"DEPENDENCIES_FILE",
		"getDependenciesInformations"]

LOGGER = foundations.verbose.installLogger()

GIT_EXECUTABLE = "/usr/local/git/bin/git"
FOUNDATIONS_DIRECTORY = "../../Foundations"
MANAGER_DIRECTORY = "../../Manager"
UMBRA_DIRECTORY = "../../Umbra"
TEMPLATES_DIRECTORY = "../../sIBL_GUI_Templates"
DEPENDENCIES = OrderedDict((("Foundations", FOUNDATIONS_DIRECTORY),
							("Manager", MANAGER_DIRECTORY),
							("Umbra", UMBRA_DIRECTORY),
							("sIBL_GUI_Templates", TEMPLATES_DIRECTORY)))
DEPENDENCIES_FILE = "../releases/sIBL_GUI_Dependencies.rc"

LOGGER = foundations.verbose.installLogger()
foundations.verbose.getLoggingConsoleHandler()
foundations.verbose.setVerbosityLevel(3)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getDependenciesInformations():
	"""
	This definition gets sIBL_GUI dependencies informations file.
	"""

	content = ["[Dependencies]\n"]
	for dependency, path in DEPENDENCIES.iteritems():
		release = subprocess.Popen("cd {0} && {1} describe".format(path, GIT_EXECUTABLE),
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
