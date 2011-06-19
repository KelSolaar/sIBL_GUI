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
***	preview.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Preview Component Module.
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
import ui.common
import ui.widgets.messageBox as messageBox
from globals.constants import Constants
from globals.uiConstants import UiConstants
from libraries.freeImage.freeImage import Image
from manager.uiComponent import UiComponent

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
		self._image = image

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def image(self):
		"""
		This Method Is The Property For The _image Attribute.

		@return: self._image. ( QImage )
		"""

		return self._image

	@image.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def image(self, value):
		"""
		This Method Is The Setter Method For The _image Attribute.
		
		@param value: Attribute Value. ( QImage )
		"""

		if value:
			assert type(value) is QImage, "'{0}' Attribute: '{1}' Type Is Not 'QImage'!".format("image", value)
		self._imagePath = value

	@image.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def image(self):
		"""
		This Method Is The Deleter Method For The _image Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("image"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def boundingRect(self):
		"""
		This Method Sets The Bounding Rectangle.
		"""

		return QRectF(-(self._image.width()) / 2, -(self._image.height()) / 2, self._image.width(), self._image.height())

	@core.executionTrace
	def paint(self, painter, options, widget):
		"""
		This Method Paints The Image.

		@param painter: QPainter ( QPainter )
		@param options: QStyleOptionGraphicsItem  ( QStyleOptionGraphicsItem  )
		@param widget: QWidget ( QWidget )
		"""

		painter.drawImage(-(self._image.width() / 2), -(self._image.height() / 2), self._image)

class ImagePreviewer(object):
	"""
	This Is The ImagePreviewer Class.
	"""

	@core.executionTrace
	def __init__(self, container, imagePath):
		"""
		This Method Initializes The Class.
		
		@param container: Container. ( Object )
		@param imagePath: Image Path. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self._container = container
		self._imagePath = imagePath

		self._uiPath = "ui/Image_Previewer.ui"
		self._uiPath = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiPath)
		self._uiResources = "resources"
		self._uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiResources)
		self._uiZoomInImage = "Zoom_In.png"
		self._uiZoomOutImage = "Zoom_Out.png"

		self._ui = uic.loadUi(self._uiPath)
		if "." in sys.path:
			sys.path.remove(".")
		# Ensure The Ui Object Is Destroyed On Close To Avoid Memory Leaks.
		self._ui.setAttribute(Qt.WA_DeleteOnClose)
		# Reimplementing Widget Close Event Method.
		self._ui.closeEvent = self.closeUi

		self._graphicsSceneBackgroundColors = (("Dark", QColor(32, 32, 32)), ("Average", QColor(128, 128, 128)), ("Bright", QColor(200, 200, 200)))
		self._minimumZoomFactor = 0.125
		self._maximumZoomFactor = 25
		self._graphicsSceneMargin = 128
		self._graphicsSceneWidth = QApplication.desktop().width() * (1 / self._minimumZoomFactor * 1.75)
		self._graphicsSceneHeight = QApplication.desktop().height() * (1 / self._minimumZoomFactor * 1.75)
		self._wheelZoomFactor = 350.0
		self._keyZoomFactor = 1.20

		self.initializeUi()

		self._ui.show()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		"""

		return self._container

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
	def imagePath(self):
		"""
		This Method Is The Property For The _imagePath Attribute.

		@return: self._imagePath. ( String )
		"""

		return self._imagePath

	@imagePath.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def imagePath(self, value):
		"""
		This Method Is The Setter Method For The _imagePath Attribute.

		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode, QString), "'{0}' Attribute: '{1}' Type Is Not 'str', 'unicode' or 'QString'!".format("imagePath", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' Image File Doesn't Exists!".format("imagePath", value)
		self._imagePath = value

	@imagePath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagePath(self):
		"""
		This Method Is The Deleter Method For The _imagePath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("imagePath"))

	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		"""

		return self._uiPath

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

		@return: self._uiResources. ( String )
		"""

		return self._uiResources

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
	def uiZoomInImage(self):
		"""
		This Method Is The Property For The _uiZoomInImage Attribute.

		@return: self._uiZoomInImage. ( String )
		"""

		return self._uiZoomInImage

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
	def uiZoomOutImage(self):
		"""
		This Method Is The Property For The _uiZoomOutImage Attribute.

		@return: self._uiZoomOutImage. ( String )
		"""

		return self._uiZoomOutImage

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
	def ui(self):
		"""
		This Method Is The Property For The _ui Attribute.

		@return: self._ui. ( Object )
		"""

		return self._ui

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
	def graphicsSceneBackgroundColors(self):
		"""
		This Method Is The Property For The _graphicsSceneBackgroundColors Attribute.

		@return: self._graphicsSceneBackgroundColors. ( QColors )
		"""

		return self._graphicsSceneBackgroundColors

	@graphicsSceneBackgroundColors.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColors(self, value):
		"""
		This Method Is The Setter Method For The _graphicsSceneBackgroundColors Attribute.
		
		@param value: Attribute Value. ( QColors )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsSceneBackgroundColors"))

	@graphicsSceneBackgroundColors.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColors(self):
		"""
		This Method Is The Deleter Method For The _graphicsSceneBackgroundColors Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsSceneBackgroundColors"))

	@property
	def graphicsSceneMargin(self):
		"""
		This Method Is The Property For The _graphicsSceneMargin Attribute.

		@return: self._graphicsSceneMargin. ( Integer )
		"""

		return self._graphicsSceneMargin

	@graphicsSceneMargin.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneMargin(self, value):
		"""
		This Method Is The Setter Method For The _graphicsSceneMargin Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsSceneMargin"))

	@graphicsSceneMargin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneMargin(self):
		"""
		This Method Is The Deleter Method For The _graphicsSceneMargin Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsSceneMargin"))

	@property
	def graphicsSceneWidth(self):
		"""
		This Method Is The Property For The _graphicsSceneWidth Attribute.

		@return: self._graphicsSceneWidth. ( Integer )
		"""

		return self._graphicsSceneWidth

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

		@return: self._graphicsSceneHeight. ( Object )
		"""

		return self._graphicsSceneHeight

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

		@return: self._minimumZoomFactor. ( Float )
		"""

		return self._minimumZoomFactor

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

		@return: self._maximumZoomFactor. ( Float )
		"""

		return self._maximumZoomFactor

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

		@return: self._wheelZoomFactor. ( Float )
		"""

		return self._wheelZoomFactor

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

		@return: self._keyZoomFactor. ( Float )
		"""

		return self._keyZoomFactor

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

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Widget Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Ui.".format(self.__class__.__name__))

		self._ui.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiZoomInImage)))
		self._ui.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiZoomOutImage)))

		self._ui.Background_Colors_comboBox.addItems([color[0] for color in self._graphicsSceneBackgroundColors])

		for extension in UiConstants.nativeImageFormats.values():
			if re.search(extension, self._imagePath):
				LOGGER.debug("> Loading Native Format '{0}' Image.".format(self._imagePath))
				image = QImage(self._imagePath)
				bpp = image.depth()
				break
		else:
			for extension in UiConstants.thirdPartyImageFormats.values():
				if re.search(extension, self._imagePath):
					LOGGER.debug("> Loading Third Party Format '{0}' Image.".format(self._imagePath))
					image = Image(str(self._imagePath))
					image = image.convertToQImage()
					bpp = image._datas.bpp
					break

		self._ui.Image_Informations_label.setText("{0} - {1} x {2} - {3} BPP".format(os.path.basename(self._imagePath), image.width(), image.height(), bpp))

		LOGGER.debug("> Initializing Graphics View.")
		graphicsView = QGraphicsView()
		graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
		# Reimplementing QGraphics View wheelEvent Method.
		graphicsView.wheelEvent = self.wheelEvent

		LOGGER.debug("> Initializing Graphics Scene.")
		graphicsScene = QGraphicsScene(graphicsView)
		graphicsScene.setItemIndexMethod(QGraphicsScene.NoIndex)
		graphicsScene.setSceneRect(-(float(self._graphicsSceneWidth)) / 2, -(float(self._graphicsSceneHeight)) / 2, float(self._graphicsSceneWidth), float(self._graphicsSceneHeight))

		graphicsView.setScene(graphicsScene)

		graphicsView.setBackgroundBrush(QBrush(self._graphicsSceneBackgroundColors[0][1]))

		LOGGER.debug("> Initializing Graphics Item.")
		graphicsItem = Image_QGraphicsItem(image)
		graphicsScene.addItem(graphicsItem)

		self._ui.Image_Previewer_frame_gridLayout.addWidget(graphicsView)

		width = image.width() > QApplication.desktop().width() and QApplication.desktop().width() / 1.5 + self._graphicsSceneMargin or image.width() + self._graphicsSceneMargin
		height = image.height() > QApplication.desktop().height() and QApplication.desktop().height() / 1.5 + self._graphicsSceneMargin or image.height() + self._graphicsSceneMargin

		self._ui.resize(width, height)

		# Signals / Slots.
		self.ui.Zoom_In_pushButton.clicked.connect(self.Zoom_In_pushButton_OnClicked)
		self.ui.Zoom_Out_pushButton.clicked.connect(self.Zoom_Out_pushButton_OnClicked)
		self.ui.Background_Colors_comboBox.activated.connect(self.Background_Colors_comboBox_OnActivated)

	@core.executionTrace
	def closeUi(self, event):
		"""
		This Method Redefines The Ui Close Event.

		@param event: QEvent ( QEvent )
		"""

		event.accept()

		LOGGER.debug("> Removing '{0}' From Image Previewers List.".format(self))
		self._container.imagePreviewers.remove(self)

	@core.executionTrace
	def Zoom_In_pushButton_OnClicked(self, checked):
		"""
		This Method Is Triggered When Zoom_In_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.scaleView(self._keyZoomFactor)

	@core.executionTrace
	def Zoom_Out_pushButton_OnClicked(self, checked):
		"""
		This Method Is Triggered When Zoom_Out_pushButton Is Clicked.

		@param checked: Checked State. ( Boolean )
		"""

		self.scaleView(1 / self._keyZoomFactor)

	@core.executionTrace
	def Background_Colors_comboBox_OnActivated(self, index):
		"""
		This Method Is Triggered When Background_Colors_comboBox Index Changes.
		
		@param index: ComboBox Activated Item Index. ( Integer )
		"""

		graphicsView = self._ui.findChild(QGraphicsView)
		graphicsView.setBackgroundBrush(QBrush(self._graphicsSceneBackgroundColors[index][1]))

	@core.executionTrace
	def scaleView(self, scaleFactor):
		"""
		This Method Scales The QGraphicsView.

		@param scaleFactor: Float ( Float )
		"""

		graphicsView = self._ui.findChild(QGraphicsView)
		factor = graphicsView.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
		if factor < self._minimumZoomFactor or factor > self._maximumZoomFactor:
			return

		graphicsView.scale(scaleFactor, scaleFactor)

	@core.executionTrace
	def wheelEvent(self, event):
		"""
		This Method Redefines wheelEvent.

		@param event: QEvent ( QEvent )
		"""

		self.scaleView(pow(1.5, event.delta() / self._wheelZoomFactor))

	@core.executionTrace
	def keyPressEvent(self, event):
		"""
		This Method Redefines keyPressEvent.

		@param event: QEvent ( QEvent )
		"""

		key = event.key()
		if key == Qt.Key_Plus:
			self.scaleView(self._keyZoomFactor)
		elif key == Qt.Key_Minus:
			self.scaleView(1 / self._keyZoomFactor)
		else:
			QGraphicsView.keyPressEvent(self, event)

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

		self._uiPath = "ui/Preview.ui"
		self._uiResources = "resources"

		self._container = None
		self._settings = None
		self._settingsSection = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None
		self._coreInspector = None

		self._imagePreviewers = None
		self._maximumImagePreviewersInstances = 5

		self._previewLightingImageAction = None
		self._previewReflectionImageAction = None
		self._previewBackgroundImageAction = None
		
		self._inspectorButtons = {"Background" : {"object" : None, "text": "Preview Background Image", "row" : 1,"column" : 3},
									"Lighting" : {"object" : None, "text": "Preview Lighting Image", "row" : 1,"column" : 4},
									"Reflection" : {"object" : None, "text": "Preview Reflection Image", "row" : 1,"column" : 5}}

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		"""

		return self._uiPath

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

		@return: self._uiResources. ( String )
		"""

		return self._uiResources

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

		@return: self._container. ( QObject )
		"""

		return self._container

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

		@return: self._settings. ( QSettings )
		"""

		return self._settings

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

		@return: self._settingsSection. ( String )
		"""

		return self._settingsSection

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

		@return: self._corePreferencesManager. ( Object )
		"""

		return self._corePreferencesManager

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

		@return: self._coreDatabaseBrowser. ( Object )
		"""

		return self._coreDatabaseBrowser

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

		@return: self._coreInspector. ( Object )
		"""

		return self._coreInspector

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
	def imagePreviewers(self):
		"""
		This Method Is The Property For The _imagePreviewers Attribute.

		@return: self._imagePreviewers. ( List )
		"""

		return self._imagePreviewers

	@imagePreviewers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagePreviewers(self, value):
		"""
		This Method Is The Setter Method For The _imagePreviewers Attribute.

		@param value: Attribute Value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("imagePreviewers"))

	@imagePreviewers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagePreviewers(self):
		"""
		This Method Is The Deleter Method For The _imagePreviewers Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("imagePreviewers"))

	@property
	def maximumImagePreviewersInstances(self):
		"""
		This Method Is The Property For The _maximumImagePreviewersInstances Attribute.

		@return: self._maximumImagePreviewersInstances. ( Integer )
		"""

		return self._maximumImagePreviewersInstances

	@maximumImagePreviewersInstances.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumImagePreviewersInstances(self, value):
		"""
		This Method Is The Setter Method For The _maximumImagePreviewersInstances Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("maximumImagePreviewersInstances"))

	@maximumImagePreviewersInstances.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumImagePreviewersInstances(self):
		"""
		This Method Is The Deleter Method For The _maximumImagePreviewersInstances Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("maximumImagePreviewersInstances"))

	@property
	def previewBackgroundImageAction(self):
		"""
		This Method Is The Property For The _previewBackgroundImageAction Attribute.

		@return: self._previewBackgroundImageAction. ( QAction )
		"""

		return self._previewBackgroundImageAction

	@previewBackgroundImageAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewBackgroundImageAction(self, value):
		"""
		This Method Is The Setter Method For The _previewBackgroundImageAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("previewBackgroundImageAction"))

	@previewBackgroundImageAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewBackgroundImageAction(self):
		"""
		This Method Is The Deleter Method For The _previewBackgroundImageAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("previewBackgroundImageAction"))

	@property
	def previewLightingImageAction(self):
		"""
		This Method Is The Property For The _previewLightingImageAction Attribute.

		@return: self._previewLightingImageAction. ( QAction )
		"""

		return self._previewLightingImageAction

	@previewLightingImageAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewLightingImageAction(self, value):
		"""
		This Method Is The Setter Method For The _previewLightingImageAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("previewLightingImageAction"))

	@previewLightingImageAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewLightingImageAction(self):
		"""
		This Method Is The Deleter Method For The _previewLightingImageAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("previewLightingImageAction"))

	@property
	def previewReflectionImageAction(self):
		"""
		This Method Is The Property For The _previewReflectionImageAction Attribute.

		@return: self._previewReflectionImageAction. ( QAction )
		"""

		return self._previewReflectionImageAction

	@previewReflectionImageAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewReflectionImageAction(self, value):
		"""
		This Method Is The Setter Method For The _previewReflectionImageAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("previewReflectionImageAction"))

	@previewReflectionImageAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewReflectionImageAction(self):
		"""
		This Method Is The Deleter Method For The _previewReflectionImageAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("previewReflectionImageAction"))

	@property
	def inspectorButtons(self):
		"""
		This Method Is The Property For The _inspectorButtons Attribute.

		@return: self._inspectorButtons. ( Dictionary )
		"""

		return self._inspectorButtons

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

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiPath)
		self._uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiResources)
		self._container = container
		self._settings = self._container.settings
		self._settingsSection = self.name

		self._corePreferencesManager = self._container.componentsManager.components["core.preferencesManager"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface
		self._coreInspector = self._container.componentsManager.components["core.inspector"].interface

		self._imagePreviewers = []

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self._uiResources = os.path.basename(self._uiResources)
		self._container = None
		self._settings = None
		self._settingsSection = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None
		self._coreInspector = None

		for imagePreviewer in self._imagePreviewers[:]:
			imagePreviewer.ui.close()

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.Custom_Previewer_Path_lineEdit_setUi()
		
		self.addActions_()		
		self.addInspectorButtons()

		# Signals / Slots.
		self.ui.Custom_Previewer_Path_toolButton.clicked.connect(self.Custom_Previewer_Path_toolButton_OnClicked)
		self.ui.Custom_Previewer_Path_lineEdit.editingFinished.connect(self.Custom_Previewer_Path_lineEdit_OnEditFinished)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.removeActions_()
		self.removeInspectorButtons()

		# Signals / Slots.
		self.ui.Custom_Previewer_Path_toolButton.clicked.disconnect(self.Custom_Previewer_Path_toolButton_OnClicked)
		self.ui.Custom_Previewer_Path_lineEdit.editingFinished.disconnect(self.Custom_Previewer_Path_lineEdit_OnEditFinished)

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self._corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Custom_Previewer_Path_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self._corePreferencesManager.ui.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self.ui)
		self.ui.Custom_Previewer_Path_groupBox.setParent(None)

	@core.executionTrace
	def addActions_(self):
		"""
		This Method Adds Actions.
		"""

		LOGGER.debug("> Adding '{0}' Component Actions.".format(self.__class__.__name__))

		separatorAction = QAction(self._coreDatabaseBrowser.ui.Database_Browser_listView)
		separatorAction.setSeparator(True)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction(separatorAction)

		self._previewBackgroundImageAction = QAction("Preview Background Image ...", self._coreDatabaseBrowser.ui.Database_Browser_listView)
		self._previewBackgroundImageAction.triggered.connect(self.Database_Browser_listView_previewBackgroundImageAction)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self._previewBackgroundImageAction)

		self._previewLightingImageAction = QAction("Preview Lighting Image ...", self._coreDatabaseBrowser.ui.Database_Browser_listView)
		self._previewLightingImageAction.triggered.connect(self.Database_Browser_listView_previewLightingImageAction)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self._previewLightingImageAction)

		self._previewReflectionImageAction = QAction("Preview Reflection Image ...", self._coreDatabaseBrowser.ui.Database_Browser_listView)
		self._previewReflectionImageAction.triggered.connect(self.Database_Browser_listView_previewReflectionImageAction)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self._previewReflectionImageAction)

	@core.executionTrace
	def removeActions_(self):
		"""
		This Method Removes Actions.
		"""

		LOGGER.debug("> Removing '{0}' Component Actions.".format(self.__class__.__name__))

		self._coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self._previewBackgroundImageAction)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self._previewLightingImageAction)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self._previewReflectionImageAction)

		self._previewBackgroundImageAction = None
		self._previewLightingImageAction = None
		self._previewReflectionImageAction = None

	@core.executionTrace
	def addInspectorButtons(self):
		"""
		This Method Adds Buttons To The Inspector Component.
		"""
		
		self._coreInspector.ui.Options_groupBox.show()
		for key, value in self._inspectorButtons.items():
			value["object"] = QPushButton(value["text"])
			self._coreInspector.ui.Options_groupBox_gridLayout.addWidget(value["object"], value["row"], value["column"])
			value["object"].clicked.connect(functools.partial(self.showImagePreview, key))

	def removeInspectorButtons(self):
		"""
		This Method Removes Buttons From The Inspector Component.
		"""	

		for value in self._inspectorButtons.values():
			value["object"].setParent(None)

	@core.executionTrace
	def Database_Browser_listView_previewBackgroundImageAction(self, checked):
		"""
		This Method Is Triggered By previewBackgroundImageAction.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.showImagePreview("Background")

	@core.executionTrace
	def Database_Browser_listView_previewLightingImageAction(self, checked):
		"""
		This Method Is Triggered By previewLightingImageAction.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.showImagePreview("Lighting")

	@core.executionTrace
	def Database_Browser_listView_previewReflectionImageAction(self, checked):
		"""
		This Method Is Triggered By previewReflectionImageAction.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.showImagePreview("Reflection")

	@core.executionTrace
	def Custom_Previewer_Path_lineEdit_setUi(self):
		"""
		This Method Fills The Custom_Previewer_Path_lineEdit.
		"""

		customPreviewer = self._settings.getKey(self._settingsSection, "customPreviewer")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("Custom_Previewer_Path_lineEdit", customPreviewer.toString()))
		self.ui.Custom_Previewer_Path_lineEdit.setText(customPreviewer.toString())

	@core.executionTrace
	def Custom_Previewer_Path_toolButton_OnClicked(self, checked):
		"""
		This Method Is Called When Custom_Previewer_Path_toolButton Is Clicked.

		@param checked: Checked State. ( Boolean )
		"""

		customPreviewerExecutable = self._container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom Previewer Executable:", self._container.lastBrowsedPath))
		if customPreviewerExecutable != "":
			LOGGER.debug("> Chosen Custom Previewer Executable: '{0}'.".format(customPreviewerExecutable))
			self.ui.Custom_Previewer_Path_lineEdit.setText(QString(customPreviewerExecutable))
			self._settings.setKey(self._settingsSection, "customPreviewer", self.ui.Custom_Previewer_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def Custom_Previewer_Path_lineEdit_OnEditFinished(self):
		"""
		This Method Is Called When Custom_Previewer_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.Custom_Previewer_Path_lineEdit.text()))) and str(self.ui.Custom_Previewer_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring Preferences!")
			self.Custom_Previewer_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid Custom Previewer Executable File!".format(self.__class__.__name__)
		else:
			self._settings.setKey(self._settingsSection, "customPreviewer", self.ui.Custom_Previewer_Path_lineEdit.text())

	@core.executionTrace
	def showImagePreview(self, imageType, *args):
		"""
		This Method Launches An Image Preview.
		
		@param imageType: Image Type. ( String )
		@param *args: Arguments. ( * )
		"""
		
		customPreviewer = str(self.ui.Custom_Previewer_Path_lineEdit.text())

		selectedIblSets = self._coreDatabaseBrowser.getSelectedItems()
		for iblSet in selectedIblSets:
			if imageType == "Background":
				imagePath = getattr(iblSet._datas, "backgroundImage")
			elif imageType == "Lighting":
				imagePath = getattr(iblSet._datas, "lightingImage")
			elif imageType == "Reflection":
				imagePath = getattr(iblSet._datas, "reflectionImage")
			if imagePath:
				if os.path.exists(imagePath):
					if customPreviewer:
						previewCommand = None
						imagePath = os.path.normpath(imagePath)
						if platform.system() == "Windows" or platform.system() == "Microsoft":
								LOGGER.info("{0} | Launching '{1}' Custom Image Previewer With '{2}'.".format(self.__class__.__name__, os.path.basename(customPreviewer), imagePath))
								previewCommand = "\"{0}\" \"{1}\"".format(customPreviewer, imagePath)
						elif platform.system() == "Darwin":
								LOGGER.info("{0} | Launching '{1}' Custom Image Previewer With '{2}'.".format(self.__class__.__name__, os.path.basename(customPreviewer), imagePath))
								previewCommand = "open -a \"{0}\" \"{1}\"".format(customPreviewer, imagePath)
						elif platform.system() == "Linux":
								LOGGER.info("{0} | Launching '{1}' Custom Image Previewer With '{2}'.".format(self.__class__.__name__, os.path.basename(customPreviewer), imagePath))
								previewCommand = "\"{0}\" \"{1}\"".format(customPreviewer, imagePath)
						if previewCommand:
							LOGGER.debug("> Current Image Preview Command: '{0}'.".format(previewCommand))
							editProcess = QProcess()
							editProcess.startDetached(previewCommand)
					else:
						if not len(self._imagePreviewers) >= self._maximumImagePreviewersInstances:
							self.launchImagePreviewer(imagePath)
						else:
							messageBox.messageBox("Warning", "Warning", "{0} | You Can Only Launch '{1}' Image Previewer Instances At Same Time!".format(self.__class__.__name__, self._maximumImagePreviewersInstances))
							break
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Image File Doesn't Exists And Will Be Skipped!".format(self.__class__.__name__, imagePath))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Ibl Set Has No '{2}' Image Type And Will Be Skipped!".format(self.__class__.__name__, iblSet._datas.title, imageType))

	@core.executionTrace
	def launchImagePreviewer(self, imagePath):
		"""
		This Method Launches An Image Previewer.
		
		@param imagePath: Image Path. ( String )
		"""

		LOGGER.debug("> Launching Image Previewer For '{0}' Image.".format(imagePath))

		imagePreviewer = ImagePreviewer(self, imagePath)
		self._imagePreviewers.append(imagePreviewer)

	@core.executionTrace
	def removeImagePreviewer(self, imagePreviewer):
		"""
		This Method Removes An Image Previewer.
		
		@param imagePreviewer: Image Previewer. ( ImagePreviewer )
		"""

		LOGGER.debug("> Removing '{0}' Image Previewer.".format(imagePreviewer))

		self._imagePreviewers.remove(imagePreviewer)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
