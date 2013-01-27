#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsExceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`sibl_gui.exceptions` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import sibl_gui.exceptions

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["EXCEPTIONS", "ExceptionsTestCase"]

EXCEPTIONS = []

def _gatherExceptions():
	"""
	This definition gathers the exceptions.
	"""

	for attribute in dir(sibl_gui.exceptions):
		object = getattr(sibl_gui.exceptions, attribute)
		if not inspect.isclass(object):
			continue
		if issubclass(object, Exception):
			EXCEPTIONS.append(object)

_gatherExceptions()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ExceptionsTestCase(unittest.TestCase):
	"""
	This class defines :mod:`sibl_gui.exceptions` module exceptions classes units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("value",)
		for exception in EXCEPTIONS:
			exceptionInstance = exception(None)
			for attribute in requiredAttributes:
				self.assertIn(attribute, dir(exceptionInstance))

	def test__str__(self):
		"""
		This method tests exceptions classes **__str__** method.
		"""

		for exception in EXCEPTIONS:
			exceptionInstance = exception("{0} Exception raised!".format(exception.__class__))
			self.assertIsInstance(exceptionInstance.__str__(), str)
			exceptionInstance = exception([exception.__class__, "Exception raised!"])
			self.assertIsInstance(exceptionInstance.__str__(), str)
			exceptionInstance = exception(0)
			self.assertIsInstance(exceptionInstance.__str__(), str)

if __name__ == "__main__":
	unittest.main()
