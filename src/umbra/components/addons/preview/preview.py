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
# If You Are A HDRI Resources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**preview.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Preview Component Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
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
#***	Internal Imports
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
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Image_QGraphicsItem(QGraphicsItem):
	"""
	This Class Is The Image_QGraphicsItem Class.
	"""

	@core.executionTrace
	def __init__(self, image):
		"""
		This Method Initializes The Class.
		
		@param image: Image. ( QImage )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QGraphicsItem.__init__(self)

		# --- Setting Class Attributes. ---
		self.__image = image
		self.__width = image.width()
		self.__height = image.height()

	#***********************************************************************************************
	#***	Attributes Properties
	#***********************************************************************************************
	@property
	def image(self):
		"""
		This Method Is The Property For The _image Attribute.

		@return: self.__image. ( QImage )
		"""

		return self.__image

	@image.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def image(self, value):
		"""
		This Method Is The Setter Method For The _image Attribute.
		
		@param value: Attribute Value. ( QImage )
		"""

		if value:
			assert type(value) is QImage, "'{0}' Attribute: '{1}' Type Is Not 'QImage'!".format("image", value)
		self.__image = value

	@image.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def image(self):
		"""
		This Method Is The Deleter Method For The _image Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("image"))

	@property
	def width(self):
		"""
		This Method Is The Property For The _width Attribute.

		@return: self.__width. ( Integer )
		"""

		return self.__width

	@width.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def width(self, value):
		"""
		This Method Is The Setter Method For The _width Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' Attribute: '{1}' Type Is Not 'int'!".format("width", value)
		self.__width = value

	@width.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def width(self):
		"""
		This Method Is The Deleter Method For The _width Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("width"))

	@property
	def height(self):
		"""
		This Method Is The Property For The _height Attribute.

		@return: self.__height. ( Integer )
		"""

		return self.__height

	@height.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def height(self, value):
		"""
		This Method Is The Setter Method For The _height Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' Attribute: '{1}' Type Is Not 'int'!".format("height", value)
		self.__height = value

	@height.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def height(self):
		"""
		This Method Is The Deleter Method For The _height Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("height"))

	#***********************************************************************************************
	#***	Class Methods
	#***********************************************************************************************
	@core.executionTrace
	def boundingRect(self):
		"""
		This Method Sets The Bounding Rectangle.
		"""

		return QRectF(-(self.__image.width()) / 2, -(self.__image.height()) / 2, self.__image.width(), self.__image.height())

	@core.executionTrace
	def paint(self, painter, options, widget):
		"""
		This Method Paints The Image.

		@param painter: QPainter ( QPainter )
		@param options: QStyleOptionGraphicsItem  ( QStyleOptionGraphicsItem  )
		@param widget: QWidget ( QWidget )
		"""

		painter.drawImage(-(self.__image.width() / 2), -(self.__image.height() / 2), self.__image)

class ImagesPreviewer(object):
	"""
	This Is The ImagesPreviewer Class.
	"""

	@core.executionTrace
	def __init__(self, container, paths=None):
		"""
		This Method Initializes The Class.
		
		@param container: Container. ( Object )
		@param paths: Images Paths. ( List )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
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
		# Ensure The Ui Object Is Destroyed On Close To Avoid Memory Leaks.
		self.__ui.setAttribute(Qt.WA_DeleteOnClose)
		# Reimplementing Widget Close Event Method.
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
	#***	Attributes Properties
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def paths(self):
		"""
		This Method Is The Property For The _paths Attribute.

		@return: self.__paths. ( List )
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def paths(self, value):
		"""
		This Method Is The Setter Method For The _paths Attribute.

		@param value: Attribute Value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' Attribute: '{1}' Type Is Not 'list'!".format("paths", value)
		self.__paths = value

	@paths.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		This Method Is The Deleter Method For The _paths Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("paths"))

	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This Method Is The Property For The _uiResources Attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This Method Is The Deleter Method For The _uiResources Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def uiPreviousImage(self):
		"""
		This Method Is The Property For The _uiPreviousImage Attribute.

		@return: self.__uiPreviousImage. ( String )
		"""

		return self.__uiPreviousImage

	@uiPreviousImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self, value):
		"""
		This Method Is The Setter Method For The _uiPreviousImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self):
		"""
		This Method Is The Deleter Method For The _uiPreviousImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPreviousImage"))

	@property
	def uiNextImage(self):
		"""
		This Method Is The Property For The _uiNextImage Attribute.

		@return: self.__uiNextImage. ( String )
		"""

		return self.__uiNextImage

	@uiNextImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self, value):
		"""
		This Method Is The Setter Method For The _uiNextImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self):
		"""
		This Method Is The Deleter Method For The _uiNextImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiNextImage"))

	@property
	def uiZoomOutImage(self):
		"""
		This Method Is The Property For The _uiZoomOutImage Attribute.

		@return: self.__uiZoomOutImage. ( String )
		"""

		return self.__uiZoomOutImage

	@uiZoomOutImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self, value):
		"""
		This Method Is The Setter Method For The _uiZoomOutImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiZoomOutImage"))

	@uiZoomOutImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self):
		"""
		This Method Is The Deleter Method For The _uiZoomOutImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiZoomOutImage"))

	@property
	def uiZoomInImage(self):
		"""
		This Method Is The Property For The _uiZoomInImage Attribute.

		@return: self.__uiZoomInImage. ( String )
		"""

		return self.__uiZoomInImage

	@uiZoomInImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self, value):
		"""
		This Method Is The Setter Method For The _uiZoomInImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiZoomInImage"))

	@uiZoomInImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self):
		"""
		This Method Is The Deleter Method For The _uiZoomInImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiZoomInImage"))

	@property
	def ui(self):
		"""
		This Method Is The Property For The _ui Attribute.

		@return: self.__ui. ( Object )
		"""

		return self.__ui

	@ui.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self, value):
		"""
		This Method Is The Setter Method For The _ui Attribute.
		
		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("ui"))

	@ui.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self):
		"""
		This Method Is The Deleter Method For The _ui Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("ui"))

	@property
	def graphicsSceneBackgroundColor(self):
		"""
		This Method Is The Property For The _graphicsSceneBackgroundColor Attribute.

		@return: self.__graphicsSceneBackgroundColor. ( QColors )
		"""

		return self.__graphicsSceneBackgroundColor

	@graphicsSceneBackgroundColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self, value):
		"""
		This Method Is The Setter Method For The _graphicsSceneBackgroundColor Attribute.
		
		@param value: Attribute Value. ( QColors )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsSceneBackgroundColor"))

	@graphicsSceneBackgroundColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self):
		"""
		This Method Is The Deleter Method For The _graphicsSceneBackgroundColor Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsSceneBackgroundColor"))

	@property
	def previewerMargin(self):
		"""
		This Method Is The Property For The _previewerMargin Attribute.

		@return: self.__previewerMargin. ( Integer )
		"""

		return self.__previewerMargin

	@previewerMargin.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewerMargin(self, value):
		"""
		This Method Is The Setter Method For The _previewerMargin Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("previewerMargin"))

	@previewerMargin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewerMargin(self):
		"""
		This Method Is The Deleter Method For The _previewerMargin Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("previewerMargin"))

	@property
	def graphicsSceneWidth(self):
		"""
		This Method Is The Property For The _graphicsSceneWidth Attribute.

		@return: self.__graphicsSceneWidth. ( Integer )
		"""

		return self.__graphicsSceneWidth

	@graphicsSceneWidth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self, value):
		"""
		This Method Is The Setter Method For The _graphicsSceneWidth Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsSceneWidth"))

	@graphicsSceneWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self):
		"""
		This Method Is The Deleter Method For The _graphicsSceneWidth Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsSceneWidth"))

	@property
	def graphicsSceneHeight(self):
		"""
		This Method Is The Property For The _graphicsSceneHeight Attribute.

		@return: self.__graphicsSceneHeight. ( Object )
		"""

		return self.__graphicsSceneHeight

	@graphicsSceneHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self, value):
		"""
		This Method Is The Setter Method For The _graphicsSceneHeight Attribute.
		
		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsSceneHeight"))

	@graphicsSceneHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self):
		"""
		This Method Is The Deleter Method For The _graphicsSceneHeight Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsSceneHeight"))

	@property
	def minimumZoomFactor(self):
		"""
		This Method Is The Property For The _minimumZoomFactor Attribute.

		@return: self.__minimumZoomFactor. ( Float )
		"""

		return self.__minimumZoomFactor

	@minimumZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self, value):
		"""
		This Method Is The Setter Method For The _minimumZoomFactor Attribute.
		
		@param value: Attribute Value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("minimumZoomFactor"))

	@minimumZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self):
		"""
		This Method Is The Deleter Method For The _minimumZoomFactor Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("minimumZoomFactor"))

	@property
	def maximumZoomFactor(self):
		"""
		This Method Is The Property For The _maximumZoomFactor Attribute.

		@return: self.__maximumZoomFactor. ( Float )
		"""

		return self.__maximumZoomFactor

	@maximumZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self, value):
		"""
		This Method Is The Setter Method For The _maximumZoomFactor Attribute.
		
		@param value: Attribute Value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("maximumZoomFactor"))

	@maximumZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self):
		"""
		This Method Is The Deleter Method For The _maximumZoomFactor Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("maximumZoomFactor"))

	@property
	def wheelZoomFactor(self):
		"""
		This Method Is The Property For The _wheelZoomFactor Attribute.

		@return: self.__wheelZoomFactor. ( Float )
		"""

		return self.__wheelZoomFactor

	@wheelZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self, value):
		"""
		This Method Is The Setter Method For The _wheelZoomFactor Attribute.
		
		@param value: Attribute Value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("wheelZoomFactor"))

	@wheelZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self):
		"""
		This Method Is The Deleter Method For The _wheelZoomFactor Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("wheelZoomFactor"))

	@property
	def keyZoomFactor(self):
		"""
		This Method Is The Property For The _keyZoomFactor Attribute.

		@return: self.__keyZoomFactor. ( Float )
		"""

		return self.__keyZoomFactor

	@keyZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self, value):
		"""
		This Method Is The Setter Method For The _keyZoomFactor Attribute.
		
		@param value: Attribute Value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("keyZoomFactor"))

	@keyZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self):
		"""
		This Method Is The Deleter Method For The _keyZoomFactor Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("keyZoomFactor"))

	@property
	def graphicsView(self):
		"""
		This Method Is The Property For The _graphicsView Attribute.

		@return: self.__graphicsView. ( QGraphicsView )
		"""

		return self.__graphicsView

	@graphicsView.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsView(self, value):
		"""
		This Method Is The Setter Method For The _graphicsView Attribute.
		
		@param value: Attribute Value. ( QGraphicsView )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsView"))

	@graphicsView.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsView(self):
		"""
		This Method Is The Deleter Method For The _graphicsView Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsView"))

	@property
	def graphicsScene(self):
		"""
		This Method Is The Property For The _graphicsScene Attribute.

		@return: self.__graphicsScene. ( QGraphicsScene )
		"""

		return self.__graphicsScene

	@graphicsScene.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsScene(self, value):
		"""
		This Method Is The Setter Method For The _graphicsScene Attribute.
		
		@param value: Attribute Value. ( QGraphicsScene )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsScene"))

	@graphicsScene.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsScene(self):
		"""
		This Method Is The Deleter Method For The _graphicsScene Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsScene"))

	@property
	def displayGraphicsItem(self):
		"""
		This Method Is The Property For The _displayGraphicsItem Attribute.

		@return: self.__displayGraphicsItem. ( QGraphicsItem )
		"""

		return self.__displayGraphicsItem

	@displayGraphicsItem.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self, value):
		"""
		This Method Is The Setter Method For The _displayGraphicsItem Attribute.
		
		@param value: Attribute Value. ( QGraphicsItem )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("displayGraphicsItem"))

	@displayGraphicsItem.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self):
		"""
		This Method Is The Deleter Method For The _displayGraphicsItem Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("displayGraphicsItem"))

	#***********************************************************************************************
	#***	Class Methods
	#***********************************************************************************************
	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Widget Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Ui.".format(self.__class__.__name__))

		self.ui.Previous_Image_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiPreviousImage)))
		self.ui.Next_Image_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiNextImage)))
		self.__ui.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiZoomInImage)))
		self.__ui.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiZoomOutImage)))
		len(self.__paths) <= 1 and self.ui.Navigation_groupBox.hide()

		LOGGER.debug("> Initializing Graphics View.")
		self.__graphicsView = QGraphicsView()
		self.__graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.__graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.__graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		self.__graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
		# Reimplementing QGraphicsView wheelEvent Method.
		self.__graphicsView.wheelEvent = self.wheelEvent

		LOGGER.debug("> Initializing Graphics Scene.")
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
		This Method Redefines The Ui Close Event.

		@param event: QEvent ( QEvent )
		"""

		event.accept()

		LOGGER.debug("> Removing '{0}' From Image Previewers List.".format(self))
		self.__container.imagesPreviewers.remove(self)

	@core.executionTrace
	def wheelEvent(self, event):
		"""
		This Method Redefines wheelEvent.

		@param event: QEvent ( QEvent )
		"""

		self.scaleView(pow(1.5, event.delta() / self.__wheelZoomFactor))

	@core.executionTrace
	def keyPressEvent(self, event):
		"""
		This Method Redefines keyPressEvent.

		@param event: QEvent ( QEvent )
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
		This Method Is Triggered When Previous_Image_pushButton Is Clicked.

		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughImages(True)

	@core.executionTrace
	def __Next_Image_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Next_Image_pushButton Is Clicked.

		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughImages()

	@core.executionTrace
	def __Zoom_In_pushButton_clicked(self, checked):
		"""
		This Method Is Triggered When Zoom_In_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.scaleView(self.__keyZoomFactor)

	@core.executionTrace
	def __Zoom_Out_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Zoom_Out_pushButton Is Clicked.

		@param checked: Checked State. ( Boolean )
		"""

		self.scaleView(1 / self.__keyZoomFactor)

	@core.executionTrace
	def __Zoom_Fit_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Zoom_Fit_pushButton Is Clicked.

		@param checked: Checked State. ( Boolean )
		"""

		self.fitImage()

	@core.executionTrace
	def scaleView(self, scaleFactor):
		"""
		This Method Scales The QGraphicsView.

		@param scaleFactor: Float ( Float )
		"""

		graphicsView = self.__ui.findChild(QGraphicsView)
		factor = graphicsView.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
		if factor < self.__minimumZoomFactor or factor > self.__maximumZoomFactor:
			return

		graphicsView.scale(scaleFactor, scaleFactor)

	@core.executionTrace
	def fitPreviewer(self):
		"""
		This Method Fits The Previewer Window.
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
		This Method Sets The Display Image.
		
		@param index: Index To Display. ( Integer )
		"""

		if self.__paths:
			path = self.__paths[index]
			image = umbra.ui.common.getImage(path)
			if not hasattr(image, "_datas"):
				image._datas = freeImage.ImageInformationsHeader(path=path, width=image.width(), height=image.height(), bpp=image.depth())

			LOGGER.debug("> Initializing Graphics Item.")
			self.__displayGraphicsItem = Image_QGraphicsItem(image)
			self.__graphicsScene.addItem(self.__displayGraphicsItem)

			self.__ui.Images_Informations_label.setText("{0} - {1} x {2} - {3} BPP".format(os.path.basename(image._datas.path), image._datas.width, image._datas.height, image._datas.bpp))

	@core.executionTrace
	def fitImage(self):
		"""
		This Method Fits The Display Image.
		"""

		if self.__displayGraphicsItem:
			self.__graphicsView.fitInView(QRectF(-(self.__displayGraphicsItem.width / 2) - (self.__displayGraphicsItemMargin / 2), -(self.__displayGraphicsItem.height / 2) - (self.__displayGraphicsItemMargin / 2), self.__displayGraphicsItem.width + self.__displayGraphicsItemMargin, self.__displayGraphicsItem.height + self.__displayGraphicsItemMargin), Qt.KeepAspectRatio)

	@core.executionTrace
	def loopThroughImages(self, backward=False):
		"""
		This Method Loops Through Previewer Images.
		
		@param backward: Looping Backward. ( Boolean )
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
	This Class Is The Preview Class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
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
									"Plates" : {"object" : None, "text": "View Plates", "row" : 1, "column" : 6}}

	#***********************************************************************************************
	#***	Attributes Properties
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This Method Is The Property For The _uiResources Attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This Method Is The Deleter Method For The _uiResources Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def settings(self):
		"""
		This Method Is The Property For The _settings Attribute.

		@return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This Method Is The Deleter Method For The _settings Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settings"))

	@property
	def settingsSection(self):
		"""
		This Method Is The Property For The _settingsSection Attribute.

		@return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This Method Is The Setter Method For The _settingsSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This Method Is The Deleter Method For The _settingsSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settingsSection"))

	@property
	def corePreferencesManager(self):
		"""
		This Method Is The Property For The _corePreferencesManager Attribute.

		@return: self.__corePreferencesManager. ( Object )
		"""

		return self.__corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self, value):
		"""
		This Method Is The Setter Method For The _corePreferencesManager Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("corePreferencesManager"))

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self):
		"""
		This Method Is The Deleter Method For The _corePreferencesManager Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("corePreferencesManager"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDatabaseBrowser"))

	@property
	def coreInspector(self):
		"""
		This Method Is The Property For The _coreInspector Attribute.

		@return: self.__coreInspector. ( Object )
		"""

		return self.__coreInspector

	@coreInspector.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self, value):
		"""
		This Method Is The Setter Method For The _coreInspector Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreInspector"))

	@coreInspector.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self):
		"""
		This Method Is The Deleter Method For The _coreInspector Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreInspector"))

	@property
	def imagesPreviewers(self):
		"""
		This Method Is The Property For The _imagesPreviewers Attribute.

		@return: self.__imagesPreviewers. ( List )
		"""

		return self.__imagesPreviewers

	@imagesPreviewers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagesPreviewers(self, value):
		"""
		This Method Is The Setter Method For The _imagesPreviewers Attribute.

		@param value: Attribute Value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("imagesPreviewers"))

	@imagesPreviewers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagesPreviewers(self):
		"""
		This Method Is The Deleter Method For The _imagesPreviewers Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("imagesPreviewers"))

	@property
	def maximumImagesPreviewersInstances(self):
		"""
		This Method Is The Property For The _maximumImagesPreviewersInstances Attribute.

		@return: self.__maximumImagesPreviewersInstances. ( Integer )
		"""

		return self.__maximumImagesPreviewersInstances

	@maximumImagesPreviewersInstances.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumImagesPreviewersInstances(self, value):
		"""
		This Method Is The Setter Method For The _maximumImagesPreviewersInstances Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("maximumImagesPreviewersInstances"))

	@maximumImagesPreviewersInstances.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumImagesPreviewersInstances(self):
		"""
		This Method Is The Deleter Method For The _maximumImagesPreviewersInstances Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("maximumImagesPreviewersInstances"))

	@property
	def viewIblSetsBackgroundImagesAction(self):
		"""
		This Method Is The Property For The _viewIblSetsBackgroundImagesAction Attribute.

		@return: self.__viewIblSetsBackgroundImagesAction. ( QAction )
		"""

		return self.__viewIblSetsBackgroundImagesAction

	@viewIblSetsBackgroundImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsBackgroundImagesAction(self, value):
		"""
		This Method Is The Setter Method For The _viewIblSetsBackgroundImagesAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("viewIblSetsBackgroundImagesAction"))

	@viewIblSetsBackgroundImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsBackgroundImagesAction(self):
		"""
		This Method Is The Deleter Method For The _viewIblSetsBackgroundImagesAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("viewIblSetsBackgroundImagesAction"))

	@property
	def viewIblSetsLightingImagesAction(self):
		"""
		This Method Is The Property For The _viewIblSetsLightingImagesAction Attribute.

		@return: self.__viewIblSetsLightingImagesAction. ( QAction )
		"""

		return self.__viewIblSetsLightingImagesAction

	@viewIblSetsLightingImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsLightingImagesAction(self, value):
		"""
		This Method Is The Setter Method For The _viewIblSetsLightingImagesAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("viewIblSetsLightingImagesAction"))

	@viewIblSetsLightingImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsLightingImagesAction(self):
		"""
		This Method Is The Deleter Method For The _viewIblSetsLightingImagesAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("viewIblSetsLightingImagesAction"))

	@property
	def viewIblSetsReflectionImagesAction(self):
		"""
		This Method Is The Property For The _viewIblSetsReflectionImagesAction Attribute.

		@return: self.__viewIblSetsReflectionImagesAction. ( QAction )
		"""

		return self.__viewIblSetsReflectionImagesAction

	@viewIblSetsReflectionImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsReflectionImagesAction(self, value):
		"""
		This Method Is The Setter Method For The _viewIblSetsReflectionImagesAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("viewIblSetsReflectionImagesAction"))

	@viewIblSetsReflectionImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsReflectionImagesAction(self):
		"""
		This Method Is The Deleter Method For The _viewIblSetsReflectionImagesAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("viewIblSetsReflectionImagesAction"))

	@property
	def viewIblSetsPlatesAction(self):
		"""
		This Method Is The Property For The _viewIblSetsPlatesAction Attribute.

		@return: self.__viewIblSetsPlatesAction. ( QAction )
		"""

		return self.__viewIblSetsPlatesAction

	@viewIblSetsPlatesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsPlatesAction(self, value):
		"""
		This Method Is The Setter Method For The _viewIblSetsPlatesAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("viewIblSetsPlatesAction"))

	@viewIblSetsPlatesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewIblSetsPlatesAction(self):
		"""
		This Method Is The Deleter Method For The _viewIblSetsPlatesAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("viewIblSetsPlatesAction"))
	@property
	def viewInspectorIblSetBackgroundImagesAction(self):
		"""
		This Method Is The Property For The _viewInspectorIblSetBackgroundImagesAction Attribute.

		@return: self.__viewInspectorIblSetBackgroundImagesAction. ( QAction )
		"""

		return self.__viewInspectorIblSetBackgroundImagesAction

	@viewInspectorIblSetBackgroundImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetBackgroundImagesAction(self, value):
		"""
		This Method Is The Setter Method For The _viewInspectorIblSetBackgroundImagesAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("viewInspectorIblSetBackgroundImagesAction"))

	@viewInspectorIblSetBackgroundImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetBackgroundImagesAction(self):
		"""
		This Method Is The Deleter Method For The _viewInspectorIblSetBackgroundImagesAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("viewInspectorIblSetBackgroundImagesAction"))

	@property
	def viewInspectorIblSetLightingImagesAction(self):
		"""
		This Method Is The Property For The _viewInspectorIblSetLightingImagesAction Attribute.

		@return: self.__viewInspectorIblSetLightingImagesAction. ( QAction )
		"""

		return self.__viewInspectorIblSetLightingImagesAction

	@viewInspectorIblSetLightingImagesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetLightingImagesAction(self, value):
		"""
		This Method Is The Setter Method For The _viewInspectorIblSetLightingImagesAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("viewInspectorIblSetLightingImagesAction"))

	@viewInspectorIblSetLightingImagesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetLightingImagesAction(self):
		"""
		This Method Is The Deleter Method For The _viewInspectorIblSetLightingImagesAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("viewInspectorIblSetLightingImagesAction"))

	@property
	def viewInspectorIblSetReflectionImageAction(self):
		"""
		This Method Is The Property For The _viewInspectorIblSetReflectionImageAction Attribute.

		@return: self.__viewInspectorIblSetReflectionImageAction. ( QAction )
		"""

		return self.__viewInspectorIblSetReflectionImageAction

	@viewInspectorIblSetReflectionImageAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetReflectionImageAction(self, value):
		"""
		This Method Is The Setter Method For The _viewInspectorIblSetReflectionImageAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("viewInspectorIblSetReflectionImageAction"))

	@viewInspectorIblSetReflectionImageAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetReflectionImageAction(self):
		"""
		This Method Is The Deleter Method For The _viewInspectorIblSetReflectionImageAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("viewInspectorIblSetReflectionImageAction"))

	@property
	def viewInspectorIblSetPlatesAction(self):
		"""
		This Method Is The Property For The _viewInspectorIblSetPlatesAction Attribute.

		@return: self.__viewInspectorIblSetPlatesAction. ( QAction )
		"""

		return self.__viewInspectorIblSetPlatesAction

	@viewInspectorIblSetPlatesAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetPlatesAction(self, value):
		"""
		This Method Is The Setter Method For The _viewInspectorIblSetPlatesAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("viewInspectorIblSetPlatesAction"))

	@viewInspectorIblSetPlatesAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewInspectorIblSetPlatesAction(self):
		"""
		This Method Is The Deleter Method For The _viewInspectorIblSetPlatesAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("viewInspectorIblSetPlatesAction"))

	@property
	def inspectorButtons(self):
		"""
		This Method Is The Property For The _inspectorButtons Attribute.

		@return: self.__inspectorButtons. ( Dictionary )
		"""

		return self.__inspectorButtons

	@inspectorButtons.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorButtons(self, value):
		"""
		This Method Is The Setter Method For The _inspectorButtons Attribute.

		@param value: Attribute Value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("inspectorButtons"))

	@inspectorButtons.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorButtons(self):
		"""
		This Method Is The Deleter Method For The _inspectorButtons Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("inspectorButtons"))

	#***********************************************************************************************
	#***	Class Methods
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
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
		This Method Deactivates The Component.
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
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__Custom_Previewer_Path_lineEdit_setUi()

		self.__addActions()
		self.__addInspectorButtons()

		# Signals / Slots.
		self.ui.Custom_Previewer_Path_toolButton.clicked.connect(self.__Custom_Previewer_Path_toolButton__clicked)
		self.ui.Custom_Previewer_Path_lineEdit.editingFinished.connect(self.__Custom_Previewer_Path_lineEdit__editFinished)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__removeActions()
		self.__removeInspectorButtons()

		# Signals / Slots.
		self.ui.Custom_Previewer_Path_toolButton.clicked.disconnect(self.__Custom_Previewer_Path_toolButton__clicked)
		self.ui.Custom_Previewer_Path_lineEdit.editingFinished.disconnect(self.__Custom_Previewer_Path_lineEdit__editFinished)

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Custom_Previewer_Path_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self.ui)
		self.ui.Custom_Previewer_Path_groupBox.setParent(None)

	@core.executionTrace
	def __addActions(self):
		"""
		This Method Adds Actions.
		"""

		LOGGER.debug("> Adding '{0}' Component Actions.".format(self.__class__.__name__))

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

		self.__viewIblSetsPlatesAction = QAction("View Plates ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
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

		self.__viewInspectorIblSetPlatesAction = QAction("View Plates ...", self.__coreInspector.ui.Inspector_Overall_frame)
		self.__viewInspectorIblSetPlatesAction.triggered.connect(self.__Inspector_Overall_frame_viewInspectorIblSetPlatesAction__triggered)
		self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__viewInspectorIblSetPlatesAction)

	@core.executionTrace
	def __removeActions(self):
		"""
		This Method Removes Actions.
		"""

		LOGGER.debug("> Removing '{0}' Component Actions.".format(self.__class__.__name__))

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
		This Method Adds Buttons To The Inspector Component.
		"""

		self.__coreInspector.ui.Inspector_Options_groupBox.show()
		for key, value in self.__inspectorButtons.items():
			value["object"] = QPushButton(value["text"])
			self.__coreInspector.ui.Inspector_Options_groupBox_gridLayout.addWidget(value["object"], value["row"], value["column"])
			value["object"].clicked.connect(functools.partial(self.viewIblSetsImages__, key))

	def __removeInspectorButtons(self):
		"""
		This Method Removes Buttons From The Inspector Component.
		"""

		for value in self.__inspectorButtons.values():
			value["object"].setParent(None)

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsBackgroundImagesAction__triggered(self, checked):
		"""
		This Method Is Triggered By viewIblSetsBackgroundImagesAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.viewIblSetsImages__("Background")

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsLightingImagesAction__triggered(self, checked):
		"""
		This Method Is Triggered By viewIblSetsLightingImagesAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.viewIblSetsImages__("Lighting")

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsReflectionImagesAction__triggered(self, checked):
		"""
		This Method Is Triggered By viewIblSetsReflectionImagesAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.viewIblSetsImages__("Reflection")

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsPlatesAction__triggered(self, checked):
		"""
		This Method Is Triggered By viewPlatesAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.viewIblSetsImages__("Plates")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetBackgroundImageAction__triggered(self, checked):
		"""
		This Method Is Triggered By viewInspectorIblSetBackgroundImageAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.viewIblSetsImages__("Background")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetLightingImageAction__triggered(self, checked):
		"""
		This Method Is Triggered By viewInspectorIblSetLightingImageAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.viewIblSetsImages__("Lighting")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetReflectionImageAction__triggered(self, checked):
		"""
		This Method Is Triggered By viewInspectorIblSetReflectionImageAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.viewIblSetsImages__("Reflection")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetPlatesAction__triggered(self, checked):
		"""
		This Method Is Triggered By viewInspectorIblSetPlatesAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.viewIblSetsImages__("Plates")

	@core.executionTrace
	def __Custom_Previewer_Path_lineEdit_setUi(self):
		"""
		This Method Fills The Custom_Previewer_Path_lineEdit.
		"""

		customPreviewer = self.__settings.getKey(self.__settingsSection, "customPreviewer")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("Custom_Previewer_Path_lineEdit", customPreviewer.toString()))
		self.ui.Custom_Previewer_Path_lineEdit.setText(customPreviewer.toString())

	@core.executionTrace
	def __Custom_Previewer_Path_toolButton__clicked(self, checked):
		"""
		This Method Is Called When Custom_Previewer_Path_toolButton Is Clicked.

		@param checked: Checked State. ( Boolean )
		"""

		customPreviewerExecutable = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom Previewer Executable:", self.__container.lastBrowsedPath))
		if customPreviewerExecutable != "":
			LOGGER.debug("> Chosen Custom Previewer Executable: '{0}'.".format(customPreviewerExecutable))
			self.ui.Custom_Previewer_Path_lineEdit.setText(QString(customPreviewerExecutable))
			self.__settings.setKey(self.__settingsSection, "customPreviewer", self.ui.Custom_Previewer_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __Custom_Previewer_Path_lineEdit__editFinished(self):
		"""
		This Method Is Called When Custom_Previewer_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.Custom_Previewer_Path_lineEdit.text()))) and str(self.ui.Custom_Previewer_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring Preferences!")
			self.__Custom_Previewer_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid Custom Previewer Executable File!".format(self.__class__.__name__)
		else:
			self.__settings.setKey(self.__settingsSection, "customPreviewer", self.ui.Custom_Previewer_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def viewIblSetsImages__(self, imageType, *args):
		"""
		This Method Launches Selected Ibl Sets Images Previewer.
		
		@param imageType: Image Type. ( String )
		@param *args: Arguments. ( * )
		"""

		success = True
		for iblSet in self.__coreDatabaseBrowser.getSelectedIblSets():
			if len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				messageBox.messageBox("Warning", "Warning", "{0} | You Can Only Launch '{1}' Image Previewer Instances At Same Time!".format(self.__class__.__name__, self.__maximumImagesPreviewersInstances))
				break
			paths = self.getIblSetImagesPaths(iblSet, imageType)
			if paths:
				success *= self.viewImages(paths, str(self.ui.Custom_Previewer_Path_lineEdit.text())) or False
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Ibl Set Has No '{2}' Image Type And Will Be Skipped!".format(self.__class__.__name__, iblSet.title, imageType))
		if success:
			return True
		else:
			raise Exception, "{0} | Exception Raised While Displaying '{1}' Ibl Set Image(s)!".format(self.__class__.__name__, iblSet.title)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, OSError, Exception)
	def viewInspectorIblSetImages__(self, imageType, *args):
		"""
		This Method Launches Inspector Ibl Set Images Previewer.
		
		@param imageType: Image Type. ( String )
		@param *args: Arguments. ( * )
		"""

		inspectorIblSet = self.__coreInspector.inspectorIblSet
		inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
		if inspectorIblSet:
			if len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				messageBox.messageBox("Warning", "Warning", "{0} | You Can Only Launch '{1}' Image Previewer Instances At Same Time!".format(self.__class__.__name__, self.__maximumImagesPreviewersInstances))
			paths = self.getIblSetImagesPaths(inspectorIblSet, imageType)
			if paths:
				if self.viewImages(paths, str(self.ui.Custom_Previewer_Path_lineEdit.text())):
					return True
				else:
					raise Exception, "{0} | Exception Raised While Displaying '{1}' Inspector Ibl Set Image(s)!".format(self.__class__.__name__, inspectorIblSet.title)
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Inspector Ibl Set Has No '{2}' Image Type!".format(self.__class__.__name__, inspectorIblSet.title, imageType))
		else:
			raise OSError, "{0} | Exception Raised While Opening Inspector Ibl Set Directory: '{1}' Ibl Set File Doesn't Exists!".format(self.__class__.__name__, inspectorIblSet.title)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def viewImages(self, paths, customPreviewer=None):
		"""
		This Method Launches An Ibl Set Images Previewer.
		
		@param paths: Image Paths. ( List )
		@param customPreviewer: Custom Previewer. ( String )
		"""

		if customPreviewer:
			previewCommand = self.getProcessCommand(paths, customPreviewer)
			if previewCommand:
				LOGGER.debug("> Current Image Preview Command: '{0}'.".format(previewCommand))
				LOGGER.info("{0} | Launching Previewer With '{1}' Images Paths.".format(self.__class__.__name__, ", ".join(paths)))
				editProcess = QProcess()
				editProcess.startDetached(previewCommand)
				return True
			else:
				raise Exception, "{0} | Exception Raised: No Suitable Process Command Provided!".format(self.__class__.__name__)
		else:
			if not len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				return self.getImagesPreviewer(paths)
			else:
				LOGGER.warning("!> {0} | You Can Only Launch '{1}' Image Previewer Instances At Same Time!".format(self.__class__.__name__, self.__maximumImagesPreviewersInstances))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addImagesPreviewer(self, imagesPreviewer):
		"""
		This Method Adds An Images Previewer.
		
		@param imagesPreviewer: Images Previewer. ( ImagesPreviewer )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Images Previewer.".format(imagesPreviewer))

		self.__imagesPreviewers.append(imagesPreviewer)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeImagesPreviewer(self, imagesPreviewer):
		"""
		This Method Removes An Images Previewer.
		
		@param imagesPreviewer: Images Previewer. ( ImagesPreviewer )
		"""

		LOGGER.debug("> Removing '{0}' Images Previewer.".format(imagesPreviewer))

		self.__imagesPreviewers.remove(imagesPreviewer)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getImagesPreviewer(self, paths):
		"""
		This Method Launches An Images Previewer.
		
		@param paths: Images Paths. ( List )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Launching Images Previewer For '{0}' Image.".format(paths))

		self.addImagesPreviewer(ImagesPreviewer(self, paths))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProcessCommand(self, paths, customPreviewer):
		"""
		This Method Gets Process Command.

		@param paths: Paths To Preview. ( String )
		@param customPreviewer: Custom Browser. ( String )
		@return: Process Command. ( String )		
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
		This Method Gets Ibl Set Images Paths.
		
		@param iblSet: Ibl Set. ( DbIblSet )
		@param imageType: Image Type. ( String )
		@return: Images Paths. ( List )		
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
				LOGGER.debug("> Parsing Inspector Ibl Set File: '{0}'.".format(iblSet))
				parser = Parser(iblSet.path)
				parser.read() and parser.parse()
				for section in parser.sections:
					if re.search("Plate[0-9]+", section):
						imagePaths.append(os.path.normpath(os.path.join(os.path.dirname(iblSet.path), parser.getValue("PLATEfile", section))))

		for path in imagePaths[:]:
			if not os.path.exists(path):
				imagePaths.remove(path) and LOGGER.warning("!> {0} | '{1}' Image File Doesn't Exists And Will Be Skipped!".format(self.__class__.__name__, path))
		return imagePaths

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
