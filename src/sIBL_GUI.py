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
import logging
import os
import platform
import sys
import time
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import foundations.common
import ui.widgets.messageBox as messageBox
from ui.widgets.delayed_QSplashScreen import Delayed_QSplashScreen
from foundations.environment import Environment
from foundations.streamObject import StreamObject
from globals.uiConstants import UiConstants
from globals.constants import Constants
from manager.manager import Manager

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

# Starting The Console Handler.
LOGGING_CONSOLE_HANDLER = logging.StreamHandler( sys.stdout )
LOGGING_CONSOLE_HANDLER.setFormatter( core.LOGGING_FORMATTER )
LOGGER.addHandler( LOGGING_CONSOLE_HANDLER )

UI_FILE = os.path.join( os.getcwd(), UiConstants.frameworkUiFile )
if os.path.exists( UI_FILE ):
	Ui_Setup, Ui_Type = uic.loadUiType( UI_FILE )
else :
	messageBox.standaloneMessageBox( "Critical", "Critical", "Exception In {0}.__init__() Method | '{1}' ui File Is Not Available, {2} Will Now Close !".format( Constants.applicationName, UiConstants.frameworkUiFile, Constants.applicationName ) )
	foundations.common.exit( 1, LOGGER, [ LOGGING_CONSOLE_HANDLER ] )

USER_DATAS_DIRECTORY = None
USER_APPLICATION_DIRECTORY = None
GUI_LOGGING_FILE = None
LOGGING_FILE_HANDLER = None
SETTINGS_FILE = None
SETTINGS = None
VERBOSITY_LEVEL = None
APPLICATION = None
SPLASHSCREEN_PICTURE = None
SPLASHSCREEN = None
LOGGING_SESSION_HANDLER_STREAM = None
LOGGING_SESSION_HANDLER = None
UI = None

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

		self._settings.beginGroup( "Settings" )
		self._settings.setValue( "VerbosityLevel", QVariant( "3" ) )
		self._settings.setValue( "DeactivatedComponents", QVariant( "" ) )
		self._settings.endGroup()
		self._settings.beginGroup( "Others" )
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

class sIBL_GUI( Ui_Type, Ui_Setup ):
	'''
	This Class Is The Main Class For sIBL_GUI.
	'''

	#***************************************************************************************
	#***	Initialization.
	#***************************************************************************************
	@core.executionTrace
	def __init__( self ) :
		'''
		This Method Initializes The Class.
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		Ui_Type.__init__( self )
		Ui_Setup.__init__( self )

		self.setupUi( self )

		# --- Setting Class Attributes. ---
		self._componentsManager = None
		self._coreComponentsManagerUi = None
		self._preferencesManager = None
		self._coreDb = None
		self._coreDatabaseBrowser = None
		self._coreCollectionsOutliner = None
		self._coreTemplatesOutliner = None
		self._lastBrowsedPath = os.getcwd()
		self._userApplicationDirectory = USER_APPLICATION_DIRECTORY
		self._loggingMemoryHandler = LOGGING_SESSION_HANDLER_STREAM
		self._settings = SETTINGS
		self._verbosityLevel = VERBOSITY_LEVEL
		self._setsCentricLayoutComponents = []
		self._templatesCentricLayoutComponents = []
		self._preferencesCentricLayoutComponents = []
		self._layoutMenu = None
		self._miscMenu = None

		# --- Initializing sIBL_GUI. ---
		SPLASHSCREEN.setMessage( "{0} - {1} | Initializing Interface.".format( self.__class__.__name__, Constants.releaseVersion ) )

		# Visual Style Choice.
		if not platform.system() == "Darwin" :
			QApplication.setStyle( "Plastique" )

		# Setting Window Title And Toolbar.
		self.setWindowTitle( "{0} - {1}".format( Constants.applicationName, Constants.releaseVersion ) )
		self.initializeToolbar()

		# --- Initializing Component Manager. ---
		SPLASHSCREEN.setMessage( "{0} - {1} | Initializing Components Manager.".format( self.__class__.__name__, Constants.releaseVersion ) )

		self._componentsManager = Manager( { "Core" : os.path.join( os.getcwd(), Constants.coreComponentsDirectory ), "Addons" : os.path.join( os.getcwd(), Constants.addonsComponentsDirectory ), "User" : os.path.join( self._userApplicationDirectory, Constants.userComponentsDirectory ) } )
		self._componentsManager.gatherComponents()

		if not self._componentsManager.components :
			messageBox.messageBox( "Critical", "Critical", "Exception In {0}.__init__() Method | '{1}' Manager Has No Components !, {2} Will Now Close !".format( self.__class__.__name__, self._componentsManager, Constants.applicationName ) )
			foundations.common.exit( 1, LOGGER, [ LOGGING_SESSION_HANDLER, LOGGING_FILE_HANDLER, LOGGING_CONSOLE_HANDLER ] )

		self._componentsManager.instantiateComponents()

		# --- Activating Component Manager Ui. ---
		self._coreComponentsManagerUi = self._componentsManager.getInterface( "core.componentsManagerUi" )
		if self._coreComponentsManagerUi :
			SPLASHSCREEN.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.componentsManagerUi" ) )
			self._coreComponentsManagerUi.activate( self )
			self._coreComponentsManagerUi.addWidget()
			self._coreComponentsManagerUi.initializeUi()
		else:
			messageBox.messageBox( "Critical", "Critical", "Exception In {0}.__init__() Method | '{1}' Component Is Not Available, {2} Will Now Close !".format( self.__class__.__name__, "core.componentsManagerUi", Constants.applicationName ) )
			foundations.common.exit( 1, LOGGER, [ LOGGING_SESSION_HANDLER, LOGGING_FILE_HANDLER, LOGGING_CONSOLE_HANDLER ] )

		# --- Activating Preferences Manager Component. ---
		self._preferencesManager = self._componentsManager.getInterface( "core.preferencesManager" )
		if self._preferencesManager :
			SPLASHSCREEN.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.preferencesManager" ) )
			self._preferencesManager.activate( self )
			self._preferencesManager.addWidget()
			self._preferencesManager.initializeUi()
		else:
			messageBox.messageBox( "Critical", "Critical", "Exception In {0}.__init__() Method | '{1}' Component Is Not Available, {2} Will Now Close !".format( self.__class__.__name__, "core.preferencesManager", Constants.applicationName ) )
			foundations.common.exit( 1, LOGGER, [ LOGGING_SESSION_HANDLER, LOGGING_FILE_HANDLER, LOGGING_CONSOLE_HANDLER ] )

		# --- Activating Database Component. ---
		self._coreDb = self._componentsManager.getInterface( "core.db" )
		if self._coreDb :
			SPLASHSCREEN.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.db" ) )
			self._coreDb.activate( self )
			self._coreDb.initialize()
		else:
			messageBox.messageBox( "Critical", "Critical", "Exception In {0}.__init__() Method | '{1}' Component Is Not Available, {2} Will Now Close !".format( self.__class__.__name__, "core.db", Constants.applicationName ) )
			foundations.common.exit( 1, LOGGER, [ LOGGING_SESSION_HANDLER, LOGGING_FILE_HANDLER, LOGGING_CONSOLE_HANDLER ] )

		# --- Activating Collections Outliner Component. ---
		self._coreCollectionsOutliner = self._componentsManager.getInterface( "core.collectionsOutliner" )
		if self._coreCollectionsOutliner :
			SPLASHSCREEN.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.collectionsOutliner" ) )
			self._coreCollectionsOutliner.activate( self )
			self._coreCollectionsOutliner.addWidget()
			self._coreCollectionsOutliner.initializeUi()
		else:
			messageBox.messageBox( "Critical", "Critical", "Exception In {0}.__init__() Method | '{1}' Component Is Not Available, {2} Will Now Close !".format( self.__class__.__name__, "core.collectionsOutliner", Constants.applicationName ) )
			foundations.common.exit( 1, LOGGER, [ LOGGING_SESSION_HANDLER, LOGGING_FILE_HANDLER, LOGGING_CONSOLE_HANDLER ] )

		# --- Activating Database Browser Component. ---
		self._coreDatabaseBrowser = self._componentsManager.getInterface( "core.databaseBrowser" )
		if self._coreDatabaseBrowser :
			SPLASHSCREEN.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.databaseBrowser" ) )
			self._coreDatabaseBrowser.activate( self )
			self._coreDatabaseBrowser.addWidget()
			self._coreDatabaseBrowser.initializeUi()
		else:
			messageBox.messageBox( "Critical", "Critical", "Exception In {0}.__init__() Method | '{1}' Component Is Not Available, {2} Will Now Close !".format( self.__class__.__name__, "core.databaseBrowser", Constants.applicationName ) )
			foundations.common.exit( 1, LOGGER, [ LOGGING_SESSION_HANDLER, LOGGING_FILE_HANDLER, LOGGING_CONSOLE_HANDLER ] )

		# --- Activating Templates Outliner Component. ---
		self._coreTemplatesOutliner = self._componentsManager.getInterface( "core.templatesOutliner" )
		if self._coreTemplatesOutliner :
			SPLASHSCREEN.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, "core.templatesOutliner" ) )
			self._coreTemplatesOutliner.activate( self )
			self._coreTemplatesOutliner.addWidget()
			self._coreTemplatesOutliner.initializeUi()
		else:
			messageBox.messageBox( "Critical", "Critical", "Exception In {0}.__init__() Method | '{1}' Component Is Not Available, {2} Will Now Close !".format( self.__class__.__name__, "core.templatesOutliner", Constants.applicationName ) )
			foundations.common.exit( 1, LOGGER, [ LOGGING_SESSION_HANDLER, LOGGING_FILE_HANDLER, LOGGING_CONSOLE_HANDLER ] )

		# --- Activating Others Components. ---
		deactivatedComponents = self._settings.getKey( "Settings", "DeactivatedComponents" ).toString().split( "," )
		for component in self._componentsManager.getComponents() :
			if component not in deactivatedComponents :
				profile = self._componentsManager.components[component]
				interface = self._componentsManager.getInterface( component )
				if not interface.activated:
					SPLASHSCREEN.setMessage( "{0} - {1} | Activating {2}.".format( self.__class__.__name__, Constants.releaseVersion, component ) )
					interface.activate( self )
					if profile.categorie == "default" :
						interface.initialize()
					elif profile.categorie == "ui" :
						interface.addWidget()
						interface.initializeUi()

		# Hiding Splashscreen.
		LOGGER.debug( " > Hiding SplashScreen." )
		SPLASHSCREEN.setMessage( "{0} - {1} | Initialization Done.".format( self.__class__.__name__, Constants.releaseVersion ) )
		SPLASHSCREEN.hide()

		# --- Running onStartup Components Methods. ---
		for component in self._componentsManager.getComponents() :
			interface = self._componentsManager.getInterface( component )
			if interface.activated:
				hasattr( interface, "onStartup" ) and interface.onStartup()

		# for component in self._componentsManager.getComponents() :
		# 	interface = self._componentsManager.getInterface( component )
		# 	hasattr( interface, "ui" ) and interface.name != "code.databaseBrowser" and interface.ui.hide()

		self.restoreSetsCentricLayout()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
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
	def userApplicationDirectory( self ):
		'''
		This Method Is The Property For The _userApplicationDirectory Attribute.

		@return: self._userApplicationDirectory. ( String )
		'''

		return self._userApplicationDirectory

	@userApplicationDirectory.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def userApplicationDirectory( self, value ):
		'''
		This Method Is The Setter Method For The _userApplicationDirectory Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "userApplicationDirectory" ) )

	@userApplicationDirectory.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def userApplicationDirectory( self ):
		'''
		This Method Is The Deleter Method For The _userApplicationDirectory Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "userApplicationDirectory" ) )

	@property
	def loggingMemoryHandler( self ):
		'''
		This Method Is The Property For The _loggingMemoryHandler Attribute.

		@return: self._loggingMemoryHandler. ( StreamObject )
		'''

		return self._loggingMemoryHandler

	@loggingMemoryHandler.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingMemoryHandler( self, value ):
		'''
		This Method Is The Setter Method For The _loggingMemoryHandler Attribute.

		@param value: Attribute Value. ( StreamObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "loggingMemoryHandler" ) )

	@loggingMemoryHandler.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def loggingMemoryHandler( self ):
		'''
		This Method Is The Deleter Method For The _loggingMemoryHandler Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "loggingMemoryHandler" ) )

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
	def setsCentricLayoutComponents( self ):
		'''
		This Method Is The Property For The _setsCentricLayoutComponents Attribute.

		@return: self._setsCentricLayoutComponents. ( List )
		'''

		return self._setsCentricLayoutComponents

	@setsCentricLayoutComponents.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def setsCentricLayoutComponents( self, value ):
		'''
		This Method Is The Setter Method For The _setsCentricLayoutComponents Attribute.

		@param value: Attribute Value. ( List )
		'''

		if value :
			assert type( value ) is list, "'{0}' Attribute : '{1}' Type Is Not 'list' !".format( "content", value )
		self._setsCentricLayoutComponents = value

	@setsCentricLayoutComponents.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def setsCentricLayoutComponents( self ):
		'''
		This Method Is The Deleter Method For The _setsCentricLayoutComponents Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "setsCentricLayoutComponents" ) )

	@property
	def templatesCentricLayoutComponents( self ):
		'''
		This Method Is The Property For The _templatesCentricLayoutComponents Attribute.

		@return: self._templatesCentricLayoutComponents. ( List )
		'''

		return self._templatesCentricLayoutComponents

	@templatesCentricLayoutComponents.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def templatesCentricLayoutComponents( self, value ):
		'''
		This Method Is The Setter Method For The _templatesCentricLayoutComponents Attribute.

		@param value: Attribute Value. ( List )
		'''

		if value :
			assert type( value ) is list, "'{0}' Attribute : '{1}' Type Is Not 'list' !".format( "content", value )
		self._templatesCentricLayoutComponents = value

	@templatesCentricLayoutComponents.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templatesCentricLayoutComponents( self ):
		'''
		This Method Is The Deleter Method For The _templatesCentricLayoutComponents Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "templatesCentricLayoutComponents" ) )

	@property
	def preferencesCentricLayoutComponents( self ):
		'''
		This Method Is The Property For The _preferencesCentricLayoutComponents Attribute.

		@return: self._preferencesCentricLayoutComponents. ( List )
		'''

		return self._preferencesCentricLayoutComponents

	@preferencesCentricLayoutComponents.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def preferencesCentricLayoutComponents( self, value ):
		'''
		This Method Is The Setter Method For The _preferencesCentricLayoutComponents Attribute.

		@param value: Attribute Value. ( List )
		'''

		if value :
			assert type( value ) is list, "'{0}' Attribute : '{1}' Type Is Not 'list' !".format( "content", value )
		self._preferencesCentricLayoutComponents = value

	@preferencesCentricLayoutComponents.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def preferencesCentricLayoutComponents( self ):
		'''
		This Method Is The Deleter Method For The _preferencesCentricLayoutComponents Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "preferencesCentricLayoutComponents" ) )

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

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def closeEvent( self, event ) :
		'''
		This Method Is Called When Close Event Is Fired.

		@param event: QEvent. ( QEvent )
		'''

		foundations.common.closeHandler( LOGGER, LOGGING_FILE_HANDLER )
		foundations.common.closeHandler( LOGGER, LOGGING_SESSION_HANDLER )
		# foundations.common.closeHandler( LOGGER, LOGGING_CONSOLE_HANDLER )

		self.deleteLater()
		event.accept()

		sIBL_GUI_close()

	@core.executionTrace
	def initializeToolbar( self ):
		'''
		This Method Initializes sIBL_GUI Toolbar.
		'''

		logolabel = QLabel()
		logolabel.setPixmap( QPixmap( UiConstants.frameworkLogoPicture ) )
		self.toolBar.addWidget( logolabel )

		spacer = QWidget()
		spacer.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
		self.toolBar.addWidget( spacer )

		centralWidgetButton = QToolButton()
		centralWidgetButton.setIcon( QIcon( QPixmap( UiConstants.frameworCentralWidgetIcon ) ) )
		self.toolBar.addWidget( centralWidgetButton )

		self.connect( centralWidgetButton, SIGNAL( "clicked()" ), self.centralWidgetButton_OnClicked )

		layoutbutton = QToolButton()
		layoutbutton.setIcon( QIcon( QPixmap( UiConstants.frameworLayoutIcon ) ) )
		layoutbutton.setPopupMode( QToolButton.InstantPopup )

		self._layoutMenu = QMenu( "Layout", layoutbutton )

		restoreSetsCentricLayoutAction = QAction( "Restore Sets Centric Layout", self )
		restoreSetsCentricLayoutAction.setShortcut( QKeySequence( Qt.Key_0 ) )
		restoreTemplatesCentricLayoutAction = QAction( "Restore Templates Centric Layout", self )
		restoreTemplatesCentricLayoutAction.setShortcut( QKeySequence( Qt.Key_9 ) )
		restorePreferencesCentricLayoutAction = QAction( "Restore Preferences Centric Layout", self )
		restorePreferencesCentricLayoutAction.setShortcut( QKeySequence( Qt.Key_8 ) )

		restoreLayoutOneAction = QAction( "Restore Layout 1", self )
		restoreLayoutOneAction.setShortcut( QKeySequence( Qt.Key_1 ) )
		storeLayoutOneAction = QAction( "Store Layout 1", self )
		storeLayoutOneAction.setShortcut( QKeySequence( Qt.CTRL + Qt.Key_1 ) )

		restoreLayoutTwoAction = QAction( "Restore Layout 2", self )
		restoreLayoutTwoAction.setShortcut( QKeySequence( Qt.Key_2 ) )
		storeLayoutTwoAction = QAction( "Store Layout 2", self )
		storeLayoutTwoAction.setShortcut( QKeySequence( Qt.CTRL + Qt.Key_2 ) )

		restoreLayoutThreeAction = QAction( "Restore Layout 3", self )
		restoreLayoutThreeAction.setShortcut( QKeySequence( Qt.Key_3 ) )
		storeLayoutThreeAction = QAction( "Store Layout 3", self )
		storeLayoutThreeAction.setShortcut( QKeySequence( Qt.CTRL + Qt.Key_3 ) )

		restoreLayoutFourAction = QAction( "Restore Layout 4", self )
		restoreLayoutFourAction.setShortcut( QKeySequence( Qt.Key_4 ) )
		storeLayoutFourAction = QAction( "Store Layout 4", self )
		storeLayoutFourAction.setShortcut( QKeySequence( Qt.CTRL + Qt.Key_4 ) )

		restoreLayoutFiveAction = QAction( "Restore Layout 5", self )
		restoreLayoutFiveAction.setShortcut( QKeySequence( Qt.Key_5 ) )
		storeLayoutFiveAction = QAction( "Store Layout 5", self )
		storeLayoutFiveAction.setShortcut( QKeySequence( Qt.CTRL + Qt.Key_5 ) )

		self._layoutMenu.addAction( restoreSetsCentricLayoutAction )
		self._layoutMenu.addAction( restoreTemplatesCentricLayoutAction )
		self._layoutMenu.addAction( restorePreferencesCentricLayoutAction )
		self._layoutMenu.addSeparator()
		self._layoutMenu.addAction( restoreLayoutOneAction )
		self._layoutMenu.addAction( restoreLayoutTwoAction )
		self._layoutMenu.addAction( restoreLayoutThreeAction )
		self._layoutMenu.addAction( restoreLayoutFourAction )
		self._layoutMenu.addAction( restoreLayoutFiveAction )
		self._layoutMenu.addSeparator()
		self._layoutMenu.addAction( storeLayoutOneAction )
		self._layoutMenu.addAction( storeLayoutTwoAction )
		self._layoutMenu.addAction( storeLayoutThreeAction )
		self._layoutMenu.addAction( storeLayoutFourAction )
		self._layoutMenu.addAction( storeLayoutFiveAction )

		# Signals / Slots.
		self.connect( restoreSetsCentricLayoutAction, SIGNAL( "triggered()" ), self.restoreSetsCentricLayoutAction_OnTriggered )
		self.connect( restoreTemplatesCentricLayoutAction, SIGNAL( "triggered()" ), self.restoreTemplatesCentricLayoutAction_OnTriggered )
		self.connect( restorePreferencesCentricLayoutAction, SIGNAL( "triggered()" ), self.restorePreferencesCentricLayoutAction_OnTriggered )
		self.connect( restoreLayoutOneAction, SIGNAL( "triggered()" ), self.restoreLayoutOneAction_OnTriggered )
		self.connect( restoreLayoutTwoAction, SIGNAL( "triggered()" ), self.restoreLayoutTwoAction_OnTriggered )
		self.connect( restoreLayoutThreeAction, SIGNAL( "triggered()" ), self.restoreLayoutThreeAction_OnTriggered )
		self.connect( restoreLayoutFourAction, SIGNAL( "triggered()" ), self.restoreLayoutFourAction_OnTriggered )
		self.connect( restoreLayoutFiveAction, SIGNAL( "triggered()" ), self.restoreLayoutFiveAction_OnTriggered )
		self.connect( storeLayoutOneAction, SIGNAL( "triggered()" ), self.storeLayoutOneAction_OnTriggered )
		self.connect( storeLayoutTwoAction, SIGNAL( "triggered()" ), self.storeLayoutTwoAction_OnTriggered )
		self.connect( storeLayoutThreeAction, SIGNAL( "triggered()" ), self.storeLayoutThreeAction_OnTriggered )
		self.connect( storeLayoutFourAction, SIGNAL( "triggered()" ), self.storeLayoutFourAction_OnTriggered )
		self.connect( storeLayoutFiveAction, SIGNAL( "triggered()" ), self.storeLayoutFiveAction_OnTriggered )

		layoutbutton.setMenu( self._layoutMenu )

		self.toolBar.addWidget( layoutbutton )

		miscButton = QToolButton()
		miscButton.setIcon( QIcon( QPixmap( UiConstants.frameworkMiscIcon ) ) )
		miscButton.setPopupMode( QToolButton.InstantPopup )

		helpDisplayMiscAction = QAction( "Help Content ...", self )
		apiDisplayMiscAction = QAction( "Api Content ...", self )

		self._miscMenu = QMenu( "Miscellaneous", miscButton )

		self._miscMenu.addAction( helpDisplayMiscAction )
		self._miscMenu.addAction( apiDisplayMiscAction )
		self._miscMenu.addSeparator()

		# Signals / Slots.
		self.connect( helpDisplayMiscAction, SIGNAL( "triggered()" ), self.helpDisplayMiscAction_OnTriggered )
		self.connect( apiDisplayMiscAction, SIGNAL( "triggered()" ), self.apiDisplayMiscAction_OnTriggered )

		miscButton.setMenu( self._miscMenu )

		self.toolBar.addWidget( miscButton )

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
	def storeLayout( self, name ):
		'''
		This Method Is Called When Storing A Layout.

		@param name: Layout Name. ( String )
		'''

		LOGGER.debug( " > Storing Layout '{0}'.".format( name ) )

		self._settings.setKey( "Layouts", "{0}_geometry".format( name ), self.saveGeometry() )
		self._settings.setKey( "Layouts", "{0}_windowState".format( name ), self.saveState() )
		self._settings.setKey( "Layouts", "{0}_centralWidget".format( name ), self.centralwidget.isVisible() )

	@core.executionTrace
	def restoreLayout( self, name ):
		'''
		This Method Is Called When Restoring A Layout.

		@param name: Layout Name. ( String )
		'''

		LOGGER.debug( " > Restoring Layout '{0}'.".format( name ) )


		#self.hide()
		self.centralwidget.setVisible( self._settings.getKey( "Layouts", "{0}_centralWidget".format( name ) ).toBool() )
		self.restoreState( self._settings.getKey( "Layouts", "{0}_windowState".format( name ) ).toByteArray() )
		self.restoreGeometry( self._settings.getKey( "Layouts", "{0}_geometry".format( name ) ).toByteArray() )
		#self.show()
		QApplication.focusWidget() and QApplication.focusWidget().clearFocus()

	@core.executionTrace
	def restoreSetsCentricLayout( self ):
		'''
		This Method Restores The Sets Centric Layout.
		'''

		for component, profile in self._componentsManager.components.items() :
			profile.categorie == "ui" and component not in self._setsCentricLayoutComponents and self._componentsManager.getInterface( component ).ui and self._componentsManager.getInterface( component ).ui.hide()
		self.restoreLayout( "setsCentric" )

	@core.executionTrace
	def restoreSetsCentricLayoutAction_OnTriggered( self ):
		'''
		This Method Is Called When Restoring Sets Centric Layout.
		'''

		self.restoreSetsCentricLayout()

	@core.executionTrace
	def restoreTemplatesCentricLayout( self ):
		'''
		This Method Restores The Templates Centric Layout.
		'''

		for component, profile in self._componentsManager.components.items() :
			profile.categorie == "ui" and component not in self._templatesCentricLayoutComponents and self._componentsManager.getInterface( component ).ui and self._componentsManager.getInterface( component ).ui.hide()
		self.restoreLayout( "templatesCentric" )

	@core.executionTrace
	def restoreTemplatesCentricLayoutAction_OnTriggered( self ):
		'''
		This Method Is Called When Restoring Templates Centric Layout.
		'''

		self.restoreTemplatesCentricLayout()

	@core.executionTrace
	def restorePreferencesCentricLayout( self ):
		'''
		This Method Restores The Preferences Centric Layout.
		'''

		for component, profile in self._componentsManager.components.items() :
			profile.categorie == "ui" and component not in self._preferencesCentricLayoutComponents and self._componentsManager.getInterface( component ).ui and self._componentsManager.getInterface( component ).ui.hide()
		self.restoreLayout( "preferencesCentric" )

	@core.executionTrace
	def restorePreferencesCentricLayoutAction_OnTriggered( self ):
		'''
		This Method Is Called When Restoring Preferences Centric Layout.
		'''

		self.restorePreferencesCentricLayout()

	@core.executionTrace
	def restoreLayoutOneAction_OnTriggered( self ):
		'''
		This Method Is Called When Restoring Layout One.
		'''

		self.restoreLayout( "one" )

	@core.executionTrace
	def restoreLayoutTwoAction_OnTriggered( self ):
		'''
		This Method Is Called When Restoring Layout Two.
		'''

		self.restoreLayout( "two" )

	@core.executionTrace
	def restoreLayoutThreeAction_OnTriggered( self ):
		'''
		This Method Is Called When Restoring Layout Three.
		'''

		self.restoreLayout( "three" )

	@core.executionTrace
	def restoreLayoutFourAction_OnTriggered( self ):
		'''
		This Method Is Called When Restoring Layout Four.
		'''

		self.restoreLayout( "four" )

	@core.executionTrace
	def restoreLayoutFiveAction_OnTriggered( self ):
		'''
		This Method Is Called When Restoring Layout Five.
		'''

		self.restoreLayout( "five" )

	@core.executionTrace
	def storeLayoutOneAction_OnTriggered( self ):
		'''
		This Method Is Called When Storing Layout One.
		'''

		self.storeLayout( "one" )

	@core.executionTrace
	def storeLayoutTwoAction_OnTriggered( self ):
		'''
		This Method Is Called When Storing Layout Two.
		'''

		self.storeLayout( "two" )

	@core.executionTrace
	def storeLayoutThreeAction_OnTriggered( self ):
		'''
		This Method Is Called When Storing Layout Three.
		'''

		self.storeLayout( "three" )

	@core.executionTrace
	def storeLayoutFourAction_OnTriggered( self ):
		'''
		This Method Is Called When Storing Layout Four.
		'''

		self.storeLayout( "four" )

	@core.executionTrace
	def storeLayoutFiveAction_OnTriggered( self ):
		'''
		This Method Is Called When Storing Layout Five.
		'''

		self.storeLayout( "five" )

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
def sIBL_GUI_start():
	'''
	This Method Is Called When sIBL_GUI Starts.
	'''

	global USER_DATAS_DIRECTORY
	global USER_APPLICATION_DIRECTORY
	global GUI_LOGGING_FILE
	global LOGGING_FILE_HANDLER
	global SETTINGS_FILE
	global SETTINGS
	global VERBOSITY_LEVEL
	global APPLICATION
	global SPLASHSCREEN_PICTURE
	global SPLASHSCREEN
	global LOGGING_SESSION_HANDLER_STREAM
	global LOGGING_SESSION_HANDLER
	global UI

	# Setting User Preferences Directory.
	USER_DATAS_DIRECTORY = foundations.common.getSystemApplicationDatasDirectory()
	USER_APPLICATION_DIRECTORY = foundations.common.getUserApplicationDatasDirectory()

	if USER_DATAS_DIRECTORY :
		setApplicationPreferencesDirectories( USER_DATAS_DIRECTORY ) or messageBox.standaloneMessageBox( "Error", "Error", "{0} Has Encountered An Error And Will Now Close !".format( Constants.applicationName ) ) or foundations.common.exit( 1, LOGGER, [ LOGGING_CONSOLE_HANDLER, LOGGING_SESSION_HANDLER ] )
	else :
		messageBox.standaloneMessageBox( "Error", "Error", "'{0}' User Application Datas Directory Is Not Available, {1} Will Now Close !".format( USER_DATAS_DIRECTORY, Constants.applicationName ) )
		foundations.common.exit( 1, LOGGER, [ LOGGING_CONSOLE_HANDLER ] )

	# Getting The Logging File Path.
	GUI_LOGGING_FILE = os.path.join( USER_APPLICATION_DIRECTORY, Constants.loggingDirectory, Constants.loggingFile )

	try :
		os.path.exists( GUI_LOGGING_FILE ) and os.remove( GUI_LOGGING_FILE )
	except :
		messageBox.standaloneMessageBox( "Error", "Error", "{0} File Is Currently Locked, Unpredictable Application Behavior !".format( GUI_LOGGING_FILE ) )

	try :
		LOGGING_FILE_HANDLER = logging.FileHandler( GUI_LOGGING_FILE )
		LOGGING_FILE_HANDLER.setFormatter( core.LOGGING_FORMATTER )
		LOGGER.addHandler( LOGGING_FILE_HANDLER )
	except Exception as error:
		foundations.exceptions.defaultExceptionsHandler( error, Constants.applicationName )
		messageBox.standaloneMessageBox( "Critical", "Critical", "Exception In {0} Module | Logging File Is Not Available, {0} Will Now Close !".format( Constants.applicationName ) )
		foundations.common.exit( 1, LOGGER, [ LOGGING_CONSOLE_HANDLER ] )

	# Retrieving Framework Verbose Level From Settings File.
	LOGGER.debug( "> Initializing {0} !".format( Constants.applicationName ) )
	LOGGER.debug( "> Retrieving Stored Verbose Level." )

	SETTINGS_FILE = os.path.join( USER_APPLICATION_DIRECTORY, Constants.settingsDirectory, Constants.settingsFile )

	SETTINGS = Preferences( SETTINGS_FILE )

	os.path.exists( SETTINGS_FILE ) or SETTINGS.setDefaultPreferences()

	VERBOSITY_LEVEL = SETTINGS.getKey( "Settings", "VerbosityLevel" ).toInt()[0]
	LOGGER.debug( "> Setting Logger Verbosity Level To : '{0}'.".format( VERBOSITY_LEVEL ) )
	core.setVerbosityLevel( VERBOSITY_LEVEL )

	if hasattr( sys, "frozen" ) :
		foundations.common.closeHandler ( LOGGER, LOGGING_CONSOLE_HANDLER )

	# Starting The Session Handler.
	LOGGING_SESSION_HANDLER_STREAM = StreamObject()
	LOGGING_SESSION_HANDLER = logging.StreamHandler( LOGGING_SESSION_HANDLER_STREAM )
	LOGGING_SESSION_HANDLER.setFormatter( core.LOGGING_FORMATTER )
	LOGGER.addHandler( LOGGING_SESSION_HANDLER )

	LOGGER.info( Constants.loggingSeparators )
	LOGGER.info( "{0} | Copyright ( C ) 2008 - 2010 Thomas Mansencal - kelsolaar_fool@hotmail.com".format( Constants.applicationName ) )
	LOGGER.info( "{0} | This Software Is Released Under Terms Of GNU GPL V3 License.".format( Constants.applicationName ) )
	LOGGER.info( "{0} | http://www.gnu.org/licenses/ ".format( Constants.applicationName ) )
	LOGGER.info( "{0} | Version : {1}".format( Constants.applicationName, Constants.releaseVersion ) )
	LOGGER.info( "{0} | Session Started At : {1}".format( Constants.applicationName, time.strftime( '%X - %x' ) ) )
	LOGGER.info( Constants.loggingSeparators )
	LOGGER.info( "{0} | Starting Interface !".format( Constants.applicationName ) )

	APPLICATION = QApplication( sys.argv )

	# Initializing SplashScreen.
	LOGGER.debug( "> Initializing SplashScreen." )

	SPLASHSCREEN_PICTURE = QPixmap( UiConstants.frameworkSplashScreenPicture )
	SPLASHSCREEN = Delayed_QSplashScreen( SPLASHSCREEN_PICTURE, 0.05 )
	SPLASHSCREEN.setMessage( "{0} - {1} | Initializing {0}.".format( Constants.applicationName, Constants.releaseVersion ) )
	SPLASHSCREEN.show()

	UI = sIBL_GUI()
	UI.show()
	UI.raise_()

	sys.exit( APPLICATION.exec_() )

@core.executionTrace
def sIBL_GUI_close() :
	'''
	This Method Is Called When sIBL_GUI Closes.
	'''

	LOGGER.info( "{0} | Closing Interface ! ".format( Constants.applicationName ) )
	LOGGER.info( Constants.loggingSeparators )
	LOGGER.info( "{0} | Session Ended At : {1}".format( Constants.applicationName, time.strftime( '%X - %x' ) ) )
	LOGGER.info( Constants.loggingSeparators )

	foundations.common.exit( 0, LOGGER, [ LOGGING_CONSOLE_HANDLER ] )

@core.executionTrace
def setApplicationPreferencesDirectories( path ):
	'''
	This Method Sets The Application Preferences Directory.

	@param path: Starting Point For The Directories Tree Creation. ( String )
	'''

	applicationDirectory = USER_APPLICATION_DIRECTORY

	LOGGER.debug( "> Current Application Preferences Directory '{0}'.".format( applicationDirectory ) )
	if io.setLocalDirectory( applicationDirectory ) :
		for directory in Constants.preferencesDirectories :
				io.setLocalDirectory( os.path.join( applicationDirectory, directory ) ) or messageBox.standaloneMessageBox( "Critical", "Critical", "'{0}' Directory Creation Failed !".format( os.path.join( applicationDirectory, directory ) ) )
		return True
	else :
		messageBox.standaloneMessageBox( "Error", "Error", "'{0}' Directory Creation Failed !".format( applicationDirectory ) )

#***********************************************************************************************
#***	Launcher
#***********************************************************************************************
if __name__ == "__main__":
	sIBL_GUI_start()
	# TODO: Make Documentations.
	# TODO: Saves Default Layouts.
	# TODO: Better Component Comments.
	# TODO: Add Origin In Templates.
#***********************************************************************************************
#***	Python End
#***********************************************************************************************
