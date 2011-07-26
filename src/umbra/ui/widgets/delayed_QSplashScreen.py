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
**delayed_QSplashScreen.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Custom Delayed QSplashScreen Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.common
import foundations.exceptions
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Delayed_QSplashScreen(QSplashScreen):
	"""
	This Class Is The sIBL_SplashScreen Class.
	"""

	@core.executionTrace
	def __init__(self, picture, waitTime=None):
		"""
		This Method Initializes The Class.

		@param picture: Current Picture Path. ( String )
		@param waitTime Wait Time. ( Integer )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QSplashScreen.__init__(self, picture)

		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

		# --- Setting class attributes. ---
		self.__waitTime = None
		self.waitTime = waitTime

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def waitTime(self):
		"""
		This Method Is The Property For The _waitTime Attribute.

		@return: self.__waitTime ( Integer / Float )
		"""

		return self.__waitTime

	@waitTime.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def waitTime(self, value):
		"""
		This Method Is The Setter Method For The _waitTime Attribute.
		
		@param value: Attribute Value. ( Integer / Float )
		"""

		if value:
			assert type(value) in (int, float), "'{0}' Attribute: '{1}' Type Is Not 'int' or 'float'!".format("waitTime", value)
			assert value > 0, "'{0}' Attribute: '{1}' Need To Be Exactly Positive!".format("waitTime", value)
		self.__waitTime = value

	@waitTime.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def waitTime(self):
		"""
		This Method Is The Deleter Method For The _waitTime Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("waitTime"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def setMessage(self, message, textAlignement=Qt.AlignLeft, textColor=Qt.black, waitTime=None):
		"""
		This Method Initializes The Class.

		@param message: Message To Display On The Splashscreen. ( String )
		@param textAlignement: Text Message Alignment. ( Object )
		@param textColor: Text Message Color. ( Object )
		@param waitTime: Wait Time. ( Float )
		"""

		self.showMessage(message, textAlignement, textColor)

		# Force QSplashscreen refresh.
		QApplication.processEvents()

		if self.__waitTime:
			waitTime = self.__waitTime

		waitTime and foundations.common.wait(waitTime)

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
