#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**collections_outliner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`CollectionsOutliner` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

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
import umbra.ui.widgets.message_box as message_box
from manager.QWidget_component import QWidgetComponentFactory
from sibl_gui.components.core.collections_outliner.models import CollectionsModel
from sibl_gui.components.core.collections_outliner.nodes import OverallCollectionNode
from sibl_gui.components.core.collections_outliner.views import IblSetsCollections_QTreeView
from sibl_gui.components.core.database.nodes import CollectionNode
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "CollectionsOutliner"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Collections_Outliner.ui")

class CollectionsOutliner(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.core.collections_outliner.collections_outliner` Component Interface class.
	| It defines methods for Database Collections management.
	"""

	# Custom signals definitions.
	refresh_nodes = pyqtSignal()
	"""
	This signal is emited by the :class:`CollectionsOutliner` class when :obj:`CollectionsOutliner.model` class
	property Model Nodes needs to be refreshed.
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

		self.__ui_resources_directory = "resources"
		self.__ui_default_collection_image = "Default_Collection.png"
		self.__ui_user_collection_image = "User_Collection.png"
		self.__dock_area = 1

		self.__engine = None
		self.__settings = None
		self.__settings_section = None
		self.__settings_separator = ","

		self.__ibl_sets_outliner = None

		self.__model = None
		self.__view = None
		self.__overall_collection = "Overall"
		self.__default_collection = "Default"
		self.__ibl_sets_count_label = "Ibl Sets"
		self.__headers = OrderedDict([("Collections", "name"),
										(self.__ibl_sets_count_label, "count"),
										("Comment", "comment")])

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
	def ui_default_collection_image(self):
		"""
		Property for **self.__ui_default_collection_image** attribute.

		:return: self.__ui_default_collection_image.
		:rtype: unicode
		"""

		return self.__ui_default_collection_image

	@ui_default_collection_image.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_default_collection_image(self, value):
		"""
		Setter for **self.__ui_default_collection_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_default_collection_image"))

	@ui_default_collection_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_default_collection_image(self):
		"""
		Deleter for **self.__ui_default_collection_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_default_collection_image"))

	@property
	def ui_user_collection_image(self):
		"""
		Property for **self.__ui_user_collection_image** attribute.

		:return: self.__ui_user_collection_image.
		:rtype: unicode
		"""

		return self.__ui_user_collection_image

	@ui_user_collection_image.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_user_collection_image(self, value):
		"""
		Setter for **self.__ui_user_collection_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_user_collection_image"))

	@ui_user_collection_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_user_collection_image(self):
		"""
		Deleter for **self.__ui_user_collection_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_user_collection_image"))

	@property
	def dock_area(self):
		"""
		Property for **self.__dock_area** attribute.

		:return: self.__dock_area.
		:rtype: int
		"""

		return self.__dock_area

	@dock_area.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def dock_area(self, value):
		"""
		Setter for **self.__dock_area** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dock_area"))

	@dock_area.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def dock_area(self):
		"""
		Deleter for **self.__dock_area** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dock_area"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settings_section(self):
		"""
		Property for **self.__settings_section** attribute.

		:return: self.__settings_section.
		:rtype: unicode
		"""

		return self.__settings_section

	@settings_section.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_section(self, value):
		"""
		Setter for **self.__settings_section** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings_section"))

	@settings_section.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_section(self):
		"""
		Deleter for **self.__settings_section** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings_section"))

	@property
	def settings_separator(self):
		"""
		Property for **self.__settings_separator** attribute.

		:return: self.__settings_separator.
		:rtype: unicode
		"""

		return self.__settings_separator

	@settings_separator.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_separator(self, value):
		"""
		Setter for **self.__settings_separator** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings_separator"))

	@settings_separator.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_separator(self):
		"""
		Deleter for **self.__settings_separator** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings_separator"))

	@property
	def ibl_sets_outliner(self):
		"""
		Property for **self.__ibl_sets_outliner** attribute.

		:return: self.__ibl_sets_outliner.
		:rtype: QWidget
		"""

		return self.__ibl_sets_outliner

	@ibl_sets_outliner.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_outliner(self, value):
		"""
		Setter for **self.__ibl_sets_outliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ibl_sets_outliner"))

	@ibl_sets_outliner.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_outliner(self):
		"""
		Deleter for **self.__ibl_sets_outliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ibl_sets_outliner"))

	@property
	def model(self):
		"""
		Property for **self.__model** attribute.

		:return: self.__model.
		:rtype: CollectionsModel
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		Setter for **self.__model** attribute.

		:param value: Attribute value.
		:type value: CollectionsModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	def overall_collection(self):
		"""
		Property for **self.__overall_collection** attribute.

		:return: self.__overall_collection.
		:rtype: unicode
		"""

		return self.__overall_collection

	@overall_collection.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def overall_collection(self, value):
		"""
		Setter for **self.__overall_collection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "overall_collection"))

	@overall_collection.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def overall_collection(self):
		"""
		Deleter for **self.__overall_collection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "overall_collection"))

	@property
	def default_collection(self):
		"""
		Property for **self.__default_collection** attribute.

		:return: self.__default_collection.
		:rtype: unicode
		"""

		return self.__default_collection

	@default_collection.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_collection(self, value):
		"""
		Setter for **self.__default_collection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_collection"))

	@default_collection.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_collection(self):
		"""
		Deleter for **self.__default_collection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_collection"))

	@property
	def ibl_sets_count_label(self):
		"""
		Property for **self.__ibl_sets_count_label** attribute.

		:return: self.__ibl_sets_count_label.
		:rtype: unicode
		"""

		return self.__ibl_sets_count_label

	@ibl_sets_count_label.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_count_label(self, value):
		"""
		Setter for **self.__ibl_sets_count_label** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ibl_sets_count_label"))

	@ibl_sets_count_label.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_count_label(self):
		"""
		Deleter for **self.__ibl_sets_count_label** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ibl_sets_count_label"))

	@property
	def headers(self):
		"""
		Property for **self.__headers** attribute.

		:return: self.__headers.
		:rtype: OrderedDict
		"""

		return self.__headers

	@headers.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		Setter for **self.__headers** attribute.

		:param value: Attribute value.
		:type value: OrderedDict
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

	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Engine to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__ui_resources_directory = os.path.join(os.path.dirname(__file__), self.__ui_resources_directory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settings_section = self.name

		self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]

		self.activated = True
		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		Deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	def initialize_ui(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__engine.parameters.database_read_only and \
		LOGGER.info("{0} | Model edition deactivated by '{1}' command line parameter value!".format(self.__class__.__name__,
																									"database_read_only"))
		self.__model = CollectionsModel(self, horizontal_headers=self.__headers)
		self.set_collections()

		self.Collections_Outliner_treeView.setParent(None)
		self.Collections_Outliner_treeView = IblSetsCollections_QTreeView(self,
																		self.__model,
																		self.__engine.parameters.database_read_only)
		self.Collections_Outliner_treeView.setObjectName("Collections_Outliner_treeView")
		self.Collections_Outliner_dockWidgetContents_gridLayout.addWidget(self.Collections_Outliner_treeView, 0, 0)
		self.__view = self.Collections_Outliner_treeView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__view_add_actions()

		# Signals / Slots.
		self.__engine.images_caches.QIcon.content_added.connect(self.__view.viewport().update)
		self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.refresh_nodes.connect(self.__model__refresh_nodes)
		if not self.__engine.parameters.database_read_only:
			self.__model.dataChanged.connect(self.__model__dataChanged)

		self.initialized_ui = True
		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def uninitialize_ui(self):
		"""
		Uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def add_widget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dock_area), self)

		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def remove_widget(self):
		"""
		Removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	def on_startup(self):
		"""
		Defines the slot triggered on Framework startup.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'on_startup' method.".format(self.__class__.__name__))

		if not self.__engine.parameters.database_read_only:
			not self.get_collections() and self.add_collection(self.__default_collection, "Default Collection")
		else:
			LOGGER.info("{0} | Database default Collection wizard deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "database_read_only"))

		active_collections_identities = foundations.strings.to_string(
		self.__settings.get_key(self.__settings_section, "active_collections").toString())
		LOGGER.debug("> '{0}' View stored selected Collections identities '{1}'.".format(self.__class__.__name__,
																						active_collections_identities))
		self.__view.model_selection["collections"] = active_collections_identities and \
													[int(identity) for identity in active_collections_identities.split(
													self.__settings_separator)] or []

		active_overall_collection = foundations.strings.to_string(
		self.__settings.get_key(self.__settings_section, "active_overall_collection").toString())
		LOGGER.debug("> '{0}' View stored 'Overall' Collection: '{1}'.".format(self.__class__.__name__,
																				active_overall_collection))
		self.__view.model_selection[self.__overall_collection] = active_collections_identities and \
																[active_overall_collection] or []
		self.__view.restore_model_selection()
		return True

	def on_close(self):
		"""
		Defines the slot triggered on Framework close.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'on_close' method.".format(self.__class__.__name__))

		self.__view.store_model_selection()
		self.__settings.set_key(self.__settings_section,
								"active_collections",
								self.__settings_separator.join((foundations.strings.to_string(
								identity) for identity in self.__view.model_selection[
								"collections"])))
		self.__settings.set_key(self.__settings_section,
								"active_overall_collection",
								self.__settings_separator.join((foundations.strings.to_string(name)
								for name in self.__view.model_selection[self.__overall_collection])))
		return True

	def __model__refresh_nodes(self):
		"""
		Defines the slot triggered by the Model when Nodes need refresh.
		"""

		self.set_collections()

	def __model__refresh_attributes(self):
		"""
		Refreshes the Model Nodes attributes.
		"""

		for node in foundations.walkers.nodes_walker(self.__model.root_node):
			if not node.family == "Collection":
				continue

			node.update_node_attributes()

		overall_collection_node = \
		foundations.common.get_first_item(self.__model.find_children("^{0}$".format(self.__overall_collection)))
		overall_collection_node.update_node_attributes()

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
											foundations.exceptions.UserError)
	def __model__dataChanged(self, start_index, end_index):
		"""
		Defines the slot triggered by the Model when data has changed.

		:param start_index: Edited item starting QModelIndex.
		:type start_index: QModelIndex
		:param end_index: Edited item ending QModelIndex.
		:type end_index: QModelIndex
		"""

		collection_node = self.__model.get_node(start_index)
		if collection_node.family != "Collection":
			return

		if start_index.column() == 0:
			if self.collection_exists(collection_node.name):
				self.__engine.notifications_manager.warnify(
				"{0} | '{1}' Collection name already exists in Database!".format(self.__class__.__name__,
																				collection_node.name))
				return

			if not collection_node.name:
				collection_node.update_node()
				raise foundations.exceptions.UserError(
				"{0} | Exception while editing a Collection field: Cannot use an empty value!".format(
				self.__class__.__name__))

		collection_node.update_database_item()
		collection_node.update_tool_tip()

		sibl_gui.components.core.database.operations.commit()

	def __view_add_actions(self):
		"""
		Sets the View actions.
		"""

		if not self.__engine.parameters.database_read_only:
			self.__view.addAction(self.__engine.actions_manager.register_action(
			"Actions|Umbra|Components|core.collections_outliner|Add Content ...",
			slot=self.__view_add_content_action__triggered))
			self.__view.addAction(self.__engine.actions_manager.register_action(
			"Actions|Umbra|Components|core.collections_outliner|Add Collection ...",
			slot=self.__view_add_collectionAction__triggered))
			self.__view.addAction(self.__engine.actions_manager.register_action(
			"Actions|Umbra|Components|core.collections_outliner|Remove Collection(s) ...",
			slot=self.__view_remove_collectionsAction__triggered))
		else:
			LOGGER.info(
			"{0} | Collections Database alteration capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "database_read_only"))

	def __view_add_content_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|core.collections_outliner|Add Content ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.add_content_ui()

	def __view_add_collectionAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|core.collections_outliner|Add Collection ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.add_collection_ui()

	def __view_remove_collectionsAction__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|core.collections_outliner|Remove Collection(s) ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.remove_collections_ui()

	def __view_selectionModel__selectionChanged(self, selected_items, deselected_items):
		"""
		Defines the slot triggered by the View **selectionModel** when selection changed.

		:param selected_items: Selected items.
		:type selected_items: QItemSelection
		:param deselected_items: Deselected items.
		:type deselected_items: QItemSelection
		"""

		self.__ibl_sets_outliner.refresh_nodes.emit()

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
	@umbra.engine.show_processing("Adding Content ...")
	def add_content_ui(self):
		"""
		Adds user defined content to the Database.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		collection = self.add_collection_ui()
		if not collection:
			return False

		directory = umbra.ui.common.store_last_browsed_path((QFileDialog.getExistingDirectory(self,
																						"Add Content:",
																						RuntimeGlobals.last_browsed_path)))
		if not directory:
			return False

		LOGGER.debug("> Chosen directory path: '{0}'.".format(directory))
		if self.__ibl_sets_outliner.add_directory(directory, self.get_collection_id(collection)):
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
			self.__class__.__name__, directory))

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
											foundations.exceptions.UserError,
											Exception)
	@umbra.engine.show_processing("Adding Collection ...")
	def add_collection_ui(self):
		"""
		Adds an user defined Collection to the Database.

		:return: Collection name.
		:rtype: unicode

		:note: May require user interaction.
		"""

		collection_informations, state = QInputDialog.getText(self, "Add Collection", "Enter your Collection name:")
		if not state:
			return False

		if collection_informations:
			collection_informations = foundations.strings.to_string(collection_informations).split(",")
			name = collection_informations[0].strip()
			if name != self.__overall_collection:
				if not self.collection_exists(name):
					comment = len(collection_informations) == 1 and "Double click to set a comment!" or \
					collection_informations[1].strip()
					if self.add_collection(name, comment):
						self.__view.selectionModel().setCurrentIndex(self.__model.get_node_index(
						foundations.common.get_first_item(self.__model.find_children(r"^{0}$".format(name)))),
						QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
						return name
					else:
						raise Exception("{0} | Exception raised while adding '{1}' Collection to the Database!".format(
						self.__class__.__name__, name))
				else:
					self.__engine.notifications_manager.warnify(
					"{0} | '{1}' Collection already exists in Database!".format(self.__class__.__name__, name))
			else:
				raise foundations.exceptions.UserError(
				"{0} | Exception while adding a Collection to the Database: Cannot use '{1}' as Collection name!".format(
				self.__class__.__name__, self.__model.overall_collection))
		else:
			raise foundations.exceptions.UserError(
			"{0} | Exception while adding a Collection to the Database: Cannot use an empty name!".format(
			self.__class__.__name__))

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
	@umbra.engine.encapsulate_processing
	def remove_collections_ui(self):
		"""
		Removes user selected Collections from the Database.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		selected_nodes = self.get_selected_nodes().keys()
		if self.__overall_collection in (node.name for node in selected_nodes) or \
		self.__default_collection in (node.name for node in selected_nodes):
			self.__engine.notifications_manager.warnify(
			"{0} | '{1}' and '{2}' Collections cannot be removed!".format(self.__class__.__name__,
																	self.__overall_collection,
																	self.__default_collection))

		selected_collections = [collection
								for collection in self.get_selected_collections()
								if collection.name != self.__default_collection]
		if not selected_collections:
			return False

		if message_box.message_box("Question", "Question",
		"Are you sure you want to remove '{0}' Collection(s)?".format(", ".join((foundations.strings.to_string(collection.name)
																	for collection in selected_collections))),
		buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.start_processing("Removing Collections ...", len(selected_collections))
			success = True
			for collection in selected_collections:
				success *= self.remove_collection(collection) or False
				self.__engine.step_processing()
			self.__engine.stop_processing()
			self.__view.selectionModel().setCurrentIndex(self.__model.index(0, 0),
			QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
			if success:
				return True
			else:
				raise Exception("{0} | Exception raised while removing '{1}' Collections from the Database!".format(
				self.__class__.__name__, ", ". join((collection.name for collection in selected_collections))))

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError,
											sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def add_collection(self, name, comment="Double click to set a comment!"):
		"""
		Adds a Collection to the Database.

		:param name: Collection name.
		:type name: unicode
		:param collection: Collection name.
		:type collection: unicode
		:return: Method success.
		:rtype: bool
		"""

		if name != self.__overall_collection:
			if not self.collection_exists(name):
				LOGGER.info("{0} | Adding '{1}' Collection to the Database!".format(self.__class__.__name__, name))
				if sibl_gui.components.core.database.operations.add_collection(name, "ibl_sets", comment):
					self.refresh_nodes.emit()
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
		"{0} | Cannot use '{1}' as Collection name!".format(self.__class__.__name__, self.__model.overall_collection))

	@foundations.exceptions.handle_exceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def remove_collection(self, collection):
		"""
		Removes given Collection from the Database.

		:param collection: Collection to remove.
		:type collection: Collection
		:return: Method success.
		:rtype: bool
		"""

		ibl_sets = sibl_gui.components.core.database.operations.get_collections_ibl_sets((collection.id,))
		for ibl_set in ibl_sets:
			LOGGER.info("{0} | Moving '{1}' Ibl Set to default Collection!".format(self.__class__.__name__, ibl_set.title))
			ibl_set.collection = self.get_collection_id(self.__default_collection)

		LOGGER.info("{0} | Removing '{1}' Collection from the Database!".format(self.__class__.__name__, collection.name))
		if sibl_gui.components.core.database.operations.remove_collection(foundations.strings.to_string(collection.id)):
			self.refresh_nodes.emit()
			self.__ibl_sets_outliner.refresh_nodes.emit()
			return True
		else:
			raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
			"{0} | Exception raised while removing '{1}' Collection from the Database!".format(self.__class__.__name__,
																								collection.name))
	def get_collections(self):
		"""
		Returns Database Ibl Sets Collections.

		:return: Database Ibl Sets Collections.
		:rtype: list
		"""

		return sibl_gui.components.core.database.operations.get_collections_by_type("ibl_sets")

	def filter_collections(self, pattern, attribute, flags=re.IGNORECASE):
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

		return sibl_gui.components.core.database.operations.filter_ibl_sets_collections(
		"{0}".format(foundations.strings.to_string(pattern.pattern)), attribute, flags)

	def collection_exists(self, name):
		"""
		Returns if given Collection name exists in the Database.

		:param name: Collection name.
		:type name: unicode
		:return: Collection exists.
		:rtype: bool
		"""

		return sibl_gui.components.core.database.operations.collection_exists(name)

	def list_collections(self):
		"""
		Lists Database Ibl Sets Collections names.

		:return: Database Ibl Sets Collections names.
		:rtype: list
		"""

		return [collection.name for collection in self.get_collections()]

	def set_collections(self):
		"""
		Sets the Collections Model nodes.
		"""

		node_flags = attributes_flags = self.__engine.parameters.database_read_only and \
		int(Qt.ItemIsSelectable | Qt.ItemIsEnabled) or int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
		collections = self.get_collections()

		root_node = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")

		overall_collection_node = OverallCollectionNode(name=self.__overall_collection,
													parent=root_node,
													node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
													attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

		for collection in collections:
			decoration_role = os.path.join(self.__ui_resources_directory, self.__ui_user_collection_image)
			if collection.name == self.__default_collection:
				collection_node = CollectionNode(collection,
												name=collection.name,
												parent=overall_collection_node,
												node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
												attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
				decoration_role = os.path.join(self.__ui_resources_directory, self.__ui_default_collection_image)
			else:
				collection_node = CollectionNode(collection,
												name=collection.name,
												parent=overall_collection_node,
												node_flags=node_flags,
												attributes_flags=attributes_flags)
			collection_node.roles[Qt.DecorationRole] = foundations.common.filter_path(decoration_role)
		overall_collection_node.update_node_attributes()
		root_node.sort_children()

		self.__model.initialize_model(root_node)
		return True

	def get_collection_by_name(self, name):
		"""
		Returns Database Ibl Sets Collection with given name.

		:param name: Collection name.
		:type name: unicode
		:return: Database Ibl Sets Collection.
		:rtype: Collection
		"""

		collections = self.filter_collections(r"^{0}$".format(name), "name")
		return foundations.common.get_first_item(collections)

	def get_collections_ibl_sets(self, collections):
		"""
		Gets given Collections Ibl Sets.

		:param collections: Collections to get Ibl Sets from.
		:type collections: list
		:return: Ibl Sets list.
		:rtype: list
		"""

		return [ibl_set for ibl_set in \
		sibl_gui.components.core.database.operations.get_collections_ibl_sets([collection.id for collection in collections])]

	def get_collection_id(self, collection):
		"""
		Returns given Collection id.

		:param collection: Collection to get the id from.
		:type collection: unicode
		:return: Provided Collection id.
		:rtype: int
		"""

		children = self.__model.find_children(r"^{0}$".format(collection))
		child = foundations.common.get_first_item(children)
		return child and child.database_item.id or None

	def get_selected_nodes(self):
		"""
		Returns the View selected nodes.

		:return: View selected nodes.
		:rtype: dict
		"""

		return self.__view.get_selected_nodes()

	def get_selected_collections_nodes(self):
		"""
		Returns the View selected Collections nodes.

		:return: View selected Collections nodes.
		:rtype: list
		"""

		return [node for node in self.get_selected_nodes() if node.family == "Collection"]

	def get_selected_collections(self):
		"""
		Gets the View selected Collections.

		:return: View selected Collections.
		:rtype: list
		"""

		return [node.database_item for node in self.get_selected_collections_nodes()]
