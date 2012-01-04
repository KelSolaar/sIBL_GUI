#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**databaseBrowser.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`DatabaseBrowser` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import logging
import os
import platform
import re
from collections import OrderedDict
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QStringListModel

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.strings as strings
import sibl_gui.components.core.db.exceptions as dbExceptions
import sibl_gui.components.core.db.utilities.common as dbCommon
import sibl_gui.components.core.db.utilities.nodes as dbNodes
import umbra.engine
import umbra.ui.common
import umbra.ui.models
import umbra.ui.widgets.messageBox as messageBox
from foundations.walkers import OsWalker
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.core.databaseBrowser.models import IblSetsModel
from sibl_gui.components.core.databaseBrowser.views import Columns_QListView
from sibl_gui.components.core.databaseBrowser.views import Details_QTreeView
from sibl_gui.components.core.databaseBrowser.views import Thumbnails_QListView
from sibl_gui.components.core.databaseBrowser.workers import DatabaseBrowser_worker
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "DatabaseBrowser"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Database_Browser.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class DatabaseBrowser(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.core.databaseBrowser.databaseBrowser` Component Interface class.
	| It defines methods for Database Ibl Sets management.
	"""

	# Custom signals definitions.
	modelRefresh = pyqtSignal()
	"""
	This signal is emited by the :class:`DatabaseBrowser` class when :obj:`DatabaseBrowser.model` class property model
	needs to be refreshed. ( pyqtSignal )
	"""

	activeViewChanged = pyqtSignal(int)
	"""
	This signal is emited by the :class:`DatabaseBrowser` class when the current active view is changed. ( pyqtSignal )
	
	:return: Current active view index. ( Integer )	
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(DatabaseBrowser, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiResourcesDirectory = "resources"
		self.__uiThumbnailsViewImage = "Thumbnails_View.png"
		self.__uiColumnsViewImage = "Columns_View.png"
		self.__uiDetailsViewImage = "Details_View.png"
		self.__uiSearchImage = "images/Search_Glass.png"
		self.__uiSearchClickedImage = "images/Search_Glass_Clicked.png"
		self.__uiClearImage = "images/Search_Clear.png"
		self.__uiClearClickedImage = "images/Search_Clear_Clicked.png"
		self.__uiLargestSizeImage = "Largest_Size.png"
		self.__uiSmallestSizeImage = "Smallest_Size.png"
		self.__dockArea = 8

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None
		self.__settingsSeparator = ","

		self.__extension = "ibl"

		self.__editLayout = "editCentric"
		self.__inspectLayout = "inspectCentric"

		self.__factoryScriptEditor = None
		self.__coreDb = None
		self.__coreCollectionsOutliner = None

		self.__model = None
		self.__views = None
		self.__viewsPushButtons = None
		self.__thumbnailsView = None
		self.__columnsView = None
		self.__detailsView = None
		self.__detailsHeaders = OrderedDict([("Ibl Set", "title"),
										("Author", "author"),
										("Shot Location", "location"),
										("Latitude", "latitude"),
										("Longitude", "longitude"),
										("Shot Date", "date"),
										("Shot Time", "time"),
										("Comment", "comment")])

		self.__searchContexts = OrderedDict([("Search In Names", "title"),
								("Search In Authors", "author"),
								("Search In Links", "link"),
								("Search In Locations", "location"),
								("Search In Comments", "comment")])
		self.__activeSearchContext = "Search In Names"

		self.__databaseBrowserWorkerThread = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
	def uiThumbnailsViewImage(self):
		"""
		This method is the property for **self.__uiThumbnailsViewImage** attribute.

		:return: self.__uiThumbnailsViewImage. ( String )
		"""

		return self.__uiThumbnailsViewImage

	@uiThumbnailsViewImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiThumbnailsViewImage(self, value):
		"""
		This method is the setter method for **self.__uiThumbnailsViewImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiThumbnailsViewImage"))

	@uiThumbnailsViewImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiThumbnailsViewImage(self):
		"""
		This method is the deleter method for **self.__uiThumbnailsViewImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiThumbnailsViewImage"))

	@property
	def uiColumnsViewImage(self):
		"""
		This method is the property for **self.__uiColumnsViewImage** attribute.

		:return: self.__uiColumnsViewImage. ( String )
		"""

		return self.__uiColumnsViewImage

	@uiColumnsViewImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiColumnsViewImage(self, value):
		"""
		This method is the setter method for **self.__uiColumnsViewImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiColumnsViewImage"))

	@uiColumnsViewImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiColumnsViewImage(self):
		"""
		This method is the deleter method for **self.__uiColumnsViewImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiColumnsViewImage"))

	@property
	def uiDetailsViewImage(self):
		"""
		This method is the property for **self.__uiDetailsViewImage** attribute.

		:return: self.__uiDetailsViewImage. ( String )
		"""

		return self.__uiDetailsViewImage

	@uiDetailsViewImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDetailsViewImage(self, value):
		"""
		This method is the setter method for **self.__uiDetailsViewImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiDetailsViewImage"))

	@uiDetailsViewImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDetailsViewImage(self):
		"""
		This method is the deleter method for **self.__uiDetailsViewImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiDetailsViewImage"))

	@property
	def uiSearchImage(self):
		"""
		This method is the property for **self.__uiSearchImage** attribute.

		:return: self.__uiSearchImage. ( String )
		"""

		return self.__uiSearchImage

	@uiSearchImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self, value):
		"""
		This method is the setter method for **self.__uiSearchImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiSearchImage"))

	@uiSearchImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self):
		"""
		This method is the deleter method for **self.__uiSearchImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSearchImage"))

	@property
	def uiSearchClickedImage(self):
		"""
		This method is the property for **self.__uiSearchClickedImage** attribute.

		:return: self.__uiSearchClickedImage. ( String )
		"""

		return self.__uiSearchClickedImage

	@uiSearchClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchClickedImage(self, value):
		"""
		This method is the setter method for **self.__uiSearchClickedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiSearchClickedImage"))

	@uiSearchClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchClickedImage(self):
		"""
		This method is the deleter method for **self.__uiSearchClickedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSearchClickedImage"))

	@property
	def uiClearImage(self):
		"""
		This method is the property for **self.__uiClearImage** attribute.

		:return: self.__uiClearImage. ( String )
		"""

		return self.__uiClearImage

	@uiClearImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self, value):
		"""
		This method is the setter method for **self.__uiClearImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiClearImage"))

	@uiClearImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self):
		"""
		This method is the deleter method for **self.__uiClearImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiClearImage"))

	@property
	def uiClearClickedImage(self):
		"""
		This method is the property for **self.__uiClearClickedImage** attribute.

		:return: self.__uiClearClickedImage. ( String )
		"""

		return self.__uiClearClickedImage

	@uiClearClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self, value):
		"""
		This method is the setter method for **self.__uiClearClickedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiClearClickedImage"))

	@uiClearClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self):
		"""
		This method is the deleter method for **self.__uiClearClickedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiClearClickedImage"))

	@property
	def uiLargestSizeImage(self):
		"""
		This method is the property for **self.__uiLargestSizeImage** attribute.

		:return: self.__uiLargestSizeImage. ( String )
		"""

		return self.__uiLargestSizeImage

	@uiLargestSizeImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLargestSizeImage(self, value):
		"""
		This method is the setter method for **self.__uiLargestSizeImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLargestSizeImage"))

	@uiLargestSizeImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLargestSizeImage(self):
		"""
		This method is the deleter method for **self.__uiLargestSizeImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiLargestSizeImage"))

	@property
	def uiSmallestSizeImage(self):
		"""
		This method is the property for **self.__uiSmallestSizeImage** attribute.

		:return: self.__uiSmallestSizeImage. ( String )
		"""

		return self.__uiSmallestSizeImage

	@uiSmallestSizeImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSmallestSizeImage(self, value):
		"""
		This method is the setter method for **self.__uiSmallestSizeImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiSmallestSizeImage"))

	@uiSmallestSizeImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSmallestSizeImage(self):
		"""
		This method is the deleter method for **self.__uiSmallestSizeImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSmallestSizeImage"))

	@property
	def dockArea(self):
		"""
		This method is the property for **self.__dockArea** attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def engine(self):
		"""
		This method is the property for **self.__engine** attribute.

		:return: self.__engine. ( QObject )
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settingsSection(self):
		"""
		This method is the property for **self.__settingsSection** attribute.

		:return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for **self.__settingsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def settingsSeparator(self):
		"""
		This method is the property for **self.__settingsSeparator** attribute.

		:return: self.__settingsSeparator. ( String )
		"""

		return self.__settingsSeparator

	@settingsSeparator.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self, value):
		"""
		This method is the setter method for **self.__settingsSeparator** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self):
		"""
		This method is the deleter method for **self.__settingsSeparator** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSeparator"))

	@property
	def extension(self):
		"""
		This method is the property for **self.__extension** attribute.

		:return: self.__extension. ( String )
		"""

		return self.__extension

	@extension.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self, value):
		"""
		This method is the setter method for **self.__extension** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "extension"))

	@extension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		This method is the deleter method for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

	@property
	def editLayout(self):
		"""
		This method is the property for **self.__editLayout** attribute.

		:return: self.__editLayout. ( String )
		"""

		return self.__editLayout

	@editLayout.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editLayout(self, value):
		"""
		This method is the setter method for **self.__editLayout** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "editLayout"))

	@editLayout.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editLayout(self):
		"""
		This method is the deleter method for **self.__editLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editLayout"))

	@property
	def inspectLayout(self):
		"""
		This method is the property for **self.__editLayout** attribute.

		:return: self.__editLayout. ( String )
		"""

		return self.__editLayout

	@inspectLayout.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectLayout(self, value):
		"""
		This method is the setter method for **self.__editLayout** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectLayout"))

	@inspectLayout.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectLayout(self):
		"""
		This method is the deleter method for **self.__editLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectLayout"))

	@property
	def factoryScriptEditor(self):
		"""
		This method is the property for **self.__factoryScriptEditor** attribute.

		:return: self.__factoryScriptEditor. ( Object )
		"""

		return self.__factoryScriptEditor

	@factoryScriptEditor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self, value):
		"""
		This method is the setter method for **self.__factoryScriptEditor** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryScriptEditor"))

	@factoryScriptEditor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self):
		"""
		This method is the deleter method for **self.__factoryScriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryScriptEditor"))

	@property
	def coreDb(self):
		"""
		This method is the property for **self.__coreDb** attribute.

		:return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This method is the setter method for **self.__coreDb** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for **self.__coreDb** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDb"))

	@property
	def coreCollectionsOutliner(self):
		"""
		This method is the property for **self.__coreCollectionsOutliner** attribute.

		:return: self.__coreCollectionsOutliner. ( Object )
		"""

		return self.__coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		"""
		This method is the setter method for **self.__coreCollectionsOutliner** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This method is the deleter method for **self.__coreCollectionsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreCollectionsOutliner"))

	@property
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def views(self):
		"""
		This method is the property for **self.__views** attribute.

		:return: self.__views. ( Tuple )
		"""

		return self.__views

	@views.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def views(self, value):
		"""
		This method is the setter method for **self.__views** attribute.

		:param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "views"))

	@views.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def views(self):
		"""
		This method is the deleter method for **self.__views** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "views"))

	@property
	def viewsPushButtons(self):
		"""
		This method is the property for **self.__viewsPushButtons** attribute.

		:return: self.__viewsPushButtons. ( Dictionary )
		"""

		return self.__viewsPushButtons

	@viewsPushButtons.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewsPushButtons(self, value):
		"""
		This method is the setter method for **self.__viewsPushButtons** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "viewsPushButtons"))

	@viewsPushButtons.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewsPushButtons(self):
		"""
		This method is the deleter method for **self.__viewsPushButtons** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "viewsPushButtons"))

	@property
	def thumbnailsView(self):
		"""
		This method is the property for **self.__thumbnailsView** attribute.

		:return: self.__thumbnailsView. ( QListView )
		"""

		return self.__thumbnailsView

	@thumbnailsView.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def thumbnailsView(self, value):
		"""
		This method is the setter method for **self.__thumbnailsView** attribute.

		:param value: Attribute value. ( QListView )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "thumbnailsView"))

	@thumbnailsView.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def thumbnailsView(self):
		"""
		This method is the deleter method for **self.__thumbnailsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def columnsView(self):
		"""
		This method is the property for **self.__columnsView** attribute.

		:return: self.__columnsView. ( QListView )
		"""

		return self.__columnsView

	@columnsView.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def columnsView(self, value):
		"""
		This method is the setter method for **self.__columnsView** attribute.

		:param value: Attribute value. ( QListView )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "columnsView"))

	@columnsView.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def columnsView(self):
		"""
		This method is the deleter method for **self.__columnsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def detailsView(self):
		"""
		This method is the property for **self.__detailsView** attribute.

		:return: self.__detailsView. ( QTreeView )
		"""

		return self.__detailsView

	@detailsView.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def detailsView(self, value):
		"""
		This method is the setter method for **self.__detailsView** attribute.

		:param value: Attribute value. ( QTreeView )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "detailsView"))

	@detailsView.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def detailsView(self):
		"""
		This method is the deleter method for **self.__detailsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def detailsViewHeaders(self):
		"""
		This method is the property for **self.__detailsViewHeaders** attribute.

		:return: self.__detailsViewHeaders. ( OrderedDict )
		"""

		return self.__detailsViewHeaders

	@detailsViewHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def detailsViewHeaders(self, value):
		"""
		This method is the setter method for **self.__detailsViewHeaders** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "detailsViewHeaders"))

	@detailsViewHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def detailsViewHeaders(self):
		"""
		This method is the deleter method for **self.__detailsViewHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def searchContexts(self):
		"""
		This method is the property for **self.__searchContexts** attribute.

		:return: self.__searchContexts. ( OrderedDict )
		"""

		return self.__searchContexts

	@searchContexts.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchContexts(self, value):
		"""
		This method is the setter method for **self.__searchContexts** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchContexts"))

	@searchContexts.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchContexts(self):
		"""
		This method is the deleter method for **self.__searchContexts** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchContexts"))

	@property
	def activeSearchContext(self):
		"""
		This method is the property for **self.__activeSearchContext** attribute.

		:return: self.__activeSearchContext. ( OrderedDict )
		"""

		return self.__activeSearchContext

	@activeSearchContext.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def activeSearchContext(self, value):
		"""
		This method is the setter method for **self.__activeSearchContext** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "activeSearchContext"))

	@activeSearchContext.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def activeSearchContext(self):
		"""
		This method is the deleter method for **self.__activeSearchContext** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activeSearchContext"))

	@property
	def databaseBrowserWorkerThread(self):
		"""
		This method is the property for **self.__databaseBrowserWorkerThread** attribute.

		:return: self.__databaseBrowserWorkerThread. ( QThread )
		"""

		return self.__databaseBrowserWorkerThread

	@databaseBrowserWorkerThread.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseBrowserWorkerThread(self, value):
		"""
		This method is the setter method for **self.__databaseBrowserWorkerThread** attribute.

		:param value: Attribute value. ( QThread )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseBrowserWorkerThread"))

	@databaseBrowserWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseBrowserWorkerThread(self):
		"""
		This method is the deleter method for **self.__databaseBrowserWorkerThread** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseBrowserWorkerThread"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__),
													self.__uiResourcesDirectory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__factoryScriptEditor = self.__engine.componentsManager.components["factory.scriptEditor"].interface
		self.__coreDb = self.__engine.componentsManager.components["core.db"].interface
		self.__coreCollectionsOutliner = self.__engine.componentsManager.components["core.collectionsOutliner"].interface

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__engine.parameters.databaseReadOnly and \
		LOGGER.info("{0} | Model edition deactivated by '{1}' command line parameter value!".format(self.__class__.__name__,
																									"databaseReadOnly"))
		self.__model = IblSetsModel(self, horizontalHeaders=self.__detailsHeaders)

		self.Database_Browser_stackedWidget = QStackedWidget(self)
		self.Database_Browser_gridLayout.addWidget(self.Database_Browser_stackedWidget)

		self.__thumbnailsView = Thumbnails_QListView(self, self.__model, self.__engine.parameters.databaseReadOnly)
		self.__thumbnailsView.setObjectName("Thumbnails_listView")
		self.__thumbnailsView.setContextMenuPolicy(Qt.ActionsContextMenu)
		listViewIconSize, state = self.__settings.getKey(self.__settingsSection, "listViewIconSize").toInt()
		if state:
			self.__thumbnailsView.listViewIconSize = listViewIconSize
		self.Database_Browser_stackedWidget.addWidget(self.__thumbnailsView)

		self.__columnsView = Columns_QListView(self, self.__model, self.__engine.parameters.databaseReadOnly)
		self.__columnsView.setObjectName("Columns_listView")
		self.__columnsView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.Database_Browser_stackedWidget.addWidget(self.__columnsView)

		self.__detailsView = Details_QTreeView(self, self.__model, self.__engine.parameters.databaseReadOnly)
		self.__detailsView.setObjectName("Details_treeView")
		self.__detailsView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.Database_Browser_stackedWidget.addWidget(self.__detailsView)

		self.__views = (self.__thumbnailsView, self.__columnsView, self.__detailsView)
		self.__views_addActions()
		self.__viewsPushButtons = {0 : (self.Thumbnails_View_pushButton, self.__uiThumbnailsViewImage),
									1 : (self.Columns_View_pushButton, self.__uiColumnsViewImage),
									2 : (self.Details_View_pushButton, self.__uiDetailsViewImage)}

		for index, data in self.__viewsPushButtons.iteritems():
			viewPushButton, image = data
			viewPushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, image)))

		self.Search_Database_lineEdit = Search_QLineEdit(self, umbra.ui.common.getResourcePath(self.__uiSearchImage),
														umbra.ui.common.getResourcePath(self.__uiSearchClickedImage),
														umbra.ui.common.getResourcePath(self.__uiClearImage),
														umbra.ui.common.getResourcePath(self.__uiClearClickedImage))
		self.Search_Database_horizontalLayout.addWidget(self.Search_Database_lineEdit)
		self.Search_Database_lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		searchContextsMenu = QMenu()
		for context in self.__searchContexts:
			searchContextsMenu.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.databaseBrowser|Search|Set '{0}' Context ...".format(context),
			text="{0} ...".format(context),
			checkable=True,
			slot=functools.partial(self.setActiveSearchContext, context)))
		self.Search_Database_lineEdit.searchActiveLabel.setMenu(searchContextsMenu)
		self.setActiveSearchContext(self.__activeSearchContext)

		self.Thumbnails_Size_horizontalSlider.setValue(self.__thumbnailsView.listViewIconSize)
		self.Largest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiLargestSizeImage)))
		self.Smallest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiSmallestSizeImage)))

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				self.__databaseBrowserWorkerThread = DatabaseBrowser_worker(self)
				self.__databaseBrowserWorkerThread.start()
				self.__engine.workerThreads.append(self.__databaseBrowserWorkerThread)
			else:
				LOGGER.info("{0} | Ibl Sets continuous scanner deactivated by '{1}' command line parameter value!".format(
				self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Ibl Sets continuous scanner deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		# Signals / Slots.
		for view in self.__views:
			self.__engine.imagesCaches.QIcon.contentAdded.connect(view.viewport().update)
			view.doubleClicked.connect(self.__views__doubleClicked)
		self.activeViewChanged.connect(self.__views__activeViewChanged)
		for index, data in self.__viewsPushButtons.iteritems():
			viewPushButton, image = data
			viewPushButton.clicked.connect(functools.partial(self.__views_pushButtons__clicked, index))

		self.Search_Database_lineEdit.textChanged.connect(self.__Search_Database_lineEdit__textChanged)

		self.Thumbnails_Size_horizontalSlider.valueChanged.connect(self.__Thumbnails_Size_horizontalSlider__changed)

		self.modelRefresh.connect(self.__databaseBrowser__modelRefresh)
		self.__model.modelReset.connect(self.__coreCollectionsOutliner._CollectionsOutliner__view_setIblSetsCounts)

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				self.__databaseBrowserWorkerThread.databaseChanged.connect(self.__coreDb_database__databaseChanged)
			self.__model.dataChanged.connect(self.__model__dataChanged)
			self.__engine.contentDropped.connect(self.__engine__contentDropped)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.centralwidget_gridLayout.addWidget(self)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def onStartup(self):
		"""
		This method is triggered on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			# Wizard if sets table is empty.
			if not self.getIblSets():
				if messageBox.messageBox("Question", "Question",
				"The Database is empty, would you like to add some Ibl Sets?",
				buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
					directory = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self,
																						 "Add content:",
																						RuntimeGlobals.lastBrowsedPath)))
					if directory:
						if not self.addDirectory(directory):
							raise Exception(
							"{0} | Exception raised while adding '{1}' directory content to the Database!".format(
							self.__class__.__name__, directory))

			# Ibl Sets table integrity checking.
			erroneousIblSets = dbCommon.checkIblSetsTableIntegrity(self.__coreDb.dbSession)
			if erroneousIblSets:
				for iblSet in erroneousIblSets:
					if erroneousIblSets[iblSet] == "INEXISTING_IBL_SET_FILE_EXCEPTION":
						if messageBox.messageBox("Question", "Error",
						"{0} | '{1}' Ibl Set file is missing, would you like to update it's location?".format(
						self.__class__.__name__, iblSet.title),
						QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
							file = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																"Updating '{0}' Ibl Set location:".format(iblSet.title),
																RuntimeGlobals.lastBrowsedPath,
																"Ibls files (*.{0})".format(self.__extension))))
							file and self.updateIblSetLocation(iblSet, file)
					else:
						messageBox.messageBox("Warning", "Warning",
						"{0} | '{1}' {2}".format(self.__class__.__name__,
						iblSet.title, dbCommon.DB_EXCEPTIONS[erroneousIblSets[iblSet]]))
		else:
			LOGGER.info(
			"{0} | Database Ibl Sets wizard and Ibl Sets integrity checking method deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		activeView, state = self.__settings.getKey(self.__settingsSection, "activeView").toInt()
		state and self.setActiveViewIndex(activeView)

		for view in self.__views:
			viewName = view.objectName()
			viewSelectedIblSetsIdentities = str(self.__settings.getKey(self.__settingsSection,
																	"{0}_viewSelecteIblSets".format(viewName)).toString())
			LOGGER.debug("> '{0}' View stored selected Ibl Sets identities: '{1}'.".format(viewName,
																							viewSelectedIblSetsIdentities))
			view.modelSelection["Default"] = viewSelectedIblSetsIdentities and \
			[int(identity) for identity in viewSelectedIblSetsIdentities.split(self.__settingsSeparator)] or []
			view.restoreModelSelection()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def onClose(self):
		"""
		This method is triggered on Framework close.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		for view in self.__views:
			view.storeModelSelection()
			self.__settings.setKey(self.__settingsSection,
								"{0}_viewSelecteIblSets".format(view.objectName()),
								self.__settingsSeparator.join(str(identity) for identity in view.modelSelection["Default"]))

		self.__settings.setKey(self.__settingsSection, "activeView", self.getActiveViewIndex())

		return True

	@core.executionTrace
	def __views_addActions(self):
		"""
		This method sets the Views actions.
		"""

		if not self.__engine.parameters.databaseReadOnly:
			addContentAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.databaseBrowser|Add Content ...",
			slot=self.__views_addContentAction__triggered)
			addIblSetAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.databaseBrowser|Add Ibl Set ...",
			slot=self.__views_addIblSetAction__triggered)
			removeIblSetsAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.databaseBrowser|Remove Ibl Set(s) ...",
			slot=self.__views_removeIblSetsAction__triggered)
			updateIblSetsLocationsAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.databaseBrowser|Update Ibl Set(s) Location(s) ...",
			slot=self.__views_updateIblSetsLocationsAction__triggered)

			for view in self.__views:
				separatorAction = QAction(view)
				separatorAction.setSeparator(True)
				for action in (addContentAction,
								addIblSetAction,
								removeIblSetsAction,
								updateIblSetsLocationsAction,
								separatorAction):
					view.addAction(action)
		else:
			LOGGER.info(
			"{0} | Ibl Sets Database alteration capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __views_addContentAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|Add Content ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addContent_ui()

	@core.executionTrace
	def __views_addIblSetAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|Add Ibl Set ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addIblSet_ui()

	@core.executionTrace
	def __views_removeIblSetsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|Remove Ibl Set(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.removeIblSets_ui()

	@core.executionTrace
	def __views_updateIblSetsLocationsAction__triggered(self, checked):
		"""
		This method is triggered by 
		**'Actions|Umbra|Components|core.databaseBrowser|Update Ibl Set(s) Location(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.updateIblSetsLocation_ui()

	@core.executionTrace
	def __views_pushButtons__clicked(self, index, checked):
		"""
		This method is triggered when **\*_View_pushButton** Widget is clicked.

		:param index: Button index. ( Integer )
		:param checked: Checked state. ( Boolean )
		"""

		self.setActiveViewIndex(index)

	@core.executionTrace
	def __views__doubleClicked(self, index):
		"""
		This method is triggered when a **\*_View** Widget is double clicked.

		:param index: Clicked item index. ( QModelIndex )
		"""

		self.__engine.restoreLayout(self.__inspectLayout)

	@core.executionTrace
	def __Search_Database_lineEdit__textChanged(self, text):
		"""
		This method is triggered when **Search_Database_lineEdit** text changes.

		:param text: Current text value. ( QString )
		"""

		self.setIblSets(self.__searchIblSets(str(self.Search_Database_lineEdit.text()),
											self.__searchContexts[self.__activeSearchContext],
											not self.Case_Sensitive_Matching_pushButton.isChecked() and re.IGNORECASE or 0))

	@core.executionTrace
	def __Thumbnails_Size_horizontalSlider__changed(self, value):
		"""
		This method scales the View icons.

		:param value: Thumbnails size. ( Integer )
		"""

		self.__thumbnailsView.listViewIconSize = value

		self.__thumbnailsView._Thumbnails_QListView__setDefaultUiState()

		# Storing settings key.
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("listViewIconSize", value))
		self.__settings.setKey(self.__settingsSection, "listViewIconSize", value)

	@core.executionTrace
	def __databaseBrowser__modelRefresh(self):
		"""
		This method is triggered when the Model data need refresh.
		"""

		self.setIblSets()

	@core.executionTrace
	def __model__dataChanged(self, startIndex, endIndex):
		"""
		This method is triggered when the Model data have changed.

		:param startIndex: Edited item starting QModelIndex. ( QModelIndex )
		:param endIndex: Edited item ending QModelIndex. ( QModelIndex )
		"""

		iblSetNode = self.__model.getNode(startIndex)

		LOGGER.debug("> Updating Ibl Set '{0}' title to '{1}'.".format(iblSetNode.dbItem.title, iblSetNode.name))
		iblSetNode.synchronizeDbItem()
		iblSetNode.synchronizeToolTip()

		self.__coreDb.commit()

	@core.executionTrace
	def __views__activeViewChanged(self, index):
		"""
		This method is triggered when the active View has changed.

		:param index: Current active View. ( integer )
		"""

		self.Database_Browser_Thumbnails_Slider_frame.setVisible(not index)
		for viewIndex, data in self.__viewsPushButtons.iteritems():
			viewPushButton, image = data
			viewPushButton.setChecked(viewIndex == index and True or False)

	@core.executionTrace
	def __coreDb_database__databaseChanged(self, iblSets):
		"""
		This method is triggered by the
		:class:`umbra.components.core.databaseBrowser.workers.DatabaseBrowser_worker` class
		when the Database has changed.

		:param iblSets: Modified Ibl Sets. ( List )
		"""

		# Ensure that db objects modified by the worker thread will refresh properly.
		self.__coreDb.dbSession.expire_all()
		self.modelRefresh.emit()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler,
											False,
											foundations.exceptions.UserError)
	@umbra.engine.showProcessing("Retrieving Ibl Sets ...")
	def __engine__contentDropped(self, event):
		"""
		This method is triggered when content is dropped into the engine.
		
		:param event: Event. ( QEvent )
		"""

		if not event.mimeData().hasUrls():
			return

		LOGGER.debug("> Drag event urls list: '{0}'!".format(event.mimeData().urls()))

		if not self.__engine.parameters.databaseReadOnly:
			for url in event.mimeData().urls():
				path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
				re.search(r"^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
				if re.search(r"\.{0}$".format(self.__extension), str(url.path())):
					name = strings.getSplitextBasename(path)
					choice = messageBox.messageBox("Question", "Question",
					"'{0}' Ibl Set file has been dropped, would you like to 'Add' it to the Database or \
'Edit' it in the Script Editor?".format(name),
					buttons=QMessageBox.Cancel,
					customButtons=((QString("Add"), QMessageBox.AcceptRole), (QString("Edit"), QMessageBox.AcceptRole)))
					if choice == 0:
						self.addIblSet(name, path)
					elif choice == 1:
						self.__factoryScriptEditor.loadFile(path)
						self.__engine.currentLayout != self.__editLayout and self.__engine.restoreLayout(self.__editLayout)
				else:
					if not os.path.isdir(path):
						return

					osWalker = OsWalker(path)
					osWalker.walk(("\.{0}$".format(self.__extension),), ("\._",))

					if not osWalker.files:
						return

					if messageBox.messageBox("Question", "Question",
					"Would you like to add '{0}' directory Ibl Set(s) file(s) to the Database?".format(path),
					buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
						self.addDirectory(path)
				self.__engine.processEvents()
		else:
			raise foundations.exceptions.UserError("{0} | Cannot perform action, Database has been set read only!".format(
			self.__class__.__name__))

	@core.executionTrace
	def __getCandidateCollectionId(self):
		"""
		This method returns a Collection id.
		
		:return: Collection id. ( Integer )
		"""

		collections = self.__coreCollectionsOutliner.getSelectedCollections()
		id = collections and collections[0].id or None
		return id and id or self.__coreCollectionsOutliner.getCollectionId(
		self.__coreCollectionsOutliner.defaultCollection)

	@core.executionTrace
	def __searchIblSets(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		This method filters the current Collection Ibl Sets.
		
		:param pattern: Ibl Sets filter pattern. ( String )
		:param attribute: Attribute to filter Ibl Sets on. ( String )
		:param flags: Regex filtering flags. ( Integer )

		:return: Filtered Ibl Sets. ( List )
		"""

		try:
			pattern = re.compile(pattern, flags)
		except:
			return

		iblSets = [iblSet for iblSet in set(self.__coreCollectionsOutliner.getCollectionsIblSets(
		self.__coreCollectionsOutliner.getSelectedCollections() or \
		self.__coreCollectionsOutliner.getCollections())).intersection(
		dbCommon.filterIblSets(self.__coreDb.dbSession, "{0}".format(str(pattern.pattern)), attribute, flags))]
		self.Search_Database_lineEdit.completer.setModel(QStringListModel(sorted((value
														for value in set((getattr(iblSetNode, attribute)
														for iblSetNode in iblSets if getattr(iblSetNode, attribute)))))))

		return iblSets

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getActiveView(self):
		"""
		This method returns the current active View.

		:return: Current active View. ( QWidget )
		"""

		return self.Database_Browser_stackedWidget.currentWidget()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getActiveViewIndex(self):
		"""
		This method returns the current active View index.

		:return: Current active View index. ( Integer )
		"""

		return self.Database_Browser_stackedWidget.currentIndex()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setActiveView(self, view):
		"""
		This method sets the active View to given View.

		:param view: View. ( QWidget )
		:return: Method success. ( Boolean )
		"""

		index = self.Database_Browser_stackedWidget.indexOf(view)
		self.Database_Browser_stackedWidget.setCurrentIndex()
		self.activeViewChanged.emit(index)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setActiveViewIndex(self, index):
		"""
		This method sets the active View to given index.

		:param index: Index. ( Integer )
		:return: Method success. ( Boolean )
		"""

		self.Database_Browser_stackedWidget.setCurrentIndex(index)
		self.activeViewChanged.emit(index)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setActiveSearchContext(self, context, *args):
		"""
		This method sets the active search context.

		:param context: Search context. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method succes. ( Boolean )
		"""

		text = "{0} ...".format(context)
		for action in  self.__engine.actionsManager.getCategory(
		"Actions|Umbra|Components|core.databaseBrowser|Search").itervalues():
			action.setChecked(action.text() == text and True or False)

		self.__activeSearchContext = context
		self.Search_Database_lineEdit.setPlaceholderText(text)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.showProcessing("Adding Content ...")
	def addContent_ui(self):
		"""
		This method adds user defined content to the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		directory = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self,
																						"Add content:",
																						RuntimeGlobals.lastBrowsedPath)))
		if not directory:
			return

		LOGGER.debug("> Chosen directory path: '{0}'.".format(directory))
		if self.addDirectory(directory):
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
			self.__class__.__name__, directory))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.showProcessing("Adding Ibl Set ...")
	def addIblSet_ui(self):
		"""
		This method adds an user defined Ibl Set to the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		path = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																		"Add Ibl Set:",
																		RuntimeGlobals.lastBrowsedPath,
																		"Ibls files (*{0})".format(self.__extension))))
		if not path:
			return

		if not self.iblSetExists(path):
			LOGGER.debug("> Chosen Ibl Set path: '{0}'.".format(path))
			if self.addIblSet(strings.getSplitextBasename(path), path):
				return True
			else:
				raise Exception("{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(
				self.__class__.__name__, path))
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Ibl Set already exists in Database!".format(
			self.__class__.__name__, path))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.encapsulateProcessing
	def removeIblSets_ui(self):
		"""
		This method removes user selected Ibl Sets from the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedIblSets = self.getSelectedIblSets()
		if not selectedIblSets:
			return

		if messageBox.messageBox("Question", "Question", "Are you sure you want to remove '{0}' sets(s)?".format(
		", ".join((iblSet.title for iblSet in selectedIblSets))),
		 buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.startProcessing("Removing Ibl Sets ...", len(selectedIblSets))
			success = True
			for iblSet in selectedIblSets:
				success *= self.removeIblSet(iblSet, emitSignal=False) or False
				self.__engine.stepProcessing()
			self.__engine.stopProcessing()

			self.modelRefresh.emit()

			if success:
				return True
			else:
				raise Exception("{0} | Exception raised while removing '{1}' Ibls sets from the Database!".format(
				self.__class__.__name__, ", ". join((iblSet.title for iblSet in selectedIblSets))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.encapsulateProcessing
	def updateIblSetsLocation_ui(self):
		"""
		This method updates user selected Ibl Sets locations.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedIblSets = self.getSelectedIblSets()
		if not selectedIblSets:
			return

		self.__engine.startProcessing("Update Ibl Sets Locations ...", len(selectedIblSets))
		success = True
		for iblSet in selectedIblSets:
			file = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																"Updating '{0}' Ibl Set location:".format(iblSet.title),
																RuntimeGlobals.lastBrowsedPath,
																"Ibls files (*.{0})".format(self.__extension))))
			success *= file and self.updateIblSetLocation(iblSet, file) or False
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.modelRefresh.emit()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while updating '{1}' Ibls sets locations!".format(
			self.__class__.__name__, ", ". join((iblSet.title for iblSet in selectedIblSets))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None,
											False,
											foundations.exceptions.ProgrammingError,
											dbExceptions.DatabaseOperationError)
	def addIblSet(self, name, path, collectionId=None, emitSignal=True):
		"""
		This method adds an Ibl Set to the Database.

		:param name: Ibl Set name. ( String )
		:param path: Ibl Set path. ( String )
		:param collectionId: Target Collection id. ( Integer )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.iblSetExists(path):
			LOGGER.info("{0} | Adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, name))
			if dbCommon.addIblSet(self.__coreDb.dbSession, name, path, collectionId or self.__getCandidateCollectionId()):
				emitSignal and self.modelRefresh.emit()
				return True
			else:
				raise dbExceptions.DatabaseOperationError(
				"{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, name))
		else:
			raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Ibl Set already exists in Database!".format(self.__class__.__name__, name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@umbra.engine.encapsulateProcessing
	def addDirectory(self, directory, collectionId=None):
		"""
		This method adds directory Ibl Sets to the Database.

		:param directory: Directory to add. ( String )
		:param collectionId: Target Collection id. ( Integer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing directory '{0}' osWalker.".format(directory))

		osWalker = OsWalker(directory)
		osWalker.walk(("\.{0}$".format(self.__extension),), ("\._",))

		self.__engine.startProcessing("Adding Directory Ibl Sets ...", len(osWalker.files))
		success = True
		for iblSet, path in osWalker.files.iteritems():
			if not self.iblSetExists(path):
				success *= self.addIblSet(namespace.getNamespace(iblSet, rootOnly=True),
										path,
										collectionId or self.__getCandidateCollectionId(),
										emitSignal=False) or False
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.modelRefresh.emit()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
			self.__class__.__name__, directory))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, dbExceptions.DatabaseOperationError)
	def removeIblSet(self, iblSet, emitSignal=True):
		"""
		This method removes given Ibl Set from the Database.

		:param iblSet: Ibl Set to remove. ( DbIblSet )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Removing '{1}' Ibl Set from the Database!".format(self.__class__.__name__, iblSet.title))
		if dbCommon.removeIblSet(self.__coreDb.dbSession, iblSet.id):
			emitSignal and self.modelRefresh.emit()
			return True
		else:
			raise dbExceptions.DatabaseOperationError(
			"{0} | Exception raised while removing '{1}' Ibl Set from the Database!".format(self.__class__.__name__,
																							iblSet.title))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, dbExceptions.DatabaseOperationError)
	def updateIblSetLocation(self, iblSet, file, emitSignal=True):
		"""
		This method updates given Ibl Set location.

		:param iblSet: Ibl Set to update. ( DbIblSet )
		:param iblSet: New Ibl Set file. ( String )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Updating '{1}' Ibl Set with new location: '{2}'!".format(self.__class__.__name__,
																					iblSet.title,
																					file))
		if dbCommon.updateIblSetLocation(self.__coreDb.dbSession, iblSet, file):
			emitSignal and self.modelRefresh.emit()
			return True
		else:
			raise dbExceptions.DatabaseOperationError("{0} | Exception raised while updating '{1}' Ibl Set location!".format(
			self.__class__.__name__, iblSet.title))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getIblSets(self):
		"""
		This method returns Database Ibl Sets.

		:return: Database Ibl Sets. ( List )
		"""

		return [iblSet for iblSet in dbCommon.getIblSets(self.__coreDb.dbSession)]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def filterIblSets(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		This method filters the Database Ibl Sets on given attribute using given pattern.
		
		:param pattern: Filter pattern. ( String )
		:param attribute: Attribute to filter on. ( String )
		:param flags: Regex filtering flags. ( Integer )

		:return: Filtered Database Ibl Sets. ( List )
		"""

		try:
			pattern = re.compile(pattern, flags)
		except:
			return

		return list(set(self.getIblSets()).intersection(
		dbCommon.filterIblSets(self.__coreDb.dbSession, "{0}".format(str(pattern.pattern)), attribute, flags)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def iblSetExists(self, path):
		"""
		This method returns if given Ibl Set path exists in the Database.

		:param path: Collection path. ( String )
		:return: Collection exists. ( Boolean )
		"""

		return dbCommon.iblSetExists(self.__coreDb.dbSession, path)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listIblSets(self):
		"""
		This method lists Database Ibl Sets names.

		:return: Database Ibl Sets names. ( List )
		
		:note: The list is actually returned using 'title' attributes instead of 'name' attributes
		"""

		return [iblSet.title for iblSet in self.getIblSets()]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setIblSets(self, iblSets=None):
		"""
		This method sets the Ibl Sets Model nodes.
	
		:param iblSets: Ibl Sets to set. ( List )
		:return: Method success. ( Boolean )
		"""

		nodeFlags = self.__engine.parameters.databaseReadOnly and int(Qt.ItemIsSelectable | Qt.ItemIsEnabled) or \
		int(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)
		iblSets = iblSets or self.__coreCollectionsOutliner.getCollectionsIblSets(
		self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())
		rootNode = umbra.ui.models.DefaultNode(name="InvisibleRootNode")
		for iblSet in iblSets:
			iblSetNode = dbNodes.IblSetNode(iblSet,
											name=iblSet.title,
											parent=rootNode,
											nodeFlags=nodeFlags,
											attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

		rootNode.sortChildren(attribute="title")

		self.__model.initializeModel(rootNode)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getIblSetByName(self, name):
		"""
		This method returns Database Ibl Set with given name.

		:param name: Ibl Set name. ( String )
		:return: Database Ibl Set. ( DbIblSet )
		
		:note: The filtering is actually performed on 'title' attributes instead of 'name' attributes.
		"""

		iblSets = self.filterIblSets(r"^{0}$".format(name), "title")
		return iblSets and iblSets[0] or None

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedNodes(self):
		"""
		This method returns the current active View selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return self.getActiveView().getSelectedNodes()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedIblSetsNodes(self):
		"""
		This method returns the current active View selected Ibl Sets nodes.

		:return: View selected Ibl Sets nodes. ( List )
		"""

		return [node for node in self.getSelectedNodes() if node.family == "IblSet"]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedIblSets(self):
		"""
		This method returns the current active View selected Ibl Sets.

		:return: View selected Ibl Sets. ( List )
		"""

		return [node.dbItem for node in self.getSelectedIblSetsNodes()]
