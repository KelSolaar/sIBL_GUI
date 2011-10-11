#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**downloadManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`DownloadManager` class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.ui.common
import umbra.exceptions
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UI_FILE", "DownloadManager"]

LOGGER = logging.getLogger(Constants.logger)

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Download_Manager.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class DownloadManager(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	| This class defines the Application download manager.
	| Once initialized with a `QNetworkAccessManager <http://doc.qt.nokia.com/4.7/qnetworkaccessmanager.html>`_ instance, a download directory and a list of requests ( List of online resources / files ), this class can proceed of the download of those requests using the :meth:`DownloadManager.startDownload` method.
	"""

	# Custom signals definitions.
	downloadFinished = pyqtSignal()

	@core.executionTrace
	def __init__(self, parent, networkAccessManager, downloadDirectory, requests=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param networkAccessManager: Network access manager. ( QNetworkAccessManager )
		:param downloadDirectory: Download directory. ( String )
		:param requests: Download requests. ( List )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(DownloadManager, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__networkAccessManager = networkAccessManager
		self.__downloadDirectory = downloadDirectory

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

		DownloadManager.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def networkAccessManager(self):
		"""
		This method is the property for **self.__networkAccessManager** attribute.

		:return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This method is the setter method for **self.__networkAccessManager** attribute.

		:param value: Attribute value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This method is the deleter method for **self.__networkAccessManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("networkAccessManager"))

	@property
	def downloadDirectory(self):
		"""
		This method is the property for **self.__downloadDirectory** attribute.

		:return: self.__downloadDirectory. ( String )
		"""

		return self.__downloadDirectory

	@downloadDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadDirectory(self, value):
		"""
		This method is the setter method for **self.__downloadDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("downloadDirectory"))

	@downloadDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadDirectory(self):
		"""
		This method is the deleter method for **self.__downloadDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("downloadDirectory"))

	@property
	def uiResources(self):
		"""
		This method is the property for **self.__uiResources** attribute.

		:return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for **self.__uiResources** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for **self.__uiResources** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiLogoImage(self):
		"""
		This method is the property for **self.__uiLogoImage** attribute.

		:return: self.__uiLogoImage. ( String )
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This method is the setter method for **self.__uiLogoImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This method is the deleter method for **self.__uiLogoImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiLogoImage"))

	@property
	def requests(self):
		"""
		This method is the property for **self.__requests** attribute.

		:return: self.__requests. ( List )
		"""

		return self.__requests

	@requests.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def requests(self, value):
		"""
		This method is the setter method for **self.__requests** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("requests", value)
		self.__requests = value

	@requests.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def requests(self):
		"""
		This method is the deleter method for **self.__requests** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("requests"))

	@property
	def downloads(self):
		"""
		This method is the property for **self.__downloads** attribute.

		:return: self.__downloads. ( List )
		"""

		return self.__downloads

	@downloads.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def downloads(self, value):
		"""
		This method is the setter method for **self.__downloads** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("downloads"))

	@downloads.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloads(self):
		"""
		This method is the deleter method for **self.__downloads** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("downloads"))

	@property
	def currentRequest(self):
		"""
		This method is the property for **self.__currentRequest** attribute.

		:return: self.__currentRequest. ( QNetworkReply )
		"""

		return self.__currentRequest

	@currentRequest.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentRequest(self, value):
		"""
		This method is the setter method for **self.__currentRequest** attribute.

		:param value: Attribute value. ( QNetworkReply )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("currentRequest"))

	@currentRequest.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentRequest(self):
		"""
		This method is the deleter method for **self.__currentRequest** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("currentRequest"))

	@property
	def currentFile(self):
		"""
		This method is the property for **self.__currentFile** attribute.

		:return: self.__currentFile. ( QFile )
		"""

		return self.__currentFile

	@currentFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFile(self, value):
		"""
		This method is the setter method for **self.__currentFile** attribute.

		:param value: Attribute value. ( QFile )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("currentFile"))

	@currentFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFile(self):
		"""
		This method is the deleter method for **self.__currentFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("currentFile"))

	@property
	def currentFilePath(self):
		"""
		This method is the property for **self.__currentFilePath** attribute.

		:return: self.__currentFilePath. ( String )
		"""

		return self.__currentFilePath

	@currentFilePath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFilePath(self, value):
		"""
		This method is the setter method for **self.__currentFilePath** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("currentFilePath"))

	@currentFilePath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentFilePath(self):
		"""
		This method is the deleter method for **self.__currentFilePath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("currentFilePath"))

	@property
	def downloadStatus(self):
		"""
		This method is the property for **self.__downloadStatus** attribute.

		:return: self.__downloadStatus. ( QObject )
		"""

		return self.__downloadStatus

	@downloadStatus.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadStatus(self, value):
		"""
		This method is the setter method for **self.__downloadStatus** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("downloadStatus"))

	@downloadStatus.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadStatus(self):
		"""
		This method is the deleter method for **self.__downloadStatus** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("downloadStatus"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def closeEvent(self, closeEvent):
		"""
		This method overloads the download manager close event.

		:param closeEvent: Close event. ( QCloseEvent )
		"""

		self.__downloadStatus or self.abortDownload()
		closeEvent.accept()

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		self.Download_progressBar.setValue(0)
		self.Download_progressBar.hide()
		self.Logo_label.setPixmap(QPixmap(os.path.join(self.__uiResources, self.__uiLogoImage)))

		self.closeEvent = self.closeEvent

		# Signals / Slots.
		self.Cancel_Close_pushButton.clicked.connect(self.__Cancel_Close_pushButton__clicked)

	@core.executionTrace
	def __Cancel_Close_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Cancel_Close_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.close()

	@core.executionTrace
	def __downloadNext(self):
		"""
		This method downloads the next request.
		"""

		if self.__requests:
			self.Download_progressBar.show()

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

			# Signals / Slots.
			self.__currentRequest.downloadProgress.connect(self.__downloadProgress)
			self.__currentRequest.finished.connect(self.__downloadComplete)
			self.__currentRequest.readyRead.connect(self.__requestReady)

	@core.executionTrace
	def __downloadProgress(self, bytesReceived, bytesTotal):
		"""
		This method updates the download progress.

		:param bytesReceived: Bytes received. ( Integer )
		:param bytesTotal: Bytes total. ( Integer )
		"""

		LOGGER.debug("> Updating download progress: '{0}' bytes received, '{1}' bytes total.".format(bytesReceived, bytesTotal))

		self.Current_File_label.setText("Downloading: '{0}'.".format(os.path.basename(str(self.__currentRequest.url().path()))))
		self.Download_progressBar.setRange(0, bytesTotal)
		self.Download_progressBar.setValue(bytesReceived)

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
		self.Current_File_label.setText("'{0}' downloading done!".format(os.path.basename(self.__currentFilePath)))
		self.Download_progressBar.hide()
		self.__currentRequest.deleteLater();

		if self.__requests:
			LOGGER.debug("> Proceeding to next download request.")
			self.__downloadNext()
		else:
			self.__downloadStatus = True
			self.Current_File_label.setText("Downloads complete!")
			self.Cancel_Close_pushButton.setText("Close")
			self.downloadFinished.emit()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def startDownload(self):
		"""
		This method triggers the download.

		:return: Method success. ( Boolean )
		"""

		self.__downloadStatus = False
		self.__downloadNext()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def abortDownload(self):
		"""
		This method aborts the current download.

		:return: Method success. ( Boolean )
		"""

		self.__currentRequest.abort()
		self.__currentRequest.deleteLater()
		return True

