#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_gui.components.core.collections_outliner.collections_outliner.CollectionsOutliner`
	Component Interface class nodes.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt

import foundations.verbose
import sibl_gui.ui.nodes

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "OverallCollectionNode"]

LOGGER = foundations.verbose.install_logger()

class OverallCollectionNode(sibl_gui.ui.nodes.GraphModelNode):
	"""
	Defines :class:`sibl_gui.components.core.collections_outliner.collections_outliner.CollectionsOutliner`
		Component Interface class Model **Overall** collection node.
	"""

	__family = "OverallCollection"

	def __init__(self,
				name=None,
				parent=None,
				children=None,
				roles=None,
				node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				icon_size=None,
				icon_placeholder=None,
				**kwargs):
		"""
		Initializes the class.

		:param name: Node name.
		:type name: unicode
		:param parent: Node parent.
		:type parent: GraphModelNode
		:param children: Children.
		:type children: list
		:param roles: Roles.
		:type roles: dict
		:param node_flags: Node flags.
		:type node_flags: int
		:param attributes_flags: Attributes flags.
		:type attributes_flags: int
		:param icon_size: Icon size.
		:type icon_size: unicode
		:param icon_placeholder: Icon placeholder.
		:type icon_placeholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.nodes.GraphModelNode.__init__(self,
												name,
												parent,
												children,
												roles,
												node_flags,
												icon_size,
												icon_placeholder,
												**kwargs)

		OverallCollectionNode.__initialize_node(self, attributes_flags)

	def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		Initializes the node.

		:param attributes_flags: Attributes flags.
		:type attributes_flags: int
		"""

		self["count"] = sibl_gui.ui.nodes.GraphModelAttribute(name="count",
															value=sum(node["count"].value for node in self.children),
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
		self["comment"] = sibl_gui.ui.nodes.GraphModelAttribute(name="comment",
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

	def update_node(self):
		"""
		Updates the node.

		:return: Method success.
		:rtype: bool
		"""

		return self.update_node_attributes()

	def update_node_attributes(self):
		"""
		Updates the Node attributes.

		:return: Method success.
		:rtype: bool
		"""

		self.count.value = self.count.roles[Qt.DisplayRole] = sum(node.count.value for node in self.children)
