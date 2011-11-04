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

__all__ = ["LOGGER", "Thumbnails_QListView", "Columns_QListView", "Details_QTreeView"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Thumbnails_QListView(sibl_gui.ui.views.Abstract_QListView):
	"""
	This class is used to display Database Ibl Sets as thumbnails.
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

		sibl_gui.ui.views.Abstract_QListView.__init__(self, parent, model, readOnly)

		# --- Setting class attributes. ---
		self.__listViewSpacing = 24
		self.__listViewMargin = 32
		self.__listViewIconSize = 128

		Thumbnails_QListView.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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

		self.__setDefaultUiState()

		# Signals / Slots.
		self.model().modelReset.connect(self.__setDefaultUiState)

	@core.executionTrace
	def __setDefaultUiState(self):
		"""
		This method sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

		self.setIconSize(QSize(self.__listViewIconSize, self.__listViewIconSize))
		self.setGridSize(QSize(self.__listViewIconSize + self.__listViewSpacing, self.__listViewIconSize + self.__listViewMargin))

class Columns_QListView(sibl_gui.ui.views.Abstract_QListView):
	"""
	This class is used to display Database Ibl Sets in columns.
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

		sibl_gui.ui.views.Abstract_QListView.__init__(self, parent, model, readOnly)

		Columns_QListView.__initializeUi(self)

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.setAutoScroll(True)
		self.setResizeMode(QListView.Adjust)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setDragDropMode(QAbstractItemView.DragOnly)

		self.__setDefaultUiState()

		# Signals / Slots.
		self.model().modelReset.connect(self.__setDefaultUiState)

	@core.executionTrace
	def __setDefaultUiState(self):
		"""
		This method sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

class Details_QTreeView(sibl_gui.ui.views.Abstract_QTreeView):
	"""
	This class is used to display Database Ibl Sets columns.
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

		Details_QTreeView.__initializeUi(self)

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

		for column in range(len(self.model().horizontalHeaders)):
			self.resizeColumnToContents(column)
