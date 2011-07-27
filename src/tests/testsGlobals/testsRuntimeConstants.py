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
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**testsRuntimeConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Runtime constants tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from umbra.globals.runtimeConstants import RuntimeConstants

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class RuntimeConstantsTestCase(unittest.TestCase):
	"""
	This class is the RuntimeConstantsTestCase class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

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

if __name__ == "__main__":
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
