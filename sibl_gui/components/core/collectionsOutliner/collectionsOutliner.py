#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**collectionsOutliner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`CollectionsOutliner` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import re
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QMessageBox

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.walkers
import foundations.strings
import foundations.verbose
import sibl_gui.components.core.database.exceptions
import sibl_gui.components.core.database.operations
import umbra.engine
import umbra.exceptions
import umbra.ui.common
import umbra.ui.nodes
import umbra.ui.widgets.messageBox as messageBox
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.core.collectionsOutliner.models import CollectionsModel
from sibl_gui.components.core.collectionsOutliner.nodes import OverallCollectionNode
from sibl_gui.components.core.collectionsOutliner.views import IblSetsCollections_QTreeView
from sibl_gui.components.core.database.nodes import CollectionNode
from sibl_gui.components.core.database.types import IblSet
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "CollectionsOutliner"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Collections_Outliner.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class CollectionsOutliner(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.core.collectionsOutliner.collectionsOutliner` Component Interface class.
	| It defines methods for Database Collections management.
	"""

	# Custom signals definitions.
	refreshNodes = pyqtSignal()
	"""
	This signal is emited by the :class:`CollectionsOutliner` class when :obj:`CollectionsOutliner.model` class
	property Model Nodes needs to be refreshed. ( pyqtSignal )
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

		super(CollectionsOutliner, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiResourcesDirectory = "resources"
		self.__uiDefaultCollectionImage = "Default_Collection.png"
		self.__uiUserCollectionImage = "User_Collection.png"
		self.__dockArea = 1

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None
		self.__settingsSeparator = ","

		self.__iblSetsOutliner = None

		self.__model = None
		self.__view = None
		self.__overallCollection = "Overall"
		self.__defaultCollection = "Default"
		self.__iblSetsCountLabel = "Ibl Sets"
		self.__headers = OrderedDict([("Collections", "name"),
										(self.__iblSetsCountLabel, "count"),
										("Comment", "comment")])

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
	def uiDefaultCollectionImage(self):
		"""
		This method is the property for **self.__uiDefaultCollectionImage** attribute.

		:return: self.__uiDefaultCollectionImage. ( String )
		"""

		return self.__uiDefaultCollectionImage

	@uiDefaultCollectionImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self, value):
		"""
		This method is the setter method for **self.__uiDefaultCollectionImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiDefaultCollectionImage"))

	@uiDefaultCollectionImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self):
		"""
		This method is the deleter method for **self.__uiDefaultCollectionImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiDefaultCollectionImage"))

	@property
	def uiUserCollectionImage(self):
		"""
		This method is the property for **self.__uiUserCollectionImage** attribute.

		:return: self.__uiUserCollectionImage. ( String )
		"""

		return self.__uiUserCollectionImage

	@uiUserCollectionImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self, value):
		"""
		This method is the setter method for **self.__uiUserCollectionImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiUserCollectionImage"))

	@uiUserCollectionImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self):
		"""
		This method is the deleter method for **self.__uiUserCollectionImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiUserCollectionImage"))

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
	def iblSetsOutliner(self):
		"""
		This method is the property for **self.__iblSetsOutliner** attribute.

		:return: self.__iblSetsOutliner. ( QWidget )
		"""

		return self.__iblSetsOutliner

	@iblSetsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self, value):
		"""
		This method is the setter method for **self.__iblSetsOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsOutliner"))

	@iblSetsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self):
		"""
		This method is the deleter method for **self.__iblSetsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsOutliner"))

	@property
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( CollectionsModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( CollectionsModel )
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
	def view(self):
		"""
		This method is the property for **self.__view** attribute.

		:return: self.__view. ( QWidget )
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		This method is the setter method for **self.__view** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		This method is the deleter method for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def overallCollection(self):
		"""
		This method is the property for **self.__overallCollection** attribute.

		:return: self.__overallCollection. ( String )
		"""

		return self.__overallCollection

	@overallCollection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def overallCollection(self, value):
		"""
		This method is the setter method for **self.__overallCollection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "overallCollection"))

	@overallCollection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def overallCollection(self):
		"""
		This method is the deleter method for **self.__overallCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "overallCollection"))

	@property
	def defaultCollection(self):
		"""
		This method is the property for **self.__defaultCollection** attribute.

		:return: self.__defaultCollection. ( String )
		"""

		return self.__defaultCollection

	@defaultCollection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultCollection(self, value):
		"""
		This method is the setter method for **self.__defaultCollection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultCollection"))

	@defaultCollection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultCollection(self):
		"""
		This method is the deleter method for **self.__defaultCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultCollection"))

	@property
	def iblSetsCountLabel(self):
		"""
		This method is the property for **self.__iblSetsCountLabel** attribute.

		:return: self.__iblSetsCountLabel. ( String )
		"""

		return self.__iblSetsCountLabel

	@iblSetsCountLabel.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsCountLabel(self, value):
		"""
		This method is the setter method for **self.__iblSetsCountLabel** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsCountLabel"))

	@iblSetsCountLabel.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsCountLabel(self):
		"""
		This method is the deleter method for **self.__iblSetsCountLabel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsCountLabel"))

	@property
	def headers(self):
		"""
		This method is the property for **self.__headers** attribute.

		:return: self.__headers. ( OrderedDict )
		"""

		return self.__headers

	@headers.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		This method is the setter method for **self.__headers** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

	@headers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def headers(self):
		"""
		This method is the deleter method for **self.__headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

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

		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]

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
		self.__model = CollectionsModel(self, horizontalHeaders=self.__headers)
		self.setCollections()

		self.Collections_Outliner_treeView.setParent(None)
		self.Collections_Outliner_treeView = IblSetsCollections_QTreeView(self,
																		self.__model,
																		self.__engine.parameters.databaseReadOnly)
		self.Collections_Outliner_treeView.setObjectName("Collections_Outliner_treeView")
		self.Collections_Outliner_dockWidgetContents_gridLayout.addWidget(self.Collections_Outliner_treeView, 0, 0)
		self.__view = self.Collections_Outliner_treeView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__view_addActions()

		# Signals / Slots.
		self.__engine.imagesCaches.QIcon.contentAdded.connect(self.__view.viewport().update)
		self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.refreshNodes.connect(self.__model__refreshNodes)
		if not self.__engine.parameters.databaseReadOnly:
			self.__model.dataChanged.connect(self.__model__dataChanged)

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

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	def onStartup(self):
		"""
		This method is triggered on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			not self.getCollections() and self.addCollection(self.__defaultCollection, "Default Collection")
		else:
			LOGGER.info("{0} | Database default Collection wizard deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		activeCollectionsIdentities = foundations.strings.encode(
		self.__settings.getKey(self.__settingsSection, "activeCollections").toString())
		LOGGER.debug("> '{0}' View stored selected Collections identities '{1}'.".format(self.__class__.__name__,
																						activeCollectionsIdentities))
		self.__view.modelSelection["Collections"] = activeCollectionsIdentities and \
													[int(identity) for identity in activeCollectionsIdentities.split(
													self.__settingsSeparator)] or []

		activeOverallCollection = foundations.strings.encode(
		self.__settings.getKey(self.__settingsSection, "activeOverallCollection").toString())
		LOGGER.debug("> '{0}' View stored 'Overall' Collection: '{1}'.".format(self.__class__.__name__,
																				activeOverallCollection))
		self.__view.modelSelection[self.__overallCollection] = activeCollectionsIdentities and \
																[activeOverallCollection] or []
		self.__view.restoreModelSelection()
		return True

	def onClose(self):
		"""
		This method is triggered on Framework close.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		self.__view.storeModelSelection()
		self.__settings.setKey(self.__settingsSection,
								"activeCollections",
								self.__settingsSeparator.join((foundations.strings.encode(
								identity) for identity in self.__view.modelSelection[
								"Collections"])))
		self.__settings.setKey(self.__settingsSection,
								"activeOverallCollection",
								self.__settingsSeparator.join((foundations.strings.encode(name)
								for name in self.__view.modelSelection[self.__overallCollection])))
		return True

	def __model__refreshNodes(self):
		"""
		This method is triggered when the Model Nodes need refresh.
		"""

		self.setCollections()

	def __model__refreshAttributes(self):
		"""
		This method refreshes the Model Nodes attributes.
		"""

		for node in foundations.walkers.nodesWalker(self.__model.rootNode):
			if not node.family == "Collection":
				continue

			node.updateNodeAttributes()

		overallCollectionNode = \
		foundations.common.getFirstItem(self.__model.findChildren("^{0}$".format(self.__overallCollection)))
		overallCollectionNode.updateNodeAttributes()

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError)
	def __model__dataChanged(self, startIndex, endIndex):
		"""
		This method is triggered when the Model data has changed.
		
		:param startIndex: Edited item starting QModelIndex. ( QModelIndex )
		:param endIndex: Edited item ending QModelIndex. ( QModelIndex )
		"""

		collectionNode = self.__model.getNode(startIndex)
		if collectionNode.family != "Collection":
			return

		if startIndex.column() == 0:
			if self.collectionExists(collectionNode.name):
				self.__engine.notificationsManager.warnify(
				"{0} | '{1}' Collection name already exists in Database!".format(self.__class__.__name__,
																				collectionNode.name))
				return

			if not collectionNode.name:
				collectionNode.updateNode()
				raise foundations.exceptions.UserError(
				"{0} | Exception while editing a Collection field: Cannot use an empty value!".format(
				self.__class__.__name__))

		collectionNode.updateDatabaseItem()
		collectionNode.updateToolTip()

		sibl_gui.components.core.database.operations.commit()

	def __view_addActions(self):
		"""
		This method sets the View actions.
		"""

		if not self.__engine.parameters.databaseReadOnly:
			self.__view.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.collectionsOutliner|Add Content ...",
			slot=self.__view_addContentAction__triggered))
			self.__view.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.collectionsOutliner|Add Collection ...",
			slot=self.__view_addCollectionAction__triggered))
			self.__view.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.collectionsOutliner|Remove Collection(s) ...",
			slot=self.__view_removeCollectionsAction__triggered))
		else:
			LOGGER.info(
			"{0} | Collections Database alteration capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

	def __view_addContentAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.collectionsOutliner|Add Content ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addContentUi()

	def __view_addCollectionAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.collectionsOutliner|Add Collection ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addCollectionUi()

	def __view_removeCollectionsAction__triggered(self, checked):
		"""
		This method is triggered by 
		**'Actions|Umbra|Components|core.collectionsOutliner|Remove Collection(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.removeCollectionsUi()

	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when the View **selectionModel** has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		self.__iblSetsOutliner.refreshNodes.emit()

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.showProcessing("Adding Content ...")
	def addContentUi(self):
		"""
		This method adds user defined content to the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		collection = self.addCollectionUi()
		if not collection:
			return False

		directory = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self,
																						"Add Content:",
																						RuntimeGlobals.lastBrowsedPath)))
		if not directory:
			return False

		LOGGER.debug("> Chosen directory path: '{0}'.".format(directory))
		if self.__iblSetsOutliner.addDirectory(directory, self.getCollectionId(collection)):
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
			self.__class__.__name__, directory))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError,
											Exception)
	@umbra.engine.showProcessing("Adding Collection ...")
	def addCollectionUi(self):
		"""
		This method adds an user defined Collection to the Database.

		:return: Collection name. ( String )

		:note: This method may require user interaction.
		"""

		collectionInformations, state = QInputDialog.getText(self, "Add Collection", "Enter your Collection name:")
		if not state:
			return False

		if collectionInformations:
			collectionInformations = foundations.strings.encode(collectionInformations).split(",")
			name = collectionInformations[0].strip()
			if name != self.__overallCollection:
				if not self.collectionExists(name):
					comment = len(collectionInformations) == 1 and "Double click to set a comment!" or \
					collectionInformations[1].strip()
					if self.addCollection(name, comment):
						self.__view.selectionModel().setCurrentIndex(self.__model.getNodeIndex(
						foundations.common.getFirstItem(self.__model.findChildren(r"^{0}$".format(name)))),
						QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
						return name
					else:
						raise Exception("{0} | Exception raised while adding '{1}' Collection to the Database!".format(
						self.__class__.__name__, name))
				else:
					self.__engine.notificationsManager.warnify(
					"{0} | '{1}' Collection already exists in Database!".format(self.__class__.__name__, name))
			else:
				raise foundations.exceptions.UserError(
				"{0} | Exception while adding a Collection to the Database: Cannot use '{1}' as Collection name!".format(
				self.__class__.__name__, self.__model.overallCollection))
		else:
			raise foundations.exceptions.UserError(
			"{0} | Exception while adding a Collection to the Database: Cannot use an empty name!".format(
			self.__class__.__name__))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.encapsulateProcessing
	def removeCollectionsUi(self):
		"""
		This method removes user selected Collections from the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedNodes = self.getSelectedNodes().keys()
		if self.__overallCollection in (node.name for node in selectedNodes) or \
		self.__defaultCollection in (node.name for node in selectedNodes):
			self.__engine.notificationsManager.warnify(
			"{0} | '{1}' and '{2}' Collections cannot be removed!".format(self.__class__.__name__,
																	self.__overallCollection,
																	self.__defaultCollection))

		selectedCollections = [collection
								for collection in self.getSelectedCollections()
								if collection.name != self.__defaultCollection]
		if not selectedCollections:
			return False

		if messageBox.messageBox("Question", "Question",
		"Are you sure you want to remove '{0}' Collection(s)?".format(", ".join((foundations.strings.encode(collection.name)
																	for collection in selectedCollections))),
		buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.startProcessing("Removing Collections ...", len(selectedCollections))
			success = True
			for collection in selectedCollections:
				success *= self.removeCollection(collection) or False
				self.__engine.stepProcessing()
			self.__engine.stopProcessing()
			self.__view.selectionModel().setCurrentIndex(self.__model.index(0, 0),
			QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
			if success:
				return True
			else:
				raise Exception("{0} | Exception raised while removing '{1}' Collections from the Database!".format(
				self.__class__.__name__, ", ". join((collection.name for collection in selectedCollections))))

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError,
											sibl_gui.components.core.database.exceptions.DatabaseOperationError)
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
				if sibl_gui.components.core.database.operations.addCollection(name, "IblSets", comment):
					self.refreshNodes.emit()
					return True
				else:
					raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
					"{0} | Exception raised while adding '{1}' Collection to the Database!".format(self.__class__.__name__,
																									name))
			else:
				raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Collection already exists in Database!".format(self.__class__.__name__, name))
		else:
			raise foundations.exceptions.ProgrammingError(
		"{0} | Cannot use '{1}' as Collection name!".format(self.__class__.__name__, self.__model.overallCollection))

	@foundations.exceptions.handleExceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def removeCollection(self, collection):
		"""
		This method removes given Collection from the Database.

		:param collection: Collection to remove. ( Collection )
		:return: Method success. ( Boolean )
		"""

		iblSets = sibl_gui.components.core.database.operations.getCollectionsIblSets((collection.id,))
		for iblSet in iblSets:
			LOGGER.info("{0} | Moving '{1}' Ibl Set to default Collection!".format(self.__class__.__name__, iblSet.title))
			iblSet.collection = self.getCollectionId(self.__defaultCollection)

		LOGGER.info("{0} | Removing '{1}' Collection from the Database!".format(self.__class__.__name__, collection.name))
		if sibl_gui.components.core.database.operations.removeCollection(foundations.strings.encode(collection.id)):
			self.refreshNodes.emit()
			self.__iblSetsOutliner.refreshNodes.emit()
			return True
		else:
			raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
			"{0} | Exception raised while removing '{1}' Collection from the Database!".format(self.__class__.__name__,
																								collection.name))
	def getCollections(self):
		"""
		This method returns Database Ibl Sets Collections.

		:return: Database Ibl Sets Collections. ( List )
		"""

		return sibl_gui.components.core.database.operations.getCollectionsByType("IblSets")

	def filterCollections(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		This method filters the Database Ibl Sets Collections on given attribute using given pattern.
		
		:param pattern: Filter pattern. ( String )
		:param attribute: Attribute to filter on. ( String )
		:param flags: Regex filtering flags. ( Integer )

		:return: Filtered Database Ibl Sets Collections. ( List )
		"""

		try:
			pattern = re.compile(pattern, flags)
		except Exception:
			return list()

		return sibl_gui.components.core.database.operations.filterIblSetsCollections(
		"{0}".format(foundations.strings.encode(pattern.pattern)), attribute, flags)

	def collectionExists(self, name):
		"""
		This method returns if given Collection name exists in the Database.

		:param name: Collection name. ( String )
		:return: Collection exists. ( Boolean )
		"""

		return sibl_gui.components.core.database.operations.collectionExists(name)

	def listCollections(self):
		"""
		This method lists Database Ibl Sets Collections names.

		:return: Database Ibl Sets Collections names. ( List )
		"""

		return [collection.name for collection in self.getCollections()]

	def setCollections(self):
		"""
		This method sets the Collections Model nodes.
		"""

		nodeFlags = attributesFlags = self.__engine.parameters.databaseReadOnly and \
		int(Qt.ItemIsSelectable | Qt.ItemIsEnabled) or int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
		collections = self.getCollections()

		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")

		overallCollectionNode = OverallCollectionNode(name="Overall",
													parent=rootNode,
													nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
													attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

		for collection in collections:
			decorationRole = os.path.join(self.__uiResourcesDirectory, self.__uiUserCollectionImage)
			if collection.name == self.__defaultCollection:
				collectionNode = CollectionNode(collection,
												name=collection.name,
												parent=overallCollectionNode,
												nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
												attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
				decorationRole = os.path.join(self.__uiResourcesDirectory, self.__uiDefaultCollectionImage)
			else:
				collectionNode = CollectionNode(collection,
												name=collection.name,
												parent=overallCollectionNode,
												nodeFlags=nodeFlags,
												attributesFlags=attributesFlags)
			collectionNode.roles[Qt.DecorationRole] = decorationRole
		overallCollectionNode.updateNodeAttributes()
		rootNode.sortChildren()

		self.__model.initializeModel(rootNode)
		return True

	def getCollectionByName(self, name):
		"""
		This method returns Database Ibl Sets Collection with given name.

		:param name: Collection name. ( String )
		:return: Database Ibl Sets Collection. ( Collection )
		"""

		collections = self.filterCollections(r"^{0}$".format(name), "name")
		return foundations.common.getFirstItem(collections)

	def getCollectionsIblSets(self, collections):
		"""
		This method gets given Collections Ibl Sets.

		:param collections: Collections to get Ibl Sets from. ( List )
		:return: Ibl Sets list. ( List )
		"""

		return [iblSet for iblSet in \
		sibl_gui.components.core.database.operations.getCollectionsIblSets([collection.id for collection in collections])]

	def getCollectionId(self, collection):
		"""
		This method returns given Collection id.

		:param collection: Collection to get the id from. ( String )
		:return: Provided Collection id. ( Integer )
		"""

		children = self.__model.findChildren(r"^{0}$".format(collection))
		child = foundations.common.getFirstItem(children)
		return child and child.databaseItem.id or None

	def getSelectedNodes(self):
		"""
		This method returns the View selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return self.__view.getSelectedNodes()

	def getSelectedCollectionsNodes(self):
		"""
		This method returns the View selected Collections nodes.

		:return: View selected Collections nodes. ( List )
		"""

		return [node for node in self.getSelectedNodes() if node.family == "Collection"]

	def getSelectedCollections(self):
		"""
		This method gets the View selected Collections.

		:return: View selected Collections. ( List )
		"""

		return [node.databaseItem for node in self.getSelectedCollectionsNodes()]
