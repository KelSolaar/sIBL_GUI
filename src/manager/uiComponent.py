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
***	uiComponent.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Ui Component Module.
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
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import ui.common as common
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class UiComponent(QWidget):
	'''
	This Class Is The UiComponent Class.
	'''

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QWidget.__init__(self)

		# --- Setting Class Attributes. ---
		self._name = None
		self.name = name

		self._uiFile = None
		self.uiFile = uiFile

		self._activated = False
		self._deactivatable = True

		self._ui = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def name(self):
		'''
		This Method Is The Property For The _name Attribute.

		@return: self._name. ( String )
		'''

		return self._name

	@name.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def name(self, value):
		'''
		This Method Is The Setter Method For The _name Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("name", value)
		self._name = value

	@name.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def name(self):
		'''
		This Method Is The Deleter Method For The _name Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("name"))

	@property
	def activated(self):
		'''
		This Method Is The Property For The _activated Attribute.

		@return: self._activated. ( String )
		'''

		return self._activated

	@activated.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def activated(self, value):
		'''
		This Method Is The Setter Method For The _activated Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) is bool, "'{0}' Attribute : '{1}' Type Is Not 'bool' !".format("activated", value)
		self._activated = value

	@activated.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def activated(self):
		'''
		This Method Is The Deleter Method For The _activated Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("activated"))

	@property
	def deactivatable(self):
		'''
		This Method Is The Property For The _deactivatable Attribute.

		@return: self._deactivatable. ( String )
		'''

		return self._deactivatable

	@deactivatable.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def deactivatable(self, value):
		'''
		This Method Is The Setter Method For The _deactivatable Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) is bool, "'{0}' Attribute : '{1}' Type Is Not 'bool' !".format("deactivatable", value)
		self._deactivatable = value

	@deactivatable.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivatable(self):
		'''
		This Method Is The Deleter Method For The _deactivatable Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("deactivatable"))

	@property
	def uiFile(self):
		'''
		This Method Is The Property For The _uiFile Attribute.

		@return: self._uiFile. ( String )
		'''

		return self._uiFile

	@uiFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiFile(self, value):
		'''
		This Method Is The Setter Method For The _uiFile Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("uiFile", value)
			assert os.path.exists(value), "'{0}' Attribute : '{1}' ui File Doesn't Exists !".format("uiFile", value)
		self._uiFile = value

	@uiFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiFile(self):
		'''
		This Method Is The Deleter Method For The _uiFile Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiFile"))

	@property
	def ui(self):
		'''
		This Method Is The Property For The _ui Attribute.

		@return: self._ui. ( Object )
		'''

		return self._ui

	@ui.setter
	def ui(self, value):
		'''
		This Method Is The Setter Method For The _ui Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		self._ui = value

	@ui.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self):
		'''
		This Method Is The Deleter Method For The _ui Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("ui"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def _activate(self):
		'''
		This Method Sets Activation State.
		'''

		self._activated = True

		self._loadUi()

	@core.executionTrace
	def _deactivate(self):
		'''
		This Method UnSets Activation State.
		'''

		self._activated = False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(common.uiExtendedExceptionHandler, False, Exception)
	def _loadUi(self):
		'''
		This Method Loads The Ui File.
		'''

		if self._uiFile:
			self._ui = uic.loadUi(self._uiFile)
			if "." in sys.path:
				sys.path.remove(".")
			return True
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Ui File Doesn't Exists !".format(self._name)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
