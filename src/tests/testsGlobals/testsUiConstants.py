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
**testsUiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Ui uiconstants tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

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
#***	Overall variables.
#***********************************************************************************************

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class UiConstantsTestCase(unittest.TestCase):
	"""
	This class is the UiConstantsTestCase class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("frameworkUiFile",
								"frameworkWindowsStylesheetFile",
								"frameworkDarwinStylesheetFile",
								"frameworkLinuxStylesheetFile",
								"frameworkLayoutsFile",
								"frameworkApplicationWindowsIcon",
								"frameworkApplicationDarwinIcon",
								"frameworkLogoPicture",
								"frameworkDefaultToolbarIconSize",
								"frameworkStartupLayout",
								"frameworkHelpFile",
								"nativeImageFormats",
								"thirdPartyImageFormats",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, UiConstants.__dict__)

	def testFrameworkUiFileAttribute(self):
		"""
		This method tests the "frameworkUiFile" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkUiFile, "\w")

	def testFrameworkWindowsStylesheetFileAttribute(self):
		"""
		This method tests the "frameworkWindowsStylesheetFile" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkWindowsStylesheetFile, "\w")

	def testFrameworkDarwinStylesheetFileAttribute(self):
		"""
		This method tests the "frameworkDarwinStylesheetFile" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkDarwinStylesheetFile, "\w")

	def testFrameworkLinuxStylesheetFileAttribute(self):
		"""
		This method tests the "frameworkLinuxStylesheetFile" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLinuxStylesheetFile, "\w")

	def testFrameworkLayoutsFileAttribute(self):
		"""
		This method tests the "frameworkLayoutsFile" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLayoutsFile, "\w")

	def testFrameworkApplicationWindowsIconAttribute(self):
		"""
		This method tests the "frameworkApplicationWindowsIcon" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkApplicationWindowsIcon, "\w")
		self.assertRegexpMatches(UiConstants.frameworkApplicationWindowsIcon, "\.[pP][nN][gG]$")

	def testFrameworkApplicationDarwinIconAttribute(self):
		"""
		This method tests the "frameworkApplicationDarwinIcon" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkApplicationDarwinIcon, "\w")
		self.assertRegexpMatches(UiConstants.frameworkApplicationDarwinIcon, "\.[pP][nN][gG]$")

	def testFrameworkLogoPictureAttribute(self):
		"""
		This method tests the "frameworkLogoPicture" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLogoPicture, "\w")
		self.assertRegexpMatches(UiConstants.frameworkLogoPicture, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkDefaultToolbarIconSizeAttribute(self):
		"""
		This method tests the "frameworkDefaultToolbarIconSize" attribute.
		"""

		self.assertIsInstance(UiConstants.frameworkDefaultToolbarIconSize, int)
		self.assertGreaterEqual(UiConstants.frameworkDefaultToolbarIconSize, 8)
		self.assertLessEqual(UiConstants.frameworkDefaultToolbarIconSize, 128)

	def testFrameworkStartupLayoutAttribute(self):
		"""
		This method tests the "frameworkStartupLayout" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkStartupLayout, "\w")

	def testFrameworkHelpFileAttribute(self):
		"""
		This method tests the "frameworkHelpFile" attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkHelpFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

def testNativeImageFormatsAttribute(self):
		"""
		This method tests the "nativeImageFormats" attribute.
		"""

		self.assertIsInstance(UiConstants.nativeImageFormats, dict)
		for key, value in UiConstants.nativeImageFormats:
			self.assertIsInstance(key, str)
			self.assertIsInstance(value, str)
			self.assertTrue(re.compile(value))

def testThirdPartyImageFormatsAttribute(self):
		"""
		This method tests the "thirdPartyImageFormats" attribute.
		"""

		self.assertIsInstance(UiConstants.thirdPartyImageFormats, dict)
		for key, value in UiConstants.thirdPartyImageFormats:
			self.assertIsInstance(key, str)
			self.assertIsInstance(value, str)
			self.assertTrue(re.compile(value))

if __name__ == "__main__":
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
