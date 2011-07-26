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
# If You Are A HDRI Resources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**loaderScript.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Loader Script Component Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports.
#***********************************************************************************************
import logging
import os
import platform
import re
import socket
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.parser
import foundations.strings as strings
import umbra.components.core.db.dbUtilities.types as dbTypes
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from foundations.io import File
from foundations.parser import Parser
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions.
#***********************************************************************************************
class LoaderScript(UiComponent):
	"""
	This Class Is The LoaderScript Class.
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

		self.__uiPath = "ui/Loader_Script.ui"
		self.__dockArea = 2

		self.__container = None

		self.__coreDatabaseBrowser = None
		self.__coreTemplatesOutliner = None

		self.__ioDirectory = "loaderScripts/"

		self.__bindingIdentifierPattern = "@[a-zA-Z0-9_]*"
		self.__templateScriptSection = "Script"
		self.__templateIblSetAttributesSection = "Ibl Set Attributes"
		self.__templateRemoteConnectionSection = "Remote Connection"

		self.__win32ExecutionMethod = "ExecuteSIBLLoaderScript"

		self.__overrideKeys = {}

		self.__defaultStringSeparator = "|"
		self.__unnamedLightName = "Unnamed_Light"

	#***********************************************************************************************
	#***	Attributes Properties.
	#***********************************************************************************************
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
	def ioDirectory(self):
		"""
		This Method Is The Property For The _ioDirectory Attribute.

		@return: self.__ioDirectory. ( String )
		"""

		return self.__ioDirectory

	@ioDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self, value):
		"""
		This Method Is The Setter Method For The _ioDirectory Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("ioDirectory"))

	@ioDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self):
		"""
		This Method Is The Deleter Method For The _ioDirectory Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("ioDirectory"))

	@property
	def bindingIdentifierPattern(self):
		"""
		This Method Is The Property For The _bindingIdentifierPattern Attribute.

		@return: self.__bindingIdentifierPattern. ( String )
		"""

		return self.__bindingIdentifierPattern

	@bindingIdentifierPattern.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def bindingIdentifierPattern(self, value):
		"""
		This Method Is The Setter Method For The _bindingIdentifierPattern Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("bindingIdentifierPattern"))

	@bindingIdentifierPattern.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def bindingIdentifierPattern(self):
		"""
		This Method Is The Deleter Method For The _bindingIdentifierPattern Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("bindingIdentifierPattern"))

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
	def templateIblSetAttributesSection(self):
		"""
		This Method Is The Property For The _templateIblSetAttributesSection Attribute.

		@return: self.__templateIblSetAttributesSection. ( String )
		"""

		return self.__templateIblSetAttributesSection

	@templateIblSetAttributesSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateIblSetAttributesSection(self, value):
		"""
		This Method Is The Setter Method For The _templateIblSetAttributesSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templateIblSetAttributesSection"))

	@templateIblSetAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateIblSetAttributesSection(self):
		"""
		This Method Is The Deleter Method For The _templateIblSetAttributesSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templateIblSetAttributesSection"))

	@property
	def templateRemoteConnectionSection(self):
		"""
		This Method Is The Property For The _templateRemoteConnectionSection Attribute.

		@return: self.__templateRemoteConnectionSection. ( String )
		"""

		return self.__templateRemoteConnectionSection

	@templateRemoteConnectionSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateRemoteConnectionSection(self, value):
		"""
		This Method Is The Setter Method For The _templateRemoteConnectionSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templateRemoteConnectionSection"))

	@templateRemoteConnectionSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateRemoteConnectionSection(self):
		"""
		This Method Is The Deleter Method For The _templateRemoteConnectionSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templateRemoteConnectionSection"))

	@property
	def overrideKeys(self):
		"""
		This Method Is The Property For The _overrideKeys Attribute.

		@return: self.__overrideKeys. ( Dictionary )
		"""

		return self.__overrideKeys

	@overrideKeys.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overrideKeys(self, value):
		"""
		This Method Is The Setter Method For The _overrideKeys Attribute.

		@param value: Attribute Value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' Attribute: '{1}' Type Is Not 'dict'!".format("sections", value)
		self.__overrideKeys = value

	@overrideKeys.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overrideKeys(self):
		"""
		This Method Is The Deleter Method For The _overrideKeys Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("overrideKeys"))

	@property
	def defaultStringSeparator(self):
		"""
		This Method Is The Property For The _defaultStringSeparator Attribute.

		@return: self.__defaultStringSeparator. ( String )
		"""

		return self.__defaultStringSeparator

	@defaultStringSeparator.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultStringSeparator(self, value):
		"""
		This Method Is The Setter Method For The _defaultStringSeparator Attribute.

		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("defaultStringSeparator", value)
			assert len(value) == 1, "'{0}' Attribute: '{1}' Has Multiples Characters!".format("defaultStringSeparator", value)
			assert not re.search("\w", value), "'{0}' Attribute: '{1}' Is An AlphaNumeric Character!".format("defaultStringSeparator", value)
		self.__defaultStringSeparator = value

	@defaultStringSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultStringSeparator(self):
		"""
		This Method Is The Deleter Method For The _defaultStringSeparator Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("defaultStringSeparator"))

	@property
	def unnamedLightName(self):
		"""
		This Method Is The Property For The _unnamedLightName Attribute.

		@return: self.__unnamedLightName. ( String )
		"""

		return self.__unnamedLightName

	@unnamedLightName.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def unnamedLightName(self, value):
		"""
		This Method Is The Setter Method For The _unnamedLightName Attribute.

		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("unnamedLightName", value)
		self.__unnamedLightName = value

	@unnamedLightName.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def unnamedLightName(self):
		"""
		This Method Is The Deleter Method For The _unnamedLightName Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("unnamedLightName"))

	#***********************************************************************************************
	#***	Class Methods.
	#***********************************************************************************************
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
		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface

		self.__ioDirectory = os.path.join(self.__container.userApplicationDatasDirectory, Constants.ioDirectory, self.__ioDirectory)
		not os.path.exists(self.__ioDirectory) and os.makedirs(self.__ioDirectory)

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""
		raise
		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__container = None

		self.__coreDatabaseBrowser = None
		self.__coreTemplatesOutliner = None

		self.__ioDirectory = os.path.basename(os.path.abspath(self.__ioDirectory))

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.ui.Remote_Connection_groupBox.hide()
		if platform.system() == "Linux" or platform.system() == "Darwin":
			self.ui.Options_groupBox.hide()

		# Signals / Slots.
		self.ui.Output_Loader_Script_pushButton.clicked.connect(self.__Output_Loader_Script_pushButton__clicked)
		self.ui.Send_To_Software_pushButton.clicked.connect(self.__Send_To_Software_pushButton__clicked)
		self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.connect(self.__coreTemplatesOutlinerUi_Templates_Outliner_treeView_selectionModel_selectionChanged)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Output_Loader_Script_pushButton.clicked.disconnect(self.__Output_Loader_Script_pushButton__clicked)
		self.ui.Send_To_Software_pushButton.clicked.disconnect(self.__Send_To_Software_pushButton__clicked)
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
	def __Output_Loader_Script_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Output_Loader_Script_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.outputLoaderScript__()

	@core.executionTrace
	def __Send_To_Software_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Send_To_Software_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.sendLoaderScriptToSoftware__()

	@core.executionTrace
	def __coreTemplatesOutlinerUi_Templates_Outliner_treeView_selectionModel_selectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Is Triggered When coreTemplatesOutlinerUi_Templates_Outliner_treeView Selection Has Changed.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None

		if template:
			LOGGER.debug("> Parsing '{0}' Template For '{1}' Section.".format(template.name, self.__templateRemoteConnectionSection))

			if os.path.exists(template.path):
				templateParser = Parser(template.path)
				templateParser.read() and templateParser.parse(rawSections=(self.__templateScriptSection))

				if self.__templateRemoteConnectionSection in templateParser.sections:
					LOGGER.debug("> {0}' Section Found.".format(self.__templateRemoteConnectionSection))
					self.ui.Remote_Connection_groupBox.show()
					connectionType = foundations.parser.getAttributeCompound("ConnectionType", templateParser.getValue("ConnectionType", self.__templateRemoteConnectionSection))
					if connectionType.value == "Socket":
						LOGGER.debug("> Remote Connection Type: 'Socket'.")
						self.ui.Software_Port_spinBox.setValue(int(foundations.parser.getAttributeCompound("DefaultPort", templateParser.getValue("DefaultPort", self.__templateRemoteConnectionSection)).value))
						self.ui.Address_lineEdit.setText(QString(foundations.parser.getAttributeCompound("DefaultAddress", templateParser.getValue("DefaultAddress", self.__templateRemoteConnectionSection)).value))
						self.ui.Remote_Connection_Options_frame.show()
					elif connectionType.value == "Win32":
						LOGGER.debug("> Remote Connection: 'Win32'.")
						self.ui.Remote_Connection_Options_frame.hide()
				else:
					self.ui.Remote_Connection_groupBox.hide()
		else:
			self.ui.Remote_Connection_groupBox.hide()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError, OSError, Exception)
	def outputLoaderScript__(self):
		"""
		This Method Outputs The Loader Script.
		
		@return: Method Success. ( Boolean )
		"""

		LOGGER.debug("> Initializing Loader Script Output.")

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		if selectedTemplates and len(selectedTemplates) != 1:
			messageBox.messageBox("Information", "Information", "{0} | Multiple Selected Templates, '{1}' Will Be Used!".format(self.__class__.__name__, selectedTemplates[0].name))

		template = selectedTemplates and selectedTemplates[0] or None

		if not template:
			raise foundations.exceptions.UserError, "{0} | In Order To Output The Loader Script, You Need To Select A Template!".format(self.__class__.__name__)

		if not os.path.exists(template.path):
			raise OSError, "{0} | '{1}' Template File Doesn't Exists!".format(self.__class__.__name__, template.name)

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
		iblSet = selectedIblSets and selectedIblSets[0] or None
		if not iblSet:
			raise foundations.exceptions.UserError, "{0} | In Order To Output The Loader Script, You Need To Select A Set!".format(self.__class__.__name__)

		if not os.path.exists(iblSet.path):
			raise OSError, "{0} | '{1}' Ibl Set File Doesn't Exists!".format(self.__class__.__name__, iblSet.title)

		if self.outputLoaderScript(template, iblSet):
			messageBox.messageBox("Information", "Information", "{0} | '{1}' Output Done!".format(self.__class__.__name__, template.outputScript))
			return True
		else:
			raise Exception, "{0} | Exception Raised: '{1}' Output Failed!".format(self.__class__.__name__, template.outputScript)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def sendLoaderScriptToSoftware__(self):
		"""
		This Method Sends The Output Loader Script To Associated Package.
		
		@return: Method Success. ( Boolean )
		"""

		if self.outputLoaderScript__():
			selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
			template = selectedTemplates and selectedTemplates[0] or None
			if not template:
				return

			loaderScriptPath = strings.getNormalizedPath(os.path.join(self.__ioDirectory, template.outputScript))
			if self.ui.Convert_To_Posix_Paths_checkBox.isChecked():
				loaderScriptPath = strings.toPosixPath(loaderScriptPath)
			if not self.sendLoaderScriptToSoftware(template, loaderScriptPath):
				raise Exception, "{0} | Exception Raised While Sending Loader Script!".format(self.__class__.__name__)
		else:
			raise Exception, "{0} | Exception Raised While Outputing Loader Script!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def outputLoaderScript(self, template, iblSet):
		"""
		This Method Outputs The Loader Script.

		@param template: Template. ( DbTemplate )
		@param iblSet: Ibl Set. ( DbIblSet )	
		@return: Method Success. ( Boolean )
		"""

		self.__overrideKeys = self.getDefaultOverrideKeys()

		for component in self.__container.componentsManager.getComponents():
			profile = self.__container.componentsManager.components[component]
			interface = self.__container.componentsManager.getInterface(component)
			if interface.activated and profile.name != self.name:
				hasattr(interface, "getOverrideKeys") and interface.getOverrideKeys()

		if self.__container.parameters.loaderScriptsOutputDirectory:
			if os.path.exists(self.__container.parameters.loaderScriptsOutputDirectory):
				loaderScript = File(os.path.join(self.__container.parameters.loaderScriptsOutputDirectory, template.outputScript))
			else:
				raise OSError, "{0} | '{1}' Loader Script Output Directory Doesn't Exists!".format(self.__class__.__name__, self.__container.parameters.loaderScriptsOutputDirectory)
		else:
			loaderScript = File(os.path.join(self.__ioDirectory, template.outputScript))

		LOGGER.debug("> Loader Script Output File Path: '{0}'.".format(loaderScript.file))

		loaderScript.content = self.getLoaderScript(template.path, iblSet.path, self.__overrideKeys)

		if loaderScript.content and loaderScript.write():
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.SocketConnectionError)
	def sendLoaderScriptToSoftware(self, template, loaderScriptPath):
		"""
		This Method Sends The Loader Script To Associated Package.
		
		@param template: Template. ( DbTemplate )
		@param loaderScriptPath: Loader Script Path. ( String )
		@return: Method Success. ( Boolean )
		"""

		LOGGER.info("{0} | Starting Remote Connection!".format(self.__class__.__name__))
		templateParser = Parser(template.path)
		templateParser.read() and templateParser.parse(rawSections=(self.__templateScriptSection))
		connectionType = foundations.parser.getAttributeCompound("ConnectionType", templateParser.getValue("ConnectionType", self.__templateRemoteConnectionSection))

		if connectionType.value == "Socket":
			try:
				connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				connection.connect((str(self.ui.Address_lineEdit.text()), int(self.ui.Software_Port_spinBox.value())))
				socketCommand = foundations.parser.getAttributeCompound("ExecutionCommand", templateParser.getValue("ExecutionCommand", self.__templateRemoteConnectionSection)).value.replace("$loaderScriptPath", loaderScriptPath)
				LOGGER.debug("> Current Socket Command: '%s'.", socketCommand)
				connection.send(socketCommand)
				dataBack = connection.recv(8192)
				LOGGER.debug("> Received Back From Application: '%s'", dataBack)
				connection.close()
				LOGGER.info("{0} | Ending Remote Connection!".format(self.__class__.__name__))
			except Exception as error:
				raise foundations.exceptions.SocketConnectionError, "{0} | Socket Connection Error: '{1}'!".format(self.__class__.__name__, error)
		elif connectionType.value == "Win32":
			if platform.system() == "Windows" or platform.system() == "Microsoft":
				try:
					import win32com.client
					connection = win32com.client.Dispatch(foundations.parser.getAttributeCompound("TargetApplication", templateParser.getValue("TargetApplication", self.__templateRemoteConnectionSection)).value)
					connection._FlagAsMethod(self.__win32ExecutionMethod)
					connectionCommand = foundations.parser.getAttributeCompound("ExecutionCommand", templateParser.getValue("ExecutionCommand", self.__templateRemoteConnectionSection)).value.replace("$loaderScriptPath", loaderScriptPath)
					LOGGER.debug("> Current Connection Command: '%s'.", connectionCommand)
					getattr(connection, self.__win32ExecutionMethod)(connectionCommand)
				except Exception as error:
					raise foundations.exceptions.SocketConnectionError, "{0} | Win32 OLE Server Connection Error: '{1}'!".format(self.__class__.__name__, error)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getDefaultOverrideKeys(self):
		"""
		This Method Gets Default Override Keys.

		@return: Override Keys. ( Dictionary )
		"""

		LOGGER.debug("> Constructing Default Override Keys.")

		overrideKeys = {}

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None

		if template:
			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format("Template|Path", template.path))
			overrideKeys["Template|Path"] = foundations.parser.getAttributeCompound("Template|Path", template.path)

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
		iblSet = selectedIblSets and selectedIblSets[0] or None
		if iblSet:
			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format("Ibl Set|Path", iblSet.path))
			overrideKeys["Ibl Set|Path"] = iblSet.path and foundations.parser.getAttributeCompound("Ibl Set|Path", strings.getNormalizedPath(iblSet.path))

			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format("Background|BGfile", iblSet.backgroundImage))
			overrideKeys["Background|BGfile"] = iblSet.backgroundImage and foundations.parser.getAttributeCompound("Background|BGfile", strings.getNormalizedPath(iblSet.backgroundImage))

			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format("Enviroment|EVfile", iblSet.lightingImage))
			overrideKeys["Enviroment|EVfile"] = iblSet.lightingImage and foundations.parser.getAttributeCompound("Enviroment|EVfile", strings.getNormalizedPath(iblSet.lightingImage))

			LOGGER.debug("> Adding '{0}' Override Key With Value: '{1}'.".format("Reflection|REFfile", iblSet.reflectionImage))
			overrideKeys["Reflection|REFfile"] = iblSet.reflectionImage and foundations.parser.getAttributeCompound("Reflection|REFfile", strings.getNormalizedPath(iblSet.reflectionImage))
		return overrideKeys

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getLoaderScript(self, template, iblSet, overrideKeys):
		"""
		This Method Builds A Loader Script.
		
		@param template: Template Path. ( String )
		@param iblSet: iblSet Path. ( String )
		@param overrideKeys: Override Keys. ( Dictionary )
		@return: Loader Script. ( List )
		"""

		LOGGER.debug("> Parsing Template File: '{0}'.".format(template))
		templateParser = Parser(template)
		templateParser.read() and templateParser.parse(rawSections=(self.__templateScriptSection))
		templateSections = dict.copy(templateParser.sections)

		for attribute, value in dict.copy(templateSections[self.__templateIblSetAttributesSection]).items():
			templateSections[self.__templateIblSetAttributesSection][namespace.removeNamespace(attribute, rootOnly=True)] = value
			del templateSections[self.__templateIblSetAttributesSection][attribute]

		LOGGER.debug("> Binding Templates File Attributes.")
		bindedAttributes = dict(((attribute, foundations.parser.getAttributeCompound(attribute, value)) for section in templateSections.keys() if section not in (self.__templateScriptSection) for attribute, value in templateSections[section].items()))

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
				if re.search("Light[0-9]+", section):
					dynamicLights.append(section)
					lightName = iblSetParser.getValue("LIGHTname", section)
					dynamicLights.append(lightName and lightName or self.__unnamedLightName)
					lightColorTokens = iblSetParser.getValue("LIGHTcolor", section).split(",")
					for color in lightColorTokens:
						dynamicLights.append(color)
					dynamicLights.append(iblSetParser.getValue("LIGHTmulti", section))
					dynamicLights.append(iblSetParser.getValue("LIGHTu", section))
					dynamicLights.append(iblSetParser.getValue("LIGHTv", section))

			LOGGER.debug("> Adding '{0}' Custom Attribute With Value: '{1}'.".format("Lights|DynamicLights", ", ".join(dynamicLights)))
			bindedAttributes["Lights|DynamicLights"].value = self.__defaultStringSeparator.join(dynamicLights)

		LOGGER.debug("> Updating Attributes With Override Keys.")
		for attribute in overrideKeys:
			if attribute in bindedAttributes.keys():
				bindedAttributes[attribute].value = overrideKeys[attribute] and overrideKeys[attribute].value or None

		LOGGER.debug("> Updating Loader Script Content.")
		loaderScript = templateParser.sections[self.__templateScriptSection][namespace.setNamespace("Script", templateParser.rawSectionContentIdentifier)]

		bindedLoaderScript = []
		for line in loaderScript:
			bindingParameters = re.findall("{0}".format(self.__bindingIdentifierPattern), line)
			if bindingParameters:
				for parameter in bindingParameters:
					for attribute in bindedAttributes.values():
						if parameter == attribute.link:
							LOGGER.debug("> Updating Loader Script Parameter '{0}' With Value: '{1}'.".format(parameter, attribute.value))
							line = line.replace(parameter, attribute.value and attribute.value or "-1")
			bindedLoaderScript.append(line)
		return bindedLoaderScript

#***********************************************************************************************
#***	Python End.
#***********************************************************************************************
