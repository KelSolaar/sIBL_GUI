#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines Application nodes classes related to Database objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.nodes
import sibl_gui.components.core.database.operations
import sibl_gui.ui.common
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"getTemplateUserName",
			"AbstractDatabaseNode",
			"IblSetNode",
			"TemplateNode",
			"CollectionNode"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getTemplateUserName(title, software):
	"""
	This method returns the Template user name.

	:param title: Template title.  ( String )
	:param software: Template software.  ( String )
	:return: Template user name. ( String )
	"""

	return foundations.strings.removeStrip(title, software)

class AbstractDatabaseNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class defines Application Database abstract base class used by concrete Database Node classes.
	"""

	__family = "AbstractDatabaseNode"
	"""Node family. ( String )"""

	def __init__(self,
				databaseItem,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=None,
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled),
				**kwargs):
		"""
		This method initializes the class.

		:param databaseItem: Database object.  ( Object )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		# --- Setting class attributes. ---
		self.__databaseItem = databaseItem
		self.__toolTipText = unicode()

		AbstractDatabaseNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def databaseItem(self):
		"""
		This method is the property for **self.__databaseItem** attribute.

		:return: self.__databaseItem. ( Object )
		"""

		return self.__databaseItem

	@databaseItem.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseItem(self, value):
		"""
		This method is the setter method for **self.__databaseItem** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseItem"))

	@databaseItem.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseItem(self):
		"""
		This method is the deleter method for **self.__databaseItem** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseItem"))

	@property
	def toolTipText(self):
		"""
		This method is the property for **self.__toolTipText** attribute.

		:return: self.__toolTipText. ( String )
		"""

		return self.__toolTipText

	@toolTipText.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def toolTipText(self, value):
		"""
		This method is the setter method for **self.__toolTipText** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"toolTipText", value)
		self.__toolTipText = value

	@toolTipText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def toolTipText(self):
		"""
		This method is the deleter method for **self.__toolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "toolTipText"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		for column in self.__databaseItem.__table__.columns:
			attribute = column.key
			if attribute == "name":
				continue

			value = getattr(self.__databaseItem, attribute)
			roles = {Qt.DisplayRole : value,
					Qt.EditRole : value}
			self[attribute] = umbra.ui.nodes.GraphModelAttribute(attribute, value, roles, attributesFlags)

	def updateNode(self):
		"""
		This method updates the Node from the database item.

		:return: Method success. ( Boolean )
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(
		self.__class__.__name__, self.updateNode.__name__, self.__class__.__name__))

	def updateNodeAttributes(self):
		"""
		This method updates the Node attributes from the database item attributes.
		
		:return: Method success. ( Boolean )
		"""

		for column in self.__databaseItem.__table__.columns:
			attribute = column.key
			if not attribute in self:
				continue

			if issubclass(self[attribute].__class__, umbra.ui.nodes.GraphModelAttribute):
				self[attribute].value = self[attribute].roles[Qt.DisplayRole] = self[attribute].roles[Qt.EditRole] = \
				getattr(self.__databaseItem, attribute)
		return True

	def updateDatabaseItem(self):
		"""
		This method updates the database item from the node.

		:return: Method success. ( Boolean )
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(
		self.__class__.__name__, self.updateDatabaseItem.__name__, self.__class__.__name__))

	def updateDatabaseItemAttributes(self):
		"""
		This method updates the database item attributes from the Node attributes.

		:return: Method success. ( Boolean )
		"""

		for column in self.__databaseItem.__table__.columns:
			attribute = column.key
			if not attribute in self:
				continue

			if issubclass(self[attribute].__class__, umbra.ui.nodes.GraphModelAttribute):
				setattr(self.__databaseItem, attribute, self[attribute].value)
		return True

	@foundations.exceptions.handleExceptions(NotImplementedError)
	def updateToolTip(self):
		"""
		This method updates the Node tooltip.

		:return: Method success. ( Boolean )
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(
		self.__class__.__name__, self.updateToolTip.__name__, self.__class__.__name__))

class IblSetNode(AbstractDatabaseNode):
	"""
	This class defines Ibl Sets nodes.
	"""

	__family = "IblSet"
	"""Node family. ( String )"""

	def __init__(self,
				databaseItem,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=None,
				attributesFlags=None,
				**kwargs):
		"""
		This method initializes the class.

		:param databaseItem: Database object.  ( Object )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractDatabaseNode.__init__(self, databaseItem, name, parent, children, roles, nodeFlags, attributesFlags, **kwargs)

		# --- Setting class attributes. ---
		self.toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Author: </b>{1}<br>
				<b>Location: </b>{2}<br>
				<b>Shot Date: </b>{3}<br>
				<b>Comment: </b>{4}</p>
				"""

		IblSetNode.__initializeNode(self)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self):
		"""
		This method initializes the node.
		"""

		self.roles.update({Qt.DisplayRole : self.databaseItem.title,
							Qt.DecorationRole : self.databaseItem.icon,
							Qt.EditRole : self.databaseItem.title})
		self.updateToolTip()

	def updateNode(self):
		"""
		This method updates the node from the database item.

		:return: Method success. ( Boolean )
		"""

		self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = self.__databaseItem.title
		return self.updateNodeAttributes()

	def updateNodeAttributes(self):
		"""
		This method updates the node attributes from the database item attributes.
		
		:return: Method success. ( Boolean )
		"""

		return AbstractDatabaseNode.updateNodeAttributes(self)

	def updateDatabaseItem(self):
		"""
		This method updates the database item from the node.

		:return: Method success. ( Boolean )
		"""

		self.title = self.databaseItem.title = self.name
		return self.updateDatabaseItemAttributes()

	def updateToolTip(self):
		"""
		This method updates the node tooltip.

		:return: Method success. ( Boolean )
		"""

		self.roles[Qt.ToolTipRole] = self.toolTipText.format(self.databaseItem.title,
															self.databaseItem.author or Constants.nullObject,
															self.databaseItem.location or Constants.nullObject,
															sibl_gui.ui.common.getFormatedShotDate(self.databaseItem.date,
																			self.databaseItem.time) or Constants.nullObject,
															self.databaseItem.comment or Constants.nullObject)
		return True

class TemplateNode(AbstractDatabaseNode):
	"""
	This class defines Templates nodes.
	"""

	__family = "Template"
	"""Node family. ( String )"""

	def __init__(self,
				databaseItem,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=None,
				attributesFlags=None,
				**kwargs):
		"""
		This method initializes the class.

		:param databaseItem: Database object.  ( Object )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractDatabaseNode.__init__(self, databaseItem, name, parent, children, roles, nodeFlags, attributesFlags, **kwargs)

		# --- Setting class attributes. ---
		self.toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Author: </b>{1}<br>
				<b>Release Date: </b>{2}<br>
				<b>Comment: </b>{3}</p></p>
				"""

		TemplateNode.__initializeNode(self)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self):
		"""
		This method initializes the node.
		"""

		templateUserName = getTemplateUserName(self.databaseItem.title, self.databaseItem.software)
		self.roles.update({Qt.DisplayRole : templateUserName,
							Qt.EditRole : templateUserName})
		self.updateToolTip()

	def updateNode(self):
		"""
		This method updates the node from the database item.

		:return: Method success. ( Boolean )
		"""

		self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = getTemplateUserName(self.databaseItem.title,
																								self.databaseItem.software)

		return self.updateNodeAttributes()

	def updateNodeAttributes(self):
		"""
		This method updates the node attributes from the database item attributes.
		
		:return: Method success. ( Boolean )
		"""

		return AbstractDatabaseNode.updateNodeAttributes(self)

	def updateDatabaseItem(self):
		"""
		This method updates the database item from the node.

		:return: Method success. ( Boolean )
		"""

		self.title = self.databaseItem.title = self.name
		return self.updateDatabaseItemAttributes()

	def updateToolTip(self):
		"""
		This method updates the node tooltip.

		:return: Method success. ( Boolean )
		"""

		self.roles[Qt.ToolTipRole] = self.toolTipText.format(getTemplateUserName(self.databaseItem.title,
																				self.databaseItem.software),
																	self.databaseItem.author,
																	self.databaseItem.date,
																	self.databaseItem.comment)
		return True

class CollectionNode(AbstractDatabaseNode):
	"""
	This class defines Collections nodes.
	"""

	__family = "Collection"
	"""Node family. ( String )"""

	def __init__(self,
				databaseItem,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=None,
				attributesFlags=None,
				**kwargs):
		"""
		This method initializes the class.

		:param databaseItem: Database object.  ( Object )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractDatabaseNode.__init__(self, databaseItem, name, parent, children, roles, nodeFlags, attributesFlags, **kwargs)

		# --- Setting class attributes. ---
		self.toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Comment: </b>{1}<br></p>
				"""

		CollectionNode.__initializeNode(self)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self):
		"""
		This method initializes the node.
		"""

		self["count"] = umbra.ui.nodes.GraphModelAttribute(
						name="count",
						value=sibl_gui.components.core.database.operations.getCollectionIblSetsCount(self.databaseItem),
						flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

		self.roles.update({Qt.DisplayRole : self.databaseItem.name, Qt.EditRole : self.databaseItem.name})
		self.updateToolTip()

	def updateNode(self):
		"""
		This method updates the node from the database item.

		:return: Method success. ( Boolean )
		"""

		self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = self.databaseItem.name
		return self.updateNodeAttributes()

	def updateNodeAttributes(self):
		"""
		This method updates the node attributes from the database item attributes.
		
		:return: Method success. ( Boolean )
		"""

		self.count.value = self.count.roles[Qt.DisplayRole] = \
		sibl_gui.components.core.database.operations.getCollectionIblSetsCount(self.databaseItem)

		return AbstractDatabaseNode.updateNodeAttributes(self)

	def updateDatabaseItem(self):
		"""
		This method updates the database item from the node.

		:return: Method success. ( Boolean )
		"""

		self.databaseItem.name = self.name
		return self.updateDatabaseItemAttributes()

	def updateToolTip(self):
		"""
		This method updates the node tooltip.

		:return: Method success. ( Boolean )
		"""

		self.roles[Qt.ToolTipRole] = self.toolTipText.format(self.databaseItem.name,
																self.databaseItem.comment)
		return True
