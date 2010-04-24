#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2010 - Thomas Mansencal - kelsolaar_fool@hotmail.com
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
# Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	active_QLabel.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Custom Active QLabel.
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
import foundations.exceptions
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Active_QLabel( QLabel ):
	'''
	This Class Is The Active_QLabel Class.
	'''

	@core.executionTrace
	def __init__( self, defaultPixmap, hoverPixmap, activePixmap, parent = None ) :
		'''
		This Method Initializes The Class.

		@param defaultPixmap: Label Default Pixmap. ( QPixmap )
		@param hoverPixmap: Label Hover Pixmap. ( QPixmap )
		@param activePixmap: Label Active Pixmap. ( QPixmap )
		@param parent: Widget Parent. ( QObject )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		QLabel.__init__( self, parent )

		# --- Setting Class Attributes. ---
		self._defaultPixmap = defaultPixmap
		self._hoverPixmap = hoverPixmap
		self._activePixmap = activePixmap
		self._activated = None

		self.setPixmap( self._defaultPixmap )

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def defaultPixmap( self ):
		'''
		This Method Is The Property For The _defaultPixmap Attribute.

		@return: self._defaultPixmap. ( QPixmap )
		'''

		return self._defaultPixmap

	@defaultPixmap.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def defaultPixmap( self, value ):
		'''
		This Method Is The Setter Method For The _defaultPixmap Attribute.

		@param value: Attribute Value. ( QPixmap )
		'''

		if value :
			assert type( value ) is bool, "'{0}' Attribute : '{1}' Type Is Not 'bool' !".format( "activated", value )
		self._defaultPixmap = value

	@defaultPixmap.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def defaultPixmap( self ):
		'''
		This Method Is The Deleter Method For The _defaultPixmap Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "defaultPixmap" ) )

	@property
	def hoverPixmap( self ):
		'''
		This Method Is The Property For The _hoverPixmap Attribute.

		@return: self._hoverPixmap. ( QPixmap )
		'''

		return self._hoverPixmap

	@hoverPixmap.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def hoverPixmap( self, value ):
		'''
		This Method Is The Setter Method For The _hoverPixmap Attribute.

		@param value: Attribute Value. ( QPixmap )
		'''

		if value :
			assert type( value ) is bool, "'{0}' Attribute : '{1}' Type Is Not 'bool' !".format( "activated", value )
		self._hoverPixmap = value

	@hoverPixmap.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def hoverPixmap( self ):
		'''
		This Method Is The Deleter Method For The _hoverPixmap Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "hoverPixmap" ) )

	@property
	def activePixmap( self ):
		'''
		This Method Is The Property For The _activePixmap Attribute.

		@return: self._activePixmap. ( QPixmap )
		'''

		return self._activePixmap

	@activePixmap.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def activePixmap( self, value ):
		'''
		This Method Is The Setter Method For The _activePixmap Attribute.

		@param value: Attribute Value. ( QPixmap )
		'''

		if value :
			assert type( value ) is bool, "'{0}' Attribute : '{1}' Type Is Not 'bool' !".format( "activated", value )
		self._activePixmap = value

	@activePixmap.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def activePixmap( self ):
		'''
		This Method Is The Deleter Method For The _activePixmap Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "activePixmap" ) )

	@property
	def activated( self ):
		'''
		This Method Is The Property For The _activated Attribute.

		@return: self._activated. ( Boolean )
		'''

		return self._activated

	@activated.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def activated( self, value ):
		'''
		This Method Is The Setter Method For The _activated Attribute.

		@param value: Attribute Value. ( Boolean )
		'''

		if value :
			assert type( value ) is bool, "'{0}' Attribute : '{1}' Type Is Not 'bool' !".format( "activated", value )
		self._activated = value

	@activated.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def activated( self ):
		'''
		This Method Is The Deleter Method For The _activated Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "activated" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate( self ):
		'''
		This Method Sets The Widget Activated State.
		'''

		self._activated = True
		self.setPixmap( self._activePixmap )

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Sets The Widget Deactivated State.
		'''
		self._activated = False
		self.setPixmap( self._defaultPixmap )

	@core.executionTrace
	def enterEvent( self, event ):
		'''
		This Method Defines The Mouse Enter Event.
		
		@param event: QEvent. ( QEvent )
		'''

		not self._activated and self.setPixmap( self._hoverPixmap )

	@core.executionTrace
	def leaveEvent( self, event ):
		'''
		This Method Defines The Mouse Leave Event.
		
		@param event: QEvent. ( QEvent )
		'''

		not self._activated and self.setPixmap( self._defaultPixmap )

	@core.executionTrace
	def mousePressEvent( self, event ):
		'''
		This Method Defines The Mouse Press Event.
		
		@param event: QEvent. ( QEvent )
		'''

		self.emit( SIGNAL( "clicked()" ) )
		self.activate()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
