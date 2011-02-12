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
***	testsStrings.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Strings Tests Module.
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
import platform
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.strings

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class GetNiceNameTestCase(unittest.TestCase):
	'''
	This Class Is The GetNiceNameTestCase Class.
	'''

	def testGetNiceName(self):
		'''
		This Method Tests The "getNiceName" Definition.
		'''

		self.assertIsInstance(foundations.strings.getNiceName("testGetNiceName"), str)
		self.assertEqual(foundations.strings.getNiceName("testGetNiceName"), "Test Get Nice Name")
		self.assertEqual(foundations.strings.getNiceName("TestGetNiceName"), "Test Get Nice Name")
		self.assertEqual(foundations.strings.getNiceName("_testGetNiceName"), "_test Get Nice Name")
		self.assertEqual(foundations.strings.getNiceName("Test Get NiceName"), "Test Get NiceName")

class GetVersionRankTestCase(unittest.TestCase):
	'''
	This Class Is The GetVersionRankTestCase Class.
	'''

	def testGetVersionRank(self):
		'''
		This Method Tests The "getVersionRank" Definition.
		'''

		self.assertIsInstance(foundations.strings.getVersionRank("0.0.0"), int)
		self.assertEqual(foundations.strings.getVersionRank("0.0.0"), 0)
		self.assertEqual(foundations.strings.getVersionRank("0.1.0"), 10)
		self.assertEqual(foundations.strings.getVersionRank("1.1.0"), 110)
		self.assertEqual(foundations.strings.getVersionRank("1.2.3.4.5"), 12345)

class ReplaceTestCase(unittest.TestCase):
	'''
	This Class Is The ReplaceTestCase Class.
	'''

	def testReplace(self):
		'''
		This Method Tests The "replace" Definition.
		'''

		self.assertIsInstance(foundations.strings.replace("To@Forward|Slashes@Test|Case", {}), str)
		self.assertEqual(foundations.strings.replace("To@Forward|Slashes@Test|Case", {"@":"|", "|":":"}), "To:Forward:Slashes:Test:Case")
		self.assertEqual(foundations.strings.replace("To@Forward@Slashes@Test@Case", {"@":"|", "|":"@", "@":"|" }), "To@Forward@Slashes@Test@Case")

class ToForwardSlashesTestCase(unittest.TestCase):
	'''
	This Class Is The ToForwardSlashesTestCase Class.
	'''

	def testToForwardSlashes(self):
		'''
		This Method Tests The "toForwardSlashes" Definition.
		'''

		self.assertIsInstance(foundations.strings.toForwardSlashes("To\Forward\Slashes\Test\Case"), str)
		self.assertEqual(foundations.strings.toForwardSlashes("To\Forward\Slashes\Test\Case"), "To/Forward/Slashes/Test/Case")
		self.assertEqual(foundations.strings.toForwardSlashes("\Users/JohnDoe\Documents"), "/Users/JohnDoe/Documents")

class ToBackwardSlashesTestCase(unittest.TestCase):
	'''
	This Class Is The ToBackwardSlashesTestCase Class.
	'''

	def testToBackwardSlashes(self):
		'''
		This Method Tests The "toBackwardSlashes" Definition.
		'''

		self.assertIsInstance(foundations.strings.toBackwardSlashes("\Users\JohnDoe\Documents"), str)
		self.assertEqual(foundations.strings.toBackwardSlashes("To/Forward/Slashes/Test/Case"), "To\Forward\Slashes\Test\Case")
		self.assertEqual(foundations.strings.toBackwardSlashes("/Users/JohnDoe/Documents"), "\Users\JohnDoe\Documents")

class GetNormalizedPathTestCase(unittest.TestCase):
	'''
	This Class Is The GetNormalizedPathTestCase Class.
	'''

	def testGetNormalizedPath(self):
		'''
		This Method Tests The "getNormalizedPath" Definition.
		'''

		self.assertIsInstance(foundations.strings.getNormalizedPath("/Users/JohnDoe/Documents"), str)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			self.assertEqual(foundations.strings.getNormalizedPath("C:/Users\JohnDoe/Documents"), r"C:\\Users\\JohnDoe\\Documents")
			self.assertEqual(foundations.strings.getNormalizedPath("C://Users\/JohnDoe//Documents/"), r"C:\\Users\\JohnDoe\\Documents")
			self.assertEqual(foundations.strings.getNormalizedPath("C:\\Users\\JohnDoe\\Documents"), r"C:\\Users\\JohnDoe\\Documents")
		else:
			self.assertEqual(foundations.strings.getNormalizedPath("/Users/JohnDoe/Documents/"), "/Users/JohnDoe/Documents")
			self.assertEqual(foundations.strings.getNormalizedPath("/Users\JohnDoe/Documents"), "/Users\JohnDoe/Documents")

class IsEmailTestCase(unittest.TestCase):
	'''
	This Class Is The IsEmailTestCase Class.
	'''

	def testIsEmail(self):
		'''
		This Method Tests The "isEmail" Definition.
		'''

		self.assertIsInstance(foundations.strings.isEmail("john.doe@domain.com"), bool)
		self.assertTrue(foundations.strings.isEmail("john.doe@domain.com"))
		self.assertTrue(foundations.strings.isEmail("john.doe@domain.server.department.company.com"))
		self.assertFalse(foundations.strings.isEmail("john.doe"))
		self.assertFalse(foundations.strings.isEmail("john.doe@domain"))

class IsWebsiteTestCase(unittest.TestCase):
	'''
	This Class Is The IsWebsiteTestCase Class.
	'''

	def testIsWebsite(self):
		'''
		This Method Tests The "isWebsite" Definition.
		'''

		self.assertIsInstance(foundations.strings.isWebsite("http://domain.com"), bool)
		self.assertTrue(foundations.strings.isWebsite("http://www.domain.com"))
		self.assertTrue(foundations.strings.isWebsite("http://domain.com"))
		self.assertTrue(foundations.strings.isWebsite("https://domain.com"))
		self.assertTrue(foundations.strings.isWebsite("ftp://domain.com"))
		self.assertTrue(foundations.strings.isWebsite("http://domain.subdomain.com"))
		self.assertFalse(foundations.strings.isWebsite(".com"))
		self.assertFalse(foundations.strings.isWebsite("domain.com"))

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
