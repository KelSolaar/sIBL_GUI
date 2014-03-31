#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_gui.components.core.templatesOutliner.templatesOutliner.TemplatesOutliner`
	Component Interface class nodes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
import sibl_gui.ui.nodes

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "SoftwareNode"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class SoftwareNode(sibl_gui.ui.nodes.GraphModelNode):
	"""
	Defines :class:`sibl_gui.components.core.templatesOutliner.templatesOutliner.TemplatesOutliner`
		Component Interface class Model software node.
	"""

	__family = "Software"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

	def __init__(self,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				iconSize=None,
				iconPlaceholder=None,
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
		:param nodeFlags: Node flags.
		:type nodeFlags: int
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		:param iconSize: Icon size.
		:type iconSize: unicode
		:param iconPlaceholder: Icon placeholder.
		:type iconPlaceholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.nodes.GraphModelNode.__init__(self,
												name,
												parent,
												children,
												roles,
												nodeFlags,
												iconSize,
												iconPlaceholder,
												**kwargs)

		SoftwareNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		Initializes the node.
		
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		"""

		self["release"] = sibl_gui.ui.nodes.GraphModelAttribute(name="release",
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
		self["version"] = sibl_gui.ui.nodes.GraphModelAttribute(name="version",
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
