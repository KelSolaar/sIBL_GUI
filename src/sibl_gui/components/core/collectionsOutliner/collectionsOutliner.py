#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**collectionsOutliner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`CollectionsOutliner` Component Interface class and the :class:`CollectionsOutliner_QTreeView` class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import sibl_gui.components.core.db.exceptions as dbExceptions
import sibl_gui.components.core.db.utilities.common as dbCommon
import sibl_gui.components.core.db.utilities.types as dbTypes
import umbra.engine
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "CollectionsModel", "CollectionsOutliner_QTreeView", "CollectionsOutliner"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Collections_Outliner.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class CollectionsModel(QStandardItemModel):
	"""
	This class is a `QStandardItemModel <http://doc.qt.nokia.com/4.7/qstandarditemModel.html>`_ subclass used to store :mod:`umbra.components.core.collectionsOutliner.CollectionsOutliner` Component Collections.
	"""

	aboutToChange = pyqtSignal()
	changed = pyqtSignal()

	@core.executionTrace
	def __init__(self, parent, collections=None, editable=True):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param collections: Collections. ( List )
		:param editable: Model editable. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QStandardItemModel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__collections = []
		self.__editable = editable

		self.__uiResourcesDirectory = "resources"
		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResourcesDirectory)
		self.__uiDefaultCollectionImage = "Default_Collection.png"
		self.__uiUserCollectionImage = "User_Collection.png"

		self.__overallCollection = "Overall"
		self.__defaultCollection = "Default"
		self.__setsCountLabel = "Sets"
		self.__headers = ["Collections", self.__setsCountLabel, "Comment"]

		self.__coreDb = self.__container.engine.componentsManager.components["core.db"].interface

		collections and self.setCollections(collections)

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
	def collections(self):
		"""
		This method is the property for **self.__collections** attribute.

		:return: self.__collections. ( List )
		"""

		return self.__collections

	@collections.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def collections(self, value):
		"""
		This method is the setter method for **self.__collections** attribute.

		:param value: Attribute value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("collections", value)
		self.__collections = value

	@collections.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def collections(self):
		"""
		This method is the deleter method for **self.__collections** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "collections"))

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
	def uiDefaultCollectionImage(self):
		"""
		This method is the property for **self.__uiDefaultCollectionImage** attribute.

		:return: self.__uiDefaultCollectionImage. ( String )
		"""

		return self.__uiDefaultCollectionImage

	@uiDefaultCollectionImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self, value):
		"""
		This method is the setter method for **self.__uiDefaultCollectionImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiDefaultCollectionImage"))

	@uiDefaultCollectionImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self):
		"""
		This method is the deleter method for **self.__uiDefaultCollectionImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiDefaultCollectionImage"))

	@property
	def uiUserCollectionImage(self):
		"""
		This method is the property for **self.__uiUserCollectionImage** attribute.

		:return: self.__uiUserCollectionImage. ( String )
		"""

		return self.__uiUserCollectionImage

	@uiUserCollectionImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self, value):
		"""
		This method is the setter method for **self.__uiUserCollectionImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiUserCollectionImage"))

	@uiUserCollectionImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self):
		"""
		This method is the deleter method for **self.__uiUserCollectionImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiUserCollectionImage"))

	@property
	def overallCollection(self):
		"""
		This method is the property for **self.__overallCollection** attribute.

		:return: self.__overallCollection. ( String )
		"""

		return self.__overallCollection

	@overallCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overallCollection(self, value):
		"""
		This method is the setter method for **self.__overallCollection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "overallCollection"))

	@overallCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overallCollection(self):
		"""
		This method is the deleter method for **self.__overallCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "overallCollection"))

	@property
	def defaultCollection(self):
		"""
		This method is the property for **self.__defaultCollection** attribute.

		:return: self.__defaultCollection. ( String )
		"""

		return self.__defaultCollection

	@defaultCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollection(self, value):
		"""
		This method is the setter method for **self.__defaultCollection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultCollection"))

	@defaultCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollection(self):
		"""
		This method is the deleter method for **self.__defaultCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultCollection"))

	@property
	def setsCountLabel(self):
		"""
		This method is the property for **self.__setsCountLabel** attribute.

		:return: self.__setsCountLabel. ( String )
		"""

		return self.__setsCountLabel

	@setsCountLabel.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setsCountLabel(self, value):
		"""
		This method is the setter method for **self.__setsCountLabel** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "setsCountLabel"))

	@setsCountLabel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setsCountLabel(self):
		"""
		This method is the deleter method for **self.__setsCountLabel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "setsCountLabel"))

	@property
	def headers(self):
		"""
		This method is the property for **self.__headers** attribute.

		:return: self.__headers. ( List )
		"""

		return self.__headers

	@headers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		This method is the setter method for **self.__headers** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

	@headers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def headers(self):
		"""
		This method is the deleter method for **self.__headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

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

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeModel(self):
		"""
		This method initializes the Model using :obj:`CollectionsModel.collections` class property.
		"""

		LOGGER.debug("> Setting up Model!")

		self.aboutToChange.emit()

		self.clear()

		self.setHorizontalHeaderLabels(self.__headers)
		self.setColumnCount(len(self.__headers))
		readOnlyFlags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

		rootItem = self.invisibleRootItem()

		LOGGER.debug("> Preparing '{0}' Collection for Model.".format(self.__overallCollection))

		overallCollectionStandardItem = QStandardItem(QString(self.__overallCollection))
		overallCollectionStandardItem.setFlags(readOnlyFlags)

		overallCollectionSetsCountStandardItem = QStandardItem(QString(str(dbCommon.getIblSets(self.__coreDb.dbSession).count())))
		overallCollectionSetsCountStandardItem.setTextAlignment(Qt.AlignCenter)
		overallCollectionSetsCountStandardItem.setFlags(readOnlyFlags)

		overallCollectionCommentsStandardItem = QStandardItem()
		overallCollectionCommentsStandardItem.setFlags(readOnlyFlags)

		overallCollectionStandardItem._type = "Overall"

		LOGGER.debug("> Adding '{0}' Collection to Model.".format(self.__overallCollection))
		rootItem.appendRow([overallCollectionStandardItem, overallCollectionSetsCountStandardItem, overallCollectionCommentsStandardItem])

		if self.__collections:
			for collection in self.__collections:
				LOGGER.debug("> Preparing '{0}' Collection for Model.".format(collection.name))

				try:
					collectionStandardItem = QStandardItem(QString(collection.name))
					iconPath = collection.name == self.__defaultCollection and os.path.join(self.__uiResourcesDirectory, self.__uiDefaultCollectionImage) or os.path.join(self.__uiResourcesDirectory, self.__uiUserCollectionImage)
					collectionStandardItem.setIcon(QIcon(iconPath))
					if collection.name == self.__defaultCollection or not self.__editable:
						collectionStandardItem.setFlags(readOnlyFlags)

					collectionSetsCountStandardItem = QStandardItem(QString(str(self.__coreDb.dbSession.query(dbTypes.DbIblSet).filter_by(collection=collection.id).count())))
					collectionSetsCountStandardItem.setTextAlignment(Qt.AlignCenter)

					collectionCommentsStandardItem = QStandardItem(QString(collection.comment))
					if collection.name == self.__defaultCollection or not self.__editable:
						collectionCommentsStandardItem.setFlags(readOnlyFlags)

					collectionStandardItem._datas = collection
					collectionStandardItem._type = "Collection"

					LOGGER.debug("> Adding '{0}' Collection to Model.".format(collection.name))
					overallCollectionStandardItem.appendRow([collectionStandardItem, collectionSetsCountStandardItem, collectionCommentsStandardItem])

				except Exception as error:
					LOGGER.error("!>{0} | Exception raised while adding '{1}' Collection to Model!".format(self.__class__.__name__, collection.name))
					foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "__initializeModel"))
		else:
			LOGGER.info("{0} | Database has no user defined Collections!".format(self.__class__.__name__))

		self.changed.emit()

	@core.executionTrace
	def setCollections(self, collections):
		"""
		This method sets the provided Collections.
		
		:param collections: Collections. ( List )
		return: Method success ( Boolean )
		"""

		self.__collections = collections
		self.__initializeModel()
		return True

class CollectionsOutliner_QTreeView(QTreeView):
	"""
	| This class is a `QTreeView <http://doc.qt.nokia.com/4.7/qtreeview.html>`_ subclass used to display Database Collections.
	| It provides support for drag'n'drop by reimplementing relevant methods.
	"""

	@core.executionTrace
	def __init__(self, parent, model=None, editable=True):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param model: Model. ( QObject )
		:param editable: Model editable. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTreeView.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__editable = editable

		self.__coreDb = self.__container.engine.componentsManager.components["core.db"].interface
		self.__coreDatabaseBrowser = self.__container.engine.componentsManager.components["core.databaseBrowser"].interface
		self.__coreCollectionsOutliner = self.__container.engine.componentsManager.components["core.collectionsOutliner"].interface

		self.__previousCollection = None
		self.__treeViewIndentation = 15

		self.setModel(model)
		self.__modelSelection = {"Overall" : [], "Collections" : []}

		CollectionsOutliner_QTreeView.__initializeUi(self)

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
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDatabaseBrowser"))

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
	def previousCollection(self):
		"""
		This method is the property for **self.__previousCollection** attribute.

		:return: self.__previousCollection. ( String )
		"""

		return self.__previousCollection

	@previousCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previousCollection(self, value):
		"""
		This method is the setter method for **self.__previousCollection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "previousCollection"))

	@previousCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previousCollection(self):
		"""
		This method is the deleter method for **self.__previousCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "previousCollection"))

	@property
	def treeViewIndentation(self):
		"""
		This method is the property for **self.__treeViewIndentation** attribute.

		:return: self.__treeViewIndentation. ( Integer )
		"""

		return self.__treeViewIndentation

	@treeViewIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self, value):
		"""
		This method is the setter method for **self.__treeViewIndentation** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "treeViewIndentation"))

	@treeViewIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self):
		"""
		This method is the deleter method for **self.__treeViewIndentation** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "treeViewIndentation"))

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
	def dragEnterEvent(self, event):
		"""
		This method defines the drag enter event behavior.

		:param event: QEvent. ( QEvent )
		"""

		if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
			LOGGER.debug("> '{0}' drag event type accepted!".format("application/x-qabstractitemmodeldatalist"))
			event.accept()
		else:
			event.ignore()

	@core.executionTrace
	def dragMoveEvent(self, event):
		"""
		This method defines the drag move event behavior.

		:param event: QEvent. ( QEvent )
		"""

		pass

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.DirectoryExistsError, foundations.exceptions.UserError)
	def dropEvent(self, event):
		"""
		This method defines the drop event behavior.

		:param event: QEvent. ( QEvent )
		"""

		if self.__editable:
			indexAt = self.indexAt(event.pos())
			itemAt = self.model().itemFromIndex(indexAt)

			if not itemAt:
				return

			LOGGER.debug("> Item at drop position: '{0}'.".format(itemAt))
			collectionStandardItem = self.model().itemFromIndex(self.model().sibling(indexAt.row(), 0, indexAt))
			if collectionStandardItem.text() != self.model().overallCollection:
				collection = collectionStandardItem._datas
				for iblSet in self.__coreDatabaseBrowser.getSelectedIblSets():
					LOGGER.info("> Moving '{0}' Ibl Set to '{1}' Collection.".format(iblSet.title, collection.name))
					iblSet.collection = collection.id
				if dbCommon.commit(self.__coreDb.dbSession):
					self.selectionModel().setCurrentIndex(indexAt, QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
		else:
			raise foundations.exceptions.UserError("{0} | Cannot perform action, View has been set read only!".format(self.__class__.__name__))

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
		self.model().aboutToChange.connect(self.__model__aboutToChange)
		self.model().changed.connect(self.__model__changed)

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.setAutoScroll(False)
		self.setDragDropMode(QAbstractItemView.DropOnly)
		self.setIndentation(self.__treeViewIndentation)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setSortingEnabled(True)

		self.__setDefaultUiState()

		# Signals / Slots.
		self.clicked.connect(self.__QTreeView__clicked)
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

		for column in range(len(self.model().headers)):
			self.resizeColumnToContents(column)

	@core.executionTrace
	def __QTreeView__clicked(self, index):
		"""
		This method defines the behavior when the Widget is clicked.

		:param index: Clicked Model item index. ( QModelIndex )
		"""

		self.__previousCollection = self.model().itemFromIndex(self.model().sibling(index.row(), 0, index)).text()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __QTreeView__doubleClicked(self, index):
		"""
		This method defines the behavior when the Widget is double clicked.

		:param index: Clicked Model item index. ( QModelIndex )
		"""

		if self.__editable:
			collectionStandardItem = self.model().itemFromIndex(self.model().sibling(index.row(), 0, index))

			if collectionStandardItem.text() != self.model().defaultCollection and collectionStandardItem.text() != self.model().overallCollection:
				if self.model().itemFromIndex(index).column() == self.model().headers.index(self.model().setsCountLabel):
					messageBox.messageBox("Warning", "Warning", "{0} | 'Ibl Sets Counts' column is read only!".format(self.__class__.__name__))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' and '{2}' Collections attributes are read only!".format(self.__class__.__name__, self.model().overallCollection, self.model().defaultCollection))
		else:
			raise foundations.exceptions.UserError("{0} | Cannot perform action, View has been set read only!".format(self.__class__.__name__))

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
		self.__setDefaultUiState()

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This method returns the selected items.

		:param rowsRootOnly: Return rows roots only. ( Boolean )
		:return: View selected items. ( List )
		"""

		return rowsRootOnly and [item for item in set([self.model().itemFromIndex(self.model().sibling(index.row(), 0, index)) for index in self.selectedIndexes()])] or [self.model().itemFromIndex(index) for index in self.selectedIndexes()]

	@core.executionTrace
	def storeModelSelection(self):
		"""
		This method stores the Model selection.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing Model selection!")

		for item in self.getSelectedItems():
			if item._type == self.model().overallCollection:
				self.__modelSelection["Overall"].append(item.text())
			elif item._type == "Collection":
				self.__modelSelection["Collections"].append(item._datas.id)
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
			overallCollectionStandardItem = self.model().item(i)
			overallCollectionStandardItem.text() in self.__modelSelection["Overall"] and indexes.append(self.model().indexFromItem(overallCollectionStandardItem))
			for j in range(overallCollectionStandardItem.rowCount()):
				collectionStandardItem = overallCollectionStandardItem.child(j, 0)
				collectionStandardItem._datas.id in self.__modelSelection["Collections"] and indexes.append(self.model().indexFromItem(collectionStandardItem))

		if self.selectionModel():
			self.selectionModel().clear()
			for index in indexes:
				self.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
		return True

class CollectionsOutliner(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.core.collectionsOutliner.collectionsOutliner` Component Interface class.
	| It defines methods for Database Collections management.
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

		super(CollectionsOutliner, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiResourcesDirectory = "resources"
		self.__dockArea = 1

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None
		self.__settingsSeparator = ","

		self.__coreDb = None
		self.__coreDatabaseBrowser = None

		self.__model = None
		self.__view = None

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
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDatabaseBrowser"))

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

		:return: self.__view. ( QWidget )
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		This method is the setter method for **self.__view** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		This method is the deleter method for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

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

		self.__coreDb = self.__engine.componentsManager.components["core.db"].interface
		self.__coreDatabaseBrowser = self.__engine.componentsManager.components["core.databaseBrowser"].interface

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
		self.__model = CollectionsModel(self, self.getCollections(), not self.__engine.parameters.databaseReadOnly)

		self.Collections_Outliner_treeView = CollectionsOutliner_QTreeView(self, self.__model, not self.__engine.parameters.databaseReadOnly)
		self.Collections_Outliner_dockWidgetContents_gridLayout.addWidget(self.Collections_Outliner_treeView, 0, 0)
		self.__view = self.Collections_Outliner_treeView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__view_addActions()

		# Signals / Slots.
		self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.modelRefresh.connect(self.__collectionsOutliner__modelRefresh)
		not self.__engine.parameters.databaseReadOnly and self.__model.dataChanged.connect(self.__model__dataChanged)

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

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	def onStartup(self):
		"""
		This method is called on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			not self.getCollections() and self.addCollection(self.__model.defaultCollection, "Default Collection")
		else:
			LOGGER.info("{0} | Database default Collection wizard deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeCollectionsIds = str(self.__settings.getKey(self.__settingsSection, "activeCollections").toString())
		LOGGER.debug("> Stored '{0}' active Collections ids selection: '{1}'.".format(self.__class__.__name__, activeCollectionsIds))
		if activeCollectionsIds:
			if self.__settingsSeparator in activeCollectionsIds:
				ids = activeCollectionsIds.split(self.__settingsSeparator)
			else:
				ids = [activeCollectionsIds]
			self.__view.modelSelection["Collections"] = [int(id) for id in ids]

		activeOverallCollection = str(self.__settings.getKey(self.__settingsSection, "activeOverallCollection").toString())
		LOGGER.debug("> Stored '{0}' active overall Collection selection: '{1}'.".format(self.__class__.__name__, activeOverallCollection))
		if activeOverallCollection:
			self.__view.modelSelection[self.__model.overallCollection] = [activeOverallCollection]

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
		self.__settings.setKey(self.__settingsSection, "activeCollections", self.__settingsSeparator.join((str(id) for id in self.__view.modelSelection["Collections"])))
		self.__settings.setKey(self.__settingsSection, "activeOverallCollection", self.__settingsSeparator.join((str(id) for id in self.__view.modelSelection[self.__model.overallCollection])))
		return True

	@core.executionTrace
	def __view_addActions(self):
		"""
		This method sets the View actions.
		"""

		if not self.__engine.parameters.databaseReadOnly:
			self.__view.addAction(self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.collectionsOutliner|Add Content ...", slot=self.__view_addContentAction__triggered))
			self.__view.addAction(self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.collectionsOutliner|Add Collection ...", slot=self.__view_addCollectionAction__triggered))
			self.__view.addAction(self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.collectionsOutliner|Remove Collection(s) ...", slot=self.__view_removeCollectionsAction__triggered))
		else:
			LOGGER.info("{0} | Collections Database alteration capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __view_addContentAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.collectionsOutliner|Add Content ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addContent_ui()

	@core.executionTrace
	def __view_addCollectionAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.collectionsOutliner|Add Collection ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addCollection_ui()

	@core.executionTrace
	def __view_removeCollectionsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.collectionsOutliner|Remove Collection(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.removeCollections_ui()

	@core.executionTrace
	def __view_setIblSetsCounts(self):
		"""
		This method sets the View Ibl Sets counts.
		"""

		# Disconnecting Model "dataChanged()" signal.
		not self.__engine.parameters.databaseReadOnly and self.__model.dataChanged.disconnect(self.__model__dataChanged)

		for i in range(self.__model.rowCount()):
			currentStandardItem = self.__model.item(i)
			if currentStandardItem.text() == self.__model.overallCollection:
				self.__model.itemFromIndex(self.__model.sibling(i, 1, self.__model.indexFromItem(currentStandardItem))).setText(str(dbCommon.getIblSets(self.__coreDb.dbSession).count()))
			for j in range(currentStandardItem.rowCount()):
				collectionStandardItem = currentStandardItem.child(j, 0)
				collectionSetsCountStandardItem = currentStandardItem.child(j, 1)
				collectionSetsCountStandardItem.setText(str(self.__coreDb.dbSession.query(dbTypes.DbIblSet).filter_by(collection=collectionStandardItem._datas.id).count()))

		# Reconnecting Model "dataChanged()" signal.
		not self.__engine.parameters.databaseReadOnly and self.__model.dataChanged.connect(self.__model__dataChanged)

	@core.executionTrace
	def __collectionsOutliner__modelRefresh(self):
		"""
		This method is triggered when the Model datas need refresh.
		"""

		self.setCollections()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __model__dataChanged(self, startIndex, endIndex):
		"""
		This method is triggered when the Model datas have changed.
		
		:param startIndex: Edited item starting QModelIndex. ( QModelIndex )
		:param endIndex: Edited item ending QModelIndex. ( QModelIndex )
		"""

		standardItem = self.__model.itemFromIndex(startIndex)
		currentText = standardItem.text()

		if currentText:
			collectionStandardItem = self.__model.itemFromIndex(self.__model.sibling(startIndex.row(), 0, startIndex))
			id = collectionStandardItem._type == "Collection" and collectionStandardItem._datas.id or None
			collections = [collection for collection in self.getCollections()]
			if not id and not collections:
				return

			if startIndex.column() == 0:
				if currentText not in (collection.name for collection in collections):
					LOGGER.debug("> Updating Collection '{0}' name to '{1}'.".format(id, currentText))
					collection = dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(id), "id")[0]
					collection.name = str(currentText)
					dbCommon.commit(self.__coreDb.dbSession)
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Collection name already exists in Database!".format(self.__class__.__name__, currentText))
			elif startIndex.column() == 2:
				LOGGER.debug("> Updating Collection '{0}' comment to '{1}'.".format(id, currentText))
				collection = dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(id), "id")[0]
				collection.comment = str(currentText)
				dbCommon.commit(self.__coreDb.dbSession)
		else:
			raise foundations.exceptions.UserError("{0} | Exception while editing a Collection field: Cannot use an empty value!".format(self.__class__.__name__))
		self.modelRefresh.emit()

	@core.executionTrace
	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when the View **selectionModel** has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		self.__coreDatabaseBrowser.modelRefresh.emit()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.showProcessing("Adding Content ...")
	def addContent_ui(self):
		"""
		This method adds user defined content to the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		collection = self.addCollection_ui()
		if not collection:
			return

		directory = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self, "Add content:", RuntimeGlobals.lastBrowsedPath)))
		if not directory:
			return

		LOGGER.debug("> Chosen directory path: '{0}'.".format(directory))
		if self.__coreDatabaseBrowser.addDirectory(directory, self.getCollectionId(collection)):
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(self.__class__.__name__, directory))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError, Exception)
	@umbra.engine.showProcessing("Adding Collection ...")
	def addCollection_ui(self):
		"""
		This method adds an user defined Collection to the Database.

		:return: Collection name. ( String )

		:note: This method may require user interaction.
		"""

		collectionInformations, state = QInputDialog.getText(self, "Add Collection", "Enter your Collection name!")
		if not state:
			return

		if collectionInformations:
			collectionInformations = str(collectionInformations).split(",")
			name = collectionInformations[0].strip()
			if name != self.__model.overallCollection:
				if not self.collectionExists(name):
					comment = len(collectionInformations) == 1 and "Double click to set a comment!" or collectionInformations[1].strip()
					if self.addCollection(name, comment):
						self.__view.selectionModel().setCurrentIndex(self.__model.indexFromItem(self.__model.findItems(name, Qt.MatchExactly | Qt.MatchRecursive, 0)[0]), QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
						return name
					else:
						raise Exception("{0} | Exception raised while adding '{1}' Collection to the Database!".format(self.__class__.__name__, name))
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Collection already exists in Database!".format(self.__class__.__name__, name))
			else:
				raise foundations.exceptions.UserError("{0} | Exception while adding a Collection to the Database: Cannot use '{1}' as Collection name!".format(self.__class__.__name__, self.__model.overallCollection))
		else:
			raise foundations.exceptions.UserError("{0} | Exception while adding a Collection to the Database: Cannot use an empty name!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.encapsulateProcessing
	def removeCollections_ui(self):
		"""
		This method removes user selected Collections from the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedItems = self.getSelectedItems()
		if self.__overallCollection in (str(collection.text()) for collection in selectedItems) or self.__model.defaultCollection in (str(collection.text()) for collection in selectedItems):
			messageBox.messageBox("Warning", "Warning", "{0} | Cannot remove '{1}' or '{2}' Collection!".format(self.__class__.__name__, self.__model.overallCollection, self.__model.defaultCollection))

		selectedCollections = [collection for collection in self.getSelectedCollections() if collection.name != self.__model.defaultCollection]
		if not selectedCollections:
			return

		if messageBox.messageBox("Question", "Question", "Are you sure you want to remove '{0}' Collection(s)?".format(", ".join((str(collection.name) for collection in selectedCollections))), buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.startProcessing("Removing Collections ...", len(selectedCollections))
			success = True
			for collection in selectedCollections:
				success *= self.removeCollection(collection) or False
				self.__engine.stepProcessing()
			self.__engine.stopProcessing()
			self.__view.selectionModel().setCurrentIndex(self.__model.index(0, 0), QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
			if success:
				return True
			else:
				raise Exception("{0} | Exception raised while removing '{1}' Collections from the Database!".format(self.__class__.__name__, ", ". join((collection.name for collection in selectedCollections))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError, dbExceptions.DatabaseOperationError)
	def addCollection(self, name, comment="Double click to set a comment!"):
		"""
		This method adds a Collection to the Database.

		:param name: Collection name. ( String )
		:param collection: Collection name. ( String )
		:return: Method success. ( Boolean )
		"""

		if name != self.__model.overallCollection:
			if not self.collectionExists(name):
				LOGGER.info("{0} | Adding '{1}' Collection to the Database!".format(self.__class__.__name__, name))
				if dbCommon.addCollection(self.__coreDb.dbSession, name, "Sets", comment):
					self.modelRefresh.emit()
					return True
				else:
					raise dbExceptions.DatabaseOperationError("{0} | Exception raised while adding '{1}' Collection to the Database!".format(self.__class__.__name__, name))
			else:
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' Collection already exists in Database!".format(self.__class__.__name__, name))
		else:
			raise foundations.exceptions.ProgrammingError("{0} | Cannot use '{1}' as Collection name!".format(self.__class__.__name__, self.__model.overallCollection))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, dbExceptions.DatabaseOperationError)
	def removeCollection(self, collection):
		"""
		This method removes provided Collection from the Database.

		:param collection: Collection to remove. ( DbCollection )
		:return: Method success. ( Boolean )
		"""

		iblSets = dbCommon.getCollectionsIblSets(self.__coreDb.dbSession, (collection.id,))
		for iblSet in iblSets:
			LOGGER.info("{0} | Moving '{1}' Ibl Set to default Collection!".format(self.__class__.__name__, iblSet.title))
			iblSet.collection = self.getCollectionId(self.__model.defaultCollection)

		LOGGER.info("{0} | Removing '{1}' Collection from the Database!".format(self.__class__.__name__, collection.name))
		if dbCommon.removeCollection(self.__coreDb.dbSession, str(collection.id)):
			self.modelRefresh.emit()
			self.__coreDatabaseBrowser.modelRefresh.emit()
			return True
		else:
			raise dbExceptions.DatabaseOperationError("{0} | Exception raised while removing '{1}' Collection from the Database!".format(self.__class__.__name__, collection.name))

	@core.executionTrace
	def collectionExists(self, name):
		"""
		This method returns if provided Collection name exists in the Database.

		:param name: Collection name. ( String )
		:return: Collection exists. ( Boolean )
		"""

		return dbCommon.collectionExists(self.__coreDb.dbSession, name)

	@core.executionTrace
	def getCollections(self):
		"""
		This method returns Database set Collections.

		:return: Database set Collections. ( List )
		"""

		return [collection for collection in dbCommon.filterCollections(self.__coreDb.dbSession, "Sets", "type")]

	@core.executionTrace
	def setCollections(self):
		"""
		This method sets Model Collections.
		"""

		self.__model.setCollections(self.getCollections())

	@core.executionTrace
	def getCollectionsIblSets(self, collections):
		"""
		This method gets provided Collections Ibl Sets.

		:param collections: Collections to get Ibl Sets from. ( List )
		:return: Ibl Sets list. ( List )
		"""

		return [iblSet for iblSet in dbCommon.getCollectionsIblSets(self.__coreDb.dbSession, [collection.id for collection in collections])]

	@core.executionTrace
	def getCollectionId(self, collection):
		"""
		This method returns provided Collection id.

		:param collection: Collection to get the id from. ( String )
		:return: Provided Collection id. ( Integer )
		"""

		return self.__model.findItems(collection, Qt.MatchExactly | Qt.MatchRecursive, 0)[0]._datas.id

	@core.executionTrace
	def getUniqueCollectionId(self):
		"""
		This method returns an unique Collection id (Either first selected Collection or default one).

		:return: Unique id. ( Integer )
		"""

		ids = [collection.id for collection in self.getSelectedCollections()]
		if not ids:
			return self.getCollectionId(self.__model.defaultCollection)
		else:
			len(ids) > 1 and LOGGER.warning("!> {0} | Multiple Collections selected, using '{1}' id!".format(self.__class__.__name__, ids[0]))
			return ids[0]

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This method returns the selected items.

		:param rowsRootOnly: Return rows roots only. ( Boolean )
		:return: View selected items. ( List )
		"""

		return self.__view.getSelectedItems(rowsRootOnly)

	@core.executionTrace
	def getSelectedCollections(self):
		"""
		This method gets the selected Collections.

		:return: View selected Collections. ( List )
		"""

		selectedCollections = [item._datas for item in self.getSelectedItems() if item._type == "Collection"]
		return selectedCollections and selectedCollections or []
