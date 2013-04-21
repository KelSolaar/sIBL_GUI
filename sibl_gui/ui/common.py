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
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import hashlib
import itertools
import os
import re
from PyQt4.QtCore import Qt
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
from umbra.globals.uiConstants import UiConstants
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
		"getThumbnailPath",
		"extractThumbnail",
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
	This definition converts given image to given type.

	:param image: Image to convert. ( QImage )
	:param type: Type to convert to. ( QImage / QPixmap / QIcon )
	:return: Converted image. ( QImage / QPixmap / QIcon )
	"""

	graphicsItem = image
	if type == QIcon:
		graphicsItem = QIcon(QPixmap(image))
	elif type == QPixmap:
		graphicsItem = QPixmap(image)

	return graphicsItem

def getThumbnailPath(path, size, cacheDirectory=None):
	"""
	This definition returns given image thumbnail cached path at given size.

	:param path: Image path. ( String )
	:param size: Thumbnail size. ( String )
	:param cacheDirectory: Thumbnails cache directory. ( String )
	:return: Cached thumbnail path. ( String )
	"""

	cacheDirectory = cacheDirectory if cacheDirectory is not None else RuntimeGlobals.thumbnailsCacheDirectory
	return os.path.join(cacheDirectory,
					hashlib.md5("{0}_{1}.png".format(path, size).encode(Constants.encodingCodec)).hexdigest())

def extractThumbnail(path,
					size="Default",
					image=None,
					format="PNG",
					quality= -1,
					cacheDirectory=None):
	"""
	This definition extract given image thumbnail at given size.

	:param path: Image path. ( String )
	:param size: Thumbnail size. ( String )
	:param image: Image to use instead of given path one. ( QImage )
	:param format: Thumbnail format. ( String )
	:param quality: Thumbnail quality, -1 to 100. ( Integer )
	:param cacheDirectory: Thumbnails cache directory. ( String )
	:return: Thumbnail image. ( QImage )
	"""

	cacheDirectory = cacheDirectory if cacheDirectory is not None else RuntimeGlobals.thumbnailsCacheDirectory

	if not foundations.common.pathExists(cacheDirectory):
		foundations.io.setDirectory(cacheDirectory)

	thumbnailPath = getThumbnailPath(path, size, cacheDirectory)
	if not os.path.exists(thumbnailPath):
		thumbnail = QImage(path) if image is None else image
		thumbnail = thumbnail.scaled(UiConstants.thumbnailsSizes.get(size),
							UiConstants.thumbnailsSizes.get(size),
							Qt.KeepAspectRatio,
							Qt.SmoothTransformation)
		thumbnail.save(thumbnailPath, format, quality)
		return thumbnail
	else:
		return QImage(thumbnailPath)

def loadGraphicsItem(path, type, size="Default"):
	"""
	This definition loads a graphic item: `QIcon <http://doc.qt.nokia.com/qicon.html>`_,
	`QImage <http://doc.qt.nokia.com/qimage.html>`_, `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_.

	:param path: Image path. ( String )
	:param type: QIcon, QImage, QPixmap. ( QObject )
	:param size: Image size. ( String )
	:return: Image. ( QIcon, QImage, QPixmap )
	"""

	if not foundations.common.pathExists(path):
		graphicsItem = type(umbra.ui.common.getResourcePath(UiConstants.missingImage))
	else:
		for extension in UiConstants.nativeImageFormats.itervalues():
			if re.search(extension, path, flags=re.IGNORECASE):
				graphicsItem = convertImage(extractThumbnail(path, size), type) if size != "Default" else type(path)
				break
		else:
			errorImage = umbra.ui.common.getResourcePath(UiConstants.formatErrorImage)
			for extension in UiConstants.thirdPartyImageFormats.itervalues():
				if re.search(extension, path, flags=re.IGNORECASE):
					try:
						image = Image(path)
						image = image.convertToQImage()
						graphicsItem = \
						convertImage(extractThumbnail(path, size, image), type) if size != "Default" else \
						convertImage(image, type)
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

def getGraphicsItem(path, type, size="Default", asynchronousLoading=True, placeholder=None, imagesCache=None):
	"""
	This definition returns a display item: `QIcon <http://doc.qt.nokia.com/qicon.html>`_,
	`QImage <http://doc.qt.nokia.com/qimage.html>`_, `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_ instance.

	:param path: Image path. ( String )
	:param type: QIcon, QImage, QPixmap. ( QObject )
	:param size: Image size. ( String )
	:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
	:param placeholder: Placeholder to use while loading asynchronously. ( QIcon, QImage, QPixmap )
	:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
	:return: Image. ( QIcon, QImage, QPixmap )
	"""

	if not foundations.common.pathExists(path):
		LOGGER.warning("!> {0} | '{1}' file doesn't exists!".format(__name__, path))
		return loadGraphicsItem(path, type, size)

	cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get(type.__name__)
	if cache is None:
		raise sibl_gui.exceptions.CacheExistsError("{0} | '{1}' cache doesn't exists!".format(__name__, type.__name__))

	graphicsItem = cache.getContent(path, size)
	if graphicsItem is None:
		if asynchronousLoading:
			cache.loadAsynchronousContent(**{path : (type, size, placeholder)})
		else:
			cache.loadContent(**{path : (type, size)})
		return cache.getContent(path, size)
	return graphicsItem

def getIcon(path, size="Default", asynchronousLoading=True, placeholder=None, imagesCache=None):
	"""
	This definition returns a `QIcon <http://doc.qt.nokia.com/qicon.html>`_ instance.

	:param path: Icon image path. ( String )
	:param size: Image size. ( String )
	:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
	:param placeholder: Placeholder to use while loading asynchronously. ( QIcon )
	:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
	:return: QIcon. ( QIcon )
	"""

	cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get("QIcon")
	return getGraphicsItem(path, QIcon, size, asynchronousLoading, placeholder, cache)

def getPixmap(path, size="Default", asynchronousLoading=True, placeholder=None, imagesCache=None):
	"""
	This definition returns a `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_ instance.

	:param path: Icon image path. ( String )
	:param size: Image size. ( String )
	:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
	:param placeholder: Placeholder to use while loading asynchronously. ( QPixmap )
	:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
	:return: QPixmap. ( QPixmap )
	"""

	cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get("QPixmap")
	return getGraphicsItem(path, QPixmap, size, asynchronousLoading, placeholder, cache)

def getImage(path, size="Default", asynchronousLoading=True, placeholder=None, imagesCache=None):
	"""
	This definition returns a `QImage <http://doc.qt.nokia.com/qimage.html>`_ instance.

	:param path: Icon image path. ( String )
	:param size: Image size. ( String )
	:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
	:param placeholder: Placeholder to use while loading asynchronously. ( QImage )
	:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
	:return: QImage. ( QImage )
	"""

	cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get("QImage")
	return getGraphicsItem(path, QImage, size, asynchronousLoading, placeholder, cache)

def createPixmap(width=128, height=128, text=None):
	"""
	This definition create a default `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_ instance.

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
	This definition returns a :class:`sibl_gui.libraries.freeImage.freeImage.ImageInformationsHeader` class
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
	This definition filters the image path.

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
	This definition returns a formated shot date.

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
