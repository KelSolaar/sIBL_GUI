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
***	testsComponentA.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Tests Component A Module.
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

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from globals.constants import Constants
from manager.component import Component

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class TestsComponentA(Component):
	'''
	This Class Is The TestsComponentA Class.
	'''

	@core.executionTrace
	def __init__(self, name=None):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		Component.__init__(self, name=name)

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self._container = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("container"))
	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self._container = container

		self._activate()

	@core.executionTrace
	def deactivate(self):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self._container = None

		self._deactivate()

	@core.executionTrace
	def initialize(self):
		'''
		This Method Initializes The Component.
		'''

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

	@core.executionTrace
	def uninitialize(self):
		'''
		This Method Uninitializes The Component.
		'''

		LOGGER.debug("> Uninitializing '{0}' Component.".format(self.__class__.__name__))

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
