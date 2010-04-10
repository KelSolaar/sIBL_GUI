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
***	loaderScriptOptions.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Loader Script Options Component Module.
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
import foundations.parser
import foundations.strings as strings
import ui.widgets.messageBox as messageBox
from foundations.parser import Parser
from globals.constants import Constants
from manager.uiComponent import UiComponent
from ui.widgets.variable_QPushButton import Variable_QPushButton

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class LoaderScriptOptions( UiComponent ):
	'''
	This Class Is The LoaderScriptOptions Class.
	'''

	@core.executionTrace
	def __init__( self, name = None, uiFile = None ):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		UiComponent.__init__( self, name = name, uiFile = uiFile )

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self._uiPath = "ui/Loader_Script_Options.ui"
		self._dockArea = 2

		self._container = None

		self._coreTemplatesOutliner = None
		self._addonsLoaderScript = None

		self._templateCommonAttributesSection = "Common Attributes"
		self._templateAdditionalAttributesSection = "Additional Attributes"
		self._templateScriptSection = "Script"
		self._optionsToolboxesHeaders = ["Value"]

		self._uiGreenColor = QColor( 128, 192, 128 )
		self._uiRedColor = QColor( 192, 128, 128 )

		self._tableWidgetRowHeight = 30
		self._tableWidgetHeaderHeight = 26

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	@core.executionTrace
	def uiPath( self ):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self, value ):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiPath" ) )

	@uiPath.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self ):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiPath" ) )

	@property
	@core.executionTrace
	def dockArea( self ):
		'''
		This Method Is The Property For The _dockArea Attribute.

		@return: self._dockArea. ( Integer )
		'''

		return self._dockArea

	@dockArea.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self, value ):
		'''
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dockArea" ) )

	@dockArea.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self ):
		'''
		This Method Is The Deleter Method For The _dockArea Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dockArea" ) )

	@property
	@core.executionTrace
	def container( self ):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self, value ):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "container" ) )

	@container.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self ):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "container" ) )

	@property
	@core.executionTrace
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self._coreTemplatesOutliner. ( Object )
		'''

		return self._coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self, value ):
		'''
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreTemplatesOutliner" ) )

	@coreTemplatesOutliner.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreTemplatesOutliner" ) )

	@property
	@core.executionTrace
	def addonsLoaderScript( self ):
		'''
		This Method Is The Property For The _addonsLoaderScript Attribute.

		@return: self._addonsLoaderScript. ( Object )
		'''

		return self._addonsLoaderScript

	@addonsLoaderScript.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def addonsLoaderScript( self, value ):
		'''
		This Method Is The Setter Method For The _addonsLoaderScript Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "addonsLoaderScript" ) )

	@addonsLoaderScript.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def addonsLoaderScript( self ):
		'''
		This Method Is The Deleter Method For The _addonsLoaderScript Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "addonsLoaderScript" ) )

	@property
	@core.executionTrace
	def templateCommonAttributesSection( self ):
		'''
		This Method Is The Property For The _templateCommonAttributesSection Attribute.

		@return: self._templateCommonAttributesSection. ( String )
		'''

		return self._templateCommonAttributesSection

	@templateCommonAttributesSection.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateCommonAttributesSection( self, value ):
		'''
		This Method Is The Setter Method For The _templateCommonAttributesSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "templateCommonAttributesSection" ) )

	@templateCommonAttributesSection.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateCommonAttributesSection( self ):
		'''
		This Method Is The Deleter Method For The _templateCommonAttributesSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "templateCommonAttributesSection" ) )

	@property
	@core.executionTrace
	def templateAdditionalAttributesSection( self ):
		'''
		This Method Is The Property For The _templateAdditionalAttributesSection Attribute.

		@return: self._templateAdditionalAttributesSection. ( String )
		'''

		return self._templateAdditionalAttributesSection

	@templateAdditionalAttributesSection.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateAdditionalAttributesSection( self, value ):
		'''
		This Method Is The Setter Method For The _templateAdditionalAttributesSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "templateAdditionalAttributesSection" ) )

	@templateAdditionalAttributesSection.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateAdditionalAttributesSection( self ):
		'''
		This Method Is The Deleter Method For The _templateAdditionalAttributesSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "templateAdditionalAttributesSection" ) )

	@property
	@core.executionTrace
	def templateScriptSection( self ):
		'''
		This Method Is The Property For The _templateScriptSection Attribute.

		@return: self._templateScriptSection. ( String )
		'''

		return self._templateScriptSection

	@templateScriptSection.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateScriptSection( self, value ):
		'''
		This Method Is The Setter Method For The _templateScriptSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "templateScriptSection" ) )

	@templateScriptSection.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateScriptSection( self ):
		'''
		This Method Is The Deleter Method For The _templateScriptSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "templateScriptSection" ) )

	@property
	@core.executionTrace
	def optionsToolboxesHeaders( self ):
		'''
		This Method Is The Property For The _optionsToolboxesHeaders Attribute.

		@return: self._optionsToolboxesHeaders. ( List )
		'''

		return self._optionsToolboxesHeaders

	@optionsToolboxesHeaders.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def optionsToolboxesHeaders( self, value ):
		'''
		This Method Is The Setter Method For The _optionsToolboxesHeaders Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "optionsToolboxesHeaders" ) )

	@optionsToolboxesHeaders.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def optionsToolboxesHeaders( self ):
		'''
		This Method Is The Deleter Method For The _optionsToolboxesHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "optionsToolboxesHeaders" ) )

	@property
	@core.executionTrace
	def uiGreenColor( self ):
		'''
		This Method Is The Property For The _uiGreenColor Attribute.

		@return: self._uiGreenColor. ( QColor )
		'''

		return self._uiGreenColor

	@uiGreenColor.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiGreenColor( self, value ):
		'''
		This Method Is The Setter Method For The _uiGreenColor Attribute.

		@param value: Attribute Value. ( QColor )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiGreenColor" ) )

	@uiGreenColor.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiGreenColor( self ):
		'''
		This Method Is The Deleter Method For The _uiGreenColor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiGreenColor" ) )

	@property
	@core.executionTrace
	def uiRedColor( self ):
		'''
		This Method Is The Property For The _uiRedColor Attribute.

		@return: self._uiRedColor. ( QColor )
		'''

		return self._uiRedColor

	@uiRedColor.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiRedColor( self, value ):
		'''
		This Method Is The Setter Method For The _uiRedColor Attribute.

		@param value: Attribute Value. ( QColor )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiRedColor" ) )

	@uiRedColor.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiRedColor( self ):
		'''
		This Method Is The Deleter Method For The _uiRedColor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiRedColor" ) )

	@property
	@core.executionTrace
	def tableWidgetRowHeight( self ):
		'''
		This Method Is The Property For The _tableWidgetRowHeight Attribute.

		@return: self._tableWidgetRowHeight. ( Integer )
		'''

		return self._tableWidgetRowHeight

	@tableWidgetRowHeight.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def tableWidgetRowHeight( self, value ):
		'''
		This Method Is The Setter Method For The _tableWidgetRowHeight Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "tableWidgetRowHeight" ) )

	@tableWidgetRowHeight.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def tableWidgetRowHeight( self ):
		'''
		This Method Is The Deleter Method For The _tableWidgetRowHeight Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "tableWidgetRowHeight" ) )

	@property
	@core.executionTrace
	def tableWidgetHeaderHeight( self ):
		'''
		This Method Is The Property For The _tableWidgetHeaderHeight Attribute.

		@return: self._tableWidgetHeaderHeight. ( Integer )
		'''

		return self._tableWidgetHeaderHeight

	@tableWidgetHeaderHeight.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def tableWidgetHeaderHeight( self, value ):
		'''
		This Method Is The Setter Method For The _tableWidgetHeaderHeight Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "tableWidgetHeaderHeight" ) )

	@tableWidgetHeaderHeight.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def tableWidgetHeaderHeight( self ):
		'''
		This Method Is The Deleter Method For The _tableWidgetHeaderHeight Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "tableWidgetHeaderHeight" ) )

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

		self._container.templatesCentricLayoutComponents.append( self.name )

		self._coreTemplatesOutliner = self._container.componentsManager.components["core.templatesOutliner"].interface
		self._addonsLoaderScript = self._container.componentsManager.components["addons.loaderScript"].interface

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug( "> Deactivating '{0}' Component.".format( self.__class__.__name__ ) )

		self._container.templatesCentricLayoutComponents.remove( self.name )

		self.uiFile = None
		self._container = None

		self._coreTemplatesOutliner = None
		self._addonsLoaderScript = None

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		# Signals / Slots.
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget.connect( self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget, SIGNAL( "itemSelectionChanged()" ), self.coreTemplatesOutlinerUi_Templates_Outliner_treeWidget_OnItemSelectionChanged )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		# Signals / Slots.
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget.disconnect( self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget, SIGNAL( "itemSelectionChanged()" ), self.coreTemplatesOutlinerUi_Templates_Outliner_treeWidget_OnItemSelectionChanged )

	@core.executionTrace
	def addWidget( self ):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug( "> Adding '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._container.addDockWidget( Qt.DockWidgetArea( self._dockArea ), self.ui )

	@core.executionTrace
	def removeWidget( self ):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug( "> Removing '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._container.removeDockWidget( self.ui )
		self.ui.setParent( None )

	@core.executionTrace
	def coreTemplatesOutlinerUi_Templates_Outliner_treeWidget_OnItemSelectionChanged( self ):
		'''
		This Method Sets Is Triggered When coreTemplatesOutlinerUi_Templates_Outliner_treeWidget Selection Has Changed.
		'''

		template = self._coreTemplatesOutliner.getSelectedTemplate()

		if template :
			templateParser = Parser( template._datas.path )
			templateParser.read() and templateParser.parse( rawSections = ( self._templateScriptSection ) )

			self.setOptionsToolBox( templateParser.sections[self._templateCommonAttributesSection], self.ui.Common_Attributes_tableWidget )
			self.setOptionsToolBox( templateParser.sections[self._templateAdditionalAttributesSection], self.ui.Additional_Attributes_tableWidget )

	@core.executionTrace
	def setOptionsToolBox( self, section, tableWidget ) :
		'''
		This Method Defines And Sets Options TableWidgets.

		@param section: Section Attributes. ( Dictionary )
		@param tableWidget: Table Widget. ( QTableWidget )
		'''

		tableWidget.hide()

		tableWidget.clear()
		tableWidget.setRowCount( len( section ) )
		tableWidget.setColumnCount( len( self._optionsToolboxesHeaders ) )
		tableWidget.horizontalHeader().setStretchLastSection( True )
		tableWidget.setHorizontalHeaderLabels( self._optionsToolboxesHeaders )
		tableWidget.horizontalHeader().hide()

		tableWidget.setMinimumHeight( len( section ) * self._tableWidgetRowHeight + self._tableWidgetHeaderHeight )

		palette = QPalette()
		palette.setColor( QPalette.Base, Qt.transparent )
		tableWidget.setPalette( palette )

		verticalHeaderLabels = []
		for row, attribute in enumerate( section.keys() ) :
			LOGGER.debug( " > Current Attribute : '%s'.", attribute )
			attributeCompound = foundations.parser.getAttributeCompound( attribute, section[attribute] )
			if attributeCompound.name :
				verticalHeaderLabels.append( attributeCompound.alias )
			else:
				verticalHeaderLabels.append( strings.getNiceName( attributeCompound.name ) )

			if attributeCompound.type == "Boolean" :
				if attributeCompound.value == "1":
					item = Variable_QPushButton( True, ( self._uiGreenColor, self._uiRedColor ), ( "True", "False" ) )
					item.setChecked( True )
					item._datas = attributeCompound
					tableWidget.setCellWidget( row, 0, item )
				else :
					item = Variable_QPushButton( False, ( self._uiGreenColor, self._uiRedColor ), ( "True", "False" ) )
					item.setChecked( False )
					item._datas = attributeCompound
					tableWidget.setCellWidget( row, 0, item )
			elif attributeCompound.type == "Float" :
				item = QDoubleSpinBox()
				item.setMinimum( 0 )
				item.setMaximum( 65535 )
				item.setValue( float ( attributeCompound.value ) )
				item._datas = attributeCompound
				tableWidget.setCellWidget( row, 0, item )
			else :
				item = QTableWidgetItem( QString( attributeCompound.value ) )
				item.setTextAlignment( Qt.AlignCenter )
				item._datas = attributeCompound
				tableWidget.setItem( row, 0, item )

		tableWidget.setVerticalHeaderLabels ( verticalHeaderLabels )
		tableWidget.show()

	@core.executionTrace
	def updateOverrideKeys( self, tableWidget ):
		'''
		This Method Updates The Loader Script Component Override Keys.
		
		@param tableWidget: Table Widget. ( QTableWidget )
		'''

		for row in range( tableWidget.rowCount() ) :
			widget = tableWidget.cellWidget( row, 0 )
			if type( widget ) is Variable_QPushButton :
				value = tableWidget.cellWidget( row, 0 ).text() == "True" and "1" or "0"
			elif type( widget ) is QDoubleSpinBox :
				value = str( tableWidget.cellWidget( row, 0 ).value() )
			else:
				value = str( tableWidget.cellWidget( row, 0 ).text() )
			widget._datas.value = value
			self._addonsLoaderScript.overrideKeys[widget._datas.name] = widget._datas

	@core.executionTrace
	def getOverrideKeys( self ):
		'''
		This Method Gets Override Keys.
		'''

		self.updateOverrideKeys( self.ui.Common_Attributes_tableWidget )
		self.updateOverrideKeys( self.ui.Additional_Attributes_tableWidget )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
