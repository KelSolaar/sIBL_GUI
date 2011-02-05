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
***	databaseBrowser.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Database Browser Component Module.
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
import re
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.common
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import ui.common
import ui.widgets.messageBox as messageBox
from foundations.walker import Walker
from globals.constants import Constants
from globals.uiConstants import UiConstants
from libraries.freeImage.freeImage import Image
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class DatabaseBrowser_Worker( QThread ):
	'''
	This Class Is The DatabaseBrowser_Worker Class.
	'''

	# Custom Signals Definitions.
	databaseChanged = pyqtSignal()

	@core.executionTrace
	def __init__( self, container ):
		'''
		This Method Initializes The Class.
		
		@param container: Object Container. ( Object )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		QThread.__init__( self, container )

		# --- Setting Class Attributes. ---
		self._container = container

		self._dbSession = self._container.coreDb.dbSessionMaker()

		self._timer = None
		self._timerCycleMultiplier = 5

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
	def timer( self ):
		'''
		This Method Is The Property For The _timer Attribute.

		@return: self._timer. ( QTimer )
		'''

		return self._timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def timer( self, value ):
		'''
		This Method Is The Setter Method For The _timer Attribute.

		@param value: Attribute Value. ( QTimer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "timer" ) )

	@timer.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def timer( self ):
		'''
		This Method Is The Deleter Method For The _timer Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "timer" ) )

	@property
	def timerCycleMultiplier( self ):
		'''
		This Method Is The Property For The _timerCycleMultiplier Attribute.

		@return: self._timerCycleMultiplier. ( Float )
		'''

		return self._timerCycleMultiplier

	@timerCycleMultiplier.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def timerCycleMultiplier( self, value ):
		'''
		This Method Is The Setter Method For The _timerCycleMultiplier Attribute.

		@param value: Attribute Value. ( Float )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "timerCycleMultiplier" ) )

	@timerCycleMultiplier.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def timerCycleMultiplier( self ):
		'''
		This Method Is The Deleter Method For The _timerCycleMultiplier Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "timerCycleMultiplier" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def run( self ):
		'''
		This Method Starts The QThread.
		'''

		self._timer = QTimer()
		self._timer.moveToThread( self )
		self._timer.start( Constants.defaultTimerCycle * self._timerCycleMultiplier )

		self._timer.timeout.connect( self.updateSets, Qt.DirectConnection )

		self.exec_()

	@core.executionTrace
	def updateSets( self ):
		'''
		This Method Updates Database Sets If They Have Been Modified On Disk.
		'''

		needModelRefresh = False
		for iblSet in dbUtilities.common.getIblSets( self._dbSession ) :
			if iblSet.path :
				if os.path.exists( iblSet.path ) :
					storedStats = iblSet.osStats.split( "," )
					osStats = os.stat( iblSet.path )
					if str( osStats[8] ) != str( storedStats[8] ):
						LOGGER.info( "{0} | '{1}' Ibl Set File Has Been Modified And Will Be Updated !".format( self.__class__.__name__, iblSet.name ) )
						if dbUtilities.common.updateIblSetContent( self._dbSession, iblSet ) :
							LOGGER.info( "{0} | '{1}' Ibl Set Has Been Updated !".format( self.__class__.__name__, iblSet.name ) )
							needModelRefresh = True

		needModelRefresh and self.emit( SIGNAL( "databaseChanged()" ) )

class DatabaseBrowser_QListView( QListView ):
	'''
	This Class Is The DatabaseBrowser_QListView Class.
	'''

	@core.executionTrace
	def __init__( self, container ):
		'''
		This Method Initializes The Class.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		QListView.__init__( self, container )

		self.setAcceptDrops( True )


		# --- Setting Class Attributes. ---
		self._container = container

		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface

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
	def dragEnterEvent( self, event ):
		'''
		This Method Defines The Drag Enter Event Behavior.
		
		@param event: QEvent. ( QEvent )
		'''

		if event.mimeData().hasFormat( "application/x-qabstractitemmodeldatalist" ):
			LOGGER.debug( "> '{0}' Drag Event Type Accepted !".format( "application/x-qabstractitemmodeldatalist" ) )
			event.accept()
		elif event.mimeData().hasFormat( "text/uri-list" ):
			LOGGER.debug( "> '{0}' Drag Event Type Accepted !".format( "text/uri-list" ) )
			event.accept()
		else:
			event.ignore()

	@core.executionTrace
	def dragMoveEvent( self, event ):
		'''
		This Method Defines The Drag Move Event Behavior.
		
		@param event: QEvent. ( QEvent )
		'''

		pass

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( ui.common.uiBasicExceptionHandler, False, OSError, foundations.exceptions.UserError )
	def dropEvent( self, event ):
		'''
		This Method Defines The Drop Event Behavior.
		
		@param event: QEvent. ( QEvent )		
		'''

		if not self._container.parameters.databaseReadOnly :
			if event.mimeData().hasUrls() :
				LOGGER.debug( "> Drag Event Urls List : '{0}' !".format( event.mimeData().urls() ) )
				for url in event.mimeData().urls() :
					path = ( platform.system() == "Windows" or platform.system() == "Microsoft" ) and re.search( "^\/[A-Z]:", str( url.path() ) ) and str( url.path() )[1:] or str( url.path() )
					if re.search( "\.{0}$".format( self._coreDatabaseBrowser.extension ), str( url.path() ) ) :
						name = os.path.splitext( os.path.basename( path ) )[0]
						if messageBox.messageBox( "Question", "Question", "'{0}' Ibl Set File Has Been Dropped, Would You Like To Add It To The Database ?".format( name ), buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
							 self._coreDatabaseBrowser.addIblSet( name, path ) and self._coreDatabaseBrowser.Database_Browser_listView_extendedRefreshModel()
					else :
						if os.path.isdir( path ):
							if messageBox.messageBox( "Question", "Question", "'{0}' Directory Has Been Dropped, Would You Like To Add Its Content To The Database ?".format( path ), buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
								 self._coreDatabaseBrowser.addDirectory( path )
								 self._coreDatabaseBrowser.Database_Browser_listView_extendedRefreshModel()
						else :
							raise OSError, "{0} | Exception Raised While Parsing '{1}' Path : Syntax Is Invalid !".format( self.__class__.__name__, path )
		else :
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only !".format( self.__class__.__name__ )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError )
	def QListView_OnDoubleClicked( self, index ):
		'''
		This Method Defines The Behavior When A QStandardItem Is Double Clicked.
		
		@param index: Clicked Model Item Index. ( QModelIndex )
		'''

		if not self._container.parameters.databaseReadOnly :
			pass
		else :
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only !".format( self.__class__.__name__ )

class DatabaseBrowser( UiComponent ):
	'''
	This Class Is The DatabaseBrowser Class.
	'''

	# Custom Signals Definitions.
	modelChanged = pyqtSignal()

	@core.executionTrace
	def __init__( self, name = None, uiFile = None ):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		UiComponent.__init__( self, name = name, uiFile = uiFile )

		# --- Setting Class Attributes. ---
		self.deactivatable = False

		self._uiPath = "ui/Database_Browser.ui"
		self._uiResources = "resources"
		self._uiFormatErrorIcon = "Thumbnails_Format_Not_Supported_Yet.png"
		self._uiMissingIcon = "Thumbnailst_Not_Found.png"
		self._uiLargestSizeIcon = "Largest_Size.png"
		self._uiSmallestSizeIcon = "Smallest_Size.png"
		self._dockArea = 8
		if platform.system() == "Linux" :
			self._listViewSpacing = 14
		else :
			self._listViewSpacing = 16
		self._listViewMargin = 24
		self._listViewIconSize = 128

		self._container = None
		self._settings = None
		self._settingsSection = None

		self._extension = "ibl"

		self._coreDb = None
		self._coreCollectionsOutliner = None

		self._model = None
		self._modelSelection = None
		# Crash Preventing Code.
		self._modelSelectionState = True

		self._databaseBrowserWorkerThread = None

		self._displaySets = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath( self ):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self, value ):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiPath" ) )

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self ):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiPath" ) )

	@property
	def uiResources( self ):
		'''
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		'''

		return self._uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self, value ):
		'''
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiResources" ) )

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self ):
		'''
		This Method Is The Deleter Method For The _uiResources Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiResources" ) )

	@property
	def uiFormatErrorIcon( self ):
		'''
		This Method Is The Property For The _uiFormatErrorIcon Attribute.

		@return: self._uiFormatErrorIcon. ( String )
		'''

		return self._uiFormatErrorIcon

	@uiFormatErrorIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiFormatErrorIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiFormatErrorIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiFormatErrorIcon" ) )

	@uiFormatErrorIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiFormatErrorIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiFormatErrorIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiFormatErrorIcon" ) )

	@property
	def uiMissingIcon( self ):
		'''
		This Method Is The Property For The _uiMissingIcon Attribute.

		@return: self._uiMissingIcon. ( String )
		'''

		return self._uiMissingIcon

	@uiMissingIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiMissingIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiMissingIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiMissingIcon" ) )

	@uiMissingIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiMissingIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiMissingIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiMissingIcon" ) )

	@property
	def uiLargestSizeIcon( self ):
		'''
		This Method Is The Property For The _uiLargestSizeIcon Attribute.

		@return: self._uiLargestSizeIcon. ( String )
		'''

		return self._uiLargestSizeIcon

	@uiLargestSizeIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLargestSizeIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiLargestSizeIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiLargestSizeIcon" ) )

	@uiLargestSizeIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLargestSizeIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiLargestSizeIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiLargestSizeIcon" ) )

	@property
	def uiSmallestSizeIcon( self ):
		'''
		This Method Is The Property For The _uiSmallestSizeIcon Attribute.

		@return: self._uiSmallestSizeIcon. ( String )
		'''

		return self._uiSmallestSizeIcon

	@uiSmallestSizeIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiSmallestSizeIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiSmallestSizeIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiSmallestSizeIcon" ) )

	@uiSmallestSizeIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiSmallestSizeIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiSmallestSizeIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiSmallestSizeIcon" ) )

	@property
	def dockArea( self ):
		'''
		This Method Is The Property For The _dockArea Attribute.

		@return: self._dockArea. ( Integer )
		'''

		return self._dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self, value ):
		'''
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dockArea" ) )

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self ):
		'''
		This Method Is The Deleter Method For The _dockArea Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dockArea" ) )

	@property
	def listViewSpacing( self ):
		'''
		This Method Is The Property For The _listViewSpacing Attribute.

		@return: self._listViewSpacing. ( Integer )
		'''

		return self._listViewSpacing

	@listViewSpacing.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def listViewSpacing( self, value ):
		'''
		This Method Is The Setter Method For The _listViewSpacing Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		if value :
			assert type( value ) is int, "'{0}' Attribute : '{1}' Type Is Not 'int' !".format( "listViewSpacing", value )
			assert value > 0, "'{0}' Attribute : '{1}' Need To Be Exactly Positive !".format( "listViewSpacing", value )
		self._listViewSpacing = value

	@listViewSpacing.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def listViewSpacing( self ):
		'''
		This Method Is The Deleter Method For The _listViewSpacing Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "listViewSpacing" ) )

	@property
	def listViewMargin( self ):
		'''
		This Method Is The Property For The _listViewMargin Attribute.

		@return: self._listViewMargin. ( Integer )
		'''

		return self._listViewMargin

	@listViewMargin.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def listViewMargin( self, value ):
		'''
		This Method Is The Setter Method For The _listViewMargin Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		if value :
			assert type( value ) is int, "'{0}' Attribute : '{1}' Type Is Not 'int' !".format( "listViewMargin", value )
			assert value > 0, "'{0}' Attribute : '{1}' Need To Be Exactly Positive !".format( "listViewMargin", value )
		self._listViewMargin = value

	@listViewMargin.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def listViewMargin( self ):
		'''
		This Method Is The Deleter Method For The _listViewMargin Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "listViewMargin" ) )

	@property
	def listViewIconSize( self ):
		'''
		This Method Is The Property For The _listViewIconSize Attribute.

		@return: self._listViewIconSize. ( Integer )
		'''

		return self._listViewIconSize

	@listViewIconSize.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def listViewIconSize( self, value ):
		'''
		This Method Is The Setter Method For The _listViewIconSize Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		if value :
			assert type( value ) is int, "'{0}' Attribute : '{1}' Type Is Not 'int' !".format( "listViewIconSize", value )
			assert value > 0, "'{0}' Attribute : '{1}' Need To Be Exactly Positive !".format( "listViewIconSize", value )
		self._listViewIconSize = value

	@listViewIconSize.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def listViewIconSize( self ):
		'''
		This Method Is The Deleter Method For The _listViewIconSize Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "listViewIconSize" ) )

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
	def settings( self ):
		'''
		This Method Is The Property For The _settings Attribute.

		@return: self._settings. ( QSettings )
		'''

		return self._settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settings( self, value ):
		'''
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "settings" ) )

	@settings.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settings( self ):
		'''
		This Method Is The Deleter Method For The _settings Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "settings" ) )

	@property
	def settingsSection( self ):
		'''
		This Method Is The Property For The _settingsSection Attribute.

		@return: self._settingsSection. ( String )
		'''

		return self._settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settingsSection( self, value ):
		'''
		This Method Is The Setter Method For The _settingsSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "settingsSection" ) )

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settingsSection( self ):
		'''
		This Method Is The Deleter Method For The _settingsSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "settingsSection" ) )

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
	def model( self ):
		'''
		This Method Is The Property For The _model Attribute.

		@return: self._model. ( QStandardItemModel )
		'''

		return self._model

	@model.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def model( self, value ):
		'''
		This Method Is The Setter Method For The _model Attribute.

		@param value: Attribute Value. ( QStandardItemModel )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "model" ) )

	@model.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def model( self ):
		'''
		This Method Is The Deleter Method For The _model Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "model" ) )

	@property
	def modelSelection( self ):
		'''
		This Method Is The Property For The _modelSelection Attribute.

		@return: self._modelSelection. ( Dictionary )
		'''

		return self._modelSelection

	@modelSelection.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def modelSelection( self, value ):
		'''
		This Method Is The Setter Method For The _modelSelection Attribute.

		@param value: Attribute Value. ( Dictionary )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "modelSelection" ) )

	@modelSelection.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def modelSelection( self ):
		'''
		This Method Is The Deleter Method For The _modelSelection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "modelSelection" ) )

	# Crash Preventing Code.
	@property
	def modelSelectionState( self ):
		'''
		This Method Is The Property For The _modelSelectionState Attribute.

		@return: self._modelSelectionState. ( Boolean )
		'''

		return self._modelSelectionState

	@modelSelectionState.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def modelSelectionState( self, value ):
		'''
		This Method Is The Setter Method For The _modelSelectionState Attribute.

		@param value: Attribute Value. ( Boolean )
		'''

		if value :
			assert type( value ) is bool, "'{0}' Attribute : '{1}' Type Is Not 'bool' !".format( "modelSelectionState", value )
		self._modelSelectionState = value

	@modelSelectionState.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def modelSelectionState( self ):
		'''
		This Method Is The Deleter Method For The _modelSelectionState Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "modelSelectionState" ) )

	@property
	def databaseBrowserWorkerThread( self ):
		'''
		This Method Is The Property For The _databaseBrowserWorkerThread Attribute.

		@return: self._databaseBrowserWorkerThread. ( QThread )
		'''

		return self._databaseBrowserWorkerThread

	@databaseBrowserWorkerThread.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def databaseBrowserWorkerThread( self, value ):
		'''
		This Method Is The Setter Method For The _databaseBrowserWorkerThread Attribute.

		@param value: Attribute Value. ( QThread )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "databaseBrowserWorkerThread" ) )

	@databaseBrowserWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def databaseBrowserWorkerThread( self ):
		'''
		This Method Is The Deleter Method For The _databaseBrowserWorkerThread Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "databaseBrowserWorkerThread" ) )

	@property
	def displaySets( self ):
		'''
		This Method Is The Property For The _displaySets Attribute.

		@return: self._displaySets. ( List )
		'''

		return self._displaySets

	@displaySets.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def displaySets( self, value ):
		'''
		This Method Is The Setter Method For The _displaySets Attribute.

		@param value: Attribute Value. ( List )
		'''

		if value :
			assert type( value ) is list, "'{0}' Attribute : '{1}' Type Is Not 'list' !".format( "content", value )
		self._displaySets = value

	@displaySets.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def displaySets( self ):
		'''
		This Method Is The Deleter Method For The _displaySets Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "displaySets" ) )

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

		self.uiFile = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiPath )
		self._uiResources = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiResources )
		self._container = container
		self._settings = self._container.settings
		self._settingsSection = self.name

		self._coreDb = self._container.componentsManager.components["core.db"].interface
		self._coreCollectionsOutliner = self._container.componentsManager.components["core.collectionsOutliner"].interface

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Component Cannot Be Deactivated !".format( self._name ) )

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self.ui.Database_Browser_listView = DatabaseBrowser_QListView( self._container )
		self.ui.Database_Browser_Widget_gridLayout.addWidget( self.ui.Database_Browser_listView, 0, 0 )

		self._displaySets = dbUtilities.common.getIblSets( self._coreDb.dbSession )

		listViewIconSize = self._settings.getKey( self._settingsSection, "listViewIconSize" )
		self._listViewIconSize = listViewIconSize.toInt()[1] and listViewIconSize.toInt()[0] or self._listViewIconSize

		self._container.parameters.databaseReadOnly and	LOGGER.info( "{0} | Database_Browser_listView Model Edition Deactivated By '{1}' Command Line Parameter Value !".format( self.__class__.__name__, "databaseReadOnly" ) )
		self._model = QStandardItemModel()
		self.Database_Browser_listView_setModel()

		self.ui.Database_Browser_listView.setContextMenuPolicy( Qt.ActionsContextMenu )
		self.Database_Browser_listView_setActions()

		self.Database_Browser_listView_setView()

		if not self._container.parameters.databaseReadOnly :
			self._databaseBrowserWorkerThread = DatabaseBrowser_Worker( self )
			self._databaseBrowserWorkerThread.start()
			self._container.workerThreads.append( self._databaseBrowserWorkerThread )
		else :
			LOGGER.info( "{0} | Ibl Sets Continuous Scanner Deactivated By '{1}' Command Line Parameter Value !".format( self.__class__.__name__, "databaseReadOnly" ) )

		self.ui.Thumbnails_Size_horizontalSlider.setValue( self._listViewIconSize )
		self.ui.Largest_Size_label.setPixmap( QPixmap( os.path.join( self._uiResources, self._uiLargestSizeIcon ) ) )
		self.ui.Smallest_Size_label.setPixmap( QPixmap( os.path.join( self._uiResources, self._uiSmallestSizeIcon ) ) )

		# Signals / Slots.
		self.ui.Thumbnails_Size_horizontalSlider.valueChanged.connect( self.Thumbnails_Size_horizontalSlider_OnChanged )
		self.ui.Database_Browser_listView.doubleClicked.connect( self.ui.Database_Browser_listView.QListView_OnDoubleClicked )
		self.modelChanged.connect( self.Database_Browser_listView_refreshView )
		if not self._container.parameters.databaseReadOnly :
			self._databaseBrowserWorkerThread.databaseChanged.connect( self.databaseChanged )
			self._model.dataChanged.connect( self.Database_Browser_listView_OnModelDataChanged )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Component Ui Cannot Be Uninitialized !".format( self.name ) )

	@core.executionTrace
	def addWidget( self ):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug( "> Adding '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._container.centralwidget_gridLayout.addWidget( self.ui )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def removeWidget( self ):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Component Widget Cannot Be Removed !".format( self.name ) )

	@core.executionTrace
	def onStartup( self ):
		'''
		This Method Is Called On Framework Startup.
		'''

		LOGGER.debug( "> Calling '{0}' Component Framework Startup Method.".format( self.__class__.__name__ ) )

		if not self._container.parameters.databaseReadOnly :
			# Wizard If Sets Table Is Empty.
			if not dbUtilities.common.getIblSets( self._coreDb.dbSession ).count() :
				if messageBox.messageBox( "Question", "Question", "The Database Is Empty, Would You Like To Add Some Sets ?", buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
					directory = self._container.storeLastBrowsedPath( ( QFileDialog.getExistingDirectory( self, "Add Content :", self._container.lastBrowsedPath ) ) )
					if directory :
						self.addDirectory( directory )
						self.Database_Browser_listView_extendedRefreshModel()

			# Ibl Sets Table Integrity Checking.
			erroneousIblSets = dbUtilities.common.checkIblSetsTableIntegrity( self._coreDb.dbSession )
			if erroneousIblSets :
				for iblSet in erroneousIblSets :
					if erroneousIblSets[iblSet] == "INEXISTING_IBL_SET_FILE_EXCEPTION" :
						if messageBox.messageBox( "Question", "Error", "{0} | '{1}' Ibl Set File Is Missing, Would You Like To Update It's Location ?".format( self.__class__.__name__, iblSet.name ), QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No ) == 16384 :
							self.updateIblSetLocation( iblSet )
					else :
						messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' {2}".format( self.__class__.__name__, iblSet.name, dbUtilities.common.DB_EXCEPTIONS[erroneousIblSets[iblSet]] ) )
				self.Database_Browser_listView_localRefreshModel()
		else :
			LOGGER.info( "{0} | Database Ibl Sets Wizard And Ibl Sets Integrity Checking Method Deactivated By '{1}' Command Line Parameter Value !".format( self.__class__.__name__, "databaseReadOnly" ) )

	@core.executionTrace
	def Database_Browser_listView_setModel( self ):
		'''
		This Method Sets The Database_Browser_listView Model.
		'''

		LOGGER.debug( "> Setting Up '{0}' Model !".format( "Templates_Outliner_treeView" ) )

		self.Database_Browser_listView_storeModelSelection()

		self._model.clear()

		for iblSet in [iblSet[0] for iblSet in sorted( [( displaySet, displaySet.title ) for displaySet in self._displaySets], key = lambda x:( x[1] ) )] :
			LOGGER.debug( "> Preparing '{0}' Ibl Set For '{1}' Model.".format( iblSet.name, "Database_Browser_listView" ) )

			try :
				iblSetStandardItem = QStandardItem()
				iblSetStandardItem.setData( iblSet.title, Qt.DisplayRole )

				shotDateString = "<b>Shot Date : </b>{0}".format( self.getFormatedShotDate( iblSet.date, iblSet.time ) or Constants.nullObject )
				toolTip = QString( """
								<p><b>{0}</b></p>
								<p><b>Author : </b>{1}<br>
								<b>Location : </b>{2}<br>
								{3}<br>
								<b>Comment : </b>{4}</p>
								""".format( iblSet.title, iblSet.author or Constants.nullObject, iblSet.location or Constants.nullObject, shotDateString, iblSet.comment or Constants.nullObject ) )
				iblSetStandardItem.setToolTip( toolTip )

				iblIcon = QIcon()
				if os.path.exists( iblSet.icon ) :
					for extension in UiConstants.nativeImageFormats.values() :
						if re.search( extension, iblSet.icon ) :
							iblIcon = QIcon( iblSet.icon )
							break
					else :
						for extension in UiConstants.thirdPartyImageFormats.values() :
							if re.search( extension, iblSet.icon ) :
								image = Image( str( iblSet.icon ) )
								iblIcon = QIcon( QPixmap( image.convertToQImage() ) )
								break

				if iblIcon.isNull() :
					iblIcon = QIcon( os.path.join( self._uiResources, self.uiMissingIcon ) )
				iblSetStandardItem.setIcon( iblIcon )

				self._container.parameters.databaseReadOnly and iblSetStandardItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsDragEnabled )

				iblSetStandardItem._datas = iblSet

				LOGGER.debug( "> Adding '{0}' To '{1}' Model.".format( iblSet.name, "Database_Browser_listView" ) )
				self._model.appendRow( iblSetStandardItem )

			except Exception as error :
				LOGGER.error( "!>{0} | Exception Raised While Adding '{1}' Ibl Set To '{2}' Model !".format( self.__class__.__name__, iblSet.name, "Database_Browser_listView" ) )
				foundations.exceptions.defaultExceptionsHandler( error, "{0} | {1}.{2}()".format( core.getModule( self ).__name__, self.__class__.__name__, "Database_Browser_listView_setModel" ) )

		self.Database_Browser_listView_restoreModelSelection()

		self.emit( SIGNAL( "modelChanged()" ) )

	@core.executionTrace
	def Database_Browser_listView_refreshModel( self ):
		'''
		This Method Refreshes The Database_Browser_listView Model.
		'''

		LOGGER.debug( "> Refreshing '{0}' Model !".format( "Database_Browser_listView" ) )

		self.Database_Browser_listView_setModel()

	@core.executionTrace
	def Database_Browser_listView_localRefreshModel( self ):
		'''
		This Method Implements The Local Refresh Behavior.
		'''

		self.setCollectionsDisplaySets()
		self.Database_Browser_listView_refreshModel()

	@core.executionTrace
	def Database_Browser_listView_extendedRefreshModel( self ):
		'''
		This Method Implements The Extended Refresh Behavior.
		'''

		self._coreCollectionsOutliner.Collections_Outliner_treeView_refreshSetsCounts()
		self.Database_Browser_listView_localRefreshModel()

	@core.executionTrace
	def Database_Browser_listView_OnModelDataChanged( self, startIndex, endIndex ):
		'''
		This Method Defines The Behavior When The Database_Browser_listView Model Data Changes.
		
		@param startIndex: Edited Item Starting QModelIndex. ( QModelIndex )
		@param endIndex: Edited Item Ending QModelIndex. ( QModelIndex )
		'''

		standardItem = self._model.itemFromIndex( startIndex )
		currentTitle = standardItem.text()

		LOGGER.debug( "> Updating Ibl Set '{0}' Title To '{1}'.".format( standardItem._datas.title, currentTitle ) )
		iblSet = dbUtilities.common.filterIblSets( self._coreDb.dbSession, "^{0}$".format( standardItem._datas.id ), "id" )[0]
		iblSet.title = str( currentTitle )
		dbUtilities.common.commit( self._coreDb.dbSession )

		self.Database_Browser_listView_refreshModel()

	@core.executionTrace
	def Database_Browser_listView_setView( self ):
		'''
		This Method Sets The Database_Browser_listView Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Widget !".format( "Database_Browser_listView" ) )

		# self.ui.Database_Browser_listView.setAutoScroll( False )
		self.ui.Database_Browser_listView.setViewMode( QListView.IconMode )
		self.ui.Database_Browser_listView.setResizeMode( QListView.Adjust )
		self.ui.Database_Browser_listView.setSelectionMode( QAbstractItemView.ExtendedSelection )
		# self.ui.Database_Browser_listView.setAcceptDrops( False )

		self.Database_Browser_listView_setItemSize()

		self.ui.Database_Browser_listView.setModel( self._model )

	@core.executionTrace
	def Database_Browser_listView_refreshView( self ):
		'''
		This Method Refreshes The Database_Browser_listView View.
		'''

		self.Database_Browser_listView_setDefaultViewState()

	@core.executionTrace
	def Database_Browser_listView_setDefaultViewState( self ):
		'''
		This Method Sets Database_Browser_listView Default View State.
		'''

		LOGGER.debug( "> Setting '{0}' Default View State !".format( "Database_Browser_listView" ) )

		self.Database_Browser_listView_setItemSize()

	@core.executionTrace
	def Database_Browser_listView_storeModelSelection( self ):
		'''
		This Method Stores Database_Browser_listView Model Selection.
		'''

		# Crash Preventing Code.
		if self._modelSelectionState :

			LOGGER.debug( "> Storing '{0}' Model Selection !".format( "Database_Browser_listView" ) )

			self._modelSelection = []
			for item in self.getSelectedItems() :
				self._modelSelection.append( item._datas.id )

	@core.executionTrace
	def Database_Browser_listView_restoreModelSelection( self ):
		'''
		This Method Restores Database_Browser_listView Model Selection.
		'''

		# Crash Preventing Code.
		if self._modelSelectionState :

			LOGGER.debug( "> Restoring '{0}' Model Selection !".format( "Database_Browser_listView" ) )

			indexes = []
			for i in range( self._model.rowCount() ) :
				iblSetStandardItem = self._model.item( i )
				iblSetStandardItem._datas.id in self._modelSelection and indexes.append( self._model.indexFromItem( iblSetStandardItem ) )

			selectionModel = self.ui.Database_Browser_listView.selectionModel()
			if selectionModel :
				selectionModel.reset()
				for index in indexes :
					selectionModel.setCurrentIndex( index, QItemSelectionModel.Select )

	@core.executionTrace
	def Database_Browser_listView_setItemSize( self ):
		'''
		This Method Scales The Database_Browser_listView Item Size.
		
		@param value: Thumbnails Size. ( Integer )
		'''

		LOGGER.debug( "> Setting '{0}' View Item Size To : {1}.".format( "Database_Browser_listView", self._listViewIconSize ) )

		self.ui.Database_Browser_listView.setIconSize( QSize( self._listViewIconSize, self._listViewIconSize ) )
		self.ui.Database_Browser_listView.setGridSize( QSize( self._listViewIconSize + self._listViewSpacing, self._listViewIconSize + self._listViewMargin ) )

	@core.executionTrace
	def Database_Browser_listView_setActions( self ):
		'''
		This Method Sets The Database Browser Actions.
		'''

		if not self._container.parameters.databaseReadOnly :
			addContentAction = QAction( "Add Content ...", self.ui.Database_Browser_listView )
			addContentAction.triggered.connect( self.Database_Browser_listView_addContentAction )
			self.ui.Database_Browser_listView.addAction( addContentAction )

			addIblSetAction = QAction( "Add Ibl Set ...", self.ui.Database_Browser_listView )
			addIblSetAction.triggered.connect( self.Database_Browser_listView_addIblSetAction )
			self.ui.Database_Browser_listView.addAction( addIblSetAction )

			removeIblSetsAction = QAction( "Remove Ibl Set(s) ...", self.ui.Database_Browser_listView )
			removeIblSetsAction.triggered.connect( self.Database_Browser_listView_removeIblSetsAction )
			self.ui.Database_Browser_listView.addAction( removeIblSetsAction )

			updateIblSetsLocationsAction = QAction( "Update Ibl Set(s) Location(s) ...", self.ui.Database_Browser_listView )
			updateIblSetsLocationsAction.triggered.connect( self.Database_Browser_listView_updateIblSetsLocationsAction )
			self.ui.Database_Browser_listView.addAction( updateIblSetsLocationsAction )

			separatorAction = QAction( self.ui.Database_Browser_listView )
			separatorAction.setSeparator( True )
			self.ui.Database_Browser_listView.addAction( separatorAction )
		else :
			LOGGER.info( "{0} | Ibl Sets Database Alteration Capabilities Deactivated By '{1}' Command Line Parameter Value !".format( self.__class__.__name__, "databaseReadOnly" ) )

	@core.executionTrace
	def Database_Browser_listView_addContentAction( self, checked ):
		'''
		This Method Is Triggered By addContentAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		directory = self._container.storeLastBrowsedPath( ( QFileDialog.getExistingDirectory( self, "Add Content :", self._container.lastBrowsedPath ) ) )
		if directory :
			LOGGER.debug( "> Chosen Directory Path : '{0}'.".format( directory ) )
			self.addDirectory( directory )
			self.Database_Browser_listView_extendedRefreshModel()

	@core.executionTrace
	def Database_Browser_listView_addIblSetAction( self, checked ):
		'''
		This Method Is Triggered By addIblSetAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		iblSetPath = self._container.storeLastBrowsedPath( ( QFileDialog.getOpenFileName( self, "Add Ibl Set :", self._container.lastBrowsedPath, "Ibls Files (*{0})".format( self._extension ) ) ) )
		if iblSetPath :
			LOGGER.debug( "> Chosen Ibl Set Path : '{0}'.".format( iblSetPath ) )
			self.addIblSet( os.path.basename( iblSetPath ).replace( ".{0}".format( self._extension ), "" ), iblSetPath ) and self.Database_Browser_listView_extendedRefreshModel()

	@core.executionTrace
	def Database_Browser_listView_removeIblSetsAction( self, checked ):
		'''
		This Method Is Triggered By removeIblSetsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.removeIblSets()
		self.Database_Browser_listView_extendedRefreshModel()

	@core.executionTrace
	def Database_Browser_listView_updateIblSetsLocationsAction( self, checked ):
		'''
		This Method Is Triggered By updateIblSetsLocationsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		needModelRefresh = False
		selectedIblSets = self.getSelectedItems()
		if selectedIblSets :
			for iblSet in selectedIblSets :
				self.updateIblSetLocation( iblSet._datas )
				needModelRefresh = True

		if needModelRefresh :
			self.Database_Browser_listView_localRefreshModel()

	@core.executionTrace
	def Thumbnails_Size_horizontalSlider_OnChanged( self, value ):
		'''
		This Method Scales The Database_Browser_listView Icons.
		
		@param value: Thumbnails Size. ( Integer )
		'''

		self._listViewIconSize = value

		self.Database_Browser_listView_setItemSize()

		# Storing Settings Key.
		LOGGER.debug( "> Setting '{0}' With Value '{1}'.".format( "listViewIconSize", value ) )
		self._settings.setKey( self._settingsSection, "listViewIconSize", value )

	@core.executionTrace
	def databaseChanged( self ):
		'''
		This Method Is Triggered By The DatabaseBrowser_Worker When The Database Has Changed.
		'''

		# Ensure That DB Objects Modified By The Worker Thread Will Refresh Properly.
		self._coreDb.dbSession.expire_all()
		self.Database_Browser_listView_extendedRefreshModel()

	@core.executionTrace
	def setCollectionsDisplaySets( self ):
		'''
		This Method Gets The Display Sets Associated To Selected coreCollectionsOutliner Collections.
		'''

		self._displaySets = self._coreCollectionsOutliner.getCollectionsSets()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( ui.common.uiBasicExceptionHandler, False, foundations.exceptions.DatabaseOperationError )
	def addIblSet( self, name, path, collectionId = None, noWarning = False ):
		'''
		This Method Adds An Ibl Set To The Database.
		
		@param name: Ibl Set Name. ( String )		
		@param path: Ibl Set Path. ( String )		
		@param collectionId: Target Collection Id. ( Integer )		
		@param noWarning: No Warning Message. ( Boolean )
		@return: Ibl Set Database Addition Success. ( Boolean )		
		'''

		if not dbUtilities.common.filterIblSets( self._coreDb.dbSession, "^{0}$".format( re.escape( path ) ), "path" ) :
			LOGGER.info( "{0} | Adding '{1}' Ibl Set To Database !".format( self.__class__.__name__, name ) )
			if dbUtilities.common.addIblSet( self._coreDb.dbSession, name, path, collectionId or self._coreCollectionsOutliner.getUniqueCollectionId() ) :
				return True
			else :
				raise foundations.exceptions.DatabaseOperationError, "{0} | Exception Raised While Adding '{1}' Ibl Set To Database !".format( self.__class__.__name__, name )
		else:
			noWarning or messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Ibl Set Path Already Exists In Database !".format( self.__class__.__name__, name ) )

	@core.executionTrace
	def addDirectory( self, directory, collectionId = None, noWarning = False ):
		'''
		This Method Adds A Sets Directory Content To The Database.
		
		@param directory: Directory To Add. ( String )		
		@param collectionId: Target Collection Id. ( Integer )		
		@param noWarning: No Warning Message. ( Boolean )
		'''

		LOGGER.debug( "> Initializing Directory '{0}' Walker.".format( directory ) )

		walker = Walker( directory )
		walker.walk( ( "\.{0}$".format( self._extension ), ), ( "\._", ) )
		for iblSet, path in walker.files.items() :
			self.addIblSet( iblSet, path, collectionId or self._coreCollectionsOutliner.getUniqueCollectionId() )

	@core.executionTrace
	def removeIblSets( self ):
		'''
		This Method Remove Ibl Sets From The Database.
		
		@return: Removal Success. ( Boolean )
		'''

		selectedIblSets = self.getSelectedItems()
		if selectedIblSets :
			if messageBox.messageBox( "Question", "Question", "Are You Sure You Want To Remove '{0}' Sets(s) ?".format( ", ".join( [str( iblSet.text() ) for iblSet in selectedIblSets] ) ), buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
				for iblSet in selectedIblSets :
					LOGGER.info( "{0} | Removing '{1}' Ibl Set From Database !".format( self.__class__.__name__, iblSet.text() ) )
					dbUtilities.common.removeIblSet( self._coreDb.dbSession, iblSet._datas.id )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( ui.common.uiBasicExceptionHandler, False, foundations.exceptions.DatabaseOperationError )
	def updateIblSetLocation( self, iblSet ):
		'''
		This Method Updates An Ibl Set Location.
		
		@param iblSet: Ibl Set To Update. ( DbIblSet )
		@return: Update Success. ( Boolean )
		'''

		file = self._container.storeLastBrowsedPath( ( QFileDialog.getOpenFileName( self, "Updating '{0}' Ibl Set Location :".format( iblSet.name ), self._container.lastBrowsedPath, "Ibls Files (*.{0})".format( self._extension ) ) ) )
		if file :
			LOGGER.info( "{0} | Updating '{1}' Ibl Set With New Location : '{2}' !".format( self.__class__.__name__, iblSet.name, file ) )
			if not dbUtilities.common.updateIblSetLocation( self._coreDb.dbSession, iblSet, file ) :
				raise foundations.exceptions.DatabaseOperationError, "{0} | Exception Raised While Updating '{1}' Ibl Set !".format( self.__class__.__name__, iblSet.name )
			else :
				return True

	@core.executionTrace
	def getSelectedItems( self ):
		'''
		This Method Returns The Database_Browser_listView Selected Items.
		
		@return: View Selected Items. ( List )
		'''

		return [self._model.itemFromIndex( index ) for index in self.ui.Database_Browser_listView.selectedIndexes()]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, Exception )
	def getFormatedShotDate( self, date, time ):
		'''
		This Method Returns A Formated Shot Date.

		@param date: sIBL Set Date Key Value. ( String )
		@param time: sIBL Set Time Key Value. ( String )
		@return: Current Shot Date. ( String )
		'''

		LOGGER.debug( "> Formatting Shot Date With '{0}' Date and '{1} Time'.".format( date, time ) )

		if date and time and date != Constants.nullObject and time != Constants.nullObject :
			shotTime = time.split( ":" )
			shotTime = shotTime[0] + "H" + shotTime[1]
			shotDate = date.replace( ":", "/" )[2:] + " - " + shotTime

			LOGGER.debug( "> Formatted Shot Date : '{0}'.".format( shotDate ) )
			return shotDate
		else :
			return Constants.nullObject

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
