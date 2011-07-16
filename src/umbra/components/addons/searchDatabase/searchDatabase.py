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
"""

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
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class SearchDatabase(UiComponent):
	"""
	This Class Is The SearchDatabase Class.
	"""

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
		self.deactivatable = True

		self.__uiPath = "ui/Search_Database.ui"
		self.__uiResources = "resources"
		self.__uiSearchImage = "Search_Glass.png"
		self.__uiClearImage = "Search_Clear.png"
		self.__uiClearClickedImage = "Search_Clear_Clicked.png"
		self.__dockArea = 2
		self.__tagsCloudListWidgetSpacing = 4

		self.__container = None

		self.__coreDatabaseBrowser = None
		self.__coreCollectionsOutliner = None

		self.__completer = None
		self.__completerVisibleItemsCount = 16

		self.__tagsCloudField = "In Tags Cloud "
		self.__databaseFields = (("In Names", "title"),
								("In Authors", "author"),
								("In Links", "link"),
								("In Locations", "location"),
								("In Comments", "comment"),
								(self.__tagsCloudField, "comment"),)

		self.__cloudExcludedTags = ("^a$", "^and$", "^by$", "^for$", "^from$", "^in$", "^of$", "^on$", "^or$", "^the$", "^to$", "^with$",)

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
	def uiSearchImage(self):
		"""
		This Method Is The Property For The _uiSearchImage Attribute.

		@return: self.__uiSearchImage. ( String )
		"""

		return self.__uiSearchImage

	@uiSearchImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self, value):
		"""
		This Method Is The Setter Method For The _uiSearchImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiSearchImage"))

	@uiSearchImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self):
		"""
		This Method Is The Deleter Method For The _uiSearchImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiSearchImage"))

	@property
	def uiClearImage(self):
		"""
		This Method Is The Property For The _uiClearImage Attribute.

		@return: self.__uiClearImage. ( String )
		"""

		return self.__uiClearImage

	@uiClearImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self, value):
		"""
		This Method Is The Setter Method For The _uiClearImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiClearImage"))

	@uiClearImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self):
		"""
		This Method Is The Deleter Method For The _uiClearImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiClearImage"))

	@property
	def uiClearClickedImage(self):
		"""
		This Method Is The Property For The _uiClearClickedImage Attribute.

		@return: self.__uiClearClickedImage. ( String )
		"""

		return self.__uiClearClickedImage

	@uiClearClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self, value):
		"""
		This Method Is The Setter Method For The _uiClearClickedImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiClearClickedImage"))

	@uiClearClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self):
		"""
		This Method Is The Deleter Method For The _uiClearClickedImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiClearClickedImage"))

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
	def tagsCloudListWidgetSpacing(self):
		"""
		This Method Is The Property For The _tagsCloudListWidgetSpacing Attribute.

		@return: self.__tagsCloudListWidgetSpacing. ( Integer )
		"""

		return self.__tagsCloudListWidgetSpacing

	@tagsCloudListWidgetSpacing.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudListWidgetSpacing(self, value):
		"""
		This Method Is The Setter Method For The _tagsCloudListWidgetSpacing Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("tagsCloudListWidgetSpacing"))

	@tagsCloudListWidgetSpacing.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudListWidgetSpacing(self):
		"""
		This Method Is The Deleter Method For The _tagsCloudListWidgetSpacing Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("tagsCloudListWidgetSpacing"))

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
	def completer(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QCompleter )
		"""

		return self.__container

	@completer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QCompleter )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("completer"))

	@completer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("completer"))

	@property
	def completerVisibleItemsCount(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( Integer )
		"""

		return self.__container

	@completerVisibleItemsCount.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("completerVisibleItemsCount"))

	@completerVisibleItemsCount.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("completerVisibleItemsCount"))

	@property
	def tagsCloudField(self):
		"""
		This Method Is The Property For The _tagsCloudField Attribute.

		@return: self.__tagsCloudField. ( String )
		"""

		return self.__tagsCloudField

	@tagsCloudField.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudField(self, value):
		"""
		This Method Is The Setter Method For The _tagsCloudField Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("tagsCloudField"))

	@tagsCloudField.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudField(self):
		"""
		This Method Is The Deleter Method For The _tagsCloudField Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("tagsCloudField"))

	@property
	def databaseFields(self):
		"""
		This Method Is The Property For The _databaseFields Attribute.

		@return: self.__databaseFields. ( List )
		"""

		return self.__databaseFields

	@databaseFields.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseFields(self, value):
		"""
		This Method Is The Setter Method For The _databaseFields Attribute.

		@param value: Attribute Value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("databaseFields"))

	@databaseFields.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseFields(self):
		"""
		This Method Is The Deleter Method For The _databaseFields Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("databaseFields"))

	@property
	def cloudExcludedTags(self):
		"""
		This Method Is The Property For The _cloudExcludedTags Attribute.

		@return: self.__cloudExcludedTags. ( List )
		"""

		return self.__cloudExcludedTags

	@cloudExcludedTags.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self, value):
		"""
		This Method Is The Setter Method For The _cloudExcludedTags Attribute.

		@param value: Attribute Value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("cloudExcludedTags"))

	@cloudExcludedTags.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self):
		"""
		This Method Is The Deleter Method For The _cloudExcludedTags Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("cloudExcludedTags"))

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

		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreCollectionsOutliner = self.__container.componentsManager.components["core.collectionsOutliner"].interface

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__uiResources = os.path.basename(self.__uiResources)
		self.__container = None

		self.__coreDb = None
		self.__coreDatabaseBrowser = None
		self.__coreCollectionsOutliner = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.ui.Search_Database_lineEdit = Search_QLineEdit(os.path.join(self.__uiResources, self.__uiClearImage), os.path.join(self.__uiResources, self.__uiClearClickedImage))
		self.ui.Search_Database_horizontalLayout.addWidget(self.ui.Search_Database_lineEdit)
		self.ui.Tags_Cloud_groupBox.hide()
		self.ui.Tags_Cloud_listWidget.setSpacing(self.__tagsCloudListWidgetSpacing)

		self.ui.Search_Database_label.setPixmap(QPixmap(os.path.join(self.__uiResources, self.__uiSearchImage)))
		self.ui.Search_Database_comboBox.addItems([databaseField[0] for databaseField in self.__databaseFields])

		self.__completer = QCompleter()
		self.__completer.setCaseSensitivity(Qt.CaseInsensitive)
		self.__completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
		self.__completer.setMaxVisibleItems(self.__completerVisibleItemsCount)
		self.ui.Search_Database_lineEdit.setCompleter(self.__completer)

		# Signals / Slots.
		self.ui.Search_Database_lineEdit.textChanged.connect(self.__Search_Database_lineEdit__textChanged)
		self.ui.Search_Database_comboBox.activated.connect(self.__Search_Database_comboBox__activated)
		self.ui.Case_Insensitive_Matching_checkBox.stateChanged.connect(self.__Case_Insensitive_Matching_checkBox__stateChanged)
		self.ui.Time_Low_timeEdit.timeChanged.connect(self.__Time_Low_timeEdit__timeChanged)
		self.ui.Time_High_timeEdit.timeChanged.connect(self.__Time_High_timeEdit__timeChanged)
		self.ui.Tags_Cloud_listWidget.itemDoubleClicked.connect(self.__Tags_Cloud_listWidget__doubleClicked)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Search_Database_lineEdit.textChanged.disconnect(self.__Search_Database_lineEdit__textChanged)
		self.ui.Search_Database_comboBox.activated.disconnect(self.__Search_Database_comboBox__activated)
		self.ui.Case_Insensitive_Matching_checkBox.stateChanged.disconnect(self.__Case_Insensitive_Matching_checkBox__stateChanged)
		self.ui.Time_Low_timeEdit.timeChanged.disconnect(self.__Time_Low_timeEdit__timeChanged)
		self.ui.Time_High_timeEdit.timeChanged.disconnect(self.__Time_High_timeEdit__timeChanged)
		self.ui.Tags_Cloud_listWidget.itemDoubleClicked.disconnect(self.__Tags_Cloud_listWidget__doubleClicked)

		self.__completer = None

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self.ui)
		self.ui.setParent(None)

	@core.executionTrace
	def __Search_Database_lineEdit__textChanged(self, text):
		"""
		This Method Is Triggered When Search_Database_lineEdit Text Changes.
		
		@param text: Current Text Value. ( QString )
		"""

		self.setSearchMatchingIblsSets()

	@core.executionTrace
	def __Search_Database_comboBox__activated(self, index):
		"""
		This Method Is Triggered When Search_Database_comboBox Index Changes.
		
		@param index: ComboBox Activated Item Index. ( Integer )
		"""

		if self.ui.Search_Database_comboBox.currentText() == self.__tagsCloudField:
			self.ui.Tags_Cloud_groupBox.show()
		else:
			self.ui.Tags_Cloud_groupBox.hide()
		self.setSearchMatchingIblsSets()

	@core.executionTrace
	def __Case_Insensitive_Matching_checkBox__stateChanged(self, state):
		"""
		This Method Is Triggered When Case_Insensitive_Matching_checkBox State Changes.
		
		@param state: Current Checkbox State. ( Integer )
		"""

		self.setSearchMatchingIblsSets()

	@core.executionTrace
	def __Time_Low_timeEdit__timeChanged(self, time):
		"""
		This Method Is Triggered When Time_Low_timeEdit Time Changes.
		
		@param time: Current Time. ( QTime )
		"""

		self.ui.Time_Low_timeEdit.time() >= self.ui.Time_High_timeEdit.time() and self.ui.Time_Low_timeEdit.setTime(self.ui.Time_High_timeEdit.time().addSecs(-60))
		self.setTimeMatchingIblSets()

	@core.executionTrace
	def __Time_High_timeEdit__timeChanged(self, time):
		"""
		This Method Is Triggered When Time_Low_timeEdit Time Changes.
		
		@param time: Current Time. ( QTime )
		"""

		self.ui.Time_High_timeEdit.time() <= self.ui.Time_Low_timeEdit.time() and self.ui.Time_High_timeEdit.setTime(self.ui.Time_Low_timeEdit.time().addSecs(60))
		self.setTimeMatchingIblSets()

	@core.executionTrace
	def __Tags_Cloud_listWidget__doubleClicked(self, listWidgetItem):
		"""
		This Method Is Triggered When Tags_Cloud_listWidget Is Double Clicked.
		
		@param listWidgetItem:  List Widget Item. ( QlistWidgetItem )
		"""

		self.ui.Search_Database_lineEdit.setText("{0} {1}".format(self.ui.Search_Database_lineEdit.text(), listWidgetItem.text()))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setTimeMatchingIblSets(self):
		"""
		This Method Gets The Time Matching Sets And Updates coreDatabaseBrowser Model Content.
		"""

		previousModelContent = self.__coreDatabaseBrowser.modelContent

		iblSets = self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())

		timeLow = self.ui.Time_Low_timeEdit.time()
		timeHigh = self.ui.Time_High_timeEdit.time()

		LOGGER.debug("> Filtering Sets By Time Range From '{0}' To '{1}'.".format(timeLow, timeHigh))

		filteredSets = []
		for iblSet in iblSets:
			if not iblSet.time:
				continue

			timeTokens = iblSet.time.split(":")
			int(timeTokens[0]) * 60 + int(timeTokens[1]) >= timeLow.hour()* 60 + timeLow.minute() and int(timeTokens[0]) * 60 + int(timeTokens[1]) <= timeHigh.hour()*60 + timeHigh.minute() and filteredSets.append(iblSet)

		modelContent = [displaySet for displaySet in set(self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())).intersection(filteredSets)]

		LOGGER.debug("> Time Range Filtered Ibl Set(s): '{0}'".format(", ".join((iblSet.name for iblSet in modelContent))))

		if previousModelContent != modelContent:
			self.__coreDatabaseBrowser.modelContent = modelContent
			self.__coreDatabaseBrowser.emit(SIGNAL("modelRefresh()"))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.UserError)
	def setSearchMatchingIblsSets(self):
		"""
		This Method Gets The Pattern Matching Sets And Updates coreDatabaseBrowser Model Content.
		"""

		previousModelContent = self.__coreDatabaseBrowser.modelContent

		pattern = str(self.ui.Search_Database_lineEdit.text())
		currentField = self.__databaseFields[self.ui.Search_Database_comboBox.currentIndex()][1]
		flags = self.ui.Case_Insensitive_Matching_checkBox.isChecked() and re.IGNORECASE or 0

		LOGGER.debug("> Filtering Sets On '{0}' Pattern  In '{1}' Field.".format(pattern, currentField))

		if self.ui.Search_Database_comboBox.currentText() == self.__tagsCloudField:
			self.__completer.setModel(QStringListModel())
			patternTokens = pattern.split()
			patternTokens = patternTokens and patternTokens or (".*",)
			filteredSets = []
			allTags = []
			for iblSet in self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections()):
				if not getattr(iblSet, currentField):
					continue

				tagsCloud = strings.filterWords(strings.getWords(getattr(iblSet, currentField)), filtersOut=self.__cloudExcludedTags, flags=flags)
				patternsMatched = True
				for pattern in patternTokens:
					patternMatched = False
					for tag in tagsCloud:
						if re.search(pattern, tag, flags=flags):
							patternMatched = True
							break
					patternsMatched *= patternMatched
				if patternsMatched:
					allTags.extend(tagsCloud)
					filteredSets.append(iblSet)
			self.ui.Tags_Cloud_listWidget.clear()
			self.ui.Tags_Cloud_listWidget.addItems(sorted(set(allTags), key=lambda x:x.lower()))
			modelContent = [displaySet for displaySet in set(self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())).intersection(set(filteredSets))]
		else:
			try:
				re.compile(pattern)
			except:
				raise foundations.exceptions.UserError("{0} | Error While Compiling '{1}' Regex Pattern!".format(self.__class__.__name__, pattern))

			self.__completer.setModel(QStringListModel(sorted((fieldValue for fieldValue in set((getattr(iblSet, currentField) for iblSet in previousModelContent if getattr(iblSet, currentField))) if re.search(pattern, fieldValue, flags)))))
			modelContent = [displaySet for displaySet in set(self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())).intersection(dbUtilities.common.filterIblSets(self.__coreDb.dbSession, "{0}".format(str(pattern)), currentField, flags))]

		LOGGER.debug("> Pattern Filtered Ibl Set(s): '{0}'".format(", ".join((iblSet.name for iblSet in modelContent))))

		if previousModelContent != modelContent:
			self.__coreDatabaseBrowser.modelContent = modelContent
			self.__coreDatabaseBrowser.emit(SIGNAL("modelRefresh()"))
		return True

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
