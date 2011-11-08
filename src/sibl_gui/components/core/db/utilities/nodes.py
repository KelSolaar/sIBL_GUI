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

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from PyQt4.QtCore import Qt

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
			"AbstractDatabaseNode",
			"IblSetNode",
			"TemplateNode",
			"CollectionNode"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class AbstractDatabaseNode(umbra.ui.models.GraphModelNode):
	"""
	This class defines Application Database abstract base class used by concrete Database node classes.
	"""

	__family = "AbstractDatabaseNode"

	@core.executionTrace
	def __init__(self, dbItem, name=None, parent=None, children=None, roles=None, nodeFlags=None, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled), ** kwargs):
		"""
		This method initializes the class.

		:param dbItem: Database object.  ( Object )
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

		# --- Setting class attributes. ---
		self.__dbItem = dbItem
		self.__toolTipText = str()

		AbstractDatabaseNode.__initializeNode(self, attributesFlags)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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

	@property
	def toolTipText(self):
		"""
		This method is the property for **self.__toolTipText** attribute.

		:return: self.__toolTipText. ( String )
		"""

		return self.__toolTipText

	@toolTipText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolTipText(self, value):
		"""
		This method is the setter method for **self.__toolTipText** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("toolTipText", value)
		self.__toolTipText = value

	@toolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolTipText(self):
		"""
		This method is the deleter method for **self.__toolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "toolTipText"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeNode(self, attributesFlags):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		for column in self.__dbItem.__table__.columns:
			attribute = column.key
			if attribute == "name":
				continue

			value = getattr(self.__dbItem, attribute)
			roles = {Qt.DisplayRole : value,
					Qt.EditRole : value}
			self[attribute] = umbra.ui.models.GraphModelAttribute(attribute, value, roles, attributesFlags)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeNodeAttributes(self):
		"""
		This method synchronizes the node attributes from the dbItem attributes.
		
		:return: Method success. ( Boolean )
		"""

		for column in self.__dbItem.__table__.columns:
			attribute = column.key
			if not attribute in self.keys():
				continue

			if issubclass(self[attribute].__class__, umbra.ui.models.GraphModelAttribute):
				self[attribute].value = self[attribute].roles[Qt.DisplayRole] = self[attribute].roles[Qt.EditRole] = getattr(self.__dbItem, attribute)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeDbItemAttributes(self):
		"""
		This method synchronizes the dbItem attributes from the node attributes.

		:return: Method success. ( Boolean )
		"""

		for column in self.__dbItem.__table__.columns:
			attribute = column.key
			if not attribute in self.keys():
				continue

			if issubclass(self[attribute].__class__, umbra.ui.models.GraphModelAttribute):
				setattr(self.__dbItem, attribute, self[attribute].value)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeNode(self):
		"""
		This method synchronizes the node from the dbItem.

		:return: Method success. ( Boolean )
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(self.__class__.__name__, self.synchronizeNode.__name__, self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeDbItem(self):
		"""
		This method synchronizes the dbItem from the node.

		:return: Method success. ( Boolean )
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(self.__class__.__name__, self.synchronizeDbItem.__name__, self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeToolTip(self):
		"""
		This method synchronizes the node tooltip.

		:return: Method success. ( Boolean )
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(self.__class__.__name__, self.synchronizeToolTip.__name__, self.__class__.__name__))

class IblSetNode(AbstractDatabaseNode):
	"""
	This class defines Ibl Sets nodes.
	"""

	__family = "IblSet"

	def __init__(self, dbItem, name=None, parent=None, children=None, roles=None, nodeFlags=None, attributesFlags=None, **kwargs):
		"""
		This method initializes the class.

		:param dbItem: Database object.  ( Object )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractDatabaseNode.__init__(self, dbItem, name, parent, children, roles, nodeFlags, attributesFlags, **kwargs)

		# --- Setting class attributes. ---
		self.toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Author: </b>{1}<br>
				<b>Location: </b>{2}<br>
				<b>Shot Date: </b>{3}<br>
				<b>Comment: </b>{4}</p>
				"""

		IblSetNode.__initializeNode(self)

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeNode(self):
		"""
		This method initializes the node.
		"""

		self.roles.update({Qt.DisplayRole : self.dbItem.title,
							Qt.DecorationRole : self.dbItem.icon,
							Qt.EditRole : self.dbItem.title})
		self.synchronizeToolTip()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeNode(self):
		"""
		This method synchronizes the node from the dbItem.

		:return: Method success. ( Boolean )
		"""

		self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = self.__dbItem.title
		return self.synchronizeNodeAttributes()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeDbItem(self):
		"""
		This method synchronizes the dbItem from the node.

		:return: Method success. ( Boolean )
		"""

		self.title = self.dbItem.title = self.name
		return self.synchronizeDbItemAttributes()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeToolTip(self):
		"""
		This method synchronizes the node tooltip.

		:return: Method success. ( Boolean )
		"""

		self.roles[Qt.ToolTipRole] = self.toolTipText.format(self.dbItem.title,
																self.dbItem.author or Constants.nullObject,
																self.dbItem.location or Constants.nullObject,
																sibl_gui.ui.common.getFormatedShotDate(self.dbItem.date, self.dbItem.time) or Constants.nullObject,
																self.dbItem.comment or Constants.nullObject)
		return True

class TemplateNode(AbstractDatabaseNode):
	"""
	This class defines Templates nodes.
	"""

	__family = "Template"

	def __init__(self, dbItem, name=None, parent=None, children=None, roles=None, nodeFlags=None, attributesFlags=None, **kwargs):
		"""
		This method initializes the class.

		:param dbItem: Database object.  ( Object )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractDatabaseNode.__init__(self, dbItem, name, parent, children, roles, nodeFlags, attributesFlags, **kwargs)

		# --- Setting class attributes. ---
		self.toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Author: </b>{1}<br>
				<b>Release Date: </b>{2}<br>
				<b>Comment: </b>{3}</p></p>
				"""

		TemplateNode.__initializeNode(self)

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeNode(self):
		"""
		This method initializes the node.
		"""

		self.roles.update({Qt.DisplayRole : "{0} {1}".format(self.dbItem.renderer, self.dbItem.title),
							Qt.EditRole : "{0} {1}".format(self.dbItem.renderer, self.dbItem.title)})
		self.synchronizeToolTip()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeNode(self):
		"""
		This method synchronizes the node from the dbItem.

		:return: Method success. ( Boolean )
		"""

		self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = self.__dbItem.title
		return self.synchronizeNodeAttributes()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeDbItem(self):
		"""
		This method synchronizes the dbItem from the node.

		:return: Method success. ( Boolean )
		"""

		self.title = self.dbItem.title = self.name
		return self.synchronizeDbItemAttributes()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeToolTip(self):
		"""
		This method synchronizes the node tooltip.

		:return: Method success. ( Boolean )
		"""

		self.roles[Qt.ToolTipRole] = self.toolTipText.format("{0} {1}".format(self.dbItem.renderer, self.dbItem.title),
																	self.dbItem.author,
																	self.dbItem.date,
																	self.dbItem.comment)
		return True

class CollectionNode(AbstractDatabaseNode):
	"""
	This class defines Collections nodes.
	"""

	__family = "Collection"

	def __init__(self, dbItem, name=None, parent=None, children=None, roles=None, nodeFlags=None, attributesFlags=None, **kwargs):
		"""
		This method initializes the class.

		:param dbItem: Database object.  ( Object )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractDatabaseNode.__init__(self, dbItem, name, parent, children, roles, nodeFlags, attributesFlags, **kwargs)

		# --- Setting class attributes. ---
		self.toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Comment: </b>{1}<br></p>
				"""

		CollectionNode.__initializeNode(self)

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeNode(self):
		"""
		This method initializes the node.
		"""

		self.roles.update({Qt.DisplayRole : self.dbItem.name,
			Qt.EditRole : self.dbItem.name})
		self["count"] = umbra.ui.models.GraphModelAttribute(name="count", value=None, flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
		self.synchronizeToolTip()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeNode(self):
		"""
		This method synchronizes the node from the dbItem.

		:return: Method success. ( Boolean )
		"""

		self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = self.dbItem.name
		return self.synchronizeNodeAttributes()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeDbItem(self):
		"""
		This method synchronizes the dbItem from the node.

		:return: Method success. ( Boolean )
		"""

		self.dbItem.name = self.name
		return self.synchronizeDbItemAttributes()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeToolTip(self):
		"""
		This method synchronizes the node tooltip.

		:return: Method success. ( Boolean )
		"""

		self.roles[Qt.ToolTipRole] = self.toolTipText.format(self.dbItem.name,
																self.dbItem.comment)
		return True
