#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_gui.components.core.collections_outliner.collections_outliner.CollectionsOutliner`
	Component Interface class Views.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import pickle
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import sibl_gui.components.core.database.operations
import sibl_gui.ui.views
import umbra.exceptions

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "IblSetsCollections_QTreeView"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class IblSetsCollections_QTreeView(sibl_gui.ui.views.Abstract_QTreeView):
	"""
	Defines the view for Database Collections.
	"""

	def __init__(self, parent, model=None, read_only=False, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param model: Model.
		:type model: QObject
		:param read_only: View is read only.
		:type read_only: bool
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.views.Abstract_QTreeView.__init__(self, parent, model, read_only, message)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__tree_view_indentation = 15

		IblSetsCollections_QTreeView.__initialize_ui(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def tree_view_indentation(self):
		"""
		Property for **self.__tree_view_indentation** attribute.

		:return: self.__tree_view_indentation.
		:rtype: int
		"""

		return self.__tree_view_indentation

	@tree_view_indentation.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def tree_view_indentation(self, value):
		"""
		Setter for **self.__tree_view_indentation** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tree_view_indentation"))

	@tree_view_indentation.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def tree_view_indentation(self):
		"""
		Deleter for **self.__tree_view_indentation** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tree_view_indentation"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def dragEnterEvent(self, event):
		"""
		Reimplements the :meth:`sibl_gui.ui.views.Abstract_QTreeView.dragEnterEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		if event.mimeData().hasFormat("application/x-umbragraphmodeldatalist"):
			LOGGER.debug("> '{0}' drag event type accepted!".format("application/x-umbragraphmodeldatalist"))
			event.accept()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		"""
		Reimplements the :meth:`sibl_gui.ui.views.Abstract_QTreeView.dragMoveEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		pass

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
											foundations.exceptions.DirectoryExistsError,
											foundations.exceptions.UserError)
	def dropEvent(self, event):
		"""
		Reimplements the :meth:`sibl_gui.ui.views.Abstract_QTreeView.dropEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		if not self.read_only:
			index_at = self.indexAt(event.pos())
			collection_node = self.model().get_node(index_at)

			if not collection_node:
				return

			if collection_node.name in (self.__container.overall_collection, "InvisibleRootNode"):
				return

			LOGGER.debug("> Item at drop position: '{0}'.".format(collection_node))

			database_session = sibl_gui.components.core.database.operations.get_session()

			nodes = pickle.loads(event.mimeData().data("application/x-umbragraphmodeldatalist"))
			for node in nodes:
				if node.family != "IblSet":
					continue

				node._AbstractDatabaseNode__database_item = database_session.merge(node.database_item)
				if collection_node.database_item.id != node.database_item.collection:
					LOGGER.info("> Moving '{0}' Ibl Set to '{1}' Collection.".format(node.database_item.title,
																					collection_node.database_item.name))
					node.database_item.collection = collection_node.database_item.id

			if sibl_gui.components.core.database.operations.commit():
				self.__container.refresh_nodes.emit()
		else:
			raise foundations.exceptions.UserError("{0} | Cannot perform action, View has been set read only!".format(
			self.__class__.__name__))

	def __initialize_ui(self):
		"""
		Initializes the Widget ui.
		"""

		self.setAutoScroll(True)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setIndentation(self.__tree_view_indentation)
		self.setDragDropMode(QAbstractItemView.DropOnly)

		self.setSortingEnabled(True)
		self.sortByColumn(0, Qt.AscendingOrder)

		self.__set_default_ui_state()

		# Signals / Slots.
		self.model().modelReset.connect(self.__set_default_ui_state)

	def __set_default_ui_state(self):
		"""
		Sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

		if not self.model():
			return

		self.expandAll()

		for column in range(len(self.model().horizontal_headers)):
			self.resizeColumnToContents(column)

	def store_model_selection(self):
		"""
		Stores the Model selection.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Storing Model selection!")

		self.model_selection = {self.__container.overall_collection : [], "collections" : []}
		for node in self.get_selected_nodes():
			if node.name == self.__container.overall_collection:
				self.model_selection[self.__container.overall_collection].append(node.name)
			elif node.family == "Collection":
				self.model_selection["collections"].append(node.id.value)
		return True

	def restore_model_selection(self):
		"""
		Restores the Model selection.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Restoring Model selection!")

		if not self.model_selection:
			return False

		selection = self.model_selection.get(self.__container.overall_collection, None) or self.model_selection.get("collections", None)
		if not selection:
			return False

		indexes = []
		for node in foundations.walkers.nodes_walker(self.model().root_node):
			if node.family == "Collection":
				self.model_selection.get("collections", None) and \
				node.id.value in self.model_selection["collections"] and indexes.append(self.model().get_node_index(node))
			else:
				self.model_selection.get(self.__container.overall_collection, None) and \
				node.name in self.model_selection[self.__container.overall_collection] and indexes.append(self.model().get_node_index(node))

		return self.select_indexes(indexes)
