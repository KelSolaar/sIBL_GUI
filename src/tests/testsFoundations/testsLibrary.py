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
***	testsLibrary.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Library Tests Module.
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
import ctypes
import os
import platform
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
from foundations.library import Library, LibraryHook

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LIBRARIES_DIRECTORY = "libraries"
if platform.system() == "Windows" or platform.system() == "Microsoft":
	FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/resources/FreeImage.dll")
elif platform.system() == "Darwin":
	FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/resources/libfreeimage.dylib")
elif platform.system() == "Linux":
	FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/resources/libfreeimage.so")


LIBRARIES = {"freeImage":os.path.normpath(os.path.join(os.path.dirname(__file__), "../../", FREEIMAGE_LIBRARY))}

LIBRARIES_FUNCTIONS = {"freeImage":(LibraryHook(name="FreeImage_GetVersion" , affixe="@0", argumentsType=None, returnValue=ctypes.c_char_p),
								LibraryHook(name="FreeImage_GetCopyrightMessage" , affixe="@0", argumentsType=None, returnValue=ctypes.c_char_p))}

LIBRARIES_TESTS_CASES = {"freeImage":{"FreeImage_GetVersion":"3.13.1",
							"FreeImage_GetCopyrightMessage":"This program uses FreeImage, a free, open source image library supporting all common bitmap formats. See http://freeimage.sourceforge.net for details"}}
#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class LibraryTestCase(unittest.TestCase):
	'''
	This Class Is The LibraryTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		library = Library(LIBRARIES["freeImage"], LIBRARIES_FUNCTIONS["freeImage"])
		requiredAttributes = ("_libraryInstantiated",
								"_libraryPath",
								"_functions",
								"_library")
		for attribute in requiredAttributes:
			self.assertIn(attribute, library.__dict__)

		requiredClassAttributes = ("_librariesInstances",
								"_callback",
								)
		for classAttribute in requiredClassAttributes:
			self.assertIn(classAttribute, dir(library))

	def testRequiredMethods(self):
		'''
		This Method Tests Presence Of Required Methods.
		'''

		library = Library(LIBRARIES["freeImage"], LIBRARIES_FUNCTIONS["freeImage"])
		requiredMethods = ("bindLibrary",
							"bindFunction")

		for method in requiredMethods:
			self.assertIn(method, dir(library))

	def testBindFunction(self):
		'''
		This Method Tests The "Library" Class "bindFunction" Method.
		'''

		for name, path in LIBRARIES.items():
			library = Library(path)
			library.functions = LIBRARIES_FUNCTIONS[name]
			for function in LIBRARIES_FUNCTIONS[name]:
				hasattr(library, function.name) and delattr(library, function.name)
				library.bindFunction(function)
				self.assertTrue(hasattr(library, function.name))

	def testBindLibrary(self):
		'''
		This Method Tests The "Library" Class "bindLibrary" Method.
		'''

		for name, path in LIBRARIES.items():
			library = Library(path)
			library.functions = LIBRARIES_FUNCTIONS[name]
			for function in LIBRARIES_FUNCTIONS[name]:
				hasattr(library, function.name) and delattr(library, function.name)
			library.bindLibrary()
			for function in LIBRARIES_FUNCTIONS[name]:
				self.assertTrue(hasattr(library, function.name))

	def testLibrary(self):
		'''
		This Method Tests The "Library" Class Binding.
		'''

		for name, path in LIBRARIES.items():
			library = Library(path, LIBRARIES_FUNCTIONS[name])
			for function, value in LIBRARIES_TESTS_CASES[name].items():
				self.assertEqual(getattr(library, function)(), value)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
