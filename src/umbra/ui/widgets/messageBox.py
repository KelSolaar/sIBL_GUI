#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**messageBox.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Message box Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
from umbra.globals.runtimeConstants import RuntimeConstants
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
@core.executionTrace
def messageBox(type, title, message, icon=None, buttons=QMessageBox.Ok):
	"""
	This definition provides a fast GUI message box.

	:param title: Current message title. ( String )
	:param message: Message. ( String )
	:param icon: Custom icon. ( QConstant )
	:param buttons: Custom buttons. ( QConstant )
	:return: User choice. ( Integer )
	"""

	LOGGER.debug("> Launching messagebox().")
	LOGGER.debug("> Message type: '{0}'.".format(type))
	LOGGER.debug("> Title: '{0}'.".format(title))
	LOGGER.debug("> Message: '{0}'.".format(message))

	messageBox = QMessageBox()
	messageBox.setWindowTitle("{0} | {1}".format(Constants.applicationName, title))
	messageBox.setText(message)

	if type == "Critical":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Critical)
		LOGGER.critical("!> {0}".format(message))
	elif type == "Error":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Critical)
		LOGGER.error("!> {0}".format(message))
	elif type == "Detailed Error":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Critical)
		RuntimeConstants.loggingSessionHandlerStream and messageBox.setDetailedText("".join(RuntimeConstants.loggingSessionHandlerStream.stream))
		textEdit = messageBox.findChild(QTextEdit)
		if textEdit:
			textEdit.setCurrentFont(QFont("Courier"))
			textEdit.setLineWrapMode(QTextEdit.NoWrap)
			textEdit.moveCursor(QTextCursor.End)
			textEdit.ensureCursorVisible()
		LOGGER.error("!> {0}".format(message))
	elif type == "Warning":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Warning)
		LOGGER.warning("{0}".format(message))
	elif type == "Information":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Information)
		LOGGER.info("{0}".format(message))
	elif type == "Question":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Question)
		LOGGER.info("{0}".format(message))

	messageBox.setStandardButtons(buttons)
	messageBox.setWindowFlags(Qt.WindowStaysOnTopHint)

	return messageBox.exec_()

@core.executionTrace
def standaloneMessageBox(type, caption, message, icon=None, buttons=QMessageBox.Ok):
	"""
	This definition provides a standalone message box.

	:param type: MessageBox type. ( String )
	:param caption: MessageBox title. ( String )
	:param message: MessageBox message. ( String )
	:param icon: Custom icon. ( QConstant )
	:param buttons: Custom buttons. ( QConstant )
	"""

	application = QApplication(sys.argv)
	messageBox(type, caption, message, icon, buttons)
