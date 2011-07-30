#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**searchDatabase.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Search Database Component Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import umbra.components.core.db.dbUtilities.common as dbCommon
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class SearchDatabase(UiComponent):
	"""
	This class is the SearchDatabase class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		:param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
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

		self.__tagsCloudField = "In tags cloud "
		self.__databaseFields = (("In names", "title"),
								("In authors", "author"),
								("In links", "link"),
								("In locations", "location"),
								("In comments", "comment"),
								(self.__tagsCloudField, "comment"),)

		self.__cloudExcludedTags = ("^a$", "^and$", "^by$", "^for$", "^from$", "^in$", "^of$", "^on$", "^or$", "^the$", "^to$", "^with$",)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for the _uiPath attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for the _uiPath attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for the _uiPath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This method is the property for the _uiResources attribute.

		:return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for the _uiResources attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for the _uiResources attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiSearchImage(self):
		"""
		This method is the property for the _uiSearchImage attribute.

		:return: self.__uiSearchImage. ( String )
		"""

		return self.__uiSearchImage

	@uiSearchImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self, value):
		"""
		This method is the setter method for the _uiSearchImage attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiSearchImage"))

	@uiSearchImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self):
		"""
		This method is the deleter method for the _uiSearchImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiSearchImage"))

	@property
	def uiClearImage(self):
		"""
		This method is the property for the _uiClearImage attribute.

		:return: self.__uiClearImage. ( String )
		"""

		return self.__uiClearImage

	@uiClearImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self, value):
		"""
		This method is the setter method for the _uiClearImage attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiClearImage"))

	@uiClearImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self):
		"""
		This method is the deleter method for the _uiClearImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiClearImage"))

	@property
	def uiClearClickedImage(self):
		"""
		This method is the property for the _uiClearClickedImage attribute.

		:return: self.__uiClearClickedImage. ( String )
		"""

		return self.__uiClearClickedImage

	@uiClearClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self, value):
		"""
		This method is the setter method for the _uiClearClickedImage attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiClearClickedImage"))

	@uiClearClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self):
		"""
		This method is the deleter method for the _uiClearClickedImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiClearClickedImage"))

	@property
	def dockArea(self):
		"""
		This method is the property for the _dockArea attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for the _dockArea attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for the _dockArea attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

	@property
	def tagsCloudListWidgetSpacing(self):
		"""
		This method is the property for the _tagsCloudListWidgetSpacing attribute.

		:return: self.__tagsCloudListWidgetSpacing. ( Integer )
		"""

		return self.__tagsCloudListWidgetSpacing

	@tagsCloudListWidgetSpacing.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudListWidgetSpacing(self, value):
		"""
		This method is the setter method for the _tagsCloudListWidgetSpacing attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("tagsCloudListWidgetSpacing"))

	@tagsCloudListWidgetSpacing.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudListWidgetSpacing(self):
		"""
		This method is the deleter method for the _tagsCloudListWidgetSpacing attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("tagsCloudListWidgetSpacing"))

	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def coreDb(self):
		"""
		This method is the property for the _coreDb attribute.

		:return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This method is the setter method for the _coreDb attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for the _coreDb attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDb"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for the _coreDatabaseBrowser attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for the _coreDatabaseBrowser attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for the _coreDatabaseBrowser attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def coreCollectionsOutliner(self):
		"""
		This method is the property for the _coreCollectionsOutliner attribute.

		:return: self.__coreCollectionsOutliner. ( Object )
		"""

		return self.__coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		"""
		This method is the setter method for the _coreCollectionsOutliner attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This method is the deleter method for the _coreCollectionsOutliner attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreCollectionsOutliner"))

	@property
	def completer(self):
		"""
		This method is the property for the _container attribute.

		:return: self.__container. ( QCompleter )
		"""

		return self.__container

	@completer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self, value):
		"""
		This method is the setter method for the _container attribute.

		:param value: Attribute value. ( QCompleter )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("completer"))

	@completer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("completer"))

	@property
	def completerVisibleItemsCount(self):
		"""
		This method is the property for the _container attribute.

		:return: self.__container. ( Integer )
		"""

		return self.__container

	@completerVisibleItemsCount.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self, value):
		"""
		This method is the setter method for the _container attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("completerVisibleItemsCount"))

	@completerVisibleItemsCount.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("completerVisibleItemsCount"))

	@property
	def tagsCloudField(self):
		"""
		This method is the property for the _tagsCloudField attribute.

		:return: self.__tagsCloudField. ( String )
		"""

		return self.__tagsCloudField

	@tagsCloudField.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudField(self, value):
		"""
		This method is the setter method for the _tagsCloudField attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("tagsCloudField"))

	@tagsCloudField.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudField(self):
		"""
		This method is the deleter method for the _tagsCloudField attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("tagsCloudField"))

	@property
	def databaseFields(self):
		"""
		This method is the property for the _databaseFields attribute.

		:return: self.__databaseFields. ( List )
		"""

		return self.__databaseFields

	@databaseFields.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseFields(self, value):
		"""
		This method is the setter method for the _databaseFields attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("databaseFields"))

	@databaseFields.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseFields(self):
		"""
		This method is the deleter method for the _databaseFields attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("databaseFields"))

	@property
	def cloudExcludedTags(self):
		"""
		This method is the property for the _cloudExcludedTags attribute.

		:return: self.__cloudExcludedTags. ( List )
		"""

		return self.__cloudExcludedTags

	@cloudExcludedTags.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self, value):
		"""
		This method is the setter method for the _cloudExcludedTags attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("cloudExcludedTags"))

	@cloudExcludedTags.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self):
		"""
		This method is the deleter method for the _cloudExcludedTags attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("cloudExcludedTags"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************

	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
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
		This method deactivates the Component.
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
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

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
		This method uninitializes the Component ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

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
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self.ui)
		self.ui.setParent(None)

	@core.executionTrace
	def __Search_Database_lineEdit__textChanged(self, text):
		"""
		This method is triggered when Search_Database_lineEdit text changes.

		:param text: Current text value. ( QString )
		"""

		self.setSearchMatchingIblsSets()

	@core.executionTrace
	def __Search_Database_comboBox__activated(self, index):
		"""
		This method is triggered when Search_Database_comboBox index changes.

		:param index: ComboBox activated item index. ( Integer )
		"""

		if self.ui.Search_Database_comboBox.currentText() == self.__tagsCloudField:
			self.ui.Tags_Cloud_groupBox.show()
		else:
			self.ui.Tags_Cloud_groupBox.hide()
		self.setSearchMatchingIblsSets()

	@core.executionTrace
	def __Case_Insensitive_Matching_checkBox__stateChanged(self, state):
		"""
		This method is triggered when Case_Insensitive_Matching_checkBox state changes.

		:param state: Current checkbox state. ( Integer )
		"""

		self.setSearchMatchingIblsSets()

	@core.executionTrace
	def __Time_Low_timeEdit__timeChanged(self, time):
		"""
		This method is triggered when Time_Low_timeEdit time changes.

		:param time: Current time. ( QTime )
		"""

		self.ui.Time_Low_timeEdit.time() >= self.ui.Time_High_timeEdit.time() and self.ui.Time_Low_timeEdit.setTime(self.ui.Time_High_timeEdit.time().addSecs(-60))
		self.setTimeMatchingIblSets()

	@core.executionTrace
	def __Time_High_timeEdit__timeChanged(self, time):
		"""
		This method is triggered when Time_Low_timeEdit time changes.

		:param time: Current time. ( QTime )
		"""

		self.ui.Time_High_timeEdit.time() <= self.ui.Time_Low_timeEdit.time() and self.ui.Time_High_timeEdit.setTime(self.ui.Time_Low_timeEdit.time().addSecs(60))
		self.setTimeMatchingIblSets()

	@core.executionTrace
	def __Tags_Cloud_listWidget__doubleClicked(self, listWidgetItem):
		"""
		This method is triggered when Tags_Cloud_listWidget is double clicked.

		:param listWidgetItem: List Widget item. ( QlistWidgetItem )
		"""

		self.ui.Search_Database_lineEdit.setText("{0} {1}".format(self.ui.Search_Database_lineEdit.text(), listWidgetItem.text()))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setTimeMatchingIblSets(self):
		"""
		This method gets the time matching sets and updates coreDatabaseBrowser Model content.
		"""

		previousModelContent = self.__coreDatabaseBrowser.modelContent

		iblSets = self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())

		timeLow = self.ui.Time_Low_timeEdit.time()
		timeHigh = self.ui.Time_High_timeEdit.time()

		LOGGER.debug("> Filtering sets by time range from '{0}' to '{1}'.".format(timeLow, timeHigh))

		filteredSets = []
		for iblSet in iblSets:
			if not iblSet.time:
				continue

			timeTokens = iblSet.time.split(":")
			int(timeTokens[0]) * 60 + int(timeTokens[1]) >= timeLow.hour()* 60 + timeLow.minute() and int(timeTokens[0]) * 60 + int(timeTokens[1]) <= timeHigh.hour()*60 + timeHigh.minute() and filteredSets.append(iblSet)

		modelContent = [displaySet for displaySet in set(self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())).intersection(filteredSets)]

		LOGGER.debug("> Time range filtered Ibl Set(s): '{0}'".format(", ".join((iblSet.name for iblSet in modelContent))))

		if previousModelContent != modelContent:
			self.__coreDatabaseBrowser.modelContent = modelContent
			self.__coreDatabaseBrowser.emit(SIGNAL("modelRefresh()"))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.UserError)
	def setSearchMatchingIblsSets(self):
		"""
		This method gets the pattern matching sets and updates coreDatabaseBrowser Model content.
		"""

		previousModelContent = self.__coreDatabaseBrowser.modelContent

		pattern = str(self.ui.Search_Database_lineEdit.text())
		currentField = self.__databaseFields[self.ui.Search_Database_comboBox.currentIndex()][1]
		flags = self.ui.Case_Insensitive_Matching_checkBox.isChecked() and re.IGNORECASE or 0

		LOGGER.debug("> Filtering Ibl Sets on '{0}' pattern in '{1}' field.".format(pattern, currentField))

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
				raise foundations.exceptions.UserError("{0} | Error while compiling '{1}' regex pattern!".format(self.__class__.__name__, pattern))

			self.__completer.setModel(QStringListModel(sorted((fieldValue for fieldValue in set((getattr(iblSet, currentField) for iblSet in previousModelContent if getattr(iblSet, currentField))) if re.search(pattern, fieldValue, flags)))))
			modelContent = [displaySet for displaySet in set(self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())).intersection(dbCommon.filterIblSets(self.__coreDb.dbSession, "{0}".format(str(pattern)), currentField, flags))]

		LOGGER.debug("> Pattern filtered Ibl Set(s): '{0}'".format(", ".join((iblSet.name for iblSet in modelContent))))

		if previousModelContent != modelContent:
			self.__coreDatabaseBrowser.modelContent = modelContent
			self.__coreDatabaseBrowser.emit(SIGNAL("modelRefresh()"))
		return True

