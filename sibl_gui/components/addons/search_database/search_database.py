#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**search_database.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`SearchDatabase` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

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

import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.common
from manager.QWidget_component import QWidgetComponentFactory
from sibl_gui.components.addons.search_database.views import TagsCloud_QListView
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "SearchDatabase"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_Database.ui")

class SearchDatabase(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`sibl_gui.components.addons.search_database.search_database` Component Interface class.
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

        self.__dock_area = 2
        self.__view_spacing = 4

        self.__engine = None

        self.__ibl_sets_outliner = None
        self.__collections_outliner = None

        self.__view = None

        self.__cloud_excluded_tags = ("a", "and", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with")

    @property
    def dock_area(self):
        """
        Property for **self.__dock_area** attribute.

        :return: self.__dock_area.
        :rtype: int
        """

        return self.__dock_area

    @dock_area.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def dock_area(self, value):
        """
        Setter for **self.__dock_area** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dock_area"))

    @dock_area.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def dock_area(self):
        """
        Deleter for **self.__dock_area** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dock_area"))

    @property
    def view_spacing(self):
        """
        Property for **self.__view_spacing** attribute.

        :return: self.__view_spacing.
        :rtype: int
        """

        return self.__view_spacing

    @view_spacing.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def view_spacing(self, value):
        """
        Setter for **self.__view_spacing** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view_spacing"))

    @view_spacing.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def view_spacing(self):
        """
        Deleter for **self.__view_spacing** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view_spacing"))

    @property
    def engine(self):
        """
        Property for **self.__engine** attribute.

        :return: self.__engine.
        :rtype: QObject
        """

        return self.__engine

    @engine.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def engine(self, value):
        """
        Setter for **self.__engine** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

    @engine.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def engine(self):
        """
        Deleter for **self.__engine** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))


    @property
    def ibl_sets_outliner(self):
        """
        Property for **self.__ibl_sets_outliner** attribute.

        :return: self.__ibl_sets_outliner.
        :rtype: QWidget
        """

        return self.__ibl_sets_outliner

    @ibl_sets_outliner.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ibl_sets_outliner(self, value):
        """
        Setter for **self.__ibl_sets_outliner** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ibl_sets_outliner"))

    @ibl_sets_outliner.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ibl_sets_outliner(self):
        """
        Deleter for **self.__ibl_sets_outliner** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ibl_sets_outliner"))

    @property
    def collections_outliner(self):
        """
        Property for **self.__collections_outliner** attribute.

        :return: self.__collections_outliner.
        :rtype: QWidget
        """

        return self.__collections_outliner

    @collections_outliner.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def collections_outliner(self, value):
        """
        Setter for **self.__collections_outliner** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "collections_outliner"))

    @collections_outliner.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def collections_outliner(self):
        """
        Deleter for **self.__collections_outliner** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "collections_outliner"))

    @property
    def view(self):
        """
        Property for **self.__view** attribute.

        :return: self.__view.
        :rtype: QWidget
        """

        return self.__view

    @view.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def view(self, value):
        """
        Setter for **self.__view** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

    @view.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def view(self):
        """
        Deleter for **self.__view** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

    @property
    def cloud_excluded_tags(self):
        """
        Property for **self.__cloud_excluded_tags** attribute.

        :return: self.__cloud_excluded_tags.
        :rtype: list
        """

        return self.__cloud_excluded_tags

    @cloud_excluded_tags.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def cloud_excluded_tags(self, value):
        """
        Setter for **self.__cloud_excluded_tags** attribute.

        :param value: Attribute value.
        :type value: list
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "cloud_excluded_tags"))

    @cloud_excluded_tags.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def cloud_excluded_tags(self):
        """
        Deleter for **self.__cloud_excluded_tags** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "cloud_excluded_tags"))

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

        self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]
        self.__collections_outliner = self.__engine.components_manager["core.collections_outliner"]

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

        self.__ibl_sets_outliner = None
        self.__collections_outliner = None

        self.activated = False
        return True

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        umbra.ui.common.set_toolBox_height(self.Search_toolBox)

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
        self.__view.setSpacing(self.__view_spacing)

        self.__cloud_excluded_tags = list(itertools.chain.from_iterable(
                                    [(r"^{0}$".format(tag), r"^{0}$".format(tag.title()), r"^{0}$".format(tag.upper()))
                                    for tag in self.__cloud_excluded_tags]))
        self.set_tags_cloud_matching_ibls_sets_ui()

        # Remove vertical scrollBars from **Search_toolBox** Widget.
        for scrollArea in self.findChildren(QScrollArea):
            scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Signals / Slots.
        self.Search_Database_lineEdit.textChanged.connect(self.__Search_Database_lineEdit__textChanged)
        self.Case_Sensitive_Matching_pushButton.clicked.connect(self.__Case_Sensitive_Matching_pushButton__clicked)
        self.Time_Low_timeEdit.timeChanged.connect(self.__Time_Low_timeEdit__timeChanged)
        self.Time_High_timeEdit.timeChanged.connect(self.__Time_High_timeEdit__timeChanged)
        self.__view.itemDoubleClicked.connect(self.__view__doubleClicked)
        self.__collections_outliner.view.selectionModel().selectionChanged.connect(
        self.__collections_outliner_view_selectionModel__selectionChanged)

        self.initialized_ui = True
        return True

    def uninitialize_ui(self):
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
        self.__collections_outliner.view.selectionModel().selectionChanged.disconnect(
        self.__collections_outliner_view_selectionModel__selectionChanged)

        self.Search_Database_lineEdit.setParent(None)
        self.Search_Database_lineEdit = None

        self.initialized_ui = False
        return True

    def add_widget(self):
        """
        Adds the Component Widget to the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

        self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dock_area), self)

        return True

    def remove_widget(self):
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

        self.set_tags_cloud_matching_ibls_sets_ui()

    def __Case_Sensitive_Matching_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Case_Sensitive_Matching_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.set_tags_cloud_matching_ibls_sets_ui()

    def __Time_Low_timeEdit__timeChanged(self, time):
        """
        Defines the slot triggered by **Time_Low_timeEdit** Widget when time changed.

        :param time: Current time.
        :type time: QTime
        """

        self.Time_Low_timeEdit.time() >= self.Time_High_timeEdit.time() and \
        self.Time_Low_timeEdit.setTime(self.Time_High_timeEdit.time().addSecs(-60))
        self.set_time_matching_ibl_sets_ui()

    def __Time_High_timeEdit__timeChanged(self, time):
        """
        Defines the slot triggered by **Time_Low_timeEdit** Widget when time changed.

        :param time: Current time.
        :type time: QTime
        """

        self.Time_High_timeEdit.time() <= self.Time_Low_timeEdit.time() and \
        self.Time_High_timeEdit.setTime(self.Time_Low_timeEdit.time().addSecs(60))
        self.set_time_matching_ibl_sets_ui()

    def __view__doubleClicked(self, list_widget_item):
        """
        Defines the slot triggered by the View when double clicked.

        :param list_widget_item: List Widget item.
        :type list_widget_item: Qlist_widget_item
        """

        self.Search_Database_lineEdit.setText("{0} {1}".format(self.Search_Database_lineEdit.text(), list_widget_item.text()))

    def __collections_outliner_view_selectionModel__selectionChanged(self, selected_items, deselected_items):
        """
        Defines the slot triggered by **collections_outliner.view** Model when selection changed

        :param selected_items: Selected items.
        :type selected_items: QItemSelection
        :param deselected_items: Deselected items.
        :type deselected_items: QItemSelection
        """

        self.set_tags_cloud_matching_ibls_sets_ui()

    def set_tags_cloud_matching_ibls_sets_ui(self):
        """
        Sets the user defined pattern matching Ibl Sets and
        updates :mod:`sibl_gui.components.core.ibl_sets_outliner.ibl_sets_outliner` Component Model content.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        return self.set_tags_cloud_matching_ibls_sets(foundations.strings.to_string(self.Search_Database_lineEdit.text()),
        not self.Case_Sensitive_Matching_pushButton.isChecked() and re.IGNORECASE or 0)

    def set_time_matching_ibl_sets_ui(self):
        """
        Sets the user defined time matching Ibl Sets and
        updates :mod:`sibl_gui.components.core.ibl_sets_outliner.ibl_sets_outliner` Component Model content.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        return self.set_time_matching_ibl_sets(self.Time_Low_timeEdit.time(), self.Time_High_timeEdit.time())

    def set_tags_cloud_matching_ibls_sets(self, pattern, flags=re.IGNORECASE):
        """
        Sets the pattern matching Ibl Sets and
        updates :mod:`sibl_gui.components.core.ibl_sets_outliner.ibl_sets_outliner` Component Model content.

        :param pattern: Filtering pattern.
        :type pattern: unicode
        :param flags: Regex filtering flags.
        :type flags: int
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Filtering Ibl Sets by Tags.")

        patterns_default = (".*",)
        pattern_tokens = pattern.split() or patterns_default

        all_tags = set()
        filtered_ibl_sets = []

        ibl_sets = self.__collections_outliner.get_collections_ibl_sets(
        self.__collections_outliner.get_selected_collections() or self.__collections_outliner.get_collections())
        for ibl_set in ibl_sets:
            comment = getattr(ibl_set, "comment")
            if not comment:
                continue

            tags_cloud = foundations.strings.filter_words(foundations.strings.get_words(comment),
                                                        filters_out=self.__cloud_excluded_tags,
                                                        flags=flags)

            patterns_matched = True
            if pattern_tokens != patterns_default:
                for pattern in pattern_tokens:
                    pattern_matched = False
                    try:
                        pattern = re.compile(pattern, flags)
                        for tag in tags_cloud:
                            if re.search(pattern, tag):
                                pattern_matched = True
                                break
                    except re.error:
                        LOGGER.warning("!> {0} | '{1}' regex pattern is invalid!".format(self.__class__.__name__, pattern))
                    patterns_matched *= pattern_matched

            if patterns_matched:
                all_tags.update(tags_cloud)
                filtered_ibl_sets.append(ibl_set)

        self.__view.clear()
        self.__view.addItems(sorted(all_tags, key=lambda x:x.lower()))
        if Counter(filtered_ibl_sets) != Counter(ibl_sets) or \
        len(self.__ibl_sets_outliner.get_active_view().filter_nodes("IblSet", "family")) != len(ibl_sets):
            filtered_ibl_sets = [ibl_set for ibl_set in set(ibl_sets).intersection(set(filtered_ibl_sets))]

            LOGGER.debug("> Tags Cloud filtered Ibl Set(s): '{0}'".format(
            ", ".join((foundations.strings.to_string(ibl_set.name) for ibl_set in filtered_ibl_sets))))

            self.__ibl_sets_outliner.set_ibl_sets(filtered_ibl_sets)
        return True

    def set_time_matching_ibl_sets(self, time_low, time_high):
        """
        Sets the time matching Ibl Sets and
        updates :mod:`sibl_gui.components.core.ibl_sets_outliner.ibl_sets_outliner` Component Model content.

        :param time_low: Time low.
        :type time_low: QTime
        :param time_high: Time high.
        :type time_high: QTime
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Filtering Ibl Sets by time range from '{0}' to '{1}'.".format(time_low, time_high))

        ibl_sets = self.__collections_outliner.get_collections_ibl_sets(
                self.__collections_outliner.get_selected_collections())

        filtered_ibl_sets = []
        for ibl_set in ibl_sets:
            if not ibl_set.time:
                continue

            hours, minutes, seconds = ibl_set.time.split(":")
            int(hours) * 60 + int(minutes) >= time_low.hour() * 60 + time_low.minute() and \
            int(hours) * 60 + int(minutes) <= time_high.hour() * 60 + time_high.minute() and \
            filtered_ibl_sets.append(ibl_set)

        filtered_ibl_sets = [ibl_set for ibl_set in set(ibl_sets).intersection(filtered_ibl_sets)]

        if Counter(filtered_ibl_sets) != Counter(ibl_sets) or \
        len(self.__ibl_sets_outliner.get_active_view().filter_nodes("IblSet", "family")) != len(ibl_sets):
            LOGGER.debug("> Time range filtered Ibl Set(s): '{0}'".format(
            ", ".join((ibl_set.name for ibl_set in filtered_ibl_sets))))

            self.__ibl_sets_outliner.set_ibl_sets(filtered_ibl_sets)
        return True
