#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application views classes.

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
import umbra.ui.views
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

__all__ = ["LOGGER", "storeDefaultViewModelSelection", "restoreDefaultViewModelSelection", "Abstract_QListView", "Abstract_QTreeView"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
def storeDefaultViewModelSelection(view):
	"""
	This method stores the View Model selection.

	:param view: View. ( QWidget )
	:return: Definition success. ( Boolean )
	"""

	LOGGER.debug("> Storing Model selection!")

	view.modelSelection = {"Default" : []}
	for node in view.getSelectedNodes().keys():
		view.modelSelection["Default"].append(node.id.value)
	return True

@core.executionTrace
def restoreDefaultModelSelection(view):
	"""
	This method restores the View Model selection.

	:param view: View. ( QWidget )
	:return: Method success. ( Boolean )
	"""

	LOGGER.debug("> Restoring Model selection!")

	if not view.modelSelection:
		return

	selection = view.modelSelection.get("Default", None)
	if not selection:
		return

	indexes = []
	for i in range(view.model().rowCount()):
		index = view.model().index(i)
		node = view.model().getNode(index)
		node.id.value in selection and indexes.append(index)

	if view.selectionModel():
		view.selectionModel().clear()
		for index in indexes:
			view.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
	return True

class Abstract_QListView(umbra.ui.views.Abstract_QListView):
	"""
	This class used as base by others Application views classes.
	"""

	@core.executionTrace
	def __init__(self, parent=None, model=None, readOnly=False):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param model: Model. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.views.Abstract_QListView.__init__(self, parent, readOnly)

		# --- Setting class attributes. ---
		self.__modelSelection = []

		self.setModel(model)

		Abstract_QListView.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("modelSelection", value)
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
	def setModel(self, model):
		"""
		This method reimplements the **QListView.setModel** method.
		
		:param model: Model to set. ( QObject )
		"""

		if not model:
			return

		umbra.ui.views.Abstract_QListView.setModel(self, model)

		# Signals / Slots.
		self.model().modelAboutToBeReset.connect(self.__model__modelAboutToBeReset)
		self.model().modelReset.connect(self.__model__modelReset)

	@core.executionTrace
	def __model__modelAboutToBeReset(self):
		"""
		This method is triggered when the Model is about to be reset.
		"""

		self.storeModelSelection()

	@core.executionTrace
	def __model__modelReset(self):
		"""
		This method is triggered when the Model is changed.
		"""

		self.restoreModelSelection()

	@core.executionTrace
	def storeModelSelection(self):
		"""
		This method stores the Model selection.

		:return: Method success. ( Boolean )
		"""

		return storeDefaultViewModelSelection(self)

	@core.executionTrace
	def restoreModelSelection(self):
		"""
		This method restores the Model selection.

		:return: Method success. ( Boolean )
		"""

		return restoreDefaultModelSelection(self)

class Abstract_QTreeView(umbra.ui.views.Abstract_QTreeView):
	"""
	This class used as base by others Application views classes.
	"""

	@core.executionTrace
	def __init__(self, parent=None, model=None, readOnly=False):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param model: Model. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.views.Abstract_QTreeView.__init__(self, parent, readOnly)

		# --- Setting class attributes. ---
		self.__modelSelection = []

		self.setModel(model)

		Abstract_QTreeView.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("modelSelection", value)
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
	def setModel(self, model):
		"""
		This method reimplements the **QListView.setModel** method.
		
		:param model: Model to set. ( QObject )
		"""

		if not model:
			return

		umbra.ui.views.Abstract_QTreeView.setModel(self, model)

		# Signals / Slots.
		self.model().modelAboutToBeReset.connect(self.__model__modelAboutToBeReset)
		self.model().modelReset.connect(self.__model__modelReset)

	@core.executionTrace
	def __model__modelAboutToBeReset(self):
		"""
		This method is triggered when the Model is about to be reset.
		"""

		self.storeModelSelection()

	@core.executionTrace
	def __model__modelReset(self):
		"""
		This method is triggered when the Model is changed.
		"""

		self.restoreModelSelection()

	@core.executionTrace
	def storeModelSelection(self):
		"""
		This method stores the Model selection.

		:return: Method success. ( Boolean )
		"""

		return storeDefaultViewModelSelection(self)

	@core.executionTrace
	def restoreModelSelection(self):
		"""
		This method restores the Model selection.

		:return: Method success. ( Boolean )
		"""

		return restoreDefaultModelSelection(self)
