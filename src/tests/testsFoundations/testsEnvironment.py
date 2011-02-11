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
***	testsEnvironment.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Environment Tests Module.
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
from foundations.environment import Environment

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class EnvironmentTestCase(unittest.TestCase):
	'''
	This Class Is The EnvironmentTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		environment = Environment()
		requiredAttributes = ("_variable",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, environment.__dict__)

	def testRequiredMethods(self):
		'''
		This Method Tests Presence Of Required Methods.
		'''

		environment = Environment()
		requiredMethods = ("getPath",)

		for method in requiredMethods:
			self.assertIn(method, dir(environment))

	def testGetPath(self):
		'''
		This Method Tests The "Environment" Class "getPath" Method.
		'''

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			environment = Environment("APPDATA")
		elif platform.system() == "Darwin":
			environment = Environment("HOME")
		elif platform.system() == "Linux":
			environment = Environment("HOME")
		self.assertTrue(environment.getPath())
		self.assertIsInstance(environment.getPath(), str)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
