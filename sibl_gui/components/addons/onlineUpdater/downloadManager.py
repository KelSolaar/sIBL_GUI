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
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
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
	| This class defines the Application download manager.
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
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param networkAccessManager: Network access manager. ( QNetworkAccessManager )
		:param downloadDirectory: Download directory. ( String )
		:param requests: Download requests. ( List )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
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
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def networkAccessManager(self):
		"""
		This method is the property for **self.__networkAccessManager** attribute.

		:return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This method is the setter method for **self.__networkAccessManager** attribute.

		:param value: Attribute value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This method is the deleter method for **self.__networkAccessManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "networkAccessManager"))

	@property
	def downloadDirectory(self):
		"""
		This method is the property for **self.__downloadDirectory** attribute.

		:return: self.__downloadDirectory. ( String )
		"""

		return self.__downloadDirectory

	@downloadDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloadDirectory(self, value):
		"""
		This method is the setter method for **self.__downloadDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "downloadDirectory"))

	@downloadDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloadDirectory(self):
		"""
		This method is the deleter method for **self.__downloadDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "downloadDirectory"))

	@property
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiLogoImage(self):
		"""
		This method is the property for **self.__uiLogoImage** attribute.

		:return: self.__uiLogoImage. ( String )
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This method is the setter method for **self.__uiLogoImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This method is the deleter method for **self.__uiLogoImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiLogoImage"))

	@property
	def requests(self):
		"""
		This method is the property for **self.__requests** attribute.

		:return: self.__requests. ( List )
		"""

		return self.__requests

	@requests.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def requests(self, value):
		"""
		This method is the setter method for **self.__requests** attribute.

		:param value: Attribute value. ( List )
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("requests", value)
			for element in value:
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"requests", element)
		self.__requests = value

	@requests.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def requests(self):
		"""
		This method is the deleter method for **self.__requests** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requests"))

	@property
	def downloads(self):
		"""
		This method is the property for **self.__downloads** attribute.

		:return: self.__downloads. ( Dictionary )
		"""

		return self.__downloads

	@downloads.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloads(self, value):
		"""
		This method is the setter method for **self.__downloads** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "downloads"))

	@downloads.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloads(self):
		"""
		This method is the deleter method for **self.__downloads** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "downloads"))

	@property
	def currentRequest(self):
		"""
		This method is the property for **self.__currentRequest** attribute.

		:return: self.__currentRequest. ( QNetworkReply )
		"""

		return self.__currentRequest

	@currentRequest.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentRequest(self, value):
		"""
		This method is the setter method for **self.__currentRequest** attribute.

		:param value: Attribute value. ( QNetworkReply )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "currentRequest"))

	@currentRequest.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentRequest(self):
		"""
		This method is the deleter method for **self.__currentRequest** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "currentRequest"))

	@property
	def currentFile(self):
		"""
		This method is the property for **self.__currentFile** attribute.

		:return: self.__currentFile. ( QFile )
		"""

		return self.__currentFile

	@currentFile.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentFile(self, value):
		"""
		This method is the setter method for **self.__currentFile** attribute.

		:param value: Attribute value. ( QFile )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "currentFile"))

	@currentFile.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentFile(self):
		"""
		This method is the deleter method for **self.__currentFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "currentFile"))

	@property
	def currentFilePath(self):
		"""
		This method is the property for **self.__currentFilePath** attribute.

		:return: self.__currentFilePath. ( String )
		"""

		return self.__currentFilePath

	@currentFilePath.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentFilePath(self, value):
		"""
		This method is the setter method for **self.__currentFilePath** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "currentFilePath"))

	@currentFilePath.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentFilePath(self):
		"""
		This method is the deleter method for **self.__currentFilePath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "currentFilePath"))

	@property
	def downloadStatus(self):
		"""
		This method is the property for **self.__downloadStatus** attribute.

		:return: self.__downloadStatus. ( QObject )
		"""

		return self.__downloadStatus

	@downloadStatus.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloadStatus(self, value):
		"""
		This method is the setter method for **self.__downloadStatus** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "downloadStatus"))

	@downloadStatus.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def downloadStatus(self):
		"""
		This method is the deleter method for **self.__downloadStatus** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "downloadStatus"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def closeEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.closeEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		self.__downloadStatus or self.abortDownload()

		super(DownloadManager, self).closeEvent(event)

	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		self.Download_progressBar.setValue(0)
		self.Download_progressBar.hide()
		self.Logo_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiLogoImage)))


		# Signals / Slots.
		self.Cancel_Close_pushButton.clicked.connect(self.__Cancel_Close_pushButton__clicked)

	def __Cancel_Close_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Cancel_Close_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.close()

	def __downloadNext(self):
		"""
		This method downloads the next request.
		"""

		if not self.__requests:
			return

		self.Download_progressBar.show()

		self.__currentRequest = self.__networkAccessManager.get(QNetworkRequest(QUrl(self.__requests.pop())))

		self.__currentFilePath = os.path.join(self.__downloadDirectory,
											os.path.basename(foundations.strings.encode(self.__currentRequest.url().path())))
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
		This method updates the download progress.

		:param bytesReceived: Bytes received. ( Integer )
		:param bytesTotal: Bytes total. ( Integer )
		"""

		LOGGER.debug("> Updating download progress: '{0}' bytes received, '{1}' bytes total.".format(bytesReceived,
																									bytesTotal))

		self.Current_File_label.setText("Downloading: '{0}'.".format(
		os.path.basename(foundations.strings.encode(self.__currentRequest.url().path()))))
		self.Download_progressBar.setRange(0, bytesTotal)
		self.Download_progressBar.setValue(bytesReceived)

	def __requestReady(self):
		"""
		This method is triggered when the request is ready to write.
		"""

		LOGGER.debug("> Updating '{0}' file content.".format(self.__currentFile))

		self.__currentFile.write(self.__currentRequest.readAll())

	def __downloadComplete(self):
		"""
		This method is triggered when the request download is complete.
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
		This method triggers the download.

		:return: Method success. ( Boolean )
		"""

		self.__downloadStatus = False
		self.__downloadNext()
		return True

	def abortDownload(self):
		"""
		This method aborts the current download.

		:return: Method success. ( Boolean )
		"""

		self.__currentRequest.abort()
		self.__currentRequest.deleteLater()
		return True
