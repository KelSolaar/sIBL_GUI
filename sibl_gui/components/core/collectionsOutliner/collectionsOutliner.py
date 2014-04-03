#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**collectionsOutliner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`CollectionsOutliner` Component Interface class.

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
import re
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict
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
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	| Defines the :mod:`sibl_gui.components.core.collectionsOutliner.collectionsOutliner` Component Interface class.
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
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param name: Component name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
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
		Property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory.
		:rtype: unicode
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		Setter for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		Deleter for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiDefaultCollectionImage(self):
		"""
		Property for **self.__uiDefaultCollectionImage** attribute.

		:return: self.__uiDefaultCollectionImage.
		:rtype: unicode
		"""

		return self.__uiDefaultCollectionImage

	@uiDefaultCollectionImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self, value):
		"""
		Setter for **self.__uiDefaultCollectionImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiDefaultCollectionImage"))

	@uiDefaultCollectionImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self):
		"""
		Deleter for **self.__uiDefaultCollectionImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiDefaultCollectionImage"))

	@property
	def uiUserCollectionImage(self):
		"""
		Property for **self.__uiUserCollectionImage** attribute.

		:return: self.__uiUserCollectionImage.
		:rtype: unicode
		"""

		return self.__uiUserCollectionImage

	@uiUserCollectionImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self, value):
		"""
		Setter for **self.__uiUserCollectionImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiUserCollectionImage"))

	@uiUserCollectionImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self):
		"""
		Deleter for **self.__uiUserCollectionImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiUserCollectionImage"))

	@property
	def dockArea(self):
		"""
		Property for **self.__dockArea** attribute.

		:return: self.__dockArea.
		:rtype: int
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		Setter for **self.__dockArea** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		Deleter for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: QSettings
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settingsSection(self):
		"""
		Property for **self.__settingsSection** attribute.

		:return: self.__settingsSection.
		:rtype: unicode
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		Setter for **self.__settingsSection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		Deleter for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def settingsSeparator(self):
		"""
		Property for **self.__settingsSeparator** attribute.

		:return: self.__settingsSeparator.
		:rtype: unicode
		"""

		return self.__settingsSeparator

	@settingsSeparator.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSeparator(self, value):
		"""
		Setter for **self.__settingsSeparator** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSeparator(self):
		"""
		Deleter for **self.__settingsSeparator** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSeparator"))

	@property
	def iblSetsOutliner(self):
		"""
		Property for **self.__iblSetsOutliner** attribute.

		:return: self.__iblSetsOutliner.
		:rtype: QWidget
		"""

		return self.__iblSetsOutliner

	@iblSetsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self, value):
		"""
		Setter for **self.__iblSetsOutliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsOutliner"))

	@iblSetsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self):
		"""
		Deleter for **self.__iblSetsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsOutliner"))

	@property
	def model(self):
		"""
		Property for **self.__model** attribute.

		:return: self.__model.
		:rtype: CollectionsModel
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		Setter for **self.__model** attribute.

		:param value: Attribute value.
		:type value: CollectionsModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		Deleter for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def view(self):
		"""
		Property for **self.__view** attribute.

		:return: self.__view.
		:rtype: QWidget
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		Setter for **self.__view** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		Deleter for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def overallCollection(self):
		"""
		Property for **self.__overallCollection** attribute.

		:return: self.__overallCollection.
		:rtype: unicode
		"""

		return self.__overallCollection

	@overallCollection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def overallCollection(self, value):
		"""
		Setter for **self.__overallCollection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "overallCollection"))

	@overallCollection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def overallCollection(self):
		"""
		Deleter for **self.__overallCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "overallCollection"))

	@property
	def defaultCollection(self):
		"""
		Property for **self.__defaultCollection** attribute.

		:return: self.__defaultCollection.
		:rtype: unicode
		"""

		return self.__defaultCollection

	@defaultCollection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultCollection(self, value):
		"""
		Setter for **self.__defaultCollection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultCollection"))

	@defaultCollection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultCollection(self):
		"""
		Deleter for **self.__defaultCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultCollection"))

	@property
	def iblSetsCountLabel(self):
		"""
		Property for **self.__iblSetsCountLabel** attribute.

		:return: self.__iblSetsCountLabel.
		:rtype: unicode
		"""

		return self.__iblSetsCountLabel

	@iblSetsCountLabel.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsCountLabel(self, value):
		"""
		Setter for **self.__iblSetsCountLabel** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsCountLabel"))

	@iblSetsCountLabel.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsCountLabel(self):
		"""
		Deleter for **self.__iblSetsCountLabel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsCountLabel"))

	@property
	def headers(self):
		"""
		Property for **self.__headers** attribute.

		:return: self.__headers.
		:rtype: OrderedDict
		"""

		return self.__headers

	@headers.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		Setter for **self.__headers** attribute.

		:param value: Attribute value.
		:type value: OrderedDict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

	@headers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def headers(self):
		"""
		Deleter for **self.__headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Engine to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
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
		Deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	def initializeUi(self):
		"""
		Initializes the Component ui.
		
		:return: Method success.
		:rtype: bool
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
		Uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	def onStartup(self):
		"""
		Defines the slot triggered on Framework startup.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			not self.getCollections() and self.addCollection(self.__defaultCollection, "Default Collection")
		else:
			LOGGER.info("{0} | Database default Collection wizard deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		activeCollectionsIdentities = foundations.strings.toString(
		self.__settings.getKey(self.__settingsSection, "activeCollections").toString())
		LOGGER.debug("> '{0}' View stored selected Collections identities '{1}'.".format(self.__class__.__name__,
																						activeCollectionsIdentities))
		self.__view.modelSelection["Collections"] = activeCollectionsIdentities and \
													[int(identity) for identity in activeCollectionsIdentities.split(
													self.__settingsSeparator)] or []

		activeOverallCollection = foundations.strings.toString(
		self.__settings.getKey(self.__settingsSection, "activeOverallCollection").toString())
		LOGGER.debug("> '{0}' View stored 'Overall' Collection: '{1}'.".format(self.__class__.__name__,
																				activeOverallCollection))
		self.__view.modelSelection[self.__overallCollection] = activeCollectionsIdentities and \
																[activeOverallCollection] or []
		self.__view.restoreModelSelection()
		return True

	def onClose(self):
		"""
		Defines the slot triggered on Framework close.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		self.__view.storeModelSelection()
		self.__settings.setKey(self.__settingsSection,
								"activeCollections",
								self.__settingsSeparator.join((foundations.strings.toString(
								identity) for identity in self.__view.modelSelection[
								"Collections"])))
		self.__settings.setKey(self.__settingsSection,
								"activeOverallCollection",
								self.__settingsSeparator.join((foundations.strings.toString(name)
								for name in self.__view.modelSelection[self.__overallCollection])))
		return True

	def __model__refreshNodes(self):
		"""
		Defines the slot triggered by the Model when Nodes need refresh.
		"""

		self.setCollections()

	def __model__refreshAttributes(self):
		"""
		Refreshes the Model Nodes attributes.
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
		Defines the slot triggered by the Model when data has changed.
		
		:param startIndex: Edited item starting QModelIndex.
		:type startIndex: QModelIndex
		:param endIndex: Edited item ending QModelIndex.
		:type endIndex: QModelIndex
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
		Sets the View actions.
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
		Defines the slot triggered by **'Actions|Umbra|Components|core.collectionsOutliner|Add Content ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.addContentUi()

	def __view_addCollectionAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|core.collectionsOutliner|Add Collection ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.addCollectionUi()

	def __view_removeCollectionsAction__triggered(self, checked):
		"""
		Defines the slot triggered by 
		**'Actions|Umbra|Components|core.collectionsOutliner|Remove Collection(s) ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.removeCollectionsUi()

	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		Defines the slot triggered by the View **selectionModel** when selection changed.

		:param selectedItems: Selected items.
		:type selectedItems: QItemSelection
		:param deselectedItems: Deselected items.
		:type deselectedItems: QItemSelection
		"""

		self.__iblSetsOutliner.refreshNodes.emit()

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.showProcessing("Adding Content ...")
	def addContentUi(self):
		"""
		Adds user defined content to the Database.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
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
		Adds an user defined Collection to the Database.

		:return: Collection name.
		:rtype: unicode

		:note: May require user interaction.
		"""

		collectionInformations, state = QInputDialog.getText(self, "Add Collection", "Enter your Collection name:")
		if not state:
			return False

		if collectionInformations:
			collectionInformations = foundations.strings.toString(collectionInformations).split(",")
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
		Removes user selected Collections from the Database.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
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
		"Are you sure you want to remove '{0}' Collection(s)?".format(", ".join((foundations.strings.toString(collection.name)
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
		Adds a Collection to the Database.

		:param name: Collection name.
		:type name: unicode
		:param collection: Collection name.
		:type collection: unicode
		:return: Method success.
		:rtype: bool
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
		Removes given Collection from the Database.

		:param collection: Collection to remove.
		:type collection: Collection
		:return: Method success.
		:rtype: bool
		"""

		iblSets = sibl_gui.components.core.database.operations.getCollectionsIblSets((collection.id,))
		for iblSet in iblSets:
			LOGGER.info("{0} | Moving '{1}' Ibl Set to default Collection!".format(self.__class__.__name__, iblSet.title))
			iblSet.collection = self.getCollectionId(self.__defaultCollection)

		LOGGER.info("{0} | Removing '{1}' Collection from the Database!".format(self.__class__.__name__, collection.name))
		if sibl_gui.components.core.database.operations.removeCollection(foundations.strings.toString(collection.id)):
			self.refreshNodes.emit()
			self.__iblSetsOutliner.refreshNodes.emit()
			return True
		else:
			raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
			"{0} | Exception raised while removing '{1}' Collection from the Database!".format(self.__class__.__name__,
																								collection.name))
	def getCollections(self):
		"""
		Returns Database Ibl Sets Collections.

		:return: Database Ibl Sets Collections.
		:rtype: list
		"""

		return sibl_gui.components.core.database.operations.getCollectionsByType("IblSets")

	def filterCollections(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		Filters the Database Ibl Sets Collections on given attribute using given pattern.
		
		:param pattern: Filter pattern.
		:type pattern: unicode
		:param attribute: Attribute to filter on.
		:type attribute: unicode
		:param flags: Regex filtering flags.
		:type flags: int

		:return: Filtered Database Ibl Sets Collections.
		:rtype: list
		"""

		try:
			pattern = re.compile(pattern, flags)
		except Exception:
			return list()

		return sibl_gui.components.core.database.operations.filterIblSetsCollections(
		"{0}".format(foundations.strings.toString(pattern.pattern)), attribute, flags)

	def collectionExists(self, name):
		"""
		Returns if given Collection name exists in the Database.

		:param name: Collection name.
		:type name: unicode
		:return: Collection exists.
		:rtype: bool
		"""

		return sibl_gui.components.core.database.operations.collectionExists(name)

	def listCollections(self):
		"""
		Lists Database Ibl Sets Collections names.

		:return: Database Ibl Sets Collections names.
		:rtype: list
		"""

		return [collection.name for collection in self.getCollections()]

	def setCollections(self):
		"""
		Sets the Collections Model nodes.
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
			collectionNode.roles[Qt.DecorationRole] = foundations.common.filterPath(decorationRole)
		overallCollectionNode.updateNodeAttributes()
		rootNode.sortChildren()

		self.__model.initializeModel(rootNode)
		return True

	def getCollectionByName(self, name):
		"""
		Returns Database Ibl Sets Collection with given name.

		:param name: Collection name.
		:type name: unicode
		:return: Database Ibl Sets Collection.
		:rtype: Collection
		"""

		collections = self.filterCollections(r"^{0}$".format(name), "name")
		return foundations.common.getFirstItem(collections)

	def getCollectionsIblSets(self, collections):
		"""
		Gets given Collections Ibl Sets.

		:param collections: Collections to get Ibl Sets from.
		:type collections: list
		:return: Ibl Sets list.
		:rtype: list
		"""

		return [iblSet for iblSet in \
		sibl_gui.components.core.database.operations.getCollectionsIblSets([collection.id for collection in collections])]

	def getCollectionId(self, collection):
		"""
		Returns given Collection id.

		:param collection: Collection to get the id from.
		:type collection: unicode
		:return: Provided Collection id.
		:rtype: int
		"""

		children = self.__model.findChildren(r"^{0}$".format(collection))
		child = foundations.common.getFirstItem(children)
		return child and child.databaseItem.id or None

	def getSelectedNodes(self):
		"""
		Returns the View selected nodes.

		:return: View selected nodes.
		:rtype: dict
		"""

		return self.__view.getSelectedNodes()

	def getSelectedCollectionsNodes(self):
		"""
		Returns the View selected Collections nodes.

		:return: View selected Collections nodes.
		:rtype: list
		"""

		return [node for node in self.getSelectedNodes() if node.family == "Collection"]

	def getSelectedCollections(self):
		"""
		Gets the View selected Collections.

		:return: View selected Collections.
		:rtype: list
		"""

		return [node.databaseItem for node in self.getSelectedCollectionsNodes()]
