#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Resources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**variable_QPushButton.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Custom Variable QPushButton Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Variable_QPushButton(QPushButton):
	"""
	This Class Is The Variable_QPushButton Class.
	"""

	@core.executionTrace
	def __init__(self, state, colors, labels, parent=None):
		"""
		This Method Initializes The Class.

		@param state: Current Button State. ( Boolean )
		@param colors: Button Colors. ( Tuple )
		@param labels: Button Texts. ( Tuple )
		@param parent: Widget Parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QPushButton.__init__(self, parent)

		# --- Setting Class Attributes. ---
		self.__state = None
		self.state = state

		self.__colors = None
		self.colors = colors

		self.__labels = None
		self.labels = labels

		self.__parent = None
		self.parent = parent

		# Initializing The Button
		self.setCheckable(True)
		if self.__state:
			self.__setTrueState()
		else:
			self.__setFalseState()

		# Signals / Slots.
		self.clicked.connect(self.__variable_QPushButton__clicked)

	#***********************************************************************************************
	#***	Attributes Properties
	#***********************************************************************************************
	@property
	def state(self):
		"""
		This Method Is The Property For The _state Attribute.

		@return: self.__state. ( Boolean )
		"""

		return self.__state

	@state.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def state(self, value):
		"""
		This Method Is The Setter Method For The _state Attribute.

		@param value: Attribute Value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' Attribute: '{1}' Type Is Not 'bool'!".format("activated", value)
		self.__state = value

	@state.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def state(self):
		"""
		This Method Is The Deleter Method For The _state Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("state"))

	@property
	def colors(self):
		"""
		This Method Is The Property For The _colors Attribute.

		@return: self.__colors. ( Tuple )
		"""

		return self.__colors

	@colors.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def colors(self, value):
		"""
		This Method Is The Setter Method For The _colors Attribute.

		@param value: Attribute Value. ( Tuple )
		"""
		if value:
			assert type(value) is tuple, "'{0}' Attribute: '{1}' Type Is Not 'tuple'!".format("colors", value)
			assert len(value) == 2, "'{0}' Attribute: '{1}' Length Should Be '2'!".format("colors", value)
			for index in range(len(value)):
				assert type(value[index]) is QColor, "'{0}' Attribute Element '{1}': '{2}' Type Is Not 'QColor'!".format("colors", index, value)
		self.__colors = value

	@colors.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def colors(self):
		"""
		This Method Is The Deleter Method For The _colors Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("colors"))

	@property
	def labels(self):
		"""
		This Method Is The Property For The _labels Attribute.

		@return: self.__labels. ( Tuple )
		"""

		return self.__labels

	@labels.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def labels(self, value):
		"""
		This Method Is The Setter Method For The _labels Attribute.

		@param value: Attribute Value. ( Tuple )
		"""
		if value:
			assert type(value) is tuple, "'{0}' Attribute: '{1}' Type Is Not 'tuple'!".format("labels", value)
			assert len(value) == 2, "'{0}' Attribute: '{1}' Length Should Be '2'!".format("labels", value)
			for index in range(len(value)):
				assert type(value[index]) in (str, unicode), "'{0}' Attribute Element '{1}': '{2}' Type Is Not 'str' or 'unicode'!".format("labels", index, value)
		self.__labels = value

	@labels.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def labels(self):
		"""
		This Method Is The Deleter Method For The _labels Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("labels"))

	@property
	def parent(self):
		"""
		This Method Is The Property For The _parent Attribute.

		@return: self.__parent. ( QObject )
		"""

		return self.__parent

	@parent.setter
	def parent(self, value):
		"""
		This Method Is The Setter Method For The _parent Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		self.__parent = value

	@parent.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parent(self):
		"""
		This Method Is The Deleter Method For The _parent Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("parent"))

	#***********************************************************************************************
	#***	Class Methods
	#***********************************************************************************************
	@core.executionTrace
	def __variable_QPushButton__clicked(self, checked):
		"""
		This Method Is Called When A Variable QPushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		if self.__state:
			self.__setFalseState()
		else:
			self.__setTrueState()

	@core.executionTrace
	def __setTrueState(self):
		"""
		This Method Sets The Variable Button True State.
		"""

		LOGGER.debug("> Setting Variable QPushButton() To 'True' State.")
		self.__state = True

		palette = QPalette()
		palette.setColor(QPalette.Button, self.__colors[0])
		self.setPalette(palette)

		self.setChecked(True)
		self.setText(self.__labels[0])

	@core.executionTrace
	def __setFalseState(self):
		"""
		This Method Sets The Variable QPushButton True State.
		"""

		LOGGER.debug("> Setting Variable QPushButton() To 'False' State.")

		self.__state = False

		palette = QPalette()
		palette.setColor(QPalette.Button, self.__colors[1])
		self.setPalette(palette)

		self.setChecked(False)
		self.setText(self.__labels[1])

#***********************************************************************************************
#***	Python End
#***********************************************************************************************

