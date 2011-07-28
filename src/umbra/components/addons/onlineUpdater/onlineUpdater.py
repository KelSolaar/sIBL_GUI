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
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**onlineUpdater.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Online Updater Component Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
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
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import umbra.components.core.db.dbUtilities.common as dbCommon
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from foundations.parser import Parser
from foundations.pkzip import Pkzip
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants
from umbra.ui.widgets.variable_QPushButton import Variable_QPushButton

#***********************************************************************************************
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

REPOSITORY_URL = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Repository/"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class ReleaseObject(core.Structure):
	"""
	This is the ReleaseObject class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		@param kwargs: name, repositoryversion, localversion, type, url, comment. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__dict__.update(kwargs)

class DownloadManager(QObject):
	"""
	This is the DownloadManager class.
	"""

	# Custom signals definitions.
	downloadFinished = pyqtSignal()

	@core.executionTrace
	def __init__(self, container, networkAccessManager, downloadDirectory, requests=None):
		"""
		This method initializes the class.

		@param container: Container. ( Object )
		@param networkAccessManager: Network access manager. ( QNetworkAccessManager )
		@param downloadDirectory: Download directory. ( String )
		@param requests: Download requests. ( List )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self)

		# --- Setting class attributes. ---
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

		# Helper attribute for QNetwork reply crash.
		self.__downloadStatus = None

		self.__ui = uic.loadUi(self.__uiPath)
		if "." in sys.path:
			sys.path.remove(".")

		self.initializeUi()

		self.__ui.show()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		@param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def networkAccessManager(self):
		"""
		This method is the property for the _networkAccessManager attribute.

		@return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This method is the setter method for the _networkAccessManager attribute.

		@param value: Attribute value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This method is the deleter method for the _networkAccessManager attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("networkAccessManager"))

	@property
	def downloadDirectory(self):
		"""
		This method is the property for the _downloadDirectory attribute.

		@return: self.__downloadDirectory. ( String )
		"""

		return self.__downloadDirectory

	@downloadDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadDirectory(self, value):
		"""
		This method is the setter method for the _downloadDirectory attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("downloadDirectory"))

	@downloadDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadDirectory(self):
		"""
		This method is the deleter method for the _downloadDirectory attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("downloadDirectory"))

	@property
	def uiPath(self):
		"""
		This method is the property for the _uiPath attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for the _uiPath attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for the _uiPath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This method is the property for the _uiResources attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for the _uiResources attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for the _uiResources attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiLogoImage(self):
		"""
		This method is the property for the _uiLogoImage attribute.

		@return: self.__uiLogoImage. ( String )
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This method is the setter method for the _uiLogoImage attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This method is the deleter method for the _uiLogoImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiLogoImage"))

	@property
	def requests(self):
		"""
		This method is the property for the _requests attribute.

		@return: self.__requests. ( List )
		"""

		return self.__requests

	@requests.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def requests(self, value):
		"""
		This method is the setter method for the _requests attribute.

		@param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("requests", value)
		self.__requests = value

	@requests.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def requests(self):
		"""
		This method is the deleter method for the _requests attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("requests"))

	@property
	def downloads(self):
		"""
		This method is the property for the _downloads attribute.

		@return: self.__downloads. ( List )
		"""

		return self.__downloads

	@downloads.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def downloads(self, value):
		"""
		This method is the setter method for the _downloads attribute.

		@param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("downloads"))

	@downloads.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloads(self):
		"""
		This method is the deleter method for the _downloads attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("downloads"))

	@property
	def currentRequest(self):
		"""
		This method is the property for the _currentRequest attribute.

		@return: self.__currentRequest. ( QNetworkReply )
		"""

		return self.__currentRequest

	@currentRequest.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentRequest(self, value):
		"""
		This method is the setter method for the _currentRequest attribute.

		@param value: Attribute value. ( QNetworkReply )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("currentRequest"))

	@currentRequest.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentRequest(self):
		"""
		This method is the deleter method for the _currentRequest attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("currentRequest"))

	@property
	def currentFile(self):
		"""
		This method is the property for the _currentFile attribute.

		@return: self.__currentFile. ( QFile )
		"""

		return self.__currentFile

	@currentFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFile(self, value):
		"""
		This method is the setter method for the _currentFile attribute.

		@param value: Attribute value. ( QFile )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("currentFile"))

	@currentFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFile(self):
		"""
		This method is the deleter method for the _currentFile attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("currentFile"))

	@property
	def currentFilePath(self):
		"""
		This method is the property for the _currentFilePath attribute.

		@return: self.__currentFilePath. ( String )
		"""

		return self.__currentFilePath

	@currentFilePath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFilePath(self, value):
		"""
		This method is the setter method for the _currentFilePath attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("currentFilePath"))

	@currentFilePath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFilePath(self):
		"""
		This method is the deleter method for the _currentFilePath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("currentFilePath"))

	@property
	def downloadStatus(self):
		"""
		This method is the property for the _downloadStatus attribute.

		@return: self.__downloadStatus. ( QObject )
		"""

		return self.__downloadStatus

	@downloadStatus.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadStatus(self, value):
		"""
		This method is the setter method for the _downloadStatus attribute.

		@param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("downloadStatus"))

	@downloadStatus.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadStatus(self):
		"""
		This method is the deleter method for the _downloadStatus attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("downloadStatus"))

	@property
	def ui(self):
		"""
		This method is the property for the _ui attribute.

		@return: self.__ui. ( Object )
		"""

		return self.__ui

	@ui.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self, value):
		"""
		This method is the setter method for the _ui attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("ui"))

	@ui.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self):
		"""
		This method is the deleter method for the _ui attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("ui"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self.ui)

		self.__ui.Download_progressBar.setValue(0)
		self.__ui.Download_progressBar.hide()
		self.__ui.Logo_label.setPixmap(QPixmap(os.path.join(self.__uiResources, self.__uiLogoImage)))

		self.__ui.closeEvent = self.closeEvent

		# Signals / slots.
		self.__ui.Cancel_Close_pushButton.clicked.connect(self.__Cancel_Close_pushButton__clicked)

	@core.executionTrace
	def closeEvent(self, closeEvent):
		"""
		This method overloads the download Manager close event.

		@param closeEvent: Close event. ( QCloseEvent )
		"""

		self.__downloadStatus or self.abortDownload()
		closeEvent.accept()

	@core.executionTrace
	def __Cancel_Close_pushButton__clicked(self, checked):
		"""
		This method triggers the downloadmanager close.

		@param checked: Checked state. ( Boolean )
		"""

		self.__ui.close()

	@core.executionTrace
	def __downloadNext(self):
		"""
		This method downloads the next request.
		"""

		if self.__requests:
			self.__ui.Download_progressBar.show()

			self.__currentRequest = self.__networkAccessManager.get(QNetworkRequest(QUrl(self.__requests.pop())))

			self.__currentFilePath = os.path.join(self.__downloadDirectory, os.path.basename(str(self.__currentRequest.url().path())))
			if os.path.exists(self.__currentFilePath):
				LOGGER.info("{0} | Removing '{1}' local file from previous online update!".format(self.__class__.__name__, os.path.basename(self.__currentFilePath)))
				os.remove(self.__currentFilePath)

			self.__currentFile = QFile(self.__currentFilePath)

			if not self.__currentFile.open(QIODevice.WriteOnly):
				messageBox.messageBox("Warning", "Warning", "{0} | Error while writing '{1}' file to disk, proceeding to next download!".format(self.__class__.__name__, os.path.basename(self.__currentFilePath)))
				self.__downloadNext()
				return

			# Signals / slots.
			self.__currentRequest.downloadProgress.connect(self.__downloadProgress)
			self.__currentRequest.finished.connect(self.__downloadComplete)
			self.__currentRequest.readyRead.connect(self.__requestReady)

	@core.executionTrace
	def __downloadProgress(self, bytesReceived, bytesTotal):
		"""
		This method updates the download progress.

		@param bytesReceived: Bytes received. ( Integer )
		@param bytesTotal: Bytes total. ( Integer )
		"""

		LOGGER.debug("> Updating download progress: '{0}' bytes received, '{1}' bytes total.".format(bytesReceived, bytesTotal))

		self.__ui.Current_File_label.setText("Downloading: '{0}'.".format(os.path.basename(str(self.__currentRequest.url().path()))))
		self.__ui.Download_progressBar.setRange(0, bytesTotal)
		self.__ui.Download_progressBar.setValue(bytesReceived)

	@core.executionTrace
	def __requestReady(self):
		"""
		This method is triggered when the request is ready to write.
		"""

		LOGGER.debug("> Updating '{0}' file content.".format(self.__currentFile))

		self.__currentFile.write(self.__currentRequest.readAll())

	@core.executionTrace
	def __downloadComplete(self):
		"""
		This method is triggered when the request download is complete.
		"""

		LOGGER.debug("> '{0}' download complete.".format(self.__currentFile))

		self.__currentFile.close()
		self.__downloads.append(self.__currentFilePath)
		self.__ui.Current_File_label.setText("'{0}' downloading done!".format(os.path.basename(self.__currentFilePath)))
		self.__ui.Download_progressBar.hide()
		self.__currentRequest.deleteLater();

		if self.__requests:
			LOGGER.debug("> Proceeding to next download request.")
			self.__downloadNext()
		else:
			self.__downloadStatus = True
			self.__ui.Current_File_label.setText("Downloads complete!")
			self.__ui.Cancel_Close_pushButton.setText("Close")
			self.emit(SIGNAL("downloadFinished()"))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def startDownload(self):
		"""
		This method triggers the download.

		@return: Method success. ( Boolean )
		"""

		self.__downloadStatus = False
		self.__downloadNext()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def abortDownload(self):
		"""
		This method aborts the current download.

		@return: Method success. ( Boolean )
		"""

		self.__currentRequest.abort()
		self.__currentRequest.deleteLater()
		return True

class RemoteUpdater(object):
	"""
	This class is the RemoteUpdater class.
	"""

	@core.executionTrace
	def __init__(self, container, releases=None):
		"""
		This method initializes the class.

		@param releases: Releases. ( Dictionary )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
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

		self.__templatesTableWidgetHeaders = ["_datas", "Get it!", "Local version", "Repository version", "Release type", "Comment"]

		self.__applicationChangeLogUrl = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Change%20Log/Change%20Log.html"
		self.__repositoryUrl = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository"

		self.__downloadManager = None
		self.__networkAccessManager = self.__container.networkAccessManager

		self.__ui = uic.loadUi(self.__uiPath)
		if "." in sys.path:
			sys.path.remove(".")

		self.initializeUi()

		self.__ui.show()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		@param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def releases(self):
		"""
		This method is the property for the _releases attribute.

		@return: self.__releases. ( Dictionary )
		"""

		return self.__releases

	@releases.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def releases(self, value):
		"""
		This method is the setter method for the _releases attribute.

		@param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("releases", value)
		self.__releases = value

	@releases.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releases(self):
		"""
		This method is the deleter method for the _releases attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("releases"))

	@property
	def uiPath(self):
		"""
		This method is the property for the _uiPath attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for the _uiPath attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for the _uiPath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This method is the property for the _uiResources attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for the _uiResources attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for the _uiResources attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiLogoImage(self):
		"""
		This method is the property for the _uiLogoImage attribute.

		@return: self.__uiLogoImage. ( String )
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This method is the setter method for the _uiLogoImage attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This method is the deleter method for the _uiLogoImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiLogoImage"))

	@property
	def uiTemplatesImage(self):
		"""
		This method is the property for the _uiTemplatesImage attribute.

		@return: self.__uiTemplatesImage. ( String )
		"""

		return self.__uiTemplatesImage

	@uiTemplatesImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiTemplatesImage(self, value):
		"""
		This method is the setter method for the _uiTemplatesImage attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiTemplatesImage"))

	@uiTemplatesImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiTemplatesImage(self):
		"""
		This method is the deleter method for the _uiTemplatesImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiTemplatesImage"))

	@property
	def uiLightGrayColor(self):
		"""
		This method is the property for the _uiLightGrayColor attribute.

		@return: self.__uiLightGrayColor. ( QColor )
		"""

		return self.__uiLightGrayColor

	@uiLightGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self, value):
		"""
		This method is the setter method for the _uiLightGrayColor attribute.

		@param value: Attribute value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiLightGrayColor"))

	@uiLightGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self):
		"""
		This method is the deleter method for the _uiLightGrayColor attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiLightGrayColor"))

	@property
	def uiDarkGrayColor(self):
		"""
		This method is the property for the _uiDarkGrayColor attribute.

		@return: self.__uiDarkGrayColor. ( QColor )
		"""

		return self.__uiDarkGrayColor

	@uiDarkGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self, value):
		"""
		This method is the setter method for the _uiDarkGrayColor attribute.

		@param value: Attribute value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiDarkGrayColor"))

	@uiDarkGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self):
		"""
		This method is the deleter method for the _uiDarkGrayColor attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiDarkGrayColor"))

	@property
	def splitter(self):
		"""
		This method is the property for the _splitter attribute.

		@return: self.__splitter. ( String )
		"""

		return self.__splitter

	@splitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def splitter(self, value):
		"""
		This method is the setter method for the _splitter attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("splitter"))

	@splitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def splitter(self):
		"""
		This method is the deleter method for the _splitter attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("splitter"))

	@property
	def tableWidgetRowHeight(self):
		"""
		This method is the property for the _tableWidgetRowHeight attribute.

		@return: self.__tableWidgetRowHeight. ( Integer )
		"""

		return self.__tableWidgetRowHeight

	@tableWidgetRowHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self, value):
		"""
		This method is the setter method for the _tableWidgetRowHeight attribute.

		@param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("tableWidgetRowHeight"))

	@tableWidgetRowHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self):
		"""
		This method is the deleter method for the _tableWidgetRowHeight attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("tableWidgetRowHeight"))

	@property
	def tableWidgetHeaderHeight(self):
		"""
		This method is the property for the _tableWidgetHeaderHeight attribute.

		@return: self.__tableWidgetHeaderHeight. ( Integer )
		"""

		return self.__tableWidgetHeaderHeight

	@tableWidgetHeaderHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self, value):
		"""
		This method is the setter method for the _tableWidgetHeaderHeight attribute.

		@param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("tableWidgetHeaderHeight"))

	@tableWidgetHeaderHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self):
		"""
		This method is the deleter method for the _tableWidgetHeaderHeight attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("tableWidgetHeaderHeight"))

	@property
	def templatesTableWidgetHeaders(self):
		"""
		This method is the property for the _templatesTableWidgetHeaders attribute.

		@return: self.__templatesTableWidgetHeaders. ( String )
		"""

		return self.__templatesTableWidgetHeaders

	@templatesTableWidgetHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesTableWidgetHeaders(self, value):
		"""
		This method is the setter method for the _templatesTableWidgetHeaders attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templatesTableWidgetHeaders"))

	@templatesTableWidgetHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesTableWidgetHeaders(self):
		"""
		This method is the deleter method for the _templatesTableWidgetHeaders attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templatesTableWidgetHeaders"))

	@property
	def applicationChangeLogUrl(self):
		"""
		This method is the property for the _applicationChangeLogUrl attribute.

		@return: self.__applicationChangeLogUrl. ( String )
		"""

		return self.__applicationChangeLogUrl

	@applicationChangeLogUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def applicationChangeLogUrl(self, value):
		"""
		This method is the setter method for the _applicationChangeLogUrl attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("applicationChangeLogUrl"))

	@applicationChangeLogUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def applicationChangeLogUrl(self):
		"""
		This method is the deleter method for the _applicationChangeLogUrl attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("applicationChangeLogUrl"))

	@property
	def repositoryUrl(self):
		"""
		This method is the property for the _repositoryUrl attribute.

		@return: self.__repositoryUrl. ( String )
		"""

		return self.__repositoryUrl

	@repositoryUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self, value):
		"""
		This method is the setter method for the _repositoryUrl attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("repositoryUrl"))

	@repositoryUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self):
		"""
		This method is the deleter method for the _repositoryUrl attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("repositoryUrl"))

	@property
	def downloadManager(self):
		"""
		This method is the property for the _downloadManager attribute.

		@return: self.__downloadManager. ( Object )
		"""

		return self.__downloadManager

	@downloadManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadManager(self, value):
		"""
		This method is the setter method for the _downloadManager attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("downloadManager"))

	@downloadManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadManager(self):
		"""
		This method is the deleter method for the _downloadManager attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("downloadManager"))

	@property
	def networkAccessManager(self):
		"""
		This method is the property for the _networkAccessManager attribute.

		@return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This method is the setter method for the _networkAccessManager attribute.

		@param value: Attribute value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This method is the deleter method for the _networkAccessManager attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("networkAccessManager"))

	@property
	def ui(self):
		"""
		This method is the property for the _ui attribute.

		@return: self.__ui. ( Object )
		"""

		return self.__ui

	@ui.setter
	def ui(self, value):
		"""
		This method is the setter method for the _ui attribute.

		@param value: Attribute value. ( Object )
		"""

		self.__ui = value

	@ui.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self):
		"""
		This method is the deleter method for the _ui attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("ui"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Remote_Updater Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self.ui)

		LOGGER.debug("> Initializing '{0}' ui.".format(self.__class__.__name__))

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

		# Signals / slots.
		self.__ui.Get_sIBL_GUI_pushButton.clicked.connect(self.__Get_sIBL_GUI_pushButton__clicked)
		self.__ui.Get_Latest_Templates_pushButton.clicked.connect(self.__Get_Latest_Templates_pushButton__clicked)
		self.__ui.Open_Repository_pushButton.clicked.connect(self.__Open_Repository_pushButton__clicked)
		self.__ui.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

	@core.executionTrace
	def __Get_sIBL_GUI_pushButton__clicked(self, checked):
		"""
		This method is triggered when Get_sIBL_GUI_pushButton is clicked.

		@param checked: Checked state. ( Boolean )
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
		This method is triggered when Get_Latest_Templates_pushButton is clicked.

		@param checked: Checked state. ( Boolean )
		"""

		requests = []
		for row in range(self.__ui.Templates_tableWidget.rowCount()):
			if self.__ui.Templates_tableWidget.cellWidget(row, 1).state:
				requests.append(self.__ui.Templates_tableWidget.item(row, 0)._datas)
		if requests:
			downloadDirectory = self.__getTemplatesDownloadDirectory()
			if downloadDirectory:
				LOGGER.debug("> Templates download directory: '{0}'.".format(downloadDirectory))
				self.__downloadManager = DownloadManager(self, self.__networkAccessManager, downloadDirectory, [request.url for request in requests])
				self.__downloadManager.downloadFinished.connect(self.__downloadManager__finished)
				self.__downloadManager.startDownload()

	@core.executionTrace
	def __Open_Repository_pushButton__clicked(self, checked):
		"""
		This method is triggered when Open_Repository_pushButton is clicked.

		@param checked: Checked state. ( Boolean )
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(self.__repositoryUrl))
		QDesktopServices.openUrl(QUrl(QString(self.__repositoryUrl)))

	@core.executionTrace
	def __Close_pushButton__clicked(self, checked):
		"""
		This method closes the RemoteUpdater.

		@param checked: Checked state. ( Boolean )
		"""

		LOGGER.info("{0} | Closing '{1}' updater!".format(self.__class__.__name__, Constants.applicationName))
		self.__ui.close()

	@core.executionTrace
	def __downloadManager__finished(self):
		"""
		This method is triggered when the download Manager finishes.
		"""

		for download in self.__downloadManager.downloads:
			if download.endswith(".zip"):
				if self.extractZipFile(download):
					LOGGER.info("{0} | Removing '{1}' archive!".format(self.__class__.__name__, download))
					os.remove(download)
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | Failed extracting '{1}', proceeding to next file!".format(self.__class__.__name__, os.path.basename(download)))
				self.__container.coreTemplatesOutliner.addDirectory(os.path.dirname(download), self.__container.coreTemplatesOutliner.getCollection(self.__container.coreTemplatesOutliner.userCollection).id)
			else:
				if self.__container.addonsLocationsBrowser.activated:
					self.__container.addonsLocationsBrowser.exploreDirectory(os.path.dirname(download))

	@core.executionTrace
	def __getTemplatesDownloadDirectory(self):
		"""
		This method gets the Templates directory.
		"""

		LOGGER.debug("> Retrieving Templates download directory.")

		messageBox = QMessageBox()
		messageBox.setWindowTitle("{0}".format(self.__class__.__name__))
		messageBox.setIcon(QMessageBox.Question)
		messageBox.setText("{0} | Which directory do you want to install the Templates into?".format(self.__class__.__name__))
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
			return self.__container.container.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self.__ui, "Choose Templates directory:", self.__container.container.lastBrowsedPath)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def extractZipFile(self, file):
		"""
		This method uncompress the provided zip file.

		@param file: File to extract. ( String )
		@return: Extraction success. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}' file uncompress.".format(file))

		pkzip = Pkzip()
		pkzip.archive = file

		return pkzip.extract(os.path.dirname(file))

class OnlineUpdater(UiComponent):
	"""
	This class is the OnlineUpdater class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		@param name: Component name. ( String )
		@param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
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

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for the _uiPath attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for the _uiPath attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for the _uiPath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		@param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def settings(self):
		"""
		This method is the property for the _settings attribute.

		@return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@property
	def settingsSection(self):
		"""
		This method is the property for the _settingsSection attribute.

		@return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for the _settingsSection attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for the _settingsSection attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settingsSection"))

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for the _settings attribute.

		@param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for the _settings attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))

	@property
	def corePreferencesManager(self):
		"""
		This method is the property for the _corePreferencesManager attribute.

		@return: self.__corePreferencesManager. ( Object )
		"""

		return self.__corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self, value):
		"""
		This method is the setter method for the _corePreferencesManager attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("corePreferencesManager"))

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self):
		"""
		This method is the deleter method for the _corePreferencesManager attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("corePreferencesManager"))

	@property
	def coreDb(self):
		"""
		This method is the property for the _coreDb attribute.

		@return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This method is the setter method for the _coreDb attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for the _coreDb attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDb"))

	@property
	def coreTemplatesOutliner(self):
		"""
		This method is the property for the _coreTemplatesOutliner attribute.

		@return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This method is the setter method for the _coreTemplatesOutliner attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This method is the deleter method for the _coreTemplatesOutliner attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreTemplatesOutliner"))

	@property
	def addonsLocationsBrowser(self):
		"""
		This method is the property for the _addonsLocationsBrowser attribute.

		@return: self.__addonsLocationsBrowser. ( Object )
		"""

		return self.__addonsLocationsBrowser

	@addonsLocationsBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLocationsBrowser(self, value):
		"""
		This method is the setter method for the _addonsLocationsBrowser attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("addonsLocationsBrowser"))

	@addonsLocationsBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLocationsBrowser(self):
		"""
		This method is the deleter method for the _addonsLocationsBrowser attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("addonsLocationsBrowser"))

	@property
	def ioDirectory(self):
		"""
		This method is the property for the _ioDirectory attribute.

		@return: self.__ioDirectory. ( String )
		"""

		return self.__ioDirectory

	@ioDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self, value):
		"""
		This method is the setter method for the _ioDirectory attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("ioDirectory"))

	@ioDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self):
		"""
		This method is the deleter method for the _ioDirectory attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("ioDirectory"))

	@property
	def repositoryUrl(self):
		"""
		This method is the property for the _repositoryUrl attribute.

		@return: self.__repositoryUrl. ( String )
		"""

		return self.__repositoryUrl

	@repositoryUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self, value):
		"""
		This method is the setter method for the _repositoryUrl attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("repositoryUrl"))

	@repositoryUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self):
		"""
		This method is the deleter method for the _repositoryUrl attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("repositoryUrl"))

	@property
	def releasesFileUrl(self):
		"""
		This method is the property for the _releasesFileUrl attribute.

		@return: self.__releasesFileUrl. ( String )
		"""

		return self.__releasesFileUrl

	@releasesFileUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releasesFileUrl(self, value):
		"""
		This method is the setter method for the _releasesFileUrl attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("releasesFileUrl"))

	@releasesFileUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releasesFileUrl(self):
		"""
		This method is the deleter method for the _releasesFileUrl attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("releasesFileUrl"))

	@property
	def networkAccessManager(self):
		"""
		This method is the property for the _networkAccessManager attribute.

		@return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This method is the setter method for the _networkAccessManager attribute.

		@param value: Attribute value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This method is the deleter method for the _networkAccessManager attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("networkAccessManager"))

	@property
	def releaseReply(self):
		"""
		This method is the property for the _releaseReply attribute.

		@return: self.__releaseReply. ( QNetworkReply )
		"""

		return self.__releaseReply

	@releaseReply.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releaseReply(self, value):
		"""
		This method is the setter method for the _releaseReply attribute.

		@param value: Attribute value. ( QNetworkReply )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("releaseReply"))

	@releaseReply.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releaseReply(self):
		"""
		This method is the deleter method for the _releaseReply attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("releaseReply"))

	@property
	def remoteUpdater(self):
		"""
		This method is the property for the _remoteUpdater attribute.

		@return: self.__remoteUpdater. ( Object )
		"""

		return self.__remoteUpdater

	@remoteUpdater.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def remoteUpdater(self, value):
		"""
		This method is the setter method for the _remoteUpdater attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("remoteUpdater"))

	@remoteUpdater.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def remoteUpdater(self):
		"""
		This method is the deleter method for the _remoteUpdater attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("remoteUpdater"))

	@property
	def reportUpdateStatus(self):
		"""
		This method is the property for the _reportUpdateStatus attribute.

		@return: self.__reportUpdateStatus. ( Boolean )
		"""

		return self.__reportUpdateStatus

	@reportUpdateStatus.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reportUpdateStatus(self, value):
		"""
		This method is the setter method for the _reportUpdateStatus attribute.

		@param value: Attribute value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("reportUpdateStatus"))

	@reportUpdateStatus.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reportUpdateStatus(self):
		"""
		This method is the deleter method for the _reportUpdateStatus attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("reportUpdateStatus"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		@param container: Container to attach the Component to. ( QObject )
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
		This method deactivates the Component.
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
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__container.parameters.deactivateWorkerThreads and LOGGER.info("{0} | 'OnStartup' Online Updater worker thread deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "deactivateWorkerThreads"))

		self.__Check_For_New_Releases_On_Startup_checkBox_setUi()
		self.__Ignore_Non_Existing_Templates_checkBox_setUi()

		# Signals / slots.
		self.ui.Check_For_New_Releases_pushButton.clicked.connect(self.__Check_For_New_Releases_pushButton__clicked)
		self.ui.Check_For_New_Releases_On_Startup_checkBox.stateChanged.connect(self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.ui.Ignore_Non_Existing_Templates_checkBox.stateChanged.connect(self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / slots.
		self.ui.Check_For_New_Releases_pushButton.clicked.disconnect(self.__Check_For_New_Releases_pushButton__clicked)
		self.ui.Check_For_New_Releases_On_Startup_checkBox.stateChanged.disconnect(self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.ui.Ignore_Non_Existing_Templates_checkBox.stateChanged.disconnect(self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

	@core.executionTrace
	def onStartup(self):
		"""
		This method is called on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework startup method.".format(self.__class__.__name__))

		self.__reportUpdateStatus = False
		not self.__container.parameters.deactivateWorkerThreads and self.ui.Check_For_New_Releases_On_Startup_checkBox.isChecked() and self.checkForNewReleases()

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Online_Updater_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.ui.Online_Updater_groupBox.setParent(None)

	@core.executionTrace
	def __Check_For_New_Releases_On_Startup_checkBox_setUi(self):
		"""
		This method sets the Check_For_New_Releases_On_Startup_checkBox.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "checkForNewReleasesOnStartup").isNull() and self.__settings.setKey(self.__settingsSection, "checkForNewReleasesOnStartup", Qt.Checked)

		checkForNewReleasesOnStartup = self.__settings.getKey(self.__settingsSection, "checkForNewReleasesOnStartup")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Check_For_New_Releases_On_Startup_checkBox", checkForNewReleasesOnStartup.toInt()[0]))
		self.ui.Check_For_New_Releases_On_Startup_checkBox.setCheckState(checkForNewReleasesOnStartup.toInt()[0])

	@core.executionTrace
	def __Check_For_New_Releases_On_Startup_checkBox__stateChanged(self, state):
		"""
		This method is called when Check_For_New_Releases_On_Startup_checkBox state changes.

		@param state: Checkbox state. ( Integer )
		"""

		LOGGER.debug("> Check for new releases on startup state: '{0}'.".format(self.ui.Check_For_New_Releases_On_Startup_checkBox.checkState()))
		self.__settings.setKey(self.__settingsSection, "checkForNewReleasesOnStartup", self.ui.Check_For_New_Releases_On_Startup_checkBox.checkState())

	@core.executionTrace
	def __Ignore_Non_Existing_Templates_checkBox_setUi(self):
		"""
		This method sets the Ignore_Non_Existing_Templates_checkBox.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "ignoreNonExistingTemplates").isNull() and self.__settings.setKey(self.__settingsSection, "ignoreNonExistingTemplates", Qt.Checked)

		ignoreNonExistingTemplates = self.__settings.getKey(self.__settingsSection, "ignoreNonExistingTemplates")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Ignore_Non_Existing_Templates_checkBox", ignoreNonExistingTemplates.toInt()[0]))
		self.ui.Ignore_Non_Existing_Templates_checkBox.setCheckState(ignoreNonExistingTemplates.toInt()[0])

	@core.executionTrace
	def __Ignore_Non_Existing_Templates_checkBox__stateChanged(self, state):
		"""
		This method is called when Ignore_Non_Existing_Templates_checkBox state changes.

		@param state: Checkbox state. ( Integer )
		"""

		LOGGER.debug("> Ignore non existing Templates state: '{0}'.".format(self.ui.Ignore_Non_Existing_Templates_checkBox.checkState()))
		self.__settings.setKey(self.__settingsSection, "ignoreNonExistingTemplates", self.ui.Ignore_Non_Existing_Templates_checkBox.checkState())

	@core.executionTrace
	def __Check_For_New_Releases_pushButton__clicked(self, checked):
		"""
		This method is triggered when Check_For_New_Releases_pushButton is clicked.

		@param checked: Checked state. ( Boolean )
		"""

		self.checkForNewReleases__()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.NetworkError)
	def __releaseReply__finished(self):
		"""
		This method is triggered when the release reply finishes.
		"""

		if not self.__releaseReply.error():
			content = []
			while not self.__releaseReply.atEnd ():
				content.append(str(self.__releaseReply.readLine()))

			LOGGER.debug("> Parsing releases file content.")
			parser = Parser()
			parser.content = content
			parser.parse()

			releases = {}
			for remoteObject in parser.sections:
				if remoteObject != Constants.applicationName:
						dbTemplates = dbCommon.filterTemplates(self.__coreDb.dbSession, "^{0}$".format(remoteObject), "name")
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
							LOGGER.info("{0} | '{1}' repository remote object skipped by '{2}' command line parameter value!".format(self.__class__.__name__, remoteObject, "databaseReadOnly"))
				else:
					if Constants.releaseVersion != parser.getValue("Release", remoteObject):
						releases[remoteObject] = ReleaseObject(name=remoteObject,
															repositoryVersion=parser.getValue("Release", remoteObject),
															localVersion=Constants.releaseVersion,
															url=parser.getValue("Url", remoteObject),
															type=parser.getValue("Type", remoteObject),
															comment=None)
			if releases:
				LOGGER.debug("> Initializing Remote Updater.")
				self.__remoteUpdater = RemoteUpdater(self, releases)
			else:
				self.__reportUpdateStatus and messageBox.messageBox("Information", "Information", "{0} | '{1}' is up to date!".format(self.__class__.__name__, Constants.applicationName))
		else:
			raise foundations.exceptions.NetworkError("QNetworkAccessManager error code: '{0}'.".format(self.__releaseReply.error()))

	@core.executionTrace
	def __getReleaseFile(self, url):
		"""
		This method gets the release file.
		"""

		LOGGER.debug("> Downloading '{0}' releases file.".format(url.path()))

		self.__releaseReply = self.__networkAccessManager.get(QNetworkRequest(url))
		self.__releaseReply.finished.connect(self.__releaseReply__finished)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def checkForNewReleases__(self):
		"""
		This method checks for new releases.

		@return: Method success. ( Boolean )
		"""

		self.__reportUpdateStatus = True
		if self.checkForNewReleases():
			return True
		else:
			raise Exception, "{0} | Exception raised while checking for new releases!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def checkForNewReleases(self):
		"""
		This method checks for new releases.

		@return: Method success. ( Boolean )
		"""

		self.__getReleaseFile(QUrl(os.path.join(self.__repositoryUrl, self.__releasesFileUrl)))
		return True

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
