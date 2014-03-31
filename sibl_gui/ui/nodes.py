#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application nodes classes.

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines a mixin used to bring common capabilities in Application Nodes classes.
	"""

	def __init__(self):
		"""
		Initializes the class.

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
		Property for **self.__iconSize** attribute.

		:return: self.__iconSize.
		:rtype: unicode
		"""

		return self.__iconSize

	@iconSize.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def iconSize(self, value):
		"""
		Setter for **self.__iconSize** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"iconSize", value)
		self.__iconSize = value

	@iconSize.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iconSize(self):
		"""
		Deleter for **self.__iconSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iconSize"))

	@property
	def iconPlaceholder(self):
		"""
		Property for **self.__iconPlaceholder** attribute.

		:return: self.__iconPlaceholder.
		:rtype: QIcon
		"""

		return self.__iconPlaceholder

	@iconPlaceholder.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def iconPlaceholder(self, value):
		"""
		Setter for **self.__iconPlaceholder** attribute.

		:param value: Attribute value.
		:type value: QIcon
		"""

		if value is not None:
			assert type(value) is QIcon, "'{0}' attribute: '{1}' type is not 'QIcon'!".format(
			"iconPlaceholder", value)
		self.__iconPlaceholder = value

	@iconPlaceholder.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iconPlaceholder(self):
		"""
		Deleter for **self.__iconPlaceholder** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iconPlaceholder"))

class GraphModelAttribute(umbra.ui.nodes.GraphModelAttribute, Mixin_GraphModelObject):
	"""
	Defines a storage object for the :class:`GraphModelNode` class attributes.
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
		Initializes the class.

		:param name: Attribute name.
		:type name: unicode
		:param value: Attribute value.
		:type value: object
		:param roles: Roles.
		:type roles: dict
		:param flags: Flags.
		:type flags: int
		:param iconSize: Icon size.
		:type iconSize: unicode
		:param iconPlaceholder: Icon placeholder.
		:type iconPlaceholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelAttribute.__init__(self, name, value, roles, flags, **kwargs)
		Mixin_GraphModelObject.__init__(self)

		# --- Setting class attributes. ---
		self.iconSize = iconSize if iconSize is not None else "Default"
		self.iconPlaceholder = iconPlaceholder

class GraphModelNode(umbra.ui.nodes.GraphModelNode, Mixin_GraphModelObject):
	"""
	Defines :class:`GraphModel` class base Node object.
	"""

	__family = "GraphModel"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

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
		Initializes the class.

		:param name: Node name.
		:type name: unicode
		:param parent: Node parent.
		:type parent: AbstractNode or AbstractCompositeNode
		:param children: Children.
		:type children: list
		:param roles: Roles.
		:type roles: dict
		:param flags: Flags. ( Qt.ItemFlag )
		:param iconSize: Icon size.
		:type iconSize: unicode
		:param iconPlaceholder: Icon placeholder.
		:type iconPlaceholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, flags, **kwargs)
		Mixin_GraphModelObject.__init__(self)

		# --- Setting class attributes. ---
		self.iconSize = iconSize if iconSize is not None else "Default"
		self.iconPlaceholder = iconPlaceholder
