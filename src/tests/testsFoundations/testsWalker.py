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
***	testsWalker.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Walker Tests Module.
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
import re
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
from foundations.strings import replace
from foundations.walker import Walker

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
ROOT_DIRECTORY = "standard"
TREE_HIERARCHY = ("loremIpsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT",
					"level_0/standard.ibl",
					"level_0/level_1/loremIpsum.txt", "level_0/level_1/standard.rc",
					"level_0/level_1/level_2/standard.sIBLT")

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class WalkerTestCase(unittest.TestCase):
	'''
	This Class Is The WalkerTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		walker = Walker(RESOURCES_DIRECTORY)
		requiredAttributes = ("_root",
								"_files")

		for attribute in requiredAttributes:
			self.assertIn(attribute, walker.__dict__)

	def testRequiredMethods(self):
		'''
		This Method Tests Presence Of Required Methods.
		'''

		walker = Walker(RESOURCES_DIRECTORY)
		requiredMethods = ("walk",)

		for method in requiredMethods:
			self.assertIn(method, dir(walker))

	def testWalk(self):
		'''
		This Method Tests The "Walker" Class "walk" Method.
		'''

		walker = Walker()
		walker.root = os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY)
		walker.walk()
		for path in walker.files.values():
			self.assertTrue(os.path.exists(path))

		referencePaths = [replace(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY, path), {"/":"|", "\\":"|"}) for path in TREE_HIERARCHY]
		walkerFiles = [replace(path, {"/":"|", "\\":"|"}) for path in walker.files.values()]
		for item in referencePaths:
			self.assertIn(item, walkerFiles)

		walker.walk(filtersOut=("\.rc$",))
		walkerFiles = [replace(path, {"/":"|", "\\":"|"}) for path in walker.files.values()]
		for item in walkerFiles:
				self.assertTrue(not re.search("\.rc$", item))

		walker.walk(filtersOut=("\.ibl", "\.rc$", "\.sIBLT$", "\.txt$"))
		self.assertTrue(not walker.files)

		referencePaths = [replace(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY, path), {"/":"|", "\\":"|"}) for path in TREE_HIERARCHY if re.search("\.rc$", path)]
		walker.walk(filtersIn=("\.rc$",))
		walkerFiles = [replace(path, {"/":"|", "\\":"|"}) for path in walker.files.values()]
		for item in referencePaths:
			self.assertIn(item, walkerFiles)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
