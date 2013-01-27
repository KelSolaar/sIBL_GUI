#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**getHDRLabsDocumentation.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Extracts sIBL_GUI documentation body for HDRLabs.com.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sys
import re

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

__all__ = ["LOGGER", "getHDRLabsDocumentation"]

LOGGER = foundations.verbose.installLogger()

foundations.verbose.getLoggingConsoleHandler()
foundations.verbose.setVerbosityLevel(3)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getHDRLabsDocumentation(fileIn, fileOut):
	"""
	This definition extracts sIBL_GUI Documentation body for HDRLabs.com.

	:param fileIn: File to convert. ( String )
	:param fileOut: Output file. ( String )
	"""

	LOGGER.info("{0} | Extracting 'body' tag content from {1}' file!".format(getHDRLabsDocumentation.__name__, fileIn))
	file = File(fileIn)
	file.cache()

	LOGGER.info("{0} | Processing 'body' data!".format(getHDRLabsDocumentation.__name__))
	content = []
	skipLine = True
	for line in file.content:
		if re.search(r"<body>", line):
			skipLine = False
		elif re.search(r"</body>", line):
			skipLine = True

		not skipLine and content.append("{0}\n".format(line.replace("\t", "", 2)))

	file = File(fileOut)
	file.content = content
	file.write()

if __name__ == "__main__":
	getHDRLabsDocumentation(sys.argv[1], sys.argv[2])
