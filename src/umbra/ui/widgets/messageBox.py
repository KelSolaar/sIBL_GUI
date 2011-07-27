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
**messageBox.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Message box Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

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
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
def messageBox(type, title, message, icon=None, buttons=QMessageBox.Ok):
	"""
	This definition provides a fast gui message box.

	@param title: Current message title. ( String )
	@param message: Message. ( String )
	@param icon: Custom icon. ( QConstant )
	@param buttons: Custom buttons. ( QConstant )
	@return: User choice. ( Integer )
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
	elif type == "Detailed error":
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

	@param type: MessageBox type. ( String )
	@param caption: MessageBox title. ( String )
	@param message: MessageBox message. ( String )
	@param icon: Custom icon. ( QConstant )
	@param buttons: Custom buttons. ( QConstant )
	"""

	application = QApplication(sys.argv)
	messageBox(type, caption, message, icon, buttons)

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
