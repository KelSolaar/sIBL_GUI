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
#***********************************************************s************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	Walker.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Walker Module
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
import re

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import core
import foundations.exceptions
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Walker( object ):
	'''
	This Class Provides Methods For Walking In A Directory.
	'''

	@core.executionTrace
	def __init__( self, root = None ):
		'''
		This Method Initializes The Class.

		@param root: Root Directory Path To Recurse. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		# --- Setting Class Attributes. ---
		self._root = None
		self.root = root

		self._files = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def root( self ):
		'''
		This Method Is The Property For The _root Attribute.

		@return: self._root. ( String )
		'''

		return self._root

	@root.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def root( self, value ):
		'''
		This Method Is The Setter Method For The _root Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type( value ) in ( str, unicode ), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format( "root", value )
			assert os.path.exists( value ), "'{0}' Attribute : '{1}' Directory Doesn't Exists !".format( "root", value )
		self._root = value

	@root.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def root( self ):
		'''
		This Method Is The Deleter Method For The _root Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "root" ) )

	@property
	def files( self ):
		'''
		This Method Is The Property For The _files Attribute.

		@return: self._files. ( Dictionary )
		'''

		return self._files

	@files.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def files( self, value ):
		'''
		This Method Is The Setter Method For The _files Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		'''

		if value :
			assert type( value ) is dict, "'{0}' Attribute : '{1}' Type Is Not 'dict' !".format( "files", value )
		self._files = value

	@files.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def files( self ):
		'''
		This Method Is The Deleter Method For The _files Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "files" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler()
	def walk( self, filtersIn = None, filtersOut = None ):
		'''
		This Method Gets Root Directory Files List As A Dictionary.

		@param filtersIn: Regex filtersIn String. ( String )
		@param filtersIn: Regex filtersOut String. ( String )
		@return: Files List. ( Dictionary Or None )
		'''

		if filtersIn :
			LOGGER.debug( "> Current filtersIn : '{0}'.".format( filtersIn ) )

		if self._root :
				self._files = {}
				for root, dirs, files in os.walk( self._root, topdown = False ):
					for item in files:
						LOGGER.debug( "> Current File : '{0}' In '{1}'.".format( item, self._root ) )
						itemPath = os.path.join( root, item ).replace( "\\", "/" )
						if os.path.isfile( itemPath ):
							if filtersIn :
								filterMatched = False
								for filter in filtersIn :
									if not re.search( filter, itemPath ):
										LOGGER.debug( "> '{0}' File Skipped, Filter In '{1}' Not Matched !.".format( itemPath, filter ) )
									else :
										filterMatched = True
										break
								if not filterMatched :
									continue

							if filtersOut :
								filterMatched = False
								for filter in filtersOut :
									if re.search( filter, itemPath ) :
										LOGGER.debug( "> '{0}' File Skipped, Filter Out '{1}' Matched !.".format( itemPath, filter ) )
										filterMatched = True
										break
								if filterMatched :
									continue

							LOGGER.debug( "> '{0}' File Filtered In !".format( itemPath ) )

							fileTokens = os.path.splitext( item )
							if fileTokens[0] in self._files:
								itemName = itemPath.replace( self._root, "" ).replace( "/", "|" ).replace( item, "" ) + fileTokens[0]
								LOGGER.debug( "> Adding '{0}' With Path : '{1}' To Files List.".format( itemName, itemPath ) )
								self._files[itemName] = itemPath
							else:
								LOGGER.debug( "> Adding '{0}' With Path : '{1}' To Files List.".format( fileTokens[0], itemPath ) )
								self._files[fileTokens[0]] = itemPath
				return self._files

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
