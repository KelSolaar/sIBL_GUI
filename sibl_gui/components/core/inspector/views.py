#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_gui.components.core.inspector.inspector.Inspector`
	Component Interface class Views.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QListView

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import sibl_gui.ui.views

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Plates_QListView"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Plates_QListView(sibl_gui.ui.views.Abstract_QListView):
	"""
	Defines the view for Ibl Sets Plates as thumbnails.
	"""

	def __init__(self, parent, model=None, read_only=False, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param model: Model.
		:type model: QObject
		:param read_only: View is read only.
		:type read_only: bool
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.views.Abstract_QListView.__init__(self, parent, model, read_only, message)

		# --- Setting class attributes. ---
		self.__list_view_icon_size = 30

		Plates_QListView.__initialize_ui(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def list_view_icon_size(self):
		"""
		Property for **self.__list_view_icon_size** attribute.

		:return: self.__list_view_icon_size.
		:rtype: int
		"""

		return self.__list_view_icon_size

	@list_view_icon_size.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def list_view_icon_size(self, value):
		"""
		Setter for **self.__list_view_icon_size** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "list_view_icon_size"))

	@list_view_icon_size.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def list_view_icon_size(self):
		"""
		Deleter for **self.__list_view_icon_size** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "list_view_icon_size"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initialize_ui(self):
		"""
		Initializes the Widget ui.
		"""

		self.setAcceptDrops(False)
		self.setAutoScroll(True)
		self.setFlow(QListView.LeftToRight)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setMovement(QListView.Static)
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setViewMode(QListView.IconMode)
		self.setWrapping(False)

		self.__set_default_ui_state()

		# Signals / Slots.
		self.model().modelReset.connect(self.__set_default_ui_state)

	def __set_default_ui_state(self):
		"""
		Sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

		self.setMinimumSize(600, 52)
		self.setMaximumSize(16777215, 52)
		self.setIconSize(QSize(self.__list_view_icon_size, self.__list_view_icon_size))
