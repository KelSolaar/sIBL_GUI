#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**application_QToolBar.py.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`Application_QToolBar` class.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QPixmap

import foundations.guerilla
import foundations.verbose
import umbra.ui.widgets.application_QToolBar
from umbra.globals.ui_constants import UiConstants
from umbra.ui.widgets.active_QLabel import Active_QLabel
from umbra.ui.widgets.active_QLabelsCollection import Active_QLabelsCollection

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Application_QToolBar"]

LOGGER = foundations.verbose.install_logger()


class Application_QToolBar(umbra.ui.widgets.application_QToolBar.Application_QToolBar):
    """
    Defines defines the Application toolbar.
    """

    __metaclass__ = foundations.guerilla.base_warfare

    def __central_widgetButton__clicked(self):
        """
        Sets the **Central** Widget visibility.
        """

        LOGGER.debug("> Central Widget button clicked!")

        if self.__container.centralWidget().isVisible():
            self.__container.centralWidget().hide()
        else:
            self.__container.centralWidget().show()

    def set_toolbar_children_widgets(self):
        """
        Sets the toolBar children widgets.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding 'Application_Logo_label' widget!")
        self.addWidget(self.get_application_logo_label())

        LOGGER.debug("> Adding 'Spacer_label' widget!")
        self.addWidget(self.get_spacer_label())

        LOGGER.debug("> Adding 'Library_active_label', \
                    'Inspect_active_label', \
                    'Export_active_label', \
                    'Edit_active_label', \
                    'Preferences_active_label' \
                    widgets!")
        for layout_active_label in self.get_layouts_active_labels():
            self.addWidget(layout_active_label)

        LOGGER.debug("> Adding 'Central_Widget_active_label' widget!")
        self.addWidget(self.get_central_widget_active_label())

        LOGGER.debug("> Adding 'Custom_Layouts_active_label' widget!")
        self.addWidget(self.get_custom_layouts_active_label())

        LOGGER.debug("> Adding 'Miscellaneous_active_label' widget!")
        self.addWidget(self.get_miscellaneous_active_label())
        self.extend_miscellaneous_active_label()

        LOGGER.debug("> Adding 'Closure_Spacer_label' widget!")
        self.addWidget(self.get_closure_spacer_label())

        return True

    def get_layouts_active_labels(self):
        """
        Returns the layouts **Active_QLabel** widgets.

        :return: Layouts active labels.
        :rtype: list
        """

        self.__layouts_active_labels_collection = Active_QLabelsCollection(self)

        self.__layouts_active_labels_collection.add_active_label(self.get_layout_active_label((UiConstants.library_icon,
                                                                                               UiConstants.library_hover_icon,
                                                                                               UiConstants.library_active_icon),
                                                                                              "Library_active_label",
                                                                                              "Library",
                                                                                              "sets_centric",
                                                                                              Qt.Key_6))

        self.__layouts_active_labels_collection.add_active_label(self.get_layout_active_label((UiConstants.inspect_icon,
                                                                                               UiConstants.inspect_hover_icon,
                                                                                               UiConstants.inspect_active_icon),
                                                                                              "Inspect_active_label",
                                                                                              "Inspect",
                                                                                              "inspect_centric",
                                                                                              Qt.Key_7))

        self.__layouts_active_labels_collection.add_active_label(self.get_layout_active_label((UiConstants.export_icon,
                                                                                               UiConstants.export_hover_icon,
                                                                                               UiConstants.export_active_icon),
                                                                                              "Export_active_label",
                                                                                              "Export",
                                                                                              "templates_centric",
                                                                                              Qt.Key_8))

        self.__layouts_active_labels_collection.add_active_label(self.get_layout_active_label((UiConstants.edit_icon,
                                                                                               UiConstants.edit_hover_icon,
                                                                                               UiConstants.edit_active_icon),
                                                                                              "Edit_active_label",
                                                                                              "Edit",
                                                                                              "edit_centric",
                                                                                              Qt.Key_9))

        self.__layouts_active_labels_collection.add_active_label(
            self.get_layout_active_label((UiConstants.preferences_icon,
                                          UiConstants.preferences_hover_icon,
                                          UiConstants.preferences_active_icon),
                                         "Preferences_active_label",
                                         "Preferences",
                                         "preferences_centric",
                                         Qt.Key_0))
        return self.__layouts_active_labels_collection.active_labels

    def get_central_widget_active_label(self):
        """
        Provides the default **Central_Widget_active_label** widget.

        :return: Central Widget active label.
        :rtype: Active_QLabel
        """

        central_widget_button = Active_QLabel(self,
                                              QPixmap(
                                                  umbra.ui.common.get_resource_path(UiConstants.central_widget_icon)),
                                              QPixmap(umbra.ui.common.get_resource_path(
                                                  UiConstants.central_widget_hover_icon)),
                                              QPixmap(umbra.ui.common.get_resource_path(
                                                  UiConstants.central_widget_active_icon)))
        central_widget_button.setObjectName("Central_Widget_active_label")

        # Signals / Slots.
        central_widget_button.clicked.connect(self.__central_widgetButton__clicked)
        return central_widget_button

    def extend_miscellaneous_active_label(self):
        """
        Extends the default **Miscellaneous_active_label** widget.

        :return: Method success.
        :rtype: bool
        """

        self.miscellaneous_menu.addAction(self.__container.actions_manager.register_action(
            "Actions|Umbra|ToolBar|Miscellaneous|Make A Donation ...",
            slot=self.__make_donation_display_misc_action__triggered))
        self.miscellaneous_menu.addSeparator()
        return True

    def __make_donation_display_misc_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|ToolBar|Miscellaneous|Make A Donation ...'** action.

        :param checked: Checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.make_donation_file))
        QDesktopServices.openUrl(QUrl(QString(UiConstants.make_donation_file)))
        return True
