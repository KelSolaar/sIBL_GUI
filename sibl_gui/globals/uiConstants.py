#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**uiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **sIBL_GUI** package ui constants through the :class:`UiConstants` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines **sIBL_GUI** package ui constants.
	"""

	uiFile = "sIBL_GUI.ui"
	"""
	:param uiFile: Application ui file.
	:type uiFile: unicode
	"""

	windowsStylesheetFile = "styles/Windows_styleSheet.qss"
	"""
	:param windowsStylesheetFile: Application Windows Os stylesheet file.
	:type windowsStylesheetFile: unicode
	"""
	darwinStylesheetFile = "styles/Darwin_styleSheet.qss"
	"""
	:param darwinStylesheetFile: Application Mac Os X Os stylesheet file.
	:type darwinStylesheetFile: unicode
	"""
	linuxStylesheetFile = "styles/Linux_styleSheet.qss"
	"""
	:param linuxStylesheetFile: Application Linux Os stylesheet file.
	:type linuxStylesheetFile: unicode
	"""
	windowsStyle = "plastique"
	"""
	:param windowsStyle: Application Windows Os style.
	:type windowsStyle: unicode
	"""
	darwinStyle = "plastique"
	"""
	:param darwinStyle: Application Mac Os X Os style.
	:type darwinStyle: unicode
	"""
	linuxStyle = "plastique"
	"""
	:param linuxStyle: Application Linux Os style.
	:type linuxStyle: unicode
	"""

	settingsFile = "preferences/Default_Settings.rc"
	"""
	:param settingsFile: Application defaults settings file.
	:type settingsFile: unicode
	"""

	layoutsFile = "layouts/Default_Layouts.rc"
	"""
	:param layoutsFile: Application defaults layouts file.
	:type layoutsFile: unicode
	"""

	applicationWindowsIcon = "images/Icon_Light.png"
	"""
	:param applicationWindowsIcon: Application icon file.
	:type applicationWindowsIcon: unicode
	"""

	splashScreenImage = "images/sIBL_GUI_SpashScreen.png"
	"""
	:param splashScreenImage: Application splashscreen image.
	:type splashScreenImage: unicode
	"""
	logoImage = "images/sIBL_GUI_Logo.png"
	"""
	:param logoImage: Application logo image.
	:type logoImage: unicode
	"""

	defaultToolbarIconSize = 32
	"""
	:param defaultToolbarIconSize: Application toolbar icons size.
	:type defaultToolbarIconSize: int
	"""

	centralWidgetIcon = "images/Central_Widget.png"
	"""
	:param centralWidgetIcon: Application **Central Widget** icon.
	:type centralWidgetIcon: unicode
	"""
	centralWidgetHoverIcon = "images/Central_Widget_Hover.png"
	"""
	:param centralWidgetHoverIcon: Application **Central Widget** hover icon.
	:type centralWidgetHoverIcon: unicode
	"""
	centralWidgetActiveIcon = "images/Central_Widget_Active.png"
	"""
	:param centralWidgetActiveIcon: Application **Central Widget** active icon.
	:type centralWidgetActiveIcon: unicode
	"""

	customLayoutsIcon = "images/Custom_Layouts.png"
	"""
	:param customLayoutsIcon: Application **Custom Layouts** icon.
	:type customLayoutsIcon: unicode
	"""
	customLayoutsHoverIcon = "images/Custom_Layouts_Hover.png"
	"""
	:param customLayoutsHoverIcon: Application **Custom Layouts** hover icon.
	:type customLayoutsHoverIcon: unicode
	"""
	customLayoutsActiveIcon = "images/Custom_Layouts_Active.png"
	"""
	:param customLayoutsActiveIcon: Application **Custom Layouts** active icon.
	:type customLayoutsActiveIcon: unicode
	"""

	miscellaneousIcon = "images/Miscellaneous.png"
	"""
	:param miscellaneousIcon: Application **Miscellaneous** icon.
	:type miscellaneousIcon: unicode
	"""
	miscellaneousHoverIcon = "images/Miscellaneous_Hover.png"
	"""
	:param miscellaneousHoverIcon: Application **Miscellaneous** hover icon.
	:type miscellaneousHoverIcon: unicode
	"""
	miscellaneousActiveIcon = "images/Miscellaneous_Active.png"
	"""
	:param miscellaneousActiveIcon: Application **Miscellaneous** active icon.
	:type miscellaneousActiveIcon: unicode
	"""

	libraryIcon = "images/Library.png"
	"""
	:param libraryIcon: Application **Library** icon.
	:type libraryIcon: unicode
	"""
	libraryHoverIcon = "images/Library_Hover.png"
	"""
	:param libraryHoverIcon: Application **Library** hover icon.
	:type libraryHoverIcon: unicode
	"""
	libraryActiveIcon = "images/Library_Active.png"
	"""
	:param libraryActiveIcon: Application **Library** active icon.
	:type libraryActiveIcon: unicode
	"""

	inspectIcon = "images/Inspect.png"
	"""
	:param inspectIcon: Application **Inspect** icon.
	:type inspectIcon: unicode
	"""
	inspectHoverIcon = "images/Inspect_Hover.png"
	"""
	:param inspectHoverIcon: Application **Inspect** hover icon.
	:type inspectHoverIcon: unicode
	"""
	inspectActiveIcon = "images/Inspect_Active.png"
	"""
	:param inspectActiveIcon: Application **Inspect** active icon.
	:type inspectActiveIcon: unicode
	"""

	exportIcon = "images/Export.png"
	"""
	:param exportIcon: Application **Export** icon.
	:type exportIcon: unicode
	"""
	exportHoverIcon = "images/Export_Hover.png"
	"""
	:param exportHoverIcon: Application **Export** hover icon.
	:type exportHoverIcon: unicode
	"""
	exportActiveIcon = "images/Export_Active.png"
	"""
	:param exportActiveIcon: Application **Export** active icon.
	:type exportActiveIcon: unicode
	"""

	editIcon = "images/Edit.png"
	"""
	:param editIcon: Application **Edit** icon.
	:type editIcon: unicode
	"""
	editHoverIcon = "images/Edit_Hover.png"
	"""
	:param editHoverIcon: Application **Edit** hover icon.
	:type editHoverIcon: unicode
	"""
	editActiveIcon = "images/Edit_Active.png"
	"""
	:param editActiveIcon: Application **Edit** active icon.
	:type editActiveIcon: unicode
	"""

	preferencesIcon = "images/Preferences.png"
	"""
	:param preferencesIcon: Application **Preferences** icon.
	:type preferencesIcon: unicode
	"""
	preferencesHoverIcon = "images/Preferences_Hover.png"
	"""
	:param preferencesHoverIcon: Application **Preferences** hover icon.
	:type preferencesHoverIcon: unicode
	"""
	preferencesActiveIcon = "images/Preferences_Active.png"
	"""
	:param preferencesActiveIcon: Application **Preferences** active icon.
	:type preferencesActiveIcon: unicode
	"""

	formatErrorImage = "images/Thumbnail_Format_Not_Supported_Yet.png"
	"""
	:param formatErrorImage: Application format error image thumbnail.
	:type formatErrorImage: unicode
	"""
	missingImage = "images/Thumbnail_Not_Found.png"
	"""
	:param missingImage: Application missing image thumbnail.
	:type missingImage: unicode
	"""
	loadingImage = "images/Loading.png"
	"""
	:param loadingImage: Application loading image thumbnail.
	:type loadingImage: unicode
	"""

	startupLayout = "startupCentric"
	"""
	:param startupLayout: Application startup layout.
	:type startupLayout: unicode
	"""
	developmentLayout = "editCentric"
	"""
	:param developmentLayout: Application development layout.
	:type developmentLayout: unicode
	"""

	helpFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html"
	"""Application online help file:
	'**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html**' ( String )"""
	apiFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html"
	"""Application online api file:
	'**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html**' ( String )"""
	makeDonationFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Donations/Make_A_Donation.html"
	"""Application online donation file:
	'**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Donations/Make_A_Donation.html**' ( String )"""

	nativeImageFormats = {"Bmp" : "\.bmp$",
						"Jpeg" : "\.jpeg$",
						"Jpg" : "\.jpg$",
						"Png" : "\.png$" }
	"""
	:param nativeImageFormats: Application native image file formats.
	:type nativeImageFormats: dict
	"""

	thirdPartyImageFormats = {"Exr" : ("\.exr$"),
							"Hdr" : ("\.hdr$"),
							"Tif" : ("\.tif$"),
							"Tiff" : ("\.tiff$"),
							"Tga" : ("\.tga$")}
	"""
	:param thirdPartyImageFormats: Application third party image file formats.
	:type thirdPartyImageFormats: dict
	"""

	thumbnailsSizes = { "Default" : None,
					"XLarge" : 512,
					"Large" : 256,
					"Medium" : 128,
					"Small" : 64,
					"XSmall" : 32,
					"Special1" : 600}
	"""
	:param thumbnailsSizes: Application thumbnails sizes.
	:type thumbnailsSizes: dict
	"""

	thumbnailsCacheDirectory = "thumbnails"
	"""Thumbnails cache directory."""

	crittercismId = "51290b3589ea7429250004fe"
	"""
	:param crittercismId: Crittercism Id.
	:type crittercismId: unicode
	"""

