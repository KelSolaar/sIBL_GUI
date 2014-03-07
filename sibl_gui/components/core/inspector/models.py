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

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class PlatesModel(sibl_gui.ui.models.GraphModel):
	"""
	Defines the Model used the by :class:`sibl_gui.components.core.inspector.inspector.Inspector`
	Component Interface class. 
	"""

	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None):
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
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.models.GraphModel.__init__(self,
											parent,
											rootNode,
											horizontalHeaders,
											verticalHeaders)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def initializeModel(self, rootNode):
		"""
		Initializes the Model using given root node.
		
		:param rootNode: Graph root node.
		:type rootNode: DefaultNode
		:return: Method success
		:rtype: bool
		"""

		LOGGER.debug("> Initializing model with '{0}' root node.".format(rootNode))

		self.beginResetModel()
		self.rootNode = rootNode
		self.enableModelTriggers(True)
		self.endResetModel()
		return True
