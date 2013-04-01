#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application nodes classes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtGui import QIcon

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.ui.nodes

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
		"Mixin_GraphModelObject",
		"GraphModelAttribute",
		"GraphModelNode"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Mixin_GraphModelObject(object):
	"""
	This class is a mixin used to bring common capabilities in Application Nodes classes.
	"""

	def __init__(self):
		"""
		This method initializes the class.

		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__iconSize = None
		self.__iconPlaceholder = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def iconSize(self):
		"""
		This method is the property for **self.__iconSize** attribute.

		:return: self.__iconSize. ( String )
		"""

		return self.__iconSize

	@iconSize.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def iconSize(self, value):
		"""
		This method is the setter method for **self.__iconSize** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"iconSize", value)
		self.__iconSize = value

	@iconSize.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iconSize(self):
		"""
		This method is the deleter method for **self.__iconSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iconSize"))

	@property
	def iconPlaceholder(self):
		"""
		This method is the property for **self.__iconPlaceholder** attribute.

		:return: self.__iconPlaceholder. ( QIcon )
		"""

		return self.__iconPlaceholder

	@iconPlaceholder.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def iconPlaceholder(self, value):
		"""
		This method is the setter method for **self.__iconPlaceholder** attribute.

		:param value: Attribute value. ( QIcon )
		"""

		if value is not None:
			assert type(value) is QIcon, "'{0}' attribute: '{1}' type is not 'QIcon'!".format(
			"iconPlaceholder", value)
		self.__iconPlaceholder = value

	@iconPlaceholder.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iconPlaceholder(self):
		"""
		This method is the deleter method for **self.__iconPlaceholder** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iconPlaceholder"))

class GraphModelAttribute(umbra.ui.nodes.GraphModelAttribute, Mixin_GraphModelObject):
	"""
	This class represents a storage object for the :class:`GraphModelNode` class attributes.
	"""

	def __init__(self,
				name=None,
				value=None,
				roles=None,
				flags=None,
				iconSize=None,
				iconPlaceholder=None,
				**kwargs):
		"""
		This method initializes the class.

		:param name: Attribute name. ( String )
		:param value: Attribute value. ( Object )
		:param roles: Roles. ( Dictionary )
		:param flags: Flags. ( Integer )
		:param iconSize: Icon size.  ( String )
		:param iconPlaceholder: Icon placeholder.  ( QIcon )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelAttribute.__init__(self, name, value, roles, flags, **kwargs)
		Mixin_GraphModelObject.__init__(self)

		# --- Setting class attributes. ---
		self.iconSize = iconSize if iconSize is not None else "Default"
		self.iconPlaceholder = iconPlaceholder

class GraphModelNode(umbra.ui.nodes.GraphModelNode, Mixin_GraphModelObject):
	"""
	This class defines :class:`GraphModel` class base Node object.
	"""

	__family = "GraphModel"
	"""Node family. ( String )"""

	def __init__(self,
				name=None,
				parent=None,
				children=None,
				roles=None,
				flags=None,
				iconSize=None,
				iconPlaceholder=None,
				**kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param parent: Node parent. ( AbstractNode / AbstractCompositeNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param flags: Flags. ( Qt.ItemFlag )
		:param iconSize: Icon size.  ( String )
		:param iconPlaceholder: Icon placeholder.  ( QIcon )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, flags, **kwargs)
		Mixin_GraphModelObject.__init__(self)

		# --- Setting class attributes. ---
		self.iconSize = iconSize if iconSize is not None else "Default"
		self.iconPlaceholder = iconPlaceholder
