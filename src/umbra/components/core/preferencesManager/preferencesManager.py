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
**preferencesManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Preferences Manager Component Module.

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
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants
from umbra.globals.runtimeConstants import RuntimeConstants

#***********************************************************************************************
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class PreferencesManager(UiComponent):
	"""
	This Class Is The PreferencesManager Class.
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

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiPath = "ui/Preferences_Manager.ui"
		self.__dockArea = 2

		self.__container = None
		self.__settings = None

	#***********************************************************************************************
	#***	Attributes properties.
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
	def settings(self):
		"""
		This Method Is The Property For The _settings Attribute.

		@return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This Method Is The Deleter Method For The _settings Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settings"))

	#***********************************************************************************************
	#***	Class methods.
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

		self.__settings = self.__container.settings

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Cannot Be Deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__Logging_Formatters_comboBox_setUi()
		self.__Verbose_Level_comboBox_setUi()
		self.__Restore_Geometry_On_Layout_Change_checkBox_setUi()

		# Signals / slots.
		self.ui.Logging_Formatters_comboBox.activated.connect(self.__Logging_Formatters_comboBox__activated)
		self.ui.Verbose_Level_comboBox.activated.connect(self.__Verbose_Level_comboBox__activated)
		self.ui.Restore_Geometry_On_Layout_Change_checkBox.stateChanged.connect(self.__Restore_Geometry_On_Layout_Change_checkBox__stateChanged)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Ui Cannot Be Uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget Cannot Be Removed!".format(self.name))

	@core.executionTrace
	def __Logging_Formatters_comboBox_setUi(self):
		"""
		This Method Fills The Logging Formatter ComboBox.
		"""

		self.ui.Logging_Formatters_comboBox.clear()
		LOGGER.debug("> Available Logging Formatters: '{0}'.".format(", ".join(RuntimeConstants.loggingFormatters.keys())))
		self.ui.Logging_Formatters_comboBox.insertItems(0, QStringList (RuntimeConstants.loggingFormatters.keys()))
		loggingFormatter = self.__settings.getKey("Settings", "loggingFormatter").toString()
		self.__container.loggingActiveFormatter = loggingFormatter and loggingFormatter or Constants.loggingDefaultFormatter
		self.ui.Logging_Formatters_comboBox.setCurrentIndex(self.ui.Logging_Formatters_comboBox.findText(self.__container.loggingActiveFormatter, Qt.MatchExactly))

	@core.executionTrace
	def __Logging_Formatters_comboBox__activated(self, index):
		"""
		This Method Is Called When The Logging Formatter Is Triggered.

		@param index: ComboBox Activated Item Index. ( Integer )
		"""

		formatter = str(self.ui.Logging_Formatters_comboBox.currentText())
		LOGGER.debug("> Setting Logging Formatter: '{0}'.".format(formatter))
		RuntimeConstants.loggingActiveFormatter = formatter
		self.setLoggingFormatter()
		self.__settings.setKey("Settings", "loggingFormatter", self.ui.Logging_Formatters_comboBox.currentText())

	@core.executionTrace
	def __Verbose_Level_comboBox_setUi(self):
		"""
		This Method Fills The Verbose_Level_ComboBox.
		"""

		self.ui.Verbose_Level_comboBox.clear()
		LOGGER.debug("> Available Verbose Levels: '{0}'.".format(Constants.verbosityLabels))
		self.ui.Verbose_Level_comboBox.insertItems(0, QStringList (Constants.verbosityLabels))
		self.__container.verbosityLevel = self.__settings.getKey("Settings", "verbosityLevel").toInt()[0]
		self.ui.Verbose_Level_comboBox.setCurrentIndex(self.__container.verbosityLevel)

	@core.executionTrace
	def __Verbose_Level_comboBox__activated(self, index):
		"""
		This Method Is Called When The Verbose_Level_ComboBox Is Triggered.

		@param index: ComboBox Activated Item Index. ( Integer )
		"""

		LOGGER.debug("> Setting Verbose Level: '{0}'.".format(self.ui.Verbose_Level_comboBox.currentText()))
		self.__container.verbosityLevel = int(self.ui.Verbose_Level_comboBox.currentIndex())
		core.setVerbosityLevel(int(self.ui.Verbose_Level_comboBox.currentIndex()))
		self.__settings.setKey("Settings", "verbosityLevel", self.ui.Verbose_Level_comboBox.currentIndex())

	@core.executionTrace
	def __Restore_Geometry_On_Layout_Change_checkBox_setUi(self):
		"""
		This Method Sets The Restore_Geometry_On_Layout_Change_checkBox.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey("Settings", "restoreGeometryOnLayoutChange").isNull() and self.__settings.setKey("Settings", "restoreGeometryOnLayoutChange", Qt.Unchecked)

		restoreGeometryOnLayoutChange = self.__settings.getKey("Settings", "restoreGeometryOnLayoutChange")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("Restore_Geometry_On_Layout_Change_checkBox", restoreGeometryOnLayoutChange.toInt()[0]))
		self.ui.Restore_Geometry_On_Layout_Change_checkBox.setCheckState(restoreGeometryOnLayoutChange.toInt()[0])

	@core.executionTrace
	def __Restore_Geometry_On_Layout_Change_checkBox__stateChanged(self, state):
		"""
		This Method Is Called When Restore_Geometry_On_Layout_Change_checkBox State Changes.

		@param state: Checkbox State. ( Integer )
		"""

		LOGGER.debug("> Restore Geometry On Layout Change State: '{0}'.".format(self.ui.Restore_Geometry_On_Layout_Change_checkBox.checkState()))
		self.__settings.setKey("Settings", "restoreGeometryOnLayoutChange", self.ui.Restore_Geometry_On_Layout_Change_checkBox.checkState())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setLoggingFormatter(self):
		"""
		This Method Sets The Logging Formatter.
		"""

		for handler in (RuntimeConstants.loggingConsoleHandler, RuntimeConstants.loggingFileHandler, RuntimeConstants.loggingSessionHandler):
			handler and handler.setFormatter(RuntimeConstants.loggingFormatters[RuntimeConstants.loggingActiveFormatter])

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
