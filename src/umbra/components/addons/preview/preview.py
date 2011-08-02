#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preview.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Preview Component Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import logging
import os
import platform
import re
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.libraries.freeImage.freeImage as freeImage
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from foundations.parser import Parser
from manager.uiComponent import UiComponent
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
class Image_QGraphicsItem(QGraphicsItem):
	"""
	This class is the **Image_QGraphicsItem** class.
	"""

	@core.executionTrace
	def __init__(self, image):
		"""
		This method initializes the class.

		:param image: Image. ( QImage )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QGraphicsItem.__init__(self)

		# --- Setting class attributes. ---
		self.__image = image
		self.__width = image.width()
		self.__height = image.height()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def image(self):
		"""
		This method is the property for **self.__image** attribute.

		:return: self.__image. ( QImage )
		"""

		return self.__image

	@image.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def image(self, value):
		"""
		This method is the setter method for **self.__image** attribute.

		:param value: Attribute value. ( QImage )
		"""

		if value:
			assert type(value) is QImage, "'{0}' attribute: '{1}' type is not 'QImage'!".format("image", value)
		self.__image = value

	@image.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def image(self):
		"""
		This method is the deleter method for **self.__image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("image"))

	@property
	def width(self):
		"""
		This method is the property for **self.__width** attribute.

		:return: self.__width. ( Integer )
		"""

		return self.__width

	@width.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def width(self, value):
		"""
		This method is the setter method for **self.__width** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("width", value)
		self.__width = value

	@width.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def width(self):
		"""
		This method is the deleter method for **self.__width** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("width"))

	@property
	def height(self):
		"""
		This method is the property for **self.__height** attribute.

		:return: self.__height. ( Integer )
		"""

		return self.__height

	@height.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def height(self, value):
		"""
		This method is the setter method for **self.__height** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("height", value)
		self.__height = value

	@height.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def height(self):
		"""
		This method is the deleter method for **self.__height** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("height"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def boundingRect(self):
		"""
		This method sets the bounding rectangle.
		"""

		return QRectF(-(self.__image.width()) / 2, -(self.__image.height()) / 2, self.__image.width(), self.__image.height())

	@core.executionTrace
	def paint(self, painter, options, widget):
		"""
		This method paints the image.

		:param painter: QPainter ( QPainter )
		:param options: QStyleOptionGraphicsItem ( QStyleOptionGraphicsItem )
		:param widget: QWidget ( QWidget )
		"""

		painter.drawImage(-(self.__image.width() / 2), -(self.__image.height() / 2), self.__image)

class ImagesPreviewer(object):
	"""
	This is the **ImagesPreviewer** class.
	"""

	@core.executionTrace
	def __init__(self, container, paths=None):
		"""
		This method initializes the class.

		:param container: Container. ( Object )
		:param paths: Images paths. ( List )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__container = container
		self.__paths = None
		self.paths = paths

		self.__uiPath = "ui/Images_Previewer.ui"
		self.__uiPath = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = "resources"
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__uiPreviousImage = "Previous.png"
		self.__uiNextImage = "Next.png"
		self.__uiZoomOutImage = "Zoom_Out.png"
		self.__uiZoomInImage = "Zoom_In.png"

		self.__ui = uic.loadUi(self.__uiPath)
		if "." in sys.path:
			sys.path.remove(".")
		# Ensure the ui object is destroyed on close to avoid memory leaks.
		self.__ui.setAttribute(Qt.WA_DeleteOnClose)
		# Reimplementing widget close event method.
		self.__ui.closeEvent = self.closeUi

		self.__graphicsSceneBackgroundColor = QColor(48, 48, 48)
		self.__minimumZoomFactor = 0.05
		self.__maximumZoomFactor = 25
		self.__previewerMargin = 128
		self.__displayGraphicsItemMargin = 32
		self.__graphicsSceneWidth = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).width() * (1 / self.__minimumZoomFactor * 1.75)
		self.__graphicsSceneHeight = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).height() * (1 / self.__minimumZoomFactor * 1.75)
		self.__wheelZoomFactor = 350.0
		self.__keyZoomFactor = 1.20

		self.__graphicsView = None
		self.__graphicsScene = None
		self.__displayGraphicsItem = None

		self.initializeUi()

		self.__ui.show()

		self.fitImage()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def paths(self):
		"""
		This method is the property for **self.__paths** attribute.

		:return: self.__paths. ( List )
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def paths(self, value):
		"""
		This method is the setter method for **self.__paths** attribute.

		:param value: Attribute value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("paths", value)
		self.__paths = value

	@paths.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		This method is the deleter method for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("paths"))

	@property
	def uiPath(self):
		"""
		This method is the property for **self.__uiPath** attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for **self.__uiPath** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for **self.__uiPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This method is the property for **self.__uiResources** attribute.

		:return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for **self.__uiResources** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for **self.__uiResources** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiPreviousImage(self):
		"""
		This method is the property for **self.__uiPreviousImage** attribute.

		:return: self.__uiPreviousImage. ( String )
		"""

		return self.__uiPreviousImage

	@uiPreviousImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self, value):
		"""
		This method is the setter method for **self.__uiPreviousImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self):
		"""
		This method is the deleter method for **self.__uiPreviousImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPreviousImage"))

	@property
	def uiNextImage(self):
		"""
		This method is the property for **self.__uiNextImage** attribute.

		:return: self.__uiNextImage. ( String )
		"""

		return self.__uiNextImage

	@uiNextImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self, value):
		"""
		This method is the setter method for **self.__uiNextImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self):
		"""
		This method is the deleter method for **self.__uiNextImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiNextImage"))

	@property
	def uiZoomOutImage(self):
		"""
		This method is the property for **self.__uiZoomOutImage** attribute.

		:return: self.__uiZoomOutImage. ( String )
		"""

		return self.__uiZoomOutImage

	@uiZoomOutImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self, value):
		"""
		This method is the setter method for **self.__uiZoomOutImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiZoomOutImage"))

	@uiZoomOutImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self):
		"""
		This method is the deleter method for **self.__uiZoomOutImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiZoomOutImage"))

	@property
	def uiZoomInImage(self):
		"""
		This method is the property for **self.__uiZoomInImage** attribute.

		:return: self.__uiZoomInImage. ( String )
		"""

		return self.__uiZoomInImage

	@uiZoomInImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self, value):
		"""
		This method is the setter method for **self.__uiZoomInImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiZoomInImage"))

	@uiZoomInImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self):
		"""
		This method is the deleter method for **self.__uiZoomInImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiZoomInImage"))

	@property
	def ui(self):
		"""
		This method is the property for **self.__ui** attribute.

		:return: self.__ui. ( Object )
		"""

		return self.__ui

	@ui.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self, value):
		"""
		This method is the setter method for **self.__ui** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("ui"))

	@ui.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self):
		"""
		This method is the deleter method for **self.__ui** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("ui"))

	@property
	def graphicsSceneBackgroundColor(self):
		"""
		This method is the property for **self.__graphicsSceneBackgroundColor** attribute.

		:return: self.__graphicsSceneBackgroundColor. ( QColors )
		"""

		return self.__graphicsSceneBackgroundColor

	@graphicsSceneBackgroundColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self, value):
		"""
		This method is the setter method for **self.__graphicsSceneBackgroundColor** attribute.

		:param value: Attribute value. ( QColors )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("graphicsSceneBackgroundColor"))

	@graphicsSceneBackgroundColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self):
		"""
		This method is the deleter method for **self.__graphicsSceneBackgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("graphicsSceneBackgroundColor"))

	@property
	def previewerMargin(self):
		"""
		This method is the property for **self.__previewerMargin** attribute.

		:return: self.__previewerMargin. ( Integer )
		"""

		return self.__previewerMargin

	@previewerMargin.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewerMargin(self, value):
		"""
		This method is the setter method for **self.__previewerMargin** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("previewerMargin"))

	@previewerMargin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewerMargin(self):
		"""
		This method is the deleter method for **self.__previewerMargin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("previewerMargin"))

	@property
	def graphicsSceneWidth(self):
		"""
		This method is the property for **self.__graphicsSceneWidth** attribute.

		:return: self.__graphicsSceneWidth. ( Integer )
		"""

		return self.__graphicsSceneWidth

	@graphicsSceneWidth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self, value):
		"""
		This method is the setter method for **self.__graphicsSceneWidth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("graphicsSceneWidth"))

	@graphicsSceneWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self):
		"""
		This method is the deleter method for **self.__graphicsSceneWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("graphicsSceneWidth"))

	@property
	def graphicsSceneHeight(self):
		"""
		This method is the property for **self.__graphicsSceneHeight** attribute.

		:return: self.__graphicsSceneHeight. ( Object )
		"""

		return self.__graphicsSceneHeight

	@graphicsSceneHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self, value):
		"""
		This method is the setter method for **self.__graphicsSceneHeight** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("graphicsSceneHeight"))

	@graphicsSceneHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self):
		"""
		This method is the deleter method for **self.__graphicsSceneHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("graphicsSceneHeight"))

	@property
	def minimumZoomFactor(self):
		"""
		This method is the property for **self.__minimumZoomFactor** attribute.

		:return: self.__minimumZoomFactor. ( Float )
		"""

		return self.__minimumZoomFactor

	@minimumZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self, value):
		"""
		This method is the setter method for **self.__minimumZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("minimumZoomFactor"))

	@minimumZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self):
		"""
		This method is the deleter method for **self.__minimumZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("minimumZoomFactor"))

	@property
	def maximumZoomFactor(self):
		"""
		This method is the property for **self.__maximumZoomFactor** attribute.

		:return: self.__maximumZoomFactor. ( Float )
		"""

		return self.__maximumZoomFactor

	@maximumZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self, value):
		"""
		This method is the setter method for **self.__maximumZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("maximumZoomFactor"))

	@maximumZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self):
		"""
		This method is the deleter method for **self.__maximumZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("maximumZoomFactor"))

	@property
	def wheelZoomFactor(self):
		"""
		This method is the property for **self.__wheelZoomFactor** attribute.

		:return: self.__wheelZoomFactor. ( Float )
		"""

		return self.__wheelZoomFactor

	@wheelZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self, value):
		"""
		This method is the setter method for **self.__wheelZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("wheelZoomFactor"))

	@wheelZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self):
		"""
		This method is the deleter method for **self.__wheelZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("wheelZoomFactor"))

	@property
	def keyZoomFactor(self):
		"""
		This method is the property for **self.__keyZoomFactor** attribute.

		:return: self.__keyZoomFactor. ( Float )
		"""

		return self.__keyZoomFactor

	@keyZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self, value):
		"""
		This method is the setter method for **self.__keyZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("keyZoomFactor"))

	@keyZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self):
		"""
		This method is the deleter method for **self.__keyZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("keyZoomFactor"))

	@property
	def graphicsView(self):
		"""
		This method is the property for **self.__graphicsView** attribute.

		:return: self.__graphicsView. ( QGraphicsView )
		"""

		return self.__graphicsView

	@graphicsView.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsView(self, value):
		"""
		This method is the setter method for **self.__graphicsView** attribute.

		:param value: Attribute value. ( QGraphicsView )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("graphicsView"))

	@graphicsView.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsView(self):
		"""
		This method is the deleter method for **self.__graphicsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("graphicsView"))

	@property
	def graphicsScene(self):
		"""
		This method is the property for **self.__graphicsScene** attribute.

		:return: self.__graphicsScene. ( QGraphicsScene )
		"""

		return self.__graphicsScene

	@graphicsScene.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsScene(self, value):
		"""
		This method is the setter method for **self.__graphicsScene** attribute.

		:param value: Attribute value. ( QGraphicsScene )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("graphicsScene"))

	@graphicsScene.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsScene(self):
		"""
		This method is the deleter method for **self.__graphicsScene** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("graphicsScene"))

	@property
	def displayGraphicsItem(self):
		"""
		This method is the property for **self.__displayGraphicsItem** attribute.

		:return: self.__displayGraphicsItem. ( QGraphicsItem )
		"""

		return self.__displayGraphicsItem

	@displayGraphicsItem.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self, value):
		"""
		This method is the setter method for **self.__displayGraphicsItem** attribute.

		:param value: Attribute value. ( QGraphicsItem )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("displayGraphicsItem"))

	@displayGraphicsItem.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self):
		"""
		This method is the deleter method for **self.__displayGraphicsItem** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("displayGraphicsItem"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		LOGGER.debug("> Initializing '{0}' ui.".format(self.__class__.__name__))

		self.ui.Previous_Image_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiPreviousImage)))
		self.ui.Next_Image_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiNextImage)))
		self.__ui.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiZoomInImage)))
		self.__ui.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiZoomOutImage)))
		len(self.__paths) <= 1 and self.ui.Navigation_groupBox.hide()

		LOGGER.debug("> Initializing graphics View.")
		self.__graphicsView = QGraphicsView()
		self.__graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.__graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.__graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		self.__graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
		# Reimplementing QGraphicsView wheelEvent method.
		self.__graphicsView.wheelEvent = self.wheelEvent

		LOGGER.debug("> Initializing graphics scene.")
		self.__graphicsScene = QGraphicsScene(self.__graphicsView)
		self.__graphicsScene.setItemIndexMethod(QGraphicsScene.NoIndex)
		self.__graphicsScene.setSceneRect(-(float(self.__graphicsSceneWidth)) / 2, -(float(self.__graphicsSceneHeight)) / 2, float(self.__graphicsSceneWidth), float(self.__graphicsSceneHeight))

		self.__graphicsView.setScene(self.__graphicsScene)
		self.__graphicsView.setBackgroundBrush(QBrush(self.__graphicsSceneBackgroundColor))

		self.setImage()
		self.fitPreviewer()

		self.__ui.Images_Previewer_frame_gridLayout.addWidget(self.__graphicsView)

		# Signals / Slots.
		self.ui.Previous_Image_pushButton.clicked.connect(self.__Previous_Image_pushButton__clicked)
		self.ui.Next_Image_pushButton.clicked.connect(self.__Next_Image_pushButton__clicked)
		self.ui.Zoom_Out_pushButton.clicked.connect(self.__Zoom_Out_pushButton__clicked)
		self.ui.Zoom_In_pushButton.clicked.connect(self.__Zoom_In_pushButton_clicked)
		self.ui.Zoom_Fit_pushButton.clicked.connect(self.__Zoom_Fit_pushButton__clicked)

	@core.executionTrace
	def closeUi(self, event):
		"""
		This method redefines the ui close event.

		:param event: QEvent ( QEvent )
		"""

		event.accept()

		LOGGER.debug("> Removing '{0}' from Images Previewers list.".format(self))
		self.__container.imagesPreviewers.remove(self)

	@core.executionTrace
	def wheelEvent(self, event):
		"""
		This method redefines wheelevent.

		:param event: QEvent ( QEvent )
		"""

		self.scaleView(pow(1.5, event.delta() / self.__wheelZoomFactor))

	@core.executionTrace
	def keyPressEvent(self, event):
		"""
		This method redefines keypressevent.

		:param event: QEvent ( QEvent )
		"""

		key = event.key()
		if key == Qt.Key_Plus:
			self.scaleView(self.__keyZoomFactor)
		elif key == Qt.Key_Minus:
			self.scaleView(1 / self.__keyZoomFactor)
		else:
			QGraphicsView.keyPressEvent(self, event)

	@core.executionTrace
	def __Previous_Image_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Previous_Image_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughImages(True)

	@core.executionTrace
	def __Next_Image_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Next_Image_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughImages()

	@core.executionTrace
	def __Zoom_In_pushButton_clicked(self, checked):
		"""
		This method is triggered when **Zoom_In_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.scaleView(self.__keyZoomFactor)

	@core.executionTrace
	def __Zoom_Out_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Zoom_Out_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.scaleView(1 / self.__keyZoomFactor)

	@core.executionTrace
	def __Zoom_Fit_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Zoom_Fit_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.fitImage()

	@core.executionTrace
	def scaleView(self, scaleFactor):
		"""
		This method scales the QGraphicsView.

		:param scaleFactor: Float ( Float )
		"""

		graphicsView = self.__ui.findChild(QGraphicsView)
		factor = graphicsView.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
		if factor < self.__minimumZoomFactor or factor > self.__maximumZoomFactor:
			return

		graphicsView.scale(scaleFactor, scaleFactor)

	@core.executionTrace
	def fitPreviewer(self):
		"""
		This method fits the previewer window.
		"""

		if self.__displayGraphicsItem:
			desktopWidth = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).width()
			desktopHeight = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).height()
			width = self.__displayGraphicsItem.width > desktopWidth and desktopWidth / 1.5 + self.__previewerMargin or self.__displayGraphicsItem.width + self.__previewerMargin
			height = self.__displayGraphicsItem.height > desktopHeight and desktopHeight / 1.5 + self.__previewerMargin or self.__displayGraphicsItem.height + self.__previewerMargin

			self.__ui.resize(width, height)
			umbra.ui.common.centerWidgetOnScreen(self.__ui)

	@core.executionTrace
	def setImage(self, index=0):
		"""
		This method sets the display image.

		:param index: Index to display. ( Integer )
		"""

		if self.__paths:
			path = self.__paths[index]
			image = umbra.ui.common.getImage(path)
			if not hasattr(image, "_datas"):
				image._datas = freeImage.ImageInformationsHeader(path=path, width=image.width(), height=image.height(), bpp=image.depth())

			LOGGER.debug("> Initializing graphics item.")
			self.__displayGraphicsItem = Image_QGraphicsItem(image)
			self.__graphicsScene.addItem(self.__displayGraphicsItem)

			self.__ui.Images_Informations_label.setText("{0} - {1} x {2} - {3} bpp".format(os.path.basename(image._datas.path), image._datas.width, image._datas.height, image._datas.bpp))

	@core.executionTrace
	def fitImage(self):
		"""
		This method fits the display image.
		"""

		if self.__displayGraphicsItem:
			self.__graphicsView.fitInView(QRectF(-(self.__displayGraphicsItem.width / 2) - (self.__displayGraphicsItemMargin / 2), -(self.__displayGraphicsItem.height / 2) - (self.__displayGraphicsItemMargin / 2), self.__displayGraphicsItem.width + self.__displayGraphicsItemMargin, self.__displayGraphicsItem.height + self.__displayGraphicsItemMargin), Qt.KeepAspectRatio)

	@core.executionTrace
	def loopThroughImages(self, backward=False):
		"""
		This method loops through Images Previewer images.

		:param backward: Looping backward. ( Boolean )
		"""

		index = self.__paths.index(self.__displayGraphicsItem.image._datas.path)
		index += not backward and 1 or - 1
		if index < 0:
			index = len(self.__paths) - 1
		elif index > len(self.__paths) - 1:
			index = 0
		self.setImage(index)
		self.fitImage()

class Preview(UiComponent):
	"""
	This class is the **Preview** class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		:param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__uiPath = "ui/Preview.ui"
		self.__uiResources = "resources"

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None

		self.__imagesPreviewers = None
		self.__maximumImagesPreviewersInstances = 5

		self.__viewIblSetsLightingImagesAction = None
		self.__viewIblSetsReflectionImagesAction = None
		self.__viewIblSetsBackgroundImagesAction = None
		self.__viewIblSetsPlatesAction = None

		self.__inspectorButtons = {"Background" : {"object" : None, "text": "View Background Image", "row" : 1, "column" : 3},
									"Lighting" : {"object" : None, "text": "View Lighting Image", "row" : 1, "column" : 4},
									"Reflection" : {"object" : None, "text": "View Reflection Image", "row" : 1, "column" : 5},
									"Plates" : {"object" : None, "text": "View Plate(s)", "row" : 1, "column" : 6}}

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for **self.__uiPath** attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for **self.__uiPath** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for **self.__uiPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This method is the property for **self.__uiResources** attribute.

		:return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for **self.__uiResources** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for **self.__uiResources** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))

	@property
	def settingsSection(self):
		"""
		This method is the property for **self.__settingsSection** attribute.

		:return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for **self.__settingsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settingsSection"))

	@property
	def corePreferencesManager(self):
		"""
		This method is the property for **self.__corePreferencesManager** attribute.

		:return: self.__corePreferencesManager. ( Object )
		"""

		return self.__corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self, value):
		"""
		This method is the setter method for **self.__corePreferencesManager** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("corePreferencesManager"))

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self):
		"""
		This method is the deleter method for **self.__corePreferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("corePreferencesManager"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def coreInspector(self):
		"""
		This method is the property for **self.__coreInspector** attribute.

		:return: self.__coreInspector. ( Object )
		"""

		return self.__coreInspector

	@coreInspector.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self, value):
		"""
		This method is the setter method for **self.__coreInspector** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreInspector"))

	@coreInspector.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self):
		"""
		This method is the deleter method for **self.__coreInspector** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreInspector"))

	@property
	def imagesPreviewers(self):
		"""
		This method is the property for **self.__imagesPreviewers** attribute.

		:return: self.__imagesPreviewers. ( List )
		"""

		return self.__imagesPreviewers

	@imagesPreviewers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagesPreviewers(self, value):
		"""
		This method is the setter method for **self.__imagesPreviewers** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("imagesPreviewers"))

	@imagesPreviewers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagesPreviewers(self):
		"""
		This method is the deleter method for **self.__imagesPreviewers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("imagesPreviewers"))

	@property
	def maximumImagesPreviewersInstances(self):
		"""
		This method is the property for **self.__maximumImagesPreviewersInstances** attribute.

		:return: self.__maximumImagesPreviewersInstances. ( Integer )
		"""

		return self.__maximumImagesPreviewersInstances

	@maximumImagesPreviewersInstances.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumImagesPreviewersInstances(self, value):
		"""
		This method is the setter method for **self.__maximumImagesPreviewersInstances** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("maximumImagesPreviewersInstances"))

	@maximumImagesPreviewersInstances.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumImagesPreviewersInstances(self):
		"""
		This method is the deleter method for **self.__maximumImagesPreviewersInstances** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("maximumImagesPreviewersInstances"))

	@property
	def viewIblSetsBackgroundImagesAction(self):
		"""
		This method is the property for **self.__viewIblSetsBackgroundImagesAction** attribute.

		:return: self.__viewIblSetsBackgroundImagesAction. ( QAction )
		"""

		return self.__viewIblSetsBackgroundImagesAction

	@viewIblSetsBackgroundImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsBackgroundImagesAction(self, value):
		"""
		This method is the setter method for **self.__viewIblSetsBackgroundImagesAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("viewIblSetsBackgroundImagesAction"))

	@viewIblSetsBackgroundImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsBackgroundImagesAction(self):
		"""
		This method is the deleter method for **self.__viewIblSetsBackgroundImagesAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("viewIblSetsBackgroundImagesAction"))

	@property
	def viewIblSetsLightingImagesAction(self):
		"""
		This method is the property for **self.__viewIblSetsLightingImagesAction** attribute.

		:return: self.__viewIblSetsLightingImagesAction. ( QAction )
		"""

		return self.__viewIblSetsLightingImagesAction

	@viewIblSetsLightingImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsLightingImagesAction(self, value):
		"""
		This method is the setter method for **self.__viewIblSetsLightingImagesAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("viewIblSetsLightingImagesAction"))

	@viewIblSetsLightingImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsLightingImagesAction(self):
		"""
		This method is the deleter method for **self.__viewIblSetsLightingImagesAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("viewIblSetsLightingImagesAction"))

	@property
	def viewIblSetsReflectionImagesAction(self):
		"""
		This method is the property for **self.__viewIblSetsReflectionImagesAction** attribute.

		:return: self.__viewIblSetsReflectionImagesAction. ( QAction )
		"""

		return self.__viewIblSetsReflectionImagesAction

	@viewIblSetsReflectionImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsReflectionImagesAction(self, value):
		"""
		This method is the setter method for **self.__viewIblSetsReflectionImagesAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("viewIblSetsReflectionImagesAction"))

	@viewIblSetsReflectionImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsReflectionImagesAction(self):
		"""
		This method is the deleter method for **self.__viewIblSetsReflectionImagesAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("viewIblSetsReflectionImagesAction"))

	@property
	def viewIblSetsPlatesAction(self):
		"""
		This method is the property for **self.__viewIblSetsPlatesAction** attribute.

		:return: self.__viewIblSetsPlatesAction. ( QAction )
		"""

		return self.__viewIblSetsPlatesAction

	@viewIblSetsPlatesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsPlatesAction(self, value):
		"""
		This method is the setter method for **self.__viewIblSetsPlatesAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("viewIblSetsPlatesAction"))

	@viewIblSetsPlatesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsPlatesAction(self):
		"""
		This method is the deleter method for **self.__viewIblSetsPlatesAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("viewIblSetsPlatesAction"))
	@property
	def viewInspectorIblSetBackgroundImagesAction(self):
		"""
		This method is the property for **self.__viewInspectorIblSetBackgroundImagesAction** attribute.

		:return: self.__viewInspectorIblSetBackgroundImagesAction. ( QAction )
		"""

		return self.__viewInspectorIblSetBackgroundImagesAction

	@viewInspectorIblSetBackgroundImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetBackgroundImagesAction(self, value):
		"""
		This method is the setter method for **self.__viewInspectorIblSetBackgroundImagesAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("viewInspectorIblSetBackgroundImagesAction"))

	@viewInspectorIblSetBackgroundImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetBackgroundImagesAction(self):
		"""
		This method is the deleter method for **self.__viewInspectorIblSetBackgroundImagesAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("viewInspectorIblSetBackgroundImagesAction"))

	@property
	def viewInspectorIblSetLightingImagesAction(self):
		"""
		This method is the property for **self.__viewInspectorIblSetLightingImagesAction** attribute.

		:return: self.__viewInspectorIblSetLightingImagesAction. ( QAction )
		"""

		return self.__viewInspectorIblSetLightingImagesAction

	@viewInspectorIblSetLightingImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetLightingImagesAction(self, value):
		"""
		This method is the setter method for **self.__viewInspectorIblSetLightingImagesAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("viewInspectorIblSetLightingImagesAction"))

	@viewInspectorIblSetLightingImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetLightingImagesAction(self):
		"""
		This method is the deleter method for **self.__viewInspectorIblSetLightingImagesAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("viewInspectorIblSetLightingImagesAction"))

	@property
	def viewInspectorIblSetReflectionImageAction(self):
		"""
		This method is the property for **self.__viewInspectorIblSetReflectionImageAction** attribute.

		:return: self.__viewInspectorIblSetReflectionImageAction. ( QAction )
		"""

		return self.__viewInspectorIblSetReflectionImageAction

	@viewInspectorIblSetReflectionImageAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetReflectionImageAction(self, value):
		"""
		This method is the setter method for **self.__viewInspectorIblSetReflectionImageAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("viewInspectorIblSetReflectionImageAction"))

	@viewInspectorIblSetReflectionImageAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetReflectionImageAction(self):
		"""
		This method is the deleter method for **self.__viewInspectorIblSetReflectionImageAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("viewInspectorIblSetReflectionImageAction"))

	@property
	def viewInspectorIblSetPlatesAction(self):
		"""
		This method is the property for **self.__viewInspectorIblSetPlatesAction** attribute.

		:return: self.__viewInspectorIblSetPlatesAction. ( QAction )
		"""

		return self.__viewInspectorIblSetPlatesAction

	@viewInspectorIblSetPlatesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetPlatesAction(self, value):
		"""
		This method is the setter method for **self.__viewInspectorIblSetPlatesAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("viewInspectorIblSetPlatesAction"))

	@viewInspectorIblSetPlatesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetPlatesAction(self):
		"""
		This method is the deleter method for **self.__viewInspectorIblSetPlatesAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("viewInspectorIblSetPlatesAction"))

	@property
	def inspectorButtons(self):
		"""
		This method is the property for **self.__inspectorButtons** attribute.

		:return: self.__inspectorButtons. ( Dictionary )
		"""

		return self.__inspectorButtons

	@inspectorButtons.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorButtons(self, value):
		"""
		This method is the setter method for **self.__inspectorButtons** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("inspectorButtons"))

	@inspectorButtons.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorButtons(self):
		"""
		This method is the deleter method for **self.__inspectorButtons** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("inspectorButtons"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__corePreferencesManager = self.__container.componentsManager.components["core.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreInspector = self.__container.componentsManager.components["core.inspector"].interface

		self.__imagesPreviewers = []

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__uiResources = os.path.basename(self.__uiResources)
		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None

		for imagesPreviewer in self.__imagesPreviewers[:]:
			imagesPreviewer.ui.close()

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__Custom_Previewer_Path_lineEdit_setUi()

		self.__addActions()
		self.__addInspectorButtons()

		# Signals / Slots.
		self.ui.Custom_Previewer_Path_toolButton.clicked.connect(self.__Custom_Previewer_Path_toolButton__clicked)
		self.ui.Custom_Previewer_Path_lineEdit.editingFinished.connect(self.__Custom_Previewer_Path_lineEdit__editFinished)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__removeActions()
		self.__removeInspectorButtons()

		# Signals / Slots.
		self.ui.Custom_Previewer_Path_toolButton.clicked.disconnect(self.__Custom_Previewer_Path_toolButton__clicked)
		self.ui.Custom_Previewer_Path_lineEdit.editingFinished.disconnect(self.__Custom_Previewer_Path_lineEdit__editFinished)

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Custom_Previewer_Path_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self.ui)
		self.ui.Custom_Previewer_Path_groupBox.setParent(None)

	@core.executionTrace
	def __addActions(self):
		"""
		This method adds actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		separatorAction = QAction(self.__coreDatabaseBrowser.ui.Database_Browser_listView)
		separatorAction.setSeparator(True)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(separatorAction)

		self.__viewIblSetsBackgroundImagesAction = QAction("View Background Image ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
		self.__viewIblSetsBackgroundImagesAction.triggered.connect(self.__Database_Browser_listView_viewIblSetsBackgroundImagesAction__triggered)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__viewIblSetsBackgroundImagesAction)

		self.__viewIblSetsLightingImagesAction = QAction("View Lighting Image ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
		self.__viewIblSetsLightingImagesAction.triggered.connect(self.__Database_Browser_listView_viewIblSetsLightingImagesAction__triggered)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__viewIblSetsLightingImagesAction)

		self.__viewIblSetsReflectionImagesAction = QAction("View Reflection Image ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
		self.__viewIblSetsReflectionImagesAction.triggered.connect(self.__Database_Browser_listView_viewIblSetsReflectionImagesAction__triggered)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__viewIblSetsReflectionImagesAction)

		self.__viewIblSetsPlatesAction = QAction("View Plate(s) ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
		self.__viewIblSetsPlatesAction.triggered.connect(self.__Database_Browser_listView_viewIblSetsPlatesAction__triggered)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__viewIblSetsPlatesAction)

		separatorAction = QAction(self.__coreInspector.ui.Inspector_Overall_frame)
		separatorAction.setSeparator(True)
		self.__coreInspector.ui.Inspector_Overall_frame.addAction(separatorAction)

		self.__viewInspectorIblSetBackgroundImageAction = QAction("View Background Image ...", self.__coreInspector.ui.Inspector_Overall_frame)
		self.__viewInspectorIblSetBackgroundImageAction.triggered.connect(self.__Inspector_Overall_frame_viewInspectorIblSetBackgroundImageAction__triggered)
		self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__viewInspectorIblSetBackgroundImageAction)

		self.__viewInspectorIblSetLightingImageAction = QAction("View Lighting Image ...", self.__coreInspector.ui.Inspector_Overall_frame)
		self.__viewInspectorIblSetLightingImageAction.triggered.connect(self.__Inspector_Overall_frame_viewInspectorIblSetLightingImageAction__triggered)
		self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__viewInspectorIblSetLightingImageAction)

		self.__viewInspectorIblSetReflectionImageAction = QAction("View Reflection Image ...", self.__coreInspector.ui.Inspector_Overall_frame)
		self.__viewInspectorIblSetReflectionImageAction.triggered.connect(self.__Inspector_Overall_frame_viewInspectorIblSetReflectionImageAction__triggered)
		self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__viewInspectorIblSetReflectionImageAction)

		self.__viewInspectorIblSetPlatesAction = QAction("View Plate(s) ...", self.__coreInspector.ui.Inspector_Overall_frame)
		self.__viewInspectorIblSetPlatesAction.triggered.connect(self.__Inspector_Overall_frame_viewInspectorIblSetPlatesAction__triggered)
		self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__viewInspectorIblSetPlatesAction)

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		self.__coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self.__viewIblSetsBackgroundImagesAction)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self.__viewIblSetsLightingImagesAction)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self.__viewIblSetsReflectionImagesAction)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self.__viewIblSetsPlatesAction)

		self.__viewIblSetsBackgroundImagesAction = None
		self.__viewIblSetsLightingImagesAction = None
		self.__viewIblSetsReflectionImagesAction = None
		self.__viewIblSetsPlatesAction = None

		self.__coreInspector.ui.Inspector_Overall_frame.removeAction(self.__viewInspectorIblSetBackgroundImageAction)
		self.__coreInspector.ui.Inspector_Overall_frame.removeAction(self.__viewInspectorIblSetLightingImageAction)
		self.__coreInspector.ui.Inspector_Overall_frame.removeAction(self.__viewInspectorIblSetReflectionImageAction)
		self.__coreInspector.ui.Inspector_Overall_frame.removeAction(self.__viewInspectorIblSetPlatesAction)

		self.__viewInspectorIblSetBackgroundImageAction = None
		self.__viewInspectorIblSetLightingImageAction = None
		self.__viewInspectorIblSetReflectionImageAction = None
		self.__viewInspectorIblSetPlatesAction = None

	@core.executionTrace
	def __addInspectorButtons(self):
		"""
		This method adds buttons to the **coreInspector** Component.
		"""

		self.__coreInspector.ui.Inspector_Options_groupBox.show()
		for key, value in self.__inspectorButtons.items():
			value["object"] = QPushButton(value["text"])
			self.__coreInspector.ui.Inspector_Options_groupBox_gridLayout.addWidget(value["object"], value["row"], value["column"])
			value["object"].clicked.connect(functools.partial(self.viewIblSetsImages__, key))

	def __removeInspectorButtons(self):
		"""
		This method removes buttons from the **coreInspector** Component.
		"""

		for value in self.__inspectorButtons.values():
			value["object"].setParent(None)

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsBackgroundImagesAction__triggered(self, checked):
		"""
		This method is triggered by **viewIblSetsBackgroundImagesAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.viewIblSetsImages__("Background")

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsLightingImagesAction__triggered(self, checked):
		"""
		This method is triggered by **viewIblSetsLightingImagesAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.viewIblSetsImages__("Lighting")

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsReflectionImagesAction__triggered(self, checked):
		"""
		This method is triggered by **viewIblSetsReflectionImagesAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.viewIblSetsImages__("Reflection")

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsPlatesAction__triggered(self, checked):
		"""
		This method is triggered by **viewPlatesAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.viewIblSetsImages__("Plates")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetBackgroundImageAction__triggered(self, checked):
		"""
		This method is triggered by **viewInspectorIblSetBackgroundImageAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.viewIblSetsImages__("Background")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetLightingImageAction__triggered(self, checked):
		"""
		This method is triggered by **viewInspectorIblSetLightingImageAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.viewIblSetsImages__("Lighting")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetReflectionImageAction__triggered(self, checked):
		"""
		This method is triggered by **viewInspectorIblSetReflectionImageAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.viewIblSetsImages__("Reflection")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetPlatesAction__triggered(self, checked):
		"""
		This method is triggered by **viewInspectorIblSetPlatesAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.viewIblSetsImages__("Plates")

	@core.executionTrace
	def __Custom_Previewer_Path_lineEdit_setUi(self):
		"""
		This method fills **Custom_Previewer_Path_lineEdit** Widget.
		"""

		customPreviewer = self.__settings.getKey(self.__settingsSection, "customPreviewer")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Custom_Previewer_Path_lineEdit", customPreviewer.toString()))
		self.ui.Custom_Previewer_Path_lineEdit.setText(customPreviewer.toString())

	@core.executionTrace
	def __Custom_Previewer_Path_toolButton__clicked(self, checked):
		"""
		This method is called when **Custom_Previewer_Path_toolButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		customPreviewerExecutable = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom previewer executable:", self.__container.lastBrowsedPath))
		if customPreviewerExecutable != "":
			LOGGER.debug("> Chosen custom Images Previewer executable: '{0}'.".format(customPreviewerExecutable))
			self.ui.Custom_Previewer_Path_lineEdit.setText(QString(customPreviewerExecutable))
			self.__settings.setKey(self.__settingsSection, "customPreviewer", self.ui.Custom_Previewer_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __Custom_Previewer_Path_lineEdit__editFinished(self):
		"""
		This method is called when **Custom_Previewer_Path_lineEdit** Widget is edited and check that entered path is valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.Custom_Previewer_Path_lineEdit.text()))) and str(self.ui.Custom_Previewer_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring preferences!")
			self.__Custom_Previewer_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid custom Images Previewer executable file!".format(self.__class__.__name__)
		else:
			self.__settings.setKey(self.__settingsSection, "customPreviewer", self.ui.Custom_Previewer_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def viewIblSetsImages__(self, imageType, *args):
		"""
		This method launches selected Ibl Sets Images Previewer.

		:param imageType: Image type. ( String )
		:param *args: Arguments. ( * )
		"""

		success = True
		for iblSet in self.__coreDatabaseBrowser.getSelectedIblSets():
			if len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				messageBox.messageBox("Warning", "Warning", "{0} | You can only launch '{1}' images Previewer instances at same time!".format(self.__class__.__name__, self.__maximumImagesPreviewersInstances))
				break
			paths = self.getIblSetImagesPaths(iblSet, imageType)
			if paths:
				success *= self.viewImages(paths, str(self.ui.Custom_Previewer_Path_lineEdit.text())) or False
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Ibl Set has no '{2}' image type and will be skipped!".format(self.__class__.__name__, iblSet.title, imageType))
		if success:
			return True
		else:
			raise Exception, "{0} | Exception raised while displaying '{1}' Ibl Set image(s)!".format(self.__class__.__name__, iblSet.title)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, OSError, Exception)
	def viewInspectorIblSetImages__(self, imageType, *args):
		"""
		This method launches **coreInspector** Ibl Set Images Previewer.

		:param imageType: Image type. ( String )
		:param *args: Arguments. ( * )
		"""

		inspectorIblSet = self.__coreInspector.inspectorIblSet
		inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
		if inspectorIblSet:
			if len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				messageBox.messageBox("Warning", "Warning", "{0} | You can only launch '{1}' images Previewer instances at same time!".format(self.__class__.__name__, self.__maximumImagesPreviewersInstances))
			paths = self.getIblSetImagesPaths(inspectorIblSet, imageType)
			if paths:
				if self.viewImages(paths, str(self.ui.Custom_Previewer_Path_lineEdit.text())):
					return True
				else:
					raise Exception, "{0} | Exception raised while displaying '{1}' inspector Ibl Set image(s)!".format(self.__class__.__name__, inspectorIblSet.title)
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' inspector Ibl Set has no '{2}' image type!".format(self.__class__.__name__, inspectorIblSet.title, imageType))
		else:
			raise OSError, "{0} | Exception raised while opening Inspector Ibl Set directory: '{1}' Ibl Set file doesn't exists!".format(self.__class__.__name__, inspectorIblSet.title)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def viewImages(self, paths, customPreviewer=None):
		"""
		This method launches an Ibl Set Images Previewer.

		:param paths: Image paths. ( List )
		:param customPreviewer: Custom previewer. ( String )
		"""

		if customPreviewer:
			previewCommand = self.getProcessCommand(paths, customPreviewer)
			if previewCommand:
				LOGGER.debug("> Current image preview command: '{0}'.".format(previewCommand))
				LOGGER.info("{0} | Launching Previewer with '{1}' images paths.".format(self.__class__.__name__, ", ".join(paths)))
				editProcess = QProcess()
				editProcess.startDetached(previewCommand)
				return True
			else:
				raise Exception, "{0} | Exception raised: No suitable process command provided!".format(self.__class__.__name__)
		else:
			if not len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				return self.getImagesPreviewer(paths)
			else:
				LOGGER.warning("!> {0} | You can only launch '{1}' images Previewer instances at same time!".format(self.__class__.__name__, self.__maximumImagesPreviewersInstances))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addImagesPreviewer(self, imagesPreviewer):
		"""
		This method adds an Images Previewer.

		:param imagesPreviewer: Images Previewer. ( ImagesPreviewer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' Images Previewer.".format(imagesPreviewer))

		self.__imagesPreviewers.append(imagesPreviewer)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeImagesPreviewer(self, imagesPreviewer):
		"""
		This method removes an Images Previewer.

		:param imagesPreviewer: Images Previewer. ( ImagesPreviewer )
		"""

		LOGGER.debug("> Removing '{0}' Images Previewer.".format(imagesPreviewer))

		self.__imagesPreviewers.remove(imagesPreviewer)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getImagesPreviewer(self, paths):
		"""
		This method launches an Images Previewer.

		:param paths: Images paths. ( List )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Launching Images Previewer for '{0}' image.".format(paths))

		self.addImagesPreviewer(ImagesPreviewer(self, paths))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProcessCommand(self, paths, customPreviewer):
		"""
		This method gets process command.

		:param paths: Paths to preview. ( String )
		:param customPreviewer: Custom browser. ( String )
		:return: Process command. ( String )
		"""

		processCommand = None
		imagesPaths = [os.path.normpath(path) for path in paths]
		if platform.system() == "Windows" or platform.system() == "Microsoft":
				processCommand = "\"{0}\" \"{1}\"".format(customPreviewer, " ".join(imagesPaths))
		elif platform.system() == "Darwin":
				processCommand = "open -a \"{0}\" \"{1}\"".format(customPreviewer, " ".join(imagesPaths))
		elif platform.system() == "Linux":
				processCommand = "\"{0}\" \"{1}\"".format(customPreviewer, " ".join(imagesPaths))
		return processCommand

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getIblSetImagesPaths(self, iblSet, imageType):
		"""
		This method gets Ibl Set images paths.

		:param iblSet: Ibl Set. ( DbIblSet )
		:param imageType: Image type. ( String )
		:return: Images paths. ( List )
		"""

		imagePaths = []
		if imageType == "Background":
			path = iblSet.backgroundImage
			path and imagePaths.append(path)
		elif imageType == "Lighting":
			path = iblSet.lightingImage
			path and imagePaths.append(path)
		elif imageType == "Reflection":
			path = iblSet.reflectionImage
			path and imagePaths.append(path)
		elif imageType == "Plates":
			if os.path.exists(iblSet.path):
				LOGGER.debug("> Parsing Inspector Ibl Set file: '{0}'.".format(iblSet))
				parser = Parser(iblSet.path)
				parser.read() and parser.parse()
				for section in parser.sections:
					if re.search("Plate[0-9]+", section):
						imagePaths.append(os.path.normpath(os.path.join(os.path.dirname(iblSet.path), parser.getValue("PLATEfile", section))))

		for path in imagePaths[:]:
			if not os.path.exists(path):
				imagePaths.remove(path) and LOGGER.warning("!> {0} | '{1}' image file doesn't exists and will be skipped!".format(self.__class__.__name__, path))
		return imagePaths

