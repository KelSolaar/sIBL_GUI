#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**uiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **sIBL_GUI** package ui constants through the :class:`UiConstants` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UiConstants"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class UiConstants():
	"""
	This class provides **sIBL_GUI** package ui constants.
	"""

	uiFile = "sIBL_GUI.ui"
	"""Application ui file: '**sIBL_GUI.ui**' ( String )"""

	windowsStylesheetFile = "styles/Windows_styleSheet.qss"
	"""Application Windows Os stylesheet file: '**styles/Windows_styleSheet.qss**' ( String )"""
	darwinStylesheetFile = "styles/Darwin_styleSheet.qss"
	"""Application Mac Os X Os stylesheet file: '**styles/Darwin_styleSheet.qss**' ( String )"""
	linuxStylesheetFile = "styles/Linux_styleSheet.qss"
	"""Application Linux Os stylesheet file: '**styles/Linux_styleSheet.qss**' ( String )"""
	windowsStyle = "plastique"
	"""Application Windows Os style: '**plastique**' ( String )"""
	darwinStyle = "plastique"
	"""Application Mac Os X Os style: '**plastique**' ( String )"""
	linuxStyle = "plastique"
	"""Application Linux Os style: '**plastique**' ( String )"""

	settingsFile = "preferences/Default_Settings.rc"
	"""Application defaults settings file: '**preferences/Default_Settings.rc**' ( String )"""

	layoutsFile = "layouts/Default_Layouts.rc"
	"""Application defaults layouts file: '**layouts/Default_Layouts.rc**' ( String )"""

	applicationWindowsIcon = "images/Icon_Light.png"
	"""Application icon file: '**images/Icon_Light.png**' ( String )"""

	splashScreenImage = "images/sIBL_GUI_SpashScreen.png"
	"""Application splashscreen image: '**images/sIBL_GUI_SpashScreen.png**' ( String )"""
	logoImage = "images/sIBL_GUI_Logo.png"
	"""Application logo image: '**images/sIBL_GUI_Logo.png**' ( String )"""

	defaultToolbarIconSize = 32
	"""Application toolbar icons size: '**32**' ( Integer )"""

	centralWidgetIcon = "images/Central_Widget.png"
	"""Application **Central Widget** icon: '**images/Central_Widget.png**' ( String )"""
	centralWidgetHoverIcon = "images/Central_Widget_Hover.png"
	"""Application **Central Widget** hover icon: '**images/Central_Widget_Hover.png**' ( String )"""
	centralWidgetActiveIcon = "images/Central_Widget_Active.png"
	"""Application **Central Widget** active icon: '**images/Central_Widget_Active.png**' ( String )"""

	customLayoutsIcon = "images/Custom_Layouts.png"
	"""Application **Custom Layouts** icon: '**images/Custom_Layouts.png**' ( String )"""
	customLayoutsHoverIcon = "images/Custom_Layouts_Hover.png"
	"""Application **Custom Layouts** hover icon: '**images/Custom_Layouts_Hover.png**' ( String )"""
	customLayoutsActiveIcon = "images/Custom_Layouts_Active.png"
	"""Application **Custom Layouts** active icon: '**images/Custom_Layouts_Active.png**' ( String )"""

	miscellaneousIcon = "images/Miscellaneous.png"
	"""Application **Miscellaneous** icon: '**images/Miscellaneous.png**' ( String )"""
	miscellaneousHoverIcon = "images/Miscellaneous_Hover.png"
	"""Application **Miscellaneous** hover icon: '**images/Miscellaneous_Hover.png**' ( String )"""
	miscellaneousActiveIcon = "images/Miscellaneous_Active.png"
	"""Application **Miscellaneous** active icon: '**images/Miscellaneous_Active.png**' ( String )"""

	libraryIcon = "images/Library.png"
	"""Application **Library** icon: '**images/Library.png**' ( String )"""
	libraryHoverIcon = "images/Library_Hover.png"
	"""Application **Library** hover icon: '**images/Library_Hover.png**' ( String )"""
	libraryActiveIcon = "images/Library_Active.png"
	"""Application **Library** active icon: '**images/Library_Active.png**' ( String )"""

	inspectIcon = "images/Inspect.png"
	"""Application **Inspect** icon: '**images/Inspect.png**' ( String )"""
	inspectHoverIcon = "images/Inspect_Hover.png"
	"""Application **Inspect** hover icon: '**images/Inspect_Hover.png**' ( String )"""
	inspectActiveIcon = "images/Inspect_Active.png"
	"""Application **Inspect** active icon: '**images/Inspect_Active.png**' ( String )"""

	exportIcon = "images/Export.png"
	"""Application **Export** icon: '**images/Export.png**' ( String )"""
	exportHoverIcon = "images/Export_Hover.png"
	"""Application **Export** hover icon: '**images/Export_Hover.png**' ( String )"""
	exportActiveIcon = "images/Export_Active.png"
	"""Application **Export** active icon: '**images/Export_Active.png**' ( String )"""

	editIcon = "images/Edit.png"
	"""Application **Edit** icon: '**images/Edit.png**' ( String )"""
	editHoverIcon = "images/Edit_Hover.png"
	"""Application **Edit** hover icon: '**images/Edit_Hover.png**' ( String )"""
	editActiveIcon = "images/Edit_Active.png"
	"""Application **Edit** active icon: '**images/Edit_Active.png**' ( String )"""

	preferencesIcon = "images/Preferences.png"
	"""Application **Preferences** icon: '**images/Preferences.png**' ( String )"""
	preferencesHoverIcon = "images/Preferences_Hover.png"
	"""Application **Preferences** hover icon: '**images/Preferences_Hover.png**' ( String )"""
	preferencesActiveIcon = "images/Preferences_Active.png"
	"""Application **Preferences** active icon: '**images/Preferences_Active.png**' ( String )"""

	formatErrorImage = "images/Thumbnail_Format_Not_Supported_Yet.png"
	"""Application format error image thumbnail: '**images/Thumbnail_Format_Not_Supported_Yet.png**' ( String )"""
	missingImage = "images/Thumbnail_Not_Found.png"
	"""Application missing image thumbnail: '**images/Thumbnail_Not_Found.png**' ( String )"""
	loadingImage = "images/Loading.png"
	"""Application loading image thumbnail: '**images/Loading.png**' ( String )"""

	startupLayout = "startupCentric"
	"""Application startup layout: '**startupCentric**' ( String )"""
	developmentLayout = "editCentric"
	"""Application development layout: '**"editCentric"**' ( String )"""

	helpFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html"
	"""Application online help file:
	'**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html**' ( String )"""
	apiFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html"
	"""Application online api file:
	'**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html**' ( String )"""
	makeDonationFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Donations/Make_A_Donation.html"
	"""Application online donation file:
	'**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Donations/Make_A_Donation.html**' ( String )"""

	nativeImageFormats = { "Bmp" : "\.bmp$",
							"Jpeg" : "\.jpeg$",
							"Jpg" : "\.jpg$",
							"Png" : "\.png$" }
	"""Application native image file formats. ( Dictionary )"""

	thirdPartyImageFormats = { "Exr" : ("\.exr$"),
								"Hdr" : ("\.hdr$"),
								"Tif" : ("\.tif$"),
								"Tiff" : ("\.tiff$"),
								"Tga" : ("\.tga$")}
	"""Application third party image file formats. ( Dictionary )"""

	crittercismId = "50aa8ac9866b845bd6000007"
	"""Crittercism Id: '**50aa8ac9866b845bd6000007**' ( String )"""

