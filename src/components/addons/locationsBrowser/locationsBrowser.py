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
***	LocationsBrowser.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Locations Browser Component Module.
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import ui.widgets.messageBox as messageBox
from foundations.environment import Environment
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class LocationsBrowser( UiComponent ):
	'''
	This Class Is The LocationsBrowser Class.
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
		self.deactivatable = True

		self._uiPath = "ui/Locations_Browser.ui"

		self._container = None
		self._settings = None

		self._coreComponentsManagerUi = None
		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None
		self._coreTemplatesOutliner = None
		self._addonsLoaderScript = None

		self._openSetsLocationsAction = None
		self._openComponentLocationAction = None
		self._openTemplateLocationAction = None

		self._Open_Output_Folder_pushButton = None

		self._linuxBrowsers = ( "nautilus", "dolphin", "konqueror", "thunar" )

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	@core.executionTrace
	def uiPath( self ):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self, value ):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiPath" ) )

	@uiPath.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self ):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiPath" ) )

	@property
	@core.executionTrace
	def container( self ):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self, value ):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "container" ) )

	@container.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self ):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "container" ) )

	@property
	@core.executionTrace
	def settings( self ):
		'''
		This Method Is The Property For The _settings Attribute.

		@return: self._settings. ( QSettings )
		'''

		return self._settings

	@settings.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settings( self, value ):
		'''
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "settings" ) )

	@settings.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settings( self ):
		'''
		This Method Is The Deleter Method For The _settings Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "settings" ) )

	@property
	@core.executionTrace
	def coreComponentsManagerUi( self ):
		'''
		This Method Is The Property For The _coreComponentsManagerUi Attribute.

		@return: self._coreComponentsManagerUi. ( Object )
		'''

		return self._coreComponentsManagerUi

	@coreComponentsManagerUi.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreComponentsManagerUi( self, value ):
		'''
		This Method Is The Setter Method For The _coreComponentsManagerUi Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreComponentsManagerUi" ) )

	@coreComponentsManagerUi.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreComponentsManagerUi( self ):
		'''
		This Method Is The Deleter Method For The _coreComponentsManagerUi Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreComponentsManagerUi" ) )

	@property
	@core.executionTrace
	def corePreferencesManager( self ):
		'''
		This Method Is The Property For The _corePreferencesManager Attribute.

		@return: self._corePreferencesManager. ( Object )
		'''

		return self._corePreferencesManager

	@corePreferencesManager.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def corePreferencesManager( self, value ):
		'''
		This Method Is The Setter Method For The _corePreferencesManager Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "corePreferencesManager" ) )

	@corePreferencesManager.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def corePreferencesManager( self ):
		'''
		This Method Is The Deleter Method For The _corePreferencesManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "corePreferencesManager" ) )

	@property
	@core.executionTrace
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self, value ):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDatabaseBrowser" ) )

	@coreDatabaseBrowser.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDatabaseBrowser" ) )

	@property
	@core.executionTrace
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self._coreTemplatesOutliner. ( Object )
		'''

		return self._coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self, value ):
		'''
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreTemplatesOutliner" ) )

	@coreTemplatesOutliner.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreTemplatesOutliner" ) )

	@property
	@core.executionTrace
	def addonsLoaderScript( self ):
		'''
		This Method Is The Property For The _addonsLoaderScript Attribute.

		@return: self._addonsLoaderScript. ( Object )
		'''

		return self._addonsLoaderScript

	@addonsLoaderScript.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def addonsLoaderScript( self, value ):
		'''
		This Method Is The Setter Method For The _addonsLoaderScript Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "addonsLoaderScript" ) )

	@addonsLoaderScript.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def addonsLoaderScript( self ):
		'''
		This Method Is The Deleter Method For The _addonsLoaderScript Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "addonsLoaderScript" ) )

	@property
	@core.executionTrace
	def openSetsLocationsAction( self ):
		'''
		This Method Is The Property For The _openSetsLocationsAction Attribute.

		@return: self._openSetsLocationsAction. ( QAction )
		'''

		return self._openSetsLocationsAction

	@openSetsLocationsAction.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openSetsLocationsAction( self, value ):
		'''
		This Method Is The Setter Method For The _openSetsLocationsAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "openSetsLocationsAction" ) )

	@openSetsLocationsAction.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openSetsLocationsAction( self ):
		'''
		This Method Is The Deleter Method For The _openSetsLocationsAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "openSetsLocationsAction" ) )

	@property
	@core.executionTrace
	def openComponentLocationAction( self ):
		'''
		This Method Is The Property For The _openComponentLocationAction Attribute.

		@return: self._openComponentLocationAction. ( QAction )
		'''

		return self._openComponentLocationAction

	@openComponentLocationAction.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openComponentLocationAction( self, value ):
		'''
		This Method Is The Setter Method For The _openComponentLocationAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "openComponentLocationAction" ) )

	@openComponentLocationAction.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openComponentLocationAction( self ):
		'''
		This Method Is The Deleter Method For The _openComponentLocationAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "openComponentLocationAction" ) )

	@property
	@core.executionTrace
	def openTemplateLocationAction( self ):
		'''
		This Method Is The Property For The _openTemplateLocationAction Attribute.

		@return: self._openTemplateLocationAction. ( QAction )
		'''

		return self._openTemplateLocationAction

	@openTemplateLocationAction.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openTemplateLocationAction( self, value ):
		'''
		This Method Is The Setter Method For The _openTemplateLocationAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "openTemplateLocationAction" ) )

	@openTemplateLocationAction.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openTemplateLocationAction( self ):
		'''
		This Method Is The Deleter Method For The _openTemplateLocationAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "openTemplateLocationAction" ) )

	@property
	@core.executionTrace
	def Open_Output_Folder_pushButton( self ):
		'''
		This Method Is The Property For The _Open_Output_Folder_pushButton Attribute.

		@return: self._Open_Output_Folder_pushButton. ( QPushButton )
		'''

		return self._Open_Output_Folder_pushButton

	@Open_Output_Folder_pushButton.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Open_Output_Folder_pushButton( self, value ):
		'''
		This Method Is The Setter Method For The _Open_Output_Folder_pushButton Attribute.

		@param value: Attribute Value. ( QPushButton )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "Open_Output_Folder_pushButton" ) )

	@Open_Output_Folder_pushButton.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Open_Output_Folder_pushButton( self ):
		'''
		This Method Is The Deleter Method For The _Open_Output_Folder_pushButton Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "Open_Output_Folder_pushButton" ) )

	@property
	@core.executionTrace
	def linuxBrowsers( self ):
		'''
		This Method Is The Property For The _linuxBrowsers Attribute.

		@return: self._linuxBrowsers. ( QObject )
		'''

		return self._linuxBrowsers

	@linuxBrowsers.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def linuxBrowsers( self, value ):
		'''
		This Method Is The Setter Method For The _linuxBrowsers Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "linuxBrowsers" ) )

	@linuxBrowsers.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def linuxBrowsers( self ):
		'''
		This Method Is The Deleter Method For The _linuxBrowsers Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "linuxBrowsers" ) )

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
		self._container = container
		self._settings = self._container.settings

		self._coreComponentsManagerUi = self._container.componentsManager.components["core.componentsManagerUi"].interface
		self._corePreferencesManager = self._container.componentsManager.components["core.preferencesManager"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface
		self._coreTemplatesOutliner = self._container.componentsManager.components["core.templatesOutliner"].interface
		self._addonsLoaderScript = self._container.componentsManager.components["addons.loaderScript"].interface

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug( "> Deactivating '{0}' Component.".format( self.__class__.__name__ ) )

		self.uiFile = None
		self._container = None
		self._settings = None

		self._coreComponentsManagerUi = None
		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None
		self._coreTemplatesOutliner = None
		self._addonsLoaderScript = None

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )


		self.Custom_File_Browser_Path_lineEdit_setUi()

		self.addActions_()

		# Signals / Slots.
		self.ui.Custom_File_Browser_Path_toolButton.connect( self.ui.Custom_File_Browser_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_File_Browser_Path_toolButton_OnClicked )
		self.ui.Custom_File_Browser_Path_lineEdit.connect( self.ui.Custom_File_Browser_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_File_Browser_Path_lineEdit_OnEditFinished )

		# LoaderScript Addon Component Specific Code.
		if self._addonsLoaderScript.activated :
			self._Open_Output_Folder_pushButton = QPushButton( "Open Output Folder" )
			self._addonsLoaderScript.ui.Loader_Script_verticalLayout.addWidget( self._Open_Output_Folder_pushButton )

			# Signals / Slots.
			self._Open_Output_Folder_pushButton.connect( self._Open_Output_Folder_pushButton, SIGNAL( "clicked()" ), self.Open_Output_Folder_pushButton_OnClicked )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		# Signals / Slots.
		self.ui.Custom_File_Browser_Path_toolButton.disconnect( self.ui.Custom_File_Browser_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_File_Browser_Path_toolButton_OnClicked )
		self.ui.Custom_File_Browser_Path_lineEdit.disconnect( self.ui.Custom_File_Browser_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_File_Browser_Path_lineEdit_OnEditFinished )

		# LoaderScript Addon Component Specific Code.
		if self._addonsLoaderScript.activated :
			self._Open_Output_Folder_pushButton.setParent( None )
			self._Open_Output_Folder_pushButton = None

			# Signals / Slots.
			self._Open_Output_Folder_pushButton.disconnect( self._Open_Output_Folder_pushButton, SIGNAL( "clicked()" ), self.Open_Output_Folder_pushButton_OnClicked )

		self.removeActions_()

	@core.executionTrace
	def addWidget( self ):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug( "> Adding '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget( self.ui.Custom_File_Browser_Path_groupBox )

	@core.executionTrace
	def removeWidget( self ):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug( "> Removing '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self.ui.Custom_File_Browser_Path_groupBox.setParent( None )

	@core.executionTrace
	def addActions_( self ):
		'''
		This Method Adds Actions.
		'''

		self._openSetsLocationsAction = QAction( "Open Set(s) Location(s) ...", self._coreDatabaseBrowser.ui.Database_Browser_listWidget )
		self._openSetsLocationsAction.triggered.connect( self.Database_Browser_listWidget_openSetsLocationsAction )
		self._coreDatabaseBrowser.ui.Database_Browser_listWidget.addAction( self._openSetsLocationsAction )

		self._openComponentLocationAction = QAction( "Open Component Location ...", self._coreComponentsManagerUi.ui.Components_Manager_Ui_treeWidget )
		self._openComponentLocationAction.triggered.connect( self.Components_Manager_Ui_treeWidget_openComponentLocationAction )
		self._coreComponentsManagerUi.ui.Components_Manager_Ui_treeWidget.addAction( self._openComponentLocationAction )

		self._openTemplateLocationAction = QAction( "Open Template Location ...", self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget )
		self._openTemplateLocationAction.triggered.connect( self.Templates_Outliner_treeWidget_openTemplateLocationAction )
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget.addAction( self._openTemplateLocationAction )

	@core.executionTrace
	def removeActions_( self ):
		'''
		This Method Removes Actions.
		'''

		self._coreDatabaseBrowser.ui.Database_Browser_listWidget.removeAction( self._openSetsLocationsAction )
		self._coreComponentsManagerUi.ui.Components_Manager_Ui_treeWidget.removeAction( self._openComponentLocationAction )
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget.removeAction( self._openTemplateLocationAction )

		self._openSetsLocationsAction = None
		self._openComponentLocationAction = None
		self._openTemplateLocationAction = None

	@core.executionTrace
	def Database_Browser_listWidget_openSetsLocationsAction( self, checked ):
		'''
		This Method Is Triggered By openSetsLocationsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedSets = self._coreDatabaseBrowser.ui.Database_Browser_listWidget.selectedItems()
		for set in selectedSets :
			setPath = set._datas.path
			setPath = setPath and os.path.exists( setPath ) and os.path.dirname( setPath )
			setPath and self.exploreProvidedFolder( setPath )

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_openComponentLocationAction( self, checked ):
		'''
		This Method Is Triggered By openComponentLocationAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedComponent = self._coreComponentsManagerUi.ui.Components_Manager_Ui_treeWidget.selectedItems()
		for component in selectedComponent :
			hasattr( component, "_datas" ) and os.path.exists( component._datas.path ) and self.exploreProvidedFolder( component._datas.path )

	@core.executionTrace
	def Templates_Outliner_treeWidget_openTemplateLocationAction( self, checked ):
		'''
		This Method Is Triggered By openTemplateLocationAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedTemplate = self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget.selectedItems()
		selectedTemplate = selectedTemplate and selectedTemplate[0] or None
		selectedTemplate and hasattr( selectedTemplate, "_datas" ) and type( selectedTemplate._datas ) == dbUtilities.types.DbTemplate and os.path.exists( selectedTemplate._datas.path ) and self.exploreProvidedFolder( selectedTemplate._datas.path )

	@core.executionTrace
	def Custom_File_Browser_Path_lineEdit_setUi( self ) :
		'''
		This Method Fills The Custom_File_Browser_Path_lineEdit.
		'''

		customTextEditor = self._settings.getKey( "Others", "CustomFileBrowser" )
		LOGGER.debug( "> Setting '{0}' With Value '{1}'.".format( "Custom_File_Browser_Path_lineEdit", customTextEditor.toString() ) )
		self.ui.Custom_File_Browser_Path_lineEdit.setText( customTextEditor.toString() )

	@core.executionTrace
	def Custom_File_Browser_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Custom_File_Browser_Path_toolButton Is Clicked.
		'''

		customTextEditorExecutable = self._container.storeLastBrowsedPath( QFileDialog.getOpenFileName( self, self.tr( "Custom File Browser Executable :" ), self._container.lastBrowsedPath ) )
		if customTextEditorExecutable != "":
			LOGGER.debug( "> Chosen Custom File Browser Executable : '{0}'.".format( customTextEditorExecutable ) )
			self.ui.Custom_File_Browser_Path_lineEdit.setText( QString( customTextEditorExecutable ) )
			self._settings.setKey( "Others", "CustomFileBrowser", self.ui.Custom_File_Browser_Path_lineEdit.text() )

	@core.executionTrace
	def Custom_File_Browser_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When Custom_File_Browser_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.ui.Custom_File_Browser_Path_lineEdit.text() ) ) ) and str( self.ui.Custom_File_Browser_Path_lineEdit.text() ) != "":
			LOGGER.debug( "> Restoring Preferences !" )
			self.Custom_File_Browser_Path_lineEdit_setUi()

			messageBox.messageBox( "Error", "Error", "{0} | Invalid Custom File Browser Executable File !".format( self.__class__.__name__ ) )
		else :
			self._settings.setKey( "Others", "CustomFileBrowser", self.ui.Custom_File_Browser_Path_lineEdit.text() )

	@core.executionTrace
	def Open_Output_Folder_pushButton_OnClicked( self ) :
		'''
		This Method Is Called When Open_Output_Folder_pushButton Is Clicked.
		'''

		self.exploreProvidedFolder( os.path.join( self._container.userApplicationDirectory, Constants.ioDirectory ) )

	@core.executionTrace
	def exploreProvidedFolder( self, folder ) :
		'''
		This Method Provides Folder Exploring Capability.

		@param folder: Folder To Explore. ( String )
		'''

		browserCommand = None
		customFileBrowser = str( self.ui.Custom_File_Browser_Path_lineEdit.text() )

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			folder = folder.replace( "/", "\\" )
			if customFileBrowser :
				LOGGER.info( "{0} | Launching '{1}' Custom File Browser With '{2}'.".format( self.__class__.__name__, os.path.basename( customFileBrowser ), folder ) )
				browserCommand = "\"{0}\" \"{1}\"".format( customFileBrowser, folder )
			else:
				LOGGER.info( "{0} | Launching 'explorer.exe' With '{1}'.".format( self.__class__.__name__, folder ) )
				browserCommand = "explorer.exe \"{0}\"".format( folder )

		elif platform.system() == "Darwin" :
			if customFileBrowser :
				LOGGER.info( "{0} | Launching '{1}' Custom File Browser With '{2}'.".format( self.__class__.__name__, os.path.basename( customFileBrowser ), folder ) )
				browserCommand = "open -a \"{0}\" \"{1}\"".format( customFileBrowser, folder )
			else:
				LOGGER.info( "{0} | Launching 'Finder' With '{1}'.".format( self.__class__.__name__, folder ) )
				browserCommand = "open \"{0}\"".format( folder )
		elif platform.system() == "Linux":
			if customFileBrowser :
				LOGGER.info( "{0} | Launching '{1}' Custom File Browser With '{2}'.".format( self.__class__.__name__, os.path.basename( customFileBrowser ), folder ) )
				browserCommand = "\"{0}\" \"{1}\"".format( customFileBrowser, folder )
			else :
				environmentVariable = Environment( "PATH" )
				paths = environmentVariable.getPath().split( ":" )

				browserFound = False
				for browser in self._linuxBrowsers :
					if not browserFound :
						try :
							for path in paths :
								if os.path.exists( os.path.join( path, browser ) ) :
									LOGGER.info( "{0} | Launching '{1}' File Browser With '{2}'.".format( self.__class__.__name__, browser, folder ) )
									browserCommand = "\"{0}\" \"{1}\"".format( browser, folder )
									browserFound = True
									raise StopIteration
						except StopIteration:
							pass
					else :
						break

		if browserCommand :
			LOGGER.debug( "> Current Browser Command : '{0}'.".format( browserCommand ) )
			browserProcess = QProcess()
			browserProcess.startDetached( browserCommand )
		else :
			messageBox.messageBox( "Warning", "Warning", "{0} | Please Define A Browser Executable In The Preferences !".format( self.__class__.__name__ ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
