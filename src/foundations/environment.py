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
***	environment.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Environment Module.
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
import os
import re

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import core
import foundations.exceptions
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Environment(object):
	'''
	This Class Provides Methods To Manipulate Environment Variables.
	'''

	@core.executionTrace
	def __init__(self, variable=None):
		'''
		This Method Initializes The Class.

		@param variable: Variable To Manipulate. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self._variable = None
		self.variable = variable

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def variable(self):
		'''
		This Method Is The Property For The _variable Attribute.
		
		@return: self._variable. ( String )
		'''

		return self._variable

	@variable.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def variable(self, value):
		'''
		This Method Is The Setter Method For The _variable Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("variable", value)
			assert not re.search("\W", value), "'{0}' Attribute : '{1}' Contains Non AlphaNumerics Characters !".format("variable", value)
		self._variable = value

	@variable.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def variable(self):
		'''
		This Method Is The Deleter Method For The _variable Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("variable"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def getPath(self):
		'''
		This Method Gets The Chosen Environment Variable Path As A String.

		@return: Variable Path. ( String )
		'''

		if self._variable:
			LOGGER.debug("> Current Environment Variable : '{0}'.".format(self._variable))
			LOGGER.debug("> Available System Environment Variables : '{0}'".format(os.environ.keys()))

			if self._variable in os.environ.keys():
				return os.environ[self._variable]

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
