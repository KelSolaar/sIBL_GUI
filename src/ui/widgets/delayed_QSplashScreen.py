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
***	delayed_QSplashScreen.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Custom Delayed QSplashScreen Module.
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.common
import foundations.exceptions
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Delayed_QSplashScreen( QSplashScreen ) :
	'''
	This Class Is The sIBL_SplashScreen Class.
	'''

	@core.executionTrace
	def __init__( self, picture, waitTime = None ) :
		'''
		This Method Initializes The Class.

		@param picture: Current Picture Path. ( String )
		@param waitTime Wait Time. ( Integer )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		QSplashScreen.__init__( self, picture )

		self.setWindowFlags( self.windowFlags() | Qt.WindowStaysOnTopHint )

		# --- Setting Class Attributes. ---
		self._waitTime = None
		self.waitTime = waitTime

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def waitTime( self ):
		'''
		This Method Is The Property For The _waitTime Attribute.

		@return: self._waitTime ( Integer / Float )
		'''

		return self._waitTime

	@waitTime.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def waitTime( self, value ):
		'''
		This Method Is The Setter Method For The _waitTime Attribute.
		
		@param value: Attribute Value. ( Integer / Float )
		'''

		if value :
			assert type( value ) in ( int, float ), "'{0}' Attribute : '{1}' Type Is Not 'int' or 'float' !".format( "waitTime", value )
			assert value > 0, "'{0}' Attribute : '{1}' Need To Be Exactly Positive !".format( "waitTime", value )
		self._waitTime = value

	@waitTime.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def waitTime( self ):
		'''
		This Method Is The Deleter Method For The _waitTime Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "waitTime" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def setMessage( self, message, waitTime = None ):
		'''
		This Method Initializes The Class.

		@param message: Message To Display On The Splashscreen. ( String )
		'''

		self.showMessage( message )

		if self._waitTime :
			waitTime = self._waitTime

		waitTime and foundations.common.wait( waitTime )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
