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
***	testsCore.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Core Tests Module.
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
import inspect
import logging
import types
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class StandardMessageHookTestCase(unittest.TestCase):
	'''
	This Class Is The StandardMessageHookTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		hook = core.StandardMessageHook(None)
		requiredAttributes = ("_logger",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, hook.__dict__)

	def testRequiredMethods(self):
		'''
		This Method Tests Presence Of Required Methods.
		'''

		hook = core.StandardMessageHook(None)
		requiredMethods = ("write",)

		for method in requiredMethods:
			self.assertIn(method, dir(hook))

class SetVerbosityLevelTestCase(unittest.TestCase):
	'''
	This Class Is The SetVerbosityLevelTestCase Class.
	'''

	def testSetVerbosityLevel(self):
		'''
		This Method Tests The "setVerbosityLevel" definition.
		'''

		LOGGER = logging.getLogger(Constants.logger)
		levels = {logging.CRITICAL:0, logging.ERROR:1, logging.WARNING:2, logging.INFO:3, logging.DEBUG:4  }
		for level, value in levels.items():
			core.setVerbosityLevel(value)
			self.assertEqual(level, LOGGER.level)

class GetFrameTestCase(unittest.TestCase):
	'''
	This Class Is The GetFrameTestCase Class.
	'''

	def testGetFrame(self):
		'''
		This Method Tests The "getFrame" definition.
		'''

		self.assertIsInstance(core.getFrame(0), inspect.currentframe().__class__)

class GetCodeLayerNameTestCase(unittest.TestCase):
	'''
	This Class Is The GetCodeLayerNameTestCase Class.
	'''

	def testGetCodeLayerName(self):
		'''
		This Method Tests The "getCodeLayerName" definition.
		'''

		codeLayerName = core.getCodeLayerName()
		self.assertIsInstance(codeLayerName, str)
		self.assertEqual(codeLayerName, inspect.currentframe().f_code.co_name)

class GetModuleTestCase(unittest.TestCase):
	'''
	This Class Is The GetCodeLayerNameTestCase Class.
	'''

	def testGetModule(self):
		'''
		This Method Tests The "getModule" definition.
		'''

		self.assertEqual(type(core.getModule(object)), types.ModuleType)
		self.assertEqual(core.getModule(object), inspect.getmodule(object))

class GetObjectNameTestCase(unittest.TestCase):
	'''
	This Class Is The GetObjectNameTestCase Class.
	'''

	def testGetObjectName(self):
		'''
		This Method Tests The "getObjectName" definition.
		'''

		objectName = core.getObjectName(object)
		self.assertIsInstance(objectName, str)
		self.assertEqual(objectName, "__builtin__ | testGetObjectName.object()")

if __name__ == "__main__":
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
