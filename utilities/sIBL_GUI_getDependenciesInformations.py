#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#

"""
************************************************************************************************
***	sIBL_GUI_getDependenciesInformations.py
***
***	Platform:
***		Windows
***
***	Description:
***		Get Dependencies Informations.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************
#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import subprocess
import sys
from collections import OrderedDict

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
from foundations.io import File
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

LOGGING_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
LOGGING_CONSOLE_HANDLER.setFormatter(core.LOGGING_FORMATTER)
LOGGER.addHandler(LOGGING_CONSOLE_HANDLER)

core.setVerbosityLevel(3)

FOUNDATIONS_DIRECTORY = "../../Foundations"
MANAGER_DIRECTORY = "../../Manager"
TEMPLATES_DIRECTORY = "../../sIBL_GUI_Templates"
DEPENDENCIES = OrderedDict((("Foundations", FOUNDATIONS_DIRECTORY), ("Manager", MANAGER_DIRECTORY), ("sIBL_GUI_Templates", TEMPLATES_DIRECTORY)))
DEPENDENCIES_FILE = "../releases/sIBL_GUI_Dependencies.rc"

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def getDependenciesInformations():
	content = ["[Dependencies]\n"]
	for dependency, path in DEPENDENCIES.items():
		release = subprocess.Popen("cd {0} && /opt/local/bin/git describe".format(path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
		LOGGER.info("{0} | '{1}': '{2}'.".format(getDependenciesInformations.__name__, dependency, release.strip()))
		content.append("{0}={1}".format(dependency, release))
	file = File(DEPENDENCIES_FILE)
	file.content = content
	file.write()

if __name__ == "__main__":
	getDependenciesInformations()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
