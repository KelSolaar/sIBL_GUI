#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application models classes.

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines a graph Model based on :class:`umbra.ui.models.GraphModel`
	but reimplementing the :meth:`umbra.ui.models.GraphModel.data` method
	to support various images formats as **Qt.DecorationRole**.
	"""

	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None, defaultNode=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param rootNode: Root node.
		:type rootNode: AbstractCompositeNode
		:param horizontalHeaders: Headers.
		:type horizontalHeaders: OrderedDict
		:param verticalHeaders: Headers.
		:type verticalHeaders: OrderedDict
		:param defaultNode: Default node.
		:type defaultNode: GraphModelNode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders, defaultNode)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def data(self, index, role=Qt.DisplayRole):
		"""
		Reimplements the :meth:`umbra.ui.models.GraphModel.data` method.
		
		:param index: Index.
		:type index: QModelIndex
		:param role: Role.
		:type role: int
		:return: Data.
		:rtype: QVariant
		"""

		if not index.isValid():
			return QVariant()

		node = self.getNode(index)
		if index.column() == 0:
			if hasattr(node, "roles"):
				value = node.roles.get(role)
				if role == Qt.DecorationRole:
					return sibl_gui.ui.common.getIcon(value,
													size=node.get("iconSize", "Default"),
													placeholder=node.get("iconPlaceholder")) \
													if value is not None else QVariant()
				else:
					return value if value is not None else QVariant()
		else:
			attribute = self.getAttribute(node, index.column())
			if attribute:
				if hasattr(attribute, "roles"):
					value = attribute.roles.get(role)
					if role == Qt.DecorationRole:
						return sibl_gui.ui.common.getIcon(value,
													size=attribute.get("iconSize", "Default"),
													placeholder=attribute.get("iconPlaceholder")) \
													if value is not None else QVariant()
					else:
						return value if value is not None else QVariant()
		return QVariant()
