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
class CollectionsOutliner_QTreeWidget( QTreeWidget ):
	'''
	This Class Is The CollectionsOutliner_QTreeWidget Class.
	'''

	@core.executionTrace
	def __init__( self, container ):
		'''
		This Method Initializes The Class.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		QTreeWidget.__init__( self )

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
	def coreDb( self ):
		'''
		This Method Is The Property For The _coreDb Attribute.

		@return: self._coreDb. ( Object )
		'''

		return self._coreDb

	@coreDb.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self, value ):
		'''
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDb" ) )

	@coreDb.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self ):
		'''
		This Method Is The Deleter Method For The _coreDb Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDb" ) )

	@property
	@core.executionTrace
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self, value ):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDatabaseBrowser" ) )

	@coreDatabaseBrowser.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDatabaseBrowser" ) )

	@property
	@core.executionTrace
	def coreCollectionsOutliner( self ):
		'''
		This Method Is The Property For The _coreCollectionsOutliner Attribute.

		@return: self._coreCollectionsOutliner. ( Object )
		'''

		return self._coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreCollectionsOutliner( self, value ):
		'''
		This Method Is The Setter Method For The _coreCollectionsOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreCollectionsOutliner" ) )

	@coreCollectionsOutliner.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreCollectionsOutliner( self ):
		'''
		This Method Is The Deleter Method For The _coreCollectionsOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreCollectionsOutliner" ) )

	@property
	@core.executionTrace
	def previousCollection( self ):
		'''
		This Method Is The Property For The _previousCollection Attribute.

		@return: self._previousCollection. ( String )
		'''

		return self._previousCollection

	@previousCollection.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def previousCollection( self, value ):
		'''
		This Method Is The Setter Method For The _previousCollection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "previousCollection" ) )

	@previousCollection.deleter
	@core.executionTrace
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

		if self.itemAt( event.pos() ) :
			LOGGER.debug( "> Item At Drop Position : '{0}'.".format( self.itemAt( event.pos() ) ) )
			if self.itemAt( event.pos() ).text( 0 ) != self._coreCollectionsOutliner._overallCollection :
				sets = self._coreDatabaseBrowser.ui.Database_Browser_listWidget.selectedItems()
				for set in sets :
					set._datas.collection = self.itemAt( event.pos() )._datas.id
				if dbUtilities.common.commit( self._coreDb.dbSession ) :
					self._coreCollectionsOutliner.Collections_Outliner_treeWidget_refreshSetsCounts()
					self._coreCollectionsOutliner.Collections_Outliner_treeWidget.setCurrentItem( self.itemAt( event.pos() ) )

	@core.executionTrace
	def QTreeWidgetItem_OnClicked( self, treeWidgetItem, column ):
		'''
		This Method Defines The Behavior When A QTreeWidgetItem Is Clicked.
		
		@param treeWidgetItem: Activated QTreeWidgetItem. ( QTreeWidgetItem )
		@param column: Activated Column. ( Integer )	
		'''

		self._previousCollection = treeWidgetItem.text( 0 )

	@core.executionTrace
	def QTreeWidgetItem_OnDoubleClicked( self, treeWidgetItem, column ):
		'''
		This Method Defines The Behavior When A QTreeWidgetItem Is Double Clicked.
		
		@param treeWidgetItem: Activated QTreeWidgetItem. ( QTreeWidgetItem )
		@param column: Activated Column. ( Integer )	
		'''

		setsCountLabel = self._coreCollectionsOutliner.setsCountLabel
		if treeWidgetItem.text( 0 ) != self._coreCollectionsOutliner.defaultCollection and treeWidgetItem.text( 0 ) != self._coreCollectionsOutliner.overallCollection :
			if column == self._coreCollectionsOutliner.treeWidgetHeaders.index( setsCountLabel ) :
				LOGGER.debug( "> Updating '{0}' QTreeWidgetItem Flags To 'Qt.ItemIsSelectable | Qt.ItemIsEnabled'.".format( treeWidgetItem ) )
				treeWidgetItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
				messageBox.messageBox( "Warning", "Warning", "{0} | 'Sets Counts' Column Is Read Only !".format( self.__class__.__name__ ) )
			else:
				LOGGER.debug( "> Updating '{0}' QTreeWidgetItem Flags To 'Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable'.".format( treeWidgetItem ) )
				treeWidgetItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable )
		else :
			messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' And '{2}' Collections Attributes Are Read Only !".format( self.__class__.__name__, self._coreCollectionsOutliner.overallCollection, self._coreCollectionsOutliner.defaultCollection ) )

	@core.executionTrace
	def QTreeWidgetItem_OnItemChanged( self, treeWidgetItem, column ):
		'''
		This Method Defines The Behavior When A QTreeWidgetItem Is Edited.
		
		@param treeWidgetItem: Activated QTreeWidgetItem. ( QTreeWidgetItem )
		@param column: Activated Column. ( Integer )	
		'''

		currentText = treeWidgetItem.text( column )

		if currentText != self._previousCollection :
			identity = hasattr( treeWidgetItem, "_datas" ) and treeWidgetItem._datas.id or None
			collections = [collection for collection in dbUtilities.common.filterCollections( self._coreDb.dbSession, "Sets", "type" )]
			if identity and collections :
				if column == 0 :
					if currentText not in [collection.name for collection in collections]:
						LOGGER.debug( "> Updating Collection '{0}' Name To '{1}'.".format( identity, currentText ) )
						collection = dbUtilities.common.filterCollections( self._coreDb.dbSession, "^{0}$".format( identity ), "id" )[0]
						collection.name = str( currentText )
						dbUtilities.common.commit( self._coreDb.dbSession )
					else :
						messageBox.messageBox( "Warning", "Warning", "{0} | '{1}' Collection Name Already Exists In Database !".format( self.__class__.__name__, currentText ) )
				elif column == 2 :
					LOGGER.debug( "> Updating Collection '{0}' Comment To '{1}'.".format( identity, currentText ) )
					collection = dbUtilities.common.filterCollections( self._coreDb.dbSession, "^{0}$".format( identity ), "id" )[0]
					collection.comment = str( currentText )
					dbUtilities.common.commit( self._coreDb.dbSession )

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

		self._coreDb = None
		self._coreDatabaseBrowser = None

		self._Collections_Outliner_treeWidget = None

		self._overallCollection = "Overall"
		self._defaultCollection = "Default"
		self._setsCountLabel = "Sets"
		self._treeWidgetHeaders = [ "Collections", self._setsCountLabel, "Comment" ]
		self._treeWidgetIndentation = 15

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
	def uiResources( self ):
		'''
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		'''

		return self._uiResources

	@uiResources.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self, value ):
		'''
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiResources" ) )

	@uiResources.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self ):
		'''
		This Method Is The Deleter Method For The _uiResources Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiResources" ) )

	@property
	@core.executionTrace
	def uiDefaultCollectionIcon( self ):
		'''
		This Method Is The Property For The _uiDefaultCollectionIcon Attribute.

		@return: self._uiDefaultCollectionIcon. ( String )
		'''

		return self._uiDefaultCollectionIcon

	@uiDefaultCollectionIcon.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiDefaultCollectionIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiDefaultCollectionIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiDefaultCollectionIcon" ) )

	@uiDefaultCollectionIcon.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiDefaultCollectionIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiDefaultCollectionIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiDefaultCollectionIcon" ) )

	@property
	@core.executionTrace
	def uiUserCollectionIcon( self ):
		'''
		This Method Is The Property For The _uiUserCollectionIcon Attribute.

		@return: self._uiUserCollectionIcon. ( String )
		'''

		return self._uiUserCollectionIcon

	@uiUserCollectionIcon.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiUserCollectionIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiUserCollectionIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiUserCollectionIcon" ) )

	@uiUserCollectionIcon.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiUserCollectionIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiUserCollectionIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiUserCollectionIcon" ) )

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
	def coreDb( self ):
		'''
		This Method Is The Property For The _coreDb Attribute.

		@return: self._coreDb. ( Object )
		'''

		return self._coreDb

	@coreDb.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self, value ):
		'''
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDb" ) )

	@coreDb.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDb( self ):
		'''
		This Method Is The Deleter Method For The _coreDb Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDb" ) )

	@property
	@core.executionTrace
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self, value ):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDatabaseBrowser" ) )

	@coreDatabaseBrowser.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDatabaseBrowser" ) )

	@property
	@core.executionTrace
	def Collections_Outliner_treeWidget( self ):
		'''
		This Method Is The Property For The _Collections_Outliner_treeWidget Attribute.

		@return: self._Collections_Outliner_treeWidget. ( QTreeWidget )
		'''

		return self._Collections_Outliner_treeWidget

	@Collections_Outliner_treeWidget.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Collections_Outliner_treeWidget( self, value ):
		'''
		This Method Is The Setter Method For The _Collections_Outliner_treeWidget Attribute.

		@param value: Attribute Value. ( QTreeWidget )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "Collections_Outliner_treeWidget" ) )

	@Collections_Outliner_treeWidget.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def Collections_Outliner_treeWidget( self ):
		'''
		This Method Is The Deleter Method For The _Collections_Outliner_treeWidget Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "Collections_Outliner_treeWidget" ) )

	@property
	@core.executionTrace
	def overallCollection( self ):
		'''
		This Method Is The Property For The _overallCollection Attribute.

		@return: self._overallCollection. ( String )
		'''

		return self._overallCollection

	@overallCollection.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def overallCollection( self, value ):
		'''
		This Method Is The Setter Method For The _overallCollection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "overallCollection" ) )

	@overallCollection.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def overallCollection( self ):
		'''
		This Method Is The Deleter Method For The _overallCollection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "overallCollection" ) )

	@property
	@core.executionTrace
	def defaultCollection( self ):
		'''
		This Method Is The Property For The _defaultCollection Attribute.

		@return: self._defaultCollection. ( String )
		'''

		return self._defaultCollection

	@defaultCollection.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def defaultCollection( self, value ):
		'''
		This Method Is The Setter Method For The _defaultCollection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "defaultCollection" ) )

	@defaultCollection.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def defaultCollection( self ):
		'''
		This Method Is The Deleter Method For The _defaultCollection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "defaultCollection" ) )

	@property
	@core.executionTrace
	def setsCountLabel( self ):
		'''
		This Method Is The Property For The _setsCountLabel Attribute.

		@return: self._setsCountLabel. ( String )
		'''

		return self._setsCountLabel

	@setsCountLabel.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def setsCountLabel( self, value ):
		'''
		This Method Is The Setter Method For The _setsCountLabel Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "setsCountLabel" ) )

	@setsCountLabel.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def setsCountLabel( self ):
		'''
		This Method Is The Deleter Method For The _setsCountLabel Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "setsCountLabel" ) )

	@property
	@core.executionTrace
	def treeWidgetHeaders( self ):
		'''
		This Method Is The Property For The _treeWidgetHeaders Attribute.

		@return: self._treeWidgetHeaders. ( List )
		'''

		return self._treeWidgetHeaders

	@treeWidgetHeaders.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetHeaders( self, value ):
		'''
		This Method Is The Setter Method For The _treeWidgetHeaders Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "treeWidgetHeaders" ) )

	@treeWidgetHeaders.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetHeaders( self ):
		'''
		This Method Is The Deleter Method For The _treeWidgetHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "treeWidgetHeaders" ) )

	@property
	@core.executionTrace
	def treeWidgetIndentation( self ):
		'''
		This Method Is The Property For The _treeWidgetIndentation Attribute.

		@return: self._treeWidgetIndentation. ( Integer )
		'''

		return self._treeWidgetIndentation

	@treeWidgetIndentation.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetIndentation( self, value ):
		'''
		This Method Is The Setter Method For The _treeWidgetIndentation Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "treeWidgetIndentation" ) )

	@treeWidgetIndentation.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def treeWidgetIndentation( self ):
		'''
		This Method Is The Deleter Method For The _treeWidgetIndentation Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "treeWidgetIndentation" ) )

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

		self._container.setsCentricLayoutComponents.append( self.name )

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

		self._Collections_Outliner_treeWidget = CollectionsOutliner_QTreeWidget( self._container )
		self.ui.Collections_Outliner_dockWidgetContents_gridLayout.addWidget( self._Collections_Outliner_treeWidget )

		self._Collections_Outliner_treeWidget.setContextMenuPolicy( Qt.ActionsContextMenu )
		self.Collections_Outliner_treeWidget_setActions()

		self.Collections_Outliner_treeWidget_setUi()

		# Signals / Slots.
		self._Collections_Outliner_treeWidget.connect( self._Collections_Outliner_treeWidget, SIGNAL( "itemSelectionChanged()" ), self.Collections_Outliner_treeWidget_OnItemSelectionChanged )
		self._Collections_Outliner_treeWidget.connect( self._Collections_Outliner_treeWidget, SIGNAL( "itemClicked( QTreeWidgetItem *, int )" ), self._Collections_Outliner_treeWidget.QTreeWidgetItem_OnClicked )
		self._Collections_Outliner_treeWidget.connect( self._Collections_Outliner_treeWidget, SIGNAL( "itemDoubleClicked( QTreeWidgetItem *, int )" ), self._Collections_Outliner_treeWidget.QTreeWidgetItem_OnDoubleClicked )

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
	def Collections_Outliner_treeWidget_setUi( self ):
		'''
		This Method Sets The _Collections_Outliner_treeWidget.
		'''

		LOGGER.debug( " > Refreshing '{0}' Ui !".format( self.__class__.__name__ ) )

		self._Collections_Outliner_treeWidget.disconnect( self._Collections_Outliner_treeWidget, SIGNAL( "itemChanged( QTreeWidgetItem *, int )" ), self._Collections_Outliner_treeWidget.QTreeWidgetItem_OnItemChanged )

		self._Collections_Outliner_treeWidget.clear()
		self._Collections_Outliner_treeWidget.setSelectionMode( QAbstractItemView.ExtendedSelection )
		self._Collections_Outliner_treeWidget.setColumnCount( len( self._treeWidgetHeaders ) )
		self._Collections_Outliner_treeWidget.setHeaderLabels( QStringList( self._treeWidgetHeaders ) )
		self._Collections_Outliner_treeWidget.setIndentation( self._treeWidgetIndentation )
		self._Collections_Outliner_treeWidget.setSortingEnabled( True )

		collections = dbUtilities.common.filterCollections( self._coreDb.dbSession, "Sets", "type" )

		overallTreeWidgetItem = QTreeWidgetItem()
		overallTreeWidgetItem.setText( 0, self._overallCollection )
		overallTreeWidgetItem.setText( 1, str( dbUtilities.common.getSets( self._coreDb.dbSession ).count() ) )
		overallTreeWidgetItem.setTextAlignment( 1, Qt.AlignCenter )

		LOGGER.debug( " > Adding '{0}' Collection To 'Collections_Outliner_treeWidget'.".format( self._overallCollection ) )
		self._Collections_Outliner_treeWidget.addTopLevelItem( overallTreeWidgetItem )
		overallTreeWidgetItem.setExpanded( True )

		if collections :
			for collection in collections :
				id = collection.id
				name = collection.name
				type = collection.type
				comment = collection.comment

				treeWidgetItem = QTreeWidgetItem( overallTreeWidgetItem )
				treeWidgetItem._datas = collection
				treeWidgetItem.setText( 0, name )
				icon = name == self.defaultCollection and QIcon( os.path.join( self._uiResources, self._uiDefaultCollectionIcon ) ) or QIcon( os.path.join( self._uiResources, self._uiUserCollectionIcon ) )
				treeWidgetItem.setIcon( 0, icon )

				treeWidgetItem.setText( 1, str( self._coreDb.dbSession.query( dbUtilities.types.DbSet ).filter_by( collection = id ).count() ) )
				treeWidgetItem.setTextAlignment( 1, Qt.AlignCenter )

				treeWidgetItem.setText( 2, comment )
				# font = QFont()
				# font.setItalic( True )
				# treeWidgetItem.setFont( 2, font )

				LOGGER.debug( " > Adding '{0}' Collection To 'Collections_Outliner_treeWidget'.".format( collection ) )

				self._Collections_Outliner_treeWidget.addTopLevelItem( treeWidgetItem )
		else :
			LOGGER.info( "{0} | Database Has No User Defined Collections !".format( self.__class__.__name__ ) )

		for column in range( len( self._treeWidgetHeaders ) ) :
			self._Collections_Outliner_treeWidget.resizeColumnToContents( column )

		self._Collections_Outliner_treeWidget.sortItems( 0, Qt.AscendingOrder )

		self._Collections_Outliner_treeWidget.connect( self._Collections_Outliner_treeWidget, SIGNAL( "itemChanged( QTreeWidgetItem *, int )" ), self._Collections_Outliner_treeWidget.QTreeWidgetItem_OnItemChanged )

	@core.executionTrace
	def refreshUi( self ):
		'''
		This Method Refreshes The _Collections_Outliner_treeWidget.
		'''

		self.Collections_Outliner_treeWidget_setUi()

	@core.executionTrace
	def Collections_Outliner_treeWidget_refreshSetsCounts( self ):
		'''
		This Method Refreshes The _Collections_Outliner_treeWidget Sets Counts.
		'''

		for treeWidgetItem in self._Collections_Outliner_treeWidget.findItems( ".*", Qt.MatchRegExp | Qt.MatchRecursive, 0 ):
			if treeWidgetItem.text( 0 ) == self._overallCollection :
				treeWidgetItem.setText( 1, str( dbUtilities.common.getSets( self._coreDb.dbSession ).count() ) )
			else:
				treeWidgetItem.setText( 1, str( self._coreDb.dbSession.query( dbUtilities.types.DbSet ).filter_by( collection = treeWidgetItem._datas.id ).count() ) )

	@core.executionTrace
	def getCollectionsSets( self ):
		'''
		This Method Gets The Sets Associated To Selected Collections.
		
		@return: Sets List. ( List )
		'''

		selectedItems = self._Collections_Outliner_treeWidget.selectedItems()
		selectedCollections = selectedItems != [] and selectedItems or None
		allIds = [collection._datas.id for collection in self._Collections_Outliner_treeWidget.findItems( ".*", Qt.MatchRegExp | Qt.MatchRecursive, 0 ) if hasattr( collection, "_datas" )]
		ids = selectedCollections and ( self._overallCollection in [collection.text( 0 ) for collection in selectedCollections] and allIds or self.getSelectedCollectionsIds() ) or allIds

		return dbUtilities.common.getCollectionsSets( self._coreDb.dbSession, ids )

	@core.executionTrace
	def Collections_Outliner_treeWidget_setActions( self ):
		'''
		This Method Sets The Collections Outliner Actions.
		'''

		addContentAction = QAction( "Add Content ...", self._Collections_Outliner_treeWidget )
		addContentAction.triggered.connect( self.Collections_Outliner_treeWidget_addContentAction )
		self._Collections_Outliner_treeWidget.addAction( addContentAction )

		addCollectionAction = QAction( "Add Collection ...", self._Collections_Outliner_treeWidget )
		addCollectionAction.triggered.connect( self.Collections_Outliner_treeWidget_addCollectionAction )
		self._Collections_Outliner_treeWidget.addAction( addCollectionAction )

		removeCollectionsAction = QAction( "Remove Collection(s) ...", self._Collections_Outliner_treeWidget )
		removeCollectionsAction.triggered.connect( self.Collections_Outliner_treeWidget_removeCollectionsAction )
		self._Collections_Outliner_treeWidget.addAction( removeCollectionsAction )

	@core.executionTrace
	def Collections_Outliner_treeWidget_addContentAction( self, checked ):
		'''
		This Method Is Triggered By addContentAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		collection = self.addCollection()
		if collection :
			self.Collections_Outliner_treeWidget_setUi()
			self.coreDatabaseBrowser.addDirectory( self.getCollectionId( collection ) )
			self._Collections_Outliner_treeWidget.setCurrentItem( self.Collections_Outliner_treeWidget.findItems( collection, Qt.MatchExactly | Qt.MatchRecursive, 0 )[0] )
			self.Collections_Outliner_treeWidget_refreshSetsCounts()

	@core.executionTrace
	def Collections_Outliner_treeWidget_addCollectionAction( self, checked ):
		'''
		This Method Is Triggered By addCollectionAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		collection = self.addCollection()
		if collection :
			self.Collections_Outliner_treeWidget_setUi()

	@core.executionTrace
	def Collections_Outliner_treeWidget_removeCollectionsAction( self, checked ):
		'''
		This Method Is Triggered By removeCollectionsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.removeCollections()
		self.Collections_Outliner_treeWidget_setUi()

	@core.executionTrace
	def Collections_Outliner_treeWidget_OnItemSelectionChanged ( self ):
		'''
		This Method Refreshes The Database Browser Depending On The Collections Outliner Selected Items.
		'''

		self._coreDatabaseBrowser.setCollectionsDisplaySets()
		self._coreDatabaseBrowser.refreshUi()
		self.Collections_Outliner_treeWidget_refreshSetsCounts()

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

		selectedCollections = self._Collections_Outliner_treeWidget.selectedItems()

		if self._overallCollection in [str( collection.text( 0 ) ) for collection in selectedCollections] or self._defaultCollection in [str( collection.text( 0 ) ) for collection in selectedCollections]:
			messageBox.messageBox( "Warning", "Warning", "{0} | Cannot Remove '{1}' Or '{2}' Collection !".format( self.__class__.__name__, self._overallCollection, self._defaultCollection ) )

		selectedCollections = [collection for collection in self._Collections_Outliner_treeWidget.selectedItems() if collection.text( 0 ) != self._overallCollection and collection.text( 0 ) != self._defaultCollection ]
		if selectedCollections :
			if messageBox.messageBox( "Question", "Question", "Are You Sure You Want To Remove '{0}' Collection(s) ?".format( ", ".join( [str( collection.text( 0 ) ) for collection in selectedCollections] ) ), buttons = QMessageBox.Yes | QMessageBox.No ) == 16384 :
				sets = dbUtilities.common.getCollectionsSets( self._coreDb.dbSession, self.getSelectedCollectionsIds() )
				for set in sets :
					LOGGER.info( "{0} | Moving '{1}' Set To Default Collection !".format( self.__class__.__name__, set.name ) )
					set.collection = self.getCollectionId( self._defaultCollection )
				success = True
				for collection in selectedCollections :
					LOGGER.info( "{0} | Removing '{1}' Collection From Database !".format( self.__class__.__name__, collection.text( 0 ) ) )
					success *= dbUtilities.common.removeCollection( self._coreDb.dbSession, str( collection._datas.id ) )
				return success

	@core.executionTrace
	def getSelectedCollectionsIds( self ):
		'''
		This Method Gets Selected Collections Ids.
	
		@return: Collections Ids. ( List )
		'''

		selectedCollections = self._Collections_Outliner_treeWidget.selectedItems() != [] and self._Collections_Outliner_treeWidget.selectedItems() or None
		ids = []
		if selectedCollections :
			ids = [collection._datas.id for collection in selectedCollections if hasattr( collection, "_datas" )]
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

		return self.Collections_Outliner_treeWidget.findItems( collection, Qt.MatchExactly | Qt.MatchRecursive, 0 )[0]._datas.id

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
