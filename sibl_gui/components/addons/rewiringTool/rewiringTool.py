#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**rewiringTool.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`RewiringTool` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFileDialog

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.parsers
import foundations.strings
import foundations.verbose
import umbra.ui.common
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "RewiringTool"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Rewiring_Tool.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RewiringTool(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.addons.rewiringTool.rewiringTool` Component Interface class.
	| It provides override keys on request for the :mod:`sibl_gui.components.addons.loaderScript.loaderScript` Component.
	"""

	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param name: Component name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(RewiringTool, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__dockArea = 2

		self.__engine = None

		self.__iblSetsOutliner = None

		self.__reWireFramesWidgets = None
		self.__reWireComboBoxesWidgets = None
		self.__reWireLineEditWidgets = None

		self.__loaderScript = None

		self.__rewiringParameters = (("Background", "Background|BGfile", "backgroundImage"),
									("Lighting", "Enviroment|EVfile", "lightingImage"),
									("Reflection", "Reflection|REFfile", "reflectionImage"),
									("Custom image", None, None))

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def dockArea(self):
		"""
		Property for **self.__dockArea** attribute.

		:return: self.__dockArea.
		:rtype: int
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		Setter for **self.__dockArea** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		Deleter for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def iblSetsOutliner(self):
		"""
		Property for **self.__iblSetsOutliner** attribute.

		:return: self.__iblSetsOutliner.
		:rtype: QWidget
		"""

		return self.__iblSetsOutliner

	@iblSetsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self, value):
		"""
		Setter for **self.__iblSetsOutliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsOutliner"))

	@iblSetsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self):
		"""
		Deleter for **self.__iblSetsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsOutliner"))

	@property
	def reWireFramesWidgets(self):
		"""
		Property for **self.__reWireFramesWidgets** attribute.

		:return: self.__reWireFramesWidgets.
		:rtype: tuple
		"""

		return self.__reWireFramesWidgets

	@reWireFramesWidgets.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def reWireFramesWidgets(self, value):
		"""
		Setter for **self.__reWireFramesWidgets** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "reWireFramesWidgets"))

	@reWireFramesWidgets.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def reWireFramesWidgets(self):
		"""
		Deleter for **self.__reWireFramesWidgets** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "reWireFramesWidgets"))

	@property
	def reWireComboBoxesWidgets(self):
		"""
		Property for **self.__reWireComboBoxesWidgets** attribute.

		:return: self.__reWireComboBoxesWidgets.
		:rtype: tuple
		"""

		return self.__reWireComboBoxesWidgets

	@reWireComboBoxesWidgets.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def reWireComboBoxesWidgets(self, value):
		"""
		Setter for **self.__reWireComboBoxesWidgets** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "reWireComboBoxesWidgets"))

	@reWireComboBoxesWidgets.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def reWireComboBoxesWidgets(self):
		"""
		Deleter for **self.__reWireComboBoxesWidgets** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "reWireComboBoxesWidgets"))

	@property
	def reWireLineEditWidgets(self):
		"""
		Property for **self.__reWireLineEditWidgets** attribute.

		:return: self.__reWireLineEditWidgets.
		:rtype: tuple
		"""

		return self.__reWireLineEditWidgets

	@reWireLineEditWidgets.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def reWireLineEditWidgets(self, value):
		"""
		Setter for **self.__reWireLineEditWidgets** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "reWireLineEditWidgets"))

	@reWireLineEditWidgets.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def reWireLineEditWidgets(self):
		"""
		Deleter for **self.__reWireLineEditWidgets** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "reWireLineEditWidgets"))

	@property
	def rewiringParameters(self):
		"""
		Property for **self.__rewiringParameters** attribute.

		:return: self.__rewiringParameters.
		:rtype: tuple
		"""

		return self.__rewiringParameters

	@rewiringParameters.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def rewiringParameters(self, value):
		"""
		Setter for **self.__rewiringParameters** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "rewiringParameters"))

	@rewiringParameters.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def rewiringParameters(self):
		"""
		Deleter for **self.__rewiringParameters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rewiringParameters"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Engine to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine

		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]
		self.__loaderScript = self.__engine.componentsManager["addons.loaderScript"]

		self.activated = True
		return True

	def deactivate(self):
		"""
		Deactivates the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.__iblSetsOutliner = None
		self.__loaderScript = None

		self.activated = False
		return True

	def initializeUi(self):
		"""
		Initializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__reWireFramesWidgets = (self.Background_frame, self.Lighting_frame, self.Reflection_frame)
		self.__reWireComboBoxesWidgets = (self.Background_comboBox, self.Lighting_comboBox, self.Reflection_comboBox)
		self.__reWireLineEditWidgets = (self.Background_Path_lineEdit,
										self.Lighting_Path_lineEdit,
										self.Reflection_Path_lineEdit)

		for frame in self.__reWireFramesWidgets:
			LOGGER.debug("> Hiding '%s'.", frame)
			frame.hide()

		for index in range(len(self.__reWireComboBoxesWidgets)):
			self.__reWireComboBoxesWidgets[index].data = self.__rewiringParameters[index][1]
			self.__reWireComboBoxesWidgets[index].addItems([foundations.common.getFirstItem(parameter) \
														 for parameter in self.__rewiringParameters])
			self.__reWireComboBoxesWidgets[index].setCurrentIndex(index)

		# Signals / Slots.
		self.Background_comboBox.activated.connect(self.__setReWireWidgetFramesVisibility)
		self.Lighting_comboBox.activated.connect(self.__setReWireWidgetFramesVisibility)
		self.Reflection_comboBox.activated.connect(self.__setReWireWidgetFramesVisibility)
		self.Background_Path_toolButton.clicked.connect(self.__Background_Path_toolButton__clicked)
		self.Lighting_Path_toolButton.clicked.connect(self.__Lighting_Path_toolButton__clicked)
		self.Reflection_Path_toolButton.clicked.connect(self.__Reflection_Path_toolButton__clicked)

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		Uninitializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__reWireFramesWidgets = None
		self.__reWireComboBoxesWidgets = None
		self.__reWireLineEditWidgets = None

		# Signals / Slots.
		self.Background_comboBox.activated.disconnect(self.__setReWireWidgetFramesVisibility)
		self.Lighting_comboBox.activated.disconnect(self.__setReWireWidgetFramesVisibility)
		self.Reflection_comboBox.activated.disconnect(self.__setReWireWidgetFramesVisibility)
		self.Background_Path_toolButton.clicked.disconnect(self.__Background_Path_toolButton__clicked)
		self.Lighting_Path_toolButton.clicked.disconnect(self.__Lighting_Path_toolButton__clicked)
		self.Reflection_Path_toolButton.clicked.disconnect(self.__Reflection_Path_toolButton__clicked)

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	def __Background_Path_toolButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Background_ToolButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.__setReWireCustomPath("Background")

	def __Lighting_Path_toolButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Lighting_ToolButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.__setReWireCustomPath("Lighting")

	def __Reflection_Path_toolButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Reflection_ToolButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.__setReWireCustomPath("Reflection")

	def __setReWireWidgetFramesVisibility(self, index):
		"""
		Shows / hides rewire Widget frames.

		:param index: ComboBox index.
		:type index: tuple
		"""

		for index in range(len(self.__reWireComboBoxesWidgets)):
			if self.__reWireComboBoxesWidgets[index].currentText() == "Custom image":
				LOGGER.debug("> Showing rewire frame '{0}'.".format(self.__reWireFramesWidgets[index]))
				self.__reWireFramesWidgets[index].show()
			else:
				LOGGER.debug("> Hiding rewire frame '{0}'.".format(self.__reWireFramesWidgets[index]))
				self.__reWireFramesWidgets[index].hide()

	def __setReWireCustomPath(self, component):
		"""
		Sets the :mod:`sibl_gui.components.addons.rewiringTool.rewiringTool` Component
		custom image QLineEdit Widgets.

		:param component: Target Component.
		:type component: unicode
		"""

		customFile = umbra.ui.common.storeLastBrowsedPath(QFileDialog.getOpenFileName(self,
																					"Custom {0} File:".format(component),
																					RuntimeGlobals.lastBrowsedPath))
		LOGGER.debug("> Chosen custom '{0}': '{1}'.".format(component, customFile))
		if customFile != "":
			if component == "Background":
				self.Background_Path_lineEdit.setText(QString(customFile))
			elif component == "Lighting":
				self.Lighting_Path_lineEdit.setText(QString(customFile))
			elif component == "Reflection":
				self.Reflection_Path_lineEdit.setText(QString(customFile))

	def getOverrideKeys(self):
		"""
		Gets override keys.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.info("{0} | Updating Loader Script override keys!".format(self.__class__.__name__))

		selectedIblSet = self.__iblSetsOutliner.getSelectedIblSets()
		iblSet = foundations.common.getFirstItem(selectedIblSet)
		if not iblSet:
			return False

		for index, comboBox in enumerate(self.__reWireComboBoxesWidgets):
			parameter = self.__rewiringParameters[comboBox.currentIndex()]
			if comboBox.currentText() == "Custom image":
				LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format(
				comboBox.data, foundations.strings.toString(self.__reWireLineEditWidgets[index].text())))
				self.__loaderScript.overrideKeys[comboBox.data] = foundations.parsers.getAttributeCompound(
																		parameter[1],
																		foundations.strings.getNormalizedPath(
																		foundations.strings.toString(
																		self.__reWireLineEditWidgets[index].text())))
			else:
				LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format(comboBox.data,
																					getattr(iblSet, parameter[2])))
				self.__loaderScript.overrideKeys[comboBox.data] = getattr(iblSet, parameter[2]) and \
																foundations.parsers.getAttributeCompound(parameter[1],
																foundations.strings.getNormalizedPath(getattr(iblSet, parameter[2])))
		return True
