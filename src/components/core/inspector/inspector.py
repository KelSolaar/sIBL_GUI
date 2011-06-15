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
import platform
import re
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import ui.common
import ui.widgets.messageBox as messageBox
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
		self._uiPreviousIcon = "Previous.png"
		self._uiNextIcon = "Next.png"
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
												<li>Check For An Updated Set On <b>HDRLabs</b> At <a href="http://www.hdrlabs.com/sibl/archive.html"><span style=" text-decoration: underline; color:#000000;">http://www.hdrlabs.com/sibl/archive.html</span></a>.</li>
												<li>Contact <b>{1}</b> At <a href="{2}"><span style=" text-decoration: underline; color:#000000;">{2}</span></a> For An Updated Set.</li>
												<li>Resize The Background Image To 600x300 Pixels. Save It As A JPEG In Your Set Folder.<br/>Register It In The ."Ibl" File Header Using The "PREVIEWfile" Attribute.</li>
											</ul>
										</td>
									</tr>
								</table>
								</center>
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
	def uiPreviousIcon(self):
		"""
		This Method Is The Property For The _uiPreviousIcon Attribute.

		@return: self._uiPreviousIcon. ( String )
		"""

		return self._uiPreviousIcon

	@uiPreviousIcon.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousIcon(self, value):
		"""
		This Method Is The Setter Method For The _uiPreviousIcon Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPreviousIcon"))

	@uiPreviousIcon.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousIcon(self):
		"""
		This Method Is The Deleter Method For The _uiPreviousIcon Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPreviousIcon"))

	@property
	def uiNextIcon(self):
		"""
		This Method Is The Property For The _uiNextIcon Attribute.

		@return: self._uiNextIcon. ( String )
		"""

		return self._uiNextIcon

	@uiNextIcon.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextIcon(self, value):
		"""
		This Method Is The Setter Method For The _uiNextIcon Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiNextIcon"))

	@uiNextIcon.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextIcon(self):
		"""
		This Method Is The Deleter Method For The _uiNextIcon Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiNextIcon"))

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
	
		self.ui.Previous_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiPreviousIcon)))
		self.ui.Next_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self._uiResources, self._uiNextIcon)))
		
		self.ui.Overall_frame.setStyleSheet("background: rgb(128, 128, 128)")
		self.ui.Title_frame.setStyleSheet("background: rgb(160, 160, 160)")
		#self.ui.Image_frame.setStyleSheet("background: rgb(128, 128, 128)")
		self.ui.Details_frame.setStyleSheet("background: rgb(160, 160, 160)")
		
		self.Inspector_setUi()
		
		# Signals / Slots.
		self._coreDatabaseBrowser.modelChanged.connect(self.coreDatabaseBrowser_model_OnModelChanged)
		self._coreDatabaseBrowser.ui.Database_Browser_listView.selectionModel().selectionChanged.connect(self.coreDatabaseBrowser_Database_Browser_listView_OnModelSelectionChanged)
		self.ui.Previous_Ibl_Set_pushButton.clicked.connect(self.Previous_Ibl_Set_pushButton_OnClicked)
		self.ui.Next_Ibl_Set_pushButton.clicked.connect(self.Next_Ibl_Set_pushButton_OnClicked)

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
	def Inspector_setUi(self):
		"""
		This Method Sets The Inspector Ui.
		"""

		self.setInspectorIblSet()
		
		if self._inspectorIblSet:
			if self._inspectorIblSet._datas.previewImage:
				self.ui.Image_label.setPixmap(QPixmap(self._inspectorIblSet._datas.previewImage))
			else:
				self.ui.Image_label.setText(self._noPreviewImageText.format(self._inspectorIblSet._datas.icon, self._inspectorIblSet._datas.author, self._inspectorIblSet._datas.link))
			
			self.ui.Title_label.setText("<center><b>{0}</b> - {1}</center>".format(self._inspectorIblSet._datas.title, self._inspectorIblSet._datas.location))
			self.ui.Details_label.setText("<center><b>Comment:</b> {0}</center>".format(self._inspectorIblSet._datas.comment))
	
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

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
