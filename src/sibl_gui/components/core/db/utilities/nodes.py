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
			"getAbstractDatabaseNode",
			"getIblSetNode",
			"getTemplateNode",
			"getCollectionNode"]

LOGGER = logging.getLogger(Constants.logger)

DATABASE_TABLE_TO_NODE_FAMILY_MAPPING = {"Sets" : "Ibl Set", "Templates" : "Template", "Collections" : "Collection"}

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getAbstractDatabaseNode(dbItem):
	"""
	This definition is a class factory creating :class:`DatabaseNode` classes using given Database object.

	:param dbItem: Database object. ( Object )
	:return: AbstractDatabaseNode class. ( AbstractDatabaseNode )
	"""

	defaultFlags = Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled

	graphModelNode = umbra.ui.models.getGraphModelNode()

	AbstractDatabaseNode = type("AbstractDatabaseNode", (graphModelNode,), {"_AbstractDatabaseNode__family" : "AbstractDatabaseNode"})

	attributes = {}
	for column in dbItem.__table__.columns:
		attribute = column.key
		value = getattr(dbItem, attribute)
		roles = {Qt.DisplayRole : value,
				Qt.EditRole : value}
		flags = defaultFlags
		attributes[attribute] = umbra.ui.models.GraphModelAttribute(attribute, value, roles, flags)

	AbstractDatabaseNode.__dbItem = dbItem

	@property
	def dbItem(self):
		"""
		This method is the property for **self.__dbItem** attribute.

		:return: self.__dbItem. ( Object )
		"""

		return self.__dbItem

	@dbItem.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbItem(self, value):
		"""
		This method is the setter method for **self.__dbItem** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dbItem"))

	@dbItem.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbItem(self):
		"""
		This method is the deleter method for **self.__dbItem** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dbItem"))

	setattr(AbstractDatabaseNode, "dbItem", dbItem)
	AbstractDatabaseNode._DatabaseNode__dbItem = dbItem

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeNodeAttributes(self):
		"""
		This method synchronizes the node attributes from the dbItem.
		
		:return: Method success. ( Boolean )
		"""

		for column in self.__dbItem.__table__.columns:
			attribute = column.key
			value = getattr(dbItem, attribute)
			if not attribute in self.keys():
				break

			if issubclass(self[attribute].__class__, umbra.ui.models.GraphModelAttribute):
					self[attribute] = value
		return True

	setattr(AbstractDatabaseNode, "synchronizeNodeAttributes", synchronizeNodeAttributes)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeDbItem(self):
		"""
		This method synchronizes the dbItem from the node attributes.

		:return: Method success. ( Boolean )
		"""

		for column in self.__dbItem.__table__.columns:
			attribute = column.key
			if not attribute in self.keys():
				break

			if issubclass(self[attribute].__class__, umbra.ui.models.GraphModelAttribute):
					setattr(self.__dbItem, attribute, self[attribute].value)
		return True

	setattr(AbstractDatabaseNode, "synchronizeDbItem", synchronizeDbItem)

	return AbstractDatabaseNode, attributes

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getIblSetNode(dbIblSet, parent=None, children=None, nodeFlags=Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled, attributeFlags=Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled):
	"""
	This definition is a class instances factory creating :class:`IblSetNode` classes using given Collection object.

	:param dbIblSet: Database Collection. ( DbIblSet )
	:param parent: Node parent. ( GraphModelNode )
	:param children: Children. ( List )
	:param nodeFlags: Node flags. ( Qt.ItemFlag )
	:param attributeFlags: Attribute flags. ( Qt.ItemFlag )
	:return: IblSetNode class instance. ( IblSetNode )
	"""

	toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Author: </b>{1}<br>
				<b>Location: </b>{2}<br>
				<b>Shot Date: </b>{3}<br>
				<b>Comment: </b>{4}</p>
				"""

	abstractDatabaseNode, attributes = getAbstractDatabaseNode(dbIblSet)

	IblSetNode = type("IblSetNode", (abstractDatabaseNode,), {"_IblSetNode__family" : DATABASE_TABLE_TO_NODE_FAMILY_MAPPING[dbIblSet.__table__.name]})

	roles = {Qt.DisplayRole : attributes["title"].value,
			Qt.DecorationRole : sibl_gui.ui.common.getIcon(attributes["icon"].value),
			Qt.EditRole : attributes["title"].value,
			Qt.ToolTipRole : toolTipText.format(attributes["title"].value,
												attributes["author"].value or Constants.nullObject,
												attributes["location"].value or Constants.nullObject,
												sibl_gui.ui.common.getFormatedShotDate(attributes["date"].value, attributes["time"].value) or Constants.nullObject,
												attributes["comment"].value or Constants.nullObject)}

	for attribute in attributes.values():
		attribute.flags = attributeFlags

	return IblSetNode(attributes.pop("name").value, parent, children, roles, nodeFlags, **attributes)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getTemplateNode(dbTemplate, parent=None, children=None):
	"""
	This definition is a class instances factory creating :class:`TemplateNode` classes using given Template object.

	:param dbTemplate: Database Template. ( DbTemplate )
	:param parent: Node parent. ( GraphModelNode )
	:param children: Children. ( List )
	:return: TemplateNode class instance. ( TemplateNode )
	"""

	abstractDatabaseNode, attributes = getAbstractDatabaseNode(dbTemplate)

	TemplateNode = type("TemplateNode", (abstractDatabaseNode,), {"_TemplateNode__family" : DATABASE_TABLE_TO_NODE_FAMILY_MAPPING[dbTemplate.__table__.name]})

	roles = None
	flags = None

	name = attributes.pop("name").value
	return TemplateNode(attributes["title"].value, parent, children, roles, flags, **attributes)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getCollectionNode(dbCollection, parent=None, children=None, nodeFlags=Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled, attributeFlags=Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled):
	"""
	This definition is a class instances factory creating :class:`CollectionNode` classes using given Collection object.

	:param dbCollection: Database Collection. ( DbCollection )
	:param parent: Node parent. ( GraphModelNode )
	:param children: Children. ( List )
	:param nodeFlags: Node flags. ( Qt.ItemFlag )
	:param attributeFlags: Attribute flags. ( Qt.ItemFlag )
	:return: CollectionNode class instance. ( CollectionNode )
	"""

	abstractDatabaseNode, attributes = getAbstractDatabaseNode(dbCollection)

	CollectionNode = type("CollectionNode", (abstractDatabaseNode,), {"_CollectionNode__family" : DATABASE_TABLE_TO_NODE_FAMILY_MAPPING[dbCollection.__table__.name]})

	roles = {Qt.DisplayRole : attributes["name"].value,
			Qt.EditRole : attributes["name"].value}

	for attribute in attributes.values():
		attribute.flags = attributeFlags

	attributes["count"] = umbra.ui.models.GraphModelAttribute(name="count", value=None, flags=Qt.ItemIsSelectable | Qt.ItemIsEnabled)

	return CollectionNode(attributes.pop("name").value, parent, children, roles, nodeFlags, **attributes)
