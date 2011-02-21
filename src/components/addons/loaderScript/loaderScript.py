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

'''
************************************************************************************************
***	loaderScript.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Loader Script Component Module.
***
***	Others:
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
import platform
import re
import socket
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.parser
import foundations.strings as strings
import ui.common
import ui.widgets.messageBox as messageBox
from foundations.parser import Parser
from foundations.io import File
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class LoaderScript(UiComponent):
	'''
	This Class Is The LoaderScript Class.
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

		self._uiPath = "ui/Loader_Script.ui"
		self._dockArea = 2

		self._container = None

		self._coreDatabaseBrowser = None
		self._coreTemplatesOutliner = None

		self._ioDirectory = "loaderScripts/"

		self._bindingIdentifierPattern = "@[a-zA-Z0-9_]*"
		self._templateScriptSection = "Script"
		self._templateIblAttributesSection = "sIBL File Attributes"
		self._templateRemoteConnectionSection = "Remote Connection"

		self._win32ExecutionMethod = "ExecuteSIBLLoaderScript"

		self._overrideKeys = {}

		self._defaultStringSeparator = "|"
		self._unnamedLightName = "Unnamed_Light"

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		'''
		This Method Is The Deleter Method For The _dockArea Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dockArea"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def coreDatabaseBrowser(self):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDatabaseBrowser"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		'''
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreTemplatesOutliner"))

	@property
	def ioDirectory(self):
		'''
		This Method Is The Property For The _ioDirectory Attribute.

		@return: self._ioDirectory. ( String )
		'''

		return self._ioDirectory

	@ioDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self, value):
		'''
		This Method Is The Setter Method For The _ioDirectory Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("ioDirectory"))

	@ioDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self):
		'''
		This Method Is The Deleter Method For The _ioDirectory Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("ioDirectory"))

	@property
	def bindingIdentifierPattern(self):
		'''
		This Method Is The Property For The _bindingIdentifierPattern Attribute.

		@return: self._bindingIdentifierPattern. ( String )
		'''

		return self._bindingIdentifierPattern

	@bindingIdentifierPattern.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def bindingIdentifierPattern(self, value):
		'''
		This Method Is The Setter Method For The _bindingIdentifierPattern Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("bindingIdentifierPattern"))

	@bindingIdentifierPattern.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def bindingIdentifierPattern(self):
		'''
		This Method Is The Deleter Method For The _bindingIdentifierPattern Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("bindingIdentifierPattern"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templateScriptSection"))

	@templateScriptSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateScriptSection(self):
		'''
		This Method Is The Deleter Method For The _templateScriptSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templateScriptSection"))

	@property
	def templateIblAttributesSection(self):
		'''
		This Method Is The Property For The _templateIblAttributesSection Attribute.

		@return: self._templateIblAttributesSection. ( String )
		'''

		return self._templateIblAttributesSection

	@templateIblAttributesSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateIblAttributesSection(self, value):
		'''
		This Method Is The Setter Method For The _templateIblAttributesSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templateIblAttributesSection"))

	@templateIblAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateIblAttributesSection(self):
		'''
		This Method Is The Deleter Method For The _templateIblAttributesSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templateIblAttributesSection"))

	@property
	def templateRemoteConnectionSection(self):
		'''
		This Method Is The Property For The _templateRemoteConnectionSection Attribute.

		@return: self._templateRemoteConnectionSection. ( String )
		'''

		return self._templateRemoteConnectionSection

	@templateRemoteConnectionSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateRemoteConnectionSection(self, value):
		'''
		This Method Is The Setter Method For The _templateRemoteConnectionSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templateRemoteConnectionSection"))

	@templateRemoteConnectionSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateRemoteConnectionSection(self):
		'''
		This Method Is The Deleter Method For The _templateRemoteConnectionSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templateRemoteConnectionSection"))

	@property
	def overrideKeys(self):
		'''
		This Method Is The Property For The _overrideKeys Attribute.

		@return: self._overrideKeys. ( Dictionary )
		'''

		return self._overrideKeys

	@overrideKeys.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overrideKeys(self, value):
		'''
		This Method Is The Setter Method For The _overrideKeys Attribute.

		@param value: Attribute Value. ( Dictionary )
		'''

		if value:
			assert type(value) is dict, "'{0}' Attribute: '{1}' Type Is Not 'dict'!".format("sections", value)
		self._overrideKeys = value

	@overrideKeys.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overrideKeys(self):
		'''
		This Method Is The Deleter Method For The _overrideKeys Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("overrideKeys"))

	@property
	def defaultStringSeparator(self):
		'''
		This Method Is The Property For The _defaultStringSeparator Attribute.

		@return: self._defaultStringSeparator. ( String )
		'''

		return self._defaultStringSeparator

	@defaultStringSeparator.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultStringSeparator(self, value):
		'''
		This Method Is The Setter Method For The _defaultStringSeparator Attribute.

		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("defaultStringSeparator", value)
			assert len(value) == 1, "'{0}' Attribute: '{1}' Has Multiples Characters!".format("defaultStringSeparator", value)
			assert not re.search("\w", value), "'{0}' Attribute: '{1}' Is An AlphaNumeric Character!".format("defaultStringSeparator", value)
		self._defaultStringSeparator = value

	@defaultStringSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultStringSeparator(self):
		'''
		This Method Is The Deleter Method For The _defaultStringSeparator Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("defaultStringSeparator"))

	@property
	def unnamedLightName(self):
		'''
		This Method Is The Property For The _unnamedLightName Attribute.

		@return: self._unnamedLightName. ( String )
		'''

		return self._unnamedLightName

	@unnamedLightName.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def unnamedLightName(self, value):
		'''
		This Method Is The Setter Method For The _unnamedLightName Attribute.

		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("unnamedLightName", value)
		self._unnamedLightName = value

	@unnamedLightName.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def unnamedLightName(self):
		'''
		This Method Is The Deleter Method For The _unnamedLightName Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("unnamedLightName"))

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

		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface
		self._coreTemplatesOutliner = self._container.componentsManager.components["core.templatesOutliner"].interface

		self._ioDirectory = os.path.join(self._container.userApplicationDatasDirectory, Constants.ioDirectory, self._ioDirectory)
		not os.path.exists(self._ioDirectory) and os.makedirs(self._ioDirectory)

		self._activate()

	@core.executionTrace
	def deactivate(self):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self._container = None

		self._coreDatabaseBrowser = None
		self._coreTemplatesOutliner = None

		self._ioDirectory = os.path.basename(os.path.abspath(self._ioDirectory))

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.ui.Remote_Connection_groupBox.hide()

		# Signals / Slots.
		self.ui.Output_Loader_Script_pushButton.clicked.connect(self.Output_Loader_Script_pushButton_OnClicked)
		self.ui.Send_To_Software_pushButton.clicked.connect(self.Send_To_Software_pushButton_OnClicked)
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.connect(self.coreTemplatesOutlinerUi_Templates_Outliner_treeView_OnSelectionChanged)

	@core.executionTrace
	def uninitializeUi(self):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Output_Loader_Script_pushButton.clicked.disconnect(self.Output_Loader_Script_pushButton_OnClicked)
		self.ui.Send_To_Software_pushButton.clicked.disconnect(self.Send_To_Software_pushButton_OnClicked)
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
	def Output_Loader_Script_pushButton_OnClicked(self, checked):
		'''
		This Method Is Triggered When Output_Loader_Script_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		'''

		self.outputLoaderScript()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.SocketConnectionError)
	def Send_To_Software_pushButton_OnClicked(self, checked):
		'''
		This Method Is Triggered When Send_To_Software_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		'''

		if self.outputLoaderScript():
			selectedTemplate = self._coreTemplatesOutliner.getSelectedTemplates()[0]
			LOGGER.info("{0} | Starting Remote Connection!".format(self.__class__.__name__))
			templateParser = Parser(selectedTemplate._datas.path)
			templateParser.read() and templateParser.parse(rawSections=(self._templateScriptSection))
			connectionType = foundations.parser.getAttributeCompound("ConnectionType", templateParser.getValue("ConnectionType", self._templateRemoteConnectionSection))
			loaderScriptPath = strings.getNormalizedPath(os.path.join(self._ioDirectory, selectedTemplate._datas.outputScript))
			if connectionType.value == "Socket":
				try:
					connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					connection.connect((str(self.ui.Address_lineEdit.text()), int(self.ui.Software_Port_spinBox.value())))
					socketCommand = foundations.parser.getAttributeCompound("ExecutionCommand", templateParser.getValue("ExecutionCommand", self._templateRemoteConnectionSection)).value.replace("$loaderScriptPath", loaderScriptPath)
					LOGGER.debug("> Current Socket Command: '%s'.", socketCommand)
					connection.send(socketCommand)
					dataBack = connection.recv(8192)
					LOGGER.debug("> Received Back From Application: '%s'", dataBack)
					connection.close()
					LOGGER.info("{0} | Ending Remote Connection!".format(self.__class__.__name__))
				except Exception as error:
					raise foundations.exceptions.SocketConnectionError, "{0} | Remote Connection Error: '{1}'!".format(self.__class__.__name__, error)
			elif connectionType.value == "Win32":
				if platform.system() == "Windows" or platform.system() == "Microsoft":
					try:
						import win32com.client
						connection = win32com.client.Dispatch(foundations.parser.getAttributeCompound("TargetApplication", templateParser.getValue("TargetApplication", self._templateRemoteConnectionSection)).value)
						connection._FlagAsMethod(self._win32ExecutionMethod)
						connectionCommand = foundations.parser.getAttributeCompound("ExecutionCommand", templateParser.getValue("ExecutionCommand", self._templateRemoteConnectionSection)).value.replace("$loaderScriptPath", loaderScriptPath)
						LOGGER.debug("> Current Connection Command: '%s'.", connectionCommand)
						getattr(connection, self._win32ExecutionMethod)(connectionCommand)
					except Exception as error:
						raise foundations.exceptions.SocketConnectionError, "{0} | Remote On Win32 OLE Server Error: '{1}'!".format(self.__class__.__name__, error)

	@core.executionTrace
	def coreTemplatesOutlinerUi_Templates_Outliner_treeView_OnSelectionChanged(self, selectedItems, deselectedItems):
		'''
		This Method Sets Is Triggered When coreTemplatesOutlinerUi_Templates_Outliner_treeView Selection Has Changed.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		'''

		selectedTemplates = self._coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None

		if template:
			LOGGER.debug("> Parsing '{0}' Template For '{1}' Section.".format(template._datas.name, self._templateRemoteConnectionSection))

			if os.path.exists(template._datas.path):
				templateParser = Parser(template._datas.path)
				templateParser.read() and templateParser.parse(rawSections=(self._templateScriptSection))

				if self._templateRemoteConnectionSection in templateParser.sections:
					LOGGER.debug("> {0}' Section Found.".format(self._templateRemoteConnectionSection))
					self.ui.Remote_Connection_groupBox.show()
					connectionType = foundations.parser.getAttributeCompound("ConnectionType", templateParser.getValue("ConnectionType", self._templateRemoteConnectionSection))
					if connectionType.value == "Socket":
						LOGGER.debug("> Remote Connection Type: 'Socket'.")
						self.ui.Software_Port_spinBox.setValue(int(foundations.parser.getAttributeCompound("DefaultPort", templateParser.getValue("DefaultPort", self._templateRemoteConnectionSection)).value))
						self.ui.Address_lineEdit.setText(QString(foundations.parser.getAttributeCompound("DefaultAddress", templateParser.getValue("DefaultAddress", self._templateRemoteConnectionSection)).value))
						self.ui.Remote_Connection_Options_frame.show()
					elif connectionType.value == "Win32":
						LOGGER.debug("> Remote Connection: 'Win32'.")
						self.ui.Remote_Connection_Options_frame.hide()
				else:
					self.ui.Remote_Connection_groupBox.hide()
		else:
			self.ui.Remote_Connection_groupBox.hide()

	@core.executionTrace
	def getDefaultOverrideKeys(self):
		'''
		This Method Gets Default Override Keys.
		'''

		LOGGER.debug("> Constructing Default Override Keys.")

		overrideKeys = {}

		selectedTemplates = self._coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None

		if template:
			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format("Template|Path", template._datas.path))
			overrideKeys["Template|Path"] = foundations.parser.getAttributeCompound("Template|Path", template._datas.path)

		selectedIblSets = self._coreDatabaseBrowser.getSelectedItems()
		iblSet = selectedIblSets and selectedIblSets[0] or None

		if iblSet:
			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format("Background|BGfile", iblSet._datas.backgroundImage))
			overrideKeys["Background|BGfile"] = iblSet._datas.backgroundImage and foundations.parser.getAttributeCompound("Background|BGfile", strings.getNormalizedPath(iblSet._datas.backgroundImage))

			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format("Enviroment|EVfile", iblSet._datas.lightingImage))
			overrideKeys["Enviroment|EVfile"] = iblSet._datas.lightingImage and foundations.parser.getAttributeCompound("Enviroment|EVfile", strings.getNormalizedPath(iblSet._datas.lightingImage))

			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format("Reflection|REFfile", iblSet._datas.reflectionImage))
			overrideKeys["Reflection|REFfile"] = iblSet._datas.reflectionImage and foundations.parser.getAttributeCompound("Reflection|REFfile", strings.getNormalizedPath(iblSet._datas.reflectionImage))

		return overrideKeys

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError, OSError, Exception)
	def outputLoaderScript(self):
		'''
		This Method Output The Loader Script.
		
		@return: Output Success. ( Boolean )
		'''

		LOGGER.debug("> Initializing Loader Script Output.")

		selectedTemplates = self._coreTemplatesOutliner.getSelectedTemplates()
		if selectedTemplates and len(selectedTemplates) != 1:
			messageBox.messageBox("Information", "Information", "{0} | Multiple Selected Templates, '{1}' Will Be Used!".format(self.__class__.__name__, selectedTemplates[0]._datas.name))

		template = selectedTemplates and selectedTemplates[0] or None

		if not template:
			raise foundations.exceptions.UserError, "{0} | In Order To Output The Loader Script, You Need To Select A Template!".format(self.__class__.__name__)

		if not os.path.exists(template._datas.path):
			raise OSError, "{0} | '{1}' Template File Doesn't Exists!".format(self.__class__.__name__, template._datas.name)

		selectedIblSet = self._coreDatabaseBrowser.getSelectedItems()
		iblSet = selectedIblSet and selectedIblSet[0] or None

		if not iblSet:
			raise foundations.exceptions.UserError, "{0} | In Order To Output The Loader Script, You Need To Select A Set!".format(self.__class__.__name__)

		if not os.path.exists(iblSet._datas.path):
			raise OSError, "{0} | '{1}' Ibl Set File Doesn't Exists!".format(self.__class__.__name__, iblSet._datas.name)

		self._overrideKeys = self.getDefaultOverrideKeys()

		for component in self._container.componentsManager.getComponents():
			profile = self._container._componentsManager.components[component]
			interface = self._container.componentsManager.getInterface(component)
			if interface.activated and profile.name != self.name:
				hasattr(interface, "getOverrideKeys") and interface.getOverrideKeys()

		if self._container.parameters.loaderScriptsOutputDirectory:
			if os.path.exists(self._container.parameters.loaderScriptsOutputDirectory):
				loaderScript = File(os.path.join(self._container.parameters.loaderScriptsOutputDirectory, template._datas.outputScript))
			else:
				raise OSError, "{0} | '{1}' Loader Script Output Directory Doesn't Exists!".format(self.__class__.__name__, self._container.parameters.loaderScriptsOutputDirectory)
		else:
			loaderScript = File(os.path.join(self._ioDirectory, template._datas.outputScript))

		LOGGER.debug("> Loader Script Output File Path: '{0}'.".format(loaderScript.file))

		loaderScript.content = self.getLoaderScript(template._datas.path, iblSet._datas.path, self._overrideKeys)
		if loaderScript.content and loaderScript.write():
			messageBox.messageBox("Information", "Information", "{0} | '{1}' Output Done!".format(self.__class__.__name__, template._datas.outputScript))
			return True
		else:
			raise Exception, "{0} | '{1}' Output Failed!".format(self.__class__.__name__, template._datas.outputScript)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getLoaderScript(self, template, iblSet, overrideKeys):
		'''
		This Method Build A Loader Script.
		
		@param template: Template Path. ( String )
		@param iblSet: iblSet Path. ( String )
		@param overrideKeys: Override Keys. ( Dictionary )
		@return: Loader Script. ( List )
		'''

		LOGGER.debug("> Parsing Template File: '{0}'.".format(template))
		templateParser = Parser(template)
		templateParser.read() and templateParser.parse(rawSections=(self._templateScriptSection))
		templateSections = dict.copy(templateParser.sections)

		for attribute, value in dict.copy(templateSections[self._templateIblAttributesSection]).items():
			templateSections[self._templateIblAttributesSection][namespace.removeNamespace(attribute, rootOnly=True)] = value
			del templateSections[self._templateIblAttributesSection][attribute]

		LOGGER.debug("> Binding Templates File Attributes.")
		bindedAttributes = dict(((attribute, foundations.parser.getAttributeCompound(attribute, value)) for section in templateSections.keys() if section not in (self._templateScriptSection) for attribute, value in templateSections[section].items()))

		LOGGER.debug("> Parsing Ibl Set File: '{0}'.".format(iblSet))
		iblSetParser = Parser(iblSet)
		iblSetParser.read() and iblSetParser.parse()
		iblSetSections = dict.copy(iblSetParser.sections)

		LOGGER.debug("> Flattening Ibl Set File Attributes.")
		flattenedIblAttributes = dict(((attribute, foundations.parser.getAttributeCompound(attribute, value)) for section in iblSetSections.keys() for attribute, value in iblSetSections[section].items()))

		for attribute in flattenedIblAttributes:
			if attribute in bindedAttributes.keys():
				bindedAttributes[attribute].value = flattenedIblAttributes[attribute].value

		if "Lights|DynamicLights" in bindedAttributes.keys():
			LOGGER.debug("> Building '{0}' Custom Attribute.".format("Lights|DynamicLights"))
			dynamicLights = []
			for section in iblSetSections:
				if re.search("Light[0-9]*", section):
					dynamicLights.append(section)
					lightName = iblSetParser.getValue("LIGHTname", section)
					dynamicLights.append(lightName and lightName or self._unnamedLightName)
					lightColorTokens = iblSetParser.getValue("LIGHTcolor", section).split(",")
					for color in lightColorTokens:
						dynamicLights.append(color)
					dynamicLights.append(iblSetParser.getValue("LIGHTmulti", section))
					dynamicLights.append(iblSetParser.getValue("LIGHTu", section))
					dynamicLights.append(iblSetParser.getValue("LIGHTv", section))

			LOGGER.debug("> Adding '{0}' Custom Attribute With Value: '{1}'.".format("Lights|DynamicLights", ", ".join(dynamicLights)))
			bindedAttributes["Lights|DynamicLights"].value = self._defaultStringSeparator.join(dynamicLights)

		LOGGER.debug("> Updating Attributes With Override Keys.")
		for attribute in overrideKeys:
			if attribute in bindedAttributes.keys():
				bindedAttributes[attribute].value = overrideKeys[attribute] and overrideKeys[attribute].value or None

		LOGGER.debug("> Updating Loader Script Content.")
		loaderScript = templateParser.sections[self._templateScriptSection][namespace.setNamespace("Script", templateParser.rawSectionContentIdentifier)]

		bindedLoaderScript = []
		for line in loaderScript:
			bindingParameters = re.findall("{0}".format(self._bindingIdentifierPattern), line)
			if bindingParameters:
				for parameter in bindingParameters:
					for attribute in bindedAttributes.values():
						if parameter == attribute.link:
							LOGGER.debug("> Updating Loader Script Parameter '{0}' With Value: '{1}'.".format(parameter, attribute.value))
							line = line.replace(parameter, attribute.value and attribute.value or "-1")
			bindedLoaderScript.append(line)

		return bindedLoaderScript

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
