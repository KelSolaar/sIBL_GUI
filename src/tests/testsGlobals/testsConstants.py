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
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	testsConstants.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Constants Tests Module.
***
***	Others:
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class ConstantsTestCase(unittest.TestCase):
	'''
	This Class Is The ConstantsTests Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		requiredAttributes = ("applicationName",
								"releaseVersion",
								"logger",
								"verbosityLevel",
								"verbosityLabels",
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
		'''
		This Method Tests The "applicationName" Attribute.
		'''

		self.assertRegexpMatches(Constants.applicationName, "\w")

	def testReleaseVersionAttribute(self):
		'''
		This Method Tests The "releaseVersion" Attribute.
		'''

		self.assertRegexpMatches(Constants.releaseVersion, "[0-9]\.[0-9]\.[0-9]")

	def testLoggerAttribute(self):
		'''
		This Method Tests The "logger" Attribute.
		'''

		self.assertRegexpMatches(Constants.logger, "\w")

	def testVerbosityLevelAttribute(self):
		'''
		This Method Tests The "verbosityLevel" Attribute.
		'''

		self.assertIsInstance(Constants.verbosityLevel, int)
		self.assertGreaterEqual(Constants.verbosityLevel, 0)
		self.assertLessEqual(Constants.verbosityLevel, 4)

	def testLoggingSeparatorsAttribute(self):
		'''
		This Method Tests The "loggingSeparators" Attribute.
		'''

		self.assertIsInstance(Constants.loggingSeparators, str)

	def testEncodingFormatAttribute(self):
		'''
		This Method Tests The "encodingFormat" Attribute.
		'''

		validEncodings = ("ascii",
						"utf-8",
						"cp1252")

		self.assertIn(Constants.encodingFormat, validEncodings)

	def testEncodingErrorAttribute(self):
		'''
		This Method Tests The "encodingError" Attribute.
		'''

		validEncodings = ("strict",
						"ignore",
						"replace",
						"xmlcharrefreplace")

		self.assertIn(Constants.encodingError, validEncodings)

	def testApplicationDirectoryAttribute(self):
		'''
		This Method Tests The "applicationDirectory" Attribute.
		'''

		self.assertRegexpMatches(Constants.applicationDirectory, "\w")

	def testProviderDirectoryAttribute(self):
		'''
		This Method Tests The "providerDirectory" Attribute.
		'''

		self.assertRegexpMatches(Constants.providerDirectory, "\w")

	def testSettingsDirectoryAttribute(self):
		'''
		This Method Tests The "settingsDirectory" Attribute.
		'''

		self.assertRegexpMatches(Constants.settingsDirectory, "\w")

	def testUserComponentsDirectoryAttribute(self):
		'''
		This Method Tests The "userComponentsDirectory" Attribute.
		'''

		self.assertRegexpMatches(Constants.userComponentsDirectory, "\w")

	def testLoggingDirectoryAttribute(self):
		'''
		This Method Tests The "loggingDirectory" Attribute.
		'''

		self.assertRegexpMatches(Constants.loggingDirectory, "\w")

	def testIoDirectoryAttribute(self):
		'''
		This Method Tests The "ioDirectory" Attribute.
		'''

		self.assertRegexpMatches(Constants.ioDirectory, "\w")

	def testPreferencesDirectoriesAttribute(self):
		'''
		This Method Tests The "preferencesDirectories" Attribute.
		'''

		self.assertIsInstance(Constants.preferencesDirectories, tuple)

	def testCoreComponentsDirectoryAttribute(self):
		'''
		This Method Tests The "coreComponentsDirectory" Attribute.
		'''

		self.assertRegexpMatches(Constants.coreComponentsDirectory, "\w")

	def testAddonsComponentsDirectoryAttribute(self):
		'''
		This Method Tests The "addonsComponentsDirectory" Attribute.
		'''

		self.assertRegexpMatches(Constants.addonsComponentsDirectory, "\w")

	def testLibrariesDirectoryAttribute(self):
		'''
		This Method Tests The "librariesDirectory" Attribute.
		'''

		self.assertRegexpMatches(Constants.librariesDirectory, "\w")

	def testSettingsFileAttribute(self):
		'''
		This Method Tests The "settingsFile" Attribute.
		'''

		self.assertRegexpMatches(Constants.settingsFile, "\w")

	def testLoggingFileAttribute(self):
		'''
		This Method Tests The "settingsFile" Attribute.
		'''

		self.assertRegexpMatches(Constants.loggingFile, "\w")

	def testDefaultTimerCycleAttribute(self):
		'''
		This Method Tests The "defaultTimerCycle" Attribute.
		'''

		self.assertIsInstance(Constants.defaultTimerCycle, int)
		self.assertGreaterEqual(Constants.defaultTimerCycle, 25)
		self.assertLessEqual(Constants.defaultTimerCycle, 4 ** 32)

	def testNullObjectAttribute(self):
		'''
		This Method Tests The "nullObject" Attribute.
		'''

		self.assertRegexpMatches(Constants.nullObject, "\w")

if __name__ == '__main__':
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
