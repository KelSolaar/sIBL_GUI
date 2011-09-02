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

	frameworkUiFile = "sIBL_GUI.ui"
	"""Application ui file: '**sIBL_GUI.ui**' ( String )"""

	frameworkWindowsStylesheetFile = "styles/Windows_styleSheet.qss"
	"""Application Windows Os stylesheet file: '**styles/Windows_styleSheet.qss**' ( String )"""
	frameworkDarwinStylesheetFile = "styles/Darwin_styleSheet.qss"
	"""Application Mac Os X Os stylesheet file: '**styles/Darwin_styleSheet.qss**' ( String )"""
	frameworkLinuxStylesheetFile = "styles/Linux_styleSheet.qss"
	"""Application Linux Os stylesheet file: '**styles/Linux_styleSheet.qss**' ( String )"""
	frameworkWindowsStyle = "plastique"
	"""Application Windows Os style: '**plastique**' ( String )"""
	frameworkDarwinStyle = "plastique"
	"""Application Mac Os X Os style: '**plastique**' ( String )"""
	frameworkLinuxStyle = "plastique"
	"""Application Linux Os style: '**plastique**' ( String )"""

	frameworkLayoutsFile = "layouts/sIBL_GUI_Layouts.rc"
	"""Application defaults layouts file: '**layouts/Defaults_Layouts.rc**' ( String )"""

	frameworkApplicationWindowsIcon = "images/Icon_Light.png"
	"""Application Windows Os layouts file: '**images/Icon_Light.png**' ( String )"""
	frameworkApplicationDarwinIcon = "images/Icon_Light.png"
	"""Application Mac Os X Os layouts file: '**images/Icon_Light.png**' ( String )"""

	frameworkSplashScreenImage = "images/sIBL_GUI_SpashScreen.png"
	"""Application splashscreen image: '**images/sIBL_GUI_SpashScreen.png**' ( String )"""
	frameworkLogoImage = "images/sIBL_GUI_Logo.png"
	"""Application logo image: '**images/sIBL_GUI_Logo.png**' ( String )"""

	frameworkDefaultToolbarIconSize = 32
	"""Application toolbar icons size: '**32**' ( Integer )"""

	frameworkCentralWidgetIcon = "images/Central_Widget.png"
	"""Application **Central Widget** icon: '**images/Central_Widget.png**' ( String )"""
	frameworkCentralWidgetHoverIcon = "images/Central_Widget_Hover.png"
	"""Application **Central Widget** hover icon: '**images/Central_Widget_Hover.png**' ( String )"""
	frameworkCentralWidgetActiveIcon = "images/Central_Widget_Active.png"
	"""Application **Central Widget** active icon: '**images/Central_Widget_Active.png**' ( String )"""

	frameworkLayoutIcon = "images/Layout.png"
	"""Application **Layout** icon: '**images/Layout.png**' ( String )"""
	frameworkLayoutHoverIcon = "images/Layout_Hover.png"
	"""Application **Layout** hover icon: '**images/Layout_Hover.png**' ( String )"""
	frameworkLayoutActiveIcon = "images/Layout_Active.png"
	"""Application **Layout** active icon: '**images/Layout_Active.png**' ( String )"""

	frameworMiscellaneousIcon = "images/Miscellaneous.png"
	"""Application **Miscellaneous** icon: '**images/Miscellaneous.png**' ( String )"""
	frameworMiscellaneousHoverIcon = "images/Miscellaneous_Hover.png"
	"""Application **Miscellaneous** hover icon: '**images/Miscellaneous_Hover.png**' ( String )"""
	frameworMiscellaneousActiveIcon = "images/Miscellaneous_Active.png"
	"""Application **Miscellaneous** active icon: '**images/Miscellaneous_Active.png**' ( String )"""

	frameworkLibraryIcon = "images/Library.png"
	"""Application **Library** icon: '**images/Library.png**' ( String )"""
	frameworkLibraryHoverIcon = "images/Library_Hover.png"
	"""Application **Library** hover icon: '**images/Library_Hover.png**' ( String )"""
	frameworkLibraryActiveIcon = "images/Library_Active.png"
	"""Application **Library** active icon: '**images/Library_Active.png**' ( String )"""

	frameworkInspectIcon = "images/Inspect.png"
	"""Application **Inspect** icon: '**images/Inspect.png**' ( String )"""
	frameworkInspectHoverIcon = "images/Inspect_Hover.png"
	"""Application **Inspect** hover icon: '**images/Inspect_Hover.png**' ( String )"""
	frameworkInspectActiveIcon = "images/Inspect_Active.png"
	"""Application **Inspect** active icon: '**images/Inspect_Active.png**' ( String )"""

	frameworkExportIcon = "images/Export.png"
	"""Application **Export** icon: '**images/Export.png**' ( String )"""
	frameworkExportHoverIcon = "images/Export_Hover.png"
	"""Application **Export** hover icon: '**images/Export_Hover.png**' ( String )"""
	frameworkExportActiveIcon = "images/Export_Active.png"
	"""Application **Export** active icon: '**images/Export_Active.png**' ( String )"""

	frameworkPreferencesIcon = "images/Preferences.png"
	"""Application **Preferences** icon: '**images/Preferences.png**' ( String )"""
	frameworkPreferencesHoverIcon = "images/Preferences_Hover.png"
	"""Application **Preferences** hover icon: '**images/Preferences_Hover.png**' ( String )"""
	frameworkPreferencesActiveIcon = "images/Preferences_Active.png"
	"""Application **Preferences** active icon: '**images/Preferences_Active.png**' ( String )"""

	frameworkFormatErrorImage = "images/Thumbnail_Format_Not_Supported_Yet.png"
	"""Application format error image thumbnail: '**images/Thumbnail_Format_Not_Supported_Yet.png**' ( String )"""
	frameworkMissingImage = "images/Thumbnail_Not_Found.png"
	"""Application missing image thumbnail: '**images/Thumbnail_Not_Found.png**' ( String )"""

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

	pythonTokensFile = "others/Python_Tokens.rc"
	"""Python tokens file: '**others/Python_Tokens.rc**' ( String )"""
