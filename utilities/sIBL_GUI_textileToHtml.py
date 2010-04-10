#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2010 - Thomas Mansencal - kelsolaar_fool@hotmail.com
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
***	sIBL_GUI_textileToHtml.py
***
***	Platform :
***		Windows
***
***	Description :
***		Converts A Textile File To HTML.
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
import textile

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
from foundations.io import File
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

LOGGING_CONSOLE_HANDLER = logging.StreamHandler( sys.stdout )
LOGGING_CONSOLE_HANDLER.setFormatter( core.LOGGING_FORMATTER )
LOGGER.addHandler( LOGGING_CONSOLE_HANDLER )

core.setVerbosityLevel( 3 )

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def textileToHtml( fileIn, fileOut, title ):
	'''
	This Method Outputs A Textile File To HTML.
		
	@param fileIn: File To Convert. ( String )
	@param fileOut: Output File. ( String )
	@param title: HTML File Title. ( String )
	'''

	LOGGER.info( "{0} | Converting '{1}' Textile File To HTML !".format( textileToHtml.__name__, fileIn ) )
	file = File( fileIn )
	file.read()

	output = []
	output.append( "<html>\n\t<head>\n" )
	output.append( "\t\t<title>{0}</title>\n".format( title ) )
	output.append( 
			"""\t\t<style type="text/css">
	            body {
	                text-align: justify;
	                margin: 10px 10px 10px 10px;
	                background-color: rgb(192, 192, 192);
	                color: rgb(45, 50, 50);
	            }
	            A:link {
	                text-decoration: none;
	                color: rgb(100, 120, 135);
	            }
	            A:visited {
	                text-decoration: none;
	                color: rgb(100, 120, 135);
	            }
	            A:active {
	                text-decoration: none;
	                color: rgb(100, 120, 135);
	            }
	            A:hover {
	                text-decoration: underline;
	                color: rgb(100, 120, 135);
	            }
	        </style>\n""" )
	output.append( "\t</head>\n\t<body>\n" )
	output.append( "\t\t<span>\n\t\t" )
	output.append( "\n\t\t".join( [line for line in textile.textile( "".join( file.content ) ).split( "\n" ) if line] ) )
	output.append( "\t\t</span>\n" )
	output.append( "\t</body>\n</html>" )

	file = File( fileOut )
	file.content = output
	file.write()

if __name__ == '__main__':
	textileToHtml( sys.argv[1], sys.argv[2], sys.argv[3] )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
