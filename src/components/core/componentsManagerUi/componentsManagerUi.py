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

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
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
class ComponentsManagerUi( UiComponent ):
	'''
	This Class Is The ComponentsManagerUi Class.
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

		self._uiPath = "ui/Components_Manager_Ui.ui"
		self._uiResources = "resources"
		self._uiActivatedIcon = "Activated.png"
		self._uiDeactivatedIcon = "Deactivated.png"
		self._uiCategorieAffixe = "_Categorie.png"
		self._dockArea = 1

		self._container = None
		self._settings = None

		self._treeWidgetHeaders = [ "Components", "Activated", "Categorie", "Rank", "Version" ]
		self._treeWidgetIndentation = 15
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
	def treeWidgetHeaders( self ):
		'''
		This Method Is The Property For The _treeWidgetHeaders Attribute.

		@return: self._treeWidgetHeaders. ( List )
		'''

		return self._treeWidgetHeaders

	@treeWidgetHeaders.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetHeaders( self, value ):
		'''
		This Method Is The Setter Method For The _treeWidgetHeaders Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "treeWidgetHeaders" ) )

	@treeWidgetHeaders.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetHeaders( self ):
		'''
		This Method Is The Deleter Method For The _treeWidgetHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "treeWidgetHeaders" ) )

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

		self.ui.Components_Manager_Ui_treeWidget.setContextMenuPolicy( Qt.ActionsContextMenu )
		self.Components_Manager_Ui_treeWidget_setActions()

		self.Components_Manager_Ui_treeWidget_setUi()

		self.ui.Components_Informations_textBrowser.setText( self._Components_Informations_textBrowser_defaultText )

		self.ui.Components_Manager_Ui_splitter.setSizes( [ 16777215, 1 ] )

		# Signals / Slots.
		self.ui.Components_Manager_Ui_treeWidget.connect( self.ui.Components_Manager_Ui_treeWidget, SIGNAL( "itemSelectionChanged()" ), self.Components_Manager_Ui_treeWidget_OnItemSelectionChanged )

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
	def Components_Manager_Ui_treeWidget_setUi( self ):
		'''
		This Method Sets The Components_Manager_Ui_treeWidget.
		'''

		LOGGER.debug( " > Refreshing '{0}' Ui !".format( self.__class__.__name__ ) )

		self.ui.Components_Manager_Ui_treeWidget.clear()
		self.ui.Components_Manager_Ui_treeWidget.setSelectionMode( QAbstractItemView.ExtendedSelection )
		self.ui.Components_Manager_Ui_treeWidget.setColumnCount( len( self._treeWidgetHeaders ) )
		self.ui.Components_Manager_Ui_treeWidget.setHeaderLabels( QStringList( self._treeWidgetHeaders ) )
		self.ui.Components_Manager_Ui_treeWidget.setIndentation( self._treeWidgetIndentation )
		self.ui.Components_Manager_Ui_treeWidget.setSortingEnabled( True )

		for path in self._container.componentsManager.paths :
			pathTreeWidgetItem = QTreeWidgetItem()
			pathTreeWidgetItem.setText( 0, path )
			pathTreeWidgetItem.setTextAlignment( 1, Qt.AlignCenter )

			LOGGER.debug( " > Adding '{0}' Path To 'Components_Manager_Ui_treeWidget'.".format( path ) )
			self.ui.Components_Manager_Ui_treeWidget.addTopLevelItem( pathTreeWidgetItem )

			pathTreeWidgetItem.setExpanded( True )

			for component in self._container.componentsManager.components :
				if os.path.normpath( self._container.componentsManager.paths[path] ) in os.path.normpath( self._container.componentsManager.components[component].path ):
					componentTreeWidgetItem = QTreeWidgetItem( pathTreeWidgetItem )

					componentTreeWidgetItem.setText( 0, strings.getNiceName( self._container.componentsManager.components[component].module ) )
					iconPath = os.path.join( self._uiResources, "{0}{1}".format( strings.getNiceName( self._container.componentsManager.components[component].categorie ), self._uiCategorieAffixe ) )
					os.path.exists( iconPath ) and	componentTreeWidgetItem.setIcon( 0, QIcon( iconPath ) )

					componentTreeWidgetItem.setText( 1, str( self._container.componentsManager.components[component].interface.activated ) )
					icon = self._container.componentsManager.components[component].interface.activated and QIcon( os.path.join( self._uiResources, self._uiActivatedIcon ) ) or QIcon( os.path.join( self._uiResources, self._uiDeactivatedIcon ) )
					componentTreeWidgetItem.setIcon( 1, icon )

					componentTreeWidgetItem.setText( 2, self._container.componentsManager.components[component].categorie and strings.getNiceName( self._container.componentsManager.components[component].categorie ) or "" )
					componentTreeWidgetItem.setTextAlignment( 2, Qt.AlignCenter )

					componentTreeWidgetItem.setText( 3, self._container.componentsManager.components[component].rank or "" )
					componentTreeWidgetItem.setTextAlignment( 3, Qt.AlignCenter )

					componentTreeWidgetItem.setText( 4, self._container.componentsManager.components[component].version or "" )
					componentTreeWidgetItem.setTextAlignment( 3, Qt.AlignCenter )

					componentTreeWidgetItem._datas = self._container.componentsManager.components[component]

					LOGGER.debug( " > Adding '{0}' Component To 'Components_Manager_Ui_treeWidget'.".format( component ) )
					self.ui.Components_Manager_Ui_treeWidget.addTopLevelItem( componentTreeWidgetItem )

			for column in range( len( self._treeWidgetHeaders ) ) :
				self.ui.Components_Manager_Ui_treeWidget.resizeColumnToContents( column )

			self.ui.Components_Manager_Ui_treeWidget.sortItems( 0, Qt.AscendingOrder )

	@core.executionTrace
	def refreshUi( self ):
		'''
		This Method Refreshes The _Collections_Outliner_treeWidget.
		'''

		self.Collections_Outliner_treeWidget_setUi()

	@core.executionTrace
	def onStartup( self ):
		'''
		This Method Is Called On Framework Startup.
		'''

		self.Components_Manager_Ui_treeWidget_refreshActivationsStatus()

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_refreshActivationsStatus( self ):
		'''
		This Method Refreshes The Components_Manager_Ui_treeWidget Activations Status.
		'''

		for treeWidgetItem in self.ui.Components_Manager_Ui_treeWidget.findItems( ".*", Qt.MatchRegExp | Qt.MatchRecursive, 0 ) :
			if hasattr( treeWidgetItem, "_datas" ) :
				treeWidgetItem.setText( 1, str( treeWidgetItem._datas.interface.activated ) )
				icon = treeWidgetItem._datas.interface.activated and QIcon( os.path.join( self._uiResources, self._uiActivatedIcon ) ) or QIcon( os.path.join( self._uiResources, self._uiDeactivatedIcon ) )
				treeWidgetItem.setIcon( 1, icon )

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_setActions( self ):
		'''
		This Method Sets The Components_Manager_Ui_treeWidget Actions.
		'''

		activateComponentAction = QAction( "Activate Component", self.ui.Components_Manager_Ui_treeWidget )
		activateComponentAction.triggered.connect( self.Components_Manager_Ui_treeWidget_activateComponentAction )
		self.ui.Components_Manager_Ui_treeWidget.addAction( activateComponentAction )

		deactivateComponentAction = QAction( "Deactivate Component", self.ui.Components_Manager_Ui_treeWidget )
		deactivateComponentAction.triggered.connect( self.Components_Manager_Ui_treeWidget_deactivateComponentAction )
		self.ui.Components_Manager_Ui_treeWidget.addAction( deactivateComponentAction )

		separatorAction = QAction( self.ui.Components_Manager_Ui_treeWidget )
		separatorAction.setSeparator( True )
		self.ui.Components_Manager_Ui_treeWidget.addAction( separatorAction )

		reloadComponentAction = QAction( "Reload Component", self.ui.Components_Manager_Ui_treeWidget )
		reloadComponentAction.triggered.connect( self.Components_Manager_Ui_treeWidget_reloadComponentAction )
		self.ui.Components_Manager_Ui_treeWidget.addAction( reloadComponentAction )

		separatorAction = QAction( self.ui.Components_Manager_Ui_treeWidget )
		separatorAction.setSeparator( True )
		self.ui.Components_Manager_Ui_treeWidget.addAction( separatorAction )

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_activateComponentAction( self, checked ):
		'''
		This Method Is Triggered By activateComponentAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedComponents = self.ui.Components_Manager_Ui_treeWidget.selectedItems()
		for component in selectedComponents :
			if component and hasattr( component, "_datas" ) :
				if not component._datas.interface.activated :
					self.activateComponent( component )
				else :
					messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Component Is Already Activated !".format( self.__class__.__name__, component._datas.name ) )

		selectedComponents and self.Components_Manager_Ui_treeWidget_refreshActivationsStatus()
		selectedComponents and self.storeDeactivatedComponents()

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_deactivateComponentAction( self, checked ):
		'''
		This Method Is Triggered By deactivateComponentAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedComponents = self.ui.Components_Manager_Ui_treeWidget.selectedItems()
		for component in selectedComponents :
			if component and hasattr( component, "_datas" ) :
				if component._datas.interface.activated :
					if component._datas.interface.deactivatable :
						self.deactivateComponent( component )
					else :
						messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Component Cannot Be Deactivated !".format( self.__class__.__name__, component._datas.name ) )
				else :
					messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Component Is Already Deactivated !".format( self.__class__.__name__, component._datas.name ) )

		selectedComponents and self.Components_Manager_Ui_treeWidget_refreshActivationsStatus()
		selectedComponents and self.storeDeactivatedComponents()

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_reloadComponentAction( self, checked ):
		'''
		This Method Is Triggered By reloadComponentAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedComponents = self.ui.Components_Manager_Ui_treeWidget.selectedItems()
		for component in selectedComponents :
			if component and hasattr( component, "_datas" ) :
				if component._datas.interface.deactivatable :
					if component._datas.interface.activated :
						self.deactivateComponent( component )
					self._container.componentsManager.reloadComponent( component._datas.name )
					if not component._datas.interface.activated :
						self.activateComponent( component )
				else :
					messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Component Cannot Be Reloaded !".format( self.__class__.__name__, component._datas.name ) )
		selectedComponents and self.Components_Manager_Ui_treeWidget_refreshActivationsStatus()

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_OnItemSelectionChanged( self ):
		'''
		This Method Sets The Additional_Informations_textEdit Widget.
		'''

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

		selectedComponents = self.ui.Components_Manager_Ui_treeWidget.selectedItems()
		for component in selectedComponents :
			if component and hasattr( component, "_datas" ) :
				content.append( subContent.format( component._datas.name,
												strings.getNiceName( component._datas.categorie ),
												component._datas.author,
												component._datas.email,
												component._datas.url,
												component._datas.description
												) )
			else:
				len( selectedComponents ) == 1 and content.append( self._Components_Informations_textBrowser_defaultText )

		separator = len( content ) == 1 and "" or "<p><center>* * *<center/></p>"
		self.ui.Components_Informations_textBrowser.setText( separator.join( content ) )

	@core.executionTrace
	def activateComponent( self, component ):
		'''
		This Method Activates The Provided Component.
		'''

		component._datas.interface.activate( self._container )
		if component._datas.categorie == "default" :
			component._datas.interface.initialize()
		elif component._datas.categorie == "ui" :
			component._datas.interface.addWidget()
			component._datas.interface.initializeUi()

	@core.executionTrace
	def deactivateComponent( self, component ):
		'''
		This Method Deactivates The Provided Component.
		'''

		if component._datas.categorie == "default" :
			component._datas.interface.uninitialize()
		elif component._datas.categorie == "ui" :
			component._datas.interface.uninitializeUi()
			component._datas.interface.removeWidget()
		component._datas.interface.deactivate()

	@core.executionTrace
	def storeDeactivatedComponents( self ):
		'''
		This Method Stores Deactivated Components In The Settings File.
		'''

		deactivatedComponents = []
		for component in self.ui.Components_Manager_Ui_treeWidget.findItems( ".*", Qt.MatchRegExp | Qt.MatchRecursive, 0 ) :
			if component and hasattr( component, "_datas" ) :
				component._datas.interface.activated or deactivatedComponents.append( component._datas.name )
		self._settings.setKey( "Settings", "deactivatedComponents", ",".join( deactivatedComponents ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
