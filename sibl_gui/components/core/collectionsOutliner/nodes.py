#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`sibl_gui.components.core.collectionsOutliner.collectionsOutliner.CollectionsOutliner`
	Component Interface class nodes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
import umbra.ui.nodes

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "OverallCollectionNode"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class OverallCollectionNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`sibl_gui.components.core.collectionsOutliner.collectionsOutliner.CollectionsOutliner`
		Component Interface class Model **Overall** collection node.
	"""

	__family = "OverallCollection"

	def __init__(self,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				**kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		OverallCollectionNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		self["count"] = umbra.ui.nodes.GraphModelAttribute(name="count",
															value=sum(node["count"].value for node in self.children),
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
		self["comment"] = umbra.ui.nodes.GraphModelAttribute(name="comment",
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

	def updateNode(self):
		"""
		This method updates the node.

		:return: Method success. ( Boolean )
		"""

		return self.updateNodeAttributes()

	def updateNodeAttributes(self):
		"""
		This method updates the Node attributes.
		
		:return: Method success. ( Boolean )
		"""

		self.count.value = self.count.roles[Qt.DisplayRole] = sum(node.count.value for node in self.children)
