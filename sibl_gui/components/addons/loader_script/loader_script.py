#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**loader_script.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`LoaderScript` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform
import re
import socket
from PyQt4.QtCore import Qt

import foundations.common
import foundations.exceptions
import foundations.namespace
import foundations.parsers
import foundations.strings
import foundations.verbose
import sibl_gui.exceptions
import umbra.exceptions
from foundations.io import File
from manager.QWidget_component import QWidgetComponentFactory
from umbra.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_FILE", "LoaderScript"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_FILE = os.path.join(os.path.dirname(__file__), "ui", "Loader_Script.ui")


class LoaderScript(QWidgetComponentFactory(ui_file=COMPONENT_FILE)):
    """
    | Defines the :mod:`sibl_gui.components.addons.loader_script.loader_script` Component Interface class.
    | It provides the glue between the Ibl Sets, the Templates and the 3d package.

    A typical operation is the following:

        - Retrieve both Ibl Set and Template files.
        - Parse Ibl Set and Template files.
        - Retrieve override keys defined by the user and / or another Component.
        - Generate the Loader Script.
        - Write the Loader Script.
        - Establish a connection with the 3d package and trigger the Loader Script execution.
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

        super(LoaderScript, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = True

        self.__dock_area = 2

        self.__engine = None

        self.__ibl_sets_outliner = None
        self.__templates_outliner = None
        self.__tcp_client_ui = None

        self.__io_directory = "loader_scripts"

        self.__binding_identifier_pattern = "@[a-zA-Z0-9_]*"
        self.__template_script_section = "Script"
        self.__template_ibl_set_attributes_section = "Ibl Set Attributes"
        self.__template_remote_connection_section = "Remote Connection"

        self.__win32_execution_method = "ExecuteSIBLLoaderScript"

        self.__override_keys = {}

        self.__default_string_separator = "|"
        self.__unnamed_light_name = "Unnamed_Light"

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
    def templates_outliner(self):
        """
        Property for **self.__templates_outliner** attribute.

        :return: self.__templates_outliner.
        :rtype: QWidget
        """

        return self.__templates_outliner

    @templates_outliner.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def templates_outliner(self, value):
        """
        Setter for **self.__templates_outliner** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templates_outliner"))

    @templates_outliner.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def templates_outliner(self):
        """
        Deleter for **self.__templates_outliner** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templates_outliner"))

    @property
    def tcp_client_ui(self):
        """
        Property for **self.__tcp_client_ui** attribute.

        :return: self.__tcp_client_ui.
        :rtype: QWidget
        """

        return self.__tcp_client_ui

    @tcp_client_ui.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tcp_client_ui(self, value):
        """
        Setter for **self.__tcp_client_ui** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tcp_client_ui"))

    @tcp_client_ui.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tcp_client_ui(self):
        """
        Deleter for **self.__tcp_client_ui** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tcp_client_ui"))

    @property
    def io_directory(self):
        """
        Property for **self.__io_directory** attribute.

        :return: self.__io_directory.
        :rtype: unicode
        """

        return self.__io_directory

    @io_directory.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def io_directory(self, value):
        """
        Setter for **self.__io_directory** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "io_directory"))

    @io_directory.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def io_directory(self):
        """
        Deleter for **self.__io_directory** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "io_directory"))

    @property
    def binding_identifier_pattern(self):
        """
        Property for **self.__binding_identifier_pattern** attribute.

        :return: self.__binding_identifier_pattern.
        :rtype: unicode
        """

        return self.__binding_identifier_pattern

    @binding_identifier_pattern.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def binding_identifier_pattern(self, value):
        """
        Setter for **self.__binding_identifier_pattern** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "binding_identifier_pattern"))

    @binding_identifier_pattern.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def binding_identifier_pattern(self):
        """
        Deleter for **self.__binding_identifier_pattern** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "binding_identifier_pattern"))

    @property
    def template_script_section(self):
        """
        Property for **self.__template_script_section** attribute.

        :return: self.__template_script_section.
        :rtype: unicode
        """

        return self.__template_script_section

    @template_script_section.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def template_script_section(self, value):
        """
        Setter for **self.__template_script_section** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "template_script_section"))

    @template_script_section.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def template_script_section(self):
        """
        Deleter for **self.__template_script_section** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "template_script_section"))

    @property
    def template_ibl_set_attributes_section(self):
        """
        Property for **self.__template_ibl_set_attributes_section** attribute.

        :return: self.__template_ibl_set_attributes_section.
        :rtype: unicode
        """

        return self.__template_ibl_set_attributes_section

    @template_ibl_set_attributes_section.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def template_ibl_set_attributes_section(self, value):
        """
        Setter for **self.__template_ibl_set_attributes_section** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__,
                                                         "template_ibl_set_attributes_section"))

    @template_ibl_set_attributes_section.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def template_ibl_set_attributes_section(self):
        """
        Deleter for **self.__template_ibl_set_attributes_section** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__,
                                                             "template_ibl_set_attributes_section"))

    @property
    def template_remote_connection_section(self):
        """
        Property for **self.__template_remote_connection_section** attribute.

        :return: self.__template_remote_connection_section.
        :rtype: unicode
        """

        return self.__template_remote_connection_section

    @template_remote_connection_section.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def template_remote_connection_section(self, value):
        """
        Setter for **self.__template_remote_connection_section** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "template_remote_connection_section"))

    @template_remote_connection_section.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def template_remote_connection_section(self):
        """
        Deleter for **self.__template_remote_connection_section** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__,
                                                             "template_remote_connection_section"))

    @property
    def override_keys(self):
        """
        Property for **self.__override_keys** attribute.

        :return: self.__override_keys.
        :rtype: dict
        """

        return self.__override_keys

    @override_keys.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def override_keys(self, value):
        """
        Setter for **self.__override_keys** attribute.

        :param value: Attribute value.
        :type value: dict
        """

        if value is not None:
            assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("override_keys", value)
            for key, element in value.iteritems():
                assert type(key) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
                    "override_keys", key)
                assert type(element) is foundations.parsers.AttributeCompound, \
                    "'{0}' attribute: '{1}' type is not 'foundations.parsers.AttributeCompound'!".format(
                        "override_keys", element)
        self.__override_keys = value

    @override_keys.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def override_keys(self):
        """
        Deleter for **self.__override_keys** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "override_keys"))

    @property
    def default_string_separator(self):
        """
        Property for **self.__default_string_separator** attribute.

        :return: self.__default_string_separator.
        :rtype: unicode
        """

        return self.__default_string_separator

    @default_string_separator.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def default_string_separator(self, value):
        """
        Setter for **self.__default_string_separator** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
                "default_string_separator", value)
            assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format(
                "default_string_separator", value)
            assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
                "default_string_separator", value)
        self.__default_string_separator = value

    @default_string_separator.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_string_separator(self):
        """
        Deleter for **self.__default_string_separator** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_string_separator"))

    @property
    def unnamed_light_name(self):
        """
        Property for **self.__unnamed_light_name** attribute.

        :return: self.__unnamed_light_name.
        :rtype: unicode
        """

        return self.__unnamed_light_name

    @unnamed_light_name.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def unnamed_light_name(self, value):
        """
        Setter for **self.__unnamed_light_name** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
                "unnamed_light_name", value)
        self.__unnamed_light_name = value

    @unnamed_light_name.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def unnamed_light_name(self):
        """
        Deleter for **self.__unnamed_light_name** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "unnamed_light_name"))

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
        self.__templates_outliner = self.__engine.components_manager["core.templates_outliner"]
        self.__tcp_client_ui = self.__engine.components_manager["addons.tcp_client_ui"]

        self.__io_directory = os.path.join(self.__engine.user_application_data_directory,
                                           Constants.io_directory,
                                           self.__io_directory)
        not foundations.common.path_exists(self.__io_directory) and os.makedirs(self.__io_directory)

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
        self.__templates_outliner = None
        self.__tcp_client_ui = None

        self.__io_directory = os.path.basename(os.path.abspath(self.__io_directory))

        self.activated = False
        return True

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        if platform.system() in ("Darwin", "Linux"):
            self.Options_groupBox.hide()

        # Signals / Slots.
        self.Output_Loader_Script_pushButton.clicked.connect(self.__Output_Loader_Script_pushButton__clicked)
        self.Send_To_Software_pushButton.clicked.connect(self.__Send_To_Software_pushButton__clicked)
        self.__templates_outliner.view.selectionModel().selectionChanged.connect(
            self.__templates_outliner_view_selectionModel__selectionChanged)

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
        self.Output_Loader_Script_pushButton.clicked.disconnect(self.__Output_Loader_Script_pushButton__clicked)
        self.Send_To_Software_pushButton.clicked.disconnect(self.__Send_To_Software_pushButton__clicked)
        self.__templates_outliner.view.selectionModel().selectionChanged.disconnect(
            self.__templates_outliner_view_selectionModel__selectionChanged)

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

    def __Output_Loader_Script_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Output_Loader_Script_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.output_loader_script_ui()

    def __Send_To_Software_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Send_To_Software_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.send_loader_script_to_software_ui()

    def __templates_outliner_view_selectionModel__selectionChanged(self, selected_items, deselected_items):
        """
        Defines the slot triggered by **templates_outliner.view** Model when selection changed

        :param selected_items: Selected items.
        :type selected_items: QItemSelection
        :param deselected_items: Deselected items.
        :type deselected_items: QItemSelection
        """

        selected_templates = self.__templates_outliner.get_selected_templates()
        template = foundations.common.get_first_item(selected_templates)
        if not (template and foundations.common.path_exists(template.path)):
            return

        LOGGER.debug("> Parsing '{0}' Template for '{1}' section.".format(template.name,
                                                                          self.__template_remote_connection_section))
        template_sections_file_parser = foundations.parsers.SectionsFileParser(template.path)
        template_sections_file_parser.parse(raw_sections=(self.__template_script_section))

        if not self.__template_remote_connection_section in template_sections_file_parser.sections:
            return

        LOGGER.debug("> {0}' section found.".format(self.__template_remote_connection_section))
        connection_type = foundations.parsers.get_attribute_compound("ConnectionType",
                                                                     template_sections_file_parser.get_value(
                                                                         "ConnectionType",
                                                                         self.__template_remote_connection_section))
        if connection_type.value == "Socket":
            LOGGER.debug("> Remote connection type: 'Socket'.")
            self.__tcp_client_ui.address = foundations.parsers.get_attribute_compound("DefaultAddress",
                                                                                      template_sections_file_parser.get_value(
                                                                                          "DefaultAddress",
                                                                                          self.__template_remote_connection_section)).value
            self.__tcp_client_ui.port = int(foundations.parsers.get_attribute_compound("DefaultPort",
                                                                                       template_sections_file_parser.get_value(
                                                                                           "DefaultPort",
                                                                                           self.__template_remote_connection_section)).value)
        elif connection_type.value == "Win32":
            LOGGER.debug("> Remote connection: 'Win32'.")

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              foundations.exceptions.FileExistsError,
                                              Exception)
    def output_loader_script_ui(self):
        """
        Outputs the Loader Script.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        LOGGER.debug("> Initializing Loader Script output.")

        selected_templates = self.__templates_outliner.get_selected_templates()
        if selected_templates and len(selected_templates) != 1:
            self.__engine.notifications_manager.warnify(
                "{0} | Multiple selected Templates, '{1}' will be used!".format(self.__class__.__name__,
                                                                                foundations.common.get_first_item(
                                                                                    selected_templates).name))

        template = foundations.common.get_first_item(selected_templates)

        if not template:
            raise foundations.exceptions.UserError(
                "{0} | In order to output the Loader Script, you need to select a Template!".format(
                    self.__class__.__name__))

        if not foundations.common.path_exists(template.path):
            raise foundations.exceptions.FileExistsError("{0} | '{1}' Template file doesn't exists!".format(
                self.__class__.__name__, template.name))

        selected_ibl_sets = self.__ibl_sets_outliner.get_selected_ibl_sets()
        if selected_ibl_sets and len(selected_ibl_sets) != 1:
            self.__engine.notifications_manager.warnify(
                "{0} | Multiple selected Ibl Sets, '{1}' will be used!".format(self.__class__.__name__,
                                                                               foundations.common.get_first_item(
                                                                                   selected_ibl_sets).name))

        ibl_set = foundations.common.get_first_item(selected_ibl_sets)
        if not ibl_set:
            raise foundations.exceptions.UserError(
                "{0} | In order to output the Loader Script, you need to select an Ibl Set!".format(
                    self.__class__.__name__))

        if not foundations.common.path_exists(ibl_set.path):
            raise foundations.exceptions.FileExistsError("{0} | '{1}' Ibl Set file doesn't exists!".format(
                self.__class__.__name__, ibl_set.title))

        if self.output_loader_script(template, ibl_set):
            self.__engine.notifications_manager.notify(
                "{0} | '{1}' output done!".format(self.__class__.__name__, template.output_script))
            return True
        else:
            raise Exception("{0} | Exception raised: '{1}' output failed!".format(self.__class__.__name__,
                                                                                  template.output_script))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def send_loader_script_to_software_ui(self):
        """
        Sends the Loader Script to associated 3d package.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        if not self.output_loader_script_ui():
            return False

        selected_templates = self.__templates_outliner.get_selected_templates()
        template = foundations.common.get_first_item(selected_templates)
        if not template:
            return False

        loader_script_path = foundations.strings.get_normalized_path(
            os.path.join(self.__io_directory, template.output_script))
        if self.Convert_To_Posix_Paths_checkBox.isChecked():
            loader_script_path = foundations.strings.to_posix_path(loader_script_path)
        if self.send_loader_script_to_software(template, loader_script_path):
            return True
        else:
            raise Exception("{0} | Exception raised while sending Loader Script!".format(self.__class__.__name__))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              foundations.exceptions.DirectoryExistsError)
    def output_loader_script(self, template, ibl_set):
        """
        Outputs the Loader Script.

        :param template: Template.
        :type template: Template
        :param ibl_set: Ibl Set.
        :type ibl_set: IblSet
        :return: Loader Script file.
        :rtype: unicode
        """

        self.__override_keys = self.get_default_override_keys()

        for component in self.__engine.components_manager.list_components():
            profile = self.__engine.components_manager.components[component]
            interface = self.__engine.components_manager.get_interface(component)
            if interface.activated and profile.name != self.name:
                hasattr(interface, "get_override_keys") and interface.get_override_keys()

        if self.__engine.parameters.loader_scripts_output_directory:
            if foundations.common.path_exists(self.__engine.parameters.loader_scripts_output_directory):
                loader_script = File(
                    os.path.join(self.__engine.parameters.loader_scripts_output_directory, template.output_script))
            else:
                raise foundations.exceptions.DirectoryExistsError(
                    "{0} | '{1}' loader Script output directory doesn't exists!".format(
                        self.__class__.__name__, self.__engine.parameters.loader_scripts_output_directory))
        else:
            loader_script = File(os.path.join(self.__io_directory, template.output_script))

        LOGGER.debug("> Loader Script output file path: '{0}'.".format(loader_script.path))

        loader_script.content = self.get_loader_script(template.path, ibl_set.path, self.__override_keys)

        if loader_script.content and loader_script.write():
            return loader_script.path

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              sibl_gui.exceptions.SocketConnectionError,
                                              sibl_gui.exceptions.Win32OLEServerConnectionError)
    def send_loader_script_to_software(self, template, loader_script_path):
        """
        Sends the Loader Script to associated 3d package.

        :param template: Template.
        :type template: Template
        :param loader_script_path: Loader Script path.
        :type loader_script_path: unicode
        :return: Method success.
        :rtype: bool
        """

        LOGGER.info("{0} | Starting remote connection!".format(self.__class__.__name__))
        template_sections_file_parser = foundations.parsers.SectionsFileParser(template.path)
        template_sections_file_parser.parse(raw_sections=(self.__template_script_section))
        connection_type = foundations.parsers.get_attribute_compound("ConnectionType",
                                                                     template_sections_file_parser.get_value(
                                                                         "ConnectionType",
                                                                         self.__template_remote_connection_section))

        if connection_type.value == "Socket":
            try:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.settimeout(2.5)
                connection.connect(
                    (foundations.strings.to_string(self.__tcp_client_ui.address), self.__tcp_client_ui.port))
                socket_command = foundations.parsers.get_attribute_compound("ExecutionCommand",
                                                                            template_sections_file_parser.get_value(
                                                                                "ExecutionCommand",
                                                                                self.__template_remote_connection_section)).value.replace(
                    "$loader_script_path",
                    loader_script_path)
                LOGGER.debug("> Current socket command: '%s'.", socket_command)
                connection.send(socket_command)
                self.__engine.notifications_manager.notify(
                    "{0} | Socket connection command dispatched!".format(self.__class__.__name__))
                dataBack = connection.recv(4096)
                LOGGER.debug("> Received from connection: '{0}'.".format(dataBack))
                connection.close()
                LOGGER.info("{0} | Closing remote connection!".format(self.__class__.__name__))
            except socket.timeout as error:
                LOGGER.info("{0} | Closing remote connection on timeout!".format(self.__class__.__name__))
            except Exception as error:
                raise sibl_gui.exceptions.SocketConnectionError(
                    "{0} | Socket connection error: '{1}'!".format(self.__class__.__name__,
                                                                   foundations.strings.to_string(error)))
        elif connection_type.value == "Win32":
            if platform.system() == "Windows" or platform.system() == "Microsoft":
                try:
                    import win32com.client

                    connection = win32com.client.Dispatch(
                        foundations.parsers.get_attribute_compound("TargetApplication",
                                                                   template_sections_file_parser.get_value(
                                                                       "TargetApplication",
                                                                       self.__template_remote_connection_section)).value)
                    connection._FlagAsMethod(self.__win32_execution_method)
                    connection_command = foundations.parsers.get_attribute_compound("ExecutionCommand",
                                                                                    template_sections_file_parser.get_value(
                                                                                        "ExecutionCommand",
                                                                                        self.__template_remote_connection_section)).value.replace(
                        "$loader_script_path",
                        loader_script_path)
                    LOGGER.debug("> Current connection command: '%s'.", connection_command)
                    getattr(connection, self.__win32_execution_method)(connection_command)
                    self.__engine.notifications_manager.notify(
                        "{0} | Win32 connection command dispatched!".format(self.__class__.__name__))
                except Exception as error:
                    raise sibl_gui.exceptions.Win32OLEServerConnectionError(
                        "{0} | Win32 OLE server connection error: '{1}'!".format(self.__class__.__name__,
                                                                                 foundations.strings.to_string(error)))
        return True

    def get_default_override_keys(self):
        """
        Gets default override keys.

        :return: Override keys.
        :rtype: dict
        """

        LOGGER.debug("> Constructing default override keys.")

        override_keys = {}

        selected_templates = self.__templates_outliner.get_selected_templates()
        template = foundations.common.get_first_item(selected_templates)

        if template:
            LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Template|Path", template.path))
            override_keys["Template|Path"] = foundations.parsers.get_attribute_compound("Template|Path", template.path)

        selected_ibl_sets = self.__ibl_sets_outliner.get_selected_ibl_sets()
        ibl_set = foundations.common.get_first_item(selected_ibl_sets)
        if ibl_set:
            LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Ibl Set|Path", ibl_set.path))
            override_keys["Ibl Set|Path"] = ibl_set.path and foundations.parsers.get_attribute_compound("Ibl Set|Path",
                                                                                                        foundations.strings.get_normalized_path(
                                                                                                            ibl_set.path))

            LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Background|BGfile",
                                                                                 ibl_set.background_image))
            override_keys[
                "Background|BGfile"] = ibl_set.background_image and foundations.parsers.get_attribute_compound(
                "Background|BGfile",
                foundations.strings.get_normalized_path(
                    ibl_set.background_image))

            LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Enviroment|EVfile",
                                                                                 ibl_set.lighting_image))
            override_keys["Enviroment|EVfile"] = ibl_set.lighting_image and foundations.parsers.get_attribute_compound(
                "Enviroment|EVfile",
                foundations.strings.get_normalized_path(
                    ibl_set.lighting_image))

            LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Reflection|REFfile",
                                                                                 ibl_set.reflection_image))
            override_keys[
                "Reflection|REFfile"] = ibl_set.reflection_image and foundations.parsers.get_attribute_compound(
                "Reflection|REFfile",
                foundations.strings.get_normalized_path(
                    ibl_set.reflection_image))
        return override_keys

    def get_loader_script(self, template, ibl_set, override_keys):
        """
        Builds a Loader Script.

        :param template: Template path.
        :type template: unicode
        :param ibl_set: Ibl Set path.
        :type ibl_set: unicode
        :param override_keys: Override keys.
        :type override_keys: dict
        :return: Loader Script.
        :rtype: list
        """

        LOGGER.debug("> Parsing Template file: '{0}'.".format(template))
        template_sections_file_parser = foundations.parsers.SectionsFileParser(template)
        template_sections_file_parser.parse(raw_sections=(self.__template_script_section))
        template_sections = dict.copy(template_sections_file_parser.sections)

        for attribute, value in dict.copy(template_sections[self.__template_ibl_set_attributes_section]).iteritems():
            template_sections[self.__template_ibl_set_attributes_section][
                foundations.namespace.remove_namespace(attribute,
                                                       root_only=True)] = value
            del template_sections[self.__template_ibl_set_attributes_section][attribute]

        LOGGER.debug("> Binding Templates file attributes.")
        bound_attributes = dict(((attribute, foundations.parsers.get_attribute_compound(attribute, value))
                                 for section in template_sections if section not in (self.__template_script_section)
                                 for attribute, value in template_sections[section].iteritems()))

        LOGGER.debug("> Parsing Ibl Set file: '{0}'.".format(ibl_set))
        ibl_set_sections_file_parser = foundations.parsers.SectionsFileParser(ibl_set)
        ibl_set_sections_file_parser.parse()
        ibl_set_sections = dict.copy(ibl_set_sections_file_parser.sections)

        LOGGER.debug("> Flattening Ibl Set file attributes.")
        flattened_ibl_attributes = dict(((attribute, foundations.parsers.get_attribute_compound(attribute, value))
                                         for section in ibl_set_sections
                                         for attribute, value in ibl_set_sections[section].iteritems()))

        for attribute in flattened_ibl_attributes:
            if attribute in bound_attributes:
                bound_attributes[attribute].value = flattened_ibl_attributes[attribute].value

        if "Lights|DynamicLights" in bound_attributes:
            LOGGER.debug("> Building '{0}' custom attribute.".format("Lights|DynamicLights"))
            dynamic_lights = []
            for section in ibl_set_sections:
                if re.search(r"Light\d+", section):
                    dynamic_lights.append(section)
                    lightName = ibl_set_sections_file_parser.get_value("LIGHTname", section)
                    dynamic_lights.append(lightName and lightName or self.__unnamed_light_name)
                    lightColorTokens = ibl_set_sections_file_parser.get_value("LIGHTcolor", section).split(",")
                    for color in lightColorTokens:
                        dynamic_lights.append(color)
                    dynamic_lights.append(ibl_set_sections_file_parser.get_value("LIGHTmulti", section))
                    dynamic_lights.append(ibl_set_sections_file_parser.get_value("LIGHTu", section))
                    dynamic_lights.append(ibl_set_sections_file_parser.get_value("LIGHTv", section))

            LOGGER.debug("> Adding '{0}' custom attribute with value: '{1}'.".format("Lights|DynamicLights",
                                                                                     ", ".join(dynamic_lights)))
            bound_attributes["Lights|DynamicLights"].value = self.__default_string_separator.join(dynamic_lights)

        LOGGER.debug("> Updating attributes with override keys.")
        for attribute in override_keys:
            if attribute in bound_attributes:
                bound_attributes[attribute].value = override_keys[attribute] and override_keys[attribute].value or None

        LOGGER.debug("> Updating Loader Script content.")
        loader_script = template_sections_file_parser.sections[
            self.__template_script_section][template_sections_file_parser.raw_section_content_identifier]

        bound_loader_script = []
        for line in loader_script:
            binding_parameters = re.findall(r"{0}".format(self.__binding_identifier_pattern), line)
            if binding_parameters:
                for parameter in binding_parameters:
                    for attribute in bound_attributes.itervalues():
                        if not parameter == attribute.link:
                            continue

                        LOGGER.debug("> Updating Loader Script parameter '{0}' with value: '{1}'.".format(parameter,
                                                                                                          attribute.value))
                        line = line.replace(parameter, attribute.value if attribute.value else "-1")
            bound_loader_script.append(line)
        return bound_loader_script
