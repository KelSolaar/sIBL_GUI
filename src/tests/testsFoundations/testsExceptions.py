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
***	testsExceptions.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Exceptions Tests Module.
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
import foundations.exceptions

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
EXCEPTIONS = (foundations.exceptions.AttributeStructureError,
				foundations.exceptions.ComponentActivationError,
				foundations.exceptions.ComponentDeactivationError,
				foundations.exceptions.DatabaseOperationError,
				foundations.exceptions.DirectoryExistsError,
				foundations.exceptions.FileExistsError,
				foundations.exceptions.FileStructureError,
				foundations.exceptions.LibraryExecutionError,
				foundations.exceptions.LibraryInitializationError,
				foundations.exceptions.LibraryInstantiationError,
				foundations.exceptions.NetworkError,
				foundations.exceptions.ObjectExistsError,
				foundations.exceptions.ObjectTypeError,
				foundations.exceptions.ProgrammingError,
				foundations.exceptions.SocketConnectionError,
				foundations.exceptions.UserError)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************

class ExceptionsTestCase(unittest.TestCase):
	'''
	This Class Is The ExceptionsTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		requiredAttributes = ("value",)
		for exception in EXCEPTIONS:
			exceptionInstance = exception(None)
			for attribute in requiredAttributes:
				self.assertIn(attribute, exceptionInstance.__dict__)

	def test__str__(self):
		'''
		This Method Tests The "Exceptions" Class "__str__" Method.
		'''

		for exception in EXCEPTIONS:
			exceptionInstance = exception("{0} Exception Raised !".format(exception.__class__))
			self.assertIsInstance(exceptionInstance.__str__(), str)
			exceptionInstance = exception([exception.__class__, "Exception Raised !"])
			self.assertIsInstance(exceptionInstance.__str__(), str)
			exceptionInstance = exception(0)
			self.assertIsInstance(exceptionInstance.__str__(), str)

if __name__ == "__main__":
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
