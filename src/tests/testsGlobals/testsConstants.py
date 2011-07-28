#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**testsConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Constants tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class ConstantsTestCase(unittest.TestCase):
	"""
	This class is the ConstantsTests class.
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
		This method tests the "applicationName" attribute.
		"""

		self.assertRegexpMatches(Constants.applicationName, "\w+")

	def testReleaseVersionAttribute(self):
		"""
		This method tests the "releaseVersion" attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "[0-9]\.[0-9]\.[0-9]")

	def testLoggerAttribute(self):
		"""
		This method tests the "logger" attribute.
		"""

		self.assertRegexpMatches(Constants.logger, "\w+")

	def testVerbosityLevelAttribute(self):
		"""
		This method tests the "verbosityLevel" attribute.
		"""

		self.assertIsInstance(Constants.verbosityLevel, int)
		self.assertGreaterEqual(Constants.verbosityLevel, 0)
		self.assertLessEqual(Constants.verbosityLevel, 4)

	def testLoggingDefaultFormaterAttribute(self):
		"""
		This method tests the "loggingDefaultFormatter" attribute.
		"""

		self.assertIsInstance(Constants.loggingDefaultFormatter, str)

	def testVerbosityLabelsAttribute(self):
		"""
		This method tests the "verbosityLabels" attribute.
		"""

		self.assertIsInstance(Constants.verbosityLabels, tuple)
		for label in Constants.verbosityLabels:
			self.assertIsInstance(label, str)

	def testLoggingSeparatorsAttribute(self):
		"""
		This method tests the "loggingSeparators" attribute.
		"""

		self.assertIsInstance(Constants.loggingSeparators, str)

	def testEncodingFormatAttribute(self):
		"""
		This method tests the "encodingFormat" attribute.
		"""

		validEncodings = ("ascii",
						"utf-8",
						"cp1252")

		self.assertIn(Constants.encodingFormat, validEncodings)

	def testEncodingErrorAttribute(self):
		"""
		This method tests the "encodingError" attribute.
		"""

		validEncodings = ("strict",
						"ignore",
						"replace",
						"xmlcharrefreplace")

		self.assertIn(Constants.encodingError, validEncodings)

	def testApplicationDirectoryAttribute(self):
		"""
		This method tests the "applicationDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.applicationDirectory, "\w+")

	def testProviderDirectoryAttribute(self):
		"""
		This method tests the "providerDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.providerDirectory, "\w+")

	def testSettingsDirectoryAttribute(self):
		"""
		This method tests the "settingsDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.settingsDirectory, "\w+")

	def testUserComponentsDirectoryAttribute(self):
		"""
		This method tests the "userComponentsDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.userComponentsDirectory, "\w+")

	def testLoggingDirectoryAttribute(self):
		"""
		This method tests the "loggingDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.loggingDirectory, "\w+")

	def testIoDirectoryAttribute(self):
		"""
		This method tests the "ioDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.ioDirectory, "\w+")

	def testPreferencesDirectoriesAttribute(self):
		"""
		This method tests the "preferencesDirectories" attribute.
		"""

		self.assertIsInstance(Constants.preferencesDirectories, tuple)

	def testCoreComponentsDirectoryAttribute(self):
		"""
		This method tests the "coreComponentsDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.coreComponentsDirectory, "\w+")

	def testAddonsComponentsDirectoryAttribute(self):
		"""
		This method tests the "addonsComponentsDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.addonsComponentsDirectory, "\w+")

	def testLibrariesDirectoryAttribute(self):
		"""
		This method tests the "librariesDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.librariesDirectory, "\w+")

	def testSettingsFileAttribute(self):
		"""
		This method tests the "settingsFile" attribute.
		"""

		self.assertRegexpMatches(Constants.settingsFile, "\w+")

	def testLoggingFileAttribute(self):
		"""
		This method tests the "settingsFile" attribute.
		"""

		self.assertRegexpMatches(Constants.loggingFile, "\w+")

	def testDefaultTimerCycleAttribute(self):
		"""
		This method tests the "defaultTimerCycle" attribute.
		"""

		self.assertIsInstance(Constants.defaultTimerCycle, int)
		self.assertGreaterEqual(Constants.defaultTimerCycle, 25)
		self.assertLessEqual(Constants.defaultTimerCycle, 4 ** 32)

	def testNullObjectAttribute(self):
		"""
		This method tests the "nullObject" attribute.
		"""

		self.assertRegexpMatches(Constants.nullObject, "\w+")

if __name__ == "__main__":
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
