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

'''
************************************************************************************************
***	searchDatabase.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Search Database Component Module.
***
***	Others:
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
import foundations.strings as strings
from globals.constants import Constants
from manager.uiComponent import UiComponent
from ui.widgets.search_QLineEdit import Search_QLineEdit

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class SearchDatabase(UiComponent):
	'''
	This Class Is The SearchDatabase Class.
	'''

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self._uiPath = "ui/Search_Database.ui"
		self._uiResources = "resources"
		self._uiSearchIcon = "Search_Icon.png"
		self._uiClearIcon = "Clear_Icon.png"
		self._uiClearClickedIcon = "Clear_Clicked_Icon.png"
		self._dockArea = 2
		self._tagsCloudListWidgetSpacing = 4

		self._container = None

		self._coreDatabaseBrowser = None
		self._coreCollectionsOutliner = None

		self._completer = None
		self._completerVisibleItemsCount = 16

		self._tagsCloudField = "In Tags Cloud "
		self._databaseFields = (("In Names", "title"),
								("In Authors", "author"),
								("In Links", "link"),
								("In Locations", "location"),
								("In Comments", "comment"),
								(self._tagsCloudField, "comment"),)

		self._cloudExcludedTags = ("^a$", "^and$", "^by$", "^for$", "^from$", "^in$", "^of$", "^on$", "^or$", "^the$", "^to$", "^with$",)

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiPath"))

	@property
	def uiResources(self):
		'''
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		'''

		return self._uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		'''
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		'''
		This Method Is The Deleter Method For The _uiResources Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiResources"))

	@property
	def uiSearchIcon(self):
		'''
		This Method Is The Property For The _uiLargestSizeIcon Attribute.

		@return: self._uiLargestSizeIcon. ( String )
		'''

		return self._uiLargestSizeIcon

	@uiSearchIcon.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchIcon(self, value):
		'''
		This Method Is The Setter Method For The _uiLargestSizeIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("uiSearchIcon"))

	@uiSearchIcon.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchIcon(self):
		'''
		This Method Is The Deleter Method For The _uiLargestSizeIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiSearchIcon"))

	@property
	def uiClearIcon(self):
		'''
		This Method Is The Property For The _uiLargestSizeIcon Attribute.

		@return: self._uiLargestSizeIcon. ( String )
		'''

		return self._uiLargestSizeIcon

	@uiClearIcon.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearIcon(self, value):
		'''
		This Method Is The Setter Method For The _uiLargestSizeIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("uiClearIcon"))

	@uiClearIcon.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearIcon(self):
		'''
		This Method Is The Deleter Method For The _uiLargestSizeIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiClearIcon"))

	@property
	def uiClearClickedIcon(self):
		'''
		This Method Is The Property For The _uiLargestSizeIcon Attribute.

		@return: self._uiLargestSizeIcon. ( String )
		'''

		return self._uiLargestSizeIcon

	@uiClearClickedIcon.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedIcon(self, value):
		'''
		This Method Is The Setter Method For The _uiLargestSizeIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("uiClearClickedIcon"))

	@uiClearClickedIcon.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedIcon(self):
		'''
		This Method Is The Deleter Method For The _uiLargestSizeIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiClearClickedIcon"))

	@property
	def dockArea(self):
		'''
		This Method Is The Property For The _dockArea Attribute.

		@return: self._dockArea. ( Integer )
		'''

		return self._dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		'''
		This Method Is The Setter Method For The _dockArea Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		'''
		This Method Is The Deleter Method For The _dockArea Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("dockArea"))

	@property
	def tagsCloudListWidgetSpacing(self):
		'''
		This Method Is The Property For The _tagsCloudListWidgetSpacing Attribute.

		@return: self._tagsCloudListWidgetSpacing. ( Integer )
		'''

		return self._tagsCloudListWidgetSpacing

	@tagsCloudListWidgetSpacing.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudListWidgetSpacing(self, value):
		'''
		This Method Is The Setter Method For The _tagsCloudListWidgetSpacing Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("tagsCloudListWidgetSpacing"))

	@tagsCloudListWidgetSpacing.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudListWidgetSpacing(self):
		'''
		This Method Is The Deleter Method For The _tagsCloudListWidgetSpacing Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("tagsCloudListWidgetSpacing"))

	@property
	def container(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("container"))

	@property
	def coreDb(self):
		'''
		This Method Is The Property For The _coreDb Attribute.

		@return: self._coreDb. ( Object )
		'''

		return self._coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		'''
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		'''
		This Method Is The Deleter Method For The _coreDb Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("coreDb"))

	@property
	def coreDatabaseBrowser(self):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("coreDatabaseBrowser"))

	@property
	def coreCollectionsOutliner(self):
		'''
		This Method Is The Property For The _coreCollectionsOutliner Attribute.

		@return: self._coreCollectionsOutliner. ( Object )
		'''

		return self._coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		'''
		This Method Is The Setter Method For The _coreCollectionsOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		'''
		This Method Is The Deleter Method For The _coreCollectionsOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("coreCollectionsOutliner"))

	@property
	def completer(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QCompleter )
		'''

		return self._container

	@completer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QCompleter )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("completer"))

	@completer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("completer"))

	@property
	def completerVisibleItemsCount(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( Integer )
		'''

		return self._container

	@completerVisibleItemsCount.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("completerVisibleItemsCount"))

	@completerVisibleItemsCount.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("completerVisibleItemsCount"))

	@property
	def tagsCloudField(self):
		'''
		This Method Is The Property For The _tagsCloudField Attribute.

		@return: self._tagsCloudField. ( String )
		'''

		return self._tagsCloudField

	@tagsCloudField.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudField(self, value):
		'''
		This Method Is The Setter Method For The _tagsCloudField Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("tagsCloudField"))

	@tagsCloudField.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudField(self):
		'''
		This Method Is The Deleter Method For The _tagsCloudField Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("tagsCloudField"))

	@property
	def databaseFields(self):
		'''
		This Method Is The Property For The _databaseFields Attribute.

		@return: self._databaseFields. ( List )
		'''

		return self._databaseFields

	@databaseFields.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseFields(self, value):
		'''
		This Method Is The Setter Method For The _databaseFields Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("databaseFields"))

	@databaseFields.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseFields(self):
		'''
		This Method Is The Deleter Method For The _databaseFields Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("databaseFields"))

	@property
	def cloudExcludedTags(self):
		'''
		This Method Is The Property For The _cloudExcludedTags Attribute.

		@return: self._cloudExcludedTags. ( List )
		'''

		return self._cloudExcludedTags

	@cloudExcludedTags.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self, value):
		'''
		This Method Is The Setter Method For The _cloudExcludedTags Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("cloudExcludedTags"))

	@cloudExcludedTags.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self):
		'''
		This Method Is The Deleter Method For The _cloudExcludedTags Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("cloudExcludedTags"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************

	@core.executionTrace
	def activate(self, container):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiPath)
		self._uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiResources)
		self._container = container

		self._coreDb = self._container.componentsManager.components["core.db"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface
		self._coreCollectionsOutliner = self._container.componentsManager.components["core.collectionsOutliner"].interface

		self._activate()

	@core.executionTrace
	def deactivate(self):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self._uiResources = os.path.basename(self._uiResources)
		self._container = None

		self._coreDb = None
		self._coreDatabaseBrowser = None
		self._coreCollectionsOutliner = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.ui.Search_Database_lineEdit = Search_QLineEdit(os.path.join(self._uiResources, self._uiClearIcon), os.path.join(self._uiResources, self._uiClearClickedIcon))
		self.ui.Search_Database_horizontalLayout.addWidget(self.ui.Search_Database_lineEdit)
		self.ui.Tags_Cloud_groupBox.hide()
		self.ui.Tags_Cloud_listWidget.setSpacing(self._tagsCloudListWidgetSpacing)
		self.ui.Tags_Cloud_listWidget.setStyleSheet("QListView { background: rgb(240, 240, 240) }\nQListView::item { background: rgb(224, 224, 224) }")

		self.ui.Search_Database_label.setPixmap(QPixmap(os.path.join(self._uiResources, self._uiSearchIcon)))
		self.ui.Search_Database_comboBox.addItems([databaseField[0] for databaseField in self._databaseFields])

		self._completer = QCompleter()
		self._completer.setCaseSensitivity(Qt.CaseInsensitive)
		self._completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
		self._completer.setMaxVisibleItems(self._completerVisibleItemsCount)
		self.ui.Search_Database_lineEdit.setCompleter(self._completer)

		# Signals / Slots.
		self.ui.Search_Database_lineEdit.textChanged.connect(self.Search_Database_lineEdit_OnTextChanged)
		self.ui.Search_Database_comboBox.activated.connect(self.Search_Database_comboBox_OnActivated)
		self.ui.Case_Insensitive_Matching_checkBox.stateChanged.connect(self.Case_Insensitive_Matching_checkBox_OnStateChanged)
		self.ui.Time_Low_timeEdit.timeChanged.connect(self.Time_Low_timeEdit_OnTimeChanged)
		self.ui.Time_High_timeEdit.timeChanged.connect(self.Time_High_timeEdit_OnTimeChanged)
		self.ui.Tags_Cloud_listWidget.itemDoubleClicked.connect(self.Tags_Cloud_listWidget_OnDoubleClicked)

	@core.executionTrace
	def uninitializeUi(self):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Search_Database_lineEdit.textChanged.disconnect(self.Search_Database_lineEdit_OnTextChanged)
		self.ui.Search_Database_comboBox.activated.disconnect(self.Search_Database_comboBox_OnActivated)
		self.ui.Case_Insensitive_Matching_checkBox.stateChanged.disconnect(self.Case_Insensitive_Matching_checkBox_OnStateChanged)
		self.ui.Time_Low_timeEdit.timeChanged.disconnect(self.Time_Low_timeEdit_OnTimeChanged)
		self.ui.Time_High_timeEdit.timeChanged.disconnect(self.Time_High_timeEdit_OnTimeChanged)
		self.ui.Tags_Cloud_listWidget.itemDoubleClicked.disconnect(self.Tags_Cloud_listWidget_OnDoubleClicked)

		self._completer = None

	@core.executionTrace
	def addWidget(self):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self._container.addDockWidget(Qt.DockWidgetArea(self._dockArea), self.ui)

	@core.executionTrace
	def removeWidget(self):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self._container.removeDockWidget(self.ui)
		self.ui.setParent(None)

	@core.executionTrace
	def Search_Database_lineEdit_OnTextChanged(self, text):
		'''
		This Method Is Triggered When Search_Database_lineEdit Text Changes.
		
		@param text: Current Text Value. ( QString )
		'''

		self.setSearchMatchingSets()

	@core.executionTrace
	def Search_Database_comboBox_OnActivated(self, index):
		'''
		This Method Is Triggered When Search_Database_comboBox Index Changes.
		
		@param index: ComboBox Activated Item Index. ( Integer )
		'''

		if self.ui.Search_Database_comboBox.currentText() == self._tagsCloudField :
			self.ui.Tags_Cloud_groupBox.show()
		else :
			self.ui.Tags_Cloud_groupBox.hide()
		self.setSearchMatchingSets()

	@core.executionTrace
	def Case_Insensitive_Matching_checkBox_OnStateChanged(self, state):
		'''
		This Method Is Triggered When Case_Insensitive_Matching_checkBox State Changes.
		
		@param state: Current Checkbox State. ( Integer )
		'''

		self.setSearchMatchingSets()

	@core.executionTrace
	def Time_Low_timeEdit_OnTimeChanged(self, time):
		'''
		This Method Is Triggered When Time_Low_timeEdit Time Changes.
		
		@param time: Current Time. ( QTime )
		'''

		self.ui.Time_Low_timeEdit.time() >= self.ui.Time_High_timeEdit.time() and self.ui.Time_Low_timeEdit.setTime(self.ui.Time_High_timeEdit.time().addSecs(-60))
		self.setTimeMatchingSets()

	@core.executionTrace
	def Time_High_timeEdit_OnTimeChanged(self, time):
		'''
		This Method Is Triggered When Time_Low_timeEdit Time Changes.
		
		@param time: Current Time. ( QTime )
		'''

		self.ui.Time_High_timeEdit.time() <= self.ui.Time_Low_timeEdit.time() and self.ui.Time_High_timeEdit.setTime(self.ui.Time_Low_timeEdit.time().addSecs(60))
		self.setTimeMatchingSets()

	@core.executionTrace
	def Tags_Cloud_listWidget_OnDoubleClicked(self, listWidgetItem):
		'''
		This Method Is Triggered When Tags_Cloud_listWidget Is Double Clicked.
		
		@param listWidgetItem:  List Widget Item. ( QlistWidgetItem )
		'''

		self.ui.Search_Database_lineEdit.setText("{0} {1}".format(self.ui.Search_Database_lineEdit.text(), listWidgetItem.text()))

	@core.executionTrace
	def setTimeMatchingSets(self):
		'''
		This Method Gets The Time Matching Sets And Updates coreDatabaseBrowser displaySets.
		'''

		previousDisplaySets = self._coreDatabaseBrowser.displaySets

		iblSets = self._coreCollectionsOutliner.getCollectionsSets()

		timeLow = self.ui.Time_Low_timeEdit.time()
		timeHigh = self.ui.Time_High_timeEdit.time()

		LOGGER.debug("> Filtering Sets By Time Range From '{0}' To '{1}'.".format(timeLow, timeHigh))

		filteredSets = []
		for iblSet in iblSets:
			if iblSet.time:
				timeTokens = iblSet.time.split(":")
				int(timeTokens[0]) * 60 + int(timeTokens[1]) >= timeLow.hour()* 60 + timeLow.minute() and int(timeTokens[0]) * 60 + int(timeTokens[1]) <= timeHigh.hour()*60 + timeHigh.minute() and filteredSets.append(iblSet)

		displaySets = [displaySet for displaySet in set(self._coreCollectionsOutliner.getCollectionsSets()).intersection(filteredSets)]

		LOGGER.debug("> Time Range Filtered Ibl Set(s) : '{0}'".format(", ".join((iblSet.name for iblSet in displaySets))))

		if previousDisplaySets != displaySets:
			self._coreDatabaseBrowser.displaySets = displaySets
			self._coreDatabaseBrowser.Database_Browser_listView_refreshModel()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.UserError)
	def setSearchMatchingSets(self):
		'''
		This Method Gets The Pattern Matching Sets And Updates coreDatabaseBrowser displaySets.
		'''

		previousDisplaySets = self._coreDatabaseBrowser.displaySets

		pattern = str(self.ui.Search_Database_lineEdit.text())
		currentField = self._databaseFields[self.ui.Search_Database_comboBox.currentIndex()][1]
		flags = self.ui.Case_Insensitive_Matching_checkBox.isChecked() and re.IGNORECASE or 0

		LOGGER.debug("> Filtering Sets On '{0}' Pattern  In '{1}' Field.".format(pattern, currentField))

		if self.ui.Search_Database_comboBox.currentText() == self._tagsCloudField :
			self._completer.setModel(QStringListModel())
			patternTokens = pattern.split()
			patternTokens = patternTokens and patternTokens or (".*",)
			filteredSets = []
			allTags = []
			for iblSet in self._coreCollectionsOutliner.getCollectionsSets():
				tagsCloud = strings.filterWords(strings.getWords(getattr(iblSet, currentField)), filtersOut=self._cloudExcludedTags, flags=flags)
				patternsMatched = True
				for pattern in patternTokens :
					patternMatched = False
					for tag in tagsCloud :
						if re.search(pattern, tag, flags=flags):
							patternMatched = True
							break
					patternsMatched *= patternMatched
				if patternsMatched :
					allTags.extend((tag.lower() for tag in tagsCloud))
					filteredSets.append(iblSet)
			self.ui.Tags_Cloud_listWidget.clear()
			self.ui.Tags_Cloud_listWidget.addItems(sorted(set(allTags)))
			displaySets = [displaySet for displaySet in set(self._coreCollectionsOutliner.getCollectionsSets()).intersection(set(filteredSets))]
		else :
			try:
				re.compile(pattern)
			except:
				raise foundations.exceptions.UserError("{0} | Error While Compiling '{1}' Regex Pattern!".format(self.__class__.__name__, pattern))

			self._completer.setModel(QStringListModel(sorted((fieldValue for fieldValue in set((getattr(iblSet, currentField) for iblSet in previousDisplaySets if getattr(iblSet, currentField))) if re.search(pattern, fieldValue, flags)))))
			displaySets = [displaySet for displaySet in set(self._coreCollectionsOutliner.getCollectionsSets()).intersection(dbUtilities.common.filterIblSets(self._coreDb.dbSession, "{0}".format(str(pattern)), currentField, flags))]

		LOGGER.debug("> Pattern Filtered Ibl Set(s) : '{0}'".format(", ".join((iblSet.name for iblSet in displaySets))))

		if previousDisplaySets != displaySets:
			self._coreDatabaseBrowser.displaySets = displaySets
			self._coreDatabaseBrowser.Database_Browser_listView_refreshModel()


#***********************************************************************************************
#***	Python End
#***********************************************************************************************
