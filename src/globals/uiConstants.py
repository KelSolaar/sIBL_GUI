#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
************************************************************************************************
***	uiConstants.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		uiConstants Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class UiConstants():
	"""
	This Class Is The UiConstants Class.
	"""

	frameworkUiFile = "./ui/sIBL_GUI.ui"
	frameworkWindowsStylesheetFile = "./ui/Windows_styleSheet.qss"
	frameworkDarwinStylesheetFile = "./ui/Darwin_styleSheet.qss"
	frameworkLinuxStylesheetFile = "./ui/Linux_styleSheet.qss"
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

	frameworkStartupLayout = "startupCentric"

	frameworkHelpFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html"
	frameworkApiFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html"

	nativeImageFormats = { 	"Bmp" : "\.[bB][mM][pP]",
							"Jpeg" : "\.[jJ][pP][eE][gG]",
							"Jpg" : "\.[jJ][pP][gG]",
							"Png" : "\.[pP][nN][gG]" }

	thirdPartyImageFormats = { 	"Exr" : ("\.[eE][xX][rR]"),
								"Hdr" : ("\.[hH][dD][rR]"),
								"Tif" : ("\.[tT][iI][fF]"),
								"Tiff" : ("\.[tT][iI][fF][fF]"),
								"Tga" : ("\.[tT][gG][aA]")
								 }

#***********************************************************************************************
#***	Python End
#***********************************************************************************************

