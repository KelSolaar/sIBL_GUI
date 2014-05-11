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

from __future__ import unicode_literals

from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt

import foundations.verbose
import sibl_gui.ui.common
import umbra.ui.models

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "GraphModel"]

LOGGER = foundations.verbose.install_logger()

class GraphModel(umbra.ui.models.GraphModel):
	"""
	Defines a graph Model based on :class:`umbra.ui.models.GraphModel`
	but reimplementing the :meth:`umbra.ui.models.GraphModel.data` method
	to support various images formats as **Qt.DecorationRole**.
	"""

	def __init__(self, parent=None, root_node=None, horizontal_headers=None, vertical_headers=None, default_node=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param root_node: Root node.
		:type root_node: AbstractCompositeNode
		:param horizontal_headers: Headers.
		:type horizontal_headers: OrderedDict
		:param vertical_headers: Headers.
		:type vertical_headers: OrderedDict
		:param default_node: Default node.
		:type default_node: GraphModelNode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, root_node, horizontal_headers, vertical_headers, default_node)

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

		node = self.get_node(index)
		if index.column() == 0:
			if hasattr(node, "roles"):
				value = node.roles.get(role)
				if role == Qt.DecorationRole:
					return sibl_gui.ui.common.get_icon(value,
													size=node.get("icon_size", "Default"),
													placeholder=node.get("icon_placeholder")) \
													if value is not None else QVariant()
				else:
					return value if value is not None else QVariant()
		else:
			attribute = self.get_attribute(node, index.column())
			if attribute:
				if hasattr(attribute, "roles"):
					value = attribute.roles.get(role)
					if role == Qt.DecorationRole:
						return sibl_gui.ui.common.get_icon(value,
													size=attribute.get("icon_size", "Default"),
													placeholder=attribute.get("icon_placeholder")) \
													if value is not None else QVariant()
					else:
						return value if value is not None else QVariant()
		return QVariant()
