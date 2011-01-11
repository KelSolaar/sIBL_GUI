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

'''
************************************************************************************************
***	sIBL_GUI_getTemplatesReleases.py
***
***	Platform :
***		Windows
***
***	Description :
***		Get Templates Releases.
***
***	Others :
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************
#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
import sys

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
from foundations.io import File
import foundations.parser
from globals.constants import Constants
from foundations.walker import Walker
from foundations.parser import Parser

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

LOGGING_CONSOLE_HANDLER = logging.StreamHandler( sys.stdout )
LOGGING_CONSOLE_HANDLER.setFormatter( core.LOGGING_FORMATTER )
LOGGER.addHandler( LOGGING_CONSOLE_HANDLER )

core.setVerbosityLevel( 3 )

TEMPLATES_PATH = "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates"
TEMPLATES_EXTENSION = "sIBLT"

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def getTemplatesReleases():
	'''
	This Definition Gets Templates Releases.
	'''

	walker = Walker()
	walker.root = TEMPLATES_PATH
	templates = walker.walk( ( TEMPLATES_EXTENSION, ), ( "\._", ) )
	for template in sorted( templates.keys() ) :
		parser = Parser( templates[template] )
		parser.read() and parser.parse()

		LOGGER.info( "{0} | '{1}' : '{2}' !".format( getTemplatesReleases.__name__, template, foundations.parser.getAttributeCompound( "Release", parser.getValue( "Release", "Template", encode = True ) ).value ) )

if __name__ == '__main__':
	getTemplatesReleases()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
