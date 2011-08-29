#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**codeEditor_QPlainTextEdit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`LinesNumbers_QWidget` and :class:`CodeEditor_QPlainTextEdit` classes.

**Others:**
	Portions of the code from codeeditor.py by Roberto Alsina: http://lateral.netmanagers.com.ar/weblog/posts/BB832.html

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
class LinesNumbers_QWidget(QWidget):
	"""
	This class is a `QWidget <http://doc.qt.nokia.com/4.7/qwidget.html>`_ subclass providing a lines numbers widget.
	"""

	@core.executionTrace
	def __init__(self, editor):
		"""
		This method initializes the class.

		:param editor: Editor to attach the widget to. ( QTextEdit / QPlainTextEdit )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QWidget.__init__(self, editor)

		# --- Setting class attributes. ---
		self.__editor = editor

		self.__margin = 16

		self.setEditorViewportMargins(0)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def editor(self):
		"""
		This method is the property for **self.__editor** attribute.

		:return: self.__editor. ( QWidget )
		"""

		return self.__editor

	@editor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def editor(self, value):
		"""
		This method is the setter method for **self.__editor** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		self.__editor = value

	@editor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editor(self):
		"""
		This method is the deleter method for **self.__editor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("editor"))

	@property
	def margin(self):
		"""
		This method is the property for **self.__margin** attribute.

		:return: self.__margin. ( Integer )
		"""

		return self.__margin

	@margin.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def margin(self, value):
		"""
		This method is the setter method for **self.__margin** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("margin", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("margin", value)
		self.__margin = value

	@margin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def margin(self):
		"""
		This method is the deleter method for **self.__margin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("margin"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def sizeHint(self):
		"""
		This method reimplements the Widget **sizeHint** method.

		:return: Size hint. ( QSize )
		"""

		return QSize(self.__getWidth(), 0)

	@core.executionTrace
	def paintEvent(self, event):
		"""
		This method reimplements the Widget **paintEvent** method.
		
		:param event: Event. ( QEvent )
		"""

		painter = QPainter(self)
		painter.fillRect(event.rect(), QColor(96, 96, 96))

		block = self.__editor.firstVisibleBlock()
		blockNumber = block.blockNumber();
		top = int(self.__editor.blockBoundingGeometry(block).translated(self.__editor.contentOffset()).top())
		bottom = top + int(self.__editor.blockBoundingRect(block).height())

		while block.isValid() and top <= event.rect().bottom():
			if block.isVisible() and bottom >= event.rect().top():
				number = str(blockNumber + 1)
				painter.setPen(QColor(192, 192, 192))
				painter.drawText(-self.__margin / 4, top, self.width(), self.__editor.fontMetrics().height(), Qt.AlignRight, number)
			block = block.next()

			top = bottom
			bottom = top + int(self.__editor.blockBoundingRect(block).height())
			blockNumber += 1

	@core.executionTrace
	def __getWidth(self):
		"""
		This method returns the Widget target width.

		:return: Widget target width. ( Integer )
		"""

		return self.__margin + self.__editor.fontMetrics().width(str(max(1, self.__editor.blockCount())))

	@core.executionTrace
	def setEditorViewportMargins(self, newBlocksCount):
		"""
		This method sets the editor viewport margins.
		
		:param newBlocksCount: Updated editor blocks count. ( Integer )
		:return: Method success. ( Boolean )
		"""

		self.__editor.setViewportMargins(self.__getWidth(), 0, 0, 0)
		return True

	@core.executionTrace
	def updateRectangle(self, rectangle, scrollY):
		"""
		This method updates the provided widget rectangle.
		
		:param rectangle: Rectangle to update. ( QRect )
		:param scrollY: Amount of pixels the viewport was scrolled. ( Integer )
		:return: Method success. ( Boolean )
		"""

		if scrollY:
			self.scroll(0, scrollY);
		else:
			self.update(0, rectangle.y(), self.width(), rectangle.height())

		if rectangle.contains(self.__editor.viewport().rect()):
			self.setEditorViewportMargins(0)
		return True

	@core.executionTrace
	def updateGeometry(self):
		"""
		This method updates the widget geometry.
		
		:return: Method success. ( Boolean )
		"""

		self.setGeometry(self.__editor.contentsRect().left(), self.__editor.contentsRect().top(), self.__getWidth(), self.__editor.contentsRect().height())
		return True

class CodeEditor_QPlainTextEdit(QPlainTextEdit):
	"""
	This class is a `QPlainTextEdit <http://doc.qt.nokia.com/4.7/qplaintextedit.html>`_ subclass providing a code editor base class.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QPlainTextEdit.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__marginArea_LinesNumbers_widget = None

		self.initializeUi()
		self.highlightCurrentLine()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def marginArea_LinesNumbers_widget(self):
		"""
		This method is the property for **self.__marginArea_LinesNumbers_widget** attribute.

		:return: self.__marginArea_LinesNumbers_widget. ( LinesNumbers_QWidget )
		"""

		return self.__marginArea_LinesNumbers_widget

	@marginArea_LinesNumbers_widget.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def marginArea_LinesNumbers_widget(self, value):
		"""
		This method is the setter method for **self.__marginArea_LinesNumbers_widget** attribute.

		:param value: Attribute value. ( LinesNumbers_QWidget )
		"""

		if value:
			assert type(value) is LinesNumbers_QWidget, "'{0}' attribute: '{1}' type is not 'LinesNumbers_QWidget'!".format("checked", value)
		self.__marginArea_LinesNumbers_widget = value

	@marginArea_LinesNumbers_widget.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def marginArea_LinesNumbers_widget(self):
		"""
		This method is the deleter method for **self.__marginArea_LinesNumbers_widget** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("marginArea_LinesNumbers_widget"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the widget ui.
		
		:return: Method success. ( Boolean )		
		"""

		self.__marginArea_LinesNumbers_widget = LinesNumbers_QWidget(self)

		# Signals / Slots.
		self.blockCountChanged.connect(self.__marginArea_LinesNumbers_widget.setEditorViewportMargins)
		self.updateRequest.connect(self.__marginArea_LinesNumbers_widget.updateRectangle)
		self.cursorPositionChanged.connect(self.highlightCurrentLine)

		return True

	@core.executionTrace
	def resizeEvent(self, event):
		"""
		This method reimplements the Widget **resizeEvent** method.
		
		:param event: Event. ( QEvent )
		"""

		QPlainTextEdit.resizeEvent(self, event)
		self.__marginArea_LinesNumbers_widget.updateGeometry()

	@core.executionTrace
	def highlightCurrentLine(self):
		"""
		This method highlights the current line.
		
		:return: Method success. ( Boolean )		
		"""

		extraSelections = []
		if not self.isReadOnly():
			selection = QTextEdit.ExtraSelection()
			lineColor = QColor(Qt.yellow).lighter(160)
			selection.format.setBackground(lineColor)
			selection.format.setProperty(QTextFormat.FullWidthSelection, True)
			selection.cursor = self.textCursor()
			selection.cursor.clearSelection()
			extraSelections.append(selection)

		self.setExtraSelections(extraSelections)
		return True
