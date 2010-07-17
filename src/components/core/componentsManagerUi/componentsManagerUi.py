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
***	componentsManagerUi.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Components Manager Ui Component Module.
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
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import traceback

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import ui.common
import ui.widgets.messageBox as messageBox
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@core.executionTrace
def componentActivationErrorHandler( exception, origin, *args, **kwargs ):
	'''
	This Definition Provides An Exception Handler For Component Activation.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	'''

	ui.common.uiBasicExceptionHandler( Exception( "{0} | An Exception Occurred While Activating '{1}' Component :\n{2}".format( core.getModule( componentActivationErrorHandler ).__name__, args[1].name, traceback.format_exc() ) ), origin, *args, **kwargs )

@core.executionTrace
def componentDeactivationErrorHandler( exception, origin, *args, **kwargs ):
	'''
	This Definition Provides An Exception Handler For Component Deactivation.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	'''

	ui.common.uiBasicExceptionHandler( Exception( "{0} | An Exception Occurred While Deactivating '{1}' Component :\n{2}".format( core.getModule( componentActivationErrorHandler ).__name__, args[1].name, traceback.format_exc() ) ), origin, *args, **kwargs )

class ComponentsManagerUi( UiComponent ):
	'''
	This Class Is The ComponentsManagerUi Class.
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

		self._uiPath = "ui/Components_Manager_Ui.ui"
		self._uiResources = "resources"
		self._uiActivatedIcon = "Activated.png"
		self._uiDeactivatedIcon = "Deactivated.png"
		self._uiCategorieAffixe = "_Categorie.png"
		self._dockArea = 1

		self._container = None
		self._signalsSlotsCenter = None
		self._settings = None

		self._model = None

		self._modelHeaders = [ "Components", "Activated", "Categorie", "Rank", "Version" ]
		self._treeWidgetIndentation = 15
		self._treeViewInnerMargins = QMargins( 0, 0, 0, 12 )
		self._Components_Informations_textBrowser_defaultText = "<center><h4>* * *</h4>Select Some Components To Display Related Informations !<h4>* * *</h4></center>"

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
	def uiActivatedIcon( self ):
		'''
		This Method Is The Property For The _uiActivatedIcon Attribute.

		@return: self._uiActivatedIcon. ( String )
		'''

		return self._uiActivatedIcon

	@uiActivatedIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiActivatedIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiActivatedIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiActivatedIcon" ) )

	@uiActivatedIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiActivatedIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiActivatedIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiActivatedIcon" ) )

	@property
	def uiDeactivatedIcon( self ):
		'''
		This Method Is The Property For The _uiDeactivatedIcon Attribute.

		@return: self._uiDeactivatedIcon. ( String )
		'''

		return self._uiDeactivatedIcon

	@uiDeactivatedIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiDeactivatedIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiDeactivatedIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiDeactivatedIcon" ) )

	@uiDeactivatedIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiDeactivatedIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiDeactivatedIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiDeactivatedIcon" ) )

	@property
	def uiCategorieAffixe( self ):
		'''
		This Method Is The Property For The _uiCategorieAffixe Attribute.

		@return: self._uiCategorieAffixe. ( String )
		'''

		return self._uiCategorieAffixe

	@uiCategorieAffixe.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiCategorieAffixe( self, value ):
		'''
		This Method Is The Setter Method For The _uiCategorieAffixe Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiCategorieAffixe" ) )

	@uiCategorieAffixe.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiCategorieAffixe( self ):
		'''
		This Method Is The Deleter Method For The _uiCategorieAffixe Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiCategorieAffixe" ) )

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
	def modelHeaders( self ):
		'''
		This Method Is The Property For The _modelHeaders Attribute.

		@return: self._modelHeaders. ( List )
		'''

		return self._modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def modelHeaders( self, value ):
		'''
		This Method Is The Setter Method For The _modelHeaders Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "modelHeaders" ) )

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def modelHeaders( self ):
		'''
		This Method Is The Deleter Method For The _modelHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "modelHeaders" ) )

	@property
	def treeWidgetIndentation( self ):
		'''
		This Method Is The Property For The _treeWidgetIndentation Attribute.

		@return: self._treeWidgetIndentation. ( Integer )
		'''

		return self._treeWidgetIndentation

	@treeWidgetIndentation.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetIndentation( self, value ):
		'''
		This Method Is The Setter Method For The _treeWidgetIndentation Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "treeWidgetIndentation" ) )

	@treeWidgetIndentation.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetIndentation( self ):
		'''
		This Method Is The Deleter Method For The _treeWidgetIndentation Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "treeWidgetIndentation" ) )

	@property
	def treeViewInnerMargins( self ):
		'''
		This Method Is The Property For The _treeViewInnerMargins Attribute.

		@return: self._treeViewInnerMargins. ( Integer )
		'''

		return self._treeViewInnerMargins

	@treeViewInnerMargins.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeViewInnerMargins( self, value ):
		'''
		This Method Is The Setter Method For The _treeViewInnerMargins Attribute.

		@param value: Attribute Value. ( Integer )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "treeViewInnerMargins" ) )

	@treeViewInnerMargins.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeViewInnerMargins( self ):
		'''
		This Method Is The Deleter Method For The _treeViewInnerMargins Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "treeViewInnerMargins" ) )

	@property
	def Components_Informations_textBrowser_defaultText( self ):
		'''
		This Method Is The Property For The _Components_Informations_textBrowser_defaultText Attribute.

		@return: self._Components_Informations_textBrowser_defaultText. ( String )
		'''

		return self._Components_Informations_textBrowser_defaultText

	@Components_Informations_textBrowser_defaultText.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Components_Informations_textBrowser_defaultText( self, value ):
		'''
		This Method Is The Setter Method For The _Components_Informations_textBrowser_defaultText Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "Components_Informations_textBrowser_defaultText" ) )

	@Components_Informations_textBrowser_defaultText.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Components_Informations_textBrowser_defaultText( self ):
		'''
		This Method Is The Deleter Method For The _Components_Informations_textBrowser_defaultText Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "Components_Informations_textBrowser_defaultText" ) )

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

		self._settings = self._container.settings

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

		self._model = QStandardItemModel()

		self.Components_Manager_Ui_treeView_setModel()

		self.ui.Components_Manager_Ui_gridLayout.setContentsMargins( self._treeViewInnerMargins )

		self.ui.Components_Manager_Ui_treeView.setContextMenuPolicy( Qt.ActionsContextMenu )
		self.Components_Manager_Ui_treeView_setActions()

		self.Components_Manager_Ui_treeView_setView()

		self.ui.Components_Informations_textBrowser.setText( self._Components_Informations_textBrowser_defaultText )

		self.ui.Components_Manager_Ui_splitter.setSizes( [ 16777215, 1 ] )

		# Signals / Slots.
		self._signalsSlotsCenter.connect( self.ui.Components_Manager_Ui_treeView.selectionModel(), SIGNAL( "selectionChanged( const QItemSelection &, const QItemSelection & )" ), self.Components_Manager_Ui_treeView_OnSelectionChanged )
		self._signalsSlotsCenter.connect( self, SIGNAL( "modelChanged()" ), self.Components_Manager_Ui_treeView_refreshView )

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

		self._container.addDockWidget( Qt.DockWidgetArea( self._dockArea ), self.ui )

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

		self.Components_Manager_Ui_treeView_refreshActivationsStatus()

	@core.executionTrace
	def Components_Manager_Ui_treeView_setModel( self ):
		'''
		This Method Sets The Components_Manager_Ui_treeView Model.
		
		Columns :
		Collections | Activated | Categorie | Rank | Version
		
		Rows :
		* Path : { _type : "Path" }
		** Component : { _type : "Component", _datas : profile }
		'''

		LOGGER.debug( "> Setting Up '{0}' Model !".format( "Components_Manager_Ui_treeView" ) )

		self._model.clear()

		self._model.setHorizontalHeaderLabels( self._modelHeaders )
		self._model.setColumnCount( len( self._modelHeaders ) )

		for path in self._container.componentsManager.paths :
			components = [component for component in self._container.componentsManager.components if os.path.normpath( self._container.componentsManager.paths[path] ) in os.path.normpath( self._container.componentsManager.components[component].path )]

			if components :
				pathStandardItem = QStandardItem( QString( path ) )
				pathStandardItem._type = "Path"

				LOGGER.debug( "> Adding '{0}' Path To '{1}' Model.".format( path, "Components_Manager_Ui_treeView" ) )
				self._model.appendRow( pathStandardItem )

				for component in components :
					componentStandardItem = QStandardItem( QString( strings.getNiceName( self._container.componentsManager.components[component].module ) ) )
					iconPath = os.path.join( self._uiResources, "{0}{1}".format( strings.getNiceName( self._container.componentsManager.components[component].categorie ), self._uiCategorieAffixe ) )
					componentStandardItem.setIcon( QIcon( iconPath ) )

					componentActivationStandardItem = QStandardItem( QString( str( self._container.componentsManager.components[component].interface.activated ) ) )
					iconPath = self._container.componentsManager.components[component].interface.activated and os.path.join( self._uiResources, self._uiActivatedIcon ) or os.path.join( self._uiResources, self._uiDeactivatedIcon )
					componentActivationStandardItem.setIcon( QIcon( iconPath ) )

					componentCategorieStandardItem = QStandardItem( QString( self._container.componentsManager.components[component].categorie and strings.getNiceName( self._container.componentsManager.components[component].categorie ) or "" ) )
					componentCategorieStandardItem.setTextAlignment( Qt.AlignCenter )

					componentRankStandardItem = QStandardItem( QString( self._container.componentsManager.components[component].rank or "" ) )
					componentRankStandardItem.setTextAlignment( Qt.AlignCenter )

					componentVersionStandardItem = QStandardItem( QString( self._container.componentsManager.components[component].version or "" ) )
					componentVersionStandardItem.setTextAlignment( Qt.AlignCenter )

					componentStandardItem._datas = self._container.componentsManager.components[component]
					componentStandardItem._type = "Component"

					LOGGER.debug( "> Adding '{0}' Component To '{1}'.".format( component, "Components_Manager_Ui_treeView" ) )
					pathStandardItem.appendRow( [componentStandardItem, componentActivationStandardItem, componentCategorieStandardItem, componentRankStandardItem, componentVersionStandardItem] )

		self.emit( SIGNAL( "modelChanged()" ) )

	@core.executionTrace
	def Components_Manager_Ui_treeView_refreshModel( self ):
		'''
		This Method Refreshes The Components_Manager_Ui_treeView Model.
		'''

		LOGGER.debug( "> Refreshing '{0}' Model !".format( "Components_Manager_Ui_treeView" ) )

		self.Components_Manager_Ui_treeView_setModel()

	@core.executionTrace
	def Components_Manager_Ui_treeView_setView( self ):
		'''
		This Method Sets The Components_Manager_Ui_treeView View.
		'''

		LOGGER.debug( "> Refreshing '{0}' Ui !".format( self.__class__.__name__ ) )

		self.ui.Components_Manager_Ui_treeView.setAutoScroll( False )
		self.ui.Components_Manager_Ui_treeView.setEditTriggers( QAbstractItemView.NoEditTriggers )
		self.ui.Components_Manager_Ui_treeView.setDragDropMode( QAbstractItemView.NoDragDrop )
		self.ui.Components_Manager_Ui_treeView.setSelectionMode( QAbstractItemView.ExtendedSelection )
		self.ui.Components_Manager_Ui_treeView.setIndentation( self._treeWidgetIndentation )
		self.ui.Components_Manager_Ui_treeView.setSortingEnabled( True )

		self.ui.Components_Manager_Ui_treeView.setModel( self._model )

		self.Components_Manager_Ui_treeView_setDefaultViewState()

	@core.executionTrace
	def Components_Manager_Ui_treeView_refreshView( self ):
		'''
		This Method Refreshes The Components_Manager_Ui_treeView View.
		'''

		self.Components_Manager_Ui_treeView_setDefaultViewState()

	@core.executionTrace
	def Components_Manager_Ui_treeView_setDefaultViewState( self ):
		'''
		This Method Sets Components_Manager_Ui_treeView Default View State.
		'''

		LOGGER.debug( "> Setting '{0}' Default View State !".format( "Components_Manager_Ui_treeView" ) )

		self.ui.Components_Manager_Ui_treeView.expandAll()
		for column in range( len( self._modelHeaders ) ) :
			self.ui.Components_Manager_Ui_treeView.resizeColumnToContents( column )

		self.ui.Components_Manager_Ui_treeView.sortByColumn( 0, Qt.AscendingOrder )

	@core.executionTrace
	def Components_Manager_Ui_treeView_refreshActivationsStatus( self ):
		'''
		This Method Refreshes The Components_Manager_Ui_treeView Activations Status.
		'''

		for i in range( self._model.rowCount() ) :
			for j in range( self._model.item( i ).rowCount() ):
				componentStandardItem = self._model.item( i ).child( j, 0 )
				componentActivationStandardItem = self._model.item( i ).child( j, 1 )
				componentActivationStandardItem.setText( str( componentStandardItem._datas.interface.activated ) )
				iconPath = componentStandardItem._datas.interface.activated and os.path.join( self._uiResources, self._uiActivatedIcon ) or os.path.join( self._uiResources, self._uiDeactivatedIcon )
				componentActivationStandardItem.setIcon( QIcon( iconPath ) )

	@core.executionTrace
	def Components_Manager_Ui_treeView_setActions( self ):
		'''
		This Method Sets The Components_Manager_Ui_treeView Actions.
		'''

		activateComponentsAction = QAction( "Activate Component(s)", self.ui.Components_Manager_Ui_treeView )
		activateComponentsAction.triggered.connect( self.Components_Manager_Ui_treeView_activateComponentsAction )
		self.ui.Components_Manager_Ui_treeView.addAction( activateComponentsAction )

		deactivateComponentsAction = QAction( "Deactivate Component(s)", self.ui.Components_Manager_Ui_treeView )
		deactivateComponentsAction.triggered.connect( self.Components_Manager_Ui_treeView_deactivateComponentsAction )
		self.ui.Components_Manager_Ui_treeView.addAction( deactivateComponentsAction )

		separatorAction = QAction( self.ui.Components_Manager_Ui_treeView )
		separatorAction.setSeparator( True )
		self.ui.Components_Manager_Ui_treeView.addAction( separatorAction )

		reloadComponentsAction = QAction( "Reload Component(s)", self.ui.Components_Manager_Ui_treeView )
		reloadComponentsAction.triggered.connect( self.Components_Manager_Ui_treeView_reloadComponentsAction )
		self.ui.Components_Manager_Ui_treeView.addAction( reloadComponentsAction )

		separatorAction = QAction( self.ui.Components_Manager_Ui_treeView )
		separatorAction.setSeparator( True )
		self.ui.Components_Manager_Ui_treeView.addAction( separatorAction )

	@core.executionTrace
	def Components_Manager_Ui_treeView_activateComponentsAction( self, checked ):
		'''
		This Method Is Triggered By activateComponentsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedComponents = self.getSelectedItems()

		if selectedComponents :
			for component in selectedComponents :
				if component._type == "Component" :
					if not component._datas.interface.activated :
						self.activateComponent( component._datas )
					else :
						messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Component Is Already Activated !".format( self.__class__.__name__, component._datas.name ) )

			self.Components_Manager_Ui_treeView_refreshActivationsStatus()
			self.storeDeactivatedComponents()

	@core.executionTrace
	def Components_Manager_Ui_treeView_deactivateComponentsAction( self, checked ):
		'''
		This Method Is Triggered By deactivateComponentsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedComponents = self.getSelectedItems()

		if selectedComponents :
			for component in selectedComponents :
				if component._type == "Component" :
					if component._datas.interface.activated :
						if component._datas.interface.deactivatable :
							self.deactivateComponent( component._datas )
						else :
							messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Component Cannot Be Deactivated !".format( self.__class__.__name__, component._datas.name ) )
					else :
						messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Component Is Already Deactivated !".format( self.__class__.__name__, component._datas.name ) )

			self.Components_Manager_Ui_treeView_refreshActivationsStatus()
			self.storeDeactivatedComponents()

	@core.executionTrace
	def Components_Manager_Ui_treeView_reloadComponentsAction( self, checked ):
		'''
		This Method Is Triggered By reloadComponentsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedComponents = self.getSelectedItems()
		if selectedComponents :
			for component in selectedComponents :
				if component._type == "Component" :
					if component._datas.interface.deactivatable :
						if component._datas.interface.activated :
							self.deactivateComponent( component._datas )
						self._container.componentsManager.reloadComponent( component._datas.name )
						if not component._datas.interface.activated :
							self.activateComponent( component._datas )
					else :
						messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Component Cannot Be Reloaded !".format( self.__class__.__name__, component._datas.name ) )
			self.Components_Manager_Ui_treeView_refreshActivationsStatus()

	@core.executionTrace
	def Components_Manager_Ui_treeView_OnSelectionChanged( self, selectedItems, deselectedItems ):
		'''
		This Method Sets The Additional_Informations_textEdit Widget.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		'''

		LOGGER.debug( "> Initializing '{0}' Widget.".format( "Additional_Informations_textEdit" ) )

		content = []
		subContent = """
					<h4><center>{0}</center></h4>
					<p>
					<b>Categorie :</b> {1}
					<br/>
					<b>Author :</b> {2}
					<br/>
					<b>Email :</b> <a href="mailto:{3}"><span style=" text-decoration: underline; color:#000000;">{3}</span></a>
					<br/>
					<b>Url :</b> <a href="{4}"><span style=" text-decoration: underline; color:#000000;">{4}</span></a>
					<p>
					<b>Description :</b> {5}
					</p>
					</p>
					"""

		selectedItems = self.getSelectedItems()
		for item in selectedItems :
			if item._type == "Component" :
				content.append( subContent.format( item._datas.name,
												strings.getNiceName( item._datas.categorie ),
												item._datas.author,
												item._datas.email,
												item._datas.url,
												item._datas.description
												) )
			else:
				len( selectedItems ) == 1 and content.append( self._Components_Informations_textBrowser_defaultText )

		separator = len( content ) == 1 and "" or "<p><center>* * *<center/></p>"
		self.ui.Components_Informations_textBrowser.setText( separator.join( content ) )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( componentActivationErrorHandler, False, foundations.exceptions.ComponentActivationError )
	def activateComponent( self, component ):
		'''
		This Method Activates The Provided Component.
		
		@param component: Component. ( Profile )
		'''

		LOGGER.debug( "> Attempting '{0}' Component Activation.".format( component.name ) )

		component.interface.activate( self._container )
		if component.categorie == "default" :
			component.interface.initialize()
		elif component.categorie == "ui" :
			component.interface.addWidget()
			component.interface.initializeUi()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( componentDeactivationErrorHandler, False, foundations.exceptions.ComponentDeactivationError )
	def deactivateComponent( self, component ):
		'''
		This Method Deactivates The Provided Component.
		
		@param component: Component. ( Profile )
		'''

		LOGGER.debug( "> Attempting '{0}' Component Deactivation.".format( component.name ) )

		if component.categorie == "default" :
			component.interface.uninitialize()
		elif component.categorie == "ui" :
			component.interface.uninitializeUi()
			component.interface.removeWidget()
		component.interface.deactivate()

	@core.executionTrace
	def storeDeactivatedComponents( self ):
		'''
		This Method Stores Deactivated Components In The Settings File.
		'''

		deactivatedComponents = []
		for component in self._model.findItems( ".*", Qt.MatchRegExp | Qt.MatchRecursive, 0 ) :
			if component._type == "Component" :
				component._datas.interface.activated or deactivatedComponents.append( component._datas.name )

		LOGGER.debug( "> Storing '{0}' Deactivated Components.".format( ", ".join( deactivatedComponents ) ) )
		self._settings.setKey( "Settings", "deactivatedComponents", ",".join( deactivatedComponents ) )

	@core.executionTrace
	def getSelectedItems( self, rowsRootOnly = True ):
		'''
		This Method Returns The Components_Manager_Ui_treeView Selected Items.
		
		@param rowsRootOnly:  Return Rows Roots Only. ( Boolean )
		@return: View Selected Items. ( List )
		'''

		selectedIndexes = self.ui.Components_Manager_Ui_treeView.selectedIndexes()

		return rowsRootOnly and [item for item in set( [self._model.itemFromIndex( self._model.sibling( index.row(), 0, index ) ) for index in selectedIndexes] )] or [self._model.itemFromIndex( index ) for index in selectedIndexes]

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
