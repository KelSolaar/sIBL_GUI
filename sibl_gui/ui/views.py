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

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import foundations.walkers
import umbra.ui.views

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"storeViewModelSelection",
			"restoreViewModelSelection",
			"Abstract_QListView",
			"Abstract_QTreeView"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def storeViewModelSelection(view):
	"""
	This method stores the View Model selection.

	:param view: View. ( QWidget )
	:return: Definition success. ( Boolean )
	"""

	LOGGER.debug("> Storing Model selection!")

	view.modelSelection = {"Default" : []}
	for node in view.getSelectedNodes():
		view.modelSelection["Default"].append(node.id.value)
	return True

@foundations.exceptions.exceptionsHandler(None, False, Exception)
def restoreViewModelSelection(view):
	"""
	This method restores the View Model selection.

	:param view: View. ( QWidget )
	:return: Method success. ( Boolean )
	"""

	LOGGER.debug("> Restoring Model selection!")

	if not view.modelSelection:
		return False

	selection = view.modelSelection.get("Default", None)
	if not selection:
		return False

	indexes = []
	for node in foundations.walkers.nodesWalker(view.model().rootNode):
		node.id.value in selection and indexes.append(view.model().getNodeIndex(node))

	return umbra.ui.views.selectViewIndexes(view, indexes)

class Abstract_QListView(umbra.ui.views.Abstract_QListView):
	"""
	This class used as base by others Application views classes.
	"""

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
		self.__modelSelection = {"Default" : []}

		self.setModel(model)

		Abstract_QListView.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def modelSelection(self):
		"""
		This method is the property for **self.__modelSelection** attribute.

		:return: self.__modelSelection. ( Dictionary )
		"""

		return self.__modelSelection

	@modelSelection.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def modelSelection(self, value):
		"""
		This method is the setter method for **self.__modelSelection** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("modelSelection", value)
			for key, element in value.iteritems():
				assert type(key) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"modelSelection", key)
				assert type(element) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("modelSelection",
																								element)
		self.__modelSelection = value

	@modelSelection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self):
		"""
		This method is the deleter method for **self.__modelSelection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "modelSelection"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setModel(self, model):
		"""
		This method reimplements the **umbra.ui.views.Abstract_QListView.setModel** method.
		
		:param model: Model to set. ( QObject )
		"""

		if not model:
			return

		LOGGER.debug("> Setting '{0}' model.".format(model))

		umbra.ui.views.Abstract_QListView.setModel(self, model)

		# Signals / Slots.
		self.model().modelAboutToBeReset.connect(self.__model__modelAboutToBeReset)
		self.model().modelReset.connect(self.__model__modelReset)

	def __model__modelAboutToBeReset(self):
		"""
		This method is triggered when the Model is about to be reset.
		"""

		self.storeModelSelection()

	def __model__modelReset(self):
		"""
		This method is triggered when the Model is changed.
		"""

		self.restoreModelSelection()

	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeModelSelection(self):
		"""
		This method stores the Model selection.

		:return: Method success. ( Boolean )
		"""

		return storeViewModelSelection(self)

	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreModelSelection(self):
		"""
		This method restores the Model selection.

		:return: Method success. ( Boolean )
		"""

		return restoreViewModelSelection(self)

class Abstract_QTreeView(umbra.ui.views.Abstract_QTreeView):
	"""
	This class used as base by others Application views classes.
	"""

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
		self.__modelSelection = {"Default" : []}

		self.setModel(model)

		Abstract_QTreeView.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def modelSelection(self):
		"""
		This method is the property for **self.__modelSelection** attribute.

		:return: self.__modelSelection. ( Dictionary )
		"""

		return self.__modelSelection

	@modelSelection.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def modelSelection(self, value):
		"""
		This method is the setter method for **self.__modelSelection** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("modelSelection", value)
			for key, element in value.iteritems():
				assert type(key) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"modelSelection", key)
				assert type(element) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("modelSelection",
																								element)
			self.__modelSelection = value

	@modelSelection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self):
		"""
		This method is the deleter method for **self.__modelSelection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "modelSelection"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setModel(self, model):
		"""
		This method reimplements the **umbra.ui.views.Abstract_QTreeView.setModel** method.
		
		:param model: Model to set. ( QObject )
		"""

		if not model:
			return

		LOGGER.debug("> Setting '{0}' model.".format(model))

		umbra.ui.views.Abstract_QTreeView.setModel(self, model)

		# Signals / Slots.
		self.model().modelAboutToBeReset.connect(self.__model__modelAboutToBeReset)
		self.model().modelReset.connect(self.__model__modelReset)

	def __model__modelAboutToBeReset(self):
		"""
		This method is triggered when the Model is about to be reset.
		"""

		self.storeModelSelection()

	def __model__modelReset(self):
		"""
		This method is triggered when the Model is changed.
		"""

		self.restoreModelSelection()

	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeModelSelection(self):
		"""
		This method stores the Model selection.

		:return: Method success. ( Boolean )
		"""

		return storeViewModelSelection(self)

	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreModelSelection(self):
		"""
		This method restores the Model selection.

		:return: Method success. ( Boolean )
		"""

		return restoreViewModelSelection(self)
