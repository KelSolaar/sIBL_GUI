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

		requiredAttributes = ("frameworkUiFile",
								"frameworkWindowsStylesheetFile",
								"frameworkDarwinStylesheetFile",
								"frameworkLinuxStylesheetFile",
								"frameworkWindowsStyle",
								"frameworkDarwinStyle",
								"frameworkLinuxStyle",
								"frameworkLayoutsFile",
								"frameworkApplicationWindowsIcon",
								"frameworkApplicationDarwinIcon",
								"frameworkSplashScreenImage",
								"frameworkLogoImage",
								"frameworkDefaultToolbarIconSize",
								"frameworkCentralWidgetIcon",
								"frameworkCentralWidgetHoverIcon",
								"frameworkCentralWidgetActiveIcon",
								"frameworkLayoutIcon",
								"frameworkLayoutHoverIcon",
								"frameworkLayoutActiveIcon",
								"frameworMiscellaneousIcon",
								"frameworMiscellaneousHoverIcon",
								"frameworMiscellaneousActiveIcon",
								"frameworkLibraryIcon",
								"frameworkLibraryHoverIcon",
								"frameworkLibraryActiveIcon",
								"frameworkInspectIcon",
								"frameworkInspectHoverIcon",
								"frameworkInspectActiveIcon",
								"frameworkExportIcon",
								"frameworkExportHoverIcon",
								"frameworkExportActiveIcon",
								"frameworkPreferencesIcon",
								"frameworkPreferencesHoverIcon",
								"frameworkPreferencesActiveIcon",
								"frameworkFormatErrorImage",
								"frameworkMissingImage",
								"frameworkStartupLayout",
								"frameworkHelpFile",
								"frameworkApiFile",
								"nativeImageFormats",
								"thirdPartyImageFormats",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, UiConstants.__dict__)

	def testFrameworkUiFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkUiFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkUiFile, "\w+")

	def testFrameworkWindowsStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkWindowsStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkWindowsStylesheetFile, "\w+")

	def testFrameworkDarwinStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkDarwinStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkDarwinStylesheetFile, "\w+")

	def testFrameworkLinuxStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLinuxStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLinuxStylesheetFile, "\w+")

	def testFrameworkWindowsStyleAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkWindowsStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkWindowsStyle, "\w+")

	def testFrameworkDarwinStyleAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkDarwinStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkDarwinStyle, "\w+")

	def testFrameworkLinuxStyleAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLinuxStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLinuxStyle, "\w+")

	def testFrameworkLayoutsFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLayoutsFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLayoutsFile, "\w+")

	def testFrameworkApplicationWindowsIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkApplicationWindowsIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkApplicationWindowsIcon, "\w+")
		self.assertRegexpMatches(UiConstants.frameworkApplicationWindowsIcon, "\.[pP][nN][gG]$")

	def testFrameworkApplicationDarwinIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkApplicationDarwinIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkApplicationDarwinIcon, "\w+")
		self.assertRegexpMatches(UiConstants.frameworkApplicationDarwinIcon, "\.[pP][nN][gG]$")

	def testFrameworkSplashscreemImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkSplashScreenImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkSplashScreenImage, "\w+")
		self.assertRegexpMatches(UiConstants.frameworkSplashScreenImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkLogoImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLogoImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLogoImage, "\w+")
		self.assertRegexpMatches(UiConstants.frameworkLogoImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkDefaultToolbarIconSizeAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkDefaultToolbarIconSize` attribute.
		"""

		self.assertIsInstance(UiConstants.frameworkDefaultToolbarIconSize, int)
		self.assertGreaterEqual(UiConstants.frameworkDefaultToolbarIconSize, 8)
		self.assertLessEqual(UiConstants.frameworkDefaultToolbarIconSize, 128)

	def testFrameworkCentralWidgetIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkCentralWidgetIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkCentralWidgetIcon, "\w+")

	def testFrameworkCentralWidgetHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkCentralWidgetHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkCentralWidgetHoverIcon, "\w+")

	def testFrameworkCentralWidgetActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkCentralWidgetActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkCentralWidgetActiveIcon, "\w+")

	def testFrameworLayoutIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLayoutIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLayoutIcon, "\w+")

	def testFrameworLayoutHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLayoutHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLayoutHoverIcon, "\w+")

	def testFrameworLayoutActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLayoutActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLayoutActiveIcon, "\w+")

	def testFrameworMiscellaneousIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworMiscellaneousIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworMiscellaneousIcon, "\w+")

	def testFrameworMiscellaneousHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworMiscellaneousHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworMiscellaneousHoverIcon, "\w+")

	def testFrameworMiscellaneousActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworMiscellaneousActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworMiscellaneousActiveIcon, "\w+")

	def testFrameworkLibraryIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLibraryIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLibraryIcon, "\w+")

	def testFrameworkLibraryHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLibraryHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLibraryHoverIcon, "\w+")

	def testFrameworkLibraryActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkLibraryActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLibraryActiveIcon, "\w+")

	def testFrameworkInspectIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkInspectIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkInspectIcon, "\w+")

	def testFrameworkInspectHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkInspectHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkInspectHoverIcon, "\w+")

	def testFrameworkInspectActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkInspectActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkInspectActiveIcon, "\w+")

	def testFrameworkExportIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkExportIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkExportIcon, "\w+")

	def testFrameworkExportHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkExportHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkExportHoverIcon, "\w+")

	def testFrameworkExportActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkExportActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkExportActiveIcon, "\w+")

	def testFrameworkPreferencesIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkPreferencesIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkPreferencesIcon, "\w+")

	def testFrameworkPreferencesHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkPreferencesHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkPreferencesHoverIcon, "\w+")

	def testFrameworkPreferencesActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkPreferencesActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkPreferencesActiveIcon, "\w+")

	def testFrameworkFormatErrorImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkFormatErrorImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkFormatErrorImage, "\w+")
		self.assertRegexpMatches(UiConstants.frameworkFormatErrorImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkMissingImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkMissingImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkMissingImage, "\w+")
		self.assertRegexpMatches(UiConstants.frameworkMissingImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkStartupLayoutAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkStartupLayout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkStartupLayout, "\w+")

	def testFrameworkHelpFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkHelpFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkHelpFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def testFrameworkApiFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.frameworkApiFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkApiFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

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

if __name__ == "__main__":
	unittest.main()
