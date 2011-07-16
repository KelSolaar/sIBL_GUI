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

"""
************************************************************************************************
***	testsUiConstants.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Ui UiConstants Tests Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import re
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
from umbra.globals.uiConstants import UiConstants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class UiConstantsTestCase(unittest.TestCase):
	"""
	This Class Is The UiConstantsTestCase Class.
	"""

	def testRequiredAttributes(self):
		"""
		This Method Tests Presence Of Required Attributes.
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
		This Method Tests The "frameworkUiFile" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkUiFile, "\w")

	def testFrameworkWindowsStylesheetFileAttribute(self):
		"""
		This Method Tests The "frameworkWindowsStylesheetFile" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkWindowsStylesheetFile, "\w")

	def testFrameworkDarwinStylesheetFileAttribute(self):
		"""
		This Method Tests The "frameworkDarwinStylesheetFile" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkDarwinStylesheetFile, "\w")

	def testFrameworkLinuxStylesheetFileAttribute(self):
		"""
		This Method Tests The "frameworkLinuxStylesheetFile" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLinuxStylesheetFile, "\w")

	def testFrameworkLayoutsFileAttribute(self):
		"""
		This Method Tests The "frameworkLayoutsFile" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLayoutsFile, "\w")

	def testFrameworkApplicationWindowsIconAttribute(self):
		"""
		This Method Tests The "frameworkApplicationWindowsIcon" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkApplicationWindowsIcon, "\w")
		self.assertRegexpMatches(UiConstants.frameworkApplicationWindowsIcon, "\.[pP][nN][gG]$")

	def testFrameworkApplicationDarwinIconAttribute(self):
		"""
		This Method Tests The "frameworkApplicationDarwinIcon" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkApplicationDarwinIcon, "\w")
		self.assertRegexpMatches(UiConstants.frameworkApplicationDarwinIcon, "\.[pP][nN][gG]$")

	def testFrameworkLogoPictureAttribute(self):
		"""
		This Method Tests The "frameworkLogoPicture" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkLogoPicture, "\w")
		self.assertRegexpMatches(UiConstants.frameworkLogoPicture, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testFrameworkDefaultToolbarIconSizeAttribute(self):
		"""
		This Method Tests The "frameworkDefaultToolbarIconSize" Attribute.
		"""

		self.assertIsInstance(UiConstants.frameworkDefaultToolbarIconSize, int)
		self.assertGreaterEqual(UiConstants.frameworkDefaultToolbarIconSize, 8)
		self.assertLessEqual(UiConstants.frameworkDefaultToolbarIconSize, 128)

	def testFrameworkStartupLayoutAttribute(self):
		"""
		This Method Tests The "frameworkStartupLayout" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkStartupLayout, "\w")

	def testFrameworkHelpFileAttribute(self):
		"""
		This Method Tests The "frameworkHelpFile" Attribute.
		"""

		self.assertRegexpMatches(UiConstants.frameworkHelpFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

def testNativeImageFormatsAttribute(self):
		"""
		This Method Tests The "nativeImageFormats" Attribute.
		"""

		self.assertIsInstance(UiConstants.nativeImageFormats, dict)
		for key, value in UiConstants.nativeImageFormats:
			self.assertIsInstance(key, str)
			self.assertIsInstance(value, str)
			self.assertTrue(re.compile(value))

def testThirdPartyImageFormatsAttribute(self):
		"""
		This Method Tests The "thirdPartyImageFormats" Attribute.
		"""

		self.assertIsInstance(UiConstants.thirdPartyImageFormats, dict)
		for key, value in UiConstants.thirdPartyImageFormats:
			self.assertIsInstance(key, str)
			self.assertIsInstance(value, str)
			self.assertTrue(re.compile(value))

if __name__ == '__main__':
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
