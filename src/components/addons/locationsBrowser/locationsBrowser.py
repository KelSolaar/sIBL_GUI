#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - kelsolaar_fool@hotmail.com
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
import foundations.strings as strings
import ui.common
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
		self._signalsSlotsCenter = None
		self._settings = None
		self._settingsSection = None

		self._coreComponentsManagerUi = None
		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None
		self._coreTemplatesOutliner = None
		self._addonsLoaderScript = None

		self._openIblSetsLocationsAction = None
		self._openComponentsLocationsAction = None
		self._openTemplatesLocationsAction = None

		self._Open_Output_Folder_pushButton = None

		self._linuxBrowsers = ( "nautilus", "dolphin", "konqueror", "thunar" )

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
	def coreComponentsManagerUi( self ):
		'''
		This Method Is The Property For The _coreComponentsManagerUi Attribute.

		@return: self._coreComponentsManagerUi. ( Object )
		'''

		return self._coreComponentsManagerUi

	@coreComponentsManagerUi.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreComponentsManagerUi( self, value ):
		'''
		This Method Is The Setter Method For The _coreComponentsManagerUi Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreComponentsManagerUi" ) )

	@coreComponentsManagerUi.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreComponentsManagerUi( self ):
		'''
		This Method Is The Deleter Method For The _coreComponentsManagerUi Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreComponentsManagerUi" ) )

	@property
	def corePreferencesManager( self ):
		'''
		This Method Is The Property For The _corePreferencesManager Attribute.

		@return: self._corePreferencesManager. ( Object )
		'''

		return self._corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def corePreferencesManager( self, value ):
		'''
		This Method Is The Setter Method For The _corePreferencesManager Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "corePreferencesManager" ) )

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def corePreferencesManager( self ):
		'''
		This Method Is The Deleter Method For The _corePreferencesManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "corePreferencesManager" ) )

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

	@property
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self._coreTemplatesOutliner. ( Object )
		'''

		return self._coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self, value ):
		'''
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreTemplatesOutliner" ) )

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreTemplatesOutliner" ) )

	@property
	def addonsLoaderScript( self ):
		'''
		This Method Is The Property For The _addonsLoaderScript Attribute.

		@return: self._addonsLoaderScript. ( Object )
		'''

		return self._addonsLoaderScript

	@addonsLoaderScript.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def addonsLoaderScript( self, value ):
		'''
		This Method Is The Setter Method For The _addonsLoaderScript Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "addonsLoaderScript" ) )

	@addonsLoaderScript.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def addonsLoaderScript( self ):
		'''
		This Method Is The Deleter Method For The _addonsLoaderScript Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "addonsLoaderScript" ) )

	@property
	def openIblSetsLocationsAction( self ):
		'''
		This Method Is The Property For The _openIblSetsLocationsAction Attribute.

		@return: self._openIblSetsLocationsAction. ( QAction )
		'''

		return self._openIblSetsLocationsAction

	@openIblSetsLocationsAction.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openIblSetsLocationsAction( self, value ):
		'''
		This Method Is The Setter Method For The _openIblSetsLocationsAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "openIblSetsLocationsAction" ) )

	@openIblSetsLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openIblSetsLocationsAction( self ):
		'''
		This Method Is The Deleter Method For The _openIblSetsLocationsAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "openIblSetsLocationsAction" ) )

	@property
	def openComponentsLocationsAction( self ):
		'''
		This Method Is The Property For The _openComponentsLocationsAction Attribute.

		@return: self._openComponentsLocationsAction. ( QAction )
		'''

		return self._openComponentsLocationsAction

	@openComponentsLocationsAction.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openComponentsLocationsAction( self, value ):
		'''
		This Method Is The Setter Method For The _openComponentsLocationsAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "openComponentsLocationsAction" ) )

	@openComponentsLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openComponentsLocationsAction( self ):
		'''
		This Method Is The Deleter Method For The _openComponentsLocationsAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "openComponentsLocationsAction" ) )

	@property
	def openTemplatesLocationsAction( self ):
		'''
		This Method Is The Property For The _openTemplatesLocationsAction Attribute.

		@return: self._openTemplatesLocationsAction. ( QAction )
		'''

		return self._openTemplatesLocationsAction

	@openTemplatesLocationsAction.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openTemplatesLocationsAction( self, value ):
		'''
		This Method Is The Setter Method For The _openTemplatesLocationsAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "openTemplatesLocationsAction" ) )

	@openTemplatesLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def openTemplatesLocationsAction( self ):
		'''
		This Method Is The Deleter Method For The _openTemplatesLocationsAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "openTemplatesLocationsAction" ) )

	@property
	def Open_Output_Folder_pushButton( self ):
		'''
		This Method Is The Property For The _Open_Output_Folder_pushButton Attribute.

		@return: self._Open_Output_Folder_pushButton. ( QPushButton )
		'''

		return self._Open_Output_Folder_pushButton

	@Open_Output_Folder_pushButton.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Open_Output_Folder_pushButton( self, value ):
		'''
		This Method Is The Setter Method For The _Open_Output_Folder_pushButton Attribute.

		@param value: Attribute Value. ( QPushButton )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "Open_Output_Folder_pushButton" ) )

	@Open_Output_Folder_pushButton.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Open_Output_Folder_pushButton( self ):
		'''
		This Method Is The Deleter Method For The _Open_Output_Folder_pushButton Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "Open_Output_Folder_pushButton" ) )

	@property
	def linuxBrowsers( self ):
		'''
		This Method Is The Property For The _linuxBrowsers Attribute.

		@return: self._linuxBrowsers. ( QObject )
		'''

		return self._linuxBrowsers

	@linuxBrowsers.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def linuxBrowsers( self, value ):
		'''
		This Method Is The Setter Method For The _linuxBrowsers Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "linuxBrowsers" ) )

	@linuxBrowsers.deleter
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
		self._signalsSlotsCenter = QObject()
		self._settings = self._container.settings
		self._settingsSection = self.name

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
		self._signalsSlotsCenter = None
		self._settings = None
		self._settingsSection = None

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
		self._signalsSlotsCenter.connect( self.ui.Custom_File_Browser_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_File_Browser_Path_toolButton_OnClicked )
		self._signalsSlotsCenter.connect( self.ui.Custom_File_Browser_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_File_Browser_Path_lineEdit_OnEditFinished )

		# LoaderScript Addon Component Specific Code.
		if self._addonsLoaderScript.activated :
			self._Open_Output_Folder_pushButton = QPushButton( "Open Output Folder" )
			self._addonsLoaderScript.ui.Loader_Script_verticalLayout.addWidget( self._Open_Output_Folder_pushButton )

			# Signals / Slots.
			self._signalsSlotsCenter.connect( self._Open_Output_Folder_pushButton, SIGNAL( "clicked()" ), self.Open_Output_Folder_pushButton_OnClicked )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		# Signals / Slots.
		self._signalsSlotsCenter.disconnect( self.ui.Custom_File_Browser_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_File_Browser_Path_toolButton_OnClicked )
		self._signalsSlotsCenter.disconnect( self.ui.Custom_File_Browser_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_File_Browser_Path_lineEdit_OnEditFinished )

		# LoaderScript Addon Component Specific Code.
		if self._addonsLoaderScript.activated :
			# Signals / Slots.
			self._signalsSlotsCenter.disconnect( self._Open_Output_Folder_pushButton, SIGNAL( "clicked()" ), self.Open_Output_Folder_pushButton_OnClicked )

			self._Open_Output_Folder_pushButton.setParent( None )
			self._Open_Output_Folder_pushButton = None

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

		LOGGER.debug( "> Adding '{0}' Component Actions.".format( self.__class__.__name__ ) )

		self._openIblSetsLocationsAction = QAction( "Open Ibl Set(s) Location(s) ...", self._coreDatabaseBrowser.ui.Database_Browser_listView )
		self._openIblSetsLocationsAction.triggered.connect( self.Database_Browser_listView_openIblSetsLocationsAction )
		self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction( self._openIblSetsLocationsAction )

		self._openComponentsLocationsAction = QAction( "Open Component(s) Location(s) ...", self._coreComponentsManagerUi.ui.Components_Manager_Ui_treeView )
		self._openComponentsLocationsAction.triggered.connect( self.Components_Manager_Ui_treeView_openComponentsLocationsAction )
		self._coreComponentsManagerUi.ui.Components_Manager_Ui_treeView.addAction( self._openComponentsLocationsAction )

		self._openTemplatesLocationsAction = QAction( "Open Template(s) Location(s) ...", self._coreTemplatesOutliner.ui.Templates_Outliner_treeView )
		self._openTemplatesLocationsAction.triggered.connect( self.Templates_Outliner_treeView_openTemplatesLocationsAction )
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeView.addAction( self._openTemplatesLocationsAction )

	@core.executionTrace
	def removeActions_( self ):
		'''
		This Method Removes Actions.
		'''

		LOGGER.debug( "> Removing '{0}' Component Actions.".format( self.__class__.__name__ ) )

		self._coreDatabaseBrowser.ui.Database_Browser_listView.removeAction( self._openIblSetsLocationsAction )
		self._coreComponentsManagerUi.ui.Components_Manager_Ui_treeView.removeAction( self._openComponentsLocationsAction )
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeView.removeAction( self._openTemplatesLocationsAction )

		self._openIblSetsLocationsAction = None
		self._openComponentsLocationsAction = None
		self._openTemplatesLocationsAction = None

	@core.executionTrace
	def Database_Browser_listView_openIblSetsLocationsAction( self, checked ):
		'''
		This Method Is Triggered By openIblSetsLocationsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedIblSets = self._coreDatabaseBrowser.getSelectedItems()
		for iblSet in selectedIblSets :
			iblSetPath = iblSet._datas.path
			iblSetPath = iblSetPath and os.path.exists( iblSetPath ) and os.path.dirname( iblSetPath )
			iblSetPath and self.exploreProvidedFolder( iblSetPath )

	@core.executionTrace
	def Components_Manager_Ui_treeView_openComponentsLocationsAction( self, checked ):
		'''
		This Method Is Triggered By openComponentsLocationsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedComponent = self._coreComponentsManagerUi.getSelectedItems()
		for component in selectedComponent :
			hasattr( component, "_datas" ) and os.path.exists( component._datas.path ) and self.exploreProvidedFolder( component._datas.path )

	@core.executionTrace
	def Templates_Outliner_treeView_openTemplatesLocationsAction( self, checked ):
		'''
		This Method Is Triggered By openTemplatesLocationsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedTemplates = self._coreTemplatesOutliner.getSelectedTemplates()
		if selectedTemplates :
			for template in selectedTemplates :
				os.path.exists( template._datas.path ) and self.exploreProvidedFolder( os.path.dirname( template._datas.path ) )

	@core.executionTrace
	def Custom_File_Browser_Path_lineEdit_setUi( self ) :
		'''
		This Method Fills The Custom_File_Browser_Path_lineEdit.
		'''

		customTextEditor = self._settings.getKey( self._settingsSection, "customFileBrowser" )
		LOGGER.debug( "> Setting '{0}' With Value '{1}'.".format( "Custom_File_Browser_Path_lineEdit", customTextEditor.toString() ) )
		self.ui.Custom_File_Browser_Path_lineEdit.setText( customTextEditor.toString() )

	@core.executionTrace
	def Custom_File_Browser_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Custom_File_Browser_Path_toolButton Is Clicked.
		'''

		customTextEditorExecutable = self._container.storeLastBrowsedPath( QFileDialog.getOpenFileName( self, "Custom File Browser Executable :", self._container.lastBrowsedPath ) )
		if customTextEditorExecutable != "":
			LOGGER.debug( "> Chosen Custom File Browser Executable : '{0}'.".format( customTextEditorExecutable ) )
			self.ui.Custom_File_Browser_Path_lineEdit.setText( QString( customTextEditorExecutable ) )
			self._settings.setKey( self._settingsSection, "customFileBrowser", self.ui.Custom_File_Browser_Path_lineEdit.text() )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError )
	def Custom_File_Browser_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When Custom_File_Browser_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.ui.Custom_File_Browser_Path_lineEdit.text() ) ) ) and str( self.ui.Custom_File_Browser_Path_lineEdit.text() ) != "":
			LOGGER.debug( "> Restoring Preferences !" )
			self.Custom_File_Browser_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid Custom File Browser Executable File !".format( self.__class__.__name__ )
		else :
			self._settings.setKey( self._settingsSection, "customFileBrowser", self.ui.Custom_File_Browser_Path_lineEdit.text() )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( ui.common.uiBasicExceptionHandler, False, OSError )
	def Open_Output_Folder_pushButton_OnClicked( self ) :
		'''
		This Method Is Called When Open_Output_Folder_pushButton Is Clicked.
		'''

		if self._container.parameters.loaderScriptsOutputDirectory :
			if os.path.exists( self._container.parameters.loaderScriptsOutputDirectory ) :
				self.exploreProvidedFolder( self._container.parameters.loaderScriptsOutputDirectory )
			else :
				raise OSError, "{0} | '{1}' Loader Script Output Directory Doesn't Exists !".format( self.__class__.__name__, self._container.parameters.loaderScriptsOutputDirectory )
		else :
			self.exploreProvidedFolder( self._addonsLoaderScript.ioDirectory )

	@core.executionTrace
	def exploreProvidedFolder( self, folder ) :
		'''
		This Method Provides Folder Exploring Capability.

		@param folder: Folder To Explore. ( String )
		'''

		browserCommand = None
		customFileBrowser = str( self.ui.Custom_File_Browser_Path_lineEdit.text() )

		folder = os.path.normpath( folder )
		if platform.system() == "Windows" or platform.system() == "Microsoft":
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
