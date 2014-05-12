#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**templates_outliner.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`TemplatesOutliner` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform
import re
import sys

if sys.version_info[:2] <= (2, 6):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
from PyQt4.QtCore import QMargins
from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QMessageBox

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import foundations.walkers
import sibl_gui.components.core.database.exceptions
import sibl_gui.components.core.database.operations
import umbra.engine
import umbra.exceptions
import umbra.ui.common
import umbra.ui.nodes
import umbra.ui.widgets.message_box as message_box
from manager.QWidget_component import QWidgetComponentFactory
from sibl_gui.components.core.database.nodes import CollectionNode
from sibl_gui.components.core.database.nodes import TemplateNode
from sibl_gui.components.core.templates_outliner.models import TemplatesModel
from sibl_gui.components.core.templates_outliner.nodes import SoftwareNode
from sibl_gui.components.core.templates_outliner.views import Templates_QTreeView
from sibl_gui.components.core.database.types import Template
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.globals.ui_constants import UiConstants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "TemplatesOutliner"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Templates_Outliner.ui")


class TemplatesOutliner(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`sibl_gui.components.core.templates_outliner.templates_outliner` Component Interface class.
    | It defines methods for Database Templates management.
    """

    # Custom signals definitions.
    refresh_nodes = pyqtSignal()
    """
    This signal is emited by the :class:`TemplatesOutliner` class when :obj:`TemplatesOutliner.model` class property
    model Nodes needs to be refreshed.
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

        super(TemplatesOutliner, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = False

        self.__ui_resources_directory = "resources"
        self.__ui_software_affixe = "_Software.png"
        self.__ui_unknown_software_image = "Unknown_Software.png"
        self.__dock_area = 1

        self.__engine = None
        self.__settings = None
        self.__settings_section = None
        self.__settings_separator = ","

        self.__script_editor = None
        self.__database = None

        self.__model = None
        self.__view = None
        self.__headers = OrderedDict([("templates", "name"),
                                      ("Release", "release"),
                                      ("Software Version", "version")])

        self.__extension = "sIBLT"

        self.__default_collections = None
        self.__factory_collection = "Factory"
        self.__user_collection = "User"

        self.__tree_view_inner_margins = QMargins(0, 0, 0, 12)

        self.__templates_informations_default_text = \
            "<center><h4>* * *</h4>Select a Template to display related informations!<h4>* * *</h4></center>"
        self.__templates_informations_text = """
                                            <h4><center>{0}</center></h4>
                                            <p>
                                            <b>Date:</b> {1}
                                            <br/>
                                            <b>Author:</b> {2}
                                            <br/>
                                            <b>Email:</b> <a href="mailto:{3}">
                                            <span style=" text-decoration: underline; color:#e0e0e0;">{3}</span></a>
                                            <br/>
                                            <b>Url:</b> <a href="{4}">
                                            <span style=" text-decoration: underline; color:#e0e0e0;">{4}</span></a>
                                            <br/>
                                            <b>Output script:</b> {5}
                                            <p>
                                            <b>Comment:</b> {6}
                                            </p>
                                            <p>
                                            <b>Help file:</b> <a href="{7}">
                                            <span style=" text-decoration: underline; color:#e0e0e0;">
                                            Template Manual</span></a>
                                            </p>
                                            </p>
                                            """

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
    def ui_software_affixe(self):
        """
        Property for **self.__ui_software_affixe** attribute.

        :return: self.__ui_software_affixe.
        :rtype: unicode
        """

        return self.__ui_software_affixe

    @ui_software_affixe.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_software_affixe(self, value):
        """
        Setter for **self.__ui_software_affixe** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_software_affixe"))

    @ui_software_affixe.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_software_affixe(self):
        """
        Deleter for **self.__ui_software_affixe** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_software_affixe"))

    @property
    def ui_unknown_software_image(self):
        """
        Property for **self.__ui_unknown_software_image** attribute.

        :return: self.__ui_unknown_software_image.
        :rtype: unicode
        """

        return self.__ui_unknown_software_image

    @ui_unknown_software_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_unknown_software_image(self, value):
        """
        Setter for **self.__ui_unknown_software_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_unknown_software_image"))

    @ui_unknown_software_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_unknown_software_image(self):
        """
        Deleter for **self.__ui_unknown_software_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_unknown_software_image"))

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
    def database(self):
        """
        Property for **self.__database** attribute.

        :return: self.__database.
        :rtype: object
        """

        return self.__database

    @database.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database(self, value):
        """
        Setter for **self.__database** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "database"))

    @database.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database(self):
        """
        Deleter for **self.__database** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "database"))

    @property
    def model(self):
        """
        Property for **self.__model** attribute.

        :return: self.__model.
        :rtype: TemplatesModel
        """

        return self.__model

    @model.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self, value):
        """
        Setter for **self.__model** attribute.

        :param value: Attribute value.
        :type value: TemplatesModel
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
    def headers(self):
        """
        Property for **self.__headers** attribute.

        :return: self.__headers.
        :rtype: OrderedDict
        """

        return self.__headers

    @headers.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def headers(self, value):
        """
        Setter for **self.__headers** attribute.

        :param value: Attribute value.
        :type value: OrderedDict
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

    @headers.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def headers(self):
        """
        Deleter for **self.__headers** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

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
    def default_collections(self):
        """
        Property for **self.__default_collections** attribute.

        :return: self.__default_collections.
        :rtype: dict
        """

        return self.__default_collections

    @default_collections.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_collections(self, value):
        """
        Setter for **self.__default_collections** attribute.

        :param value: Attribute value.
        :type value: dict
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_collections"))

    @default_collections.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_collections(self):
        """
        Deleter for **self.__default_collections** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_collections"))

    @property
    def factory_collection(self):
        """
        Property for **self.__factory_collection** attribute.

        :return: self.__factory_collection.
        :rtype: unicode
        """

        return self.__factory_collection

    @factory_collection.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def factory_collection(self, value):
        """
        Setter for **self.__factory_collection** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factory_collection"))

    @factory_collection.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def factory_collection(self):
        """
        Deleter for **self.__factory_collection** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factory_collection"))

    @property
    def user_collection(self):
        """
        Property for **self.__user_collection** attribute.

        :return: self.__user_collection.
        :rtype: unicode
        """

        return self.__user_collection

    @user_collection.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def user_collection(self, value):
        """
        Setter for **self.__user_collection** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "user_collection"))

    @user_collection.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def user_collection(self):
        """
        Deleter for **self.__user_collection** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "user_collection"))

    @property
    def templates_informations_default_text(self):
        """
        Property for **self.__templates_informations_default_text** attribute.

        :return: self.__templates_informations_default_text.
        :rtype: unicode
        """

        return self.__templates_informations_default_text

    @templates_informations_default_text.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def templates_informations_default_text(self, value):
        """
        Setter for **self.__templates_informations_default_text** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__,
                                                         "templates_informations_default_text"))

    @templates_informations_default_text.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def templates_informations_default_text(self):
        """
        Deleter for **self.__templates_informations_default_text** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__,
                                                             "templates_informations_default_text"))

    @property
    def tree_view_inner_margins(self):
        """
        Property for **self.__tree_view_inner_margins** attribute.

        :return: self.__tree_view_inner_margins.
        :rtype: int
        """

        return self.__tree_view_inner_margins

    @tree_view_inner_margins.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tree_view_inner_margins(self, value):
        """
        Setter for **self.__tree_view_inner_margins** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tree_view_inner_margins"))

    @tree_view_inner_margins.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tree_view_inner_margins(self):
        """
        Deleter for **self.__tree_view_inner_margins** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tree_view_inner_margins"))

    @property
    def templates_informations_text(self):
        """
        Property for **self.__templates_informations_text** attribute.

        :return: self.__templates_informations_text.
        :rtype: unicode
        """

        return self.__templates_informations_text

    @templates_informations_text.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def templates_informations_text(self, value):
        """
        Setter for **self.__templates_informations_text** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templates_informations_text"))

    @templates_informations_text.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def templates_informations_text(self):
        """
        Deleter for **self.__templates_informations_text** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templates_informations_text"))

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
        self.__database = self.__engine.components_manager["core.database"]

        RuntimeGlobals.templates_factory_directory = umbra.ui.common.get_resource_path(Constants.templates_directory)
        RuntimeGlobals.templates_user_directory = os.path.join(self.__engine.user_application_data_directory,
                                                               Constants.templates_directory)

        self.__default_collections = {self.__factory_collection: RuntimeGlobals.templates_factory_directory,
                                      self.__user_collection: RuntimeGlobals.templates_user_directory}

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
        LOGGER.info("{0} | Model edition deactivated by '{1}' command line parameter value!".format(
            self.__class__.__name__, "database_read_only"))
        self.__model = TemplatesModel(self, horizontal_headers=self.__headers)
        self.set_templates()

        self.Templates_Outliner_treeView.setParent(None)
        self.Templates_Outliner_treeView = Templates_QTreeView(self,
                                                               self.__model,
                                                               self.__engine.parameters.database_read_only,
                                                               "No Template to view!")
        self.Templates_Outliner_treeView.setObjectName("Templates_Outliner_treeView")
        self.Templates_Outliner_gridLayout.setContentsMargins(self.__tree_view_inner_margins)
        self.Templates_Outliner_gridLayout.addWidget(self.Templates_Outliner_treeView, 0, 0)
        self.__view = self.Templates_Outliner_treeView
        self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.__view_add_actions()

        self.Template_Informations_textBrowser.setText(self.__templates_informations_default_text)
        self.Template_Informations_textBrowser.setOpenLinks(False)

        self.Templates_Outliner_splitter.setSizes([16777215, 1])

        # Signals / Slots.
        self.__engine.images_caches.QIcon.content_added.connect(self.__view.viewport().update)
        self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
        self.Template_Informations_textBrowser.anchorClicked.connect(
            self.__Template_Informations_textBrowser__anchorClicked)
        self.refresh_nodes.connect(self.__model__refresh_nodes)
        if not self.__engine.parameters.database_read_only:
            self.__engine.file_system_events_manager.file_changed.connect(
                self.__engine_file_system_events_manager__file_changed)
            self.__engine.content_dropped.connect(self.__engine__content_dropped)
        else:
            LOGGER.info("{0} | Templates file system events ignored by '{1}' command line parameter value!".format(
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

        self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dock_area), self)

        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def remove_widget(self):
        """
        Removes the Component Widget from the engine.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

    def on_startup(self):
        """
        Defines the slot triggered by Framework startup.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Calling '{0}' Component Framework 'on_startup' method.".format(self.__class__.__name__))

        if not self.__engine.parameters.database_read_only:
            # Adding default Templates.
            self.add_default_templates()

            # Wizard if Templates table is empty.
            if not self.get_templates():
                if message_box.message_box("Question", "Question",
                                           "The Database has no Templates, would you like to add some?",
                                           buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    directory = umbra.ui.common.store_last_browsed_path((QFileDialog.getExistingDirectory(self,
                                                                                                          "Add Content:",
                                                                                                          RuntimeGlobals.last_browsed_path)))
                    if directory:
                        if not self.add_directory(directory):
                            raise Exception(
                                "{0} | Exception raised while adding '{1}' directory content to the Database!".format(
                                    self.__class__.__name__, directory))

            # Templates table integrity checking.
            erroneous_templates = sibl_gui.components.core.database.operations.check_templates_table_integrity()
            for template, exceptions in erroneous_templates.iteritems():
                if sibl_gui.components.core.database.exceptions.MissingTemplateFileError in exceptions:
                    choice = message_box.message_box("Question", "Error",
                                                     "{0} | '{1}' Template file is missing, would you like to update it's location?".format(
                                                         self.__class__.__name__, template.name),
                                                     QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No,
                                                     custom_buttons=((QString("No To All"), QMessageBox.RejectRole),))

                    if choice == 0:
                        break

                    if choice == QMessageBox.Yes:
                        if self.update_template_location_ui(template):
                            # TODO: Check updated Template file integrity.
                            continue

                for exception in exceptions:
                    self.__engine.notifications_manager.warnify(
                        "{0} | '{1}' {2}".format(self.__class__.__name__,
                                                 template.name,
                                                 sibl_gui.components.core.database.operations.DATABASE_EXCEPTIONS[
                                                     exception]))
        else:
            LOGGER.info("{0} | Database default Templates wizard and Templates integrity checking method deactivated\
by '{1}' command line parameter value!".format(self.__class__.__name__, "database_read_only"))

        active_collections_identities = foundations.strings.to_string(self.__settings.get_key(
            self.__settings_section, "active_collections").toString())
        LOGGER.debug("> Stored '{0}' active Collections selection: '{1}'.".format(self.__class__.__name__,
                                                                                  active_collections_identities))
        self.__view.model_selection["collections"] = active_collections_identities and [int(identity)
                                                                                        for identity in
                                                                                        active_collections_identities.split(
                                                                                            self.__settings_separator)] or []

        active_softwares = foundations.strings.to_string(
            self.__settings.get_key(self.__settings_section, "active_softwares").toString())
        LOGGER.debug("> Stored '{0}' active softwares selection: '{1}'.".format(
            self.__class__.__name__, active_softwares))
        self.__view.model_selection["Softwares"] = active_softwares and active_softwares.split(
            self.__settings_separator) or []

        active_templates_identities = foundations.strings.to_string(
            self.__settings.get_key(self.__settings_section, "activeTemplates").toString())
        LOGGER.debug("> '{0}' View stored selected Templates identities '{1}'.".format(self.__class__.__name__,
                                                                                       active_templates_identities))
        self.__view.model_selection["templates"] = active_templates_identities and [int(identity)
                                                                                    for identity in
                                                                                    active_templates_identities.split(
                                                                                        self.__settings_separator)] or []

        self.__view.restore_model_selection()
        return True

    def on_close(self):
        """
        Defines the slot triggered by Framework close.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Calling '{0}' Component Framework 'on_close' method.".format(self.__class__.__name__))

        self.__view.store_model_selection()
        self.__settings.set_key(self.__settings_section,
                                "activeTemplates",
                                self.__settings_separator.join(foundations.strings.to_string(identity)
                                                               for identity in
                                                               self.__view.model_selection["templates"]))
        self.__settings.set_key(self.__settings_section,
                                "active_collections",
                                self.__settings_separator.join(foundations.strings.to_string(identity)
                                                               for identity in
                                                               self.__view.model_selection["collections"]))
        self.__settings.set_key(self.__settings_section,
                                "active_softwares",
                                self.__settings_separator.join(foundations.strings.to_string(name)
                                                               for name in self.__view.model_selection["Softwares"]))
        return True

    def __model__refresh_nodes(self):
        """
        Defines the slot triggered by the Model when nodes need refresh.
        """

        self.set_templates()

    def __view_add_actions(self):
        """
        Sets the View actions.
        """

        if not self.__engine.parameters.database_read_only:
            self.__view.addAction(self.__engine.actions_manager.register_action(
                "Actions|Umbra|Components|core.templates_outliner|Add Template ...",
                slot=self.__view_add_template_action__triggered))
            self.__view.addAction(self.__engine.actions_manager.register_action(
                "Actions|Umbra|Components|core.templates_outliner|Remove Template(s) ...",
                slot=self.__view_remove_templates_action__triggered))

            separator_action = QAction(self.__view)
            separator_action.setSeparator(True)
            self.__view.addAction(separator_action)

            self.__view.addAction(self.__engine.actions_manager.register_action(
                "Actions|Umbra|Components|core.templates_outliner|Import Default Templates",
                slot=self.__view_import_default_templates_action__triggered))
            self.__view.addAction(self.__engine.actions_manager.register_action(
                "Actions|Umbra|Components|core.templates_outliner|Filter Templates Versions",
                slot=self.__view_filter_templates_versions_action__triggered))

            separator_action = QAction(self.__view)
            separator_action.setSeparator(True)
            self.__view.addAction(separator_action)
        else:
            LOGGER.info("{0} | Templates Database alteration capabilities deactivated\
by '{1}' command line parameter value!".format(self.__class__.__name__, "database_read_only"))

        self.__view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.templates_outliner|Display Help File(s) ...",
            slot=self.__view_display_help_files_action__triggered))

        separator_action = QAction(self.__view)
        separator_action.setSeparator(True)
        self.__view.addAction(separator_action)

    def __view_add_template_action__triggered(self, checked):
        """
        Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templates_outliner|Add Template ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.add_template_ui()

    def __view_remove_templates_action__triggered(self, checked):
        """
        Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templates_outliner|Remove Template(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.remove_templates_ui()

    def __view_import_default_templates_action__triggered(self, checked):
        """
        Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templates_outliner|Import Default Templates'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.import_default_templates_ui()

    def __view_display_help_files_action__triggered(self, checked):
        """
        Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templates_outliner|Display Help File(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.display_help_files_ui()

    def __view_filter_templates_versions_action__triggered(self, checked):
        """
        Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templates_outliner|Filter Templates Versions'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.filter_templates_versions_ui()

    def __view_selectionModel__selectionChanged(self, selected_items, deselected_items):
        """
        Sets the **Template_Informations_textEdit** Widget.

        :param selected_items: Selected items.
        :type selected_items: QItemSelection
        :param deselected_items: Deselected items.
        :type deselected_items: QItemSelection
        """

        LOGGER.debug("> Initializing '{0}' Widget.".format("Template_Informations_textEdit"))

        selected_templates = self.get_selected_templates()
        content = []

        if selected_templates:
            for template in selected_templates:
                help_file = template.help_file or umbra.ui.common.get_resource_path(UiConstants.invalid_link_html_file)
                content.append(self.__templates_informations_text.format(template.title,
                                                                         template.date,
                                                                         template.author,
                                                                         template.email,
                                                                         template.url,
                                                                         template.output_script,
                                                                         template.comment,
                                                                         QUrl.fromLocalFile(help_file).toString()))
        else:
            content.append(self.__templates_informations_default_text)

        separator = "" if len(content) == 1 else "<p><center>* * *<center/></p>"

        self.Template_Informations_textBrowser.setText(separator.join(content))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              foundations.exceptions.UserError)
    @umbra.engine.show_processing("Retrieving Templates ...")
    def __engine__content_dropped(self, event):
        """
        Defines the slot triggered when content is dropped into the engine.

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
                                                     "'{0}' Template file has been dropped, would you like to 'Add' it to the Database or \
'Edit' it in the Script Editor?".format(name),
                                                     buttons=QMessageBox.Cancel,
                                                     custom_buttons=((QString("Add"), QMessageBox.AcceptRole),
                                                                     (QString("Edit"), QMessageBox.AcceptRole)))
                    if choice == 0:
                        self.add_template(name, path)
                    elif choice == 1:
                        self.__script_editor.load_file(path) and self.__script_editor.restore_development_layout()
                else:
                    if not os.path.isdir(path):
                        return

                    if not list(foundations.walkers.files_walker(path, ("\.{0}$".format(self.__extension),), ("\._",))):
                        return

                    if message_box.message_box("Question", "Question",
                                               "Would you like to add '{0}' directory Template(s) file(s) to the Database?".format(
                                                       path),
                                               buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                        self.add_directory(path)
                self.__engine.process_events()
        else:
            raise foundations.exceptions.UserError(
                "{0} | Cannot perform action, Database has been set read only!".format(self.__class__.__name__))

    def __engine_file_system_events_manager__file_changed(self, file):
        """
        Defines the slot triggered by the **file_system_events_manager** when a file is changed.

        :param file: File changed.
        :type file: unicode
        """

        template = foundations.common.get_first_item(filter(lambda x: x.path == file, self.get_templates()))
        if not template:
            return

        if sibl_gui.components.core.database.operations.update_template_content(template):
            self.__engine.notifications_manager.notify(
                "{0} | '{1}' Template file has been reparsed and associated database object updated!".format(
                    self.__class__.__name__, template.title))
            self.refresh_nodes.emit()

    def __Template_Informations_textBrowser__anchorClicked(self, url):
        """
        Defines the slot triggered by **Template_Informations_textBrowser** Widget when a link is clicked.

        :param url: Url to explore.
        :type url: QUrl
        """

        QDesktopServices.openUrl(url)

    def __get_candidate_collection_id(self, path=None):
        """
        Returns a Collection id.

        :param path: Template path.
        :type path: unicode
        :return: Collection id.
        :rtype: int
        """

        collection = self.get_collection_by_name(self.__user_collection)
        identity = collection and collection.id or None

        factory_collectionPath = self.__default_collections[self.__factory_collection]
        if path and factory_collectionPath:
            if os.path.normpath(factory_collectionPath) in os.path.normpath(path):
                collection = self.get_collection_by_name(self.__factory_collection)
                identity = collection and collection.id or None
        return identity

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.show_processing("Adding Template ...")
    def add_template_ui(self):
        """
        Adds an user defined Template to the Database.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        path = umbra.ui.common.store_last_browsed_path((QFileDialog.getOpenFileName(self,
                                                                                    "Add Template:",
                                                                                    RuntimeGlobals.last_browsed_path,
                                                                                    "sIBLT files (*.{0})".format(
                                                                                        self.__extension))))
        if not path:
            return

        if not self.template_exists(path):
            LOGGER.debug("> Chosen Template path: '{0}'.".format(path))
            if self.add_template(foundations.strings.get_splitext_basename(path), path):
                return True
            else:
                raise Exception("{0} | Exception raised while adding '{1}' Template to the Database!".format(
                    self.__class__.__name__, path))
        else:
            self.__engine.notifications_manager.warnify(
                "{0} | '{1}' Template already exists in Database!".format(self.__class__.__name__, path))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.encapsulate_processing
    def remove_templates_ui(self):
        """
        Removes user selected Templates from the Database.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_nodes = self.get_selected_nodes()

        selected_collections = []
        selected_softwares = []
        for item in selected_nodes:
            if item.family == "Collection":
                selected_collections.append(item.name)
            elif item.family == "Software":
                selected_softwares.append(item.name)
        selected_collections and self.__engine.notifications_manager.warnify(
            "{0} | '{1}' Collection(s) cannot be removed!".format(self.__class__.__name__,
                                                                  ", ".join(selected_collections)))
        selected_softwares and self.__engine.notifications_manager.warnify(
            "{0} | '{1}' software(s) cannot be removed!".format(self.__class__.__name__, ", ".join(selected_softwares)))

        selected_templates = self.get_selected_templates()
        if not selected_templates:
            return False

        if message_box.message_box("Question", "Question",
                                   "Are you sure you want to remove '{0}' Template(s)?".format(
                                           ", ".join([foundations.strings.to_string(template.name) for template in
                                                      selected_templates])),
                                   buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.__engine.start_processing("Removing Templates ...", len(selected_templates))
            success = True
            for template in selected_templates:
                success *= umbra.ui.common.signals_blocker(self, self.remove_template, template) or False
                self.__engine.step_processing()
            self.__engine.stop_processing()

            self.refresh_nodes.emit()

            if success:
                return True
            else:
                raise Exception("{0} | Exception raised while removing '{1}' Templates from the Database!".format(
                    self.__class__.__name__, ", ".join((template.name for template in selected_templates))))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              sibl_gui.components.core.database.exceptions.DatabaseOperationError)
    def update_template_location_ui(self, template):
        """
        Updates given Template location.

        :param template: Template to update.
        :type template: Template
        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        file = umbra.ui.common.store_last_browsed_path((QFileDialog.getOpenFileName(self,
                                                                                    "Updating '{0}' Template Location:".format(
                                                                                        template.name),
                                                                                    RuntimeGlobals.last_browsed_path,
                                                                                    "Template files (*{0})".format(
                                                                                        self.__extension))))
        if not file:
            return False

        LOGGER.info("{0} | Updating '{1}' Template with new location '{2}'!".format(self.__class__.__name__,
                                                                                    template.name, file))
        if sibl_gui.components.core.database.operations.update_template_location(template, file):
            self.refresh_nodes.emit()
            return True
        else:
            raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
                "{0} | Exception raised while updating '{1}' Template location!".format(self.__class__.__name__,
                                                                                        template.name))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.show_processing("Importing Default Templates ...")
    def import_default_templates_ui(self):
        """
        Imports default Templates into the Database.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        if self.add_default_templates(force_import=True):
            return True
        else:
            raise Exception("{0} | Exception raised while importing default Templates into the Database!".format(
                self.__class__.__name__))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.encapsulate_processing
    def display_help_files_ui(self):
        """
        Displays user selected Templates help files.

        :return: Method success.
        :rtype: bool
        """

        selected_templates = self.get_selected_templates()
        if not selected_templates:
            return False

        self.__engine.start_processing("Displaying Templates Help Files ...", len(selected_templates))
        success = True
        for template in selected_templates:
            success *= self.display_help_file(template) or False
            self.__engine.step_processing()
        self.__engine.stop_processing()

        if success:
            return True
        else:
            raise Exception(
                "{0} | Exception raised while displaying Templates help files!".format(self.__class__.__name__))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.encapsulate_processing
    def filter_templates_versions_ui(self):
        """
        Filters Templates by versions.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        templates = sibl_gui.components.core.database.operations.get_templates()
        self.__engine.start_processing("Filtering Templates ...", len(templates.all()))
        success = True
        for template in templates:
            matching_templates = sibl_gui.components.core.database.operations.filter_templates(
                "^{0}$".format(template.name), "name")
            if len(matching_templates) != 1:
                for identity in sorted(
                        [(database_template.id, database_template.release) for database_template in matching_templates],
                        reverse=True,
                        key=lambda x: (foundations.strings.get_version_rank(x[1])))[1:]:
                    success *= sibl_gui.components.core.database.operations.remove_template(
                        foundations.common.get_first_item(identity)) or False
                self.refresh_nodes.emit()
            self.__engine.step_processing()
        self.__engine.stop_processing()

        if success:
            return True
        else:
            raise Exception(
                "{0} | Exception raised while filtering Templates by versions!".format(self.__class__.__name__))

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError,
                                              sibl_gui.components.core.database.exceptions.DatabaseOperationError)
    def add_template(self, name, path, collection_id=None):
        """
        Adds a Template to the Database.

        :param name: Template set name.
        :type name: unicode
        :param path: Template set path.
        :type path: unicode
        :param collection_id: Target Collection id.
        :type collection_id: int
        :return: Method success.
        :rtype: bool
        """

        if not sibl_gui.components.core.database.operations.filter_templates("^{0}$".format(re.escape(path)), "path"):
            LOGGER.info("{0} | Adding '{1}' Template to the Database!".format(self.__class__.__name__, name))
            if sibl_gui.components.core.database.operations.add_template(
                    name, path, collection_id or self.__get_candidate_collection_id(path)):
                self.refresh_nodes.emit()
                return True
            else:
                raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
                    "{0} | Exception raised while adding '{1}' Template to the Database!".format(
                        self.__class__.__name__, name))
        else:
            raise foundations.exceptions.ProgrammingError(
                "{0} | '{1}' Template already exists in Database!".format(self.__class__.__name__, name))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    @umbra.engine.encapsulate_processing
    def add_directory(self, directory, collection_id=None):
        """
        Adds given directory Templates to the Database.

        :param directory: Templates directory.
        :type directory: unicode
        :param collection_id: Collection id.
        :type collection_id: int
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing directory '{0}' files_walker.".format(directory))

        files = list(foundations.walkers.files_walker(directory, ("\.{0}$".format(self.__extension),), ("\._",)))

        self.__engine.start_processing("Adding Directory Templates ...", len(files))
        success = True
        for path in files:
            if not self.template_exists(path):
                success *= umbra.ui.common.signals_blocker(self,
                                                           self.add_template,
                                                           foundations.strings.get_splitext_basename(path),
                                                           path,
                                                           collection_id) or False
            self.__engine.step_processing()
        self.__engine.stop_processing()

        self.refresh_nodes.emit()

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
                self.__class__.__name__, directory))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def add_default_templates(self, force_import=False):
        """
        Adds default Templates Collections / Templates to the Database.

        :param force_import: Force Templates import.
        :type force_import: bool
        :return: Method success.
        :rtype: bool
        """

        if not force_import and self.get_templates():
            return False

        LOGGER.debug("> Adding default Templates to the Database.")

        success = True
        for collection, path in ((collection, path) for (collection, path) in self.__default_collections.iteritems() if
                                 path):
            if not foundations.common.path_exists(path):
                continue

            if not set(sibl_gui.components.core.database.operations.filter_collections(
                    "^{0}$".format(collection), "name")).intersection(
                    sibl_gui.components.core.database.operations.filter_collections("templates", "type")):
                LOGGER.info("{0} | Adding '{1}' Collection to the Database!".format(
                    self.__class__.__name__, collection))
                sibl_gui.components.core.database.operations.add_collection(
                    collection, "templates", "Template {0} Collection".format(collection))
            success *= self.add_directory(path, self.get_collection_by_name(collection).id)

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while adding default Templates to the Database!".format(
                self.__class__.__name__))

    @foundations.exceptions.handle_exceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
    def remove_template(self, template):
        """
        Removes given Template from the Database.

        :param templates: Template to remove.
        :type templates: list
        :return: Method success.
        :rtype: bool
        """

        LOGGER.info("{0} | Removing '{1}' Template from the Database!".format(self.__class__.__name__, template.name))
        if sibl_gui.components.core.database.operations.remove_template(foundations.strings.to_string(template.id)):
            self.refresh_nodes.emit()
            return True
        else:
            raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
                "{0} | Exception raised while removing '{1}' Template from the Database!".format(
                    self.__class__.__name__,
                    template.name))

    def template_exists(self, path):
        """
        Returns if given Template path exists in the Database.

        :param name: Template path.
        :type name: unicode
        :return: Template exists.
        :rtype: bool
        """

        return sibl_gui.components.core.database.operations.template_exists(path)

    @foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
    def display_help_file(self, template):
        """
        Displays given Templates help file.

        :param template: Template to display help file.
        :type template: Template
        :return: Method success.
        :rtype: bool
        """

        help_file = template.help_file or umbra.ui.common.get_resource_path(UiConstants.invalid_link_html_file)
        if foundations.common.path_exists(help_file):
            LOGGER.info("{0} | Opening '{1}' Template help file: '{2}'.".format(self.__class__.__name__,
                                                                                template.name,
                                                                                help_file))
            QDesktopServices.openUrl(QUrl.fromLocalFile(help_file))
            return True
        else:
            raise foundations.exceptions.FileExistsError(
                "{0} | Exception raised while displaying '{1}' Template help file: '{2}' file doesn't exists!".format(
                    self.__class__.__name__, template.name, help_file))

    def get_collections(self):
        """
        Returns Database Templates Collections.

        :return: Database Templates Collections.
        :rtype: list
        """

        return sibl_gui.components.core.database.operations.get_collections_by_type("templates")

    def filter_collections(self, pattern, attribute, flags=re.IGNORECASE):
        """
        Filters the Database Templates Collections on given attribute using given pattern.

        :param pattern: Filter pattern.
        :type pattern: unicode
        :param attribute: Attribute to filter on.
        :type attribute: unicode
        :param flags: Regex filtering flags.
        :type flags: int

        :return: Filtered Database Templates Collections.
        :rtype: list
        """

        try:
            pattern = re.compile(pattern, flags)
        except Exception:
            return list()

        return sibl_gui.components.core.database.operations.filter_templates_collections(
            "{0}".format(foundations.strings.to_string(pattern.pattern)), attribute, flags)

    def get_templates(self):
        """
        Returns Database Templates.

        :return: Database Templates.
        :rtype: list
        """

        return [template for template in sibl_gui.components.core.database.operations.get_templates()]

    def filter_templates(self, pattern, attribute, flags=re.IGNORECASE):
        """
        Filters the Database Templates on given attribute using given pattern.

        :param pattern: Filter pattern.
        :type pattern: unicode
        :param attribute: Attribute to filter on.
        :type attribute: unicode
        :param flags: Regex filtering flags.
        :type flags: int

        :return: Filtered Database Templates.
        :rtype: list
        """

        try:
            pattern = re.compile(pattern, flags)
        except Exception:
            return list()

        return list(set(self.get_templates()).intersection(
            sibl_gui.components.core.database.operations.filter_templates(
                "{0}".format(foundations.strings.to_string(pattern.pattern)), attribute, flags)))

    def list_templates(self):
        """
        Lists Database Templates names.

        :return: Database Templates names.
        :rtype: list
        """

        return [template.title for template in self.get_templates()]

    def set_templates(self):
        """
        Sets the Templates Model nodes.
        """

        node_flags = attributes_flags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)

        root_node = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")

        collections = sibl_gui.components.core.database.operations.filter_collections("templates", "type")
        for collection in collections:
            softwares = set((foundations.common.get_first_item(software) for software in
                             sibl_gui.components.core.database.operations.query(Template.software).filter(
                                 Template.collection == collection.id)))
            if not softwares:
                continue

            collection_node = CollectionNode(collection,
                                             name=collection.name,
                                             parent=root_node,
                                             node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                                             attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
            collection_node["release"] = sibl_gui.ui.nodes.GraphModelAttribute(name="release",
                                                                               flags=int(
                                                                                   Qt.ItemIsSelectable | Qt.ItemIsEnabled))
            collection_node["version"] = sibl_gui.ui.nodes.GraphModelAttribute(name="version",
                                                                               flags=int(
                                                                                   Qt.ItemIsSelectable | Qt.ItemIsEnabled))
            for software in softwares:
                templates = set((template for template in sibl_gui.components.core.database.operations.query(
                    Template).filter(Template.collection == collection.id).filter(
                    Template.software == software)))

                if not templates:
                    continue

                software_node = SoftwareNode(name=software,
                                             parent=collection_node,
                                             node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                                             attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
                icon_path = os.path.join(
                    self.__ui_resources_directory, "{0}{1}".format(software, self.__ui_software_affixe))
                software_node.roles[Qt.DecorationRole] = icon_path if foundations.common.path_exists(icon_path) else \
                    os.path.join(self.__ui_resources_directory, self.__ui_unknown_software_image)

                for template in templates:
                    template_node = TemplateNode(template,
                                                 name=foundations.strings.remove_strip(
                                                     template.title, template.software),
                                                 parent=software_node,
                                                 node_flags=node_flags,
                                                 attributes_flags=attributes_flags)

                    path = foundations.strings.to_string(template.path)
                    if not foundations.common.path_exists(path):
                        continue

                    not self.__engine.file_system_events_manager.is_path_registered(path) and \
                    self.__engine.file_system_events_manager.register_path(
                        path, modified_time=float(template.os_stats.split(",")[8]))

        root_node.sort_children(attribute="title")

        self.__model.initialize_model(root_node)
        return True

    def get_template_by_name(self, name):
        """
        Returns Database Template with given name.

        :param name: Template name.
        :type name: unicode
        :return: Database Template.
        :rtype: Template

        :note: The filtering is actually performed on 'title' attributes instead of 'name' attributes.
        """

        templates = self.filter_templates(r"^{0}$".format(name), "title")
        return foundations.common.get_first_item(templates)

    def get_collection_by_name(self, name):
        """
        Returns Templates Collection from given Collection name.

        :param collection: Collection name.
        :type collection: unicode
        :return: Collection.
        :rtype: Collection
        """

        collections = self.filter_collections(r"^{0}$".format(name), "name")
        return foundations.common.get_first_item(collections)

    def get_collection_id(self, collection):
        """
        Returns given Collection id.

        :param collection: Collection to get the id from.
        :type collection: unicode
        :return: Provided Collection id.
        :rtype: int
        """

        children = self.__model.find_children(r"^{0}$".format(collection))
        child = foundations.common.get_first_item(children)
        return child and child.database_item.id or None

    def get_selected_nodes(self):
        """
        Returns the View selected nodes.

        :return: View selected nodes.
        :rtype: dict
        """

        return self.__view.get_selected_nodes()

    def get_selected_templates_nodes(self):
        """
        Returns the View selected Templates nodes.

        :return: View selected Templates nodes.
        :rtype: list
        """

        return [node for node in self.get_selected_nodes() if node.family == "Template"]

    def get_selected_templates(self):
        """
        Returns the View selected Templates.

        :return: View selected Templates.
        :rtype: list
        """

        return [node.database_item for node in self.get_selected_templates_nodes()]
