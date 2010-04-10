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
***	onlineUpdater.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Online Updater Component Module.
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
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.common
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import ui.widgets.messageBox as messageBox
from foundations.io import File
from foundations.parser import Parser
from globals.constants import Constants
from manager.uiComponent import UiComponent
from ui.widgets.variable_QPushButton import Variable_QPushButton

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

REPOSITORY_URL = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Repository/"

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class ReleaseObject( core.Structure ):
	'''
	This Is The ReleaseObject Class.
	'''

	@core.executionTrace
	def __init__( self, **kwargs ):
		'''
		This Method Initializes The Class.

		@param kwargs: name, repositoryVersion, localVersion, type, comment. ( Key / Value Pairs )
		'''

		core.Structure.__init__( self, **kwargs )

		# --- Setting Class Attributes. ---
		self.__dict__.update( kwargs )

class RemoteUpdater( object ):
	'''
	This Class Is The RemoteUpdater Class.
	'''

	@core.executionTrace
	def __init__( self, releases = None ):
		'''
		This Method Initializes The Class.
		
		@param releases: Releases. ( Dictionary )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		# --- Setting Class Attributes. ---
		self._releases = None
		self.releases = releases
		self._uiPath = "ui/Remote_Updater.ui"
		self._uiFile = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiPath )
		self._uiResources = "resources/"
		self._uiResources = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiResources )
		self._uiLogoIcon = "sIBL_GUI_Small_Logo.png"

		self._applicationChangeLogUrl = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Change%20Log/Change%20Log.html"

		self._uiGreenColor = QColor( 128, 192, 128 )
		self._uiRedColor = QColor( 192, 128, 128 )

#		self._templatesUrl = "templates/"
#		self._sIBL_GUI_BuildsUrl = "builds/"

		self._templatesTableWidgetHeaders = ["Get It !", "Local Version", "Repository Version", "Release Type", "Comment"]

		self._ui = uic.loadUi( self._uiFile )
		if "." in sys.path :
			sys.path.remove( "." )
		self.initializeUi()
		self._ui.show()

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
	def uiFile( self ):
		'''
		This Method Is The Property For The _uiFile Attribute.

		@return: self._uiFile. ( String )
		'''

		return self._uiFile

	@uiFile.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiFile( self, value ):
		'''
		This Method Is The Setter Method For The _uiFile Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiFile" ) )

	@uiFile.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiFile( self ):
		'''
		This Method Is The Deleter Method For The _uiFile Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiFile" ) )

	@property
	@core.executionTrace
	def uiResources( self ):
		'''
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		'''

		return self._uiResources

	@uiResources.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self, value ):
		'''
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiResources" ) )

	@uiResources.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self ):
		'''
		This Method Is The Deleter Method For The _uiResources Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiResources" ) )

	@property
	@core.executionTrace
	def uiLogoIcon( self ):
		'''
		This Method Is The Property For The _uiLogoIcon Attribute.

		@return: self._uiLogoIcon. ( String )
		'''

		return self._uiLogoIcon

	@uiLogoIcon.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLogoIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiLogoIcon Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiLogoIcon" ) )

	@uiLogoIcon.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLogoIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiLogoIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiLogoIcon" ) )

	@property
	@core.executionTrace
	def releases( self ):
		'''
		This Method Is The Property For The _releases Attribute.

		@return: self._releases. ( Dictionary )
		'''

		return self._releases

	@releases.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def releases( self, value ):
		'''
		This Method Is The Setter Method For The _releases Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		'''

		if value :
			assert type( value ) is dict, "'{0}' Attribute : '{1}' Type Is Not 'dict' !".format( "releases", value )
		self._releases = value

	@releases.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def releases( self ):
		'''
		This Method Is The Deleter Method For The _releases Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "releases" ) )

	@property
	@core.executionTrace
	def templatesTableWidgetHeaders( self ):
		'''
		This Method Is The Property For The _templatesTableWidgetHeaders Attribute.

		@return: self._templatesTableWidgetHeaders. ( String )
		'''

		return self._templatesTableWidgetHeaders

	@templatesTableWidgetHeaders.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templatesTableWidgetHeaders( self, value ):
		'''
		This Method Is The Setter Method For The _templatesTableWidgetHeaders Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "templatesTableWidgetHeaders" ) )

	@templatesTableWidgetHeaders.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templatesTableWidgetHeaders( self ):
		'''
		This Method Is The Deleter Method For The _templatesTableWidgetHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "templatesTableWidgetHeaders" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Widget Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Ui.".format( self.__class__.__name__ ) )

		if Constants.applicationName not in self._releases :
			self._ui.sIBL_GUI_groupBox.hide()
		else :
			self._ui.Logo_label.setPixmap( QPixmap( os.path.join( self._uiResources, self._uiLogoIcon ) ) )
			self._ui.Your_Version_label.setText( self._releases[Constants.applicationName].localVersion )
			self._ui.Latest_Version_label.setText( self._releases[Constants.applicationName].repositoryVersion )
			self._ui.Change_Log_webView.load( QUrl.fromEncoded( QByteArray( self._applicationChangeLogUrl ) ) )

		if not len( self._releases ):
			self._ui.Templates_groupBox.hide()
		else :
			if Constants.applicationName in self._releases :
				templatesReleases = dict( self._releases )
				templatesReleases.pop( Constants.applicationName )
			else :
				templatesReleases = self._releases

			self._ui.Templates_tableWidget.clear()
			self._ui.Templates_tableWidget.setEditTriggers( QAbstractItemView.NoEditTriggers )
			self._ui.Templates_tableWidget.setRowCount( len( templatesReleases ) )
			self._ui.Templates_tableWidget.setColumnCount( len( self._templatesTableWidgetHeaders ) )
			self._ui.Templates_tableWidget.setHorizontalHeaderLabels( self._templatesTableWidgetHeaders )
			self._ui.Templates_tableWidget.horizontalHeader().setStretchLastSection( True )

			verticalHeaderLabels = []
			for row, release in enumerate( templatesReleases ) :
					verticalHeaderLabels.append( release )

					item = Variable_QPushButton( True, ( self._uiGreenColor, self._uiRedColor ), ( "Yes", "No" ) )
					self._ui.Templates_tableWidget.setCellWidget( row, 0, item )

					tableWidgetItem = QTableWidgetItem( templatesReleases[release].localVersion or Constants.nullObject )
					tableWidgetItem.setTextAlignment( Qt.AlignCenter )
					self._ui.Templates_tableWidget.setItem( row, 1, tableWidgetItem )

					tableWidgetItem = QTableWidgetItem( templatesReleases[release].repositoryVersion )
					tableWidgetItem.setTextAlignment( Qt.AlignCenter )
					self._ui.Templates_tableWidget.setItem( row, 2, tableWidgetItem )

					tableWidgetItem = QTableWidgetItem( templatesReleases[release].type )
					tableWidgetItem.setTextAlignment( Qt.AlignCenter )
					self._ui.Templates_tableWidget.setItem( row, 3, tableWidgetItem )

					tableWidgetItem = QTableWidgetItem( templatesReleases[release].comment )
					self._ui.Templates_tableWidget.setItem( row, 4, tableWidgetItem )

			self._ui.Templates_tableWidget.setVerticalHeaderLabels( verticalHeaderLabels )
			self._ui.Templates_tableWidget.resizeColumnsToContents()

class OnlineUpdater( UiComponent ):
	'''
	This Class Is The OnlineUpdater Class.
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

		self._uiPath = "ui/Online_Updater.ui"
		self._dockArea = 8

		self._container = None
		self._settings = None

		self._corePreferencesManager = None

		self._ioDirectory = None

		self._repositoryUrl = REPOSITORY_URL
		self._releasesFileUrl = "sIBL_GUI_Releases.rc"

		self._remoteUpdater = None

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
	def dockArea( self ):
		'''
		This Method Is The Property For The _dockArea Attribute.

		@return: self._dockArea. ( Integer )
		'''

		return self._dockArea

	@dockArea.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self, value ):
		'''
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dockArea" ) )

	@dockArea.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self ):
		'''
		This Method Is The Deleter Method For The _dockArea Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dockArea" ) )

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
	def coreDb( self ):
		'''
		This Method Is The Property For The _coreDb Attribute.

		@return: self._coreDb. ( Object )
		'''

		return self._coreDb

	@coreDb.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self, value ):
		'''
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDb" ) )

	@coreDb.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self ):
		'''
		This Method Is The Deleter Method For The _coreDb Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDb" ) )

	@property
	@core.executionTrace
	def ioDirectory( self ):
		'''
		This Method Is The Property For The _ioDirectory Attribute.

		@return: self._ioDirectory. ( String )
		'''

		return self._ioDirectory

	@ioDirectory.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ioDirectory( self, value ):
		'''
		This Method Is The Setter Method For The _ioDirectory Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "ioDirectory" ) )

	@ioDirectory.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ioDirectory( self ):
		'''
		This Method Is The Deleter Method For The _ioDirectory Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "ioDirectory" ) )

	@property
	@core.executionTrace
	def repositoryUrl( self ):
		'''
		This Method Is The Property For The _repositoryUrl Attribute.

		@return: self._repositoryUrl. ( String )
		'''

		return self._repositoryUrl

	@repositoryUrl.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def repositoryUrl( self, value ):
		'''
		This Method Is The Setter Method For The _repositoryUrl Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "repositoryUrl" ) )

	@repositoryUrl.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def repositoryUrl( self ):
		'''
		This Method Is The Deleter Method For The _repositoryUrl Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "repositoryUrl" ) )

	@property
	@core.executionTrace
	def releasesFileUrl( self ):
		'''
		This Method Is The Property For The _releasesFileUrl Attribute.

		@return: self._releasesFileUrl. ( String )
		'''

		return self._releasesFileUrl

	@releasesFileUrl.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def releasesFileUrl( self, value ):
		'''
		This Method Is The Setter Method For The _releasesFileUrl Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "releasesFileUrl" ) )

	@releasesFileUrl.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def releasesFileUrl( self ):
		'''
		This Method Is The Deleter Method For The _releasesFileUrl Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "releasesFileUrl" ) )

	@property
	@core.executionTrace
	def remoteUpdater( self ):
		'''
		This Method Is The Property For The _remoteUpdater Attribute.

		@return: self._remoteUpdater. ( Object )
		'''

		return self._remoteUpdater

	@remoteUpdater.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def remoteUpdater( self, value ):
		'''
		This Method Is The Setter Method For The _remoteUpdater Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "remoteUpdater" ) )

	@remoteUpdater.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def remoteUpdater( self ):
		'''
		This Method Is The Deleter Method For The _remoteUpdater Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "remoteUpdater" ) )

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

		self._corePreferencesManager = self._container.componentsManager.components["core.preferencesManager"].interface
		self._coreDb = self._container.componentsManager.components["core.db"].interface

		self._ioDirectory = os.path.join( self._container.userApplicationDirectory, Constants.ioDirectory )

		self._networkAccessManager = QNetworkAccessManager()

		self._networkAccessManager.connect( self._networkAccessManager, SIGNAL( "finished(QNetworkReply *)" ), self.networkAccessManager_OnReplyFinished )

		self._remoteStack = {}

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug( "> Deactivating '{0}' Component.".format( self.__class__.__name__ ) )

		self.uiFile = None
		self._container = None

		self._corePreferencesManager = None
		self._coreDb = None

		self._ioDirectory = None

		self._networkAccessManager = None

		self._remoteStack = None

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		# Signals / Slots.
		self.ui.Check_For_New_Releases_pushButton.connect( self.ui.Check_For_New_Releases_pushButton, SIGNAL( "clicked()" ), self.Check_For_New_Releases_pushButton_OnClicked )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		# Signals / Slots.
		self.ui.Check_For_New_Releases_pushButton.disconnect( self.ui.Check_For_New_Releases_pushButton, SIGNAL( "clicked()" ), self.Check_For_New_Releases_pushButton_OnClicked )

	@core.executionTrace
	def addWidget( self ):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug( "> Adding '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget( self.ui.Online_Updater_groupBox )

	@core.executionTrace
	def removeWidget( self ):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug( "> Removing '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self.ui.Online_Updater_groupBox.setParent( None )

	@core.executionTrace
	def Check_For_New_Releases_pushButton_OnClicked( self ):
		'''
		This Method Is Triggered When Check_For_New_Releases_pushButton Is Clicked.
		'''

		self.checkForNewReleases()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.NetworkError )
	def networkAccessManager_OnReplyFinished( self, reply ):
		'''
		This Method Is Triggered When The networkAccessManager Reply Finishes.
		'''

		if not reply.error():
			content = []
			while not reply.atEnd () :
				content.append( str( reply.readLine() ) )

			parser = Parser()
			parser.content = content
			parser.parse()

			releases = {}
			for remoteObject in parser.sections :
				if remoteObject != Constants.applicationName :
					dbTemplates = dbUtilities.common.filterTemplates( self._coreDb.dbSession, "^{0}$".format( remoteObject ), "name" )
					dbTemplate = dbTemplates and [dbTemplate[0] for dbTemplate in sorted( [( dbTemplate, dbTemplate.release ) for dbTemplate in dbTemplates], reverse = True, key = lambda x:( strings.getVersionRank( x[1] ) ) )][0] or None
					if dbTemplate :
						if dbTemplate.release != parser.getValue( "Release", remoteObject ) :
							releases[remoteObject] = ReleaseObject( name = remoteObject, repositoryVersion = parser.getValue( "Release", remoteObject ), localVersion = dbTemplate.release, type = parser.getValue( "Type", remoteObject ), comment = parser.getValue( "Comment", remoteObject ) )
					else :
							releases[remoteObject] = ReleaseObject( name = remoteObject, repositoryVersion = parser.getValue( "Release", remoteObject ), localVersion = None, type = parser.getValue( "Type", remoteObject ), comment = parser.getValue( "Comment", remoteObject ) )
				else :
					if Constants.releaseVersion != parser.getValue( "Release", remoteObject ) :
						releases[remoteObject] = ReleaseObject( name = remoteObject, repositoryVersion = parser.getValue( "Release", remoteObject ), localVersion = Constants.releaseVersion, type = parser.getValue( "Type", remoteObject ), comment = None )
			if releases :
				self._remoteUpdater = RemoteUpdater( releases )
			else :
				messageBox.messageBox( "Informations", "Informations", "{0} | '{1}' Is Up To Date !".format( self.__class__.__name__, Constants.applicationName ) )
		else:
			raise foundations.exceptions.NetworkError( "QNetworkAccessManager Error Code : '{0}'.".format( reply.error() ) )

	@core.executionTrace
	def checkForNewReleases( self ):
		'''
		This Method Checks For New Releases.
		'''

		self.getReleaseFile( QUrl( os.path.join( self._repositoryUrl, self._releasesFileUrl ) ) )

	@core.executionTrace
	def getReleaseFile( self, url ):
		'''
		This Method Gets A Remote File.
		'''

		self._networkAccessManager.get( QNetworkRequest( url ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
