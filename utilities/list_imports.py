#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**list_imports.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Lists Application imports.

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
import foundations.walkers
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

__all__ = ["LOGGER", "IMPORTS", "FILTERS_IN", "FILTERS_OUT", "list_imports", "get_command_line_arguments", "main"]

LOGGER = foundations.verbose.install_logger()

IMPORTS = ["PyQt.uic"]

FILTERS_IN = ("\.py$",)
FILTERS_OUT = ("default_script\.py", "tests")

foundations.verbose.get_logging_console_handler()
foundations.verbose.set_verbosity_level(3)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def list_imports(packages, filters_in, filters_out):
	"""
	Lists Application imports.

	:param packages: Packages.
	:type packages: list
	:param filters_in: Filters in.
	:type filters_in: tuple or list
	:param filters_out: Filters out.
	:type filters_out: tuple or list
	:return: Imports.
	:rtype: list
	"""

	imports = set(IMPORTS)
	for package in packages:
		path = __import__(package).__path__.pop()
		for file in sorted(list(foundations.walkers.files_walker(path, filters_in, filters_out))):
			source = File(file)
			source.cache()
			for line in source.content:
				if not re.search("oncilla|foundations|manager|umbra|sibl_gui", line):
					search = re.search("^\s*import\s*(?P<moduleA>[\w+\.]+)|^\s*from\s*(?P<moduleB>[\w+\.]+)\s+import",
									   line)
					if search:
						statement = search.group("moduleA") or search.group("moduleB")
						statement != "_" and imports.add(statement)
	return imports

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

	parser.add_argument("-p",
						"--packages",
						nargs="*",
						dest="packages",
						help="'Packages.'")

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
	args.packages = args.packages if all(args.packages) else []
	imports = list_imports(args.packages, filters_in=FILTERS_IN, filters_out=FILTERS_OUT)
	LOGGER.info("{0} | Imports: \"{1}\"".format(list_imports.__name__, ",".join(sorted(imports))))
	return True

if __name__ == "__main__":
	main()
