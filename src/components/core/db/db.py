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
***	db.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Database Backup Component Module.
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
import sqlalchemy
import sqlalchemy.orm

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.common
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import ui.widgets.messageBox as messageBox
from globals.constants import Constants
from manager.component import Component

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Db( Component ):
	'''
	This Class Is The Db Class.
	'''

	@core.executionTrace
	def __init__( self, name = None ):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		Component.__init__( self, name = name )

		# --- Setting Class Attributes. ---
		self.deactivatable = False

		self._container = None

		self._dbName = None
		self._dbSession = None
		self._dbEngine = None
		self._dbCatalog = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container( self ):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self, value ):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "container" ) )

	@container.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self ):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "container" ) )

	@property
	def dbName( self ):
		'''
		This Method Is The Property For The _dbName Attribute.

		@return: self._dbName. ( String )
		'''

		return self._dbName

	@dbName.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbName( self, value ):
		'''
		This Method Is The Setter Method For The _dbName Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dbName" ) )

	@dbName.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbName( self ):
		'''
		This Method Is The Deleter Method For The _dbName Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dbName" ) )

	@property
	def dbEngine( self ):
		'''
		This Method Is The Property For The _dbEngine Attribute.

		@return: self._dbEngine. ( Object )
		'''

		return self._dbEngine

	@dbEngine.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbEngine( self, value ):
		'''
		This Method Is The Setter Method For The _dbEngine Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dbEngine" ) )

	@dbEngine.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbEngine( self ):
		'''
		This Method Is The Deleter Method For The _dbEngine Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dbEngine" ) )

	@property
	def dbCatalog( self ):
		'''
		This Method Is The Property For The _dbCatalog Attribute.

		@return: self._dbCatalog. ( Object )
		'''

		return self._dbCatalog

	@dbCatalog.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbCatalog( self, value ):
		'''
		This Method Is The Setter Method For The _dbCatalog Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dbCatalog" ) )

	@dbCatalog.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbCatalog( self ):
		'''
		This Method Is The Deleter Method For The _dbCatalog Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dbCatalog" ) )

	@property
	def dbSession( self ):
		'''
		This Method Is The Property For The _dbSession Attribute.

		@return: self._dbSession. ( Object )
		'''

		return self._dbSession

	@dbSession.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbSession( self, value ):
		'''
		This Method Is The Setter Method For The _dbSession Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dbSession" ) )

	@dbSession.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbSession( self ):
		'''
		This Method Is The Deleter Method For The _dbSession Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dbSession" ) )

	@property
	def dbSessionMaker( self ):
		'''
		This Method Is The Property For The _dbSessionMaker Attribute.

		@return: self._dbSessionMaker. ( Object )
		'''

		return self._dbSessionMaker

	@dbSessionMaker.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbSessionMaker( self, value ):
		'''
		This Method Is The Setter Method For The _dbSessionMaker Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dbSessionMaker" ) )

	@dbSessionMaker.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dbSessionMaker( self ):
		'''
		This Method Is The Deleter Method For The _dbSessionMaker Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dbSessionMaker" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate( self, container ):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug( "> Activating '{0}' Component.".format( self.__class__.__name__ ) )

		self._container = container

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		messageBox.messageBox( "Warning", "Warning", "{0} Component Cannot Be Deactivated !".format( self.__class__.__name__ ) )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, OSError )
	def initialize( self ):
		'''
		This Method Initializes The Component.
		'''

		LOGGER.debug( "> Initializing '{0}' Component.".format( self.__class__.__name__ ) )

		LOGGER.debug( "> Initializing '{0}' SQLite Database.".format( Constants.databaseFile ) )
		if self._container.parameters.databaseDirectory :
			if os.path.exists( self._container.parameters.databaseDirectory ) :
				self._dbName = os.path.join( self._container.parameters.databaseDirectory, Constants.databaseFile )
			else :
				raise OSError, "'{0}' Database Storing Directory Does'nt Exists !".format( self._container.parameters.databaseDirectory )
		else :
			self._dbName = os.path.join( self._container.userApplicationDatasDirectory , Constants.databaseDirectory, Constants.databaseFile )

		LOGGER.debug( "> Creating Database Engine." )
		self._dbEngine = sqlalchemy.create_engine( "sqlite:///{0}".format( self._dbName ) )

		LOGGER.debug( "> Creating Database Metadatas." )
		self._dbCatalog = dbUtilities.types.DbBase.metadata
		self._dbCatalog.create_all( self._dbEngine )

		LOGGER.debug( "> Initializing Database Session." )
		self._dbSessionMaker = sqlalchemy.orm.sessionmaker( bind = self._dbEngine )

		self._dbSession = self._dbSessionMaker()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uninitialize( self ):
		'''
		This Method Uninitializes The Component.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Component Cannot Be Uninitialized !".format( self.name ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
