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
***	testsUiComponent.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		UiComponent Tests Module.
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
import sys
import unittest
from PyQt4.QtGui import QApplication

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
UI_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.ui")

APPLICATION = QApplication(sys.argv)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class ComponentTestCase(unittest.TestCase):
	'''
	This Class Is The ComponentTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		uiComponent = UiComponent()
		requiredAttributes = ("_name",
							"_uiFile",
							"_activated",
							"_deactivatable",
							"_ui")

		for attribute in requiredAttributes:
			self.assertIn(attribute, uiComponent.__dict__)

	def testRequiredMethods(self):
		'''
		This Method Tests Presence Of Required Methods.
		'''

		uiComponent = UiComponent()
		requiredMethods = ("_activate",
						"_deactivate",
						"_loadUi")

		for method in requiredMethods:
			self.assertIn(method, dir(uiComponent))

	def test_activate(self):
		'''
		This Method Tests The "uiComponent" Class "_activate" Method.
		'''

		uiComponent = UiComponent(uiFile=UI_FILE)
		uiComponent._activate()
		self.assertTrue(uiComponent._activated)

	def test_deactivate(self):
		'''
		This Method Tests The "uiComponent" Class "_deactivate" Method.
		'''

		uiComponent = UiComponent()
		uiComponent._activated = True
		uiComponent._deactivate()
		self.assertFalse(uiComponent._activated)

	def test_loadUi(self):
		'''
		This Method Tests The "uiComponent" Class "_loadUi" Method.
		'''

		uiComponent = UiComponent(uiFile=UI_FILE)
		self.assertTrue(uiComponent._loadUi())

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
