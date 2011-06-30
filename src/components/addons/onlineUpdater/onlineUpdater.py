#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
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
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
************************************************************************************************
***	onlineUpdater.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Online Updater Component Module.
***
***	Others:
***
************************************************************************************************
"""

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
import ui.common
import ui.widgets.messageBox as messageBox
from foundations.parser import Parser
from foundations.pkzip import Pkzip
from globals.constants import Constants
from manager.uiComponent import UiComponent
from ui.widgets.variable_QPushButton import Variable_QPushButton

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

REPOSITORY_URL = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Repository/"

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class ReleaseObject(core.Structure):
	"""
	This Is The ReleaseObject Class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This Method Initializes The Class.

		@param kwargs: name, repositoryVersion, localVersion, type, url, comment. ( Key / Value Pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting Class Attributes. ---
		self.__dict__.update(kwargs)

class DownloadManager(QObject):
	"""
	This Is The DownloadManager Class.
	"""

	# Custom Signals Definitions.
	downloadFinished = pyqtSignal()

	@core.executionTrace
	def __init__(self, container, networkAccessManager, downloadDirectory, requests=None):
		"""
		This Method Initializes The Class.
		
		@param container: Container. ( Object )
		@param networkAccessManager: Network Access Manager. ( QNetworkAccessManager )
		@param downloadDirectory: Download Directory. ( String )
		@param requests: Download Requests. ( List )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QObject.__init__(self)

		# --- Setting Class Attributes. ---
		self.__container = container
		self.__networkAccessManager = networkAccessManager
		self.__downloadDirectory = downloadDirectory

		self.__uiPath = "ui/Download_Manager.ui"
		self.__uiPath = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = "resources/"
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__uiLogoImage = "sIBL_GUI_Small_Logo.png"

		self.__requests = None
		self.requests = requests
		self.__downloads = []
		self.__currentRequest = None
		self.__currentFile = None
		self.__currentFilePath = None

		# Helper Attribute For QNetwork Reply Crash.
		self.__downloadStatus = None

		self.__ui = uic.loadUi(self.__uiPath)
		if "." in sys.path:
			sys.path.remove(".")

		self.initializeUi()

		self.__ui.show()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def networkAccessManager(self):
		"""
		This Method Is The Property For The _networkAccessManager Attribute.

		@return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This Method Is The Setter Method For The _networkAccessManager Attribute.

		@param value: Attribute Value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This Method Is The Deleter Method For The _networkAccessManager Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("networkAccessManager"))

	@property
	def downloadDirectory(self):
		"""
		This Method Is The Property For The _downloadDirectory Attribute.

		@return: self.__downloadDirectory. ( String )
		"""

		return self.__downloadDirectory

	@downloadDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadDirectory(self, value):
		"""
		This Method Is The Setter Method For The _downloadDirectory Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("downloadDirectory"))

	@downloadDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadDirectory(self):
		"""
		This Method Is The Deleter Method For The _downloadDirectory Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("downloadDirectory"))

	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This Method Is The Property For The _uiResources Attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This Method Is The Deleter Method For The _uiResources Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def uiLogoImage(self):
		"""
		This Method Is The Property For The _uiLogoImage Attribute.

		@return: self.__uiLogoImage. ( String )
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This Method Is The Setter Method For The _uiLogoImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This Method Is The Deleter Method For The _uiLogoImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiLogoImage"))

	@property
	def requests(self):
		"""
		This Method Is The Property For The _requests Attribute.

		@return: self.__requests. ( List )
		"""

		return self.__requests

	@requests.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def requests(self, value):
		"""
		This Method Is The Setter Method For The _requests Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		"""

		if value:
			assert type(value) is list, "'{0}' Attribute: '{1}' Type Is Not 'list'!".format("requests", value)
		self.__requests = value

	@requests.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def requests(self):
		"""
		This Method Is The Deleter Method For The _requests Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("requests"))

	@property
	def downloads(self):
		"""
		This Method Is The Property For The _downloads Attribute.

		@return: self.__downloads. ( List )
		"""

		return self.__downloads

	@downloads.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def downloads(self, value):
		"""
		This Method Is The Setter Method For The _downloads Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("downloads"))

	@downloads.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloads(self):
		"""
		This Method Is The Deleter Method For The _downloads Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("downloads"))

	@property
	def currentRequest(self):
		"""
		This Method Is The Property For The _currentRequest Attribute.

		@return: self.__currentRequest. ( QNetworkReply )
		"""

		return self.__currentRequest

	@currentRequest.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentRequest(self, value):
		"""
		This Method Is The Setter Method For The _currentRequest Attribute.

		@param value: Attribute Value. ( QNetworkReply )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("currentRequest"))

	@currentRequest.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentRequest(self):
		"""
		This Method Is The Deleter Method For The _currentRequest Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("currentRequest"))

	@property
	def currentFile(self):
		"""
		This Method Is The Property For The _currentFile Attribute.

		@return: self.__currentFile. ( QFile )
		"""

		return self.__currentFile

	@currentFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFile(self, value):
		"""
		This Method Is The Setter Method For The _currentFile Attribute.

		@param value: Attribute Value. ( QFile )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("currentFile"))

	@currentFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFile(self):
		"""
		This Method Is The Deleter Method For The _currentFile Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("currentFile"))

	@property
	def currentFilePath(self):
		"""
		This Method Is The Property For The _currentFilePath Attribute.

		@return: self.__currentFilePath. ( String )
		"""

		return self.__currentFilePath

	@currentFilePath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFilePath(self, value):
		"""
		This Method Is The Setter Method For The _currentFilePath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("currentFilePath"))

	@currentFilePath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFilePath(self):
		"""
		This Method Is The Deleter Method For The _currentFilePath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("currentFilePath"))

	@property
	def downloadStatus(self):
		"""
		This Method Is The Property For The _downloadStatus Attribute.

		@return: self.__downloadStatus. ( QObject )
		"""

		return self.__downloadStatus

	@downloadStatus.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadStatus(self, value):
		"""
		This Method Is The Setter Method For The _downloadStatus Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("downloadStatus"))

	@downloadStatus.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadStatus(self):
		"""
		This Method Is The Deleter Method For The _downloadStatus Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("downloadStatus"))

	@property
	def ui(self):
		"""
		This Method Is The Property For The _ui Attribute.

		@return: self.__ui. ( Object )
		"""

		return self.__ui

	@ui.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self, value):
		"""
		This Method Is The Setter Method For The _ui Attribute.
		
		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("ui"))

	@ui.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self):
		"""
		This Method Is The Deleter Method For The _ui Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("ui"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Widget Ui.
		"""

		ui.common.setWindowDefaultIcon(self.ui)

		self.__ui.Download_progressBar.setValue(0)
		self.__ui.Download_progressBar.hide()
		self.__ui.Logo_label.setPixmap(QPixmap(os.path.join(self.__uiResources, self.__uiLogoImage)))

		self.__ui.closeEvent = self.closeEvent

		# Signals / Slots.
		self.__ui.Cancel_Close_pushButton.clicked.connect(self.__Cancel_Close_pushButton__clicked)

	@core.executionTrace
	def closeEvent(self, closeEvent):
		"""
		This Method Overloads The DownloadManager CloseEvent.
		
		@param closeEvent: Close Event. ( QCloseEvent )
		"""

		self.__downloadStatus or self.abortDownload()
		closeEvent.accept()

	@core.executionTrace
	def __Cancel_Close_pushButton__clicked(self, checked):
		"""
		This Method Triggers The DownloadManager Close.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.__ui.close()

	@core.executionTrace
	def __downloadNext(self):
		"""
		This Method Downloads The Next Request.
		"""

		if self.__requests:
			self.__ui.Download_progressBar.show()

			self.__currentRequest = self.__networkAccessManager.get(QNetworkRequest(QUrl(self.__requests.pop())))

			self.__currentFilePath = os.path.join(self.__downloadDirectory, os.path.basename(str(self.__currentRequest.url().path())))
			if os.path.exists(self.__currentFilePath):
				LOGGER.info("{0} | Removing '{1}' Local File From Previous Online Update!".format(self.__class__.__name__, os.path.basename(self.__currentFilePath)))
				os.remove(self.__currentFilePath)

			self.__currentFile = QFile(self.__currentFilePath)

			if not self.__currentFile.open(QIODevice.WriteOnly):
				messageBox.messageBox("Warning", "Warning", "{0} | Error While Writing '{1}' File To Disk, Proceeding To Next Download!".format(self.__class__.__name__, os.path.basename(self.__currentFilePath)))
				self.__downloadNext()
				return

			# Signals / Slots.
			self.__currentRequest.__downloadProgress.connect(self.__downloadProgress)
			self.__currentRequest.finished.connect(self.__downloadComplete)
			self.__currentRequest.readyRead.connect(self.__requestReady)

	@core.executionTrace
	def __downloadProgress(self, bytesReceived, bytesTotal):
		"""
		This Method Updates The Download Progress.
		
		@param bytesReceived: Bytes Received. ( Integer )
		@param bytesTotal: Bytes Total. ( Integer )
		"""

		LOGGER.debug("> Updating Download Progress: '{0}' Bytes Received, '{1}' Bytes Total.".format(bytesReceived, bytesTotal))

		self.__ui.Current_File_label.setText("Downloading: '{0}'.".format(os.path.basename(str(self.__currentRequest.url().path()))))
		self.__ui.Download_progressBar.setRange(0, bytesTotal)
		self.__ui.Download_progressBar.setValue(bytesReceived)

	@core.executionTrace
	def __requestReady(self):
		"""
		This Method Is Triggered When The Request Is Ready To Write.
		"""

		LOGGER.debug("> Updating '{0}' File Content.".format(self.__currentFile))

		self.__currentFile.write(self.__currentRequest.readAll())

	@core.executionTrace
	def __downloadComplete(self):
		"""
		This Method Is Triggered When The Request Download Is Complete.
		"""

		LOGGER.debug("> '{0}' Download Complete.".format(self.__currentFile))

		self.__currentFile.close()
		self.__downloads.append(self.__currentFilePath)
		self.__ui.Current_File_label.setText("'{0}' Downloading Done!".format(os.path.basename(self.__currentFilePath)))
		self.__ui.Download_progressBar.hide()
		self.__currentRequest.deleteLater();

		if self.__requests:
			LOGGER.debug("> Proceeding To Next Download Request.")
			self.__downloadNext()
		else:
			self.__downloadStatus = True
			self.__ui.Current_File_label.setText("Downloads Complete!")
			self.__ui.Cancel_Close_pushButton.setText("Close")
			self.emit(SIGNAL("downloadFinished()"))

	@core.executionTrace
	def startDownload(self):
		"""
		This Method Triggers The Download.
		"""

		self.__downloadStatus = False
		self.__downloadNext()

	@core.executionTrace
	def abortDownload(self):
		"""
		This Method Aborts The Current Download.
		"""

		self.__currentRequest.abort()
		self.__currentRequest.deleteLater()

class RemoteUpdater(object):
	"""
	This Class Is The RemoteUpdater Class.
	"""

	@core.executionTrace
	def __init__(self, container, releases=None):
		"""
		This Method Initializes The Class.
		
		@param releases: Releases. ( Dictionary )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.__container = container
		self.__releases = None
		self.releases = releases
		self.__uiPath = "ui/Remote_Updater.ui"
		self.__uiPath = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = "resources/"
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__uiLogoImage = "sIBL_GUI_Small_Logo.png"
		self.__uiTemplatesImage = "Templates_Logo.png"
		self.__uiLightGrayColor = QColor(240, 240, 240)
		self.__uiDarkGrayColor = QColor(160, 160, 160)
		self.__splitter = "|"
		self.__tableWidgetRowHeight = 30
		self.__tableWidgetHeaderHeight = 25

		self.__templatesTableWidgetHeaders = ["_datas", "Get It!", "Local Version", "Repository Version", "Release Type", "Comment"]

		self.__applicationChangeLogUrl = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Change%20Log/Change%20Log.html"
		self.__repositoryUrl = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository"

		self.__downloadManager = None
		self.__networkAccessManager = self.__container.networkAccessManager

		self.__ui = uic.loadUi(self.__uiPath)
		if "." in sys.path:
			sys.path.remove(".")

		self.initializeUi()

		self.__ui.show()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def releases(self):
		"""
		This Method Is The Property For The _releases Attribute.

		@return: self.__releases. ( Dictionary )
		"""

		return self.__releases

	@releases.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def releases(self, value):
		"""
		This Method Is The Setter Method For The _releases Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' Attribute: '{1}' Type Is Not 'dict'!".format("releases", value)
		self.__releases = value

	@releases.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releases(self):
		"""
		This Method Is The Deleter Method For The _releases Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("releases"))

	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This Method Is The Property For The _uiResources Attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This Method Is The Deleter Method For The _uiResources Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def uiLogoImage(self):
		"""
		This Method Is The Property For The _uiLogoImage Attribute.

		@return: self.__uiLogoImage. ( String )
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This Method Is The Setter Method For The _uiLogoImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This Method Is The Deleter Method For The _uiLogoImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiLogoImage"))

	@property
	def uiTemplatesImage(self):
		"""
		This Method Is The Property For The _uiTemplatesImage Attribute.

		@return: self.__uiTemplatesImage. ( String )
		"""

		return self.__uiTemplatesImage

	@uiTemplatesImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiTemplatesImage(self, value):
		"""
		This Method Is The Setter Method For The _uiTemplatesImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiTemplatesImage"))

	@uiTemplatesImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiTemplatesImage(self):
		"""
		This Method Is The Deleter Method For The _uiTemplatesImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiTemplatesImage"))

	@property
	def uiLightGrayColor(self):
		"""
		This Method Is The Property For The _uiLightGrayColor Attribute.

		@return: self.__uiLightGrayColor. ( QColor )
		"""

		return self.__uiLightGrayColor

	@uiLightGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self, value):
		"""
		This Method Is The Setter Method For The _uiLightGrayColor Attribute.

		@param value: Attribute Value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiLightGrayColor"))

	@uiLightGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self):
		"""
		This Method Is The Deleter Method For The _uiLightGrayColor Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiLightGrayColor"))

	@property
	def uiDarkGrayColor(self):
		"""
		This Method Is The Property For The _uiDarkGrayColor Attribute.

		@return: self.__uiDarkGrayColor. ( QColor )
		"""

		return self.__uiDarkGrayColor

	@uiDarkGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self, value):
		"""
		This Method Is The Setter Method For The _uiDarkGrayColor Attribute.

		@param value: Attribute Value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiDarkGrayColor"))

	@uiDarkGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self):
		"""
		This Method Is The Deleter Method For The _uiDarkGrayColor Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiDarkGrayColor"))

	@property
	def splitter(self):
		"""
		This Method Is The Property For The _splitter Attribute.

		@return: self.__splitter. ( String )
		"""

		return self.__splitter

	@splitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def splitter(self, value):
		"""
		This Method Is The Setter Method For The _splitter Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("splitter"))

	@splitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def splitter(self):
		"""
		This Method Is The Deleter Method For The _splitter Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("splitter"))

	@property
	def tableWidgetRowHeight(self):
		"""
		This Method Is The Property For The _tableWidgetRowHeight Attribute.

		@return: self.__tableWidgetRowHeight. ( Integer )
		"""

		return self.__tableWidgetRowHeight

	@tableWidgetRowHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self, value):
		"""
		This Method Is The Setter Method For The _tableWidgetRowHeight Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("tableWidgetRowHeight"))

	@tableWidgetRowHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self):
		"""
		This Method Is The Deleter Method For The _tableWidgetRowHeight Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("tableWidgetRowHeight"))

	@property
	def tableWidgetHeaderHeight(self):
		"""
		This Method Is The Property For The _tableWidgetHeaderHeight Attribute.

		@return: self.__tableWidgetHeaderHeight. ( Integer )
		"""

		return self.__tableWidgetHeaderHeight

	@tableWidgetHeaderHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self, value):
		"""
		This Method Is The Setter Method For The _tableWidgetHeaderHeight Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("tableWidgetHeaderHeight"))

	@tableWidgetHeaderHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self):
		"""
		This Method Is The Deleter Method For The _tableWidgetHeaderHeight Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("tableWidgetHeaderHeight"))

	@property
	def templatesTableWidgetHeaders(self):
		"""
		This Method Is The Property For The _templatesTableWidgetHeaders Attribute.

		@return: self.__templatesTableWidgetHeaders. ( String )
		"""

		return self.__templatesTableWidgetHeaders

	@templatesTableWidgetHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesTableWidgetHeaders(self, value):
		"""
		This Method Is The Setter Method For The _templatesTableWidgetHeaders Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templatesTableWidgetHeaders"))

	@templatesTableWidgetHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesTableWidgetHeaders(self):
		"""
		This Method Is The Deleter Method For The _templatesTableWidgetHeaders Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templatesTableWidgetHeaders"))

	@property
	def applicationChangeLogUrl(self):
		"""
		This Method Is The Property For The _applicationChangeLogUrl Attribute.

		@return: self.__applicationChangeLogUrl. ( String )
		"""

		return self.__applicationChangeLogUrl

	@applicationChangeLogUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def applicationChangeLogUrl(self, value):
		"""
		This Method Is The Setter Method For The _applicationChangeLogUrl Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("applicationChangeLogUrl"))

	@applicationChangeLogUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def applicationChangeLogUrl(self):
		"""
		This Method Is The Deleter Method For The _applicationChangeLogUrl Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("applicationChangeLogUrl"))

	@property
	def repositoryUrl(self):
		"""
		This Method Is The Property For The _repositoryUrl Attribute.

		@return: self.__repositoryUrl. ( String )
		"""

		return self.__repositoryUrl

	@repositoryUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self, value):
		"""
		This Method Is The Setter Method For The _repositoryUrl Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("repositoryUrl"))

	@repositoryUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self):
		"""
		This Method Is The Deleter Method For The _repositoryUrl Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("repositoryUrl"))

	@property
	def downloadManager(self):
		"""
		This Method Is The Property For The _downloadManager Attribute.

		@return: self.__downloadManager. ( Object )
		"""

		return self.__downloadManager

	@downloadManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadManager(self, value):
		"""
		This Method Is The Setter Method For The _downloadManager Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("downloadManager"))

	@downloadManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadManager(self):
		"""
		This Method Is The Deleter Method For The _downloadManager Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("downloadManager"))

	@property
	def networkAccessManager(self):
		"""
		This Method Is The Property For The _networkAccessManager Attribute.

		@return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This Method Is The Setter Method For The _networkAccessManager Attribute.

		@param value: Attribute Value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This Method Is The Deleter Method For The _networkAccessManager Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("networkAccessManager"))

	@property
	def ui(self):
		"""
		This Method Is The Property For The _ui Attribute.

		@return: self.__ui. ( Object )
		"""

		return self.__ui

	@ui.setter
	def ui(self, value):
		"""
		This Method Is The Setter Method For The _ui Attribute.
		
		@param value: Attribute Value. ( Object )
		"""

		self.__ui = value

	@ui.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self):
		"""
		This Method Is The Deleter Method For The _ui Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("ui"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Remote_Updater Widget Ui.
		"""

		ui.common.setWindowDefaultIcon(self.ui)

		LOGGER.debug("> Initializing '{0}' Ui.".format(self.__class__.__name__))

		if Constants.applicationName not in self.__releases:
			self.__ui.sIBL_GUI_groupBox.hide()
			self.__ui.Get_sIBL_GUI_pushButton.hide()
		else:
			self.__ui.Logo_label.setPixmap(QPixmap(os.path.join(self.__uiResources, self.__uiLogoImage)))
			self.__ui.Your_Version_label.setText(self.__releases[Constants.applicationName].localVersion)
			self.__ui.Latest_Version_label.setText(self.__releases[Constants.applicationName].repositoryVersion)
			self.__ui.Change_Log_webView.load(QUrl.fromEncoded(QByteArray(self.__applicationChangeLogUrl)))

		templatesReleases = dict(self.__releases)
		if Constants.applicationName in self.__releases:
			templatesReleases.pop(Constants.applicationName)

		if not templatesReleases:
			self.__ui.Templates_groupBox.hide()
			self.__ui.Get_Latest_Templates_pushButton.hide()
		else:
			self.__ui.Templates_label.setPixmap(QPixmap(os.path.join(self.__uiResources, self.__uiTemplatesImage)))
			self.__ui.Templates_tableWidget.clear()
			self.__ui.Templates_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
			self.__ui.Templates_tableWidget.setRowCount(len(templatesReleases))
			self.__ui.Templates_tableWidget.setColumnCount(len(self.__templatesTableWidgetHeaders))
			self.__ui.Templates_tableWidget.setHorizontalHeaderLabels(self.__templatesTableWidgetHeaders)
			self.__ui.Templates_tableWidget.hideColumn(0)
			self.__ui.Templates_tableWidget.horizontalHeader().setStretchLastSection(True)
			self.__ui.Templates_tableWidget.setMinimumHeight(len(templatesReleases) * self.__tableWidgetRowHeight + self.__tableWidgetHeaderHeight)
			self.__ui.Templates_tableWidget.setMaximumHeight(len(templatesReleases) * self.__tableWidgetRowHeight + self.__tableWidgetHeaderHeight)

			palette = QPalette()
			palette.setColor(QPalette.Base, Qt.transparent)
			self.__ui.Templates_tableWidget.setPalette(palette)

			verticalHeaderLabels = []
			for row, release in enumerate(sorted(templatesReleases)):
					verticalHeaderLabels.append(release)

					tableWidgetItem = QTableWidgetItem()
					tableWidgetItem._datas = templatesReleases[release]
					self.__ui.Templates_tableWidget.setItem(row, 0, tableWidgetItem)

					tableWidgetItem = Variable_QPushButton(True, (self.__uiLightGrayColor, self.__uiDarkGrayColor), ("Yes", "No"))
					self.__ui.Templates_tableWidget.setCellWidget(row, 1, tableWidgetItem)

					tableWidgetItem = QTableWidgetItem(templatesReleases[release].localVersion or Constants.nullObject)
					tableWidgetItem.setTextAlignment(Qt.AlignCenter)
					self.__ui.Templates_tableWidget.setItem(row, 2, tableWidgetItem)

					tableWidgetItem = QTableWidgetItem(templatesReleases[release].repositoryVersion)
					tableWidgetItem.setTextAlignment(Qt.AlignCenter)
					self.__ui.Templates_tableWidget.setItem(row, 3, tableWidgetItem)

					tableWidgetItem = QTableWidgetItem(templatesReleases[release].type)
					tableWidgetItem.setTextAlignment(Qt.AlignCenter)
					self.__ui.Templates_tableWidget.setItem(row, 4, tableWidgetItem)

					tableWidgetItem = QTableWidgetItem(templatesReleases[release].comment)
					self.__ui.Templates_tableWidget.setItem(row, 5, tableWidgetItem)

			self.__ui.Templates_tableWidget.setVerticalHeaderLabels(verticalHeaderLabels)
			self.__ui.Templates_tableWidget.resizeColumnsToContents()

		# Signals / Slots.
		self.__ui.Get_sIBL_GUI_pushButton.clicked.connect(self.__Get_sIBL_GUI_pushButton__clicked)
		self.__ui.Get_Latest_Templates_pushButton.clicked.connect(self.__Get_Latest_Templates_pushButton__clicked)
		self.__ui.Open_Repository_pushButton.clicked.connect(self.__Open_Repository_pushButton__clicked)
		self.__ui.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

	@core.executionTrace
	def __Get_sIBL_GUI_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Get_sIBL_GUI_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""
		urlTokens = self.releases[Constants.applicationName].url.split(self.__splitter)
		builds = dict(((urlTokens[i].strip(), urlTokens[i + 1].strip(" \"")) for i in range(0, len(urlTokens), 2)))

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			url = builds["Windows"]
		elif platform.system() == "Darwin":
			url = builds["Mac Os X"]
		elif platform.system() == "Linux":
			url = builds["Linux"]

		self.__downloadManager = DownloadManager(self, self.__networkAccessManager, self.__container.ioDirectory, [url])
		self.__downloadManager.downloadFinished.connect(self.__downloadManager__finished)
		self.__downloadManager.startDownload()

	@core.executionTrace
	def __Get_Latest_Templates_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Get_Latest_Templates_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		requests = []
		for row in range(self.__ui.Templates_tableWidget.rowCount()):
			if self.__ui.Templates_tableWidget.cellWidget(row, 1).state:
				requests.append(self.__ui.Templates_tableWidget.item(row, 0)._datas)
		if requests:
			downloadDirectory = self.__getTemplatesDownloadDirectory()
			if downloadDirectory:
				LOGGER.debug("> Templates Download Directory: '{0}'.".format(downloadDirectory))
				self.__downloadManager = DownloadManager(self, self.__networkAccessManager, downloadDirectory, [request.url for request in requests])
				self.__downloadManager.downloadFinished.connect(self.__downloadManager__finished)
				self.__downloadManager.startDownload()

	@core.executionTrace
	def __Open_Repository_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Open_Repository_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		LOGGER.debug("> Opening URL: '{0}'.".format(self.__repositoryUrl))
		QDesktopServices.openUrl(QUrl(QString(self.__repositoryUrl)))

	@core.executionTrace
	def __Close_pushButton__clicked(self, checked):
		"""
		This Method Closes The RemoteUpdater.
		
		@param checked: Checked State. ( Boolean )
		"""

		LOGGER.info("{0} | Closing '{1}' Updater!".format(self.__class__.__name__, Constants.applicationName))
		self.__ui.close()

	@core.executionTrace
	def __downloadManager__finished(self):
		"""
		This Method Is Triggered When The Download Manager Finishes.
		"""

		for download in self.__downloadManager.downloads:
			if download.endswith(".zip"):
				if self.extractZipFile(download):
					LOGGER.info("{0} | Removing '{1}' Archive!".format(self.__class__.__name__, download))
					os.remove(download)
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | Failed Extracting '{1}', Proceeding To Next File!".format(self.__class__.__name__, os.path.basename(download)))
				self.__container.coreTemplatesOutliner.addDirectory(os.path.dirname(download), self.__container.coreTemplatesOutliner.getCollection(self.__container.coreTemplatesOutliner.userCollection).id, ignoreWarning=True)
			else:
				if self.__container.addonsLocationsBrowser.activated:
					self.__container.addonsLocationsBrowser.exploreDirectory(os.path.dirname(download))

	@core.executionTrace
	def __getTemplatesDownloadDirectory(self):
		"""
		This Method Gets The Templates Directory.
		"""

		LOGGER.debug("> Retrieving Templates Download Directory.")

		messageBox = QMessageBox()
		messageBox.setWindowTitle("{0}".format(self.__class__.__name__))
		messageBox.setIcon(QMessageBox.Question)
		messageBox.setText("{0} | Which Directory Do You Want To Install The Templates Into?".format(self.__class__.__name__))
		messageBox.addButton(QString("Factory"), QMessageBox.AcceptRole)
		messageBox.addButton(QString("User"), QMessageBox.AcceptRole)
		messageBox.addButton(QString("Custom"), QMessageBox.AcceptRole)
		messageBox.addButton(QString("Cancel"), QMessageBox.AcceptRole)
		reply = messageBox.exec_()

		if reply == 0:
			return os.path.join(os.getcwd(), Constants.templatesDirectory)
		elif reply == 1:
			return os.path.join(self.__container.container.userApplicationDatasDirectory, Constants.templatesDirectory)
		elif reply == 2:
			return self.__container.container.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self.__ui, "Choose Templates Directory:", self.__container.container.lastBrowsedPath)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def extractZipFile(self, file):
		"""
		This Method Uncompress The Provided Zip File.
		
		@param file: File To Extract. ( String )
		@return: Extraction Success. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}' File Uncompress.".format(file))

		pkzip = Pkzip()
		pkzip.archive = file

		return pkzip.extract(os.path.dirname(file))

class OnlineUpdater(UiComponent):
	"""
	This Class Is The OnlineUpdater Class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self.__uiPath = "ui/Online_Updater.ui"

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDb = None
		self.__coreTemplatesOutliner = None
		self.__addonsLocationsBrowser = None

		self.__ioDirectory = "remote/"

		self.__repositoryUrl = REPOSITORY_URL
		self.__releasesFileUrl = "sIBL_GUI_Releases.rc"

		self.__networkAccessManager = None
		self.__releaseReply = None

		self.__remoteUpdater = None
		self.__reportUpdateStatus = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def settings(self):
		"""
		This Method Is The Property For The _settings Attribute.

		@return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@property
	def settingsSection(self):
		"""
		This Method Is The Property For The _settingsSection Attribute.

		@return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This Method Is The Setter Method For The _settingsSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This Method Is The Deleter Method For The _settingsSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settingsSection"))

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This Method Is The Deleter Method For The _settings Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settings"))

	@property
	def corePreferencesManager(self):
		"""
		This Method Is The Property For The _corePreferencesManager Attribute.

		@return: self.__corePreferencesManager. ( Object )
		"""

		return self.__corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self, value):
		"""
		This Method Is The Setter Method For The _corePreferencesManager Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("corePreferencesManager"))

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self):
		"""
		This Method Is The Deleter Method For The _corePreferencesManager Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("corePreferencesManager"))

	@property
	def coreDb(self):
		"""
		This Method Is The Property For The _coreDb Attribute.

		@return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This Method Is The Deleter Method For The _coreDb Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDb"))

	@property
	def coreTemplatesOutliner(self):
		"""
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreTemplatesOutliner"))

	@property
	def addonsLocationsBrowser(self):
		"""
		This Method Is The Property For The _addonsLocationsBrowser Attribute.

		@return: self.__addonsLocationsBrowser. ( Object )
		"""

		return self.__addonsLocationsBrowser

	@addonsLocationsBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLocationsBrowser(self, value):
		"""
		This Method Is The Setter Method For The _addonsLocationsBrowser Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("addonsLocationsBrowser"))

	@addonsLocationsBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLocationsBrowser(self):
		"""
		This Method Is The Deleter Method For The _addonsLocationsBrowser Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("addonsLocationsBrowser"))

	@property
	def ioDirectory(self):
		"""
		This Method Is The Property For The _ioDirectory Attribute.

		@return: self.__ioDirectory. ( String )
		"""

		return self.__ioDirectory

	@ioDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self, value):
		"""
		This Method Is The Setter Method For The _ioDirectory Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("ioDirectory"))

	@ioDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self):
		"""
		This Method Is The Deleter Method For The _ioDirectory Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("ioDirectory"))

	@property
	def repositoryUrl(self):
		"""
		This Method Is The Property For The _repositoryUrl Attribute.

		@return: self.__repositoryUrl. ( String )
		"""

		return self.__repositoryUrl

	@repositoryUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self, value):
		"""
		This Method Is The Setter Method For The _repositoryUrl Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("repositoryUrl"))

	@repositoryUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self):
		"""
		This Method Is The Deleter Method For The _repositoryUrl Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("repositoryUrl"))

	@property
	def releasesFileUrl(self):
		"""
		This Method Is The Property For The _releasesFileUrl Attribute.

		@return: self.__releasesFileUrl. ( String )
		"""

		return self.__releasesFileUrl

	@releasesFileUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releasesFileUrl(self, value):
		"""
		This Method Is The Setter Method For The _releasesFileUrl Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("releasesFileUrl"))

	@releasesFileUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releasesFileUrl(self):
		"""
		This Method Is The Deleter Method For The _releasesFileUrl Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("releasesFileUrl"))

	@property
	def networkAccessManager(self):
		"""
		This Method Is The Property For The _networkAccessManager Attribute.

		@return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This Method Is The Setter Method For The _networkAccessManager Attribute.

		@param value: Attribute Value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This Method Is The Deleter Method For The _networkAccessManager Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("networkAccessManager"))

	@property
	def releaseReply(self):
		"""
		This Method Is The Property For The _releaseReply Attribute.

		@return: self.__releaseReply. ( QNetworkReply )
		"""

		return self.__releaseReply

	@releaseReply.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releaseReply(self, value):
		"""
		This Method Is The Setter Method For The _releaseReply Attribute.

		@param value: Attribute Value. ( QNetworkReply )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("releaseReply"))

	@releaseReply.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releaseReply(self):
		"""
		This Method Is The Deleter Method For The _releaseReply Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("releaseReply"))

	@property
	def remoteUpdater(self):
		"""
		This Method Is The Property For The _remoteUpdater Attribute.

		@return: self.__remoteUpdater. ( Object )
		"""

		return self.__remoteUpdater

	@remoteUpdater.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def remoteUpdater(self, value):
		"""
		This Method Is The Setter Method For The _remoteUpdater Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("remoteUpdater"))

	@remoteUpdater.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def remoteUpdater(self):
		"""
		This Method Is The Deleter Method For The _remoteUpdater Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("remoteUpdater"))

	@property
	def reportUpdateStatus(self):
		"""
		This Method Is The Property For The _reportUpdateStatus Attribute.

		@return: self.__reportUpdateStatus. ( Boolean )
		"""

		return self.__reportUpdateStatus

	@reportUpdateStatus.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reportUpdateStatus(self, value):
		"""
		This Method Is The Setter Method For The _reportUpdateStatus Attribute.

		@param value: Attribute Value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("reportUpdateStatus"))

	@reportUpdateStatus.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reportUpdateStatus(self):
		"""
		This Method Is The Deleter Method For The _reportUpdateStatus Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("reportUpdateStatus"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__corePreferencesManager = self.__container.componentsManager.components["core.preferencesManager"].interface
		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface
		self.__addonsLocationsBrowser = self.__container.componentsManager.components["addons.locationsBrowser"].interface

		self.__ioDirectory = os.path.join(self.__container.userApplicationDatasDirectory, Constants.ioDirectory, self.__ioDirectory)
		not os.path.exists(self.__ioDirectory) and os.makedirs(self.__ioDirectory)

		self.__networkAccessManager = QNetworkAccessManager()

		self.__reportUpdateStatus = True

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDb = None
		self.__coreTemplatesOutliner = None
		self.__addonsLocationsBrowser = None

		self.__ioDirectory = os.path.basename(os.path.abspath(self.__ioDirectory))

		self.__networkAccessManager = None

		self.__reportUpdateStatus = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__container.parameters.deactivateWorkerThreads and LOGGER.info("{0} | 'OnStartup' Online Updater Worker Thread Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "deactivateWorkerThreads"))

		self.__Check_For_New_Releases_On_Startup_checkBox_setUi()
		self.__Ignore_Non_Existing_Templates_checkBox_setUi()

		# Signals / Slots.
		self.ui.Check_For_New_Releases_pushButton.clicked.connect(self.__Check_For_New_Releases_pushButton__clicked)
		self.ui.Check_For_New_Releases_On_Startup_checkBox.stateChanged.connect(self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.ui.Ignore_Non_Existing_Templates_checkBox.stateChanged.connect(self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Check_For_New_Releases_pushButton.clicked.disconnect(self.__Check_For_New_Releases_pushButton__clicked)
		self.ui.Check_For_New_Releases_On_Startup_checkBox.stateChanged.disconnect(self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.ui.Ignore_Non_Existing_Templates_checkBox.stateChanged.disconnect(self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

	@core.executionTrace
	def onStartup(self):
		"""
		This Method Is Called On Framework Startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework Startup Method.".format(self.__class__.__name__))

		self.__reportUpdateStatus = False
		not self.__container.parameters.deactivateWorkerThreads and self.ui.Check_For_New_Releases_On_Startup_checkBox.isChecked() and self.checkForNewReleases()

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Online_Updater_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.ui.Online_Updater_groupBox.setParent(None)

	@core.executionTrace
	def __Check_For_New_Releases_On_Startup_checkBox_setUi(self):
		"""
		This Method Sets The Check_For_New_Releases_On_Startup_checkBox.
		"""

		# Adding Settings Key If It Doesn't Exists.
		self.__settings.getKey(self.__settingsSection, "checkForNewReleasesOnStartup").isNull() and self.__settings.setKey(self.__settingsSection, "checkForNewReleasesOnStartup", Qt.Checked)

		checkForNewReleasesOnStartup = self.__settings.getKey(self.__settingsSection, "checkForNewReleasesOnStartup")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("Check_For_New_Releases_On_Startup_checkBox", checkForNewReleasesOnStartup.toInt()[0]))
		self.ui.Check_For_New_Releases_On_Startup_checkBox.setCheckState(checkForNewReleasesOnStartup.toInt()[0])

	@core.executionTrace
	def __Check_For_New_Releases_On_Startup_checkBox__stateChanged(self, state):
		"""
		This Method Is Called When Check_For_New_Releases_On_Startup_checkBox State Changes.
		
		@param state: Checkbox State. ( Integer )
		"""

		LOGGER.debug("> Check For New Releases On Startup State: '{0}'.".format(self.ui.Check_For_New_Releases_On_Startup_checkBox.checkState()))
		self.__settings.setKey(self.__settingsSection, "checkForNewReleasesOnStartup", self.ui.Check_For_New_Releases_On_Startup_checkBox.checkState())

	@core.executionTrace
	def __Ignore_Non_Existing_Templates_checkBox_setUi(self):
		"""
		This Method Sets The Ignore_Non_Existing_Templates_checkBox.
		"""

		# Adding Settings Key If It Doesn't Exists.
		self.__settings.getKey(self.__settingsSection, "ignoreNonExistingTemplates").isNull() and self.__settings.setKey(self.__settingsSection, "ignoreNonExistingTemplates", Qt.Checked)

		ignoreNonExistingTemplates = self.__settings.getKey(self.__settingsSection, "ignoreNonExistingTemplates")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("Ignore_Non_Existing_Templates_checkBox", ignoreNonExistingTemplates.toInt()[0]))
		self.ui.Ignore_Non_Existing_Templates_checkBox.setCheckState(ignoreNonExistingTemplates.toInt()[0])

	@core.executionTrace
	def __Ignore_Non_Existing_Templates_checkBox__stateChanged(self, state):
		"""
		This Method Is Called When Ignore_Non_Existing_Templates_checkBox State Changes.
		
		@param state: Checkbox State. ( Integer )
		"""

		LOGGER.debug("> Ignore Non Existing Templates State: '{0}'.".format(self.ui.Ignore_Non_Existing_Templates_checkBox.checkState()))
		self.__settings.setKey(self.__settingsSection, "ignoreNonExistingTemplates", self.ui.Ignore_Non_Existing_Templates_checkBox.checkState())

	@core.executionTrace
	def __Check_For_New_Releases_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Check_For_New_Releases_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.__reportUpdateStatus = True
		self.checkForNewReleases()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.NetworkError)
	def __releaseReply__finished(self):
		"""
		This Method Is Triggered When The Release Reply Finishes.
		"""

		if not self.__releaseReply.error():
			content = []
			while not self.__releaseReply.atEnd ():
				content.append(str(self.__releaseReply.readLine()))

			LOGGER.debug("> Parsing Releases File Content.")
			parser = Parser()
			parser.content = content
			parser.parse()

			releases = {}
			for remoteObject in parser.sections:
				if remoteObject != Constants.applicationName:
						dbTemplates = dbUtilities.common.filterTemplates(self.__coreDb.dbSession, "^{0}$".format(remoteObject), "name")
						dbTemplate = dbTemplates and [dbTemplate[0] for dbTemplate in sorted(((dbTemplate, dbTemplate.release) for dbTemplate in dbTemplates), reverse=True, key=lambda x:(strings.getVersionRank(x[1])))][0] or None
						if not self.__container.parameters.databaseReadOnly:
							if dbTemplate:
								if dbTemplate.release != parser.getValue("Release", remoteObject):
									releases[remoteObject] = ReleaseObject(name=remoteObject,
																		repositoryVersion=parser.getValue("Release", remoteObject),
																		localVersion=dbTemplate.release,
																		type=parser.getValue("Type", remoteObject),
																		url=parser.getValue("Url", remoteObject),
																		comment=parser.getValue("Comment", remoteObject))
							else:
								if not self.ui.Ignore_Non_Existing_Templates_checkBox.isChecked():
									releases[remoteObject] = ReleaseObject(name=remoteObject,
																		repositoryVersion=parser.getValue("Release", remoteObject),
																		localVersion=None,
																		type=parser.getValue("Type", remoteObject),
																		url=parser.getValue("Url", remoteObject),
																		comment=parser.getValue("Comment", remoteObject))
						else:
							LOGGER.info("{0} | '{1}' Repository Remote Object Skipped By '{2}' Command Line Parameter Value!".format(self.__class__.__name__, remoteObject, "databaseReadOnly"))
				else:
					if Constants.releaseVersion != parser.getValue("Release", remoteObject):
						releases[remoteObject] = ReleaseObject(name=remoteObject,
															repositoryVersion=parser.getValue("Release", remoteObject),
															localVersion=Constants.releaseVersion,
															url=parser.getValue("Url", remoteObject),
															type=parser.getValue("Type", remoteObject),
															comment=None)
			if releases:
				LOGGER.debug("> Initialising Remote Updater.")
				self.__remoteUpdater = RemoteUpdater(self, releases)
			else:
				self.__reportUpdateStatus and messageBox.messageBox("Information", "Information", "{0} | '{1}' Is Up To Date!".format(self.__class__.__name__, Constants.applicationName))
		else:
			raise foundations.exceptions.NetworkError("QNetworkAccessManager Error Code: '{0}'.".format(self.__releaseReply.error()))

	@core.executionTrace
	def checkForNewReleases(self):
		"""
		This Method Checks For New Releases.
		"""

		self.getReleaseFile(QUrl(os.path.join(self.__repositoryUrl, self.__releasesFileUrl)))

	@core.executionTrace
	def getReleaseFile(self, url):
		"""
		This Method Gets The Release File.
		"""

		LOGGER.debug("> Downloading '{0}' Releases File.".format(url.path()))

		self.__releaseReply = self.__networkAccessManager.get(QNetworkRequest(url))
		self.__releaseReply.finished.connect(self.__releaseReply__finished)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
