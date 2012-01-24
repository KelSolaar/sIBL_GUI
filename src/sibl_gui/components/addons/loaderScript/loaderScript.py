#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**loaderScript.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`LoaderScript` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import platform
import re
import socket
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.parsers
import foundations.strings as strings
import sibl_gui.exceptions
import umbra.ui.common
from foundations.io import File
from foundations.parsers import SectionsFileParser
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_FILE", "LoaderScript"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_FILE = os.path.join(os.path.dirname(__file__), "ui", "Loader_Script.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LoaderScript(QWidgetComponentFactory(uiFile=COMPONENT_FILE)):
	"""
	| This class is the :mod:`umbra.components.addons.loaderScript.loaderScript` Component Interface class.
	| It provides the glue between the Ibl Sets, the Templates and the 3d package.
	
	A typical operation is the following:
	
		- Retrieve both Ibl Set and Template files.
		- Parse Ibl Set and Template files.
		- Retrieve override keys defined by the user and / or another Component. 
		- Generate the Loader Script.
		- Write the Loader Script.
		- Establish a connection with the 3d package and trigger the Loader Script execution.
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(LoaderScript, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__dockArea = 2

		self.__engine = None

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

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def engine(self):
		"""
		This method is the property for **self.__engine** attribute.

		:return: self.__engine. ( QObject )
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDatabaseBrowser"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This method is the deleter method for **self.__coreTemplatesOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreTemplatesOutliner"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ioDirectory"))

	@ioDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self):
		"""
		This method is the deleter method for **self.__ioDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ioDirectory"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "bindingIdentifierPattern"))

	@bindingIdentifierPattern.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def bindingIdentifierPattern(self):
		"""
		This method is the deleter method for **self.__bindingIdentifierPattern** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "bindingIdentifierPattern"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templateScriptSection"))

	@templateScriptSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateScriptSection(self):
		"""
		This method is the deleter method for **self.__templateScriptSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templateScriptSection"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templateIblSetAttributesSection"))

	@templateIblSetAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateIblSetAttributesSection(self):
		"""
		This method is the deleter method for **self.__templateIblSetAttributesSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templateIblSetAttributesSection"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templateRemoteConnectionSection"))

	@templateRemoteConnectionSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateRemoteConnectionSection(self):
		"""
		This method is the deleter method for **self.__templateRemoteConnectionSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templateRemoteConnectionSection"))

	@property
	def overrideKeys(self):
		"""
		This method is the property for **self.__overrideKeys** attribute.

		:return: self.__overrideKeys. ( Dictionary )
		"""

		return self.__overrideKeys

	@overrideKeys.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def overrideKeys(self, value):
		"""
		This method is the setter method for **self.__overrideKeys** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("overrideKeys", value)
			for key, element in value.iteritems():
				assert type(key) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"overrideKeys", key)
				assert type(element) is foundations.parsers.AttributeCompound, \
				"'{0}' attribute: '{1}' type is not 'foundations.parsers.AttributeCompound'!".format(
				"overrideKeys", element)
		self.__overrideKeys = value

	@overrideKeys.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def overrideKeys(self):
		"""
		This method is the deleter method for **self.__overrideKeys** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "overrideKeys"))

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

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"defaultStringSeparator", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format(
			"defaultStringSeparator", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
			"defaultStringSeparator", value)
		self.__defaultStringSeparator = value

	@defaultStringSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultStringSeparator(self):
		"""
		This method is the deleter method for **self.__defaultStringSeparator** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultStringSeparator"))

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

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"unnamedLightName", value)
		self.__unnamedLightName = value

	@unnamedLightName.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def unnamedLightName(self):
		"""
		This method is the deleter method for **self.__unnamedLightName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "unnamedLightName"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine

		self.__coreDatabaseBrowser = self.__engine.componentsManager.components["core.databaseBrowser"].interface
		self.__coreTemplatesOutliner = self.__engine.componentsManager.components["core.templatesOutliner"].interface

		self.__ioDirectory = os.path.join(self.__engine.userApplicationDataDirectory,
										Constants.ioDirectory,
										self.__ioDirectory)
		not foundations.common.pathExists(self.__ioDirectory) and os.makedirs(self.__ioDirectory)

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.__coreDatabaseBrowser = None
		self.__coreTemplatesOutliner = None

		self.__ioDirectory = os.path.basename(os.path.abspath(self.__ioDirectory))

		self.activated = False
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.Remote_Connection_groupBox.hide()
		if platform.system() == "Linux" or platform.system() == "Darwin":
			self.Options_groupBox.hide()

		# Signals / Slots.
		self.Output_Loader_Script_pushButton.clicked.connect(self.__Output_Loader_Script_pushButton__clicked)
		self.Send_To_Software_pushButton.clicked.connect(self.__Send_To_Software_pushButton__clicked)
		self.__coreTemplatesOutliner.view.selectionModel().selectionChanged.connect(
		self.__coreTemplatesOutliner_view_selectionModel__selectionChanged)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.Output_Loader_Script_pushButton.clicked.disconnect(self.__Output_Loader_Script_pushButton__clicked)
		self.Send_To_Software_pushButton.clicked.disconnect(self.__Send_To_Software_pushButton__clicked)
		self.__coreTemplatesOutliner.view.selectionModel().selectionChanged.disconnect(
		self.__coreTemplatesOutliner_view_selectionModel__selectionChanged)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	@core.executionTrace
	def __Output_Loader_Script_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Output_Loader_Script_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.outputLoaderScriptUi()

	@core.executionTrace
	def __Send_To_Software_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Send_To_Software_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.sendLoaderScriptToSoftwareUi()

	@core.executionTrace
	def __coreTemplatesOutliner_view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when **coreTemplatesOutliner.view** Model selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None
		if not (template and foundations.common.pathExists(template.path)):
			return

		LOGGER.debug("> Parsing '{0}' Template for '{1}' section.".format(template.name,
																	self.__templateRemoteConnectionSection))
		templateSectionsFileParser = SectionsFileParser(template.path)
		templateSectionsFileParser.read() and templateSectionsFileParser.parse(
		rawSections=(self.__templateScriptSection))

		if not self.__templateRemoteConnectionSection in templateSectionsFileParser.sections:
			self.Remote_Connection_groupBox.hide()
			return

		LOGGER.debug("> {0}' section found.".format(self.__templateRemoteConnectionSection))
		self.Remote_Connection_groupBox.show()
		connectionType = foundations.parsers.getAttributeCompound("ConnectionType",
		templateSectionsFileParser.getValue("ConnectionType", self.__templateRemoteConnectionSection))
		if connectionType.value == "Socket":
			LOGGER.debug("> Remote connection type: 'Socket'.")
			self.Software_Port_spinBox.setValue(int(foundations.parsers.getAttributeCompound("DefaultPort",
			templateSectionsFileParser.getValue("DefaultPort",
												self.__templateRemoteConnectionSection)).value))
			self.Address_lineEdit.setText(QString(foundations.parsers.getAttributeCompound("DefaultAddress",
			templateSectionsFileParser.getValue("DefaultAddress",
												self.__templateRemoteConnectionSection)).value))
			self.Remote_Connection_Options_frame.show()
		elif connectionType.value == "Win32":
			LOGGER.debug("> Remote connection: 'Win32'.")
			self.Remote_Connection_Options_frame.hide()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler,
											False,
											foundations.exceptions.FileExistsError,
											Exception)
	def outputLoaderScriptUi(self):
		"""
		This method outputs the Loader Script.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		LOGGER.debug("> Initializing Loader Script output.")

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		if selectedTemplates and len(selectedTemplates) != 1:
			self.__engine.notificationsManager.warnify(
			"{0} | Multiple selected Templates, '{1}' will be used!".format(self.__class__.__name__, selectedTemplates[0].name))

		template = selectedTemplates and selectedTemplates[0] or None

		if not template:
			raise foundations.exceptions.UserError(
			"{0} | In order to output the Loader Script, you need to select a Template!".format(self.__class__.__name__))

		if not foundations.common.pathExists(template.path):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' Template file doesn't exists!".format(
			self.__class__.__name__, template.name))

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
		if selectedIblSets and len(selectedIblSets) != 1:
			self.__engine.notificationsManager.warnify(
			"{0} | Multiple selected Ibl Sets, '{1}' will be used!".format(self.__class__.__name__, selectedIblSets[0].name))

		iblSet = selectedIblSets and selectedIblSets[0] or None
		if not iblSet:
			raise foundations.exceptions.UserError(
			"{0} | In order to output the Loader Script, you need to select an Ibl Set!".format(self.__class__.__name__))

		if not foundations.common.pathExists(iblSet.path):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' Ibl Set file doesn't exists!".format(
			self.__class__.__name__, iblSet.title))

		if self.outputLoaderScript(template, iblSet):
			self.__engine.notificationsManager.notify(
			"{0} | '{1}' output done!".format(self.__class__.__name__, template.outputScript))
			return True
		else:
			raise Exception("{0} | Exception raised: '{1}' output failed!".format(self.__class__.__name__,
			template.outputScript))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def sendLoaderScriptToSoftwareUi(self):
		"""
		This method sends the Loader Script to associated 3d package.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		if not self.outputLoaderScriptUi():
			return

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None
		if not template:
			return

		loaderScriptPath = strings.getNormalizedPath(os.path.join(self.__ioDirectory, template.outputScript))
		if self.Convert_To_Posix_Paths_checkBox.isChecked():
			loaderScriptPath = strings.toPosixPath(loaderScriptPath)
		if not self.sendLoaderScriptToSoftware(template, loaderScriptPath):
			raise Exception("{0} | Exception raised while sending Loader Script!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.DirectoryExistsError)
	def outputLoaderScript(self, template, iblSet):
		"""
		This method outputs the Loader Script.

		:param template: Template. ( DbTemplate )
		:param iblSet: Ibl Set. ( DbIblSet )
		:return: Loader Script file. ( String )
		"""

		self.__overrideKeys = self.getDefaultOverrideKeys()

		for component in self.__engine.componentsManager.listComponents():
			profile = self.__engine.componentsManager.components[component]
			interface = self.__engine.componentsManager.getInterface(component)
			if interface.activated and profile.name != self.name:
				hasattr(interface, "getOverrideKeys") and interface.getOverrideKeys()

		if self.__engine.parameters.loaderScriptsOutputDirectory:
			if foundations.common.pathExists(self.__engine.parameters.loaderScriptsOutputDirectory):
				loaderScript = File(os.path.join(self.__engine.parameters.loaderScriptsOutputDirectory, template.outputScript))
			else:
				raise foundations.exceptions.DirectoryExistsError(
				"{0} | '{1}' loader Script output directory doesn't exists!".format(
				self.__class__.__name__, self.__engine.parameters.loaderScriptsOutputDirectory))
		else:
			loaderScript = File(os.path.join(self.__ioDirectory, template.outputScript))

		LOGGER.debug("> Loader Script output file path: '{0}'.".format(loaderScript.file))

		loaderScript.content = self.getLoaderScript(template.path, iblSet.path, self.__overrideKeys)

		if loaderScript.content and loaderScript.write():
			return loaderScript.file

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler,
											False,
											sibl_gui.exceptions.SocketConnectionError)
	def sendLoaderScriptToSoftware(self, template, loaderScriptPath):
		"""
		This method sends the Loader Script to associated 3d package.

		:param template: Template. ( DbTemplate )
		:param loaderScriptPath: Loader Script path. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Starting remote connection!".format(self.__class__.__name__))
		templateSectionsFileParser = SectionsFileParser(template.path)
		templateSectionsFileParser.read() and templateSectionsFileParser.parse(
		rawSections=(self.__templateScriptSection))
		connectionType = foundations.parsers.getAttributeCompound("ConnectionType",
		templateSectionsFileParser.getValue("ConnectionType", self.__templateRemoteConnectionSection))

		if connectionType.value == "Socket":
			try:
				connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				connection.settimeout(2.5)
				connection.connect((str(self.Address_lineEdit.text()), int(self.Software_Port_spinBox.value())))
				socketCommand = foundations.parsers.getAttributeCompound("ExecutionCommand",
								templateSectionsFileParser.getValue("ExecutionCommand",
								self.__templateRemoteConnectionSection)).value.replace("$loaderScriptPath",
																						loaderScriptPath)
				LOGGER.debug("> Current socket command: '%s'.", socketCommand)
				connection.send(socketCommand)
				self.__engine.notificationsManager.notify(
				"{0} | Socket connection command dispatched!".format(self.__class__.__name__))
				dataBack = connection.recv(4096)
				LOGGER.debug("> Received from connection: '{0}'.".format(dataBack))
				connection.close()
				LOGGER.info("{0} | Closing remote connection!".format(self.__class__.__name__))
			except socket.timeout as error:
				LOGGER.info("{0} | Closing remote connection on timeout!".format(self.__class__.__name__))
			except Exception as error:
				raise sibl_gui.exceptions.SocketConnectionError(
				"{0} | Socket connection error: '{1}'!".format(self.__class__.__name__, error))
		elif connectionType.value == "Win32":
			if platform.system() == "Windows" or platform.system() == "Microsoft":
				try:
					import win32com.client
					connection = win32com.client.Dispatch(foundations.parsers.getAttributeCompound("TargetApplication",
								templateSectionsFileParser.getValue("TargetApplication",
																	self.__templateRemoteConnectionSection)).value)
					connection._FlagAsMethod(self.__win32ExecutionMethod)
					connectionCommand = foundations.parsers.getAttributeCompound("ExecutionCommand",
										templateSectionsFileParser.getValue("ExecutionCommand",
										self.__templateRemoteConnectionSection)).value.replace("$loaderScriptPath",
																								loaderScriptPath)
					LOGGER.debug("> Current connection command: '%s'.", connectionCommand)
					getattr(connection, self.__win32ExecutionMethod)(connectionCommand)
					self.__engine.notificationsManager.notify(
					"{0} | Win32 connection command dispatched!".format(self.__class__.__name__))
				except Exception as error:
					raise sibl_gui.exceptions.Win32OLEServerConnectionError(
					"{0} | Win32 OLE server connection error: '{1}'!".format(self.__class__.__name__, error))
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
			overrideKeys["Template|Path"] = foundations.parsers.getAttributeCompound("Template|Path", template.path)

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
		iblSet = selectedIblSets and selectedIblSets[0] or None
		if iblSet:
			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Ibl Set|Path", iblSet.path))
			overrideKeys["Ibl Set|Path"] = iblSet.path and foundations.parsers.getAttributeCompound("Ibl Set|Path",
															strings.getNormalizedPath(iblSet.path))

			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Background|BGfile",
																				iblSet.backgroundImage))
			overrideKeys["Background|BGfile"] = iblSet.backgroundImage and foundations.parsers.getAttributeCompound(
																			"Background|BGfile",
																			strings.getNormalizedPath(
																			iblSet.backgroundImage))

			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Enviroment|EVfile",
			 																	iblSet.lightingImage))
			overrideKeys["Enviroment|EVfile"] = iblSet.lightingImage and foundations.parsers.getAttributeCompound(
																		"Enviroment|EVfile",
																		strings.getNormalizedPath(
																		iblSet.lightingImage))

			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format("Reflection|REFfile",
			 															iblSet.reflectionImage))
			overrideKeys["Reflection|REFfile"] = iblSet.reflectionImage and foundations.parsers.getAttributeCompound(
																			"Reflection|REFfile",
																			strings.getNormalizedPath(
																			iblSet.reflectionImage))
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
		templateSectionsFileParser = SectionsFileParser(template)
		templateSectionsFileParser.read() and templateSectionsFileParser.parse(
											rawSections=(self.__templateScriptSection))
		templateSections = dict.copy(templateSectionsFileParser.sections)

		for attribute, value in dict.copy(templateSections[self.__templateIblSetAttributesSection]).iteritems():
			templateSections[self.__templateIblSetAttributesSection][namespace.removeNamespace(attribute,
																								rootOnly=True)] = value
			del templateSections[self.__templateIblSetAttributesSection][attribute]

		LOGGER.debug("> Binding Templates file attributes.")
		bindedAttributes = dict(((attribute, foundations.parsers.getAttributeCompound(attribute, value))
							for section in templateSections if section not in (self.__templateScriptSection)
							for attribute, value in templateSections[section].iteritems()))

		LOGGER.debug("> Parsing Ibl Set file: '{0}'.".format(iblSet))
		iblSetSectionsFileParser = SectionsFileParser(iblSet)
		iblSetSectionsFileParser.read() and iblSetSectionsFileParser.parse()
		iblSetSections = dict.copy(iblSetSectionsFileParser.sections)

		LOGGER.debug("> Flattening Ibl Set file attributes.")
		flattenedIblAttributes = dict(((attribute, foundations.parsers.getAttributeCompound(attribute, value))
		 						for section in iblSetSections
								for attribute, value in iblSetSections[section].iteritems()))

		for attribute in flattenedIblAttributes:
			if attribute in bindedAttributes:
				bindedAttributes[attribute].value = flattenedIblAttributes[attribute].value

		if "Lights|DynamicLights" in bindedAttributes:
			LOGGER.debug("> Building '{0}' custom attribute.".format("Lights|DynamicLights"))
			dynamicLights = []
			for section in iblSetSections:
				if re.search(r"Light\d+", section):
					dynamicLights.append(section)
					lightName = iblSetSectionsFileParser.getValue("LIGHTname", section)
					dynamicLights.append(lightName and lightName or self.__unnamedLightName)
					lightColorTokens = iblSetSectionsFileParser.getValue("LIGHTcolor", section).split(",")
					for color in lightColorTokens:
						dynamicLights.append(color)
					dynamicLights.append(iblSetSectionsFileParser.getValue("LIGHTmulti", section))
					dynamicLights.append(iblSetSectionsFileParser.getValue("LIGHTu", section))
					dynamicLights.append(iblSetSectionsFileParser.getValue("LIGHTv", section))

			LOGGER.debug("> Adding '{0}' custom attribute with value: '{1}'.".format("Lights|DynamicLights",
																					", ".join(dynamicLights)))
			bindedAttributes["Lights|DynamicLights"].value = self.__defaultStringSeparator.join(dynamicLights)

		LOGGER.debug("> Updating attributes with override keys.")
		for attribute in overrideKeys:
			if attribute in bindedAttributes:
				bindedAttributes[attribute].value = overrideKeys[attribute] and overrideKeys[attribute].value or None

		LOGGER.debug("> Updating Loader Script content.")
		loaderScript = templateSectionsFileParser.sections[
						self.__templateScriptSection][templateSectionsFileParser.rawSectionContentIdentifier]

		boundLoaderScript = []
		for line in loaderScript:
			bindingParameters = re.findall(r"{0}".format(self.__bindingIdentifierPattern), line)
			if bindingParameters:
				for parameter in bindingParameters:
					for attribute in bindedAttributes.itervalues():
						if parameter == attribute.link:
							LOGGER.debug(
							"> Updating Loader Script parameter '{0}' with value: '{1}'.".format(parameter,
																								attribute.value))
							line = line.replace(parameter, attribute.value and attribute.value or "-1")
			boundLoaderScript.append(line)
		return boundLoaderScript
