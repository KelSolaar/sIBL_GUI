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
**search_QLineEdit.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Custom Search QLineEdit Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import logging
import os
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
class Search_QLineEdit(QLineEdit):
	"""
	This Class Is The Search_QLineEdit Class.
	"""

	@core.executionTrace
	def __init__(self, uiClearImage=None, uiClearClickedImage=None, parent=None):
		"""
		This Method Initializes The Class.

		@param uiClearImage: Icon Path. ( String )
		@param parent: Widget Parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QLineEdit.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__uiClearImage = None
		self.uiClearImage = uiClearImage
		self.__uiClearClickedImage = None
		self.uiClearClickedImage = uiClearClickedImage
		self.__parent = None
		self.parent = parent

		self.__clearButton = QToolButton(self)
		self.__clearButton.setObjectName("Clear_Field_button")
		self.__setClearButtonStyle()
		self.__setClearButtonVisibility(self.text())

		# Signals / slots.
		self.__clearButton.clicked.connect(self.clear)
		self.textChanged.connect(self.__setClearButtonVisibility)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiClearImage(self):
		"""
		This Method Is The Property For The _uiClearImage Attribute.

		@return: self.__uiClearImage. ( String )
		"""

		return self.__uiClearImage

	@uiClearImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiClearImage(self, value):
		"""
		This Method Is The Setter Method For The _uiClearImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("uiClearImage", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' File Doesn't Exists!".format("uiClearImage", value)
		self.__uiClearImage = value

	@uiClearImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self):
		"""
		This Method Is The Deleter Method For The _uiClearImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiClearImage"))

	@property
	def uiClearClickedImage(self):
		"""
		This Method Is The Property For The _uiClearClickedImage Attribute.

		@return: self.__uiClearClickedImage. ( String )
		"""

		return self.__uiClearClickedImage

	@uiClearClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiClearClickedImage(self, value):
		"""
		This Method Is The Setter Method For The _uiClearClickedImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("uiClearClickedImage", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' File Doesn't Exists!".format("uiClearClickedImage", value)
		self.__uiClearClickedImage = value

	@uiClearClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self):
		"""
		This Method Is The Deleter Method For The _uiClearClickedImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiClearClickedImage"))

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

	@property
	def clearButton(self):
		"""
		This Method Is The Property For The _clearButton Attribute.

		@return: self.__clearButton. ( QPushButton )
		"""

		return self.__clearButton

	@clearButton.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self, value):
		"""
		This Method Is The Setter Method For The _clearButton Attribute.

		@param value: Attribute Value. ( QPushButton )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("clearButton"))

	@clearButton.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self):
		"""
		This Method Is The Deleter Method For The _clearButton Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("clearButton"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def resizeEvent(self, event):
		"""
		This Method Overloads The Search_QLineEdit ResizeEvent.

		@param event: Resize Event. ( QResizeEvent )
		"""

		size = self.__clearButton.sizeHint()
		frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		self.__clearButton.move(self.rect().right() - frameWidth - size.width() + 1, (self.rect().bottom() - size.height()) / 2 + 1);

	@core.executionTrace
	def __setClearButtonStyle(self):
		"""
		This Method Sets The Clear Button Style.
		"""

		self.__clearButton.setCursor(Qt.ArrowCursor)
		if self.__uiClearImage and self.__uiClearClickedImage:
			pixmap = QPixmap(self.__uiClearImage)
			clickedPixmap = QPixmap(self.__uiClearClickedImage)
			self.__clearButton.setStyleSheet("QToolButton { border: none; padding: 0px; }");
			self.__clearButton.setIcon(QIcon(pixmap))
			self.__clearButton.setMaximumSize(pixmap.size())

			# Signals / slots.
			self.__clearButton.pressed.connect(functools.partial(self.__clearButton.setIcon, QIcon(clickedPixmap)))
			self.__clearButton.released.connect(functools.partial(self.__clearButton.setIcon, QIcon(pixmap)))
		else:
			self.__clearButton.setText("Clear")

		frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		self.setStyleSheet(QString("QLineEdit { padding-right: " + str(self.__clearButton.sizeHint().width() + frameWidth)) + "px; }")
		self.setMinimumSize(max(self.minimumSizeHint().width(), self.__clearButton.sizeHint().height() + frameWidth * 2), max(self.minimumSizeHint().height(), self.__clearButton.sizeHint().height() + frameWidth * 2));

	@core.executionTrace
	def __setClearButtonVisibility(self, text):
		"""
		This Method Sets The Clear Button Visibility.

		@param text: Current Text. ( QString )
		"""

		if text:
			self.__clearButton.show()
		else:
			self.__clearButton.hide()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************

