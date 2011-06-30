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
import logging
import os
import platform
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.common
import dbUtilities.types
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
		self.__container = container

		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreCollectionsOutliner = self.__container.componentsManager.components["core.collectionsOutliner"].interface

		self.__previousCollection = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

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

		@return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

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

		@return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

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

		@return: self.__coreCollectionsOutliner. ( Object )
		"""

		return self.__coreCollectionsOutliner

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

		@return: self.__previousCollection. ( String )
		"""

		return self.__previousCollection

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

		if not self.__container.parameters.databaseReadOnly:
			if event.mimeData().hasUrls():
				LOGGER.debug("> Drag Event Urls List: '{0}'!".format(event.mimeData().urls()))
				for url in event.mimeData().urls():
					path = (platform.system() == "Windows" or platform.system() == "Microsoft") and re.search("^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
					if re.search("\.{0}$".format(self.__coreDatabaseBrowser.extension), str(url.path())):
						name = foundations.strings.getSplitextBasename(path)
						if messageBox.messageBox("Question", "Question", "'{0}' Ibl Set File Has Been Dropped, Would You Like To Add It To The Database?".format(name), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
							self.__coreDatabaseBrowser.addIblSet(name, path)
					else:
						if os.path.isdir(path):
							if messageBox.messageBox("Question", "Question", "'{0}' Directory Has Been Dropped, Would You Like To Add Its Content To The Database?".format(path), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
								self.__coreDatabaseBrowser.addDirectory(path)
						else:
							raise OSError, "{0} | Exception Raised While Parsing '{1}' Path: Syntax Is Invalid!".format(self.__class__.__name__, path)
			else:
				indexAt = self.indexAt(event.pos())
				itemAt = self.model().itemFromIndex(indexAt)

				if itemAt:
					LOGGER.debug("> Item At Drop Position: '{0}'.".format(itemAt))
					collectionStandardItem = self.model().itemFromIndex(self.model().sibling(indexAt.row(), 0, indexAt))
					if collectionStandardItem.text() != self.__coreCollectionsOutliner.overallCollection:
						iblSets = self.__coreDatabaseBrowser.getSelectedItems()
						for iblSet in iblSets:
							LOGGER.info("> Moving '{0}' Ibl Set To '{1}' Collection.".format(iblSet._datas.name, collectionStandardItem._datas.name))
							iblSet._datas.collection = collectionStandardItem._datas.id
						if dbUtilities.common.commit(self.__coreDb.dbSession):
							self.__coreCollectionsOutliner.ui.Collections_Outliner_treeView.selectionModel().setCurrentIndex(indexAt, QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only!".format(self.__class__.__name__)

	@core.executionTrace
	def __QTreeView__clicked(self, index):
		"""
		This Method Defines The Behavior When The Model Is Clicked.
		
		@param index: Clicked Model Item Index. ( QModelIndex )
		"""

		self.__previousCollection = self.model().itemFromIndex(self.model().sibling(index.row(), 0, index)).text()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __QTreeView__doubleClicked(self, index):
		"""
		This Method Defines The Behavior When A QStandardItem Is Double Clicked.
		
		@param index: Clicked Model Item Index. ( QModelIndex )
		"""

		if not self.__container.parameters.databaseReadOnly:
			collectionStandardItem = self.model().itemFromIndex(self.model().sibling(index.row(), 0, index))

			if collectionStandardItem.text() != self.__coreCollectionsOutliner.defaultCollection and collectionStandardItem.text() != self.__coreCollectionsOutliner.overallCollection:
				if self.model().itemFromIndex(index).column() == self.__coreCollectionsOutliner.modelHeaders.index(self.__coreCollectionsOutliner.setsCountLabel):
					messageBox.messageBox("Warning", "Warning", "{0} | 'Sets Counts' Column Is Read Only!".format(self.__class__.__name__))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' And '{2}' Collections Attributes Are Read Only!".format(self.__class__.__name__, self.__coreCollectionsOutliner.overallCollection, self.__coreCollectionsOutliner.defaultCollection))
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only!".format(self.__class__.__name__)

class CollectionsOutliner(UiComponent):
	"""
	This Class Is The CollectionsOutliner Class.
	"""

	# Custom Signals Definitions.
	modelChanged = pyqtSignal()
	modelRefresh = pyqtSignal()
	modelPartialRefresh = pyqtSignal()

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

		self.__uiPath = "ui/Collections_Outliner.ui"
		self.__uiResources = "resources"
		self.__uiDefaultCollectionImage = "Default_Collection.png"
		self.__uiUserCollectionImage = "User_Collection.png"
		self.__dockArea = 1

		self.__container = None
		self.__settings = None
		self.__settingsSection = None
		self.__settingsSeparator = ","

		self.__coreDb = None
		self.__coreDatabaseBrowser = None

		self.__model = None
		self.__modelSelection = None

		self.__overallCollection = "Overall"
		self.__defaultCollection = "Default"
		self.__setsCountLabel = "Sets"
		self.__modelHeaders = [ "Collections", self.__setsCountLabel, "Comment" ]
		self.__treeViewIndentation = 15

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

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

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

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
	def uiDefaultCollectionImage(self):
		"""
		This Method Is The Property For The _uiDefaultCollectionImage Attribute.

		@return: self.__uiDefaultCollectionImage. ( String )
		"""

		return self.__uiDefaultCollectionImage

	@uiDefaultCollectionImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self, value):
		"""
		This Method Is The Setter Method For The _uiDefaultCollectionImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiDefaultCollectionImage"))

	@uiDefaultCollectionImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDefaultCollectionImage(self):
		"""
		This Method Is The Deleter Method For The _uiDefaultCollectionImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiDefaultCollectionImage"))

	@property
	def uiUserCollectionImage(self):
		"""
		This Method Is The Property For The _uiUserCollectionImage Attribute.

		@return: self.__uiUserCollectionImage. ( String )
		"""

		return self.__uiUserCollectionImage

	@uiUserCollectionImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self, value):
		"""
		This Method Is The Setter Method For The _uiUserCollectionImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiUserCollectionImage"))

	@uiUserCollectionImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUserCollectionImage(self):
		"""
		This Method Is The Deleter Method For The _uiUserCollectionImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiUserCollectionImage"))

	@property
	def dockArea(self):
		"""
		This Method Is The Property For The _dockArea Attribute.

		@return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

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

		@return: self.__container. ( QObject )
		"""

		return self.__container

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

		@return: self.__settings. ( QSettings )
		"""

		return self.__settings

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

		@return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

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

		@return: self.__settingsSeparator. ( String )
		"""

		return self.__settingsSeparator

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

		@return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

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

		@return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

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

		@return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

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

		@return: self.__modelSelection. ( Dictionary )
		"""

		return self.__modelSelection

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

		@return: self.__overallCollection. ( String )
		"""

		return self.__overallCollection

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

		@return: self.__defaultCollection. ( String )
		"""

		return self.__defaultCollection

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

		@return: self.__setsCountLabel. ( String )
		"""

		return self.__setsCountLabel

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

		@return: self.__modelHeaders. ( List )
		"""

		return self.__modelHeaders

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

		@return: self.__treeViewIndentation. ( Integer )
		"""

		return self.__treeViewIndentation

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

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Cannot Be Deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__container.parameters.databaseReadOnly and	LOGGER.info("{0} | Collections_Outliner_treeView Model Edition Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))
		self.__model = QStandardItemModel()
		self.__Collections_Outliner_treeView_setModel()

		self.ui.Collections_Outliner_treeView = CollectionsOutliner_QTreeView(self.__container)
		self.ui.Collections_Outliner_dockWidgetContents_gridLayout.addWidget(self.ui.Collections_Outliner_treeView, 0, 0)

		self.ui.Collections_Outliner_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Collections_Outliner_treeView_addActions()

		self.__Collections_Outliner_treeView_setView()

		# Signals / Slots.
		self.ui.Collections_Outliner_treeView.selectionModel().selectionChanged.connect(self.__Collections_Outliner_treeView_selectionModel__selectionChanged)
		self.ui.Collections_Outliner_treeView.clicked.connect(self.ui.Collections_Outliner_treeView._CollectionsOutliner_QTreeView__QTreeView__clicked)
		self.ui.Collections_Outliner_treeView.doubleClicked.connect(self.ui.Collections_Outliner_treeView._CollectionsOutliner_QTreeView__QTreeView__doubleClicked)
		self.modelChanged.connect(self.__Collections_Outliner_treeView_refreshView)
		self.modelRefresh.connect(self.__Collections_Outliner_treeView_refreshModel)
		self.modelPartialRefresh.connect(self.__Collections_Outliner_treeView_setIblSetsCounts)
		not self.__container.parameters.databaseReadOnly and self.__model.dataChanged.connect(self.__Collections_Outliner_treeView_model__dataChanged)

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

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

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

		if not self.__container.parameters.databaseReadOnly:
			self.addDefaultCollection()
		else:
			LOGGER.info("{0} | Database Default Collection Wizard Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeCollectionsIds = str(self.__settings.getKey(self.__settingsSection, "activeCollections").toString())
		LOGGER.debug("> Stored '{0}' Active Collections Ids Selection: '{1}'.".format(self.__class__.__name__, activeCollectionsIds))
		if activeCollectionsIds:
			if self.__settingsSeparator in activeCollectionsIds:
				ids = activeCollectionsIds.split(self.__settingsSeparator)
			else:
				ids = [activeCollectionsIds]
			self.__modelSelection["Collections"] = [int(id) for id in ids]

		activeOverallCollection = str(self.__settings.getKey(self.__settingsSection, "activeOverallCollection").toString())
		LOGGER.debug("> Stored '{0}' Active Overall Collection Selection: '{1}'.".format(self.__class__.__name__, activeOverallCollection))
		if activeOverallCollection:
			self.__modelSelection[self.__overallCollection] = [activeOverallCollection]

		self.__Collections_Outliner_treeView_restoreModelSelection()

	@core.executionTrace
	def onClose(self):
		"""
		This Method Is Called On Framework Close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework Close Method.".format(self.__class__.__name__))

		self.__Collections_Outliner_treeView_storeModelSelection()
		self.__settings.setKey(self.__settingsSection, "activeCollections", self.__settingsSeparator.join((str(id) for id in self.__modelSelection["Collections"])))
		self.__settings.setKey(self.__settingsSection, "activeOverallCollection", self.__settingsSeparator.join((str(id) for id in self.__modelSelection[self.__overallCollection])))

	@core.executionTrace
	def __Collections_Outliner_treeView_setModel(self):
		"""
		This Method Sets The Collections_Outliner_treeView Model.

		Columns:
		Collections | Sets | Comment
		
		Rows:
		* Overall Collection: { _type: "Overall" }
		** Collection: { _type: "Collection", _datas: dbUtilities.types.DbCollection }
		"""

		LOGGER.debug("> Setting Up '{0}' Model!".format("Collections_Outliner_treeView"))

		self.__Collections_Outliner_treeView_storeModelSelection()

		self.__model.clear()

		self.__model.setHorizontalHeaderLabels(self.__modelHeaders)
		self.__model.setColumnCount(len(self.__modelHeaders))
		readOnlyFlags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

		LOGGER.debug("> Preparing '{0}' Collection For '{1}' Model.".format(self.__overallCollection, "Collections_Outliner_treeView"))

		overallCollectionStandardItem = QStandardItem(QString(self.__overallCollection))
		overallCollectionStandardItem.setFlags(readOnlyFlags)

		overallCollectionSetsCountStandardItem = QStandardItem(QString(str(dbUtilities.common.getIblSets(self.__coreDb.dbSession).count())))
		overallCollectionSetsCountStandardItem.setTextAlignment(Qt.AlignCenter)
		overallCollectionSetsCountStandardItem.setFlags(readOnlyFlags)

		overallCollectionCommentsStandardItem = QStandardItem()
		overallCollectionCommentsStandardItem.setFlags(readOnlyFlags)

		overallCollectionStandardItem._type = "Overall"

		LOGGER.debug("> Adding '{0}' Collection To '{1}'.".format(self.__overallCollection, "Collections_Outliner_treeView"))
		self.__model.appendRow([overallCollectionStandardItem, overallCollectionSetsCountStandardItem, overallCollectionCommentsStandardItem])

		collections = dbUtilities.common.filterCollections(self.__coreDb.dbSession, "Sets", "type")

		if collections:
			for collection in collections:
				LOGGER.debug("> Preparing '{0}' Collection For '{1}' Model.".format(collection.name, "Collections_Outliner_treeView"))

				try:
					collectionStandardItem = QStandardItem(QString(collection.name))
					iconPath = collection.name == self.defaultCollection and os.path.join(self.__uiResources, self.__uiDefaultCollectionImage) or os.path.join(self.__uiResources, self.__uiUserCollectionImage)
					collectionStandardItem.setIcon(QIcon(iconPath))
					(collection.name == self.__defaultCollection or self.__container.parameters.databaseReadOnly) and collectionStandardItem.setFlags(readOnlyFlags)

					collectionSetsCountStandardItem = QStandardItem(QString(str(self.__coreDb.dbSession.query(dbUtilities.types.DbIblSet).filter_by(collection=collection.id).count())))
					collectionSetsCountStandardItem.setTextAlignment(Qt.AlignCenter)
					collectionSetsCountStandardItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

					collectionCommentsStandardItem = QStandardItem(QString(collection.comment))
					(collection.name == self.__defaultCollection or self.__container.parameters.databaseReadOnly) and collectionCommentsStandardItem.setFlags(readOnlyFlags)

					collectionStandardItem._datas = collection
					collectionStandardItem._type = "Collection"

					LOGGER.debug("> Adding '{0}' Collection To '{1}' Model.".format(collection.name, "Collections_Outliner_treeView"))
					overallCollectionStandardItem.appendRow([collectionStandardItem, collectionSetsCountStandardItem, collectionCommentsStandardItem])

				except Exception as error:
					LOGGER.error("!>{0} | Exception Raised While Adding '{1}' Collection To '{2}' Model!".format(self.__class__.__name__, collection.name, "Collections_Outliner_treeView"))
					foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "Collections_Outliner_treeView"))
		else:
			LOGGER.info("{0} | Database Has No User Defined Collections!".format(self.__class__.__name__))

		self.__Collections_Outliner_treeView_restoreModelSelection()
		self.emit(SIGNAL("modelChanged()"))

	@core.executionTrace
	def __Collections_Outliner_treeView_refreshModel(self):
		"""
		This Method Refreshes The Collections_Outliner_treeView Model.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Collections_Outliner_treeView"))

		self.__Collections_Outliner_treeView_setModel()

	@core.executionTrace
	def __Collections_Outliner_treeView_setView(self):
		"""
		This Method Sets The Collections_Outliner_treeView View.
		"""

		LOGGER.debug("> Initializing '{0}' Widget!".format("Collections_Outliner_treeView"))

		self.ui.Collections_Outliner_treeView.setAutoScroll(False)
		self.ui.Collections_Outliner_treeView.setIndentation(self.__treeViewIndentation)
		self.ui.Collections_Outliner_treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.Collections_Outliner_treeView.setSortingEnabled(True)

		self.ui.Collections_Outliner_treeView.setModel(self.__model)

		self.__Collections_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def __Collections_Outliner_treeView_setDefaultViewState(self):
		"""
		This Method Sets Collections_Outliner_treeView Default View State.
		"""

		LOGGER.debug("> Setting '{0}' Default View State!".format("Collections_Outliner_treeView"))

		self.ui.Collections_Outliner_treeView.expandAll()
		for column in range(len(self.__modelHeaders)):
			self.ui.Collections_Outliner_treeView.resizeColumnToContents(column)

		self.ui.Collections_Outliner_treeView.sortByColumn(0, Qt.AscendingOrder)

	@core.executionTrace
	def __Collections_Outliner_treeView_setIblSetsCounts(self):
		"""
		This Method Sets The Collections_Outliner_treeView Ibl Sets Counts.
		"""

		# Disconnecting Model "dataChanged()" Signal.
		not self.__container.parameters.databaseReadOnly and self.__model.dataChanged.disconnect(self.__Collections_Outliner_treeView_model__dataChanged)

		for i in range(self.__model.rowCount()):
			currentStandardItem = self.__model.item(i)
			if currentStandardItem.text() == self.__overallCollection:
				self.__model.itemFromIndex(self.__model.sibling(i, 1, self.__model.indexFromItem(currentStandardItem))).setText(str(dbUtilities.common.getIblSets(self.__coreDb.dbSession).count()))
			for j in range(currentStandardItem.rowCount()):
				collectionStandardItem = currentStandardItem.child(j, 0)
				collectionSetsCountStandardItem = currentStandardItem.child(j, 1)
				collectionSetsCountStandardItem.setText(str(self.__coreDb.dbSession.query(dbUtilities.types.DbIblSet).filter_by(collection=collectionStandardItem._datas.id).count()))

		# Reconnecting Model "dataChanged()" Signal.
		not self.__container.parameters.databaseReadOnly and self.__model.dataChanged.connect(self.__Collections_Outliner_treeView_model__dataChanged)

	@core.executionTrace
	def __Collections_Outliner_treeView_refreshView(self):
		"""
		This Method Refreshes The Collections_Outliner_treeView View.
		"""

		self.__Collections_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def __Collections_Outliner_treeView_storeModelSelection(self):
		"""
		This Method Stores Collections_Outliner_treeView Model Selection.
		"""

		LOGGER.debug("> Storing '{0}' Model Selection!".format("Collections_Outliner_treeView"))

		self.__modelSelection = { self.__overallCollection:[], "Collections":[] }
		for item in self.getSelectedItems():
			if item._type == self.__overallCollection:
				self.__modelSelection[self.__overallCollection].append(item.text())
			elif item._type == "Collection":
				self.__modelSelection["Collections"].append(item._datas.id)

	@core.executionTrace
	def __Collections_Outliner_treeView_restoreModelSelection(self):
		"""
		This Method Restores Collections_Outliner_treeView Model Selection.
		"""

		LOGGER.debug("> Restoring '{0}' Model Selection!".format("Collections_Outliner_treeView"))

		indexes = []
		for i in range(self.__model.rowCount()):
			overallCollectionStandardItem = self.__model.item(i)
			overallCollectionStandardItem.text() in self.__modelSelection["Overall"] and indexes.append(self.__model.indexFromItem(overallCollectionStandardItem))
			for j in range(overallCollectionStandardItem.rowCount()):
				collectionStandardItem = overallCollectionStandardItem.child(j, 0)
				collectionStandardItem._datas.id in self.__modelSelection["Collections"] and indexes.append(self.__model.indexFromItem(collectionStandardItem))

		selectionModel = self.ui.Collections_Outliner_treeView.selectionModel()
		if selectionModel:
			selectionModel.clear()
			for index in indexes:
				selectionModel.setCurrentIndex(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

	@core.executionTrace
	def __Collections_Outliner_treeView_addActions(self):
		"""
		This Method Sets The Collections Outliner Actions.
		"""

		if not self.__container.parameters.databaseReadOnly:
			addContentAction = QAction("Add Content ...", self.ui.Collections_Outliner_treeView)
			addContentAction.triggered.connect(self.__Collections_Outliner_treeView_addContentAction__triggered)
			self.ui.Collections_Outliner_treeView.addAction(addContentAction)

			addSingleCollectionAction = QAction("Add Collection ...", self.ui.Collections_Outliner_treeView)
			addSingleCollectionAction.triggered.connect(self.__Collections_Outliner_treeView_addCollectionAction__triggered)
			self.ui.Collections_Outliner_treeView.addAction(addSingleCollectionAction)

			removeCollectionsAction = QAction("Remove Collection(s) ...", self.ui.Collections_Outliner_treeView)
			removeCollectionsAction.triggered.connect(self.__Collections_Outliner_treeView_removeCollectionsAction__triggered)
			self.ui.Collections_Outliner_treeView.addAction(removeCollectionsAction)
		else:
			LOGGER.info("{0} | Collections Database Alteration Capabilities Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __Collections_Outliner_treeView_addContentAction__triggered(self, checked):
		"""
		This Method Is Triggered By addContentAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.addUserContent()

	@core.executionTrace
	def __Collections_Outliner_treeView_addCollectionAction__triggered(self, checked):
		"""
		This Method Is Triggered By addSingleCollectionAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.addUserCollection()

	@core.executionTrace
	def __Collections_Outliner_treeView_removeCollectionsAction__triggered(self, checked):
		"""
		This Method Is Triggered By removeCollectionsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.removeUserCollections()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __Collections_Outliner_treeView_model__dataChanged(self, startIndex, endIndex):
		"""
		This Method Defines The Behavior When The Collections_Outliner_treeView Model Data Change.
		
		@param startIndex: Edited Item Starting QModelIndex. ( QModelIndex )
		@param endIndex: Edited Item Ending QModelIndex. ( QModelIndex )
		"""

		standardItem = self.__model.itemFromIndex(startIndex)
		currentText = standardItem.text()

		if currentText:
			collectionStandardItem = self.__model.itemFromIndex(self.__model.sibling(startIndex.row(), 0, startIndex))

			identity = collectionStandardItem._type == "Collection" and collectionStandardItem._datas.id or None
			collections = [collection for collection in dbUtilities.common.filterCollections(self.__coreDb.dbSession, "Sets", "type")]
			if identity and collections:
				if startIndex.column() == 0:
					if currentText not in (collection.name for collection in collections):
						LOGGER.debug("> Updating Collection '{0}' Name To '{1}'.".format(identity, currentText))
						collection = dbUtilities.common.filterCollections(self.__coreDb.dbSession, "^{0}$".format(identity), "id")[0]
						collection.name = str(currentText)
						dbUtilities.common.commit(self.__coreDb.dbSession)
					else:
						messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Collection Name Already Exists In Database!".format(self.__class__.__name__, currentText))
				elif startIndex.column() == 2:
					LOGGER.debug("> Updating Collection '{0}' Comment To '{1}'.".format(identity, currentText))
					collection = dbUtilities.common.filterCollections(self.__coreDb.dbSession, "^{0}$".format(identity), "id")[0]
					collection.comment = str(currentText)
					dbUtilities.common.commit(self.__coreDb.dbSession)
		else:
			raise foundations.exceptions.UserError, "{0} | Exception While Editing A Collection Field: Cannot Use An Empty Value!".format(self.__class__.__name__)
		self.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	def __Collections_Outliner_treeView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Triggers The Database_Browser_listView Refresh Depending On The Collections Outliner Selected Items.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""
		self.__coreDatabaseBrowser.emit(SIGNAL("modelDatasRefresh()"))
		self.__coreDatabaseBrowser.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	def __coreDatabaseBrowser_Database_Browser_listView_setModelContent(self):
		"""
		This Method Sets coreDatabaseBrowser Model Content.
		"""

		self.__coreDatabaseBrowser.modelContent = self.getSelectedCollectionsIblSets()

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This Method Returns The Collections_Outliner_treeView Selected Items.
		
		@param rowsRootOnly: Return Rows Roots Only. ( Boolean )
		@return: View Selected Items. ( List )
		"""

		selectedIndexes = self.ui.Collections_Outliner_treeView.selectedIndexes()

		return rowsRootOnly and [item for item in set([self.__model.itemFromIndex(self.__model.sibling(index.row(), 0, index)) for index in selectedIndexes])] or [self.__model.itemFromIndex(index) for index in selectedIndexes]

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
			return ids == [] and ids.append(self.getCollectionId(self.__defaultCollection)) or ids
		else:
			return ids

	@core.executionTrace
	def getSelectedCollectionsIblSets(self):
		"""
		This Method Gets The Ibl Sets Associated To Selected Collections.
		
		@return: Sets List. ( List )
		"""

		selectedCollections = self.getSelectedCollections()
		allIds = [collection._datas.id for collection in self.__model.findItems(".*", Qt.MatchRegExp | Qt.MatchRecursive, 0) if collection._type == "Collection"]
		ids = selectedCollections and (self.__overallCollection in (collection.text() for collection in selectedCollections) and allIds or self.getSelectedCollectionsIds()) or allIds

		return dbUtilities.common.getCollectionsIblSets(self.__coreDb.dbSession, ids)

	@core.executionTrace
	def getCollectionId(self, collection):
		"""
		This Method Returns The Provided Collection Id.

		@param collection: Collection To Get The Id From. ( String )
		@return: Provided Collection Id. ( Integer )
		"""

		return self.__model.findItems(collection, Qt.MatchExactly | Qt.MatchRecursive, 0)[0]._datas.id

	@core.executionTrace
	def getUniqueCollectionId(self):
		"""
		This Method Returns A Unique Collection Id ( Either First Selected Collection Or Default One).

		@return: Unique Id. ( String )
		"""

		selectedCollectionsIds = self.getSelectedCollectionsIds()
		if not len(selectedCollectionsIds):
			return self.getCollectionId(self.__defaultCollection)
		else:
			len(selectedCollectionsIds) > 1 and LOGGER.warning("!> {0} | Multiple Collection Selected, Using '{1}' Id!".format(self.__class__.__name__, selectedCollectionsIds[0]))
			return selectedCollectionsIds[0]

	@core.executionTrace
	def addUserContent(self):
		"""
		This Method Adds User Content To The Database.
		"""

		collection, state = self.addUserCollection()
		if state:
			directory = self.__container.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self, "Add Content:", self.__container.lastBrowsedPath)))
			if directory:
				LOGGER.debug("> Chosen Directory Path: '{0}'.".format(directory))
				self.__coreDatabaseBrowser.addDirectory(directory, self.getCollectionId(collection))
				self.ui.Collections_Outliner_treeView.selectionModel().setCurrentIndex(self.__model.indexFromItem(self.__model.findItems(collection, Qt.MatchExactly | Qt.MatchRecursive, 0)[0]), QItemSelectionModel.Current | QItemSelectionModel.Select | QItemSelectionModel.Rows)

	@core.executionTrace
	def	addUserCollection(self):
		"""
		This Method Adds User Collection To The Database.
		
		@return: Collection Name, Addition Success. ( String, Boolean )		
		"""

		collectionInformations, state = QInputDialog.getText(self, "Add Collection", "Enter Your Collection Name!")
		if state:
			collectionInformations = str(collectionInformations).split(",")
			name = collectionInformations[0].strip()
			comment = len(collectionInformations) == 1 and "Double Click To Set A Comment!" or collectionInformations[1].strip()
			return name, self.addCollection(name, comment)
		else:
			return collectionInformations, state

	@core.executionTrace
	def	removeUserCollections(self):
		"""
		This Method Removes User Collections From The Database.
		"""

		selectedItems = self.getSelectedItems()

		if self.__overallCollection in (str(collection.text()) for collection in selectedItems) or self.__defaultCollection in (str(collection.text()) for collection in selectedItems):
			messageBox.messageBox("Warning", "Warning", "{0} | Cannot Remove '{1}' Or '{2}' Collection!".format(self.__class__.__name__, self.__overallCollection, self.__defaultCollection))

		selectedCollections = self.getSelectedCollections()
		selectedCollections = selectedCollections and [collection._datas for collection in self.getSelectedCollections() if collection.text() != self.__defaultCollection] or None
		if selectedCollections:
			if messageBox.messageBox("Question", "Question", "Are You Sure You Want To Remove '{0}' Collection(s)?".format(", ".join((str(collection.name) for collection in selectedCollections))), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
				self.removeCollections(selectedCollections)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.ProgrammingError)
	def addCollection(self, name, comment="Double Click To Set A Comment!"):
		"""
		This Method Adds A Collection To The Database.
		
		@param name: Collection Name. ( String )
		@param collection: Collection Name. ( String )
		"""

		if name:
			LOGGER.debug("> Chosen Collection Name: '{0}'.".format(name))
			if not set(dbUtilities.common.filterCollections(self.__coreDb.dbSession, "^{0}$".format(name), "name")).intersection(dbUtilities.common.filterCollections(self.__coreDb.dbSession, "Sets", "type")):
				LOGGER.info("{0} | Adding '{1}' Collection To Database!".format(self.__class__.__name__, name))
				if dbUtilities.common.addCollection(self.__coreDb.dbSession, name, "Sets", comment):
					self.emit(SIGNAL("modelRefresh()"))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Collection Already Exists In Database!".format(self.__class__.__name__, name))
		else:
			raise foundations.exceptions.ProgrammingError, "{0} | Exception While Adding A Collection To Database: Cannot Use An Empty Name!".format(self.__class__.__name__)

	@core.executionTrace
	def addDefaultCollection(self):
		"""
		This Method Adds A Default Collection To The Database.
		"""

		collections = [collection for collection in dbUtilities.common.filterCollections(self.__coreDb.dbSession, "Sets", "type")]

		if not collections:
			LOGGER.info("{0} | Adding '{1}' Collection To Database!".format(self.__class__.__name__, self.__defaultCollection))
			dbUtilities.common.addCollection(self.__coreDb.dbSession, self.__defaultCollection, "Sets", "Default Collection")
			self.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	def removeCollections(self, collections):
		"""
		This Method Removes Collections From The Database.
		
		@param collections: Collections To Remove ( DbCollection List )
		"""

		iblSets = dbUtilities.common.getCollectionsIblSets(self.__coreDb.dbSession, [collection.id for collection in collections])
		for iblSet in iblSets:
			LOGGER.info("{0} | Moving '{1}' Ibl Set To Default Collection!".format(self.__class__.__name__, iblSet.name))
			iblSet.collection = self.getCollectionId(self.__defaultCollection)
		for collection in collections:
			LOGGER.info("{0} | Removing '{1}' Collection From Database!".format(self.__class__.__name__, collection.name))
			dbUtilities.common.removeCollection(self.__coreDb.dbSession, str(collection.id))
		self.emit(SIGNAL("modelRefresh()"))
		self.__coreDatabaseBrowser.emit(SIGNAL("modelDatasRefresh()"))

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
