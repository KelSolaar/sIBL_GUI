#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application models classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import sibl_gui.ui.common
import umbra.ui.models
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "GraphModel"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class GraphModel(umbra.ui.models.GraphModel):
	"""
	This class provideds a graph model based on :class:`umbra.ui.models.GraphModel`
	but reimplementing the :meth:`umbra.ui.models.GraphModel.data` method
	to support various images formats as **Qt.DecorationRole**.
	"""

	@core.executionTrace
	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None, defaultNode=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		:param defaultNode: Default node. ( AbstractCompositeNode )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders, defaultNode)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def data(self, index, role=Qt.DisplayRole):
		"""
		This method reimplements the :meth:`umbra.ui.models.GraphModel.data` method.
		
		:param index: Index. ( QModelIndex )
		:param role: Role. ( Integer )
		:return: Data. ( QVariant )
		"""

		if not index.isValid():
			return QVariant()

		node = self.getNode(index)
		if index.column() == 0:
			if hasattr(node, "roles"):
				value = node.roles.get(role)
				if role == Qt.DecorationRole:
					return value is not None and sibl_gui.ui.common.getIcon(value) or QVariant()
				else:
					return value is not None and value or QVariant()
		else:
			attribute = self.getAttribute(node, index.column())
			if attribute:
				if hasattr(attribute, "roles"):
					value = attribute.roles.get(role)
					if role == Qt.DecorationRole:
						return value is not None and sibl_gui.ui.common.getIcon(value) or QVariant()
					else:
						return value is not None and value or QVariant()
		return QVariant()
