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
import platform
import sys
from new import instancemethod
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
from foundations.pkzip import Pkzip
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

		@param kwargs: name, repositoryVersion, localVersion, type, url, comment. ( Key / Value Pairs )
		'''

		core.Structure.__init__( self, **kwargs )

		# --- Setting Class Attributes. ---
		self.__dict__.update( kwargs )

class DownloadManager( QObject ):
	'''
	This Is The DownloadManager Class.
	'''

	@core.executionTrace
	def __init__( self, container, networkAccessManager, downloadFolder, requests = None ):
		'''
		This Method Initializes The Class.
		
		@param container: Container. ( Object )
		@param networkAccessManager: Network Access Manager. ( QNetworkAccessManager )
		@param downloadFolder: Download Folder. ( String )
		@param requests: Download Requests. ( List )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		QObject.__init__( self )

		# --- Setting Class Attributes. ---
		self._container = container
		self._networkAccessManager = networkAccessManager
		self._downloadFolder = downloadFolder

		self._uiPath = "ui/Download_Manager.ui"
		self._uiPath = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiPath )
		self._uiResources = "resources/"
		self._uiResources = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiResources )
		self._uiLogoIcon = "sIBL_GUI_Small_Logo.png"

		self._requests = None
		self.requests = requests
		self._downloads = []
		self._currentRequest = None

		# Helper Attribute For QNetwork Reply Crash.
		self._downloadStatus = None

		self._ui = uic.loadUi( self._uiPath )
		if "." in sys.path :
			sys.path.remove( "." )

		self.initializeUi()
		self._ui.show()

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
	def networkAccessManager( self ):
		'''
		This Method Is The Property For The _networkAccessManager Attribute.

		@return: self._networkAccessManager. ( QNetworkAccessManager )
		'''

		return self._networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def networkAccessManager( self, value ):
		'''
		This Method Is The Setter Method For The _networkAccessManager Attribute.

		@param value: Attribute Value. ( QNetworkAccessManager )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "networkAccessManager" ) )

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def networkAccessManager( self ):
		'''
		This Method Is The Deleter Method For The _networkAccessManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "networkAccessManager" ) )

	@property
	def downloadFolder( self ):
		'''
		This Method Is The Property For The _downloadFolder Attribute.

		@return: self._downloadFolder. ( String )
		'''

		return self._downloadFolder

	@downloadFolder.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def downloadFolder( self, value ):
		'''
		This Method Is The Setter Method For The _downloadFolder Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "downloadFolder" ) )

	@downloadFolder.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def downloadFolder( self ):
		'''
		This Method Is The Deleter Method For The _downloadFolder Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "downloadFolder" ) )

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
	def uiLogoIcon( self ):
		'''
		This Method Is The Property For The _uiLogoIcon Attribute.

		@return: self._uiLogoIcon. ( String )
		'''

		return self._uiLogoIcon

	@uiLogoIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLogoIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiLogoIcon Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiLogoIcon" ) )

	@uiLogoIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLogoIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiLogoIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiLogoIcon" ) )

	@property
	def requests( self ):
		'''
		This Method Is The Property For The _requests Attribute.

		@return: self._requests. ( List )
		'''

		return self._requests

	@requests.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def requests( self, value ):
		'''
		This Method Is The Setter Method For The _requests Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		'''

		if value :
			assert type( value ) is list, "'{0}' Attribute : '{1}' Type Is Not 'list' !".format( "requests", value )
		self._requests = value

	@requests.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def requests( self ):
		'''
		This Method Is The Deleter Method For The _requests Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "requests" ) )

	@property
	def downloads( self ):
		'''
		This Method Is The Property For The _downloads Attribute.

		@return: self._downloads. ( List )
		'''

		return self._downloads

	@downloads.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def downloads( self, value ):
		'''
		This Method Is The Setter Method For The _downloads Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "downloads" ) )

	@downloads.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def downloads( self ):
		'''
		This Method Is The Deleter Method For The _downloads Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "downloads" ) )

	@property
	def currentRequest( self ):
		'''
		This Method Is The Property For The _currentRequest Attribute.

		@return: self._currentRequest. ( QNetworkReply )
		'''

		return self._currentRequest

	@currentRequest.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def currentRequest( self, value ):
		'''
		This Method Is The Setter Method For The _currentRequest Attribute.

		@param value: Attribute Value. ( QNetworkReply )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "currentRequest" ) )

	@currentRequest.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def currentRequest( self ):
		'''
		This Method Is The Deleter Method For The _currentRequest Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "currentRequest" ) )

	@property
	def downloadStatus( self ):
		'''
		This Method Is The Property For The _downloadStatus Attribute.

		@return: self._downloadStatus. ( QObject )
		'''

		return self._downloadStatus

	@downloadStatus.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def downloadStatus( self, value ):
		'''
		This Method Is The Setter Method For The _downloadStatus Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "downloadStatus" ) )

	@downloadStatus.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def downloadStatus( self ):
		'''
		This Method Is The Deleter Method For The _downloadStatus Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "downloadStatus" ) )

	@property
	def ui( self ):
		'''
		This Method Is The Property For The _ui Attribute.

		@return: self._ui. ( Object )
		'''

		return self._ui

	@ui.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ui( self, value ):
		'''
		This Method Is The Setter Method For The _ui Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "ui" ) )

	@ui.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ui( self ):
		'''
		This Method Is The Deleter Method For The _ui Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "ui" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Widget Ui.
		'''

		self._ui.Download_progressBar.setValue( 0 )
		self._ui.Download_progressBar.hide()
		self._ui.Logo_label.setPixmap( QPixmap( os.path.join( self._uiResources, self._uiLogoIcon ) ) )

		self._ui.closeEvent = self.closeEvent

		# Signals / Slots.
		self._ui.Cancel_Close_pushButton.connect( self._ui.Cancel_Close_pushButton, SIGNAL( "clicked()" ), self.Cancel_Close_pushButton_OnClicked )

	@core.executionTrace
	def closeEvent( self, closeEvent ):
		'''
		This Method Overloads The DownloadManager CloseEvent.
		
		@param closeEvent: Close Event. ( QCloseEvent )
		'''

		self._downloadStatus or self.abortDownload()
		closeEvent.accept()

	@core.executionTrace
	def Cancel_Close_pushButton_OnClicked( self ):
		'''
		This Method Triggers The DownloadManager Close.
		'''

		self._ui.close()

	@core.executionTrace
	def downloadNext( self ):
		'''
		This Method Downloads The Next Request.
		'''

		if self._requests :
			self._ui.Download_progressBar.show()

			self._currentRequest = self._networkAccessManager.get( QNetworkRequest( QUrl( self._requests.pop() ) ) )

			# Signals / Slots.
			self._currentRequest.connect( self._currentRequest, SIGNAL( "downloadProgress( qint64, qint64 )" ), self.downloadProgress )
			self._currentRequest.connect( self._currentRequest, SIGNAL( "finished()" ), self.downloadFinished )
			self._currentRequest.connect( self._currentRequest, SIGNAL( "readyRead()" ), self.requestReady )

	@core.executionTrace
	def downloadProgress( self, bytesReceived, bytesTotal ):
		'''
		This Method Updates The Download Progress.
		
		@param bytesReceived: Bytes Received. ( Integer )
		@param bytesTotal: Bytes Total. ( Integer )
		'''

		self._ui.Current_File_label.setText( "Downloading : '{0}'.".format( os.path.basename( str( self._currentRequest.url().path() ) ) ) )
		self._ui.Download_progressBar.setRange( 0, bytesTotal )
		self._ui.Download_progressBar.setValue( bytesReceived )

	@core.executionTrace
	def requestReady( self ):
		'''
		This Method Is Triggered When The Request Is Ready To Write.
		'''

		file = File( os.path.join( self._downloadFolder, os.path.basename( str( self._currentRequest.url().path() ) ) ), [self._currentRequest.readAll()] )
		file.append()

	@core.executionTrace
	def downloadFinished( self ):
		'''
		This Method Is Triggered When The Request Download Is Finished.
		'''

		self._downloads.append( os.path.join( self._downloadFolder, os.path.basename( str( self._currentRequest.url().path() ) ) ) )
		self._ui.Current_File_label.setText( "'{0}' Downloading Done !".format( os.path.basename( str( self._currentRequest.url().path() ) ) ) )
		self._ui.Download_progressBar.hide()
		self._currentRequest.deleteLater();
		if self._requests :
			self.downloadNext()
		else :
			self._downloadStatus = True
			self._ui.Current_File_label.setText( "Downloads Finished !" )
			self._ui.Cancel_Close_pushButton.setText( "Close" )
			self.emit( SIGNAL( "downloadFinished()" ) )

	@core.executionTrace
	def startDownload( self ):
		'''
		This Method Triggers The Download.
		'''

		self._downloadStatus = False
		self.downloadNext()

	@core.executionTrace
	def abortDownload( self ):
		'''
		This Method Aborts The Current Download.
		'''

		self._currentRequest.abort()
		self._currentRequest.deleteLater()

class RemoteUpdater( object ):
	'''
	This Class Is The RemoteUpdater Class.
	'''

	@core.executionTrace
	def __init__( self, container, releases = None ):
		'''
		This Method Initializes The Class.
		
		@param releases: Releases. ( Dictionary )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		# --- Setting Class Attributes. ---
		self._container = container
		self._releases = None
		self.releases = releases
		self._uiPath = "ui/Remote_Updater.ui"
		self._uiPath = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiPath )
		self._uiResources = "resources/"
		self._uiResources = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiResources )
		self._uiLogoIcon = "sIBL_GUI_Small_Logo.png"
		self._uiGreenColor = QColor( 128, 192, 128 )
		self._uiRedColor = QColor( 192, 128, 128 )
		self._splitter = "|"
		self._tableWidgetRowHeight = 30
		self._tableWidgetHeaderHeight = 25

		self._templatesTableWidgetHeaders = ["_datas", "Get It !", "Local Version", "Repository Version", "Release Type", "Comment"]

		self._applicationChangeLogUrl = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Change%20Log/Change%20Log.html"
		self._repositoryUrl = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository"

		self._downloadManager = None
		self._networkAccessManager = self._container.networkAccessManager

		self._ui = uic.loadUi( self._uiPath )
		if "." in sys.path :
			sys.path.remove( "." )

		self.initializeUi()
		self._ui.show()

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
	def releases( self ):
		'''
		This Method Is The Property For The _releases Attribute.

		@return: self._releases. ( Dictionary )
		'''

		return self._releases

	@releases.setter
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
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def releases( self ):
		'''
		This Method Is The Deleter Method For The _releases Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "releases" ) )

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
	def uiLogoIcon( self ):
		'''
		This Method Is The Property For The _uiLogoIcon Attribute.

		@return: self._uiLogoIcon. ( String )
		'''

		return self._uiLogoIcon

	@uiLogoIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLogoIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiLogoIcon Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiLogoIcon" ) )

	@uiLogoIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLogoIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiLogoIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiLogoIcon" ) )

	@property
	def uiGreenColor( self ):
		'''
		This Method Is The Property For The _uiGreenColor Attribute.

		@return: self._uiGreenColor. ( QColor )
		'''

		return self._uiGreenColor

	@uiGreenColor.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiGreenColor( self, value ):
		'''
		This Method Is The Setter Method For The _uiGreenColor Attribute.

		@param value: Attribute Value. ( QColor )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiGreenColor" ) )

	@uiGreenColor.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiGreenColor( self ):
		'''
		This Method Is The Deleter Method For The _uiGreenColor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiGreenColor" ) )

	@property
	def uiRedColor( self ):
		'''
		This Method Is The Property For The _uiRedColor Attribute.

		@return: self._uiRedColor. ( QColor )
		'''

		return self._uiRedColor

	@uiRedColor.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiRedColor( self, value ):
		'''
		This Method Is The Setter Method For The _uiRedColor Attribute.

		@param value: Attribute Value. ( QColor )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiRedColor" ) )

	@uiRedColor.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiRedColor( self ):
		'''
		This Method Is The Deleter Method For The _uiRedColor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiRedColor" ) )

	@property
	def splitter( self ):
		'''
		This Method Is The Property For The _splitter Attribute.

		@return: self._splitter. ( String )
		'''

		return self._splitter

	@splitter.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def splitter( self, value ):
		'''
		This Method Is The Setter Method For The _splitter Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "splitter" ) )

	@splitter.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def splitter( self ):
		'''
		This Method Is The Deleter Method For The _splitter Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "splitter" ) )

	@property
	def tableWidgetRowHeight( self ):
		'''
		This Method Is The Property For The _tableWidgetRowHeight Attribute.

		@return: self._tableWidgetRowHeight. ( Integer )
		'''

		return self._tableWidgetRowHeight

	@tableWidgetRowHeight.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def tableWidgetRowHeight( self, value ):
		'''
		This Method Is The Setter Method For The _tableWidgetRowHeight Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "tableWidgetRowHeight" ) )

	@tableWidgetRowHeight.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def tableWidgetRowHeight( self ):
		'''
		This Method Is The Deleter Method For The _tableWidgetRowHeight Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "tableWidgetRowHeight" ) )

	@property
	def tableWidgetHeaderHeight( self ):
		'''
		This Method Is The Property For The _tableWidgetHeaderHeight Attribute.

		@return: self._tableWidgetHeaderHeight. ( Integer )
		'''

		return self._tableWidgetHeaderHeight

	@tableWidgetHeaderHeight.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def tableWidgetHeaderHeight( self, value ):
		'''
		This Method Is The Setter Method For The _tableWidgetHeaderHeight Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "tableWidgetHeaderHeight" ) )

	@tableWidgetHeaderHeight.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def tableWidgetHeaderHeight( self ):
		'''
		This Method Is The Deleter Method For The _tableWidgetHeaderHeight Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "tableWidgetHeaderHeight" ) )

	@property
	def templatesTableWidgetHeaders( self ):
		'''
		This Method Is The Property For The _templatesTableWidgetHeaders Attribute.

		@return: self._templatesTableWidgetHeaders. ( String )
		'''

		return self._templatesTableWidgetHeaders

	@templatesTableWidgetHeaders.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templatesTableWidgetHeaders( self, value ):
		'''
		This Method Is The Setter Method For The _templatesTableWidgetHeaders Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "templatesTableWidgetHeaders" ) )

	@templatesTableWidgetHeaders.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templatesTableWidgetHeaders( self ):
		'''
		This Method Is The Deleter Method For The _templatesTableWidgetHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "templatesTableWidgetHeaders" ) )

	@property
	def applicationChangeLogUrl( self ):
		'''
		This Method Is The Property For The _applicationChangeLogUrl Attribute.

		@return: self._applicationChangeLogUrl. ( String )
		'''

		return self._applicationChangeLogUrl

	@applicationChangeLogUrl.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def applicationChangeLogUrl( self, value ):
		'''
		This Method Is The Setter Method For The _applicationChangeLogUrl Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "applicationChangeLogUrl" ) )

	@applicationChangeLogUrl.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def applicationChangeLogUrl( self ):
		'''
		This Method Is The Deleter Method For The _applicationChangeLogUrl Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "applicationChangeLogUrl" ) )

	@property
	def repositoryUrl( self ):
		'''
		This Method Is The Property For The _repositoryUrl Attribute.

		@return: self._repositoryUrl. ( String )
		'''

		return self._repositoryUrl

	@repositoryUrl.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def repositoryUrl( self, value ):
		'''
		This Method Is The Setter Method For The _repositoryUrl Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "repositoryUrl" ) )

	@repositoryUrl.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def repositoryUrl( self ):
		'''
		This Method Is The Deleter Method For The _repositoryUrl Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "repositoryUrl" ) )

	@property
	def downloadManager( self ):
		'''
		This Method Is The Property For The _downloadManager Attribute.

		@return: self._downloadManager. ( Object )
		'''

		return self._downloadManager

	@downloadManager.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def downloadManager( self, value ):
		'''
		This Method Is The Setter Method For The _downloadManager Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "downloadManager" ) )

	@downloadManager.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def downloadManager( self ):
		'''
		This Method Is The Deleter Method For The _downloadManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "downloadManager" ) )

	@property
	def networkAccessManager( self ):
		'''
		This Method Is The Property For The _networkAccessManager Attribute.

		@return: self._networkAccessManager. ( QNetworkAccessManager )
		'''

		return self._networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def networkAccessManager( self, value ):
		'''
		This Method Is The Setter Method For The _networkAccessManager Attribute.

		@param value: Attribute Value. ( QNetworkAccessManager )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "networkAccessManager" ) )

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def networkAccessManager( self ):
		'''
		This Method Is The Deleter Method For The _networkAccessManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "networkAccessManager" ) )

	@property
	def ui( self ):
		'''
		This Method Is The Property For The _ui Attribute.

		@return: self._ui. ( Object )
		'''

		return self._ui

	@ui.setter
	def ui( self, value ):
		'''
		This Method Is The Setter Method For The _ui Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		self._ui = value

	@ui.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ui( self ):
		'''
		This Method Is The Deleter Method For The _ui Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "ui" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Remote_Updater Widget Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Ui.".format( self.__class__.__name__ ) )

		if Constants.applicationName not in self._releases :
			self._ui.sIBL_GUI_groupBox.hide()
			self._ui.Get_sIBL_GUI_pushButton.hide()
		else :
			self._ui.Logo_label.setPixmap( QPixmap( os.path.join( self._uiResources, self._uiLogoIcon ) ) )
			self._ui.Your_Version_label.setText( self._releases[Constants.applicationName].localVersion )
			self._ui.Latest_Version_label.setText( self._releases[Constants.applicationName].repositoryVersion )
			self._ui.Change_Log_webView.load( QUrl.fromEncoded( QByteArray( self._applicationChangeLogUrl ) ) )

		templatesReleases = dict( self._releases )
		if Constants.applicationName in self._releases :
			templatesReleases.pop( Constants.applicationName )

		if not templatesReleases :
			self._ui.Templates_groupBox.hide()
			self._ui.Get_Latest_Templates_pushButton.hide()
		else :
			self._ui.Templates_tableWidget.clear()
			self._ui.Templates_tableWidget.setEditTriggers( QAbstractItemView.NoEditTriggers )
			self._ui.Templates_tableWidget.setRowCount( len( templatesReleases ) )
			self._ui.Templates_tableWidget.setColumnCount( len( self._templatesTableWidgetHeaders ) )
			self._ui.Templates_tableWidget.setHorizontalHeaderLabels( self._templatesTableWidgetHeaders )
			self._ui.Templates_tableWidget.hideColumn( 0 )
			self._ui.Templates_tableWidget.horizontalHeader().setStretchLastSection( True )
			self._ui.Templates_tableWidget.setMinimumHeight( len( templatesReleases ) * self._tableWidgetRowHeight + self._tableWidgetHeaderHeight )
			self._ui.Templates_tableWidget.setMaximumHeight( len( templatesReleases ) * self._tableWidgetRowHeight + self._tableWidgetHeaderHeight )

			palette = QPalette()
			palette.setColor( QPalette.Base, Qt.transparent )
			self._ui.Templates_tableWidget.setPalette( palette )

			verticalHeaderLabels = []
			for row, release in enumerate( templatesReleases ) :
					verticalHeaderLabels.append( release )

					tableWidgetItem = QTableWidgetItem()
					tableWidgetItem._datas = templatesReleases[release]
					self._ui.Templates_tableWidget.setItem( row, 0, tableWidgetItem )

					tableWidgetItem = Variable_QPushButton( True, ( self._uiGreenColor, self._uiRedColor ), ( "Yes", "No" ) )
					self._ui.Templates_tableWidget.setCellWidget( row, 1, tableWidgetItem )

					tableWidgetItem = QTableWidgetItem( templatesReleases[release].localVersion or Constants.nullObject )
					tableWidgetItem.setTextAlignment( Qt.AlignCenter )
					self._ui.Templates_tableWidget.setItem( row, 2, tableWidgetItem )

					tableWidgetItem = QTableWidgetItem( templatesReleases[release].repositoryVersion )
					tableWidgetItem.setTextAlignment( Qt.AlignCenter )
					self._ui.Templates_tableWidget.setItem( row, 3, tableWidgetItem )

					tableWidgetItem = QTableWidgetItem( templatesReleases[release].type )
					tableWidgetItem.setTextAlignment( Qt.AlignCenter )
					self._ui.Templates_tableWidget.setItem( row, 4, tableWidgetItem )

					tableWidgetItem = QTableWidgetItem( templatesReleases[release].comment )
					self._ui.Templates_tableWidget.setItem( row, 5, tableWidgetItem )

			self._ui.Templates_tableWidget.setVerticalHeaderLabels( verticalHeaderLabels )
			self._ui.Templates_tableWidget.resizeColumnsToContents()

		# Signals / Slots.
		self._ui.Get_sIBL_GUI_pushButton.connect( self._ui.Get_sIBL_GUI_pushButton, SIGNAL( "clicked()" ), self.Get_sIBL_GUI_pushButton_OnClicked )
		self._ui.Get_Latest_Templates_pushButton.connect( self._ui.Get_Latest_Templates_pushButton, SIGNAL( "clicked()" ), self.Get_Latest_Templates_pushButton_OnClicked )
		self._ui.Open_Repository_pushButton.connect( self._ui.Open_Repository_pushButton, SIGNAL( "clicked()" ), self.Open_Repository_pushButton_OnClicked )
		self._ui.Close_pushButton.connect( self._ui.Close_pushButton, SIGNAL( "clicked()" ), self.Close_pushButton_OnClicked )

	@core.executionTrace
	def Get_sIBL_GUI_pushButton_OnClicked( self ):
		'''
		This Method Is Triggered When Get_sIBL_GUI_pushButton Is Clicked.
		'''
		urlTokens = self.releases[Constants.applicationName].url.split( self._splitter )
		builds = dict( [( urlTokens[i].strip(), urlTokens[i + 1].strip( " \"" ) ) for i in range( 0, len( urlTokens ), 2 )] )

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			url = builds["Windows"]
		elif platform.system() == "Darwin" :
			url = builds["Mac Os X"]
		elif platform.system() == "Linux":
			url = builds["Linux"]

		self._downloadManager = DownloadManager( self, self._networkAccessManager, self._container.ioDirectory, [url] )
		self._downloadManager.connect( self._downloadManager, SIGNAL( "downloadFinished()" ), self.downloadManager_OnFinished )
		self._downloadManager.startDownload()

	@core.executionTrace
	def Get_Latest_Templates_pushButton_OnClicked( self ):
		'''
		This Method Is Triggered When Get_Latest_Templates_pushButton Is Clicked.
		'''

		requests = []
		for row in range( self._ui.Templates_tableWidget.rowCount() ) :
			if self._ui.Templates_tableWidget.cellWidget( row, 1 ).state :
				requests.append( self._ui.Templates_tableWidget.item( row, 0 )._datas )
		if requests :
			downloadFolder = self.getTemplatesDownloadFolder()
			if downloadFolder :
				self._downloadManager = DownloadManager( self, self._networkAccessManager, downloadFolder, [request.url for request in requests] )
				self._downloadManager.connect( self._downloadManager, SIGNAL( "downloadFinished()" ), self.downloadManager_OnFinished )
				self._downloadManager.startDownload()

	@core.executionTrace
	def Open_Repository_pushButton_OnClicked( self ):
		'''
		This Method Is Triggered When Open_Repository_pushButton Is Clicked.
		'''

		LOGGER.debug( "> Opening URL : '{0}'.".format( self._repositoryUrl ) )
		QDesktopServices.openUrl( QUrl( QString( self._repositoryUrl ) ) )

	@core.executionTrace
	def Close_pushButton_OnClicked( self ):
		'''
		This Method Closes The RemoteUpdater.
		'''

		LOGGER.info( "{0} | Closing '{1}' Updater !".format( self.__class__.__name__, Constants.applicationName ) )
		self._ui.close()

	@core.executionTrace
	def getTemplatesDownloadFolder( self ):
		'''
		This Method Gets The Templates Folder.
		'''

		messageBox = QMessageBox()
		messageBox.setWindowTitle( "{0}".format( self.__class__.__name__ ) )
		messageBox.setIcon( QMessageBox.Question )
		messageBox.setText( "{0} | Which Directory Do You Want To Install The Templates Into ?".format( self.__class__.__name__ ) )
		messageBox.addButton( QString( "Cancel" ), QMessageBox.AcceptRole )
		messageBox.addButton( QString( "Custom" ), QMessageBox.AcceptRole )
		messageBox.addButton( QString( "User" ), QMessageBox.AcceptRole )
		messageBox.addButton( QString( "Factory" ), QMessageBox.AcceptRole )
		reply = messageBox.exec_()

		if reply == 3 :
			return os.path.join( os.getcwd(), Constants.templatesDirectory )
		elif reply == 2 :
			return os.path.join( self._container.container.userApplicationDirectory, Constants.templatesDirectory )
		elif reply == 1 :
			return self._container.container.storeLastBrowsedPath( ( QFileDialog.getExistingDirectory( self._ui, "Add Directory :", self._container.container.lastBrowsedPath ) ) )

	@core.executionTrace
	def downloadManager_OnFinished( self ):
		'''
		This Method Is Triggered When The Download Manager Finishes.
		'''

		for download in self._downloadManager.downloads :
			if download.endswith( ".zip" ) :
				pkzip = Pkzip()
				pkzip.archive = download
				pkzip.extract( os.path.dirname( download ) )

				LOGGER.info( "{0} | Deleting '{1}' Archive !".format( self.__class__.__name__, download ) )
				os.remove( download )

				self._container.coreTemplatesOutliner.getTemplates( os.path.dirname( download ), self._container.coreTemplatesOutliner.getCollection( self._container.coreTemplatesOutliner.userCollection ).id )
				self._container.coreTemplatesOutliner.refreshUi()
			else :
				if self._container.addonsLocationsBrowser.activated :
					self._container.addonsLocationsBrowser.exploreProvidedFolder( os.path.dirname( download ) )

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
		self._coreDb = None
		self._coreTemplatesOutliner = None
		self._addonsLocationsBrowser = None

		self._ioDirectory = "remote/"

		self._repositoryUrl = REPOSITORY_URL
		self._releasesFileUrl = "sIBL_GUI_Releases.rc"

		self._networkAccessManager = None
		self._releaseReply = None

		self._remoteUpdater = None

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
	def addonsLocationsBrowser( self ):
		'''
		This Method Is The Property For The _addonsLocationsBrowser Attribute.

		@return: self._addonsLocationsBrowser. ( Object )
		'''

		return self._addonsLocationsBrowser

	@addonsLocationsBrowser.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def addonsLocationsBrowser( self, value ):
		'''
		This Method Is The Setter Method For The _addonsLocationsBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "addonsLocationsBrowser" ) )

	@addonsLocationsBrowser.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def addonsLocationsBrowser( self ):
		'''
		This Method Is The Deleter Method For The _addonsLocationsBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "addonsLocationsBrowser" ) )

	@property
	def ioDirectory( self ):
		'''
		This Method Is The Property For The _ioDirectory Attribute.

		@return: self._ioDirectory. ( String )
		'''

		return self._ioDirectory

	@ioDirectory.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ioDirectory( self, value ):
		'''
		This Method Is The Setter Method For The _ioDirectory Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "ioDirectory" ) )

	@ioDirectory.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ioDirectory( self ):
		'''
		This Method Is The Deleter Method For The _ioDirectory Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "ioDirectory" ) )

	@property
	def repositoryUrl( self ):
		'''
		This Method Is The Property For The _repositoryUrl Attribute.

		@return: self._repositoryUrl. ( String )
		'''

		return self._repositoryUrl

	@repositoryUrl.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def repositoryUrl( self, value ):
		'''
		This Method Is The Setter Method For The _repositoryUrl Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "repositoryUrl" ) )

	@repositoryUrl.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def repositoryUrl( self ):
		'''
		This Method Is The Deleter Method For The _repositoryUrl Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "repositoryUrl" ) )

	@property
	def releasesFileUrl( self ):
		'''
		This Method Is The Property For The _releasesFileUrl Attribute.

		@return: self._releasesFileUrl. ( String )
		'''

		return self._releasesFileUrl

	@releasesFileUrl.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def releasesFileUrl( self, value ):
		'''
		This Method Is The Setter Method For The _releasesFileUrl Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "releasesFileUrl" ) )

	@releasesFileUrl.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def releasesFileUrl( self ):
		'''
		This Method Is The Deleter Method For The _releasesFileUrl Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "releasesFileUrl" ) )

	@property
	def networkAccessManager( self ):
		'''
		This Method Is The Property For The _networkAccessManager Attribute.

		@return: self._networkAccessManager. ( QNetworkAccessManager )
		'''

		return self._networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def networkAccessManager( self, value ):
		'''
		This Method Is The Setter Method For The _networkAccessManager Attribute.

		@param value: Attribute Value. ( QNetworkAccessManager )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "networkAccessManager" ) )

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def networkAccessManager( self ):
		'''
		This Method Is The Deleter Method For The _networkAccessManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "networkAccessManager" ) )

	@property
	def releaseReply( self ):
		'''
		This Method Is The Property For The _releaseReply Attribute.

		@return: self._releaseReply. ( QNetworkReply )
		'''

		return self._releaseReply

	@releaseReply.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def releaseReply( self, value ):
		'''
		This Method Is The Setter Method For The _releaseReply Attribute.

		@param value: Attribute Value. ( QNetworkReply )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "releaseReply" ) )

	@releaseReply.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def releaseReply( self ):
		'''
		This Method Is The Deleter Method For The _releaseReply Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "releaseReply" ) )

	@property
	def remoteUpdater( self ):
		'''
		This Method Is The Property For The _remoteUpdater Attribute.

		@return: self._remoteUpdater. ( Object )
		'''

		return self._remoteUpdater

	@remoteUpdater.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def remoteUpdater( self, value ):
		'''
		This Method Is The Setter Method For The _remoteUpdater Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "remoteUpdater" ) )

	@remoteUpdater.deleter
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
		self._settings = self._container.settings

		self._corePreferencesManager = self._container.componentsManager.components["core.preferencesManager"].interface
		self._coreDb = self._container.componentsManager.components["core.db"].interface
		self._coreTemplatesOutliner = self._container.componentsManager.components["core.templatesOutliner"].interface
		self._addonsLocationsBrowser = self._container.componentsManager.components["addons.locationsBrowser"].interface

		self._ioDirectory = os.path.join( self._container.userApplicationDirectory, Constants.ioDirectory, self._ioDirectory )
		not os.path.exists( self._ioDirectory ) and os.makedirs( self._ioDirectory )

		self._networkAccessManager = QNetworkAccessManager()

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

		self._corePreferencesManager = None
		self._coreDb = None
		self._coreTemplatesOutliner = None
		self._addonsLocationsBrowser = None

		self._ioDirectory = os.path.basename( os.path.abspath( self._ioDirectory ) )

		self._networkAccessManager = None

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self.Check_For_New_Releases_On_Startup_checkBox_setUi()

		# Signals / Slots.
		self.ui.Check_For_New_Releases_pushButton.connect( self.ui.Check_For_New_Releases_pushButton, SIGNAL( "clicked()" ), self.Check_For_New_Releases_pushButton_OnClicked )
		self.ui.Check_For_New_Releases_On_Startup_checkBox.connect( self.ui.Check_For_New_Releases_On_Startup_checkBox, SIGNAL( "stateChanged( int )" ), self.Check_For_New_Releases_On_Startup_checkBox_OnStateChanged )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		# Signals / Slots.
		self.ui.Check_For_New_Releases_pushButton.disconnect( self.ui.Check_For_New_Releases_pushButton, SIGNAL( "clicked()" ), self.Check_For_New_Releases_pushButton_OnClicked )
		self.ui.Check_For_New_Releases_On_Startup_checkBox.disconnect( self.ui.Check_For_New_Releases_On_Startup_checkBox, SIGNAL( "stateChanged()" ), self.Check_For_New_Releases_On_Startup_checkBox_OnStateChanged )

	@core.executionTrace
	def Check_For_New_Releases_On_Startup_checkBox_setUi( self ) :
		'''
		This Method Sets The Check_For_New_Releases_On_Startup_checkBox.
		'''

		# Adding Settings Key If It Does'nt Exists.
		self._settings.getKey( "Others", "CheckForNewReleasesOnStartup" ).isNull() and self._settings.setKey( "Others", "CheckForNewReleasesOnStartup", Qt.Checked )

		checkForNewReleasesOnStartup = self._settings.getKey( "Others", "CheckForNewReleasesOnStartup" )
		LOGGER.debug( "> Setting '{0}' With Value '{1}'.".format( "Check_For_New_Releases_On_Startup_checkBox", checkForNewReleasesOnStartup.toInt()[0] ) )
		self.ui.Check_For_New_Releases_On_Startup_checkBox.setCheckState( checkForNewReleasesOnStartup.toInt()[0] )

	@core.executionTrace
	def Check_For_New_Releases_On_Startup_checkBox_OnStateChanged( self, state ) :
		'''
		This Method Is Called When Check_For_New_Releases_On_Startup_checkBox State Changes.
		
		@param state: Checkbox State. ( Integer )
		'''

		LOGGER.debug( "> Check For New Releases On Startup State : '{0}'.".format( self.ui.Check_For_New_Releases_On_Startup_checkBox.checkState() ) )
		self._settings.setKey( "Others", "CheckForNewReleasesOnStartup", self.ui.Check_For_New_Releases_On_Startup_checkBox.checkState() )

	@core.executionTrace
	def onStartup( self ):
		'''
		This Method Is Called On Framework Startup.
		'''

		self._ui.Check_For_New_Releases_On_Startup_checkBox.isChecked() and self.checkForNewReleases()

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
	def releaseReply_OnDownloadFinished( self ):
		'''
		This Method Is Triggered When The Release Reply Finishes.
		'''

		if not self._releaseReply.error():
			content = []
			while not self._releaseReply.atEnd () :
				content.append( str( self._releaseReply.readLine() ) )

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
							releases[remoteObject] = ReleaseObject( name = remoteObject,
																repositoryVersion = parser.getValue( "Release", remoteObject ),
																localVersion = dbTemplate.release,
																type = parser.getValue( "Type", remoteObject ),
																url = parser.getValue( "Url", remoteObject ),
																comment = parser.getValue( "Comment", remoteObject ) )
					else :
							releases[remoteObject] = ReleaseObject( name = remoteObject,
																repositoryVersion = parser.getValue( "Release", remoteObject ),
																localVersion = None,
																type = parser.getValue( "Type", remoteObject ),
																url = parser.getValue( "Url", remoteObject ),
																comment = parser.getValue( "Comment", remoteObject ) )
				else :
					if Constants.releaseVersion != parser.getValue( "Release", remoteObject ) :
						releases[remoteObject] = ReleaseObject( name = remoteObject,
															repositoryVersion = parser.getValue( "Release", remoteObject ),
															localVersion = Constants.releaseVersion,
															url = parser.getValue( "Url", remoteObject ),
															type = parser.getValue( "Type", remoteObject ),
															comment = None )
			if releases :
				self._remoteUpdater = RemoteUpdater( self, releases )
			else :
				messageBox.messageBox( "Informations", "Informations", "{0} | '{1}' Is Up To Date !".format( self.__class__.__name__, Constants.applicationName ) )
		else:
			raise foundations.exceptions.NetworkError( "QNetworkAccessManager Error Code : '{0}'.".format( self._releaseReply.error() ) )

	@core.executionTrace
	def checkForNewReleases( self ):
		'''
		This Method Checks For New Releases.
		'''

		self.getReleaseFile( QUrl( os.path.join( self._repositoryUrl, self._releasesFileUrl ) ) )

	@core.executionTrace
	def getReleaseFile( self, url ):
		'''
		This Method Gets The Release File.
		'''

		self._releaseReply = self._networkAccessManager.get( QNetworkRequest( url ) )
		self._releaseReply.connect( self._releaseReply, SIGNAL( "finished()" ), self.releaseReply_OnDownloadFinished )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
