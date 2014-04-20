#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**get_hdrlabs_documentation.py**

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

__all__ = ["LOGGER", "get_hdrlabs_documentation", "get_command_line_arguments", "main"]

LOGGER = foundations.verbose.install_logger()

foundations.verbose.get_logging_console_handler()
foundations.verbose.set_verbosity_level(3)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def get_hdrlabs_documentation(input, output):
	"""
	Extracts sIBL_GUI Documentation body for HDRLabs.com.

	:param input: Input file to extract documentation body.
	:type input: unicode
	:param output: Output html file.
	:type output: unicode
	:return: Definition success.
	:rtype: bool
	"""

	LOGGER.info("{0} | Extracting 'body' tag content from {1}' file!".format(get_hdrlabs_documentation.__name__, input))
	file = File(input)
	file.cache()

	LOGGER.info("{0} | Processing 'body' data!".format(get_hdrlabs_documentation.__name__))
	content = []
	skip_line = True
	for line in file.content:
		if re.search(r"<body>", line):
			skip_line = False
		elif re.search(r"</body>", line):
			skip_line = True

		not skip_line and content.append("{0}\n".format(line.replace("\t", "", 2)))

	file = File(output)
	file.content = content
	file.write()

	return True

def get_command_line_arguments():
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

@foundations.decorators.system_exit
def main():
	"""
	Starts the Application.

	:return: Definition success.
	:rtype: bool
	"""

	args = get_command_line_arguments()
	return get_hdrlabs_documentation(args.input, args.output)

if __name__ == "__main__":
	main()
