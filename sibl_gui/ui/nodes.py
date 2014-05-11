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

from __future__ import unicode_literals

from PyQt4.QtGui import QIcon

import foundations.exceptions
import foundations.verbose
import umbra.ui.nodes

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

LOGGER = foundations.verbose.install_logger()

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
		self.__icon_size = None
		self.__icon_placeholder = None

	@property
	def icon_size(self):
		"""
		Property for **self.__icon_size** attribute.

		:return: self.__icon_size.
		:rtype: unicode
		"""

		return self.__icon_size

	@icon_size.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def icon_size(self, value):
		"""
		Setter for **self.__icon_size** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"icon_size", value)
		self.__icon_size = value

	@icon_size.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def icon_size(self):
		"""
		Deleter for **self.__icon_size** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "icon_size"))

	@property
	def icon_placeholder(self):
		"""
		Property for **self.__icon_placeholder** attribute.

		:return: self.__icon_placeholder.
		:rtype: QIcon
		"""

		return self.__icon_placeholder

	@icon_placeholder.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def icon_placeholder(self, value):
		"""
		Setter for **self.__icon_placeholder** attribute.

		:param value: Attribute value.
		:type value: QIcon
		"""

		if value is not None:
			assert type(value) is QIcon, "'{0}' attribute: '{1}' type is not 'QIcon'!".format(
			"icon_placeholder", value)
		self.__icon_placeholder = value

	@icon_placeholder.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def icon_placeholder(self):
		"""
		Deleter for **self.__icon_placeholder** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "icon_placeholder"))

class GraphModelAttribute(umbra.ui.nodes.GraphModelAttribute, Mixin_GraphModelObject):
	"""
	Defines a storage object for the :class:`GraphModelNode` class attributes.
	"""

	def __init__(self,
				name=None,
				value=None,
				roles=None,
				flags=None,
				icon_size=None,
				icon_placeholder=None,
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
		:param icon_size: Icon size.
		:type icon_size: unicode
		:param icon_placeholder: Icon placeholder.
		:type icon_placeholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelAttribute.__init__(self, name, value, roles, flags, **kwargs)
		Mixin_GraphModelObject.__init__(self)

		# --- Setting class attributes. ---
		self.icon_size = icon_size if icon_size is not None else "Default"
		self.icon_placeholder = icon_placeholder

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
				icon_size=None,
				icon_placeholder=None,
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
		:param icon_size: Icon size.
		:type icon_size: unicode
		:param icon_placeholder: Icon placeholder.
		:type icon_placeholder: QIcon
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, flags, **kwargs)
		Mixin_GraphModelObject.__init__(self)

		# --- Setting class attributes. ---
		self.icon_size = icon_size if icon_size is not None else "Default"
		self.icon_placeholder = icon_placeholder
