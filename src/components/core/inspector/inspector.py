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
***	preview.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Inspector Component Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
import re
from collections import OrderedDict
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import ui.common
from foundations.parser import Parser
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Plate(core.Structure):
	"""
	This Is The Plate Class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This Method Initializes The Class.

		@param kwargs: name, icon, previewImage, image ( Key / Value Pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting Class Attributes. ---
		self.__dict__.update(kwargs)

class Light(core.Structure):
	"""
	This Is The Light Class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This Method Initializes The Class.

		@param kwargs: name, color, uCoordinate, vCoordinate ( Key / Value Pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting Class Attributes. ---
		self.__dict__.update(kwargs)

class Inspector(UiComponent):
	"""
	This Class Is The Preview Class.
	"""

	# Custom Signals Definitions.
	modelRefresh = pyqtSignal()
	uiRefresh = pyqtSignal()
	uiClear = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
		self.deactivatable = False

		self.__uiPath = "ui/Inspector.ui"
		self.__uiResources = "resources"
		self.__uiPreviousImage = "Previous.png"
		self.__uiNextImage = "Next.png"
		self.__dockArea = 2
		self.__listViewIconSize = 30

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None

		self.__model = None

		self.__inspectorIblSet = None
		self.__inspectorIblSetParser = None
		self.__inspectorPlates = None

		self.__noPreviewImageText = """
								<center>
								<table border="0" bordercolor="" cellpadding="0" cellspacing="16">
									<tr>
										<td>
											<img src="{0}">
										</td>
										<td>
											<p><b>Preview Image Unavailable!<b></p>
											What Now?
											<ul>
												<li>Check For An Updated Set On <b>HDRLabs</b> At <a href="http://www.hdrlabs.com/sibl/archive.html"><span style=" text-decoration: underline; color:#e0e0e0;">http://www.hdrlabs.com/sibl/archive.html</span></a>.</li>
												<li>Contact <b>{1}</b> At <a href="{2}"><span style=" text-decoration: underline; color:#e0e0e0;">{2}</span></a> For An Updated Set.</li>
												<li>Resize The Background Image To 600x300 Pixels. Save It As A JPEG In Your Set Directory.<br/>Register It In The ."Ibl" File Header Using The "PREVIEWfile" Attribute.</li>
											</ul>
										</td>
									</tr>
								</table>
								</center>
								"""
		self.__noInspectorIblSetText = """
								<center>
								<table border="0" bordercolor="" cellpadding="0" cellspacing="16">
									<tr>
										<td>
											<img src="{0}">
										</td>
										<td>
											<p><b>No Ibl Set To Inspect!<b></p>
											Please Add some Ibl Set To The Database Or Select A Non Empty Collection!
										</td>
									</tr>
								</table>
								</center>
								"""
		self.__inspectorIblSetToolTipText = """
								<p><b>{0}</b></p>
								<p><b>Author: </b>{1}<br>
								<b>Location: </b>{2}<br>
								<b>Shot Date: </b>{3}<br>
								<b>Comment: </b>{4}</p>
								"""
		self.__inspectorIblSetPlatesToolTipText = """
								<p><b>{0}</b></p>
								"""

		self.__lightLabelRadius = 4
		self.__lightLabelTextOffset = 24
		self.__lightLabelTextMargin = 16
		self.__lightLabelTextHeight = 14
		self.__lightLabelTextFont = "Helvetica"

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This Method Is The Property For The _uiResources Attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This Method Is The Deleter Method For The _uiResources Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def uiPreviousImage(self):
		"""
		This Method Is The Property For The _uiPreviousImage Attribute.

		@return: self.__uiPreviousImage. ( String )
		"""

		return self.__uiPreviousImage

	@uiPreviousImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self, value):
		"""
		This Method Is The Setter Method For The _uiPreviousImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self):
		"""
		This Method Is The Deleter Method For The _uiPreviousImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPreviousImage"))

	@property
	def uiNextImage(self):
		"""
		This Method Is The Property For The _uiNextImage Attribute.

		@return: self.__uiNextImage. ( String )
		"""

		return self.__uiNextImage

	@uiNextImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self, value):
		"""
		This Method Is The Setter Method For The _uiNextImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self):
		"""
		This Method Is The Deleter Method For The _uiNextImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiNextImage"))

	@property
	def dockArea(self):
		"""
		This Method Is The Property For The _dockArea Attribute.

		@return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This Method Is The Deleter Method For The _dockArea Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dockArea"))

	@property
	def listViewIconSize(self):
		"""
		This Method Is The Property For The _listViewIconSize Attribute.

		@return: self.__listViewIconSize. ( Integer )
		"""

		return self.__listViewIconSize

	@listViewIconSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def listViewIconSize(self, value):
		"""
		This Method Is The Setter Method For The _listViewIconSize Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' Attribute: '{1}' Type Is Not 'int'!".format("listViewIconSize", value)
			assert value > 0, "'{0}' Attribute: '{1}' Need To Be Exactly Positive!".format("listViewIconSize", value)
		self.__listViewIconSize = value

	@listViewIconSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def listViewIconSize(self):
		"""
		This Method Is The Deleter Method For The _listViewIconSize Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("listViewIconSize"))

	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDatabaseBrowser"))

	@property
	def model(self):
		"""
		This Method Is The Property For The _model Attribute.

		@return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This Method Is The Setter Method For The _model Attribute.

		@param value: Attribute Value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This Method Is The Deleter Method For The _model Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("model"))

	@property
	def inspectorIblSet(self):
		"""
		This Method Is The Property For The _inspectorIblSet Attribute.

		@return: self.__inspectorIblSet. ( QStandardItem )
		"""

		return self.__inspectorIblSet

	@inspectorIblSet.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSet(self, value):
		"""
		This Method Is The Setter Method For The _inspectorIblSet Attribute.

		@param value: Attribute Value. ( QStandardItem )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("inspectorIblSet"))

	@inspectorIblSet.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSet(self):
		"""
		This Method Is The Deleter Method For The _inspectorIblSet Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("inspectorIblSet"))

	@property
	def inspectorIblSetParser(self):
		"""
		This Method Is The Property For The _inspectorIblSetParser Attribute.

		@return: self.__inspectorIblSetParser. ( Parser )
		"""

		return self.__inspectorIblSetParser

	@inspectorIblSetParser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetParser(self, value):
		"""
		This Method Is The Setter Method For The _inspectorIblSetParser Attribute.

		@param value: Attribute Value. ( Parser )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("inspectorIblSetParser"))

	@inspectorIblSetParser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetParser(self):
		"""
		This Method Is The Deleter Method For The _inspectorIblSetParser Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("inspectorIblSetParser"))

	@property
	def inspectorPlates(self):
		"""
		This Method Is The Property For The _inspectorPlates Attribute.

		@return: self.__inspectorPlates. ( Dictionary )
		"""

		return self.__inspectorPlates

	@inspectorPlates.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorPlates(self, value):
		"""
		This Method Is The Setter Method For The _inspectorPlates Attribute.

		@param value: Attribute Value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("inspectorPlates"))

	@inspectorPlates.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorPlates(self):
		"""
		This Method Is The Deleter Method For The _inspectorPlates Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("inspectorPlates"))

	@property
	def noPreviewImageText(self):
		"""
		This Method Is The Property For The _noPreviewImageText Attribute.

		@return: self.__noPreviewImageText. ( String )
		"""

		return self.__noPreviewImageText

	@noPreviewImageText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noPreviewImageText(self, value):
		"""
		This Method Is The Setter Method For The _noPreviewImageText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("noPreviewImageText"))

	@noPreviewImageText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noPreviewImageText(self):
		"""
		This Method Is The Deleter Method For The _noPreviewImageText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("noPreviewImageText"))

	@property
	def noInspectorIblSetText(self):
		"""
		This Method Is The Property For The _noInspectorIblSetText Attribute.

		@return: self.__noInspectorIblSetText. ( String )
		"""

		return self.__noInspectorIblSetText

	@noInspectorIblSetText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noInspectorIblSetText(self, value):
		"""
		This Method Is The Setter Method For The _noInspectorIblSetText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("noInspectorIblSetText"))

	@noInspectorIblSetText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noInspectorIblSetText(self):
		"""
		This Method Is The Deleter Method For The _noInspectorIblSetText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("noInspectorIblSetText"))

	@property
	def inspectorIblSetToolTipText(self):
		"""
		This Method Is The Property For The _inspectorIblSetToolTipText Attribute.

		@return: self.__inspectorIblSetToolTipText. ( String )
		"""

		return self.__inspectorIblSetToolTipText

	@inspectorIblSetToolTipText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetToolTipText(self, value):
		"""
		This Method Is The Setter Method For The _inspectorIblSetToolTipText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("inspectorIblSetToolTipText"))

	@inspectorIblSetToolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetToolTipText(self):
		"""
		This Method Is The Deleter Method For The _inspectorIblSetToolTipText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("inspectorIblSetToolTipText"))

	@property
	def inspectorIblSetPlatesToolTipText(self):
		"""
		This Method Is The Property For The _inspectorIblSetPlatesToolTipText Attribute.

		@return: self.__inspectorIblSetPlatesToolTipText. ( String )
		"""

		return self.__inspectorIblSetPlatesToolTipText

	@inspectorIblSetPlatesToolTipText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetPlatesToolTipText(self, value):
		"""
		This Method Is The Setter Method For The _inspectorIblSetPlatesToolTipText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("inspectorIblSetPlatesToolTipText"))

	@inspectorIblSetPlatesToolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetPlatesToolTipText(self):
		"""
		This Method Is The Deleter Method For The _inspectorIblSetPlatesToolTipText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("inspectorIblSetPlatesToolTipText"))

	@property
	def lightLabelRadius(self):
		"""
		This Method Is The Property For The _lightLabelRadius Attribute.

		@return: self.__lightLabelRadius. ( Integer )
		"""

		return self.__lightLabelRadius

	@lightLabelRadius.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelRadius(self, value):
		"""
		This Method Is The Setter Method For The _lightLabelRadius Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("lightLabelRadius"))

	@lightLabelRadius.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelRadius(self):
		"""
		This Method Is The Deleter Method For The _lightLabelRadius Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("lightLabelRadius"))

	@property
	def lightLabelTextOffset(self):
		"""
		This Method Is The Property For The _lightLabelTextOffset Attribute.

		@return: self.__lightLabelTextOffset. ( Integer )
		"""

		return self.__lightLabelTextOffset

	@lightLabelTextOffset.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextOffset(self, value):
		"""
		This Method Is The Setter Method For The _lightLabelTextOffset Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("lightLabelTextOffset"))

	@lightLabelTextOffset.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextOffset(self):
		"""
		This Method Is The Deleter Method For The _lightLabelTextOffset Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("lightLabelTextOffset"))

	@property
	def lightLabelTextMargin(self):
		"""
		This Method Is The Property For The _lightLabelTextMargin Attribute.

		@return: self.__lightLabelTextMargin. ( Integer )
		"""

		return self.__lightLabelTextMargin

	@lightLabelTextMargin.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextMargin(self, value):
		"""
		This Method Is The Setter Method For The _lightLabelTextMargin Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("lightLabelTextMargin"))

	@lightLabelTextMargin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextMargin(self):
		"""
		This Method Is The Deleter Method For The _lightLabelTextMargin Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("lightLabelTextMargin"))

	@property
	def lightLabelTextHeight(self):
		"""
		This Method Is The Property For The _lightLabelTextHeight Attribute.

		@return: self.__lightLabelTextHeight. ( Integer )
		"""

		return self.__lightLabelTextHeight

	@lightLabelTextHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextHeight(self, value):
		"""
		This Method Is The Setter Method For The _lightLabelTextHeight Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("lightLabelTextHeight"))

	@lightLabelTextHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextHeight(self):
		"""
		This Method Is The Deleter Method For The _lightLabelTextHeight Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("lightLabelTextHeight"))

	@property
	def lightLabelTextFont(self):
		"""
		This Method Is The Property For The _lightLabelTextFont Attribute.

		@return: self.__lightLabelTextFont. ( String )
		"""

		return self.__lightLabelTextFont

	@lightLabelTextFont.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextFont(self, value):
		"""
		This Method Is The Setter Method For The _lightLabelTextFont Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("lightLabelTextFont"))

	@lightLabelTextFont.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextFont(self):
		"""
		This Method Is The Deleter Method For The _lightLabelTextFont Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("lightLabelTextFont"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__corePreferencesManager = self.__container.componentsManager.components["core.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Cannot Be Deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))


		self.ui.Previous_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiPreviousImage)))
		self.ui.Next_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiNextImage)))
		self.ui.Previous_Plate_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiPreviousImage)))
		self.ui.Next_Plate_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiNextImage)))

		self.ui.Plates_frame.hide()
		self.ui.Inspector_Options_groupBox.hide()

		self.__model = QStandardItemModel()
		self.__Plates_listView_setModel()
		self.__Plates_listView_setView()

		self.__Inspector_DockWidget_setUi()

		self.ui.Inspector_Overall_frame.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Inspector_Overall_frame_addActions()

		# Signals / Slots.
		self.ui.Plates_listView.selectionModel().selectionChanged.connect(self.__Plates_listView_selectionModel__selectionChanged)
		self.__coreDatabaseBrowser.modelChanged.connect(self.__coreDatabaseBrowser__modelChanged)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.selectionModel().selectionChanged.connect(self.__coreDatabaseBrowser_Database_Browser_listView_selectionModel__selectionChanged)
		self.ui.Previous_Ibl_Set_pushButton.clicked.connect(self.__Previous_Ibl_Set_pushButton__clicked)
		self.ui.Next_Ibl_Set_pushButton.clicked.connect(self.__Next_Ibl_Set_pushButton__clicked)
		self.ui.Previous_Plate_pushButton.clicked.connect(self.__Previous_Plate_pushButton__clicked)
		self.ui.Next_Plate_pushButton.clicked.connect(self.__Next_Plate_pushButton__clicked)
		self.ui.Image_label.linkActivated.connect(self.__Image_label__linkActivated)
		self.modelRefresh.connect(self.__Plates_listView_refreshModel)
		self.uiRefresh.connect(self.__Inspector_DockWidget_refreshUi)
		self.uiClear.connect(self.__Inspector_DockWidget_clearUi)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Ui Cannot Be Uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget Cannot Be Removed!".format(self.name))

	@core.executionTrace
	def __Inspector_DockWidget_setUi(self):
		"""
		This Method Sets The Inspector DockWidget Ui.
		"""

		if self.__inspectorIblSet:

			self.ui.Title_label.setText("<center><b>{0}</b> - {1}</center>".format(self.__inspectorIblSet.title, self.__inspectorIblSet.location))

			if self.__inspectorIblSet.previewImage:
				self.ui.Image_label.setPixmap(ui.common.getPixmap(self.__inspectorIblSet.previewImage))
				self.__drawInspectorIblSetOverlay()
			else:
				self.ui.Image_label.setText(self.__noPreviewImageText.format(ui.common.filterImagePath(self.__inspectorIblSet.icon), self.__inspectorIblSet.author, self.__inspectorIblSet.link))

			self.ui.Image_label.setToolTip(self.__inspectorIblSetToolTipText.format(self.__inspectorIblSet.title, self.__inspectorIblSet.author or Constants.nullObject, self.__inspectorIblSet.location or Constants.nullObject, self.__coreDatabaseBrowser.getFormatedShotDate(self.__inspectorIblSet.date, self.__inspectorIblSet.time) or Constants.nullObject, self.__inspectorIblSet.comment or Constants.nullObject))

			self.ui.Details_label.setText("<center><b>Comment:</b> {0}</center>".format(self.__inspectorIblSet.comment))

			if self.__inspectorPlates:
				self.ui.Plates_frame.show()
			else:
				self.ui.Plates_frame.hide()
		else:
			self.__Inspector_DockWidget_clearUi()

	@core.executionTrace
	def __Inspector_DockWidget_refreshUi(self):
		"""
		This Method Sets The Inspector DockWidget Ui.
		"""

		self.__Inspector_DockWidget_setUi()

	@core.executionTrace
	def __Inspector_DockWidget_clearUi(self):
		"""
		This Method Clears The Inspector DockWidget Ui.
		"""

		self.ui.Title_label.setText(QString())
		self.ui.Image_label.setText(self.__noInspectorIblSetText.format(ui.common.filterImagePath("")))
		self.ui.Image_label.setToolTip(QString())
		self.ui.Details_label.setText(QString())

		self.ui.Plates_frame.hide()

	@core.executionTrace
	def __Plates_listView_setModel(self):
		"""
		This Method Sets The Plates_listView Model.
		"""

		LOGGER.debug("> Setting Up '{0}' Model!".format("Plates_listView"))

		self.__model.clear()

		if self.__inspectorIblSet:
			LOGGER.debug("> Preparing '{0}' Ibl Set For '{1}' Model.".format(self.__inspectorIblSet.name, "Plates_listView"))
			inspectorIblSetStandardItem = QStandardItem()
			inspectorIblSetStandardItem.setIcon(ui.common.getIcon(self.__inspectorIblSet.icon))
			inspectorIblSetStandardItem.setToolTip(self.__inspectorIblSetToolTipText.format(self.__inspectorIblSet.title, self.__inspectorIblSet.author or Constants.nullObject, self.__inspectorIblSet.location or Constants.nullObject, self.__coreDatabaseBrowser.getFormatedShotDate(self.__inspectorIblSet.date, self.__inspectorIblSet.time) or Constants.nullObject, self.__inspectorIblSet.comment or Constants.nullObject))
			self.__model.appendRow(inspectorIblSetStandardItem)

			for name, plate in self.__inspectorPlates.items():
				LOGGER.debug("> Preparing '{0}' Plate For '{1}' Model.".format(name, "Plates_listView"))
				try:
					plateStandardItem = QStandardItem()
					plateStandardItem.setIcon(ui.common.getIcon(plate.icon))
					plateStandardItem.setToolTip(self.__inspectorIblSetPlatesToolTipText.format(plate.name))

					plateStandardItem._datas = plate

					LOGGER.debug("> Adding '{0}' To '{1}' Model.".format(name, "Plates_listView"))
					self.__model.appendRow(plateStandardItem)

				except Exception as error:
					LOGGER.error("!>{0} | Exception Raised While Adding '{1}' Plate To '{2}' Model!".format(self.__class__.__name__, name, "Plates_listView"))
					foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "Plates_listView"))

	@core.executionTrace
	def __Plates_listView_refreshModel(self):
		"""
		This Method Refreshes The Plates_listView Model.
		"""

		self.__Plates_listView_setModel()

	@core.executionTrace
	def __Plates_listView_setView(self):
		"""
		This Method Sets The Plates_listView Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Widget!".format("Plates_listView"))

		self.ui.Plates_listView.setAcceptDrops(False)
		self.ui.Plates_listView.setAutoScroll(True)
		self.ui.Plates_listView.setFlow(QListView.LeftToRight)
		self.ui.Plates_listView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.ui.Plates_listView.setMovement(QListView.Static)
		self.ui.Plates_listView.setSelectionMode(QAbstractItemView.SingleSelection)
		self.ui.Plates_listView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.ui.Plates_listView.setViewMode(QListView.IconMode)
		self.ui.Plates_listView.setWrapping(False)

		self.__Plates_listView_setDefaultViewState()

		self.ui.Plates_listView.setModel(self.__model)

	@core.executionTrace
	def __Plates_listView_setDefaultViewState(self):
		"""
		This Method Scales The Plates_listView Item Size.
		"""

		LOGGER.debug("> Setting '{0}' View Item Size To: {1}.".format("Plates_listView", self.__listViewIconSize))

		self.ui.Plates_listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.ui.Plates_listView.setIconSize(QSize(self.__listViewIconSize, self.__listViewIconSize))

	@core.executionTrace
	def __Inspector_Overall_frame_addActions(self):
		"""
		This Method Sets The Inspector_Overall_frame Actions.
		"""

		pass

	@core.executionTrace
	def __Plates_listView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Sets Is Triggered When Plates_listView Model Selection Has Changed.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""

		index = selectedItems.indexes() and selectedItems.indexes()[0] or None
		item = index and self.__model.itemFromIndex(index) or None
		if item:
			if hasattr(item, "_datas"):
				self.ui.Image_label.setPixmap(ui.common.getPixmap(item._datas.previewImage))
			else:
				self.emit(SIGNAL("uiRefresh()"))

	@core.executionTrace
	def __coreDatabaseBrowser__modelChanged(self):
		"""
		This Method Sets Is Triggered When coreDatabaseBrowser Model Has Changed.
		"""

		self.__setInspectorIblSet()

	@core.executionTrace
	def __coreDatabaseBrowser_Database_Browser_listView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Sets Is Triggered When coreDatabaseBrowser Database_Browser_listView Model Selection Has Changed.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""

		self.__setInspectorIblSet()

		self.__setInspectorIblSetPlates()
		self.emit(SIGNAL("modelRefresh()"))

		if self.__inspectorIblSet:
			self.emit(SIGNAL("uiRefresh()"))
		else:
			self.emit(SIGNAL("uiClear()"))

	@core.executionTrace
	def __Previous_Ibl_Set_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Previous_Ibl_Set_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughIblSets(True)

	@core.executionTrace
	def __Next_Ibl_Set_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Next_Ibl_Set_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughIblSets()

	@core.executionTrace
	def __Previous_Plate_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Previous_Plate_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughPlates(True)

	@core.executionTrace
	def __Next_Plate_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Next_Plate_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughPlates()

	@core.executionTrace
	def __Image_label__linkActivated(self, url):
		"""
		This Method Is Triggered When A Link Is Clicked In The Image_label Widget.

		@param url: Url To Explore. ( QString )
		"""

		QDesktopServices.openUrl(QUrl(url))

	@core.executionTrace
	def __setInspectorIblSet(self):
		"""
		This Method Sets The Inspector Ibl Set.
		"""

		selectedIblSet = self.__coreDatabaseBrowser.getSelectedIblSets()
		self.__inspectorIblSet = selectedIblSet and selectedIblSet[0] or None
		if not self.__inspectorIblSet:
			model = self.__coreDatabaseBrowser.model
			self.__inspectorIblSet = model.rowCount() != 0 and model.item(0)._datas or None
		self.__inspectorIblSet and self.__setInspectorIblSetParser()

	@core.executionTrace
	def __setInspectorIblSetParser(self):
		"""
		This Method Sets The Inspector Ibl Set Parser.
		"""

		if os.path.exists(self.__inspectorIblSet.path):
			LOGGER.debug("> Parsing Inspector Ibl Set File: '{0}'.".format(self.__inspectorIblSet))
			self.__inspectorIblSetParser = Parser(self.__inspectorIblSet.path)
			self.__inspectorIblSetParser.read() and self.__inspectorIblSetParser.parse()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def __setInspectorIblSetPlates(self):
		"""
		This Method Sets The Plates From The Inspector Ibl Set.
		"""

		if self.__inspectorIblSet:
			if os.path.exists(self.__inspectorIblSet.path):
				self.__inspectorPlates = OrderedDict()
				for section in self.__inspectorIblSetParser.sections:
					if re.search("Plate[0-9]+", section):
						self.__inspectorPlates[section] = Plate(name=strings.getSplitextBasename(self.__inspectorIblSetParser.getValue("PLATEfile", section)),
																icon=os.path.normpath(os.path.join(os.path.dirname(self.__inspectorIblSet.path), self.__inspectorIblSetParser.getValue("PLATEthumb", section))),
																previewImage=os.path.normpath(os.path.join(os.path.dirname(self.__inspectorIblSet.path), self.__inspectorIblSetParser.getValue("PLATEpreview", section))),
																image=os.path.normpath(os.path.join(os.path.dirname(self.__inspectorIblSet.path), self.__inspectorIblSetParser.getValue("PLATEfile", section))))
			else:
				raise OSError, "{0} | Exception Raised While Retrieving Plates: '{1}' Ibl Set File Doesn't Exists!".format(self.__class__.__name__, self.__inspectorIblSet.title)

	@core.executionTrace
	def __drawInspectorIblSetOverlay(self):
		"""
		This Method Draws An Overlay On .
		"""

		painter = QPainter(self.ui.Image_label.pixmap())
		painter.setRenderHints(QPainter.Antialiasing)
		for section in self.__inspectorIblSetParser.sections:
				if section == "Sun":
					self.__drawLightLabel(painter, Light(name="Sun",
													color=[int(value)for value in self.__inspectorIblSetParser.getValue("SUNcolor", section).split(",")],
													uCoordinate=float(self.__inspectorIblSetParser.getValue("SUNu", section)),
													vCoordinate=float(self.__inspectorIblSetParser.getValue("SUNv", section))))
				elif re.search("Light[0-9]+", section):
					self.__drawLightLabel(painter, Light(name=self.__inspectorIblSetParser.getValue("LIGHTname", section),
													color=[int(value)for value in self.__inspectorIblSetParser.getValue("LIGHTcolor", section).split(",")],
													uCoordinate=float(self.__inspectorIblSetParser.getValue("LIGHTu", section)),
													vCoordinate=float(self.__inspectorIblSetParser.getValue("LIGHTv", section))))
		painter.end()

	@core.executionTrace
	def __drawLightLabel(self, painter, light):
		"""
		This Method Draws A Light Label On Provided QPainter.

		@param painter: QPainter. ( QPainter )
		@param light: Light. ( Light )
		"""

		width = painter.window().width()
		height = painter.window().height()

		painter.setBrush(QColor(light.color[0], light.color[1], light.color[2], 200))
		painter.setPen(QPen(QBrush(QColor(light.color[0], light.color[1], light.color[2], 200)), 2))
		font = QFont(self.__lightLabelTextFont, self.__lightLabelTextHeight)
		font.setBold(True)
		painter.setFont(font)

		x = int(light.uCoordinate * width)
		y = int(light.vCoordinate * height)

		textWidth = painter.fontMetrics().width(light.name.title())
		xLabelTextOffset = x + textWidth + self.__lightLabelTextMargin + self.__lightLabelTextOffset > width and - (self.__lightLabelTextOffset + textWidth) or self.__lightLabelTextOffset
		yLabelTextOffset = y - (self.__lightLabelTextHeight + self.__lightLabelTextMargin + self.__lightLabelTextOffset) < 0 and - (self.__lightLabelTextOffset + self.__lightLabelTextHeight) or self.__lightLabelTextOffset
		painter.drawText(x + xLabelTextOffset, y - yLabelTextOffset, light.name.title())

		painter.drawLine(x, y, x + (xLabelTextOffset < 0 and xLabelTextOffset + textWidth or xLabelTextOffset), y - (yLabelTextOffset < 0 and yLabelTextOffset + self.__lightLabelTextHeight or yLabelTextOffset))

		painter.drawEllipse(QPoint(x, y), self.__lightLabelRadius, self.__lightLabelRadius)

		painter.setBrush(Qt.NoBrush)
		painter.setPen(QPen(QBrush(QColor(light.color[0], light.color[1], light.color[2], 100)), 2))
		painter.drawEllipse(QPoint(x, y), self.__lightLabelRadius * 3, self.__lightLabelRadius * 3)
		painter.setPen(QPen(QBrush(QColor(light.color[0], light.color[1], light.color[2], 50)), 2))
		painter.drawEllipse(QPoint(x, y), self.__lightLabelRadius * 4, self.__lightLabelRadius * 4)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, Exception)
	def loopThroughIblSets(self, backward=False):
		"""
		This Method Loops Through Database Browser Ibl Sets.
		
		@param backward: Looping Backward. ( Boolean )
		@return: Method Success. ( Boolean )	
		"""

		if self.__inspectorIblSet:
			iblSetStandardItems = [iblSetStandardItem for iblSetStandardItem in self.__coreDatabaseBrowser.model.findItems("*", Qt.MatchWildcard | Qt.MatchRecursive, 0) if iblSetStandardItem._datas.path == self.__inspectorIblSet.path]
			inspectorIblSetStandardItem = iblSetStandardItems and iblSetStandardItems[0] or None
			if not inspectorIblSetStandardItem: return True

			model = self.__coreDatabaseBrowser.model
			index = model.indexFromItem(inspectorIblSetStandardItem)

			step = not backward and 1 or - 1
			idx = index.row() + step
			if idx < 0:
				idx = model.rowCount() - 1
			elif idx > model.rowCount() - 1:
				idx = 0

			selectionModel = self.__coreDatabaseBrowser.ui.Database_Browser_listView.selectionModel()
			selectionModel.clear()
			selectionModel.setCurrentIndex(index.sibling(idx, index.column()), QItemSelectionModel.Select)
		else:
			self.emit(SIGNAL("uiClear()"))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, Exception)
	def loopThroughPlates(self, backward=False):
		"""
		This Method Loops Through Inspector Plates.
		
		@param backward: Looping Backward. ( Boolean )
		@return: Method Success. ( Boolean )	
		"""

		index = self.ui.Plates_listView.selectedIndexes() and self.ui.Plates_listView.selectedIndexes()[0] or None
		if index:
			step = not backward and 1 or - 1
			idx = index.row() + step
			if idx < 0:
				idx = self.__model.rowCount() - 1
			elif idx > self.__model.rowCount() - 1:
				idx = 0

			selectionModel = self.ui.Plates_listView.selectionModel()
			selectionModel.clear()
			selectionModel.setCurrentIndex(index.sibling(idx, index.column()), QItemSelectionModel.Select)
		else:
			self.ui.Plates_listView.setCurrentIndex(self.__model.index(0, 0))
		return True

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
