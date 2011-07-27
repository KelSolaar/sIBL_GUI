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
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**rewiringTool.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Rewiring tool addons Component Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.parser
import foundations.strings as strings
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class RewiringTool(UiComponent):
	"""
	This class is the RewiringTool class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		@param name: Component name. ( String )
		@param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
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
									("Custom image", None, None))

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for the _uiPath attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for the _uiPath attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for the _uiPath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def dockArea(self):
		"""
		This method is the property for the _dockArea attribute.

		@return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for the _dockArea attribute.

		@param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for the _dockArea attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		@param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for the _coreDatabaseBrowser attribute.

		@return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for the _coreDatabaseBrowser attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for the _coreDatabaseBrowser attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def reWireFramesWidgets(self):
		"""
		This method is the property for the _reWireFramesWidgets attribute.

		@return: self.__reWireFramesWidgets. ( Tuple )
		"""

		return self.__reWireFramesWidgets

	@reWireFramesWidgets.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireFramesWidgets(self, value):
		"""
		This method is the setter method for the _reWireFramesWidgets attribute.

		@param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("reWireFramesWidgets"))

	@reWireFramesWidgets.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireFramesWidgets(self):
		"""
		This method is the deleter method for the _reWireFramesWidgets attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("reWireFramesWidgets"))

	@property
	def reWireComboBoxesWidgets(self):
		"""
		This method is the property for the _reWireComboBoxesWidgets attribute.

		@return: self.__reWireComboBoxesWidgets. ( Tuple )
		"""

		return self.__reWireComboBoxesWidgets

	@reWireComboBoxesWidgets.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireComboBoxesWidgets(self, value):
		"""
		This method is the setter method for the _reWireComboBoxesWidgets attribute.

		@param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("reWireComboBoxesWidgets"))

	@reWireComboBoxesWidgets.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireComboBoxesWidgets(self):
		"""
		This method is the deleter method for the _reWireComboBoxesWidgets attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("reWireComboBoxesWidgets"))

	@property
	def reWireLineEditWidgets(self):
		"""
		This method is the property for the _reWireLineEditWidgets attribute.

		@return: self.__reWireLineEditWidgets. ( Tuple )
		"""

		return self.__reWireLineEditWidgets

	@reWireLineEditWidgets.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireLineEditWidgets(self, value):
		"""
		This method is the setter method for the _reWireLineEditWidgets attribute.

		@param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("reWireLineEditWidgets"))

	@reWireLineEditWidgets.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reWireLineEditWidgets(self):
		"""
		This method is the deleter method for the _reWireLineEditWidgets attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("reWireLineEditWidgets"))

	@property
	def rewiringParameters(self):
		"""
		This method is the property for the _rewiringParameters attribute.

		@return: self.__rewiringParameters. ( Tuple )
		"""

		return self.__rewiringParameters

	@rewiringParameters.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rewiringParameters(self, value):
		"""
		This method is the setter method for the _rewiringParameters attribute.

		@param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("rewiringParameters"))

	@rewiringParameters.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rewiringParameters(self):
		"""
		This method is the deleter method for the _rewiringParameters attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("rewiringParameters"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		@param container: Container to attach the Component to. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container

		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__addonsLoaderScript = self.__container.componentsManager.components["addons.loaderScript"].interface

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		LOGGER.debug("> Deactivating '{0}' component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__container = None

		self.__coreDatabaseBrowser = None
		self.__addonsLoaderScript = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' component ui.".format(self.__class__.__name__))

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

		# Signals / slots.
		self.ui.Background_comboBox.activated.connect(self.__setReWireWidgetFramesVisibility)
		self.ui.Lighting_comboBox.activated.connect(self.__setReWireWidgetFramesVisibility)
		self.ui.Reflection_comboBox.activated.connect(self.__setReWireWidgetFramesVisibility)
		self.ui.Background_Path_toolButton.clicked.connect(self.__Background_Path_toolButton__clicked)
		self.ui.Lighting_Path_toolButton.clicked.connect(self.__Lighting_Path_toolButton__clicked)
		self.ui.Reflection_Path_toolButton.clicked.connect(self.__Reflection_Path_toolButton__clicked)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' component ui.".format(self.__class__.__name__))

		self.__reWireFramesWidgets = None
		self.__reWireComboBoxesWidgets = None
		self.__reWireLineEditWidgets = None

		# Signals / slots.
		self.ui.Background_comboBox.activated.disconnect(self.__setReWireWidgetFramesVisibility)
		self.ui.Lighting_comboBox.activated.disconnect(self.__setReWireWidgetFramesVisibility)
		self.ui.Reflection_comboBox.activated.disconnect(self.__setReWireWidgetFramesVisibility)
		self.ui.Background_Path_toolButton.clicked.disconnect(self.__Background_Path_toolButton__clicked)
		self.ui.Lighting_Path_toolButton.clicked.disconnect(self.__Lighting_Path_toolButton__clicked)
		self.ui.Reflection_Path_toolButton.clicked.disconnect(self.__Reflection_Path_toolButton__clicked)

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		LOGGER.debug("> Removing '{0}' component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self.ui)
		self.ui.setParent(None)

	@core.executionTrace
	def __Background_Path_toolButton__clicked(self, checked):
		"""
		This method is called when Background_ToolButton is clicked.

		@param checked: Checked state. ( Boolean )
		"""

		self.__setReWireCustomPath("Background")

	@core.executionTrace
	def __Lighting_Path_toolButton__clicked(self, checked):
		"""
		This method is called when Lighting_ToolButton is clicked.

		@param checked: Checked state. ( Boolean )
		"""

		self.__setReWireCustomPath("Lighting")

	@core.executionTrace
	def __Reflection_Path_toolButton__clicked(self, checked):
		"""
		This method is called when Reflection_ToolButton is clicked.

		@param checked: Checked state. ( Boolean )
		"""

		self.__setReWireCustomPath("Reflection")

	@core.executionTrace
	def __setReWireWidgetFramesVisibility(self, index):
		"""
		This method shows / hides rewire Widget frames.

		@param index: ComboBox index. ( Tuple )
		"""

		for index in range(len(self.__reWireComboBoxesWidgets)):
			if self.__reWireComboBoxesWidgets[index].currentText() == "Custom image":
				LOGGER.debug("> Showing rewire frame '{0}'.".format(self.__reWireFramesWidgets[index]))
				self.__reWireFramesWidgets[index].show()
			else:
				LOGGER.debug("> Hiding rewire frame '{0}'.".format(self.__reWireFramesWidgets[index]))
				self.__reWireFramesWidgets[index].hide()

	@core.executionTrace
	def __setReWireCustomPath(self, component):
		"""
		This method sets the RewiringTool Component custom image QLineEdit Widgets.

		@param component: Target Component. ( String )
		"""

		customFile = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom " + component + " File:", self.__container.lastBrowsedPath))
		LOGGER.debug("> Chosen custom '{0}': '{1}'.".format(component, customFile))
		if customFile != "":
			if component == "Background":
				self.ui.Background_Path_lineEdit.setText(QString(customFile))
			elif component == "Lighting":
				self.ui.Lighting_Path_lineEdit.setText(QString(customFile))
			elif component == "Reflection":
				self.ui.Reflection_Path_lineEdit.setText(QString(customFile))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getOverrideKeys(self):
		"""
		This method gets override keys.

		@return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Updating Loader Script override keys!".format(self.__class__.__name__))

		selectedIblSet = self.__coreDatabaseBrowser.getSelectedIblSets()
		iblSet = selectedIblSet and selectedIblSet[0] or None
		if not iblSet:
			return

		for index, comboBox in enumerate(self.__reWireComboBoxesWidgets):
			parameter = self.__rewiringParameters[comboBox.currentIndex()]
			if comboBox.currentText() == "Custom image":
				LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format(comboBox._datas, str(self.__reWireLineEditWidgets[index].text())))
				self.__addonsLoaderScript.overrideKeys[comboBox._datas] = foundations.parser.getAttributeCompound(parameter[1], strings.getNormalizedPath(str(self.__reWireLineEditWidgets[index].text())))
			else:
				LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format(comboBox._datas, getattr(iblSet, parameter[2])))
				self.__addonsLoaderScript.overrideKeys[comboBox._datas] = getattr(iblSet, parameter[2]) and foundations.parser.getAttributeCompound(parameter[1], strings.getNormalizedPath(getattr(iblSet, parameter[2])))
		return True

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
