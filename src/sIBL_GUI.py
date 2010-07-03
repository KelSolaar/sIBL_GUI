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
***	sIBL_GUI.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL_GUI Framework Module.
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
import inspect
import logging
import os
import optparse
import platform
import sys
import time
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import ui.common
import ui.widgets.messageBox as messageBox
from ui.widgets.active_QLabel import Active_QLabel
from ui.widgets.delayed_QSplashScreen import Delayed_QSplashScreen
from foundations.environment import Environment
from foundations.streamObject import StreamObject
from globals.constants import Constants
from globals.runtimeConstants import RuntimeConstants
from globals.uiConstants import UiConstants
from manager.manager import Manager

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

# Starting The Console Handler.
if not hasattr( sys, "frozen" ) and not ( platform.system() == "Windows" or platform.system() == "Microsoft" ) :
	RuntimeConstants.loggingConsoleHandler = logging.StreamHandler( sys.__stdout__ )
	RuntimeConstants.loggingConsoleHandler.setFormatter( core.LOGGING_FORMATTER )
	LOGGER.addHandler( RuntimeConstants.loggingConsoleHandler )

RuntimeConstants.uiFile = os.path.join( os.getcwd(), UiConstants.frameworkUiFile )
if os.path.exists( RuntimeConstants.uiFile ):
	Ui_Setup, Ui_Type = uic.loadUiType( RuntimeConstants.uiFile )
else :
	ui.common.uiStandaloneSystemExitExceptionHandler( OSError( "'{0}' Ui File Is Not Available, {1} Will Now Close !".format( UiConstants.frameworkUiFile, Constants.applicationName ) ), Constants.applicationName )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Preferences():
	'''
	This Class Is The Preferences Class.
	'''

	@core.executionTrace
	def __init__( self, preferencesFile = None ):
		'''
		This Method Initializes The Class.

		@param preferencesFile: Current Preferences File Path. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		# --- Setting Class Attributes. ---
		self._preferencesFile = None
		self._preferencesFile = preferencesFile

		self._settings = QSettings( self.preferencesFile, QSettings.IniFormat )

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def preferencesFile( self ):
		'''
		This Method Is The Property For The _preferencesFile Attribute.

		@return: self._preferencesFile. ( String )
		'''

		return self._preferencesFile

	@preferencesFile.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def preferencesFile( self, value ):
		'''
		This Method Is The Setter Method For The _preferencesFile Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type( value ) in ( str, unicode ), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format( "preferencesFile", value )
			assert os.path.exists( value ), "'{0}' Attribute : '{1}' File Doesn't Exists !".format( "preferencesFile", value )
		self._preferencesFile = value

	@preferencesFile.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def preferencesFile( self ):
		'''
		This Method Is The Deleter Method For The _preferencesFile Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "preferencesFile" ) )

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

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def setDefaultPreferences( self ) :
		'''
		This Method Defines The Default Settings File Content.
		'''

		LOGGER.debug( "> Initializing Default Settings !" )

		LOGGER.debug( "> Accessing '{0}' Layouts Settings File !".format( UiConstants.frameworkLayoutsFile ) )

		layoutSettings = QSettings( os.path.join( os.getcwd(), UiConstants.frameworkLayoutsFile ), QSettings.IniFormat )

		self._settings.beginGroup( "Settings" )
		self._settings.setValue( "verbosityLevel", QVariant( "3" ) )
		self._settings.setValue( "restoreGeometryOnLayoutChange", Qt.Unchecked )
		self._settings.setValue( "deactivatedComponents", QVariant( "" ) )
		self._settings.endGroup()
		self._settings.beginGroup( "Layouts" )
		self._settings.setValue( "startupCentric_geometry", layoutSettings.value( "startupCentric/geometry" ) )
		self._settings.setValue( "startupCentric_windowState", layoutSettings.value( "startupCentric/windowState" ) )
		self._settings.setValue( "startupCentric_centralWidget", layoutSettings.value( "startupCentric/centralWidget" ) )
		self._settings.setValue( "startupCentric_activeLabel", layoutSettings.value( "startupCentric/activeLabel" ) )
		self._settings.setValue( "setsCentric_geometry", layoutSettings.value( "setsCentric/geometry" ) )
		self._settings.setValue( "setsCentric_windowState", layoutSettings.value( "setsCentric/windowState" ) )
		self._settings.setValue( "setsCentric_centralWidget", layoutSettings.value( "setsCentric/centralWidget" ) )
		self._settings.setValue( "setsCentric_activeLabel", layoutSettings.value( "setsCentric/activeLabel" ) )
		self._settings.setValue( "templatesCentric_geometry", layoutSettings.value( "templatesCentric/geometry" ) )
		self._settings.setValue( "templatesCentric_windowState", layoutSettings.value( "templatesCentric/windowState" ) )
		self._settings.setValue( "templatesCentric_centralWidget", layoutSettings.value( "templatesCentric/centralWidget" ) )
		self._settings.setValue( "templatesCentric_activeLabel", layoutSettings.value( "templatesCentric/activeLabel" ) )
		self._settings.setValue( "preferencesCentric_geometry", layoutSettings.value( "preferencesCentric/geometry" ) )
		self._settings.setValue( "preferencesCentric_windowState", layoutSettings.value( "preferencesCentric/windowState" ) )
		self._settings.setValue( "preferencesCentric_centralWidget", layoutSettings.value( "preferencesCentric/centralWidget" ) )
		self._settings.setValue( "preferencesCentric_activeLabel", layoutSettings.value( "preferencesCentric/activeLabel" ) )
		self._settings.setValue( "one_geometry", "" )
		self._settings.setValue( "one_windowState", "" )
		self._settings.setValue( "one_centralWidget", True )
		self._settings.setValue( "one_activeLabel", "" )
		self._settings.setValue( "two_geometry", "" )
		self._settings.setValue( "two_windowState", "" )
		self._settings.setValue( "two_centralWidget", True )
		self._settings.setValue( "two_activeLabel", "" )
		self._settings.setValue( "three_geometry", "" )
		self._settings.setValue( "three_windowState", "" )
		self._settings.setValue( "three_centralWidget", True )
		self._settings.setValue( "three_activeLabel", "" )
		self._settings.setValue( "four_geometry", "" )
		self._settings.setValue( "four_windowState", "" )
		self._settings.setValue( "four_centralWidget", True )
		self._settings.setValue( "four_activeLabel", "" )
		self._settings.setValue( "five_geometry", "" )
		self._settings.setValue( "five_windowState", "" )
		self._settings.setValue( "five_centralWidget", True )
		self._settings.setValue( "five_activeLabel", "" )
		self._settings.endGroup()

	@core.executionTrace
	def setKey( self, section, key, value ) :
		'''
		This Method Stores Provided Key In Settings File.
	
		@param section: Current Section To Save The Key Into. ( String )
		@param key: Current Key To Save. ( String )
		@param value: Current Key Value To Save. ( Object )
		'''

		LOGGER.debug( "> Saving '{0}' In '{1}' Section With Value : '{2}' In Settings File.".format( key, section, value ) )

		self._settings.beginGroup( section )
		self._settings.setValue( key , QVariant( value ) )
		self._settings.endGroup()

	@core.executionTrace
	def getKey( self, section, key ) :
		'''
		This Method Gets Key Value From Settings File.
	
		@param section: Current Section To Retrieve Key From. ( String )
		@param key: Current Key To Retrieve. ( String )
		@return: Current Key Value. ( Object )
		'''

		LOGGER.debug( "> Retrieving '{0}' In '{1}' Section.".format( key, section ) )

		self._settings.beginGroup( section )
		value = self._settings.value( key )
		LOGGER.debug( "> Key Value : '{0}'.".format( value ) )
		self._settings.endGroup()

		return value

class LayoutActiveLabel( core.Structure ):
	'''
	This Is The LayoutActiveLabel Class.
	'''

	@core.executionTrace
	def __init__( self, **kwargs ):
		'''
		This Method Initializes The Class.

		@param kwargs: name, object_, layout, shortcut. ( Key / Value Pairs )
		'''

		core.Structure.__init__( self, **kwargs )

		# --- Setting Class Attributes. ---
		self.__dict__.update( kwargs )

class sIBL_GUI( Ui_Type, Ui_Setup ):
	'''
	This Class Is The Main Class For sIBL_GUI.
	'''

	#***************************************************************************************
	#***	Initialization.
	#***************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( ui.common.uiSystemExitExceptionHandler, False, Exception )
	def __init__( self ) :
		'''
		This Method Initializes The Class.
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		Ui_Type.__init__( self )
		Ui_Setup.__init__( self )

		self.setupUi( self )

		# --- Setting Class Attributes. ---
		self._signalsSlotsCenter = QObject()
		self._componentsManager = None
		self._coreComponentsManagerUi = None
		self._preferencesManager = None
		self._coreDb = None
		self._coreDatabaseBrowser = None
		self._coreCollectionsOutliner = None
		self._coreTemplatesOutliner = None
		self._lastBrowsedPath = os.getcwd()
		self._userApplicationDatasDirectory = RuntimeConstants.userApplicationDatasDirectory
		self._loggingSessionHandler = RuntimeConstants.loggingSessionHandler
		self._loggingFileHandler = RuntimeConstants.loggingFileHandler
		self._loggingConsoleHandler = RuntimeConstants.loggingConsoleHandler
		self._loggingSessionHandlerStream = RuntimeConstants.loggingSessionHandlerStream
		self._settings = RuntimeConstants.settings
		self._verbosityLevel = RuntimeConstants.verbosityLevel
		self._parameters = RuntimeConstants.parameters
		self._libraryActiveLabel = None
		self._exportActiveLabel = None
		self._preferencesActiveLabel = None
		self._layoutsActiveLabels = None
		self._layoutMenu = None
		self._miscMenu = None
		self._workerThreads = []

		# --- Initializing sIBL_GUI. ---
		RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Initializing Interface.".format( self.__class__.__name__, Constants.releaseVersion ), 0.25 )

		# Visual Style Initialisation.
		self.setVisualStyle()
		ui.common.setWindowDefaultIcon( self )

		# Setting Window Title And Toolbar.
		self.setWindowTitle( "{0} - {1}".format( Constants.applicationName, Constants.releaseVersion ) )
		self.initializeToolbar()

		# --- Initializing Component Manager. ---
		RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Initializing Components Manager.".format( self.__class__.__name__, Constants.releaseVersion ), 0.25 )

		self._componentsManager = Manager( { "Core" : os.path.join( os.getcwd(), Constants.coreComponentsDirectory ), "Addons" : os.path.join( os.getcwd(), Constants.addonsComponentsDirectory ), "User" : os.path.join( self._userApplicationDatasDirectory, Constants.userComponentsDirectory ) } )
		self._componentsManager.gatherComponents()

		if not self._componentsManager.components :
			raise foundations.exceptions.ProgrammingError, "'{0}' Manager Has No Components, {1} Will Now Close !".format( self._componentsManager, Constants.applicationName )

		self._componentsManager.instantiateComponents( self.componentsInstantiationCallback )

		# --- Activating Component Manager Ui. ---
		self._coreComponentsManagerUi = self._componentsManager.getInterface( "core.componentsManagerUi" )
		if self._coreComponentsManagerUi :
			RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.componentsManagerUi" ) )
			self._coreComponentsManagerUi.activate( self )
			self._coreComponentsManagerUi.addWidget()
			self._coreComponentsManagerUi.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close !".format( "core.componentsManagerUi", Constants.applicationName )

		# --- Activating Preferences Manager Component. ---
		self._preferencesManager = self._componentsManager.getInterface( "core.preferencesManager" )
		if self._preferencesManager :
			RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.preferencesManager" ) )
			self._preferencesManager.activate( self )
			self._preferencesManager.addWidget()
			self._preferencesManager.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close !".format( "core.preferencesManager", Constants.applicationName )

		# --- Activating Database Component. ---
		self._coreDb = self._componentsManager.getInterface( "core.db" )
		if self._coreDb :
			RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.db" ) )
			self._coreDb.activate( self )
			self._coreDb.initialize()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close !".format( "core.db", Constants.applicationName )

		# --- Activating Collections Outliner Component. ---
		self._coreCollectionsOutliner = self._componentsManager.getInterface( "core.collectionsOutliner" )
		if self._coreCollectionsOutliner :
			RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.collectionsOutliner" ) )
			self._coreCollectionsOutliner.activate( self )
			self._coreCollectionsOutliner.addWidget()
			self._coreCollectionsOutliner.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close !".format( "core.collectionsOutliner", Constants.applicationName )

		# --- Activating Database Browser Component. ---
		self._coreDatabaseBrowser = self._componentsManager.getInterface( "core.databaseBrowser" )
		if self._coreDatabaseBrowser :
			RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.databaseBrowser" ) )
			self._coreDatabaseBrowser.activate( self )
			self._coreDatabaseBrowser.addWidget()
			self._coreDatabaseBrowser.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close !".format( "core.databaseBrowser", Constants.applicationName )

		# --- Activating Templates Outliner Component. ---
		self._coreTemplatesOutliner = self._componentsManager.getInterface( "core.templatesOutliner" )
		if self._coreTemplatesOutliner :
			RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.templatesOutliner" ) )
			self._coreTemplatesOutliner.activate( self )
			self._coreTemplatesOutliner.addWidget()
			self._coreTemplatesOutliner.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close !".format( "core.templatesOutliner", Constants.applicationName )

		# --- Activating Others Components. ---
		deactivatedComponents = self._settings.getKey( "Settings", "deactivatedComponents" ).toString().split( "," )
		for component in self._componentsManager.getComponents() :
			if component not in deactivatedComponents :
				profile = self._componentsManager.components[component]
				interface = self._componentsManager.getInterface( component )
				if not interface.activated:
					RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, component ) )
					interface.activate( self )
					if profile.categorie == "default" :
						interface.initialize()
					elif profile.categorie == "ui" :
						interface.addWidget()
						interface.initializeUi()

		# Hiding Splashscreen.
		LOGGER.debug( "> Hiding SplashScreen." )
		RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Initialization Done.".format( self.__class__.__name__, Constants.releaseVersion ) )
		RuntimeConstants.splashscreen.hide()

		# --- Running onStartup Components Methods. ---
		for component in self._componentsManager.getComponents() :
			interface = self._componentsManager.getInterface( component )
			if interface.activated:
				hasattr( interface, "onStartup" ) and interface.onStartup()

		# Layouts Helper Snippet.
		# visibleComponents = ()
		# for component in self._componentsManager.getComponents() :
		#	 interface = self._componentsManager.getInterface( component )
		#	 hasattr( interface, "ui" ) and interface.name != "core.databaseBrowser" and interface.name not in visibleComponents and interface.ui and interface.ui.hide()

		self.setLayoutsActiveLabelsShortcuts()

		self.restoreStartupLayout()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
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
	def componentsManager( self ):
		'''
		This Method Is The Property For The _componentsManager Attribute.

		@return: self._componentsManager. ( Object )
		'''

		return self._componentsManager

	@componentsManager.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def componentsManager( self, value ):
		'''
		This Method Is The Setter Method For The _componentsManager Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "componentsManager" ) )

	@componentsManager.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def componentsManager( self ):
		'''
		This Method Is The Deleter Method For The _componentsManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "componentsManager" ) )

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
	def lastBrowsedPath( self ):
		'''
		This Method Is The Property For The _lastBrowsedPath Attribute.

		@return: self._lastBrowsedPath. ( String )
		'''

		return self._lastBrowsedPath

	@lastBrowsedPath.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def lastBrowsedPath( self, value ):
		'''
		This Method Is The Setter Method For The _lastBrowsedPath Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type( value ) in ( str, unicode ), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format( "lastBrowsedPath", value )
			assert os.path.exists( value ), "'{0}' Attribute : '{1}' Directory Doesn't Exists !".format( "lastBrowsedPath", value )
		self._lastBrowsedPath = value

	@lastBrowsedPath.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def lastBrowsedPath( self ):
		'''
		This Method Is The Deleter Method For The _lastBrowsedPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "lastBrowsedPath" ) )

	@property
	def userApplicationDatasDirectory( self ):
		'''
		This Method Is The Property For The _userApplicationDatasDirectory Attribute.

		@return: self._userApplicationDatasDirectory. ( String )
		'''

		return self._userApplicationDatasDirectory

	@userApplicationDatasDirectory.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def userApplicationDatasDirectory( self, value ):
		'''
		This Method Is The Setter Method For The _userApplicationDatasDirectory Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "userApplicationDatasDirectory" ) )

	@userApplicationDatasDirectory.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def userApplicationDatasDirectory( self ):
		'''
		This Method Is The Deleter Method For The _userApplicationDatasDirectory Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "userApplicationDatasDirectory" ) )

	@property
	def loggingSessionHandler( self ):
		'''
		This Method Is The Property For The _loggingSessionHandler Attribute.

		@return: self._loggingSessionHandler. ( Handler )
		'''

		return self._loggingSessionHandler

	@loggingSessionHandler.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingSessionHandler( self, value ):
		'''
		This Method Is The Setter Method For The _loggingSessionHandler Attribute.

		@param value: Attribute Value. ( Handler )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "loggingSessionHandler" ) )

	@loggingSessionHandler.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingSessionHandler( self ):
		'''
		This Method Is The Deleter Method For The _loggingSessionHandler Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "loggingSessionHandler" ) )

	@property
	def loggingFileHandler( self ):
		'''
		This Method Is The Property For The _loggingFileHandler Attribute.

		@return: self._loggingFileHandler. ( Handler )
		'''

		return self._loggingFileHandler

	@loggingFileHandler.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingFileHandler( self, value ):
		'''
		This Method Is The Setter Method For The _loggingFileHandler Attribute.

		@param value: Attribute Value. ( Handler )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "loggingFileHandler" ) )

	@loggingFileHandler.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingFileHandler( self ):
		'''
		This Method Is The Deleter Method For The _loggingFileHandler Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "loggingFileHandler" ) )

	@property
	def loggingConsoleHandler( self ):
		'''
		This Method Is The Property For The _loggingConsoleHandler Attribute.

		@return: self._loggingConsoleHandler. ( Handler )
		'''

		return self._loggingConsoleHandler

	@loggingConsoleHandler.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingConsoleHandler( self, value ):
		'''
		This Method Is The Setter Method For The _loggingConsoleHandler Attribute.

		@param value: Attribute Value. ( Handler )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "loggingConsoleHandler" ) )

	@loggingConsoleHandler.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingConsoleHandler( self ):
		'''
		This Method Is The Deleter Method For The _loggingConsoleHandler Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "loggingConsoleHandler" ) )

	@property
	def loggingSessionHandlerStream( self ):
		'''
		This Method Is The Property For The _loggingSessionHandlerStream Attribute.

		@return: self._loggingSessionHandlerStream. ( StreamObject )
		'''

		return self._loggingSessionHandlerStream

	@loggingSessionHandlerStream.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingSessionHandlerStream( self, value ):
		'''
		This Method Is The Setter Method For The _loggingSessionHandlerStream Attribute.

		@param value: Attribute Value. ( StreamObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "loggingSessionHandlerStream" ) )

	@loggingSessionHandlerStream.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingSessionHandlerStream( self ):
		'''
		This Method Is The Deleter Method For The _loggingSessionHandlerStream Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "loggingSessionHandlerStream" ) )

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
	def verbosityLevel( self ):
		'''
		This Method Is The Property For The _verbosityLevel Attribute.

		@return: self._verbosityLevel. ( Integer )
		'''

		return self._verbosityLevel

	@verbosityLevel.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def verbosityLevel( self, value ):
		'''
		This Method Is The Setter Method For The _verbosityLevel Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		if value :
			assert type( value ) is int, "'{0}' Attribute : '{1}' Type Is Not 'int' !".format( "verbosityLevel", value )
			assert value >= 0 and value <= 4, "'{0}' Attribute : Value Need To Be Exactly Beetween 0 and 4 !".format( "verbosityLevel" )
		self._verbosityLevel = value

	@verbosityLevel.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def verbosityLevel( self ):
		'''
		This Method Is The Deleter Method For The _verbosityLevel Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "verbosityLevel" ) )

	@property
	def parameters( self ):
		'''
		This Method Is The Property For The _parameters Attribute.

		@return: self._parameters. ( Object )
		'''

		return self._parameters

	@parameters.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def parameters( self, value ):
		'''
		This Method Is The Setter Method For The _parameters Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "parameters" ) )

	@parameters.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def parameters( self ):
		'''
		This Method Is The Deleter Method For The _parameters Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "parameters" ) )

	@property
	def libraryActiveLabel ( self ):
		'''
		This Method Is The Property For The _libraryActiveLabel  Attribute.

		@return: self._libraryActiveLabel . ( Active_QLabel )
		'''

		return self._libraryActiveLabel

	@libraryActiveLabel .setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def libraryActiveLabel ( self, value ):
		'''
		This Method Is The Setter Method For The _libraryActiveLabel  Attribute.

		@param value: Attribute Value. ( Active_QLabel )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "libraryActiveLabel " ) )

	@libraryActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def libraryActiveLabel ( self ):
		'''
		This Method Is The Deleter Method For The _libraryActiveLabel  Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "libraryActiveLabel " ) )

	@property
	def exportActiveLabel ( self ):
		'''
		This Method Is The Property For The _exportActiveLabel  Attribute.

		@return: self._exportActiveLabel . ( Active_QLabel )
		'''

		return self._exportActiveLabel

	@exportActiveLabel .setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def exportActiveLabel ( self, value ):
		'''
		This Method Is The Setter Method For The _exportActiveLabel  Attribute.

		@param value: Attribute Value. ( Active_QLabel )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "exportActiveLabel " ) )

	@exportActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def exportActiveLabel ( self ):
		'''
		This Method Is The Deleter Method For The _exportActiveLabel  Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "exportActiveLabel " ) )

	@property
	def preferencesActiveLabel ( self ):
		'''
		This Method Is The Property For The _preferencesActiveLabel  Attribute.

		@return: self._preferencesActiveLabel . ( Active_QLabel )
		'''

		return self._preferencesActiveLabel

	@preferencesActiveLabel .setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def preferencesActiveLabel ( self, value ):
		'''
		This Method Is The Setter Method For The _preferencesActiveLabel  Attribute.

		@param value: Attribute Value. ( Active_QLabel )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "preferencesActiveLabel " ) )

	@preferencesActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def preferencesActiveLabel ( self ):
		'''
		This Method Is The Deleter Method For The _preferencesActiveLabel  Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "preferencesActiveLabel " ) )

	@property
	def layoutsActiveLabels( self ):
		'''
		This Method Is The Property For The _layoutsActiveLabels Attribute.

		@return: self._layoutsActiveLabels. ( Tuple )
		'''

		return self._layoutsActiveLabels

	@layoutsActiveLabels.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def layoutsActiveLabels( self, value ):
		'''
		This Method Is The Setter Method For The _layoutsActiveLabels Attribute.

		@param value: Attribute Value. ( Tuple )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "layoutsActiveLabels" ) )

	@layoutsActiveLabels.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def layoutsActiveLabels( self ):
		'''
		This Method Is The Deleter Method For The _layoutsActiveLabels Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "layoutsActiveLabels" ) )

	@property
	def layoutMenu( self ):
		'''
		This Method Is The Property For The _layoutMenu Attribute.

		@return: self._layoutMenu. ( QMenu )
		'''

		return self._layoutMenu

	@layoutMenu.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def layoutMenu( self, value ):
		'''
		This Method Is The Setter Method For The _layoutMenu Attribute.

		@param value: Attribute Value. ( QMenu )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "layoutMenu" ) )

	@layoutMenu.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def layoutMenu( self ):
		'''
		This Method Is The Deleter Method For The _layoutMenu Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "layoutMenu" ) )

	@property
	def miscMenu( self ):
		'''
		This Method Is The Property For The _miscMenu Attribute.

		@return: self._miscMenu. ( QMenu )
		'''

		return self._miscMenu

	@miscMenu.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def miscMenu( self, value ):
		'''
		This Method Is The Setter Method For The _miscMenu Attribute.

		@param value: Attribute Value. ( QMenu )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "miscMenu" ) )

	@miscMenu.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def miscMenu( self ):
		'''
		This Method Is The Deleter Method For The _miscMenu Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "miscMenu" ) )

	@property
	def workerThreads( self ):
		'''
		This Method Is The Property For The _workerThreads Attribute.

		@return: self._workerThreads. ( List )
		'''

		return self._workerThreads

	@workerThreads.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def workerThreads( self, value ):
		'''
		This Method Is The Setter Method For The _workerThreads Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "workerThreads" ) )

	@workerThreads.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def workerThreads( self ):
		'''
		This Method Is The Deleter Method For The _workerThreads Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "workerThreads" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def closeEvent( self, event ) :
		'''
		This Method Is Called When Close Event Is Fired.

		@param event: QEvent. ( QEvent )
		'''

		# Storing Current Layout.
		self.storeStartupLayout()
		self._settings.settings.sync()

		# Stopping Worker Threads.
		for workerThread in self._workerThreads :
			if not workerThread.isFinished() :
				LOGGER.debug( "> Stopping Worker Thread : '{0}'.".format( workerThread ) )
				workerThread.exit()

		foundations.common.closeHandler( LOGGER, self._loggingFileHandler )
		foundations.common.closeHandler( LOGGER, self._loggingSessionHandler )
		# foundations.common.closeHandler( LOGGER, self._loggingConsoleHandler )

		self.deleteLater()
		event.accept()

		sIBL_GUI_close()

	@core.executionTrace
	def componentsInstantiationCallback( self, profile ):
		'''
		This Method Is A Callback For The Components Instantiation.
		
		@param profile: Component Profile. ( Profile )	
		'''

		RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Instantiating {2} Component.".format( self.__class__.__name__, Constants.releaseVersion, profile.name ) )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( ui.common.uiBasicExceptionHandler, False, OSError )
	def setVisualStyle( self ):
		'''
		This Method Sets The Application Visual Style.
		'''

		if platform.system() == "Windows" or platform.system() == "Microsoft" :
			RuntimeConstants.application.setStyle( "Plastique" )
			styleSheetFile = io.File( UiConstants.frameworkWindowsStylesheetFile )
		elif platform.system() == "Darwin" :
			styleSheetFile = io.File( UiConstants.frameworkDarwinStylesheetFile )
		elif platform.system() == "Linux" :
			RuntimeConstants.application.setStyle( "Plastique" )
			styleSheetFile = io.File( UiConstants.frameworkLinuxStylesheetFile )

		if os.path.exists( styleSheetFile.file ):
			styleSheetFile.read()
			RuntimeConstants.application.setStyleSheet( QString( "".join( styleSheetFile.content ) ) )
		else :
			raise OSError, "{0} | '{1}' Stylesheet File Is Not Available, Visual Style Will Not Be Applied !".format( self.__class__.__name__, styleSheetFile.file )

	@core.executionTrace
	def initializeToolbar( self ):
		'''
		This Method Initializes sIBL_GUI Toolbar.
		'''

		self.toolBar.setIconSize( QSize( UiConstants.frameworkDefaultToolbarIconSize, UiConstants.frameworkDefaultToolbarIconSize ) )

		logolabel = QLabel()
		logolabel.setPixmap( QPixmap( UiConstants.frameworkLogoPicture ) )
		self.toolBar.addWidget( logolabel )

		spacer = QLabel()
		spacer.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
		self.toolBar.addWidget( spacer )

		toolbarFont = QFont()
		toolbarFont.setPointSize( 16 )

		self._libraryActiveLabel = Active_QLabel( QPixmap( UiConstants.frameworkLibraryIcon ), QPixmap( UiConstants.frameworkLibraryHoverIcon ), QPixmap( UiConstants.frameworkLibraryActiveIcon ), True )
		self.toolBar.addWidget( self._libraryActiveLabel )

		self._exportActiveLabel = Active_QLabel( QPixmap( UiConstants.frameworkExportIcon ), QPixmap( UiConstants.frameworkExportHoverIcon ), QPixmap( UiConstants.frameworkExportActiveIcon ), True )
		self.toolBar.addWidget( self._exportActiveLabel )

		self._preferencesActiveLabel = Active_QLabel( QPixmap( UiConstants.frameworkPreferencesIcon ), QPixmap( UiConstants.frameworkPreferencesHoverIcon ), QPixmap( UiConstants.frameworkPreferencesActiveIcon ), True )
		self.toolBar.addWidget( self._preferencesActiveLabel )

		self._layoutsActiveLabels = ( LayoutActiveLabel( name = "Library", object_ = self._libraryActiveLabel, layout = "setsCentric", shortcut = Qt.Key_8 ),
									LayoutActiveLabel( name = "Export", object_ = self._exportActiveLabel, layout = "templatesCentric", shortcut = Qt.Key_9 ),
									LayoutActiveLabel( name = "Preferences", object_ = self._preferencesActiveLabel, layout = "preferencesCentric", shortcut = Qt.Key_0 )
									)

		# Signals / Slots.
		for layoutActiveLabel in self._layoutsActiveLabels :
			self._signalsSlotsCenter.connect( layoutActiveLabel.object_, SIGNAL( "clicked()" ), lambda activeLabel = layoutActiveLabel.layout : self.activeLabel_OnClicked( activeLabel ) )

		centralWidgetButton = Active_QLabel( QPixmap( UiConstants.frameworCentralWidgetIcon ), QPixmap( UiConstants.frameworCentralWidgetHoverIcon ), QPixmap( UiConstants.frameworCentralWidgetActiveIcon ) )
		self.toolBar.addWidget( centralWidgetButton )

		self._signalsSlotsCenter.connect( centralWidgetButton, SIGNAL( "clicked()" ), self.centralWidgetButton_OnClicked )

		layoutbutton = Active_QLabel( QPixmap( UiConstants.frameworLayoutIcon ), QPixmap( UiConstants.frameworLayoutHoverIcon ), QPixmap( UiConstants.frameworLayoutActiveIcon ), parent = self )
		self.toolBar.addWidget( layoutbutton )

		self._layoutMenu = QMenu( "Layout", layoutbutton )

		userLayouts = ( ( "1", Qt.Key_1, "one" ), ( "2", Qt.Key_2, "two" ), ( "3", Qt.Key_3, "three" ), ( "4", Qt.Key_4, "four" ), ( "5", Qt.Key_5, "five" ) )

		for layout in userLayouts :
			action = QAction( "Restore Layout {0}".format( layout[0] ), self )
			action.setShortcut( QKeySequence( layout[1] ) )
			self._layoutMenu.addAction( action )

			# Signals / Slots.
			self._signalsSlotsCenter.connect( action, SIGNAL( "triggered()" ), lambda layout = layout[2] : self.restoreLayout( layout ) )

		self._layoutMenu.addSeparator()

		for layout in userLayouts :
			action = QAction( "Store Layout {0}".format( layout[0] ), self )
			action.setShortcut( QKeySequence( Qt.CTRL + layout[1] ) )
			self._layoutMenu.addAction( action )

			# Signals / Slots.
			self._signalsSlotsCenter.connect( action, SIGNAL( "triggered()" ), lambda layout = layout[2] : self.storeLayout( layout ) )

		layoutbutton.setMenu( self._layoutMenu )

		miscellaneousbutton = Active_QLabel( QPixmap( UiConstants.frameworMiscellaneousIcon ), QPixmap( UiConstants.frameworMiscellaneousHoverIcon ), QPixmap( UiConstants.frameworMiscellaneousActiveIcon ), parent = self )
		self.toolBar.addWidget( miscellaneousbutton )

		helpDisplayMiscAction = QAction( "Help Content ...", self )
		apiDisplayMiscAction = QAction( "Api Content ...", self )

		self._miscMenu = QMenu( "Miscellaneous", miscellaneousbutton )

		self._miscMenu.addAction( helpDisplayMiscAction )
		self._miscMenu.addAction( apiDisplayMiscAction )
		self._miscMenu.addSeparator()

		# Signals / Slots.
		self._signalsSlotsCenter.connect( helpDisplayMiscAction, SIGNAL( "triggered()" ), self.helpDisplayMiscAction_OnTriggered )
		self._signalsSlotsCenter.connect( apiDisplayMiscAction, SIGNAL( "triggered()" ), self.apiDisplayMiscAction_OnTriggered )

		miscellaneousbutton.setMenu( self._miscMenu )

		spacer = QLabel()
		spacer.setSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )
		self.toolBar.addWidget( spacer )

	@core.executionTrace
	def activeLabel_OnClicked( self, activeLabel ):
		'''
		This Method Is Triggered When An Active Label Is Clicked.
		'''

		self.restoreLayout( activeLabel )
		for layoutActivelabel in self._layoutsActiveLabels :
			layoutActivelabel.layout is not activeLabel and layoutActivelabel.object_.setChecked( False )

	@core.executionTrace
	def centralWidgetButton_OnClicked( self ):
		'''
		This Method Sets The Central Widget Visibility.
		'''

		if self.centralwidget.isVisible() :
			self.centralwidget.hide()
		else :
			self.centralwidget.show()

	@core.executionTrace
	def setLayoutsActiveLabelsShortcuts( self ):
		'''
		This Method Sets The Layouts Active Labels Shortcuts.
		'''

		for layoutActiveLabel in self._layoutsActiveLabels :
			action = QAction( layoutActiveLabel.name, self )
			action.setShortcut( QKeySequence( layoutActiveLabel.shortcut ) )
			self.addAction( action )
			self._signalsSlotsCenter.connect( action, SIGNAL( "triggered()" ), lambda layout = layoutActiveLabel.layout : self.restoreLayout( layout ) )

	@core.executionTrace
	def getLayoutsActiveLabel( self ):
		'''
		This Method Returns The Layouts Active Label Index.

		@return: Layouts Active Label Index. ( Integer )
		'''

		for index in range( len( self._layoutsActiveLabels ) ):
			if self._layoutsActiveLabels[index].object_.isChecked():
				return index

	@core.executionTrace
	def setLayoutsActiveLabel( self, index ):
		'''
		This Method Sets The Layouts Active Label.

		@param index: Layouts Active Label. ( Integer )
		'''

		for index_ in range( len( self._layoutsActiveLabels ) ):
			self._layoutsActiveLabels[index_].object_.setChecked( index == index_ and True or False )

	@core.executionTrace
	def storeLayout( self, name ):
		'''
		This Method Is Called When Storing A Layout.

		@param name: Layout Name. ( String )
		'''

		LOGGER.debug( "> Storing Layout '{0}'.".format( name ) )

		self._settings.setKey( "Layouts", "{0}_geometry".format( name ), self.saveGeometry() )
		self._settings.setKey( "Layouts", "{0}_windowState".format( name ), self.saveState() )
		self._settings.setKey( "Layouts", "{0}_centralWidget".format( name ), self.centralwidget.isVisible() )
		self._settings.setKey( "Layouts", "{0}_activeLabel".format( name ), self.getLayoutsActiveLabel() )

	@core.executionTrace
	def restoreLayout( self, name ):
		'''
		This Method Is Called When Restoring A Layout.

		@param name: Layout Name. ( String )
		'''

		LOGGER.debug( "> Restoring Layout '{0}'.".format( name ) )

		visibleComponents = [ "core.databaseBrowser" ]
		for component, profile in self._componentsManager.components.items() :
			profile.categorie == "ui" and component not in visibleComponents and self._componentsManager.getInterface( component ).ui and self._componentsManager.getInterface( component ).ui.hide()

		self.centralwidget.setVisible( self._settings.getKey( "Layouts", "{0}_centralWidget".format( name ) ).toBool() )
		self.restoreState( self._settings.getKey( "Layouts", "{0}_windowState".format( name ) ).toByteArray() )
		self._preferencesManager.ui.Restore_Geometry_On_Layout_Change_checkBox.isChecked() and self.restoreGeometry( self._settings.getKey( "Layouts", "{0}_geometry".format( name ) ).toByteArray() )
		self.setLayoutsActiveLabel( self._settings.getKey( "Layouts", "{0}_activeLabel".format( name ) ).toInt()[0] )
		QApplication.focusWidget() and QApplication.focusWidget().clearFocus()

	@core.executionTrace
	def restoreStartupLayout( self ):
		'''
		This Method Restores The Startup Layout.
		'''

		LOGGER.debug( "> Restoring Startup Layout." )

		self.restoreLayout( UiConstants.frameworkStartupLayout )
		not self._preferencesManager.ui.Restore_Geometry_On_Layout_Change_checkBox.isChecked() and self.restoreGeometry( self._settings.getKey( "Layouts", "{0}_geometry".format( UiConstants.frameworkStartupLayout ) ).toByteArray() )

	@core.executionTrace
	def storeStartupLayout( self ):
		'''
		This Method Restores The Startup Layout.
		'''

		LOGGER.debug( "> Storing Startup Layout." )

		self.storeLayout( UiConstants.frameworkStartupLayout )

	@core.executionTrace
	def helpDisplayMiscAction_OnTriggered( self ):
		'''
		This Method Is Triggered By helpDisplayMiscAction.
		'''

		LOGGER.debug( "> Opening URL : '{0}'.".format( UiConstants.frameworkHelpFile ) )
		QDesktopServices.openUrl( QUrl( QString( UiConstants.frameworkHelpFile ) ) )

	@core.executionTrace
	def apiDisplayMiscAction_OnTriggered( self ):
		'''
		This Method Is Triggered By apiDisplayMiscAction.
		'''

		LOGGER.debug( "> Opening URL : '{0}'.".format( UiConstants.frameworkApiFile ) )
		QDesktopServices.openUrl( QUrl( QString( UiConstants.frameworkApiFile ) ) )

	@core.executionTrace
	def storeLastBrowsedPath( self, path ):
		'''
		This Method Is A Wrapper Method For Storing The Last Browser Path.
		
		@param path: Provided Path. ( QString )
		@return: Provided Path. ( QString )
		'''

		path = str( path )

		lastBrowserPath = os.path.normpath( os.path.join( os.path.isfile( path ) and os.path.dirname( path ) or path, ".." ) )
		LOGGER.debug( "> Storing Last Browsed Path : '%s'.", lastBrowserPath )

		self._lastBrowsedPath = lastBrowserPath

		return path

#***************************************************************************************
#***	Overall Definitions.
#***************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler( ui.common.uiStandaloneSystemExitExceptionHandler, False, OSError )
def sIBL_GUI_start():
	'''
	This Definition Is Called When sIBL_GUI Starts.
	'''

	# Command Line Parameters Handling.
	RuntimeConstants.parameters, RuntimeConstants.args = getCommandLineParameters( sys.argv )

	if RuntimeConstants.parameters.about :
		for line in getHeaderMessage() :
			sys.stdout.write( "{0}\n".format( line ) )
		foundations.common.exit( 1, LOGGER, [] )

	# Redirecting Standard Output And Error Messages.
	sys.stdout = core.StandardMessageHook( LOGGER )
	sys.stderr = core.StandardMessageHook( LOGGER )

	# Setting Application Verbose Level.
	LOGGER.setLevel( logging.DEBUG )

	# Setting User Application Datas Directory.
	if RuntimeConstants.parameters.userApplicationDatasDirectory :
		RuntimeConstants.userApplicationDatasDirectory = RuntimeConstants.parameters.userApplicationDatasDirectory
	else :
		RuntimeConstants.userApplicationDatasDirectory = foundations.common.getUserApplicationDatasDirectory()

	if not setUserApplicationDatasDirectory( RuntimeConstants.userApplicationDatasDirectory ) :
		raise OSError, "'{0}' User Application Datas Directory Is Not Available, {1} Will Now Close !".format( RuntimeConstants.userApplicationDatasDirectory, Constants.applicationName )

	# Getting The Logging File Path.
	RuntimeConstants.loggingFile = os.path.join( RuntimeConstants.userApplicationDatasDirectory, Constants.loggingDirectory, Constants.loggingFile )

	try :
		os.path.exists( RuntimeConstants.loggingFile ) and os.remove( RuntimeConstants.loggingFile )
	except :
		raise OSError, "{0} Logging File Is Currently Locked, {1} Will Now Close !".format( RuntimeConstants.loggingFile, Constants.applicationName )

	try :
		RuntimeConstants.loggingFileHandler = logging.FileHandler( RuntimeConstants.loggingFile )
		RuntimeConstants.loggingFileHandler.setFormatter( core.LOGGING_FORMATTER )
		LOGGER.addHandler( RuntimeConstants.loggingFileHandler )
	except :
		raise OSError, "{0} Logging File Is Not Available, {1} Will Now Close !".format( RuntimeConstants.loggingFile, Constants.applicationName )

	# Retrieving Framework Verbose Level From Settings File.
	LOGGER.debug( "> Initializing {0} !".format( Constants.applicationName ) )
	LOGGER.debug( "> Retrieving Stored Verbose Level." )

	RuntimeConstants.settingsFile = os.path.join( RuntimeConstants.userApplicationDatasDirectory, Constants.settingsDirectory, Constants.settingsFile )

	RuntimeConstants.settings = Preferences( RuntimeConstants.settingsFile )

	os.path.exists( RuntimeConstants.settingsFile ) or RuntimeConstants.settings.setDefaultPreferences()

	RuntimeConstants.verbosityLevel = RuntimeConstants.parameters.verbosityLevel and RuntimeConstants.parameters.verbosityLevel or RuntimeConstants.settings.getKey( "Settings", "verbosityLevel" ).toInt()[0]
	LOGGER.debug( "> Setting Logger Verbosity Level To : '{0}'.".format( RuntimeConstants.verbosityLevel ) )
	core.setVerbosityLevel( RuntimeConstants.verbosityLevel )

	# Starting The Session Handler.
	RuntimeConstants.loggingSessionHandlerStream = StreamObject()
	RuntimeConstants.loggingSessionHandler = logging.StreamHandler( RuntimeConstants.loggingSessionHandlerStream )
	RuntimeConstants.loggingSessionHandler.setFormatter( core.LOGGING_FORMATTER )
	LOGGER.addHandler( RuntimeConstants.loggingSessionHandler )

	LOGGER.info( Constants.loggingSeparators )
	for line in getHeaderMessage() :
		LOGGER.info( line )
	LOGGER.info( "{0} | Session Started At : {1}".format( Constants.applicationName, time.strftime( '%X - %x' ) ) )
	LOGGER.info( Constants.loggingSeparators )
	LOGGER.info( "{0} | Starting Interface !".format( Constants.applicationName ) )

	RuntimeConstants.application = QApplication( sys.argv )

	# Initializing SplashScreen.
	LOGGER.debug( "> Initializing SplashScreen." )

	RuntimeConstants.splashscreenPicture = QPixmap( UiConstants.frameworkSplashScreenPicture )
	RuntimeConstants.splashscreen = Delayed_QSplashScreen( RuntimeConstants.splashscreenPicture )
	RuntimeConstants.splashscreen.setMessage( "{0} - {1} | Initializing {0}.".format( Constants.applicationName, Constants.releaseVersion ) )
	RuntimeConstants.splashscreen.show()

	RuntimeConstants.ui = sIBL_GUI()
	RuntimeConstants.ui.show()
	RuntimeConstants.ui.raise_()

	sys.exit( RuntimeConstants.application.exec_() )

@core.executionTrace
def sIBL_GUI_close() :
	'''
	This Definition Is Called When sIBL_GUI Closes.
	'''

	LOGGER.info( "{0} | Closing Interface ! ".format( Constants.applicationName ) )
	LOGGER.info( Constants.loggingSeparators )
	LOGGER.info( "{0} | Session Ended At : {1}".format( Constants.applicationName, time.strftime( '%X - %x' ) ) )
	LOGGER.info( Constants.loggingSeparators )

	foundations.common.closeHandler( LOGGER, RuntimeConstants.loggingConsoleHandler )

	QApplication.exit()

@core.executionTrace
@foundations.exceptions.exceptionsHandler( ui.common.uiStandaloneSystemExitExceptionHandler, False, OSError )
def setUserApplicationDatasDirectory( path ):
	'''
	This Definition Sets The Application Datas Directory.

	@param path: Starting Point For The Directories Tree Creation. ( String )
	'''

	userApplicationDatasDirectory = RuntimeConstants.userApplicationDatasDirectory

	LOGGER.debug( "> Current Application Datas Directory '{0}'.".format( userApplicationDatasDirectory ) )
	if io.setLocalDirectory( userApplicationDatasDirectory ) :
		for directory in Constants.preferencesDirectories :
			if not io.setLocalDirectory( os.path.join( userApplicationDatasDirectory, directory ) ) :
				raise OSError, "'{0}' Directory Creation Failed , {1} Will Now Close !".format( os.path.join( userApplicationDatasDirectory, directory ), Constants.applicationName )
		return True
	else :
		raise OSError, "'{0}' Directory Creation Failed , {1} Will Now Close !".format( userApplicationDatasDirectory, Constants.applicationName )

@core.executionTrace
def getHeaderMessage():
	'''
	This Definition Builds The Header Message.

	@return: Header Message ( List )
	'''

	message = []

	message.append( "{0} | Copyright ( C ) 2008 - 2010 Thomas Mansencal - kelsolaar_fool@hotmail.com".format( Constants.applicationName ) )
	message.append( "{0} | This Software Is Released Under Terms Of GNU GPL V3 License.".format( Constants.applicationName ) )
	message.append( "{0} | http://www.gnu.org/licenses/ ".format( Constants.applicationName ) )
	message.append( "{0} | Version : {1}".format( Constants.applicationName, Constants.releaseVersion ) )

	return message

@core.executionTrace
def getCommandLineParameters( argv ):
	'''
	This Definition Process Command Line Parameters.

	@param argv: Command Line Parameters. ( String )
	@return: Settings, Arguments ( Parser Instance )
	'''

	argv = argv or sys.argv[1:]

	parser = optparse.OptionParser( formatter = optparse.IndentedHelpFormatter ( indent_increment = 2, max_help_position = 8, width = 128, short_first = 1 ), add_help_option = None )

	parser.add_option( "-h", "--help", action = "help", help = "'Display This Help Message And Exit.'" )
	parser.add_option( "-a", "--about", action = "store_true", default = False, dest = "about", help = "'Display Application About Message.'" )
	parser.add_option( "-v", "--verbose", action = "store", type = "int", dest = "verbosityLevel", help = "'Application Verbosity Levels :  0 = Critical | 1 = Error | 2 = Warning | 3 = Info | 4 = Debug.'" )
	parser.add_option( "-u", "--userApplicationDatasDirectory", action = "store", type = "string", dest = "userApplicationDatasDirectory", help = "'User Application Datas Directory'." )

	parser.add_option( "-d", "--databaseDirectory", action = "store", type = "string", dest = "databaseDirectory", help = "'Database Directory'." )
	parser.add_option( "-r", "--databaseReadOnly", action = "store_true", default = False, dest = "databaseReadOnly", help = "'Database Read Only'." )

	parser.add_option( "-o", "--loaderScriptsOutputDirectory", action = "store", type = "string", dest = "loaderScriptsOutputDirectory", help = "'Loader Scripts Output Directory'." )

	parameters, args = parser.parse_args( argv )

	return parameters, args

#***********************************************************************************************
#***	Launcher
#***********************************************************************************************
if __name__ == "__main__":
	sIBL_GUI_start()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
