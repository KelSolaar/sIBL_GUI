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
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	search_QLineEdit.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Custom Search QLineEdit Module.
***
***	Others:
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Search_QLineEdit(QLineEdit):
	'''
	This Class Is The Search_QLineEdit Class.
	'''

	@core.executionTrace
	def __init__(self, uiIconPath=None, uiClickedIconPath=None, parent=None):
		'''
		This Method Initializes The Class.

		@param uiIconPath: Icon Path. ( String )
		@param parent: Widget Parent. ( QObject )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QLineEdit.__init__(self, parent)

		# --- Setting Class Attributes. ---
		self._uiIconPath = None
		self.uiIconPath = uiIconPath
		self._uiClickedIconPath = None
		self.uiClickedIconPath = uiClickedIconPath
		self._parent = None
		self.parent = parent

		self._clearButton = QToolButton(self)
		self.setClearButtonStyle()
		self.setClearButtonVisibility(self.text())

		# Signals / Slots.
		self._clearButton.clicked.connect(self.clear)
		self.textChanged.connect(self.setClearButtonVisibility)

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiIconPath(self):
		'''
		This Method Is The Property For The _uiIconPath Attribute.

		@return: self._uiIconPath. ( String )
		'''

		return self._uiIconPath

	@uiIconPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiIconPath(self, value):
		'''
		This Method Is The Setter Method For The _uiIconPath Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("uiIconPath", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' File Doesn't Exists!".format("uiIconPath", value)
		self._uiIconPath = value

	@uiIconPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiIconPath(self):
		'''
		This Method Is The Deleter Method For The _uiIconPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiIconPath"))

	@property
	def uiClickedIconPath(self):
		'''
		This Method Is The Property For The _uiClickedIconPath Attribute.

		@return: self._uiClickedIconPath. ( String )
		'''

		return self._uiClickedIconPath

	@uiClickedIconPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiClickedIconPath(self, value):
		'''
		This Method Is The Setter Method For The _uiClickedIconPath Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("uiClickedIconPath", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' File Doesn't Exists!".format("uiClickedIconPath", value)
		self._uiClickedIconPath = value

	@uiClickedIconPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClickedIconPath(self):
		'''
		This Method Is The Deleter Method For The _uiClickedIconPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiClickedIconPath"))

	@property
	def parent(self):
		'''
		This Method Is The Property For The _parent Attribute.

		@return: self._parent. ( QObject )
		'''

		return self._parent

	@parent.setter
	def parent(self, value):
		'''
		This Method Is The Setter Method For The _parent Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		self._parent = value

	@parent.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parent(self):
		'''
		This Method Is The Deleter Method For The _parent Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("parent"))

	@property
	def clearButton(self):
		'''
		This Method Is The Property For The _clearButton Attribute.

		@return: self._clearButton. ( QPushButton )
		'''

		return self._clearButton

	@clearButton.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self, value):
		'''
		This Method Is The Setter Method For The _clearButton Attribute.

		@param value: Attribute Value. ( QPushButton )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("clearButton"))

	@clearButton.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self):
		'''
		This Method Is The Deleter Method For The _clearButton Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("clearButton"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************

	@core.executionTrace
	def resizeEvent(self, event):
		'''
		This Method Overloads The Search_QLineEdit ResizeEvent.
		
		@param event: Resize Event. ( QResizeEvent )
		'''

		size = self._clearButton.sizeHint()
		frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		offset = self._uiIconPath and self._uiClickedIconPath and 4 or 2
		self._clearButton.move(self.rect().right() - frameWidth - size.width(), (self.rect().bottom() + offset - size.height()) / 2);

	@core.executionTrace
	def setClearButtonStyle(self):
		'''
		This Method Sets The Clear Button Style.
		'''

		self._clearButton.setCursor(Qt.ArrowCursor)
		if self._uiIconPath and self._uiClickedIconPath:
			pixmap = QPixmap(self._uiIconPath)
			clickedPixmap = QPixmap(self._uiClickedIconPath)
			self._clearButton.setStyleSheet("QToolButton { border: none; padding: 0px; }");
			self._clearButton.setIcon(QIcon(pixmap))
			self._clearButton.setMaximumSize(pixmap.size())

			# Signals / Slots.
			self._clearButton.pressed.connect(lambda pixmap=clickedPixmap: self._clearButton.setIcon(QIcon(pixmap)))
			self._clearButton.released.connect(lambda pixmap=pixmap: self._clearButton.setIcon(QIcon(pixmap)))
		else:
			self._clearButton.setText("Clear")

		frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		self.setStyleSheet(QString("QLineEdit { padding-right: " + str(self._clearButton.sizeHint().width() + frameWidth)) + "px; }")
		self.setMinimumSize(max(self.minimumSizeHint().width(), self._clearButton.sizeHint().height() + frameWidth * 2), max(self.minimumSizeHint().height(), self._clearButton.sizeHint().height() + frameWidth * 2));

	@core.executionTrace
	def setClearButtonVisibility(self, text):
		'''
		This Method Sets The Clear Button Visibility.
		
		@param text: Current Text. ( QString )
		'''

		if text:
			self._clearButton.show()
		else:
			self._clearButton.hide()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************

