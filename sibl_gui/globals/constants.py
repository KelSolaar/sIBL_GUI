#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines **sIBL_GUI** package default constants through the :class:`Constants` class.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform

import sibl_gui

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["Constants"]

class Constants():
    """
    Defines **sIBL_GUI** package default constants.
    """

    application_name = "sIBL_GUI"
    """
    :param application_name: Package Application name.
    :type application_name: unicode
    """
    major_version = "4"
    """
    :param major_version: Package major version.
    :type major_version: unicode
    """
    minor_version = "0"
    """
    :param minor_version: Package minor version.
    :type minor_version: unicode
    """
    change_version = "8"
    """
    :param change_version: Package change version.
    :type change_version: unicode
    """
    version = ".".join((major_version, minor_version, change_version))
    """
    :param version: Package version.
    :type version: unicode
    """

    logger = "sIBL_GUI_Logger"
    """
    :param logger: Package logger name.
    :type logger: unicode
    """

    default_codec = "utf-8"
    """
    :param default_codec: Default codec.
    :type default_codec: unicode
    """
    codec_error = "ignore"
    """
    :param codec_error: Default codec error behavior.
    :type codec_error: unicode
    """

    application_directory = os.sep.join(("sIBL_GUI", ".".join((major_version, minor_version))))
    """
    :param application_directory: Package Application directory.
    :type application_directory: unicode
    """
    if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Darwin":
        provider_directory = "HDRLabs"
        """
        :param provider_directory: Package provider directory.
        :type provider_directory: unicode
        """
    elif platform.system() == "Linux":
        provider_directory = ".HDRLabs"
        """
        :param provider_directory: Package provider directory.
        :type provider_directory: unicode
        """

    database_directory = "database"
    """
    :param database_directory: Application Database directory.
    :type database_directory: unicode
    """
    patches_directory = "patches"
    """
    :param patches_directory: Application patches directory.
    :type patches_directory: unicode
    """
    settings_directory = "settings"
    """
    :param settings_directory: Application settings directory.
    :type settings_directory: unicode
    """
    user_components_directory = "components"
    """
    :param user_components_directory: Application user components directory.
    :type user_components_directory: unicode
    """
    logging_directory = "logging"
    """
    :param logging_directory: Application logging directory.
    :type logging_directory: unicode
    """
    templates_directory = "templates"
    """
    :param templates_directory: Application Templates directory.
    :type templates_directory: unicode
    """
    io_directory = "io"
    """
    :param io_directory: Application io directory.
    :type io_directory: unicode
    """

    preferences_directories = (database_directory,
                                patches_directory,
                                settings_directory,
                                user_components_directory,
                                logging_directory,
                                templates_directory,
                                io_directory)
    """
    :param preferences_directories: Application preferences directories.
    :type preferences_directories: tuple
    """

    core_components_directory = "components/core"
    """
    :param core_components_directory: Application core components directory.
    :type core_components_directory: unicode
    """
    addons_components_directory = "components/addons"
    """
    :param addons_components_directory: Application addons components directory.
    :type addons_components_directory: unicode
    """

    resources_directory = "resources"
    """
    :param resources_directory: Application resources directory.
    :type resources_directory: unicode
    """

    patches_file = "sIBL_GUI_Patches.rc"
    """
    :param patches_file: Application settings file.
    :type patches_file: unicode
    """
    database_file = "sIBL_GUI_Database.sqlite"
    """
    :param database_file: Application Database file.
    :type database_file: unicode
    """
    settings_file = "sIBL_GUI_Settings.rc"
    """
    :param settings_file: Application settings file.
    :type settings_file: unicode
    """
    logging_file = "sIBL_GUI_Logging_{0}.log"
    """
    :param logging_file: Application logging file.
    :type logging_file: unicode
    """

    libraries_directory = "libraries"
    """
    :param libraries_directory: Application libraries directory.
    :type libraries_directory: unicode
    """
    if platform.system() == "Windows" or platform.system() == "Microsoft":
        freeimage_library = os.path.join(libraries_directory, "freeimage/resources/FreeImage.dll")
        """FreeImage library path: '**freeimage/resources/FreeImage.dll** on Windows,
        **freeimage/resources/libfreeimage.dylib** on Darwin,
        **freeimage/resources/libfreeimage.so** on Linux' ( String )"""
    elif platform.system() == "Darwin":
        freeimage_library = os.path.join(libraries_directory, "freeimage/resources/libfreeimage.dylib")
        """FreeImage library path: '**freeimage/resources/FreeImage.dll** on Windows,
        **freeimage/resources/libfreeimage.dylib** on Darwin,
        **freeimage/resources/libfreeimage.so** on Linux' ( String )"""
    elif platform.system() == "Linux":
        freeimage_library = os.path.join(libraries_directory, "freeimage/resources/libfreeimage.so")
        """FreeImage library path: '**freeimage/resources/FreeImage.dll** on Windows,
        **freeimage/resources/libfreeimage.dylib** on Darwin,
        **freeimage/resources/libfreeimage.so** on Linux' ( String )"""
