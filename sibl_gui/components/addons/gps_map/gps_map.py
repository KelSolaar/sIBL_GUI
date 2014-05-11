#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**gps_map.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`GpsMap` Component Interface class and the :class:`Map` class.

**Others:**

"""

from __future__ import unicode_literals

import os
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import sibl_gui.ui.common
import umbra.exceptions
from manager.QWidget_component import QWidgetComponentFactory
from sibl_gui.components.addons.gps_map.views import Map_QWebView
from umbra.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_FILE", "GpsMap"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_FILE = os.path.join(os.path.dirname(__file__), "ui", "Gps_Map.ui")

class GpsMap(QWidgetComponentFactory(ui_file=COMPONENT_FILE)):
    """
    | Defines the :mod:`sibl_gui.components.addons.gps_map.gps_map` Component Interface class.
    | It displays the GPS map inside a `QDockWidget <http://doc.qt.nokia.com/qdockwidget.html>`_ window.
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

        super(GpsMap, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = True

        self.__ui_resources_directory = "resources"
        self.__ui_zoom_in_image = "Zoom_In.png"
        self.__ui_zoom_out_image = "Zoom_Out.png"
        self.__gps_map_html_file = "Bing_Maps.html"
        self.__gps_map_base_size = QSize(160, 100)
        self.__dock_area = 2

        self.__engine = None

        self.__ibl_sets_outliner = None

        self.__map = None
        self.__map_type_ids = (("Auto", "MapTypeId.auto"), ("Aerial", "MapTypeId.aerial"), ("Road", "MapTypeId.road"))

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
    def ui_zoom_in_image(self):
        """
        Property for **self.__ui_zoom_in_image** attribute.

        :return: self.__ui_zoom_in_image.
        :rtype: unicode
        """

        return self.__ui_zoom_in_image

    @ui_zoom_in_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_zoom_in_image(self, value):
        """
        Setter for **self.__ui_zoom_in_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_zoom_in_image"))

    @ui_zoom_in_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_zoom_in_image(self):
        """
        Deleter for **self.__ui_zoom_in_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_zoom_in_image"))

    @property
    def ui_zoom_out_image(self):
        """
        Property for **self.__ui_zoom_out_image** attribute.

        :return: self.__ui_zoom_out_image.
        :rtype: unicode
        """

        return self.__ui_zoom_out_image

    @ui_zoom_out_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_zoom_out_image(self, value):
        """
        Setter for **self.__ui_zoom_out_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_zoom_out_image"))

    @ui_zoom_out_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_zoom_out_image(self):
        """
        Deleter for **self.__ui_zoom_out_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_zoom_out_image"))

    @property
    def gps_map_html_file(self):
        """
        Property for **self.__gps_map_html_file** attribute.

        :return: self.__gps_map_html_file.
        :rtype: unicode
        """

        return self.__gps_map_html_file

    @gps_map_html_file.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def gps_map_html_file(self, value):
        """
        Setter for **self.__gps_map_html_file** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "gps_map_html_file"))

    @gps_map_html_file.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def gps_map_html_file(self):
        """
        Deleter for **self.__gps_map_html_file** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "gps_map_html_file"))

    @property
    def gps_map_base_size(self):
        """
        Property for **self.__gps_map_base_size** attribute.

        :return: self.__gps_map_base_size. ( QSize() )
        """

        return self.__gps_map_base_size

    @gps_map_base_size.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def gps_map_base_size(self, value):
        """
        Setter for **self.__gps_map_base_size** attribute.

        :param value: Attribute value. ( QSize() )
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "gps_map_base_size"))

    @gps_map_base_size.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def gps_map_base_size(self):
        """
        Deleter for **self.__gps_map_base_size** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "gps_map_base_size"))

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
    def map(self):
        """
        Property for **self.__map** attribute.

        :return: self.__map.
        :rtype: QObject
        """

        return self.__map

    @map.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def map(self, value):
        """
        Setter for **self.__map** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "map"))

    @map.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def map(self):
        """
        Deleter for **self.__map** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "map"))

    @property
    def map_type_ids(self):
        """
        Property for **self.__map_type_ids** attribute.

        :return: self.__map_type_ids.
        :rtype: tuple
        """

        return self.__map_type_ids

    @map_type_ids.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def map_type_ids(self, value):
        """
        Setter for **self.__map_type_ids** attribute.

        :param value: Attribute value.
        :type value: tuple
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "map_type_ids"))

    @map_type_ids.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def map_type_ids(self):
        """
        Deleter for **self.__map_type_ids** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "map_type_ids"))

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

        self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]

        self.activated = True
        return True

    def deactivate(self):
        """
        Deactivates the Component.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

        self.__ui_resources_directory = os.path.basename(self.__ui_resources_directory)

        self.__engine = None

        self.__ibl_sets_outliner = None

        self.activated = False
        return True

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        self.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_zoom_in_image)))
        self.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_zoom_out_image)))

        self.Map_Type_comboBox.addItems([foundations.common.get_first_item(mapType) for mapType in self.__map_type_ids])

        self.__map = Map_QWebView()
        self.__map.setMinimumSize(self.__gps_map_base_size)
        self.__map.load(QUrl.fromLocalFile(os.path.normpath(os.path.join(self.__ui_resources_directory,
                                                                        self.__gps_map_html_file))))
        self.__map.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        self.__map.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        self.Map_scrollAreaWidgetContents_gridLayout.addWidget(self.__map)

        # Signals / Slots.
        for view in self.__ibl_sets_outliner.views:
            view.selectionModel().selectionChanged.connect(
            self.__ibl_sets_outliner_view_selectionModel__selectionChanged)
        self.__map.loadFinished.connect(self.__map__loadFinished)
        self.Map_Type_comboBox.activated.connect(self.__Map_Type_comboBox__activated)
        self.Zoom_In_pushButton.clicked.connect(self.__Zoom_In_pushButton__clicked)
        self.Zoom_Out_pushButton.clicked.connect(self.__Zoom_Out_pushButton__clicked)

        self.initialized_ui = True
        return True

    def uninitialize_ui(self):
        """
        Uninitializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        # Signals / Slots.
        for view in self.__ibl_sets_outliner.views:
            view.selectionModel().selectionChanged.disconnect(
            self.__ibl_sets_outliner_view_selectionModel__selectionChanged)
        self.__map.loadFinished.disconnect(self.__map__loadFinished)
        self.Map_Type_comboBox.activated.disconnect(self.__Map_Type_comboBox__activated)
        self.Zoom_In_pushButton.clicked.disconnect(self.__Zoom_In_pushButton__clicked)
        self.Zoom_Out_pushButton.clicked.disconnect(self.__Zoom_Out_pushButton__clicked)

        self.__map.setParent(None)
        self.__map = None

        self.initialized_ui = True
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

    def on_close(self):
        """
        Defines the slot triggered on Framework close.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Calling '{0}' Component Framework 'on_close' method.".format(self.__class__.__name__))

        self.__map.stop()
        return True

    def __ibl_sets_outliner_view_selectionModel__selectionChanged(self, selected_items, deselected_items):
        """
        Defines the slot triggered by **Data** Model when selection changed

        :param selected_items: Selected items.
        :type selected_items: QItemSelection
        :param deselected_items: Deselected items.
        :type deselected_items: QItemSelection
        """

        self.set_markers_ui()

    def __Map_Type_comboBox__activated(self, index):
        """
        Defines the slot triggered by **Map_Type_comboBox** when activated.

        :param index: ComboBox activated item index.
        :type index: int
        """

        self.__map.set_map_type(self.__map_type_ids[index][1])

    def __Zoom_In_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Zoom_In_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.__map.set_zoom("In")

    def __Zoom_Out_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Zoom_Out_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.__map.set_zoom("Out")

    def __map__loadFinished(self, state):
        """
        Defines the slot triggered by the GPS map when load finished.

        :param state: Loading state.
        :type state: bool
        """

        self.set_markers_ui()

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def set_markers_ui(self):
        """
        Sets selected Ibl Sets markers.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_ibl_sets = self.__ibl_sets_outliner.get_selected_ibl_sets()
        self.__map.remove_markers()
        success = True
        for ibl_set in selected_ibl_sets:
            success *= self.set_marker(ibl_set) or False
        self.__map.set_center()

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while setting '{1}' GPS markers!".format(
            self.__class__.__name__, ", ". join((ibl_set.title for ibl_set in selected_ibl_sets))))

    def set_marker(self, ibl_set):
        """
        Sets given Ibl Set marker.

        :param ibl_set: Ibl Set to display marker.
        :type ibl_set: IblSet
        :return: Method success.
        :rtype: bool
        """

        if not ibl_set.latitude and not ibl_set.longitude:
            return True

        LOGGER.debug("> Ibl Set '{0}' provides GEO coordinates.".format(ibl_set.name))
        shot_date_string = "<b>Shot Date: </b>{0}".format(
        sibl_gui.ui.common.get_formatted_shot_date(ibl_set.date, ibl_set.time) or Constants.null_object)
        content = "<p><h3><b>{0}</b></h3></p><p><b>\
        Author: </b>{1}<br><b>\
        Location: </b>{2}<br>{3}<br><b>\
        Comment: </b>{4}</p>".format(ibl_set.title, ibl_set.author, ibl_set.location, shot_date_string, ibl_set.comment)
        return self.__map.add_marker((ibl_set.latitude, ibl_set.longitude),
                                    ibl_set.title,
                                    foundations.strings.to_forward_slashes(ibl_set.icon), content)

    def remove_markers(self):
        """
        Removes the GPS map markers.

        :return: Method success.
        :rtype: bool
        """

        self.__map.remove_markers()
        return True
