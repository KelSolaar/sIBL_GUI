#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**search_QLineEdit.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Custom search QLineEdit Module.

**Others:**

"""

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
class Search_QLineEdit(QLineEdit):
	"""
	This class is the Search_QLineEdit class.
	"""

	@core.executionTrace
	def __init__(self, uiClearImage=None, uiClearClickedImage=None, parent=None):
		"""
		This method initializes the class.

		:param uiClearImage: Icon path. ( String )
		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

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

		# Signals / Slots.
		self.__clearButton.clicked.connect(self.clear)
		self.textChanged.connect(self.__setClearButtonVisibility)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiClearImage(self):
		"""
		This method is the property for **self.__uiClearImage** attribute.

		:return: self.__uiClearImage. ( String )
		"""

		return self.__uiClearImage

	@uiClearImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiClearImage(self, value):
		"""
		This method is the setter method for **self.__uiClearImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("uiClearImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("uiClearImage", value)
		self.__uiClearImage = value

	@uiClearImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self):
		"""
		This method is the deleter method for **self.__uiClearImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiClearImage"))

	@property
	def uiClearClickedImage(self):
		"""
		This method is the property for **self.__uiClearClickedImage** attribute.

		:return: self.__uiClearClickedImage. ( String )
		"""

		return self.__uiClearClickedImage

	@uiClearClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiClearClickedImage(self, value):
		"""
		This method is the setter method for **self.__uiClearClickedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("uiClearClickedImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("uiClearClickedImage", value)
		self.__uiClearClickedImage = value

	@uiClearClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self):
		"""
		This method is the deleter method for **self.__uiClearClickedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiClearClickedImage"))

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
	def clearButton(self):
		"""
		This method is the property for **self.__clearButton** attribute.

		:return: self.__clearButton. ( QPushButton )
		"""

		return self.__clearButton

	@clearButton.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self, value):
		"""
		This method is the setter method for **self.__clearButton** attribute.

		:param value: Attribute value. ( QPushButton )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("clearButton"))

	@clearButton.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self):
		"""
		This method is the deleter method for **self.__clearButton** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("clearButton"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def resizeEvent(self, event):
		"""
		This method overloads the Search_QLineEdit resizeevent.

		:param event: Resize event. ( QResizeEvent )
		"""

		size = self.__clearButton.sizeHint()
		frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		self.__clearButton.move(self.rect().right() - frameWidth - size.width() + 1, (self.rect().bottom() - size.height()) / 2 + 1);

	@core.executionTrace
	def __setClearButtonStyle(self):
		"""
		This method sets the clear button style.
		"""

		self.__clearButton.setCursor(Qt.ArrowCursor)
		if self.__uiClearImage and self.__uiClearClickedImage:
			pixmap = QPixmap(self.__uiClearImage)
			clickedPixmap = QPixmap(self.__uiClearClickedImage)
			self.__clearButton.setStyleSheet("QToolButton { border: none; padding: 0px; }");
			self.__clearButton.setIcon(QIcon(pixmap))
			self.__clearButton.setMaximumSize(pixmap.size())

			# Signals / Slots.
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
		This method sets the clear button visibility.

		:param text: Current text. ( QString )
		"""

		if text:
			self.__clearButton.show()
		else:
			self.__clearButton.hide()

