#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**launcher.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    | Defines various classes, methods and definitions to run, maintain and exit the Application.
    | The main Application object is the :class:`sIBL_GUI` class.

**Others:**

"""

from __future__ import unicode_literals

import os
import sys
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QPixmap


def _set_package_directory():
    """
    Sets the Application package directory in the path.
    """

    if hasattr(sys, "frozen"):
        package_directory = os.path.dirname(__file__)
    else:
        package_directory = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
    package_directory not in sys.path and sys.path.append(package_directory)


_set_package_directory()

import sibl_gui.globals.constants
import sibl_gui.globals.ui_constants
import sibl_gui.globals.runtime_globals
import umbra.globals.constants
import umbra.globals.ui_constants
import umbra.globals.runtime_globals

umbra.globals.constants.Constants.__dict__.update(sibl_gui.globals.constants.Constants.__dict__)
umbra.globals.ui_constants.UiConstants.__dict__.update(sibl_gui.globals.ui_constants.UiConstants.__dict__)
umbra.globals.runtime_globals.RuntimeGlobals.__dict__.update(sibl_gui.globals.runtime_globals.RuntimeGlobals.__dict__)

for path in (os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.resources_directory),
             os.path.join(os.getcwd(), sibl_gui.__name__, sibl_gui.globals.constants.Constants.resources_directory)):
    path = os.path.normpath(path)
    if os.path.exists(path):
        path not in umbra.globals.runtime_globals.RuntimeGlobals.resources_directories and \
        umbra.globals.runtime_globals.RuntimeGlobals.resources_directories.append(path)

import foundations.globals.constants
import manager.globals.constants


def _override_dependencies_globals():
    """
    Overrides dependencies globals.
    """

    foundations.globals.constants.Constants.logger = \
        manager.globals.constants.Constants.logger = umbra.globals.constants.Constants.logger

    foundations.globals.constants.Constants.application_directory = \
        manager.globals.constants.Constants.application_directory = umbra.globals.constants.Constants.application_directory


_override_dependencies_globals()

import foundations.common
import foundations.verbose
import sibl_gui.ui.models
import sibl_gui.ui.caches
import sibl_gui.ui.widgets.application_QToolBar
import umbra.engine
import umbra.ui.common
import umbra.ui.models
import umbra.ui.widgets.application_QToolBar

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "sIBL_GUI", "extend_command_line_parameters_parser"]

LOGGER = foundations.verbose.install_logger()


class sIBL_GUI(umbra.engine.Umbra):
    """
    Defines the main class of the **sIBL_GUI** package.
    """

    def __init__(self,
                 parent=None,
                 *args,
                 **kwargs):
        """
        Initializes the class.

        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        umbra.engine.Umbra.__init__(self,
                                    parent,
                                    *args,
                                    **kwargs)

        # --- Setting class attributes. ---
        self.__thumbnails_cache_directory = self.__thumbnails_cache_directory
        self.__images_caches = self.__images_caches

    @property
    def thumbnails_cache_directory(self):
        """
        Property for **self.__thumbnails_cache_directory** attribute.

        :return: self.__thumbnails_cache_directory.
        :rtype: unicode
        """

        return self.__thumbnails_cache_directory

    @thumbnails_cache_directory.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def thumbnails_cache_directory(self, value):
        """
        Setter for **self.__thumbnails_cache_directory** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "thumbnails_cache_directory"))

    @thumbnails_cache_directory.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def thumbnails_cache_directory(self):
        """
        Deleter for **self.__thumbnails_cache_directory** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "thumbnails_cache_directory"))

    @property
    def images_caches(self):
        """
        Property for **self.__images_caches** attribute.

        :return: self.__images_caches.
        :rtype: Structure
        """

        return self.__images_caches

    @images_caches.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def images_caches(self, value):
        """
        Setter for **self.__images_caches** attribute.

        :param value: Attribute value.
        :type value: Structure
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "images_caches"))

    @images_caches.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def images_caches(self):
        """
        Deleter for **self.__images_caches** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "images_caches"))

    def __override_application_toolbar(self):
        """
        Overrides the Application toolbar.
        """

        umbra.ui.widgets.application_QToolBar.Application_QToolBar = \
            sibl_gui.ui.widgets.application_QToolBar.Application_QToolBar

    def __set_thumbnails_cache_directory(self):
        """
        Sets the Application thumbnails cache directory.
        """

        self.__thumbnails_cache_directory = umbra.globals.runtime_globals.RuntimeGlobals.thumbnails_cache_directory = \
            os.path.join(umbra.globals.runtime_globals.RuntimeGlobals.user_application_data_directory,
                         umbra.globals.constants.Constants.io_directory,
                         umbra.globals.ui_constants.UiConstants.thumbnails_cache_directory)

    def __set_images_caches(self):
        """
        Sets the Application images caches.
        """

        loading_image = umbra.ui.common.get_resource_path(umbra.globals.ui_constants.UiConstants.loading_image)
        self.__images_caches = umbra.globals.runtime_globals.RuntimeGlobals.images_caches = \
            foundations.data_structures.Structure(**{
                "QImage": sibl_gui.ui.caches.AsynchronousGraphicsItemsCache(type=QImage, placeholder=loading_image),
                "QPixmap": sibl_gui.ui.caches.AsynchronousGraphicsItemsCache(type=QPixmap, placeholder=loading_image),
                "QIcon": sibl_gui.ui.caches.AsynchronousGraphicsItemsCache(type=QIcon, placeholder=loading_image)})

        # Override "umbra.ui.models.GraphModel.data" method to use "sibl_gui.ui.models.GraphModel.data" method
        # with asynchronous images loading.
        setattr(umbra.ui.models.GraphModel, "data", umbra.ui.models.GraphModel.data)

    def on_pre_initialisation(self):
        """
        Called by :class:`umbra.engine.Umbra` class before Application main class initialisation.
        """

        self.__override_application_toolbar()
        self.__set_thumbnails_cache_directory()
        self.__set_images_caches()

    def on_initialisation(self):
        """
        Called by :class:`umbra.engine.Umbra` class on Application main class initialisation.
        """

        pass

    def on_post_initialisation(self):
        """
        Called by :class:`umbra.engine.Umbra` class after Application main class initialisation.
        """

        for cache in self.__images_caches.itervalues():
            self.worker_threads.append(cache.worker)

        components_manager_ui = self.components_manager.get_interface("factory.components_manager_ui")
        self.images_caches.QIcon.content_added.connect(components_manager_ui.view.viewport().update)

        script_editor = self.components_manager.get_interface("factory.script_editor")
        self.content_dropped.disconnect(script_editor._ScriptEditor__engine__content_dropped)


def extend_command_line_parameters_parser(parser):
    """
    Returns the command line parameters parser.

    :param parser: Command line parameters parser.
    :type parser: Parser
    :return: Definition success.
    :rtype: bool
    """

    parser.add_option("-d",
                      "--database_directory",
                      action="store",
                      type="string",
                      dest="database_directory",
                      help="'Database directory'.")
    parser.add_option("-r",
                      "--database_read_only",
                      action="store_true",
                      default=False,
                      dest="database_read_only",
                      help="'Database read only'.")
    parser.add_option("-o",
                      "--loader_scripts_output_directory",
                      action="store",
                      type="string",
                      dest="loader_scripts_output_directory",
                      help="'Loader Scripts output directory'.")

    return True


def main():
    """
    Starts the Application.

    :return: Definition success.
    :rtype: bool
    """

    command_line_parameters_parser = umbra.engine.get_command_line_parameters_parser()
    extend_command_line_parameters_parser(command_line_parameters_parser)
    components_paths = []
    for path in (os.path.join(umbra.__path__[0], umbra.globals.constants.Constants.factory_components_directory),
                 os.path.join(
                         os.getcwd(), umbra.__name__, umbra.globals.constants.Constants.factory_components_directory),
                 os.path.join(
                         umbra.__path__[0], umbra.globals.constants.Constants.factory_addons_components_directory),
                 os.path.join(os.getcwd(), umbra.__name__,
                              umbra.globals.constants.Constants.factory_addons_components_directory),
                 os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.core_components_directory),
                 os.path.join(os.getcwd(), sibl_gui.__name__,
                              sibl_gui.globals.constants.Constants.core_components_directory),
                 os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.addons_components_directory),
                 os.path.join(os.getcwd(), sibl_gui.__name__,
                              sibl_gui.globals.constants.Constants.addons_components_directory)):
        (foundations.common.path_exists(path) and not path in components_paths) and components_paths.append(path)

    return umbra.engine.run(sIBL_GUI,
                            command_line_parameters_parser.parse_args([unicode(argument,
                                                                               umbra.globals.constants.Constants.default_codec,
                                                                               umbra.globals.constants.Constants.codec_error)
                                                                       for argument in sys.argv]),
                            components_paths,
                            ("factory.script_editor",
                             "factory.preferences_manager",
                             "factory.components_manager_ui",
                             "core.database",
                             "core.collections_outliner",
                             "core.ibl_sets_outliner",
                             "core.inspector",
                             "core.templates_outliner"),
                            ("core.ibl_sets_outliner",))


if __name__ == "__main__":
    main()
