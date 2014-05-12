#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preview.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`Preview` Component Interface class, the :class:`ImagesPreviewer` class and
    others images preview related objects.

**Others:**

"""

from __future__ import unicode_literals

import functools
import os
import platform
import re
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QPushButton

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.engine
import umbra.exceptions
import umbra.ui.common
from foundations.parsers import SectionsFileParser
from manager.QWidget_component import QWidgetComponentFactory
from sibl_gui.components.addons.preview.images_previewer import ImagesPreviewer
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Preview"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Preview.ui")


class Preview(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`sibl_gui.components.addons.preview.preview` Component Interface class.
    | It provides a basic image previewer.
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

        super(Preview, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = True

        self.__ui_resources_directory = "resources"

        self.__engine = None
        self.__settings = None
        self.__settings_section = None

        self.__preferences_manager = None
        self.__ibl_sets_outliner = None
        self.__inspector = None

        self.__images_previewers = None
        self.__maximum_images_previewers_instances = 5

        self.__inspector_buttons = {"Background": {"object": None,
                                                   "text": "View Background Image",
                                                   "row": 1,
                                                   "column": 3},
                                    "Lighting": {"object": None,
                                                 "text": "View Lighting Image",
                                                 "row": 1,
                                                 "column": 4},
                                    "Reflection": {"object": None,
                                                   "text": "View Reflection Image",
                                                   "row": 1,
                                                   "column": 5},
                                    "Plate": {"object": None,
                                              "text": "View Plate(s)",
                                              "row": 1,
                                              "column": 6}}

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
    def images_previewers(self):
        """
        Property for **self.__images_previewers** attribute.

        :return: self.__images_previewers.
        :rtype: list
        """

        return self.__images_previewers

    @images_previewers.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def images_previewers(self, value):
        """
        Setter for **self.__images_previewers** attribute.

        :param value: Attribute value.
        :type value: list
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "images_previewers"))

    @images_previewers.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def images_previewers(self):
        """
        Deleter for **self.__images_previewers** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "images_previewers"))

    @property
    def maximum_images_previewers_instances(self):
        """
        Property for **self.__maximum_images_previewers_instances** attribute.

        :return: self.__maximum_images_previewers_instances.
        :rtype: int
        """

        return self.__maximum_images_previewers_instances

    @maximum_images_previewers_instances.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def maximum_images_previewers_instances(self, value):
        """
        Setter for **self.__maximum_images_previewers_instances** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__,
                                                         "maximum_images_previewers_instances"))

    @maximum_images_previewers_instances.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def maximum_images_previewers_instances(self):
        """
        Deleter for **self.__maximum_images_previewers_instances** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__,
                                                             "maximum_images_previewers_instances"))

    @property
    def inspector_buttons(self):
        """
        Property for **self.__inspector_buttons** attribute.

        :return: self.__inspector_buttons.
        :rtype: dict
        """

        return self.__inspector_buttons

    @inspector_buttons.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def inspector_buttons(self, value):
        """
        Setter for **self.__inspector_buttons** attribute.

        :param value: Attribute value.
        :type value: dict
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspector_buttons"))

    @inspector_buttons.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def inspector_buttons(self):
        """
        Deleter for **self.__inspector_buttons** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspector_buttons"))

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

        self.__preferences_manager = self.__engine.components_manager["factory.preferences_manager"]
        self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]
        self.__inspector = self.__engine.components_manager["core.inspector"]

        self.__images_previewers = []

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
        self.__settings = None
        self.__settings_section = None

        self.__preferences_manager = None
        self.__ibl_sets_outliner = None
        self.__inspector = None

        for images_previewer in self.__images_previewers[:]:
            images_previewer.ui.close()

        self.activated = False
        return True

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        self.__Custom_Previewer_Path_lineEdit_set_ui()

        self.__add_actions()
        self.__add_inspector_buttons()

        # Signals / Slots.
        self.Custom_Previewer_Path_toolButton.clicked.connect(self.__Custom_Previewer_Path_toolButton__clicked)
        self.Custom_Previewer_Path_lineEdit.editingFinished.connect(
            self.__Custom_Previewer_Path_lineEdit__editFinished)

        self.initialized_ui = True
        return True

    def uninitialize_ui(self):
        """
        Uninitializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

        self.__remove_actions()
        self.__remove_inspector_buttons()

        # Signals / Slots.
        self.Custom_Previewer_Path_toolButton.clicked.disconnect(self.__Custom_Previewer_Path_toolButton__clicked)
        self.Custom_Previewer_Path_lineEdit.editingFinished.disconnect(
            self.__Custom_Previewer_Path_lineEdit__editFinished)

        self.initialized_ui = False
        return True

    def add_widget(self):
        """
        Adds the Component Widget to the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

        self.__preferences_manager.Others_Preferences_gridLayout.addWidget(self.Custom_Previewer_Path_groupBox)

        return True

    def remove_widget(self):
        """
        Removes the Component Widget from the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

        self.__preferences_manager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
        self.Custom_Previewer_Path_groupBox.setParent(None)

        return True

    def __add_actions(self):
        """
        Sets Component actions.
        """

        LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

        view_ibl_sets_background_images_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|View Background Image ...",
            slot=self.__ibl_sets_outliner_views_view_ibl_sets_background_images_action__triggered)
        view_ibl_sets_lighting_images_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|View Lighting Image ...",
            slot=self.__ibl_sets_outliner_views_view_ibl_sets_lighting_images_action__triggered)
        view_ibl_sets_reflection_images_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|View Reflection Image ...",
            slot=self.__ibl_sets_outliner_views_view_ibl_sets_reflection_images_action__triggered)
        view_ibl_sets_plates_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.ibl_sets_outliner|View Plate(s) ...",
            slot=self.__ibl_sets_outliner_views_view_ibl_sets_plates_action__triggered)
        for view in self.__ibl_sets_outliner.views:
            separator_action = QAction(view)
            separator_action.setSeparator(True)
            for action in (separator_action,
                           view_ibl_sets_background_images_action,
                           view_ibl_sets_lighting_images_action,
                           view_ibl_sets_reflection_images_action,
                           view_ibl_sets_plates_action):
                view.addAction(action)

        separator_action = QAction(self.__inspector.Inspector_Overall_frame)
        separator_action.setSeparator(True)
        self.__inspector.Inspector_Overall_frame.addAction(separator_action)

        self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.inspector|View Background Image ...",
            slot=self.__Inspector_Overall_frame_view_active_ibl_set_background_image_action__triggered))
        self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.inspector|View Lighting Image ...",
            slot=self.__Inspector_Overall_frame_view_active_ibl_set_lighting_image_action__triggered))
        self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.inspector|View Reflection Image ...",
            slot=self.__Inspector_Overall_frame_view_active_ibl_set_reflection_image_action__triggered))
        self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|core.inspector|View Plate(s) ...",
            slot=self.__Inspector_Overall_frame_view_active_ibl_set_plates_action__triggered))

    def __remove_actions(self):
        """
        Removes actions.
        """

        LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

        view_ibl_sets_background_images_action = "Actions|Umbra|Components|core.ibl_sets_outliner|View Background Image ..."
        view_ibl_sets_lighting_images_action = "Actions|Umbra|Components|core.ibl_sets_outliner|View Lighting Image ..."
        view_ibl_sets_reflection_images_action = "Actions|Umbra|Components|core.ibl_sets_outliner|View Reflection Image ..."
        view_ibl_sets_plates_action = "Actions|Umbra|Components|core.ibl_sets_outliner|View Plate(s) ..."
        actions = (view_ibl_sets_background_images_action,
                   view_ibl_sets_lighting_images_action,
                   view_ibl_sets_reflection_images_action,
                   view_ibl_sets_plates_action)
        for view in self.__ibl_sets_outliner.views:
            for action in actions:
                view.removeAction(self.__engine.actions_manager.get_action(action))
        for action in actions:
            self.__engine.actions_manager.unregister_action(action)

        view_active_ibl_set_background_image_action = "Actions|Umbra|Components|core.inspector|View Background Image ..."
        view_active_ibl_set_lighting_image_action = "Actions|Umbra|Components|core.inspector|View Lighting Image ..."
        view_active_ibl_set_reflection_image_action = "Actions|Umbra|Components|core.inspector|View Reflection Image ..."
        view_active_ibl_set_plates_action = "Actions|Umbra|Components|core.inspector|View Plate(s) ..."
        actions = (view_active_ibl_set_background_image_action,
                   view_active_ibl_set_lighting_image_action,
                   view_active_ibl_set_reflection_image_action,
                   view_active_ibl_set_plates_action)
        for action in actions:
            self.__inspector.Inspector_Overall_frame.removeAction(self.__engine.actions_manager.get_action(action))
            self.__engine.actions_manager.unregister_action(action)

    def __add_inspector_buttons(self):
        """
        Adds buttons to the :mod:`sibl_gui.components.core.inspector.inspector` Component.
        """

        self.__inspector.Inspector_Options_groupBox.show()
        for key, value in self.__inspector_buttons.iteritems():
            value["object"] = QPushButton(value["text"])
            self.__inspector.Inspector_Options_groupBox_gridLayout.addWidget(value["object"],
                                                                             value["row"],
                                                                             value["column"])
            value["object"].clicked.connect(functools.partial(self.view_active_ibl_set_images_ui, key))

    def __remove_inspector_buttons(self):
        """
        Removes buttons from the :mod:`sibl_gui.components.core.inspector.inspector` Component.
        """

        for value in self.__inspector_buttons.itervalues():
            value["object"].setParent(None)

    def __ibl_sets_outliner_views_view_ibl_sets_background_images_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.ibl_sets_outliner|View Background Image ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.view_ibl_sets_images_ui("Background")

    def __ibl_sets_outliner_views_view_ibl_sets_lighting_images_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.ibl_sets_outliner|View Lighting Image ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.view_ibl_sets_images_ui("Lighting")

    def __ibl_sets_outliner_views_view_ibl_sets_reflection_images_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.ibl_sets_outliner|View Reflection Image ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.view_ibl_sets_images_ui("Reflection")

    def __ibl_sets_outliner_views_view_ibl_sets_plates_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.ibl_sets_outliner|View Plate(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.view_ibl_sets_images_ui("Plate")

    def __Inspector_Overall_frame_view_active_ibl_set_background_image_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.inspector|View Background Image ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.view_active_ibl_set_images_ui("Background")

    def __Inspector_Overall_frame_view_active_ibl_set_lighting_image_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.inspector|View Lighting Image ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.view_active_ibl_set_images_ui("Lighting")

    def __Inspector_Overall_frame_view_active_ibl_set_reflection_image_action__triggered(self, checked):
        """
        Defines the slot triggered by **'"Actions|Umbra|Components|core.inspector|View Reflection Image ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.view_active_ibl_set_images_ui("Reflection")

    def __Inspector_Overall_frame_view_active_ibl_set_plates_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|core.inspector|View Plate(s) ...'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.view_active_ibl_set_images_ui("Plate")

    def __Custom_Previewer_Path_lineEdit_set_ui(self):
        """
        Fills **Custom_Previewer_Path_lineEdit** Widget.
        """

        custom_previewer = self.__settings.get_key(self.__settings_section, "custom_previewer")
        LOGGER.debug("> Setting '{0}' with value '{1}'.".format(
            "Custom_Previewer_Path_lineEdit", custom_previewer.toString()))
        self.Custom_Previewer_Path_lineEdit.setText(custom_previewer.toString())

    def __Custom_Previewer_Path_toolButton__clicked(self, checked):
        """
        Defines the slot triggered by **Custom_Previewer_Path_toolButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        custom_previewerExecutable = umbra.ui.common.store_last_browsed_path(
            QFileDialog.getOpenFileName(self, "Custom Previewer Executable:", RuntimeGlobals.last_browsed_path))
        if custom_previewerExecutable != "":
            LOGGER.debug("> Chosen custom Images Previewer executable: '{0}'.".format(custom_previewerExecutable))
            self.Custom_Previewer_Path_lineEdit.setText(QString(custom_previewerExecutable))
            self.__settings.set_key(self.__settings_section,
                                    "custom_previewer",
                                    self.Custom_Previewer_Path_lineEdit.text())

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              foundations.exceptions.UserError)
    def __Custom_Previewer_Path_lineEdit__editFinished(self):
        """
        Defines the slot triggered by **Custom_Previewer_Path_lineEdit** Widget when edited and check that entered path is valid.
        """

        value = foundations.strings.to_string(self.Custom_Previewer_Path_lineEdit.text())
        if not foundations.common.path_exists(os.path.abspath(value)) and value != "":
            LOGGER.debug("> Restoring preferences!")
            self.__Custom_Previewer_Path_lineEdit_set_ui()

            raise foundations.exceptions.UserError("{0} | Invalid custom Images Previewer executable file!".format(
                self.__class__.__name__))
        else:
            self.__settings.set_key(
                self.__settings_section, "custom_previewer", self.Custom_Previewer_Path_lineEdit.text())

    def __maximum_images_previewers_instances_reached(self):
        """
        Returns if the maximum Previewers instances allowed is reached.

        :return: Maximum instances reached.
        :rtype: bool
        """

        if len(self.__images_previewers) >= self.__maximum_images_previewers_instances:
            self.__engine.notifications_manager.warnify(
                "{0} | You can only launch '{1}' images Previewer instances at same time!".format(
                    self.__class__.__name__, self.__maximum_images_previewers_instances))
            return True
        else:
            return False

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def view_ibl_sets_images_ui(self, image_type, *args):
        """
        Launches selected Ibl Sets Images Previewer.

        :param image_type: Image type.
        :type image_type: unicode
        :param \*args: Arguments.
        :type \*args: \*
        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_ibl_sets = self.__ibl_sets_outliner.get_selected_ibl_sets()

        paths = []
        for ibl_set in selected_ibl_sets:
            if self.__maximum_images_previewers_instances_reached():
                break

            ibl_set_paths = self.get_ibl_set_images_paths(ibl_set, image_type)
            if not ibl_set_paths:
                self.__engine.notifications_manager.warnify(
                    "{0} | '{1}' Ibl Set has no '{2}' image type and will be skipped!".format(
                        self.__class__.__name__, ibl_set.title, image_type))

            paths.extend(ibl_set_paths)

        if self.view_images(paths, foundations.strings.to_string(self.Custom_Previewer_Path_lineEdit.text())):
            return True
        else:
            raise Exception("{0} | Exception raised while displaying '{1}' Ibl Set(s) image(s)!".format(
                self.__class__.__name__, ", ".join((ibl_set.title for ibl_set in selected_ibl_sets))))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              foundations.exceptions.FileExistsError,
                                              Exception)
    def view_active_ibl_set_images_ui(self, image_type, *args):
        """
        Launches :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set Images Previewer.

        :param image_type: Image type.
        :type image_type: unicode
        :param \*args: Arguments.
        :type \*args: \*
        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        active_ibl_set = self.__inspector.active_ibl_set
        if active_ibl_set is None:
            return False

        if not foundations.common.path_exists(active_ibl_set.path):
            raise foundations.exceptions.FileExistsError(
                "{0} | Exception raised while opening Inspector Ibl Set directory: '{1}' Ibl Set file doesn't exists!".format(
                    self.__class__.__name__, active_ibl_set.title))

        if self.__maximum_images_previewers_instances_reached():
            return False

        paths = self.get_ibl_set_images_paths(active_ibl_set, image_type)
        if paths:
            if self.view_images(paths,
                                foundations.strings.to_string(self.Custom_Previewer_Path_lineEdit.text())):
                return True
            else:
                raise Exception("{0} | Exception raised while displaying '{1}' inspector Ibl Set image(s)!".format(
                    self.__class__.__name__, active_ibl_set.title))
        else:
            self.__engine.notifications_manager.warnify(
                "{0} | '{1}' Inspector Ibl Set has no '{2}' image type!".format(self.__class__.__name__,
                                                                                active_ibl_set.title,
                                                                                image_type))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
    def view_images(self, paths, custom_previewer=None):
        """
        Launches an Ibl Set Images Previewer.

        :param paths: Image paths.
        :type paths: list
        :param custom_previewer: Custom previewer.
        :type custom_previewer: unicode
        """

        if custom_previewer:
            preview_command = self.get_process_command(paths, custom_previewer)
            if preview_command:
                LOGGER.debug("> Current image preview command: '{0}'.".format(preview_command))
                LOGGER.info("{0} | Launching Previewer with '{1}' images paths.".format(self.__class__.__name__,
                                                                                        ", ".join(paths)))
                edit_process = QProcess()
                edit_process.startDetached(preview_command)
                return True
            else:
                raise Exception("{0} | Exception raised: No suitable process command given!".format(
                    self.__class__.__name__))
        else:
            if not len(self.__images_previewers) >= self.__maximum_images_previewers_instances:
                return self.get_images_previewer(paths)
            else:
                LOGGER.warning("!> {0} | You can only launch '{1}' images Previewer instances at same time!".format(
                    self.__class__.__name__, self.__maximum_images_previewers_instances))

    def add_images_previewer(self, images_previewer):
        """
        Adds an Images Previewer.

        :param images_previewer: Images Previewer.
        :type images_previewer: ImagesPreviewer
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding '{0}' Images Previewer.".format(images_previewer))

        self.__images_previewers.append(images_previewer)
        return True

    def remove_images_previewer(self, images_previewer):
        """
        Removes an Images Previewer.

        :param images_previewer: Images Previewer.
        :type images_previewer: ImagesPreviewer
        """

        LOGGER.debug("> Removing '{0}' Images Previewer.".format(images_previewer))

        self.__images_previewers.remove(images_previewer)
        return True

    @umbra.ui.common.show_wait_cursor
    @umbra.engine.show_processing("Reading Images...")
    def get_images_previewer(self, paths):
        """
        Launches an Images Previewer.

        :param paths: Images paths.
        :type paths: list
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Launching Images Previewer for '{0}' images.".format(", ".join(paths)))

        self.add_images_previewer(ImagesPreviewer(self, paths, Qt.Window))
        self.__images_previewers[-1].show()
        return True

    def get_process_command(self, paths, custom_previewer):
        """
        Gets process command.

        :param paths: Paths to preview.
        :type paths: unicode
        :param custom_previewer: Custom browser.
        :type custom_previewer: unicode
        :return: Process command.
        :rtype: unicode
        """

        process_command = None
        images_paths = [os.path.normpath(path) for path in paths]
        if platform.system() == "Windows" or platform.system() == "Microsoft":
            process_command = "\"{0}\" \"{1}\"".format(custom_previewer, " ".join(images_paths))
        elif platform.system() == "Darwin":
            process_command = "open -a \"{0}\" \"{1}\"".format(custom_previewer, " ".join(images_paths))
        elif platform.system() == "Linux":
            process_command = "\"{0}\" \"{1}\"".format(custom_previewer, " ".join(images_paths))
        return process_command

    def get_ibl_set_images_paths(self, ibl_set, image_type):
        """
        Gets Ibl Set images paths.

        :param ibl_set: Ibl Set.
        :type ibl_set: IblSet
        :param image_type: Image type.
        :type image_type: unicode
        :return: Images paths.
        :rtype: list
        """

        image_paths = []
        if image_type == "Background":
            path = ibl_set.background_image
            path and image_paths.append(path)
        elif image_type == "Lighting":
            path = ibl_set.lighting_image
            path and image_paths.append(path)
        elif image_type == "Reflection":
            path = ibl_set.reflection_image
            path and image_paths.append(path)
        elif image_type == "Plate":
            if foundations.common.path_exists(ibl_set.path):
                LOGGER.debug("> Parsing Inspector Ibl Set file: '{0}'.".format(ibl_set))
                sections_file_parser = SectionsFileParser(ibl_set.path)
                sections_file_parser.parse()
                for section in sections_file_parser.sections:
                    if re.search(r"Plate\d+", section):
                        image_paths.append(os.path.normpath(os.path.join(os.path.dirname(ibl_set.path),
                                                                         sections_file_parser.get_value("PLATEfile",
                                                                                                        section))))

        for path in image_paths[:]:
            if not foundations.common.path_exists(path):
                image_paths.remove(path) and LOGGER.warning(
                    "!> {0} | '{1}' image file doesn't exists and will be skipped!".format(self.__class__.__name__,
                                                                                           path))
        return image_paths
