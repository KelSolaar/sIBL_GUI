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
***	SetsScanner.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Sets Scanner Component Module.
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

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.common
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
from foundations.walker import Walker
from globals.constants import Constants
from manager.component import Component

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class SetsScanner( Component ):
	'''
	This Class Is The SetsScanner Class.
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
		self.deactivatable = True

		self._container = None

		self._extension = ".ibl"

		self._coreDb = None
		self._coreCollectionsOutliner = None

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
	def extension( self ):
		'''
		This Method Is The Property For The _extension Attribute.

		@return: self._extension. ( String )
		'''

		return self._extension

	@extension.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def extension( self, value ):
		'''
		This Method Is The Setter Method For The _extension Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "extension" ) )

	@extension.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def extension( self ):
		'''
		This Method Is The Deleter Method For The _extension Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "extension" ) )

	@property
	def coreDb( self ):
		'''
		This Method Is The Property For The _coreDb Attribute.

		@return: self._coreDb. ( Object )
		'''

		return self._coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self, value ):
		'''
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDb" ) )

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self ):
		'''
		This Method Is The Deleter Method For The _coreDb Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDb" ) )

	@property
	def coreCollectionsOutliner( self ):
		'''
		This Method Is The Property For The _coreCollectionsOutliner Attribute.

		@return: self._coreCollectionsOutliner. ( Object )
		'''

		return self._coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreCollectionsOutliner( self, value ):
		'''
		This Method Is The Setter Method For The _coreCollectionsOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreCollectionsOutliner" ) )

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreCollectionsOutliner( self ):
		'''
		This Method Is The Deleter Method For The _coreCollectionsOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreCollectionsOutliner" ) )

	@property
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self, value ):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDatabaseBrowser" ) )

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDatabaseBrowser" ) )

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

		self._coreDb = self._container.componentsManager.components["core.db"].interface
		self._coreCollectionsOutliner = self._container.componentsManager.components["core.collectionsOutliner"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug( "> Deactivating '{0}' Component.".format( self.__class__.__name__ ) )

		self._container = None

		self._coreDb = None
		self._coreCollectionsOutliner = None
		self._coreDatabaseBrowser = None

		self._deactivate()

	@core.executionTrace
	def initialize( self ):
		'''
		This Method Initializes The Component.
		'''

		LOGGER.debug( "> Initializing '{0}' Component.".format( self.__class__.__name__ ) )

		pass

	@core.executionTrace
	def uninitialize( self ):
		'''
		This Method Uninitializes The Component.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component.".format( self.__class__.__name__ ) )

		pass

	@core.executionTrace
	def onStartup( self ):
		'''
		This Method Is Called On Framework Startup.
		'''

		LOGGER.debug( "> Calling '{0}' Component Framework Startup Method.".format( self.__class__.__name__ ) )

		self.scanSetsDirectories()

	@core.executionTrace
	def scanSetsDirectories( self ):
		'''
		This Method Scans Sets Directories.
		'''

		LOGGER.info( "{0} | Scanning Sets Directories For New Sets !".format( self.__class__.__name__ ) )

		paths = [path[0] for path in self._coreDb.dbSession.query( dbUtilities.types.DbSet.path ).all()]
		folders = set( [os.path.normpath( os.path.join( os.path.dirname( path ), ".." ) ) for path in paths] )
		needUiRefresh = False
		for folder in folders :
			walker = Walker( folder )
			walker.walk( self._extension )
			for set_, path in walker.files.items() :
				if not dbUtilities.common.filterSets( self._coreDb.dbSession, "^{0}$".format( path ), "path" ) :
					needUiRefresh = True
					LOGGER.info( "{0} | Adding '{1}' Set To Database !".format( self.__class__.__name__, set_ ) )
					if not dbUtilities.common.addSet( self._coreDb.dbSession, set_, path, self._coreCollectionsOutliner.getCollectionId( self._coreCollectionsOutliner._defaultCollection ) ) :
						LOGGER.error( "!>{0} | Exception Raised While Adding '{1}' Set To Database !".format( self.__class__.__name__, set_ ) )

		if needUiRefresh :
			self._coreCollectionsOutliner.Collections_Outliner_treeView_refreshSetsCounts()
			self._coreDatabaseBrowser.setCollectionsDisplaySets()
			self._coreDatabaseBrowser.Database_Browser_listView_refreshModel()

		LOGGER.info( "{0} | Scanning Done !".format( self.__class__.__name__ ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
