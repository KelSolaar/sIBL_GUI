#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**loaderScript.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Loader Script Component Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import platform
import re
import socket
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
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
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LoaderScript(UiComponent):
	"""
	This class is the **LoaderScript** class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		:param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
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
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for **self.__uiPath** attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for **self.__uiPath** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for **self.__uiPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def dockArea(self):
		"""
		This method is the property for **self.__dockArea** attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def coreTemplatesOutliner(self):
		"""
		This method is the property for **self.__coreTemplatesOutliner** attribute.

		:return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This method is the setter method for **self.__coreTemplatesOutliner** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This method is the deleter method for **self.__coreTemplatesOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreTemplatesOutliner"))

	@property
	def ioDirectory(self):
		"""
		This method is the property for **self.__ioDirectory** attribute.

		:return: self.__ioDirectory. ( String )
		"""

		return self.__ioDirectory

	@ioDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self, value):
		"""
		This method is the setter method for **self.__ioDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("ioDirectory"))

	@ioDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self):
		"""
		This method is the deleter method for **self.__ioDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("ioDirectory"))

	@property
	def bindingIdentifierPattern(self):
		"""
		This method is the property for **self.__bindingIdentifierPattern** attribute.

		:return: self.__bindingIdentifierPattern. ( String )
		"""

		return self.__bindingIdentifierPattern

	@bindingIdentifierPattern.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def bindingIdentifierPattern(self, value):
		"""
		This method is the setter method for **self.__bindingIdentifierPattern** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("bindingIdentifierPattern"))

	@bindingIdentifierPattern.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def bindingIdentifierPattern(self):
		"""
		This method is the deleter method for **self.__bindingIdentifierPattern** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("bindingIdentifierPattern"))

	@property
	def templateScriptSection(self):
		"""
		This method is the property for **self.__templateScriptSection** attribute.

		:return: self.__templateScriptSection. ( String )
		"""

		return self.__templateScriptSection

	@templateScriptSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateScriptSection(self, value):
		"""
		This method is the setter method for **self.__templateScriptSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templateScriptSection"))

	@templateScriptSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateScriptSection(self):
		"""
		This method is the deleter method for **self.__templateScriptSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templateScriptSection"))

	@property
	def templateIblSetAttributesSection(self):
		"""
		This method is the property for **self.__templateIblSetAttributesSection** attribute.

		:return: self.__templateIblSetAttributesSection. ( String )
		"""

		return self.__templateIblSetAttributesSection

	@templateIblSetAttributesSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateIblSetAttributesSection(self, value):
		"""
		This method is the setter method for **self.__templateIblSetAttributesSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templateIblSetAttributesSection"))

	@templateIblSetAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateIblSetAttributesSection(self):
		"""
		This method is the deleter method for **self.__templateIblSetAttributesSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templateIblSetAttributesSection"))

	@property
	def templateRemoteConnectionSection(self):
		"""
		This method is the property for **self.__templateRemoteConnectionSection** attribute.

		:return: self.__templateRemoteConnectionSection. ( String )
		"""

		return self.__templateRemoteConnectionSection

	@templateRemoteConnectionSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateRemoteConnectionSection(self, value):
		"""
		This method is the setter method for **self.__templateRemoteConnectionSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templateRemoteConnectionSection"))

	@templateRemoteConnectionSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateRemoteConnectionSection(self):
		"""
		This method is the deleter method for **self.__templateRemoteConnectionSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templateRemoteConnectionSection"))

	@property
	def overrideKeys(self):
		"""
		This method is the property for **self.__overrideKeys** attribute.

		:return: self.__overrideKeys. ( Dictionary )
		"""

		return self.__overrideKeys

	@overrideKeys.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overrideKeys(self, value):
		"""
		This method is the setter method for **self.__overrideKeys** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("sections", value)
		self.__overrideKeys = value

	@overrideKeys.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overrideKeys(self):
		"""
		This method is the deleter method for **self.__overrideKeys** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("overrideKeys"))

	@property
	def defaultStringSeparator(self):
		"""
		This method is the property for **self.__defaultStringSeparator** attribute.

		:return: self.__defaultStringSeparator. ( String )
		"""

		return self.__defaultStringSeparator

	@defaultStringSeparator.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultStringSeparator(self, value):
		"""
		This method is the setter method for **self.__defaultStringSeparator** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("defaultStringSeparator", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("defaultStringSeparator", value)
			assert not re.search("\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format("defaultStringSeparator", value)
		self.__defaultStringSeparator = value

	@defaultStringSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultStringSeparator(self):
		"""
		This method is the deleter method for **self.__defaultStringSeparator** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultStringSeparator"))

	@property
	def unnamedLightName(self):
		"""
		This method is the property for **self.__unnamedLightName** attribute.

		:return: self.__unnamedLightName. ( String )
		"""

		return self.__unnamedLightName

	@unnamedLightName.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def unnamedLightName(self, value):
		"""
		This method is the setter method for **self.__unnamedLightName** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("unnamedLightName", value)
		self.__unnamedLightName = value

	@unnamedLightName.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def unnamedLightName(self):
		"""
		This method is the deleter method for **self.__unnamedLightName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("unnamedLightName"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
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
		This method deactivates the Component.
		"""

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
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.ui.Remote_Connection_groupBox.hide()
		if platform.system() == "Linux" or platform.system() == "Darwin":
			self.ui.Options_groupBox.hide()

		# Signals / Slots.
		self.ui.Output_Loader_Script_pushButton.clicked.connect(self.__Output_Loader_Script_pushButton__clicked)
		self.ui.Send_To_Software_pushButton.clicked.connect(self.__Send_To_Software_pushButton__clicked)
		self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.connect(self.__coreTemplatesOutliner_Templates_Outliner_treeView_selectionModel_selectionChanged)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Output_Loader_Script_pushButton.clicked.disconnect(self.__Output_Loader_Script_pushButton__clicked)
		self.ui.Send_To_Software_pushButton.clicked.disconnect(self.__Send_To_Software_pushButton__clicked)
		self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.disconnect(self.__coreTemplatesOutliner_Templates_Outliner_treeView_selectionModel_selectionChanged)

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self.ui)
		self.ui.setParent(None)

	@core.executionTrace
	def __Output_Loader_Script_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Output_Loader_Script_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.outputLoaderScript__()

	@core.executionTrace
	def __Send_To_Software_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Send_To_Software_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.sendLoaderScriptToSoftware__()

	@core.executionTrace
	def __coreTemplatesOutliner_Templates_Outliner_treeView_selectionModel_selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when **coreTemplatesOutliner.Templates_Outliner_treeView** selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None

		if template:
			LOGGER.debug("> Parsing '{0}' Template for '{1}' section.".format(template.name, self.__templateRemoteConnectionSection))

			if os.path.exists(template.path):
				templateParser = Parser(template.path)
				templateParser.read() and templateParser.parse(rawSections=(self.__templateScriptSection))

				if self.__templateRemoteConnectionSection in templateParser.sections:
					LOGGER.debug("> {0}' section found.".format(self.__templateRemoteConnectionSection))
					self.ui.Remote_Connection_groupBox.show()
					connectionType = foundations.parser.getAttributeCompound("ConnectionType", templateParser.getValue("ConnectionType", self.__templateRemoteConnectionSection))
					if connectionType.value == "Socket":
						LOGGER.debug("> Remote connection type: 'Socket'.")
						self.ui.Software_Port_spinBox.setValue(int(foundations.parser.getAttributeCompound("DefaultPort", templateParser.getValue("DefaultPort", self.__templateRemoteConnectionSection)).value))
						self.ui.Address_lineEdit.setText(QString(foundations.parser.getAttributeCompound("DefaultAddress", templateParser.getValue("DefaultAddress", self.__templateRemoteConnectionSection)).value))
						self.ui.Remote_Connection_Options_frame.show()
					elif connectionType.value == "Win32":
						LOGGER.debug("> Remote connection: 'Win32'.")
						self.ui.Remote_Connection_Options_frame.hide()
				else:
					self.ui.Remote_Connection_groupBox.hide()
		else:
			self.ui.Remote_Connection_groupBox.hide()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError, OSError, Exception)
	def outputLoaderScript__(self):
		"""
		This method outputs the Loader Script.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing Loader Script output.")

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		if selectedTemplates and len(selectedTemplates) != 1:
			messageBox.messageBox("Information", "Information", "{0} | Multiple selected Templates, '{1}' will be used!".format(self.__class__.__name__, selectedTemplates[0].name))

		template = selectedTemplates and selectedTemplates[0] or None

		if not template:
			raise foundations.exceptions.UserError, "{0} | In order to output the Loader Script, you need to select a Template!".format(self.__class__.__name__)

		if not os.path.exists(template.path):
			raise OSError, "{0} | '{1}' Template file doesn't exists!".format(self.__class__.__name__, template.name)

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
		iblSet = selectedIblSets and selectedIblSets[0] or None
		if not iblSet:
			raise foundations.exceptions.UserError, "{0} | In order to output the Loader Script, you need to select an Ibl Set!".format(self.__class__.__name__)

		if not os.path.exists(iblSet.path):
			raise OSError, "{0} | '{1}' Ibl Set file doesn't exists!".format(self.__class__.__name__, iblSet.title)

		if self.outputLoaderScript(template, iblSet):
			messageBox.messageBox("Information", "Information", "{0} | '{1}' output done!".format(self.__class__.__name__, template.outputScript))
			return True
		else:
			raise Exception, "{0} | Exception raised: '{1}' output failed!".format(self.__class__.__name__, template.outputScript)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def sendLoaderScriptToSoftware__(self):
		"""
		This method sends the output Loader Script to associated package.

		:return: Method success. ( Boolean )
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
				raise Exception, "{0} | Exception raised while sending Loader Script!".format(self.__class__.__name__)
		else:
			raise Exception, "{0} | Exception raised while outputing Loader Script!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def outputLoaderScript(self, template, iblSet):
		"""
		This method outputs the Loader Script.

		:param template: Template. ( DbTemplate )
		:param iblSet: Ibl Set. ( DbIblSet )
		:return: Method success. ( Boolean )
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
				raise OSError, "{0} | '{1}' loader Script output directory doesn't exists!".format(self.__class__.__name__, self.__container.parameters.loaderScriptsOutputDirectory)
		else:
			loaderScript = File(os.path.join(self.__ioDirectory, template.outputScript))

		LOGGER.debug("> Loader Script output file path: '{0}'.".format(loaderScript.file))

		loaderScript.content = self.getLoaderScript(template.path, iblSet.path, self.__overrideKeys)

		if loaderScript.content and loaderScript.write():
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.SocketConnectionError)
	def sendLoaderScriptToSoftware(self, template, loaderScriptPath):
		"""
		This method sends the Loader Script to associated package.

		:param template: Template. ( DbTemplate )
		:param loaderScriptPath: Loader Script path. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Starting remote connection!".format(self.__class__.__name__))
		templateParser = Parser(template.path)
		templateParser.read() and templateParser.parse(rawSections=(self.__templateScriptSection))
		connectionType = foundations.parser.getAttributeCompound("ConnectionType", templateParser.getValue("ConnectionType", self.__templateRemoteConnectionSection))

		if connectionType.value == "Socket":
			try:
				connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				connection.connect((str(self.ui.Address_lineEdit.text()), int(self.ui.Software_Port_spinBox.value())))
				socketCommand = foundations.parser.getAttributeCompound("ExecutionCommand", templateParser.getValue("ExecutionCommand", self.__templateRemoteConnectionSection)).value.replace("$loaderScriptPath", loaderScriptPath)
				LOGGER.debug("> Current socket command: '%s'.", socketCommand)
				connection.send(socketCommand)
				dataBack = connection.recv(8192)
				LOGGER.debug("> Received back from Application: '%s'", dataBack)
				connection.close()
				LOGGER.info("{0} | Ending remote connection!".format(self.__class__.__name__))
			except Exception as error:
				raise foundations.exceptions.SocketConnectionError, "{0} | Socket connection error: '{1}'!".format(self.__class__.__name__, error)
		elif connectionType.value == "Win32":
			if platform.system() == "Windows" or platform.system() == "Microsoft":
				try:
					import win32com.client
					connection = win32com.client.Dispatch(foundations.parser.getAttributeCompound("TargetApplication", templateParser.getValue("TargetApplication", self.__templateRemoteConnectionSection)).value)
					connection._FlagAsMethod(self.__win32ExecutionMethod)
					connectionCommand = foundations.parser.getAttributeCompound("ExecutionCommand", templateParser.getValue("ExecutionCommand", self.__templateRemoteConnectionSection)).value.replace("$loaderScriptPath", loaderScriptPath)
					LOGGER.debug("> Current connection command: '%s'.", connectionCommand)
					getattr(connection, self.__win32ExecutionMethod)(connectionCommand)
				except Exception as error:
					raise foundations.exceptions.SocketConnectionError, "{0} | Win32 OLE server connection error: '{1}'!".format(self.__class__.__name__, error)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getDefaultOverrideKeys(self):
		"""
		This method gets default override keys.

		:return: Override keys. ( Dictionary )
		"""

		LOGGER.debug("> Constructing default override keys.")

		overrideKeys = {}

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None

		if template:
			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Template|Path", template.path))
			overrideKeys["Template|Path"] = foundations.parser.getAttributeCompound("Template|Path", template.path)

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
		iblSet = selectedIblSets and selectedIblSets[0] or None
		if iblSet:
			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Ibl Set|Path", iblSet.path))
			overrideKeys["Ibl Set|Path"] = iblSet.path and foundations.parser.getAttributeCompound("Ibl Set|Path", strings.getNormalizedPath(iblSet.path))

			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Background|BGfile", iblSet.backgroundImage))
			overrideKeys["Background|BGfile"] = iblSet.backgroundImage and foundations.parser.getAttributeCompound("Background|BGfile", strings.getNormalizedPath(iblSet.backgroundImage))

			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Enviroment|EVfile", iblSet.lightingImage))
			overrideKeys["Enviroment|EVfile"] = iblSet.lightingImage and foundations.parser.getAttributeCompound("Enviroment|EVfile", strings.getNormalizedPath(iblSet.lightingImage))

			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Reflection|REFfile", iblSet.reflectionImage))
			overrideKeys["Reflection|REFfile"] = iblSet.reflectionImage and foundations.parser.getAttributeCompound("Reflection|REFfile", strings.getNormalizedPath(iblSet.reflectionImage))
		return overrideKeys

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getLoaderScript(self, template, iblSet, overrideKeys):
		"""
		This method builds a Loader Script.

		:param template: Template path. ( String )
		:param iblSet: iblSet path. ( String )
		:param overrideKeys: Override keys. ( Dictionary )
		:return: Loader Script. ( List )
		"""

		LOGGER.debug("> Parsing Template file: '{0}'.".format(template))
		templateParser = Parser(template)
		templateParser.read() and templateParser.parse(rawSections=(self.__templateScriptSection))
		templateSections = dict.copy(templateParser.sections)

		for attribute, value in dict.copy(templateSections[self.__templateIblSetAttributesSection]).items():
			templateSections[self.__templateIblSetAttributesSection][namespace.removeNamespace(attribute, rootOnly=True)] = value
			del templateSections[self.__templateIblSetAttributesSection][attribute]

		LOGGER.debug("> Binding Templates file attributes.")
		bindedAttributes = dict(((attribute, foundations.parser.getAttributeCompound(attribute, value)) for section in templateSections.keys() if section not in (self.__templateScriptSection) for attribute, value in templateSections[section].items()))

		LOGGER.debug("> Parsing Ibl Set file: '{0}'.".format(iblSet))
		iblSetParser = Parser(iblSet)
		iblSetParser.read() and iblSetParser.parse()
		iblSetSections = dict.copy(iblSetParser.sections)

		LOGGER.debug("> Flattening Ibl Set file attributes.")
		flattenedIblAttributes = dict(((attribute, foundations.parser.getAttributeCompound(attribute, value)) for section in iblSetSections.keys() for attribute, value in iblSetSections[section].items()))

		for attribute in flattenedIblAttributes:
			if attribute in bindedAttributes.keys():
				bindedAttributes[attribute].value = flattenedIblAttributes[attribute].value

		if "Lights|DynamicLights" in bindedAttributes.keys():
			LOGGER.debug("> Building '{0}' custom attribute.".format("Lights|DynamicLights"))
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

			LOGGER.debug("> Adding '{0}' custom attribute with value: '{1}'.".format("Lights|DynamicLights", ", ".join(dynamicLights)))
			bindedAttributes["Lights|DynamicLights"].value = self.__defaultStringSeparator.join(dynamicLights)

		LOGGER.debug("> Updating attributes with override keys.")
		for attribute in overrideKeys:
			if attribute in bindedAttributes.keys():
				bindedAttributes[attribute].value = overrideKeys[attribute] and overrideKeys[attribute].value or None

		LOGGER.debug("> Updating Loader Script content.")
		loaderScript = templateParser.sections[self.__templateScriptSection][namespace.setNamespace("Script", templateParser.rawSectionContentIdentifier)]

		bindedLoaderScript = []
		for line in loaderScript:
			bindingParameters = re.findall("{0}".format(self.__bindingIdentifierPattern), line)
			if bindingParameters:
				for parameter in bindingParameters:
					for attribute in bindedAttributes.values():
						if parameter == attribute.link:
							LOGGER.debug("> Updating Loader Script parameter '{0}' with value: '{1}'.".format(parameter, attribute.value))
							line = line.replace(parameter, attribute.value and attribute.value or "-1")
			bindedLoaderScript.append(line)
		return bindedLoaderScript
