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
***	strings.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Strings Module.
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
import logging
import os
import platform
import re

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import core
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@core.executionTrace
def getNiceName(name):
	'''
	This Definition Converts A String To Nice String : currentLogText -> Current Log Text.

	@param name: Current String To Be Nicified. ( String )
	@return: Nicified String. ( String )
	'''

	niceName = ""
	for index in range(len(name)):
		if index == 0:
			niceName += name[ index ].upper()
		else:
			if name[ index ].upper() == name[ index ]:
				if index + 1 < len(name):
					if  name[ index + 1 ].upper() != name[ index + 1 ]:
						niceName += " " + name[ index ]
					else:
						LOGGER.debug("> '{0}' To '{1}'.".format(name, name))
						return name
				else:
					niceName += name[ index ]
			else:
				niceName += name[ index ]
	LOGGER.debug("> '{0}' To '{1}'.".format(name, niceName))
	return niceName

@core.executionTrace
def getVersionRank(version):
	'''
	This Definition Converts A Version String To It's Rank.

	@param version: Current Version To Calculate Rank. ( String )
	@return: Rank. ( Integer )
	'''

	tokens = version.split(".")
	rank = sum([int(10 ** (i - 1)) * int(tokens[-i]) for i in range(len(tokens), 0, -1)])
	LOGGER.debug("> Rank : '{0}'.".format(rank))
	return rank

@core.executionTrace
def replace(string, datas):
	'''
	This Definition Replaces The Datas Occurences In The String.
	@param string: String To Manipulate. ( String )
	@param datas: Replacement Occurences. ( Dictionary )
	@return: Manipulated String. ( String )
	'''

	for old, new in datas.items():
		string = string.replace(old, new)
	return string

@core.executionTrace
def toForwardSlashes(datas):
	'''
	This Definition Converts Backward Slashes To Forward Slashes.

	@param datas: Datas To Convert. ( String )	
	@return: Converted Path. ( String )
	'''

	datas = datas.replace("\\", "/")
	LOGGER.debug("> Datas : '{0}' To Forward Slashes.".format(datas))
	return datas

@core.executionTrace
def toBackwardSlashes(datas):
	'''
	This Definition Converts Forward Slashes To Backward Slashes.

	@param datas: Datas To Convert. ( String )	
	@return: Converted Path. ( String )
	'''

	datas = datas.replace("/", "\\")
	LOGGER.debug("> Datas : '{0}' To Backward Slashes.".format(datas))
	return datas

@core.executionTrace
def getNormalizedPath(path):
	'''
	This Definition Normalizes A Path, Escaping Slashes If Needed On Windows.

	@param path: Path To Normalize. ( String )
	@return: Normalized Path. ( String )
	'''

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		path = os.path.normpath(path).replace("\\", "\\\\")
		LOGGER.debug("> Path : '{0}', Normalized Path.".format(path))
		return path
	else:
		path = os.path.normpath(path)
		LOGGER.debug("> Path : '{0}', Normalized Path.".format(path))
		return path

@core.executionTrace
def isEmail(datas):
	'''
	This Definition Check If Provided Datas String Is An Email.

	@param datas: Datas To Check. ( String )	
	@return: Is Email. ( Boolean )
	'''

	if re.match("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}", datas):
		LOGGER.debug("> {0}' Is Matched As Email.".format(datas))
		return True
	else:
		LOGGER.debug("> {0}' Is Not Matched As Email.".format(datas))
		return False

@core.executionTrace
def isWebsite(datas):
	'''
	This Definition Check If Provided Datas String Is A Website.

	@param datas: Datas To Check. ( String )	
	@return: Is Website. ( Boolean )
	'''

	if re.match("(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?", datas):
		LOGGER.debug("> {0}' Is Matched As Website.".format(datas))
		return True
	else:
		LOGGER.debug("> {0}' Is Not Matched As Website.".format(datas))
		return False

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
