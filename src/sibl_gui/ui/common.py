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
import inspect
import itertools
import logging
import os
import re
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QPixmap

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
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
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"Icon",
			"convertImage",
			"loadGraphicsItem",
			"getGraphicsItem",
			"getIcon",
			"getPixmap",
			"getImage",
			"getImageInformationsHeader",
			"filterImagePath",
			"getFormatedShotDate"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Icon(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for icon.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: path ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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
				for extension in UiConstants.thirdPartyImageFormats.itervalues():
					if re.search(extension, path, flags=re.IGNORECASE):
						image = Image(str(path))
						image = image.convertToQImage()
						graphicsItem = convertImage(image, type)
						break
				else:
					graphicsItem = type(umbra.ui.common.getResourcePath(UiConstants.formatErrorImage))
		return graphicsItem

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getGraphicsItem(path, type, asynchronousLoading=True, imagesCache=None):
		"""
		This method gets a display item: `QIcon <http://doc.qt.nokia.com/qicon.html>`_,
		`QImage <http://doc.qt.nokia.com/qimage.html>`_, `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_.

		:param path: Image path. ( String )
		:param type: QIcon, QImage, QPixmap. ( QObject )
		:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
		:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
		:return: Graphic display. ( QIcon, QImage, QPixmap )
		"""

		cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get(type.__name__)
		if cache is None:
			raise sibl_gui.exceptions.CacheExistsError("{0} | '{1}' cache doesn't exists!".format(
				inspect.getmodulename(__file__), type.__name__))

		if asynchronousLoading:
			cache.addDeferredContent(path)
		else:
			not cache.getContent(path) and cache.addContent(**{path : loadGraphicsItem(path, type)})
		return cache.getContent(path)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getIcon(path, asynchronousLoading=True, imagesCache=None):
		"""
		This method gets a `QIcon <http://doc.qt.nokia.com/qicon.html>`_.

		:param path: Icon image path. ( String )
		:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
		:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
		:return: QIcon. ( QIcon )
		"""

		cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get("QIcon")
		return getGraphicsItem(path, QIcon, asynchronousLoading, cache)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getPixmap(path, asynchronousLoading=True, imagesCache=None):
		"""
		This method gets a `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_.

		:param path: Icon image path. ( String )
		:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
		:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
		:return: QPixmap. ( QPixmap )
		"""

		cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get("QPixmap")
		return getGraphicsItem(path, QPixmap, asynchronousLoading, cache)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getImage(path, asynchronousLoading=True, imagesCache=None):
		"""
		This method gets a `QImage <http://doc.qt.nokia.com/qimage.html>`_.

		:param path: Icon image path. ( String )
		:param asynchronousLoading: Images are loaded asynchronously. ( Boolean )
		:param imagesCache: Image cache. ( Dictionary / AsynchronousGraphicsItemsCache )
		:return: QImage. ( QImage )
		"""

		cache = imagesCache and imagesCache or RuntimeGlobals.imagesCaches.get("QImage")
		return getGraphicsItem(path, QImage, asynchronousLoading, cache)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
def getImageInformationsHeader(path, graphicsItem):
		"""
		This method returns a :class:`sibl_gui.libraries.freeImage.freeImage.ImageInformationsHeader` class
		from given path and graphics item.

		:param path: Image path. ( String )
		:param graphicsItem: Image graphics item. ( QImage, QPixmap, QIcon )
		:return: Image informations header. ( ImageInformationsHeader )
		"""

		if not foundations.common.pathExists(path):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			inspect.getmodulename(__file__), path))

		if type(graphicsItem) is QIcon:
			graphicsItem = QPixmap(path)

		return ImageInformationsHeader(path=path,
										width=graphicsItem.width(),
										height=graphicsItem.height(),
										bpp=graphicsItem.depth(),
										osStats=os.stat(path))

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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
