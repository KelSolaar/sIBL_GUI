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
***	testsCommon.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Common Tests Module.
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
import os
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.common

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class GetSystemApplicationDatasDirectoryTestCase(unittest.TestCase):
	'''
	This Class Is The GetSystemApplicationDatasDirectoryTestCase Class.
	'''

	def testGetSystemApplicationDatasDirectory(self):
		'''
		This Method Tests The "getSystemApplicationDatasDirectory" definition.
		'''

		path = foundations.common.getSystemApplicationDatasDirectory()
		self.assertIsInstance(path, str)
		self.assertTrue(os.path.exists(path))

class GetUserApplicationDatasDirectoryTestCase(unittest.TestCase):
	'''
	This Class Is The GetUserApplicationDatasDirectory Class.
	'''

	def testGetUserApplicationDatasDirectory(self):
		'''
		This Method Tests The "getUserApplicationDatasDirectory" definition.
		'''

		path = foundations.common.getUserApplicationDatasDirectory()
		self.assertIsInstance(path, str)
		self.assertTrue(os.path.exists(path))

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
