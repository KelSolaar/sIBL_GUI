#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**listImports.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Lists Application imports.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import re
import sys

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
import foundations.walkers
from foundations.io import File

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "IMPORTS", "FILTERS_IN", "FILTERS_OUT", "listImports"]

LOGGER = foundations.verbose.installLogger()

IMPORTS = ["PyQt.uic"]

FILTERS_IN = ("\.py$",)
FILTERS_OUT = ("defaultScript\.py", "tests")

foundations.verbose.getLoggingConsoleHandler()
foundations.verbose.setVerbosityLevel(3)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def listImports(sourceDirectory, filtersIn, filtersOut):
	"""
	This definition lists Application imports.

	:param sourceDirectory: Source directory. ( String )
	:param filtersIn: Filters in. ( Tuple / List )
	:param filtersOut: Filters out. ( Tuple / List )
	:return: Imports. ( List )
	"""

	imports = IMPORTS
	for file in sorted(list(foundations.walkers.filesWalker(sourceDirectory, filtersIn, filtersOut))):
		source = File(file)
		source.cache()
		for line in source.content:
			if not re.search("foundations|manager|umbra|sibl_gui", line):
				search = re.search("^\s*import\s*(?P<moduleA>[\w+\.]+)|^\s*from\s*(?P<moduleB>[\w+\.]+)\s+import", line)
				if search:
					statement = search.group("moduleA") or search.group("moduleB")
					statement not in imports and statement != "_" and imports.append(statement)
	return imports

if __name__ == "__main__":
	imports = listImports(sys.argv[1], filtersIn=FILTERS_IN, filtersOut=FILTERS_OUT)
	LOGGER.info("{0} | Imports: \"{1}\"".format(listImports.__name__, ",".join(sorted(imports))))
