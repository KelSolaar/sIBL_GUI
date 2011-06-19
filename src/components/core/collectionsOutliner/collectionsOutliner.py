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

"""
************************************************************************************************
***	collectionsOutliner.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Collections Outliner Core Component Module.
***
***	Others:
***
************************************************************************************************
"""

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
import platform
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings
import ui.common
import ui.widgets.messageBox as messageBox
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class CollectionsOutliner_QTreeView(QTreeView):
	"""
	This Class Is The CollectionsOutliner_QTreeView Class.
	"""

	@core.executionTrace
	def __init__(self, container):
		"""
		This Method Initializes The Class.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QTreeView.__init__(self, container)

		self.setAcceptDrops(True)

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
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		"""

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def coreDb(self):
		"""
		This Method Is The Property For The _coreDb Attribute.

		@return: self._coreDb. ( Object )
		"""

		return self._coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This Method Is The Deleter Method For The _coreDb Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDb"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		"""

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDatabaseBrowser"))

	@property
	def coreCollectionsOutliner(self):
		"""
		This Method Is The Property For The _coreCollectionsOutliner Attribute.

		@return: self._coreCollectionsOutliner. ( Object )
		"""

		return self._coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		"""
		This Method Is The Setter Method For The _coreCollectionsOutliner Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This Method Is The Deleter Method For The _coreCollectionsOutliner Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreCollectionsOutliner"))

	@property
	def previousCollection(self):
		"""
		This Method Is The Property For The _previousCollection Attribute.

		@return: self._previousCollection. ( String )
		"""

		return self._previousCollection

	@previousCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previousCollection(self, value):
		"""
		This Method Is The Setter Method For The _previousCollection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("previousCollection"))

	@previousCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previousCollection(self):
		"""
		This Method Is The Deleter Method For The _previousCollection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("previousCollection"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def dragEnterEvent(self, event):
		"""
		This Method Defines The Drag Enter Event Behavior.
		
		@param event: QEvent. ( QEvent )
		"""

		if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
			LOGGER.debug("> '{0}' Drag Event Type Accepted!".format("application/x-qabstractitemmodeldatalist"))
			event.accept()
		elif event.mimeData().hasFormat("text/uri-list"):
			LOGGER.debug("> '{0}' Drag Event Type Accepted!".format("text/uri-list"))
			event.accept()
		else:
			event.ignore()

	@core.executionTrace
	def dragMoveEvent(self, event):
		"""
		This Method Defines The Drag Move Event Behavior.
		
		@param event: QEvent. ( QEvent )
		"""

		pass

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, OSError, foundations.exceptions.UserError)
	def dropEvent(self, event):
		"""
		This Method Defines The Drop Event Behavior.
		
		@param event: QEvent. ( QEvent )		
		"""

		if not self._container.parameters.databaseReadOnly:
			if event.mimeData().hasUrls():
				LOGGER.debug("> Drag Event Urls List: '{0}'!".format(event.mimeData().urls()))
				for url in event.mimeData().urls():
					path = (platform.system() == "Windows" or platform.system() == "Microsoft") and re.search("^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
					if re.search("\.{0}$".format(self._coreDatabaseBrowser.extension), str(url.path())):
						name = foundations.strings.getSplitextBasename(path)
						if messageBox.messageBox("Question", "Question", "'{0}' Ibl Set File Has Been Dropped, Would You Like To Add It To The Database?".format(name), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
							self._coreDatabaseBrowser.addIblSet(name, path)
							self._coreDatabaseBrowser.Database_Browser_listView_extendedRefreshModel()
					else:
						if os.path.isdir(path):
							if messageBox.messageBox("Question", "Question", "'{0}' Directory Has Been Dropped, Would You Like To Add Its Content To The Database?".format(path), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
								self._coreDatabaseBrowser.addDirectory(path)
								self._coreDatabaseBrowser.Database_Browser_listView_extendedRefreshModel()
						else:
							raise OSError, "{0} | Exception Raised While Parsing '{1}' Path: Syntax Is Invalid!".format(self.__class__.__name__, path)
			else:
				indexAt = self.indexAt(event.pos())
				itemAt = self.model().itemFromIndex(indexAt)

				if itemAt:
					LOGGER.debug("> Item At Drop Position: '{0}'.".format(itemAt))
					collectionStandardItem = self.model().itemFromIndex(self.model().sibling(indexAt.row(), 0, indexAt))
					if collectionStandardItem.text() != self._coreCollectionsOutliner._overallCollection:
						iblSets = self._coreDatabaseBrowser.getSelectedItems()
						LOGGER.debug("> Adding '{0}' Ibl Set(s) To '{1}' Collection.".format(", ".join((iblSet._datas.name for iblSet in iblSets)), collectionStandardItem._datas.name))
						for iblSet in iblSets:
							iblSet._datas.collection = collectionStandardItem._datas.id
						if dbUtilities.common.commit(self._coreDb.dbSession):
							# Crash Preventing Code.
							self._coreDatabaseBrowser.modelSelectionState = False

							self._coreCollectionsOutliner.Collections_Outliner_treeView_refreshSetsCounts()
							self._coreCollectionsOutliner.ui.Collections_Outliner_treeView.selectionModel().setCurrentIndex(indexAt, QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)

							# Crash Preventing Code.
							self._coreDatabaseBrowser.modelSelectionState = True
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only!".format(self.__class__.__name__)

	@core.executionTrace
	def QTreeView_OnClicked(self, index):
		"""
		This Method Defines The Behavior When The Model Is Clicked.
		
		@param index: Clicked Model Item Index. ( QModelIndex )
		"""

		self._previousCollection = self.model().itemFromIndex(self.model().sibling(index.row(), 0, index)).text()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def QTreeView_OnDoubleClicked(self, index):
		"""
		This Method Defines The Behavior When A QStandardItem Is Double Clicked.
		
		@param index: Clicked Model Item Index. ( QModelIndex )
		"""

		if not self._container.parameters.databaseReadOnly:
			collectionStandardItem = self.model().itemFromIndex(self.model().sibling(index.row(), 0, index))

			if collectionStandardItem.text() != self._coreCollectionsOutliner.defaultCollection and collectionStandardItem.text() != self._coreCollectionsOutliner.overallCollection:
				if self.model().itemFromIndex(index).column() == self._coreCollectionsOutliner.modelHeaders.index(self._coreCollectionsOutliner.setsCountLabel):
					messageBox.messageBox("Warning", "Warning", "{0} | 'Sets Counts' Column Is Read Only!".format(self.__class__.__name__))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' And '{2}' Collections Attributes Are Read Only!".format(self.__class__.__name__, self._coreCollectionsOutliner.overallCollection, self._coreCollectionsOutliner.defaultCollection))
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only!".format(self.__class__.__name__)

class CollectionsOutliner(UiComponent):
	"""
	This Class Is The CollectionsOutliner Class.
	"""

	# Custom Signals Definitions.
	modelChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
		self.deactivatable = False

		self._uiPath = "ui/Collections_Outliner.ui"
		self._uiResources = "resources"
		self._uiDefaultCollectionIcon = "Default_Collection.png"
		self._uiUserCollectionIcon = "User_Collection.png"
		self._dockArea = 1

		self._container = None
		self._settings = None
		self._settingsSection = None
		self._settingsSeparator = ","

		self._coreDb = None
		self._coreDatabaseBrowser = None

		self._model = None
		self._modelSelection = None

		self._overallCollection = "Overall"
		self._defaultCollection = "Default"
		self._setsCountLabel = "Sets"
		self._modelHeaders = [ "Collections", self._setsCountLabel, "Comment" ]
		self._treeViewIndentation = 15

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		"""

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		"""

		return self._uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This Method Is The Deleter Method For The _uiResources Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def uiDefaultCollectionIcon(self):
		"""
		This Method Is The Property For The _uiDefaultCollectionIcon Attribute.

		@return: self._uiDefaultCollectionIcon. ( String )
		"""

		return self._uiDefaultCollectionIcon

	@uiDefaultCollectionIcon.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionIcon(self, value):
		"""
		This Method Is The Setter Method For The _uiDefaultCollectionIcon Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiDefaultCollectionIcon"))

	@uiDefaultCollectionIcon.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionIcon(self):
		"""
		This Method Is The Deleter Method For The _uiDefaultCollectionIcon Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiDefaultCollectionIcon"))

	@property
	def uiUserCollectionIcon(self):
		"""
		This Method Is The Property For The _uiUserCollectionIcon Attribute.

		@return: self._uiUserCollectionIcon. ( String )
		"""

		return self._uiUserCollectionIcon

	@uiUserCollectionIcon.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUserCollectionIcon(self, value):
		"""
		This Method Is The Setter Method For The _uiUserCollectionIcon Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiUserCollectionIcon"))

	@uiUserCollectionIcon.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUserCollectionIcon(self):
		"""
		This Method Is The Deleter Method For The _uiUserCollectionIcon Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiUserCollectionIcon"))

	@property
	def dockArea(self):
		"""
		This Method Is The Property For The _dockArea Attribute.

		@return: self._dockArea. ( Integer )
		"""

		return self._dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This Method Is The Deleter Method For The _dockArea Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dockArea"))

	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		"""

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def settings(self):
		"""
		This Method Is The Property For The _settings Attribute.

		@return: self._settings. ( QSettings )
		"""

		return self._settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This Method Is The Deleter Method For The _settings Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settings"))

	@property
	def settingsSection(self):
		"""
		This Method Is The Property For The _settingsSection Attribute.

		@return: self._settingsSection. ( String )
		"""

		return self._settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This Method Is The Setter Method For The _settingsSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This Method Is The Deleter Method For The _settingsSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settingsSection"))

	@property
	def settingsSeparator(self):
		"""
		This Method Is The Property For The _settingsSeparator Attribute.

		@return: self._settingsSeparator. ( String )
		"""

		return self._settingsSeparator

	@settingsSeparator.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self, value):
		"""
		This Method Is The Setter Method For The _settingsSeparator Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self):
		"""
		This Method Is The Deleter Method For The _settingsSeparator Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settingsSeparator"))

	@property
	def coreDb(self):
		"""
		This Method Is The Property For The _coreDb Attribute.

		@return: self._coreDb. ( Object )
		"""

		return self._coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This Method Is The Deleter Method For The _coreDb Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDb"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		"""

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDatabaseBrowser"))

	@property
	def model(self):
		"""
		This Method Is The Property For The _model Attribute.

		@return: self._model. ( QStandardItemModel )
		"""

		return self._model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This Method Is The Setter Method For The _model Attribute.

		@param value: Attribute Value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This Method Is The Deleter Method For The _model Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("model"))

	@property
	def modelSelection(self):
		"""
		This Method Is The Property For The _modelSelection Attribute.

		@return: self._modelSelection. ( Dictionary )
		"""

		return self._modelSelection

	@modelSelection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self, value):
		"""
		This Method Is The Setter Method For The _modelSelection Attribute.

		@param value: Attribute Value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("modelSelection"))

	@modelSelection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self):
		"""
		This Method Is The Deleter Method For The _modelSelection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("modelSelection"))

	@property
	def overallCollection(self):
		"""
		This Method Is The Property For The _overallCollection Attribute.

		@return: self._overallCollection. ( String )
		"""

		return self._overallCollection

	@overallCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overallCollection(self, value):
		"""
		This Method Is The Setter Method For The _overallCollection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("overallCollection"))

	@overallCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overallCollection(self):
		"""
		This Method Is The Deleter Method For The _overallCollection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("overallCollection"))

	@property
	def defaultCollection(self):
		"""
		This Method Is The Property For The _defaultCollection Attribute.

		@return: self._defaultCollection. ( String )
		"""

		return self._defaultCollection

	@defaultCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollection(self, value):
		"""
		This Method Is The Setter Method For The _defaultCollection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("defaultCollection"))

	@defaultCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollection(self):
		"""
		This Method Is The Deleter Method For The _defaultCollection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("defaultCollection"))

	@property
	def setsCountLabel(self):
		"""
		This Method Is The Property For The _setsCountLabel Attribute.

		@return: self._setsCountLabel. ( String )
		"""

		return self._setsCountLabel

	@setsCountLabel.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setsCountLabel(self, value):
		"""
		This Method Is The Setter Method For The _setsCountLabel Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("setsCountLabel"))

	@setsCountLabel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setsCountLabel(self):
		"""
		This Method Is The Deleter Method For The _setsCountLabel Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("setsCountLabel"))

	@property
	def modelHeaders(self):
		"""
		This Method Is The Property For The _modelHeaders Attribute.

		@return: self._modelHeaders. ( List )
		"""

		return self._modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self, value):
		"""
		This Method Is The Setter Method For The _modelHeaders Attribute.

		@param value: Attribute Value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("modelHeaders"))

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self):
		"""
		This Method Is The Deleter Method For The _modelHeaders Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("modelHeaders"))

	@property
	def treeViewIndentation(self):
		"""
		This Method Is The Property For The _treeViewIndentation Attribute.

		@return: self._treeViewIndentation. ( Integer )
		"""

		return self._treeViewIndentation

	@treeViewIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self, value):
		"""
		This Method Is The Setter Method For The _treeViewIndentation Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("treeViewIndentation"))

	@treeViewIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self):
		"""
		This Method Is The Deleter Method For The _treeViewIndentation Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("treeViewIndentation"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiPath)
		self._uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiResources)
		self._container = container
		self._settings = self._container.settings
		self._settingsSection = self.name

		self._coreDb = self._container.componentsManager.components["core.db"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Cannot Be Deactivated!".format(self._name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self._container.parameters.databaseReadOnly and	LOGGER.info("{0} | Collections_Outliner_treeView Model Edition Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))
		self._model = QStandardItemModel()
		self.Collections_Outliner_treeView_setModel()

		self.ui.Collections_Outliner_treeView = CollectionsOutliner_QTreeView(self._container)
		self.ui.Collections_Outliner_dockWidgetContents_gridLayout.addWidget(self.ui.Collections_Outliner_treeView, 0, 0)

		self.ui.Collections_Outliner_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.Collections_Outliner_treeView_setActions()

		self.Collections_Outliner_treeView_setView()

		# Signals / Slots.
		self.ui.Collections_Outliner_treeView.selectionModel().selectionChanged.connect(self.Collections_Outliner_treeView_OnModelSelectionChanged)
		self.ui.Collections_Outliner_treeView.clicked.connect(self.ui.Collections_Outliner_treeView.QTreeView_OnClicked)
		self.ui.Collections_Outliner_treeView.doubleClicked.connect(self.ui.Collections_Outliner_treeView.QTreeView_OnDoubleClicked)
		self.modelChanged.connect(self.Collections_Outliner_treeView_refreshView)
		not self._container.parameters.databaseReadOnly and self._model.dataChanged.connect(self.Collections_Outliner_treeView_OnModelDataChanged)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Ui Cannot Be Uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self._container.addDockWidget(Qt.DockWidgetArea(self._dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget Cannot Be Removed!".format(self.name))

	@core.executionTrace
	def onStartup(self):
		"""
		This Method Is Called On Framework Startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework Startup Method.".format(self.__class__.__name__))

		if not self._container.parameters.databaseReadOnly:
			self.addDefaultCollection()
		else:
			LOGGER.info("{0} | Database Default Collection Wizard Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeCollectionsIds = str(self._settings.getKey(self._settingsSection, "activeCollections").toString())
		LOGGER.debug("> Stored '{0}' Active Collections Ids Selection: '{1}'.".format(self.__class__.__name__, activeCollectionsIds))
		if activeCollectionsIds:
			if self._settingsSeparator in activeCollectionsIds:
				ids = activeCollectionsIds.split(self._settingsSeparator)
			else:
				ids = [activeCollectionsIds]
			self._modelSelection["Collections"] = [int(id) for id in ids]

		activeOverallCollection = str(self._settings.getKey(self._settingsSection, "activeOverallCollection").toString())
		LOGGER.debug("> Stored '{0}' Active Overall Collection Selection: '{1}'.".format(self.__class__.__name__, activeOverallCollection))
		if activeOverallCollection:
			self._modelSelection[self._overallCollection] = [activeOverallCollection]

		self.Collections_Outliner_treeView_restoreModelSelection()

	@core.executionTrace
	def onClose(self):
		"""
		This Method Is Called On Framework Close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework Close Method.".format(self.__class__.__name__))

		self.Collections_Outliner_treeView_storeModelSelection()
		self._settings.setKey(self._settingsSection, "activeCollections", self._settingsSeparator.join((str(id) for id in self._modelSelection["Collections"])))
		self._settings.setKey(self._settingsSection, "activeOverallCollection", self._settingsSeparator.join((str(id) for id in self._modelSelection[self._overallCollection])))

	@core.executionTrace
	def Collections_Outliner_treeView_setModel(self):
		"""
		This Method Sets The Collections_Outliner_treeView Model.

		Columns:
		Collections | Sets | Comment
		
		Rows:
		* Overall Collection: { _type: "Overall" }
		** Collection: { _type: "Collection", _datas: dbUtilities.types.DbCollection }
		"""

		LOGGER.debug("> Setting Up '{0}' Model!".format("Collections_Outliner_treeView"))

		self.Collections_Outliner_treeView_storeModelSelection()

		self._model.clear()

		self._model.setHorizontalHeaderLabels(self._modelHeaders)
		self._model.setColumnCount(len(self._modelHeaders))
		readOnlyFlags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

		LOGGER.debug("> Preparing '{0}' Collection For '{1}' Model.".format(self._overallCollection, "Collections_Outliner_treeView"))

		overallCollectionStandardItem = QStandardItem(QString(self._overallCollection))
		overallCollectionStandardItem.setFlags(readOnlyFlags)

		overallCollectionSetsCountStandardItem = QStandardItem(QString(str(dbUtilities.common.getIblSets(self._coreDb.dbSession).count())))
		overallCollectionSetsCountStandardItem.setTextAlignment(Qt.AlignCenter)
		overallCollectionSetsCountStandardItem.setFlags(readOnlyFlags)

		overallCollectionCommentsStandardItem = QStandardItem()
		overallCollectionCommentsStandardItem.setFlags(readOnlyFlags)

		overallCollectionStandardItem._type = "Overall"

		LOGGER.debug("> Adding '{0}' Collection To '{1}'.".format(self._overallCollection, "Collections_Outliner_treeView"))
		self._model.appendRow([overallCollectionStandardItem, overallCollectionSetsCountStandardItem, overallCollectionCommentsStandardItem])

		collections = dbUtilities.common.filterCollections(self._coreDb.dbSession, "Sets", "type")

		if collections:
			for collection in collections:
				LOGGER.debug("> Preparing '{0}' Collection For '{1}' Model.".format(collection.name, "Collections_Outliner_treeView"))

				try:
					collectionStandardItem = QStandardItem(QString(collection.name))
					iconPath = collection.name == self.defaultCollection and os.path.join(self._uiResources, self._uiDefaultCollectionIcon) or os.path.join(self._uiResources, self._uiUserCollectionIcon)
					collectionStandardItem.setIcon(QIcon(iconPath))
					(collection.name == self._defaultCollection or self._container.parameters.databaseReadOnly) and collectionStandardItem.setFlags(readOnlyFlags)

					collectionSetsCountStandardItem = QStandardItem(QString(str(self._coreDb.dbSession.query(dbUtilities.types.DbIblSet).filter_by(collection=collection.id).count())))
					collectionSetsCountStandardItem.setTextAlignment(Qt.AlignCenter)
					collectionSetsCountStandardItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

					collectionCommentsStandardItem = QStandardItem(QString(collection.comment))
					(collection.name == self._defaultCollection or self._container.parameters.databaseReadOnly) and collectionCommentsStandardItem.setFlags(readOnlyFlags)

					collectionStandardItem._datas = collection
					collectionStandardItem._type = "Collection"

					LOGGER.debug("> Adding '{0}' Collection To '{1}' Model.".format(collection.name, "Collections_Outliner_treeView"))
					overallCollectionStandardItem.appendRow([collectionStandardItem, collectionSetsCountStandardItem, collectionCommentsStandardItem])

				except Exception as error:
					LOGGER.error("!>{0} | Exception Raised While Adding '{1}' Collection To '{2}' Model!".format(self.__class__.__name__, collection.name, "Collections_Outliner_treeView"))
					foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "Collections_Outliner_treeView"))
		else:
			LOGGER.info("{0} | Database Has No User Defined Collections!".format(self.__class__.__name__))

		self.Collections_Outliner_treeView_restoreModelSelection()

		self.emit(SIGNAL("modelChanged()"))

	@core.executionTrace
	def Collections_Outliner_treeView_refreshModel(self):
		"""
		This Method Refreshes The Collections_Outliner_treeView Model.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Collections_Outliner_treeView"))

		self.Collections_Outliner_treeView_setModel()

	@core.executionTrace
	def Collections_Outliner_treeView_OnModelDataChanged(self, startIndex, endIndex):
		"""
		This Method Defines The Behavior When The Collections_Outliner_treeView Model Data Change.
		
		@param startIndex: Edited Item Starting QModelIndex. ( QModelIndex )
		@param endIndex: Edited Item Ending QModelIndex. ( QModelIndex )
		"""

		standardItem = self._model.itemFromIndex(startIndex)
		currentText = standardItem.text()

		collectionStandardItem = self._model.itemFromIndex(self._model.sibling(startIndex.row(), 0, startIndex))

		identity = collectionStandardItem._type == "Collection" and collectionStandardItem._datas.id or None
		collections = [collection for collection in dbUtilities.common.filterCollections(self._coreDb.dbSession, "Sets", "type")]
		if identity and collections:
			if startIndex.column() == 0:
				if currentText not in (collection.name for collection in collections):
					LOGGER.debug("> Updating Collection '{0}' Name To '{1}'.".format(identity, currentText))
					collection = dbUtilities.common.filterCollections(self._coreDb.dbSession, "^{0}$".format(identity), "id")[0]
					collection.name = str(currentText)
					dbUtilities.common.commit(self._coreDb.dbSession)
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Collection Name Already Exists In Database!".format(self.__class__.__name__, currentText))
			elif startIndex.column() == 2:
				LOGGER.debug("> Updating Collection '{0}' Comment To '{1}'.".format(identity, currentText))
				collection = dbUtilities.common.filterCollections(self._coreDb.dbSession, "^{0}$".format(identity), "id")[0]
				collection.comment = str(currentText)
				dbUtilities.common.commit(self._coreDb.dbSession)

		self.Collections_Outliner_treeView_refreshModel()

	@core.executionTrace
	def Collections_Outliner_treeView_setView(self):
		"""
		This Method Sets The Collections_Outliner_treeView View.
		"""

		LOGGER.debug("> Initializing '{0}' Widget!".format("Collections_Outliner_treeView"))

		self.ui.Collections_Outliner_treeView.setAutoScroll(False)
		self.ui.Collections_Outliner_treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.Collections_Outliner_treeView.setIndentation(self._treeViewIndentation)
		self.ui.Collections_Outliner_treeView.setSortingEnabled(True)

		self.ui.Collections_Outliner_treeView.setModel(self._model)

		self.Collections_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def Collections_Outliner_treeView_refreshView(self):
		"""
		This Method Refreshes The Collections_Outliner_treeView View.
		"""

		self.Collections_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def Collections_Outliner_treeView_setDefaultViewState(self):
		"""
		This Method Sets Collections_Outliner_treeView Default View State.
		"""

		LOGGER.debug("> Setting '{0}' Default View State!".format("Collections_Outliner_treeView"))

		self.ui.Collections_Outliner_treeView.expandAll()
		for column in range(len(self._modelHeaders)):
			self.ui.Collections_Outliner_treeView.resizeColumnToContents(column)

		self.ui.Collections_Outliner_treeView.sortByColumn(0, Qt.AscendingOrder)

	@core.executionTrace
	def Collections_Outliner_treeView_refreshSetsCounts(self):
		"""
		This Method Refreshes The Collections_Outliner_treeView Sets Counts.
		"""

		# Disconnecting Model "dataChanged()" Signal.
		not self._container.parameters.databaseReadOnly and self._model.dataChanged.disconnect(self.Collections_Outliner_treeView_OnModelDataChanged)

		for i in range(self._model.rowCount()):
			currentStandardItem = self._model.item(i)
			if currentStandardItem.text() == self._overallCollection:
				self._model.itemFromIndex(self._model.sibling(i, 1, self._model.indexFromItem(currentStandardItem))).setText(str(dbUtilities.common.getIblSets(self._coreDb.dbSession).count()))
			for j in range(currentStandardItem.rowCount()):
				collectionStandardItem = currentStandardItem.child(j, 0)
				collectionSetsCountStandardItem = currentStandardItem.child(j, 1)
				collectionSetsCountStandardItem.setText(str(self._coreDb.dbSession.query(dbUtilities.types.DbIblSet).filter_by(collection=collectionStandardItem._datas.id).count()))

		# Reconnecting Model "dataChanged()" Signal.
		not self._container.parameters.databaseReadOnly and self._model.dataChanged.connect(self.Collections_Outliner_treeView_OnModelDataChanged)

	@core.executionTrace
	def Collections_Outliner_treeView_storeModelSelection(self):
		"""
		This Method Stores Collections_Outliner_treeView Model Selection.
		"""

		LOGGER.debug("> Storing '{0}' Model Selection!".format("Collections_Outliner_treeView"))

		self._modelSelection = { self._overallCollection:[], "Collections":[] }
		for item in self.getSelectedItems():
			if item._type == self._overallCollection:
				self._modelSelection[self._overallCollection].append(item.text())
			elif item._type == "Collection":
				self._modelSelection["Collections"].append(item._datas.id)

	@core.executionTrace
	def Collections_Outliner_treeView_restoreModelSelection(self):
		"""
		This Method Restores Collections_Outliner_treeView Model Selection.
		"""

		LOGGER.debug("> Restoring '{0}' Model Selection!".format("Collections_Outliner_treeView"))

		indexes = []
		for i in range(self._model.rowCount()):
			overallCollectionStandardItem = self._model.item(i)
			overallCollectionStandardItem.text() in self._modelSelection["Overall"] and indexes.append(self._model.indexFromItem(overallCollectionStandardItem))
			for j in range(overallCollectionStandardItem.rowCount()):
				collectionStandardItem = overallCollectionStandardItem.child(j, 0)
				collectionStandardItem._datas.id in self._modelSelection["Collections"] and indexes.append(self._model.indexFromItem(collectionStandardItem))

		selectionModel = self.ui.Collections_Outliner_treeView.selectionModel()
		if selectionModel:
			selectionModel.clear()
			for index in indexes:
				selectionModel.setCurrentIndex(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

	@core.executionTrace
	def Collections_Outliner_treeView_setActions(self):
		"""
		This Method Sets The Collections Outliner Actions.
		"""

		if not self._container.parameters.databaseReadOnly:
			addContentAction = QAction("Add Content ...", self.ui.Collections_Outliner_treeView)
			addContentAction.triggered.connect(self.Collections_Outliner_treeView_addContentAction)
			self.ui.Collections_Outliner_treeView.addAction(addContentAction)

			addCollectionAction = QAction("Add Collection ...", self.ui.Collections_Outliner_treeView)
			addCollectionAction.triggered.connect(self.Collections_Outliner_treeView_addCollectionAction)
			self.ui.Collections_Outliner_treeView.addAction(addCollectionAction)

			removeCollectionsAction = QAction("Remove Collection(s) ...", self.ui.Collections_Outliner_treeView)
			removeCollectionsAction.triggered.connect(self.Collections_Outliner_treeView_removeCollectionsAction)
			self.ui.Collections_Outliner_treeView.addAction(removeCollectionsAction)
		else:
			LOGGER.info("{0} | Collections Database Alteration Capabilities Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def Collections_Outliner_treeView_addContentAction(self, checked):
		"""
		This Method Is Triggered By addContentAction.

		@param checked: Action Checked State. ( Boolean )
		"""

		collection = self.addCollection()
		if collection:
			self.Collections_Outliner_treeView_refreshModel()
			fileDialog = QFileDialog(self)
			directory = self._container.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self, "Add Content:", self._container.lastBrowsedPath)))
			if directory:
				LOGGER.debug("> Chosen Directory Path: '{0}'.".format(directory))
				self.coreDatabaseBrowser.addDirectory(directory, self.getCollectionId(collection))
				self.ui.Collections_Outliner_treeView.selectionModel().setCurrentIndex(self._model.indexFromItem(self._model.findItems(collection, Qt.MatchExactly | Qt.MatchRecursive, 0)[0]), QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
				self.Collections_Outliner_treeView_refreshSetsCounts()

	@core.executionTrace
	def Collections_Outliner_treeView_addCollectionAction(self, checked):
		"""
		This Method Is Triggered By addCollectionAction.

		@param checked: Action Checked State. ( Boolean )
		"""

		collection = self.addCollection()
		if collection:
			self.Collections_Outliner_treeView_refreshModel()

	@core.executionTrace
	def Collections_Outliner_treeView_removeCollectionsAction(self, checked):
		"""
		This Method Is Triggered By removeCollectionsAction.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.removeCollections()
		self.Collections_Outliner_treeView_refreshModel()
		self._coreDatabaseBrowser.Database_Browser_listView_localRefreshModel()

	@core.executionTrace
	def Collections_Outliner_treeView_OnModelSelectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Triggers The Database_Browser_listView Refresh Depending On The Collections Outliner Selected Items.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""

		self._coreDatabaseBrowser.Database_Browser_listView_localRefreshModel()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def addCollection(self):
		"""
		This Method Adds A Collection To The Database.
		
		@return: Addition Success. ( Boolean )
		"""

		dialogMessage = "Enter Your Collection Name!"
		collectionInformations = QInputDialog.getText(self, "Add Collection", dialogMessage)
		if collectionInformations[0]:
			LOGGER.debug("> Chosen Collection Name: '{0}'.".format(collectionInformations[0]))
			collectionInformations = str(collectionInformations[0]).split(",")
			collection = collectionInformations[0].strip()
			comment = len(collectionInformations) == 1 and "Double Click To Set A Comment!" or collectionInformations[1].strip()
			if not set(dbUtilities.common.filterCollections(self._coreDb.dbSession, "^{0}$".format(collection), "name")).intersection(dbUtilities.common.filterCollections(self._coreDb.dbSession, "Sets", "type")):
				LOGGER.info("{0} | Adding '{1}' Collection To Database!".format(self.__class__.__name__, collection))
				return dbUtilities.common.addCollection(self._coreDb.dbSession, collection, "Sets", comment) and collection
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Collection Already Exists In Database!".format(self.__class__.__name__, collection))
		else:
			if collectionInformations[1]: 
				raise foundations.exceptions.UserError, "{0} | Exception While Adding A Collection To Database: Cannot Add A Collection With Empty Name!".format(self.__class__.__name__)

	@core.executionTrace
	def addDefaultCollection(self):
		"""
		This Method Adds A Default Collection To The Database.
		
		@return: Addition Success. ( Boolean )
		"""

		collections = [collection for collection in dbUtilities.common.filterCollections(self._coreDb.dbSession, "Sets", "type")]

		if not collections:
			LOGGER.info("{0} | Adding '{1}' Collection To Database!".format(self.__class__.__name__, self._defaultCollection))
			dbUtilities.common.addCollection(self._coreDb.dbSession, self._defaultCollection, "Sets", "Default Collection")
			self.Collections_Outliner_treeView_refreshModel()

	@core.executionTrace
	def removeCollections(self):
		"""
		This Method Removes Collections From The Database.
		"""

		selectedCollections = self.getSelectedItems()

		if self._overallCollection in (str(collection.text()) for collection in selectedCollections) or self._defaultCollection in (str(collection.text()) for collection in selectedCollections):
			messageBox.messageBox("Warning", "Warning", "{0} | Cannot Remove '{1}' Or '{2}' Collection!".format(self.__class__.__name__, self._overallCollection, self._defaultCollection))

		selectedCollections = [collection for collection in self.getSelectedCollections() if collection.text() != self._defaultCollection]
		if selectedCollections:
			if messageBox.messageBox("Question", "Question", "Are You Sure You Want To Remove '{0}' Collection(s)?".format(", ".join((str(collection.text()) for collection in selectedCollections))), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
				iblSets = dbUtilities.common.getCollectionsSets(self._coreDb.dbSession, self.getSelectedCollectionsIds())
				for iblSet in iblSets:
					LOGGER.info("{0} | Moving '{1}' Ibl Set To Default Collection!".format(self.__class__.__name__, iblSet.name))
					iblSet.collection = self.getCollectionId(self._defaultCollection)
				for collection in selectedCollections:
					LOGGER.info("{0} | Removing '{1}' Collection From Database!".format(self.__class__.__name__, collection.text()))
					dbUtilities.common.removeCollection(self._coreDb.dbSession, str(collection._datas.id))

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This Method Returns The Collections_Outliner_treeView Selected Items.
		
		@param rowsRootOnly: Return Rows Roots Only. ( Boolean )
		@return: View Selected Items. ( List )
		"""

		selectedIndexes = self.ui.Collections_Outliner_treeView.selectedIndexes()

		return rowsRootOnly and [item for item in set([self._model.itemFromIndex(self._model.sibling(index.row(), 0, index)) for index in selectedIndexes])] or [self._model.itemFromIndex(index) for index in selectedIndexes]

	@core.executionTrace
	def getSelectedCollections(self):
		"""
		This Method Gets Selected Collections.
	
		@return: Selected Collections. ( List )
		"""

		selectedCollections = [item for item in self.getSelectedItems() if item._type == "Collection"]
		return selectedCollections and selectedCollections or None

	@core.executionTrace
	def getSelectedCollectionsIds(self):
		"""
		This Method Gets Selected Collections Ids.
	
		@return: Collections Ids. ( List )
		"""

		selectedCollections = self.getSelectedCollections()

		ids = []
		if selectedCollections:
			ids = [collection._datas.id for collection in selectedCollections]
			return ids == [] and ids.append(self.getCollectionId(self._defaultCollection)) or ids
		else:
			return ids

	@core.executionTrace
	def getCollectionId(self, collection):
		"""
		This Method Returns The Provided Collection Id.

		@param collection: Collection To Get The Id From. ( String )
		@return: Provided Collection Id. ( Integer )
		"""

		return self._model.findItems(collection, Qt.MatchExactly | Qt.MatchRecursive, 0)[0]._datas.id

	@core.executionTrace
	def getCollectionsSets(self):
		"""
		This Method Gets The Sets Associated To Selected Collections.
		
		@return: Sets List. ( List )
		"""

		selectedCollections = self.getSelectedCollections()
		allIds = [collection._datas.id for collection in self._model.findItems(".*", Qt.MatchRegExp | Qt.MatchRecursive, 0) if collection._type == "Collection"]
		ids = selectedCollections and (self._overallCollection in (collection.text() for collection in selectedCollections) and allIds or self.getSelectedCollectionsIds()) or allIds

		return dbUtilities.common.getCollectionsSets(self._coreDb.dbSession, ids)

	@core.executionTrace
	def getUniqueCollectionId(self):
		"""
		This Method Returns A Unique Collection Id ( Either First Selected Collection Or Default One).

		@return: Unique Id. ( String )
		"""

		selectedCollectionsIds = self.getSelectedCollectionsIds()
		if not len(selectedCollectionsIds):
			return self.getCollectionId(self._defaultCollection)
		else:
			len(selectedCollectionsIds) > 1 and LOGGER.warning("!> {0} | Multiple Collection Selected, Using '{1}' Id!".format(self.__class__.__name__, selectedCollectionsIds[0]))
			return selectedCollectionsIds[0]

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
