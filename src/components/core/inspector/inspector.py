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
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import ui.common
from foundations.parser import Parser
from globals.constants import Constants
from globals.uiConstants import UiConstants
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

		self._uiPath = "ui/Inspector.ui"
		self._uiResources = "resources"
		self._uiPreviousImage = "Previous.png"
		self._uiNextImage = "Next.png"
		self._dockArea = 2
		self._listViewIconSize = 32

		self._container = None
		self._settings = None
		self._settingsSection = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None

		self._model = None

		self._inspectorIblSet = None
		self._inspectorIblSetParser = None
		self._inspectorPlates = None

		self._noPreviewImageText = """
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
												<li>Resize The Background Image To 600x300 Pixels. Save It As A JPEG In Your Set Folder.<br/>Register It In The ."Ibl" File Header Using The "PREVIEWfile" Attribute.</li>
											</ul>
										</td>
									</tr>
								</table>
								</center>
								"""
		self._noInspectorIblSetText = """
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
		self._inspectorIblSetToolTipText = """
								<p><b>{0}</b></p>
								<p><b>Author: </b>{1}<br>
								<b>Location: </b>{2}<br>
								<b>Shot Date: </b>{3}<br>
								<b>Comment: </b>{4}</p>
								"""
		self._inspectorIblSetPlatesToolTipText = """
								<p><b>{0}</b></p>
								"""

		self._lightLabelRadius = 6
		self._lightLabelTextOffset = 24
		self._lightLabelTextMargin = 16
		self._lightLabelTextHeight = 14
		self._lightLabelTextFont = "Helvetica"

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		"""

		return self._uiPath

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

		@return: self._uiResources. ( String )
		"""

		return self._uiResources

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

		@return: self._uiPreviousImage. ( String )
		"""

		return self._uiPreviousImage

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

		@return: self._uiNextImage. ( String )
		"""

		return self._uiNextImage

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

		@return: self._dockArea. ( Integer )
		"""

		return self._dockArea

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

		@return: self._listViewIconSize. ( Integer )
		"""

		return self._listViewIconSize

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
		self._listViewIconSize = value

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

		@return: self._container. ( QObject )
		"""

		return self._container

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

		@return: self._coreDatabaseBrowser. ( Object )
		"""

		return self._coreDatabaseBrowser

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

		@return: self._model. ( QStandardItemModel )
		"""

		return self._model

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

		@return: self._inspectorIblSet. ( QStandardItem )
		"""

		return self._inspectorIblSet

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

		@return: self._inspectorIblSetParser. ( Parser )
		"""

		return self._inspectorIblSetParser

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

		@return: self._inspectorPlates. ( Dictionary )
		"""

		return self._inspectorPlates

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

		@return: self._noPreviewImageText. ( String )
		"""

		return self._noPreviewImageText

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

		@return: self._noInspectorIblSetText. ( String )
		"""

		return self._noInspectorIblSetText

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

		@return: self._inspectorIblSetToolTipText. ( String )
		"""

		return self._inspectorIblSetToolTipText

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

		@return: self._inspectorIblSetPlatesToolTipText. ( String )
		"""

		return self._inspectorIblSetPlatesToolTipText

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

		@return: self._lightLabelRadius. ( Integer )
		"""

		return self._lightLabelRadius

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

		@return: self._lightLabelTextOffset. ( Integer )
		"""

		return self._lightLabelTextOffset

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

		@return: self._lightLabelTextMargin. ( Integer )
		"""

		return self._lightLabelTextMargin

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

		@return: self._lightLabelTextHeight. ( Integer )
		"""

		return self._lightLabelTextHeight

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

		@return: self._lightLabelTextFont. ( String )
		"""

		return self._lightLabelTextFont

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

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiPath)
		self._uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiResources)
		self._container = container
		self._settings = self._container.settings
		self._settingsSection = self.name

		self._corePreferencesManager = self._container.componentsManager.components["core.preferencesManager"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Cannot Be Deactivated!".format(self._name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))


		self.ui.Previous_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiPreviousImage)))
		self.ui.Next_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiNextImage)))
		self.ui.Previous_Plate_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiPreviousImage)))
		self.ui.Next_Plate_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiNextImage)))

		self.ui.Plates_frame.hide()
		self.ui.Options_groupBox.hide()

		self._model = QStandardItemModel()
		self.Plates_listView_setModel()
		self.Plates_listView_setView()

		self.Inspector_DockWidget_setUi()

		# Signals / Slots.
		self.ui.Plates_listView.selectionModel().selectionChanged.connect(self.Plates_listView_OnModelSelectionChanged)
		self._coreDatabaseBrowser.modelChanged.connect(self.coreDatabaseBrowser_model_OnModelChanged)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.selectionModel().selectionChanged.connect(self.coreDatabaseBrowser_Database_Browser_listView_OnModelSelectionChanged)
		self.ui.Previous_Ibl_Set_pushButton.clicked.connect(self.Previous_Ibl_Set_pushButton_OnClicked)
		self.ui.Next_Ibl_Set_pushButton.clicked.connect(self.Next_Ibl_Set_pushButton_OnClicked)
		self.ui.Previous_Plate_pushButton.clicked.connect(self.Previous_Plate_pushButton_OnClicked)
		self.ui.Next_Plate_pushButton.clicked.connect(self.Next_Plate_pushButton_OnClicked)
		self.ui.Image_label.linkActivated.connect(self.Image_label_OnLinkActivated)

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

		self._container.addDockWidget(Qt.DockWidgetArea(self._dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget Cannot Be Removed!".format(self.name))

	@core.executionTrace
	def Inspector_DockWidget_setUi(self):
		"""
		This Method Sets The Inspector DockWidget Ui.
		"""

		if self._inspectorIblSet:
			iblSet = self._inspectorIblSet._datas

			self.ui.Title_label.setText("<center><b>{0}</b> - {1}</center>".format(iblSet.title, iblSet.location))

			if iblSet.previewImage:
				self.ui.Image_label.setPixmap(ui.common.getPixmap(iblSet.previewImage))
				self.drawInspectorIblSetOverlay()
			else:
				self.ui.Image_label.setText(self._noPreviewImageText.format(ui.common.filterImagePath(iblSet.icon), iblSet.author, iblSet.link))

			self.ui.Image_label.setToolTip(self._inspectorIblSetToolTipText.format(iblSet.title, iblSet.author or Constants.nullObject, iblSet.location or Constants.nullObject, self._coreDatabaseBrowser.getFormatedShotDate(iblSet.date, iblSet.time) or Constants.nullObject, iblSet.comment or Constants.nullObject))

			self.ui.Details_label.setText("<center><b>Comment:</b> {0}</center>".format(iblSet.comment))

			if self._inspectorPlates:
				self.ui.Plates_frame.show()
			else:
				self.ui.Plates_frame.hide()
		else:
			self.Inspector_DockWidget_clearUi()

	@core.executionTrace
	def Inspector_DockWidget_clearUi(self):
		"""
		This Method Clears The Inspector DockWidget Ui.
		"""

		self.ui.Title_label.setText(QString())
		self.ui.Image_label.setText(self._noInspectorIblSetText.format(ui.common.filterImagePath("")))
		self.ui.Image_label.setToolTip(QString())
		self.ui.Details_label.setText(QString())

		self.ui.Plates_frame.hide()

	@core.executionTrace
	def Plates_listView_setModel(self):
		"""
		This Method Sets The Plates_listView Model.
		"""

		LOGGER.debug("> Setting Up '{0}' Model!".format("Plates_listView"))

		self._model.clear()

		if self._inspectorIblSet:
			iblSet = self._inspectorIblSet._datas
			LOGGER.debug("> Preparing '{0}' Ibl Set For '{1}' Model.".format(iblSet.name, "Plates_listView"))
			inspectorIblSetStandardItem = QStandardItem()
			inspectorIblSetStandardItem.setIcon(ui.common.getIcon(self._inspectorIblSet._datas.icon))
			inspectorIblSetStandardItem.setToolTip(self._inspectorIblSetToolTipText.format(iblSet.title, iblSet.author or Constants.nullObject, iblSet.location or Constants.nullObject, self._coreDatabaseBrowser.getFormatedShotDate(iblSet.date, iblSet.time) or Constants.nullObject, iblSet.comment or Constants.nullObject))
			self._model.appendRow(inspectorIblSetStandardItem)

			for name, plate in self._inspectorPlates.items():
				LOGGER.debug("> Preparing '{0}' Plate For '{1}' Model.".format(name, "Plates_listView"))
				try:
					plateStandardItem = QStandardItem()
					plateStandardItem.setIcon(ui.common.getIcon(plate.icon))
					plateStandardItem.setToolTip(self._inspectorIblSetPlatesToolTipText.format(plate.name))

					plateStandardItem._datas = plate

					LOGGER.debug("> Adding '{0}' To '{1}' Model.".format(name, "Plates_listView"))
					self._model.appendRow(plateStandardItem)

				except Exception as error:
					LOGGER.error("!>{0} | Exception Raised While Adding '{1}' Plate To '{2}' Model!".format(self.__class__.__name__, name, "Plates_listView"))
					foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "Plates_listView"))

	@core.executionTrace
	def Plates_listView_setView(self):
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

		self.Plates_listView_setItemsSize()

		self.ui.Plates_listView.setModel(self._model)

	@core.executionTrace
	def Plates_listView_setItemsSize(self):
		"""
		This Method Scales The Plates_listView Item Size.
		"""

		LOGGER.debug("> Setting '{0}' View Item Size To: {1}.".format("Plates_listView", self._listViewIconSize))

		self.ui.Plates_listView.setIconSize(QSize(self._listViewIconSize, self._listViewIconSize))

	@core.executionTrace
	def Plates_listView_OnModelSelectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Sets Is Triggered When  Plates_listView Selection Has Changed.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""

		index = selectedItems.indexes() and selectedItems.indexes()[0] or None
		item = index and self._model.itemFromIndex(index) or None
		if item:
			if hasattr(item, "_datas"):
				self.ui.Image_label.setPixmap(ui.common.getPixmap(item._datas.previewImage))
			else:
				self.Inspector_DockWidget_setUi()

	@core.executionTrace
	def coreDatabaseBrowser_model_OnModelChanged(self):
		"""
		This Method Sets Is Triggered When coreDatabaseBrowser Model Has Changed.
		"""

		self.setInspectorIblSet()

	@core.executionTrace
	def coreDatabaseBrowser_Database_Browser_listView_OnModelSelectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Sets Is Triggered When coreDatabaseBrowser_Database_Browser_listView Selection Has Changed.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""

		self.setInspectorIblSet()

		self.setInspectorIblSetPlates()
		self.Plates_listView_setModel()

		if self._inspectorIblSet:
			self.Inspector_DockWidget_setUi()
		else:
			self.Inspector_DockWidget_clearUi()

	@core.executionTrace
	def Previous_Ibl_Set_pushButton_OnClicked(self, checked):
		"""
		This Method Is Triggered When Previous_Ibl_Set_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughIblSets(True)

	@core.executionTrace
	def Next_Ibl_Set_pushButton_OnClicked(self, checked):
		"""
		This Method Is Triggered When Next_Ibl_Set_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughIblSets()

	@core.executionTrace
	def Previous_Plate_pushButton_OnClicked(self, checked):
		"""
		This Method Is Triggered When Previous_Plate_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughPlates(True)

	@core.executionTrace
	def Next_Plate_pushButton_OnClicked(self, checked):
		"""
		This Method Is Triggered When Next_Plate_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.loopThroughPlates()

	@core.executionTrace
	def Image_label_OnLinkActivated(self, url):
		"""
		This Method Is Triggered When A Link Is Clicked In The Image_label Widget.

		@param url: Url To Explore. ( QString )
		"""

		QDesktopServices.openUrl(QUrl(url))

	@core.executionTrace
	def setInspectorIblSet(self):
		"""
		This Method Sets The Inspected Ibl Set.
		"""

		selectedIblSet = self._coreDatabaseBrowser.getSelectedItems()
		self._inspectorIblSet = selectedIblSet and selectedIblSet[0] or None
		if not self._inspectorIblSet:
			model = self._coreDatabaseBrowser.model
			self._inspectorIblSet = model.rowCount() != 0 and model.item(0) or None
		self._inspectorIblSet and self.setInspectorIblSetParser()

	@core.executionTrace
	def setInspectorIblSetParser(self):
		"""
		This Method Sets The Inspected Ibl Set Parser.
		"""

		if os.path.exists(self._inspectorIblSet._datas.path):
			LOGGER.debug("> Parsing Inspected Ibl Set File: '{0}'.".format(self._inspectorIblSet))
			self._inspectorIblSetParser = Parser(self._inspectorIblSet._datas.path)
			self._inspectorIblSetParser.read() and self._inspectorIblSetParser.parse()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def setInspectorIblSetPlates(self):
		"""
		This Method Sets The Plates From The Inspected Ibl Set.
		"""

		if self._inspectorIblSet:
			if os.path.exists(self._inspectorIblSet._datas.path):
				self._inspectorPlates = OrderedDict()
				for section in self._inspectorIblSetParser.sections:
					if re.search("Plate[0-9]+", section):
						self._inspectorPlates[section] = Plate(name=os.path.splitext(self._inspectorIblSetParser.getValue("PLATEfile", section))[0],
																icon=os.path.normpath(os.path.join(os.path.dirname(self._inspectorIblSet._datas.path), self._inspectorIblSetParser.getValue("PLATEthumb", section))),
																previewImage=os.path.normpath(os.path.join(os.path.dirname(self._inspectorIblSet._datas.path), self._inspectorIblSetParser.getValue("PLATEpreview", section))),
																image=os.path.normpath(os.path.join(os.path.dirname(self._inspectorIblSet._datas.path), self._inspectorIblSetParser.getValue("PLATEfile", section))))
			else:
				raise OSError, "{0} | Exception Raised While Retrieving Plates: '{1}' Ibl Set File Doesn't Exists, !".format(self.__class__.__name__, self._inspectorIblSet._datas.name)

	@core.executionTrace
	def drawInspectorIblSetOverlay(self):
		"""
		This Method Draws An Overlay On .
		"""

		painter = QPainter(self.ui.Image_label.pixmap())
		painter.setRenderHints(QPainter.Antialiasing)
		for section in self._inspectorIblSetParser.sections:
				if section == "Sun":
					self.drawLightLabel(painter, Light(name="Sun",
														color=[int(value)for value in self._inspectorIblSetParser.getValue("SUNcolor", section).split(",")],
														uCoordinate=float(self._inspectorIblSetParser.getValue("SUNu", section)),
														vCoordinate=float(self._inspectorIblSetParser.getValue("SUNv", section))))
				elif re.search("Light[0-9]+", section):
					self.drawLightLabel(painter, Light(name=self._inspectorIblSetParser.getValue("LIGHTname", section),
														color=[int(value)for value in self._inspectorIblSetParser.getValue("LIGHTcolor", section).split(",")],
														uCoordinate=float(self._inspectorIblSetParser.getValue("LIGHTu", section)),
														vCoordinate=float(self._inspectorIblSetParser.getValue("LIGHTv", section))))
		painter.end()

	@core.executionTrace
	def drawLightLabel(self, painter, light):
		"""
		This Method Draws A Light Label On Provided QPainter.

		@param painter: QPainter. ( QPainter )
		@param light: Light. ( Light )
		"""

		width = painter.window().width()
		height = painter.window().height()

		painter.setPen(QColor(light.color[0], light.color[1], light.color[2]))
		painter.setBrush(QColor(light.color[0], light.color[1], light.color[2]))
		painter.setFont(QFont(self._lightLabelTextFont, self._lightLabelTextHeight))

		x = int(light.uCoordinate * width)
		y = int(light.vCoordinate * height)

		textWidth = painter.fontMetrics().width(light.name.title())
		xLabelTextOffset = x + textWidth + self._lightLabelTextMargin + self._lightLabelTextOffset > width and - (self._lightLabelTextOffset + textWidth) or self._lightLabelTextOffset
		yLabelTextOffset = y - (self._lightLabelTextHeight + self._lightLabelTextMargin + self._lightLabelTextOffset) < 0 and - (self._lightLabelTextOffset + self._lightLabelTextHeight) or self._lightLabelTextOffset
		painter.drawText(x + xLabelTextOffset, y - yLabelTextOffset, light.name.title())

		painter.drawLine(x, y, x + (xLabelTextOffset < 0 and xLabelTextOffset + textWidth or xLabelTextOffset), y - (yLabelTextOffset < 0 and yLabelTextOffset + self._lightLabelTextHeight or yLabelTextOffset))

		painter.drawEllipse(QPoint(x, y), self._lightLabelRadius, self._lightLabelRadius)

	@core.executionTrace
	def loopThroughIblSets(self, backward=False):
		"""
		This Method Loops Through Database Browser Ibl Sets.
		
		@param backward: Looping Backward. ( Boolean )
		"""

		if self._inspectorIblSet:
			model = self._coreDatabaseBrowser.model
			index = model.indexFromItem(self._inspectorIblSet)

			step = not backward and 1 or - 1
			idx = index.row() + step
			if idx < 0:
				idx = model.rowCount() - 1
			elif idx > model.rowCount() - 1:
				idx = 0

			selectionModel = self._coreDatabaseBrowser.ui.Database_Browser_listView.selectionModel()
			selectionModel.clear()
			selectionModel.setCurrentIndex(index.sibling(idx, index.column()), QItemSelectionModel.Select)
		else:
			self.Inspector_DockWidget_clearUi()

	@core.executionTrace
	def loopThroughPlates(self, backward=False):
		"""
		This Method Loops Through Inspector Plates.
		
		@param backward: Looping Backward. ( Boolean )
		"""

		index = self.ui.Plates_listView.selectedIndexes() and self.ui.Plates_listView.selectedIndexes()[0] or None
		if index:
			step = not backward and 1 or - 1
			idx = index.row() + step
			if idx < 0:
				idx = self._model.rowCount() - 1
			elif idx > self._model.rowCount() - 1:
				idx = 0

			selectionModel = self.ui.Plates_listView.selectionModel()
			selectionModel.clear()
			selectionModel.setCurrentIndex(index.sibling(idx, index.column()), QItemSelectionModel.Select)
		else:
			self.ui.Plates_listView.setCurrentIndex(self._model.index(0, 0))

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
