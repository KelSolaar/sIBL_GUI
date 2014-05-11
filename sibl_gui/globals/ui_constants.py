#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**ui_constants.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines **sIBL_GUI** package ui constants through the :class:`UiConstants` class.

**Others:**

"""

from __future__ import unicode_literals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UiConstants"]

class UiConstants():
    """
    Defines **sIBL_GUI** package ui constants.
    """

    ui_file = "sIBL_GUI.ui"
    """
    :param ui_file: Application ui file.
    :type ui_file: unicode
    """

    windows_stylesheet_file = "styles/Windows_styleSheet.qss"
    """
    :param windows_stylesheet_file: Application Windows Os stylesheet file.
    :type windows_stylesheet_file: unicode
    """
    darwin_stylesheet_file = "styles/Darwin_styleSheet.qss"
    """
    :param darwin_stylesheet_file: Application Mac Os X Os stylesheet file.
    :type darwin_stylesheet_file: unicode
    """
    linux_stylesheet_file = "styles/Linux_styleSheet.qss"
    """
    :param linux_stylesheet_file: Application Linux Os stylesheet file.
    :type linux_stylesheet_file: unicode
    """
    windows_style = "plastique"
    """
    :param windows_style: Application Windows Os style.
    :type windows_style: unicode
    """
    darwin_style = "plastique"
    """
    :param darwin_style: Application Mac Os X Os style.
    :type darwin_style: unicode
    """
    linux_style = "plastique"
    """
    :param linux_style: Application Linux Os style.
    :type linux_style: unicode
    """

    settings_file = "preferences/Default_Settings.rc"
    """
    :param settings_file: Application defaults settings file.
    :type settings_file: unicode
    """

    layouts_file = "layouts/Default_Layouts.rc"
    """
    :param layouts_file: Application defaults layouts file.
    :type layouts_file: unicode
    """

    application_windows_icon = "images/Icon_Light.png"
    """
    :param application_windows_icon: Application icon file.
    :type application_windows_icon: unicode
    """

    splash_screen_image = "images/sIBL_GUI_SpashScreen.png"
    """
    :param splash_screen_image: Application splashscreen image.
    :type splash_screen_image: unicode
    """
    logo_image = "images/sIBL_GUI_Logo.png"
    """
    :param logo_image: Application logo image.
    :type logo_image: unicode
    """

    default_toolbar_icon_size = 32
    """
    :param default_toolbar_icon_size: Application toolbar icons size.
    :type default_toolbar_icon_size: int
    """

    central_widget_icon = "images/Central_Widget.png"
    """
    :param central_widget_icon: Application **Central Widget** icon.
    :type central_widget_icon: unicode
    """
    central_widget_hover_icon = "images/Central_Widget_Hover.png"
    """
    :param central_widget_hover_icon: Application **Central Widget** hover icon.
    :type central_widget_hover_icon: unicode
    """
    central_widget_active_icon = "images/Central_Widget_Active.png"
    """
    :param central_widget_active_icon: Application **Central Widget** active icon.
    :type central_widget_active_icon: unicode
    """

    custom_layouts_icon = "images/Custom_Layouts.png"
    """
    :param custom_layouts_icon: Application **Custom Layouts** icon.
    :type custom_layouts_icon: unicode
    """
    custom_layouts_hover_icon = "images/Custom_Layouts_Hover.png"
    """
    :param custom_layouts_hover_icon: Application **Custom Layouts** hover icon.
    :type custom_layouts_hover_icon: unicode
    """
    custom_layouts_active_icon = "images/Custom_Layouts_Active.png"
    """
    :param custom_layouts_active_icon: Application **Custom Layouts** active icon.
    :type custom_layouts_active_icon: unicode
    """

    miscellaneous_icon = "images/Miscellaneous.png"
    """
    :param miscellaneous_icon: Application **Miscellaneous** icon.
    :type miscellaneous_icon: unicode
    """
    miscellaneous_hover_icon = "images/Miscellaneous_Hover.png"
    """
    :param miscellaneous_hover_icon: Application **Miscellaneous** hover icon.
    :type miscellaneous_hover_icon: unicode
    """
    miscellaneous_active_icon = "images/Miscellaneous_Active.png"
    """
    :param miscellaneous_active_icon: Application **Miscellaneous** active icon.
    :type miscellaneous_active_icon: unicode
    """

    library_icon = "images/Library.png"
    """
    :param library_icon: Application **Library** icon.
    :type library_icon: unicode
    """
    library_hover_icon = "images/Library_Hover.png"
    """
    :param library_hover_icon: Application **Library** hover icon.
    :type library_hover_icon: unicode
    """
    library_active_icon = "images/Library_Active.png"
    """
    :param library_active_icon: Application **Library** active icon.
    :type library_active_icon: unicode
    """

    inspect_icon = "images/Inspect.png"
    """
    :param inspect_icon: Application **Inspect** icon.
    :type inspect_icon: unicode
    """
    inspect_hover_icon = "images/Inspect_Hover.png"
    """
    :param inspect_hover_icon: Application **Inspect** hover icon.
    :type inspect_hover_icon: unicode
    """
    inspect_active_icon = "images/Inspect_Active.png"
    """
    :param inspect_active_icon: Application **Inspect** active icon.
    :type inspect_active_icon: unicode
    """

    export_icon = "images/Export.png"
    """
    :param export_icon: Application **Export** icon.
    :type export_icon: unicode
    """
    export_hover_icon = "images/Export_Hover.png"
    """
    :param export_hover_icon: Application **Export** hover icon.
    :type export_hover_icon: unicode
    """
    export_active_icon = "images/Export_Active.png"
    """
    :param export_active_icon: Application **Export** active icon.
    :type export_active_icon: unicode
    """

    edit_icon = "images/Edit.png"
    """
    :param edit_icon: Application **Edit** icon.
    :type edit_icon: unicode
    """
    edit_hover_icon = "images/Edit_Hover.png"
    """
    :param edit_hover_icon: Application **Edit** hover icon.
    :type edit_hover_icon: unicode
    """
    edit_active_icon = "images/Edit_Active.png"
    """
    :param edit_active_icon: Application **Edit** active icon.
    :type edit_active_icon: unicode
    """

    preferences_icon = "images/Preferences.png"
    """
    :param preferences_icon: Application **Preferences** icon.
    :type preferences_icon: unicode
    """
    preferences_hover_icon = "images/Preferences_Hover.png"
    """
    :param preferences_hover_icon: Application **Preferences** hover icon.
    :type preferences_hover_icon: unicode
    """
    preferences_active_icon = "images/Preferences_Active.png"
    """
    :param preferences_active_icon: Application **Preferences** active icon.
    :type preferences_active_icon: unicode
    """

    format_error_image = "images/Thumbnail_Format_Not_Supported_Yet.png"
    """
    :param format_error_image: Application format error image thumbnail.
    :type format_error_image: unicode
    """
    missing_image = "images/Thumbnail_Not_Found.png"
    """
    :param missing_image: Application missing image thumbnail.
    :type missing_image: unicode
    """
    loading_image = "images/Loading.png"
    """
    :param loading_image: Application loading image thumbnail.
    :type loading_image: unicode
    """

    startup_layout = "startup_centric"
    """
    :param startup_layout: Application startup layout.
    :type startup_layout: unicode
    """
    development_layout = "edit_centric"
    """
    :param development_layout: Application development layout.
    :type development_layout: unicode
    """

    help_file = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html"
    """Application online help file:
    '**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html**' ( String )"""
    api_file = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html"
    """Application online api file:
    '**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html**' ( String )"""
    make_donation_file = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Donations/Make_A_Donation.html"
    """Application online donation file:
    '**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Donations/Make_A_Donation.html**' ( String )"""

    native_image_formats = {"Bmp" : "\.bmp$",
                        "Jpeg" : "\.jpeg$",
                        "Jpg" : "\.jpg$",
                        "Png" : "\.png$" }
    """
    :param native_image_formats: Application native image file formats.
    :type native_image_formats: dict
    """

    third_party_image_formats = {"Exr" : ("\.exr$"),
                            "Hdr" : ("\.hdr$"),
                            "Tif" : ("\.tif$"),
                            "Tiff" : ("\.tiff$"),
                            "Tga" : ("\.tga$")}
    """
    :param third_party_image_formats: Application third party image file formats.
    :type third_party_image_formats: dict
    """

    thumbnails_sizes = { "Default" : None,
                    "XLarge" : 512,
                    "Large" : 256,
                    "Medium" : 128,
                    "Small" : 64,
                    "XSmall" : 32,
                    "Special1" : 600}
    """
    :param thumbnails_sizes: Application thumbnails sizes.
    :type thumbnails_sizes: dict
    """

    thumbnails_cache_directory = "thumbnails"
    """Thumbnails cache directory."""

    crittercism_id = "5075c158d5f9b9796b000002"
    """
    :param crittercism_id: Crittercism Id.
    :type crittercism_id: unicode
    """
