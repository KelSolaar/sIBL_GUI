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
import ui.widgets.messageBox as messageBox
from foundations.walker import Walker
from globals.constants import Constants
from globals.uiConstants import UiConstants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class DatabaseBrowser( UiComponent ):
	'''
	This Class Is The DatabaseBrowser Class.
	'''

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
		self._dockArea = 8
		self._listWidgetSpacing = 4
		self._listWidgetIconSize = 128

		self._container = None

		self._timer = None
		self._timerCycleMultiplier = 5

		self._extension = ".ibl"

		self._coreDb = None
		self._coreCollectionsOutliner = None

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
	def listWidgetSpacing( self ):
		'''
		This Method Is The Property For The _listWidgetSpacing Attribute.

		@return: self._listWidgetSpacing. ( Integer )
		'''

		return self._listWidgetSpacing

	@listWidgetSpacing.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def listWidgetSpacing( self, value ):
		'''
		This Method Is The Setter Method For The _listWidgetSpacing Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		if value :
			assert type( value ) is int, "'{0}' Attribute : '{1}' Type Is Not 'int' !".format( "listWidgetSpacing", value )
			assert value > 0, "'{0}' Attribute : '{1}' Need To Be Exactly Positive !".format( "listWidgetSpacing", value )
		self._listWidgetSpacing = value

	@listWidgetSpacing.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def listWidgetSpacing( self ):
		'''
		This Method Is The Deleter Method For The _listWidgetSpacing Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "listWidgetSpacing" ) )

	@property
	def listWidgetIconSize( self ):
		'''
		This Method Is The Property For The _listWidgetIconSize Attribute.

		@return: self._listWidgetIconSize. ( Integer )
		'''

		return self._listWidgetIconSize

	@listWidgetIconSize.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def listWidgetIconSize( self, value ):
		'''
		This Method Is The Setter Method For The _listWidgetIconSize Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		if value :
			assert type( value ) is int, "'{0}' Attribute : '{1}' Type Is Not 'int' !".format( "listWidgetIconSize", value )
			assert value > 0, "'{0}' Attribute : '{1}' Need To Be Exactly Positive !".format( "listWidgetIconSize", value )
		self._listWidgetIconSize = value

	@listWidgetIconSize.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def listWidgetIconSize( self ):
		'''
		This Method Is The Deleter Method For The _listWidgetIconSize Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "listWidgetIconSize" ) )

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

		self._container.setsCentricLayoutComponents.append( self.name )
		self._container.templatesCentricLayoutComponents.append( self.name )
		self._container.preferencesCentricLayoutComponents.append( self.name )

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

		self.ui.Database_Browser_listWidget.setSpacing( self._listWidgetSpacing )
		self.ui.Database_Browser_listWidget.setIconSize( QSize( self._listWidgetIconSize, self._listWidgetIconSize ) )
		self.ui.Database_Browser_listWidget.setAcceptDrops( False )

		self.ui.Database_Browser_listWidget.setContextMenuPolicy( Qt.ActionsContextMenu )

		self.Database_Browser_listWidget_setActions()

		self._displaySets = dbUtilities.common.getSets( self._coreDb.dbSession )

		self.Database_Browser_listWidget_setUi()

		self._timer = QTimer( self )
		self._timer.start( Constants.defaultTimerCycle * self._timerCycleMultiplier )

		# Signals / Slots.
		self.connect( self._timer, SIGNAL( "timeout()" ), self.updateSets )

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

		# Wizard If Sets Table Is Empty.
		if not dbUtilities.common.getSets( self._coreDb.dbSession ).count() :
			if messageBox.messageBox( "Question", "Question", "The Database Has No Sets, Do You Want To Add Some ?", buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
				self.addDirectory()
				self._coreCollectionsOutliner.Collections_Outliner_treeWidget_refreshSetsCounts()
				self.refreshUi()

		# Sets Table Integrity Checking.
		erroneousSets = dbUtilities.common.checkSetsTableIntegrity( self._coreDb.dbSession )
		if erroneousSets :
			for set in erroneousSets :
				if erroneousSets[set] == "errorInexistingIblSetFile" :
					if messageBox.messageBox( "Question", "error", "{0} | '{1}' Set File Is Missing, Would You Like To Update It's Location ?".format( self.__class__.__name__, set.name ), QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No ) == 16384 :
						self.updateSetLocation( set )
				else :
					messageBox.messageBox( "Error", "Error", "{0} | '{1}' {2}".format( self.__class__.__name__, set.name, dbUtilities.common.DB_ERRORS[erroneousSets[set]] ) )
			self.setCollectionsDisplaySets()
			self.refreshUi()

	@core.executionTrace
	def setCollectionsDisplaySets( self ):
		'''
		This Method Gets The Display Sets Associated To Selected coreCollectionsOutliner Collections.
		'''

		self._displaySets = self._coreCollectionsOutliner.getCollectionsSets()

	@core.executionTrace
	def refreshUi( self ):
		'''
		This Method Refreshes The Database_Browser_listWidget Ui.
		'''

		self.Database_Browser_listWidget_setUi()

	@core.executionTrace
	def Database_Browser_listWidget_setUi( self ):
		'''
		This Method Sets The Database_Browser_listWidget Ui.
		'''

		LOGGER.debug( " > Refreshing '{0}' Ui !".format( self.__class__.__name__ ) )

		self.ui.Database_Browser_listWidget.clear()

		for set in self._displaySets :

			id = set.id
			name = set.name or Constants.nullObject
			title = set.title
			author = set.author or Constants.nullObject
			icon = set.icon or Constants.nullObject
			location = set.location or Constants.nullObject
			date = set.date or Constants.nullObject
			time = set.time or Constants.nullObject
			comment = set.comment or Constants.nullObject

			if title :
				listWidgetItem = QListWidgetItem( QString( title ) )

				shotDateString = "<b>Shot Date : </b>{0}".format( self.getFormatedShotDate( date, time ) )

				toolTip = QString( """
								<p><b>{0}</b></p>
								<p><b>Author : </b>{1}<br>
								<b>Location : </b>{2}<br>
								{3}<br>
								<b>Comment : </b>{4}</p>
								""".format( title, author, location, shotDateString, comment ) )

				listWidgetItem.setToolTip( toolTip )

				if re.search( "\.[jJ][pP][gG]", icon ) or re.search( "\.[jJ][pP][eE][gG]", icon ) or re.search( "\.[pP][nN][gG]", icon ):
					icon = os.path.exists( icon ) and QIcon( QPixmap( icon ) ) or QIcon( os.path.join( self._uiResources, self.uiMissingIcon ) )
				else :
					icon = QIcon( os.path.join( self._uiResources, self.uiFormatErrorIcon ) )
				listWidgetItem.setIcon( icon )

				listWidgetItem._datas = set

				LOGGER.debug( " > Adding '{0}' To 'self.Collections_listWidget'.".format( title ) )
				self.ui.Database_Browser_listWidget.addItem( listWidgetItem )

			else:
				messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Set Has No 'Name' Field And Can't Be Added !".format( self.__class__.__name__, name ) )

		self.ui.Database_Browser_listWidget.sortItems( Qt.AscendingOrder )

	@core.executionTrace
	def Database_Browser_listWidget_setActions( self ):
		'''
		This Method Sets The Database Browser Actions.
		'''

		addContentAction = QAction( "Add Content ...", self.ui.Database_Browser_listWidget )
		addContentAction.triggered.connect( self.Database_Browser_listWidget_addContentAction )
		self.ui.Database_Browser_listWidget.addAction( addContentAction )

		addSetAction = QAction( "Add Set ...", self.ui.Database_Browser_listWidget )
		addSetAction.triggered.connect( self.Database_Browser_listWidget_addSetAction )
		self.ui.Database_Browser_listWidget.addAction( addSetAction )

		removeSetsAction = QAction( "Remove Set(s) ...", self.ui.Database_Browser_listWidget )
		removeSetsAction.triggered.connect( self.Database_Browser_listWidget_removeSetsAction )
		self.ui.Database_Browser_listWidget.addAction( removeSetsAction )

		updateSetsLocationsAction = QAction( "Update Set(s) Location(s) ...", self.ui.Database_Browser_listWidget )
		updateSetsLocationsAction.triggered.connect( self.Database_Browser_listWidget_updateSetsLocationsAction )
		self.ui.Database_Browser_listWidget.addAction( updateSetsLocationsAction )

		separatorAction = QAction( self.ui.Database_Browser_listWidget )
		separatorAction.setSeparator( True )
		self.ui.Database_Browser_listWidget.addAction( separatorAction )

	@core.executionTrace
	def Database_Browser_listWidget_addContentAction( self, checked ):
		'''
		This Method Is Triggered By addContentAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.addDirectory()
		self._coreCollectionsOutliner.Collections_Outliner_treeWidget_refreshSetsCounts()
		self.setCollectionsDisplaySets()
		self.refreshUi()

	@core.executionTrace
	def Database_Browser_listWidget_addSetAction( self, checked ):
		'''
		This Method Is Triggered By addSetAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.addSet()
		self._coreCollectionsOutliner.Collections_Outliner_treeWidget_refreshSetsCounts()
		self.setCollectionsDisplaySets()
		self.refreshUi()

	@core.executionTrace
	def Database_Browser_listWidget_removeSetsAction( self, checked ):
		'''
		This Method Is Triggered By removeSetsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.removeSets()
		self._coreCollectionsOutliner.Collections_Outliner_treeWidget_refreshSetsCounts()
		self.setCollectionsDisplaySets()
		self.refreshUi()

	@core.executionTrace
	def Database_Browser_listWidget_updateSetsLocationsAction( self, checked ):
		'''
		This Method Is Triggered By updateSetsLocationsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		needUiRefresh = False
		selectedSets = self.ui.Database_Browser_listWidget.selectedItems()
		if selectedSets :
			for set in selectedSets :
				self.updateSetLocation( set._datas )
				needUiRefresh = True

		if needUiRefresh :
			self.setCollectionsDisplaySets()
			self.refreshUi()

	@core.executionTrace
	def updateSets( self ):
		'''
		This Method Updates Database Sets If They Have Been Modified On Disk.
		'''

		needUiRefresh = False
		for set in dbUtilities.common.getSets( self._coreDb.dbSession ) :
			if set.path :
				if os.path.exists( set.path ) :
					storedStats = set.osStats.split( "," )
					osStats = os.stat( set.path )
					if str( osStats[8] ) != str( storedStats[8] ):
						LOGGER.info( "{0} | '{1}' Set IBL File Has Been Modified And Will Be Updated !".format( self.__class__.__name__, set.name ) )
						if dbUtilities.common.updateSetContent( self._coreDb.dbSession, set ) :
							LOGGER.info( "{0} | '{1}' Set Has Been Updated !".format( self.__class__.__name__, set.name ) )
							needUiRefresh = True

		if needUiRefresh :
			self.setCollectionsDisplaySets()
			self.refreshUi()

	@core.executionTrace
	def addDirectory( self, collectionId = None ):
		'''
		This Method Adds A Sets Directory Content To The Database.
		
		@param collectionId: Target Collection Id. ( Integer )		
		'''

		directory = self._container.storeLastBrowsedPath( ( QFileDialog.getExistingDirectory( self, "Add Directory :", self._container.lastBrowsedPath ) ) )
		if directory :
			walker = Walker( directory )
			walker.walk( self._extension )
			for set, path in walker.files.items() :
				if not dbUtilities.common.filterSets( self._coreDb.dbSession, "^{0}$".format( path ), "path" ) :
					LOGGER.info( "{0} | Adding '{1}' Set To Database !".format( self.__class__.__name__, set ) )
					if not dbUtilities.common.addSet( self._coreDb.dbSession, set, path, collectionId or self._coreCollectionsOutliner.getUniqueCollectionId() ) :
						messageBox.messageBox( "Error", "Error", "{0} | Exception Raised While Adding '{1}' Set To Database !".format( self.__class__.__name__, set ) )
				else:
					messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Set Path Already Exists In Database !".format( self.__class__.__name__, set ) )

	@core.executionTrace
	def addSet( self ):
		'''
		This Method Adds A Set To The Database.
		
		@return: Addition Success. ( Boolean )
		'''

		file = self._container.storeLastBrowsedPath( ( QFileDialog.getOpenFileName( self, "Add Set :", self._container.lastBrowsedPath, "Ibls Files (*{0})".format( self._extension ) ) ) )
		if file :
			LOGGER.info( "{0} | Adding '{1}' Set To Database !".format( self.__class__.__name__, os.path.basename( file ).replace( self._extension, "" ) ) )
			if not dbUtilities.common.addSet( self._coreDb.dbSession, os.path.basename( file ).replace( self._extension, "" ), file, self._coreCollectionsOutliner.getUniqueCollectionId() ) :
				messageBox.messageBox( "Error", "Error", "{0} | Exception Raised While Adding '{1}' Set To Database !".format( self.__class__.__name__, os.path.basename( file ).replace( self._extension, "" ) ) )

	@core.executionTrace
	def removeSets( self ):
		'''
		This Method Remove Sets From The Database.
		
		@return: Removal Success. ( Boolean )
		'''

		selectedSets = self.ui.Database_Browser_listWidget.selectedItems()
		if selectedSets :
			if messageBox.messageBox( "Question", "Question", "Are You Sure You Want To Remove '{0}' Sets(s) ?".format( ", ".join( [str( set.text() ) for set in selectedSets] ) ), buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
				for set in selectedSets :
					LOGGER.info( "{0} | Removing '{1}' Set From Database !".format( self.__class__.__name__, set.text() ) )
					dbUtilities.common.removeSet( self._coreDb.dbSession, set._datas.id )

	@core.executionTrace
	def updateSetLocation( self, set ):
		'''
		This Method Updates A Set Location.
		
		@param set: Set To Update. ( DbSet )
		@return: Update Success. ( Boolean )
		'''

		file = self._container.storeLastBrowsedPath( ( QFileDialog.getOpenFileName( self, "Updating '{0}' Set Location :".format( set.name ), self._container.lastBrowsedPath, "Ibls Files (*{0})".format( self._extension ) ) ) )
		if file :
			LOGGER.info( "{0} | Updating '{1}' Set !".format( self.__class__.__name__, os.path.basename( file ).replace( self._extension, "" ) ) )
			if not dbUtilities.common.updateSetLocation( self._coreDb.dbSession, set, file ) :
				messageBox.messageBox( "Error", "Error", "{0} | Exception Raised While Updating '{1}' Set !".format( self.__class__.__name__, set.name ) )
				return False
			else :
				return True

	@core.executionTrace
	def getFormatedShotDate( self, date, time ):
		'''
		This Method Returns A Formated Shot Date.

		@param date: sIBL Set Date Key Value. ( String )
		@param time: sIBL Set Time Key Value. ( String )
		@return: Current Shot Date. ( String )
		'''

		try :
			assert date and date != Constants.nullObject
			assert time and time != Constants.nullObject
			shotTime = time.split( ":" )
			shotTime = shotTime[0] + "H" + shotTime[1]
			shotDate = date.replace( ":", "/" )[2:] + " - " + shotTime
			return shotDate
		except :
			return Constants.nullObject

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
