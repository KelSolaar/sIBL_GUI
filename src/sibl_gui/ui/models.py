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
import sibl_gui.ui.common
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

__all__ = ["LOGGER", "GraphModel"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class GraphModel(umbra.ui.models.GraphModel):
	"""
	This class provideds a graph model based on :class:`umbra.ui.models.GraphModel` but reimplementing the :meth:`umbra.ui.models.GraphModel.data` method to support various images formats as **Qt.DecorationRole**.
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
			return hasattr(node, "roles") and role == Qt.DecorationRole and sibl_gui.ui.common.getIcon(node.roles.get(role, str())) or node.roles.get(role, None) or QVariant()
		else:
			attribute = self.getAttribute(node, index.column())
			return attribute and hasattr(attribute, "roles") and role == Qt.DecorationRole and sibl_gui.ui.common.getIcon(attribute.roles.get(role, str())) or attribute.roles.get(role, QVariant()) or QVariant()
