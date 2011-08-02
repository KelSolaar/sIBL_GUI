#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**uiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	uiConstants Module.

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
	This class is the **UiConstants** class.
	"""

	frameworkUiFile = "./ui/sIBL_GUI.ui"
	frameworkWindowsStylesheetFile = "./ui/Windows_styleSheet.qss"
	frameworkDarwinStylesheetFile = "./ui/Darwin_styleSheet.qss"
	frameworkLinuxStylesheetFile = "./ui/Linux_styleSheet.qss"
	frameworkWindowsStyle = "plastique"
	frameworkDarwinStyle = "plastique"
	frameworkLinuxStyle = "plastique"
	frameworkLayoutsFile = "./ui/sIBL_GUI_Layouts.rc"

	frameworkApplicationWindowsIcon = "./resources/Icon_Light.png"
	frameworkApplicationDarwinIcon = "./resources/Icon_Light.png"

	frameworkSplashScreenPicture = "./resources/sIBL_GUI_SpashScreen.png"
	frameworkLogoPicture = "./resources/sIBL_GUI_Logo.png"

	frameworkDefaultToolbarIconSize = 32

	frameworCentralWidgetIcon = "./resources/Central_Widget.png"
	frameworCentralWidgetHoverIcon = "./resources/Central_Widget_Hover.png"
	frameworCentralWidgetActiveIcon = "./resources/Central_Widget_Active.png"

	frameworLayoutIcon = "./resources/Layout.png"
	frameworLayoutHoverIcon = "./resources/Layout_Hover.png"
	frameworLayoutActiveIcon = "./resources/Layout_Active.png"

	frameworMiscellaneousIcon = "./resources/Miscellaneous.png"
	frameworMiscellaneousHoverIcon = "./resources/Miscellaneous_Hover.png"
	frameworMiscellaneousActiveIcon = "./resources/Miscellaneous_Active.png"

	frameworkLibraryIcon = "./resources/Library.png"
	frameworkLibraryHoverIcon = "./resources/Library_Hover.png"
	frameworkLibraryActiveIcon = "./resources/Library_Active.png"

	frameworkInspectIcon = "./resources/Inspect.png"
	frameworkInspectHoverIcon = "./resources/Inspect_Hover.png"
	frameworkInspectActiveIcon = "./resources/Inspect_Active.png"

	frameworkExportIcon = "./resources/Export.png"
	frameworkExportHoverIcon = "./resources/Export_Hover.png"
	frameworkExportActiveIcon = "./resources/Export_Active.png"

	frameworkPreferencesIcon = "./resources/Preferences.png"
	frameworkPreferencesHoverIcon = "./resources/Preferences_Hover.png"
	frameworkPreferencesActiveIcon = "./resources/Preferences_Active.png"

	frameworkFormatErrorImage = "./resources/Thumbnail_Format_Not_Supported_Yet.png"
	frameworkMissingImage = "./resources/Thumbnail_Not_Found.png"

	frameworkStartupLayout = "startupCentric"

	frameworkHelpFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html"
	frameworkApiFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html"

	nativeImageFormats = { "Bmp" : "\.[bB][mM][pP]",
							"Jpeg" : "\.[jJ][pP][eE][gG]",
							"Jpg" : "\.[jJ][pP][gG]",
							"Png" : "\.[pP][nN][gG]" }

	thirdPartyImageFormats = { "Exr" : ("\.[eE][xX][rR]"),
								"Hdr" : ("\.[hH][dD][rR]"),
								"Tif" : ("\.[tT][iI][fF]"),
								"Tiff" : ("\.[tT][iI][fF][fF]"),
								"Tga" : ("\.[tT][gG][aA]")}