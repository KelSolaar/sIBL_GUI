#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**uiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Umbra** package ui constants through the :class:`UiConstants` class.

**Others:**

"""

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class UiConstants():
	"""
	This class provides **Umbra** package ui constants.
	"""

	frameworkUiFile = "./ui/sIBL_GUI.ui"
	"""Application ui file: '**./ui/sIBL_GUI.ui**' ( String )"""
	frameworkWindowsStylesheetFile = "./ui/Windows_styleSheet.qss"
	"""Application Windows Os stylesheet file: '**./ui/Windows_styleSheet.qss**' ( String )"""
	frameworkDarwinStylesheetFile = "./ui/Darwin_styleSheet.qss"
	"""Application Mac Os X Os stylesheet file: '**./ui/Darwin_styleSheet.qss**' ( String )"""
	frameworkLinuxStylesheetFile = "./ui/Linux_styleSheet.qss"
	"""Application Linux Os stylesheet file: '**./ui/Linux_styleSheet.qss**' ( String )"""
	frameworkWindowsStyle = "plastique"
	"""Application Windows Os style: '**plastique**' ( String )"""
	frameworkDarwinStyle = "plastique"
	"""Application Mac Os X Os style: '**plastique**' ( String )"""
	frameworkLinuxStyle = "plastique"
	"""Application Linux Os style: '**plastique**' ( String )"""
	frameworkLayoutsFile = "./ui/sIBL_GUI_Layouts.rc"
	"""Application defaults layouts file: '**./ui/sIBL_GUI_Layouts.rc**' ( String )"""

	frameworkApplicationWindowsIcon = "./resources/Icon_Light.png"
	"""Application Windows Os layouts file: '**./resources/Icon_Light.png**' ( String )"""
	frameworkApplicationDarwinIcon = "./resources/Icon_Light.png"
	"""Application Mac Os X Os layouts file: '**./resources/Icon_Light.png**' ( String )"""

	frameworkSplashScreenImage = "./resources/sIBL_GUI_SpashScreen.png"
	"""Application splashscreen image: '**./resources/sIBL_GUI_SpashScreen.png**' ( String )"""
	frameworkLogoImage = "./resources/sIBL_GUI_Logo.png"
	"""Application logo image: '**./resources/sIBL_GUI_Logo.png**' ( String )"""

	frameworkDefaultToolbarIconSize = 32
	"""Application toolbar icons size: '**32**' ( Integer )"""

	frameworkCentralWidgetIcon = "./resources/Central_Widget.png"
	"""Application **Central Widget** icon: '**./resources/Central_Widget.png**' ( String )"""
	frameworkCentralWidgetHoverIcon = "./resources/Central_Widget_Hover.png"
	"""Application **Central Widget** hover icon: '**./resources/Central_Widget_Hover.png**' ( String )"""
	frameworkCentralWidgetActiveIcon = "./resources/Central_Widget_Active.png"
	"""Application **Central Widget** active icon: '**./resources/Central_Widget_Active.png**' ( String )"""

	frameworkLayoutIcon = "./resources/Layout.png"
	"""Application **Layout** icon: '**./resources/Layout.png**' ( String )"""
	frameworkLayoutHoverIcon = "./resources/Layout_Hover.png"
	"""Application **Layout** hover icon: '**./resources/Layout_Hover.png**' ( String )"""
	frameworkLayoutActiveIcon = "./resources/Layout_Active.png"
	"""Application **Layout** active icon: '**./resources/Layout_Active.png**' ( String )"""

	frameworMiscellaneousIcon = "./resources/Miscellaneous.png"
	"""Application **Miscellaneous** icon: '**./resources/Miscellaneous.png**' ( String )"""
	frameworMiscellaneousHoverIcon = "./resources/Miscellaneous_Hover.png"
	"""Application **Miscellaneous** hover icon: '**./resources/Miscellaneous_Hover.png**' ( String )"""
	frameworMiscellaneousActiveIcon = "./resources/Miscellaneous_Active.png"
	"""Application **Miscellaneous** active icon: '**./resources/Miscellaneous_Active.png**' ( String )"""

	frameworkLibraryIcon = "./resources/Library.png"
	"""Application **Library** icon: '**./resources/Library.png**' ( String )"""
	frameworkLibraryHoverIcon = "./resources/Library_Hover.png"
	"""Application **Library** hover icon: '**./resources/Library_Hover.png**' ( String )"""
	frameworkLibraryActiveIcon = "./resources/Library_Active.png"
	"""Application **Library** active icon: '**./resources/Library_Active.png**' ( String )"""

	frameworkInspectIcon = "./resources/Inspect.png"
	"""Application **Inspect** icon: '**./resources/Inspect.png**' ( String )"""
	frameworkInspectHoverIcon = "./resources/Inspect_Hover.png"
	"""Application **Inspect** hover icon: '**./resources/Inspect_Hover.png**' ( String )"""
	frameworkInspectActiveIcon = "./resources/Inspect_Active.png"
	"""Application **Inspect** active icon: '**./resources/Inspect_Active.png**' ( String )"""

	frameworkExportIcon = "./resources/Export.png"
	"""Application **Export** icon: '**./resources/Export.png**' ( String )"""
	frameworkExportHoverIcon = "./resources/Export_Hover.png"
	"""Application **Export** hover icon: '**./resources/Export_Hover.png**' ( String )"""
	frameworkExportActiveIcon = "./resources/Export_Active.png"
	"""Application **Export** active icon: '**./resources/Export_Active.png**' ( String )"""

	frameworkPreferencesIcon = "./resources/Preferences.png"
	"""Application **Preferences** icon: '**./resources/Preferences.png**' ( String )"""
	frameworkPreferencesHoverIcon = "./resources/Preferences_Hover.png"
	"""Application **Preferences** hover icon: '**./resources/Preferences_Hover.png**' ( String )"""
	frameworkPreferencesActiveIcon = "./resources/Preferences_Active.png"
	"""Application **Preferences** active icon: '**./resources/Preferences_Active.png**' ( String )"""

	frameworkFormatErrorImage = "./resources/Thumbnail_Format_Not_Supported_Yet.png"
	"""Application format error image thumbnail: '**./resources/Thumbnail_Format_Not_Supported_Yet.png**' ( String )"""
	frameworkMissingImage = "./resources/Thumbnail_Not_Found.png"
	"""Application missing image thumbnail: '**./resources/Thumbnail_Not_Found.png**' ( String )"""

	frameworkStartupLayout = "startupCentric"
	"""Application startup layout: '**startupCentric**' ( String )"""

	frameworkHelpFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html"
	"""Application online help file: '**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html**' ( String )"""
	frameworkApiFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html"
	"""Application online api file: '**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html**' ( String )"""

	nativeImageFormats = { "Bmp" : "\.[bB][mM][pP]",
							"Jpeg" : "\.[jJ][pP][eE][gG]",
							"Jpg" : "\.[jJ][pP][gG]",
							"Png" : "\.[pP][nN][gG]" }
	"""Application native image file formats. ( Dictionary )"""

	thirdPartyImageFormats = { "Exr" : ("\.[eE][xX][rR]"),
								"Hdr" : ("\.[hH][dD][rR]"),
								"Tif" : ("\.[tT][iI][fF]"),
								"Tiff" : ("\.[tT][iI][fF][fF]"),
								"Tga" : ("\.[tT][gG][aA]")}
	"""Application third party image file formats. ( Dictionary )"""

	pythonTokensFile = "./ui/Python_Tokens.rc"
	"""Python tokens file: '**./ui/Python_Tokens.rc**' ( String )"""
