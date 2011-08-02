#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Constants tests Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from umbra.globals.constants import Constants

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
class ConstantsTestCase(unittest.TestCase):
	"""
	This class is the **ConstantsTests** class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("applicationName",
								"releaseVersion",
								"logger",
								"verbosityLevel",
								"verbosityLabels",
								"loggingDefaultFormatter",
								"loggingSeparators",
								"encodingFormat",
								"encodingError",
								"applicationDirectory",
								"providerDirectory",
								"settingsDirectory",
								"userComponentsDirectory",
								"loggingDirectory",
								"ioDirectory",
								"preferencesDirectories",
								"coreComponentsDirectory",
								"addonsComponentsDirectory",
								"librariesDirectory",
								"settingsFile",
								"loggingFile",
								"defaultTimerCycle",
								"nullObject")

		for attribute in requiredAttributes:
			self.assertIn(attribute, Constants.__dict__)

	def testApplicationNameAttribute(self):
		"""
		This method tests **applicationName** attribute.
		"""

		self.assertRegexpMatches(Constants.applicationName, "\w+")

	def testReleaseVersionAttribute(self):
		"""
		This method tests **releaseVersion** attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "[0-9]\.[0-9]\.[0-9]")

	def testLoggerAttribute(self):
		"""
		This method tests **logger** attribute.
		"""

		self.assertRegexpMatches(Constants.logger, "\w+")

	def testVerbosityLevelAttribute(self):
		"""
		This method tests **verbosityLevel** attribute.
		"""

		self.assertIsInstance(Constants.verbosityLevel, int)
		self.assertGreaterEqual(Constants.verbosityLevel, 0)
		self.assertLessEqual(Constants.verbosityLevel, 4)

	def testLoggingDefaultFormaterAttribute(self):
		"""
		This method tests **loggingDefaultFormatter** attribute.
		"""

		self.assertIsInstance(Constants.loggingDefaultFormatter, str)

	def testVerbosityLabelsAttribute(self):
		"""
		This method tests **verbosityLabels** attribute.
		"""

		self.assertIsInstance(Constants.verbosityLabels, tuple)
		for label in Constants.verbosityLabels:
			self.assertIsInstance(label, str)

	def testLoggingSeparatorsAttribute(self):
		"""
		This method tests **loggingSeparators** attribute.
		"""

		self.assertIsInstance(Constants.loggingSeparators, str)

	def testEncodingFormatAttribute(self):
		"""
		This method tests **encodingFormat** attribute.
		"""

		validEncodings = ("ascii",
						"utf-8",
						"cp1252")

		self.assertIn(Constants.encodingFormat, validEncodings)

	def testEncodingErrorAttribute(self):
		"""
		This method tests **encodingError** attribute.
		"""

		validEncodings = ("strict",
						"ignore",
						"replace",
						"xmlcharrefreplace")

		self.assertIn(Constants.encodingError, validEncodings)

	def testApplicationDirectoryAttribute(self):
		"""
		This method tests **applicationDirectory** attribute.
		"""

		self.assertRegexpMatches(Constants.applicationDirectory, "\w+")

	def testProviderDirectoryAttribute(self):
		"""
		This method tests **providerDirectory** attribute.
		"""

		self.assertRegexpMatches(Constants.providerDirectory, "\w+")

	def testSettingsDirectoryAttribute(self):
		"""
		This method tests **settingsDirectory** attribute.
		"""

		self.assertRegexpMatches(Constants.settingsDirectory, "\w+")

	def testUserComponentsDirectoryAttribute(self):
		"""
		This method tests **userComponentsDirectory** attribute.
		"""

		self.assertRegexpMatches(Constants.userComponentsDirectory, "\w+")

	def testLoggingDirectoryAttribute(self):
		"""
		This method tests **loggingDirectory** attribute.
		"""

		self.assertRegexpMatches(Constants.loggingDirectory, "\w+")

	def testIoDirectoryAttribute(self):
		"""
		This method tests **ioDirectory** attribute.
		"""

		self.assertRegexpMatches(Constants.ioDirectory, "\w+")

	def testPreferencesDirectoriesAttribute(self):
		"""
		This method tests **preferencesDirectories** attribute.
		"""

		self.assertIsInstance(Constants.preferencesDirectories, tuple)

	def testCoreComponentsDirectoryAttribute(self):
		"""
		This method tests **coreComponentsDirectory** attribute.
		"""

		self.assertRegexpMatches(Constants.coreComponentsDirectory, "\w+")

	def testAddonsComponentsDirectoryAttribute(self):
		"""
		This method tests **addonsComponentsDirectory** attribute.
		"""

		self.assertRegexpMatches(Constants.addonsComponentsDirectory, "\w+")

	def testLibrariesDirectoryAttribute(self):
		"""
		This method tests **librariesDirectory** attribute.
		"""

		self.assertRegexpMatches(Constants.librariesDirectory, "\w+")

	def testSettingsFileAttribute(self):
		"""
		This method tests **settingsFile** attribute.
		"""

		self.assertRegexpMatches(Constants.settingsFile, "\w+")

	def testLoggingFileAttribute(self):
		"""
		This method tests **settingsFile** attribute.
		"""

		self.assertRegexpMatches(Constants.loggingFile, "\w+")

	def testDefaultTimerCycleAttribute(self):
		"""
		This method tests **defaultTimerCycle** attribute.
		"""

		self.assertIsInstance(Constants.defaultTimerCycle, int)
		self.assertGreaterEqual(Constants.defaultTimerCycle, 25)
		self.assertLessEqual(Constants.defaultTimerCycle, 4 ** 32)

	def testNullObjectAttribute(self):
		"""
		This method tests **nullObject** attribute.
		"""

		self.assertRegexpMatches(Constants.nullObject, "\w+")

if __name__ == "__main__":
	unittest.main()

