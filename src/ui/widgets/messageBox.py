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

'''
************************************************************************************************
***	messageBox.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Message Box Module.
***
***	Others:
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@core.executionTrace
def messageBox(type, title, message, icon=None, buttons=QMessageBox.Ok):
	'''
	This Definition Provides A Fast GUI Message Box.

	@param title: Current Message Title. ( String )
	@param message:	Message. ( String )
	@param icon: Custom Icon. ( QConstant )
	@param buttons: Custom Buttons. ( QConstant )
	@return: User Choice. ( Integer )
	'''

	LOGGER.debug("> Launching sIBL_message().")
	LOGGER.debug("> Message Type : '{0}'.".format(type))
	LOGGER.debug("> Title : '{0}'.".format(title))
	LOGGER.debug("> Message : '{0}'.".format(message))

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
	'''
	This Definition Provides A Standalone Message Box.
	
	@param type: MessageBox Type. ( String )
	@param caption: MessageBox Title. ( String )
	@param message: MessageBox Message. ( String )	
	@param icon: Custom Icon. ( QConstant )
	@param buttons: Custom Buttons. ( QConstant )
	'''

	application = QApplication(sys.argv)
	messageBox(type, caption, message, icon, buttons)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
