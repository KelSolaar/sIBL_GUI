#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsRuntimeGlobals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`sibl_gui.globals.runtimeGlobals` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from sibl_gui.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RuntimeGlobalsTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RuntimeGlobalsTestCase(unittest.TestCase):
	"""
	This class defines :class:`sibl_gui.globals.runtimeGlobals.RuntimeGlobals` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("templatesFactoryDirectory",
								"templatesUserDirectory",
								"imagesCaches")

		for attribute in requiredAttributes:
			self.assertIn(attribute, RuntimeGlobals.__dict__)

if __name__ == "__main__":
	unittest.main()
