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
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**variable_QPushButton.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Custom variable QPushButton Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Variable_QPushButton(QPushButton):
	"""
	This class is the Variable_QPushButton class.
	"""

	@core.executionTrace
	def __init__(self, state, colors, labels, parent=None):
		"""
		This method initializes the class.

		@param state: Current button state. ( Boolean )
		@param colors: Button colors. ( Tuple )
		@param labels: Button texts. ( Tuple )
		@param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QPushButton.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__state = None
		self.state = state

		self.__colors = None
		self.colors = colors

		self.__labels = None
		self.labels = labels

		self.__parent = None
		self.parent = parent

		# Initializing the button
		self.setCheckable(True)
		if self.__state:
			self.__setTrueState()
		else:
			self.__setFalseState()

		# Signals / slots.
		self.clicked.connect(self.__variable_QPushButton__clicked)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def state(self):
		"""
		This method is the property for the _state attribute.

		@return: self.__state. ( Boolean )
		"""

		return self.__state

	@state.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def state(self, value):
		"""
		This method is the setter method for the _state attribute.

		@param value: Attribute value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("activated", value)
		self.__state = value

	@state.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def state(self):
		"""
		This method is the deleter method for the _state attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("state"))

	@property
	def colors(self):
		"""
		This method is the property for the _colors attribute.

		@return: self.__colors. ( Tuple )
		"""

		return self.__colors

	@colors.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def colors(self, value):
		"""
		This method is the setter method for the _colors attribute.

		@param value: Attribute value. ( Tuple )
		"""
		if value:
			assert type(value) is tuple, "'{0}' attribute: '{1}' type is not 'tuple'!".format("colors", value)
			assert len(value) == 2, "'{0}' attribute: '{1}' length should be '2'!".format("colors", value)
			for index in range(len(value)):
				assert type(value[index]) is QColor, "'{0}' attribute element '{1}': '{2}' type is not 'QColor'!".format("colors", index, value)
		self.__colors = value

	@colors.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def colors(self):
		"""
		This method is the deleter method for the _colors attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("colors"))

	@property
	def labels(self):
		"""
		This method is the property for the _labels attribute.

		@return: self.__labels. ( Tuple )
		"""

		return self.__labels

	@labels.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def labels(self, value):
		"""
		This method is the setter method for the _labels attribute.

		@param value: Attribute value. ( Tuple )
		"""
		if value:
			assert type(value) is tuple, "'{0}' attribute: '{1}' type is not 'tuple'!".format("labels", value)
			assert len(value) == 2, "'{0}' attribute: '{1}' length should be '2'!".format("labels", value)
			for index in range(len(value)):
				assert type(value[index]) in (str, unicode), "'{0}' attribute element '{1}': '{2}' type is not 'str' or 'unicode'!".format("labels", index, value)
		self.__labels = value

	@labels.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def labels(self):
		"""
		This method is the deleter method for the _labels attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("labels"))

	@property
	def parent(self):
		"""
		This method is the property for the _parent attribute.

		@return: self.__parent. ( QObject )
		"""

		return self.__parent

	@parent.setter
	def parent(self, value):
		"""
		This method is the setter method for the _parent attribute.

		@param value: Attribute value. ( QObject )
		"""

		self.__parent = value

	@parent.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parent(self):
		"""
		This method is the deleter method for the _parent attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("parent"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __variable_QPushButton__clicked(self, checked):
		"""
		This method is called when a Variable_QPushButton is clicked.

		@param checked: Checked state. ( Boolean )
		"""

		if self.__state:
			self.__setFalseState()
		else:
			self.__setTrueState()

	@core.executionTrace
	def __setTrueState(self):
		"""
		This method sets the variable button true state.
		"""

		LOGGER.debug("> Setting variable QPushButton() to 'True' state.")
		self.__state = True

		palette = QPalette()
		palette.setColor(QPalette.Button, self.__colors[0])
		self.setPalette(palette)

		self.setChecked(True)
		self.setText(self.__labels[0])

	@core.executionTrace
	def __setFalseState(self):
		"""
		This method sets the variable QPushButton true state.
		"""

		LOGGER.debug("> Setting variable QPushButton() to 'False' state.")

		self.__state = False

		palette = QPalette()
		palette.setColor(QPalette.Button, self.__colors[1])
		self.setPalette(palette)

		self.setChecked(False)
		self.setText(self.__labels[1])

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************

