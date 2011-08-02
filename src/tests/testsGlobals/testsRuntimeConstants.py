#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsRuntimeConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Runtime constants tests Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from umbra.globals.runtimeConstants import RuntimeConstants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class RuntimeConstantsTestCase(unittest.TestCase):
	"""
	This class is the **RuntimeConstantsTestCase** class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("parameters",
								"args",
								"loggingConsoleHandler",
								"loggingFileHandler",
								"loggingSessionHandler",
								"loggingSessionHandlerStream",
								"verbosityLevel",
								"loggingFile",
								"application",
								"userApplicationDatasDirectory",
								"uiFile",
								"ui",
								"settingsFile",
								"settings")

		for attribute in requiredAttributes:
			self.assertIn(attribute, RuntimeConstants.__dict__)

if __name__ == "__main__":
	unittest.main()

