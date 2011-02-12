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
***	pkzip.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Zip File Manipulation Module.
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
from cStringIO import StringIO
import logging
import os
import zipfile

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import core
import io
import foundations.exceptions
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Pkzip(object):
	'''
	This Class Provides Methods To Manipulate Zip Files.
	'''

	@core.executionTrace
	def __init__(self, archive=None):
		'''
		This Method Initializes The Class.

		@param archive: Variable To Manipulate. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self._archive = None
		self.archive = archive

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def archive(self):
		'''
		This Method Is The Property For The _archive Attribute.
		
		@return: self._archive. ( String )
		'''

		return self._archive

	@archive.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def archive(self, value):
		'''
		This Method Is The Setter Method For The _archive Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("archive", value)
			assert os.path.exists(value), "'{0}' Attribute : '{1}' File Doesn't Exists !".format("archive", value)
		self._archive = value

	@archive.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def archive(self):
		'''
		This Method Is The Deleter Method For The _archive Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("archive"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def extract(self, target):
		'''
		This Method Extracts The Archive File To The Provided Folder.
		
		@return: Extraction Success. ( Boolean )
		'''

		archive = zipfile.ZipFile(self._archive)
		content = archive.namelist()

		folders = [item for item in content if item.endswith("/")]
		files = [item for item in content if not item.endswith("/")]

		folders.sort()
		folders.reverse()

		for folder in folders:
			not os.path.isdir(os.path.join(target, folder)) and io.setLocalDirectory(os.path.join(target, folder))

		for file in files:
			LOGGER.info("{0} | Extracting '{1}' File !".format(self.__class__.__name__, file))
			with open(os.path.join(target, file), "w") as output:
				buffer = StringIO(archive.read(file))
				bufferSize = 2 ** 20
				datas = buffer.read(bufferSize)
				while datas:
					output.write(datas)
					datas = buffer.read(bufferSize)
		return True
#***********************************************************************************************
#***	Python End
#***********************************************************************************************
