#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines Application nodes classes related to Database objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import sibl_gui.components.core.database.operations
import sibl_gui.ui.common
import sibl_gui.ui.nodes
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Returns the Template user name.

	:param title: Template title.
	:type title: unicode
	:param software: Template software.
	:type software: unicode
	:return: Template user name.
	:rtype: unicode
	"""

	return foundations.strings.removeStrip(title, software)

class AbstractDatabaseNode(sibl_gui.ui.nodes.GraphModelNode):
	"""
	Defines Application Database abstract base class used by concrete Database Node classes.
	"""

	__family = "AbstractDatabaseNode"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

	def __init__(self,
				databaseItem,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=None,
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled),
				iconSize=None,
				iconPlaceholder=None,
				**kwargs):
		"""
		Initializes the class.

		:param databaseItem: Database object.
		:type databaseItem: object
		:param name: Node name.
		:type name: unicode
		:param parent: Node parent.
		:type parent: GraphModelNode
		:param children: Children.
		:type children: list
		:param roles: Roles.
		:type roles: dict
		:param nodeFlags: Node flags.
		:type nodeFlags: int
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		:param iconSize: Icon size.
		:type iconSize: unicode
		:param iconPlaceholder: Icon placeholder.
		:type iconPlaceholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.nodes.GraphModelNode.__init__(self,
												name,
												parent,
												children,
												roles,
												nodeFlags,
												iconSize,
												iconPlaceholder,
												**kwargs)

		# --- Setting class attributes. ---
		self.__databaseItem = databaseItem
		self.__toolTipText = ""

		AbstractDatabaseNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def databaseItem(self):
		"""
		Property for **self.__databaseItem** attribute.

		:return: self.__databaseItem.
		:rtype: object
		"""

		return self.__databaseItem

	@databaseItem.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseItem(self, value):
		"""
		Setter for **self.__databaseItem** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseItem"))

	@databaseItem.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseItem(self):
		"""
		Deleter for **self.__databaseItem** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseItem"))

	@property
	def toolTipText(self):
		"""
		Property for **self.__toolTipText** attribute.

		:return: self.__toolTipText.
		:rtype: unicode
		"""

		return self.__toolTipText

	@toolTipText.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def toolTipText(self, value):
		"""
		Setter for **self.__toolTipText** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"toolTipText", value)
		self.__toolTipText = value

	@toolTipText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def toolTipText(self):
		"""
		Deleter for **self.__toolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "toolTipText"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		Initializes the node.

		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		"""

		for column in self.__databaseItem.__table__.columns:
			attribute = column.key
			if attribute == "name":
				continue

			value = getattr(self.__databaseItem, attribute)
			roles = {Qt.DisplayRole : value,
					Qt.EditRole : value}
			self[attribute] = sibl_gui.ui.nodes.GraphModelAttribute(attribute, value, roles, attributesFlags)

	def updateNode(self):
		"""
		Updates the Node from the database item.

		:return: Method success.
		:rtype: bool
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(
		self.__class__.__name__, self.updateNode.__name__, self.__class__.__name__))

	def updateNodeAttributes(self):
		"""
		Updates the Node attributes from the database item attributes.

		:return: Method success.
		:rtype: bool
		"""

		for column in self.__databaseItem.__table__.columns:
			attribute = column.key
			if not attribute in self:
				continue

			if issubclass(self[attribute].__class__, sibl_gui.ui.nodes.GraphModelAttribute):
				self[attribute].value = self[attribute].roles[Qt.DisplayRole] = self[attribute].roles[Qt.EditRole] = \
				getattr(self.__databaseItem, attribute)
		return True

	def updateDatabaseItem(self):
		"""
		Updates the database item from the node.

		:return: Method success.
		:rtype: bool
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(
		self.__class__.__name__, self.updateDatabaseItem.__name__, self.__class__.__name__))

	def updateDatabaseItemAttributes(self):
		"""
		Updates the database item attributes from the Node attributes.

		:return: Method success.
		:rtype: bool
		"""

		for column in self.__databaseItem.__table__.columns:
			attribute = column.key
			if not attribute in self:
				continue

			if issubclass(self[attribute].__class__, sibl_gui.ui.nodes.GraphModelAttribute):
				setattr(self.__databaseItem, attribute, self[attribute].value)
		return True

	@foundations.exceptions.handleExceptions(NotImplementedError)
	def updateToolTip(self):
		"""
		Updates the Node tooltip.

		:return: Method success.
		:rtype: bool
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(
		self.__class__.__name__, self.updateToolTip.__name__, self.__class__.__name__))

class IblSetNode(AbstractDatabaseNode):
	"""
	Defines Ibl Sets nodes.
	"""

	__family = "IblSet"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

	def __init__(self,
				databaseItem,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=None,
				attributesFlags=None,
				iconPath=None,
				iconSize=None,
				iconPlaceholder=None,
				**kwargs):
		"""
		Initializes the class.

		:param databaseItem: Database object.
		:type databaseItem: object
		:param name: Node name.
		:type name: unicode
		:param parent: Node parent.
		:type parent: GraphModelNode
		:param children: Children.
		:type children: list
		:param roles: Roles.
		:type roles: dict
		:param nodeFlags: Node flags.
		:type nodeFlags: int
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		:param iconPath: Icon path.
		:type iconPath: unicode
		:param iconSize: Icon size.
		:type iconSize: unicode
		:param iconPlaceholder: Icon placeholder.
		:type iconPlaceholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractDatabaseNode.__init__(self,
									databaseItem,
									name,
									parent,
									children,
									roles,
									nodeFlags,
									attributesFlags,
									iconSize,
									iconPlaceholder,
									**kwargs)

		# --- Setting class attributes. ---
		self.__iconPath = iconPath
		self.toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Author: </b>{1}<br>
				<b>Location: </b>{2}<br>
				<b>Shot Date: </b>{3}<br>
				<b>Comment: </b>{4}</p>
				"""

		IblSetNode.__initializeNode(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def iconPath(self):
		"""
		Property for **self.__iconPath** attribute.

		:return: self.__iconPath.
		:rtype: unicode
		"""

		return self.__iconPath

	@iconPath.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iconPath(self, value):
		"""
		Setter for **self.__iconPath** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iconPath"))

	@iconPath.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iconPath(self):
		"""
		Deleter for **self.__iconPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iconPath"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self):
		"""
		Initializes the node.
		"""

		self.roles.update({Qt.DisplayRole : self.databaseItem.title,
							Qt.DecorationRole : foundations.common.filterPath(self.__iconPath),
							Qt.EditRole : self.databaseItem.title})
		self.updateToolTip()

	def updateNode(self):
		"""
		Updates the node from the database item.

		:return: Method success.
		:rtype: bool
		"""

		self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = self.__databaseItem.title
		return self.updateNodeAttributes()

	def updateNodeAttributes(self):
		"""
		Updates the node attributes from the database item attributes.

		:return: Method success.
		:rtype: bool
		"""

		return AbstractDatabaseNode.updateNodeAttributes(self)

	def updateDatabaseItem(self):
		"""
		Updates the database item from the node.

		:return: Method success.
		:rtype: bool
		"""

		self.title = self.databaseItem.title = self.name
		return self.updateDatabaseItemAttributes()

	def updateToolTip(self):
		"""
		Updates the node tooltip.

		:return: Method success.
		:rtype: bool
		"""

		self.roles[Qt.ToolTipRole] = self.toolTipText.format(self.databaseItem.title,
															self.databaseItem.author or Constants.nullObject,
															self.databaseItem.location or Constants.nullObject,
															sibl_gui.ui.common.getFormattedShotDate(self.databaseItem.date,
																			self.databaseItem.time) or Constants.nullObject,
															self.databaseItem.comment or Constants.nullObject)
		return True

class TemplateNode(AbstractDatabaseNode):
	"""
	Defines Templates nodes.
	"""

	__family = "Template"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

	def __init__(self,
				databaseItem,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=None,
				attributesFlags=None,
				iconSize=None,
				iconPlaceholder=None,
				**kwargs):
		"""
		Initializes the class.

		:param databaseItem: Database object.
		:type databaseItem: object
		:param name: Node name.
		:type name: unicode
		:param parent: Node parent.
		:type parent: GraphModelNode
		:param children: Children.
		:type children: list
		:param roles: Roles.
		:type roles: dict
		:param nodeFlags: Node flags.
		:type nodeFlags: int
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		:param iconSize: Icon size.
		:type iconSize: unicode
		:param iconPlaceholder: Icon placeholder.
		:type iconPlaceholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractDatabaseNode.__init__(self,
									databaseItem,
									name,
									parent,
									children,
									roles,
									nodeFlags,
									attributesFlags,
									iconSize,
									iconPlaceholder,
									**kwargs)

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
		Initializes the node.
		"""

		templateUserName = getTemplateUserName(self.databaseItem.title, self.databaseItem.software)
		self.roles.update({Qt.DisplayRole : templateUserName,
							Qt.EditRole : templateUserName})
		self.updateToolTip()

	def updateNode(self):
		"""
		Updates the node from the database item.

		:return: Method success.
		:rtype: bool
		"""

		self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = getTemplateUserName(self.databaseItem.title,
																								self.databaseItem.software)

		return self.updateNodeAttributes()

	def updateNodeAttributes(self):
		"""
		Updates the node attributes from the database item attributes.

		:return: Method success.
		:rtype: bool
		"""

		return AbstractDatabaseNode.updateNodeAttributes(self)

	def updateDatabaseItem(self):
		"""
		Updates the database item from the node.

		:return: Method success.
		:rtype: bool
		"""

		self.title = self.databaseItem.title = self.name
		return self.updateDatabaseItemAttributes()

	def updateToolTip(self):
		"""
		Updates the node tooltip.

		:return: Method success.
		:rtype: bool
		"""

		self.roles[Qt.ToolTipRole] = self.toolTipText.format(getTemplateUserName(self.databaseItem.title,
																				self.databaseItem.software),
																	self.databaseItem.author,
																	self.databaseItem.date,
																	self.databaseItem.comment)
		return True

class CollectionNode(AbstractDatabaseNode):
	"""
	Defines Collections nodes.
	"""

	__family = "Collection"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

	def __init__(self,
				databaseItem,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=None,
				attributesFlags=None,
				iconSize=None,
				iconPlaceholder=None,
				**kwargs):
		"""
		Initializes the class.

		:param databaseItem: Database object.
		:type databaseItem: object
		:param name: Node name.
		:type name: unicode
		:param parent: Node parent.
		:type parent: GraphModelNode
		:param children: Children.
		:type children: list
		:param roles: Roles.
		:type roles: dict
		:param nodeFlags: Node flags.
		:type nodeFlags: int
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		:param iconSize: Icon size.
		:type iconSize: unicode
		:param iconPlaceholder: Icon placeholder.
		:type iconPlaceholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractDatabaseNode.__init__(self,
									databaseItem,
									name,
									parent,
									children,
									roles,
									nodeFlags,
									attributesFlags,
									iconSize,
									iconPlaceholder,
									**kwargs)

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
		Initializes the node.
		"""

		self["count"] = sibl_gui.ui.nodes.GraphModelAttribute(
						name="count",
						value=sibl_gui.components.core.database.operations.getCollectionIblSetsCount(self.databaseItem),
						flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

		self.roles.update({Qt.DisplayRole : self.databaseItem.name, Qt.EditRole : self.databaseItem.name})
		self.updateToolTip()

	def updateNode(self):
		"""
		Updates the node from the database item.

		:return: Method success.
		:rtype: bool
		"""

		self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = self.databaseItem.name
		return self.updateNodeAttributes()

	def updateNodeAttributes(self):
		"""
		Updates the node attributes from the database item attributes.

		:return: Method success.
		:rtype: bool
		"""

		self.count.value = self.count.roles[Qt.DisplayRole] = \
		sibl_gui.components.core.database.operations.getCollectionIblSetsCount(self.databaseItem)

		return AbstractDatabaseNode.updateNodeAttributes(self)

	def updateDatabaseItem(self):
		"""
		Updates the database item from the node.

		:return: Method success.
		:rtype: bool
		"""

		self.databaseItem.name = self.name
		return self.updateDatabaseItemAttributes()

	def updateToolTip(self):
		"""
		Updates the node tooltip.

		:return: Method success.
		:rtype: bool
		"""

		self.roles[Qt.ToolTipRole] = self.toolTipText.format(self.databaseItem.name,
																self.databaseItem.comment)
		return True
