#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**caches_operations.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`CachesOperations` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import os
from PyQt4.QtGui import QGridLayout

import foundations.exceptions
import foundations.io
import foundations.verbose
import foundations.walkers
import sibl_gui.exceptions
import umbra.exceptions
from manager.QWidget_component import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.globals.ui_constants import UiConstants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "CachesOperations"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Caches_Operations.ui")


class CachesOperations(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`sibl_gui.components.addons.caches_operations.caches_operations` Component Interface class.
    | It provides various methods to operate on the images caches.
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

        super(CachesOperations, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = True

        self.__engine = None

        self.__script_editor = None
        self.__preferences_manager = None

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

        self.__script_editor = self.__engine.components_manager["factory.script_editor"]
        self.__preferences_manager = self.__engine.components_manager["factory.preferences_manager"]

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

        self.__script_editor = None
        self.__preferences_manager = None

        self.activated = False
        return True

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        # Signals / Slots.
        self.Output_Caches_Metrics_pushButton.clicked.connect(self.__Output_Caches_Metrics_pushButton__clicked)
        self.Clear_Thumbnails_Cache_pushButton.clicked.connect(self.__Clear_Thumbnails_Cache_pushButton__clicked)
        self.Clear_Images_Caches_pushButton.clicked.connect(self.__Clear_Images_Caches_pushButton__clicked)

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
        self.Output_Caches_Metrics_pushButton.clicked.disconnect(self.__Output_Caches_Metrics_pushButton__clicked)
        self.Clear_Thumbnails_Cache_pushButton.clicked.disconnect(self.__Clear_Thumbnails_Cache_pushButton__clicked)
        self.Clear_Images_Caches_pushButton.clicked.disconnect(self.__Clear_Images_Caches_pushButton__clicked)

        self.initialized_ui = False
        return True

    def add_widget(self):
        """
        Adds the Component Widget to the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

        self.__preferences_manager.Others_Preferences_gridLayout.addWidget(self.Caches_Operations_groupBox)

        return True

    def remove_widget(self):
        """
        Removes the Component Widget from the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

        self.__preferences_manager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
        self.Caches_Operations_groupBox.setParent(None)

        return True

    def __Clear_Thumbnails_Cache_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Thumbnails_Cache_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.clear_thumbnails_cache()

    def __Clear_Images_Caches_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Clear_Images_Caches_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.clear_images_caches()

    def __Output_Caches_Metrics_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Output_Caches_Metrics_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.output_caches_metrics()
        self.__script_editor.restore_development_layout()

    def output_caches_metrics(self):
        """
        Outputs caches metrics.

        :return: Method success.
        :rtype: bool
        """

        separator = "{0}".format(Constants.logging_separators.replace("*", "-"))
        metrics = dict.fromkeys(UiConstants.thumbnails_sizes, 0)
        for type, cache in self.__engine.images_caches.iteritems():
            LOGGER.info(separator)
            LOGGER.info("{0} | Metrics for '{1}' '{2}' images memory cache:".format(self.__class__.__name__,
                                                                                    Constants.application_name, type))
            cache_metrics = cache.get_metrics().content
            LOGGER.info("{0} | \tCached graphics items count: '{1}'".format(
                self.__class__.__name__, len(cache_metrics)))
            for path, data in sorted(cache.get_metrics().content.iteritems()):
                LOGGER.info("{0} | \t\t'{1}':".format(self.__class__.__name__, path))
                for size, data in sorted(data.iteritems()):
                    if data is not None:
                        metrics[size] += 1
                        path, image_informations_header = data
                        LOGGER.info("{0} | \t\t\t'{1}': '{2}':".format(self.__class__.__name__, size, path))
                        LOGGER.info("{0} | \t\t\t\tSize: {1}x{2} px".format(self.__class__.__name__,
                                                                            image_informations_header.width,
                                                                            image_informations_header.height))
                        LOGGER.info("{0} | \t\t\t\tBpp: {1} bit".format(self.__class__.__name__,
                                                                        image_informations_header.bpp / 4))
                    else:
                        LOGGER.info("{0} | \t\t\t'{1}': '{2}'.".format(
                            self.__class__.__name__, size, Constants.null_object))
            LOGGER.info(separator)

        LOGGER.info(separator)
        LOGGER.info("{0} | Metrics for 'Application' thumbnails disk cache:".format(self.__class__.__name__))
        for size, count in sorted(metrics.iteritems()):
            LOGGER.info("{0} | \t\t{1} '{2}' registered thumbnails.".format(self.__class__.__name__, count, size))
        thumbnails = list(foundations.walkers.files_walker(RuntimeGlobals.thumbnails_cache_directory))
        LOGGER.info("{0} | \t\t{1} files in disk cache directory.".format(self.__class__.__name__, len(thumbnails)))
        LOGGER.info(separator)
        return True

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              sibl_gui.exceptions.CacheOperationError)
    def clear_thumbnails_cache(self):
        """
        Clears the thumbnails cache.

        :return: Method success.
        :rtype: bool
        """

        thumbnails = list(foundations.walkers.files_walker(RuntimeGlobals.thumbnails_cache_directory))

        success = True
        for thumbnail in thumbnails:
            success *= foundations.io.remove(thumbnail)

        if success:
            self.__engine.notifications_manager.notify(
                "{0} | Thumbnails cache has been successfully cleared!".format(self.__class__.__name__))
            return True
        else:
            raise sibl_gui.exceptions.CacheOperationError(
                "{0} | Exception raised while attempting to clear thumbnails cache!".format(
                    self.__class__.__name__))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              sibl_gui.exceptions.CacheOperationError)
    def clear_images_caches(self):
        """
        Clears the images caches.

        :return: Method success.
        :rtype: bool
        """

        success = True
        for cache in self.__engine.images_caches.itervalues():
            success *= cache.flush_content()

        if success:
            self.__engine.notifications_manager.notify(
                "{0} | Images caches have been successfully cleared!".format(self.__class__.__name__))
            return True
        else:
            raise sibl_gui.exceptions.CacheOperationError(
                "{0} | Exception raised while attempting to clear images caches!".format(
                    self.__class__.__name__))
