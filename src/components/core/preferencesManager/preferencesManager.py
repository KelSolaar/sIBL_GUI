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
***	preferencesManager.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Preferences Manager Component Module.
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
import os
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import ui.widgets.messageBox as messageBox
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class PreferencesManager( UiComponent ):
	'''
	This Class Is The PreferencesManager Class.
	'''

	@core.executionTrace
	def __init__( self, name=None, uiFile=None ):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		UiComponent.__init__( self, name=name, uiFile=uiFile )

		# --- Setting Class Attributes. ---
		self.deactivatable = False

		self._uiPath = "ui/Preferences_Manager.ui"
		self._dockArea = 2

		self._container = None
		self._settings = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath( self ):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self, value ):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiPath" ) )

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self ):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiPath" ) )

	@property
	def dockArea( self ):
		'''
		This Method Is The Property For The _dockArea Attribute.

		@return: self._dockArea. ( Integer )
		'''

		return self._dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self, value ):
		'''
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dockArea" ) )

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self ):
		'''
		This Method Is The Deleter Method For The _dockArea Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dockArea" ) )

	@property
	def container( self ):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self, value ):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "container" ) )

	@container.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self ):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "container" ) )

	@property
	def settings( self ):
		'''
		This Method Is The Property For The _settings Attribute.

		@return: self._settings. ( QSettings )
		'''

		return self._settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settings( self, value ):
		'''
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "settings" ) )

	@settings.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settings( self ):
		'''
		This Method Is The Deleter Method For The _settings Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "settings" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate( self, container ):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug( "> Activating '{0}' Component.".format( self.__class__.__name__ ) )

		self.uiFile = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiPath )
		self._container = container

		self._settings = self._container.settings

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Component Cannot Be Deactivated !".format( self._name ) )

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self.Verbose_Level_comboBox_OnActivated_setUi()
		self.Restore_Geometry_On_Layout_Change_checkBox_setUi()

		# Signals / Slots.
		self.ui.Verbose_Level_comboBox.activated.connect( self.Verbose_Level_comboBox_OnActivated )
		self.ui.Restore_Geometry_On_Layout_Change_checkBox.stateChanged.connect( self.Restore_Geometry_On_Layout_Change_checkBox_OnStateChanged )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Component Ui Cannot Be Uninitialized !".format( self.name ) )

	@core.executionTrace
	def addWidget( self ):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug( "> Adding '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._container.addDockWidget( Qt.DockWidgetArea( self._dockArea ), self.ui )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def removeWidget( self ):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Component Widget Cannot Be Removed !".format( self.name ) )

	@core.executionTrace
	def Verbose_Level_comboBox_OnActivated_setUi( self ) :
		'''
		This Method Fills The Verbose Level ComboBox.
		'''

		self.ui.Verbose_Level_comboBox.clear()
		LOGGER.debug( "> Available Verbose Levels : '{0}'.".format( Constants.verbosityLabels ) )
		self.ui.Verbose_Level_comboBox.insertItems( 0, QStringList ( Constants.verbosityLabels ) )
		self._container.verbosityLevel = self._settings.getKey( "Settings", "verbosityLevel" ).toInt()[0]
		self.ui.Verbose_Level_comboBox.setCurrentIndex( self._container.verbosityLevel )

	@core.executionTrace
	def Verbose_Level_comboBox_OnActivated( self, index ) :
		'''
		This Method Is Called When The Verbose Level ComboBox Is Triggered.
		
		@param index: ComboBox Activated Item Index. ( Integer )
		'''

		LOGGER.debug( "> Setting Verbose Level : '{0}'.".format( self.ui.Verbose_Level_comboBox.currentText() ) )
		self._container.verbosityLevel = int( self.ui.Verbose_Level_comboBox.currentIndex() )
		core.setVerbosityLevel( int( self.ui.Verbose_Level_comboBox.currentIndex() ) )
		self._settings.setKey( "Settings", "verbosityLevel", self.ui.Verbose_Level_comboBox.currentIndex() )

	@core.executionTrace
	def Restore_Geometry_On_Layout_Change_checkBox_setUi( self ) :
		'''
		This Method Sets The Restore_Geometry_On_Layout_Change_checkBox.
		'''

		# Adding Settings Key If It Doesn't Exists.
		self._settings.getKey( "Settings", "restoreGeometryOnLayoutChange" ).isNull() and self._settings.setKey( "Settings", "restoreGeometryOnLayoutChange", Qt.Unchecked )

		restoreGeometryOnLayoutChange = self._settings.getKey( "Settings", "restoreGeometryOnLayoutChange" )
		LOGGER.debug( "> Setting '{0}' With Value '{1}'.".format( "Restore_Geometry_On_Layout_Change_checkBox", restoreGeometryOnLayoutChange.toInt()[0] ) )
		self.ui.Restore_Geometry_On_Layout_Change_checkBox.setCheckState( restoreGeometryOnLayoutChange.toInt()[0] )

	@core.executionTrace
	def Restore_Geometry_On_Layout_Change_checkBox_OnStateChanged( self, state ) :
		'''
		This Method Is Called When Restore_Geometry_On_Layout_Change_checkBox State Changes.
		
		@param state: Checkbox State. ( Integer )
		'''

		LOGGER.debug( "> Restore Geometry On Layout Change State : '{0}'.".format( self.ui.Restore_Geometry_On_Layout_Change_checkBox.checkState() ) )
		self._settings.setKey( "Settings", "restoreGeometryOnLayoutChange", self.ui.Restore_Geometry_On_Layout_Change_checkBox.checkState() )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
