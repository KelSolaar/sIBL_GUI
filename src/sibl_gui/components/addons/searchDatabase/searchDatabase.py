#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**searchDatabase.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`SearchDatabase` Component Interface class.

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
import sibl_gui.components.core.db.utilities.common as dbCommon
from manager.qwidgetComponent import QWidgetComponentFactory
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "SearchDatabase"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_Database.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class SearchDatabase(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.addons.searchDatabase.searchDatabase` Component Interface class.
	| It provides methods for the user to search into the Database using various filters.
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(SearchDatabase, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__uiResourcesDirectory = "resources"
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
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResourcesDirectory"))

	@property
	def uiSearchImage(self):
		"""
		This method is the property for **self.__uiSearchImage** attribute.

		:return: self.__uiSearchImage. ( String )
		"""

		return self.__uiSearchImage

	@uiSearchImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self, value):
		"""
		This method is the setter method for **self.__uiSearchImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiSearchImage"))

	@uiSearchImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self):
		"""
		This method is the deleter method for **self.__uiSearchImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiSearchImage"))

	@property
	def uiClearImage(self):
		"""
		This method is the property for **self.__uiClearImage** attribute.

		:return: self.__uiClearImage. ( String )
		"""

		return self.__uiClearImage

	@uiClearImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self, value):
		"""
		This method is the setter method for **self.__uiClearImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiClearImage"))

	@uiClearImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self):
		"""
		This method is the deleter method for **self.__uiClearImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiClearImage"))

	@property
	def uiClearClickedImage(self):
		"""
		This method is the property for **self.__uiClearClickedImage** attribute.

		:return: self.__uiClearClickedImage. ( String )
		"""

		return self.__uiClearClickedImage

	@uiClearClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self, value):
		"""
		This method is the setter method for **self.__uiClearClickedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiClearClickedImage"))

	@uiClearClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self):
		"""
		This method is the deleter method for **self.__uiClearClickedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiClearClickedImage"))

	@property
	def dockArea(self):
		"""
		This method is the property for **self.__dockArea** attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

	@property
	def tagsCloudListWidgetSpacing(self):
		"""
		This method is the property for **self.__tagsCloudListWidgetSpacing** attribute.

		:return: self.__tagsCloudListWidgetSpacing. ( Integer )
		"""

		return self.__tagsCloudListWidgetSpacing

	@tagsCloudListWidgetSpacing.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudListWidgetSpacing(self, value):
		"""
		This method is the setter method for **self.__tagsCloudListWidgetSpacing** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("tagsCloudListWidgetSpacing"))

	@tagsCloudListWidgetSpacing.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudListWidgetSpacing(self):
		"""
		This method is the deleter method for **self.__tagsCloudListWidgetSpacing** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("tagsCloudListWidgetSpacing"))

	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def coreDb(self):
		"""
		This method is the property for **self.__coreDb** attribute.

		:return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This method is the setter method for **self.__coreDb** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for **self.__coreDb** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDb"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def coreCollectionsOutliner(self):
		"""
		This method is the property for **self.__coreCollectionsOutliner** attribute.

		:return: self.__coreCollectionsOutliner. ( Object )
		"""

		return self.__coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		"""
		This method is the setter method for **self.__coreCollectionsOutliner** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This method is the deleter method for **self.__coreCollectionsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreCollectionsOutliner"))

	@property
	def completer(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QCompleter )
		"""

		return self.__container

	@completer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QCompleter )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("completer"))

	@completer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("completer"))

	@property
	def completerVisibleItemsCount(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( Integer )
		"""

		return self.__container

	@completerVisibleItemsCount.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("completerVisibleItemsCount"))

	@completerVisibleItemsCount.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("completerVisibleItemsCount"))

	@property
	def tagsCloudField(self):
		"""
		This method is the property for **self.__tagsCloudField** attribute.

		:return: self.__tagsCloudField. ( String )
		"""

		return self.__tagsCloudField

	@tagsCloudField.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudField(self, value):
		"""
		This method is the setter method for **self.__tagsCloudField** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("tagsCloudField"))

	@tagsCloudField.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudField(self):
		"""
		This method is the deleter method for **self.__tagsCloudField** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("tagsCloudField"))

	@property
	def databaseFields(self):
		"""
		This method is the property for **self.__databaseFields** attribute.

		:return: self.__databaseFields. ( List )
		"""

		return self.__databaseFields

	@databaseFields.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseFields(self, value):
		"""
		This method is the setter method for **self.__databaseFields** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("databaseFields"))

	@databaseFields.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseFields(self):
		"""
		This method is the deleter method for **self.__databaseFields** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("databaseFields"))

	@property
	def cloudExcludedTags(self):
		"""
		This method is the property for **self.__cloudExcludedTags** attribute.

		:return: self.__cloudExcludedTags. ( List )
		"""

		return self.__cloudExcludedTags

	@cloudExcludedTags.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self, value):
		"""
		This method is the setter method for **self.__cloudExcludedTags** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("cloudExcludedTags"))

	@cloudExcludedTags.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self):
		"""
		This method is the deleter method for **self.__cloudExcludedTags** attribute.
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
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResourcesDirectory)
		self.__container = container

		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreCollectionsOutliner = self.__container.componentsManager.components["core.collectionsOutliner"].interface

		self.activated = True
		return True

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.basename(self.__uiResourcesDirectory)
		self.__container = None

		self.__coreDb = None
		self.__coreDatabaseBrowser = None
		self.__coreCollectionsOutliner = None

		self.activated = False
		return True

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.Search_Database_lineEdit = Search_QLineEdit(self, os.path.join(self.__uiResourcesDirectory, self.__uiClearImage), os.path.join(self.__uiResourcesDirectory, self.__uiClearClickedImage))
		self.Search_Database_horizontalLayout.addWidget(self.Search_Database_lineEdit)
		self.Tags_Cloud_groupBox.hide()
		self.Tags_Cloud_listWidget.setSpacing(self.__tagsCloudListWidgetSpacing)

		self.Search_Database_label.setPixmap(QPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiSearchImage)))
		self.Search_Database_comboBox.addItems([databaseField[0] for databaseField in self.__databaseFields])

		self.__completer = QCompleter()
		self.__completer.setCaseSensitivity(Qt.CaseInsensitive)
		self.__completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
		self.__completer.setMaxVisibleItems(self.__completerVisibleItemsCount)
		self.Search_Database_lineEdit.setCompleter(self.__completer)

		# Signals / Slots.
		self.Search_Database_lineEdit.textChanged.connect(self.__Search_Database_lineEdit__textChanged)
		self.Search_Database_comboBox.activated.connect(self.__Search_Database_comboBox__activated)
		self.Case_Insensitive_Matching_checkBox.stateChanged.connect(self.__Case_Insensitive_Matching_checkBox__stateChanged)
		self.Time_Low_timeEdit.timeChanged.connect(self.__Time_Low_timeEdit__timeChanged)
		self.Time_High_timeEdit.timeChanged.connect(self.__Time_High_timeEdit__timeChanged)
		self.Tags_Cloud_listWidget.itemDoubleClicked.connect(self.__Tags_Cloud_listWidget__doubleClicked)

		return True

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.Search_Database_lineEdit.textChanged.disconnect(self.__Search_Database_lineEdit__textChanged)
		self.Search_Database_comboBox.activated.disconnect(self.__Search_Database_comboBox__activated)
		self.Case_Insensitive_Matching_checkBox.stateChanged.disconnect(self.__Case_Insensitive_Matching_checkBox__stateChanged)
		self.Time_Low_timeEdit.timeChanged.disconnect(self.__Time_Low_timeEdit__timeChanged)
		self.Time_High_timeEdit.timeChanged.disconnect(self.__Time_High_timeEdit__timeChanged)
		self.Tags_Cloud_listWidget.itemDoubleClicked.disconnect(self.__Tags_Cloud_listWidget__doubleClicked)

		self.__completer = None

		return True

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self)
		self.setParent(None)

		return True

	@core.executionTrace
	def __Search_Database_lineEdit__textChanged(self, text):
		"""
		This method is triggered when **Search_Database_lineEdit** text changes.

		:param text: Current text value. ( QString )
		"""

		self.setSearchMatchingIblsSets()

	@core.executionTrace
	def __Search_Database_comboBox__activated(self, index):
		"""
		This method is triggered when **Search_Database_comboBox** index changes.

		:param index: ComboBox activated item index. ( Integer )
		"""

		if self.Search_Database_comboBox.currentText() == self.__tagsCloudField:
			self.Tags_Cloud_groupBox.show()
		else:
			self.Tags_Cloud_groupBox.hide()
		self.setSearchMatchingIblsSets()

	@core.executionTrace
	def __Case_Insensitive_Matching_checkBox__stateChanged(self, state):
		"""
		This method is triggered when **Case_Insensitive_Matching_checkBox** state changes.

		:param state: Current checkbox state. ( Integer )
		"""

		self.setSearchMatchingIblsSets()

	@core.executionTrace
	def __Time_Low_timeEdit__timeChanged(self, time):
		"""
		This method is triggered when **Time_Low_timeEdit** time changes.

		:param time: Current time. ( QTime )
		"""

		self.Time_Low_timeEdit.time() >= self.Time_High_timeEdit.time() and self.Time_Low_timeEdit.setTime(self.Time_High_timeEdit.time().addSecs(-60))
		self.setTimeMatchingIblSets()

	@core.executionTrace
	def __Time_High_timeEdit__timeChanged(self, time):
		"""
		This method is triggered when **Time_Low_timeEdit** time changes.

		:param time: Current time. ( QTime )
		"""

		self.Time_High_timeEdit.time() <= self.Time_Low_timeEdit.time() and self.Time_High_timeEdit.setTime(self.Time_Low_timeEdit.time().addSecs(60))
		self.setTimeMatchingIblSets()

	@core.executionTrace
	def __Tags_Cloud_listWidget__doubleClicked(self, listWidgetItem):
		"""
		This method is triggered when **Tags_Cloud_listWidget** is double clicked.

		:param listWidgetItem: List Widget item. ( QlistWidgetItem )
		"""

		self.Search_Database_lineEdit.setText("{0} {1}".format(self.Search_Database_lineEdit.text(), listWidgetItem.text()))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setTimeMatchingIblSets(self):
		"""
		This method gets the time matching sets and updates :mod:`umbra.components.core.databaseBrowser.databaseBrowser` Component Model content.
		"""

		previousModelContent = self.__coreDatabaseBrowser.modelContent

		iblSets = self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())

		timeLow = self.Time_Low_timeEdit.time()
		timeHigh = self.Time_High_timeEdit.time()

		LOGGER.debug("> Filtering sets by time range from '{0}' to '{1}'.".format(timeLow, timeHigh))

		filteredSets = []
		for iblSet in iblSets:
			if not iblSet.time:
				continue

			hours, minutes, seconds = iblSet.time.split(":")
			int(hours) * 60 + int(minutes) >= timeLow.hour() * 60 + timeLow.minute() and int(hours) * 60 + int(minutes) <= timeHigh.hour() * 60 + timeHigh.minute() and filteredSets.append(iblSet)

		modelContent = [displaySet for displaySet in set(self.__coreCollectionsOutliner.getCollectionsIblSets(self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())).intersection(filteredSets)]

		LOGGER.debug("> Time range filtered Ibl Set(s): '{0}'".format(", ".join((iblSet.name for iblSet in modelContent))))

		if previousModelContent != modelContent:
			self.__coreDatabaseBrowser.modelContent = modelContent
			self.__coreDatabaseBrowser.modelRefresh.emit()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.UserError)
	def setSearchMatchingIblsSets(self):
		"""
		This method gets the pattern matching sets and updates :mod:`umbra.components.core.databaseBrowser.databaseBrowser` Component Model content.
		"""

		previousModelContent = self.__coreDatabaseBrowser.modelContent

		pattern = str(self.Search_Database_lineEdit.text())
		currentField = self.__databaseFields[self.Search_Database_comboBox.currentIndex()][1]
		flags = self.Case_Insensitive_Matching_checkBox.isChecked() and re.IGNORECASE or 0

		LOGGER.debug("> Filtering Ibl Sets on '{0}' pattern in '{1}' field.".format(pattern, currentField))

		if self.Search_Database_comboBox.currentText() == self.__tagsCloudField:
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
			self.Tags_Cloud_listWidget.clear()
			self.Tags_Cloud_listWidget.addItems(sorted(set(allTags), key=lambda x:x.lower()))
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
			self.__coreDatabaseBrowser.modelRefresh.emit()
		return True
