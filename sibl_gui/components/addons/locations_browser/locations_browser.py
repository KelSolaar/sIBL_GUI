#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**locations_browser.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`LocationsBrowser` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QPushButton

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.common
from foundations.environment import Environment
from manager.QWidget_component import QWidgetComponentFactory
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "LocationsBrowser"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Locations_Browser.ui")


class LocationsBrowser(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`sibl_gui.components.addons.locations_browser.locations_browser` Component Interface class.
    | It provides methods to explore operating system directories.
    | By default the Component will use current operating system file browsers but
        the user can define a custom file browser through options exposed
        in the :mod:`sibl_gui.components.core.preferences_manager.preferences_manager` Component ui.

    Defaults file browsers:

        - Windows:

            - Explorer

        - Mac Os X:

            - Finder

        - Linux:

            - Nautilus
            - Dolphin
            - Konqueror
            - Thunar
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

        super(LocationsBrowser, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = True

        self.__engine = None
        self.__settings = None
        self.__settings_section = None

        self.__components_manager_ui = None
        self.__preferences_manager = None
        self.__ibl_sets_outliner = None
        self.__inspector = None
        self.__templates_outliner = None
        self.__loader_script = None

        self.__Open_Output_Directory_pushButton = None

        self.__linux_browsers = ("nautilus", "dolphin", "konqueror", "thunar")

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
    def components_manager_ui(self):
        """
        Property for **self.__components_manager_ui** attribute.

        :return: self.__components_manager_ui.
        :rtype: QWidget
        """

        return self.__components_manager_ui

    @components_manager_ui.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_manager_ui(self, value):
        """
        Setter for **self.__components_manager_ui** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "components_manager_ui"))

    @components_manager_ui.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_manager_ui(self):
        """
        Deleter for **self.__components_manager_ui** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "components_manager_ui"))

    @property
    def preferences_manager(self):
        """
        Property for **self.__preferences_manager** attribute.

        :return: self.__preferences_manager.
        :rtype: QWidget
        """

        return self.__preferences_manager

    @preferences_manager.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def preferences_manager(self, value):
        """
        Setter for **self.__preferences_manager** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "preferences_manager"))

    @preferences_manager.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def preferences_manager(self):
        """
        Deleter for **self.__preferences_manager** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preferences_manager"))

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
    def loader_script(self):
        """
        Property for **self.__loader_script** attribute.

        :return: self.__loader_script.
        :rtype: QWidget
        """

        return self.__loader_script

    @loader_script.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def loader_script(self, value):
        """
        Setter for **self.__loader_script** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loader_script"))

    @loader_script.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def loader_script(self):
        """
        Deleter for **self.__loader_script** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loader_script"))

    @property
    def Open_Output_Directory_pushButton(self):
        """
        Property for **self.__Open_Output_Directory_pushButton** attribute.

        :return: self.__Open_Output_Directory_pushButton.
        :rtype: QPushButton
        """

        return self.__Open_Output_Directory_pushButton

    @Open_Output_Directory_pushButton.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def Open_Output_Directory_pushButton(self, value):
        """
        Setter for **self.__Open_Output_Directory_pushButton** attribute.

        :param value: Attribute value.
        :type value: QPushButton
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "Open_Output_Directory_pushButton"))

    @Open_Output_Directory_pushButton.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def Open_Output_Directory_pushButton(self):
        """
        Deleter for **self.__Open_Output_Directory_pushButton** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__,
                                                             "Open_Output_Directory_pushButton"))

    @property
    def linux_browsers(self):
        """
        Property for **self.__linux_browsers** attribute.

        :return: self.__linux_browsers.
        :rtype: QObject
        """

        return self.__linux_browsers

    @linux_browsers.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def linux_browsers(self, value):
        """
        Setter for **self.__linux_browsers** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "linux_browsers"))

    @linux_browsers.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def linux_browsers(self):
        """
        Deleter for **self.__linux_browsers** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "linux_browsers"))

    def activate(self, engine):
        """
        Activates the Component.

        :param engine: Container to attach the Component to.
        :type engine: QObject
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

        self.__engine = engine
        self.__settings = self.__engine.settings
        self.__settings_section = self.name

        self.__components_manager_ui = self.__engine.components_manager["factory.components_manager_ui"]
        self.__preferences_manager = self.__engine.components_manager["factory.preferences_manager"]
        self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]
        self.__inspector = self.__engine.components_manager["core.inspector"]
        self.__templates_outliner = self.__engine.components_manager["core.templates_outliner"]
        self.__loader_script = self.__engine.components_manager["addons.loader_script"]

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
        self.__settings = None
        self.__settings_section = None

        self.__components_manager_ui = None
        self.__preferences_manager = None
        self.__ibl_sets_outliner = None
        self.__inspector = None
        self.__templates_outliner = None
        self.__loader_script = None

        self.activated = False
        return True

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        self.__Custom_File_Browser_Path_lineEdit_set_ui()

        self.__add_actions()

        # Signals / Slots.
        self.Custom_File_Browser_Path_toolButton.clicked.connect(self.__Custom_File_Browser_Path_toolButton__clicked)
        self.Custom_File_Browser_Path_lineEdit.editingFinished.connect(
            self.__Custom_File_Browser_Path_lineEdit__editFinished)

        # LoaderScript addon component specific code.
        if self.__loader_script.activated:
            self.__Open_Output_Directory_pushButton = QPushButton("Open Output Directory ...")
            self.__loader_script.Loader_Script_verticalLayout.addWidget(self.__Open_Output_Directory_pushButton)

            # Signals / Slots.
            self.__Open_Output_Directory_pushButton.clicked.connect(self.__Open_Output_Directory_pushButton__clicked)

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
        self.Custom_File_Browser_Path_toolButton.clicked.disconnect(
            self.__Custom_File_Browser_Path_toolButton__clicked)
        self.Custom_File_Browser_Path_lineEdit.editingFinished.disconnect(
            self.__Custom_File_Browser_Path_lineEdit__editFinished)

        # LoaderScript addon component specific code.
        if self.__loader_script.activated:
            # Signals / Slots.
            self.__Open_Output_Directory_pushButton.clicked.disconnect(
                self.__Open_Output_Directory_pushButton__clicked)

            self.__Open_Output_Directory_pushButton.setParent(None)
            self.__Open_Output_Directory_pushButton = None

        self.__remove_actions()

        self.initialized_ui = False
        return True

    def add_widget(self):
        """
        Adds the Component Widget to the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

        self.__preferences_manager.Others_Preferences_gridLayout.addWidget(self.Custom_File_Browser_Path_groupBox)

        return True

    def remove_widget(self):
        """
        Removes the Component Widget from the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

        self.Custom_File_Browser_Path_groupBox.setParent(None)

        return True

    def __add_actions(self):
        """
        Sets Component actions.
        """

        LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

        open_ibl_sets_locations_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|Open Ibl Set(s) Location(s) ...",
            slot=self.__ibl_sets_outliner_views_open_ibl_sets_locations_action__triggered)
        for view in self.__ibl_sets_outliner.views:
            view.addAction(open_ibl_sets_locations_action)

        self.__inspector.Inspector_Overall_frame.addAction(
            self.__engine.actions_manager.register_action(
                "Actions|Umbra|Components|core.inspector|Open Ibl Set location ...",
                slot=self.__inspector_open_active_ibl_set_location_action__triggered))
        self.__components_manager_ui.view.addAction(
            self.__engine.actions_manager.register_action(
                "Actions|Umbra|Components|factory.ComponentsManagerUi|Open Component(s) Location(s) ...",
                slot=self.__components_manager_ui_view_open_components_locations_action__triggered))
        self.__templates_outliner.view.addAction(
            self.__engine.actions_manager.register_action(
                "Actions|Umbra|Components|core.templates_outliner|Open Template(s) Location(s) ...",
                slot=self.__templates_outliner_view_open_templates_locations_action__triggered))

    def __remove_actions(self):
        """
        Removes actions.
        """

        LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

        open_ibl_sets_locations_action = "Actions|Umbra|Components|core.ibl_sets_outliner|Open Ibl Set(s) Location(s) ..."
        for view in self.__ibl_sets_outliner.views:
            view.removeAction(self.__engine.actions_manager.get_action(open_ibl_sets_locations_action))
        self.__engine.actions_manager.unregister_action(open_ibl_sets_locations_action)
        open_active_ibl_set_location_action = "Actions|Umbra|Components|core.inspector|Open Ibl Set location ..."
        self.__inspector.Inspector_Overall_frame.removeAction(
            self.__engine.actions_manager.get_action(open_active_ibl_set_location_action))
        self.__engine.actions_manager.unregister_action(open_active_ibl_set_location_action)
        open_components_locations_action = \
            "Actions|Umbra|Components|factory.ComponentsManagerUi|Open Component(s) Location(s) ..."
        self.__components_manager_ui.view.removeAction(
            self.__engine.actions_manager.get_action(open_components_locations_action))
        self.__engine.actions_manager.unregister_action(open_components_locations_action)
        open_templates_locations_action = \
            "Actions|Umbra|Components|core.templates_outliner|Open Template(s) Location(s) ..."
        self.__templates_outliner.view.removeAction(
            self.__engine.actions_manager.get_action(open_templates_locations_action))
        self.__engine.actions_manager.unregister_action(open_templates_locations_action)

    def __ibl_sets_outliner_views_open_ibl_sets_locations_action__triggered(self, checked):
        """
        Defines the slot triggered by
        **'Actions|Umbra|Components|core.ibl_sets_outliner|Open Ibl Set(s) Location(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.open_ibl_sets_locations_ui()

    def __inspector_open_active_ibl_set_location_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.inspector|Open Ibl Set location ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.open_active_ibl_set_location_ui()

    def __components_manager_ui_view_open_components_locations_action__triggered(self, checked):
        """
        Defines the slot triggered by
        **'Actions|Umbra|Components|factory.ComponentsManagerUi|Open Component(s) Location(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.open_components_locations_ui()

    def __templates_outliner_view_open_templates_locations_action__triggered(self, checked):
        """
        Defines the slot triggered by
        **'Actions|Umbra|Components|core.templates_outliner|Open Template(s) Location(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.open_templates_locations_ui()

    def __Custom_File_Browser_Path_lineEdit_set_ui(self):
        """
        Fills **Custom_File_Browser_Path_lineEdit** Widget.
        """

        custom_file_browser = self.__settings.get_key(self.__settings_section, "custom_file_browser")
        LOGGER.debug("> Setting '{0}' with value '{1}'.".format(
            "Custom_File_Browser_Path_lineEdit", custom_file_browser.toString()))
        self.Custom_File_Browser_Path_lineEdit.setText(custom_file_browser.toString())

    def __Custom_File_Browser_Path_toolButton__clicked(self, checked):
        """
        Defines the slot triggered by **Custom_File_Browser_Path_toolButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        custom_file_browser_executable = umbra.ui.common.store_last_browsed_path(
            QFileDialog.getOpenFileName(self, "Custom File Browser Executable:", RuntimeGlobals.last_browsed_path))
        if custom_file_browser_executable != "":
            LOGGER.debug("> Chosen custom file browser executable: '{0}'.".format(custom_file_browser_executable))
            self.Custom_File_Browser_Path_lineEdit.setText(QString(custom_file_browser_executable))
            self.__settings.set_key(self.__settings_section,
                                    "custom_file_browser",
                                    self.Custom_File_Browser_Path_lineEdit.text())

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              foundations.exceptions.UserError)
    def __Custom_File_Browser_Path_lineEdit__editFinished(self):
        """
        Defines the slot triggered by **Custom_File_Browser_Path_lineEdit** Widget
        when edited and check that entered path is valid.
        """

        value = foundations.strings.to_string(self.Custom_File_Browser_Path_lineEdit.text())
        if not foundations.common.path_exists(os.path.abspath(value)) and value != "":
            LOGGER.debug("> Restoring preferences!")
            self.__Custom_File_Browser_Path_lineEdit_set_ui()

            raise foundations.exceptions.UserError(
                "{0} | Invalid custom file browser executable file!".format(self.__class__.__name__))
        else:
            self.__settings.set_key(self.__settings_section,
                                    "custom_file_browser",
                                    self.Custom_File_Browser_Path_lineEdit.text())

    def __Open_Output_Directory_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Open_Output_Directory_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.open_output_directory_ui()

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def open_ibl_sets_locations_ui(self):
        """
        Open selected Ibl Sets directories.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_ibl_sets = self.__ibl_sets_outliner.get_selected_ibl_sets()

        success = True
        for ibl_set in selected_ibl_sets:
            path = ibl_set.path and foundations.common.path_exists(ibl_set.path) and os.path.dirname(ibl_set.path)
            if path:
                success *= self.explore_directory(path,
                                                  foundations.strings.to_string(
                                                      self.Custom_File_Browser_Path_lineEdit.text())) or False
            else:
                LOGGER.warning("!> {0} | '{1}' Ibl Set file doesn't exists and will be skipped!".format(
                    self.__class__.__name__, ibl_set.title))

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while opening '{1}' Ibl Sets directories!".format(
                self.__class__.__name__, ", ".join(ibl_set.title for ibl_set in selected_ibl_sets)))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              foundations.exceptions.FileExistsError)
    def open_active_ibl_set_location_ui(self):
        """
        Opens :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set directory.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        active_ibl_set = self.__inspector.active_ibl_set
        if active_ibl_set is None:
            return False

        if foundations.common.path_exists(active_ibl_set.path):
            return self.explore_directory(os.path.dirname(active_ibl_set.path),
                                          foundations.strings.to_string(self.Custom_File_Browser_Path_lineEdit.text()))
        else:
            raise foundations.exceptions.FileExistsError(
                "{0} | Exception raised while opening Inspector Ibl Set directory: '{1}' Ibl Set file doesn't exists!".format(
                    self.__class__.__name__, active_ibl_set.title))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def open_components_locations_ui(self):
        """
        Opens selected Components directories.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_components = self.__components_manager_ui.get_selected_components()

        success = True
        for component in selected_components:
            path = component.directory and foundations.common.path_exists(component.directory) and component.directory
            if path:
                success *= self.explore_directory(path,
                                                  foundations.strings.to_string(
                                                      self.Custom_File_Browser_Path_lineEdit.text())) or False
            else:
                LOGGER.warning("!> {0} | '{1}' Component file doesn't exists and will be skipped!".format(
                    self.__class__.__name__, component.name))

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while opening '{1}' Components directories!".format(
                self.__class__.__name__, ", ".join(component.name for component in selected_components)))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def open_templates_locations_ui(self):
        """
        Opens selected Templates directories.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_templates = self.__templates_outliner.get_selected_templates()

        success = True
        for template in selected_templates:
            path = template.path and foundations.common.path_exists(template.path) and os.path.dirname(template.path)
            if path:
                success *= self.explore_directory(path,
                                                  foundations.strings.to_string(
                                                      self.Custom_File_Browser_Path_lineEdit.text())) or False
            else:
                LOGGER.warning("!> {0} | '{1}' Template file doesn't exists and will be skipped!".format(
                    self.__class__.__name__, template.name))

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while opening '{1}' Templates directories!".format(
                self.__class__.__name__, ", ".join(template.name for template in selected_templates)))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              foundations.exceptions.DirectoryExistsError,
                                              Exception)
    def open_output_directory_ui(self):
        """
        Opens output directory.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        directory = self.__engine.parameters.loader_scripts_output_directory and \
                    self.__engine.parameters.loader_scripts_output_directory or self.__loader_script.io_directory

        if not foundations.common.path_exists(directory):
            raise foundations.exceptions.DirectoryExistsError(
                "{0} | '{1}' loader Script output directory doesn't exists!".format(self.__class__.__name__, directory))

        if self.explore_directory(directory,
                                  foundations.strings.to_string(self.Custom_File_Browser_Path_lineEdit.text())):
            return True
        else:
            raise Exception("{0} | Exception raised while exploring '{1}' directory!".format(
                self.__class__.__name__, directory))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def get_process_command(self, directory, custom_browser=None):
        """
        Gets process command.

        :param directory: Directory to explore.
        :type directory: unicode
        :param custom_browser: Custom browser.
        :type custom_browser: unicode
        :return: Process command.
        :rtype: unicode
        """

        process_command = None
        directory = os.path.normpath(directory)
        if platform.system() == "Windows" or platform.system() == "Microsoft":
            if custom_browser:
                process_command = "\"{0}\" \"{1}\"".format(custom_browser, directory)
            else:
                process_command = "explorer.exe \"{0}\"".format(directory)
        elif platform.system() == "Darwin":
            if custom_browser:
                process_command = "open -a \"{0}\" \"{1}\"".format(custom_browser, directory)
            else:
                process_command = "open \"{0}\"".format(directory)
        elif platform.system() == "Linux":
            if custom_browser:
                process_command = "\"{0}\" \"{1}\"".format(custom_browser, directory)
            else:
                environment_variable = Environment("PATH")
                paths = environment_variable.get_value().split(":")

                browser_found = False
                for browser in self.__linux_browsers:
                    if browser_found:
                        break

                    try:
                        for path in paths:
                            if foundations.common.path_exists(os.path.join(path, browser)):
                                process_command = "\"{0}\" \"{1}\"".format(browser, directory)
                                browser_found = True
                                raise StopIteration
                    except StopIteration:
                        pass

                if not browser_found:
                    raise Exception("{0} | Exception raised: No suitable Linux browser found!".format(
                        self.__class__.__name__))
        return process_command

    def explore_directory(self, directory, custom_browser=None):
        """
        Provides directory exploring capability.

        :param directory: Directory to explore.
        :type directory: unicode
        :param custom_browser: Custom browser.
        :type custom_browser: unicode
        :return: Method success.
        :rtype: bool
        """

        browser_command = self.get_process_command(directory, custom_browser)
        if browser_command:
            LOGGER.debug("> Current browser command: '{0}'.".format(browser_command))
            LOGGER.info("{0} | Launching file browser with '{1}' directory.".format(
                self.__class__.__name__, directory))
            browser_process = QProcess()
            browser_process.startDetached(browser_command)
            return True
        else:
            raise Exception(
                "{0} | Exception raised: No suitable process command given!".format(self.__class__.__name__))
