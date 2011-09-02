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

	frameworkUiFile = "./resources/Umbra.ui"
	"""Application ui file: '**./resources/Umbra.ui**' ( String )"""

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

	frameworkLayoutsFile = "./resources/layouts/Defaults_Layouts.rc"
	"""Application defaults layouts file: '**./resources/layouts/Defaults_Layouts.rc**' ( String )"""

	frameworkApplicationWindowsIcon = "./resources/images/Icon_Light.png"
	"""Application Windows Os layouts file: '**./resources/images/Icon_Light.png**' ( String )"""
	frameworkApplicationDarwinIcon = "./resources/images/Icon_Light.png"
	"""Application Mac Os X Os layouts file: '**./resources/images/Icon_Light.png**' ( String )"""

	frameworkSplashScreenImage = "./resources/images/Umbra_SpashScreen.png"
	"""Application splashscreen image: '**./resources/images/Umbra_SpashScreen.png**' ( String )"""
	frameworkLogoImage = "./resources/images/Umbra_Logo.png"
	"""Application logo image: '**./resources/images/Umbra_Logo.png**' ( String )"""

	frameworkDefaultToolbarIconSize = 32
	"""Application toolbar icons size: '**32**' ( Integer )"""

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

	frameworkDevelopmentIcon = "./resources/images/Development.png"
	"""Application **Development** icon: '**./resources/images/Development.png**' ( String )"""
	frameworkDevelopmentHoverIcon = "./resources/images/Development_Hover.png"
	"""Application **Development** hover icon: '**./resources/images/Development_Hover.png**' ( String )"""
	frameworkDevelopmentActiveIcon = "./resources/images/Development_Active.png"
	"""Application **Development** active icon: '**./resources/images/Development_Active.png**' ( String )"""

	frameworkPreferencesIcon = "./resources/images/Preferences.png"
	"""Application **Preferences** icon: '**./resources/images/Preferences.png**' ( String )"""
	frameworkPreferencesHoverIcon = "./resources/images/Preferences_Hover.png"
	"""Application **Preferences** hover icon: '**./resources/images/Preferences_Hover.png**' ( String )"""
	frameworkPreferencesActiveIcon = "./resources/images/Preferences_Active.png"
	"""Application **Preferences** active icon: '**./resources/images/Preferences_Active.png**' ( String )"""

	frameworkStartupLayout = "startupCentric"
	"""Application startup layout: '**startupCentric**' ( String )"""

	frameworkHelpFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html"
	"""Application online help file: '**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html**' ( String )"""
	frameworkApiFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html"
	"""Application online api file: '**http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html**' ( String )"""

	restoreGeometryOnLayoutChange = False
	"""Restore geometry on layout change: '**False**' ( Boolean )"""

	pythonTokensFile = "./resources/others/Python_Tokens.rc"
	"""Python tokens file: '**./resources/others/Python_Tokens.rc**' ( String )"""
