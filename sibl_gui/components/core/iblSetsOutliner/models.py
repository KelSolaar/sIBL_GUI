#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner.IblSetsOutliner`
	Component Interface class Models.

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
import sibl_gui.ui.models

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "IblSetsModel"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class IblSetsModel(sibl_gui.ui.models.GraphModel):
	"""
	This class defines the Model used the by 
	:class:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner.IblSetsOutliner` Component Interface class. 
	"""

	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def initializeModel(self, rootNode):
		"""
		This method initializes the Model using given root node.
		
		:param rootNode: Graph root node. ( DefaultNode )
		:return: Method success ( Boolean )
		"""

		LOGGER.debug("> Initializing model with '{0}' root node.".format(rootNode))

		self.beginResetModel()
		self.rootNode = rootNode
		self.enableModelTriggers(True)
		self.endResetModel()
		return True

	def sort(self, column, order=Qt.AscendingOrder):
		"""
		This method reimplements the :meth:`umbra.ui.models.GraphModel.sort` method.
		
		:param column: Column. ( Integer )
		:param order: Order. ( Qt.SortOrder )
		:return: Method success. ( Boolean )
		"""

		if column > self.columnCount():
			return False

		self.beginResetModel()
		if column == 0:
			self.rootNode.sortChildren(attribute="title", reverseOrder=order)
		else:
			self.rootNode.sortChildren(attribute=self.horizontalHeaders[self.horizontalHeaders.keys()[column]],
										reverseOrder=order)
		self.endResetModel()
