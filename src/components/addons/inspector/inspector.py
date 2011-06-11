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
***		Inspector Component Module.
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
#class Image_QGraphicsItem(QGraphicsItem):
#	"""
#	This Class Is The Image_QGraphicsItem Class.
#	"""
#
#	@core.executionTrace
#	def __init__(self, image):
#		"""
#		This Method Initializes The Class.
#		
#		@param image: Image. ( QImage )
#		"""
#
#		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))
#
#		QGraphicsItem.__init__(self)
#
#		# --- Setting Class Attributes. ---
#		self._image = image
#
#	#***************************************************************************************
#	#***	Attributes Properties
#	#***************************************************************************************
#	@property
#	def image(self):
#		"""
#		This Method Is The Property For The _image Attribute.
#
#		@return: self._image. ( QImage )
#		"""
#
#		return self._image
#
#	@image.setter
#	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
#	def image(self, value):
#		"""
#		This Method Is The Setter Method For The _image Attribute.
#		
#		@param value: Attribute Value. ( QImage )
#		"""
#
#		if value:
#			assert type(value) is QImage, "'{0}' Attribute: '{1}' Type Is Not 'QImage'!".format("image", value)
#		self._imagePath = value
#
#	@image.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def image(self):
#		"""
#		This Method Is The Deleter Method For The _image Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("image"))
#
#	#***************************************************************************************
#	#***	Class Methods
#	#***************************************************************************************
#	@core.executionTrace
#	def boundingRect(self):
#		"""
#		This Method Sets The Bounding Rectangle.
#		"""
#
#		return QRectF(-(self._image.width()) / 2, -(self._image.height()) / 2, self._image.width(), self._image.height())
#
#	@core.executionTrace
#	def paint(self, painter, options, widget):
#		"""
#		This Method Paints The Image.
#
#		@param painter: QPainter ( QPainter )
#		@param options: QStyleOptionGraphicsItem  ( QStyleOptionGraphicsItem  )
#		@param widget: QWidget ( QWidget )
#		"""
#
#		painter.drawImage(-(self._image.width() / 2), -(self._image.height() / 2), self._image)
#
#class ImagePreviewer(object):
#	"""
#	This Is The ImagePreviewer Class.
#	"""
#
#	@core.executionTrace
#	def __init__(self, container, imagePath):
#		"""
#		This Method Initializes The Class.
#		
#		@param container: Container. ( Object )
#		@param imagePath: Image Path. ( String )
#		"""
#
#		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))
#
#		# --- Setting Class Attributes. ---
#		self._container = container
#		self._imagePath = imagePath
#
#		self._uiPath = "ui/Image_Previewer.ui"
#		self._uiPath = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiPath)
#		self._uiResources = "resources"
#		self._uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiResources)
#		self._uiZoomInIcon = "Zoom_In.png"
#		self._uiZoomOutIcon = "Zoom_Out.png"
#
#		self._ui = uic.loadUi(self._uiPath)
#		if "." in sys.path:
#			sys.path.remove(".")
#		# Ensure The Ui Object Is Destroyed On Close To Avoid Memory Leaks.
#		self._ui.setAttribute(Qt.WA_DeleteOnClose)
#		# Reimplementing Widget Close Event Method.
#		self._ui.closeEvent = self.closeUi
#
#		self._graphicsSceneBackgroundColors = (("Dark", QColor(32, 32, 32)), ("Average", QColor(128, 128, 128)), ("Bright", QColor(200, 200, 200)))
#		self._minimumZoomFactor = 0.125
#		self._maximumZoomFactor = 25
#		self._graphicsSceneMargin = 128
#		self._graphicsSceneWidth = QApplication.desktop().width() * (1 / self._minimumZoomFactor * 1.75)
#		self._graphicsSceneHeight = QApplication.desktop().height() * (1 / self._minimumZoomFactor * 1.75)
#		self._wheelZoomFactor = 350.0
#		self._keyZoomFactor = 1.20
#
#		self.initializeUi()
#
#		self._ui.show()
#
#	#***************************************************************************************
#	#***	Attributes Properties
#	#***************************************************************************************
#	@property
#	def container(self):
#		"""
#		This Method Is The Property For The _container Attribute.
#
#		@return: self._container. ( QObject )
#		"""
#
#		return self._container
#
#	@container.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def container(self, value):
#		"""
#		This Method Is The Setter Method For The _container Attribute.
#
#		@param value: Attribute Value. ( QObject )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))
#
#	@container.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def container(self):
#		"""
#		This Method Is The Deleter Method For The _container Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))
#
#	@property
#	def imagePath(self):
#		"""
#		This Method Is The Property For The _imagePath Attribute.
#
#		@return: self._imagePath. ( String )
#		"""
#
#		return self._imagePath
#
#	@imagePath.setter
#	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
#	def imagePath(self, value):
#		"""
#		This Method Is The Setter Method For The _imagePath Attribute.
#
#		@param value: Attribute Value. ( String )
#		"""
#
#		if value:
#			assert type(value) in (str, unicode, QString), "'{0}' Attribute: '{1}' Type Is Not 'str', 'unicode' or 'QString'!".format("imagePath", value)
#			assert os.path.exists(value), "'{0}' Attribute: '{1}' Image File Doesn't Exists!".format("imagePath", value)
#		self._imagePath = value
#
#	@imagePath.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def imagePath(self):
#		"""
#		This Method Is The Deleter Method For The _imagePath Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("imagePath"))
#
#	@property
#	def uiPath(self):
#		"""
#		This Method Is The Property For The _uiPath Attribute.
#
#		@return: self._uiPath. ( String )
#		"""
#
#		return self._uiPath
#
#	@uiPath.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def uiPath(self, value):
#		"""
#		This Method Is The Setter Method For The _uiPath Attribute.
#
#		@param value: Attribute Value. ( String )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))
#
#	@uiPath.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def uiPath(self):
#		"""
#		This Method Is The Deleter Method For The _uiPath Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))
#
#	@property
#	def uiResources(self):
#		"""
#		This Method Is The Property For The _uiResources Attribute.
#
#		@return: self._uiResources. ( String )
#		"""
#
#		return self._uiResources
#
#	@uiResources.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def uiResources(self, value):
#		"""
#		This Method Is The Setter Method For The _uiResources Attribute.
#
#		@param value: Attribute Value. ( String )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))
#
#	@uiResources.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def uiResources(self):
#		"""
#		This Method Is The Deleter Method For The _uiResources Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))
#
#	@property
#	def uiZoomInIcon(self):
#		"""
#		This Method Is The Property For The _uiZoomInIcon Attribute.
#
#		@return: self._uiZoomInIcon. ( String )
#		"""
#
#		return self._uiZoomInIcon
#
#	@uiZoomInIcon.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def uiZoomInIcon(self, value):
#		"""
#		This Method Is The Setter Method For The _uiZoomInIcon Attribute.
#
#		@param value: Attribute Value. ( String )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiZoomInIcon"))
#
#	@uiZoomInIcon.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def uiZoomInIcon(self):
#		"""
#		This Method Is The Deleter Method For The _uiZoomInIcon Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiZoomInIcon"))
#
#	@property
#	def uiZoomOutIcon(self):
#		"""
#		This Method Is The Property For The _uiZoomOutIcon Attribute.
#
#		@return: self._uiZoomOutIcon. ( String )
#		"""
#
#		return self._uiZoomOutIcon
#
#	@uiZoomOutIcon.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def uiZoomOutIcon(self, value):
#		"""
#		This Method Is The Setter Method For The _uiZoomOutIcon Attribute.
#
#		@param value: Attribute Value. ( String )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiZoomOutIcon"))
#
#	@uiZoomOutIcon.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def uiZoomOutIcon(self):
#		"""
#		This Method Is The Deleter Method For The _uiZoomOutIcon Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiZoomOutIcon"))
#
#	@property
#	def ui(self):
#		"""
#		This Method Is The Property For The _ui Attribute.
#
#		@return: self._ui. ( Object )
#		"""
#
#		return self._ui
#
#	@ui.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def ui(self, value):
#		"""
#		This Method Is The Setter Method For The _ui Attribute.
#		
#		@param value: Attribute Value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("ui"))
#
#	@ui.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def ui(self):
#		"""
#		This Method Is The Deleter Method For The _ui Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("ui"))
#
#	@property
#	def graphicsSceneBackgroundColors(self):
#		"""
#		This Method Is The Property For The _graphicsSceneBackgroundColors Attribute.
#
#		@return: self._graphicsSceneBackgroundColors. ( QColors )
#		"""
#
#		return self._graphicsSceneBackgroundColors
#
#	@graphicsSceneBackgroundColors.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def graphicsSceneBackgroundColors(self, value):
#		"""
#		This Method Is The Setter Method For The _graphicsSceneBackgroundColors Attribute.
#		
#		@param value: Attribute Value. ( QColors )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsSceneBackgroundColors"))
#
#	@graphicsSceneBackgroundColors.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def graphicsSceneBackgroundColors(self):
#		"""
#		This Method Is The Deleter Method For The _graphicsSceneBackgroundColors Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsSceneBackgroundColors"))
#
#	@property
#	def graphicsSceneMargin(self):
#		"""
#		This Method Is The Property For The _graphicsSceneMargin Attribute.
#
#		@return: self._graphicsSceneMargin. ( Integer )
#		"""
#
#		return self._graphicsSceneMargin
#
#	@graphicsSceneMargin.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def graphicsSceneMargin(self, value):
#		"""
#		This Method Is The Setter Method For The _graphicsSceneMargin Attribute.
#		
#		@param value: Attribute Value. ( Integer )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsSceneMargin"))
#
#	@graphicsSceneMargin.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def graphicsSceneMargin(self):
#		"""
#		This Method Is The Deleter Method For The _graphicsSceneMargin Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsSceneMargin"))
#
#	@property
#	def graphicsSceneWidth(self):
#		"""
#		This Method Is The Property For The _graphicsSceneWidth Attribute.
#
#		@return: self._graphicsSceneWidth. ( Integer )
#		"""
#
#		return self._graphicsSceneWidth
#
#	@graphicsSceneWidth.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def graphicsSceneWidth(self, value):
#		"""
#		This Method Is The Setter Method For The _graphicsSceneWidth Attribute.
#		
#		@param value: Attribute Value. ( Integer )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsSceneWidth"))
#
#	@graphicsSceneWidth.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def graphicsSceneWidth(self):
#		"""
#		This Method Is The Deleter Method For The _graphicsSceneWidth Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsSceneWidth"))
#
#	@property
#	def graphicsSceneHeight(self):
#		"""
#		This Method Is The Property For The _graphicsSceneHeight Attribute.
#
#		@return: self._graphicsSceneHeight. ( Object )
#		"""
#
#		return self._graphicsSceneHeight
#
#	@graphicsSceneHeight.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def graphicsSceneHeight(self, value):
#		"""
#		This Method Is The Setter Method For The _graphicsSceneHeight Attribute.
#		
#		@param value: Attribute Value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("graphicsSceneHeight"))
#
#	@graphicsSceneHeight.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def graphicsSceneHeight(self):
#		"""
#		This Method Is The Deleter Method For The _graphicsSceneHeight Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("graphicsSceneHeight"))
#
#	@property
#	def minimumZoomFactor(self):
#		"""
#		This Method Is The Property For The _minimumZoomFactor Attribute.
#
#		@return: self._minimumZoomFactor. ( Float )
#		"""
#
#		return self._minimumZoomFactor
#
#	@minimumZoomFactor.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def minimumZoomFactor(self, value):
#		"""
#		This Method Is The Setter Method For The _minimumZoomFactor Attribute.
#		
#		@param value: Attribute Value. ( Float )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("minimumZoomFactor"))
#
#	@minimumZoomFactor.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def minimumZoomFactor(self):
#		"""
#		This Method Is The Deleter Method For The _minimumZoomFactor Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("minimumZoomFactor"))
#
#	@property
#	def maximumZoomFactor(self):
#		"""
#		This Method Is The Property For The _maximumZoomFactor Attribute.
#
#		@return: self._maximumZoomFactor. ( Float )
#		"""
#
#		return self._maximumZoomFactor
#
#	@maximumZoomFactor.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def maximumZoomFactor(self, value):
#		"""
#		This Method Is The Setter Method For The _maximumZoomFactor Attribute.
#		
#		@param value: Attribute Value. ( Float )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("maximumZoomFactor"))
#
#	@maximumZoomFactor.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def maximumZoomFactor(self):
#		"""
#		This Method Is The Deleter Method For The _maximumZoomFactor Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("maximumZoomFactor"))
#
#	@property
#	def wheelZoomFactor(self):
#		"""
#		This Method Is The Property For The _wheelZoomFactor Attribute.
#
#		@return: self._wheelZoomFactor. ( Float )
#		"""
#
#		return self._wheelZoomFactor
#
#	@wheelZoomFactor.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def wheelZoomFactor(self, value):
#		"""
#		This Method Is The Setter Method For The _wheelZoomFactor Attribute.
#		
#		@param value: Attribute Value. ( Float )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("wheelZoomFactor"))
#
#	@wheelZoomFactor.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def wheelZoomFactor(self):
#		"""
#		This Method Is The Deleter Method For The _wheelZoomFactor Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("wheelZoomFactor"))
#
#	@property
#	def keyZoomFactor(self):
#		"""
#		This Method Is The Property For The _keyZoomFactor Attribute.
#
#		@return: self._keyZoomFactor. ( Float )
#		"""
#
#		return self._keyZoomFactor
#
#	@keyZoomFactor.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def keyZoomFactor(self, value):
#		"""
#		This Method Is The Setter Method For The _keyZoomFactor Attribute.
#		
#		@param value: Attribute Value. ( Float )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("keyZoomFactor"))
#
#	@keyZoomFactor.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def keyZoomFactor(self):
#		"""
#		This Method Is The Deleter Method For The _keyZoomFactor Attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("keyZoomFactor"))
#
#	#***************************************************************************************
#	#***	Class Methods
#	#***************************************************************************************
#	@core.executionTrace
#	def initializeUi(self):
#		"""
#		This Method Initializes The Widget Ui.
#		"""
#
#		LOGGER.debug("> Initializing '{0}' Ui.".format(self.__class__.__name__))
#
#		self._ui.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiZoomInIcon)))
#		self._ui.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiZoomOutIcon)))
#
#		self._ui.Background_Colors_comboBox.addItems([color[0] for color in self._graphicsSceneBackgroundColors])
#
#		for extension in UiConstants.nativeImageFormats.values():
#			if re.search(extension, self._imagePath):
#				LOGGER.debug("> Loading Native Format '{0}' Image.".format(self._imagePath))
#				image = QImage(self._imagePath)
#				bpp = image.depth()
#				break
#		else:
#			for extension in UiConstants.thirdPartyImageFormats.values():
#				if re.search(extension, self._imagePath):
#					LOGGER.debug("> Loading Third Party Format '{0}' Image.".format(self._imagePath))
#					image = Image(str(self._imagePath))
#					image = image.convertToQImage()
#					bpp = image._datas.bpp
#					break
#
#		self._ui.Image_Informations_label.setText("{0} - {1} x {2} - {3} BPP".format(os.path.basename(self._imagePath), image.width(), image.height(), bpp))
#
#		LOGGER.debug("> Initializing Graphics View.")
#		graphicsView = QGraphicsView()
#		graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#		graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#		graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
#		graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
#		# Reimplementing QGraphics View wheelEvent Method.
#		graphicsView.wheelEvent = self.wheelEvent
#
#		LOGGER.debug("> Initializing Graphics Scene.")
#		graphicsScene = QGraphicsScene(graphicsView)
#		graphicsScene.setItemIndexMethod(QGraphicsScene.NoIndex)
#		graphicsScene.setSceneRect(-(float(self._graphicsSceneWidth)) / 2, -(float(self._graphicsSceneHeight)) / 2, float(self._graphicsSceneWidth), float(self._graphicsSceneHeight))
#
#		graphicsView.setScene(graphicsScene)
#
#		graphicsView.setBackgroundBrush(QBrush(self._graphicsSceneBackgroundColors[0][1]))
#
#		LOGGER.debug("> Initializing Graphics Item.")
#		graphicsItem = Image_QGraphicsItem(image)
#		graphicsScene.addItem(graphicsItem)
#
#		self._ui.Image_Previewer_frame_gridLayout.addWidget(graphicsView)
#
#		width = image.width() > QApplication.desktop().width() and QApplication.desktop().width() / 1.5 + self._graphicsSceneMargin or image.width() + self._graphicsSceneMargin
#		height = image.height() > QApplication.desktop().height() and QApplication.desktop().height() / 1.5 + self._graphicsSceneMargin or image.height() + self._graphicsSceneMargin
#
#		self._ui.resize(width, height)
#
#		# Signals / Slots.
#		self.ui.Zoom_In_pushButton.clicked.connect(self.Zoom_In_pushButton_OnClicked)
#		self.ui.Zoom_Out_pushButton.clicked.connect(self.Zoom_Out_pushButton_OnClicked)
#		self.ui.Background_Colors_comboBox.activated.connect(self.Background_Colors_comboBox_OnActivated)
#
#	@core.executionTrace
#	def closeUi(self, event):
#		"""
#		This Method Redefines The Ui Close Event.
#
#		@param event: QEvent ( QEvent )
#		"""
#
#		event.accept()
#
#		LOGGER.debug("> Removing '{0}' From Image Previewers List.".format(self))
#		self._container.imagePreviewers.remove(self)
#
#	@core.executionTrace
#	def Zoom_In_pushButton_OnClicked(self, checked):
#		"""
#		This Method Is Triggered When Zoom_In_pushButton Is Clicked.
#		
#		@param checked: Checked State. ( Boolean )
#		"""
#
#		self.scaleView(self._keyZoomFactor)
#
#	@core.executionTrace
#	def Zoom_Out_pushButton_OnClicked(self, checked):
#		"""
#		This Method Is Triggered When Zoom_Out_pushButton Is Clicked.
#
#		@param checked: Checked State. ( Boolean )
#		"""
#
#		self.scaleView(1 / self._keyZoomFactor)
#
#	@core.executionTrace
#	def Background_Colors_comboBox_OnActivated(self, index):
#		"""
#		This Method Is Triggered When Background_Colors_comboBox Index Changes.
#		
#		@param index: ComboBox Activated Item Index. ( Integer )
#		"""
#
#		graphicsView = self._ui.findChild(QGraphicsView)
#		graphicsView.setBackgroundBrush(QBrush(self._graphicsSceneBackgroundColors[index][1]))
#
#	@core.executionTrace
#	def scaleView(self, scaleFactor):
#		"""
#		This Method Scales The QGraphicsView.
#
#		@param scaleFactor: Float ( Float )
#		"""
#
#		graphicsView = self._ui.findChild(QGraphicsView)
#		factor = graphicsView.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
#		if factor < self._minimumZoomFactor or factor > self._maximumZoomFactor:
#			return
#
#		graphicsView.scale(scaleFactor, scaleFactor)
#
#	@core.executionTrace
#	def wheelEvent(self, event):
#		"""
#		This Method Redefines wheelEvent.
#
#		@param event: QEvent ( QEvent )
#		"""
#
#		self.scaleView(pow(1.5, event.delta() / self._wheelZoomFactor))
#
#	@core.executionTrace
#	def keyPressEvent(self, event):
#		"""
#		This Method Redefines keyPressEvent.
#
#		@param event: QEvent ( QEvent )
#		"""
#
#		key = event.key()
#		if key == Qt.Key_Plus:
#			self.scaleView(self._keyZoomFactor)
#		elif key == Qt.Key_Minus:
#			self.scaleView(1 / self._keyZoomFactor)
#		else:
#			QGraphicsView.keyPressEvent(self, event)

class Inspector(UiComponent):
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

		self._uiPath = "ui/Inspector.ui"
		self._uiResources = "resources"

		self._container = None
		self._settings = None
		self._settingsSection = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None

		self._imagePreviewers = None
		self._maximumInspectorInstances = 5

		self._previewLightingImageAction = None
		self._previewReflectionImageAction = None
		self._inspectIblSetAction = None

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
	def maximumInspectorInstances(self):
		"""
		This Method Is The Property For The _maximumInspectorInstances Attribute.

		@return: self._maximumInspectorInstances. ( Integer )
		"""

		return self._maximumInspectorInstances

	@maximumInspectorInstances.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumInspectorInstances(self, value):
		"""
		This Method Is The Setter Method For The _maximumInspectorInstances Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("maximumInspectorInstances"))

	@maximumInspectorInstances.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumInspectorInstances(self):
		"""
		This Method Is The Deleter Method For The _maximumInspectorInstances Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("maximumInspectorInstances"))

	@property
	def inspectIblSetAction(self):
		"""
		This Method Is The Property For The _inspectIblSetAction Attribute.

		@return: self._inspectIblSetAction. ( QAction )
		"""

		return self._inspectIblSetAction

	@inspectIblSetAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectIblSetAction(self, value):
		"""
		This Method Is The Setter Method For The _inspectIblSetAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("inspectIblSetAction"))

	@inspectIblSetAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectIblSetAction(self):
		"""
		This Method Is The Deleter Method For The _inspectIblSetAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("inspectIblSetAction"))

	
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

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.addActions_()

		# Signals / Slots.

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.removeActions_()

		# Signals / Slots.

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self._container.addDockWidget(Qt.DockWidgetArea(1), self.ui)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		#self._corePreferencesManager.ui.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self.ui)
		#self.ui.Custom_Previewer_Path_groupBox.setParent(None)

	@core.executionTrace
	def addActions_(self):
		"""
		This Method Adds Actions.
		"""

		LOGGER.debug("> Adding '{0}' Component Actions.".format(self.__class__.__name__))

		separatorAction = QAction(self._coreDatabaseBrowser.ui.Database_Browser_listView)
		separatorAction.setSeparator(True)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction(separatorAction)

		self._inspectIblSetAction = QAction("Inspect Ibl Set ...", self._coreDatabaseBrowser.ui.Database_Browser_listView)
		self._inspectIblSetAction.triggered.connect(self.Database_Browser_listView_inspectIblSetAction)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self._inspectIblSetAction)

	@core.executionTrace
	def removeActions_(self):
		"""
		This Method Removes Actions.
		"""

		LOGGER.debug("> Removing '{0}' Component Actions.".format(self.__class__.__name__))

		self._coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self._inspectIblSetAction)

		self._inspectIblSetAction = None

	@core.executionTrace
	def Database_Browser_listView_inspectIblSetAction(self, checked):
		"""
		This Method Is Triggered By inspectIblSetAction.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.ui.show()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
