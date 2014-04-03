#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**recursiveRemove.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Recursion delete.

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
import os
import sys

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["recursiveRemove", "remove", "getCommandLineArguments" , "main"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def recursiveRemove(rootDirectory, pattern):
	"""
	Recursively deletes the matching items.

	:param rootDirectory: Directory to recurse.
	:type rootDirectory: unicode
	:param pattern: Pattern to match.
	:type pattern: unicode
	"""

	if not os.path.exists(rootDirectory):
		return

	for root, dirs, files in os.walk(rootDirectory, followlinks=True):
		for item in files:
			itemPath = os.path.join(root, item).replace("\\", "/")
			if pattern in item:
				remove(itemPath)

def remove(item):
	"""
	Deletes given item.
	:param item: Item to delete.
	:type item: unicode
	"""

	print("{0} | Removing file: '{1}'".format(remove.__name__, item))
	try:
		os.remove(item)
	except:
		print("{0} | '{1}' file removing failed!".format(remove.__name__, item))

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
						help="'Input directory to recurse.'")

	parser.add_argument("-p",
						"--pattern",
						type=unicode,
						dest="pattern",
						help="'Pattern to match.'")

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def main():
	"""
	Starts the Application.

	:return: Definition success.
	:rtype: bool
	"""

	args = getCommandLineArguments()
	return 0 if recursiveRemove(args.input, args.pattern) else 1

if __name__ == "__main__":
	main()

