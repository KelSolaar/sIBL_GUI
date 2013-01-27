#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**iblSetsOutliner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`IblSetsOutliner` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import os
import platform
import re
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
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
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import foundations.walkers
import sibl_gui.components.core.database.exceptions
import sibl_gui.components.core.database.operations
import umbra.engine
import umbra.exceptions
import umbra.ui.common
import umbra.ui.nodes
import umbra.ui.widgets.messageBox as messageBox
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.core.database.nodes import IblSetNode
from sibl_gui.components.core.iblSetsOutliner.models import IblSetsModel
from sibl_gui.components.core.iblSetsOutliner.views import Columns_QListView
from sibl_gui.components.core.iblSetsOutliner.views import Details_QTreeView
from sibl_gui.components.core.iblSetsOutliner.views import Thumbnails_QListView
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "IblSetsOutliner"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Ibl_Sets_Outliner.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class IblSetsOutliner(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner` Component Interface class.
	| It defines methods for Database Ibl Sets management.
	"""

	# Custom signals definitions.
	refreshNodes = pyqtSignal()
	"""
	This signal is emited by the :class:`IblSetsOutliner` class when :obj:`IblSetsOutliner.model` class property model
	nodes needs to be refreshed. ( pyqtSignal )
	"""

	activeViewChanged = pyqtSignal(int)
	"""
	This signal is emited by the :class:`IblSetsOutliner` class when the current active View is changed. ( pyqtSignal )
	
	:return: Current active view index. ( Integer )	
	"""

	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(IblSetsOutliner, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiResourcesDirectory = "resources"
		self.__uiThumbnailsViewImage = "Thumbnails_View.png"
		self.__uiColumnsViewImage = "Columns_View.png"
		self.__uiDetailsViewImage = "Details_View.png"
		self.__uiLargestSizeImage = "Largest_Size.png"
		self.__uiSmallestSizeImage = "Smallest_Size.png"
		self.__dockArea = 8

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None
		self.__settingsSeparator = ","

		self.__extension = "ibl"

		self.__inspectLayout = "inspectCentric"

		self.__scriptEditor = None
		self.__collectionsOutliner = None

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
		self.__searchContextsMenu = None

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
	def uiThumbnailsViewImage(self):
		"""
		This method is the property for **self.__uiThumbnailsViewImage** attribute.

		:return: self.__uiThumbnailsViewImage. ( String )
		"""

		return self.__uiThumbnailsViewImage

	@uiThumbnailsViewImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiThumbnailsViewImage(self, value):
		"""
		This method is the setter method for **self.__uiThumbnailsViewImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiThumbnailsViewImage"))

	@uiThumbnailsViewImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiColumnsViewImage(self, value):
		"""
		This method is the setter method for **self.__uiColumnsViewImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiColumnsViewImage"))

	@uiColumnsViewImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiDetailsViewImage(self, value):
		"""
		This method is the setter method for **self.__uiDetailsViewImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiDetailsViewImage"))

	@uiDetailsViewImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiDetailsViewImage(self):
		"""
		This method is the deleter method for **self.__uiDetailsViewImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiDetailsViewImage"))

	@property
	def uiLargestSizeImage(self):
		"""
		This method is the property for **self.__uiLargestSizeImage** attribute.

		:return: self.__uiLargestSizeImage. ( String )
		"""

		return self.__uiLargestSizeImage

	@uiLargestSizeImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiLargestSizeImage(self, value):
		"""
		This method is the setter method for **self.__uiLargestSizeImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLargestSizeImage"))

	@uiLargestSizeImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiSmallestSizeImage(self, value):
		"""
		This method is the setter method for **self.__uiSmallestSizeImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiSmallestSizeImage"))

	@uiSmallestSizeImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for **self.__settingsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSeparator(self, value):
		"""
		This method is the setter method for **self.__settingsSeparator** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def extension(self, value):
		"""
		This method is the setter method for **self.__extension** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "extension"))

	@extension.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		This method is the deleter method for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

	@property
	def inspectLayout(self):
		"""
		This method is the property for **self.__inspectLayout** attribute.

		:return: self.__inspectLayout. ( String )
		"""

		return self.__inspectLayout

	@inspectLayout.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def inspectLayout(self, value):
		"""
		This method is the setter method for **self.__inspectLayout** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectLayout"))

	@inspectLayout.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def inspectLayout(self):
		"""
		This method is the deleter method for **self.__inspectLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectLayout"))

	@property
	def scriptEditor(self):
		"""
		This method is the property for **self.__scriptEditor** attribute.

		:return: self.__scriptEditor. ( QWidget )
		"""

		return self.__scriptEditor

	@scriptEditor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self, value):
		"""
		This method is the setter method for **self.__scriptEditor** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "scriptEditor"))

	@scriptEditor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self):
		"""
		This method is the deleter method for **self.__scriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "scriptEditor"))

	@property
	def collectionsOutliner(self):
		"""
		This method is the property for **self.__collectionsOutliner** attribute.

		:return: self.__collectionsOutliner. ( QWidget )
		"""

		return self.__collectionsOutliner

	@collectionsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def collectionsOutliner(self, value):
		"""
		This method is the setter method for **self.__collectionsOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "collectionsOutliner"))

	@collectionsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def collectionsOutliner(self):
		"""
		This method is the deleter method for **self.__collectionsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "collectionsOutliner"))

	@property
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( IblSetsModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( IblSetsModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def views(self, value):
		"""
		This method is the setter method for **self.__views** attribute.

		:param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "views"))

	@views.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def viewsPushButtons(self, value):
		"""
		This method is the setter method for **self.__viewsPushButtons** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "viewsPushButtons"))

	@viewsPushButtons.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def thumbnailsView(self, value):
		"""
		This method is the setter method for **self.__thumbnailsView** attribute.

		:param value: Attribute value. ( QListView )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "thumbnailsView"))

	@thumbnailsView.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def columnsView(self, value):
		"""
		This method is the setter method for **self.__columnsView** attribute.

		:param value: Attribute value. ( QListView )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "columnsView"))

	@columnsView.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def detailsView(self, value):
		"""
		This method is the setter method for **self.__detailsView** attribute.

		:param value: Attribute value. ( QTreeView )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "detailsView"))

	@detailsView.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def detailsViewHeaders(self, value):
		"""
		This method is the setter method for **self.__detailsViewHeaders** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "detailsViewHeaders"))

	@detailsViewHeaders.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchContexts(self, value):
		"""
		This method is the setter method for **self.__searchContexts** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchContexts"))

	@searchContexts.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeSearchContext(self, value):
		"""
		This method is the setter method for **self.__activeSearchContext** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "activeSearchContext"))

	@activeSearchContext.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeSearchContext(self):
		"""
		This method is the deleter method for **self.__activeSearchContext** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activeSearchContext"))

	@property
	def searchContextMenu(self):
		"""
		This method is the property for **self.__searchContextMenu** attribute.

		:return: self.__searchContextMenu. ( QMenu )
		"""

		return self.__searchContextMenu

	@searchContextMenu.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchContextMenu(self, value):
		"""
		This method is the setter method for **self.__searchContextMenu** attribute.

		:param value: Attribute value. ( self.__searchContextsMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchContextMenu"))

	@searchContextMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchContextMenu(self):
		"""
		This method is the deleter method for **self.__searchContextMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchContextMenu"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(__file__), self.__uiResourcesDirectory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__scriptEditor = self.__engine.componentsManager["factory.scriptEditor"]
		self.__collectionsOutliner = self.__engine.componentsManager["core.collectionsOutliner"]

		self.activated = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

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

		self.Ibl_Sets_Outliner_stackedWidget = QStackedWidget(self)
		self.Ibl_Sets_Outliner_gridLayout.addWidget(self.Ibl_Sets_Outliner_stackedWidget)

		self.__thumbnailsView = Thumbnails_QListView(self,
													self.__model,
													self.__engine.parameters.databaseReadOnly,
													"No Ibl Set to view!")
		self.__thumbnailsView.setObjectName("Thumbnails_listView")
		self.__thumbnailsView.setContextMenuPolicy(Qt.ActionsContextMenu)
		listViewIconSize, state = self.__settings.getKey(self.__settingsSection, "listViewIconSize").toInt()
		if state:
			self.__thumbnailsView.listViewIconSize = listViewIconSize
		self.Ibl_Sets_Outliner_stackedWidget.addWidget(self.__thumbnailsView)

		self.__columnsView = Columns_QListView(self,
											self.__model,
											self.__engine.parameters.databaseReadOnly,
											"No Ibl Set to view!")
		self.__columnsView.setObjectName("Columns_listView")
		self.__columnsView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.Ibl_Sets_Outliner_stackedWidget.addWidget(self.__columnsView)

		self.__detailsView = Details_QTreeView(self,
											self.__model,
											self.__engine.parameters.databaseReadOnly,
											"No Ibl Set to view!")
		self.__detailsView.setObjectName("Details_treeView")
		self.__detailsView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.Ibl_Sets_Outliner_stackedWidget.addWidget(self.__detailsView)

		self.__views = (self.__thumbnailsView, self.__columnsView, self.__detailsView)
		self.__views_addActions()
		self.__viewsPushButtons = {0 : (self.Thumbnails_View_pushButton, self.__uiThumbnailsViewImage),
									1 : (self.Columns_View_pushButton, self.__uiColumnsViewImage),
									2 : (self.Details_View_pushButton, self.__uiDetailsViewImage)}

		for index, data in self.__viewsPushButtons.iteritems():
			viewPushButton, image = data
			viewPushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, image)))

		self.Search_Database_lineEdit = Search_QLineEdit(self)
		self.Search_Database_horizontalLayout.addWidget(self.Search_Database_lineEdit)
		self.Search_Database_lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.__searchContextsMenu = QMenu()
		for context in self.__searchContexts.iterkeys():
			self.__searchContextsMenu.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.iblSetsOutliner|Search|Set '{0}' Context ...".format(context),
			text="{0} ...".format(context),
			checkable=True,
			slot=functools.partial(self.setActiveSearchContext, context)))
		self.Search_Database_lineEdit.searchActiveLabel.setMenu(self.__searchContextsMenu)
		self.setActiveSearchContext(self.__activeSearchContext)

		self.Thumbnails_Size_horizontalSlider.setValue(self.__thumbnailsView.listViewIconSize)
		self.Largest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiLargestSizeImage)))
		self.Smallest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiSmallestSizeImage)))

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

		self.refreshNodes.connect(self.__model__refreshNodes)
		self.__model.modelReset.connect(self.__collectionsOutliner._CollectionsOutliner__model__refreshAttributes)

		if not self.__engine.parameters.databaseReadOnly:
			self.__engine.fileSystemEventsManager.fileChanged.connect(self.__engine_fileSystemEventsManager__fileChanged)
			self.__engine.contentDropped.connect(self.__engine__contentDropped)
		else:
			LOGGER.info("{0} | Ibl Sets file system events ignored by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		self.initializedUi = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.setCentralWidget(self)

		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def onStartup(self):
		"""
		This method is triggered on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			# Wizard if Ibl Sets table is empty.
			if not self.getIblSets():
				if messageBox.messageBox("Question", "Question",
				"The Database has no Ibl Sets, would you like to add some?",
				buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
					directory = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self,
																						 "Add Content:",
																						RuntimeGlobals.lastBrowsedPath)))
					if directory:
						if not self.addDirectory(directory):
							raise Exception(
							"{0} | Exception raised while adding '{1}' directory content to the Database!".format(
							self.__class__.__name__, directory))

			# Ibl Sets table integrity checking.
			erroneousIblSets = sibl_gui.components.core.database.operations.checkIblSetsTableIntegrity()
			for iblSet, exceptions in erroneousIblSets.iteritems():
				if sibl_gui.components.core.database.exceptions.MissingIblSetFileError in exceptions:
					choice = messageBox.messageBox("Question", "Error",
					"{0} | '{1}' Ibl Set file is missing, would you like to update it's location?".format(
					self.__class__.__name__, iblSet.name),
					QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No,
					customButtons=((QString("No To All"), QMessageBox.RejectRole),))

					if choice == 0:
						break

					if choice == QMessageBox.Yes:
						if self.updateIblSetLocationUi(iblSet):
							# TODO: Check updated Ibl Set file integrity.
							continue

				for exception in exceptions:
					self.__engine.notificationsManager.warnify(
					"{0} | '{1}' {2}".format(self.__class__.__name__,
									iblSet.name,
									sibl_gui.components.core.database.operations.DATABASE_EXCEPTIONS[exception]))
		else:
			LOGGER.info("{0} | Database Ibl Sets wizard and Ibl Sets integrity checking method deactivated\
by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeView, state = self.__settings.getKey(self.__settingsSection, "activeView").toInt()
		state and self.setActiveViewIndex(activeView)

		for view in self.__views:
			viewName = view.objectName()
			viewSelectedIblSetsIdentities = foundations.strings.encode(self.__settings.getKey(self.__settingsSection,
																	"{0}_viewSelecteIblSets".format(viewName)).toString())
			LOGGER.debug("> '{0}' View stored selected Ibl Sets identities: '{1}'.".format(viewName,
																							viewSelectedIblSetsIdentities))
			view.modelSelection["Default"] = viewSelectedIblSetsIdentities and \
			[int(identity) for identity in viewSelectedIblSetsIdentities.split(self.__settingsSeparator)] or []
			view.restoreModelSelection()
		return True

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
								self.__settingsSeparator.join(foundations.strings.encode(identity) \
								for identity in view.modelSelection["Default"]))

		self.__settings.setKey(self.__settingsSection, "activeView", self.getActiveViewIndex())

		return True

	def __model__refreshNodes(self):
		"""
		This method is triggered when the Model Nodes need refresh.
		"""

		self.setIblSets()

	def __views_addActions(self):
		"""
		This method sets the Views actions.
		"""

		if not self.__engine.parameters.databaseReadOnly:
			addContentAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.iblSetsOutliner|Add Content ...",
			slot=self.__views_addContentAction__triggered)
			addIblSetAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.iblSetsOutliner|Add Ibl Set ...",
			slot=self.__views_addIblSetAction__triggered)
			removeIblSetsAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.iblSetsOutliner|Remove Ibl Set(s) ...",
			slot=self.__views_removeIblSetsAction__triggered)
			updateIblSetsLocationsAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.iblSetsOutliner|Update Ibl Set(s) Location(s) ...",
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

	def __views_addContentAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.iblSetsOutliner|Add Content ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addContentUi()

	def __views_addIblSetAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.iblSetsOutliner|Add Ibl Set ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addIblSetUi()

	def __views_removeIblSetsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.iblSetsOutliner|Remove Ibl Set(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.removeIblSetsUi()

	def __views_updateIblSetsLocationsAction__triggered(self, checked):
		"""
		This method is triggered by 
		**'Actions|Umbra|Components|core.iblSetsOutliner|Update Ibl Set(s) Location(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.updateSelectedIblSetsLocationUi()

	def __views_pushButtons__clicked(self, index, checked):
		"""
		This method is triggered when **\*_View_pushButton** Widget is clicked.

		:param index: Button index. ( Integer )
		:param checked: Checked state. ( Boolean )
		"""

		self.setActiveViewIndex(index)

	def __views__doubleClicked(self, index):
		"""
		This method is triggered when a **\*_View** Widget is double clicked.

		:param index: Clicked item index. ( QModelIndex )
		"""

		self.__engine.layoutsManager.restoreLayout(self.__inspectLayout)

	def __views__activeViewChanged(self, index):
		"""
		This method is triggered when the active View has changed.

		:param index: Current active View. ( integer )
		"""

		self.Ibl_Sets_Outliner_Thumbnails_Slider_frame.setVisible(not index)
		for viewIndex, data in self.__viewsPushButtons.iteritems():
			viewPushButton, image = data
			viewPushButton.setChecked(viewIndex == index and True or False)

	def __Search_Database_lineEdit__textChanged(self, text):
		"""
		This method is triggered when **Search_Database_lineEdit** text changes.

		:param text: Current text value. ( QString )
		"""

		self.setIblSets(self.__searchIblSets(foundations.strings.encode(self.Search_Database_lineEdit.text()),
											self.__searchContexts[self.__activeSearchContext],
											re.IGNORECASE if self.Case_Sensitive_Matching_pushButton.isChecked() else 0))

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

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
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
				re.search(r"^\/[A-Z]:", foundations.strings.encode(url.path())) and foundations.strings.encode(url.path())[1:] \
				or foundations.strings.encode(url.path())
				if re.search(r"\.{0}$".format(self.__extension), foundations.strings.encode(url.path())):
					name = foundations.strings.getSplitextBasename(path)
					choice = messageBox.messageBox("Question", "Question",
					"'{0}' Ibl Set file has been dropped, would you like to 'Add' it to the Database or \
'Edit' it in the Script Editor?".format(name),
					buttons=QMessageBox.Cancel,
					customButtons=((QString("Add"), QMessageBox.AcceptRole), (QString("Edit"), QMessageBox.AcceptRole)))
					if choice == 0:
						self.addIblSet(name, path)
					elif choice == 1:
						self.__scriptEditor.loadFile(path) and self.__scriptEditor.restoreDevelopmentLayout()
				else:
					if not os.path.isdir(path):
						return

					if not list(foundations.walkers.filesWalker(path, ("\.{0}$".format(self.__extension),), ("\._",))):
						return

					if messageBox.messageBox("Question", "Question",
					"Would you like to add '{0}' directory Ibl Set(s) file(s) to the Database?".format(path),
					buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
						self.addDirectory(path)
				self.__engine.processEvents()
		else:
			raise foundations.exceptions.UserError("{0} | Cannot perform action, Database has been set read only!".format(
			self.__class__.__name__))

	def __engine_fileSystemEventsManager__fileChanged(self, file):
		"""
		This method is triggered by the **fileSystemEventsManager** when a file is changed.
		
		:param file: File changed. ( String )
		"""

		iblSet = foundations.common.getFirstItem(filter(lambda x: x.path == file, self.getIblSets()))
		if not iblSet:
			return

		if sibl_gui.components.core.database.operations.updateIblSetContent(iblSet):
			self.__engine.notificationsManager.notify(
			"{0} | '{1}' Ibl Set file has been reparsed and associated database object updated!".format(
			self.__class__.__name__, iblSet.title))
			self.refreshNodes.emit()

	def __getCandidateCollectionId(self):
		"""
		This method returns a Collection id.
		
		:return: Collection id. ( Integer )
		"""

		collections = self.__collectionsOutliner.getSelectedCollections()
		collection = foundations.common.getFirstItem(collections)
		identity = collection and collection.id or None
		return identity and identity or self.__collectionsOutliner.getCollectionId(
		self.__collectionsOutliner.defaultCollection)

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
		except Exception:
			return list()

		iblSets = [iblSet for iblSet in set(self.__collectionsOutliner.getCollectionsIblSets(
		self.__collectionsOutliner.getSelectedCollections() or \
		self.__collectionsOutliner.getCollections())).intersection(
		sibl_gui.components.core.database.operations.filterIblSets(
		"{0}".format(foundations.strings.encode(pattern.pattern)), attribute, flags))]
		self.Search_Database_lineEdit.completer.setModel(QStringListModel(sorted((value
														for value in set((getattr(iblSetNode, attribute)
														for iblSetNode in iblSets if getattr(iblSetNode, attribute)))))))

		return iblSets

	def getActiveView(self):
		"""
		This method returns the current active View.

		:return: Current active View. ( QWidget )
		"""

		return self.Ibl_Sets_Outliner_stackedWidget.currentWidget()

	def getActiveViewIndex(self):
		"""
		This method returns the current active View index.

		:return: Current active View index. ( Integer )
		"""

		return self.Ibl_Sets_Outliner_stackedWidget.currentIndex()

	def setActiveView(self, view):
		"""
		This method sets the active View to given View.

		:param view: View. ( QWidget )
		:return: Method success. ( Boolean )
		"""

		index = self.Ibl_Sets_Outliner_stackedWidget.indexOf(view)
		self.Ibl_Sets_Outliner_stackedWidget.setCurrentIndex()
		self.activeViewChanged.emit(index)
		return True

	def setActiveViewIndex(self, index):
		"""
		This method sets the active View to given index.

		:param index: Index. ( Integer )
		:return: Method success. ( Boolean )
		"""

		self.Ibl_Sets_Outliner_stackedWidget.setCurrentIndex(index)
		self.activeViewChanged.emit(index)
		return True

	def setActiveSearchContext(self, context, *args):
		"""
		This method sets the active search context.

		:param context: Search context. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method succes. ( Boolean )
		"""

		text = "{0} ...".format(context)
		for action in  self.__engine.actionsManager.getCategory(
		"Actions|Umbra|Components|core.iblSetsOutliner|Search").itervalues():
			action.setChecked(action.text() == text and True or False)

		self.__activeSearchContext = context
		self.Search_Database_lineEdit.setPlaceholderText(text)
		return True

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.showProcessing("Adding Content ...")
	def addContentUi(self):
		"""
		This method adds user defined content to the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		directory = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self,
																						"Add Content:",
																						RuntimeGlobals.lastBrowsedPath)))
		if not directory:
			return False

		LOGGER.debug("> Chosen directory path: '{0}'.".format(directory))
		if self.addDirectory(directory):
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
			self.__class__.__name__, directory))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.showProcessing("Adding Ibl Set ...")
	def addIblSetUi(self):
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
			return False

		if not self.iblSetExists(path):
			LOGGER.debug("> Chosen Ibl Set path: '{0}'.".format(path))
			if self.addIblSet(foundations.strings.getSplitextBasename(path), path):
				return True
			else:
				raise Exception("{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(
				self.__class__.__name__, path))
		else:
			self.__engine.notificationsManager.warnify(
			"{0} | '{1}' Ibl Set already exists in Database!".format(self.__class__.__name__, path))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.encapsulateProcessing
	def removeIblSetsUi(self):
		"""
		This method removes user selected Ibl Sets from the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedIblSets = self.getSelectedIblSets()
		if not selectedIblSets:
			return False

		if messageBox.messageBox("Question", "Question", "Are you sure you want to remove '{0}' sets(s)?".format(
		", ".join((iblSet.title for iblSet in selectedIblSets))),
		 buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.startProcessing("Removing Ibl Sets ...", len(selectedIblSets))
			success = True
			for iblSet in selectedIblSets:
				success *= umbra.ui.common.signalsBlocker(self, self.removeIblSet, iblSet) or False
				self.__engine.stepProcessing()
			self.__engine.stopProcessing()

			self.refreshNodes.emit()

			if success:
				return True
			else:
				raise Exception("{0} | Exception raised while removing '{1}' Ibls sets from the Database!".format(
				self.__class__.__name__, ", ". join((iblSet.title for iblSet in selectedIblSets))))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def updateIblSetLocationUi(self, iblSet):
		"""
		This method updates given Ibl Set location.

		:param iblSet: Ibl Set to update. ( IblSet )
		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		file = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																"Updating '{0}' Template Location:".format(iblSet.name),
																RuntimeGlobals.lastBrowsedPath,
																"Ibl Set files (*{0})".format(self.__extension))))
		if not file:
			return False

		LOGGER.info("{0} | Updating '{1}' Ibl Set with new location '{2}'!".format(self.__class__.__name__,
																					iblSet.name, file))
		if sibl_gui.components.core.database.operations.updateIblSetLocation(iblSet, file):
			self.refreshNodes.emit()
			return True
		else:
			raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
			"{0} | Exception raised while updating '{1}' Ibl Set location!".format(self.__class__.__name__, iblSet.name))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.encapsulateProcessing
	def updateSelectedIblSetsLocationUi(self):
		"""
		This method updates user selected Ibl Sets locations.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedIblSets = self.getSelectedIblSets()
		if not selectedIblSets:
			return False

		self.__engine.startProcessing("Update Ibl Sets Locations ...", len(selectedIblSets))
		success = True
		for iblSet in selectedIblSets:
			success *= self.updateIblSetLocationUi(iblSet)
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.refreshNodes.emit()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while updating '{1}' Ibls sets locations!".format(
			self.__class__.__name__, ", ". join((iblSet.title for iblSet in selectedIblSets))))

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError,
											sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def addIblSet(self, name, path, collectionId=None):
		"""
		This method adds an Ibl Set to the Database.

		:param name: Ibl Set name. ( String )
		:param path: Ibl Set path. ( String )
		:param collectionId: Target Collection id. ( Integer )
		:return: Method success. ( Boolean )
		"""

		if not self.iblSetExists(path):
			LOGGER.info("{0} | Adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, name))
			if sibl_gui.components.core.database.operations.addIblSet(
			name, path, collectionId or self.__getCandidateCollectionId()):
				self.refreshNodes.emit()
				return True
			else:
				raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
				"{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, name))
		else:
			raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Ibl Set already exists in Database!".format(self.__class__.__name__, name))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.encapsulateProcessing
	def addDirectory(self, directory, collectionId=None):
		"""
		This method adds directory Ibl Sets to the Database.

		:param directory: Directory to add. ( String )
		:param collectionId: Target Collection id. ( Integer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing directory '{0}' filesWalker.".format(directory))

		files = list(foundations.walkers.filesWalker(directory, ("\.{0}$".format(self.__extension),), ("\._",)))

		self.__engine.startProcessing("Adding Directory Ibl Sets ...", len(files))
		success = True
		for path in files:
			if not self.iblSetExists(path):
				success *= umbra.ui.common.signalsBlocker(self,
														self.addIblSet,
														foundations.strings.getSplitextBasename(path),
														path,
														collectionId or self.__getCandidateCollectionId()) or False
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.refreshNodes.emit()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
			self.__class__.__name__, directory))

	@foundations.exceptions.handleExceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def removeIblSet(self, iblSet):
		"""
		This method removes given Ibl Set from the Database.

		:param iblSet: Ibl Set to remove. ( IblSet )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Removing '{1}' Ibl Set from the Database!".format(self.__class__.__name__, iblSet.title))
		if sibl_gui.components.core.database.operations.removeIblSet(iblSet.id):
			self.refreshNodes.emit()
			return True
		else:
			raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
			"{0} | Exception raised while removing '{1}' Ibl Set from the Database!".format(self.__class__.__name__,
																							iblSet.title))

	@foundations.exceptions.handleExceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def updateIblSetLocation(self, iblSet, file):
		"""
		This method updates given Ibl Set location.

		:param iblSet: Ibl Set to update. ( IblSet )
		:param iblSet: New Ibl Set file. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Updating '{1}' Ibl Set with new location: '{2}'!".format(self.__class__.__name__,
																					iblSet.title,
																					file))
		if sibl_gui.components.core.database.operations.updateIblSetLocation(iblSet, file):
			self.refreshNodes.emit()
			return True
		else:
			raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
			"{0} | Exception raised while updating '{1}' Ibl Set location!".format(self.__class__.__name__, iblSet.title))

	def getIblSets(self):
		"""
		This method returns Database Ibl Sets.

		:return: Database Ibl Sets. ( List )
		"""

		return [iblSet for iblSet in sibl_gui.components.core.database.operations.getIblSets()]

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
		except Exception:
			return list()

		return list(set(self.getIblSets()).intersection(
		sibl_gui.components.core.database.operations.filterIblSets(
		"{0}".format(foundations.strings.encode(pattern.pattern)), attribute, flags)))

	def iblSetExists(self, path):
		"""
		This method returns if given Ibl Set path exists in the Database.

		:param path: Collection path. ( String )
		:return: Collection exists. ( Boolean )
		"""

		return sibl_gui.components.core.database.operations.iblSetExists(path)

	def listIblSets(self):
		"""
		This method lists Database Ibl Sets names.

		:return: Database Ibl Sets names. ( List )
		
		:note: The list is actually returned using 'title' attributes instead of 'name' attributes
		"""

		return [iblSet.title for iblSet in self.getIblSets()]

	def setIblSets(self, iblSets=None):
		"""
		This method sets the Ibl Sets Model nodes.
	
		:param iblSets: Ibl Sets to set. ( List )
		:return: Method success. ( Boolean )
		"""

		nodeFlags = self.__engine.parameters.databaseReadOnly and int(Qt.ItemIsSelectable | Qt.ItemIsEnabled) or \
		int(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)
		iblSets = iblSets or self.__collectionsOutliner.getCollectionsIblSets(
		self.__collectionsOutliner.getSelectedCollections() or self.__collectionsOutliner.getCollections())
		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		for iblSet in iblSets:
			iblSetNode = IblSetNode(iblSet,
									name=iblSet.title,
									parent=rootNode,
									nodeFlags=nodeFlags,
									attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

			path = foundations.strings.encode(iblSet.path)
			if not foundations.common.pathExists(path):
				continue

			not self.__engine.fileSystemEventsManager.isPathRegistered(path) and \
			self.__engine.fileSystemEventsManager.registerPath(path, modifiedTime=float(iblSet.osStats.split(",")[8]))

		rootNode.sortChildren(attribute="title")

		self.__model.initializeModel(rootNode)
		return True

	def getIblSetByName(self, name):
		"""
		This method returns Database Ibl Set with given name.

		:param name: Ibl Set name. ( String )
		:return: Database Ibl Set. ( IblSet )
		
		:note: The filtering is actually performed on 'title' attributes instead of 'name' attributes.
		"""

		iblSets = self.filterIblSets(r"^{0}$".format(name), "title")
		return foundations.common.getFirstItem(iblSets)

	def getSelectedNodes(self):
		"""
		This method returns the current active View selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return self.getActiveView().getSelectedNodes()

	def getSelectedIblSetsNodes(self):
		"""
		This method returns the current active View selected Ibl Sets nodes.

		:return: View selected Ibl Sets nodes. ( List )
		"""

		return [node for node in self.getSelectedNodes() if node.family == "IblSet"]

	def getSelectedIblSets(self):
		"""
		This method returns the current active View selected Ibl Sets.

		:return: View selected Ibl Sets. ( List )
		"""

		return [node.databaseItem for node in self.getSelectedIblSetsNodes()]
