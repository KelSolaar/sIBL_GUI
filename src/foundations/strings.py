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
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	strings.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Strings Module.
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
import platform

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import core
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@core.executionTrace
def getNiceName( name ) :
	'''
	This Definition Converts A String To Nice String : currentLogText -> Current Log Text.

	@param name: Current String To Be Nicified. ( String )
	@return: Nicified String. ( String )
	'''

	niceName = ""
	for index in range( len( name ) ) :
		if index == 0:
			niceName += name[ index ].upper()
		else :
			if name[ index ].upper() == name[ index ]:
				if index + 1 < len( name ) :
					if  name[ index + 1 ].upper() != name[ index + 1 ]:
						niceName += " " + name[ index ]
					else :
						LOGGER.debug( "> '{0}' To '{1}'.".format( name, name ) )
						return name
				else:
					niceName += name[ index ]
			else:
				niceName += name[ index ]
	LOGGER.debug( "> '{0}' To '{1}'.".format( name, niceName ) )
	return niceName

@core.executionTrace
def getVersionRank( version ):
	'''
	This Definition Converts A Version String To It's Rank.

	@param version: Current Version To Calculate Rank. ( String )
	@return: Rank. ( Integer )
	'''

	tokens = version.split( "." )
	return sum( [int( 10 ** ( i - 1 ) ) * int( tokens[-i] ) for i in range( len( tokens ), 0, -1 )] )

@core.executionTrace
def getNormalizedPath( path ):
	'''
	This Definition Normalizes A Path, Escaping Slashes If Needed On Windows.

	@param path: Path To Normalize. ( String )
	@return: Normalized Path. ( String )
	'''

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		return os.path.normpath( path ).replace( "\\", "\\\\" )
	else :
		return os.path.normpath( path )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
