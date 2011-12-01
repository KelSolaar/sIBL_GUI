#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**getImports.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Gets Application imports.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import re
import sys

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
from foundations.io import File
from foundations.globals.constants import Constants
from foundations.walkers import OsWalker

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
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

IMPORTS = ["PyQt.uic"]

FILTERS_IN = ("\.py$",)
FILTERS_OUT = ("defaultScript\.py", "tests")

#**********************************************************************************************************************
#***	Main Python code.
#**********************************************************************************************************************
def getImports(sourceDirectory, filtersIn, filtersOut):
	"""
	This definition gets Application imports.

	:param sourceDirectory: Source directory. ( String )
	:param filtersIn: Filters in. ( Tuple / List )
	:param filtersOut: Filters out. ( Tuple / List )
	:return: Imports. ( List )
	"""

	osWalker = OsWalker(sourceDirectory)
	osWalker.walk(filtersIn, filtersOut)

	imports = IMPORTS
	for file in sorted(osWalker.files.values()):
		source = File(file)
		source.read()
		for line in source.content:
			if not re.search("foundations|manager|umbra|sibl_gui", line):
				search = re.search("^\s*import\s*(?P<moduleA>[\w+\.]+)|^\s*from\s*(?P<moduleB>[\w+\.]+)\s+import", line)
				if search:
					statement = search.group("moduleA") or search.group("moduleB")
					statement not in imports and statement != "_" and imports.append(statement)
	return imports

if __name__ == "__main__":
	imports = getImports(sys.argv[1], filtersIn=FILTERS_IN, filtersOut=FILTERS_OUT)
	LOGGER.info("{0} | Imports: \"{1}\"".format(getImports.__name__, ",".join(sorted(imports))))
