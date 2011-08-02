#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**active_QLabel.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Custom active QLabel.

**Others:**

"""

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
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Active_QLabel(QLabel):
	"""
	This class is the Active_QLabel class.
	"""

	# Custom signals definitions.
	clicked = pyqtSignal()

	@core.executionTrace
	def __init__(self, defaultPixmap, hoverPixmap, activePixmap, checkable=False, checked=False, parent=None):
		"""
		This method initializes the class.

		:param defaultPixmap: Label default pixmap. ( QPixmap )
		:param hoverPixmap: Label hover pixmap. ( QPixmap )
		:param activePixmap: Label active pixmap. ( QPixmap )
		:param checkable: Checkable state. ( Boolean )
		:param checked: Checked state. ( Boolean )
		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QLabel.__init__(self, parent)

		# --- Setting class attributes. ---
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

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def defaultPixmap(self):
		"""
		This method is the property for **self.__defaultPixmap** attribute.

		:return: self.__defaultPixmap. ( QPixmap )
		"""

		return self.__defaultPixmap

	@defaultPixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultPixmap(self, value):
		"""
		This method is the setter method for **self.__defaultPixmap** attribute.

		:param value: Attribute value. ( QPixmap )
		"""

		if value:
			assert type(value) is QPixmap, "'{0}' attribute: '{1}' type is not 'QPixmap'!".format("checked", value)
		self.__defaultPixmap = value

	@defaultPixmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultPixmap(self):
		"""
		This method is the deleter method for **self.__defaultPixmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultPixmap"))

	@property
	def hoverPixmap(self):
		"""
		This method is the property for **self.__hoverPixmap** attribute.

		:return: self.__hoverPixmap. ( QPixmap )
		"""

		return self.__hoverPixmap

	@hoverPixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def hoverPixmap(self, value):
		"""
		This method is the setter method for **self.__hoverPixmap** attribute.

		:param value: Attribute value. ( QPixmap )
		"""

		if value:
			assert type(value) is QPixmap, "'{0}' attribute: '{1}' type is not 'QPixmap'!".format("checked", value)
		self.__hoverPixmap = value

	@hoverPixmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def hoverPixmap(self):
		"""
		This method is the deleter method for **self.__hoverPixmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("hoverPixmap"))

	@property
	def activePixmap(self):
		"""
		This method is the property for **self.__activePixmap** attribute.

		:return: self.__activePixmap. ( QPixmap )
		"""

		return self.__activePixmap

	@activePixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def activePixmap(self, value):
		"""
		This method is the setter method for **self.__activePixmap** attribute.

		:param value: Attribute value. ( QPixmap )
		"""

		if value:
			assert type(value) is QPixmap, "'{0}' attribute: '{1}' type is not 'QPixmap'!".format("checked", value)
		self.__activePixmap = value

	@activePixmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def activePixmap(self):
		"""
		This method is the deleter method for **self.__activePixmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("activePixmap"))

	@property
	def checkable(self):
		"""
		This method is the property for **self.__checkable** attribute.

		:return: self.__checkable. ( Boolean )
		"""

		return self.__checkable

	@checkable.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def checkable(self, value):
		"""
		This method is the setter method for **self.__checkable** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("checkable", value)
		self.__checkable = value

	@checkable.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def checkable(self):
		"""
		This method is the deleter method for **self.__checkable** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("checkable"))

	@property
	def checked(self):
		"""
		This method is the property for **self.__checked** attribute.

		:return: self.__checked. ( Boolean )
		"""

		return self.__checked

	@checked.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def checked(self, value):
		"""
		This method is the setter method for **self.__checked** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("checked", value)
		self.__checked = value

	@checked.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def checked(self):
		"""
		This method is the deleter method for **self.__checked** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("checked"))

	@property
	def parent(self):
		"""
		This method is the property for **self.__parent** attribute.

		:return: self.__parent. ( QObject )
		"""

		return self.__parent

	@parent.setter
	def parent(self, value):
		"""
		This method is the setter method for **self.__parent** attribute.

		:param value: Attribute value. ( QObject )
		"""

		self.__parent = value

	@parent.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parent(self):
		"""
		This method is the deleter method for **self.__parent** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("parent"))

	@property
	def menu(self):
		"""
		This method is the property for **self.__menu** attribute.

		:return: self.__menu. ( QMenu )
		"""

		return self.__menu

	@menu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menu(self, value):
		"""
		This method is the setter method for **self.__menu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("menu "))

	@menu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menu(self):
		"""
		This method is the deleter method for **self.__menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("menu"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def setChecked(self, state):
		"""
		This method sets the Widget checked state.

		:param state: New check state. ( Boolean )
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
		This method returns the Widget checked state.

		:return: Checked state. ( Boolean )
		"""

		return self.__checked

	@core.executionTrace
	def setMenu(self, menu):
		"""
		This method sets the Widget menu.

		:param menu: Menu. ( QMenu )
		"""

		self.__menu = menu

		# Propagating actions to parent.
		for action in self.__menu.actions():
			not action.shortcut().isEmpty() and self.__parent.addAction(action)

	@core.executionTrace
	def enterEvent(self, event):
		"""
		This method defines the mouse enter event.

		:param event: QEvent. ( QEvent )
		"""

		if self.__checkable:
			not self.__checked and self.setPixmap(self.__hoverPixmap)
		else:
			self.setPixmap(self.__hoverPixmap)

	@core.executionTrace
	def leaveEvent(self, event):
		"""
		This method defines the mouse leave event.

		:param event: QEvent. ( QEvent )
		"""

		if self.__checkable:
			not self.__checked and self.setPixmap(self.__defaultPixmap)
		else:
			self.setPixmap(self.__defaultPixmap)

	@core.executionTrace
	def mousePressEvent(self, event):
		"""
		This method defines the mouse press event.

		:param event: QEvent. ( QEvent )
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
		This method defines the mouse release event.

		:param event: QEvent. ( QEvent )
		"""

		not self.__checkable and	self.setPixmap(self.__defaultPixmap)

