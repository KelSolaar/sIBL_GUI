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
***	collectionsOutliner.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Collections Outliner Core Component Module.
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
import dbUtilities.common
import dbUtilities.types
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
class CollectionsOutliner_QTreeView( QTreeView ):
	'''
	This Class Is The CollectionsOutliner_QTreeView Class.
	'''

	@core.executionTrace
	def __init__( self, container ):
		'''
		This Method Initializes The Class.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		QTreeView.__init__( self )

		self.setAcceptDrops( True )

		# --- Setting Class Attributes. ---
		self._container = container

		self._coreDb = self._container.componentsManager.components["core.db"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface
		self._coreCollectionsOutliner = self._container.componentsManager.components["core.collectionsOutliner"].interface

		self._previousCollection = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
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
	def coreCollectionsOutliner( self ):
		'''
		This Method Is The Property For The _coreCollectionsOutliner Attribute.

		@return: self._coreCollectionsOutliner. ( Object )
		'''

		return self._coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreCollectionsOutliner( self, value ):
		'''
		This Method Is The Setter Method For The _coreCollectionsOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreCollectionsOutliner" ) )

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreCollectionsOutliner( self ):
		'''
		This Method Is The Deleter Method For The _coreCollectionsOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreCollectionsOutliner" ) )

	@property
	def previousCollection( self ):
		'''
		This Method Is The Property For The _previousCollection Attribute.

		@return: self._previousCollection. ( String )
		'''

		return self._previousCollection

	@previousCollection.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def previousCollection( self, value ):
		'''
		This Method Is The Setter Method For The _previousCollection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "previousCollection" ) )

	@previousCollection.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def previousCollection( self ):
		'''
		This Method Is The Deleter Method For The _previousCollection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "previousCollection" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def dragEnterEvent( self, event ):
		'''
		This Method Defines The Drag Enter Event Behavior.
		
		@param event: QEvent. ( QEvent )
		'''

		if event.mimeData().hasFormat( 'application/x-qabstractitemmodeldatalist' ):
			LOGGER.debug( "> Drag Event Accepted !" )
			event.accept()
		else:
			event.ignore()

	@foundations.exceptions.exceptionsHandler( None, False, Exception )
	@core.executionTrace
	def dropEvent( self, event ):
		'''
		This Method Defines The Drop Event Behavior.
		
		@param event: QEvent. ( QEvent )		
		'''

		indexAt = self.indexAt( event.pos() )
		itemAt = self.model().itemFromIndex( indexAt )

		if itemAt :
			LOGGER.debug( "> Item At Drop Position : '{0}'.".format( itemAt ) )
			collectionStandardItem = self.model().itemFromIndex( self.model().sibling( indexAt.row(), 0, indexAt ) )
			if collectionStandardItem.text() != self._coreCollectionsOutliner._overallCollection :
				sets = self._coreDatabaseBrowser.ui.Database_Browser_listWidget.selectedItems()
				for set in sets :
					set._datas.collection = collectionStandardItem._datas.id
				if dbUtilities.common.commit( self._coreDb.dbSession ) :
					self._coreCollectionsOutliner.Collections_Outliner_treeView_refreshSetsCounts()
					self._coreCollectionsOutliner.Collections_Outliner_treeView.selectionModel().setCurrentIndex( indexAt, QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows )

	@core.executionTrace
	def QTreeView_OnClicked( self, index ):
		'''
		This Method Defines The Behavior When The Model Is Clicked.
		
		@param index: Clicked Model Item Index. ( QModelIndex )
		'''

		self._previousCollection = self.model().itemFromIndex( self.model().sibling( index.row(), 0, index ) ).text()

	@core.executionTrace
	def QTreeView_OnDoubleClicked( self, index ):
		'''
		This Method Defines The Behavior When A QStandardItem Is Double Clicked.
		
		@param index: Clicked Model Item Index. ( QModelIndex )
		'''

		collectionStandardItem = self.model().itemFromIndex( self.model().sibling( index.row(), 0, index ) )

		if collectionStandardItem.text() != self._coreCollectionsOutliner.defaultCollection and collectionStandardItem.text() != self._coreCollectionsOutliner.overallCollection :
			if self.model().itemFromIndex( index ).column() == self._coreCollectionsOutliner.modelHeaders.index( self._coreCollectionsOutliner.setsCountLabel ) :
				messageBox.messageBox( "Warning", "Warning", "{0} | 'Sets Counts' Column Is Read Only !".format( self.__class__.__name__ ) )
		else :
			messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' And '{2}' Collections Attributes Are Read Only !".format( self.__class__.__name__, self._coreCollectionsOutliner.overallCollection, self._coreCollectionsOutliner.defaultCollection ) )

class CollectionsOutliner( UiComponent ):
	'''
	This Class Is The CollectionsOutliner Class.
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

		self._uiPath = "ui/Collections_Outliner.ui"
		self._uiResources = "resources"
		self._uiDefaultCollectionIcon = "Default_Collection.png"
		self._uiUserCollectionIcon = "User_Collection.png"
		self._dockArea = 1

		self._container = None
		self._signalsSlotsCenter = None

		self._coreDb = None
		self._coreDatabaseBrowser = None

		self._model = None

		self._Collections_Outliner_treeView = None

		self._overallCollection = "Overall"
		self._defaultCollection = "Default"
		self._setsCountLabel = "Sets"
		self._modelHeaders = [ "Collections", self._setsCountLabel, "Comment" ]
		self._treeViewIndentation = 15

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
	def uiDefaultCollectionIcon( self ):
		'''
		This Method Is The Property For The _uiDefaultCollectionIcon Attribute.

		@return: self._uiDefaultCollectionIcon. ( String )
		'''

		return self._uiDefaultCollectionIcon

	@uiDefaultCollectionIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiDefaultCollectionIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiDefaultCollectionIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiDefaultCollectionIcon" ) )

	@uiDefaultCollectionIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiDefaultCollectionIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiDefaultCollectionIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiDefaultCollectionIcon" ) )

	@property
	def uiUserCollectionIcon( self ):
		'''
		This Method Is The Property For The _uiUserCollectionIcon Attribute.

		@return: self._uiUserCollectionIcon. ( String )
		'''

		return self._uiUserCollectionIcon

	@uiUserCollectionIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiUserCollectionIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiUserCollectionIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiUserCollectionIcon" ) )

	@uiUserCollectionIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiUserCollectionIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiUserCollectionIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiUserCollectionIcon" ) )

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
	def model( self ):
		'''
		This Method Is The Property For The _model Attribute.

		@return: self._model. ( QStandardItemModel )
		'''

		return self._model

	@model.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def model( self, value ):
		'''
		This Method Is The Setter Method For The _model Attribute.

		@param value: Attribute Value. ( QStandardItemModel )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "model" ) )

	@model.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def model( self ):
		'''
		This Method Is The Deleter Method For The _model Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "model" ) )

	@property
	def Collections_Outliner_treeView( self ):
		'''
		This Method Is The Property For The _Collections_Outliner_treeView Attribute.

		@return: self._Collections_Outliner_treeView. ( QTreeView )
		'''

		return self._Collections_Outliner_treeView

	@Collections_Outliner_treeView.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Collections_Outliner_treeView( self, value ):
		'''
		This Method Is The Setter Method For The _Collections_Outliner_treeView Attribute.

		@param value: Attribute Value. ( QTreeView )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "Collections_Outliner_treeView" ) )

	@Collections_Outliner_treeView.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Collections_Outliner_treeView( self ):
		'''
		This Method Is The Deleter Method For The _Collections_Outliner_treeView Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "Collections_Outliner_treeView" ) )

	@property
	def overallCollection( self ):
		'''
		This Method Is The Property For The _overallCollection Attribute.

		@return: self._overallCollection. ( String )
		'''

		return self._overallCollection

	@overallCollection.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def overallCollection( self, value ):
		'''
		This Method Is The Setter Method For The _overallCollection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "overallCollection" ) )

	@overallCollection.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def overallCollection( self ):
		'''
		This Method Is The Deleter Method For The _overallCollection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "overallCollection" ) )

	@property
	def defaultCollection( self ):
		'''
		This Method Is The Property For The _defaultCollection Attribute.

		@return: self._defaultCollection. ( String )
		'''

		return self._defaultCollection

	@defaultCollection.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def defaultCollection( self, value ):
		'''
		This Method Is The Setter Method For The _defaultCollection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "defaultCollection" ) )

	@defaultCollection.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def defaultCollection( self ):
		'''
		This Method Is The Deleter Method For The _defaultCollection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "defaultCollection" ) )

	@property
	def setsCountLabel( self ):
		'''
		This Method Is The Property For The _setsCountLabel Attribute.

		@return: self._setsCountLabel. ( String )
		'''

		return self._setsCountLabel

	@setsCountLabel.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def setsCountLabel( self, value ):
		'''
		This Method Is The Setter Method For The _setsCountLabel Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "setsCountLabel" ) )

	@setsCountLabel.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def setsCountLabel( self ):
		'''
		This Method Is The Deleter Method For The _setsCountLabel Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "setsCountLabel" ) )

	@property
	def modelHeaders( self ):
		'''
		This Method Is The Property For The _modelHeaders Attribute.

		@return: self._modelHeaders. ( List )
		'''

		return self._modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def modelHeaders( self, value ):
		'''
		This Method Is The Setter Method For The _modelHeaders Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "modelHeaders" ) )

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def modelHeaders( self ):
		'''
		This Method Is The Deleter Method For The _modelHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "modelHeaders" ) )

	@property
	def treeViewIndentation( self ):
		'''
		This Method Is The Property For The _treeViewIndentation Attribute.

		@return: self._treeViewIndentation. ( Integer )
		'''

		return self._treeViewIndentation

	@treeViewIndentation.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeViewIndentation( self, value ):
		'''
		This Method Is The Setter Method For The _treeViewIndentation Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "treeViewIndentation" ) )

	@treeViewIndentation.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeViewIndentation( self ):
		'''
		This Method Is The Deleter Method For The _treeViewIndentation Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "treeViewIndentation" ) )

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
		self._signalsSlotsCenter = QObject()

		self._coreDb = self._container.componentsManager.components["core.db"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface

		self.addDefaultCollection()

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

		self._model = QStandardItemModel()
		self.Collections_Outliner_treeView_setModel()

		self._Collections_Outliner_treeView = CollectionsOutliner_QTreeView( self._container )
		self.ui.Collections_Outliner_dockWidgetContents_gridLayout.addWidget( self._Collections_Outliner_treeView )

		self._Collections_Outliner_treeView.setContextMenuPolicy( Qt.ActionsContextMenu )
		self.Collections_Outliner_treeView_setActions()

		self.Collections_Outliner_treeView_setView()

		# Signals / Slots.
		self._signalsSlotsCenter.connect( self._Collections_Outliner_treeView.selectionModel(), SIGNAL( "selectionChanged( const QItemSelection &, const QItemSelection & )" ), self.Collections_Outliner_treeView_OnItemSelectionChanged )
		self._signalsSlotsCenter.connect( self._Collections_Outliner_treeView, SIGNAL( "clicked( const QModelIndex & )" ), self._Collections_Outliner_treeView.QTreeView_OnClicked )
		self._signalsSlotsCenter.connect( self._Collections_Outliner_treeView, SIGNAL( "doubleClicked( const QModelIndex & )" ), self._Collections_Outliner_treeView.QTreeView_OnDoubleClicked )
		self._signalsSlotsCenter.connect( self._model, SIGNAL( "modelReset()" ), self.Collections_Outliner_treeView_refreshView )
		self._signalsSlotsCenter.connect( self._model, SIGNAL( "dataChanged( const QModelIndex &, const QModelIndex &)" ), self.Collections_Outliner_treeView_OnModelDataChanged )

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
	def Collections_Outliner_treeView_setModel( self ):
		'''
		This Method Sets The Collections_Outliner_treeView Model.
		'''

		LOGGER.debug( " > Setting Up '{0}' Model !".format( "Collections_Outliner_treeView" ) )

		self._model.beginResetModel()

		self._model.clear()
		self._model.setHorizontalHeaderLabels( self._modelHeaders )
		self._model.setColumnCount( len( self._modelHeaders ) )
		readOnlyFlags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

		overallCollectionStandardItem = QStandardItem( QString( self._overallCollection ) )
		overallCollectionStandardItem.setFlags( readOnlyFlags )

		overallCollectionSetsCountStandardItem = QStandardItem( QString( str( dbUtilities.common.getSets( self._coreDb.dbSession ).count() ) ) )
		overallCollectionSetsCountStandardItem.setTextAlignment( Qt.AlignCenter )
		overallCollectionSetsCountStandardItem.setFlags( readOnlyFlags )

		overallCollectionCommentsStandardItem = QStandardItem()
		overallCollectionCommentsStandardItem.setFlags( readOnlyFlags )

		LOGGER.debug( " > Adding '{0}' Collection To '{1}'.".format( self._overallCollection, "Collections_Outliner_treeView" ) )
		self._model.appendRow( [overallCollectionStandardItem, overallCollectionSetsCountStandardItem, overallCollectionCommentsStandardItem] )

		collections = dbUtilities.common.filterCollections( self._coreDb.dbSession, "Sets", "type" )

		if collections :
			for collection in collections :
				id = collection.id
				name = collection.name
				type = collection.type
				comment = collection.comment

				collectionStandardItem = QStandardItem( QString( name ) )
				iconPath = name == self.defaultCollection and os.path.join( self._uiResources, self._uiDefaultCollectionIcon )  or os.path.join( self._uiResources, self._uiUserCollectionIcon )
				collectionStandardItem.setIcon( QIcon( iconPath ) )
				collection.name == self._defaultCollection and collectionStandardItem.setFlags( readOnlyFlags )

				collectionSetsCountStandardItem = QStandardItem( QString( str( self._coreDb.dbSession.query( dbUtilities.types.DbSet ).filter_by( collection = id ).count() ) ) )
				collectionSetsCountStandardItem.setTextAlignment( Qt.AlignCenter )
				collectionSetsCountStandardItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )

				collectionCommentsStandardItem = QStandardItem( QString( comment ) )
				collection.name == self._defaultCollection and collectionCommentsStandardItem.setFlags( readOnlyFlags )

				collectionStandardItem._datas = collection

				LOGGER.debug( " > Adding '{0}' Collection To '{1}' Model.".format( name, "Collections_Outliner_treeView" ) )
				overallCollectionStandardItem.appendRow( [collectionStandardItem, collectionSetsCountStandardItem, collectionCommentsStandardItem] )
		else :
			LOGGER.info( "{0} | Database Has No User Defined Collections !".format( self.__class__.__name__ ) )

		self._model.endResetModel()

	@core.executionTrace
	def Collections_Outliner_treeView_refreshModel( self ):
		'''
		This Method Refreshes The Collections_Outliner_treeView Model.
		'''

		LOGGER.debug( " > Refreshing '{0}' Model !".format( "Collections_Outliner_treeView" ) )

		self.Collections_Outliner_treeView_setModel()

	@core.executionTrace
	def Collections_Outliner_treeView_OnModelDataChanged( self, startIndex, endIndex ):
		'''
		This Method Defines The Behavior When The Collections_Outliner_treeView Model Data Change.
		
		@param startIndex: Edited Item Starting QModelIndex. ( QModelIndex )
		@param endIndex: Edited Item Ending QModelIndex. ( QModelIndex )
		'''

		standardItem = self._model.itemFromIndex( startIndex )
		currentText = standardItem.text()

		collectionStandardItem = self._model.itemFromIndex( self._model.sibling( startIndex.row(), 0, startIndex ) )

		identity = hasattr( collectionStandardItem, "_datas" ) and collectionStandardItem._datas.id or None
		collections = [collection for collection in dbUtilities.common.filterCollections( self._coreDb.dbSession, "Sets", "type" )]
		if identity and collections :
			if startIndex.column() == 0 :
				if currentText not in [collection.name for collection in collections]:
					LOGGER.debug( "> Updating Collection '{0}' Name To '{1}'.".format( identity, currentText ) )
					collection = dbUtilities.common.filterCollections( self._coreDb.dbSession, "^{0}$".format( identity ), "id" )[0]
					collection.name = str( currentText )
					dbUtilities.common.commit( self._coreDb.dbSession )
				else :
					messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Collection Name Already Exists In Database !".format( self.__class__.__name__, currentText ) )
			elif startIndex.column() == 2 :
				LOGGER.debug( "> Updating Collection '{0}' Comment To '{1}'.".format( identity, currentText ) )
				collection = dbUtilities.common.filterCollections( self._coreDb.dbSession, "^{0}$".format( identity ), "id" )[0]
				collection.comment = str( currentText )
				dbUtilities.common.commit( self._coreDb.dbSession )

	@core.executionTrace
	def Collections_Outliner_treeView_setView( self ):
		'''
		This Method Sets The Collections_Outliner_treeView View.
		'''

		LOGGER.debug( " > Initializing '{0}' Widget !".format( "Collections_Outliner_treeView" ) )

		self._Collections_Outliner_treeView.setAutoScroll( False )
		self._Collections_Outliner_treeView.setSelectionMode( QAbstractItemView.ExtendedSelection )
		self._Collections_Outliner_treeView.setIndentation( self._treeViewIndentation )
		self._Collections_Outliner_treeView.setSortingEnabled( True )

		self._Collections_Outliner_treeView.setModel( self._model )

		self.Collections_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def Collections_Outliner_treeView_refreshView( self ):
		'''
		This Method Refreshes The Collections_Outliner_treeView View.
		'''

		self.Collections_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def Collections_Outliner_treeView_setDefaultViewState( self ):
		'''
		This Method Sets Collections_Outliner_treeView Default View State.
		'''

		LOGGER.debug( " > Setting '{0}' Default View State !".format( "Collections_Outliner_treeView" ) )

		self._Collections_Outliner_treeView.expandAll()
		for column in range( len( self._modelHeaders ) ) :
			self._Collections_Outliner_treeView.resizeColumnToContents( column )

		self._Collections_Outliner_treeView.sortByColumn( 0, Qt.AscendingOrder )

	@core.executionTrace
	def Collections_Outliner_treeView_refreshSetsCounts( self ):
		'''
		This Method Refreshes The _Collections_Outliner_treeView Sets Counts.
		'''

		for i in range( self._model.rowCount() ) :
			for j in range( self._model.item( i ).rowCount() ):
				collectionStandardItem = self._model.item( i ).child( j, 0 )
				collectionSetsCountStandardItem = self._model.item( i ).child( j, 1 )
				if collectionStandardItem.text() == self._overallCollection :
					collectionSetsCountStandardItem.setText( str( dbUtilities.common.getSets( self._coreDb.dbSession ).count() ) )
				else :
					collectionSetsCountStandardItem.setText( str( self._coreDb.dbSession.query( dbUtilities.types.DbSet ).filter_by( collection = collectionStandardItem._datas.id ).count() ) )

	@core.executionTrace
	def Collections_Outliner_treeView_setActions( self ):
		'''
		This Method Sets The Collections Outliner Actions.
		'''

		addContentAction = QAction( "Add Content ...", self._Collections_Outliner_treeView )
		addContentAction.triggered.connect( self.Collections_Outliner_treeView_addContentAction )
		self._Collections_Outliner_treeView.addAction( addContentAction )

		addCollectionAction = QAction( "Add Collection ...", self._Collections_Outliner_treeView )
		addCollectionAction.triggered.connect( self.Collections_Outliner_treeView_addCollectionAction )
		self._Collections_Outliner_treeView.addAction( addCollectionAction )

		removeCollectionsAction = QAction( "Remove Collection(s) ...", self._Collections_Outliner_treeView )
		removeCollectionsAction.triggered.connect( self.Collections_Outliner_treeView_removeCollectionsAction )
		self._Collections_Outliner_treeView.addAction( removeCollectionsAction )

	@core.executionTrace
	def Collections_Outliner_treeView_addContentAction( self, checked ):
		'''
		This Method Is Triggered By addContentAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		collection = self.addCollection()
		if collection :
			self.Collections_Outliner_treeView_refreshModel()
			directory = self._container.storeLastBrowsedPath( ( QFileDialog.getExistingDirectory( self, "Add Directory :", self._container.lastBrowsedPath ) ) )
			if directory :
				self.coreDatabaseBrowser.addDirectory( directory, self.getCollectionId( collection ) )
				self._Collections_Outliner_treeView.selectionModel().setCurrentIndex( self._model.indexFromItem( self._model.findItems( collection, Qt.MatchExactly | Qt.MatchRecursive, 0 )[0] ), QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows )
				self.Collections_Outliner_treeView_refreshSetsCounts()

	@core.executionTrace
	def Collections_Outliner_treeView_addCollectionAction( self, checked ):
		'''
		This Method Is Triggered By addCollectionAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		collection = self.addCollection()
		if collection :
			self.Collections_Outliner_treeView_refreshModel()

	@core.executionTrace
	def Collections_Outliner_treeView_removeCollectionsAction( self, checked ):
		'''
		This Method Is Triggered By removeCollectionsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.removeCollections()
		self.Collections_Outliner_treeView_refreshModel()

	@core.executionTrace
	def Collections_Outliner_treeView_OnItemSelectionChanged( self, selectedItems, deselectedItems ):
		'''
		This Method Refreshes The Database Browser Depending On The Collections Outliner Selected Items.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		'''

		self._coreDatabaseBrowser.displaySets = self.getCollectionsSets()
		self._coreDatabaseBrowser.refreshUi()

	@core.executionTrace
	def addCollection( self ) :
		'''
		This Method Adds A Collection To The Database.
		
		@return: Addition Success. ( Boolean )
		'''

		dialogMessage = "Enter Your Collection Name !"
		collectionInformations = QInputDialog.getText( self, "Add Collection", dialogMessage )
		if collectionInformations[1] :
			collectionInformations = str( collectionInformations[0] ).split( "," )
			collection = collectionInformations[0].strip()
			comment = len( collectionInformations ) == 1 and "Double Click To Set A Comment !" or collectionInformations[1].strip()
			if not set( dbUtilities.common.filterCollections( self._coreDb.dbSession, "^{0}$".format( collection ), "name" ) ).intersection( dbUtilities.common.filterCollections( self._coreDb.dbSession, "Sets", "type" ) ):
				LOGGER.info( "{0} | Adding '{1}' Collection To Database !".format( self.__class__.__name__, collection ) )
				return dbUtilities.common.addCollection( self._coreDb.dbSession, collection, "Sets", comment ) and collection
			else :
				messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Collection Already Exists In Database !".format( self.__class__.__name__, collection ) )

	@core.executionTrace
	def addDefaultCollection( self ) :
		'''
		This Method Adds A Default Collection To The Database.
		
		@return: Addition Success. ( Boolean )
		'''

		collections = [collection for collection in dbUtilities.common.filterCollections( self._coreDb.dbSession, "Sets", "type" )]

		if not collections :
			LOGGER.info( "{0} | Adding '{1}' Collection To Database !".format( self.__class__.__name__, self._defaultCollection ) )
			return dbUtilities.common.addCollection( self._coreDb.dbSession, self._defaultCollection, "Sets", "Default Collection" ) and self._defaultCollection

	@core.executionTrace
	def removeCollections( self ) :
		'''
		This Method Removes Collections From The Database.
		
		@return: Removal Success. ( Boolean )
		'''

		selectedCollections = self.getSelectedItems()

		if self._overallCollection in [str( collection.text() ) for collection in selectedCollections] or self._defaultCollection in [str( collection.text() ) for collection in selectedCollections]:
			messageBox.messageBox( "Warning", "Warning", "{0} | Cannot Remove '{1}' Or '{2}' Collection !".format( self.__class__.__name__, self._overallCollection, self._defaultCollection ) )

		selectedCollections = [collection for collection in self.getSelectedCollections() if collection.text() != self._defaultCollection]
		if selectedCollections :
			if messageBox.messageBox( "Question", "Question", "Are You Sure You Want To Remove '{0}' Collection(s) ?".format( ", ".join( [str( collection.text() ) for collection in selectedCollections] ) ), buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
				sets = dbUtilities.common.getCollectionsSets( self._coreDb.dbSession, self.getSelectedCollectionsIds() )
				for set in sets :
					LOGGER.info( "{0} | Moving '{1}' Set To Default Collection !".format( self.__class__.__name__, set.name ) )
					set.collection = self.getCollectionId( self._defaultCollection )
				success = True
				for collection in selectedCollections :
					LOGGER.info( "{0} | Removing '{1}' Collection From Database !".format( self.__class__.__name__, collection.text() ) )
					success *= dbUtilities.common.removeCollection( self._coreDb.dbSession, str( collection._datas.id ) )
				return success

	@core.executionTrace
	def getSelectedItems( self ):
		'''
		This Method Returns The Collections_Outliner_treeView Selected Items.
		
		@return: Selected Items. ( QStringList )
		'''

		return [self._model.itemFromIndex( index ) for index in self._Collections_Outliner_treeView.selectedIndexes()]

	@core.executionTrace
	def getSelectedCollections( self ):
		'''
		This Method Gets Selected Collections.
	
		@return: Selected Collections. ( List )
		'''

		selectedCollections = [item for item in self.getSelectedItems() if hasattr( item, "_datas" ) and item.text() != self._overallCollection]
		return selectedCollections and selectedCollections or None

	@core.executionTrace
	def getSelectedCollectionsIds( self ):
		'''
		This Method Gets Selected Collections Ids.
	
		@return: Collections Ids. ( List )
		'''

		selectedCollections = self.getSelectedCollections()

		ids = []
		if selectedCollections :
			ids = [collection._datas.id for collection in selectedCollections]
			return ids == [] and ids.append( self.getCollectionId( self._defaultCollection ) ) or ids
		else :
			return ids

	@core.executionTrace
	def getCollectionId( self, collection ):
		'''
		This Method Returns The Provided Collection Id.

		@param collection: Collection To Get The Id From. ( String )
		@return: Provided Collection Id. ( Integer )
		'''

		return self._model.findItems( collection, Qt.MatchExactly | Qt.MatchRecursive, 0 )[0]._datas.id

	@core.executionTrace
	def getCollectionsSets( self ):
		'''
		This Method Gets The Sets Associated To Selected Collections.
		
		@return: Sets List. ( List )
		'''

		selectedCollections = self.getSelectedCollections()
		allIds = [collection._datas.id for collection in self._model.findItems( ".*", Qt.MatchRegExp | Qt.MatchRecursive, 0 ) if hasattr( collection, "_datas" )]
		ids = selectedCollections and ( self._overallCollection in [collection.text() for collection in selectedCollections] and allIds or self.getSelectedCollectionsIds() ) or allIds

		return dbUtilities.common.getCollectionsSets( self._coreDb.dbSession, ids )

	@core.executionTrace
	def getUniqueCollectionId( self ):
		'''
		This Method Returns A Unique Collection Id ( Either First Selected Collection Or Default One).

		@return: Unique Id. ( String )
		'''

		selectedCollectionsIds = self.getSelectedCollectionsIds()
		if not len( selectedCollectionsIds ):
			return self.getCollectionId( self._defaultCollection )
		else :
			len( selectedCollectionsIds ) > 1 and LOGGER.warning( "!> {0} | Multiple Collection Selected, Using '{1}' Id !".format( self.__class__.__name__, selectedCollectionsIds[0] ) )
			return selectedCollectionsIds[0]

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
