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
import sibl_gui.ui.models
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
class OverallCollectionNode(umbra.ui.models.GraphModelNode):
	"""
	This class factory defines :class:`sibl_gui.components.core.collectionsOutliner.collectionsOutliner.CollectionsOutliner` Component Interface class Model **Overall** collection node.
	"""

	__family = "OverallCollection"

	@core.executionTrace
	def __init__(self, name=None, parent=None, children=None, roles=None, nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled), attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled), ** kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		OverallCollectionNode.__initializeNode(self, attributesFlags)

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeNode(self, attributesFlags):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		self["count"] = umbra.ui.models.GraphModelAttribute(name="count", flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
		self["comment"] = umbra.ui.models.GraphModelAttribute(name="comment", flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

class CollectionsModel(sibl_gui.ui.models.GraphModel):
	"""
	This class defines the Model used the by :class:`sibl_gui.components.core.collectionsOutliner.collectionsOutliner.CollectionsOutliner` Component Interface class. 
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

		sibl_gui.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders)

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeModel(self, rootNode):
		"""
		This method initializes the Model using given root node.
		
		:param rootNode: Graph root node. ( DefaultNode )
		return: Method success ( Boolean )
		"""

		self.beginResetModel()
		self.rootNode = rootNode
		self.endResetModel()
		return True
