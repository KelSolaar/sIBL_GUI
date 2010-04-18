#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2010 - Thomas Mansencal - kelsolaar_fool@hotmail.com
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
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	uiConstants.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		uiConstants Module.
***
***	Others :
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import platform

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class UiConstants():
	'''
	This Class Is The UiConstants Class.
	'''

	frameworkUiFile = "./ui/sIBL_GUI.ui"
	frameworkLayoutsFile = "./ui/sIBL_GUI_Layouts.rc"
	frameworkSplashScreenPicture = "./resources/sIBL_GUI_SpashScreen.png"
	frameworkLogoPicture = "./resources/sIBL_GUI_Logo.png"
	frameworLayoutIcon = "./resources/sIBL_GUI_Layout.png"
	frameworCentralWidgetIcon = "./resources/sIBL_GUI_CentralWidget.png"
	frameworkMiscIcon = "./resources/sIBL_GUI_Misc.png"

	componentsDirectory = "components"

	frameworkHelpFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/index.html"
	frameworkApiFile = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html"

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
