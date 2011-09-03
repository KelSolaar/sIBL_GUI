#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsUiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`umbra.globals.uiConstants` module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import re
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from umbra.globals.uiConstants import UiConstants

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
class UiConstantsTestCase(unittest.TestCase):
	"""
	This class defines :class:`umbra.globals.uiConstants.UiConstants` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("uiFile",
								"windowsStylesheetFile",
								"darwinStylesheetFile",
								"linuxStylesheetFile",
								"windowsStyle",
								"darwinStyle",
								"linuxStyle",
								"layoutsFile",
								"applicationWindowsIcon",
								"applicationDarwinIcon",
								"splashScreenImage",
								"logoImage",
								"defaultToolbarIconSize",
								"centralWidgetIcon",
								"centralWidgetHoverIcon",
								"centralWidgetActiveIcon",
								"layoutIcon",
								"layoutHoverIcon",
								"layoutActiveIcon",
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
								"preferencesIcon",
								"preferencesHoverIcon",
								"preferencesActiveIcon",
								"formatErrorImage",
								"missingImage",
								"startupLayout",
								"helpFile",
								"apiFile",
								"nativeImageFormats",
								"thirdPartyImageFormats",
								"pythonTokensFile")

		for attribute in requiredAttributes:
			self.assertIn(attribute, UiConstants.__dict__)

	def testFrameworkUiFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.uiFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.uiFile, "\w+")

	def testFrameworkWindowsStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.windowsStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windowsStylesheetFile, "\w+")

	def testFrameworkDarwinStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.darwinStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwinStylesheetFile, "\w+")

	def testFrameworkLinuxStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.linuxStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linuxStylesheetFile, "\w+")

	def testFrameworkWindowsStyleAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.windowsStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windowsStyle, "\w+")

	def testFrameworkDarwinStyleAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.darwinStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwinStyle, "\w+")

	def testFrameworkLinuxStyleAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.linuxStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linuxStyle, "\w+")

	def testFrameworkLayoutsFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.layoutsFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layoutsFile, "\w+")

	def testFrameworkApplicationWindowsIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.applicationWindowsIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.applicationWindowsIcon, "\w+")
		self.assertRegexpMatches(UiConstants.applicationWindowsIcon, "\.[pP][nN][gG]$")

	def testFrameworkApplicationDarwinIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.applicationDarwinIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.applicationDarwinIcon, "\w+")
		self.assertRegexpMatches(UiConstants.applicationDarwinIcon, "\.[pP][nN][gG]$")

	def testFrameworkSplashscreemImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.splashScreenImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.splashScreenImage, "\w+")
		self.assertRegexpMatches(UiConstants.splashScreenImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkLogoImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.logoImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.logoImage, "\w+")
		self.assertRegexpMatches(UiConstants.logoImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkDefaultToolbarIconSizeAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.defaultToolbarIconSize` attribute.
		"""

		self.assertIsInstance(UiConstants.defaultToolbarIconSize, int)
		self.assertGreaterEqual(UiConstants.defaultToolbarIconSize, 8)
		self.assertLessEqual(UiConstants.defaultToolbarIconSize, 128)

	def testFrameworkCentralWidgetIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.centralWidgetIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.centralWidgetIcon, "\w+")

	def testFrameworkCentralWidgetHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.centralWidgetHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.centralWidgetHoverIcon, "\w+")

	def testFrameworkCentralWidgetActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.centralWidgetActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.centralWidgetActiveIcon, "\w+")

	def testFrameworLayoutIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.layoutIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layoutIcon, "\w+")

	def testFrameworLayoutHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.layoutHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layoutHoverIcon, "\w+")

	def testFrameworLayoutActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.layoutActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layoutActiveIcon, "\w+")

	def testFrameworMiscellaneousIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.miscellaneousIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneousIcon, "\w+")

	def testFrameworMiscellaneousHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.miscellaneousHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneousHoverIcon, "\w+")

	def testFrameworMiscellaneousActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.miscellaneousActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneousActiveIcon, "\w+")

	def testFrameworkLibraryIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.libraryIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.libraryIcon, "\w+")

	def testFrameworkLibraryHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.libraryHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.libraryHoverIcon, "\w+")

	def testFrameworkLibraryActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.libraryActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.libraryActiveIcon, "\w+")

	def testFrameworkInspectIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.inspectIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.inspectIcon, "\w+")

	def testFrameworkInspectHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.inspectHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.inspectHoverIcon, "\w+")

	def testFrameworkInspectActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.inspectActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.inspectActiveIcon, "\w+")

	def testFrameworkExportIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.exportIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.exportIcon, "\w+")

	def testFrameworkExportHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.exportHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.exportHoverIcon, "\w+")

	def testFrameworkExportActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.exportActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.exportActiveIcon, "\w+")

	def testFrameworkPreferencesIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.preferencesIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferencesIcon, "\w+")

	def testFrameworkPreferencesHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.preferencesHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferencesHoverIcon, "\w+")

	def testFrameworkPreferencesActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.preferencesActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferencesActiveIcon, "\w+")

	def testFrameworkFormatErrorImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.formatErrorImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.formatErrorImage, "\w+")
		self.assertRegexpMatches(UiConstants.formatErrorImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkMissingImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.missingImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.missingImage, "\w+")
		self.assertRegexpMatches(UiConstants.missingImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkStartupLayoutAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.startupLayout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.startupLayout, "\w+")

	def testFrameworkHelpFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.helpFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.helpFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def testFrameworkApiFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.apiFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.apiFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def testNativeImageFormatsAttribute(self):
			"""
			This method tests :attr:`umbra.globals.uiConstants.UiConstants.nativeImageFormats` attribute.
			"""

			self.assertIsInstance(UiConstants.nativeImageFormats, dict)
			for key, value in UiConstants.nativeImageFormats.items():
				self.assertIsInstance(key, str)
				self.assertIsInstance(value, str)
				self.assertTrue(re.compile(value))

	def testThirdPartyImageFormatsAttribute(self):
			"""
			This method tests :attr:`umbra.globals.uiConstants.UiConstants.thirdPartyImageFormats` attribute.
			"""

			self.assertIsInstance(UiConstants.thirdPartyImageFormats, dict)
			for key, value in UiConstants.thirdPartyImageFormats.items():
				self.assertIsInstance(key, str)
				self.assertIsInstance(value, str)
				self.assertTrue(re.compile(value))

	def testPythonTokensFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.pythonTokensFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.pythonTokensFile, "\w+")

if __name__ == "__main__":
	unittest.main()
