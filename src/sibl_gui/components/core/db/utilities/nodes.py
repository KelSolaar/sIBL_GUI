#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines objects to generate Application nodes classes from Database objects.

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
import sibl_gui.ui.common
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

__all__ = ["LOGGER",
			"DATABASE_TABLE_TO_NODE_FAMILY_MAPPING",
			"getIblSetNode",
			"getTemplateNode",
			"getCollectionNode"]

LOGGER = logging.getLogger(Constants.logger)

DATABASE_TABLE_TO_NODE_FAMILY_MAPPING = {"Sets" : "IblSets", "Templates" : "Templates", "Collection" : "Collection"}

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getIblSetNode(dbIblSet, parent=None, children=None):
	"""
	This definition is a class instances factory creating :class:`IblSetNode` classes using given Ibl Set object.

	:param dbIblSet: Database Ibl Set. ( DbIblSet )
	:param parent: Node parent. ( AbstractNode / AbstractCompositeNode )
	:param children: Children. ( List )
	:return: IblSetNode class instance. ( IblSetNode )
	"""

	toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Author: </b>{1}<br>
				<b>Location: </b>{2}<br>
				<b>Shot Date: </b>{3}<br>
				<b>Comment: </b>{4}</p>
				"""

	dbNode, attributes = umbra.ui.models.getGraphModelNode(dbIblSet)

	IblSetNode = type("IblSetNode", (dbNode,), {"_IblSetNode__family" : DATABASE_TABLE_TO_NODE_FAMILY_MAPPING[dbIblSet.__table__.name]})

	roles = {Qt.DisplayRole : attributes["title"].value,
			Qt.DecorationRole : sibl_gui.ui.common.getIcon(attributes["icon"].value),
			Qt.EditRole : attributes["title"].value,
			Qt.ToolTipRole : toolTipText.format(attributes["title"].value,
												attributes["author"].value or Constants.nullObject,
												attributes["location"].value or Constants.nullObject,
												sibl_gui.ui.common.getFormatedShotDate(attributes["date"].value, attributes["time"].value) or Constants.nullObject,
												attributes["comment"].value or Constants.nullObject)}

	flags = None

	return IblSetNode(attributes.pop("name").value, parent, children, roles, flags, **attributes)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getTemplateNode(dbTemplate, parent=None, children=None):
	"""
	This definition is a class instances factory creating :class:`TemplateNode` classes using given Template object.

	:param dbTemplate: Database Template. ( DbTemplate )
	:param parent: Node parent. ( AbstractNode / AbstractCompositeNode )
	:param children: Children. ( List )
	:return: TemplateNode class instance. ( TemplateNode )
	"""

	dbNode, attributes = umbra.ui.models.getGraphModelNode(dbTemplate)

	TemplateNode = type("TemplateNode", (dbNode,), {"_TemplateNode__family" : DATABASE_TABLE_TO_NODE_FAMILY_MAPPING[dbTemplate.__table__.name]})

	roles = None
	flags = None

	name = attributes.pop("name").value
	return TemplateNode(attributes["title"].value, parent, children, roles, flags, **attributes)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getCollectionNode(dbCollection, parent=None, children=None):
	"""
	This definition is a class instances factory creating :class:`CollectionNode` classes using given Collection object.

	:param dbCollection: Database Collection. ( DbCollection )
	:param parent: Node parent. ( AbstractNode / AbstractCompositeNode )
	:param children: Children. ( List )
	:return: CollectionNode class instance. ( CollectionNode )
	"""

	dbNode, attributes = umbra.ui.models.getGraphModelNode(dbCollection)

	CollectionNode = type("CollectionNode", (dbNode,), {"_CollectionNode__family" : DATABASE_TABLE_TO_NODE_FAMILY_MAPPING[dbCollection.__table__.name]})

	roles = None
	flags = None

	return CollectionNode(attributes.pop("name").value, parent, children, roles, flags, **attributes)
