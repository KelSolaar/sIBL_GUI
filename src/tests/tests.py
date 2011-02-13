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
***	tests.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Tests Suite Module.
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

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
def testsSuite():
	testsLoader = unittest.TestLoader()
	return testsLoader.discover(os.path.dirname(__file__))

if __name__ == '__main__':
	import utilities
	unittest.TextTestRunner(verbosity=2).run(testsSuite())

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
