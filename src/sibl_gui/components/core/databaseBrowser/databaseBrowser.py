#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**databaseBrowser.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`DatabaseBrowser` Component Interface class, the :class:`Thumbnails_QListView` class and the the :class:`DatabaseBrowser_Worker` worker thread class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import logging
import os
import platform
import re
from collections import OrderedDict
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
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
import sibl_gui.ui.views
import umbra.ui.widgets.messageBox as messageBox
from foundations.walkers import OsWalker
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "DatabaseBrowser_Worker", "IblSetsModel", "Thumbnails_QListView", "Thumbnails_QListView", "Details_QTreeView", "DatabaseBrowser"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Database_Browser.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class DatabaseBrowser_Worker(QThread):
	"""
	This class is a `QThread <http://doc.qt.nokia.com/4.7/qthread.html>`_ subclass used to track modified Ibl Sets and update the Database accordingly.
	"""

	# Custom signals definitions.
	databaseChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QThread.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__dbSession = self.__container.coreDb.dbSessionMaker()

		self.__timer = None
		self.__timerCycleMultiplier = 5

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def dbSession(self):
		"""
		This method is the property for **self.__dbSession** attribute.

		:return: self.__dbSession. ( Object )
		"""

		return self.__dbSession

	@dbSession.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSession(self, value):
		"""
		This method is the setter method for **self.__dbSession** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dbSession"))

	@dbSession.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSession(self):
		"""
		This method is the deleter method for **self.__dbSession** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dbSession"))

	@property
	def timer(self):
		"""
		This method is the property for **self.__timer** attribute.

		:return: self.__timer. ( QTimer )
		"""

		return self.__timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		This method is the setter method for **self.__timer** attribute.

		:param value: Attribute value. ( QTimer )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timer"))

	@timer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		This method is the deleter method for **self.__timer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timer"))

	@property
	def timerCycleMultiplier(self):
		"""
		This method is the property for **self.__timerCycleMultiplier** attribute.

		:return: self.__timerCycleMultiplier. ( Float )
		"""

		return self.__timerCycleMultiplier

	@timerCycleMultiplier.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self, value):
		"""
		This method is the setter method for **self.__timerCycleMultiplier** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timerCycleMultiplier"))

	@timerCycleMultiplier.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self):
		"""
		This method is the deleter method for **self.__timerCycleMultiplier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timerCycleMultiplier"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def run(self):
		"""
		This method starts the QThread.
		"""

		self.__timer = QTimer()
		self.__timer.moveToThread(self)
		self.__timer.start(Constants.defaultTimerCycle * self.__timerCycleMultiplier)

		self.__timer.timeout.connect(self.__updateIblSets, Qt.DirectConnection)

		self.exec_()

	@core.executionTrace
	def __updateIblSets(self):
		"""
		This method updates Database Ibl Sets if they have been modified on disk.
		"""

		needModelRefresh = False
		for iblSet in dbCommon.getIblSets(self.__dbSession):
			if not iblSet.path:
				continue

			if not os.path.exists(iblSet.path):
				continue

			storedStats = iblSet.osStats.split(",")
			osStats = os.stat(iblSet.path)
			if str(osStats[8]) != str(storedStats[8]):
				LOGGER.info("{0} | '{1}' Ibl Set file has been modified and will be updated!".format(self.__class__.__name__, iblSet.title))
				if dbCommon.updateIblSetContent(self.__dbSession, iblSet):
					LOGGER.info("{0} | '{1}' Ibl Set has been updated!".format(self.__class__.__name__, iblSet.title))
					needModelRefresh = True

		needModelRefresh and self.databaseChanged.emit()

class IblSetsModel(umbra.ui.models.GraphModel):
	"""
	This class defines the model used the by :class:`DatabaseBrowser` Component Interface class. 
	"""

	@core.executionTrace
	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders)

	@core.executionTrace
	def initializeModel(self, rootNode):
		"""
		This method initializes the model using given root node.
		
		:param rootNode: Graph root node. ( DefaultNode )
		return: Method success ( Boolean )
		"""

		self.beginResetModel()
		self.rootNode = rootNode
		self.endResetModel()
		return True

class Thumbnails_QListView(sibl_gui.ui.views.Abstract_QListView):
	"""
	This class is used to display Database Ibl Sets as thumbnails.
	"""

	@core.executionTrace
	def __init__(self, parent, model=None, readOnly=False):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param model: Model. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.views.Abstract_QListView.__init__(self, parent, model, readOnly)

		# --- Setting class attributes. ---
		self.__listViewSpacing = 24
		self.__listViewMargin = 32
		self.__listViewIconSize = 128

		Thumbnails_QListView.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def listViewSpacing(self):
		"""
		This method is the property for **self.__listViewSpacing** attribute.

		:return: self.__listViewSpacing. ( Integer )
		"""

		return self.__listViewSpacing

	@listViewSpacing.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def listViewSpacing(self, value):
		"""
		This method is the setter method for **self.__listViewSpacing** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("listViewSpacing", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("listViewSpacing", value)
		self.__listViewSpacing = value

	@listViewSpacing.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def listViewSpacing(self):
		"""
		This method is the deleter method for **self.__listViewSpacing** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "listViewSpacing"))

	@property
	def listViewMargin(self):
		"""
		This method is the property for **self.__listViewMargin** attribute.

		:return: self.__listViewMargin. ( Integer )
		"""

		return self.__listViewMargin

	@listViewMargin.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def listViewMargin(self, value):
		"""
		This method is the setter method for **self.__listViewMargin** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("listViewMargin", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("listViewMargin", value)
		self.__listViewMargin = value

	@listViewMargin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def listViewMargin(self):
		"""
		This method is the deleter method for **self.__listViewMargin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "listViewMargin"))

	@property
	def listViewIconSize(self):
		"""
		This method is the property for **self.__listViewIconSize** attribute.

		:return: self.__listViewIconSize. ( Integer )
		"""

		return self.__listViewIconSize

	@listViewIconSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def listViewIconSize(self, value):
		"""
		This method is the setter method for **self.__listViewIconSize** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("listViewIconSize", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("listViewIconSize", value)
		self.__listViewIconSize = value

	@listViewIconSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def listViewIconSize(self):
		"""
		This method is the deleter method for **self.__listViewIconSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "listViewIconSize"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.setAutoScroll(True)
		self.setResizeMode(QListView.Adjust)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setViewMode(QListView.IconMode)
		# Previous statement sets the dragDropMode to "QAbstractItemView.DragDrop".
		self.setDragDropMode(QAbstractItemView.DragOnly)

		self.__setDefaultUiState()

	@core.executionTrace
	def __setDefaultUiState(self):
		"""
		This method sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

		self.setIconSize(QSize(self.__listViewIconSize, self.__listViewIconSize))
		self.setGridSize(QSize(self.__listViewIconSize + self.__listViewSpacing, self.__listViewIconSize + self.__listViewMargin))

class Columns_QListView(sibl_gui.ui.views.Abstract_QListView):
	"""
	This class is used to display Database Ibl Sets columns.
	"""

	@core.executionTrace
	def __init__(self, parent, model=None, readOnly=False):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param model: Model. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.views.Abstract_QListView.__init__(self, parent, model, readOnly)

		Columns_QListView.__initializeUi(self)

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.setAutoScroll(True)
		self.setResizeMode(QListView.Adjust)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)

		self.__setDefaultUiState()

	@core.executionTrace
	def __setDefaultUiState(self):
		"""
		This method sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

class Details_QTreeView(QTreeView):
	"""
	This class is a `QTreeView <http://doc.qt.nokia.com/4.7/qtreeview.html>`_ subclass used to display Database Ibl Sets.
	"""

	@core.executionTrace
	def __init__(self, parent, model=None, readOnly=False):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param model: Model. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTreeView.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__readOnly = readOnly

		self.setModel(model)
		self.__modelSelection = []

		Details_QTreeView.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def readOnly(self):
		"""
		This method is the property for **self.__readOnly** attribute.

		:return: self.__readOnly. ( Boolean )
		"""

		return self.__readOnly

	@readOnly.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def readOnly(self, value):
		"""
		This method is the setter method for **self.__readOnly** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "readOnly"))

	@readOnly.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def readOnly(self):
		"""
		This method is the deleter method for **self.__readOnly** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "readOnly"))

	@property
	def modelSelection(self):
		"""
		This method is the property for **self.__modelSelection** attribute.

		:return: self.__modelSelection. ( Dictionary )
		"""

		return self.__modelSelection

	@modelSelection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self, value):
		"""
		This method is the setter method for **self.__modelSelection** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format("modelSelection", value)
		self.__modelSelection = value

	@modelSelection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self):
		"""
		This method is the deleter method for **self.__modelSelection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "modelSelection"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def setModel(self, model):
		"""
		This method reimplements the **QTreeView.setModel** method.
		
		:param model: Model to set. ( QObject )
		"""

		if not model:
			return

		QTreeView.setModel(self, model)

		# Signals / Slots.
		self.model().modelAboutToBeReset.connect(self.__model__modelAboutToBeReset)
		self.model().modelReset.connect(self.__model__modelReset)

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.__setDefaultUiState()

		# Signals / Slots.
		self.doubleClicked.connect(self.__QTreeView__doubleClicked)

	@core.executionTrace
	def __setDefaultUiState(self):
		"""
		This method sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

		self.expandAll()
		self.sortByColumn(0, Qt.AscendingOrder)

		if not self.model():
			return

		for column in range(len(self.model().horizontalHeaders)):
			self.resizeColumnToContents(column)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __QTreeView__doubleClicked(self, index):
		"""
		This method defines the behavior when the Widget is double clicked.

		:param index: Clicked Model item index. ( QModelIndex )
		"""

		if not self.readOnly:
			raise foundations.exceptions.UserError("{0} | Cannot perform action, View has been set read only!".format(self.__class__.__name__))

	@core.executionTrace
	def __model__modelAboutToBeReset(self):
		"""
		This method is triggered when the Model is about to be reset.
		"""

		self.storeModelSelection()

	@core.executionTrace
	def __model__modelReset(self):
		"""
		This method is triggered when the Model is changed.
		"""

		self.restoreModelSelection()
		self.__setDefaultUiState()

	@core.executionTrace
	def getSelectedNodes(self):
		"""
		This method returns the selected items.

		:return: View selected items. ( Dictionary )
		"""

		nodes = {}
		for index in self.selectedIndexes():
			node = self.model().getNode(index)
			if not node in nodes.keys():
				nodes[node] = []
			attribute = self.model().getAttribute(node, index.column())
			attribute and nodes[node].append(attribute)
		return nodes

	@core.executionTrace
	def storeModelSelection(self):
		"""
		This method stores the Model selection.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing Model selection!")

		self.__modelSelection = []
		for item in self.getSelectedNodes().keys():
			self.__modelSelection.append(item.id.value)
		return True

	@core.executionTrace
	def restoreModelSelection(self):
		"""
		This method restores the Model selection.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Restoring Model selection!")

		if not self.__modelSelection:
			return

		indexes = []
		for i in range(self.model().rowCount()):
			index = self.model().index(i)
			iblSetNode = self.model().getNode(index)
			iblSetNode.id.value in self.__modelSelection and indexes.append(index)

		if self.selectionModel():
			self.selectionModel().clear()
			for index in indexes:
				self.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select)
		return True

class DatabaseBrowser(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.core.databaseBrowser.databaseBrowser` Component Interface class.
	| It defines methods for Database Ibl Sets management.
	"""

	# Custom signals definitions.
	modelRefresh = pyqtSignal()

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(DatabaseBrowser, self).__init__(parent, name, *args, **kwargs)

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

		self.__editLayout = "editCentric"

		self.__factoryScriptEditor = None
		self.__coreDb = None
		self.__coreCollectionsOutliner = None

		self.__model = None
		self.__views = None
		self.__thumbnailsView = None
		self.__columnsView = None
		self.__detailsView = None
		self.__detailsHeaders = OrderedDict([("Ibl Set", "title"),
										("Author", "author"),
										("Shot Location", "location"),
										("Latitude", "latitude"),
										("Longitude", "longitude"),
										("Shot Date", "date"),
										("Shot Time", "time")])

		self.__databaseBrowserWorkerThread = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLargestSizeImage"))

	@uiLargestSizeImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLargestSizeImage(self):
		"""
		This method is the deleter method for **self.__uiLargestSizeImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiLargestSizeImage"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiSmallestSizeImage"))

	@uiSmallestSizeImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSmallestSizeImage(self):
		"""
		This method is the deleter method for **self.__uiSmallestSizeImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSmallestSizeImage"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self):
		"""
		This method is the deleter method for **self.__settingsSeparator** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSeparator"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "extension"))

	@extension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		This method is the deleter method for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "editLayout"))

	@editLayout.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editLayout(self):
		"""
		This method is the deleter method for **self.__editLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editLayout"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryScriptEditor"))

	@factoryScriptEditor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self):
		"""
		This method is the deleter method for **self.__factoryScriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryScriptEditor"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for **self.__coreDb** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDb"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This method is the deleter method for **self.__coreCollectionsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreCollectionsOutliner"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "views"))

	@views.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def views(self):
		"""
		This method is the deleter method for **self.__views** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "views"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "thumbnailsView"))

	@thumbnailsView.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def thumbnailsView(self):
		"""
		This method is the deleter method for **self.__thumbnailsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "columnsView"))

	@columnsView.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def columnsView(self):
		"""
		This method is the deleter method for **self.__columnsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "detailsView"))

	@detailsView.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def detailsView(self):
		"""
		This method is the deleter method for **self.__detailsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "detailsViewHeaders"))

	@detailsViewHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def detailsViewHeaders(self):
		"""
		This method is the deleter method for **self.__detailsViewHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseBrowserWorkerThread"))

	@databaseBrowserWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseBrowserWorkerThread(self):
		"""
		This method is the deleter method for **self.__databaseBrowserWorkerThread** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseBrowserWorkerThread"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResourcesDirectory)
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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__engine.parameters.databaseReadOnly and LOGGER.info("{0} | Model edition deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))
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

		self.Thumbnails_View_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiThumbnailsViewImage)))
		self.Columns_View_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiColumnsViewImage)))
		self.Details_View_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiDetailsViewImage)))

		self.Thumbnails_Size_horizontalSlider.setValue(self.__thumbnailsView.listViewIconSize)
		self.Largest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiLargestSizeImage)))
		self.Smallest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiSmallestSizeImage)))

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				self.__databaseBrowserWorkerThread = DatabaseBrowser_Worker(self)
				self.__databaseBrowserWorkerThread.start()
				self.__engine.workerThreads.append(self.__databaseBrowserWorkerThread)
			else:
				LOGGER.info("{0} | Ibl Sets continuous scanner deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Ibl Sets continuous scanner deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		# Signals / Slots.
		self.Thumbnails_View_pushButton.clicked.connect(functools.partial(self.__views_pushButtons__clicked, 0))
		self.Columns_View_pushButton.clicked.connect(functools.partial(self.__views_pushButtons__clicked, 1))
		self.Details_View_pushButton.clicked.connect(functools.partial(self.__views_pushButtons__clicked, 2))

		self.Thumbnails_Size_horizontalSlider.valueChanged.connect(self.__Thumbnails_Size_horizontalSlider__changed)
		self.__model.modelReset.connect(self.__coreCollectionsOutliner._CollectionsOutliner__view_setIblSetsCounts)
		self.modelRefresh.connect(self.__databaseBrowser__modelRefresh)

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				self.__databaseBrowserWorkerThread.databaseChanged.connect(self.__coreDb_database__changed)
			self.__model.dataChanged.connect(self.__model__dataChanged)
			self.__engine.contentDropped.connect(self.__application__contentDropped)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	@core.executionTrace
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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def onStartup(self):
		"""
		This method is called on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			# Wizard if sets table is empty.
			if not self.getIblSets():
				if messageBox.messageBox("Question", "Question", "The Database is empty, would you like to add some Ibl Sets?", buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
					directory = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self, "Add content:", RuntimeGlobals.lastBrowsedPath)))
					if directory:
						if not self.addDirectory(directory):
							raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(self.__class__.__name__, directory))

			# Ibl Sets table integrity checking.
			erroneousIblSets = dbCommon.checkIblSetsTableIntegrity(self.__coreDb.dbSession)
			if erroneousIblSets:
				for iblSet in erroneousIblSets:
					if erroneousIblSets[iblSet] == "INEXISTING_IBL_SET_FILE_EXCEPTION":
						if messageBox.messageBox("Question", "Error", "{0} | '{1}' Ibl Set file is missing, would you like to update it's location?".format(self.__class__.__name__, iblSet.title), QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
							self.updateIblSetLocation(iblSet)
					else:
						messageBox.messageBox("Warning", "Warning", "{0} | '{1}' {2}".format(self.__class__.__name__, iblSet.title, dbCommon.DB_EXCEPTIONS[erroneousIblSets[iblSet]]))
		else:
			LOGGER.info("{0} | Database Ibl Sets wizard and Ibl Sets integrity checking method deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeIblSetsIds = str(self.__settings.getKey(self.__settingsSection, "activeIblSets").toString())
		LOGGER.debug("> Stored '{0}' active Ibl Sets ids selection: '{1}'.".format(self.__class__.__name__, activeIblSetsIds))
		if activeIblSetsIds:
			if self.__settingsSeparator in activeIblSetsIds:
				ids = activeIblSetsIds.split(self.__settingsSeparator)
			else:
				ids = [activeIblSetsIds]
			self.__thumbnailsView.modelSelection = [int(id) for id in ids]

		self.__thumbnailsView.restoreModelSelection()
		return True

	@core.executionTrace
	def onClose(self):
		"""
		This method is called on Framework close.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		self.__thumbnailsView.storeModelSelection()
		self.__settings.setKey(self.__settingsSection, "activeIblSets", self.__settingsSeparator.join(str(id) for id in self.__thumbnailsView.modelSelection))
		return True

	@core.executionTrace
	def __views_addActions(self):
		"""
		This method sets the Views actions.
		"""

		if not self.__engine.parameters.databaseReadOnly:
			addContentAction = self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|Add Content ...", slot=self.__views_addContentAction__triggered) 
			addIblSetAction = self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|Add Ibl Set ...", slot=self.__views_addIblSetAction__triggered)
			removeIblSetsAction = self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|Remove Ibl Set(s) ...", slot=self.__views_removeIblSetsAction__triggered)
			updateIblSetsLocationsAction = self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|Update Ibl Set(s) Location(s) ...", slot=self.__views_updateIblSetsLocationsAction__triggered)
			separatorAction = QAction(self.__thumbnailsView)
			separatorAction.setSeparator(True)
			
			for view in self.__views:
				for action in (addContentAction, addIblSetAction, removeIblSetsAction, updateIblSetsLocationsAction):
					view.addAction(action)
		else:
			LOGGER.info("{0} | Ibl Sets Database alteration capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

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
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|Update Ibl Set(s) Location(s) ...'** action.

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

		self.Database_Browser_Thumbnails_Slider_frame.setVisible(not index)
		self.Database_Browser_stackedWidget.setCurrentIndex(index)

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
		This method is triggered when the Model datas need refresh.
		"""

		self.setIblSets()

	@core.executionTrace
	def __model__dataChanged(self, startIndex, endIndex):
		"""
		This method is triggered when the Model datas have changed.

		:param startIndex: Edited item starting QModelIndex. ( QModelIndex )
		:param endIndex: Edited item ending QModelIndex. ( QModelIndex )
		"""

		iblSetNode = self.__model.getNode(startIndex)
		iblSetNode.synchronizeDbItem()

		title = iblSetNode.name
		LOGGER.debug("> Updating Ibl Set '{0}' title to '{1}'.".format(iblSetNode.dbItem.title, iblSetNode.name))
		iblSetNode.dbItem.title = title

		dbCommon.commit(self.__coreDb.dbSession)
		self.modelRefresh.emit()

	@core.executionTrace
	def __coreDb_database__changed(self):
		"""
		This method is triggered by the **DatabaseBrowser_Worker** when the Database has changed.
		"""

		# Ensure that db objects modified by the worker thread will refresh properly.
		self.__coreDb.dbSession.expire_all()
		self.modelRefresh.emit()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	@umbra.engine.showProcessing("Retrieving Ibl Sets ...")
	def __application__contentDropped(self, event):
		"""
		This method is triggered when content is dropped in the Application.
		
		:param event: Event. ( QEvent )
		"""

		if not event.mimeData().hasUrls():
			return

		LOGGER.debug("> Drag event urls list: '{0}'!".format(event.mimeData().urls()))

		if not self.__engine.parameters.databaseReadOnly:
			for url in event.mimeData().urls():
				path = (platform.system() == "Windows" or platform.system() == "Microsoft") and re.search(r"^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
				if re.search(r"\.{0}$".format(self.__extension), str(url.path())):
					name = strings.getSplitextBasename(path)
					choice = messageBox.messageBox("Question", "Question", "'{0}' Ibl Set file has been dropped, would you like to 'Add' it to the Database or 'Edit' it in the Script Editor?".format(name), buttons=QMessageBox.Cancel, customButtons=((QString("Add"), QMessageBox.AcceptRole), (QString("Edit"), QMessageBox.AcceptRole)))
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

					if messageBox.messageBox("Question", "Question", "Would you like to add '{0}' directory Ibl Set(s) file(s) to the Database?".format(path), buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
						self.addDirectory(path)
				self.__engine.processEvents()
		else:
			raise foundations.exceptions.UserError("{0} | Cannot perform action, Database has been set read only!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.showProcessing("Adding Content ...")
	def addContent_ui(self):
		"""
		This method adds user defined content to the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		directory = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self, "Add content:", RuntimeGlobals.lastBrowsedPath)))
		if not directory:
			return

		LOGGER.debug("> Chosen directory path: '{0}'.".format(directory))
		if self.addDirectory(directory):
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(self.__class__.__name__, directory))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.showProcessing("Adding Ibl Set ...")
	def addIblSet_ui(self):
		"""
		This method adds an user defined Ibl Set to the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		path = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Add Ibl Set:", RuntimeGlobals.lastBrowsedPath, "Ibls files (*{0})".format(self.__extension))))
		if not path:
			return

		if not self.iblSetExists(path):
			LOGGER.debug("> Chosen Ibl Set path: '{0}'.".format(path))
			if self.addIblSet(strings.getSplitextBasename(path), path):
				return True
			else:
				raise Exception("{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, path))
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Ibl Set already exists in Database!".format(self.__class__.__name__, path))

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

		if messageBox.messageBox("Question", "Question", "Are you sure you want to remove '{0}' sets(s)?".format(", ".join((iblSet.title for iblSet in selectedIblSets))), buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
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
				raise Exception("{0} | Exception raised while removing '{1}' Ibls sets from the Database!".format(self.__class__.__name__, ", ". join((iblSet.title for iblSet in selectedIblSets))))

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
			file = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Updating '{0}' Ibl Set location:".format(iblSet.title), RuntimeGlobals.lastBrowsedPath, "Ibls files (*.{0})".format(self.__extension))))
			if file:
				success *= self.updateIblSetLocation(iblSet, file) or False
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.modelRefresh.emit()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while updating '{1}' Ibls sets locations!".format(self.__class__.__name__, ", ". join((iblSet.title for iblSet in selectedIblSets))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError, dbExceptions.DatabaseOperationError)
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
			if dbCommon.addIblSet(self.__coreDb.dbSession, name, path, collectionId or self.__coreCollectionsOutliner.getUniqueCollectionId()):
				emitSignal and self.modelRefresh.emit()
				return True
			else:
				raise dbExceptions.DatabaseOperationError("{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, name))
		else:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' Ibl Set already exists in Database!".format(self.__class__.__name__, name))

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

		self.__engine.startProcessing("Adding Directory Ibl Sets ...", len(osWalker.files.keys()))
		success = True
		for iblSet, path in osWalker.files.items():
			if not self.iblSetExists(path):
				success *= self.addIblSet(namespace.getNamespace(iblSet, rootOnly=True), path, collectionId or self.__coreCollectionsOutliner.getUniqueCollectionId(), emitSignal=False) or False
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.modelRefresh.emit()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(self.__class__.__name__, directory))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, dbExceptions.DatabaseOperationError)
	def removeIblSet(self, iblSet, emitSignal=True):
		"""
		This method removes provided Ibl Set from the Database.

		:param iblSet: Ibl Set to remove. ( DbIblSet )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Removing '{1}' Ibl Set from the Database!".format(self.__class__.__name__, iblSet.title))
		if dbCommon.removeIblSet(self.__coreDb.dbSession, iblSet.id):
			emitSignal and self.modelRefresh.emit()
			return True
		else:
			raise dbExceptions.DatabaseOperationError("{0} | Exception raised while removing '{1}' Ibl Set from the Database!".format(self.__class__.__name__, iblSet.title))

	@core.executionTrace
	def iblSetExists(self, path):
		"""
		This method returns if provided Ibl Set path exists in the Database.

		:param path: Collection path. ( String )
		:return: Collection exists. ( Boolean )
		"""

		return dbCommon.iblSetExists(self.__coreDb.dbSession, path)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, dbExceptions.DatabaseOperationError)
	def updateIblSetLocation(self, iblSet, file, emitSignal=True):
		"""
		This method updates provided Ibl Set location.

		:param iblSet: Ibl Set to update. ( DbIblSet )
		:param iblSet: New Ibl Set file. ( String )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Updating '{1}' Ibl Set with new location: '{2}'!".format(self.__class__.__name__, iblSet.title, file))
		if dbCommon.updateIblSetLocation(self.__coreDb.dbSession, iblSet, file):
			emitSignal and self.modelRefresh.emit()
			return True
		else:
			raise dbExceptions.DatabaseOperationError("{0} | Exception raised while updating '{1}' Ibl Set location!".format(self.__class__.__name__, iblSet.title))

	@core.executionTrace
	def getIblSets(self):
		"""
		This method returns Database Ibl Sets.

		:return: Database Ibl Sets. ( List )
		"""

		return [iblSet for iblSet in dbCommon.getIblSets(self.__coreDb.dbSession)]

	@core.executionTrace
	def setIblSets(self):
		"""
		This method sets Model Ibl Sets nodes.
		"""

		flags = self.__engine.parameters.databaseReadOnly and Qt.ItemIsSelectable | Qt.ItemIsEnabled or Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled
		iblSets = self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())
		rootNode = umbra.ui.models.DefaultNode(name="InvisibleRootNode")
		for iblSet in iblSets:
			iblSetNode = dbNodes.getIblSetNode(iblSet, parent=rootNode, flags=flags)
		self.__model.initializeModel(rootNode)

	@core.executionTrace
	def getSelectedNodes(self):
		"""
		This method returns the selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return self.__thumbnailsView.getSelectedNodes()

	@core.executionTrace
	def getSelectedIblSetsNodes(self):
		"""
		This method returns the selected Ibl Sets nodes.

		:return: View selected Ibl Sets nodes. ( List )
		"""

		return [item for item in self.getSelectedNodes().keys()]

	@core.executionTrace
	def getSelectedIblSets(self):
		"""
		This method returns the selected Ibl Sets.

		:return: View selected Ibl Sets. ( List )
		"""

		return [node.dbItem for node in self.getSelectedIblSetsNodes()]

