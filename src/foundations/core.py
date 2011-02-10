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
***	core.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Core Module
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
import functools
import inspect
import logging
import sys

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
from globals.constants import Constants

#***********************************************************************************************
#***	Logging Classes And Definitions
#***********************************************************************************************
def setVerbosityLevel(verbosityLevel):
	'''
	This Definition Provides Overall Verbosity Levels Through An Integer.

	@param verbosityLevel: Verbosity Level. ( Integer )
	'''

	if verbosityLevel == 0:
		LOGGER.setLevel(logging.CRITICAL)
	elif verbosityLevel == 1:
		LOGGER.setLevel(logging.ERROR)
	elif verbosityLevel == 2:
		LOGGER.setLevel(logging.WARNING)
	elif verbosityLevel == 3:
		LOGGER.setLevel(logging.INFO)
	elif verbosityLevel == 4:
		LOGGER.setLevel(logging.DEBUG)

class StandardMessageHook(object):
	'''
	This Is The StandardMessageHook Class.
	'''

	def __init__(self, logger):
		'''
		This Method Initializes The Class.

		@param logger: LOGGER. ( Object )
		'''

		self._logger = logger

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def logger(self):
		'''
		This Method Is The Property For The _logger Attribute.

		@return: self._logger. ( Object )
		'''

		return self._logger

	@logger.setter
	def logger(self, value):
		'''
		This Method Is The Setter Method For The _logger Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		raise Exception("'{0}' Attribute Is Read Only !".format("logger"))

	@logger.deleter
	def logger(self):
		'''
		This Method Is The Deleter Method For The _logger Attribute.
		'''

		raise Exception("'{0}' Attribute Is Not Deletable !".format("logger"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	def write(self, message):
		'''
		This Method Logs The Current StdOut Message.
		
		@param message: Message. ( String )
		'''

		for handler in self._logger.__dict__["handlers"]:
			handler.stream.write(message)

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

LOGGING_FORMATTER = logging.Formatter("%(levelname)-8s : %(message)s")
LOGGING_STANDARD_FORMATTER = logging.Formatter()

IGNORED_CODE_LAYERS = ("getFrame",
					"getCodeLayerName",
					"getObjectName",
					"executionTrace",
					"wrapper"
					)

UNDEFINED_CODE_LAYER = "UndefinedCodeLayer"
UNDEFINED_OBJECT = "UndefinedObject"

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
def getFrame(index):
	'''
	This Definition Returns The Requested Frame.

	@param level: Frame Index. ( Object )
	@return: Frame. ( Frame )
	'''

	return sys._getframe(index)

def getCodeLayerName():
	'''
	This Definition Returns The Frame Code Layer Name.

	@return: Code Layer Name. ( String )
	'''

	for frameIndex in range(len(inspect.stack())):
		frame = getFrame(frameIndex)
		if frame.f_code.co_name not in IGNORED_CODE_LAYERS:
			return frame.f_code.co_name
	return UNDEFINED_CODE_LAYER

def getModule(object_):
	'''
	This Definition Returns The Frame Module Name.

	@param object_: Object. ( Object )
	@return: Frame Module. ( Module )
	'''

	return inspect.getmodule(object_)

def getObjectName(object_):
	'''
	This Definition Returns The Object Name Related To The Provided Frame.

	@param object_: Object. ( Object )
	@return: Object Name. ( String )
	'''

	moduleName = getModule(inspect.getmodule(object_)).__name__
	codeLayerName = getCodeLayerName()
	codeLayerName = codeLayerName != UNDEFINED_CODE_LAYER and codeLayerName != "<module>" and "{0}.".format(codeLayerName) or ""

	return hasattr(object_, "__name__") and "{0} | {1}{2}()".format(moduleName, codeLayerName, object_.__name__) or UNDEFINED_OBJECT

def executionTrace(object_):
	'''
	This Decorator Is Used For Function Tracing.

	@param object_: Object To Decorate. ( Object )
	@return: Object. ( Object )
	'''

	origin = getObjectName(object_)

	@functools.wraps(object_)
	def function(*args, **kwargs):
		'''
		This Decorator Is Used For Function Tracing.
		
		@param *args: Arguments. ( * )
		@param **kwargs: Arguments. ( * )
		@return: Object. ( Object )
		'''

		LOGGER and LOGGER.__dict__["handlers"] != {} and LOGGER.debug("--->>> '{0}' <<<---".format(origin))

		value = object_(*args, **kwargs)

		LOGGER and LOGGER.__dict__["handlers"] != {} and LOGGER.debug("---<<< '{0}' >>>---".format(origin))

		return value

	return function

class Structure(object):
	'''
	This Is The Structure Class.
	'''

	@executionTrace
	def __init__(self, **kwargs):
		'''
		This Method Initializes The Class.

		@param kwargs: Key / Value Pairs. ( Key / Value Pairs )
		'''

		self.__dict__.update(kwargs)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
