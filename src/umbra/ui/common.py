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
from foundations.parser import Parser
import umbra.ui.widgets.messageBox as messageBox
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants
from umbra.globals.runtimeConstants import RuntimeConstants
from umbra.libraries.freeImage.freeImage import Image

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
class Icon(core.Structure):
	"""
	This class represents a storage object for icon.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: path ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

@core.executionTrace
def uiExtendedExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui extended exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Arguments. ( \* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed Error", "Exception", "Exception in '{0}': {1}".format(origin, exception))

@core.executionTrace
def uiStandaloneExtendedExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui standalone extended exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Arguments. ( \* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.standaloneMessageBox("Detailed Error", "Exception", "Exception in '{0}': {1}".format(origin, exception))

@core.executionTrace
def uiBasicExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui basic exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Arguments. ( \* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed Error", "Exception", "{0}".format(exception))

@core.executionTrace
def uiStandaloneBasicExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui standalone basic exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Arguments. ( \* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.standaloneMessageBox("Detailed Error", "Exception", "{0}".format(exception))

@core.executionTrace
def uiSystemExitExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui system exit exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Arguments. ( \* )
	"""

	uiExtendedExceptionHandler(exception, origin, *args, **kwargs)
	foundations.common.exit(1, LOGGER, [RuntimeConstants.loggingSessionHandler, RuntimeConstants.loggingFileHandler, RuntimeConstants.loggingConsoleHandler])

@core.executionTrace
def uiStandaloneSystemExitExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui standalone system exit exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Arguments. ( \* )
	"""

	uiStandaloneExtendedExceptionHandler(exception, origin, *args, **kwargs)
	foundations.common.exit(1, LOGGER, [RuntimeConstants.loggingSessionHandler, RuntimeConstants.loggingFileHandler, RuntimeConstants.loggingConsoleHandler])

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def setWindowDefaultIcon(window):
	"""
	This method sets the Application icon to the provided window.

	:param window: Window. ( QWidget )
	:return: Definition success. ( Boolean )
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

	:param widget: Current Widget. ( QWidget )
	:param screen: Screen used for centering. ( Integer )
	:return: Definition success. ( Boolean )
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
		This method gets a graphic display: `QIcon <http://doc.qt.nokia.com/4.7/qicon.html>`_, `QImage <http://doc.qt.nokia.com/4.7/qimage.html>`_, `QPixmap <http://doc.qt.nokia.com/4.7/qpixmap.html>`_.

		:param path: Image path. ( String )
		:param type: QIcon, QImage, QPixmap. ( QObject )
		:return: Graphic display. ( Icon, QImage, QPixmap )
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
		This method gets a `QIcon <http://doc.qt.nokia.com/4.7/qicon.html>`_.

		:param path: Icon image path. ( String )
		:return: QIcon. ( QIcon )
		"""

		return getGraphicItem(path, QIcon)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getPixmap(path):
		"""
		This method gets a `QPixmap <http://doc.qt.nokia.com/4.7/qpixmap.html>`_.

		:param path: Icon image path. ( String )
		:return: QPixmap. ( QPixmap )
		"""

		return getGraphicItem(path, QPixmap)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getImage(path):
		"""
		This method gets a `QImage <http://doc.qt.nokia.com/4.7/qimage.html>`_.

		:param path: Icon image path. ( String )
		:return: QImage. ( QImage )
		"""

		return getGraphicItem(path, QImage)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def filterImagePath(path):
		"""
		This method filters the image path.

		:param path: Image path. ( String )
		:return: Path. ( String )
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

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, OSError)
def getTokensParser(tokensFile):
	"""
	This method returns a tokens parser.

	:param tokensFile: Tokens file. ( String )
	:return: Tokens. ( Parser )
	"""

	if not os.path.exists(tokensFile):
		raise OSError("'{0}' tokens file doesn't exists!".format(tokensFile))

	parser = Parser(tokensFile)
	parser.read() and parser.parse(orderedDictionary=False)
	return parser
