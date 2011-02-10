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
***	exceptions.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Exceptions Module.
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
import logging
import sys
import traceback

#***********************************************************************************************
#***	internal Imports
#***********************************************************************************************
import core
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
def exceptionsHandler(handler=None, raise_=False, *args):
	'''
	This Decorator Is Used For Exceptions Handling.

	@param handler: Custom Handler. ( Object )
	@param raise_: Is Default Exception Handler Catching / Raising The Exception. ( Boolean )
	@param *args: Exceptions. ( Exceptions )
	@return: Object. ( Object )
	'''

	exceptions = tuple([exception for exception in args])
	handler = handler or defaultExceptionsHandler

	def wrapper(object_):
		'''
		This Decorator Is Used For Exceptions Handling.
	
		@param object_: Object To Decorate. ( Object )
		@return: Object. ( Object )
		'''

		origin = core.getObjectName(object_)

		@functools.wraps(object_)
		def function(*args, **kwargs):
			'''
			This Decorator Is Used For Exceptions Handling.
		
			@param *args: Arguments. ( * )
			@param **kwargs: Arguments. ( * )
			'''

			exception = None

			try:
				return object_(*args, **kwargs)
			except exceptions as exception:
				handler(exception , origin, *args, **kwargs)
			except Exception as exception:
				handler(exception , origin, *args, **kwargs)
			finally:
				if raise_ and exception:
					raise exception
		return function
	return wrapper

@core.executionTrace
def defaultExceptionsHandler(exception, origin, *args, **kwargs):
	'''
	This Definition Provides An Exception Handler.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	'''

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))

	LOGGER.error("!> Exception In '{0}'.".format(origin))
	LOGGER.error("!> Exception Class : '{0}'.".format(exception.__class__.__name__))
	LOGGER.error("!> Exception Description : '{0}'.".format(exception.__doc__ and exception.__doc__.strip() or Constants.nullObject))
	LOGGER.error("!> Error Raised: '{0}'.".format(exception))

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))

	traceback_ = traceback.format_exc().splitlines()
	if len(traceback_) > 1:
		for line in traceback_:
			LOGGER.error("!> {0}".format(line))

		LOGGER.error("!> {0}".format(Constants.loggingSeparators))

class FileStructureError(Exception):
	'''	
	This Class Is Used For File Content Structure Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class AttributeStructureError(Exception):
	'''
	This Class Is Used For Errors In Attribute Structure.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class DirectoryExistsError(Exception):
	'''
	This Class Is Used For Non Existing Directory.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))


		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class FileExistsError(Exception):
	'''
	This Class Is Used For Non Existing File.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))


		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class ObjectTypeError(Exception):
	'''
	This Class Is Used For Invalid Object Type.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class ObjectExistsError(Exception):
	'''
	This Class Is Used For Non Existing Object.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class DatabaseOperationError(Exception):
	'''
	This Class Is Used For Database Operation Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class ProgrammingError(Exception):
	'''
	This Class Is Used For Programming Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class UserError(Exception):
	'''
	This Class Is Used For User Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class NetworkError(Exception):
	'''
	This Class Is Used For NetworkError Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class SocketConnectionError(Exception):
	'''
	This Class Is Used For Socket Connection Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class ComponentActivationError(Exception):
	'''
	This Class Is Used For Component Activation Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class ComponentDeactivationError(Exception):
	'''
	This Class Is Used For Component Deactivation Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class LibraryInstantiationError(Exception):
	'''
	This Class Is Used For Library Instantiation Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class LibraryInitializationError(Exception):
	'''
	This Class Is Used For Library Initialization Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)

class LibraryExecutionError(Exception):
	'''
	This Class Is Used For Library Execution Errors.
	'''

	@core.executionTrace
	def __init__(self, value):
		'''
		This Method Initializes The Class.

		@param value: Error Value Or Message. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		'''
		This Method Returns The Exception Representation.
		
		@return: Exception Representation. ( String )
		'''

		return str(self.value)
#***********************************************************************************************
#***	Python End
#***********************************************************************************************
