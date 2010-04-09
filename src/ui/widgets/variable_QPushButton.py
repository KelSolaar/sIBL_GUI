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
***	variable_QPushButton.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Custom Variable QPushButton Module.
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
class Variable_QPushButton( QPushButton ) :

	@core.executionTrace
	def __init__( self, state, colors, labels ) :
		'''
		This Method Initializes The Class.

		@param state: Current Button State. ( Boolean )
		@param colors: Button Colors. ( Tuple )
		@param labels: Button Texts. ( Tuple )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		QPushButton.__init__( self )

		# --- Setting Class Attributes. ---
		self._state = None
		self.state = state

		self._colors = None
		self.colors = colors

		self._labels = None
		self.labels = labels

		# Initializing The Button
		self.setCheckable( True )
		if self._state :
			self.setTrueState()
		else :
			self.setFalseState()

		# Variable_QPushButton Signals / Slots.
		self.connect( self, SIGNAL( "clicked()" ), self.variable_QPushButton_OnClicked )

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	@core.executionTrace
	def state( self ):
		'''
		This Method Is The Property For The _state Attribute.

		@return: self._state. ( Boolean )
		'''

		return self._state

	@state.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def state( self, value ):
		'''
		This Method Is The Setter Method For The _state Attribute.

		@param value: Attribute Value. ( Boolean )
		'''

		if value :
			assert type( value ) is bool, "'{0}' Attribute : '{1}' Type Is Not 'bool' !".format( "activated", value )
		self._state = value

	@state.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def state( self ):
		'''
		This Method Is The Deleter Method For The _state Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "state" ) )

	@property
	@core.executionTrace
	def colors( self ):
		'''
		This Method Is The Property For The _colors Attribute.

		@return: self._colors. ( Tuple )
		'''

		return self._colors

	@colors.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def colors( self, value ):
		'''
		This Method Is The Setter Method For The _colors Attribute.

		@param value: Attribute Value. ( Tuple )
		'''
		if value :
			assert type( value ) is tuple, "'{0}' Attribute : '{1}' Type Is Not 'tuple' !".format( "colors", value )
			assert len( value ) == 2, "'{0}' Attribute : '{1}' Length Should Be '2' !".format( "colors", value )
			for index in range( len( value ) ) :
				assert type( value[index] ) is QColor, "'{0}' Attribute Element '{1}' : '{2}' Type Is Not 'QColor' !".format( "colors", index, value )
		self._colors = value

	@colors.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def colors( self ):
		'''
		This Method Is The Deleter Method For The _colors Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "colors" ) )

	@property
	@core.executionTrace
	def labels( self ):
		'''
		This Method Is The Property For The _labels Attribute.

		@return: self._labels. ( Tuple )
		'''

		return self._labels

	@labels.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def labels( self, value ):
		'''
		This Method Is The Setter Method For The _labels Attribute.

		@param value: Attribute Value. ( Tuple )
		'''
		if value :
			assert type( value ) is tuple, "'{0}' Attribute : '{1}' Type Is Not 'tuple' !".format( "labels", value )
			assert len( value ) == 2, "'{0}' Attribute : '{1}' Length Should Be '2' !".format( "labels", value )
			for index in range( len( value ) ) :
				assert type( value[index] ) in ( str, unicode ), "'{0}' Attribute Element '{1}' : '{2}' Type Is Not 'str' or 'unicode' !".format( "labels", index, value )
		self._labels = value

	@labels.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def labels( self ):
		'''
		This Method Is The Deleter Method For The _labels Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "labels" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def variable_QPushButton_OnClicked( self ) :
		'''
		This Method Is Called When A Variable QPushButton Is Clicked.
		'''

		if self._state :
			self.setFalseState()
		else :
			self.setTrueState()

	@core.executionTrace
	def setTrueState( self ) :
		'''
		This Method Sets The Variable Button True State.
		'''

		LOGGER.debug( "> Setting Variable QPushButton() To 'True' State." )
		self._state = True

		palette = QPalette()
		palette.setColor( QPalette.Button, self._colors[0] )
		self.setPalette( palette )

		self.setChecked( True )
		self.setText( self._labels[0] )

	@core.executionTrace
	def setFalseState( self ) :
		'''
		This Method Sets The Variable QPushButton True State.
		'''

		LOGGER.debug( "> Setting Variable QPushButton() To 'False' State." )

		self._state = False

		palette = QPalette()
		palette.setColor( QPalette.Button, self._colors[1] )
		self.setPalette( palette )

		self.setChecked( False )
		self.setText( self._labels[1] )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
