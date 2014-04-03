#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**searchDatabase.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`SearchDatabase` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import re
import itertools
import sys
if sys.version_info[:2] <= (2, 6):
	from counter import Counter
else:
	from collections import Counter
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QListView
from PyQt4.QtGui import QScrollArea

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.common
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.addons.searchDatabase.views import TagsCloud_QListView
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "SearchDatabase"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_Database.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class SearchDatabase(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.addons.searchDatabase.searchDatabase` Component Interface class.
	| It provides methods for the user to search into the Database using various filters.
	"""

	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param name: Component name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(SearchDatabase, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__dockArea = 2
		self.__viewSpacing = 4

		self.__engine = None

		self.__iblSetsOutliner = None
		self.__collectionsOutliner = None

		self.__view = None

		self.__cloudExcludedTags = ("a", "and", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with")

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def dockArea(self):
		"""
		Property for **self.__dockArea** attribute.

		:return: self.__dockArea.
		:rtype: int
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		Setter for **self.__dockArea** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		Deleter for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def viewSpacing(self):
		"""
		Property for **self.__viewSpacing** attribute.

		:return: self.__viewSpacing.
		:rtype: int
		"""

		return self.__viewSpacing

	@viewSpacing.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def viewSpacing(self, value):
		"""
		Setter for **self.__viewSpacing** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "viewSpacing"))

	@viewSpacing.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def viewSpacing(self):
		"""
		Deleter for **self.__viewSpacing** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "viewSpacing"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))


	@property
	def iblSetsOutliner(self):
		"""
		Property for **self.__iblSetsOutliner** attribute.

		:return: self.__iblSetsOutliner.
		:rtype: QWidget
		"""

		return self.__iblSetsOutliner

	@iblSetsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self, value):
		"""
		Setter for **self.__iblSetsOutliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsOutliner"))

	@iblSetsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self):
		"""
		Deleter for **self.__iblSetsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsOutliner"))

	@property
	def collectionsOutliner(self):
		"""
		Property for **self.__collectionsOutliner** attribute.

		:return: self.__collectionsOutliner.
		:rtype: QWidget
		"""

		return self.__collectionsOutliner

	@collectionsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def collectionsOutliner(self, value):
		"""
		Setter for **self.__collectionsOutliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "collectionsOutliner"))

	@collectionsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def collectionsOutliner(self):
		"""
		Deleter for **self.__collectionsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "collectionsOutliner"))

	@property
	def view(self):
		"""
		Property for **self.__view** attribute.

		:return: self.__view.
		:rtype: QWidget
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		Setter for **self.__view** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		Deleter for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def cloudExcludedTags(self):
		"""
		Property for **self.__cloudExcludedTags** attribute.

		:return: self.__cloudExcludedTags.
		:rtype: list
		"""

		return self.__cloudExcludedTags

	@cloudExcludedTags.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self, value):
		"""
		Setter for **self.__cloudExcludedTags** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "cloudExcludedTags"))

	@cloudExcludedTags.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def cloudExcludedTags(self):
		"""
		Deleter for **self.__cloudExcludedTags** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "cloudExcludedTags"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Engine to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine

		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]
		self.__collectionsOutliner = self.__engine.componentsManager["core.collectionsOutliner"]

		self.activated = True
		return True

	def deactivate(self):
		"""
		Deactivates the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.__iblSetsOutliner = None
		self.__collectionsOutliner = None

		self.activated = False
		return True

	def initializeUi(self):
		"""
		Initializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		umbra.ui.common.setToolBoxHeight(self.Search_toolBox)

		self.Tags_Cloud_listWidget.setParent(None)
		self.Tags_Cloud_listWidget = TagsCloud_QListView(self, message="No Tag to view!")
		self.Tags_Cloud_listWidget.setObjectName("Tags_Cloud_listWidget")
		self.Tags_Cloud_verticalLayout.addWidget(self.Tags_Cloud_listWidget)
		self.__view = self.Tags_Cloud_listWidget
		self.__view.setMovement(QListView.Static)
		self.__view.setResizeMode(QListView.Adjust)
		self.__view.setViewMode(QListView.IconMode)

		self.Search_Database_lineEdit = Search_QLineEdit(self)
		self.Search_Database_lineEdit.setPlaceholderText("Search In Tags Cloud ...")
		self.Search_Database_horizontalLayout.addWidget(self.Search_Database_lineEdit)
		self.__view.setSpacing(self.__viewSpacing)

		self.__cloudExcludedTags = list(itertools.chain.from_iterable(
									[(r"^{0}$".format(tag), r"^{0}$".format(tag.title()), r"^{0}$".format(tag.upper()))
									for tag in self.__cloudExcludedTags]))
		self.setTagsCloudMatchingIblsSetsUi()

		# Remove vertical scrollBars from **Search_toolBox** Widget.
		for scrollArea in self.findChildren(QScrollArea):
			scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		# Signals / Slots.
		self.Search_Database_lineEdit.textChanged.connect(self.__Search_Database_lineEdit__textChanged)
		self.Case_Sensitive_Matching_pushButton.clicked.connect(self.__Case_Sensitive_Matching_pushButton__clicked)
		self.Time_Low_timeEdit.timeChanged.connect(self.__Time_Low_timeEdit__timeChanged)
		self.Time_High_timeEdit.timeChanged.connect(self.__Time_High_timeEdit__timeChanged)
		self.__view.itemDoubleClicked.connect(self.__view__doubleClicked)
		self.__collectionsOutliner.view.selectionModel().selectionChanged.connect(
		self.__collectionsOutliner_view_selectionModel__selectionChanged)

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		Uninitializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.Search_Database_lineEdit.textChanged.disconnect(self.__Search_Database_lineEdit__textChanged)
		self.Case_Sensitive_Matching_pushButton.clicked.disconnect(self.__Case_Sensitive_Matching_pushButton__clicked)
		self.Time_Low_timeEdit.timeChanged.disconnect(self.__Time_Low_timeEdit__timeChanged)
		self.Time_High_timeEdit.timeChanged.disconnect(self.__Time_High_timeEdit__timeChanged)
		self.__view.itemDoubleClicked.disconnect(self.__view__doubleClicked)
		self.__collectionsOutliner.view.selectionModel().selectionChanged.disconnect(
		self.__collectionsOutliner_view_selectionModel__selectionChanged)

		self.Search_Database_lineEdit.setParent(None)
		self.Search_Database_lineEdit = None

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	def __Search_Database_lineEdit__textChanged(self, text):
		"""
		Defines the slot triggered by **Search_Database_lineEdit** Widget when text changed.

		:param text: Current text value.
		:type text: QString
		"""

		self.setTagsCloudMatchingIblsSetsUi()

	def __Case_Sensitive_Matching_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Case_Sensitive_Matching_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.setTagsCloudMatchingIblsSetsUi()

	def __Time_Low_timeEdit__timeChanged(self, time):
		"""
		Defines the slot triggered by **Time_Low_timeEdit** Widget when time changed.

		:param time: Current time.
		:type time: QTime
		"""

		self.Time_Low_timeEdit.time() >= self.Time_High_timeEdit.time() and \
		self.Time_Low_timeEdit.setTime(self.Time_High_timeEdit.time().addSecs(-60))
		self.setTimeMatchingIblSetsUi()

	def __Time_High_timeEdit__timeChanged(self, time):
		"""
		Defines the slot triggered by **Time_Low_timeEdit** Widget when time changed.

		:param time: Current time.
		:type time: QTime
		"""

		self.Time_High_timeEdit.time() <= self.Time_Low_timeEdit.time() and \
		self.Time_High_timeEdit.setTime(self.Time_Low_timeEdit.time().addSecs(60))
		self.setTimeMatchingIblSetsUi()

	def __view__doubleClicked(self, listWidgetItem):
		"""
		Defines the slot triggered by the View when double clicked.

		:param listWidgetItem: List Widget item.
		:type listWidgetItem: QlistWidgetItem
		"""

		self.Search_Database_lineEdit.setText("{0} {1}".format(self.Search_Database_lineEdit.text(), listWidgetItem.text()))

	def __collectionsOutliner_view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		Defines the slot triggered by **collectionsOutliner.view** Model when selection changed

		:param selectedItems: Selected items.
		:type selectedItems: QItemSelection
		:param deselectedItems: Deselected items.
		:type deselectedItems: QItemSelection
		"""

		self.setTagsCloudMatchingIblsSetsUi()

	def setTagsCloudMatchingIblsSetsUi(self):
		"""
		Sets the user defined pattern matching Ibl Sets and 
		updates :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner` Component Model content.
		
		:return: Method success.
		:rtype: bool
		
		:note: May require user interaction.
		"""

		return self.setTagsCloudMatchingIblsSets(foundations.strings.toString(self.Search_Database_lineEdit.text()),
		not self.Case_Sensitive_Matching_pushButton.isChecked() and re.IGNORECASE or 0)

	def setTimeMatchingIblSetsUi(self):
		"""
		Sets the user defined time matching Ibl Sets and 
		updates :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner` Component Model content.
		
		:return: Method success.
		:rtype: bool
		
		:note: May require user interaction.
		"""

		return self.setTimeMatchingIblSets(self.Time_Low_timeEdit.time(), self.Time_High_timeEdit.time())

	def setTagsCloudMatchingIblsSets(self, pattern, flags=re.IGNORECASE):
		"""
		Sets the pattern matching Ibl Sets and 
		updates :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner` Component Model content.

		:param pattern: Filtering pattern.
		:type pattern: unicode
		:param flags: Regex filtering flags.
		:type flags: int
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Filtering Ibl Sets by Tags.")

		patternsDefault = (".*",)
		patternTokens = pattern.split() or patternsDefault

		allTags = set()
		filteredIblSets = []

		iblSets = self.__collectionsOutliner.getCollectionsIblSets(
		self.__collectionsOutliner.getSelectedCollections() or self.__collectionsOutliner.getCollections())
		for iblSet in iblSets:
			comment = getattr(iblSet, "comment")
			if not comment:
				continue

			tagsCloud = foundations.strings.filterWords(foundations.strings.getWords(comment),
														filtersOut=self.__cloudExcludedTags,
														flags=flags)

			patternsMatched = True
			if patternTokens != patternsDefault:
				for pattern in patternTokens:
					patternMatched = False
					try:
						pattern = re.compile(pattern, flags)
						for tag in tagsCloud:
							if re.search(pattern, tag, flags=flags):
								patternMatched = True
								break
					except re.error:
						LOGGER.warning("!> {0} | '{1}' regex pattern is invalid!".format(self.__class__.__name__, pattern))
					patternsMatched *= patternMatched

			if patternsMatched:
				allTags.update(tagsCloud)
				filteredIblSets.append(iblSet)

		self.__view.clear()
		self.__view.addItems(sorted(allTags, key=lambda x:x.lower()))
		if Counter(filteredIblSets) != Counter(iblSets) or \
		len(self.__iblSetsOutliner.getActiveView().filterNodes("IblSet", "family")) != len(iblSets):
			filteredIblSets = [iblSet for iblSet in set(iblSets).intersection(set(filteredIblSets))]

			LOGGER.debug("> Tags Cloud filtered Ibl Set(s): '{0}'".format(
			", ".join((foundations.strings.toString(iblSet.name) for iblSet in filteredIblSets))))

			self.__iblSetsOutliner.setIblSets(filteredIblSets)
		return True

	def setTimeMatchingIblSets(self, timeLow, timeHigh):
		"""
		Sets the time matching Ibl Sets and 
		updates :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner` Component Model content.
		
		:param timeLow: Time low.
		:type timeLow: QTime
		:param timeHigh: Time high.
		:type timeHigh: QTime
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Filtering Ibl Sets by time range from '{0}' to '{1}'.".format(timeLow, timeHigh))

		iblSets = self.__collectionsOutliner.getCollectionsIblSets(
				self.__collectionsOutliner.getSelectedCollections())

		filteredIblSets = []
		for iblSet in iblSets:
			if not iblSet.time:
				continue

			hours, minutes, seconds = iblSet.time.split(":")
			int(hours) * 60 + int(minutes) >= timeLow.hour() * 60 + timeLow.minute() and \
			int(hours) * 60 + int(minutes) <= timeHigh.hour() * 60 + timeHigh.minute() and \
			filteredIblSets.append(iblSet)

		filteredIblSets = [iblSet for iblSet in set(iblSets).intersection(filteredIblSets)]

		if Counter(filteredIblSets) != Counter(iblSets) or \
		len(self.__iblSetsOutliner.getActiveView().filterNodes("IblSet", "family")) != len(iblSets):
			LOGGER.debug("> Time range filtered Ibl Set(s): '{0}'".format(
			", ".join((iblSet.name for iblSet in filteredIblSets))))

			self.__iblSetsOutliner.setIblSets(filteredIblSets)
		return True
