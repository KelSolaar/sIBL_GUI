#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_gui.components.core.templates_outliner.templates_outliner.TemplatesOutliner`
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

__all__ = ["LOGGER", "SoftwareNode"]

LOGGER = foundations.verbose.install_logger()

class SoftwareNode(sibl_gui.ui.nodes.GraphModelNode):
	"""
	Defines :class:`sibl_gui.components.core.templates_outliner.templates_outliner.TemplatesOutliner`
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

		SoftwareNode.__initialize_node(self, attributes_flags)

	def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		Initializes the node.

		:param attributes_flags: Attributes flags.
		:type attributes_flags: int
		"""

		self["release"] = sibl_gui.ui.nodes.GraphModelAttribute(name="release",
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
		self["version"] = sibl_gui.ui.nodes.GraphModelAttribute(name="version",
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
