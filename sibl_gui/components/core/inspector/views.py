#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`sibl_gui.components.core.inspector.inspector.Inspector`
	Component Interface class Views.

**Others:**

"""

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
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Plates_QListView"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Plates_QListView(sibl_gui.ui.views.Abstract_QListView):
	"""
	This class is used to display Ibl Sets Plates as thumbnails.
	"""

	def __init__(self, parent, model=None, readOnly=False, message=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param model: Model. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		:param message: View default message when Model is empty. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		sibl_gui.ui.views.Abstract_QListView.__init__(self, parent, model, readOnly, message)

		# --- Setting class attributes. ---
		self.__listViewIconSize = 30

		Plates_QListView.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def listViewIconSize(self):
		"""
		This method is the property for **self.__listViewIconSize** attribute.

		:return: self.__listViewIconSize. ( Integer )
		"""

		return self.__listViewIconSize

	@listViewIconSize.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def listViewIconSize(self, value):
		"""
		This method is the setter method for **self.__listViewIconSize** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "listViewIconSize"))

	@listViewIconSize.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def listViewIconSize(self):
		"""
		This method is the deleter method for **self.__listViewIconSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "listViewIconSize"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
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

		self.__setDefaultUiState()

		# Signals / Slots.
		self.model().modelReset.connect(self.__setDefaultUiState)

	def __setDefaultUiState(self):
		"""
		This method sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

		self.setMinimumSize(600, 52)
		self.setMaximumSize(16777215, 52)
		self.setIconSize(QSize(self.__listViewIconSize, self.__listViewIconSize))
