#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**databaseBrowser.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`DatabaseBrowser` Component Interface class, the :class:`DatabaseBrowser_QListView` class and the the :class:`DatabaseBrowser_Worker` worker thread class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import platform
import re
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
import sibl_gui.ui.common
import umbra.engine
import umbra.ui.common
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "DatabaseBrowser_Worker", "DatabaseBrowser_QListView", "DatabaseBrowser"]

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
		This method updates Database sets if they have been modified on disk.
		"""

		needModelRefresh = False
		for iblSet in dbCommon.getIblSets(self.__dbSession):
			if iblSet.path:
				if os.path.exists(iblSet.path):
					storedStats = iblSet.osStats.split(",")
					osStats = os.stat(iblSet.path)
					if str(osStats[8]) != str(storedStats[8]):
						LOGGER.info("{0} | '{1}' Ibl Set file has been modified and will be updated!".format(self.__class__.__name__, iblSet.title))
						if dbCommon.updateIblSetContent(self.__dbSession, iblSet):
							LOGGER.info("{0} | '{1}' Ibl Set has been updated!".format(self.__class__.__name__, iblSet.title))
							needModelRefresh = True

		needModelRefresh and self.databaseChanged.emit()

class IblSetsModel(QStandardItemModel):
	"""
	This class is a `QStandardItemModel <http://doc.qt.nokia.com/4.7/qstandarditemModel.html>`_ subclass used to store :mod:`umbra.components.core.databaseBrowser.databaseBrowser` Component Ibl Sets.
	"""

	aboutToChange = pyqtSignal()
	changed = pyqtSignal()

	@core.executionTrace
	def __init__(self, parent, iblSets=None, editable=True):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param iblSets: iblSets. ( List )
		:param editable: Model editable. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QStandardItemModel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__iblSets = []
		self.iblSets = iblSets
		self.__container = parent
		self.__editable = editable

		self.__modelSelection = None

		self.__toolTipText = """
								<p><b>{0}</b></p>
								<p><b>Author: </b>{1}<br>
								<b>Location: </b>{2}<br>
								<b>Shot Date: </b>{3}<br>
								<b>Comment: </b>{4}</p>
								"""

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
	def iblSets(self):
		"""
		This method is the property for **self.__iblSets** attribute.

		:return: self.__iblSets. ( List )
		"""

		return self.__iblSets

	@iblSets.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def iblSets(self, value):
		"""
		This method is the setter method for **self.__iblSets** attribute.

		:param value: Attribute value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("iblSets", value)
		self.__iblSets = value

	@iblSets.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def iblSets(self):
		"""
		This method is the deleter method for **self.__iblSets** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSets"))

	@property
	def editable(self):
		"""
		This method is the property for **self.__editable** attribute.

		:return: self.__editable. ( Boolean )
		"""

		return self.__editable

	@editable.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editable(self, value):
		"""
		This method is the setter method for **self.__editable** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "editable"))

	@editable.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editable(self):
		"""
		This method is the deleter method for **self.__editable** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editable"))

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

	@property
	def toolTipText(self):
		"""
		This method is the property for **self.__toolTipText** attribute.

		:return: self.__toolTipText. ( String )
		"""

		return self.__toolTipText

	@toolTipText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolTipText(self, value):
		"""
		This method is the setter method for **self.__toolTipText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "toolTipText"))

	@toolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolTipText(self):
		"""
		This method is the deleter method for **self.__toolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "toolTipText"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def setIblSets(self, iblSets):
		"""
		This method sets the provided Ibl Sets.
		
		:param iblSets: Ibl Sets. ( List )
		return: Method success ( Boolean )
		"""

		self.__iblSets = iblSets
		return self.setModel()

	@core.executionTrace
	def setModel(self):
		"""
		This method sets the Model using provided Ibl Sets.
		
		return: Method success ( Boolean )
		"""

		LOGGER.debug("> Setting up Model!")

		self.aboutToChange.emit()

		self.clear()

		for iblSet, title in sorted(((iblSet, iblSet.title) for iblSet in self.__iblSets), key=lambda x:(x[1])):

			LOGGER.debug("> Preparing '{0}' Ibl Set for Model.".format(iblSet.name))

			try:
				iblSetStandardItem = QStandardItem()
				iblSetStandardItem.setData(iblSet.title, Qt.DisplayRole)
				iblSetStandardItem.setToolTip(self.__toolTipText.format(iblSet.title, iblSet.author or Constants.nullObject, iblSet.location or Constants.nullObject, self.__container.getFormatedShotDate(iblSet.date, iblSet.time) or Constants.nullObject, iblSet.comment or Constants.nullObject))

				iblSetStandardItem.setIcon(sibl_gui.ui.common.getIcon(iblSet.icon))

				self.__editable or iblSetStandardItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

				iblSetStandardItem._datas = iblSet

				LOGGER.debug("> Adding '{0}' to Model.".format(iblSet.name))
				self.appendRow(iblSetStandardItem)

			except Exception as error:
				LOGGER.error("!>{0} | Exception raised while adding '{1}' Ibl Set to Model!".format(self.__class__.__name__, iblSet.name))
				foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "setModel"))

		self.changed.emit()

		return True

class DatabaseBrowser_QListView(QListView):
	"""
	This class is a `QListView <http://doc.qt.nokia.com/4.7/qlistview.html>`_ subclass used to display Database Ibl Sets.
	"""

	@core.executionTrace
	def __init__(self, parent, editable=True):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param editable: Model editable. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QListView.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__editable = editable

		self.__listViewSpacing = 24
		self.__listViewMargin = 32
		self.__listViewIconSize = 128

		DatabaseBrowser_QListView.__initializeUi(self)

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
	def editable(self):
		"""
		This method is the property for **self.__editable** attribute.

		:return: self.__editable. ( Boolean )
		"""

		return self.__editable

	@editable.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editable(self, value):
		"""
		This method is the setter method for **self.__editable** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "editable"))

	@editable.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editable(self):
		"""
		This method is the deleter method for **self.__editable** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editable"))

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
	def setModel(self, model):
		"""
		This method reimplements the **QListView.setModel** method.
		
		:param model: Model to set. ( QObject )
		"""

		QListView.setModel(self, model)

		# Signals / Slots.
		self.model().aboutToChange.connect(self.__model__aboutToChange)
		self.model().changed.connect(self.__model__changed)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __QStandardItem__doubleClicked(self, index):
		"""
		This method defines the behavior when a QStandardItem is double clicked.

		:param index: Clicked Model item index. ( QModelIndex )
		"""

		if not self.editable:
			raise foundations.exceptions.UserError("{0} | Cannot perform action, View has been set read only!".format(self.__class__.__name__))

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

		self.setDefaultViewState()

		# Signals / Slots.
		self.doubleClicked.connect(self.__QStandardItem__doubleClicked)

	@core.executionTrace
	def __model__aboutToChange(self):
		"""
		This method is triggered when the Model is about to change.
		"""

		self.storeModelSelection()

	@core.executionTrace
	def __model__changed(self):
		"""
		This method is triggered when the Model is changed.
		"""

		self.restoreModelSelection()
		self.setDefaultViewState()

	@core.executionTrace
	def setDefaultViewState(self):
		"""
		This method sets the default view state.
		"""

		LOGGER.debug("> Setting view item size to: {0}.".format(self.__listViewIconSize))

		self.setIconSize(QSize(self.__listViewIconSize, self.__listViewIconSize))
		self.setGridSize(QSize(self.__listViewIconSize + self.__listViewSpacing, self.__listViewIconSize + self.__listViewMargin))

	@core.executionTrace
	def storeModelSelection(self):
		"""
		This method stores Model selection.
		"""

		LOGGER.debug("> Storing Model selection!")

		self.model().modelSelection = []
		for item in (self.model().itemFromIndex(index)._datas for index in self.selectedIndexes()):
			self.model().modelSelection.append(item.id)

	@core.executionTrace
	def restoreModelSelection(self):
		"""
		This method restoresModel selection.
		"""

		LOGGER.debug("> Restoring Model selection!")

		indexes = []
		for i in range(self.model().rowCount()):
			iblSetStandardItem = self.model().item(i)
			iblSetStandardItem._datas.id in self.model().modelSelection and indexes.append(self.model().indexFromItem(iblSetStandardItem))

		selectionModel = self.selectionModel()
		if selectionModel:
			selectionModel.clear()
			for index in indexes:
				selectionModel.setCurrentIndex(index, QItemSelectionModel.Select)

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
		self._view = None

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
	def view(self):
		"""
		This method is the property for **self.__view** attribute.

		:return: self.__view. ( QObject )
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		This method is the setter method for **self.__view** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		This method is the deleter method for **self.__view** attribute.
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

		self.__engine.parameters.databaseReadOnly and LOGGER.info("{0} | Database_Browser_listView Model edition deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))
		self.__model = IblSetsModel(self, self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections()), not self.__engine.parameters.databaseReadOnly)
		self.__model.setModel()

		self.Database_Browser_listView = DatabaseBrowser_QListView(self, not self.__engine.parameters.databaseReadOnly)
		self.Database_Browser_Widget_gridLayout.addWidget(self.Database_Browser_listView, 0, 0)
		self.__view = self.Database_Browser_listView
		listViewIconSize = self.__settings.getKey(self.__settingsSection, "listViewIconSize")
		self.__listViewIconSize = listViewIconSize.toInt()[1] and listViewIconSize.toInt()[0] or self.__listViewIconSize
		self.Database_Browser_listView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Database_Browser_listView_addActions()
		self.Database_Browser_listView.setModel(self.__model)

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				self.__databaseBrowserWorkerThread = DatabaseBrowser_Worker(self)
				self.__databaseBrowserWorkerThread.start()
				self.__engine.workerThreads.append(self.__databaseBrowserWorkerThread)
			else:
				LOGGER.info("{0} | Ibl Sets continuous scanner deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Ibl Sets continuous scanner deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		self.Thumbnails_Size_horizontalSlider.setValue(self.__listViewIconSize)
		self.Largest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiLargestSizeImage)))
		self.Smallest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiSmallestSizeImage)))

		# Signals / Slots.
		self.Thumbnails_Size_horizontalSlider.valueChanged.connect(self.__Thumbnails_Size_horizontalSlider__changed)
		self.__model.changed.connect(self.__coreCollectionsOutliner.modelPartialRefresh.emit)
		self.modelRefresh.connect(self.setIblSets)

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
			self.__model.modelSelection = [int(id) for id in ids]

		self.__view.restoreModelSelection()
		return True

	@core.executionTrace
	def onClose(self):
		"""
		This method is called on Framework close.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		self.__view.storeModelSelection()
		self.__settings.setKey(self.__settingsSection, "activeIblSets", self.__settingsSeparator.join(str(id) for id in self.__model.modelSelection))
		return True

	@core.executionTrace
	def __Database_Browser_listView_addActions(self):
		"""
		This method sets the Database Browser actions.
		"""

		if not self.__engine.parameters.databaseReadOnly:
			self.Database_Browser_listView.addAction(self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|Add Content ...", slot=self.__Database_Browser_listView_addContentAction__triggered))
			self.Database_Browser_listView.addAction(self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|Add Ibl Set ...", slot=self.__Database_Browser_listView_addIblSetAction__triggered))
			self.Database_Browser_listView.addAction(self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|Remove Ibl Set(s) ...", slot=self.__Database_Browser_listView_removeIblSetsAction__triggered))
			self.Database_Browser_listView.addAction(self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|Update Ibl Set(s) Location(s) ...", slot=self.__Database_Browser_listView_updateIblSetsLocationsAction__triggered))

			separatorAction = QAction(self.Database_Browser_listView)
			separatorAction.setSeparator(True)
			self.Database_Browser_listView.addAction(separatorAction)
		else:
			LOGGER.info("{0} | Ibl Sets Database alteration capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __Database_Browser_listView_addContentAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|Add Content ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addContent_ui()

	@core.executionTrace
	def __Database_Browser_listView_addIblSetAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|Add Ibl Set ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addIblSet_ui()

	@core.executionTrace
	def __Database_Browser_listView_removeIblSetsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|Remove Ibl Set(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.removeIblSets_ui()

	@core.executionTrace
	def __Database_Browser_listView_updateIblSetsLocationsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|Update Ibl Set(s) Location(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.updateIblSetsLocation_ui()

	@core.executionTrace
	def __Thumbnails_Size_horizontalSlider__changed(self, value):
		"""
		This method scales the **Database_Browser_listView** icons.

		:param value: Thumbnails size. ( Integer )
		"""

		self.Database_Browser_listView.listViewIconSize = value

		self.Database_Browser_listView.setDefaultViewState()

		# Storing settings key.
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("listViewIconSize", value))
		self.__settings.setKey(self.__settingsSection, "listViewIconSize", value)

	@core.executionTrace
	def __model__dataChanged(self, startIndex, endIndex):
		"""
		This method defines the behavior when the Model datas changed.

		:param startIndex: Edited item starting QModelIndex. ( QModelIndex )
		:param endIndex: Edited item ending QModelIndex. ( QModelIndex )
		"""

		standardItem = self.__model.itemFromIndex(startIndex)
		currentTitle = standardItem.text()

		LOGGER.debug("> Updating Ibl Set '{0}' title to '{1}'.".format(standardItem._datas.title, currentTitle))
		iblSet = dbCommon.filterIblSets(self.__coreDb.dbSession, "^{0}$".format(standardItem._datas.id), "id")[0]
		iblSet.title = str(currentTitle)
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

		if messageBox.messageBox("Question", "Question", "Are you sure you want to remove '{0}' sets(s)?".format(", ".join((str(iblSet.title) for iblSet in selectedIblSets))), buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
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
	def setIblSets(self):
		"""
		This method sets Model Ibl Sets.
		"""

		self.__model.setIblSets(self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections()))

	@core.executionTrace
	def getIblSets(self):
		"""
		This method returns Database Ibl Sets.

		:return: Database Ibl Sets Collections. ( List )
		"""

		return [iblSet for iblSet in dbCommon.getIblSets(self.__coreDb.dbSession)]

	@core.executionTrace
	def getSelectedItems(self):
		"""
		This method returns **Database_Browser_listView** selected items.

		:return: View selected items. ( List )
		"""

		return [self.__model.itemFromIndex(index) for index in self.Database_Browser_listView.selectedIndexes()]

	@core.executionTrace
	def getSelectedIblSets(self):
		"""
		This method returns selected Ibl Sets.

		:return: View selected Ibl Sets. ( List )
		"""

		return [item._datas for item in self.getSelectedItems()]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getFormatedShotDate(self, date, time):
		"""
		This method returns a formated shot date.

		:param date: sIBL set date key value. ( String )
		:param time: sIBL set time key value. ( String )
		:return: Current shot date. ( String )
		"""

		LOGGER.debug("> Formating shot date with '{0}' date and '{1}' time.".format(date, time))

		if date and time and date != Constants.nullObject and time != Constants.nullObject:
			shotTime = "{0}H{1}".format(*time.split(":"))
			shotDate = date.replace(":", "/")[2:] + " - " + shotTime

			LOGGER.debug("> Formated shot date: '{0}'.".format(shotDate))
			return shotDate
		else:
			return Constants.nullObject
