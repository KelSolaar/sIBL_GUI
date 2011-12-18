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
import logging
import re
import itertools
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
import umbra.ui.common
from sibl_gui.libraries.freeImage.freeImage import Image
from sibl_gui.globals.uiConstants import UiConstants
from sibl_gui.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.constants import Constants

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
			"getDisplayItem",
			"getIcon",
			"getPixmap",
			"getImage",
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
@core.memoize(RuntimeGlobals.imagesCache)
def getDisplayItem(path, type):
		"""
		This method gets a display item: `QIcon <http://doc.qt.nokia.com/4.7/qicon.html>`_,
		`QImage <http://doc.qt.nokia.com/4.7/qimage.html>`_, `QPixmap <http://doc.qt.nokia.com/4.7/qpixmap.html>`_.

		:param path: Image path. ( String )
		:param type: QIcon, QImage, QPixmap. ( QObject )
		:return: Graphic display. ( Icon, QImage, QPixmap )
		"""

		if foundations.common.pathExists(path):
			for extension in UiConstants.nativeImageFormats.itervalues():
				if re.search(extension, path, flags=re.IGNORECASE):
					return type(path)
			else:
				for extension in UiConstants.thirdPartyImageFormats.itervalues():
					if re.search(extension, path, flags=re.IGNORECASE):
						image = Image(str(path))
						image = image.convertToQImage()
						if type == QIcon:
							return QIcon(QPixmap(image))
						elif type == QImage:
							return image
						elif type == QPixmap:
							return QPixmap(image)
				else:
					return type(umbra.ui.common.getResourcePath(UiConstants.formatErrorImage))
		else:
			return type(umbra.ui.common.getResourcePath(UiConstants.missingImage))

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getIcon(path):
		"""
		This method gets a `QIcon <http://doc.qt.nokia.com/4.7/qicon.html>`_.

		:param path: Icon image path. ( String )
		:return: QIcon. ( QIcon )
		"""

		return getDisplayItem(path, QIcon)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getPixmap(path):
		"""
		This method gets a `QPixmap <http://doc.qt.nokia.com/4.7/qpixmap.html>`_.

		:param path: Icon image path. ( String )
		:return: QPixmap. ( QPixmap )
		"""

		return getDisplayItem(path, QPixmap)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getImage(path):
		"""
		This method gets a `QImage <http://doc.qt.nokia.com/4.7/qimage.html>`_.

		:param path: Icon image path. ( String )
		:return: QImage. ( QImage )
		"""

		return getDisplayItem(path, QImage)

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
