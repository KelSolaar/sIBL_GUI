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
***	loaderScriptOptions.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Loader Script Options Component Module.
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.parser
import foundations.strings as strings
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
	"""
	This Class Is The LoaderScriptOptions Class.
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

		self.__uiPath = "ui/Loader_Script_Options.ui"
		self.__dockArea = 2

		self.__container = None

		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

		self.__templateCommonAttributesSection = "Common Attributes"
		self.__templateAdditionalAttributesSection = "Additional Attributes"
		self.__templateScriptSection = "Script"
		self.__optionsToolboxesHeaders = ["Value"]

		self.__uiLightGrayColor = QColor(240, 240, 240)
		self.__uiDarkGrayColor = QColor(160, 160, 160)

		self.__tableWidgetRowHeight = 30
		self.__tableWidgetHeaderHeight = 26

		self.__enumSplitter = ";"

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
	def coreTemplatesOutliner(self):
		"""
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreTemplatesOutliner"))

	@property
	def addonsLoaderScript(self):
		"""
		This Method Is The Property For The _addonsLoaderScript Attribute.

		@return: self.__addonsLoaderScript. ( Object )
		"""

		return self.__addonsLoaderScript

	@addonsLoaderScript.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self, value):
		"""
		This Method Is The Setter Method For The _addonsLoaderScript Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("addonsLoaderScript"))

	@addonsLoaderScript.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self):
		"""
		This Method Is The Deleter Method For The _addonsLoaderScript Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("addonsLoaderScript"))

	@property
	def templateCommonAttributesSection(self):
		"""
		This Method Is The Property For The _templateCommonAttributesSection Attribute.

		@return: self.__templateCommonAttributesSection. ( String )
		"""

		return self.__templateCommonAttributesSection

	@templateCommonAttributesSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateCommonAttributesSection(self, value):
		"""
		This Method Is The Setter Method For The _templateCommonAttributesSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templateCommonAttributesSection"))

	@templateCommonAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateCommonAttributesSection(self):
		"""
		This Method Is The Deleter Method For The _templateCommonAttributesSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templateCommonAttributesSection"))

	@property
	def templateAdditionalAttributesSection(self):
		"""
		This Method Is The Property For The _templateAdditionalAttributesSection Attribute.

		@return: self.__templateAdditionalAttributesSection. ( String )
		"""

		return self.__templateAdditionalAttributesSection

	@templateAdditionalAttributesSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateAdditionalAttributesSection(self, value):
		"""
		This Method Is The Setter Method For The _templateAdditionalAttributesSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templateAdditionalAttributesSection"))

	@templateAdditionalAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateAdditionalAttributesSection(self):
		"""
		This Method Is The Deleter Method For The _templateAdditionalAttributesSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templateAdditionalAttributesSection"))

	@property
	def templateScriptSection(self):
		"""
		This Method Is The Property For The _templateScriptSection Attribute.

		@return: self.__templateScriptSection. ( String )
		"""

		return self.__templateScriptSection

	@templateScriptSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateScriptSection(self, value):
		"""
		This Method Is The Setter Method For The _templateScriptSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templateScriptSection"))

	@templateScriptSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateScriptSection(self):
		"""
		This Method Is The Deleter Method For The _templateScriptSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templateScriptSection"))

	@property
	def optionsToolboxesHeaders(self):
		"""
		This Method Is The Property For The _optionsToolboxesHeaders Attribute.

		@return: self.__optionsToolboxesHeaders. ( List )
		"""

		return self.__optionsToolboxesHeaders

	@optionsToolboxesHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def optionsToolboxesHeaders(self, value):
		"""
		This Method Is The Setter Method For The _optionsToolboxesHeaders Attribute.

		@param value: Attribute Value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("optionsToolboxesHeaders"))

	@optionsToolboxesHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def optionsToolboxesHeaders(self):
		"""
		This Method Is The Deleter Method For The _optionsToolboxesHeaders Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("optionsToolboxesHeaders"))

	@property
	def uiLightGrayColor(self):
		"""
		This Method Is The Property For The _uiLightGrayColor Attribute.

		@return: self.__uiLightGrayColor. ( QColor )
		"""

		return self.__uiLightGrayColor

	@uiLightGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self, value):
		"""
		This Method Is The Setter Method For The _uiLightGrayColor Attribute.

		@param value: Attribute Value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiLightGrayColor"))

	@uiLightGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self):
		"""
		This Method Is The Deleter Method For The _uiLightGrayColor Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiLightGrayColor"))

	@property
	def uiDarkGrayColor(self):
		"""
		This Method Is The Property For The _uiDarkGrayColor Attribute.

		@return: self.__uiDarkGrayColor. ( QColor )
		"""

		return self.__uiDarkGrayColor

	@uiDarkGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self, value):
		"""
		This Method Is The Setter Method For The _uiDarkGrayColor Attribute.

		@param value: Attribute Value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiDarkGrayColor"))

	@uiDarkGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self):
		"""
		This Method Is The Deleter Method For The _uiDarkGrayColor Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiDarkGrayColor"))

	@property
	def tableWidgetRowHeight(self):
		"""
		This Method Is The Property For The _tableWidgetRowHeight Attribute.

		@return: self.__tableWidgetRowHeight. ( Integer )
		"""

		return self.__tableWidgetRowHeight

	@tableWidgetRowHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self, value):
		"""
		This Method Is The Setter Method For The _tableWidgetRowHeight Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("tableWidgetRowHeight"))

	@tableWidgetRowHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self):
		"""
		This Method Is The Deleter Method For The _tableWidgetRowHeight Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("tableWidgetRowHeight"))

	@property
	def tableWidgetHeaderHeight(self):
		"""
		This Method Is The Property For The _tableWidgetHeaderHeight Attribute.

		@return: self.__tableWidgetHeaderHeight. ( Integer )
		"""

		return self.__tableWidgetHeaderHeight

	@tableWidgetHeaderHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self, value):
		"""
		This Method Is The Setter Method For The _tableWidgetHeaderHeight Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("tableWidgetHeaderHeight"))

	@tableWidgetHeaderHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self):
		"""
		This Method Is The Deleter Method For The _tableWidgetHeaderHeight Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("tableWidgetHeaderHeight"))

	@property
	def enumSplitter(self):
		"""
		This Method Is The Property For The _enumSplitter Attribute.

		@return: self.__enumSplitter. ( String )
		"""

		return self.__enumSplitter

	@enumSplitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def enumSplitter(self, value):
		"""
		This Method Is The Setter Method For The _enumSplitter Attribute.

		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("enumSplitter", value)
			assert len(value) == 1, "'{0}' Attribute: '{1}' Has Multiples Characters!".format("enumSplitter", value)
			assert not re.search("\w", value), "'{0}' Attribute: '{1}' Is An AlphaNumeric Character!".format("enumSplitter", value)
		self.__enumSplitter = value

	@enumSplitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def enumSplitter(self):
		"""
		This Method Is The Deleter Method For The _enumSplitter Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("enumSplitter"))

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

		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface
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

		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.connect(self.__coreTemplatesOutlinerUi_Templates_Outliner_treeView_selectionModel_selectionChanged)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.disconnect(self.__coreTemplatesOutlinerUi_Templates_Outliner_treeView_selectionModel_selectionChanged)

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
	def __tableWidget_setUi(self, section, tableWidget):
		"""
		This Method Defines And Sets Options TableWidgets.

		@param section: Section Attributes. ( Dictionary )
		@param tableWidget: Table Widget. ( QTableWidget )
		"""

		LOGGER.debug("> Updating '{0}'.".format(tableWidget.objectName()))

		tableWidget.hide()

		tableWidget.clear()
		tableWidget.setRowCount(len(section))
		tableWidget.setColumnCount(len(self.__optionsToolboxesHeaders))
		tableWidget.horizontalHeader().setStretchLastSection(True)
		tableWidget.setHorizontalHeaderLabels(self.__optionsToolboxesHeaders)
		tableWidget.horizontalHeader().hide()

		tableWidget.setMinimumHeight(len(section) * self.__tableWidgetRowHeight + self.__tableWidgetHeaderHeight)

		palette = QPalette()
		palette.setColor(QPalette.Base, Qt.transparent)
		tableWidget.setPalette(palette)

		verticalHeaderLabels = []
		for row, attribute in enumerate(section.keys()):
			LOGGER.debug("> Current Attribute: '{0}'.".format(attribute))
			attributeCompound = foundations.parser.getAttributeCompound(attribute, section[attribute])
			if attributeCompound.name:
				verticalHeaderLabels.append(attributeCompound.alias)
			else:
				verticalHeaderLabels.append(strings.getNiceName(attributeCompound.name))

			LOGGER.debug("> Attribute Type: '{0}'.".format(attributeCompound.type))
			if attributeCompound.type == "Boolean":
				state = int(attributeCompound.value) and True or False
				item = Variable_QPushButton(state, (self.__uiLightGrayColor, self.__uiDarkGrayColor), ("True", "False"))
				item.setChecked(state)
			elif attributeCompound.type == "Float":
				item = QDoubleSpinBox()
				item.setMinimum(0)
				item.setMaximum(65535)
				item.setValue(float(attributeCompound.value))
			elif attributeCompound.type == "Enum":
				item = QComboBox()
				item.addItems([enumItem.strip() for enumItem in attributeCompound.value.split(self.__enumSplitter)])
			elif attributeCompound.type == "String":
				item = QLineEdit(QString(attributeCompound.value))

			item._datas = attributeCompound
			tableWidget.setCellWidget(row, 0, item)

		tableWidget.setVerticalHeaderLabels (verticalHeaderLabels)
		tableWidget.show()

	@core.executionTrace
	def __coreTemplatesOutlinerUi_Templates_Outliner_treeView_selectionModel_selectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Sets Is Triggered When coreTemplatesOutlinerUi_Templates_Outliner_treeView Selection Has Changed.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None

		if template:
			LOGGER.debug("> Parsing '{0}' Template For '{1}' and '{2}'Section.".format(template._datas.name, self.__templateCommonAttributesSection, self.__templateAdditionalAttributesSection))

			if os.path.exists(template._datas.path):
				templateParser = Parser(template._datas.path)
				templateParser.read() and templateParser.parse(rawSections=(self.__templateScriptSection))

				self.__tableWidget_setUi(templateParser.sections[self.__templateCommonAttributesSection], self.ui.Common_Attributes_tableWidget)
				self.__tableWidget_setUi(templateParser.sections[self.__templateAdditionalAttributesSection], self.ui.Additional_Attributes_tableWidget)

	@core.executionTrace
	def updateOverrideKeys(self, tableWidget):
		"""
		This Method Updates The Loader Script Component Override Keys.
		
		@param tableWidget: Table Widget. ( QTableWidget )
		"""

		LOGGER.debug("> Updating Override Keys With '{0}' Attributes.".format(tableWidget.objectName()))

		for row in range(tableWidget.rowCount()):
			widget = tableWidget.cellWidget(row, 0)
			if type(widget) is Variable_QPushButton:
				value = widget.text() == "True" and "1" or "0"
			elif type(widget) is QDoubleSpinBox:
				value = str(widget.value())
			elif type(widget) is QComboBox:
				value = str(widget.currentText())
			else:
				value = str(widget.text())
			widget._datas.value = value

			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format(widget._datas.name, widget._datas.value))
			self.__addonsLoaderScript.overrideKeys[widget._datas.name] = widget._datas

	@core.executionTrace
	def getOverrideKeys(self):
		"""
		This Method Gets Override Keys.
		"""

		LOGGER.info("{0} | Updating Loader Script Override Keys!".format(self.__class__.__name__))

		self.updateOverrideKeys(self.ui.Common_Attributes_tableWidget)
		self.updateOverrideKeys(self.ui.Additional_Attributes_tableWidget)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
