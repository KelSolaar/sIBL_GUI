#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_gui.components.core.inspector.inspector.Inspector`
	Component Interface class nodes.

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
import foundations.exceptions
import foundations.verbose
import sibl_gui.ui.nodes

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "PlatesNode"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class PlatesNode(sibl_gui.ui.nodes.GraphModelNode):
	"""
	Defines :class:`sibl_gui.components.core.inspector.inspector.Inspector`
		Component Interface class Model Plates node.
	"""

	__family = "Plate"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

	def __init__(self,
				plate,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				iconSize=None,
				iconPlaceholder=None,
				**kwargs):
		"""
		Initializes the class.

		:param plate: Plate object.
		:type plate: Plate
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
		self.__plate = plate

		self.__toolTipText = """
								<p><b>{0}</b></p>
								"""

		PlatesNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def plate(self):
		"""
		Property for **self.__plate** attribute.

		:return: self.__plate.
		:rtype: Plate
		"""

		return self.__plate

	@plate.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def plate(self, value):
		"""
		Setter for **self.__plate** attribute.

		:param value: Attribute value.
		:type value: Plate
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "plate"))

	@plate.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def plate(self):
		"""
		Deleter for **self.__plate** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "plate"))

	@property
	def toolTipText(self):
		"""
		Property for **self.__toolTipText** attribute.

		:return: self.__toolTipText.
		:rtype: unicode
		"""

		return self.__toolTipText

	@toolTipText.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def toolTipText(self, value):
		"""
		Setter for **self.__toolTipText** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "toolTipText"))

	@toolTipText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def toolTipText(self):
		"""
		Deleter for **self.__toolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "plate"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		Initializes the node.
		
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		"""

		self.roles.update({Qt.ToolTipRole : self.__toolTipText.format(self.name)})
