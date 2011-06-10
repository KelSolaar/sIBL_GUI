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
from globals.constants import Constants

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
		self._defaultPixmap = defaultPixmap
		self._hoverPixmap = hoverPixmap
		self._activePixmap = activePixmap

		self._checkable = None
		self.checkable = checkable
		self._checked = None
		self.checked = checked

		self._parent = None
		self.parent = parent

		self._menu = None

		self._checked and self.setPixmap(self._activePixmap) or self.setPixmap(self._defaultPixmap)

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def defaultPixmap(self):
		"""
		This Method Is The Property For The _defaultPixmap Attribute.

		@return: self._defaultPixmap. ( QPixmap )
		"""

		return self._defaultPixmap

	@defaultPixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultPixmap(self, value):
		"""
		This Method Is The Setter Method For The _defaultPixmap Attribute.

		@param value: Attribute Value. ( QPixmap )
		"""

		if value:
			assert type(value) is QPixmap, "'{0}' Attribute: '{1}' Type Is Not 'QPixmap'!".format("checked", value)
		self._defaultPixmap = value

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

		@return: self._hoverPixmap. ( QPixmap )
		"""

		return self._hoverPixmap

	@hoverPixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def hoverPixmap(self, value):
		"""
		This Method Is The Setter Method For The _hoverPixmap Attribute.

		@param value: Attribute Value. ( QPixmap )
		"""

		if value:
			assert type(value) is QPixmap, "'{0}' Attribute: '{1}' Type Is Not 'QPixmap'!".format("checked", value)
		self._hoverPixmap = value

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

		@return: self._activePixmap. ( QPixmap )
		"""

		return self._activePixmap

	@activePixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def activePixmap(self, value):
		"""
		This Method Is The Setter Method For The _activePixmap Attribute.

		@param value: Attribute Value. ( QPixmap )
		"""

		if value:
			assert type(value) is QPixmap, "'{0}' Attribute: '{1}' Type Is Not 'QPixmap'!".format("checked", value)
		self._activePixmap = value

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

		@return: self._checkable. ( Boolean )
		"""

		return self._checkable

	@checkable.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def checkable(self, value):
		"""
		This Method Is The Setter Method For The _checkable Attribute.

		@param value: Attribute Value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' Attribute: '{1}' Type Is Not 'bool'!".format("checkable", value)
		self._checkable = value

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

		@return: self._checked. ( Boolean )
		"""

		return self._checked

	@checked.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def checked(self, value):
		"""
		This Method Is The Setter Method For The _checked Attribute.

		@param value: Attribute Value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' Attribute: '{1}' Type Is Not 'bool'!".format("checked", value)
		self._checked = value

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

		@return: self._parent. ( QObject )
		"""

		return self._parent

	@parent.setter
	def parent(self, value):
		"""
		This Method Is The Setter Method For The _parent Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		self._parent = value

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

		@return: self._menu. ( QMenu )
		"""

		return self._menu

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
			self._checked = True
			self.setPixmap(self._activePixmap)
		else:
			self._checked = False
			self.setPixmap(self._defaultPixmap)

	@core.executionTrace
	def isChecked(self):
		"""
		This Method Returns The Widget Checked State.
		
		@return: Checked State. ( Boolean )
		"""

		return self._checked

	@core.executionTrace
	def setMenu(self, menu):
		"""
		This Method Sets The Widget Menu.
		
		@param menu: Menu. ( QMenu )
		"""

		self._menu = menu

		# Propagating Actions To Parent.
		for action in self._menu.actions():
			not action.shortcut().isEmpty() and self._parent.addAction(action)

	@core.executionTrace
	def enterEvent(self, event):
		"""
		This Method Defines The Mouse Enter Event.
		
		@param event: QEvent. ( QEvent )
		"""

		if self._checkable:
			not self._checked and self.setPixmap(self._hoverPixmap)
		else:
			self.setPixmap(self._hoverPixmap)

	@core.executionTrace
	def leaveEvent(self, event):
		"""
		This Method Defines The Mouse Leave Event.
		
		@param event: QEvent. ( QEvent )
		"""

		if self._checkable:
			not self._checked and self.setPixmap(self._defaultPixmap)
		else:
			self.setPixmap(self._defaultPixmap)

	@core.executionTrace
	def mousePressEvent(self, event):
		"""
		This Method Defines The Mouse Press Event.
		
		@param event: QEvent. ( QEvent )
		"""

		self.emit(SIGNAL("clicked()"))

		if self._checkable:
			self.setChecked(True)
		else:
			self.setPixmap(self._activePixmap)
			self._menu and self._menu.exec_(QCursor.pos())

	@core.executionTrace
	def mouseReleaseEvent(self, event):
		"""
		This Method Defines The Mouse Release Event.
		
		@param event: QEvent. ( QEvent )
		"""

		not self._checkable and	self.setPixmap(self._defaultPixmap)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************

