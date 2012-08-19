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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import re
from collections import OrderedDict
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QDoubleSpinBox
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPalette

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import foundations.parsers
import foundations.strings as strings
from foundations.parsers import SectionsFileParser
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.ui.widgets.variable_QPushButton import Variable_QPushButton

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "LoaderScriptOptions"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Loader_Script_Options.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LoaderScriptOptions(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class isthe :mod:`sibl_gui.components.addons.loaderScriptOptions.loaderScriptOptions` Component Interface class.
	| It provides override keys on request for the :mod:`sibl_gui.components.addons.loaderScript.loaderScript` Component.
	| It exposes Templates files **Common Attributes** and **Additional Attributes** sections so that
		the user can configure the behavior of the Loader Script.
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

		super(LoaderScriptOptions, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__dockArea = 2

		self.__engine = None

		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

		self.__namespaceSplitter = "|"

		self.__templatesSettingsDirectory = "templates/"
		self.__templateSettingsFile = None
		self.__templateCommonAttributesSection = "Common Attributes"
		self.__templateAdditionalAttributesSection = "Additional Attributes"
		self.__templateScriptSection = "Script"
		self.__optionsToolboxesHeaders = ["Value"]

		self.__uiLightGrayColor = QColor(240, 240, 240)
		self.__uiDarkGrayColor = QColor(160, 160, 160)

		self.__tableWidgetRowHeight = 30
		self.__tableWidgetHeaderHeight = 26

		self.__enumSplitter = ";"

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
	def coreTemplatesOutliner(self):
		"""
		This method is the property for **self.__coreTemplatesOutliner** attribute.

		:return: self.__coreTemplatesOutliner. ( QWidget )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This method is the setter method for **self.__coreTemplatesOutliner** attribute.

		:param value: Attribute value. ( QWidget )
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
	def addonsLoaderScript(self):
		"""
		This method is the property for **self.__addonsLoaderScript** attribute.

		:return: self.__addonsLoaderScript. ( QWidget )
		"""

		return self.__addonsLoaderScript

	@addonsLoaderScript.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self, value):
		"""
		This method is the setter method for **self.__addonsLoaderScript** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "addonsLoaderScript"))

	@addonsLoaderScript.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self):
		"""
		This method is the deleter method for **self.__addonsLoaderScript** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "addonsLoaderScript"))

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

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"namespaceSplitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format(
			"namespaceSplitter", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
			"namespaceSplitter", value)
		self.__namespaceSplitter = value

	@namespaceSplitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def namespaceSplitter(self):
		"""
		This method is the deleter method for **self.__namespaceSplitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "namespaceSplitter"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesSettingsDirectory"))

	@templatesSettingsDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesSettingsDirectory(self):
		"""
		This method is the deleter method for **self.__templatesSettingsDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesSettingsDirectory"))

	@property
	def templateSettingsFile(self):
		"""
		This method is the property for **self.__templateSettingsFile** attribute.

		:return: self.__templateSettingsFile. ( String )
		"""

		return self.__templateSettingsFile

	@templateSettingsFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateSettingsFile(self, value):
		"""
		This method is the setter method for **self.__templateSettingsFile** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templateSettingsFile"))

	@templateSettingsFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateSettingsFile(self):
		"""
		This method is the deleter method for **self.__templateSettingsFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templateSettingsFile"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templateCommonAttributesSection"))

	@templateCommonAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateCommonAttributesSection(self):
		"""
		This method is the deleter method for **self.__templateCommonAttributesSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templateCommonAttributesSection"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templateAdditionalAttributesSection"))

	@templateAdditionalAttributesSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templateAdditionalAttributesSection(self):
		"""
		This method is the deleter method for **self.__templateAdditionalAttributesSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(
		self.__class__.__name__, "templateAdditionalAttributesSection"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "optionsToolboxesHeaders"))

	@optionsToolboxesHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def optionsToolboxesHeaders(self):
		"""
		This method is the deleter method for **self.__optionsToolboxesHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "optionsToolboxesHeaders"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLightGrayColor"))

	@uiLightGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLightGrayColor(self):
		"""
		This method is the deleter method for **self.__uiLightGrayColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiLightGrayColor"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiDarkGrayColor"))

	@uiDarkGrayColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDarkGrayColor(self):
		"""
		This method is the deleter method for **self.__uiDarkGrayColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiDarkGrayColor"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tableWidgetRowHeight"))

	@tableWidgetRowHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetRowHeight(self):
		"""
		This method is the deleter method for **self.__tableWidgetRowHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tableWidgetRowHeight"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tableWidgetHeaderHeight"))

	@tableWidgetHeaderHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tableWidgetHeaderHeight(self):
		"""
		This method is the deleter method for **self.__tableWidgetHeaderHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tableWidgetHeaderHeight"))

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

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"enumSplitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("enumSplitter", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
			"enumSplitter", value)
		self.__enumSplitter = value

	@enumSplitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def enumSplitter(self):
		"""
		This method is the deleter method for **self.__enumSplitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "enumSplitter"))

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

		self.__coreTemplatesOutliner = self.__engine.componentsManager.components["core.templatesOutliner"].interface
		self.__addonsLoaderScript = self.__engine.componentsManager.components["addons.loaderScript"].interface

		self.__templatesSettingsDirectory = os.path.join(self.__engine.userApplicationDataDirectory,
														Constants.settingsDirectory,
														self.__templatesSettingsDirectory)
		not foundations.common.pathExists(self.__templatesSettingsDirectory) and \
		os.makedirs(self.__templatesSettingsDirectory)
		self.__templateSettingsFile = None

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

		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

		self.__templatesSettingsDirectory = os.path.basename(os.path.abspath(self.__templatesSettingsDirectory))
		self.__templateSettingsFile = None

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

		self.__commonAndAdditionalAttributesTablesWidgets_setUi()

		# Signals / Slots.
		self.__coreTemplatesOutliner.view.selectionModel().selectionChanged.connect(
		self.__coreTemplatesOutliner_view_selectionModel__selectionChanged)

		self.initializedUi = True
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
		self.__coreTemplatesOutliner.view.selectionModel().selectionChanged.disconnect(
		self.__coreTemplatesOutliner_view_selectionModel__selectionChanged)

		self.initializedUi = False
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
	def __tableWidget_setUi(self, section, tableWidget, overrides):
		"""
		This method defines and sets the given table widget.

		:param section: Section attributes. ( Dictionary )
		:param tableWidget: Table Widget. ( QTableWidget )
		:param overrides: Attributes overrides. ( Dictionary )
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
		for row, attribute in enumerate(section):
			LOGGER.debug("> Current attribute: '{0}'.".format(attribute))

			overridesValue = attribute in overrides and overrides[attribute] or None
			LOGGER.debug("> Settings value: '{0}'.".format(overridesValue or Constants.nullObject))

			attributeCompound = foundations.parsers.getAttributeCompound(attribute, section[attribute])
			if attributeCompound.name:
				verticalHeaderLabels.append(attributeCompound.alias)
			else:
				verticalHeaderLabels.append(strings.getNiceName(attributeCompound.name))
			LOGGER.debug("> Attribute type: '{0}'.".format(attributeCompound.type))
			if attributeCompound.type == "Boolean":
				state = int(overridesValue or attributeCompound.value) and True or False
				item = Variable_QPushButton(self,
						state,
						(self.__uiLightGrayColor, self.__uiDarkGrayColor),
						("True", "False"))
				item.setChecked(state)

				# Signals / Slots.
				item.clicked.connect(self.__tableWidget__valueChanged)
			elif attributeCompound.type == "Float":
				item = QDoubleSpinBox()
				item.setMinimum(0)
				item.setMaximum(65535)
				item.setValue(float(overridesValue or attributeCompound.value))

				# Signals / Slots.
				item.valueChanged.connect(self.__tableWidget__valueChanged)
			elif attributeCompound.type == "Enum":
				item = QComboBox()
				comboBoxItems = [enumItem.strip() for enumItem in attributeCompound.value.split(self.__enumSplitter)]
				item.addItems(comboBoxItems)
				if overridesValue in comboBoxItems:
					item.setCurrentIndex(comboBoxItems.index(overridesValue))

				# Signals / Slots.
				item.currentIndexChanged.connect(self.__tableWidget__valueChanged)
			elif attributeCompound.type == "String":
				item = QLineEdit(QString(overridesValue or attributeCompound.value))

				# Signals / Slots.
				item.editingFinished.connect(self.__tableWidget__valueChanged)

			item.data = attributeCompound
			tableWidget.setCellWidget(row, 0, item)

		tableWidget.setVerticalHeaderLabels(verticalHeaderLabels)
		tableWidget.show()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __commonAndAdditionalAttributesTablesWidgets_setUi(self):
		"""
		This method sets the **Common_Attributes_tableWidget** and  **Additional_Attributes_tableWidget** widgets.
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		template = foundations.common.getFirstItem(selectedTemplates)
		if not (template and foundations.common.pathExists(template.path)):
			return

		LOGGER.debug("> Attempting to read '{0}' Template settings file.".format(template.name))
		commonAttributesOverrides = {}
		additionalAttributesOverrides = {}
		templateSettingsDirectory = os.path.join(self.__templatesSettingsDirectory, template.software, template.name)
		currentTemplateSettingsDirectory = os.path.join(templateSettingsDirectory, template.release)
		self.__templateSettingsFile = os.path.join(templateSettingsDirectory,
										template.release,
										os.path.basename(template.path))

		not foundations.common.pathExists(currentTemplateSettingsDirectory) and \
		io.setDirectory(currentTemplateSettingsDirectory)

		templateSettingsFile = None
		if foundations.common.pathExists(self.__templateSettingsFile):
			templateSettingsFile = self.__templateSettingsFile
		else:
			for version in sorted((
							path for path in os.listdir(templateSettingsDirectory)
							if re.search(r"\d\.\d\.\d", path)), reverse=True, key=lambda x:(strings.getVersionRank(x))):
				path = os.path.join(templateSettingsDirectory, version, os.path.basename(template.path))
				if foundations.common.pathExists(path):
					templateSettingsFile = path
					break

		if templateSettingsFile:
			LOGGER.debug("> Accessing '{0}' Template settings file: '{1}'.".format(template.name, templateSettingsFile))
			templateSettingsSectionsFileParser = SectionsFileParser(templateSettingsFile)
			templateSettingsSectionsFileParser.read() and templateSettingsSectionsFileParser.parse()
			commonAttributesOverrides.update(
			templateSettingsSectionsFileParser.sections[self.__templateCommonAttributesSection])
			additionalAttributesOverrides.update(
			templateSettingsSectionsFileParser.sections[self.__templateAdditionalAttributesSection])
		else:
			LOGGER.debug("> No Template settings file found for : '{0}'.".format(template.name))

		LOGGER.debug("> Parsing '{0}' Template for '{1}' and '{2}' section.".format(
		template.name, self.__templateCommonAttributesSection, self.__templateAdditionalAttributesSection))
		templateSectionsFileParser = SectionsFileParser(template.path)
		templateSectionsFileParser.read() and templateSectionsFileParser.parse(
		rawSections=(self.__templateScriptSection))

		self.__tableWidget_setUi(templateSectionsFileParser.sections[self.__templateCommonAttributesSection],
								self.Common_Attributes_tableWidget, commonAttributesOverrides)
		self.__tableWidget_setUi(templateSectionsFileParser.sections[self.__templateAdditionalAttributesSection],
								self.Additional_Attributes_tableWidget, additionalAttributesOverrides)

	@core.executionTrace
	def __coreTemplatesOutliner_view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when **coreTemplatesOutliner.view** Model selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		self.__commonAndAdditionalAttributesTablesWidgets_setUi()

	@core.executionTrace
	def __tableWidget__valueChanged(self, *args):
		"""
		This method is triggered when a **Common_Attributes_tableWidget** or 
		**Additional_Attributes_tableWidget** Widget value has changed.

		:param \*args: Arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}' Template settings file content.".format(self.__templateSettingsFile))
		templateSettingsSectionsFileParser = SectionsFileParser(self.__templateSettingsFile)
		templateSettingsSectionsFileParser.sections = OrderedDict()
		for section, tableWidget in OrderedDict([(self.__templateCommonAttributesSection,
												self.Common_Attributes_tableWidget),
												(self.__templateAdditionalAttributesSection,
												self.Additional_Attributes_tableWidget)]).iteritems():
			templateSettingsSectionsFileParser.sections[section] = OrderedDict()
			for row in range(tableWidget.rowCount()):
				widget = tableWidget.cellWidget(row, 0)
				if type(widget) is Variable_QPushButton:
					value = widget.text() == "True" and "1" or "0"
				elif type(widget) is QDoubleSpinBox:
					value = strings.encode(widget.value())
				elif type(widget) is QComboBox:
					value = strings.encode(widget.currentText())
				else:
					value = strings.encode(widget.text())
				templateSettingsSectionsFileParser.sections[
				section][foundations.namespace.removeNamespace(widget.data.name)] = value
		templateSettingsSectionsFileParser.write()

	@core.executionTrace
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
				value = strings.encode(widget.value())
			elif type(widget) is QComboBox:
				value = strings.encode(widget.currentText())
			else:
				value = strings.encode(widget.text())
			widget.data.value = value

			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format(widget.data.name, widget.data.value))
			self.__addonsLoaderScript.overrideKeys[widget.data.name] = widget.data
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
		success *= self.__updateOverrideKeys(self.Common_Attributes_tableWidget) or False
		success *= self.__updateOverrideKeys(self.Additional_Attributes_tableWidget) or False

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while retrieving override keys!".format(self.__class__.__name__))
