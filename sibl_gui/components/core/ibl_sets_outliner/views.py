#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`sibl_gui.components.core.ibl_sets_outliner.ibl_sets_outliner.IblSetsOutliner`
    Component Interface class Views.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QListView

import foundations.exceptions
import foundations.verbose
import sibl_gui.ui.views

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Thumbnails_QListView", "Details_QTreeView"]

LOGGER = foundations.verbose.install_logger()

class Thumbnails_QListView(sibl_gui.ui.views.Abstract_QListView):
    """
    Defines the view for Database Ibl Sets as thumbnails.
    """

    def __init__(self, parent, model=None, read_only=False, message=None):
        """
        Initializes the class.

        :param parent: Object parent.
        :type parent: QObject
        :param model: Model.
        :type model: QObject
        :param read_only: View is read only.
        :type read_only: bool
        :param message: View default message when Model is empty.
        :type message: unicode
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        sibl_gui.ui.views.Abstract_QListView.__init__(self, parent, model, read_only, message)

        # --- Setting class attributes. ---
        self.__list_view_spacing = 24
        self.__list_view_margin = 32

        Thumbnails_QListView.__initialize_ui(self)

    @property
    def list_view_spacing(self):
        """
        Property for **self.__list_view_spacing** attribute.

        :return: self.__list_view_spacing.
        :rtype: int
        """

        return self.__list_view_spacing

    @list_view_spacing.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def list_view_spacing(self, value):
        """
        Setter for **self.__list_view_spacing** attribute.

        :param value: Attribute value.
        :type value: int
        """

        if value is not None:
            assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("list_view_spacing", value)
            assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("list_view_spacing", value)
        self.__list_view_spacing = value

    @list_view_spacing.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def list_view_spacing(self):
        """
        Deleter for **self.__list_view_spacing** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "list_view_spacing"))

    @property
    def list_view_margin(self):
        """
        Property for **self.__list_view_margin** attribute.

        :return: self.__list_view_margin.
        :rtype: int
        """

        return self.__list_view_margin

    @list_view_margin.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def list_view_margin(self, value):
        """
        Setter for **self.__list_view_margin** attribute.

        :param value: Attribute value.
        :type value: int
        """

        if value is not None:
            assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("list_view_margin", value)
            assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("list_view_margin", value)
        self.__list_view_margin = value

    @list_view_margin.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def list_view_margin(self):
        """
        Deleter for **self.__list_view_margin** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "list_view_margin"))

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        self.setAutoScroll(True)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setViewMode(QListView.IconMode)
        # Previous statement sets the dragDropMode to "QAbstractItemView.DragDrop".
        self.setDragDropMode(QAbstractItemView.DragOnly)

        self.__set_default_ui_state()

        # Signals / Slots.
        self.model().modelReset.connect(self.__set_default_ui_state)

    def __set_default_ui_state(self, iconsSize=None, iconsRatio=2):
        """
        Sets the Widget default ui state.

        :param iconsSize: Icons size.
        :type iconsSize: int
        :param iconRatio: Icons ratio.
        :type iconRatio: int
        """

        LOGGER.debug("> Setting default View state!")

        if not iconsSize:
            return

        self.setIconSize(QSize(iconsSize, iconsSize / iconsRatio))
        self.setGridSize(QSize(iconsSize + self.__list_view_spacing, iconsSize / iconsRatio + self.__list_view_margin))
        self.viewport().update()

class Details_QTreeView(sibl_gui.ui.views.Abstract_QTreeView):
    """
    Defines the view for Database Ibl Sets columns.
    """

    def __init__(self, parent, model=None, read_only=False, message=None):
        """
        Initializes the class.

        :param parent: Object parent.
        :type parent: QObject
        :param model: Model.
        :type model: QObject
        :param read_only: View is read only.
        :type read_only: bool
        :param message: View default message when Model is empty.
        :type message: unicode
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        sibl_gui.ui.views.Abstract_QTreeView.__init__(self, parent, model, read_only, message)

        # --- Setting class attributes. ---
        self.__tree_view_indentation = 15

        Details_QTreeView.__initialize_ui(self)

    @property
    def tree_view_indentation(self):
        """
        Property for **self.__tree_view_indentation** attribute.

        :return: self.__tree_view_indentation.
        :rtype: int
        """

        return self.__tree_view_indentation

    @tree_view_indentation.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tree_view_indentation(self, value):
        """
        Setter for **self.__tree_view_indentation** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tree_view_indentation"))

    @tree_view_indentation.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tree_view_indentation(self):
        """
        Deleter for **self.__tree_view_indentation** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tree_view_indentation"))

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        self.setAutoScroll(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setIndentation(self.__tree_view_indentation)
        self.setRootIsDecorated(False)
        self.setDragDropMode(QAbstractItemView.DragOnly)

        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)

        self.__set_default_ui_state()

        # Signals / Slots.
        self.model().modelReset.connect(self.__set_default_ui_state)

    def __set_default_ui_state(self):
        """
        Sets the Widget default ui state.
        """

        LOGGER.debug("> Setting default View state!")

        if not self.model():
            return

        self.expandAll()

        for column in range(len(self.model().horizontal_headers)):
            self.resizeColumnToContents(column)
