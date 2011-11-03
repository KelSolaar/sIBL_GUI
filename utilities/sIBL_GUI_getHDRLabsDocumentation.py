#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**sIBL_GUI_getHDRLabsDocumentation.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Extracts sIBL_GUI documentation body for HDRLabs.com.

**Others:**

"""
#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import sys
import re
from xml.etree import ElementTree

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
from foundations.io import File
from foundations.globals.constants import Constants

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

LOGGING_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
LOGGING_CONSOLE_HANDLER.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
LOGGER.addHandler(LOGGING_CONSOLE_HANDLER)

core.setVerbosityLevel(3)

#***********************************************************************************************
#***	Main Python code.
#***********************************************************************************************
def getHDRLabsDocumentation(fileIn, fileOut):
	"""
	This definition extracts sIBL_GUI Documentation body for HDRLabs.com.

	:param fileIn: File to convert. ( String )
	:param fileOut: Output file. ( String )
	"""

	LOGGER.info("{0} | Extracting 'body' tag content from {1}' file!".format(getHDRLabsDocumentation.__name__, fileIn))
	file = File(fileIn)
	file.read()

	LOGGER.info("{0} | Building 'ElementTree' parsing tree!".format(getHDRLabsDocumentation.__name__))
	element = ElementTree.fromstringlist(file.content)
	tree = ElementTree.ElementTree(element)

	LOGGER.info("{0} | Processing 'body' data!".format(getHDRLabsDocumentation.__name__))
	content = ["{0}\n".format(line.replace("html:", "").replace("\t", "", 2)) for line in ElementTree.tostring(tree.find("{http://www.w3.org/1999/xhtml}body")).split("\n") if not re.search(r"<html:body.*", line) and not re.search(r"</html:body.*", line)]

	file = File(fileOut)
	file.content = content
	file.write()

if __name__ == "__main__":
	getHDRLabsDocumentation(sys.argv[1], sys.argv[2])
