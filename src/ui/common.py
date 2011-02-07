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
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	common.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		UI Common Module.
***
***	Others :
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
import os
import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import ui.widgets.messageBox as messageBox
from globals.constants import Constants
from globals.uiConstants import UiConstants
from globals.runtimeConstants import RuntimeConstants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@core.executionTrace
def uiExtendedExceptionHandler(exception, origin, *args, **kwargs) :
	'''
	This Definition Provides A Ui Extended Exception Handler.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	'''

	messageBox.messageBox("Error", "Exception", "Exception In '{0}' : {1}".format(origin, exception))
	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)

@core.executionTrace
def uiStandaloneExtendedExceptionHandler(exception, origin, *args, **kwargs) :
	'''
	This Definition Provides A Ui Standalone Extended Exception Handler.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	'''

	messageBox.standaloneMessageBox("Error", "Exception", "Exception In '{0}' : {1}".format(origin, exception))
	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)

@core.executionTrace
def uiBasicExceptionHandler(exception, origin, *args, **kwargs) :
	'''
	This Definition Provides A Ui Basic Exception Handler.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	'''

	messageBox.messageBox("Error", "Exception", "{0}".format(exception))
	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)

@core.executionTrace
def uiStandaloneBasicExceptionHandler(exception, origin, *args, **kwargs) :
	'''
	This Definition Provides A Ui Standalone Basic Exception Handler.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	'''

	messageBox.standaloneMessageBox("Error", "Exception", "{0}".format(exception))
	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)

@core.executionTrace
def uiSystemExitExceptionHandler(exception, origin, *args, **kwargs) :
	'''
	This Definition Provides A Ui System Exit Exception Handler.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	'''

	uiExtendedExceptionHandler(exception, origin, *args, **kwargs)
	foundations.common.exit(1, LOGGER, [ RuntimeConstants.loggingSessionHandler, RuntimeConstants.loggingFileHandler, RuntimeConstants.loggingConsoleHandler ])

@core.executionTrace
def uiStandaloneSystemExitExceptionHandler(exception, origin, *args, **kwargs) :
	'''
	This Definition Provides A Ui Standalone System Exit Exception Handler.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	'''

	uiStandaloneExtendedExceptionHandler(exception, origin, *args, **kwargs)
	foundations.common.exit(1, LOGGER, [ RuntimeConstants.loggingSessionHandler, RuntimeConstants.loggingFileHandler, RuntimeConstants.loggingConsoleHandler ])

@core.executionTrace
def setWindowDefaultIcon(window):
	'''
	This Method Sets The Application Icon To The Provided Window.

	@param window: Window. ( QWidget )	
	'''

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		window.setWindowIcon(QIcon(os.path.join(os.getcwd(), UiConstants.frameworkApplicationWindowsIcon)))
	elif platform.system() == "Darwin" :
		window.setWindowIcon(QIcon(os.path.join(os.getcwd(), UiConstants.frameworkApplicationDarwinIcon)))
	elif platform.system() == "Linux":
		pass

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
