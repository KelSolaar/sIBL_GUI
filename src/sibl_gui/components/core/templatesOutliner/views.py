#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`sibl_gui.components.core.templatesOutliner.templatesOutliner.TemplatesOutliner` Component Interface class Views.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.namespace
import foundations.exceptions
import sibl_gui.ui.views
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

__all__ = ["LOGGER", "Templates_QTreeView"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Templates_QTreeView(sibl_gui.ui.views.Abstract_QTreeView):
	"""
	This class is used to display Database Collections.
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

		sibl_gui.ui.views.Abstract_QTreeView.__init__(self, parent, model, readOnly)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__treeViewIndentation = 15

		Templates_QTreeView.__initializeUi(self)

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

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.setAutoScroll(True)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setIndentation(self.__treeViewIndentation)
		self.setDragDropMode(QAbstractItemView.DragOnly)

		self.setSortingEnabled(True)
		self.sortByColumn(0, Qt.AscendingOrder)

		self.__setDefaultUiState()

		# Signals / Slots.
		self.model().modelReset.connect(self.__setDefaultUiState)

	@core.executionTrace
	def __setDefaultUiState(self):
		"""
		This method sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

		if not self.model():
			return

		self.expandAll()

		for column in range(len(self.model().horizontalHeaders)):
			self.resizeColumnToContents(column)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeModelSelection(self):
		"""
		This method stores the Model selection.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing Model selection!")

		self.modelSelection = {"Templates" : [], "Collections" : [], "Softwares" : []}
		for node in self.getSelectedNodes().keys():
			if node.family == "Template":
				self.modelSelection["Templates"].append(node.id.value)
			elif node.family == "Collection":
				self.modelSelection["Collections"].append(node.id.value)
			elif node.family == "Software":
				self.modelSelection["Softwares"].append(foundations.namespace.setNamespace(node.parent.id.value, node.name))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreModelSelection(self):
		"""
		This method restores the Model selection.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Restoring Model selection!")

		if not self.modelSelection:
			return

		selection = self.modelSelection.get("Templates", None) or self.modelSelection.get("Collections", None) or self.modelSelection.get("Softwares", None)
		if not selection:
			return

		indexes = []
		for node in foundations.walkers.nodesWalker(self.model().rootNode):
			if node.family == "Template":
				node.id.value in self.modelSelection["Templates"] and indexes.append(self.model().getNodeIndex(node))
			elif node.family == "Collection":
				node.id.value in self.modelSelection["Collections"] and indexes.append(self.model().getNodeIndex(node))
			elif node.family == "Software":
				for item in self.modelSelection["Softwares"]:
					parentId, name = item.split(foundations.namespace.NAMESPACE_SPLITTER)
					for collection in self.model().rootNode.children:
						if not str(collection.id.value) == parentId:
							continue

						for software in collection.children:
							if software.name == name:
								indexes.append(self.model().getNodeIndex(software))

		if self.selectionModel():
			self.selectionModel().clear()
			for index in indexes:
				self.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
		return True
