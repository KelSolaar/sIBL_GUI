#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**sanitizer.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Sanitizes python module file. :func:`bleach` definition is called by **Oncilla** package.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import re

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.strings
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

__all__ = ["LOGGER",
		   "STATEMENT_UPDATE_MESSAGE",
		   "STATEMENT_SUBSTITUTE",
		   "bleach"]

LOGGER = foundations.verbose.installLogger()

STATEMENT_UPDATE_MESSAGE = "# Oncilla: Statement commented by auto-documentation process: "

STATEMENT_SUBSTITUTE = ("(\n)(?P<bleach>\s*if\s+__name__\s+==\s+[\"']__main__[\"']\s*:.*)",
					  "(\n)(?P<bleach>\s*@(?!property|\w+\.setter|\w+\.deleter).*?)(\n+\s*def\s+)",
					  "(?P<bleach>sys.path.append\(os.path.join\(os.path.dirname\(os.path.abspath\(__file__\)\), \"libraries\"\)\))",
					  "(?P<bleach>import python.pyclbr as moduleBrowser)",
					  "(\n)(?P<bleach>\s*_initializeApplication\(\))")

STATEMENT_REPLACE = {"PYTHON_LANGUAGE = getPythonLanguage()": \
					   "{0}\nPYTHON_LANGUAGE = None".format(STATEMENT_UPDATE_MESSAGE),
				   "LOGGING_LANGUAGE = getLoggingLanguage()": \
					   "{0}\nLOGGING_LANGUAGE = None".format(STATEMENT_UPDATE_MESSAGE),
				   "TEXT_LANGUAGE = getTextLanguage()": \
					   "{0}\nTEXT_LANGUAGE = None".format(STATEMENT_UPDATE_MESSAGE)}

STATEMENT_IGNORE = ("@handleExceptions(ZeroDivisionError)",)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def bleach(file):
	"""
	Sanitizes given python module.

	:param file: Python module file.
	:type file: unicode
	:return: Definition success.
	:rtype: bool
	"""

	LOGGER.info("{0} | Sanitizing '{1}' python module!".format(__name__, file))

	sourceFile = File(file)
	content = sourceFile.read()
	for pattern in STATEMENT_SUBSTITUTE:
		matches = [match for match in re.finditer(pattern, content, re.DOTALL)]

		offset = 0
		for match in matches:
			if any(map(lambda x: x in match.group("bleach"), STATEMENT_IGNORE)):
				continue

			start, end = match.start("bleach"), match.end("bleach")
			substitution = "{0}{1}".format(STATEMENT_UPDATE_MESSAGE,
										   re.sub("\n", "\n{0}".format(STATEMENT_UPDATE_MESSAGE),
												  match.group("bleach")))
			content = "".join((content[0: start + offset],
							   substitution,
							   content[end + offset:]))
			offset += len(substitution) - len(match.group("bleach"))

	content = foundations.strings.replace(content, STATEMENT_REPLACE)

	sourceFile.content = [content]
	sourceFile.write()

	return True
