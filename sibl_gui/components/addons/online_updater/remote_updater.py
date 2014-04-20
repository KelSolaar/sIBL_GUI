#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**remote_updater.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`RemoteUpdater` class and others online update related objects.

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
import platform
from PyQt4.QtCore import QByteArray
from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPalette
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QTableWidgetItem

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.data_structures
import foundations.exceptions
import foundations.io
import foundations.ui.common
import foundations.verbose
import umbra.ui.common
import umbra.ui.widgets.message_box as message_box
from foundations.pkzip import Pkzip
from sibl_gui.components.addons.online_updater.download_manager import DownloadManager
from sibl_gui.components.addons.online_updater.views import TemplatesReleases_QTableWidget
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.ui.widgets.variable_QPushButton import Variable_QPushButton

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "ReleaseObject", "RemoteUpdater"]

LOGGER = foundations.verbose.install_logger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Remote_Updater.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ReleaseObject(foundations.data_structures.Structure):
	"""
	Defines a storage object for a :class:`RemoteUpdater` class release.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: name, repository_version, local_version, type, url, comment.
		:type kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.data_structures.Structure.__init__(self, **kwargs)

class RemoteUpdater(foundations.ui.common.QWidget_factory(ui_file=UI_FILE)):
	"""
	| Defines the Application remote updater.
	| The remote updater is initialized with a list of available online releases
		( List of :class:`ReleaseObject` class instances ).
	"""

	def __init__(self, parent, releases=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param releases: Releases.
		:type releases: dict
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(RemoteUpdater, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__releases = None
		self.releases = releases
		self.__ui_resources_directory = "resources/"
		self.__ui_resources_directory = os.path.join(os.path.dirname(__file__), self.__ui_resources_directory)
		self.__ui_logo_image = "sIBL_GUI_Small_Logo.png"
		self.__ui_templates_image = "Templates_Logo.png"
		self.__ui_light_gray_color = QColor(240, 240, 240)
		self.__ui_dark_gray_color = QColor(160, 160, 160)
		self.__splitter = "|"

		self.__view = None

		self.__headers = ["data",
						"Get it!",
						"Local version",
						"Repository version",
						"Release type",
						"Comment"]

		self.__application_changes_url = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Changes/Changes.html"
		self.__repository_url = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository"

		self.__download_manager = None
		self.__network_access_manager = self.__container.network_access_manager

		RemoteUpdater.__initialize_ui(self)

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
	def releases(self):
		"""
		Property for **self.__releases** attribute.

		:return: self.__releases.
		:rtype: dict
		"""

		return self.__releases

	@releases.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def releases(self, value):
		"""
		Setter for **self.__releases** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("releases", value)
			for key, element in value.iteritems():
				assert type(key) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"variables", key)
				assert type(element) is ReleaseObject, "'{0}' attribute: '{1}' type is not 'ReleaseObject'!".format(
				"variables", element)
		self.__releases = value

	@releases.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def releases(self):
		"""
		Deleter for **self.__releases** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "releases"))

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
	def ui_templates_image(self):
		"""
		Property for **self.__ui_templates_image** attribute.

		:return: self.__ui_templates_image.
		:rtype: unicode
		"""

		return self.__ui_templates_image

	@ui_templates_image.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_templates_image(self, value):
		"""
		Setter for **self.__ui_templates_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_templates_image"))

	@ui_templates_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_templates_image(self):
		"""
		Deleter for **self.__ui_templates_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_templates_image"))

	@property
	def ui_light_gray_color(self):
		"""
		Property for **self.__ui_light_gray_color** attribute.

		:return: self.__ui_light_gray_color.
		:rtype: QColor
		"""

		return self.__ui_light_gray_color

	@ui_light_gray_color.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_light_gray_color(self, value):
		"""
		Setter for **self.__ui_light_gray_color** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_light_gray_color"))

	@ui_light_gray_color.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_light_gray_color(self):
		"""
		Deleter for **self.__ui_light_gray_color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_light_gray_color"))

	@property
	def ui_dark_gray_color(self):
		"""
		Property for **self.__ui_dark_gray_color** attribute.

		:return: self.__ui_dark_gray_color.
		:rtype: QColor
		"""

		return self.__ui_dark_gray_color

	@ui_dark_gray_color.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_dark_gray_color(self, value):
		"""
		Setter for **self.__ui_dark_gray_color** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_dark_gray_color"))

	@ui_dark_gray_color.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_dark_gray_color(self):
		"""
		Deleter for **self.__ui_dark_gray_color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_dark_gray_color"))

	@property
	def view(self):
		"""
		Property for **self.__view** attribute.

		:return: self.__view.
		:rtype: QWidget
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		Setter for **self.__view** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		Deleter for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def splitter(self):
		"""
		Property for **self.__splitter** attribute.

		:return: self.__splitter.
		:rtype: unicode
		"""

		return self.__splitter

	@splitter.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def splitter(self, value):
		"""
		Setter for **self.__splitter** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "splitter"))

	@splitter.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def splitter(self):
		"""
		Deleter for **self.__splitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "splitter"))

	@property
	def headers(self):
		"""
		Property for **self.__headers** attribute.

		:return: self.__headers.
		:rtype: unicode
		"""

		return self.__headers

	@headers.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		Setter for **self.__headers** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

	@headers.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def headers(self):
		"""
		Deleter for **self.__headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

	@property
	def application_changes_url(self):
		"""
		Property for **self.__application_changes_url** attribute.

		:return: self.__application_changes_url.
		:rtype: unicode
		"""

		return self.__application_changes_url

	@application_changes_url.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def application_changes_url(self, value):
		"""
		Setter for **self.__application_changes_url** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "application_changes_url"))

	@application_changes_url.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def application_changes_url(self):
		"""
		Deleter for **self.__application_changes_url** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "application_changes_url"))

	@property
	def repository_url(self):
		"""
		Property for **self.__repository_url** attribute.

		:return: self.__repository_url.
		:rtype: unicode
		"""

		return self.__repository_url

	@repository_url.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def repository_url(self, value):
		"""
		Setter for **self.__repository_url** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "repository_url"))

	@repository_url.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def repository_url(self):
		"""
		Deleter for **self.__repository_url** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "repository_url"))

	@property
	def download_manager(self):
		"""
		Property for **self.__download_manager** attribute.

		:return: self.__download_manager.
		:rtype: object
		"""

		return self.__download_manager

	@download_manager.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def download_manager(self, value):
		"""
		Setter for **self.__download_manager** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "download_manager"))

	@download_manager.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def download_manager(self):
		"""
		Deleter for **self.__download_manager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "download_manager"))

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

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initialize_ui(self):
		"""
		Initializes the Widget ui.
		"""

		umbra.ui.common.set_window_default_icon(self)

		LOGGER.debug("> Initializing '{0}' ui.".format(self.__class__.__name__))

		if Constants.application_name not in self.__releases:
			self.sIBL_GUI_frame.hide()
			self.Get_sIBL_GUI_pushButton.hide()
		else:
			self.Logo_label.setPixmap(QPixmap(os.path.join(self.__ui_resources_directory, self.__ui_logo_image)))
			self.Your_Version_label.setText(self.__releases[Constants.application_name].local_version)
			self.Latest_Version_label.setText(self.__releases[Constants.application_name].repository_version)
			self.Change_Log_webView.load(QUrl.fromEncoded(QByteArray(self.__application_changes_url)))

		templates_releases = dict(self.__releases)
		if Constants.application_name in self.__releases:
			templates_releases.pop(Constants.application_name)

		if not templates_releases:
			self.Templates_frame.hide()
			self.Get_Latest_Templates_pushButton.hide()
		else:
			self.Templates_label.setPixmap(QPixmap(os.path.join(self.__ui_resources_directory, self.__ui_templates_image)))
			self.Templates_tableWidget.setParent(None)
			self.Templates_tableWidget = TemplatesReleases_QTableWidget(self, message="No Releases to view!")
			self.Templates_tableWidget.setObjectName("Templates_tableWidget")
			self.Templates_frame_gridLayout.addWidget(self.Templates_tableWidget, 1, 0)
			self.__view = self.Templates_tableWidget
			self.__view.clear()
			self.__view.setEditTriggers(QAbstractItemView.NoEditTriggers)
			self.__view.setRowCount(len(templates_releases))
			self.__view.setColumnCount(len(self.__headers))
			self.__view.setHorizontalHeaderLabels(self.__headers)
			self.__view.hideColumn(0)
			self.__view.horizontalHeader().setStretchLastSection(True)

			palette = QPalette()
			palette.setColor(QPalette.Base, Qt.transparent)
			self.__view.setPalette(palette)

			vertical_header_labels = []
			for row, release in enumerate(sorted(templates_releases)):
				vertical_header_labels.append(release)

				table_widget_item = QTableWidgetItem()
				table_widget_item.data = templates_releases[release]
				self.__view.setItem(row, 0, table_widget_item)

				table_widget_item = Variable_QPushButton(self,
														True,
														(self.__ui_light_gray_color, self.__ui_dark_gray_color),
														("Yes", "No"))
				table_widget_item.setObjectName("Spread_Sheet_pushButton")
				self.__view.setCellWidget(row, 1, table_widget_item)

				table_widget_item = QTableWidgetItem(templates_releases[release].local_version or Constants.null_object)
				table_widget_item.setTextAlignment(Qt.AlignCenter)
				self.__view.setItem(row, 2, table_widget_item)

				table_widget_item = QTableWidgetItem(templates_releases[release].repository_version)
				table_widget_item.setTextAlignment(Qt.AlignCenter)
				self.__view.setItem(row, 3, table_widget_item)

				table_widget_item = QTableWidgetItem(templates_releases[release].type)
				table_widget_item.setTextAlignment(Qt.AlignCenter)
				self.__view.setItem(row, 4, table_widget_item)

				table_widget_item = QTableWidgetItem(templates_releases[release].comment)
				self.__view.setItem(row, 5, table_widget_item)

			self.__view.setVerticalHeaderLabels(vertical_header_labels)
			self.__view.resizeColumnsToContents()

		# Signals / Slots.
		self.Get_sIBL_GUI_pushButton.clicked.connect(self.__Get_sIBL_GUI_pushButton__clicked)
		self.Get_Latest_Templates_pushButton.clicked.connect(self.__Get_Latest_Templates_pushButton__clicked)
		self.Open_Repository_pushButton.clicked.connect(self.__Open_Repository_pushButton__clicked)
		self.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

	def __Get_sIBL_GUI_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Get_sIBL_GUI_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""
		url_tokens = self.releases[Constants.application_name].url.split(self.__splitter)
		builds = dict(((url_tokens[i].strip(), url_tokens[i + 1].strip(" \"")) for i in range(0, len(url_tokens), 2)))

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			url = builds["Windows"]
		elif platform.system() == "Darwin":
			url = builds["Mac Os X"]
		elif platform.system() == "Linux":
			url = builds["Linux"]

		self.__download_manager = DownloadManager(self,
												self.__network_access_manager,
												self.__container.io_directory,
												[url],
												Qt.Window)
		self.__download_manager.download_finished.connect(self.__download_manager__finished)
		self.__download_manager.show()
		self.__download_manager.start_download()

	def __Get_Latest_Templates_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Get_Latest_Templates_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		requests = []
		for row in range(self.__view.rowCount()):
			if self.__view.cellWidget(row, 1).state:
				requests.append(self.__view.item(row, 0).data)

		if not requests:
			return

		download_directory = self.__get_templates_download_directory()
		if not download_directory:
			return

		if not foundations.io.is_writable(download_directory):
			self.__container.engine.notifications_manager.exceptify(
					"{0} | '{1}' directory is not writable".format(
					self.__class__.__name__, download_directory))
			return

		LOGGER.debug("> Templates download directory: '{0}'.".format(download_directory))
		self.__download_manager = DownloadManager(self,
												self.__network_access_manager,
												download_directory,
												[request.url for request in requests],
												Qt.Window)
		self.__download_manager.download_finished.connect(self.__download_manager__finished)
		self.__download_manager.show()
		self.__download_manager.start_download()

	def __Open_Repository_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Open_Repository_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(self.__repository_url))
		QDesktopServices.openUrl(QUrl(QString(self.__repository_url)))

	def __Close_pushButton__clicked(self, checked):
		"""
		Closes the RemoteUpdater.

		:param checked: Checked state.
		:type checked: bool
		"""

		LOGGER.info("{0} | Closing '{1}' updater!".format(self.__class__.__name__, Constants.application_name))
		self.close()

	def __download_manager__finished(self):
		"""
		Defines the slot triggered by the download Manager when finished.
		"""

		for download, data in self.__download_manager.downloads.iteritems():
			network_error, request = data
			if network_error != 0:
				self.__container.engine.notifications_manager.exceptify(
					"{0} | '{1}' file download failed! Error code: '{2}'".format(
					self.__class__.__name__, request, network_error))
				continue

			if download.endswith(".zip"):
				if self.extract_zip_file(download):
					LOGGER.info("{0} | Removing '{1}' archive!".format(self.__class__.__name__, download))
					try:
						os.remove(download)
					except OSError as error:
						LOGGER.warning("!> {0} | Cannot remove '{1}' file!".format(download))
				else:
					self.__container.engine.notifications_manager.exceptify(
					"{0} | Failed extracting '{1}', proceeding to next file!".format(self.__class__.__name__,
																					os.path.basename(download)))
				self.__container.templates_outliner.add_directory(os.path.dirname(download),
															self.__container.templates_outliner.get_collection_by_name(
															self.__container.templates_outliner.user_collection).id)
			else:
				if self.__container.locations_browser.activated:
					self.__container.locations_browser.explore_directory(os.path.dirname(download))

	def __get_templates_download_directory(self):
		"""
		Gets the Templates directory.
		"""

		LOGGER.debug("> Retrieving Templates download directory.")

		choice = message_box.message_box("Question", "{0}".format(self.__class__.__name__),
		"{0} | Which directory do you want to install the Templates into?".format(
		self.__class__.__name__),
		buttons=QMessageBox.Cancel,
		custom_buttons=((QString("Factory"), QMessageBox.AcceptRole),
					(QString("User"), QMessageBox.AcceptRole),
					(QString("Custom"), QMessageBox.AcceptRole)))
		if choice == 0:
			return os.path.join(RuntimeGlobals.templates_factory_directory)
		elif choice == 1:
			return os.path.join(RuntimeGlobals.templates_user_directory)
		elif choice == 2:
			return umbra.ui.common.store_last_browsed_path(QFileDialog.getExistingDirectory(self,
																						"Choose Templates Directory:",
																						 RuntimeGlobals.last_browsed_path))

	def extract_zip_file(self, file):
		"""
		Uncompress the given zip file.

		:param file: File to extract.
		:type file: unicode
		:return: Extraction success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' file uncompress.".format(file))

		pkzip = Pkzip()
		pkzip.archive = file

		return pkzip.extract(os.path.dirname(file))
