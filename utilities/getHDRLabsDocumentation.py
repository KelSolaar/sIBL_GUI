#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**getHDRLabsDocumentation.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Extracts sIBL_GUI documentation body for HDRLabs.com.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import argparse
import re
import sys

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.decorators
import foundations.verbose
from foundations.io import File

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "getHDRLabsDocumentation", "getCommandLineArguments", "main"]

LOGGER = foundations.verbose.installLogger()

foundations.verbose.getLoggingConsoleHandler()
foundations.verbose.setVerbosityLevel(3)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getHDRLabsDocumentation(input, output):
	"""
	Extracts sIBL_GUI Documentation body for HDRLabs.com.

	:param input: Input file to extract documentation body.
	:type input: unicode
	:param output: Output html file.
	:type output: unicode
	:return: Definition success.
	:rtype: bool
	"""

	LOGGER.info("{0} | Extracting 'body' tag content from {1}' file!".format(getHDRLabsDocumentation.__name__, input))
	file = File(input)
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

	file = File(output)
	file.content = content
	file.write()

	return True

def getCommandLineArguments():
	"""
	Retrieves command line arguments.

	:return: Namespace.
	:rtype: Namespace
	"""

	parser = argparse.ArgumentParser(add_help=False)

	parser.add_argument("-h",
						"--help",
						action="help",
						help="'Displays this help message and exit.'")

	parser.add_argument("-i",
						"--input",
						type=unicode,
						dest="input",
						help="'Input file to extract documentation body.'")

	parser.add_argument("-o",
						"--output",
						type=unicode,
						dest="output",
						help="'Output html file.'")

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

@foundations.decorators.systemExit
def main():
	"""
	Starts the Application.

	:return: Definition success.
	:rtype: bool
	"""

	args = getCommandLineArguments()
	return getHDRLabsDocumentation(args.input, args.output)

if __name__ == "__main__":
	main()
