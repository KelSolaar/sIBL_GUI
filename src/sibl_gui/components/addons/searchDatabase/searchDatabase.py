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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import collections
import logging
import os
import re
import itertools
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import umbra.ui.common
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "SearchDatabase"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_Database.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class SearchDatabase(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.addons.searchDatabase.searchDatabase` Component Interface class.
	| It provides methods for the user to search into the Database using various filters.
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(SearchDatabase, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__dockArea = 2
		self.__tagsCloudListWidgetSpacing = 4

		self.__engine = None

		self.__coreDatabaseBrowser = None
		self.__coreCollectionsOutliner = None

		self.__cloudExcludedTags = ("a", "and", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with")

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tagsCloudListWidgetSpacing"))

	@tagsCloudListWidgetSpacing.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tagsCloudListWidgetSpacing(self):
		"""
		This method is the deleter method for **self.__tagsCloudListWidgetSpacing** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tagsCloudListWidgetSpacing"))

	@property
	def engine(self):
		"""
		This method is the property for **self.__engine** attribute.

		:return: self.__engine. ( QObject )
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for **self.__coreDb** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDb"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( QWidget )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@property
	def coreCollectionsOutliner(self):
		"""
		This method is the property for **self.__coreCollectionsOutliner** attribute.

		:return: self.__coreCollectionsOutliner. ( QWidget )
		"""

		return self.__coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		"""
		This method is the setter method for **self.__coreCollectionsOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This method is the deleter method for **self.__coreCollectionsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreCollectionsOutliner"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "cloudExcludedTags"))

	@cloudExcludedTags.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self):
		"""
		This method is the deleter method for **self.__cloudExcludedTags** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "cloudExcludedTags"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine

		self.__coreDb = self.__engine.componentsManager.components["core.db"].interface
		self.__coreDatabaseBrowser = self.__engine.componentsManager.components["core.databaseBrowser"].interface
		self.__coreCollectionsOutliner = self.__engine.componentsManager.components["core.collectionsOutliner"].interface

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.__coreDb = None
		self.__coreDatabaseBrowser = None
		self.__coreCollectionsOutliner = None

		self.activated = False
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.Search_Database_lineEdit = Search_QLineEdit(self)
		self.Search_Database_horizontalLayout.addWidget(self.Search_Database_lineEdit)
		self.Search_Database_lineEdit.setPlaceholderText("Search In Tags Cloud ...")
		self.Tags_Cloud_listWidget.setSpacing(self.__tagsCloudListWidgetSpacing)

		self.__cloudExcludedTags = list(itertools.chain.from_iterable(
									[(r"^{0}$".format(tag), r"^{0}$".format(tag.title()), r"^{0}$".format(tag.upper()))
									for tag in self.__cloudExcludedTags]))
		self.setTagsCloudMatchingIblsSetsUi()

		# Signals / Slots.
		self.Search_Database_lineEdit.textChanged.connect(self.__Search_Database_lineEdit__textChanged)
		self.Case_Sensitive_Matching_pushButton.clicked.connect(self.__Case_Sensitive_Matching_pushButton__clicked)
		self.Time_Low_timeEdit.timeChanged.connect(self.__Time_Low_timeEdit__timeChanged)
		self.Time_High_timeEdit.timeChanged.connect(self.__Time_High_timeEdit__timeChanged)
		self.Tags_Cloud_listWidget.itemDoubleClicked.connect(self.__Tags_Cloud_listWidget__doubleClicked)
		self.__coreCollectionsOutliner.view.selectionModel().selectionChanged.connect(
		self.__coreCollectionsOutliner_view_selectionModel__selectionChanged)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.Search_Database_lineEdit.textChanged.disconnect(self.__Search_Database_lineEdit__textChanged)
		self.Case_Sensitive_Matching_pushButton.clicked.disconnect(self.__Case_Sensitive_Matching_pushButton__clicked)
		self.Time_Low_timeEdit.timeChanged.disconnect(self.__Time_Low_timeEdit__timeChanged)
		self.Time_High_timeEdit.timeChanged.disconnect(self.__Time_High_timeEdit__timeChanged)
		self.Tags_Cloud_listWidget.itemDoubleClicked.disconnect(self.__Tags_Cloud_listWidget__doubleClicked)
		self.__coreCollectionsOutliner.view.selectionModel().selectionChanged.disconnect(
		self.__coreCollectionsOutliner_view_selectionModel__selectionChanged)

		self.Search_Database_lineEdit.setParent(None)
		self.Search_Database_lineEdit = None

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	@core.executionTrace
	def __Search_Database_lineEdit__textChanged(self, text):
		"""
		This method is triggered when **Search_Database_lineEdit** text changes.

		:param text: Current text value. ( QString )
		"""

		self.setTagsCloudMatchingIblsSetsUi()

	@core.executionTrace
	def __Case_Sensitive_Matching_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Case_Sensitive_Matching_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.setTagsCloudMatchingIblsSetsUi()

	@core.executionTrace
	def __Time_Low_timeEdit__timeChanged(self, time):
		"""
		This method is triggered when **Time_Low_timeEdit** time changes.

		:param time: Current time. ( QTime )
		"""

		self.Time_Low_timeEdit.time() >= self.Time_High_timeEdit.time() and \
		self.Time_Low_timeEdit.setTime(self.Time_High_timeEdit.time().addSecs(-60))
		self.setTimeMatchingIblSetsUi()

	@core.executionTrace
	def __Time_High_timeEdit__timeChanged(self, time):
		"""
		This method is triggered when **Time_Low_timeEdit** time changes.

		:param time: Current time. ( QTime )
		"""

		self.Time_High_timeEdit.time() <= self.Time_Low_timeEdit.time() and \
		self.Time_High_timeEdit.setTime(self.Time_Low_timeEdit.time().addSecs(60))
		self.setTimeMatchingIblSetsUi()

	@core.executionTrace
	def __Tags_Cloud_listWidget__doubleClicked(self, listWidgetItem):
		"""
		This method is triggered when **Tags_Cloud_listWidget** is double clicked.

		:param listWidgetItem: List Widget item. ( QlistWidgetItem )
		"""

		self.Search_Database_lineEdit.setText("{0} {1}".format(self.Search_Database_lineEdit.text(), listWidgetItem.text()))

	@core.executionTrace
	def __coreCollectionsOutliner_view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when **coreCollectionsOutliner.view** Model selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		self.setTagsCloudMatchingIblsSetsUi()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def setTagsCloudMatchingIblsSetsUi(self):
		"""
		This method sets the user defined pattern matching Ibl Sets and 
		updates :mod:`sibl_gui.components.core.databaseBrowser.databaseBrowser` Component Model content.
		
		:return: Method success. ( Boolean )
		
		:note: This method may require user interaction.
		"""

		return self.setTagsCloudMatchingIblsSets(strings.encode(self.Search_Database_lineEdit.text()),
		not self.Case_Sensitive_Matching_pushButton.isChecked() and re.IGNORECASE or 0)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def setTimeMatchingIblSetsUi(self):
		"""
		This method sets the user defined time matching Ibl Sets and 
		updates :mod:`sibl_gui.components.core.databaseBrowser.databaseBrowser` Component Model content.
		
		:return: Method success. ( Boolean )
		
		:note: This method may require user interaction.
		"""

		return self.setTimeMatchingIblSets(self.Time_Low_timeEdit.time(), self.Time_High_timeEdit.time())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.UserError)
	def setTagsCloudMatchingIblsSets(self, pattern, flags=re.IGNORECASE):
		"""
		This method sets the pattern matching Ibl Sets and 
		updates :mod:`sibl_gui.components.core.databaseBrowser.databaseBrowser` Component Model content.

		:param pattern: Filtering pattern. ( String )
		:param flags: Regex filtering flags. ( Integer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Filtering Ibl Sets by Tags.")

		patternsDefault = (".*",)
		patternTokens = pattern.split() or patternsDefault

		allTags = set()
		filteredIblSets = []

		iblSets = self.__coreCollectionsOutliner.getCollectionsIblSets(
		self.__coreCollectionsOutliner.getSelectedCollections() or self.__coreCollectionsOutliner.getCollections())
		for iblSet in iblSets:
			comment = getattr(iblSet, "comment")
			if not comment:
				continue

			tagsCloud = strings.filterWords(strings.getWords(comment), filtersOut=self.__cloudExcludedTags, flags=flags)

			patternsMatched = True
			if patternTokens != patternsDefault:
				for pattern in patternTokens:
					patternMatched = False
					for tag in tagsCloud:
						if re.search(pattern, tag, flags=flags):
							patternMatched = True
							break
					patternsMatched *= patternMatched

			if patternsMatched:
				allTags.update(tagsCloud)
				filteredIblSets.append(iblSet)

		self.Tags_Cloud_listWidget.clear()
		self.Tags_Cloud_listWidget.addItems(sorted(allTags, key=lambda x:x.lower()))
		if collections.Counter(filteredIblSets) != collections.Counter(iblSets) or \
		len(self.__coreDatabaseBrowser.getActiveView().filterNodes("IblSet", "family")) != len(iblSets):
			filteredIblSets = [iblSet for iblSet in set(iblSets).intersection(set(filteredIblSets))]

			LOGGER.debug("> Tags Cloud filtered Ibl Set(s): '{0}'".format(
			", ".join((iblSet.name for iblSet in filteredIblSets))))

			self.__coreDatabaseBrowser.setIblSets(filteredIblSets)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setTimeMatchingIblSets(self, timeLow, timeHigh):
		"""
		This method sets the time matching Ibl Sets and 
		updates :mod:`sibl_gui.components.core.databaseBrowser.databaseBrowser` Component Model content.
		
		:param timeLow: Time low. ( QTime )
		:param timeHigh: Time high. ( QTime )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Filtering Ibl Sets by time range from '{0}' to '{1}'.".format(timeLow, timeHigh))

		iblSets = self.__coreCollectionsOutliner.getCollectionsIblSets(
				self.__coreCollectionsOutliner.getSelectedCollections())

		filteredIblSets = []
		for iblSet in iblSets:
			if not iblSet.time:
				continue

			hours, minutes, seconds = iblSet.time.split(":")
			int(hours) * 60 + int(minutes) >= timeLow.hour() * 60 + timeLow.minute() and \
			int(hours) * 60 + int(minutes) <= timeHigh.hour() * 60 + timeHigh.minute() and \
			filteredIblSets.append(iblSet)

		filteredIblSets = [iblSet for iblSet in set(iblSets).intersection(filteredIblSets)]

		if collections.Counter(filteredIblSets) != collections.Counter(iblSets) or \
		len(self.__coreDatabaseBrowser.getActiveView().filterNodes("IblSet", "family")) != len(iblSets):
			LOGGER.debug("> Time range filtered Ibl Set(s): '{0}'".format(
			", ".join((iblSet.name for iblSet in filteredIblSets))))

			self.__coreDatabaseBrowser.setIblSets(filteredIblSets)
		return True
