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
***	testsManager.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Manager Tests Module.
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
from manager.manager import Manager, Profile

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
COMPONENTS_DIRECTORY = os.path.join(os.path.dirname(__file__), "components")
COMPONENTS = {"core":{"testsComponentA":"core/testsComponentA",
					"testsComponentB":"core/testsComponentB"},
			"addons":{"testsComponentC":"core/testsComponentC"}}
STANDARD_PROFILE_CONTENT = {"name":"core.testsComponentA",
							"path":os.path.join(COMPONENTS_DIRECTORY, COMPONENTS["core"]["testsComponentA"]),
							"module":"testsComponentA",
							"object_":"TestsComponentA",
							"rank":"10",
							"version":"1.0",
							"author":"Thomas Mansencal",
							"email":"thomas.mansencal@gmail.com",
							"url":"http://www.hdrlabs.com/",
							"description":"Core Tests Component A."}

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class ProfileTestCase(unittest.TestCase):
	'''
	This Class Is The ProfileTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		profile = Profile()
		requiredAttributes = ("_name",
							"_path",
							"_object_",
							"_rank",
							"_import",
							"_interface",
							"_categorie",
							"_module",
							"_version",
							"_author",
							"_email",
							"_url",
							"_description")

		for attribute in requiredAttributes:
			self.assertIn(attribute, profile.__dict__)

class ManagerTestCase(unittest.TestCase):
	'''
	This Class Is The ManagerTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		manager = Manager()
		requiredAttributes = ("_paths",
							"_extension",
							"_categories",
							"_components",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, manager.__dict__)

	def testRequiredMethods(self):
		'''
		This Method Tests Presence Of Required Methods.
		'''

		manager = Manager()
		requiredMethods = ("getProfile",
						"getComponents",
						"gatherComponents",
						"instantiateComponents",
						"reloadComponent",
						"filterComponents",
						"getInterface")

		for method in requiredMethods:
			self.assertIn(method, dir(manager))

	def testGetProfile(self):
		'''
		This Method Tests The "Manager" Class "getProfile" Method.
		'''

		path = os.path.join(COMPONENTS_DIRECTORY, COMPONENTS["core"]["testsComponentA"], "testsComponentA.rc")

		manager = Manager()
		profile = manager.getProfile(path)
		self.assertIsInstance(profile, Profile)
		for attribute, value in STANDARD_PROFILE_CONTENT.items():
			self.assertIsInstance(getattr(profile, attribute), type(value))
			self.assertEqual(getattr(profile, attribute), value)

	def testGatherComponents(self):
		'''
		This Method Tests The "Manager" Class "gatherComponents" Method.
		'''

		manager = Manager({item:os.path.join(COMPONENTS_DIRECTORY, item) for item in COMPONENTS.keys()})
		manager.gatherComponents()
		self.assertIsInstance(manager.components, dict)
		for component in ["{0}.{1}".format(item, name) for item in COMPONENTS.keys() for name in COMPONENTS[item].keys()]:
			self.assertIn(component, manager.components.keys())

	def testInstantiateComponents(self):
		'''
		This Method Tests The "Manager" Class "instantiateComponents" Method.
		'''

		manager = Manager({item:os.path.join(COMPONENTS_DIRECTORY, item) for item in COMPONENTS.keys()})
		manager.gatherComponents()
		manager.instantiateComponents()

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
