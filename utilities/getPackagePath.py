#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**getPackagePath.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Write given package path to stdout.

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
import sys

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.decorators
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "getPackagePath", "getCommandLineArguments", "main"]

LOGGER = foundations.verbose.installLogger()
foundations.verbose.getLoggingConsoleHandler()
foundations.verbose.setVerbosityLevel(3)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getPackagePath(package):
	"""
	Writes given package path to stdout.

	:param package: Package to retrieve the path.
	:type package: unicode
	:return: Definition success.
	:rtype: bool
	"""

	package = __import__(package)
	sys.stdout.write(package.__path__[0])

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

	parser.add_argument("-p",
						"--package",
						type=unicode,
						dest="package",
						help="'Package to retrieve the path.'")

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
	return getPackagePath(args.package)

if __name__ == "__main__":
	main()
