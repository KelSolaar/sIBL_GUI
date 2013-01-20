#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines common ui manipulation related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import itertools
import os
import re
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPen

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.verbose
import sibl_gui.exceptions
import umbra.ui.common
from sibl_gui.libraries.freeImage.freeImage import Image
from sibl_gui.libraries.freeImage.freeImage import ImageInformationsHeader
from sibl_gui.globals.uiConstants import UiConstants
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"convertImage",
			"loadGraphicsItem",
			"getGraphicsItem",
			"getIcon",
			"getPixmap",
			"getImage",
			"createPixmap",
			"getImageInformationsHeader",
			"filterImagePath",
			"getFormatedShotDate"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def convertImage(image, type):
	"""
	This method converts given image to given type.

	:param image: Image to convert. ( QImage )
	:return: Converted image. ( QImage / QPixmap / QIcon )
	"""

	graphicsItem = image
	if type == QIcon:
		graphicsItem = QIcon(QPixmap(image))
	elif type == QPixmap:
		graphicsItem = QPixmap(image)

	return graphicsItem

def loadGraphicsItem(path, type):
	"""
	This method loads a graphic item: `QIcon <http://doc.qt.nokia.com/qicon.html>`_,
	`QImage <http://doc.qt.nokia.com/qimage.html>`_, `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_.

	:param path: Image path. ( String )
	:param type: QIcon, QImage, QPixmap. ( QObject )
	:return: Graphics item. ( QIcon, QImage, QPixmap )
	"""

	if not foundations.common.pathExists(path):
		graphicsItem = type(umbra.ui.common.getResourcePath(UiConstants.missingImage))
	else:
		for extension in UiConstants.nativeImageFormats.itervalues():
			if re.search(extension, path, flags=re.IGNORECASE):
				graphicsItem = type(path)
				break
		else:
			errorImage = umbra.ui.common.getResourcePath(UiConstants.formatErrorImage)
			for extension in UiConstants.thirdPartyImageFormats.itervalues():
				if re.search(extension, path, flags=re.IGNORECASE):
					try:
						image = Image(path)
						image = image.convertToQImage()
						graphicsItem = convertImage(image, type)
						break
					except Exception as error:
						LOGGER.error("!> {0} | Exception raised while reading '{1}' image: '{2}'!".format(__name__,
																										path,
																										error))
						graphicsItem = type(errorImage)
						break
			else:
				graphicsItem = type(errorImage)
	return graphicsItem

def getGraphicsItem(path, type, asynchronousLoading=True, imagesCache=None):
	"""
	This method returns a display item: `QIcon <http://doc.qt.nokia.com/qicon.html>`_,
	`QImage <http://doc.qt.nokia.com/qimage.html>`_, `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_ instance.

	:param path: Image path. ( String )
	:param type: QIcon, QImage, QPixmap. ( QObject )
	:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
	:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
	:return: Graphic display. ( QIcon, QImage, QPixmap )
	"""

	if not foundations.common.pathExists(path):
		LOGGER.warning("!> {0} | '{1}' file doesn't exists!".format(__name__, path))
		return loadGraphicsItem(path, type)

	cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get(type.__name__)
	if cache is None:
		raise sibl_gui.exceptions.CacheExistsError("{0} | '{1}' cache doesn't exists!".format(__name__, type.__name__))

	if asynchronousLoading:
		cache.addDeferredContent(path)
	else:
		not cache.getContent(path) and cache.addContent(**{str(path) : loadGraphicsItem(path, type)})
	return cache.getContent(path)

def getIcon(path, asynchronousLoading=True, imagesCache=None):
	"""
	This method returns a `QIcon <http://doc.qt.nokia.com/qicon.html>`_ instance.

	:param path: Icon image path. ( String )
	:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
	:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
	:return: QIcon. ( QIcon )
	"""

	cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get("QIcon")
	return getGraphicsItem(path, QIcon, asynchronousLoading, cache)

def getPixmap(path, asynchronousLoading=True, imagesCache=None):
	"""
	This method returns a `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_ instance.

	:param path: Icon image path. ( String )
	:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
	:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
	:return: QPixmap. ( QPixmap )
	"""

	cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get("QPixmap")
	return getGraphicsItem(path, QPixmap, asynchronousLoading, cache)

def getImage(path, asynchronousLoading=True, imagesCache=None):
	"""
	This method returns a `QImage <http://doc.qt.nokia.com/qimage.html>`_ instance.

	:param path: Icon image path. ( String )
	:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
	:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
	:return: QImage. ( QImage )
	"""

	cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get("QImage")
	return getGraphicsItem(path, QImage, asynchronousLoading, cache)

def createPixmap(width=128, height=128, text=None):
	"""
	This method create a default `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_ instance.

	:param width: Pixmap width. ( Integer )
	:param height: Pixmap height. ( Integer )
	:param text: Pximap text. ( String )
	:return: QPixmap. ( QPixmap )
	"""

	loadingPixmap = QPixmap(width, height)
	loadingPixmap.fill(QColor(96, 96, 96))
	painter = QPainter(loadingPixmap)
	if text:
		painter.setPen(QPen(QColor(192, 192, 192)))
		pointX = painter.fontMetrics().width(text) / 2
		pointY = width / 2
		painter.drawText(pointX, pointY, text)
	return loadingPixmap

@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
def getImageInformationsHeader(path, graphicsItem):
	"""
	This method returns a :class:`sibl_gui.libraries.freeImage.freeImage.ImageInformationsHeader` class
	from given path and graphics item.

	:param path: Image path. ( String )
	:param graphicsItem: Image graphics item. ( QImage, QPixmap, QIcon )
	:return: Image informations header. ( ImageInformationsHeader )
	"""

	if not foundations.common.pathExists(path):
		raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(__name__, path))

	if type(graphicsItem) is QIcon:
		graphicsItem = QPixmap(path)

	return ImageInformationsHeader(path=path,
									width=graphicsItem.width(),
									height=graphicsItem.height(),
									bpp=graphicsItem.depth(),
									osStats=os.stat(path))

def filterImagePath(path):
	"""
	This method filters the image path.

	:param path: Image path. ( String )
	:return: Path. ( String )
	"""

	if foundations.common.pathExists(path):
		for extension in itertools.chain(UiConstants.nativeImageFormats.itervalues(),
										UiConstants.thirdPartyImageFormats.itervalues()):
			if re.search(extension, path, flags=re.IGNORECASE):
				return path
		else:
			return umbra.ui.common.getResourcePath(UiConstants.formatErrorImage)
	else:
		return umbra.ui.common.getResourcePath(UiConstants.missingImage)

def getFormatedShotDate(date, time):
	"""
	This method returns a formated shot date.

	:param date: Ibl Set date key value. ( String )
	:param time: Ibl Set time key value. ( String )
	:return: Current shot date. ( String )
	"""

	LOGGER.debug("> Formating shot date with '{0}' date and '{1}' time.".format(date, time))

	if date and time and date != Constants.nullObject and time != Constants.nullObject:
		shotTime = "{0}H{1}".format(*time.split(":"))
		shotDate = date.replace(":", "/")[2:] + " - " + shotTime

		LOGGER.debug("> Formated shot date: '{0}'.".format(shotDate))
		return shotDate
	else:
		return Constants.nullObject
