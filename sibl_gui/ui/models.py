#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application models classes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
import sibl_gui.ui.common
import umbra.ui.models

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "GraphModel"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class GraphModel(umbra.ui.models.GraphModel):
	"""
	This class provideds a graph Model based on :class:`umbra.ui.models.GraphModel`
	but reimplementing the :meth:`umbra.ui.models.GraphModel.data` method
	to support various images formats as **Qt.DecorationRole**.
	"""

	def __init__(self,
				parent=None,
				rootNode=None,
				horizontalHeaders=None,
				verticalHeaders=None,
				defaultNode=None,
				thumbnailsSize=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		:param defaultNode: Default node. ( GraphModelNode )
		:param thumbnailsSize: Thumbnails size. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders, defaultNode)

		# --- Setting class attributes. ---
		self.__thumbnailsSize = None
		self.thumbnailsSize = thumbnailsSize if thumbnailsSize is not None else "Default"

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def thumbnailsSize(self):
		"""
		This method is the property for **self.__thumbnailsSize** attribute.

		:return: self.__thumbnailsSize. ( Dictionary )
		"""

		return self.__thumbnailsSize

	@thumbnailsSize.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def thumbnailsSize(self, value):
		"""
		This method is the setter method for **self.__thumbnailsSize** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("thumbnailsSize", value)
		self.__thumbnailsSize = value

	@thumbnailsSize.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def thumbnailsSize(self):
		"""
		This method is the deleter method for **self.__thumbnailsSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "thumbnailsSize"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def data(self, index, role=Qt.DisplayRole):
		"""
		This method reimplements the :meth:`umbra.ui.models.GraphModel.data` method.
		
		:param index: Index. ( QModelIndex )
		:param role: Role. ( Integer )
		:return: Data. ( QVariant )
		"""

		if not index.isValid():
			return QVariant()

		node = self.getNode(index)
		if index.column() == 0:
			if hasattr(node, "roles"):
				value = node.roles.get(role)
				if role == Qt.DecorationRole:
					return sibl_gui.ui.common.getIcon(value, size=self.__thumbnailsSize) if value is not None else QVariant()
				else:
					return value if value is not None else QVariant()
		else:
			attribute = self.getAttribute(node, index.column())
			if attribute:
				if hasattr(attribute, "roles"):
					value = attribute.roles.get(role)
					if role == Qt.DecorationRole:
						return sibl_gui.ui.common.getIcon(value) if value is not None else QVariant()
					else:
						return value if value is not None else QVariant()
		return QVariant()
