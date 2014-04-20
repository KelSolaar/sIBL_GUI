#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application views classes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"Mixin_AbstractView"
			"Abstract_QListView",
			"Abstract_QTreeView"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Mixin_AbstractView(object):
	"""
	Defines a mixin used to bring common capabilities in Application Views classes.
	"""

	def __init__(self, model=None):
		"""
		Initializes the class.

		:param model: Model.
		:type model: QObject
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__model_selection = {"Default" : []}

		Mixin_AbstractView.setModel(self, model)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def model_selection(self):
		"""
		Property for **self.__model_selection** attribute.

		:return: self.__model_selection.
		:rtype: dict
		"""

		return self.__model_selection

	@model_selection.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def model_selection(self, value):
		"""
		Setter for **self.__model_selection** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("model_selection", value)
			for key, element in value.iteritems():
				assert type(key) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"model_selection", key)
				assert type(element) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("model_selection",
																								element)
		self.__model_selection = value

	@model_selection.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def model_selection(self):
		"""
		Deleter for **self.__model_selection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model_selection"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def setModel(self, model):
		"""
		Reimplements the **umbra.ui.views.Abstract_QListView.setModel** method.
		
		:param model: Model to set.
		:type model: QObject
		"""

		if not model:
			return

		LOGGER.debug("> Setting '{0}' model.".format(model))

		super(type(self), self).setModel(model)

		# Signals / Slots.
		self.model().modelAboutToBeReset.connect(self.__model__modelAboutToBeReset)
		self.model().modelReset.connect(self.__model__modelReset)

	def __model__modelAboutToBeReset(self):
		"""
		Defines the slot triggered by the Model when about to be reset.
		"""

		self.store_model_selection()

	def __model__modelReset(self):
		"""
		Defines the slot triggered by the Model when reset.
		"""

		self.restore_model_selection()

	def store_model_selection(self):
		"""
		Stores the Model selection.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Storing Model selection!")

		self.model_selection = {"Default" : []}
		for node in self.get_selected_nodes():
			self.model_selection["Default"].append(node.id.value)
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

		selection = self.model_selection.get("Default", None)
		if not selection:
			return False

		indexes = []
		for node in foundations.walkers.nodes_walker(self.model().root_node):
			node.id.value in selection and indexes.append(self.model().get_node_index(node))

		return self.select_view_indexes(indexes)

class Abstract_QListView(umbra.ui.views.Abstract_QListView, Mixin_AbstractView):
	"""
	Defines the base class used by others Application Views classes.
	"""

	def __init__(self, parent=None, model=None, read_only=False, message=None):
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

		umbra.ui.views.Abstract_QListView.__init__(self, parent, read_only, message)
		Mixin_AbstractView.__init__(self, model)

class Abstract_QTreeView(umbra.ui.views.Abstract_QTreeView, Mixin_AbstractView):
	"""
	Defines the base class used by others Application Views classes.
	"""

	def __init__(self, parent=None, model=None, read_only=False, message=None):
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

		umbra.ui.views.Abstract_QTreeView.__init__(self, parent, read_only, message)
		Mixin_AbstractView.__init__(self, model)

