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

	frameworkUiFile = "./resources/sIBL_GUI.ui"
	"""Application ui file: '**./resources/sIBL_GUI.ui**' ( String )"""

	frameworkWindowsStylesheetFile = "./resources/styles/Windows_styleSheet.qss"
	"""Application Windows Os stylesheet file: '**./resources/styles/Windows_styleSheet.qss**' ( String )"""
	frameworkDarwinStylesheetFile = "./resources/styles/Darwin_styleSheet.qss"
	"""Application Mac Os X Os stylesheet file: '**./resources/styles/Darwin_styleSheet.qss**' ( String )"""
	frameworkLinuxStylesheetFile = "./resources/styles/Linux_styleSheet.qss"
	"""Application Linux Os stylesheet file: '**./resources/styles/Linux_styleSheet.qss**' ( String )"""
	frameworkWindowsStyle = "plastique"
	"""Application Windows Os style: '**plastique**' ( String )"""
	frameworkDarwinStyle = "plastique"
	"""Application Mac Os X Os style: '**plastique**' ( String )"""
	frameworkLinuxStyle = "plastique"
	"""Application Linux Os style: '**plastique**' ( String )"""

	frameworkLayoutsFile = "./resources/layouts/sIBL_GUI_Layouts.rc"
	"""Application defaults layouts file: '**./resources/layouts/Defaults_Layouts.rc**' ( String )"""

	frameworkApplicationWindowsIcon = "./resources/images/Icon_Light.png"
	"""Application Windows Os layouts file: '**./resources/images/Icon_Light.png**' ( String )"""
	frameworkApplicationDarwinIcon = "./resources/images/Icon_Light.png"
	"""Application Mac Os X Os layouts file: '**./resources/images/Icon_Light.png**' ( String )"""

	frameworkSplashScreenImage = "./resources/images/sIBL_GUI_SpashScreen.png"
	"""Application splashscreen image: '**./resources/images/sIBL_GUI_SpashScreen.png**' ( String )"""
	frameworkLogoImage = "./resources/images/sIBL_GUI_Logo.png"
	"""Application logo image: '**./resources/images/sIBL_GUI_Logo.png**' ( String )"""

	frameworkDefaultToolbarIconSize = 32
	"""Application toolbar icons size: '**32**' ( Integer )"""

	frameworkCentralWidgetIcon = "./resources/images/Central_Widget.png"
	"""Application **Central Widget** icon: '**./resources/images/Central_Widget.png**' ( String )"""
	frameworkCentralWidgetHoverIcon = "./resources/images/Central_Widget_Hover.png"
	"""Application **Central Widget** hover icon: '**./resources/images/Central_Widget_Hover.png**' ( String )"""
	frameworkCentralWidgetActiveIcon = "./resources/images/Central_Widget_Active.png"
	"""Application **Central Widget** active icon: '**./resources/images/Central_Widget_Active.png**' ( String )"""

	frameworkLayoutIcon = "./resources/images/Layout.png"
	"""Application **Layout** icon: '**./resources/images/Layout.png**' ( String )"""
	frameworkLayoutHoverIcon = "./resources/images/Layout_Hover.png"
	"""Application **Layout** hover icon: '**./resources/images/Layout_Hover.png**' ( String )"""
	frameworkLayoutActiveIcon = "./resources/images/Layout_Active.png"
	"""Application **Layout** active icon: '**./resources/images/Layout_Active.png**' ( String )"""

	frameworMiscellaneousIcon = "./resources/images/Miscellaneous.png"
	"""Application **Miscellaneous** icon: '**./resources/images/Miscellaneous.png**' ( String )"""
	frameworMiscellaneousHoverIcon = "./resources/images/Miscellaneous_Hover.png"
	"""Application **Miscellaneous** hover icon: '**./resources/images/Miscellaneous_Hover.png**' ( String )"""
	frameworMiscellaneousActiveIcon = "./resources/images/Miscellaneous_Active.png"
	"""Application **Miscellaneous** active icon: '**./resources/images/Miscellaneous_Active.png**' ( String )"""

	frameworkLibraryIcon = "./resources/images/Library.png"
	"""Application **Library** icon: '**./resources/images/Library.png**' ( String )"""
	frameworkLibraryHoverIcon = "./resources/images/Library_Hover.png"
	"""Application **Library** hover icon: '**./resources/images/Library_Hover.png**' ( String )"""
	frameworkLibraryActiveIcon = "./resources/images/Library_Active.png"
	"""Application **Library** active icon: '**./resources/images/Library_Active.png**' ( String )"""

	frameworkInspectIcon = "./resources/images/Inspect.png"
	"""Application **Inspect** icon: '**./resources/images/Inspect.png**' ( String )"""
	frameworkInspectHoverIcon = "./resources/images/Inspect_Hover.png"
	"""Application **Inspect** hover icon: '**./resources/images/Inspect_Hover.png**' ( String )"""
	frameworkInspectActiveIcon = "./resources/images/Inspect_Active.png"
	"""Application **Inspect** active icon: '**./resources/images/Inspect_Active.png**' ( String )"""

	frameworkExportIcon = "./resources/images/Export.png"
	"""Application **Export** icon: '**./resources/images/Export.png**' ( String )"""
	frameworkExportHoverIcon = "./resources/images/Export_Hover.png"
	"""Application **Export** hover icon: '**./resources/images/Export_Hover.png**' ( String )"""
	frameworkExportActiveIcon = "./resources/images/Export_Active.png"
	"""Application **Export** active icon: '**./resources/images/Export_Active.png**' ( String )"""

	frameworkPreferencesIcon = "./resources/images/Preferences.png"
	"""Application **Preferences** icon: '**./resources/images/Preferences.png**' ( String )"""
	frameworkPreferencesHoverIcon = "./resources/images/Preferences_Hover.png"
	"""Application **Preferences** hover icon: '**./resources/images/Preferences_Hover.png**' ( String )"""
	frameworkPreferencesActiveIcon = "./resources/images/Preferences_Active.png"
	"""Application **Preferences** active icon: '**./resources/images/Preferences_Active.png**' ( String )"""

	frameworkFormatErrorImage = "./resources/images/Thumbnail_Format_Not_Supported_Yet.png"
	"""Application format error image thumbnail: '**./resources/images/Thumbnail_Format_Not_Supported_Yet.png**' ( String )"""
	frameworkMissingImage = "./resources/images/Thumbnail_Not_Found.png"
	"""Application missing image thumbnail: '**./resources/images/Thumbnail_Not_Found.png**' ( String )"""

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

	pythonTokensFile = "./resources/others/Python_Tokens.rc"
	"""Python tokens file: '**./resources/others/Python_Tokens.rc**' ( String )"""
