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
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	loaderScriptOptions.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Loader Script Options Component Module.
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
import logging
import os
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.parser
import foundations.strings as strings
import ui.widgets.messageBox as messageBox
from foundations.parser import Parser
from globals.constants import Constants
from manager.uiComponent import UiComponent
from ui.widgets.variable_QPushButton import Variable_QPushButton

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class LoaderScriptOptions(UiComponent):
	'''
	This Class Is The LoaderScriptOptions Class.
	'''

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self._uiPath = "ui/Loader_Script_Options.ui"
		self._dockArea = 2

		self._container = None

		self._coreTemplatesOutliner = None
		self._addonsLoaderScript = None

		self._templateCommonAttributesSection = "Common Attributes"
		self._templateAdditionalAttributesSection = "Additional Attributes"
		self._templateScriptSection = "Script"
		self._optionsToolboxesHeaders = ["Value"]

		self._uiLightGrayColor = QColor(240, 240, 240)
		self._uiDarkGrayColor = QColor(160, 160, 160)

		self._tableWidgetRowHeight = 30
		self._tableWidgetHeaderHeight = 26

		self._enumSplitter = ";"

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiPath"))

	@property
	def dockArea(self):
		'''
		This Method Is The Property For The _dockArea Attribute.

		@return: self._dockArea. ( Integer )
		'''

		return self._dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		'''
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		'''
		This Method Is The Deleter Method For The _dockArea Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("dockArea"))

	@property
	def container(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("container"))

	@property
	def coreTemplatesOutliner(self):
		'''
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self._coreTemplatesOutliner. ( Object )
		'''

		return self._coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		'''
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		'''
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("coreTemplatesOutliner"))

	@property
	def addonsLoaderScript(self):
		'''
		This Method Is The Property For The _addonsLoaderScript Attribute.

		@return: self._addonsLoaderScript. ( Object )
		'''

		return self._addonsLoaderScript

	@addonsLoaderScript.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self, value):
		'''
		This Method Is The Setter Method For The _addonsLoaderScript Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("addonsLoaderScript"))

	@addonsLoaderScript.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self):
		'''
		This Method Is The Deleter Method For The _addonsLoaderScript Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("addonsLoaderScript"))

	@property
	def templateCommonAttributesSection(self):
		'''
		This Method Is The Property For The _templateCommonAttributesSection Attribute.

		@return: self._templateCommonAttributesSection. ( String )
		'''

		return self._templateCommonAttributesSection

	@templateCommonAttributesSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateCommonAttributesSection(self, value):
		'''
		This Method Is The Setter Method For The _templateCommonAttributesSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("templateCommonAttributesSection"))

	@templateCommonAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateCommonAttributesSection(self):
		'''
		This Method Is The Deleter Method For The _templateCommonAttributesSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("templateCommonAttributesSection"))

	@property
	def templateAdditionalAttributesSection(self):
		'''
		This Method Is The Property For The _templateAdditionalAttributesSection Attribute.

		@return: self._templateAdditionalAttributesSection. ( String )
		'''

		return self._templateAdditionalAttributesSection

	@templateAdditionalAttributesSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateAdditionalAttributesSection(self, value):
		'''
		This Method Is The Setter Method For The _templateAdditionalAttributesSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("templateAdditionalAttributesSection"))

	@templateAdditionalAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateAdditionalAttributesSection(self):
		'''
		This Method Is The Deleter Method For The _templateAdditionalAttributesSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("templateAdditionalAttributesSection"))

	@property
	def templateScriptSection(self):
		'''
		This Method Is The Property For The _templateScriptSection Attribute.

		@return: self._templateScriptSection. ( String )
		'''

		return self._templateScriptSection

	@templateScriptSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateScriptSection(self, value):
		'''
		This Method Is The Setter Method For The _templateScriptSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("templateScriptSection"))

	@templateScriptSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateScriptSection(self):
		'''
		This Method Is The Deleter Method For The _templateScriptSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("templateScriptSection"))

	@property
	def optionsToolboxesHeaders(self):
		'''
		This Method Is The Property For The _optionsToolboxesHeaders Attribute.

		@return: self._optionsToolboxesHeaders. ( List )
		'''

		return self._optionsToolboxesHeaders

	@optionsToolboxesHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def optionsToolboxesHeaders(self, value):
		'''
		This Method Is The Setter Method For The _optionsToolboxesHeaders Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("optionsToolboxesHeaders"))

	@optionsToolboxesHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def optionsToolboxesHeaders(self):
		'''
		This Method Is The Deleter Method For The _optionsToolboxesHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("optionsToolboxesHeaders"))

	@property
	def uiLightGrayColor(self):
		'''
		This Method Is The Property For The _uiLightGrayColor Attribute.

		@return: self._uiLightGrayColor. ( QColor )
		'''

		return self._uiLightGrayColor

	@uiLightGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self, value):
		'''
		This Method Is The Setter Method For The _uiLightGrayColor Attribute.

		@param value: Attribute Value. ( QColor )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("uiLightGrayColor"))

	@uiLightGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self):
		'''
		This Method Is The Deleter Method For The _uiLightGrayColor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiLightGrayColor"))

	@property
	def uiDarkGrayColor(self):
		'''
		This Method Is The Property For The _uiDarkGrayColor Attribute.

		@return: self._uiDarkGrayColor. ( QColor )
		'''

		return self._uiDarkGrayColor

	@uiDarkGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self, value):
		'''
		This Method Is The Setter Method For The _uiDarkGrayColor Attribute.

		@param value: Attribute Value. ( QColor )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("uiDarkGrayColor"))

	@uiDarkGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self):
		'''
		This Method Is The Deleter Method For The _uiDarkGrayColor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiDarkGrayColor"))

	@property
	def tableWidgetRowHeight(self):
		'''
		This Method Is The Property For The _tableWidgetRowHeight Attribute.

		@return: self._tableWidgetRowHeight. ( Integer )
		'''

		return self._tableWidgetRowHeight

	@tableWidgetRowHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self, value):
		'''
		This Method Is The Setter Method For The _tableWidgetRowHeight Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("tableWidgetRowHeight"))

	@tableWidgetRowHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self):
		'''
		This Method Is The Deleter Method For The _tableWidgetRowHeight Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("tableWidgetRowHeight"))

	@property
	def tableWidgetHeaderHeight(self):
		'''
		This Method Is The Property For The _tableWidgetHeaderHeight Attribute.

		@return: self._tableWidgetHeaderHeight. ( Integer )
		'''

		return self._tableWidgetHeaderHeight

	@tableWidgetHeaderHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self, value):
		'''
		This Method Is The Setter Method For The _tableWidgetHeaderHeight Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("tableWidgetHeaderHeight"))

	@tableWidgetHeaderHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self):
		'''
		This Method Is The Deleter Method For The _tableWidgetHeaderHeight Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("tableWidgetHeaderHeight"))

	@property
	def enumSplitter(self):
		'''
		This Method Is The Property For The _enumSplitter Attribute.

		@return: self._enumSplitter. ( String )
		'''

		return self._enumSplitter

	@enumSplitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def enumSplitter(self, value):
		'''
		This Method Is The Setter Method For The _enumSplitter Attribute.

		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("enumSplitter", value)
			assert len(value) == 1, "'{0}' Attribute : '{1}' Has Multiples Characters !".format("enumSplitter", value)
			assert not re.search("\w", value), "'{0}' Attribute : '{1}' Is An AlphaNumeric Character !".format("enumSplitter", value)
		self._enumSplitter = value

	@enumSplitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def enumSplitter(self):
		'''
		This Method Is The Deleter Method For The _enumSplitter Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("enumSplitter"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiPath)
		self._container = container

		self._coreTemplatesOutliner = self._container.componentsManager.components["core.templatesOutliner"].interface
		self._addonsLoaderScript = self._container.componentsManager.components["addons.loaderScript"].interface

		self._activate()

	@core.executionTrace
	def deactivate(self):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self._container = None

		self._coreTemplatesOutliner = None
		self._addonsLoaderScript = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.connect(self.coreTemplatesOutlinerUi_Templates_Outliner_treeView_OnSelectionChanged)

	@core.executionTrace
	def uninitializeUi(self):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.disconnect(self.coreTemplatesOutlinerUi_Templates_Outliner_treeView_OnSelectionChanged)

	@core.executionTrace
	def addWidget(self):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self._container.addDockWidget(Qt.DockWidgetArea(self._dockArea), self.ui)

	@core.executionTrace
	def removeWidget(self):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self._container.removeDockWidget(self.ui)
		self.ui.setParent(None)

	@core.executionTrace
	def coreTemplatesOutlinerUi_Templates_Outliner_treeView_OnSelectionChanged(self, selectedItems, deselectedItems):
		'''
		This Method Sets Is Triggered When coreTemplatesOutlinerUi_Templates_Outliner_treeView Selection Has Changed.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		'''

		selectedTemplates = self._coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None

		if template :
			LOGGER.debug("> Parsing '{0}' Template For '{1}' and '{2}'Section.".format(template._datas.name, self._templateCommonAttributesSection, self._templateAdditionalAttributesSection))

			if os.path.exists(template._datas.path) :
				templateParser = Parser(template._datas.path)
				templateParser.read() and templateParser.parse(rawSections=(self._templateScriptSection))

				self.setOptionsToolBox(templateParser.sections[self._templateCommonAttributesSection], self.ui.Common_Attributes_tableWidget)
				self.setOptionsToolBox(templateParser.sections[self._templateAdditionalAttributesSection], self.ui.Additional_Attributes_tableWidget)

	@core.executionTrace
	def setOptionsToolBox(self, section, tableWidget) :
		'''
		This Method Defines And Sets Options TableWidgets.

		@param section: Section Attributes. ( Dictionary )
		@param tableWidget: Table Widget. ( QTableWidget )
		'''

		LOGGER.debug("> Updating '{0}'.".format(tableWidget.objectName()))

		tableWidget.hide()

		tableWidget.clear()
		tableWidget.setRowCount(len(section))
		tableWidget.setColumnCount(len(self._optionsToolboxesHeaders))
		tableWidget.horizontalHeader().setStretchLastSection(True)
		tableWidget.setHorizontalHeaderLabels(self._optionsToolboxesHeaders)
		tableWidget.horizontalHeader().hide()

		tableWidget.setMinimumHeight(len(section) * self._tableWidgetRowHeight + self._tableWidgetHeaderHeight)

		palette = QPalette()
		palette.setColor(QPalette.Base, Qt.transparent)
		tableWidget.setPalette(palette)

		verticalHeaderLabels = []
		for row, attribute in enumerate(section.keys()) :
			LOGGER.debug("> Current Attribute : '{0}'.".format(attribute))
			attributeCompound = foundations.parser.getAttributeCompound(attribute, section[attribute])
			if attributeCompound.name :
				verticalHeaderLabels.append(attributeCompound.alias)
			else:
				verticalHeaderLabels.append(strings.getNiceName(attributeCompound.name))

			LOGGER.debug("> Attribute Type : '{0}'.".format("Boolean"))
			if attributeCompound.type == "Boolean" :
				state = int(attributeCompound.value) and True or False
				item = Variable_QPushButton(state, (self._uiLightGrayColor, self._uiDarkGrayColor), ("True", "False"))
				item.setChecked(state)
				item._datas = attributeCompound
				tableWidget.setCellWidget(row, 0, item)
			elif attributeCompound.type == "Float" :
				item = QDoubleSpinBox()
				item.setMinimum(0)
				item.setMaximum(65535)
				item.setValue(float (attributeCompound.value))
				item._datas = attributeCompound
				tableWidget.setCellWidget(row, 0, item)
			elif attributeCompound.type == "Enum" :
				item = QComboBox()
				item.addItems(attributeCompound.value.split(self._enumSplitter))
				item._datas = attributeCompound
				tableWidget.setCellWidget(row, 0, item)
			else :
				item = QTableWidgetItem(QString(attributeCompound.value))
				item.setTextAlignment(Qt.AlignCenter)
				item._datas = attributeCompound
				tableWidget.setItem(row, 0, item)

		tableWidget.setVerticalHeaderLabels (verticalHeaderLabels)
		tableWidget.show()

	@core.executionTrace
	def updateOverrideKeys(self, tableWidget):
		'''
		This Method Updates The Loader Script Component Override Keys.
		
		@param tableWidget: Table Widget. ( QTableWidget )
		'''

		LOGGER.debug("> Updating Override Keys With '{0}' Attributes.".format(tableWidget.objectName()))

		for row in range(tableWidget.rowCount()) :
			widget = tableWidget.cellWidget(row, 0)
			if type(widget) is Variable_QPushButton :
				value = tableWidget.cellWidget(row, 0).text() == "True" and "1" or "0"
			elif type(widget) is QDoubleSpinBox :
				value = str(tableWidget.cellWidget(row, 0).value())
			elif type(widget) is QComboBox :
				value = str(tableWidget.cellWidget(row, 0).currentText())
			else:
				value = str(tableWidget.cellWidget(row, 0).text())
			widget._datas.value = value

			LOGGER.debug("> Adding '{0}' Override Key With Value : '{1}'.".format(widget._datas.name, widget._datas.value))
			self._addonsLoaderScript.overrideKeys[widget._datas.name] = widget._datas

	@core.executionTrace
	def getOverrideKeys(self):
		'''
		This Method Gets Override Keys.
		'''

		LOGGER.info("{0} | Updating Loader Script Override Keys !".format(self.__class__.__name__))

		self.updateOverrideKeys(self.ui.Common_Attributes_tableWidget)
		self.updateOverrideKeys(self.ui.Additional_Attributes_tableWidget)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
