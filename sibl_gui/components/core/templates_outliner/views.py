#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_gui.components.core.templates_outliner.templates_outliner.TemplatesOutliner`
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
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.namespace
import foundations.exceptions
import foundations.strings
import foundations.verbose
import sibl_gui.ui.views

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Templates_QTreeView"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Templates_QTreeView(sibl_gui.ui.views.Abstract_QTreeView):
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

		Templates_QTreeView.__initialize_ui(self)

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
	def __initialize_ui(self):
		"""
		Initializes the Widget ui.
		"""

		self.setAutoScroll(True)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setIndentation(self.__tree_view_indentation)
		self.setDragDropMode(QAbstractItemView.DragOnly)

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

		self.model_selection = {"templates" : [], "collections" : [], "Softwares" : []}
		for node in self.get_selected_nodes():
			if node.family == "Template":
				self.model_selection["templates"].append(node.id.value)
			elif node.family == "Collection":
				self.model_selection["collections"].append(node.id.value)
			elif node.family == "Software":
				self.model_selection["Softwares"].append(foundations.namespace.set_namespace(node.parent.id.value, node.name))
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

		selection = self.model_selection.get("templates", None) or self.model_selection.get("collections", None) or \
		self.model_selection.get("Softwares", None)
		if not selection:
			return False

		indexes = []
		for node in foundations.walkers.nodes_walker(self.model().root_node):
			if node.family == "Template":
				self.model_selection.get("templates", None) and node.id.value in self.model_selection["templates"] and \
				indexes.append(self.model().get_node_index(node))
			elif node.family == "Collection":
				self.model_selection.get("collections", None) and node.id.value in self.model_selection["collections"] and \
				indexes.append(self.model().get_node_index(node))
			elif node.family == "Software":
				for item in self.model_selection["Softwares"]:
					parentId, name = item.split(foundations.namespace.NAMESPACE_SPLITTER)
					for collection in self.model().root_node.children:
						if not foundations.strings.to_string(collection.id.value) == parentId:
							continue

						for software in collection.children:
							if software.name == name:
								indexes.append(self.model().get_node_index(software))

		return self.select_indexes(indexes)
