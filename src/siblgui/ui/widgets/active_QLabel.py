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

"""
************************************************************************************************
***	active_QLabel.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Custom Active QLabel.
***
***	Others:
***
************************************************************************************************
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
from siblgui.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Active_QLabel(QLabel):
	"""
	This Class Is The Active_QLabel Class.
	"""

	# Custom Signals Definitions.
	clicked = pyqtSignal()

	@core.executionTrace
	def __init__(self, defaultPixmap, hoverPixmap, activePixmap, checkable=False, checked=False, parent=None):
		"""
		This Method Initializes The Class.

		@param defaultPixmap: Label Default Pixmap. ( QPixmap )
		@param hoverPixmap: Label Hover Pixmap. ( QPixmap )
		@param activePixmap: Label Active Pixmap. ( QPixmap )
		@param checkable: Checkable State. ( Boolean )
		@param checked: Checked State. ( Boolean )
		@param parent: Widget Parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QLabel.__init__(self, parent)

		# --- Setting Class Attributes. ---
		self.__defaultPixmap = defaultPixmap
		self.__hoverPixmap = hoverPixmap
		self.__activePixmap = activePixmap

		self.__checkable = None
		self.checkable = checkable
		self.__checked = None
		self.checked = checked

		self.__parent = None
		self.parent = parent

		self.__menu = None

		self.__checked and self.setPixmap(self.__activePixmap) or self.setPixmap(self.__defaultPixmap)

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def defaultPixmap(self):
		"""
		This Method Is The Property For The _defaultPixmap Attribute.

		@return: self.__defaultPixmap. ( QPixmap )
		"""

		return self.__defaultPixmap

	@defaultPixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultPixmap(self, value):
		"""
		This Method Is The Setter Method For The _defaultPixmap Attribute.

		@param value: Attribute Value. ( QPixmap )
		"""

		if value:
			assert type(value) is QPixmap, "'{0}' Attribute: '{1}' Type Is Not 'QPixmap'!".format("checked", value)
		self.__defaultPixmap = value

	@defaultPixmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultPixmap(self):
		"""
		This Method Is The Deleter Method For The _defaultPixmap Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("defaultPixmap"))

	@property
	def hoverPixmap(self):
		"""
		This Method Is The Property For The _hoverPixmap Attribute.

		@return: self.__hoverPixmap. ( QPixmap )
		"""

		return self.__hoverPixmap

	@hoverPixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def hoverPixmap(self, value):
		"""
		This Method Is The Setter Method For The _hoverPixmap Attribute.

		@param value: Attribute Value. ( QPixmap )
		"""

		if value:
			assert type(value) is QPixmap, "'{0}' Attribute: '{1}' Type Is Not 'QPixmap'!".format("checked", value)
		self.__hoverPixmap = value

	@hoverPixmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def hoverPixmap(self):
		"""
		This Method Is The Deleter Method For The _hoverPixmap Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("hoverPixmap"))

	@property
	def activePixmap(self):
		"""
		This Method Is The Property For The _activePixmap Attribute.

		@return: self.__activePixmap. ( QPixmap )
		"""

		return self.__activePixmap

	@activePixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def activePixmap(self, value):
		"""
		This Method Is The Setter Method For The _activePixmap Attribute.

		@param value: Attribute Value. ( QPixmap )
		"""

		if value:
			assert type(value) is QPixmap, "'{0}' Attribute: '{1}' Type Is Not 'QPixmap'!".format("checked", value)
		self.__activePixmap = value

	@activePixmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def activePixmap(self):
		"""
		This Method Is The Deleter Method For The _activePixmap Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("activePixmap"))

	@property
	def checkable(self):
		"""
		This Method Is The Property For The _checkable Attribute.

		@return: self.__checkable. ( Boolean )
		"""

		return self.__checkable

	@checkable.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def checkable(self, value):
		"""
		This Method Is The Setter Method For The _checkable Attribute.

		@param value: Attribute Value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' Attribute: '{1}' Type Is Not 'bool'!".format("checkable", value)
		self.__checkable = value

	@checkable.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def checkable(self):
		"""
		This Method Is The Deleter Method For The _checkable Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("checkable"))

	@property
	def checked(self):
		"""
		This Method Is The Property For The _checked Attribute.

		@return: self.__checked. ( Boolean )
		"""

		return self.__checked

	@checked.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def checked(self, value):
		"""
		This Method Is The Setter Method For The _checked Attribute.

		@param value: Attribute Value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' Attribute: '{1}' Type Is Not 'bool'!".format("checked", value)
		self.__checked = value

	@checked.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def checked(self):
		"""
		This Method Is The Deleter Method For The _checked Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("checked"))

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
	def menu(self):
		"""
		This Method Is The Property For The _menu Attribute.

		@return: self.__menu. ( QMenu )
		"""

		return self.__menu

	@menu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menu(self, value):
		"""
		This Method Is The Setter Method For The _menu Attribute.

		@param value: Attribute Value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("menu "))

	@menu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menu(self):
		"""
		This Method Is The Deleter Method For The _menu Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("menu"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def setChecked(self, state):
		"""
		This Method Sets The Widget Checked State.
		
		@param state: New Check State. ( Boolean )
		"""

		if state:
			self.__checked = True
			self.setPixmap(self.__activePixmap)
		else:
			self.__checked = False
			self.setPixmap(self.__defaultPixmap)

	@core.executionTrace
	def isChecked(self):
		"""
		This Method Returns The Widget Checked State.
		
		@return: Checked State. ( Boolean )
		"""

		return self.__checked

	@core.executionTrace
	def setMenu(self, menu):
		"""
		This Method Sets The Widget Menu.
		
		@param menu: Menu. ( QMenu )
		"""

		self.__menu = menu

		# Propagating Actions To Parent.
		for action in self.__menu.actions():
			not action.shortcut().isEmpty() and self.__parent.addAction(action)

	@core.executionTrace
	def enterEvent(self, event):
		"""
		This Method Defines The Mouse Enter Event.
		
		@param event: QEvent. ( QEvent )
		"""

		if self.__checkable:
			not self.__checked and self.setPixmap(self.__hoverPixmap)
		else:
			self.setPixmap(self.__hoverPixmap)

	@core.executionTrace
	def leaveEvent(self, event):
		"""
		This Method Defines The Mouse Leave Event.
		
		@param event: QEvent. ( QEvent )
		"""

		if self.__checkable:
			not self.__checked and self.setPixmap(self.__defaultPixmap)
		else:
			self.setPixmap(self.__defaultPixmap)

	@core.executionTrace
	def mousePressEvent(self, event):
		"""
		This Method Defines The Mouse Press Event.
		
		@param event: QEvent. ( QEvent )
		"""

		self.emit(SIGNAL("clicked()"))

		if self.__checkable:
			self.setChecked(True)
		else:
			self.setPixmap(self.__activePixmap)
			self.__menu and self.__menu.exec_(QCursor.pos())

	@core.executionTrace
	def mouseReleaseEvent(self, event):
		"""
		This Method Defines The Mouse Release Event.
		
		@param event: QEvent. ( QEvent )
		"""

		not self.__checkable and	self.setPixmap(self.__defaultPixmap)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************

