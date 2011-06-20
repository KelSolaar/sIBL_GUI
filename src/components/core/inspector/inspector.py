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
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from globals.constants import Constants
from globals.uiConstants import UiConstants
from libraries.freeImage.freeImage import Image
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
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
		self._uiFormatErrorImage = "Thumbnail_Format_Not_Supported_Yet.png"
		self._uiMissingImage = "Thumbnail_Not_Found.png"
		self._uiPreviousImage = "Previous.png"
		self._uiNextImage = "Next.png"
		self._dockArea = 2
	
		self._container = None
		self._settings = None
		self._settingsSection = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None
		
		self._inspectorIblSet = None
		
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
		self._toolTipText = """
								<p><b>{0}</b></p>
								<p><b>Author: </b>{1}<br>
								<b>Location: </b>{2}<br>
								<b>Shot Date: </b>{3}<br>
								<b>Comment: </b>{4}</p>
								"""
		
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
	def uiFormatErrorImage(self):
		"""
		This Method Is The Property For The _uiFormatErrorImage Attribute.

		@return: self._uiFormatErrorImage. ( String )
		"""

		return self._uiFormatErrorImage

	@uiFormatErrorImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiFormatErrorImage(self, value):
		"""
		This Method Is The Setter Method For The _uiFormatErrorImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiFormatErrorImage"))

	@uiFormatErrorImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiFormatErrorImage(self):
		"""
		This Method Is The Deleter Method For The _uiFormatErrorImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiFormatErrorImage"))

	@property
	def uiMissingImage(self):
		"""
		This Method Is The Property For The _uiMissingImage Attribute.

		@return: self._uiMissingImage. ( String )
		"""

		return self._uiMissingImage

	@uiMissingImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiMissingImage(self, value):
		"""
		This Method Is The Setter Method For The _uiMissingImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiMissingImage"))

	@uiMissingImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiMissingImage(self):
		"""
		This Method Is The Deleter Method For The _uiMissingImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiMissingImage"))

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
	def toolTipText(self):
		"""
		This Method Is The Property For The _toolTipText Attribute.

		@return: self._toolTipText. ( String )
		"""

		return self._toolTipText

	@toolTipText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolTipText(self, value):
		"""
		This Method Is The Setter Method For The _toolTipText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("toolTipText"))

	@toolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolTipText(self):
		"""
		This Method Is The Deleter Method For The _toolTipText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("toolTipText"))

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
		
		self.ui.Options_groupBox.hide()

		self.Inspector_setUi()
		
		# Signals / Slots.
		self._coreDatabaseBrowser.modelChanged.connect(self.coreDatabaseBrowser_model_OnModelChanged)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.selectionModel().selectionChanged.connect(self.coreDatabaseBrowser_Database_Browser_listView_OnModelSelectionChanged)
		self.ui.Previous_Ibl_Set_pushButton.clicked.connect(self.Previous_Ibl_Set_pushButton_OnClicked)
		self.ui.Next_Ibl_Set_pushButton.clicked.connect(self.Next_Ibl_Set_pushButton_OnClicked)
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
	
		self.Inspector_setUi()

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
	def Image_label_OnLinkActivated(self, url):
		"""
		This Method Is Triggered When A Link Is Clicked In The Image_label Widget.

		@param url: Url To Explore. ( QString )
		"""

		QDesktopServices.openUrl(QUrl(url))

	@core.executionTrace
	def Inspector_setUi(self):
		"""
		This Method Sets The Inspector Ui.
		"""

		self.setInspectorIblSet()
		
		if self._inspectorIblSet:
			iblSet = self._inspectorIblSet._datas

			self.ui.Title_label.setText("<center><b>{0}</b> - {1}</center>".format(iblSet.title, iblSet.location))
			
			if iblSet.previewImage:
				self.ui.Image_label.setPixmap(QPixmap(iblSet.previewImage))
			else:
				if os.path.exists(iblSet.icon):
					for extension in UiConstants.nativeImageFormats.values():
						if re.search(extension, iblSet.icon):
							iblSetIcon = iblSet.icon
							break
					else:
						iblSetIcon = os.path.join(self._uiResources, self._coreDatabaseBrowser.uiFormatErrorImage)
				else:
					iblSetIcon = os.path.join(self._uiResources, self._coreDatabaseBrowser.uiMissingImage)
				self.ui.Image_label.setText(self._noPreviewImageText.format(iblSetIcon, iblSet.author, iblSet.link))
			
			self.ui.Details_label.setText("<center><b>Comment:</b> {0}</center>".format(iblSet.comment))
			
			self.ui.Overall_frame.setToolTip(self._toolTipText.format(iblSet.title, iblSet.author or Constants.nullObject, iblSet.location or Constants.nullObject, self._coreDatabaseBrowser.getFormatedShotDate(iblSet.date, iblSet.time) or Constants.nullObject, iblSet.comment or Constants.nullObject))
		else:
			self.Inspector_clearUi()

	@core.executionTrace
	def Inspector_clearUi(self):
		"""
		This Method Clears The Inspector Ui.
		"""
		
		self.ui.Title_label.setText(QString())
		self.ui.Image_label.setText(self._noInspectorIblSetText.format(os.path.join(self._uiResources, self._coreDatabaseBrowser.uiMissingImage)))
		self.ui.Details_label.setText(QString())
		self.ui.Overall_frame.setToolTip(QString())

	@core.executionTrace
	def setInspectorIblSet(self):
		"""
		This Method Sets The Inspected Ibl Set.
		"""
		
		selectedIblSet = self._coreDatabaseBrowser.getSelectedItems()
		self._inspectorIblSet = selectedIblSet and selectedIblSet[0] or None
		if not self._inspectorIblSet:
			model = self._coreDatabaseBrowser.model
			self._inspectorIblSet = model.rowCount() !=0 and model.item(0) or None
				
	@core.executionTrace
	def loopThroughIblSets(self, backward=False):
		"""
		This Method Loops Through Database Browser Ibl Sets.
		
		@param direction: Loop Direction. ( String )
		"""
		
		if not self._inspectorIblSet:
			self.setInspectorIblSet()

		if self._inspectorIblSet:
			model = self._coreDatabaseBrowser.model
			index = model.indexFromItem(self._inspectorIblSet)
			
			step = not backward and 1 or -1
			idx = index.row() + step
			if idx < 0:
				idx = model.rowCount()-1
			elif idx > model.rowCount()-1:
				idx = 0
		
			selectionModel = self._coreDatabaseBrowser.ui.Database_Browser_listView.selectionModel()
			if selectionModel:
				selectionModel.clear()
				selectionModel.setCurrentIndex(index.sibling(idx, index.column()), QItemSelectionModel.Select)
		else:
			self.Inspector_clearUi()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
