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
***	streamObject.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Stream Object Module.
***
***	Others:
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class StreamObject(object):
	'''
	This Class Is The StreamObject Class.
	'''

	def __init__(self, stream=None):
		'''
		This Method Initializes The Class.
		
		@param stream: Stream Object. ( Object )
		'''

		self._stream = []

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def stream(self):
		'''
		This Method Is The Property For The _stream Attribute.
		
		@return: self._stream. ( List )
		'''

		return self._stream

	@stream.setter
	def stream(self, value):
		'''
		This Method Is The Setter Method For The _stream Attribute.
		
		@param value: Attribute Value. ( List )
		'''

		if value:
			assert type(value) is list, "'{0}' Attribute : '{1}' Type Is Not 'list' !".format("stream", value)
		self._stream = value

	@stream.deleter
	def stream(self):
		'''
		This Method Is The Deleter Method For The _stream Attribute.
		'''

		raise Exception("'{0}' Attribute Is Not Deletable !".format("stream"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	def write(self, message):
		'''
		This Method Provides Write Ability To The Class.

		@param message: Current Message. ( String )
		'''

		self._stream.append(message)

	def flush(self):
		'''
		This Method Flushes The Current Stream.
		'''

		pass

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
