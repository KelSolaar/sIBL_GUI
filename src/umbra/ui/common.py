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
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	UI common Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import platform
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import umbra.ui.widgets.messageBox as messageBox
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants
from umbra.globals.runtimeConstants import RuntimeConstants
from umbra.libraries.freeImage.freeImage import Image

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Icon(core.Structure):
	"""
	This is the Icon class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		@param kwargs: path ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__dict__.update(kwargs)

@core.executionTrace
def uiExtendedExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui extended exception handler.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed error", "Exception", "Exception in '{0}': {1}".format(origin, exception))

@core.executionTrace
def uiStandaloneExtendedExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui standalone extended exception handler.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.standaloneMessageBox("Detailed error", "Exception", "Exception in '{0}': {1}".format(origin, exception))

@core.executionTrace
def uiBasicExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui basic exception handler.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed error", "Exception", "{0}".format(exception))

@core.executionTrace
def uiStandaloneBasicExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui standalone basic exception handler.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.standaloneMessageBox("Detailed error", "Exception", "{0}".format(exception))

@core.executionTrace
def uiSystemExitExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui system exit exception handler.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	"""

	uiExtendedExceptionHandler(exception, origin, *args, **kwargs)
	foundations.common.exit(1, LOGGER, [RuntimeConstants.loggingSessionHandler, RuntimeConstants.loggingFileHandler, RuntimeConstants.loggingConsoleHandler])

@core.executionTrace
def uiStandaloneSystemExitExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui standalone system exit exception handler.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	"""

	uiStandaloneExtendedExceptionHandler(exception, origin, *args, **kwargs)
	foundations.common.exit(1, LOGGER, [RuntimeConstants.loggingSessionHandler, RuntimeConstants.loggingFileHandler, RuntimeConstants.loggingConsoleHandler])

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def setWindowDefaultIcon(window):
	"""
	This method sets the Application icon to the provided window.

	@param window: Window. ( QWidget )
	@return: Definition success. ( Boolean )
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		window.setWindowIcon(QIcon(os.path.join(os.getcwd(), UiConstants.frameworkApplicationWindowsIcon)))
	elif platform.system() == "Darwin":
		window.setWindowIcon(QIcon(os.path.join(os.getcwd(), UiConstants.frameworkApplicationDarwinIcon)))
	elif platform.system() == "Linux":
		pass
	return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def centerWidgetOnScreen(widget, screen=None):
	"""
	This definition centers the provided Widget middle of the screen.

	@param widget: Current Widget. ( QWidget )
	@param screen: Screen used for centering. ( Integer )
	@return: Definition success. ( Boolean )
	"""

	screen = screen and screen or QApplication.desktop().primaryScreen()
	desktopWidth = QApplication.desktop().screenGeometry(screen).width()
	desktopHeight = QApplication.desktop().screenGeometry(screen).height()
	widget.move(desktopWidth / 2 - widget.width() / 2, desktopHeight / 2 - widget.height() / 2)
	return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getGraphicItem(path, type):
		"""
		This method gets a graphic display: QIcon, QImage, QPixmap.

		@param path: Image path. ( String )
		@param type: QIcon, QImage, QPixmap. ( QObject )
		@return: Graphic display. ( Icon, QImage, QPixmap )
		"""

		if os.path.exists(path):
			for extension in UiConstants.nativeImageFormats.values():
				if re.search(extension, path):
					return type(path)
			else:
				for extension in UiConstants.thirdPartyImageFormats.values():
					if re.search(extension, path):
						image = Image(str(path))
						image = image.convertToQImage()
						if type == QIcon:
							return QIcon(QPixmap(image))
						elif type == QImage:
							return image
						elif type == QPixmap:
							return QPixmap(image)
				else:
					return type(UiConstants.frameworkFormatErrorImage)
		else:
			return type(UiConstants.frameworkMissingImage)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getIcon(path):
		"""
		This method gets a QIcon.

		@param path: Icon image path. ( String )
		@return: QIcon. ( QIcon )
		"""

		return getGraphicItem(path, QIcon)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getPixmap(path):
		"""
		This method gets a QPixmap.

		@param path: Icon image path. ( String )
		@return: QPixmap. ( QPixmap )
		"""

		return getGraphicItem(path, QPixmap)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getImage(path):
		"""
		This method gets a QImage.

		@param path: Icon image path. ( String )
		@return: QImage. ( QImage )
		"""

		return getGraphicItem(path, QImage)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def filterImagePath(path):
		"""
		This method filters the image path.

		@param path: Image path. ( String )
		@return: Path. ( String )
		"""

		if os.path.exists(path):
			for extension in UiConstants.nativeImageFormats.values():
				if re.search(extension, path):
					return path
			else:
				for extension in UiConstants.thirdPartyImageFormats.values():
					if re.search(extension, path):
						return UiConstants.frameworkFormatErrorImage
		else:
			return UiConstants.frameworkMissingImage

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
