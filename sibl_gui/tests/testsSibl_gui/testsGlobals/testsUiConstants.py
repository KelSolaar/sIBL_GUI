#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsUiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`sibl_gui.globals.uiConstants` module.

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
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from sibl_gui.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UiConstantsTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class UiConstantsTestCase(unittest.TestCase):
	"""
	Defines :class:`sibl_gui.globals.uiConstants.UiConstants` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		Tests presence of required attributes.
		"""

		requiredAttributes = ("uiFile",
							"windowsStylesheetFile",
							"darwinStylesheetFile",
							"linuxStylesheetFile",
							"windowsStyle",
							"darwinStyle",
							"settingsFile",
							"linuxStyle",
							"layoutsFile",
							"applicationWindowsIcon",
							"splashScreenImage",
							"logoImage",
							"defaultToolbarIconSize",
							"centralWidgetIcon",
							"centralWidgetHoverIcon",
							"centralWidgetActiveIcon",
							"customLayoutsIcon",
							"customLayoutsHoverIcon",
							"customLayoutsActiveIcon",
							"miscellaneousIcon",
							"miscellaneousHoverIcon",
							"miscellaneousActiveIcon",
							"libraryIcon",
							"libraryHoverIcon",
							"libraryActiveIcon",
							"inspectIcon",
							"inspectHoverIcon",
							"inspectActiveIcon",
							"exportIcon",
							"exportHoverIcon",
							"exportActiveIcon",
							"editIcon",
							"editHoverIcon",
							"editActiveIcon",
							"preferencesIcon",
							"preferencesHoverIcon",
							"preferencesActiveIcon",
							"formatErrorImage",
							"missingImage",
							"loadingImage",
							"startupLayout",
							"developmentLayout",
							"helpFile",
							"apiFile",
							"nativeImageFormats",
							"thirdPartyImageFormats",
							"thumbnailsSizes",
							"thumbnailsCacheDirectory",
							"crittercismId")

		for attribute in requiredAttributes:
			self.assertIn(attribute, UiConstants.__dict__)

	def testUiFileAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.uiFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.uiFile, "\w+")

	def testWindowsStylesheetFileAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.windowsStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windowsStylesheetFile, "\w+")

	def testDarwinStylesheetFileAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.darwinStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwinStylesheetFile, "\w+")

	def testLinuxStylesheetFileAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.linuxStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linuxStylesheetFile, "\w+")

	def testWindowsStyleAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.windowsStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windowsStyle, "\w+")

	def testDarwinStyleAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.darwinStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwinStyle, "\w+")

	def testSettingsFileAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.settingsFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.settingsFile, "\w+")

	def testLinuxStyleAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.linuxStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linuxStyle, "\w+")

	def testLayoutsFileAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.layoutsFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layoutsFile, "\w+")

	def testApplicationWindowsIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.applicationWindowsIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.applicationWindowsIcon, "\w+")
		self.assertRegexpMatches(UiConstants.applicationWindowsIcon, "\.[pP][nN][gG]$")

	def testSplashscreemImageAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.splashScreenImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.splashScreenImage, "\w+")
		self.assertRegexpMatches(UiConstants.splashScreenImage,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testLogoImageAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.logoImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.logoImage, "\w+")
		self.assertRegexpMatches(UiConstants.logoImage,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testDefaultToolbarIconSizeAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.defaultToolbarIconSize` attribute.
		"""

		self.assertIsInstance(UiConstants.defaultToolbarIconSize, int)
		self.assertGreaterEqual(UiConstants.defaultToolbarIconSize, 8)
		self.assertLessEqual(UiConstants.defaultToolbarIconSize, 128)

	def testCentralWidgetIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.centralWidgetIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.centralWidgetIcon, "\w+")

	def testCentralWidgetHoverIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.centralWidgetHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.centralWidgetHoverIcon, "\w+")

	def testCentralWidgetActiveIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.centralWidgetActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.centralWidgetActiveIcon, "\w+")

	def testCustomLayoutsIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.customLayoutsIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.customLayoutsIcon, "\w+")

	def testLayoutHoverIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.customLayoutsHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.customLayoutsHoverIcon, "\w+")

	def testLayoutActiveIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.customLayoutsActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.customLayoutsActiveIcon, "\w+")

	def testMiscellaneousIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.miscellaneousIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneousIcon, "\w+")

	def testMiscellaneousHoverIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.miscellaneousHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneousHoverIcon, "\w+")

	def testMiscellaneousActiveIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.miscellaneousActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneousActiveIcon, "\w+")

	def testLibraryIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.libraryIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.libraryIcon, "\w+")

	def testLibraryHoverIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.libraryHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.libraryHoverIcon, "\w+")

	def testLibraryActiveIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.libraryActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.libraryActiveIcon, "\w+")

	def testInspectIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.inspectIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.inspectIcon, "\w+")

	def testInspectHoverIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.inspectHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.inspectHoverIcon, "\w+")

	def testInspectActiveIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.inspectActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.inspectActiveIcon, "\w+")

	def testExportIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.exportIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.exportIcon, "\w+")

	def testExportHoverIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.exportHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.exportHoverIcon, "\w+")

	def testExportActiveIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.exportActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.exportActiveIcon, "\w+")

	def testEditIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.editIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.editIcon, "\w+")

	def testEditHoverIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.editHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.editHoverIcon, "\w+")

	def testEditActiveIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.editActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.editActiveIcon, "\w+")

	def testPreferencesIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.preferencesIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferencesIcon, "\w+")

	def testPreferencesHoverIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.preferencesHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferencesHoverIcon, "\w+")

	def testPreferencesActiveIconAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.preferencesActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferencesActiveIcon, "\w+")

	def testFormatErrorImageAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.formatErrorImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.formatErrorImage, "\w+")
		self.assertRegexpMatches(UiConstants.formatErrorImage,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testMissingImageAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.missingImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.missingImage, "\w+")
		self.assertRegexpMatches(UiConstants.missingImage,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testLoadingImageAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.loadingImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.loadingImage, "\w+")
		self.assertRegexpMatches(UiConstants.loadingImage,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testStartupLayoutAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.startupLayout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.startupLayout, "\w+")

	def testDevelopmentLayoutAttribute(self):
		"""
		Tests :attr:`umbra.globals.uiConstants.UiConstants.developmentLayout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.developmentLayout, "\w+")

	def testHelpFileAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.helpFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.helpFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def testApiFileAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.apiFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.apiFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def testNativeImageFormatsAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.nativeImageFormats` attribute.
		"""

		self.assertIsInstance(UiConstants.nativeImageFormats, dict)
		for key, value in UiConstants.nativeImageFormats.iteritems():
			self.assertIsInstance(key, unicode)
			self.assertIsInstance(value, unicode)
			self.assertTrue(re.compile(value))

	def testThirdPartyImageFormatsAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.thirdPartyImageFormats` attribute.
		"""

		self.assertIsInstance(UiConstants.thirdPartyImageFormats, dict)
		for key, value in UiConstants.thirdPartyImageFormats.iteritems():
			self.assertIsInstance(key, unicode)
			self.assertIsInstance(value, unicode)
			self.assertTrue(re.compile(value))

	def testThumbnailsSizesAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.thumbnailsSizes` attribute.
		"""

		self.assertIsInstance(UiConstants.thumbnailsSizes, dict)
		for key, value in UiConstants.thumbnailsSizes.iteritems():
			self.assertIsInstance(key, unicode)
			self.assertIn(type(value), (type(None), int))

	def testThumbnailsCacheDirectoryAttribute(self):
		"""
		Tests :attr:`sibl_gui.globals.uiConstants.UiConstants.thumbnailsCacheDirectory` attribute.
		"""

		self.assertRegexpMatches(UiConstants.thumbnailsCacheDirectory, "\w+")

	def testCrittercismIdAttribute(self):
		"""
		Tests :attr:`umbra.globals.uiConstants.UiConstants.crittercismId` attribute.
		"""

		self.assertRegexpMatches(UiConstants.crittercismId, "\w+")
		self.assertEqual(UiConstants.crittercismId, "51290b3589ea7429250004fe")

if __name__ == "__main__":
	unittest.main()
