#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`sibl_gui.components.core.collectionsOutliner.collectionsOutliner.CollectionsOutliner` Component Interface class Models.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.models
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "OverallCollectionNode", "CollectionsModel"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getOverallCollectionNode(name=None, parent=None):
	"""
	This definition is a class instances factory creating :class:`OverallCollectionNode` classes instances.

	:param name: Node name. ( String )
	:param parent: Node parent. ( GraphModelNode )
	:return: OverallCollectionNode class instance. ( OverallCollectionNode )
	"""

	graphModelNode = umbra.ui.models.GraphModelNode

	OverallCollectionNode = type("OverallCollection", (graphModelNode,), {"_OverallCollection__family" : "OverallCollection"})

	overallCollectionNode = OverallCollectionNode(name, parent)

	overallCollectionNode["count"] = umbra.ui.models.GraphModelAttribute(name="count", flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
	overallCollectionNode["comment"] = umbra.ui.models.GraphModelAttribute(name="comment", flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

	return overallCollectionNode

class CollectionsModel(umbra.ui.models.GraphModel):
	"""
	This class defines the model used the by :class:`sibl_gui.components.core.collectionsOutliner.collectionsOutliner.CollectionsOutliner` Component Interface class. 
	"""

	@core.executionTrace
	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders)

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def initializeModel(self, rootNode):
		"""
		This method initializes the model using given root node.
		
		:param rootNode: Graph root node. ( DefaultNode )
		return: Method success ( Boolean )
		"""

		self.beginResetModel()
		self.rootNode = rootNode
		self.endResetModel()
		return True
