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
# If You Are A HDRI Resources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**loggingNotifier.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Logging Notifier Component Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from manager.component import Component
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class LoggingNotifier(Component):
	"""
	This Class Is The LoggingNotifier Class.
	"""

	@core.executionTrace
	def __init__(self, name=None):
		"""
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		Component.__init__(self, name=name)

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self.__container = None

		self.__memoryHandlerStackDepth = 0

	#***********************************************************************************************
	#***	Attributes Properties
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def memoryHandlerStackDepth(self):
		"""
		This Method Is The Property For The _memoryHandlerStackDepth Attribute.

		@return: self.__memoryHandlerStackDepth. ( Integer )
		"""

		return self.__memoryHandlerStackDepth

	@memoryHandlerStackDepth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self, value):
		"""
		This Method Is The Setter Method For The _memoryHandlerStackDepth Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("memoryHandlerStackDepth"))

	@memoryHandlerStackDepth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self):
		"""
		This Method Is The Deleter Method For The _memoryHandlerStackDepth Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("memoryHandlerStackDepth"))

	#***********************************************************************************************
	#***	Class Methods
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__container = container

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__container = None

		self._deactivate()

	@core.executionTrace
	def initialize(self):
		"""
		This Method Initializes The Component.
		"""

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

		# Signals / Slots.
		self.__container.timer.timeout.connect(self.__statusBar_showLoggingMessages)

	@core.executionTrace
	def uninitialize(self):
		"""
		This Method Uninitializes The Component.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component.".format(self.__class__.__name__))

		# Signals / Slots.
		self.__container.timer.timeout.disconnect(self.__statusBar_showLoggingMessages)

	# @core.executionTrace
	def __statusBar_showLoggingMessages(self):
		"""
		This Method Updates The Container Status Bar With Logging Messages.
		"""

		memoryHandlerStackDepth = len(self.__container.loggingSessionHandlerStream.stream)

		if memoryHandlerStackDepth != self.__memoryHandlerStackDepth:
			for index in range(self.__memoryHandlerStackDepth, memoryHandlerStackDepth):
				self.__container.statusBar.showMessage(self.__container.loggingSessionHandlerStream.stream[index])
			self.__memoryHandlerStackDepth = memoryHandlerStackDepth

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
