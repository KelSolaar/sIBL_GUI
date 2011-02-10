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
***	testsRuntimeConstants.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Runtime Constants Tests Module.
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
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
from globals.runtimeConstants import RuntimeConstants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class RuntimeConstantsTestCase(unittest.TestCase):
	'''
	This Class Is The RuntimeConstantsTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		requiredAttributes = ("parameters",
								"args",
								"loggingConsoleHandler",
								"loggingFileHandler",
								"loggingSessionHandler",
								"loggingSessionHandlerStream",
								"verbosityLevel",
								"loggingFile",
								"application",
								"userApplicationDatasDirectory",
								"uiFile",
								"ui",
								"settingsFile",
								"settings")

		for attribute in requiredAttributes:
			self.assertIn(attribute, RuntimeConstants.__dict__)

if __name__ == '__main__':
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
