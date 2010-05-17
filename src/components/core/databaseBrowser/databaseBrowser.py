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
		self._listViewSpacing = 16
		self._listViewMargin = 24
		self._listViewIconSize = 128

		self._container = None
		self._signalsSlotsCenter = None

		self._timer = None
		self._timerCycleMultiplier = 5

		self._extension = ".ibl"

		self._coreDb = None
		self._coreCollectionsOutliner = None

		self._model = None
		self._modelSelection = None

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
	def signalsSlotsCenter( self ):
		'''
		This Method Is The Property For The _signalsSlotsCenter Attribute.

		@return: self._signalsSlotsCenter. ( QObject )
		'''

		return self._signalsSlotsCenter

	@signalsSlotsCenter.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def signalsSlotsCenter( self, value ):
		'''
		This Method Is The Setter Method For The _signalsSlotsCenter Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "signalsSlotsCenter" ) )

	@signalsSlotsCenter.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def signalsSlotsCenter( self ):
		'''
		This Method Is The Deleter Method For The _signalsSlotsCenter Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "signalsSlotsCenter" ) )

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
		self._signalsSlotsCenter = QObject()

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

		self._displaySets = dbUtilities.common.getSets( self._coreDb.dbSession )

		self._model = QStandardItemModel()
		self.Database_Browser_listView_setModel()

		self.ui.Database_Browser_listView.setContextMenuPolicy( Qt.ActionsContextMenu )

		self.Database_Browser_listView_setActions()

		self.Database_Browser_listView_setView()

		self.ui.Largest_Size_label.setPixmap( QPixmap( os.path.join( self._uiResources, self._uiLargestSizeIcon ) ) )
		self.ui.Smallest_Size_label.setPixmap( QPixmap( os.path.join( self._uiResources, self._uiSmallestSizeIcon ) ) )

		self._timer = QTimer( self )
		self._timer.start( Constants.defaultTimerCycle * self._timerCycleMultiplier )

		# Signals / Slots.
		self._signalsSlotsCenter.connect( self._timer, SIGNAL( "timeout()" ), self.updateSets )
		self._signalsSlotsCenter.connect( self.ui.Thumbnails_Size_horizontalSlider, SIGNAL( "valueChanged( int )" ), self.Thumbnails_Size_horizontalSlider_OnChanged )
		self._signalsSlotsCenter.connect( self, SIGNAL( "modelChanged()" ), self.Database_Browser_listView_refreshView )

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

		# Wizard If Sets Table Is Empty.
		if not dbUtilities.common.getSets( self._coreDb.dbSession ).count() :
			if messageBox.messageBox( "Question", "Question", "The Database Is Empty, Would You Like To Add Some Sets ?", buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
				directory = self._container.storeLastBrowsedPath( ( QFileDialog.getExistingDirectory( self, "Add Directory :", self._container.lastBrowsedPath ) ) )
				if directory :
					self.addDirectory( directory )
					self._coreCollectionsOutliner.Collections_Outliner_treeView_refreshSetsCounts()
					self.Database_Browser_listView_refreshModel()

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
			self.Database_Browser_listView_refreshModel()

	@core.executionTrace
	def Database_Browser_listView_setModel( self ):
		'''
		This Method Sets The Database_Browser_listView Model.
		'''

		LOGGER.debug( " > Setting Up '{0}' Model !".format( "Templates_Outliner_treeView" ) )

		self.Database_Browser_listView_storeModelSelection()

		self._model.clear()

		for set in [set[0] for set in sorted( [( displaySet, displaySet.name ) for displaySet in self._displaySets], key = lambda x:( x[1] ) )] :
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
				iblSetStandardItemItem = QStandardItem()# QString( title ) )
				iblSetStandardItemItem.setData( title, Qt.DisplayRole )

				shotDateString = "<b>Shot Date : </b>{0}".format( self.getFormatedShotDate( date, time ) )
				toolTip = QString( """
								<p><b>{0}</b></p>
								<p><b>Author : </b>{1}<br>
								<b>Location : </b>{2}<br>
								{3}<br>
								<b>Comment : </b>{4}</p>
								""".format( title, author, location, shotDateString, comment ) )
				iblSetStandardItemItem.setToolTip( toolTip )

				if re.search( "\.[jJ][pP][gG]", icon ) or re.search( "\.[jJ][pP][eE][gG]", icon ) or re.search( "\.[pP][nN][gG]", icon ):
					iconPath = os.path.exists( icon ) and icon or os.path.join( self._uiResources, self.uiMissingIcon )
				else :
					iconPath = os.path.join( self._uiResources, self.uiFormatErrorIcon )
				iblSetStandardItemItem.setIcon( QIcon( iconPath ) )

				iblSetStandardItemItem._datas = set

				LOGGER.debug( " > Adding '{0}' To '{1}' Model.".format( title, "Database_Browser_listView" ) )
				self._model.appendRow( iblSetStandardItemItem )

		self.emit( SIGNAL( "modelChanged()" ) )

	@core.executionTrace
	def Database_Browser_listView_refreshModel( self ):
		'''
		This Method Refreshes The Database_Browser_listView Model.
		'''

		LOGGER.debug( " > Refreshing '{0}' Model !".format( "Database_Browser_listView" ) )

		self.Database_Browser_listView_setModel()

	@core.executionTrace
	def Database_Browser_listView_setView( self ):
		'''
		This Method Sets The Database_Browser_listView Ui.
		'''

		LOGGER.debug( " > Initializing '{0}' Widget !".format( "Database_Browser_listView" ) )

		self.ui.Database_Browser_listView.setAutoScroll( False )
		self.ui.Database_Browser_listView.setViewMode( QListView.IconMode )
		self.ui.Database_Browser_listView.setResizeMode( QListView.Adjust )
		self.ui.Database_Browser_listView.setSelectionMode( QAbstractItemView.ExtendedSelection )
		self.ui.Database_Browser_listView.setIconSize( QSize( self._listViewIconSize, self._listViewIconSize ) )
		self.ui.Database_Browser_listView.setAcceptDrops( False )

		self.Database_Browser_listView_setItemSize()

		self.ui.Database_Browser_listView.setModel( self._model )

	@core.executionTrace
	def Database_Browser_listView_refreshView( self ):
		'''
		This Method Refreshes The Database_Browser_listView View.
		'''

		self.Database_Browser_listView_setDefaultViewState()
		self.Database_Browser_listView_restoreModelSelection()

	@core.executionTrace
	def Database_Browser_listView_setDefaultViewState( self ):
		'''
		This Method Sets Database_Browser_listView Default View State.
		'''

		LOGGER.debug( " > Setting '{0}' Default View State !".format( "Database_Browser_listView" ) )

		self.Database_Browser_listView_setItemSize()

	@core.executionTrace
	def Database_Browser_listView_storeModelSelection( self ):
		'''
		This Method Stores Database_Browser_listView Model Selection.
		'''

		LOGGER.debug( " > Storing '{0}' Model Selection !".format( "Database_Browser_listView" ) )

		self._modelSelection = []
		for item in self.getSelectedItems() :
			self._modelSelection.append( item._datas.id )

	@core.executionTrace
	def Database_Browser_listView_restoreModelSelection( self ):
		'''
		This Method Restores Database_Browser_listView Model Selection.
		'''

		LOGGER.debug( " > Restoring '{0}' Model Selection !".format( "Database_Browser_listView" ) )

		indexes = []
		for i in range( self._model.rowCount() ) :
			collectionStandardItem = self._model.item( i )
			collectionStandardItem._datas.id in self._modelSelection and indexes.append( self._model.indexFromItem( collectionStandardItem ) )

		for index in indexes :
			self.ui.Database_Browser_listView.selectionModel().setCurrentIndex( index, QItemSelectionModel.Select )

	@core.executionTrace
	def Database_Browser_listView_setItemSize( self ):
		'''
		This Method Scales The Database_Browser_listView Item Size.
		
		@param value: Thumbnails Size. ( Integer )
		'''

		LOGGER.debug( " > Setting '{0}' View Item Size To : {1}.".format( "Database_Browser_listView", self._listViewIconSize ) )

		self.ui.Database_Browser_listView.setIconSize( QSize( self._listViewIconSize, self._listViewIconSize ) )
		self.ui.Database_Browser_listView.setGridSize( QSize( self._listViewIconSize + self._listViewSpacing, self._listViewIconSize + self._listViewMargin ) )

	@core.executionTrace
	def Database_Browser_listView_setActions( self ):
		'''
		This Method Sets The Database Browser Actions.
		'''

		addContentAction = QAction( "Add Content ...", self.ui.Database_Browser_listView )
		addContentAction.triggered.connect( self.Database_Browser_listView_addContentAction )
		self.ui.Database_Browser_listView.addAction( addContentAction )

		addSetAction = QAction( "Add Set ...", self.ui.Database_Browser_listView )
		addSetAction.triggered.connect( self.Database_Browser_listView_addSetAction )
		self.ui.Database_Browser_listView.addAction( addSetAction )

		removeSetsAction = QAction( "Remove Set(s) ...", self.ui.Database_Browser_listView )
		removeSetsAction.triggered.connect( self.Database_Browser_listView_removeSetsAction )
		self.ui.Database_Browser_listView.addAction( removeSetsAction )

		updateSetsLocationsAction = QAction( "Update Set(s) Location(s) ...", self.ui.Database_Browser_listView )
		updateSetsLocationsAction.triggered.connect( self.Database_Browser_listView_updateSetsLocationsAction )
		self.ui.Database_Browser_listView.addAction( updateSetsLocationsAction )

		separatorAction = QAction( self.ui.Database_Browser_listView )
		separatorAction.setSeparator( True )
		self.ui.Database_Browser_listView.addAction( separatorAction )

	@core.executionTrace
	def Database_Browser_listView_addContentAction( self, checked ):
		'''
		This Method Is Triggered By addContentAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		directory = self._container.storeLastBrowsedPath( ( QFileDialog.getExistingDirectory( self, "Add Directory :", self._container.lastBrowsedPath ) ) )
		if directory :
			LOGGER.debug( "> Chosen Directory Path : '{0}'.".format( directory ) )
			self.addDirectory( directory )
			self._coreCollectionsOutliner.Collections_Outliner_treeView_refreshSetsCounts()
			self.setCollectionsDisplaySets()
			self.Database_Browser_listView_refreshModel()

	@core.executionTrace
	def Database_Browser_listView_addSetAction( self, checked ):
		'''
		This Method Is Triggered By addSetAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		setPath = self._container.storeLastBrowsedPath( ( QFileDialog.getOpenFileName( self, "Add Set :", self._container.lastBrowsedPath, "Ibls Files (*{0})".format( self._extension ) ) ) )
		if setPath :
			LOGGER.debug( "> Chosen Ibl Set Path : '{0}'.".format( setPath ) )
			self.addSet( os.path.basename( setPath ).replace( self._extension, "" ), setPath )
			self._coreCollectionsOutliner.Collections_Outliner_treeView_refreshSetsCounts()
			self.setCollectionsDisplaySets()
			self.Database_Browser_listView_refreshModel()

	@core.executionTrace
	def Database_Browser_listView_removeSetsAction( self, checked ):
		'''
		This Method Is Triggered By removeSetsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.removeSets()
		self._coreCollectionsOutliner.Collections_Outliner_treeView_refreshSetsCounts()
		self.setCollectionsDisplaySets()
		self.Database_Browser_listView_refreshModel()

	@core.executionTrace
	def Database_Browser_listView_updateSetsLocationsAction( self, checked ):
		'''
		This Method Is Triggered By updateSetsLocationsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		needModelRefresh = False
		selectedSets = self.getSelectedItems()
		if selectedSets :
			for set in selectedSets :
				self.updateSetLocation( set._datas )
				needModelRefresh = True

		if needModelRefresh :
			self.setCollectionsDisplaySets()
			self.Database_Browser_listView_refreshModel()

	@core.executionTrace
	def Thumbnails_Size_horizontalSlider_OnChanged( self, value ):
		'''
		This Method Scales The Database_Browser_listView Icons.
		
		@param value: Thumbnails Size. ( Integer )
		'''

		self._listViewIconSize = value

		self.Database_Browser_listView_setItemSize()

	@core.executionTrace
	def setCollectionsDisplaySets( self ):
		'''
		This Method Gets The Display Sets Associated To Selected coreCollectionsOutliner Collections.
		'''

		self._displaySets = self._coreCollectionsOutliner.getCollectionsSets()

	@core.executionTrace
	def updateSets( self ):
		'''
		This Method Updates Database Sets If They Have Been Modified On Disk.
		'''

		needModelRefresh = False
		for set in dbUtilities.common.getSets( self._coreDb.dbSession ) :
			if set.path :
				if os.path.exists( set.path ) :
					storedStats = set.osStats.split( "," )
					osStats = os.stat( set.path )
					if str( osStats[8] ) != str( storedStats[8] ):
						LOGGER.info( "{0} | '{1}' Set IBL File Has Been Modified And Will Be Updated !".format( self.__class__.__name__, set.name ) )
						if dbUtilities.common.updateSetContent( self._coreDb.dbSession, set ) :
							LOGGER.info( "{0} | '{1}' Set Has Been Updated !".format( self.__class__.__name__, set.name ) )
							needModelRefresh = True

		if needModelRefresh :
			self.setCollectionsDisplaySets()
			self.Database_Browser_listView_refreshModel()

	@core.executionTrace
	def addSet( self, name, path, collectionId = None ):
		'''
		This Method Adds A Set To The Database.
		
		@param name: Set Name. ( String )		
		@param path: Set Path. ( String )		
		@param collectionId: Target Collection Id. ( Integer )		
		'''

		if not dbUtilities.common.filterSets( self._coreDb.dbSession, "^{0}$".format( path ), "path" ) :
			LOGGER.info( "{0} | Adding '{1}' Set To Database !".format( self.__class__.__name__, os.path.basename( path ).replace( self._extension, "" ) ) )
			if not dbUtilities.common.addSet( self._coreDb.dbSession, name, path, collectionId or self._coreCollectionsOutliner.getUniqueCollectionId() ) :
				messageBox.messageBox( "Error", "Error", "{0} | Exception Raised While Adding '{1}' Set To Database !".format( self.__class__.__name__, os.path.basename( path ).replace( self._extension, "" ) ) )
		else:
			messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Set Path Already Exists In Database !".format( self.__class__.__name__, name ) )

	@core.executionTrace
	def addDirectory( self, directory, collectionId = None ):
		'''
		This Method Adds A Sets Directory Content To The Database.
		
		@param directory: Directory To Add. ( String )		
		@param collectionId: Target Collection Id. ( Integer )		
		'''

		LOGGER.debug( "> Initializing Directory '{0}' Walker.".format( directory ) )

		walker = Walker( directory )
		walker.walk( self._extension )
		for set, path in walker.files.items() :
			self.addSet( set, path, collectionId or self._coreCollectionsOutliner.getUniqueCollectionId() )

	@core.executionTrace
	def removeSets( self ):
		'''
		This Method Remove Sets From The Database.
		
		@return: Removal Success. ( Boolean )
		'''

		selectedSets = self.getSelectedItems()
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
	def getSelectedItems( self ):
		'''
		This Method Returns The Database_Browser_listView Selected Items.
		
		@return: View Selected Items. ( List )
		'''

		return [self._model.itemFromIndex( index ) for index in self.ui.Database_Browser_listView.selectedIndexes()]

	@core.executionTrace
	def getFormatedShotDate( self, date, time ):
		'''
		This Method Returns A Formated Shot Date.

		@param date: sIBL Set Date Key Value. ( String )
		@param time: sIBL Set Time Key Value. ( String )
		@return: Current Shot Date. ( String )
		'''

		LOGGER.debug( "> Formatting Shot Date With '{0}' Date and '{1} Time'.".format( date, time ) )

		try :
			assert date and date != Constants.nullObject
			assert time and time != Constants.nullObject
			shotTime = time.split( ":" )
			shotTime = shotTime[0] + "H" + shotTime[1]
			shotDate = date.replace( ":", "/" )[2:] + " - " + shotTime

			LOGGER.debug( "> Formatted Shot Date : '{0}'.".format( shotDate ) )
			return shotDate
		except :
			return Constants.nullObject

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
