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
***	rawEditingUtilities.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Raw Editing Utilities Component Module.
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
import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import ui.widgets.messageBox as messageBox
from foundations.environment import Environment
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class RawEditingUtilities( UiComponent ):
	'''
	This Class Is The LocationsBrowser Class.
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

		self._uiPath = "ui/Raw_Editing_Utilities.ui"

		self._container = None
		self._signalsSlotsCenter = None
		self._settings = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None
		self._coreTemplatesOutliner = None

		self._editSetInTextEditorAction = None
		self._editTemplateInTextEditorAction = None

		self._linuxTextEditors = ( "gedit", "kwrite", "nedit", "mousepad" )

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
	def signalsSlotsCenter( self ):
		'''
		This Method Is The Property For The _signalsSlotsCenter Attribute.

		@return: self._signalsSlotsCenter. ( QObject )
		'''

		return self._signalsSlotsCenter

	@signalsSlotsCenter.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def signalsSlotsCenter( self, value ):
		'''
		This Method Is The Setter Method For The _signalsSlotsCenter Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "signalsSlotsCenter" ) )

	@signalsSlotsCenter.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def signalsSlotsCenter( self ):
		'''
		This Method Is The Deleter Method For The _signalsSlotsCenter Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "signalsSlotsCenter" ) )

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

	@property
	def corePreferencesManager( self ):
		'''
		This Method Is The Property For The _corePreferencesManager Attribute.

		@return: self._corePreferencesManager. ( Object )
		'''

		return self._corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def corePreferencesManager( self, value ):
		'''
		This Method Is The Setter Method For The _corePreferencesManager Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "corePreferencesManager" ) )

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def corePreferencesManager( self ):
		'''
		This Method Is The Deleter Method For The _corePreferencesManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "corePreferencesManager" ) )

	@property
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self, value ):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDatabaseBrowser" ) )

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDatabaseBrowser" ) )

	@property
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self._coreTemplatesOutliner. ( Object )
		'''

		return self._coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self, value ):
		'''
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreTemplatesOutliner" ) )

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreTemplatesOutliner" ) )

	@property
	def editSetInTextEditorAction( self ):
		'''
		This Method Is The Property For The _editSetInTextEditorAction Attribute.

		@return: self._editSetInTextEditorAction. ( QAction )
		'''

		return self._editSetInTextEditorAction

	@editSetInTextEditorAction.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def editSetInTextEditorAction( self, value ):
		'''
		This Method Is The Setter Method For The _editSetInTextEditorAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "editSetInTextEditorAction" ) )

	@editSetInTextEditorAction.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def editSetInTextEditorAction( self ):
		'''
		This Method Is The Deleter Method For The _editSetInTextEditorAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "editSetInTextEditorAction" ) )

	@property
	def editTemplateInTextEditorAction( self ):
		'''
		This Method Is The Property For The _editTemplateInTextEditorAction Attribute.

		@return: self._editTemplateInTextEditorAction. ( QAction )
		'''

		return self._editTemplateInTextEditorAction

	@editTemplateInTextEditorAction.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def editTemplateInTextEditorAction( self, value ):
		'''
		This Method Is The Setter Method For The _editTemplateInTextEditorAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "editTemplateInTextEditorAction" ) )

	@editTemplateInTextEditorAction.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def editTemplateInTextEditorAction( self ):
		'''
		This Method Is The Deleter Method For The _editTemplateInTextEditorAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "editTemplateInTextEditorAction" ) )

	@property
	def linuxTextEditors( self ):
		'''
		This Method Is The Property For The _linuxTextEditors Attribute.

		@return: self._linuxTextEditors. ( Tuple )
		'''

		return self._linuxTextEditors

	@linuxTextEditors.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def linuxTextEditors( self, value ):
		'''
		This Method Is The Setter Method For The _linuxTextEditors Attribute.

		@param value: Attribute Value. ( Tuple )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "linuxTextEditors" ) )

	@linuxTextEditors.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def linuxTextEditors( self ):
		'''
		This Method Is The Deleter Method For The _linuxTextEditors Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "linuxTextEditors" ) )

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
		self._signalsSlotsCenter = QObject()
		self._settings = self._container.settings

		self._corePreferencesManager = self._container.componentsManager.components["core.preferencesManager"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface
		self._coreTemplatesOutliner = self._container.componentsManager.components["core.templatesOutliner"].interface

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug( "> Deactivating '{0}' Component.".format( self.__class__.__name__ ) )

		self.uiFile = None
		self._container = None
		self._signalsSlotsCenter = None
		self._settings = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None
		self._coreTemplatesOutliner = None

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self.Custom_Text_Editor_Path_lineEdit_setUi()

		self.addActions_()

		# Signals / Slots.
		self._signalsSlotsCenter.connect( self.ui.Custom_Text_Editor_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_Text_Editor_Path_toolButton_OnClicked )
		self._signalsSlotsCenter.connect( self.ui.Custom_Text_Editor_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_Text_Editor_Path_lineEdit_OnEditFinished )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		# Signals / Slots.
		self._signalsSlotsCenter.disconnect( self.ui.Custom_Text_Editor_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_Text_Editor_Path_toolButton_OnClicked )
		self._signalsSlotsCenter.disconnect( self.ui.Custom_Text_Editor_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_Text_Editor_Path_lineEdit_OnEditFinished )

		self.removeActions_()

	@core.executionTrace
	def addWidget( self ):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug( "> Adding '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget( self.ui.Custom_Text_Editor_Path_groupBox )

	@core.executionTrace
	def removeWidget( self ):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug( "> Removing '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._corePreferencesManager.ui.findChild( QGridLayout, "Others_Preferences_gridLayout" ).removeWidget( self.ui )
		self.ui.Custom_Text_Editor_Path_groupBox.setParent( None )

	@core.executionTrace
	def addActions_( self ):
		'''
		This Method Adds Actions.
		'''

		self._editSetInTextEditorAction = QAction( "Edit In Text Editor ...", self._coreDatabaseBrowser.ui.Database_Browser_listWidget )
		self._editSetInTextEditorAction.triggered.connect( self.Database_Browser_listWidget_editSetInTextEditorAction )
		self._coreDatabaseBrowser.ui.Database_Browser_listWidget.addAction( self._editSetInTextEditorAction )

		# TODO: self._editTemplateInTextEditorAction = QAction( "Edit In Text Editor ...", self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget )
		# TODO: self._editTemplateInTextEditorAction.triggered.connect( self.Templates_Outliner_treeWidget_editSetInTextEditorAction )
		# TODO: self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget.addAction( self._editTemplateInTextEditorAction )

	@core.executionTrace
	def removeActions_( self ):
		'''
		This Method Removes Actions.
		'''

		self._coreDatabaseBrowser.ui.Database_Browser_listWidget.removeAction( self._editSetInTextEditorAction )
		# TODO: self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget.removeAction( self._editTemplateInTextEditorAction )

		self._editSetInTextEditorAction = None
		self._editTemplateInTextEditorAction = None

	@core.executionTrace
	def Database_Browser_listWidget_editSetInTextEditorAction( self, checked ):
		'''
		This Method Is Triggered By editSetInTextEditorAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedSets = self._coreDatabaseBrowser.ui.Database_Browser_listWidget.selectedItems()
		for set in selectedSets:
			set._datas.path and os.path.exists( set._datas.path ) and self.editProvidedfile( set._datas.path )

	@core.executionTrace
	def Templates_Outliner_treeWidget_editSetInTextEditorAction( self, checked ):
		'''
		This Method Is Triggered By editTemplateInTextEditorAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedTemplates = self._coreTemplatesOutliner.getSelectedTemplates()
		if selectedTemplates :
			for template in selectedTemplates :
				os.path.exists( template._datas.path ) and self.editProvidedfile( template._datas.path )

	@core.executionTrace
	def Custom_Text_Editor_Path_lineEdit_setUi( self ) :
		'''
		This Method Fills The Custom_Text_Editor_Path_lineEdit.
		'''

		customTextEditor = self._settings.getKey( "Others", "CustomTextEditor" )
		LOGGER.debug( "> Setting '{0}' With Value '{1}'.".format( "Custom_Text_Editor_Path_lineEdit", customTextEditor.toString() ) )
		self.ui.Custom_Text_Editor_Path_lineEdit.setText( customTextEditor.toString() )

	@core.executionTrace
	def Custom_Text_Editor_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Custom_Text_Editor_Path_toolButton Is Clicked.
		'''

		customTextEditorExecutable = self._container.storeLastBrowsedPath( QFileDialog.getOpenFileName( self, "Custom Text Editor Executable :", self._container.lastBrowsedPath ) )
		if customTextEditorExecutable != "":
			LOGGER.debug( "> Chosen Custom Text Editor Executable : '{0}'.".format( customTextEditorExecutable ) )
			self.ui.Custom_Text_Editor_Path_lineEdit.setText( QString( customTextEditorExecutable ) )
			self._settings.setKey( "Others", "CustomTextEditor", self.ui.Custom_Text_Editor_Path_lineEdit.text() )

	@core.executionTrace
	def Custom_Text_Editor_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When Custom_Text_Editor_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.ui.Custom_Text_Editor_Path_lineEdit.text() ) ) ) and str( self.ui.Custom_Text_Editor_Path_lineEdit.text() ) != "":
			LOGGER.debug( "> Restoring Preferences !" )
			self.Custom_Text_Editor_Path_lineEdit_setUi()

			messageBox.messageBox( "Error", "Error", "{0} | Invalid Custom Text Editor Executable File !".format( self.__class__.__name__ ) )
		else :
			self._settings.setKey( "Others", "CustomTextEditor", self.ui.Custom_Text_Editor_Path_lineEdit.text() )

	@core.executionTrace
	def editProvidedfile( self, file ):
		'''
		This Method Provides Editing Capability.

		@param file: File To Edit. ( String )
		'''

		editCommand = None
		customTextEditor = str( self.ui.Custom_Text_Editor_Path_lineEdit.text() )

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			file = file.replace( "/", "\\" )
			if customTextEditor :
				LOGGER.info( "{0} | Launching '{1}' Custom Text Editor With '{2}'.".format( self.__class__.__name__, os.path.basename( customTextEditor ), file ) )
				editCommand = "\"{0}\" \"{1}\"".format( customTextEditor, file )
			else:
				LOGGER.info( "{0} | Launching 'notepad.exe' With '{1}'.".format( self.__class__.__name__, file ) )
				editCommand = "notepad.exe \"{0}\"".format( file )
		elif platform.system() == "Darwin" :
			if customTextEditor :
				LOGGER.info( "{0} | Launching '{1}' Custom Text Editor With '{2}'.".format( self.__class__.__name__, os.path.basename( customTextEditor ), file ) )
				editCommand = "open -a \"{0}\" \"{1}\"".format( customTextEditor, file )
			else:
				LOGGER.info( "{0} | Launching Default Text Editor With '{1}'.".format( self.__class__.__name__, file ) )
				editCommand = "open -e \"{0}\"".format( file )
		elif platform.system() == "Linux":
			if customTextEditor :
				LOGGER.info( "{0} | Launching '{1}' Custom Text Editor With '{2}'.".format( self.__class__.__name__, os.path.basename( customTextEditor ), file ) )
				editCommand = "\"{0}\" \"{1}\"".format( customTextEditor, file )
			else :
				environmentVariable = Environment( "PATH" )
				paths = environmentVariable.getPath().split( ":" )

				editorFound = False
				for editor in self._linuxTextEditors :
					if not editorFound :
						try :
							for path in paths :
								if os.path.exists( os.path.join( path, editor ) ) :
									LOGGER.info( "{0} | Launching '{1}' Text Editor With '{2}'.".format( self.__class__.__name__, editor, file ) )
									editCommand = "\"{0}\" \"{1}\"".format( editor, file )
									editorFound = True
									raise StopIteration
						except StopIteration:
							pass
					else :
						break
		if editCommand :
			LOGGER.debug( "> Current Edit Command : '{0}'.".format( editCommand ) )
			editProcess = QProcess()
			editProcess.startDetached( editCommand )
		else :
			messageBox.messageBox( "Warning", "Warning", "{0} | Please Define A Text Editor Executable In The Preferences !".format( self.__class__.__name__ ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
