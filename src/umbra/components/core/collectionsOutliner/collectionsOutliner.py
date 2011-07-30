#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**collectionsOutliner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Collections Outliner core Component Module.

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
import foundations.strings
import umbra.components.core.db.dbUtilities.common as dbCommon
import umbra.components.core.db.dbUtilities.types as dbTypes
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class CollectionsOutliner_QTreeView(QTreeView):
	"""
	This class is the CollectionsOutliner_QTreeView class.
	"""

	@core.executionTrace
	def __init__(self, container):
		"""
		This method initializes the class.

		:param container: Container to attach the Component to. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTreeView.__init__(self, container)

		self.setAcceptDrops(True)

		# --- Setting class attributes. ---
		self.__container = container

		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreCollectionsOutliner = self.__container.componentsManager.components["core.collectionsOutliner"].interface

		self.__previousCollection = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def coreDb(self):
		"""
		This method is the property for the _coreDb attribute.

		:return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This method is the setter method for the _coreDb attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for the _coreDb attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDb"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for the _coreDatabaseBrowser attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for the _coreDatabaseBrowser attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for the _coreDatabaseBrowser attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def coreCollectionsOutliner(self):
		"""
		This method is the property for the _coreCollectionsOutliner attribute.

		:return: self.__coreCollectionsOutliner. ( Object )
		"""

		return self.__coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		"""
		This method is the setter method for the _coreCollectionsOutliner attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This method is the deleter method for the _coreCollectionsOutliner attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreCollectionsOutliner"))

	@property
	def previousCollection(self):
		"""
		This method is the property for the _previousCollection attribute.

		:return: self.__previousCollection. ( String )
		"""

		return self.__previousCollection

	@previousCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previousCollection(self, value):
		"""
		This method is the setter method for the _previousCollection attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("previousCollection"))

	@previousCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previousCollection(self):
		"""
		This method is the deleter method for the _previousCollection attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("previousCollection"))

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
		elif event.mimeData().hasFormat("text/uri-list"):
			LOGGER.debug("> '{0}' drag event type accepted!".format("text/uri-list"))
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
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, OSError, foundations.exceptions.UserError)
	def dropEvent(self, event):
		"""
		This method defines the drop event behavior.

		:param event: QEvent. ( QEvent )
		"""

		if not self.__container.parameters.databaseReadOnly:
			if event.mimeData().hasUrls():
				LOGGER.debug("> Drag event urls list: '{0}'!".format(event.mimeData().urls()))
				for url in event.mimeData().urls():
					path = (platform.system() == "Windows" or platform.system() == "Microsoft") and re.search("^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
					if re.search("\.{0}$".format(self.__coreDatabaseBrowser.extension), str(url.path())):
						name = foundations.strings.getSplitextBasename(path)
						if messageBox.messageBox("Question", "Question", "'{0}' Ibl Set file has been dropped, would you like to add it to the Database?".format(name), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
							self.__coreDatabaseBrowser.addIblSet(name, path)
					else:
						if os.path.isdir(path):
							if messageBox.messageBox("Question", "Question", "'{0}' directory has been dropped, would you like to add its content to the Database?".format(path), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
								self.__coreDatabaseBrowser.addDirectory(path)
						else:
							raise OSError, "{0} | Exception raised while parsing '{1}' path: Syntax is invalid!".format(self.__class__.__name__, path)
			else:
				indexAt = self.indexAt(event.pos())
				itemAt = self.model().itemFromIndex(indexAt)

				if itemAt:
					LOGGER.debug("> Item at drop position: '{0}'.".format(itemAt))
					collectionStandardItem = self.model().itemFromIndex(self.model().sibling(indexAt.row(), 0, indexAt))
					if collectionStandardItem.text() != self.__coreCollectionsOutliner.overallCollection:
						collection = collectionStandardItem._datas
						for iblSet in self.__coreDatabaseBrowser.getSelectedIblSets():
							LOGGER.info("> Moving '{0}' Ibl Set to '{1}' Collection.".format(iblSet.title, collection.name))
							iblSet.collection = collection.id
						if dbCommon.commit(self.__coreDb.dbSession):
							self.__coreCollectionsOutliner.ui.Collections_Outliner_treeView.selectionModel().setCurrentIndex(indexAt, QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot perform action, Database has been set read only!".format(self.__class__.__name__)

	@core.executionTrace
	def __QTreeView__clicked(self, index):
		"""
		This method defines the behavior when the Model is clicked.

		:param index: Clicked Model item index. ( QModelIndex )
		"""

		self.__previousCollection = self.model().itemFromIndex(self.model().sibling(index.row(), 0, index)).text()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __QTreeView__doubleClicked(self, index):
		"""
		This method defines the behavior when a QStandardItem is double clicked.

		:param index: Clicked Model item index. ( QModelIndex )
		"""

		if not self.__container.parameters.databaseReadOnly:
			collectionStandardItem = self.model().itemFromIndex(self.model().sibling(index.row(), 0, index))

			if collectionStandardItem.text() != self.__coreCollectionsOutliner.defaultCollection and collectionStandardItem.text() != self.__coreCollectionsOutliner.overallCollection:
				if self.model().itemFromIndex(index).column() == self.__coreCollectionsOutliner.modelHeaders.index(self.__coreCollectionsOutliner.setsCountLabel):
					messageBox.messageBox("Warning", "Warning", "{0} | 'Sets Counts' column is read only!".format(self.__class__.__name__))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' and '{2}' Collections attributes are read only!".format(self.__class__.__name__, self.__coreCollectionsOutliner.overallCollection, self.__coreCollectionsOutliner.defaultCollection))
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot perform action, Database has been set read only!".format(self.__class__.__name__)

class CollectionsOutliner(UiComponent):
	"""
	This class is the CollectionsOutliner class.
	"""

	# Custom signals definitions.
	modelChanged = pyqtSignal()
	modelRefresh = pyqtSignal()
	modelPartialRefresh = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		:param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiPath = "ui/Collections_Outliner.ui"
		self.__uiResources = "resources"
		self.__uiDefaultCollectionImage = "Default_Collection.png"
		self.__uiUserCollectionImage = "User_Collection.png"
		self.__dockArea = 1

		self.__container = None
		self.__settings = None
		self.__settingsSection = None
		self.__settingsSeparator = ","

		self.__coreDb = None
		self.__coreDatabaseBrowser = None

		self.__model = None
		self.__modelSelection = None

		self.__overallCollection = "Overall"
		self.__defaultCollection = "Default"
		self.__setsCountLabel = "Sets"
		self.__modelHeaders = [ "Collections", self.__setsCountLabel, "Comment" ]
		self.__treeViewIndentation = 15

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for the _uiPath attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for the _uiPath attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for the _uiPath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This method is the property for the _uiResources attribute.

		:return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for the _uiResources attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for the _uiResources attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiDefaultCollectionImage(self):
		"""
		This method is the property for the _uiDefaultCollectionImage attribute.

		:return: self.__uiDefaultCollectionImage. ( String )
		"""

		return self.__uiDefaultCollectionImage

	@uiDefaultCollectionImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self, value):
		"""
		This method is the setter method for the _uiDefaultCollectionImage attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiDefaultCollectionImage"))

	@uiDefaultCollectionImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self):
		"""
		This method is the deleter method for the _uiDefaultCollectionImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiDefaultCollectionImage"))

	@property
	def uiUserCollectionImage(self):
		"""
		This method is the property for the _uiUserCollectionImage attribute.

		:return: self.__uiUserCollectionImage. ( String )
		"""

		return self.__uiUserCollectionImage

	@uiUserCollectionImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self, value):
		"""
		This method is the setter method for the _uiUserCollectionImage attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiUserCollectionImage"))

	@uiUserCollectionImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self):
		"""
		This method is the deleter method for the _uiUserCollectionImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiUserCollectionImage"))

	@property
	def dockArea(self):
		"""
		This method is the property for the _dockArea attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for the _dockArea attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for the _dockArea attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def settings(self):
		"""
		This method is the property for the _settings attribute.

		:return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for the _settings attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for the _settings attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))

	@property
	def settingsSection(self):
		"""
		This method is the property for the _settingsSection attribute.

		:return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for the _settingsSection attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for the _settingsSection attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settingsSection"))

	@property
	def settingsSeparator(self):
		"""
		This method is the property for the _settingsSeparator attribute.

		:return: self.__settingsSeparator. ( String )
		"""

		return self.__settingsSeparator

	@settingsSeparator.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self, value):
		"""
		This method is the setter method for the _settingsSeparator attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self):
		"""
		This method is the deleter method for the _settingsSeparator attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settingsSeparator"))

	@property
	def coreDb(self):
		"""
		This method is the property for the _coreDb attribute.

		:return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This method is the setter method for the _coreDb attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for the _coreDb attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDb"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for the _coreDatabaseBrowser attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for the _coreDatabaseBrowser attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for the _coreDatabaseBrowser attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def model(self):
		"""
		This method is the property for the _model attribute.

		:return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for the _model attribute.

		:param value: Attribute value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for the _model attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("model"))

	@property
	def modelSelection(self):
		"""
		This method is the property for the _modelSelection attribute.

		:return: self.__modelSelection. ( Dictionary )
		"""

		return self.__modelSelection

	@modelSelection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self, value):
		"""
		This method is the setter method for the _modelSelection attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("modelSelection"))

	@modelSelection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self):
		"""
		This method is the deleter method for the _modelSelection attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("modelSelection"))

	@property
	def overallCollection(self):
		"""
		This method is the property for the _overallCollection attribute.

		:return: self.__overallCollection. ( String )
		"""

		return self.__overallCollection

	@overallCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overallCollection(self, value):
		"""
		This method is the setter method for the _overallCollection attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("overallCollection"))

	@overallCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overallCollection(self):
		"""
		This method is the deleter method for the _overallCollection attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("overallCollection"))

	@property
	def defaultCollection(self):
		"""
		This method is the property for the _defaultCollection attribute.

		:return: self.__defaultCollection. ( String )
		"""

		return self.__defaultCollection

	@defaultCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollection(self, value):
		"""
		This method is the setter method for the _defaultCollection attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultCollection"))

	@defaultCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollection(self):
		"""
		This method is the deleter method for the _defaultCollection attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultCollection"))

	@property
	def setsCountLabel(self):
		"""
		This method is the property for the _setsCountLabel attribute.

		:return: self.__setsCountLabel. ( String )
		"""

		return self.__setsCountLabel

	@setsCountLabel.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setsCountLabel(self, value):
		"""
		This method is the setter method for the _setsCountLabel attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("setsCountLabel"))

	@setsCountLabel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setsCountLabel(self):
		"""
		This method is the deleter method for the _setsCountLabel attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("setsCountLabel"))

	@property
	def modelHeaders(self):
		"""
		This method is the property for the _modelHeaders attribute.

		:return: self.__modelHeaders. ( List )
		"""

		return self.__modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self, value):
		"""
		This method is the setter method for the _modelHeaders attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("modelHeaders"))

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self):
		"""
		This method is the deleter method for the _modelHeaders attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("modelHeaders"))

	@property
	def treeViewIndentation(self):
		"""
		This method is the property for the _treeViewIndentation attribute.

		:return: self.__treeViewIndentation. ( Integer )
		"""

		return self.__treeViewIndentation

	@treeViewIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self, value):
		"""
		This method is the setter method for the _treeViewIndentation attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("treeViewIndentation"))

	@treeViewIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self):
		"""
		This method is the deleter method for the _treeViewIndentation attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("treeViewIndentation"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component cannot be deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__container.parameters.databaseReadOnly and LOGGER.info("{0} | Collections_Outliner_treeView Model edition deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))
		self.__model = QStandardItemModel()
		self.__Collections_Outliner_treeView_setModel()

		self.ui.Collections_Outliner_treeView = CollectionsOutliner_QTreeView(self.__container)
		self.ui.Collections_Outliner_dockWidgetContents_gridLayout.addWidget(self.ui.Collections_Outliner_treeView, 0, 0)

		self.ui.Collections_Outliner_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Collections_Outliner_treeView_addActions()

		self.__Collections_Outliner_treeView_setView()

		# Signals / Slots.
		self.ui.Collections_Outliner_treeView.selectionModel().selectionChanged.connect(self.__Collections_Outliner_treeView_selectionModel__selectionChanged)
		self.ui.Collections_Outliner_treeView.clicked.connect(self.ui.Collections_Outliner_treeView._CollectionsOutliner_QTreeView__QTreeView__clicked)
		self.ui.Collections_Outliner_treeView.doubleClicked.connect(self.ui.Collections_Outliner_treeView._CollectionsOutliner_QTreeView__QTreeView__doubleClicked)
		self.modelChanged.connect(self.__Collections_Outliner_treeView_refreshView)
		self.modelRefresh.connect(self.__Collections_Outliner_treeView_refreshModel)
		self.modelPartialRefresh.connect(self.__Collections_Outliner_treeView_setIblSetsCounts)
		not self.__container.parameters.databaseReadOnly and self.__model.dataChanged.connect(self.__Collections_Outliner_treeView_model__dataChanged)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component ui cannot be uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget cannot be removed!".format(self.name))

	@core.executionTrace
	def onStartup(self):
		"""
		This method is called on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework startup method.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			not self.getCollections() and self.addCollection(self.__defaultCollection, "Default Collection")
		else:
			LOGGER.info("{0} | Database default Collection wizard deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeCollectionsIds = str(self.__settings.getKey(self.__settingsSection, "activeCollections").toString())
		LOGGER.debug("> Stored '{0}' active Collections ids selection: '{1}'.".format(self.__class__.__name__, activeCollectionsIds))
		if activeCollectionsIds:
			if self.__settingsSeparator in activeCollectionsIds:
				ids = activeCollectionsIds.split(self.__settingsSeparator)
			else:
				ids = [activeCollectionsIds]
			self.__modelSelection["Collections"] = [int(id) for id in ids]

		activeOverallCollection = str(self.__settings.getKey(self.__settingsSection, "activeOverallCollection").toString())
		LOGGER.debug("> Stored '{0}' active overall Collection selection: '{1}'.".format(self.__class__.__name__, activeOverallCollection))
		if activeOverallCollection:
			self.__modelSelection[self.__overallCollection] = [activeOverallCollection]

		self.__Collections_Outliner_treeView_restoreModelSelection()

	@core.executionTrace
	def onClose(self):
		"""
		This method is called on Framework close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework close method.".format(self.__class__.__name__))

		self.__Collections_Outliner_treeView_storeModelSelection()
		self.__settings.setKey(self.__settingsSection, "activeCollections", self.__settingsSeparator.join((str(id) for id in self.__modelSelection["Collections"])))
		self.__settings.setKey(self.__settingsSection, "activeOverallCollection", self.__settingsSeparator.join((str(id) for id in self.__modelSelection[self.__overallCollection])))

	@core.executionTrace
	def __Collections_Outliner_treeView_setModel(self):
		"""
		This method sets the Collections_Outliner_treeView Model.

		Columns:
		Collections | Sets | Comment

		Rows:
		* Overall Collection: { _type: "Overall" }
		** Collection: { _type: "Collection", _datas: dbTypes.DbCollection }
		"""

		LOGGER.debug("> Setting up '{0}' Model!".format("Collections_Outliner_treeView"))

		self.__Collections_Outliner_treeView_storeModelSelection()

		self.__model.clear()

		self.__model.setHorizontalHeaderLabels(self.__modelHeaders)
		self.__model.setColumnCount(len(self.__modelHeaders))
		readOnlyFlags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

		LOGGER.debug("> Preparing '{0}' Collection for '{1}' Model.".format(self.__overallCollection, "Collections_Outliner_treeView"))

		overallCollectionStandardItem = QStandardItem(QString(self.__overallCollection))
		overallCollectionStandardItem.setFlags(readOnlyFlags)

		overallCollectionSetsCountStandardItem = QStandardItem(QString(str(dbCommon.getIblSets(self.__coreDb.dbSession).count())))
		overallCollectionSetsCountStandardItem.setTextAlignment(Qt.AlignCenter)
		overallCollectionSetsCountStandardItem.setFlags(readOnlyFlags)

		overallCollectionCommentsStandardItem = QStandardItem()
		overallCollectionCommentsStandardItem.setFlags(readOnlyFlags)

		overallCollectionStandardItem._type = "Overall"

		LOGGER.debug("> Adding '{0}' Collection to '{1}'.".format(self.__overallCollection, "Collections_Outliner_treeView"))
		self.__model.appendRow([overallCollectionStandardItem, overallCollectionSetsCountStandardItem, overallCollectionCommentsStandardItem])

		collections = self.getCollections()

		if collections:
			for collection in collections:
				LOGGER.debug("> Preparing '{0}' Collection for '{1}' Model.".format(collection.name, "Collections_Outliner_treeView"))

				try:
					collectionStandardItem = QStandardItem(QString(collection.name))
					iconPath = collection.name == self.defaultCollection and os.path.join(self.__uiResources, self.__uiDefaultCollectionImage) or os.path.join(self.__uiResources, self.__uiUserCollectionImage)
					collectionStandardItem.setIcon(QIcon(iconPath))
					(collection.name == self.__defaultCollection or self.__container.parameters.databaseReadOnly) and collectionStandardItem.setFlags(readOnlyFlags)

					collectionSetsCountStandardItem = QStandardItem(QString(str(self.__coreDb.dbSession.query(dbTypes.DbIblSet).filter_by(collection=collection.id).count())))
					collectionSetsCountStandardItem.setTextAlignment(Qt.AlignCenter)
					collectionSetsCountStandardItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

					collectionCommentsStandardItem = QStandardItem(QString(collection.comment))
					(collection.name == self.__defaultCollection or self.__container.parameters.databaseReadOnly) and collectionCommentsStandardItem.setFlags(readOnlyFlags)

					collectionStandardItem._datas = collection
					collectionStandardItem._type = "Collection"

					LOGGER.debug("> Adding '{0}' Collection to '{1}' Model.".format(collection.name, "Collections_Outliner_treeView"))
					overallCollectionStandardItem.appendRow([collectionStandardItem, collectionSetsCountStandardItem, collectionCommentsStandardItem])

				except Exception as error:
					LOGGER.error("!>{0} | Exception raised while adding '{1}' Collection to '{2}' Model!".format(self.__class__.__name__, collection.name, "Collections_Outliner_treeView"))
					foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "Collections_Outliner_treeView"))
		else:
			LOGGER.info("{0} | Database has no user defined Collections!".format(self.__class__.__name__))

		self.__Collections_Outliner_treeView_restoreModelSelection()
		self.emit(SIGNAL("modelChanged()"))

	@core.executionTrace
	def __Collections_Outliner_treeView_refreshModel(self):
		"""
		This method refreshes the Collections_Outliner_treeView Model.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Collections_Outliner_treeView"))

		self.__Collections_Outliner_treeView_setModel()

	@core.executionTrace
	def __Collections_Outliner_treeView_setView(self):
		"""
		This method sets the Collections_Outliner_treeView View.
		"""

		LOGGER.debug("> Initializing '{0}' Widget!".format("Collections_Outliner_treeView"))

		self.ui.Collections_Outliner_treeView.setAutoScroll(False)
		self.ui.Collections_Outliner_treeView.setIndentation(self.__treeViewIndentation)
		self.ui.Collections_Outliner_treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.Collections_Outliner_treeView.setSortingEnabled(True)

		self.ui.Collections_Outliner_treeView.setModel(self.__model)

		self.__Collections_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def __Collections_Outliner_treeView_setDefaultViewState(self):
		"""
		This method sets Collections_Outliner_treeView default View state.
		"""

		LOGGER.debug("> Setting '{0}' default View state!".format("Collections_Outliner_treeView"))

		self.ui.Collections_Outliner_treeView.expandAll()
		for column in range(len(self.__modelHeaders)):
			self.ui.Collections_Outliner_treeView.resizeColumnToContents(column)

		self.ui.Collections_Outliner_treeView.sortByColumn(0, Qt.AscendingOrder)

	@core.executionTrace
	def __Collections_Outliner_treeView_setIblSetsCounts(self):
		"""
		This method Sets the Collections_Outliner_treeView Ibl Sets counts.
		"""

		# Disconnecting model "dataChanged()" signal.
		not self.__container.parameters.databaseReadOnly and self.__model.dataChanged.disconnect(self.__Collections_Outliner_treeView_model__dataChanged)

		for i in range(self.__model.rowCount()):
			currentStandardItem = self.__model.item(i)
			if currentStandardItem.text() == self.__overallCollection:
				self.__model.itemFromIndex(self.__model.sibling(i, 1, self.__model.indexFromItem(currentStandardItem))).setText(str(dbCommon.getIblSets(self.__coreDb.dbSession).count()))
			for j in range(currentStandardItem.rowCount()):
				collectionStandardItem = currentStandardItem.child(j, 0)
				collectionSetsCountStandardItem = currentStandardItem.child(j, 1)
				collectionSetsCountStandardItem.setText(str(self.__coreDb.dbSession.query(dbTypes.DbIblSet).filter_by(collection=collectionStandardItem._datas.id).count()))

		# Reconnecting model "dataChanged()" signal.
		not self.__container.parameters.databaseReadOnly and self.__model.dataChanged.connect(self.__Collections_Outliner_treeView_model__dataChanged)

	@core.executionTrace
	def __Collections_Outliner_treeView_refreshView(self):
		"""
		This method refreshes the Collections_Outliner_treeView View.
		"""

		self.__Collections_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def __Collections_Outliner_treeView_storeModelSelection(self):
		"""
		This method stores Collections_Outliner_treeView Model selection.
		"""

		LOGGER.debug("> Storing '{0}' Model selection!".format("Collections_Outliner_treeView"))

		self.__modelSelection = { self.__overallCollection:[], "Collections":[] }
		for item in self.getSelectedItems():
			if item._type == self.__overallCollection:
				self.__modelSelection[self.__overallCollection].append(item.text())
			elif item._type == "Collection":
				self.__modelSelection["Collections"].append(item._datas.id)

	@core.executionTrace
	def __Collections_Outliner_treeView_restoreModelSelection(self):
		"""
		This method restores Collections_Outliner_treeView Model selection.
		"""

		LOGGER.debug("> Restoring '{0}' Model selection!".format("Collections_Outliner_treeView"))

		indexes = []
		for i in range(self.__model.rowCount()):
			overallCollectionStandardItem = self.__model.item(i)
			overallCollectionStandardItem.text() in self.__modelSelection["Overall"] and indexes.append(self.__model.indexFromItem(overallCollectionStandardItem))
			for j in range(overallCollectionStandardItem.rowCount()):
				collectionStandardItem = overallCollectionStandardItem.child(j, 0)
				collectionStandardItem._datas.id in self.__modelSelection["Collections"] and indexes.append(self.__model.indexFromItem(collectionStandardItem))

		selectionModel = self.ui.Collections_Outliner_treeView.selectionModel()
		if selectionModel:
			selectionModel.clear()
			for index in indexes:
				selectionModel.setCurrentIndex(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

	@core.executionTrace
	def __Collections_Outliner_treeView_addActions(self):
		"""
		This method sets the Collections Outliner actions.
		"""

		if not self.__container.parameters.databaseReadOnly:
			addContentAction = QAction("Add Content ...", self.ui.Collections_Outliner_treeView)
			addContentAction.triggered.connect(self.__Collections_Outliner_treeView_addContentAction__triggered)
			self.ui.Collections_Outliner_treeView.addAction(addContentAction)

			addSingleCollectionAction = QAction("Add Collection ...", self.ui.Collections_Outliner_treeView)
			addSingleCollectionAction.triggered.connect(self.__Collections_Outliner_treeView_addCollectionAction__triggered)
			self.ui.Collections_Outliner_treeView.addAction(addSingleCollectionAction)

			removeCollectionsAction = QAction("Remove Collection(s) ...", self.ui.Collections_Outliner_treeView)
			removeCollectionsAction.triggered.connect(self.__Collections_Outliner_treeView_removeCollectionsAction__triggered)
			self.ui.Collections_Outliner_treeView.addAction(removeCollectionsAction)
		else:
			LOGGER.info("{0} | Collections Database alteration capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __Collections_Outliner_treeView_addContentAction__triggered(self, checked):
		"""
		This method is triggered by addContentAction action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.addContent__()

	@core.executionTrace
	def __Collections_Outliner_treeView_addCollectionAction__triggered(self, checked):
		"""
		This method is triggered by addSingleCollectionAction action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.addCollection__()

	@core.executionTrace
	def __Collections_Outliner_treeView_removeCollectionsAction__triggered(self, checked):
		"""
		This method is triggered by removeCollectionsAction action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.removeCollections__()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __Collections_Outliner_treeView_model__dataChanged(self, startIndex, endIndex):
		"""
		This method defines the behavior when the Collections_Outliner_treeView Model datas changes.

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
			raise foundations.exceptions.UserError, "{0} | Exception while editing a Collection field: Cannot use an empty value!".format(self.__class__.__name__)
		self.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	def __Collections_Outliner_treeView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method triggers the Database_Browser_listView refresh depending on the Collections Outliner selected items.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""
		self.__coreDatabaseBrowser.emit(SIGNAL("modelDatasRefresh()"))
		self.__coreDatabaseBrowser.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	def __coreDatabaseBrowser_Database_Browser_listView_setModelContent(self):
		"""
		This method sets coreDatabaseBrowser Model content.
		"""

		self.__coreDatabaseBrowser.modelContent = self.getCollectionsIblSets(self.getSelectedItems())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def addContent__(self):
		"""
		This method adds user defined content to the Database.

		:return: Method success. ( Boolean )
		"""

		collection = self.addCollection__()
		if not collection:
			return

		directory = self.__container.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self, "Add content:", self.__container.lastBrowsedPath)))
		if not directory:
			return

		LOGGER.debug("> Chosen directory path: '{0}'.".format(directory))
		if self.__coreDatabaseBrowser.addDirectory(directory, self.getCollectionId(collection)):
			return True
		else:
			raise Exception, "{0} | Exception raised while adding '{1}' directory content to the Database!".format(self.__class__.__name__, directory)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError, Exception)
	def addCollection__(self):
		"""
		This method adds an user defined Collection to the Database.

		:return: Collection name. ( String )
		"""

		collectionInformations, state = QInputDialog.getText(self, "Add Collection", "Enter your Collection name!")
		if not state:
			return

		if collectionInformations:
			collectionInformations = str(collectionInformations).split(",")
			name = collectionInformations[0].strip()
			if name != self.__overallCollection:
				if not self.collectionExists(name):
					comment = len(collectionInformations) == 1 and "Double click to set a comment!" or collectionInformations[1].strip()
					if self.addCollection(name, comment):
						self.ui.Collections_Outliner_treeView.selectionModel().setCurrentIndex(self.__model.indexFromItem(self.__model.findItems(name, Qt.MatchExactly | Qt.MatchRecursive, 0)[0]), QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
						return name
					else:
						raise Exception, "{0} | Exception raised while adding '{1}' Collection to the Database!".format(self.__class__.__name__, name)
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Collection already exists in Database!".format(self.__class__.__name__, name))
			else:
				raise foundations.exceptions.UserError, "{0} | Exception while adding a Collection to the Database: Cannot use '{1}' as Collection name!".format(self.__class__.__name__, self.__overallCollection)
		else:
			raise foundations.exceptions.UserError, "{0} | Exception while adding a Collection to the Database: Cannot use an empty name!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def removeCollections__(self):
		"""
		This method removes user selected Collections from the Database.

		:return: Method success. ( Boolean )
		"""

		selectedItems = self.getSelectedItems()
		if self.__overallCollection in (str(collection.text()) for collection in selectedItems) or self.__defaultCollection in (str(collection.text()) for collection in selectedItems):
			messageBox.messageBox("Warning", "Warning", "{0} | Cannot remove '{1}' or '{2}' Collection!".format(self.__class__.__name__, self.__overallCollection, self.__defaultCollection))

		selectedCollections = [collection for collection in self.getSelectedCollections() if collection.name != self.__defaultCollection]
		if not selectedCollections:
			return

		if messageBox.messageBox("Question", "Question", "Are you sure you want to remove '{0}' Collection(s)?".format(", ".join((str(collection.name) for collection in selectedCollections))), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
			success = True
			for collection in selectedCollections:
				success *= self.removeCollection(collection) or False
			self.ui.Collections_Outliner_treeView.selectionModel().setCurrentIndex(self.__model.index(0, 0), QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
			if success:
				return True
			else:
				raise Exception, "{0} | Exception raised while removing '{1}' Collections from the Database!".format(self.__class__.__name__, ", ". join((collection.name for collection in selectedCollections)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError, foundations.exceptions.DatabaseOperationError)
	def addCollection(self, name, comment="Double click to set a comment!"):
		"""
		This method adds a Collection to the Database.

		:param name: Collection name. ( String )
		:param collection: Collection name. ( String )
		:return: Method success. ( Boolean )
		"""

		if name != self.__overallCollection:
			if not self.collectionExists(name):
				LOGGER.info("{0} | Adding '{1}' Collection to the Database!".format(self.__class__.__name__, name))
				if dbCommon.addCollection(self.__coreDb.dbSession, name, "Sets", comment):
					self.emit(SIGNAL("modelRefresh()"))
					return True
				else:
					raise foundations.exceptions.DatabaseOperationError, "{0} | Exception raised while adding '{1}' Collection to the Database!".format(self.__class__.__name__, name)
			else:
				raise foundations.exceptions.ProgrammingError, "{0} | '{1}' Collection already exists in Database!".format(self.__class__.__name__, name)
		else:
			raise foundations.exceptions.ProgrammingError, "{0} | Cannot use '{1}' as Collection name!".format(self.__class__.__name__, self.__overallCollection)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.DatabaseOperationError)
	def removeCollection(self, collection):
		"""
		This method removes provided Collection from the Database.

		:param collection: Collection to remove. ( DbCollection )
		:return: Method success. ( Boolean )
		"""

		iblSets = dbCommon.getCollectionsIblSets(self.__coreDb.dbSession, (collection.id,))
		for iblSet in iblSets:
			LOGGER.info("{0} | Moving '{1}' Ibl Set to default Collection!".format(self.__class__.__name__, iblSet.title))
			iblSet.collection = self.getCollectionId(self.__defaultCollection)

		LOGGER.info("{0} | Removing '{1}' Collection from the Database!".format(self.__class__.__name__, collection.name))
		if dbCommon.removeCollection(self.__coreDb.dbSession, str(collection.id)):
			self.emit(SIGNAL("modelRefresh()"))
			self.__coreDatabaseBrowser.emit(SIGNAL("modelDatasRefresh()"))
			return True
		else:
			raise foundations.exceptions.DatabaseOperationError, "{0} | Exception raised while removing '{1}' Collection from the Database!".format(self.__class__.__name__, collection.name)

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
	def getCollectionsIblSets(self, collections):
		"""
		This method gets provided Collections Ibl Sets.

		:param collections: Collections to get Ibl Sets from. ( List )
		:return: Ibl Sets list. ( List )
		"""

		return dbCommon.getCollectionsIblSets(self.__coreDb.dbSession, [collection.id for collection in collections])

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
			return self.getCollectionId(self.__defaultCollection)
		else:
			len(ids) > 1 and LOGGER.warning("!> {0} | Multiple Collections selected, using '{1}' id!".format(self.__class__.__name__, ids[0]))
			return ids[0]

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This method returns Collections_Outliner_treeView selected items.

		:param rowsRootOnly: Return rows roots only. ( Boolean )
		:return: View selected items. ( List )
		"""

		selectedIndexes = self.ui.Collections_Outliner_treeView.selectedIndexes()
		return rowsRootOnly and [item for item in set([self.__model.itemFromIndex(self.__model.sibling(index.row(), 0, index)) for index in selectedIndexes])] or [self.__model.itemFromIndex(index) for index in selectedIndexes]

	@core.executionTrace
	def getSelectedCollections(self):
		"""
		This method gets selected Collections.

		:return: View selected Collections. ( List )
		"""

		selectedCollections = [item._datas for item in self.getSelectedItems() if item._type == "Collection"]
		return selectedCollections and selectedCollections or []

