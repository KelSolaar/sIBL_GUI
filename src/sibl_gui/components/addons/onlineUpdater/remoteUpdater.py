#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**remoteUpdater.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`RemoteUpdater` class and others online update related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
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
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import foundations.ui.common
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from foundations.pkzip import Pkzip
from sibl_gui.components.addons.onlineUpdater.downloadManager import DownloadManager
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.ui.widgets.variable_QPushButton import Variable_QPushButton

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "ReleaseObject", "RemoteUpdater"]

LOGGER = logging.getLogger(Constants.logger)

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Remote_Updater.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ReleaseObject(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for a :class:`RemoteUpdater` class release.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: name, repositoryVersion, localVersion, type, url, comment. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class RemoteUpdater(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	| This class defines the Application remote updater.
	| The remote updater is initialized with a list of available online releases
		( List of :class:`ReleaseObject` class instances ).
	"""

	@core.executionTrace
	def __init__(self, parent, releases=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param releases: Releases. ( Dictionary )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(RemoteUpdater, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__releases = None
		self.releases = releases
		self.__uiResourcesDirectory = "resources/"
		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__),
													self.__uiResourcesDirectory)
		self.__uiLogoImage = "sIBL_GUI_Small_Logo.png"
		self.__uiTemplatesImage = "Templates_Logo.png"
		self.__uiLightGrayColor = QColor(240, 240, 240)
		self.__uiDarkGrayColor = QColor(160, 160, 160)
		self.__splitter = "|"
		self.__tableWidgetRowHeight = 30
		self.__tableWidgetHeaderHeight = 25

		self.__templatesTableWidgetHeaders = ["data",
											"Get it!",
											"Local version",
											"Repository version",
											"Release type",
											"Comment"]

		self.__applicationChangeLogUrl = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Change_Log/Change_Log.html"
		self.__repositoryUrl = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository"

		self.__downloadManager = None
		self.__networkAccessManager = self.__container.networkAccessManager

		RemoteUpdater.__initializeUi(self)

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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def releases(self):
		"""
		This method is the property for **self.__releases** attribute.

		:return: self.__releases. ( Dictionary )
		"""

		return self.__releases

	@releases.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def releases(self, value):
		"""
		This method is the setter method for **self.__releases** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("releases", value)
			for key, element in value.items():
				assert type(key) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"variables", key)
				assert type(element) is ReleaseObject, "'{0}' attribute: '{1}' type is not 'ReleaseObject'!".format(
				"variables", element)
		self.__releases = value

	@releases.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releases(self):
		"""
		This method is the deleter method for **self.__releases** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "releases"))

	@property
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This method is the setter method for **self.__uiLogoImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This method is the deleter method for **self.__uiLogoImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiLogoImage"))

	@property
	def uiTemplatesImage(self):
		"""
		This method is the property for **self.__uiTemplatesImage** attribute.

		:return: self.__uiTemplatesImage. ( String )
		"""

		return self.__uiTemplatesImage

	@uiTemplatesImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiTemplatesImage(self, value):
		"""
		This method is the setter method for **self.__uiTemplatesImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiTemplatesImage"))

	@uiTemplatesImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiTemplatesImage(self):
		"""
		This method is the deleter method for **self.__uiTemplatesImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiTemplatesImage"))

	@property
	def uiLightGrayColor(self):
		"""
		This method is the property for **self.__uiLightGrayColor** attribute.

		:return: self.__uiLightGrayColor. ( QColor )
		"""

		return self.__uiLightGrayColor

	@uiLightGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self, value):
		"""
		This method is the setter method for **self.__uiLightGrayColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLightGrayColor"))

	@uiLightGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self):
		"""
		This method is the deleter method for **self.__uiLightGrayColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiLightGrayColor"))

	@property
	def uiDarkGrayColor(self):
		"""
		This method is the property for **self.__uiDarkGrayColor** attribute.

		:return: self.__uiDarkGrayColor. ( QColor )
		"""

		return self.__uiDarkGrayColor

	@uiDarkGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self, value):
		"""
		This method is the setter method for **self.__uiDarkGrayColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiDarkGrayColor"))

	@uiDarkGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self):
		"""
		This method is the deleter method for **self.__uiDarkGrayColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiDarkGrayColor"))

	@property
	def splitter(self):
		"""
		This method is the property for **self.__splitter** attribute.

		:return: self.__splitter. ( String )
		"""

		return self.__splitter

	@splitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def splitter(self, value):
		"""
		This method is the setter method for **self.__splitter** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "splitter"))

	@splitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def splitter(self):
		"""
		This method is the deleter method for **self.__splitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "splitter"))

	@property
	def tableWidgetRowHeight(self):
		"""
		This method is the property for **self.__tableWidgetRowHeight** attribute.

		:return: self.__tableWidgetRowHeight. ( Integer )
		"""

		return self.__tableWidgetRowHeight

	@tableWidgetRowHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self, value):
		"""
		This method is the setter method for **self.__tableWidgetRowHeight** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tableWidgetRowHeight"))

	@tableWidgetRowHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self):
		"""
		This method is the deleter method for **self.__tableWidgetRowHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tableWidgetRowHeight"))

	@property
	def tableWidgetHeaderHeight(self):
		"""
		This method is the property for **self.__tableWidgetHeaderHeight** attribute.

		:return: self.__tableWidgetHeaderHeight. ( Integer )
		"""

		return self.__tableWidgetHeaderHeight

	@tableWidgetHeaderHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self, value):
		"""
		This method is the setter method for **self.__tableWidgetHeaderHeight** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tableWidgetHeaderHeight"))

	@tableWidgetHeaderHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self):
		"""
		This method is the deleter method for **self.__tableWidgetHeaderHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tableWidgetHeaderHeight"))

	@property
	def templatesTableWidgetHeaders(self):
		"""
		This method is the property for **self.__templatesTableWidgetHeaders** attribute.

		:return: self.__templatesTableWidgetHeaders. ( String )
		"""

		return self.__templatesTableWidgetHeaders

	@templatesTableWidgetHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesTableWidgetHeaders(self, value):
		"""
		This method is the setter method for **self.__templatesTableWidgetHeaders** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesTableWidgetHeaders"))

	@templatesTableWidgetHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesTableWidgetHeaders(self):
		"""
		This method is the deleter method for **self.__templatesTableWidgetHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesTableWidgetHeaders"))

	@property
	def applicationChangeLogUrl(self):
		"""
		This method is the property for **self.__applicationChangeLogUrl** attribute.

		:return: self.__applicationChangeLogUrl. ( String )
		"""

		return self.__applicationChangeLogUrl

	@applicationChangeLogUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def applicationChangeLogUrl(self, value):
		"""
		This method is the setter method for **self.__applicationChangeLogUrl** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "applicationChangeLogUrl"))

	@applicationChangeLogUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def applicationChangeLogUrl(self):
		"""
		This method is the deleter method for **self.__applicationChangeLogUrl** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "applicationChangeLogUrl"))

	@property
	def repositoryUrl(self):
		"""
		This method is the property for **self.__repositoryUrl** attribute.

		:return: self.__repositoryUrl. ( String )
		"""

		return self.__repositoryUrl

	@repositoryUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self, value):
		"""
		This method is the setter method for **self.__repositoryUrl** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "repositoryUrl"))

	@repositoryUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self):
		"""
		This method is the deleter method for **self.__repositoryUrl** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "repositoryUrl"))

	@property
	def downloadManager(self):
		"""
		This method is the property for **self.__downloadManager** attribute.

		:return: self.__downloadManager. ( Object )
		"""

		return self.__downloadManager

	@downloadManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadManager(self, value):
		"""
		This method is the setter method for **self.__downloadManager** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "downloadManager"))

	@downloadManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def downloadManager(self):
		"""
		This method is the deleter method for **self.__downloadManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "downloadManager"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This method is the deleter method for **self.__networkAccessManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "networkAccessManager"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		LOGGER.debug("> Initializing '{0}' ui.".format(self.__class__.__name__))

		if Constants.applicationName not in self.__releases:
			self.sIBL_GUI_groupBox.hide()
			self.Get_sIBL_GUI_pushButton.hide()
		else:
			self.Logo_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiLogoImage)))
			self.Your_Version_label.setText(self.__releases[Constants.applicationName].localVersion)
			self.Latest_Version_label.setText(self.__releases[Constants.applicationName].repositoryVersion)
			self.Change_Log_webView.load(QUrl.fromEncoded(QByteArray(self.__applicationChangeLogUrl)))

		templatesReleases = dict(self.__releases)
		if Constants.applicationName in self.__releases:
			templatesReleases.pop(Constants.applicationName)

		if not templatesReleases:
			self.Templates_groupBox.hide()
			self.Get_Latest_Templates_pushButton.hide()
		else:
			self.Templates_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiTemplatesImage)))
			self.Templates_tableWidget.clear()
			self.Templates_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
			self.Templates_tableWidget.setRowCount(len(templatesReleases))
			self.Templates_tableWidget.setColumnCount(len(self.__templatesTableWidgetHeaders))
			self.Templates_tableWidget.setHorizontalHeaderLabels(self.__templatesTableWidgetHeaders)
			self.Templates_tableWidget.hideColumn(0)
			self.Templates_tableWidget.horizontalHeader().setStretchLastSection(True)
			self.Templates_tableWidget.setMinimumHeight(
			len(templatesReleases) * self.__tableWidgetRowHeight + self.__tableWidgetHeaderHeight)
			self.Templates_tableWidget.setMaximumHeight(
			len(templatesReleases) * self.__tableWidgetRowHeight + self.__tableWidgetHeaderHeight)

			palette = QPalette()
			palette.setColor(QPalette.Base, Qt.transparent)
			self.Templates_tableWidget.setPalette(palette)

			verticalHeaderLabels = []
			for row, release in enumerate(sorted(templatesReleases)):
					verticalHeaderLabels.append(release)

					tableWidgetItem = QTableWidgetItem()
					tableWidgetItem.data = templatesReleases[release]
					self.Templates_tableWidget.setItem(row, 0, tableWidgetItem)

					tableWidgetItem = Variable_QPushButton(self,
															True,
															(self.__uiLightGrayColor, self.__uiDarkGrayColor),
															("Yes", "No"))
					self.Templates_tableWidget.setCellWidget(row, 1, tableWidgetItem)

					tableWidgetItem = QTableWidgetItem(templatesReleases[release].localVersion or Constants.nullObject)
					tableWidgetItem.setTextAlignment(Qt.AlignCenter)
					self.Templates_tableWidget.setItem(row, 2, tableWidgetItem)

					tableWidgetItem = QTableWidgetItem(templatesReleases[release].repositoryVersion)
					tableWidgetItem.setTextAlignment(Qt.AlignCenter)
					self.Templates_tableWidget.setItem(row, 3, tableWidgetItem)

					tableWidgetItem = QTableWidgetItem(templatesReleases[release].type)
					tableWidgetItem.setTextAlignment(Qt.AlignCenter)
					self.Templates_tableWidget.setItem(row, 4, tableWidgetItem)

					tableWidgetItem = QTableWidgetItem(templatesReleases[release].comment)
					self.Templates_tableWidget.setItem(row, 5, tableWidgetItem)

			self.Templates_tableWidget.setVerticalHeaderLabels(verticalHeaderLabels)
			self.Templates_tableWidget.resizeColumnsToContents()

		# Signals / Slots.
		self.Get_sIBL_GUI_pushButton.clicked.connect(self.__Get_sIBL_GUI_pushButton__clicked)
		self.Get_Latest_Templates_pushButton.clicked.connect(self.__Get_Latest_Templates_pushButton__clicked)
		self.Open_Repository_pushButton.clicked.connect(self.__Open_Repository_pushButton__clicked)
		self.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

	@core.executionTrace
	def __Get_sIBL_GUI_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Get_sIBL_GUI_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""
		urlTokens = self.releases[Constants.applicationName].url.split(self.__splitter)
		builds = dict(((urlTokens[i].strip(), urlTokens[i + 1].strip(" \"")) for i in range(0, len(urlTokens), 2)))

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			url = builds["Windows"]
		elif platform.system() == "Darwin":
			url = builds["Mac Os X"]
		elif platform.system() == "Linux":
			url = builds["Linux"]

		self.__downloadManager = DownloadManager(self,
												self.__networkAccessManager,
												self.__container.ioDirectory,
												[url],
												Qt.Window)
		self.__downloadManager.downloadFinished.connect(self.__downloadManager__finished)
		self.__downloadManager.show()
		self.__downloadManager.startDownload()

	@core.executionTrace
	def __Get_Latest_Templates_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Get_Latest_Templates_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		requests = []
		for row in range(self.Templates_tableWidget.rowCount()):
			if self.Templates_tableWidget.cellWidget(row, 1).state:
				requests.append(self.Templates_tableWidget.item(row, 0).data)

		if not requests:
			return

		downloadDirectory = self.__getTemplatesDownloadDirectory()
		if not downloadDirectory:
			return

		LOGGER.debug("> Templates download directory: '{0}'.".format(downloadDirectory))
		self.__downloadManager = DownloadManager(self,
												self.__networkAccessManager,
												downloadDirectory,
												[request.url for request in requests],
												Qt.Window)
		self.__downloadManager.downloadFinished.connect(self.__downloadManager__finished)
		self.__downloadManager.show()
		self.__downloadManager.startDownload()

	@core.executionTrace
	def __Open_Repository_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Open_Repository_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(self.__repositoryUrl))
		QDesktopServices.openUrl(QUrl(QString(self.__repositoryUrl)))

	@core.executionTrace
	def __Close_pushButton__clicked(self, checked):
		"""
		This method closes the RemoteUpdater.

		:param checked: Checked state. ( Boolean )
		"""

		LOGGER.info("{0} | Closing '{1}' updater!".format(self.__class__.__name__, Constants.applicationName))
		self.close()

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
					messageBox.messageBox("Warning", "Warning",
					"{0} | Failed extracting '{1}', proceeding to next file!".format(self.__class__.__name__,
																					os.path.basename(download)))
				self.__container.coreTemplatesOutliner.addDirectory(os.path.dirname(download),
															self.__container.coreTemplatesOutliner.getCollectionByName(
															self.__container.coreTemplatesOutliner.userCollection).id)
			else:
				if self.__container.addonsLocationsBrowser.activated:
					self.__container.addonsLocationsBrowser.exploreDirectory(os.path.dirname(download))

	@core.executionTrace
	def __getTemplatesDownloadDirectory(self):
		"""
		This method gets the Templates directory.
		"""

		LOGGER.debug("> Retrieving Templates download directory.")

		choice = messageBox.messageBox("Question", "{0}".format(self.__class__.__name__),
		"{0} | Which directory do you want to install the Templates into?".format(
		self.__class__.__name__),
		buttons=QMessageBox.Cancel,
		customButtons=((QString("Factory"), QMessageBox.AcceptRole),
					(QString("User"), QMessageBox.AcceptRole),
					(QString("Custom"), QMessageBox.AcceptRole)))
		if choice == 0:
			return os.path.join(RuntimeGlobals.templatesFactoryDirectory)
		elif choice == 1:
			return os.path.join(RuntimeGlobals.templatesUserDirectory)
		elif choice == 2:
			return self.__container.container.storeLastBrowsedPath(
			QFileDialog.getExistingDirectory(self,
											"Choose Templates directory:",
											self.__container.container.lastBrowsedPath))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def extractZipFile(self, file):
		"""
		This method uncompress the given zip file.

		:param file: File to extract. ( String )
		:return: Extraction success. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}' file uncompress.".format(file))

		pkzip = Pkzip()
		pkzip.archive = file

		return pkzip.extract(os.path.dirname(file))
