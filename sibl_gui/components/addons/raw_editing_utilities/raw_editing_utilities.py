#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**raw_editing_utilities.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`RawEditingUtilities` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform
import re
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QGridLayout

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.engine
import umbra.exceptions
import umbra.ui.common
from manager.QWidget_component import QWidgetComponentFactory
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "RawEditingUtilities"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Raw_Editing_Utilities.ui")

class RawEditingUtilities(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`sibl_gui.components.addons.raw_editing_utilities.raw_editing_utilities` Component Interface class.
    | It provides methods to edit Application related text files.
    | By default the Component will use the **factory.script_editor** Component	but the user can define a custom file editor
        through options exposed in the :mod:`sibl_gui.components.core.preferences_manager.preferences_manager` Component ui.
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

        super(RawEditingUtilities, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = True

        self.__engine = None
        self.__settings = None
        self.__settings_section = None

        self.__script_editor = None
        self.__preferences_manager = None
        self.__components_manager_ui = None
        self.__ibl_sets_outliner = None
        self.__inspector = None
        self.__templates_outliner = None

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
    def inspector(self):
        """
        Property for **self.__inspector** attribute.

        :return: self.__inspector.
        :rtype: QWidget
        """

        return self.__inspector

    @inspector.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def inspector(self, value):
        """
        Setter for **self.__inspector** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspector"))

    @inspector.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def inspector(self):
        """
        Deleter for **self.__inspector** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspector"))

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
        self.__settings = self.__engine.settings
        self.__settings_section = self.name

        self.__script_editor = self.__engine.components_manager["factory.script_editor"]
        self.__preferences_manager = self.__engine.components_manager["factory.preferences_manager"]
        self.__components_manager_ui = self.__engine.components_manager["factory.components_manager_ui"]
        self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]
        self.__inspector = self.__engine.components_manager["core.inspector"]
        self.__templates_outliner = self.__engine.components_manager["core.templates_outliner"]

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

        self.__script_editor = None
        self.__preferences_manager = None
        self.__components_manager_ui = None
        self.__ibl_sets_outliner = None
        self.__inspector = None
        self.__templates_outliner = None

        self.activated = False
        return True

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        self.__Custom_Text_Editor_Path_lineEdit_set_ui()
        self.__add_actions()

        # Signals / Slots.
        self.Custom_Text_Editor_Path_toolButton.clicked.connect(self.__Custom_Text_Editor_Path_toolButton__clicked)
        self.Custom_Text_Editor_Path_lineEdit.editingFinished.connect(
        self.__Custom_Text_Editor_Path_lineEdit__editFinished)
        self.__engine.content_dropped.connect(self.__engine__content_dropped)
        self.__script_editor.Script_Editor_tabWidget.content_dropped.connect(
        self.__script_editor_Script_Editor_tabWidget__content_dropped)

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
        self.Custom_Text_Editor_Path_toolButton.clicked.disconnect(self.__Custom_Text_Editor_Path_toolButton__clicked)
        self.Custom_Text_Editor_Path_lineEdit.editingFinished.disconnect(
        self.__Custom_Text_Editor_Path_lineEdit__editFinished)
        self.__engine.content_dropped.disconnect(self.__engine__content_dropped)
        self.__script_editor.Script_Editor_tabWidget.content_dropped.disconnect(
        self.__script_editor_Script_Editor_tabWidget__content_dropped)

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

        self.__preferences_manager.Others_Preferences_gridLayout.addWidget(self.Custom_Text_Editor_Path_groupBox)

        return True

    def remove_widget(self):
        """
        Removes the Component Widget from the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

        self.__preferences_manager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
        self.Custom_Text_Editor_Path_groupBox.setParent(None)

        return True

    def __add_actions(self):
        """
        Sets Component actions.
        """

        LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

        if not self.__engine.parameters.database_read_only:
            edit_ibl_sets_files_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|Edit Ibl Set(s) File(s) ...",
            slot=self.__ibl_sets_outliner_views_edit_ibl_sets_files_action__triggered)
            for view in self.__ibl_sets_outliner.views:
                view.addAction(edit_ibl_sets_files_action)

            self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.inspector|Edit Ibl Set File ...",
            slot=self.__inspector_edit_active_ibl_set_file_action__triggered))
            self.__templates_outliner.view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.templates_outliner|Edit Template(s) File(s) ...",
            slot=self.__templates_outliner_view_edit_templates_files_action__triggered))
        else:
            LOGGER.info("{0} | Text editing capabilities deactivated by '{1}' command line parameter value!".format(
            self.__class__.__name__, "database_read_only"))

        separator_action = QAction(self.__components_manager_ui.view)
        separator_action.setSeparator(True)
        self.__components_manager_ui.view.addAction(separator_action)

        self.__components_manager_ui.view.addAction(self.__engine.actions_manager.register_action(
        "Actions|Umbra|Components|factory.components_manager_ui|Edit Component(s) ...",
        slot=self.__components_manager_ui_view_edit_components_action__triggered))

    def __remove_actions(self):
        """
        Removes actions.
        """

        LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

        if not self.__engine.parameters.database_read_only:
            edit_ibl_sets_files_action = "Actions|Umbra|Components|core.ibl_sets_outliner|Edit Ibl Set(s) File(s) ..."
            for view in self.__ibl_sets_outliner.views:
                view.removeAction(self.__engine.actions_manager.get_action(edit_ibl_sets_files_action))
            self.__engine.actions_manager.unregister_action(edit_ibl_sets_files_action)
            edit_active_ibl_set_file_action = "Actions|Umbra|Components|core.inspector|Edit Ibl Set File ..."
            self.__inspector.Inspector_Overall_frame.removeAction(
            self.__engine.actions_manager.get_action(edit_active_ibl_set_file_action))
            self.__engine.actions_manager.unregister_action(edit_active_ibl_set_file_action)
            edit_templates_files_action = "Actions|Umbra|Components|core.templates_outliner|Edit Template(s) File(s) ..."
            self.__templates_outliner.view.removeAction(
            self.__engine.actions_manager.get_action(edit_templates_files_action))
            self.__engine.actions_manager.unregister_action(edit_templates_files_action)
        edit_components_action = "Actions|Umbra|Components|factory.components_manager_ui|Edit Component(s) ..."
        self.__components_manager_ui.view.removeAction(
        self.__engine.actions_manager.get_action(edit_components_action))
        self.__engine.actions_manager.unregister_action(edit_components_action)

    def __ibl_sets_outliner_views_edit_ibl_sets_files_action__triggered(self, checked):
        """
        Defines the slot triggered by
        **'Actions|Umbra|Components|core.ibl_sets_outliner|Edit Ibl Set(s) File(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.edit_ibl_sets_files_ui()

    def __inspector_edit_active_ibl_set_file_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.inspector|Edit Ibl Set File ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.edit_active_ibl_set_file_ui()

    def __templates_outliner_view_edit_templates_files_action__triggered(self, checked):
        """
        Defines the slot triggered by
        **'Actions|Umbra|Components|core.templates_outliner|Edit Template(s) File(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.edit_templates_files_ui()

    def __components_manager_ui_view_edit_components_action__triggered(self, checked):
        """
        Defines the slot triggered by
        **'Actions|Umbra|Components|factory.components_manager_ui|Edit Component(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.edit_components_ui()

    def __Custom_Text_Editor_Path_lineEdit_set_ui(self):
        """
        Fills **Custom_Text_Editor_Path_lineEdit** Widget.
        """

        custom_text_editor = self.__settings.get_key(self.__settings_section, "custom_text_editor")
        LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Custom_Text_Editor_Path_lineEdit",
                                                                custom_text_editor.toString()))
        self.Custom_Text_Editor_Path_lineEdit.setText(custom_text_editor.toString())

    def __Custom_Text_Editor_Path_toolButton__clicked(self, checked):
        """
        Defines the slot triggered by **Custom_Text_Editor_Path_toolButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        custom_text_editor_executable = umbra.ui.common.store_last_browsed_path(
        QFileDialog.getOpenFileName(self, "Custom Text Editor Executable:", RuntimeGlobals.last_browsed_path))
        if custom_text_editor_executable != "":
            LOGGER.debug("> Chosen custom text editor executable: '{0}'.".format(custom_text_editor_executable))
            self.Custom_Text_Editor_Path_lineEdit.setText(QString(custom_text_editor_executable))
            self.__settings.set_key(self.__settings_section,
                                    "custom_text_editor",
                                    self.Custom_Text_Editor_Path_lineEdit.text())

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                            foundations.exceptions.UserError)
    def __Custom_Text_Editor_Path_lineEdit__editFinished(self):
        """
        Defines the slot triggered by **Custom_Text_Editor_Path_lineEdit** Widget
        when edited and check that entered path is valid.
        """

        value = foundations.strings.to_string(self.Custom_Text_Editor_Path_lineEdit.text())
        if not foundations.common.path_exists(os.path.abspath(value)) and value != "":
            LOGGER.debug("> Restoring preferences!")
            self.__Custom_Text_Editor_Path_lineEdit_set_ui()

            raise foundations.exceptions.UserError("{0} | Invalid custom text editor executable file!".format(
            self.__class__.__name__))
        else:
            self.__settings.set_key(self.__settings_section,
                                    "custom_text_editor",
                                    self.Custom_Text_Editor_Path_lineEdit.text())

    @umbra.engine.encapsulate_processing
    def __engine__content_dropped(self, event):
        """
        Defines the slot triggered by content when dropped into the engine.

        :param event: Event.
        :type event: QEvent
        """

        if not event.mimeData().hasUrls():
            return

        urls = event.mimeData().urls()

        LOGGER.debug("> Drag event urls list: '{0}'!".format(urls))

        self.__engine.start_processing("Loading Files ...", len(urls))
        for url in event.mimeData().urls():
            path = foundations.strings.to_string(url.path())
            LOGGER.debug("> Handling dropped '{0}' file.".format(path))
            path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
            re.search(r"^\/[A-Z]:", path) and path[1:] or path
            if not re.search(r"\.{0}$".format(self.__ibl_sets_outliner.extension), path) and \
            not re.search(r"\.{0}$".format(self.templates_outliner.extension), path) and not os.path.isdir(path):
                self.edit_path(path, self.Custom_Text_Editor_Path_lineEdit.text())
            self.__engine.step_processing()
        self.__engine.stop_processing()

    def __script_editor_Script_Editor_tabWidget__content_dropped(self, event):
        """
        Defines the slot triggered by content when dropped into the **script_editor.Script_Editor_tabWidget** Widget.

        :param event: Event.
        :type event: QEvent
        """

        if event.source() in self.__ibl_sets_outliner.views:
            self.edit_ibl_sets_files_ui()
        elif event.source() is self.__templates_outliner.view:
            self.edit_templates_files_ui()

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def edit_ibl_sets_files_ui(self):
        """
        Edits selected Ibl Sets files.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_ibl_sets = self.__ibl_sets_outliner.get_selected_ibl_sets()

        success = True
        for ibl_set in selected_ibl_sets:
            path = ibl_set.path and foundations.common.path_exists(ibl_set.path) and ibl_set.path
            if path:
                success *= self.edit_path(path, self.Custom_Text_Editor_Path_lineEdit.text()) or False
            else:
                LOGGER.warning("!> {0} | '{1}' Ibl Set file doesn't exists and will be skipped!".format(
                self.__class__.__name__, ibl_set.title))

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while editing '{1}' Ibl Sets!".format(self.__class__.__name__,
                                                                ", ".join(ibl_set.title for ibl_set in selected_ibl_sets)))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                            foundations.exceptions.FileExistsError)
    def edit_active_ibl_set_file_ui(self):
        """
        Edits :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set file.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        active_ibl_set = self.__inspector.active_ibl_set
        if active_ibl_set is None:
            return False

        if foundations.common.path_exists(active_ibl_set.path):
            return self.edit_path(active_ibl_set.path, foundations.strings.to_string(self.Custom_Text_Editor_Path_lineEdit.text()))
        else:
            raise foundations.exceptions.FileExistsError(
            "{0} | Exception raised while editing Inspector Ibl Set: '{1}' Ibl Set file doesn't exists!".format(
            self.__class__.__name__, active_ibl_set.title))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def edit_templates_files_ui(self):
        """
        Edits selected Templates files.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_templates = self.__templates_outliner.get_selected_templates()

        success = True
        for template in selected_templates:
            path = template.path and foundations.common.path_exists(template.path) and template.path
            if path:
                success *= self.edit_path(path, self.Custom_Text_Editor_Path_lineEdit.text()) or False
            else:
                LOGGER.warning("!> {0} | '{1}' Template file doesn't exists and will be skipped!".format(
                self.__class__.__name__, template.name))

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while editing '{1}' templates!".format(self.__class__.__name__,
                                                            ", ".join(template.name for template in selected_templates)))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def edit_components_ui(self):
        """
        Edits selected Components packages.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_components = self.__components_manager_ui.get_selected_components()

        success = True
        for component in selected_components:
            path = component.directory and foundations.common.path_exists(component.directory) and component.directory
            if path:
                success *= self.edit_path(path, self.Custom_Text_Editor_Path_lineEdit.text()) or False
            else:
                LOGGER.warning("!> {0} | '{1}' Component path doesn't exists and will be skipped!".format(
                self.__class__.__name__, component.name))

        if success:
            return True
        else:
            raise Exception("{0} | Exception raised while editing '{1}' Components!".format(self.__class__.__name__,
                                                            ", ".join(component.name for component in selected_components)))

    def get_process_command(self, path, custom_text_editor):
        """
        Gets process command.

        :param path: Path to edit.
        :type path: unicode
        :param custom_text_editor: Custom text editor.
        :type custom_text_editor: unicode
        :return: Process command.
        :rtype: unicode
        """

        process_command = None
        path = os.path.normpath(path)
        if platform.system() == "Windows" or platform.system() == "Microsoft":
            process_command = "\"{0}\" \"{1}\"".format(custom_text_editor, path)
        elif platform.system() == "Darwin":
            process_command = "open -a \"{0}\" \"{1}\"".format(custom_text_editor, path)
        elif platform.system() == "Linux":
            process_command = "\"{0}\" \"{1}\"".format(custom_text_editor, path)
        return process_command

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def edit_path(self, path, custom_text_editor=None):
        """
        Provides editing capability.

        :param path: Path to edit.
        :type path: unicode
        :param custom_text_editor: Custom text editor.
        :type custom_text_editor: unicode
        :return: Method success.
        :rtype: bool
        """

        if custom_text_editor:
            edit_command = self.get_process_command(path, custom_text_editor)
            if edit_command:
                LOGGER.debug("> Current edit command: '{0}'.".format(edit_command))
                LOGGER.info("{0} | Launching text editor with '{1}' path.".format(self.__class__.__name__, path))
                edit_process = QProcess()
                edit_process.startDetached(edit_command)
                return True
            else:
                raise Exception("{0} | Exception raised: No suitable process command given!".format(
                self.__class__.__name__))
        else:
            self.__script_editor.load_path(path) and self.__script_editor.restore_development_layout()
            return True
