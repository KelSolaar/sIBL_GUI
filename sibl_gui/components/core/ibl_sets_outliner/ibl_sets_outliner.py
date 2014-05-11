#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**ibl_sets_outliner.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`IblSetsOutliner` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import functools
import os
import platform
import re
import sys
if sys.version_info[:2] <= (2, 6):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QStringListModel

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import foundations.walkers
import sibl_gui.components.core.database.exceptions
import sibl_gui.components.core.database.operations
import sibl_gui.ui.common
import umbra.engine
import umbra.exceptions
import umbra.ui.common
import umbra.ui.nodes
import umbra.ui.widgets.message_box as message_box
from manager.QWidget_component import QWidgetComponentFactory
from sibl_gui.components.core.database.nodes import IblSetNode
from sibl_gui.components.core.ibl_sets_outliner.models import IblSetsModel
from sibl_gui.components.core.ibl_sets_outliner.views import Details_QTreeView
from sibl_gui.components.core.ibl_sets_outliner.views import Thumbnails_QListView
from umbra.globals.ui_constants import UiConstants
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "IblSetsOutliner"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Ibl_Sets_Outliner.ui")

class IblSetsOutliner(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`sibl_gui.components.core.ibl_sets_outliner.ibl_sets_outliner` Component Interface class.
    | It defines methods for Database Ibl Sets management.
    """

    # Custom signals definitions.
    refresh_nodes = pyqtSignal()
    """
    This signal is emited by the :class:`IblSetsOutliner` class when :obj:`IblSetsOutliner.model` class property model
    nodes needs to be refreshed.
    """

    active_view_changed = pyqtSignal(int)
    """
    This signal is emited by the :class:`IblSetsOutliner` class when the current active View is changed.

    :return: Current active view index.
    :rtype: int
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

        super(IblSetsOutliner, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = False

        self.__ui_resources_directory = "resources"
        self.__ui_thumbnails_view_image = "Thumbnails_View.png"
        self.__ui_columns_view_image = "Columns_View.png"
        self.__ui_details_view_image = "Details_View.png"
        self.__ui_largest_size_image = "Largest_Size.png"
        self.__ui_smallest_size_image = "Smallest_Size.png"
        self.__ui_panoramic_loading_image = "Panoramic_Loading.png"
        self.__ui_square_loading_image = "Square_Loading.png"
        self.__ui_switch_thumbnails_type_image = "Switch_Thumbnails_Type.png"
        self.__dock_area = 8

        self.__engine = None
        self.__settings = None
        self.__settings_section = None
        self.__settings_separator = ","

        self.__extension = "ibl"

        self.__inspect_layout = "inspect_centric"

        self.__script_editor = None
        self.__collections_outliner = None

        self.__model = None
        self.__views = None
        self.__views_push_buttons = None
        self.__thumbnails_view = None
        self.__details_view = None
        self.__details_headers = OrderedDict([("Ibl Set", "title"),
                                        ("Author", "author"),
                                        ("Shot Location", "location"),
                                        ("Latitude", "latitude"),
                                        ("Longitude", "longitude"),
                                        ("Shot Date", "date"),
                                        ("Shot Time", "time"),
                                        ("Comment", "comment")])

        self.__panoramic_thumbnails = "True"
        self.__panoramic_thumbnails_size = "XLarge"
        self.__square_thumbnails_size = "Medium"
        self.__thumbnails_minimum_size = "XSmall"

        self.__search_contexts = OrderedDict([("Search In Names", "title"),
                                ("Search In Authors", "author"),
                                ("Search In Links", "link"),
                                ("Search In Locations", "location"),
                                ("Search In Comments", "comment")])
        self.__active_search_context = "Search In Names"
        self.__search_context_menu = None

        self.__icon_place_holder = None

    @property
    def ui_resources_directory(self):
        """
        Property for **self.__ui_resources_directory** attribute.

        :return: self.__ui_resources_directory.
        :rtype: unicode
        """

        return self.__ui_resources_directory

    @ui_resources_directory.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_resources_directory(self, value):
        """
        Setter for **self.__ui_resources_directory** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_resources_directory"))

    @ui_resources_directory.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_resources_directory(self):
        """
        Deleter for **self.__ui_resources_directory** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_resources_directory"))

    @property
    def ui_thumbnails_view_image(self):
        """
        Property for **self.__ui_thumbnails_view_image** attribute.

        :return: self.__ui_thumbnails_view_image.
        :rtype: unicode
        """

        return self.__ui_thumbnails_view_image

    @ui_thumbnails_view_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_thumbnails_view_image(self, value):
        """
        Setter for **self.__ui_thumbnails_view_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_thumbnails_view_image"))

    @ui_thumbnails_view_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_thumbnails_view_image(self):
        """
        Deleter for **self.__ui_thumbnails_view_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_thumbnails_view_image"))

    @property
    def ui_columns_view_image(self):
        """
        Property for **self.__ui_columns_view_image** attribute.

        :return: self.__ui_columns_view_image.
        :rtype: unicode
        """

        return self.__ui_columns_view_image

    @ui_columns_view_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_columns_view_image(self, value):
        """
        Setter for **self.__ui_columns_view_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_columns_view_image"))

    @ui_columns_view_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_columns_view_image(self):
        """
        Deleter for **self.__ui_columns_view_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_columns_view_image"))

    @property
    def ui_details_view_image(self):
        """
        Property for **self.__ui_details_view_image** attribute.

        :return: self.__ui_details_view_image.
        :rtype: unicode
        """

        return self.__ui_details_view_image

    @ui_details_view_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_details_view_image(self, value):
        """
        Setter for **self.__ui_details_view_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_details_view_image"))

    @ui_details_view_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_details_view_image(self):
        """
        Deleter for **self.__ui_details_view_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_details_view_image"))

    @property
    def ui_largest_size_image(self):
        """
        Property for **self.__ui_largest_size_image** attribute.

        :return: self.__ui_largest_size_image.
        :rtype: unicode
        """

        return self.__ui_largest_size_image

    @ui_largest_size_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_largest_size_image(self, value):
        """
        Setter for **self.__ui_largest_size_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_largest_size_image"))

    @ui_largest_size_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_largest_size_image(self):
        """
        Deleter for **self.__ui_largest_size_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_largest_size_image"))

    @property
    def ui_smallest_size_image(self):
        """
        Property for **self.__ui_smallest_size_image** attribute.

        :return: self.__ui_smallest_size_image.
        :rtype: unicode
        """

        return self.__ui_smallest_size_image

    @ui_smallest_size_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_smallest_size_image(self, value):
        """
        Setter for **self.__ui_smallest_size_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_smallest_size_image"))

    @ui_smallest_size_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_smallest_size_image(self):
        """
        Deleter for **self.__ui_smallest_size_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_smallest_size_image"))

    @property
    def ui_panoramic_loading_image(self):
        """
        Property for **self.__ui_panoramic_loading_image** attribute.

        :return: self.__ui_panoramic_loading_image.
        :rtype: unicode
        """

        return self.__ui_panoramic_loading_image

    @ui_panoramic_loading_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_panoramic_loading_image(self, value):
        """
        Setter for **self.__ui_panoramic_loading_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_panoramic_loading_image"))

    @ui_panoramic_loading_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_panoramic_loading_image(self):
        """
        Deleter for **self.__ui_panoramic_loading_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_panoramic_loading_image"))

    @property
    def ui_square_loading_image(self):
        """
        Property for **self.__ui_square_loading_image** attribute.

        :return: self.__ui_square_loading_image.
        :rtype: unicode
        """

        return self.__ui_square_loading_image

    @ui_square_loading_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_square_loading_image(self, value):
        """
        Setter for **self.__ui_square_loading_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_square_loading_image"))

    @ui_square_loading_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_square_loading_image(self):
        """
        Deleter for **self.__ui_square_loading_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_square_loading_image"))
    @property
    def ui_switch_thumbnails_type_image(self):
        """
        Property for **self.__ui_switch_thumbnails_type_image** attribute.

        :return: self.__ui_switch_thumbnails_type_image.
        :rtype: unicode
        """

        return self.__ui_switch_thumbnails_type_image

    @ui_switch_thumbnails_type_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_switch_thumbnails_type_image(self, value):
        """
        Setter for **self.__ui_switch_thumbnails_type_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_switch_thumbnails_type_image"))

    @ui_switch_thumbnails_type_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_switch_thumbnails_type_image(self):
        """
        Deleter for **self.__ui_switch_thumbnails_type_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_switch_thumbnails_type_image"))

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
    def settings(self):
        """
        Property for **self.__settings** attribute.

        :return: self.__settings.
        :rtype: QSettings
        """

        return self.__settings

    @settings.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings(self, value):
        """
        Setter for **self.__settings** attribute.

        :param value: Attribute value.
        :type value: QSettings
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

    @settings.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings(self):
        """
        Deleter for **self.__settings** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

    @property
    def settings_section(self):
        """
        Property for **self.__settings_section** attribute.

        :return: self.__settings_section.
        :rtype: unicode
        """

        return self.__settings_section

    @settings_section.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings_section(self, value):
        """
        Setter for **self.__settings_section** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings_section"))

    @settings_section.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings_section(self):
        """
        Deleter for **self.__settings_section** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings_section"))

    @property
    def settings_separator(self):
        """
        Property for **self.__settings_separator** attribute.

        :return: self.__settings_separator.
        :rtype: unicode
        """

        return self.__settings_separator

    @settings_separator.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings_separator(self, value):
        """
        Setter for **self.__settings_separator** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings_separator"))

    @settings_separator.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings_separator(self):
        """
        Deleter for **self.__settings_separator** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings_separator"))

    @property
    def extension(self):
        """
        Property for **self.__extension** attribute.

        :return: self.__extension.
        :rtype: unicode
        """

        return self.__extension

    @extension.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def extension(self, value):
        """
        Setter for **self.__extension** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "extension"))

    @extension.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def extension(self):
        """
        Deleter for **self.__extension** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

    @property
    def inspect_layout(self):
        """
        Property for **self.__inspect_layout** attribute.

        :return: self.__inspect_layout.
        :rtype: unicode
        """

        return self.__inspect_layout

    @inspect_layout.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def inspect_layout(self, value):
        """
        Setter for **self.__inspect_layout** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspect_layout"))

    @inspect_layout.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def inspect_layout(self):
        """
        Deleter for **self.__inspect_layout** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspect_layout"))

    @property
    def script_editor(self):
        """
        Property for **self.__script_editor** attribute.

        :return: self.__script_editor.
        :rtype: QWidget
        """

        return self.__script_editor

    @script_editor.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def script_editor(self, value):
        """
        Setter for **self.__script_editor** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "script_editor"))

    @script_editor.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def script_editor(self):
        """
        Deleter for **self.__script_editor** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "script_editor"))

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
    def model(self):
        """
        Property for **self.__model** attribute.

        :return: self.__model.
        :rtype: IblSetsModel
        """

        return self.__model

    @model.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self, value):
        """
        Setter for **self.__model** attribute.

        :param value: Attribute value.
        :type value: IblSetsModel
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

    @model.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self):
        """
        Deleter for **self.__model** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

    @property
    def views(self):
        """
        Property for **self.__views** attribute.

        :return: self.__views.
        :rtype: tuple
        """

        return self.__views

    @views.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def views(self, value):
        """
        Setter for **self.__views** attribute.

        :param value: Attribute value.
        :type value: tuple
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "views"))

    @views.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def views(self):
        """
        Deleter for **self.__views** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "views"))

    @property
    def views_push_buttons(self):
        """
        Property for **self.__views_push_buttons** attribute.

        :return: self.__views_push_buttons.
        :rtype: dict
        """

        return self.__views_push_buttons

    @views_push_buttons.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def views_push_buttons(self, value):
        """
        Setter for **self.__views_push_buttons** attribute.

        :param value: Attribute value.
        :type value: dict
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "views_push_buttons"))

    @views_push_buttons.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def views_push_buttons(self):
        """
        Deleter for **self.__views_push_buttons** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "views_push_buttons"))

    @property
    def thumbnails_view(self):
        """
        Property for **self.__thumbnails_view** attribute.

        :return: self.__thumbnails_view.
        :rtype: QListView
        """

        return self.__thumbnails_view

    @thumbnails_view.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def thumbnails_view(self, value):
        """
        Setter for **self.__thumbnails_view** attribute.

        :param value: Attribute value.
        :type value: QListView
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "thumbnails_view"))

    @thumbnails_view.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def thumbnails_view(self):
        """
        Deleter for **self.__thumbnails_view** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

    @property
    def details_view(self):
        """
        Property for **self.__details_view** attribute.

        :return: self.__details_view.
        :rtype: QTreeView
        """

        return self.__details_view

    @details_view.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def details_view(self, value):
        """
        Setter for **self.__details_view** attribute.

        :param value: Attribute value.
        :type value: QTreeView
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "details_view"))

    @details_view.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def details_view(self):
        """
        Deleter for **self.__details_view** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

    @property
    def details_viewHeaders(self):
        """
        Property for **self.__details_viewHeaders** attribute.

        :return: self.__details_viewHeaders.
        :rtype: OrderedDict
        """

        return self.__details_viewHeaders

    @details_viewHeaders.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def details_viewHeaders(self, value):
        """
        Setter for **self.__details_viewHeaders** attribute.

        :param value: Attribute value.
        :type value: OrderedDict
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "details_viewHeaders"))

    @details_viewHeaders.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def details_viewHeaders(self):
        """
        Deleter for **self.__details_viewHeaders** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

    @property
    def panoramic_thumbnails(self):
        """
        Property for **self.__panoramic_thumbnails** attribute.

        :return: self.__panoramic_thumbnails.
        :rtype: bool
        """

        return self.__panoramic_thumbnails

    @panoramic_thumbnails.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def panoramic_thumbnails(self, value):
        """
        Setter for **self.__panoramic_thumbnails** attribute.

        :param value: Attribute value.
        :type value: bool
        """

        if value is not None:
            assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("panoramic_thumbnails", value)
        self.set_panoramic_thumbnails(value)

    @panoramic_thumbnails.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def panoramic_thumbnails(self):
        """
        Deleter for **self.__panoramic_thumbnails** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "panoramic_thumbnails"))

    @property
    def panoramic_thumbnails_size(self):
        """
        Property for **self.__panoramic_thumbnails_size** attribute.

        :return: self.__panoramic_thumbnails_size.
        :rtype: unicode
        """

        return self.__panoramic_thumbnails_size

    @panoramic_thumbnails_size.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def panoramic_thumbnails_size(self, value):
        """
        Setter for **self.__panoramic_thumbnails_size** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("panoramic_thumbnails_size", value)
        self.__panoramic_thumbnails_size = value

    @panoramic_thumbnails_size.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def panoramic_thumbnails_size(self):
        """
        Deleter for **self.__panoramic_thumbnails_size** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "panoramic_thumbnails_size"))

    @property
    def square_thumbnails_size(self):
        """
        Property for **self.__square_thumbnails_size** attribute.

        :return: self.__square_thumbnails_size.
        :rtype: unicode
        """

        return self.__square_thumbnails_size

    @square_thumbnails_size.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def square_thumbnails_size(self, value):
        """
        Setter for **self.__square_thumbnails_size** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("square_thumbnails_size", value)
        self.__square_thumbnails_size = value

    @square_thumbnails_size.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def square_thumbnails_size(self):
        """
        Deleter for **self.__square_thumbnails_size** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "square_thumbnails_size"))

    @property
    def thumbnails_minimum_size(self):
        """
        Property for **self.__thumbnails_minimum_size** attribute.

        :return: self.__thumbnails_minimum_size.
        :rtype: dict
        """

        return self.__thumbnails_minimum_size

    @thumbnails_minimum_size.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def thumbnails_minimum_size(self, value):
        """
        Setter for **self.__thumbnails_minimum_size** attribute.

        :param value: Attribute value.
        :type value: dict
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("thumbnails_minimum_size", value)
        self.__thumbnails_minimum_size = value

    @thumbnails_minimum_size.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def thumbnails_minimum_size(self):
        """
        Deleter for **self.__thumbnails_minimum_size** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "thumbnails_minimum_size"))

    @property
    def search_contexts(self):
        """
        Property for **self.__search_contexts** attribute.

        :return: self.__search_contexts.
        :rtype: OrderedDict
        """

        return self.__search_contexts

    @search_contexts.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def search_contexts(self, value):
        """
        Setter for **self.__search_contexts** attribute.

        :param value: Attribute value.
        :type value: OrderedDict
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "search_contexts"))

    @search_contexts.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def search_contexts(self):
        """
        Deleter for **self.__search_contexts** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "search_contexts"))

    @property
    def active_search_context(self):
        """
        Property for **self.__active_search_context** attribute.

        :return: self.__active_search_context.
        :rtype: OrderedDict
        """

        return self.__active_search_context

    @active_search_context.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def active_search_context(self, value):
        """
        Setter for **self.__active_search_context** attribute.

        :param value: Attribute value.
        :type value: OrderedDict
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "active_search_context"))

    @active_search_context.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def active_search_context(self):
        """
        Deleter for **self.__active_search_context** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "active_search_context"))

    @property
    def search_context_menu(self):
        """
        Property for **self.__search_context_menu** attribute.

        :return: self.__search_context_menu.
        :rtype: QMenu
        """

        return self.__search_context_menu

    @search_context_menu.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def search_context_menu(self, value):
        """
        Setter for **self.__search_context_menu** attribute.

        :param value: Attribute value. ( self.__search_context_menu )
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "search_context_menu"))

    @search_context_menu.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def search_context_menu(self):
        """
        Deleter for **self.__search_context_menu** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "search_context_menu"))

    def activate(self, engine):
        """
        Activates the Component.

        :param engine: Engine to attach the Component to.
        :type engine: QObject
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

        self.__ui_resources_directory = os.path.join(os.path.dirname(__file__), self.__ui_resources_directory)
        self.__engine = engine
        self.__settings = self.__engine.settings
        self.__settings_section = self.name

        self.__script_editor = self.__engine.components_manager["factory.script_editor"]
        self.__collections_outliner = self.__engine.components_manager["core.collections_outliner"]

        self.activated = True
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def deactivate(self):
        """
        Deactivates the Component.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        self.__engine.parameters.database_read_only and \
        LOGGER.info("{0} | Model edition deactivated by '{1}' command line parameter value!".format(self.__class__.__name__,
                                                                                                    "database_read_only"))
        self.__model = IblSetsModel(self, horizontal_headers=self.__details_headers)

        self.Ibl_Sets_Outliner_stackedWidget = QStackedWidget(self)
        self.Ibl_Sets_Outliner_gridLayout.addWidget(self.Ibl_Sets_Outliner_stackedWidget)

        self.__thumbnails_view = Thumbnails_QListView(self,
                                                    self.__model,
                                                    self.__engine.parameters.database_read_only,
                                                    "No Ibl Set to view!")
        self.__thumbnails_view.setObjectName("Thumbnails_listView")
        self.__thumbnails_view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.Ibl_Sets_Outliner_stackedWidget.addWidget(self.__thumbnails_view)

        self.__details_view = Details_QTreeView(self,
                                            self.__model,
                                            self.__engine.parameters.database_read_only,
                                            "No Ibl Set to view!")
        self.__details_view.setObjectName("Details_treeView")
        self.__details_view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.Ibl_Sets_Outliner_stackedWidget.addWidget(self.__details_view)

        self.__views = (self.__thumbnails_view, self.__details_view)
        self.__views_add_actions()
        self.__views_push_buttons = {0 : (self.Thumbnails_View_pushButton, self.__ui_thumbnails_view_image),
                                    1 : (self.Details_View_pushButton, self.__ui_details_view_image)}

        for index, data in self.__views_push_buttons.iteritems():
            view_push_button, image = data
            view_push_button.setIcon(QIcon(os.path.join(self.__ui_resources_directory, image)))

        self.Switch_Thumbnails_Type_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_switch_thumbnails_type_image)))

        self.Search_Database_lineEdit = Search_QLineEdit(self)
        self.Search_Database_horizontalLayout.addWidget(self.Search_Database_lineEdit)
        self.Search_Database_lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__search_context_menu = QMenu()
        for context in self.__search_contexts.iterkeys():
            self.__search_context_menu.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|Search|Set '{0}' Context ...".format(context),
            text="{0} ...".format(context),
            checkable=True,
            slot=functools.partial(self.set_active_search_context, context)))
        self.Search_Database_lineEdit.search_active_label.set_menu(self.__search_context_menu)
        self.set_active_search_context(self.__active_search_context)

        self.Largest_Size_label.setPixmap(QPixmap(os.path.join(self.__ui_resources_directory, self.__ui_largest_size_image)))
        self.Smallest_Size_label.setPixmap(QPixmap(os.path.join(self.__ui_resources_directory, self.__ui_smallest_size_image)))

        if self.__settings.key_exists(self.__settings_section, "panoramic_thumbnails"):
            self.__panoramic_thumbnails = self.__settings.get_key(self.__settings_section, "panoramic_thumbnails").toBool()

        self.__views_set_ui(
        foundations.common.get_first_item(self.__settings.get_key(self.__settings_section, "list_view_icon_size").toInt()))

        # Signals / Slots.
        for view in self.__views:
            self.__engine.images_caches.QIcon.content_added.connect(view.viewport().update)
            view.doubleClicked.connect(self.__views__doubleClicked)
        self.active_view_changed.connect(self.__views__active_view_changed)
        for index, data in self.__views_push_buttons.iteritems():
            view_push_button, image = data
            view_push_button.clicked.connect(functools.partial(self.__views_pushButtons__clicked, index))

        self.Switch_Thumbnails_Type_pushButton.clicked.connect(self.__Switch_Thumbnails_Type_pushButton__clicked)
        self.Search_Database_lineEdit.textChanged.connect(self.__Search_Database_lineEdit__textChanged)

        self.Thumbnails_Size_horizontalSlider.valueChanged.connect(self.__Thumbnails_Size_horizontalSlider__changed)

        self.refresh_nodes.connect(self.__model__refresh_nodes)
        self.__model.modelReset.connect(self.__collections_outliner._CollectionsOutliner__model__refresh_attributes)

        if not self.__engine.parameters.database_read_only:
            self.__engine.file_system_events_manager.file_changed.connect(self.__engine_file_system_events_manager__file_changed)
            self.__engine.content_dropped.connect(self.__engine__content_dropped)
        else:
            LOGGER.info("{0} | Ibl Sets file system events ignored by '{1}' command line parameter value!".format(
            self.__class__.__name__, "database_read_only"))

        self.initialized_ui = True
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def uninitialize_ui(self):
        """
        Uninitializes the Component ui.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

    def add_widget(self):
        """
        Adds the Component Widget to the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

        self.__engine.setCentralWidget(self)

        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def remove_widget(self):
        """
        Removes the Component Widget from the engine.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def on_startup(self):
        """
        Defines the slot triggered on Framework startup.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Calling '{0}' Component Framework 'on_startup' method.".format(self.__class__.__name__))

        if not self.__engine.parameters.database_read_only:
            # Wizard if Ibl Sets table is empty.
            if not self.get_ibl_sets():
                if message_box.message_box("Question", "Question",
                "The Database has no Ibl Sets, would you like to add some?",
                buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    directory = umbra.ui.common.store_last_browsed_path((QFileDialog.getExistingDirectory(self,
                                                                                         "Add Content:",
                                                                                        RuntimeGlobals.last_browsed_path)))
                    if directory:
                        if not self.add_directory(directory):
                            raise Exception(
                            "{0} | Exception raised while adding '{1}' directory content to the Database!".format(
                            self.__class__.__name__, directory))

            # Ibl Sets table integrity checking.
            erroneous_ibl_sets = sibl_gui.components.core.database.operations.check_ibl_sets_table_integrity()
            for ibl_set, exceptions in erroneous_ibl_sets.iteritems():
                if sibl_gui.components.core.database.exceptions.MissingIblSetFileError in exceptions:
                    choice = message_box.message_box("Question", "Error",
                    "{0} | '{1}' Ibl Set file is missing, would you like to update it's location?".format(
                    self.__class__.__name__, ibl_set.name),
                    QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No,
                    custom_buttons=((QString("No To All"), QMessageBox.RejectRole),))

                    if choice == 0:
                        break

                    if choice == QMessageBox.Yes:
                        if self.update_ibl_set_location_ui(ibl_set):
                            # TODO: Check updated Ibl Set file integrity.
                            continue

                for exception in exceptions:
                    self.__engine.notifications_manager.warnify(
                    "{0} | '{1}' {2}".format(self.__class__.__name__,
                                    ibl_set.name,
                                    sibl_gui.components.core.database.operations.DATABASE_EXCEPTIONS[exception]))
        else:
            LOGGER.info("{0} | Database Ibl Sets wizard and Ibl Sets integrity checking method deactivated\
by '{1}' command line parameter value!".format(self.__class__.__name__, "database_read_only"))

        activeView, state = self.__settings.get_key(self.__settings_section, "activeView").toInt()
        state and self.set_active_viewIndex(activeView)

        for view in self.__views:
            viewName = view.objectName()
            viewSelectedIblSetsIdentities = foundations.strings.to_string(self.__settings.get_key(self.__settings_section,
                                                                    "{0}_viewSelecteIblSets".format(viewName)).toString())
            LOGGER.debug("> '{0}' View stored selected Ibl Sets identities: '{1}'.".format(viewName,
                                                                                            viewSelectedIblSetsIdentities))
            view.model_selection["Default"] = viewSelectedIblSetsIdentities and \
            [int(identity) for identity in viewSelectedIblSetsIdentities.split(self.__settings_separator)] or []
            view.restore_model_selection()
        return True

    def on_close(self):
        """
        Defines the slot triggered on Framework close.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Calling '{0}' Component Framework 'on_close' method.".format(self.__class__.__name__))

        for view in self.__views:
            view.store_model_selection()
            self.__settings.set_key(self.__settings_section,
                                "{0}_viewSelecteIblSets".format(view.objectName()),
                                self.__settings_separator.join(foundations.strings.to_string(identity) \
                                for identity in view.model_selection["Default"]))

        self.__settings.set_key(self.__settings_section, "activeView", self.get_active_viewIndex())

        return True

    def __views_set_ui(self, thumbnails_size=None):
        """
        Sets the Views ui.

        :param thumbnails_size: Thumbnails size.
        :type thumbnails_size: int
        """

        if not thumbnails_size:
            thumbnails_size = UiConstants.thumbnails_sizes.get(self.__panoramic_thumbnails_size \
                                                        if self.__panoramic_thumbnails else self.__square_thumbnails_size)
        self.__icon_place_holder = \
        sibl_gui.ui.common.get_icon(os.path.join(self.__ui_resources_directory,
                                            self.__ui_panoramic_loading_image if self.__panoramic_thumbnails else \
                                            self.__ui_square_loading_image),
                                    asynchronous_loading=False)

        self.__thumbnails_view._Thumbnails_QListView__set_default_ui_state(thumbnails_size,
                                                                        2 if self.__panoramic_thumbnails else 1)

        self.Thumbnails_Size_horizontalSlider.setMinimum(UiConstants.thumbnails_sizes.get(self.__thumbnails_minimum_size))
        self.Thumbnails_Size_horizontalSlider.setMaximum(UiConstants.thumbnails_sizes.get(self.__panoramic_thumbnails_size \
                                                        if self.__panoramic_thumbnails else self.__square_thumbnails_size))
        self.Thumbnails_Size_horizontalSlider.setValue(thumbnails_size)

    def __views_refresh_ui(self, thumbnails_size=None):
        """
        Refreshes the Views ui.

        :param thumbnails_size: Thumbnails size.
        :type thumbnails_size: int
        """

        self.__views_set_ui(thumbnails_size)

    def __model__refresh_nodes(self):
        """
        Defines the slot triggered by the Model when Nodes need refresh.
        """

        self.set_ibl_sets()

    def __views_add_actions(self):
        """
        Sets the Views actions.
        """

        if not self.__engine.parameters.database_read_only:
            add_content_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|Add Content ...",
            slot=self.__views_add_content_action__triggered)
            add_ibl_set_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|Add Ibl Set ...",
            slot=self.__views_add_ibl_set_action__triggered)
            remove_ibl_sets_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|Remove Ibl Set(s) ...",
            slot=self.__views_remove_ibl_sets_action__triggered)
            update_ibl_sets_locations_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|Update Ibl Set(s) Location(s) ...",
            slot=self.__views_update_ibl_sets_locations_action__triggered)

            for view in self.__views:
                separator_action = QAction(view)
                separator_action.setSeparator(True)
                for action in (add_content_action,
                                add_ibl_set_action,
                                remove_ibl_sets_action,
                                update_ibl_sets_locations_action,
                                separator_action):
                    view.addAction(action)
        else:
            LOGGER.info(
            "{0} | Ibl Sets Database alteration capabilities deactivated by '{1}' command line parameter value!".format(
            self.__class__.__name__, "database_read_only"))

    def __views_add_content_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.ibl_sets_outliner|Add Content ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.add_content_ui()

    def __views_add_ibl_set_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.ibl_sets_outliner|Add Ibl Set ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.add_ibl_setUi()

    def __views_remove_ibl_sets_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.ibl_sets_outliner|Remove Ibl Set(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.remove_ibl_setsUi()

    def __views_update_ibl_sets_locations_action__triggered(self, checked):
        """
        Defines the slot triggered by
        **'Actions|Umbra|Components|core.ibl_sets_outliner|Update Ibl Set(s) Location(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.update_selected_ibl_sets_location_ui()

    def __views_pushButtons__clicked(self, index, checked):
        """
        Defines the slot triggered by **\*_View_pushButton** Widget when clicked.

        :param index: Button index.
        :type index: int
        :param checked: Checked state.
        :type checked: bool
        """

        self.set_active_viewIndex(index)

    def __views__doubleClicked(self, index):
        """
        Defines the slot triggered by a **\*_View** Widget when double clicked.

        :param index: Clicked item index.
        :type index: QModelIndex
        """

        self.__engine.layouts_manager.restore_layout(self.__inspect_layout)

    def __views__active_view_changed(self, index):
        """
        Defines the slot triggered by the active View changed.

        :param index: Current active View.
        :type index: int
        """

        self.Ibl_Sets_Outliner_Thumbnails_Slider_frame.setVisible(not index)
        for view_index, data in self.__views_push_buttons.iteritems():
            view_push_button, image = data
            view_push_button.setChecked(True if view_index == index else False)

    def __Switch_Thumbnails_Type_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Switch_Thumbnails_Type_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.set_panoramic_thumbnails(not self.__panoramic_thumbnails)

    def __Search_Database_lineEdit__textChanged(self, text):
        """
        Defines the slot triggered by **Search_Database_lineEdit** Widget when text changed.

        :param text: Current text value.
        :type text: QString
        """

        self.set_ibl_sets(self.__search_ibl_sets(foundations.strings.to_string(self.Search_Database_lineEdit.text()),
                                            self.__search_contexts[self.__active_search_context],
                                            re.IGNORECASE if self.Case_Sensitive_Matching_pushButton.isChecked() else 0))

    def __Thumbnails_Size_horizontalSlider__changed(self, value):
        """
        Scales the View icons.

        :param value: Thumbnails size.
        :type value: int
        """

        self.__thumbnails_view._Thumbnails_QListView__set_default_ui_state(value, 2 if self.__panoramic_thumbnails else 1)

        # Storing settings key.
        LOGGER.debug("> Setting '{0}' with value '{1}'.".format("list_view_icon_size", value))
        self.__settings.set_key(self.__settings_section, "list_view_icon_size", value)

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                            foundations.exceptions.UserError)
    @umbra.engine.show_processing("Retrieving Ibl Sets ...")
    def __engine__content_dropped(self, event):
        """
        Defines the slot triggered by content when dropped into the engine.

        :param event: Event.
        :type event: QEvent
        """

        if not event.mimeData().hasUrls():
            return

        LOGGER.debug("> Drag event urls list: '{0}'!".format(event.mimeData().urls()))

        if not self.__engine.parameters.database_read_only:
            for url in event.mimeData().urls():
                path = foundations.strings.to_string(url.path())
                LOGGER.debug("> Handling dropped '{0}' file.".format(path))
                path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
                re.search(r"^\/[A-Z]:", path) and path[1:] or path
                if re.search(r"\.{0}$".format(self.__extension), path):
                    name = foundations.strings.get_splitext_basename(path)
                    choice = message_box.message_box("Question", "Question",
                    "'{0}' Ibl Set file has been dropped, would you like to 'Add' it to the Database or \
'Edit' it in the Script Editor?".format(name),
                    buttons=QMessageBox.Cancel,
                    custom_buttons=((QString("Add"), QMessageBox.AcceptRole), (QString("Edit"), QMessageBox.AcceptRole)))
                    if choice == 0:
                        self.add_ibl_set(name, path)
                    elif choice == 1:
                        self.__script_editor.load_file(path) and self.__script_editor.restore_development_layout()
                else:
                    if not os.path.isdir(path):
                        return

                    if not list(foundations.walkers.files_walker(path, ("\.{0}$".format(self.__extension),), ("\._",))):
                        return

                    if message_box.message_box("Question", "Question",
                    "Would you like to add '{0}' directory Ibl Set(s) file(s) to the Database?".format(path),
                    buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                        self.add_directory(path)
                self.__engine.process_events()
        else:
            raise foundations.exceptions.UserError("{0} | Cannot perform action, Database has been set read only!".format(
            self.__class__.__name__))

    def __engine_file_system_events_manager__file_changed(self, file):
        """
        Defines the slot triggered by the **file_system_events_manager** when a file is changed.

        :param file: File changed.
        :type file: unicode
        """

        ibl_set = foundations.common.get_first_item(filter(lambda x: x.path == file, self.get_ibl_sets()))
        if not ibl_set:
            return

        if sibl_gui.components.core.database.operations.update_ibl_set_content(ibl_set):
            self.__engine.notifications_manager.notify(
            "{0} | '{1}' Ibl Set file has been reparsed and associated database object updated!".format(
            self.__class__.__name__, ibl_set.title))
            self.refresh_nodes.emit()

    def __get_candidate_collection_id(self):
        """
        Returns a Collection id.

        :return: Collection id.
        :rtype: int
        """

        collections = self.__collections_outliner.get_selected_collections()
        collection = foundations.common.get_first_item(collections)
        identity = collection and collection.id or None
        return identity and identity or self.__collections_outliner.get_collection_id(
        self.__collections_outliner.default_collection)

    def __search_ibl_sets(self, pattern, attribute, flags=re.IGNORECASE):
        """
        Filters the current Collection Ibl Sets.

        :param pattern: Ibl Sets filter pattern.
        :type pattern: unicode
        :param attribute: Attribute to filter Ibl Sets on.
        :type attribute: unicode
        :param flags: Regex filtering flags.
        :type flags: int

        :return: Filtered Ibl Sets.
        :rtype: list
        """

        try:
            pattern = re.compile(pattern, flags)
        except Exception:
            return list()

        ibl_sets = [ibl_set for ibl_set in set(self.__collections_outliner.get_collections_ibl_sets(
        self.__collections_outliner.get_selected_collections() or \
        self.__collections_outliner.get_collections())).intersection(
        sibl_gui.components.core.database.operations.filter_ibl_sets(
        "{0}".format(foundations.strings.to_string(pattern.pattern)), attribute, flags))]
        self.Search_Database_lineEdit.completer.setModel(QStringListModel(sorted((value
                                                        for value in set((getattr(ibl_set_node, attribute)
                                                        for ibl_set_node in ibl_sets if getattr(ibl_set_node, attribute)))))))

        return ibl_sets

    def get_active_view(self):
        """
        Returns the current active View.

        :return: Current active View.
        :rtype: QWidget
        """

        return self.Ibl_Sets_Outliner_stackedWidget.currentWidget()

    def get_active_viewIndex(self):
        """
        Returns the current active View index.

        :return: Current active View index.
        :rtype: int
        """

        return self.Ibl_Sets_Outliner_stackedWidget.currentIndex()

    def set_active_view(self, view):
        """
        Sets the active View to given View.

        :param view: View.
        :type view: QWidget
        :return: Method success.
        :rtype: bool
        """

        index = self.Ibl_Sets_Outliner_stackedWidget.index_of(view)
        self.Ibl_Sets_Outliner_stackedWidget.setCurrentIndex()
        self.active_view_changed.emit(index)
        return True

    def set_active_viewIndex(self, index):
        """
        Sets the active View to given index.

        :param index: Index.
        :type index: int
        :return: Method success.
        :rtype: bool
        """

        self.Ibl_Sets_Outliner_stackedWidget.setCurrentIndex(index)
        self.active_view_changed.emit(index)
        return True

    def set_active_search_context(self, context, *args):
        """
        Sets the active search context.

        :param context: Search context.
        :type context: unicode
        :param \*args: Arguments.
        :type \*args: \*
        :return: Method succes.
        :rtype: bool
        """

        text = "{0} ...".format(context)
        for action in  self.__engine.actions_manager.get_category(
        "Actions|Umbra|Components|core.ibl_sets_outliner|Search").itervalues():
            action.setChecked(action.text() == text and True or False)

        self.__active_search_context = context
        self.Search_Database_lineEdit.setPlaceholderText(text)
        return True

    def set_panoramic_thumbnails(self, state):
        """
        Sets the panoramic thumbnails.

        :param state: Panoramic thumbnails.
        :type state: bool
        :return: Method succes.
        :rtype: bool
        """

        old_in, old_out = UiConstants.thumbnails_sizes.get(self.__thumbnails_minimum_size), UiConstants.thumbnails_sizes.get(
                    self.__panoramic_thumbnails_size if self.__panoramic_thumbnails else self.__square_thumbnails_size)

        new_in, new_out = UiConstants.thumbnails_sizes.get(self.__thumbnails_minimum_size), UiConstants.thumbnails_sizes.get(
                    self.__panoramic_thumbnails_size if state else self.__square_thumbnails_size)

        thumbnails_size = (((self.Thumbnails_Size_horizontalSlider.value() - old_in) * (new_out - new_in)) \
                        / (old_out - old_in)) + new_in

        self.__panoramic_thumbnails = state
        self.__settings.set_key(self.__settings_section, "panoramic_thumbnails", self.__panoramic_thumbnails)
        self.__views_refresh_ui(thumbnails_size)
        self.set_ibl_sets()
        return True

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.show_processing("Adding Content ...")
    def add_content_ui(self):
        """
        Adds user defined content to the Database.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        directory = umbra.ui.common.store_last_browsed_path((QFileDialog.getExistingDirectory(self,
                                                                                        "Add Content:",
                                                                                        RuntimeGlobals.last_browsed_path)))
        if not directory:
            return False

        LOGGER.debug("> Chosen directory path: '{0}'.".format(directory))
        if self.add_directory(directory):
            return True
        else:
            raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
            self.__class__.__name__, directory))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.show_processing("Adding Ibl Set ...")
    def add_ibl_setUi(self):
        """
        Adds an user defined Ibl Set to the Database.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        path = umbra.ui.common.store_last_browsed_path((QFileDialog.getOpenFileName(self,
                                                                        "Add Ibl Set:",
                                                                        RuntimeGlobals.last_browsed_path,
                                                                        "Ibls files (*{0})".format(self.__extension))))
        if not path:
            return False

        if not self.ibl_set_exists(path):
            LOGGER.debug("> Chosen Ibl Set path: '{0}'.".format(path))
            if self.add_ibl_set(foundations.strings.get_splitext_basename(path), path):
                return True
            else:
                raise Exception("{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(
                self.__class__.__name__, path))
        else:
            self.__engine.notifications_manager.warnify(
            "{0} | '{1}' Ibl Set already exists in Database!".format(self.__class__.__name__, path))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.encapsulate_processing
    def remove_ibl_setsUi(self):
        """
        Removes user selected Ibl Sets from the Database.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_ibl_sets = self.get_selected_ibl_sets()
        if not selected_ibl_sets:
            return False

        if message_box.message_box("Question", "Question", "Are you sure you want to remove '{0}' sets(s)?".format(
        ", ".join((ibl_set.title for ibl_set in selected_ibl_sets))),
         buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.__engine.start_processing("Removing Ibl Sets ...", len(selected_ibl_sets))
            success = True
            for ibl_set in selected_ibl_sets:
                success *= umbra.ui.common.signals_blocker(self, self.remove_ibl_set, ibl_set) or False
                self.__engine.step_processing()
            self.__engine.stop_processing()

            self.refresh_nodes.emit()

            if success:
                return True
            else:
                raise Exception("{0} | Exception raised while removing '{1}' Ibls sets from the Database!".format(
                self.__class__.__name__, ", ". join((ibl_set.title for ibl_set in selected_ibl_sets))))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                            sibl_gui.components.core.database.exceptions.DatabaseOperationError)
    def update_ibl_set_location_ui(self, ibl_set):
        """
        Updates given Ibl Set location.

        :param ibl_set: Ibl Set to update.
        :type ibl_set: IblSet
        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        file = umbra.ui.common.store_last_browsed_path((QFileDialog.getOpenFileName(self,
                                                                "Updating '{0}' Template Location:".format(ibl_set.name),
                                                                RuntimeGlobals.last_browsed_path,
                                                                "Ibl Set files (*{0})".format(self.__extension))))
        if not file:
            return False

        LOGGER.info("{0} | Updating '{1}' Ibl Set with new location '{2}'!".format(self.__class__.__name__,
                                                                                    ibl_set.name, file))
        if sibl_gui.components.core.database.operations.update_ibl_set_location(ibl_set, file):
            self.refresh_nodes.emit()
            return True
        else:
            raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
            "{0} | Exception raised while updating '{1}' Ibl Set location!".format(self.__class__.__name__, ibl_set.name))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.encapsulate_processing
    def update_selected_ibl_sets_location_ui(self):
        """
        Updates user selected Ibl Sets locations.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_ibl_sets = self.get_selected_ibl_sets()
        if not selected_ibl_sets:
            return False

        self.__engine.start_processing("Update Ibl Sets Locations ...", len(selected_ibl_sets))
        success = True
        for ibl_set in selected_ibl_sets:
            success *= self.update_ibl_set_location_ui(ibl_set)
            self.__engine.step_processing()
        self.__engine.stop_processing()

        self.refresh_nodes.emit()

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while updating '{1}' Ibls sets locations!".format(
            self.__class__.__name__, ", ". join((ibl_set.title for ibl_set in selected_ibl_sets))))

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError,
                                            sibl_gui.components.core.database.exceptions.DatabaseOperationError)
    def add_ibl_set(self, name, path, collection_id=None):
        """
        Adds an Ibl Set to the Database.

        :param name: Ibl Set name.
        :type name: unicode
        :param path: Ibl Set path.
        :type path: unicode
        :param collection_id: Target Collection id.
        :type collection_id: int
        :return: Method success.
        :rtype: bool
        """

        if not self.ibl_set_exists(path):
            LOGGER.info("{0} | Adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, name))
            if sibl_gui.components.core.database.operations.add_ibl_set(
            name, path, collection_id or self.__get_candidate_collection_id()):
                self.refresh_nodes.emit()
                return True
            else:
                raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
                "{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, name))
        else:
            raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' Ibl Set already exists in Database!".format(self.__class__.__name__, name))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.encapsulate_processing
    def add_directory(self, directory, collection_id=None):
        """
        Adds directory Ibl Sets to the Database.

        :param directory: Directory to add.
        :type directory: unicode
        :param collection_id: Target Collection id.
        :type collection_id: int
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing directory '{0}' files_walker.".format(directory))

        files = list(foundations.walkers.files_walker(directory, ("\.{0}$".format(self.__extension),), ("\._",)))

        self.__engine.start_processing("Adding Directory Ibl Sets ...", len(files))
        success = True
        for path in files:
            if not self.ibl_set_exists(path):
                success *= umbra.ui.common.signals_blocker(self,
                                                        self.add_ibl_set,
                                                        foundations.strings.get_splitext_basename(path),
                                                        path,
                                                        collection_id or self.__get_candidate_collection_id()) or False
            self.__engine.step_processing()
        self.__engine.stop_processing()

        self.refresh_nodes.emit()

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
            self.__class__.__name__, directory))

    @foundations.exceptions.handle_exceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
    def remove_ibl_set(self, ibl_set):
        """
        Removes given Ibl Set from the Database.

        :param ibl_set: Ibl Set to remove.
        :type ibl_set: IblSet
        :return: Method success.
        :rtype: bool
        """

        LOGGER.info("{0} | Removing '{1}' Ibl Set from the Database!".format(self.__class__.__name__, ibl_set.title))
        if sibl_gui.components.core.database.operations.remove_ibl_set(ibl_set.id):
            self.refresh_nodes.emit()
            return True
        else:
            raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
            "{0} | Exception raised while removing '{1}' Ibl Set from the Database!".format(self.__class__.__name__,
                                                                                            ibl_set.title))

    @foundations.exceptions.handle_exceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
    def update_ibl_set_location(self, ibl_set, file):
        """
        Updates given Ibl Set location.

        :param ibl_set: Ibl Set to update.
        :type ibl_set: IblSet
        :param ibl_set: New Ibl Set file.
        :type ibl_set: unicode
        :return: Method success.
        :rtype: bool
        """

        LOGGER.info("{0} | Updating '{1}' Ibl Set with new location: '{2}'!".format(self.__class__.__name__,
                                                                                    ibl_set.title,
                                                                                    file))
        if sibl_gui.components.core.database.operations.update_ibl_set_location(ibl_set, file):
            self.refresh_nodes.emit()
            return True
        else:
            raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
            "{0} | Exception raised while updating '{1}' Ibl Set location!".format(self.__class__.__name__, ibl_set.title))

    def get_ibl_sets(self):
        """
        Returns Database Ibl Sets.

        :return: Database Ibl Sets.
        :rtype: list
        """

        return [ibl_set for ibl_set in sibl_gui.components.core.database.operations.get_ibl_sets()]

    def filter_ibl_sets(self, pattern, attribute, flags=re.IGNORECASE):
        """
        Filters the Database Ibl Sets on given attribute using given pattern.

        :param pattern: Filter pattern.
        :type pattern: unicode
        :param attribute: Attribute to filter on.
        :type attribute: unicode
        :param flags: Regex filtering flags.
        :type flags: int

        :return: Filtered Database Ibl Sets.
        :rtype: list
        """

        try:
            pattern = re.compile(pattern, flags)
        except Exception:
            return list()

        return list(set(self.get_ibl_sets()).intersection(
        sibl_gui.components.core.database.operations.filter_ibl_sets(
        "{0}".format(foundations.strings.to_string(pattern.pattern)), attribute, flags)))

    def ibl_set_exists(self, path):
        """
        Returns if given Ibl Set path exists in the Database.

        :param path: Collection path.
        :type path: unicode
        :return: Collection exists.
        :rtype: bool
        """

        return sibl_gui.components.core.database.operations.ibl_set_exists(path)

    def list_ibl_sets(self):
        """
        Lists Database Ibl Sets names.

        :return: Database Ibl Sets names.
        :rtype: list

        :note: The list is actually returned using 'title' attributes instead of 'name' attributes
        """

        return [ibl_set.title for ibl_set in self.get_ibl_sets()]

    def set_ibl_sets(self, ibl_sets=None):
        """
        Sets the Ibl Sets Model nodes.

        :param ibl_sets: Ibl Sets to set.
        :type ibl_sets: list
        :return: Method success.
        :rtype: bool
        """

        node_flags = self.__engine.parameters.database_read_only and int(Qt.ItemIsSelectable | Qt.ItemIsEnabled) or \
        int(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)
        ibl_sets = ibl_sets or self.__collections_outliner.get_collections_ibl_sets(
        self.__collections_outliner.get_selected_collections() or self.__collections_outliner.get_collections())
        root_node = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")

        for ibl_set in ibl_sets:
            if self.__panoramic_thumbnails:
                icon_path = foundations.common.get_first_item(filter(foundations.common.path_exists, [ibl_set.background_image,
                                                                                            ibl_set.preview_image]))
                icon_size = self.__panoramic_thumbnails_size
            else:
                icon_path = ibl_set.icon
                icon_size = self.__square_thumbnails_size

            ibl_set_node = IblSetNode(ibl_set,
                                    name=ibl_set.title,
                                    parent=root_node,
                                    node_flags=node_flags,
                                    attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                                    icon_path=icon_path,
                                    icon_size=icon_size,
                                    icon_placeholder=self.__icon_place_holder)

            path = foundations.strings.to_string(ibl_set.path)
            if not foundations.common.path_exists(path):
                continue

            not self.__engine.file_system_events_manager.is_path_registered(path) and \
            self.__engine.file_system_events_manager.register_path(path, modified_time=float(ibl_set.os_stats.split(",")[8]))

        root_node.sort_children(attribute="title")

        self.__model.initialize_model(root_node)
        return True

    def get_ibl_set_by_name(self, name):
        """
        Returns Database Ibl Set with given name.

        :param name: Ibl Set name.
        :type name: unicode
        :return: Database Ibl Set.
        :rtype: IblSet

        :note: The filtering is actually performed on 'title' attributes instead of 'name' attributes.
        """

        ibl_sets = self.filter_ibl_sets(r"^{0}$".format(name), "title")
        return foundations.common.get_first_item(ibl_sets)

    def get_selected_nodes(self):
        """
        Returns the current active View selected nodes.

        :return: View selected nodes.
        :rtype: dict
        """

        return self.get_active_view().get_selected_nodes()

    def get_selected_ibl_sets_nodes(self):
        """
        Returns the current active View selected Ibl Sets nodes.

        :return: View selected Ibl Sets nodes.
        :rtype: list
        """

        return [node for node in self.get_selected_nodes() if node.family == "IblSet"]

    def get_selected_ibl_sets(self):
        """
        Returns the current active View selected Ibl Sets.

        :return: View selected Ibl Sets.
        :rtype: list
        """

        return [node.database_item for node in self.get_selected_ibl_sets_nodes()]
