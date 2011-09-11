#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**loaderScriptOptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`LoaderScriptOptions` Component Interface class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import foundations.parsers
import foundations.strings as strings
from foundations.parsers import SectionsFileParser
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants
from umbra.ui.widgets.variable_QPushButton import Variable_QPushButton

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LoaderScriptOptions"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LoaderScriptOptions(UiComponent):
	"""
	| This class is the :mod:`umbra.components.addons.loaderScriptOptions.loaderScriptOptions` Component Interface class.
	| It provides override keys on request for the :mod:`umbra.components.addons.loaderScript.loaderScript` Component.
	| It exposes Templates files **Common Attributes** and **Additional Attributes** sections so that the user can configure the behavior of the Loader Script.
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

		self.__uiPath = "ui/Loader_Script_Options.ui"
		self.__dockArea = 2

		self.__container = None

		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

		self.__namespaceSplitter = "|"

		self.__templatesSettingsDirectory = "templates/"
		self.__currentTemplateSettingsFile = None
		self.__templateCommonAttributesSection = "Common Attributes"
		self.__templateAdditionalAttributesSection = "Additional Attributes"
		self.__templateScriptSection = "Script"
		self.__optionsToolboxesHeaders = ["Value"]

		self.__uiLightGrayColor = QColor(240, 240, 240)
		self.__uiDarkGrayColor = QColor(160, 160, 160)

		self.__tableWidgetRowHeight = 30
		self.__tableWidgetHeaderHeight = 26

		self.__enumSplitter = ";"

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
	def addonsLoaderScript(self):
		"""
		This method is the property for **self.__addonsLoaderScript** attribute.

		:return: self.__addonsLoaderScript. ( Object )
		"""

		return self.__addonsLoaderScript

	@addonsLoaderScript.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self, value):
		"""
		This method is the setter method for **self.__addonsLoaderScript** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("addonsLoaderScript"))

	@addonsLoaderScript.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self):
		"""
		This method is the deleter method for **self.__addonsLoaderScript** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("addonsLoaderScript"))

	@property
	def namespaceSplitter(self):
		"""
		This method is the property for **self.__namespaceSplitter** attribute.

		:return: self.__namespaceSplitter. ( String )
		"""

		return self.__namespaceSplitter

	@namespaceSplitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def namespaceSplitter(self, value):
		"""
		This method is the setter method for **self.__namespaceSplitter** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("namespaceSplitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("namespaceSplitter", value)
			assert not re.search("\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format("namespaceSplitter", value)
		self.__namespaceSplitter = value

	@namespaceSplitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def namespaceSplitter(self):
		"""
		This method is the deleter method for **self.__namespaceSplitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("namespaceSplitter"))

	@property
	def templatesSettingsDirectory(self):
		"""
		This method is the property for **self.__templatesSettingsDirectory** attribute.

		:return: self.__templatesSettingsDirectory. ( String )
		"""

		return self.__templatesSettingsDirectory

	@templatesSettingsDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesSettingsDirectory(self, value):
		"""
		This method is the setter method for **self.__templatesSettingsDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templatesSettingsDirectory"))

	@templatesSettingsDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesSettingsDirectory(self):
		"""
		This method is the deleter method for **self.__templatesSettingsDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templatesSettingsDirectory"))

	@property
	def currentTemplateSettingsFile(self):
		"""
		This method is the property for **self.__currentTemplateSettingsFile** attribute.

		:return: self.__currentTemplateSettingsFile. ( String )
		"""

		return self.__currentTemplateSettingsFile

	@currentTemplateSettingsFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentTemplateSettingsFile(self, value):
		"""
		This method is the setter method for **self.__currentTemplateSettingsFile** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("currentTemplateSettingsFile"))

	@currentTemplateSettingsFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentTemplateSettingsFile(self):
		"""
		This method is the deleter method for **self.__currentTemplateSettingsFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("currentTemplateSettingsFile"))

	@property
	def templateCommonAttributesSection(self):
		"""
		This method is the property for **self.__templateCommonAttributesSection** attribute.

		:return: self.__templateCommonAttributesSection. ( String )
		"""

		return self.__templateCommonAttributesSection

	@templateCommonAttributesSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateCommonAttributesSection(self, value):
		"""
		This method is the setter method for **self.__templateCommonAttributesSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templateCommonAttributesSection"))

	@templateCommonAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateCommonAttributesSection(self):
		"""
		This method is the deleter method for **self.__templateCommonAttributesSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templateCommonAttributesSection"))

	@property
	def templateAdditionalAttributesSection(self):
		"""
		This method is the property for **self.__templateAdditionalAttributesSection** attribute.

		:return: self.__templateAdditionalAttributesSection. ( String )
		"""

		return self.__templateAdditionalAttributesSection

	@templateAdditionalAttributesSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateAdditionalAttributesSection(self, value):
		"""
		This method is the setter method for **self.__templateAdditionalAttributesSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templateAdditionalAttributesSection"))

	@templateAdditionalAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateAdditionalAttributesSection(self):
		"""
		This method is the deleter method for **self.__templateAdditionalAttributesSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templateAdditionalAttributesSection"))

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
	def optionsToolboxesHeaders(self):
		"""
		This method is the property for **self.__optionsToolboxesHeaders** attribute.

		:return: self.__optionsToolboxesHeaders. ( List )
		"""

		return self.__optionsToolboxesHeaders

	@optionsToolboxesHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def optionsToolboxesHeaders(self, value):
		"""
		This method is the setter method for **self.__optionsToolboxesHeaders** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("optionsToolboxesHeaders"))

	@optionsToolboxesHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def optionsToolboxesHeaders(self):
		"""
		This method is the deleter method for **self.__optionsToolboxesHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("optionsToolboxesHeaders"))

	@property
	def uiLightGrayColor(self):
		"""
		This method is the property for **self.__uiLightGrayColor** attribute.

		:return: self.__uiLightGrayColor. ( QColor )
		"""

		return self.__uiLightGrayColor

	@uiLightGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self, value):
		"""
		This method is the setter method for **self.__uiLightGrayColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiLightGrayColor"))

	@uiLightGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self):
		"""
		This method is the deleter method for **self.__uiLightGrayColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiLightGrayColor"))

	@property
	def uiDarkGrayColor(self):
		"""
		This method is the property for **self.__uiDarkGrayColor** attribute.

		:return: self.__uiDarkGrayColor. ( QColor )
		"""

		return self.__uiDarkGrayColor

	@uiDarkGrayColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self, value):
		"""
		This method is the setter method for **self.__uiDarkGrayColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiDarkGrayColor"))

	@uiDarkGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self):
		"""
		This method is the deleter method for **self.__uiDarkGrayColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiDarkGrayColor"))

	@property
	def tableWidgetRowHeight(self):
		"""
		This method is the property for **self.__tableWidgetRowHeight** attribute.

		:return: self.__tableWidgetRowHeight. ( Integer )
		"""

		return self.__tableWidgetRowHeight

	@tableWidgetRowHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self, value):
		"""
		This method is the setter method for **self.__tableWidgetRowHeight** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("tableWidgetRowHeight"))

	@tableWidgetRowHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self):
		"""
		This method is the deleter method for **self.__tableWidgetRowHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("tableWidgetRowHeight"))

	@property
	def tableWidgetHeaderHeight(self):
		"""
		This method is the property for **self.__tableWidgetHeaderHeight** attribute.

		:return: self.__tableWidgetHeaderHeight. ( Integer )
		"""

		return self.__tableWidgetHeaderHeight

	@tableWidgetHeaderHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self, value):
		"""
		This method is the setter method for **self.__tableWidgetHeaderHeight** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("tableWidgetHeaderHeight"))

	@tableWidgetHeaderHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self):
		"""
		This method is the deleter method for **self.__tableWidgetHeaderHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("tableWidgetHeaderHeight"))

	@property
	def enumSplitter(self):
		"""
		This method is the property for **self.__enumSplitter** attribute.

		:return: self.__enumSplitter. ( String )
		"""

		return self.__enumSplitter

	@enumSplitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def enumSplitter(self, value):
		"""
		This method is the setter method for **self.__enumSplitter** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("enumSplitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("enumSplitter", value)
			assert not re.search("\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format("enumSplitter", value)
		self.__enumSplitter = value

	@enumSplitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def enumSplitter(self):
		"""
		This method is the deleter method for **self.__enumSplitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("enumSplitter"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container

		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface
		self.__addonsLoaderScript = self.__container.componentsManager.components["addons.loaderScript"].interface

		self.__templatesSettingsDirectory = os.path.join(self.__container.userApplicationDatasDirectory, Constants.settingsDirectory, self.__templatesSettingsDirectory)
		not os.path.exists(self.__templatesSettingsDirectory) and os.makedirs(self.__templatesSettingsDirectory)

		return UiComponent.activate(self)

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__container = None

		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

		self.__templatesSettingsDirectory = os.path.basename(os.path.abspath(self.__templatesSettingsDirectory))

		return UiComponent.deactivate(self)

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.connect(self.__coreTemplatesOutliner_Templates_Outliner_treeView_selectionModel__selectionChanged)

		return True

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.disconnect(self.__coreTemplatesOutliner_Templates_Outliner_treeView_selectionModel__selectionChanged)

		return True

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self.ui)
		self.ui.setParent(None)

		return True

	@core.executionTrace
	def __tableWidget_setUi(self, section, tableWidget, settings):
		"""
		This method defines and sets the provided table widget.

		:param section: Section attributes. ( Dictionary )
		:param tableWidget: Table Widget. ( QTableWidget )
		:param settings: Attributes settings. ( Dictionary )
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
			LOGGER.debug("> Current attribute: '{0}'.".format(attribute))

			settingsValue = attribute in settings.keys() and settings[attribute] or None
			LOGGER.debug("> Settings value: '{0}'.".format(settingsValue or Constants.nullObject))

			attributeCompound = foundations.parsers.getAttributeCompound(attribute, section[attribute])
			if attributeCompound.name:
				verticalHeaderLabels.append(attributeCompound.alias)
			else:
				verticalHeaderLabels.append(strings.getNiceName(attributeCompound.name))
			LOGGER.debug("> Attribute type: '{0}'.".format(attributeCompound.type))
			if attributeCompound.type == "Boolean":
				state = int(settingsValue or attributeCompound.value) and True or False
				item = Variable_QPushButton(state, (self.__uiLightGrayColor, self.__uiDarkGrayColor), ("True", "False"))
				item.setChecked(state)

				# Signals / Slots.
				item.clicked.connect(self.__tableWidget__valueChanged)
			elif attributeCompound.type == "Float":
				item = QDoubleSpinBox()
				item.setMinimum(0)
				item.setMaximum(65535)
				item.setValue(float(settingsValue or attributeCompound.value))

				# Signals / Slots.
				item.valueChanged.connect(self.__tableWidget__valueChanged)
			elif attributeCompound.type == "Enum":
				item = QComboBox()
				comboBoxItems = [enumItem.strip() for enumItem in attributeCompound.value.split(self.__enumSplitter)]
				item.addItems(comboBoxItems)
				if settingsValue in comboBoxItems:
					item.setCurrentIndex(comboBoxItems.index(settingsValue))

				# Signals / Slots.
				item.currentIndexChanged.connect(self.__tableWidget__valueChanged)
			elif attributeCompound.type == "String":
				item = QLineEdit(QString(settingsValue or attributeCompound.value))

				# Signals / Slots.
				item.editingFinished.connect(self.__tableWidget__valueChanged)

			item._datas = attributeCompound
			tableWidget.setCellWidget(row, 0, item)

		tableWidget.setVerticalHeaderLabels (verticalHeaderLabels)
		tableWidget.show()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __commonAndAdditionalAttributesTablesWidgets_setUi(self):
		"""
		This method sets the **Common_Attributes_tableWidget** and  **Additional_Attributes_tableWidget** widgets.
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		template = selectedTemplates and selectedTemplates[0] or None
		if not template:
			return
		if not os.path.exists(template.path):
			return

		LOGGER.debug("> Attempting to read Template settings file.")
		commonAttributesSettings = {}
		additionalAttributesSettings = {}
		templateSettingsDirectory = os.path.join(self.__templatesSettingsDirectory, template.software, template.name)
		currentTemplateSettingsDirectory = os.path.join(templateSettingsDirectory, template.release)
		if not os.path.exists(currentTemplateSettingsDirectory):
			io.setDirectory(currentTemplateSettingsDirectory)
		else:
			for version in sorted((path for path in os.listdir(templateSettingsDirectory) if re.search("\d\.\d\.\d", path)), reverse=True, key=lambda x:(strings.getVersionRank(x))):
				self.__currentTemplateSettingsFile = os.path.join(templateSettingsDirectory, version, os.path.basename(template.path))
				if not os.path.exists(self.__currentTemplateSettingsFile):
					continue

				LOGGER.debug("> Accessing Template settings file: '{0}'.".format(self.__currentTemplateSettingsFile))
				templateSettingsSectionsFileParser = SectionsFileParser(self.__currentTemplateSettingsFile)
				templateSettingsSectionsFileParser.read() and templateSettingsSectionsFileParser.parse()
				commonAttributesSettings.update(templateSettingsSectionsFileParser.sections[self.__templateCommonAttributesSection])
				additionalAttributesSettings.update(templateSettingsSectionsFileParser.sections[self.__templateAdditionalAttributesSection])
				break

		LOGGER.debug("> Parsing '{0}' Template for '{1}' and '{2}' section.".format(template.name, self.__templateCommonAttributesSection, self.__templateAdditionalAttributesSection))
		templateSectionsFileParser = SectionsFileParser(template.path)
		templateSectionsFileParser.read() and templateSectionsFileParser.parse(rawSections=(self.__templateScriptSection))

		self.__tableWidget_setUi(templateSectionsFileParser.sections[self.__templateCommonAttributesSection], self.ui.Common_Attributes_tableWidget, commonAttributesSettings)
		self.__tableWidget_setUi(templateSectionsFileParser.sections[self.__templateAdditionalAttributesSection], self.ui.Additional_Attributes_tableWidget, additionalAttributesSettings)

	@core.executionTrace
	def __coreTemplatesOutliner_Templates_Outliner_treeView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when **Common_Attributes_tableWidget** or **Additional_Attributes_tableWidget** selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		self.__commonAndAdditionalAttributesTablesWidgets_setUi()

	@core.executionTrace
	def __tableWidget__valueChanged(self, *args):
		"""
		This method is triggered when a **Common_Attributes_tableWidget** or **Additional_Attributes_tableWidget** widget value has changed.

		:param \*args: Arguments. ( \* )
		"""

		templateSettingsSectionsFileParser = SectionsFileParser(self.__currentTemplateSettingsFile)
		templateSettingsSectionsFileParser.read() and templateSettingsSectionsFileParser.parse()
		for section in templateSettingsSectionsFileParser.sections:
			print section

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __updateOverrideKeys(self, tableWidget):
		"""
		This method updates the Loader Script Component override keys.

		:param tableWidget: Table Widget. ( QTableWidget )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Updating override keys with '{0}' attributes.".format(tableWidget.objectName()))

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

			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format(widget._datas.name, widget._datas.value))
			self.__addonsLoaderScript.overrideKeys[widget._datas.name] = widget._datas
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getOverrideKeys(self):
		"""
		This method gets override keys.

		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Updating Loader Script override keys!".format(self.__class__.__name__))

		success = True
		success *= self.__updateOverrideKeys(self.ui.Common_Attributes_tableWidget) or False
		success *= self.__updateOverrideKeys(self.ui.Additional_Attributes_tableWidget) or False

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while retrieving override keys!".format(self.__class__.__name__))
