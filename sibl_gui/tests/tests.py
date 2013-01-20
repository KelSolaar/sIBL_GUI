#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module runs the tests suite.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["testsSuite"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def _setPackageDirectory():
	"""
	This definition sets the package directory in the path.

	:return: Definition success. ( Boolean )
	"""

	packageDirectory = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
	packageDirectory not in sys.path and sys.path.append(packageDirectory)
	return True

_setPackageDirectory()

def testsSuite():
	"""
	This definitions runs the tests suite.
	
	:return: Tests suite. ( TestSuite )
	"""

	testsLoader = unittest.TestLoader()
	return testsLoader.discover(os.path.dirname(__file__))

if __name__ == "__main__":
	import sibl_gui.tests.utilities
	unittest.TextTestRunner(verbosity=2).run(testsSuite())
