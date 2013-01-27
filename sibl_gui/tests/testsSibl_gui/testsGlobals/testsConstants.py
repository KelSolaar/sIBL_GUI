#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`sibl_gui.globals.constants` module.

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
from sibl_gui.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["ConstantsTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ConstantsTestCase(unittest.TestCase):
	"""
	This class defines :class:`sibl_gui.globals.constants.Constants` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("applicationName",
								"majorVersion",
								"minorVersion",
								"changeVersion",
								"releaseVersion",
								"logger",
								"applicationDirectory",
								"providerDirectory",
								"databaseDirectory",
								"databaseMigrationsDirectory",
								"databaseMigrationsFilesDirectory",
								"databaseMigrationsTemplatesDirectory",
								"patchesDirectory",
								"settingsDirectory",
								"userComponentsDirectory",
								"loggingDirectory",
								"templatesDirectory",
								"ioDirectory",
								"preferencesDirectories",
								"coreComponentsDirectory",
								"addonsComponentsDirectory",
								"resourcesDirectory",
								"patchesFile",
								"databaseFile",
								"settingsFile",
								"loggingFile",
								"databaseMigrationsFilesExtension",
								"librariesDirectory",
								"freeImageLibrary")

		for attribute in requiredAttributes:
			self.assertIn(attribute, Constants.__dict__)

	def testApplicationNameAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.applicationName` attribute.
		"""

		self.assertRegexpMatches(Constants.applicationName, "\w+")

	def testMajorVersionAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.majorVersion` attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "\d")

	def testMinorVersionAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.minorVersion` attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "\d")

	def testChangeVersionAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.changeVersion` attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "\d")

	def testReleaseVersionAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.releaseVersion` attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "\d\.\d\.\d")

	def testLoggerAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.logger` attribute.
		"""

		self.assertRegexpMatches(Constants.logger, "\w+")

	def testApplicationDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.applicationDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.applicationDirectory, "\w+")

	def testProviderDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.providerDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.providerDirectory, "\w+")

	def testDatabaseDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.databaseDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.databaseDirectory, "\w+")

	def testDatabaseMigrationsDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.databaseMigrationsDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.databaseMigrationsDirectory, "\w+")

	def testDatabaseMigrationsFilesDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.databaseMigrationsFilesDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.databaseMigrationsFilesDirectory, "\w+")

	def testDatabaseMigrationsTemplatesDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.databaseMigrationsTemplatesDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.databaseMigrationsTemplatesDirectory, "\w+")

	def testPatchesDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.patchesDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.patchesDirectory, "\w+")

	def testSettingsDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.settingsDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.settingsDirectory, "\w+")

	def testUserComponentsDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.userComponentsDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.userComponentsDirectory, "\w+")

	def testLoggingDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.loggingDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.loggingDirectory, "\w+")

	def testTemplatesDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.templatesDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.templatesDirectory, "\w+")

	def testIoDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.ioDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.ioDirectory, "\w+")

	def testPreferencesDirectoriesAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.preferencesDirectories` attribute.
		"""

		self.assertIsInstance(Constants.preferencesDirectories, tuple)

	def testCoreComponentsDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.coreComponentsDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.coreComponentsDirectory, "\w+")

	def testAddonsComponentsDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.addonsComponentsDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.addonsComponentsDirectory, "\w+")

	def testResourcesDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.resourcesDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.resourcesDirectory, "\w+")

	def testPatchesFileAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.patchesFile` attribute.
		"""

		self.assertRegexpMatches(Constants.patchesFile, "\w+")

	def testDatabaseFileAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.databaseFile` attribute.
		"""

		self.assertRegexpMatches(Constants.databaseFile, "\w+")

	def testSettingsFileAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.settingsFile` attribute.
		"""

		self.assertRegexpMatches(Constants.settingsFile, "\w+")

	def testLoggingFileAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.loggingFile` attribute.
		"""

		self.assertRegexpMatches(Constants.loggingFile, "\w+")

	def testDatabaseMigrationsFilesExtensionAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.databaseMigrationsFilesExtension` attribute.
		"""

		self.assertRegexpMatches(Constants.databaseMigrationsFilesExtension, "\w+")

	def testLibrariesDirectoryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.librariesDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.librariesDirectory, "\w+")

	def testFreeImageLibraryAttribute(self):
		"""
		This method tests :attr:`sibl_gui.globals.constants.Constants.freeImageLibrary` attribute.
		"""

		self.assertRegexpMatches(Constants.freeImageLibrary, "\w+")

if __name__ == "__main__":
	unittest.main()
