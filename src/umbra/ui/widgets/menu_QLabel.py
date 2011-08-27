#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**menu_QLabel.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Menu_QLabel` class.

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
class Menu_QLabel(QLabel):
	"""
	This class is a `QLabel <http://doc.qt.nokia.com/4.7/qlabel.html>`_ subclass providing a menu label with hovering capabilities.
	"""

	# Custom signals definitions.
	clicked = pyqtSignal()

	@core.executionTrace
	def __init__(self, label=None, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QLabel.__init__(self, label, parent)

		# --- Setting class attributes. ---
		self.__label = None
		self.label = label
		self.__parent = None
		self.parent = parent

		self.__menu = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def label(self):
		"""
		This method is the property for **self.__label** attribute.

		:return: self.__label. ( String )
		"""

		return self.__label

	@label.setter
	def label(self, value):
		"""
		This method is the setter method for **self.__label** attribute.

		:param value: Attribute value. ( String )
		"""

		self.__label = value

	@label.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def label(self):
		"""
		This method is the deleter method for **self.__label** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("label"))

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
	def mousePressEvent(self, event):
		"""
		This method defines the mouse press event.

		:param event: QEvent. ( QEvent )
		"""

		self.emit(SIGNAL("clicked()"))

		self.__menu and self.__menu.exec_(QCursor.pos())
