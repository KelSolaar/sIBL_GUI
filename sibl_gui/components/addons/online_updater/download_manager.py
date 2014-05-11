#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**download_manager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`DownloadManager` class.

**Others:**

"""

from __future__ import unicode_literals

import os
from PyQt4.QtCore import QFile
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QPixmap
from PyQt4.QtNetwork import QNetworkRequest

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.ui.common
import foundations.verbose
import umbra.ui.common

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UI_FILE", "DownloadManager"]

LOGGER = foundations.verbose.install_logger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Download_Manager.ui")

class DownloadManager(foundations.ui.common.QWidget_factory(ui_file=UI_FILE)):
	"""
	| Defines the Application download manager.
	| Once initialized with a `QNetworkAccessManager <http://doc.qt.nokia.com/qnetworkaccessmanager.html>`_ instance,
		a download directory and a list of requests ( List of online resources / files ),
		this class can proceed of the download of those requests using the :meth:`DownloadManager.start_download` method.
	"""

	# Custom signals definitions.
	download_finished = pyqtSignal()
	"""
	This signal is emited by the :class:`DownloadManager` class when a download is finished.
	"""

	def __init__(self, parent, network_access_manager, download_directory, requests=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param network_access_manager: Network access manager.
		:type network_access_manager: QNetworkAccessManager
		:param download_directory: Download directory.
		:type download_directory: unicode
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
		self.__network_access_manager = network_access_manager
		self.__download_directory = download_directory

		self.__ui_resources_directory = "resources/"
		self.__ui_resources_directory = os.path.join(os.path.dirname(__file__), self.__ui_resources_directory)
		self.__ui_logo_image = "sIBL_GUI_Small_Logo.png"

		self.__requests = None
		self.requests = requests
		self.__downloads = {}
		self.__current_request = None
		self.__current_file = None
		self.__current_filePath = None

		# Helper attribute for QNetwork reply crash.
		self.__download_status = None

		DownloadManager.__initialize_ui(self)

	@property
	def container(self):
		"""
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def network_access_manager(self):
		"""
		Property for **self.__network_access_manager** attribute.

		:return: self.__network_access_manager.
		:rtype: QNetworkAccessManager
		"""

		return self.__network_access_manager

	@network_access_manager.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def network_access_manager(self, value):
		"""
		Setter for **self.__network_access_manager** attribute.

		:param value: Attribute value.
		:type value: QNetworkAccessManager
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "network_access_manager"))

	@network_access_manager.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def network_access_manager(self):
		"""
		Deleter for **self.__network_access_manager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "network_access_manager"))

	@property
	def download_directory(self):
		"""
		Property for **self.__download_directory** attribute.

		:return: self.__download_directory.
		:rtype: unicode
		"""

		return self.__download_directory

	@download_directory.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def download_directory(self, value):
		"""
		Setter for **self.__download_directory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "download_directory"))

	@download_directory.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def download_directory(self):
		"""
		Deleter for **self.__download_directory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "download_directory"))

	@property
	def ui_resources_directory(self):
		"""
		Property for **self.__ui_resources_directory** attribute.

		:return: self.__ui_resources_directory.
		:rtype: unicode
		"""

		return self.__ui_resources_directory

	@ui_resources_directory.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_resources_directory(self, value):
		"""
		Setter for **self.__ui_resources_directory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_resources_directory"))

	@ui_resources_directory.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_resources_directory(self):
		"""
		Deleter for **self.__ui_resources_directory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_resources_directory"))

	@property
	def ui_logo_image(self):
		"""
		Property for **self.__ui_logo_image** attribute.

		:return: self.__ui_logo_image.
		:rtype: unicode
		"""

		return self.__ui_logo_image

	@ui_logo_image.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_logo_image(self, value):
		"""
		Setter for **self.__ui_logo_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_logo_image"))

	@ui_logo_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_logo_image(self):
		"""
		Deleter for **self.__ui_logo_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_logo_image"))

	@property
	def requests(self):
		"""
		Property for **self.__requests** attribute.

		:return: self.__requests.
		:rtype: list
		"""

		return self.__requests

	@requests.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def downloads(self, value):
		"""
		Setter for **self.__downloads** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "downloads"))

	@downloads.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def downloads(self):
		"""
		Deleter for **self.__downloads** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "downloads"))

	@property
	def current_request(self):
		"""
		Property for **self.__current_request** attribute.

		:return: self.__current_request.
		:rtype: QNetworkReply
		"""

		return self.__current_request

	@current_request.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def current_request(self, value):
		"""
		Setter for **self.__current_request** attribute.

		:param value: Attribute value.
		:type value: QNetworkReply
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "current_request"))

	@current_request.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def current_request(self):
		"""
		Deleter for **self.__current_request** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "current_request"))

	@property
	def current_file(self):
		"""
		Property for **self.__current_file** attribute.

		:return: self.__current_file.
		:rtype: QFile
		"""

		return self.__current_file

	@current_file.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def current_file(self, value):
		"""
		Setter for **self.__current_file** attribute.

		:param value: Attribute value.
		:type value: QFile
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "current_file"))

	@current_file.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def current_file(self):
		"""
		Deleter for **self.__current_file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "current_file"))

	@property
	def current_filePath(self):
		"""
		Property for **self.__current_filePath** attribute.

		:return: self.__current_filePath.
		:rtype: unicode
		"""

		return self.__current_filePath

	@current_filePath.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def current_filePath(self, value):
		"""
		Setter for **self.__current_filePath** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "current_filePath"))

	@current_filePath.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def current_filePath(self):
		"""
		Deleter for **self.__current_filePath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "current_filePath"))

	@property
	def download_status(self):
		"""
		Property for **self.__download_status** attribute.

		:return: self.__download_status.
		:rtype: QObject
		"""

		return self.__download_status

	@download_status.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def download_status(self, value):
		"""
		Setter for **self.__download_status** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "download_status"))

	@download_status.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def download_status(self):
		"""
		Deleter for **self.__download_status** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "download_status"))

	def closeEvent(self, event):
		"""
		Reimplements the :meth:`QWidget.closeEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		self.__download_status or self.abort_download()

		super(DownloadManager, self).closeEvent(event)

	def __initialize_ui(self):
		"""
		Initializes the Widget ui.
		"""

		umbra.ui.common.set_window_default_icon(self)

		self.Download_progressBar.setValue(0)
		self.Download_progressBar.hide()
		self.Logo_label.setPixmap(QPixmap(os.path.join(self.__ui_resources_directory, self.__ui_logo_image)))


		# Signals / Slots.
		self.Cancel_Close_pushButton.clicked.connect(self.__Cancel_Close_pushButton__clicked)

	def __Cancel_Close_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Cancel_Close_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.close()

	def __download_next(self):
		"""
		Downloads the next request.
		"""

		if not self.__requests:
			return

		self.Download_progressBar.show()

		self.__current_request = self.__network_access_manager.get(QNetworkRequest(QUrl(self.__requests.pop())))

		self.__current_filePath = os.path.join(self.__download_directory,
											os.path.basename(foundations.strings.to_string(self.__current_request.url().path())))
		if foundations.common.path_exists(self.__current_filePath):
			LOGGER.info("{0} | Removing '{1}' local file from previous online update!".format(
			self.__class__.__name__, os.path.basename(self.__current_filePath)))
			os.remove(self.__current_filePath)

		self.__current_file = QFile(self.__current_filePath)

		if not self.__current_file.open(QIODevice.WriteOnly):
			LOGGER.warning("!> Error occured while writing '{0}' file to disk, proceeding to next download!".format(
			self.__current_filePath))

			self.__download_next()
			return

		# Signals / Slots.
		self.__current_request.downloadProgress.connect(self.__download_progress)
		self.__current_request.finished.connect(self.__download_complete)
		self.__current_request.readyRead.connect(self.__request_ready)

	def __download_progress(self, bytes_received, bytes_total):
		"""
		Updates the download progress.

		:param bytes_received: Bytes received.
		:type bytes_received: int
		:param bytes_total: Bytes total.
		:type bytes_total: int
		"""

		LOGGER.debug("> Updating download progress: '{0}' bytes received, '{1}' bytes total.".format(bytes_received,
																									bytes_total))

		self.Current_File_label.setText("Downloading: '{0}'.".format(
		os.path.basename(foundations.strings.to_string(self.__current_request.url().path()))))
		self.Download_progressBar.setRange(0, bytes_total)
		self.Download_progressBar.setValue(bytes_received)

	def __request_ready(self):
		"""
		Defines the slot triggered by the request when ready.
		"""

		LOGGER.debug("> Updating '{0}' file content.".format(self.__current_file))

		self.__current_file.write(self.__current_request.readAll())

	def __download_complete(self):
		"""
		Defines the slot triggered by the request when download complete.
		"""

		LOGGER.debug("> '{0}' download complete.".format(self.__current_file))

		self.__current_file.close()
		self.__downloads[self.__current_filePath] = (self.__current_request.error(), self.__current_request.url().toString())
		self.Current_File_label.setText("'{0}' downloading done!".format(os.path.basename(self.__current_filePath)))
		self.Download_progressBar.hide()
		self.__current_request.deleteLater()

		if self.__requests:
			LOGGER.debug("> Proceeding to next download request.")
			self.__download_next()
		else:
			self.__download_status = True
			self.Current_File_label.setText("Downloads complete!")
			self.Cancel_Close_pushButton.setText("Close")
			self.download_finished.emit()

	def start_download(self):
		"""
		Triggers the download.

		:return: Method success.
		:rtype: bool
		"""

		self.__download_status = False
		self.__download_next()
		return True

	def abort_download(self):
		"""
		Aborts the current download.

		:return: Method success.
		:rtype: bool
		"""

		self.__current_request.abort()
		self.__current_request.deleteLater()
		return True
