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
**sIBL_GUI_reStructuredTextToHtml.py

**Platform:**
	Windows.

**Description:**
	Converts A Textile File To HTML.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************
#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
import sys

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
from foundations.io import File
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

LOGGING_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
LOGGING_CONSOLE_HANDLER.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
LOGGER.addHandler(LOGGING_CONSOLE_HANDLER)

core.setVerbosityLevel(3)

RST2HTML = "/Library/Frameworks/Python.framework/Versions/2.7/bin/rst2html.py"
CSS_FILE = "css/style.css"
TIDY_SETTINGS_FILE = "tidy/tidySettings.rc"

NORMALIZATION = {"document": "document", }

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def reStructuredTextToHtml(fileIn, fileOut):
	"""
	This Definition Outputs A reStructuredText File To HTML.
		
	@param fileIn: File To Convert. ( String )
	@param fileOut: Output File. ( String )
	"""

	LOGGER.info("{0} | Converting '{1}' reStructuredText File To HTML!".format(reStructuredTextToHtml.__name__, fileIn))
	os.system("{0} --stylesheet-path='{1}' '{2}' > '{3}'".format(RST2HTML, os.path.join(os.path.dirname(__file__), CSS_FILE), fileIn, fileOut))


	LOGGER.info("{0} | Formatting HTML File!".format("Tidy"))
	os.system("tidy -config {0} -m '{1}'".format(os.path.join(os.path.dirname(__file__), TIDY_SETTINGS_FILE), fileOut))

	file = File(fileOut)
	file.read()
	LOGGER.info("{0} | Replacing Spaces With Tabs!".format(reStructuredTextToHtml.__name__))
	file.content = [line.replace(" " * 4, "\t") for line in file.content]
	file.write()

if __name__ == "__main__":
	reStructuredTextToHtml(sys.argv[1], sys.argv[2])

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
