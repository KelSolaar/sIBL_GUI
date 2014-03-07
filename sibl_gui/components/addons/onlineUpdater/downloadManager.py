#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**downloadManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`DownloadManager` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtCore import QFile
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QPixmap
from PyQt4.QtNetwork import QNetworkRequest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.ui.common
import foundations.verbose
import umbra.ui.common

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UI_FILE", "DownloadManager"]

LOGGER = foundations.verbose.installLogger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Download_Manager.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class DownloadManager(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	| Defines the Application download manager.
	| Once initialized with a `QNetworkAccessManager <http://doc.qt.nokia.com/qnetworkaccessmanager.html>`_ instance,
		a download directory and a list of requests ( List of online resources / files ),
		this class can proceed of the download of those requests using the :meth:`DownloadManager.startDownload` method.
	"""

	# Custom signals definitions.
	downloadFinished = pyqtSignal()
	"""
	This signal is emited by the :class:`DownloadManager` class when a download is finished. ( pyqtSignal )
	"""

	def __init__(self, parent, networkAccessManager, downloadDirectory, requests=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param networkAccessManager: Network access manager.
		:type networkAccessManager: QNetworkAccessManager
		:param downloadDirectory: Download directory.
		:type downloadDirectory: unicode
		:param requests: Download requests.
		:type requests: list
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(DownloadManager, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__networkAccessManager = networkAccessManager
		self.__downloadDirectory = downloadDirectory

		self.__uiResourcesDirectory = "resources/"
		self.__uiResourcesDirectory = os.path.join(os.path.dirname(__file__), self.__uiResourcesDirectory)
		self.__uiLogoImage = "sIBL_GUI_Small_Logo.png"

		self.__requests = None
		self.requests = requests
		self.__downloads = {}
		self.__currentRequest = None
		self.__currentFile = None
		self.__currentFilePath = None

		# Helper attribute for QNetwork reply crash.
		self.__downloadStatus = None

		DownloadManager.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def networkAccessManager(self):
		"""
		Property for **self.__networkAccessManager** attribute.

		:return: self.__networkAccessManager.
		:rtype: QNetworkAccessManager
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		Setter for **self.__networkAccessManager** attribute.

		:param value: Attribute value.
		:type value: QNetworkAccessManager
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		Deleter for **self.__networkAccessManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "networkAccessManager"))

	@property
	def downloadDirectory(self):
		"""
		Property for **self.__downloadDirectory** attribute.

		:return: self.__downloadDirectory.
		:rtype: unicode
		"""

		return self.__downloadDirectory

	@downloadDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloadDirectory(self, value):
		"""
		Setter for **self.__downloadDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "downloadDirectory"))

	@downloadDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloadDirectory(self):
		"""
		Deleter for **self.__downloadDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "downloadDirectory"))

	@property
	def uiResourcesDirectory(self):
		"""
		Property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory.
		:rtype: unicode
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		Setter for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		Deleter for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiLogoImage(self):
		"""
		Property for **self.__uiLogoImage** attribute.

		:return: self.__uiLogoImage.
		:rtype: unicode
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		Setter for **self.__uiLogoImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		Deleter for **self.__uiLogoImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiLogoImage"))

	@property
	def requests(self):
		"""
		Property for **self.__requests** attribute.

		:return: self.__requests.
		:rtype: list
		"""

		return self.__requests

	@requests.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def requests(self, value):
		"""
		Setter for **self.__requests** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("requests", value)
			for element in value:
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"requests", element)
		self.__requests = value

	@requests.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def requests(self):
		"""
		Deleter for **self.__requests** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requests"))

	@property
	def downloads(self):
		"""
		Property for **self.__downloads** attribute.

		:return: self.__downloads.
		:rtype: dict
		"""

		return self.__downloads

	@downloads.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloads(self, value):
		"""
		Setter for **self.__downloads** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "downloads"))

	@downloads.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloads(self):
		"""
		Deleter for **self.__downloads** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "downloads"))

	@property
	def currentRequest(self):
		"""
		Property for **self.__currentRequest** attribute.

		:return: self.__currentRequest.
		:rtype: QNetworkReply
		"""

		return self.__currentRequest

	@currentRequest.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentRequest(self, value):
		"""
		Setter for **self.__currentRequest** attribute.

		:param value: Attribute value.
		:type value: QNetworkReply
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "currentRequest"))

	@currentRequest.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentRequest(self):
		"""
		Deleter for **self.__currentRequest** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "currentRequest"))

	@property
	def currentFile(self):
		"""
		Property for **self.__currentFile** attribute.

		:return: self.__currentFile.
		:rtype: QFile
		"""

		return self.__currentFile

	@currentFile.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentFile(self, value):
		"""
		Setter for **self.__currentFile** attribute.

		:param value: Attribute value.
		:type value: QFile
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "currentFile"))

	@currentFile.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentFile(self):
		"""
		Deleter for **self.__currentFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "currentFile"))

	@property
	def currentFilePath(self):
		"""
		Property for **self.__currentFilePath** attribute.

		:return: self.__currentFilePath.
		:rtype: unicode
		"""

		return self.__currentFilePath

	@currentFilePath.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentFilePath(self, value):
		"""
		Setter for **self.__currentFilePath** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "currentFilePath"))

	@currentFilePath.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentFilePath(self):
		"""
		Deleter for **self.__currentFilePath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "currentFilePath"))

	@property
	def downloadStatus(self):
		"""
		Property for **self.__downloadStatus** attribute.

		:return: self.__downloadStatus.
		:rtype: QObject
		"""

		return self.__downloadStatus

	@downloadStatus.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloadStatus(self, value):
		"""
		Setter for **self.__downloadStatus** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "downloadStatus"))

	@downloadStatus.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloadStatus(self):
		"""
		Deleter for **self.__downloadStatus** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "downloadStatus"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def closeEvent(self, event):
		"""
		Reimplements the :meth:`QWidget.closeEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		self.__downloadStatus or self.abortDownload()

		super(DownloadManager, self).closeEvent(event)

	def __initializeUi(self):
		"""
		Initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		self.Download_progressBar.setValue(0)
		self.Download_progressBar.hide()
		self.Logo_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiLogoImage)))


		# Signals / Slots.
		self.Cancel_Close_pushButton.clicked.connect(self.__Cancel_Close_pushButton__clicked)

	def __Cancel_Close_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Cancel_Close_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.close()

	def __downloadNext(self):
		"""
		Downloads the next request.
		"""

		if not self.__requests:
			return

		self.Download_progressBar.show()

		self.__currentRequest = self.__networkAccessManager.get(QNetworkRequest(QUrl(self.__requests.pop())))

		self.__currentFilePath = os.path.join(self.__downloadDirectory,
											os.path.basename(foundations.strings.toString(self.__currentRequest.url().path())))
		if foundations.common.pathExists(self.__currentFilePath):
			LOGGER.info("{0} | Removing '{1}' local file from previous online update!".format(
			self.__class__.__name__, os.path.basename(self.__currentFilePath)))
			os.remove(self.__currentFilePath)

		self.__currentFile = QFile(self.__currentFilePath)

		if not self.__currentFile.open(QIODevice.WriteOnly):
			LOGGER.warning("!> Error occured while writing '{0}' file to disk, proceeding to next download!".format(
			self.__currentFilePath))

			self.__downloadNext()
			return

		# Signals / Slots.
		self.__currentRequest.downloadProgress.connect(self.__downloadProgress)
		self.__currentRequest.finished.connect(self.__downloadComplete)
		self.__currentRequest.readyRead.connect(self.__requestReady)

	def __downloadProgress(self, bytesReceived, bytesTotal):
		"""
		Updates the download progress.

		:param bytesReceived: Bytes received.
		:type bytesReceived: int
		:param bytesTotal: Bytes total.
		:type bytesTotal: int
		"""

		LOGGER.debug("> Updating download progress: '{0}' bytes received, '{1}' bytes total.".format(bytesReceived,
																									bytesTotal))

		self.Current_File_label.setText("Downloading: '{0}'.".format(
		os.path.basename(foundations.strings.toString(self.__currentRequest.url().path()))))
		self.Download_progressBar.setRange(0, bytesTotal)
		self.Download_progressBar.setValue(bytesReceived)

	def __requestReady(self):
		"""
		Defines the slot triggered by the request when ready.
		"""

		LOGGER.debug("> Updating '{0}' file content.".format(self.__currentFile))

		self.__currentFile.write(self.__currentRequest.readAll())

	def __downloadComplete(self):
		"""
		Defines the slot triggered by the request when download complete.
		"""

		LOGGER.debug("> '{0}' download complete.".format(self.__currentFile))

		self.__currentFile.close()
		self.__downloads[self.__currentFilePath] = (self.__currentRequest.error(), self.__currentRequest.url().toString())
		self.Current_File_label.setText("'{0}' downloading done!".format(os.path.basename(self.__currentFilePath)))
		self.Download_progressBar.hide()
		self.__currentRequest.deleteLater()

		if self.__requests:
			LOGGER.debug("> Proceeding to next download request.")
			self.__downloadNext()
		else:
			self.__downloadStatus = True
			self.Current_File_label.setText("Downloads complete!")
			self.Cancel_Close_pushButton.setText("Close")
			self.downloadFinished.emit()

	def startDownload(self):
		"""
		Triggers the download.

		:return: Method success.
		:rtype: bool
		"""

		self.__downloadStatus = False
		self.__downloadNext()
		return True

	def abortDownload(self):
		"""
		Aborts the current download.

		:return: Method success.
		:rtype: bool
		"""

		self.__currentRequest.abort()
		self.__currentRequest.deleteLater()
		return True
