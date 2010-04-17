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
***	componentsManagerUi.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Components Manager Ui Component Module.
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
import dbUtilities.common
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import ui.widgets.messageBox as messageBox
from globals.constants import Constants
from manager.uiComponent import UiComponent
from foundations.walker import Walker

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class TemplatesOutliner( UiComponent ):
	'''
	This Class Is The TemplatesOutliner Class.
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
		self.deactivatable = False

		self._uiPath = "ui/Templates_Outliner.ui"
		self._uiResources = "resources"
		self._uiSoftwareAffixe = "_Software.png"
		self._dockArea = 1

		self._container = None

		self._timer = None
		self._timerCycleMultiplier = 5

		self._coreDb = None

		self._extension = "sIBLT"

		self._defaultCollections = None
		self._factoryCollection = "Factory"
		self._userCollection = "User"

		self._treeWidgetHeaders = [ "Templates", "Release", "Software Version" ]
		self._treeWidgetIndentation = 15
		self._Template_Informations_textBrowser_defaultText = "<center><h4>* * *</h4>Select A Template To Display Related Informations !<h4>* * *</h4></center>"

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
	def uiResources( self ):
		'''
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		'''

		return self._uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self, value ):
		'''
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiResources" ) )

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self ):
		'''
		This Method Is The Deleter Method For The _uiResources Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiResources" ) )

	@property
	def uiSoftwareAffixe( self ):
		'''
		This Method Is The Property For The _uiSoftwareAffixe Attribute.

		@return: self._uiSoftwareAffixe. ( String )
		'''

		return self._uiSoftwareAffixe

	@uiSoftwareAffixe.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiSoftwareAffixe( self, value ):
		'''
		This Method Is The Setter Method For The _uiSoftwareAffixe Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiSoftwareAffixe" ) )

	@uiSoftwareAffixe.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiSoftwareAffixe( self ):
		'''
		This Method Is The Deleter Method For The _uiSoftwareAffixe Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiSoftwareAffixe" ) )

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
	def timer( self ):
		'''
		This Method Is The Property For The _timer Attribute.

		@return: self._timer. ( QTimer )
		'''

		return self._timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def timer( self, value ):
		'''
		This Method Is The Setter Method For The _timer Attribute.

		@param value: Attribute Value. ( QTimer )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "timer" ) )

	@timer.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def timer( self ):
		'''
		This Method Is The Deleter Method For The _timer Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "timer" ) )

	@property
	def timerCycleMultiplier( self ):
		'''
		This Method Is The Property For The _timerCycleMultiplier Attribute.

		@return: self._timerCycleMultiplier. ( Float )
		'''

		return self._timerCycleMultiplier

	@timerCycleMultiplier.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def timerCycleMultiplier( self, value ):
		'''
		This Method Is The Setter Method For The _timerCycleMultiplier Attribute.

		@param value: Attribute Value. ( Float )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "timerCycleMultiplier" ) )

	@timerCycleMultiplier.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def timerCycleMultiplier( self ):
		'''
		This Method Is The Deleter Method For The _timerCycleMultiplier Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "timerCycleMultiplier" ) )

	@property
	def coreDb( self ):
		'''
		This Method Is The Property For The _coreDb Attribute.

		@return: self._coreDb. ( Object )
		'''

		return self._coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self, value ):
		'''
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDb" ) )

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self ):
		'''
		This Method Is The Deleter Method For The _coreDb Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDb" ) )

	@property
	def extension( self ):
		'''
		This Method Is The Property For The _extension Attribute.

		@return: self._extension. ( String )
		'''

		return self._extension

	@extension.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def extension( self, value ):
		'''
		This Method Is The Setter Method For The _extension Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "extension" ) )

	@extension.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def extension( self ):
		'''
		This Method Is The Deleter Method For The _extension Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "extension" ) )

	@property
	def defaultCollections( self ):
		'''
		This Method Is The Property For The _defaultCollections Attribute.

		@return: self._defaultCollections. ( Dictionary )
		'''

		return self._defaultCollections

	@defaultCollections.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def defaultCollections( self, value ):
		'''
		This Method Is The Setter Method For The _defaultCollections Attribute.

		@param value: Attribute Value. ( Dictionary )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "defaultCollections" ) )

	@defaultCollections.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def defaultCollections( self ):
		'''
		This Method Is The Deleter Method For The _defaultCollections Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "defaultCollections" ) )

	@property
	def factoryCollection( self ):
		'''
		This Method Is The Property For The _factoryCollection Attribute.

		@return: self._factoryCollection. ( String )
		'''

		return self._factoryCollection

	@factoryCollection.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def factoryCollection( self, value ):
		'''
		This Method Is The Setter Method For The _factoryCollection Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "factoryCollection" ) )

	@factoryCollection.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def factoryCollection( self ):
		'''
		This Method Is The Deleter Method For The _factoryCollection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "factoryCollection" ) )

	@property
	def userCollection( self ):
		'''
		This Method Is The Property For The _userCollection Attribute.

		@return: self._userCollection. ( String )
		'''

		return self._userCollection

	@userCollection.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def userCollection( self, value ):
		'''
		This Method Is The Setter Method For The _userCollection Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "userCollection" ) )

	@userCollection.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def userCollection( self ):
		'''
		This Method Is The Deleter Method For The _userCollection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "userCollection" ) )

	@property
	def treeWidgetHeaders( self ):
		'''
		This Method Is The Property For The _treeWidgetHeaders Attribute.

		@return: self._treeWidgetHeaders. ( List )
		'''

		return self._treeWidgetHeaders

	@treeWidgetHeaders.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetHeaders( self, value ):
		'''
		This Method Is The Setter Method For The _treeWidgetHeaders Attribute.

		@param value: Attribute Value. ( List )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "treeWidgetHeaders" ) )

	@treeWidgetHeaders.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetHeaders( self ):
		'''
		This Method Is The Deleter Method For The _treeWidgetHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "treeWidgetHeaders" ) )

	@property
	def treeWidgetIndentation( self ):
		'''
		This Method Is The Property For The _treeWidgetIndentation Attribute.

		@return: self._treeWidgetIndentation. ( Integer )
		'''

		return self._treeWidgetIndentation

	@treeWidgetIndentation.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetIndentation( self, value ):
		'''
		This Method Is The Setter Method For The _treeWidgetIndentation Attribute.

		@param value: Attribute Value. ( Integer )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "treeWidgetIndentation" ) )

	@treeWidgetIndentation.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetIndentation( self ):
		'''
		This Method Is The Deleter Method For The _treeWidgetIndentation Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "treeWidgetIndentation" ) )

	@property
	def Template_Informations_textBrowser_defaultText( self ):
		'''
		This Method Is The Property For The _Template_Informations_textBrowser_defaultText Attribute.

		@return: self._Template_Informations_textBrowser_defaultText. ( String )
		'''

		return self._Template_Informations_textBrowser_defaultText

	@Template_Informations_textBrowser_defaultText.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Template_Informations_textBrowser_defaultText( self, value ):
		'''
		This Method Is The Setter Method For The _Template_Informations_textBrowser_defaultText Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "Template_Informations_textBrowser_defaultText" ) )

	@Template_Informations_textBrowser_defaultText.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Template_Informations_textBrowser_defaultText( self ):
		'''
		This Method Is The Deleter Method For The _Template_Informations_textBrowser_defaultText Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "Template_Informations_textBrowser_defaultText" ) )

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
		self._uiResources = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiResources )
		self._container = container
		self._container.templatesCentricLayoutComponents.append( self.name )

		self._coreDb = self._container.componentsManager.components["core.db"].interface

		self._defaultCollections = { self._factoryCollection : os.path.join( os.getcwd(), Constants.templatesDirectory ), self._userCollection : os.path.join( self._container.userApplicationDirectory, Constants.templatesDirectory ) }

		self.addDefaultTemplates()

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

		self.ui.Templates_Outliner_treeWidget.setContextMenuPolicy( Qt.ActionsContextMenu )
		self.Templates_Outliner_treeWidget_setActions()

		self.Templates_Outliner_treeWidget_setUi()

		self.ui.Template_Informations_textBrowser.setText( self._Template_Informations_textBrowser_defaultText )
		self.ui.Template_Informations_textBrowser.setOpenLinks( False )

		self.ui.Templates_Outliner_splitter.setSizes( [ 16777215, 1 ] )

		self._timer = QTimer( self )
		self._timer.start( Constants.defaultTimerCycle * self._timerCycleMultiplier )

		# Signals / Slots.
		self.ui.Templates_Outliner_treeWidget.connect( self.ui.Templates_Outliner_treeWidget, SIGNAL( "itemSelectionChanged()" ), self.Templates_Outliner_treeWidget_OnItemSelectionChanged )
		self.ui.Template_Informations_textBrowser.connect( self.ui.Template_Informations_textBrowser, SIGNAL( "anchorClicked( const QUrl & )" ), self.Template_Informations_textBrowser_OnAnchorClicked )
		self.connect( self._timer, SIGNAL( "timeout()" ), self.updateTemplates )

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
	def onStartup( self ):
		'''
		This Method Is Called On Framework Startup.
		'''

		erroneousTemplates = dbUtilities.common.checkTemplatesTableIntegrity( self._coreDb.dbSession )

		if erroneousTemplates :
			for template in erroneousTemplates :
				if erroneousTemplates[template] == "errorInexistingTemplateFile" :
					if messageBox.messageBox( "Question", "error", "{0} | '{1}' Template File Is Missing, Would You Like To Update It's Location ?".format( self.__class__.__name__, template.name ), QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No ) == 16384 :
						self.updateTemplateLocation( template )
				else :
					messageBox.messageBox( "Error", "Error", "{0} | '{1}' {2}".format( self.__class__.__name__, template.name, dbUtilities.common.DB_ERRORS[erroneousTemplates[template]] ) )
			self.refreshUi()

	@core.executionTrace
	def Templates_Outliner_treeWidget_setUi( self ):
		'''
		This Method Sets The Templates_Outliner_treeWidget.
		'''

		LOGGER.debug( " > Refreshing '{0}' Ui !".format( self.__class__.__name__ ) )

		self.ui.Templates_Outliner_treeWidget.clear()
		self.ui.Templates_Outliner_treeWidget.setColumnCount( len( self._treeWidgetHeaders ) )
		self.ui.Templates_Outliner_treeWidget.setHeaderLabels( QStringList( self._treeWidgetHeaders ) )
		self.ui.Templates_Outliner_treeWidget.setIndentation( self._treeWidgetIndentation )
		self.ui.Templates_Outliner_treeWidget.setSortingEnabled( True )

		collections = dbUtilities.common.filterCollections( self._coreDb.dbSession, "Templates", "type" )
		for collection in collections :
			collectionTreeWidgetItem = QTreeWidgetItem()
			collectionTreeWidgetItem.setText( 0, collection.name )

			collectionTreeWidgetItem._datas = collection

			LOGGER.debug( " > Adding '{0}' Path To 'Templates_Outliner_treeWidget'.".format( collection.name ) )
			self.ui.Templates_Outliner_treeWidget.addTopLevelItem( collectionTreeWidgetItem )

			collectionTreeWidgetItem.setExpanded( True )

			softwares = set( [ software[0] for software in self._coreDb.dbSession.query( dbUtilities.types.DbTemplate.software ).filter( dbUtilities.types.DbTemplate.collection == collection.id )] )

			for software in softwares :
				softwareTreeWidgetItem = QTreeWidgetItem( collectionTreeWidgetItem )
				softwareTreeWidgetItem.setText( 0, software )
				iconPath = os.path.join( self._uiResources, "{0}{1}".format( software, self._uiSoftwareAffixe ) )
				os.path.exists( iconPath ) and	softwareTreeWidgetItem.setIcon( 0, QIcon( iconPath ) )

				LOGGER.debug( " > Adding '{0}' Software To 'Templates_Outliner_treeWidget'.".format( software ) )
				self.ui.Templates_Outliner_treeWidget.addTopLevelItem( softwareTreeWidgetItem )

				softwareTreeWidgetItem.setExpanded( True )

				templates = set( [ template[0] for template in self._coreDb.dbSession.query( dbUtilities.types.DbTemplate.id ).filter( dbUtilities.types.DbTemplate.collection == collection.id ).filter( dbUtilities.types.DbTemplate.software == software )] )
				for template in templates :
					template = dbUtilities.common.filterTemplates( self._coreDb.dbSession, "^{0}$".format( template ), "id" )[0]
					templateTreeWidgetItem = QTreeWidgetItem( softwareTreeWidgetItem )
					templateTreeWidgetItem.setText( 0, "{0} {1}".format( template.renderer, template.title ) )

					templateTreeWidgetItem.setText( 1, template.release )
					templateTreeWidgetItem.setTextAlignment( 1, Qt.AlignCenter )

					templateTreeWidgetItem.setText( 2, template.version )
					templateTreeWidgetItem.setTextAlignment( 2, Qt.AlignCenter )

					templateTreeWidgetItem._datas = template

					LOGGER.debug( " > Adding '{0}' Template To 'Templates_Outliner_treeWidget'.".format( template.title ) )
					self.ui.Templates_Outliner_treeWidget.addTopLevelItem( templateTreeWidgetItem )

					templateTreeWidgetItem.setExpanded( True )

		for column in range( len( self._treeWidgetHeaders ) ) :
			self.ui.Templates_Outliner_treeWidget.resizeColumnToContents( column )

		self.ui.Templates_Outliner_treeWidget.sortItems( 0, Qt.AscendingOrder )

	@core.executionTrace
	def refreshUi( self ):
		'''
		This Method Refreshes The _Collections_Outliner_treeWidget.
		'''

		self.Templates_Outliner_treeWidget_setUi()

	@core.executionTrace
	def Templates_Outliner_treeWidget_setActions( self ):
		'''
		This Method Sets The Templates_Outliner_treeWidget Actions.
		'''

		addTemplateAction = QAction( "Add Template ...", self.ui.Templates_Outliner_treeWidget )
		addTemplateAction.triggered.connect( self.Components_Manager_Ui_treeWidget_addTemplateAction )
		self.ui.Templates_Outliner_treeWidget.addAction( addTemplateAction )

		removeTemplateAction = QAction( "Remove Template ...", self.ui.Templates_Outliner_treeWidget )
		removeTemplateAction.triggered.connect( self.Components_Manager_Ui_treeWidget_removeTemplateAction )
		self.ui.Templates_Outliner_treeWidget.addAction( removeTemplateAction )

		separatorAction = QAction( self.ui.Templates_Outliner_treeWidget )
		separatorAction.setSeparator( True )
		self.ui.Templates_Outliner_treeWidget.addAction( separatorAction )

		importDefaultTemplatesAction = QAction( "Import Default Templates", self.ui.Templates_Outliner_treeWidget )
		importDefaultTemplatesAction.triggered.connect( self.Components_Manager_Ui_treeWidget_importDefaultTemplatesAction )
		self.ui.Templates_Outliner_treeWidget.addAction( importDefaultTemplatesAction )

		separatorAction = QAction( self.ui.Templates_Outliner_treeWidget )
		separatorAction.setSeparator( True )
		self.ui.Templates_Outliner_treeWidget.addAction( separatorAction )

		displayHelpFileAction = QAction( "Display Help File ...", self.ui.Templates_Outliner_treeWidget )
		displayHelpFileAction.triggered.connect( self.Components_Manager_Ui_treeWidget_displayHelpFileAction )
		self.ui.Templates_Outliner_treeWidget.addAction( displayHelpFileAction )

		separatorAction = QAction( self.ui.Templates_Outliner_treeWidget )
		separatorAction.setSeparator( True )
		self.ui.Templates_Outliner_treeWidget.addAction( separatorAction )


	@core.executionTrace
	def Components_Manager_Ui_treeWidget_addTemplateAction( self, checked ):
		'''
		This Method Is Triggered By addTemplateAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.addTemplate() and self.refreshUi()

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_removeTemplateAction( self, checked ):
		'''
		This Method Is Triggered By removeTemplateAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.removeTemplate( self.getSelectedTemplate() ) and self.refreshUi()

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_importDefaultTemplatesAction( self, checked ):
		'''
		This Method Is Triggered By importDefaultTemplatesAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		for collection, path in self._defaultCollections.items() :
			os.path.exists( path ) and self.getTemplates( path, self.getCollection( collection ).id )
		self.refreshUi()

	@core.executionTrace
	def Components_Manager_Ui_treeWidget_displayHelpFileAction( self, checked ):
		'''
		This Method Is Triggered By importDefaultTemplatesAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		template = self.getSelectedTemplate()
		template and QDesktopServices.openUrl( QUrl( "file://{0}".format( template._datas.helpFile ) ) )

	@core.executionTrace
	def updateTemplates( self ):
		'''
		This Method Updates Database Templates If They Have Been Modified On Disk.
		'''

		needUiRefresh = False
		for template in dbUtilities.common.getTemplates( self._coreDb.dbSession ) :
			if template.path :
				if os.path.exists( template.path ) :
					storedStats = template.osStats.split( "," )
					osStats = os.stat( template.path )
					if str( osStats[8] ) != str( storedStats[8] ):
						LOGGER.info( "{0} | '{1}' Template File Has Been Modified And Will Be Updated !".format( self.__class__.__name__, template.name ) )
						if dbUtilities.common.updateTemplateContent( self._coreDb.dbSession, template ) :
							LOGGER.info( "{0} | '{1}' Template Has Been Updated !".format( self.__class__.__name__, template.name ) )
							needUiRefresh = True

		needUiRefresh and self.refreshUi()

	@core.executionTrace
	def Templates_Outliner_treeWidget_OnItemSelectionChanged( self ):
		'''
		This Method Sets The Template_Informations_textEdit Widget.
		'''

		content = []
		subContent = """
					<h4><center>{0}</center></h4>
					<p>
					<b>Date :</b> {1}
					<br/>
					<b>Author :</b> {2}
					<br/>
					<b>Email :</b> <a href="mailto:{3}"><span style=" text-decoration: underline; color:#000000;">{3}</span></a>
					<br/>
					<b>Url :</b> <a href="{4}"><span style=" text-decoration: underline; color:#000000;">{4}</span></a>
					<br/>
					<b>Output Script :</b> {5}
					<p>
					<b>Comment :</b> {6}
					</p>
					<p>
					<b>Help File :</b> <a href="file://{7}"><span style=" text-decoration: underline; color:#000000;">Template Manual</span></a>
					</p>
					</p>
					"""

		template = self.getSelectedTemplate()
		template and content.append( subContent.format( "{0} {1} {2}".format( template._datas.software, template._datas.renderer, template._datas.title ),
							template._datas.date,
							template._datas.author,
							template._datas.email,
							template._datas.url,
							template._datas.outputScript,
							template._datas.comment,
							template._datas.helpFile
							) )

		content or content.append( self._Template_Informations_textBrowser_defaultText )

		self.ui.Template_Informations_textBrowser.setText( "".join( content ) )

	@core.executionTrace
	def Template_Informations_textBrowser_OnAnchorClicked( self, url ):
		'''
		This Method Is Triggered When A Link Is Clicked In The Template_Informations_textBrowser Widget.

		@param url: Url To Explore. ( QUrl )
		'''

		QDesktopServices.openUrl( url )

	@core.executionTrace
	def getSelectedTemplate( self ):
		'''
		This Method Returns The Selected Template.
		
		@return: Selected Template. ( QTreeWidgetItem )
		'''

		selectedTemplate = self.ui.Templates_Outliner_treeWidget.selectedItems()
		selectedTemplate = selectedTemplate and selectedTemplate[0] or None
		return selectedTemplate and hasattr( selectedTemplate, "_datas" ) and type( selectedTemplate._datas ) == dbUtilities.types.DbTemplate and selectedTemplate or None

	@core.executionTrace
	def addTemplate( self ):
		'''
		This Method Adds A Template To The Database.
		
		@return: Addition Success. ( Boolean )
		'''

		file = self._container.storeLastBrowsedPath( ( QFileDialog.getOpenFileName( self, "Add Template :", self._container.lastBrowsedPath, "Ibls Files (*{0})".format( self._extension ) ) ) )
		if file :
			collectionId = self.defaultCollections[self._factoryCollection] in file and self.ui.Templates_Outliner_treeWidget.findItems( self._factoryCollection, Qt.MatchExactly, 0 )[0]._datas.id or self.ui.Templates_Outliner_treeWidget.findItems( self._userCollection, Qt.MatchExactly, 0 )[0]._datas.id
			LOGGER.info( "{0} | Adding '{1}' Template To Database !".format( self.__class__.__name__, os.path.basename( file ).replace( self._extension, "" ) ) )
			if dbUtilities.common.addTemplate( self._coreDb.dbSession, os.path.basename( file ).replace( self._extension, "" ), file, collectionId ) :
				return True
			else :
				messageBox.messageBox( "Error", "Error", "{0} | Exception Raised While Adding '{1}' Template To Database !".format( self.__class__.__name__, os.path.basename( file ).replace( self._extension, "" ) ) )

	@core.executionTrace
	def removeTemplate( self, template ) :
		'''
		This Method Removes Template From The Database.
		
		@return: Removal Success. ( Boolean )
		'''

		if template :
			if hasattr( template, "_datas" ) :
				if type( template._datas ) == dbUtilities.types.DbTemplate :
					if messageBox.messageBox( "Question", "Question", "Are You Sure You Want To Remove '{0}' Template ?".format( template.text( 0 ) ), buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
						return dbUtilities.common.removeTemplate( self._coreDb.dbSession, str( template._datas.id ) )
				else:
					messageBox.messageBox( "Warning", "Warning", "{0} | Cannot Remove '{1}' Collection !".format( self.__class__.__name__, template.text( 0 ) ) )
			else:
				messageBox.messageBox( "Warning", "Warning", "{0} | Cannot Remove '{1}' Software !".format( self.__class__.__name__, template.text( 0 ) ) )

	@core.executionTrace
	def updateTemplateLocation( self, template ):
		'''
		This Method Updates A Template Location.
		
		@param template: Template To Update. ( DbTemplate )
		@return: Update Success. ( Boolean )
		'''

		file = self._container.storeLastBrowsedPath( ( QFileDialog.getOpenFileName( self, "Updating '{0}' Template Location :".format( template.name ), self._container.lastBrowsedPath, "Template Files (*{0})".format( self._extension ) ) ) )
		if file :
			LOGGER.info( "{0} | Updating '{1}' Template !".format( self.__class__.__name__, os.path.basename( file ).replace( self._extension, "" ) ) )
			if not dbUtilities.common.updateTemplateLocation( self._coreDb.dbSession, template, file ) :
				messageBox.messageBox( "Error", "Error", "{0} | Exception Raised While Updating '{1}' Template !".format( self.__class__.__name__, template.name ) )
				return False
			else :
				return True

	@core.executionTrace
	def addDefaultTemplates( self ):
		'''
		This Method Adds Default Templates Collections / Templates To The Database.
		'''

		if not dbUtilities.common.getTemplates( self._coreDb.dbSession ).count():
			for collection, path in self._defaultCollections.items() :
				if os.path.exists( path ) :
					if not set( dbUtilities.common.filterCollections( self._coreDb.dbSession, "^{0}$".format( collection ), "name" ) ).intersection( dbUtilities.common.filterCollections( self._coreDb.dbSession, "Templates", "type" ) ):
						LOGGER.info( "{0} | Adding '{1}' Collection To Database !".format( self.__class__.__name__, collection ) )
						dbUtilities.common.addCollection( self._coreDb.dbSession, collection, "Templates", "Template {0} Collection".format( collection ) )
					self.getTemplates( path, self.getCollection( collection ).id )

	@core.executionTrace
	def getCollection( self, collection ):
		'''
		This Method Gets Template Collection From Provided Collection Name.
		
		@param collection: Collection Name. ( String )
		@return: Collection. ( dbCollection )
		'''

		return [collection for collection in set( dbUtilities.common.filterCollections( self._coreDb.dbSession, "^{0}$".format( collection ), "name" ) ).intersection( dbUtilities.common.filterCollections( self._coreDb.dbSession, "Templates", "type" ) )][0]

	@core.executionTrace
	def getTemplates( self, path, id ):
		'''
		This Method Imports Provided Path Templates Into Provided Collection.
		
		@param path: Templates Path. ( String )
		@param id: Collection Id. ( Integer )
		'''

		walker = Walker()
		walker.root = path
		templates = walker.walk( self._extension )
		for template in templates :
			if not dbUtilities.common.filterTemplates( self._coreDb.dbSession, "^{0}$".format( templates[template] ), "path" ) :
				LOGGER.info( "{0} | Adding '{1}' Template To Database !".format( self.__class__.__name__, template ) )
				dbUtilities.common.addTemplate( self._coreDb.dbSession, template, templates[template], id )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
