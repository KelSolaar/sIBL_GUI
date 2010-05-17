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
***	Parser.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL Input And Output Module.
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
import collections
import logging
import re

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import core
import foundations.exceptions
import io
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class AttributeCompound( core.Structure ):
	'''
	This Is The AttributeCompound Class.
	'''

	@core.executionTrace
	def __init__( self, **kwargs ):
		'''
		This Method Initializes The Class.

		@param kwargs: name, value, link, type, alias. ( Key / Value Pairs )
		'''

		core.Structure.__init__( self, **kwargs )

		# --- Setting Class Attributes. ---
		self.__dict__.update( kwargs )

class Parser( io.File ):
	'''
	This Class Provides Methods To Parse Sections File Format Files.
	'''

	@core.executionTrace
	def __init__( self, file = None, splitter = "=", namespaceSplitter = "|", commentLimiter = ";", rawSectionContentIdentifier = "_rawSectionContent" ):
		'''
		This Method Initializes The Class.

		@param file: Current File Path. ( String ) 
		@param splitter: Splitter Character. ( String )
		@param namespaceSplitter: Namespace Splitter Character. ( String )
		@param commentLimiter: Comment Limiter Character. ( String )
		@param rawSectionContentIdentifier: Raw Section Content Identifier. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		io.File.__init__( self, file )

		# --- Setting Class Attributes. ---
		self._splitter = None
		self.splitter = splitter
		self._namespaceSplitter = None
		self.namespaceSplitter = namespaceSplitter
		self._commentLimiter = None
		self.commentLimiter = commentLimiter
		self._rawSectionContentIdentifier = None
		self.rawSectionContentIdentifier = rawSectionContentIdentifier

		self._sections = None
		self._comments = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def splitter( self ):
		'''
		This Method Is The Property For The _splitter Attribute.

		@return: self._splitter. ( String )
		'''

		return self._splitter

	@splitter.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def splitter( self, value ):
		'''
		This Method Is The Setter Method For The _splitter Attribute.

		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type( value ) in ( str, unicode ), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format( "splitter", value )
			assert len( value ) == 1, "'{0}' Attribute : '{1}' Has Multiples Characters !".format( "splitter", value )
			assert not re.search( "\w", value ), "'{0}' Attribute : '{1}' Is An AlphaNumeric Character !".format( "splitter", value )
		self._splitter = value

	@splitter.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def splitter( self ):
		'''
		This Method Is The Deleter Method For The _splitter Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "splitter" ) )

	@property
	def namespaceSplitter( self ):
		'''
		This Method Is The Property For The _namespaceSplitter Attribute.

		@return: self._namespaceSplitter. ( String )
		'''

		return self._namespaceSplitter

	@namespaceSplitter.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def namespaceSplitter( self, value ):
		'''
		This Method Is The Setter Method For The _namespaceSplitter Attribute.

		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type( value ) in ( str, unicode ), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format( "namespaceSplitter", value )
			assert len( value ) == 1, "'{0}' Attribute : '{1}' Has Multiples Characters !".format( "namespaceSplitter", value )
			assert not re.search( "\w", value ), "'{0}' Attribute : '{1}' Is An AlphaNumeric Character !".format( "namespaceSplitter", value )
		self._namespaceSplitter = value

	@namespaceSplitter.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def namespaceSplitter( self ):
		'''
		This Method Is The Deleter Method For The _namespaceSplitter Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "namespaceSplitter" ) )

	@property
	def commentLimiter( self ):
		'''
		This Method Is The Property For The _commentLimiter Attribute.

		@return: self._commentLimiter. ( String )
		'''

		return self._commentLimiter

	@commentLimiter.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def commentLimiter( self, value ):
		'''
		This Method Is The Setter Method For The _commentLimiter Attribute.
	
		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type( value ) in ( str, unicode ), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format( "commentLimiter", value )
			assert not re.search( "\w", value ), "'{0}' Attribute : '{1}' Is An AlphaNumeric Character !".format( "commentLimiter", value )
		self._commentLimiter = value

	@commentLimiter.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def commentLimiter( self ):
		'''
		This Method Is The Deleter Method For The _commentLimiter Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "commentLimiter" ) )

	@property
	def rawSectionContentIdentifier( self ):
		'''
		This Method Is The Property For The _rawSectionContentIdentifier Attribute.

		@return: self._rawSectionContentIdentifier. ( String )
		'''

		return self._rawSectionContentIdentifier

	@rawSectionContentIdentifier.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def rawSectionContentIdentifier( self, value ):
		'''
		This Method Is The Setter Method For The _rawSectionContentIdentifier Attribute.
	
		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type( value ) in ( str, unicode ), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format( "rawSectionContentIdentifier", value )
		self._rawSectionContentIdentifier = value

	@rawSectionContentIdentifier.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def rawSectionContentIdentifier( self ):
		'''
		This Method Is The Deleter Method For The _rawSectionContentIdentifier Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "rawSectionContentIdentifier" ) )

	@property
	def sections( self ):
		'''
		This Method Is The Property For The _sections Attribute.

		@return: self._sections. ( Dictionary )
		'''

		return self._sections

	@sections.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def sections( self, value ):
		'''
		This Method Is The Setter Method For The _sections Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		'''

		if value :
			assert type( value ) is dict, "'{0}' Attribute : '{1}' Type Is Not 'dict' !".format( "sections", value )
		self._sections = value

	@sections.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def sections( self ):
		'''
		This Method Is The Deleter Method For The _sections Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "sections" ) )

	@property
	def comments( self ):
		'''
		This Method Is The Property For The _comments Attribute.

		@return: self._comments. ( Dictionary )
		'''

		return self._comments


	@comments.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def comments( self, value ):
		'''
		This Method Is The Setter Method For The _comments Attribute.

		@param value: Attribute Value. ( Dictionary )
		'''

		if value :
			assert type( value ) is dict, "'{0}' Attribute : '{1}' Type Is Not 'dict' !".format( "comments", value )
		self._comments = value

	@comments.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def comments( self ):
		'''
		This Method Is The Deleter Method For The _comments Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "comments" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.FileStructureError )
	def parse( self, rawSections = None ):
		'''
		This Method Process The File Content To Extract The Sections As A Dictionary.

		@return: Current File Sections. ( Dictionary Or None )
		'''

		LOGGER.debug( " > Reading Sections From : '{0}'.".format( self._file ) )
		if self._content :
			if re.search( "^\[.*\]", self._content[0] ) :
				self._sections = {}
				self._comments = {}
				rawSections = rawSections or []
				commentId = 0
				for line in self._content:
					if re.search( "^\[.*\]", line ):
						section = re.search( "(?<=^\[)(.*)(?=\])", line )
						section = section.group( 0 )
						attributes = {}
						rawContent = []
					else:
						if section in rawSections :
							rawContent.append( line )
							attributes[section + self._namespaceSplitter + self._rawSectionContentIdentifier] = rawContent
						else :
							if re.search( "^ *\n", line ) or re.search( "^ *\r\n", line ) :
								continue
							else :
								if line.startswith( self._commentLimiter ):
									self._comments[section + self._namespaceSplitter + "#_" + str( commentId )] = line.strip( "-;" )
									commentId += 1
								elif self._splitter in line:
									lineTokens = line.split( self._splitter )
									attributes[section + self._namespaceSplitter + lineTokens[0].strip()] = lineTokens[1].strip().strip( "\"" )
						self._sections[section] = attributes
			else:
				raise foundations.exceptions.FileStructureError( "'{0}' Structure Is Invalid : No Section Found At First Line !".format( self._file ) )

	@core.executionTrace
	def sectionsExists( self, section ):
		'''
		This Method Checks If A Section Exists.

		@param section: Section To Check Existence. ( String )
		@return: Section Existence. ( Boolean )
		'''

		if section in self._sections.keys() :
			LOGGER.debug( "> '{0}' Section Exists In '{1}'.".format( section, self ) )
			return True
		else :
			LOGGER.debug( "> '{0}' Section Doesn't Exists In '{1}'.".format( section, self ) )
			return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, KeyError )
	def attributeExists( self, attribute, section ):
		'''
		This Method Checks If An Attribute Exists.

		@param attribute: Attribute To Check Existence. ( String )
		@param section: Section To Search Attribute Into. ( String )
		@return: Attribute Existence. ( Boolean )
		'''

		if removeNamespace( attribute ) in self.getAttributes( section, False ) :
			LOGGER.debug( "> '{0}' Attribute Exists In '{1}' Section.".format( attribute, section ) )
			return True
		else :
			LOGGER.debug( "> '{0}' Attribute Doesn't Exists In '{1}' Section.".format( attribute, section ) )
			return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, KeyError )
	def getAttributes( self, section, useNamespace = True, raise_ = True ):
		'''
		This Method Returns The Section / Files Attributes.

		@param section: Section Containing The Searched Attribute. ( String )
		@param useNamespace: Use Namespace While Getting Attributes. ( Boolean )
		@param raise_: Raise If Section Doesn't Exists. ( Boolean )
		@return: Attributes. ( Dictionary )
		'''

		LOGGER.debug( "> Getting Section '{0}' Attributes.".format( section ) )

		if self.sectionsExists( section ) :
			return useNamespace and self._sections[section] or dict( [( removeNamespace( attribute ), self._sections[section][attribute] ) for attribute in self._sections[section].keys()] )
		else :
			if raise_ :
				raise KeyError( "'{0}' Section Doesn't Exists In '{1}' Sections !".format( section, self._file ) )
			else :
				LOGGER.warning( "!> {0} | '{1}' Section Doesn't Exists In '{2}' Sections !".format( self.__class__.__name__, section, self._file ) )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, KeyError )
	def getValue( self, attribute, section, encode = False ):
		'''
		This Method Returns The Requested Attribute Value Abstracting The Namespace.

		@param attribute: Attribute Name. ( String )
		@param section: Section Containing The Searched Attribute. ( String )
		@param encode: Encode Value To Unicode. ( Boolean )
		@return: Attribute Value. ( String )
		'''

		if self.attributeExists( attribute, section ):
			if attribute in self._sections[section].keys() :
				value = self._sections[section][attribute]
			elif setNamespace( section, attribute ) in self._sections[section].keys():
				value = self._sections[section][setNamespace( section, attribute )]
				LOGGER.debug( "> '{0}' Attribute Value : '{1}'.".format( attribute, value ) )

			value = encode and unicode( value, Constants.encodingFormat, Constants.encodingError ) or value
			return value

@core.executionTrace
def setNamespace( section, attribute, namespaceSplitter = "|" ):
	'''
	This Definition Returns The Compounded Attribute And Compounded Namespace.

	@param section: Section. ( String )
	@param attribute: Attribute. ( String )
	@param namespaceSplitter: Namespace Splitter Character. ( String )
	@return: Namespaced Attribute. ( String )
	'''

	return str( section + namespaceSplitter + attribute )

@core.executionTrace
def getNamespace( attribute, namespaceSplitter = "|" ):
	'''
	This Definition Returns The Attribute Namespace.

	@param attribute: Attribute. ( String )
	@param namespaceSplitter: Namespace Splitter Character. ( String )
	@return: Attribute Namespace. ( String )
	'''

	attributeTokens = attribute.split( namespaceSplitter )
	if len( attributeTokens ) == 1:
		return None
	else :
		return attributeTokens[0:-1]

@core.executionTrace
def removeNamespace( attribute, namespaceSplitter = "|", rootOnly = False ):
	'''
	This Definition Returns The Attribute Without Namespace.

	@param attribute: Attribute. ( String )
	@param namespaceSplitter: Namespace Splitter Character. ( String )
	@param rootOnly: Remove Only Root Namespace. ( Boolean )
	@return: Attribute Without Namespace. ( String )
	'''

	attributeTokens = attribute.split( namespaceSplitter )
	return rootOnly and namespaceSplitter.join( attributeTokens[1:] ) or attributeTokens[len( attributeTokens ) - 1]

@core.executionTrace
def getAttributeCompound( attribute, value, splitter = "|", bindingIdentifier = "@" ):
	'''
	This Definition Get An Attribute Compound.

	@param attribute: Attribute. ( String )
	@param value: Attribute Value. ( Object )
	@param splitter: Splitter. ( String )
	@param bindingIdentifier: Binding Identifier. ( String )
	@return: Attribute Compound. ( AttributeObject )
	'''

	if not value :
		return AttributeCompound( name = attribute, value = None, link = None, type = None, alias = None )

	if splitter in value :
		valueTokens = value.split( splitter )
		if len( valueTokens ) >= 3 and re.search( "{0}[a-zA-Z0-9_]*".format( bindingIdentifier ), valueTokens[0] ):
			return AttributeCompound( name = attribute, value = valueTokens[1].strip(), link = valueTokens[0].strip(), type = valueTokens[2].strip(), alias = len( valueTokens ) == 4 and valueTokens[3].strip() or None )
	else :
		if re.search( "{0}[a-zA-Z0-9_]*".format( bindingIdentifier ), value ) :
			return AttributeCompound( name = attribute, value = None, link = value, type = None, alias = None )

	return AttributeCompound( name = attribute, value = value, link = None, type = None, alias = None )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
