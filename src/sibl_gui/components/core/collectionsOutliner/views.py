#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`sibl_gui.components.core.databaseBrowser.databaseBrowser.DatabaseBrowser` Component Interface class Views.

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
import foundations.exceptions
import sibl_gui.ui.views
import umbra.ui.common
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

__all__ = ["LOGGER", "IblSetsCollections_QTreeView"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class IblSetsCollections_QTreeView(sibl_gui.ui.views.Abstract_QTreeView):
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
		self.__treeViewIndentation = 15

		IblSetsCollections_QTreeView.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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

		if not self.readOnly:
			indexAt = self.indexAt(event.pos())
			itemAt = self.model().getNodeIndex(indexAt)

			if not itemAt:
				return

			LOGGER.debug("> Item at drop position: '{0}'.".format(itemAt))
			print itemAt
#			collectionStandardItem = self.model().itemFromIndex(self.model().sibling(indexAt.row(), 0, indexAt))
#			if collectionStandardItem.text() != self.model().overallCollection:
#				collection = collectionStandardItem._datas
#				for iblSet in self.__coreDatabaseBrowser.getSelectedIblSets():
#					LOGGER.info("> Moving '{0}' Ibl Set to '{1}' Collection.".format(iblSet.title, collection.name))
#					iblSet.collection = collection.id
#				if dbCommon.commit(self.__coreDb.dbSession):
#					self.selectionModel().setCurrentIndex(indexAt, QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
		else:
			raise foundations.exceptions.UserError("{0} | Cannot perform action, View has been set read only!".format(self.__class__.__name__))

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.setAutoScroll(True)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setIndentation(self.__treeViewIndentation)
		self.setDragDropMode(QAbstractItemView.DropOnly)
		self.setSortingEnabled(True)

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

	def storeModelSelection(self):
		pass

	def restoreModelSelection(self):
		pass
