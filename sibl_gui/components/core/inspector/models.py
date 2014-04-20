#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_gui.components.core.inspector.inspector.Inspector`
	Component Interface class Models.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
import sibl_gui.ui.models

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "PlatesModel"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class PlatesModel(sibl_gui.ui.models.GraphModel):
	"""
	Defines the Model used the by :class:`sibl_gui.components.core.inspector.inspector.Inspector`
	Component Interface class. 
	"""

	def __init__(self, parent=None, root_node=None, horizontal_headers=None, vertical_headers=None):
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
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.models.GraphModel.__init__(self,
											parent,
											root_node,
											horizontal_headers,
											vertical_headers)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def initialize_model(self, root_node):
		"""
		Initializes the Model using given root node.
		
		:param root_node: Graph root node.
		:type root_node: DefaultNode
		:return: Method success
		:rtype: bool
		"""

		LOGGER.debug("> Initializing model with '{0}' root node.".format(root_node))

		self.beginResetModel()
		self.root_node = root_node
		self.enable_model_triggers(True)
		self.endResetModel()
		return True
