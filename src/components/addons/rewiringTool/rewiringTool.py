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
***	rewiringTool.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Rewiring Tool Addons Component Module.
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.parser
import foundations.strings as strings
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class RewiringTool(UiComponent):
	"""
	This Class Is The RewiringTool Class.
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
		self.deactivatable = True

		self.__uiPath = "ui/Rewiring_Tool.ui"
		self.__dockArea = 2

		self.__container = None

		self.__coreDatabaseBrowser = None

		self.__reWireFramesWidgets = None
		self.__reWireComboBoxesWidgets = None
		self.__reWireLineEditWidgets = None

		self.__addonsLoaderScript = None

		self.__rewiringParameters = (("Background", "Background|BGfile", "backgroundImage"),
									("Lighting", "Enviroment|EVfile", "lightingImage"),
									("Reflection", "Reflection|REFfile", "reflectionImage"),
									("Custom Image", None, None))

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
	def reWireFramesWidgets(self):
		"""
		This Method Is The Property For The _reWireFramesWidgets Attribute.

		@return: self.__reWireFramesWidgets. ( Tuple )
		"""

		return self.__reWireFramesWidgets

	@reWireFramesWidgets.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireFramesWidgets(self, value):
		"""
		This Method Is The Setter Method For The _reWireFramesWidgets Attribute.

		@param value: Attribute Value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("reWireFramesWidgets"))

	@reWireFramesWidgets.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireFramesWidgets(self):
		"""
		This Method Is The Deleter Method For The _reWireFramesWidgets Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("reWireFramesWidgets"))

	@property
	def reWireComboBoxesWidgets(self):
		"""
		This Method Is The Property For The _reWireComboBoxesWidgets Attribute.

		@return: self.__reWireComboBoxesWidgets. ( Tuple )
		"""

		return self.__reWireComboBoxesWidgets

	@reWireComboBoxesWidgets.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireComboBoxesWidgets(self, value):
		"""
		This Method Is The Setter Method For The _reWireComboBoxesWidgets Attribute.

		@param value: Attribute Value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("reWireComboBoxesWidgets"))

	@reWireComboBoxesWidgets.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireComboBoxesWidgets(self):
		"""
		This Method Is The Deleter Method For The _reWireComboBoxesWidgets Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("reWireComboBoxesWidgets"))

	@property
	def reWireLineEditWidgets(self):
		"""
		This Method Is The Property For The _reWireLineEditWidgets Attribute.

		@return: self.__reWireLineEditWidgets. ( Tuple )
		"""

		return self.__reWireLineEditWidgets

	@reWireLineEditWidgets.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireLineEditWidgets(self, value):
		"""
		This Method Is The Setter Method For The _reWireLineEditWidgets Attribute.

		@param value: Attribute Value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("reWireLineEditWidgets"))

	@reWireLineEditWidgets.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireLineEditWidgets(self):
		"""
		This Method Is The Deleter Method For The _reWireLineEditWidgets Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("reWireLineEditWidgets"))

	@property
	def rewiringParameters(self):
		"""
		This Method Is The Property For The _rewiringParameters Attribute.

		@return: self.__rewiringParameters. ( Tuple )
		"""

		return self.__rewiringParameters

	@rewiringParameters.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rewiringParameters(self, value):
		"""
		This Method Is The Setter Method For The _rewiringParameters Attribute.

		@param value: Attribute Value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("rewiringParameters"))

	@rewiringParameters.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rewiringParameters(self):
		"""
		This Method Is The Deleter Method For The _rewiringParameters Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("rewiringParameters"))

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
		self.__container = container

		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__addonsLoaderScript = self.__container.componentsManager.components["addons.loaderScript"].interface

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__container = None

		self.__coreDatabaseBrowser = None
		self.__addonsLoaderScript = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__reWireFramesWidgets = (self.ui.Background_frame, self.ui.Lighting_frame, self.ui.Reflection_frame)
		self.__reWireComboBoxesWidgets = (self.ui.Background_comboBox, self.ui.Lighting_comboBox, self.ui.Reflection_comboBox)
		self.__reWireLineEditWidgets = (self.ui.Background_Path_lineEdit, self.ui.Lighting_Path_lineEdit, self.ui.Reflection_Path_lineEdit)

		for frame in self.__reWireFramesWidgets:
			LOGGER.debug("> Hiding '%s'.", frame)
			frame.hide()

		for index in range(len(self.__reWireComboBoxesWidgets)):
			self.__reWireComboBoxesWidgets[index]._datas = self.__rewiringParameters[index][1]
			self.__reWireComboBoxesWidgets[index].addItems([parameter[0] for parameter in self.__rewiringParameters])
			self.__reWireComboBoxesWidgets[index].setCurrentIndex(index)

		# Signals / Slots.
		self.ui.Background_comboBox.activated.connect(self.setReWireWidgetFramesVisibility)
		self.ui.Lighting_comboBox.activated.connect(self.setReWireWidgetFramesVisibility)
		self.ui.Reflection_comboBox.activated.connect(self.setReWireWidgetFramesVisibility)
		self.ui.Background_Path_toolButton.clicked.connect(self.Background_Path_toolButton_OnClicked)
		self.ui.Lighting_Path_toolButton.clicked.connect(self.Lighting_Path_toolButton_OnClicked)
		self.ui.Reflection_Path_toolButton.clicked.connect(self.Reflection_Path_toolButton_OnClicked)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__reWireFramesWidgets = None
		self.__reWireComboBoxesWidgets = None
		self.__reWireLineEditWidgets = None

		# Signals / Slots.
		self.ui.Background_comboBox.activated.disconnect(self.setReWireWidgetFramesVisibility)
		self.ui.Lighting_comboBox.activated.disconnect(self.setReWireWidgetFramesVisibility)
		self.ui.Reflection_comboBox.activated.disconnect(self.setReWireWidgetFramesVisibility)
		self.ui.Background_Path_toolButton.clicked.disconnect(self.Background_Path_toolButton_OnClicked)
		self.ui.Lighting_Path_toolButton.clicked.disconnect(self.Lighting_Path_toolButton_OnClicked)
		self.ui.Reflection_Path_toolButton.clicked.disconnect(self.Reflection_Path_toolButton_OnClicked)

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self.ui)
		self.ui.setParent(None)

	@core.executionTrace
	def setReWireWidgetFramesVisibility(self, index):
		"""
		This Method Shows / Hides ReWire Widget Frames.

		@param index: ComboBox Index. ( Tuple )
		"""

		for index in range(len(self.__reWireComboBoxesWidgets)):
			if self.__reWireComboBoxesWidgets[index].currentText() == "Custom Image":
				LOGGER.debug("> Showing ReWire Frame '{0}'.".format(self.__reWireFramesWidgets[index]))
				self.__reWireFramesWidgets[index].show()
			else:
				LOGGER.debug("> Hiding ReWire Frame '{0}'.".format(self.__reWireFramesWidgets[index]))
				self.__reWireFramesWidgets[index].hide()

	@core.executionTrace
	def setReWireCustomPath(self, component):
		"""
		This Method Sets The ReWire Custom Image Line Edits.

		@param component: Target Component. ( String )
		"""

		customFile = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom " + component + " File:", self.__container.lastBrowsedPath))
		LOGGER.debug("> Chosen Custom '{0}': '{1}'.".format(component, customFile))
		if customFile != "":
			if component == "Background":
				self.ui.Background_Path_lineEdit.setText(QString(customFile))
			elif component == "Lighting":
				self.ui.Lighting_Path_lineEdit.setText(QString(customFile))
			elif component == "Reflection":
				self.ui.Reflection_Path_lineEdit.setText(QString(customFile))

	@core.executionTrace
	def Background_Path_toolButton_OnClicked(self, checked):
		"""
		This Method Is Called When Background ToolButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.setReWireCustomPath("Background")

	@core.executionTrace
	def Lighting_Path_toolButton_OnClicked(self, checked):
		"""
		This Method Is Called When Lighting ToolButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.setReWireCustomPath("Lighting")

	@core.executionTrace
	def Reflection_Path_toolButton_OnClicked(self, checked):
		"""
		This Method Is Called When Reflection ToolButton Is Clicked.

		@param checked: Checked State. ( Boolean )
		"""

		self.setReWireCustomPath("Reflection")

	@core.executionTrace
	def getOverrideKeys(self):
		"""
		This Method Gets Override Keys.
		"""

		LOGGER.info("{0} | Updating Loader Script Override Keys!".format(self.__class__.__name__))

		selectedIblSet = self.__coreDatabaseBrowser.getSelectedItems()
		iblSet = selectedIblSet and selectedIblSet[0] or None

		if iblSet:
			if os.path.exists(iblSet._datas.path):
				for index, comboBox in enumerate(self.__reWireComboBoxesWidgets):
					parameter = self.__rewiringParameters[comboBox.currentIndex()]
					if comboBox.currentText() == "Custom Image":
						LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format(comboBox._datas, str(self.__reWireLineEditWidgets[index].text())))
						self.__addonsLoaderScript.overrideKeys[comboBox._datas] = foundations.parser.getAttributeCompound(parameter[1], strings.getNormalizedPath(str(self.__reWireLineEditWidgets[index].text())))
					else:
						LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format(comboBox._datas, getattr(iblSet._datas, parameter[2])))
						self.__addonsLoaderScript.overrideKeys[comboBox._datas] = getattr(iblSet._datas, parameter[2]) and foundations.parser.getAttributeCompound(parameter[1], strings.getNormalizedPath(getattr(iblSet._datas, parameter[2])))

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
