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
**sIBL_GUI_getSphinxDocumentationApi.py

**Platform:**
	Windows.

**Description:**
	Gets Sphinx Documentation Toc Tree File.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************
#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import importlib
import logging
import os
import pyclbr
import re
import sys

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.strings as strings
from foundations.io import File
from foundations.globals.constants import Constants
from foundations.walker import Walker

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries"))
print os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries")
import python.pyclbr as moduleBrowser

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

LOGGING_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
LOGGING_CONSOLE_HANDLER.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
LOGGER.addHandler(LOGGING_CONSOLE_HANDLER)

core.setVerbosityLevel(3)

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def getSphinxDocumentationApi(rootDirectory, contentDirectory):
	"""
	This Definition Gets Sphinx Documentation Api.
		
	@param rootDirectory: Root Directory. ( String )
	@param contentDirectory: Content Directory. ( String )
	"""

	LOGGER.info("{0} | Building Sphinx Documentation Api!".format(getSphinxDocumentationApi.__name__))

	not rootDirectory in sys.path and sys.path.append(rootDirectory)

	walker = Walker(rootDirectory)
	walker.walk(filtersIn=("\.py$",), filtersOut=("__init__\.py",))

	for file in walker.files.values():
		not os.path.dirname(file) in sys.path and sys.path.append(os.path.dirname(file))

	modules = []
	for file in sorted(walker.files.values()):
		module = "{0}.{1}" .format(".".join(os.path.dirname(file).replace(rootDirectory, "").split("/")[1:]), strings.getSplitextBasename(file))
		modules.append(module)

		print file
		for member, object in moduleBrowser._readmodule(module, [file, ]).items():
			if "methods" in object.__dict__.keys():
				print member
				methods = [method for method in object.__dict__["methods"] if not method.startswith("_")]
				for method in methods:
					print "\t", method

if __name__ == "__main__":
	getSphinxDocumentationApi(sys.argv[1], sys.argv[2])

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
