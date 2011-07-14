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
***	sIBL_GUI.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***      	sIBL_GUI Framework Module.
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
import functools
import logging
import os
import optparse
import platform
import sys
import time
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Path Manipulations
#***********************************************************************************************
def _setApplicationPackageDirectory():
	"""
	This Definition Sets The Application Datas Package Directory In sys.path.

	@return: Definition Success. ( Boolean )		
	"""

	applicationPackageDirectory = os.path.normpath(os.path.join(sys.path[0], "../"))
	applicationPackageDirectory not in sys.path and sys.path.append(applicationPackageDirectory)
	return True

_setApplicationPackageDirectory()

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import siblgui.ui.common
from foundations.streamObject import StreamObject
from manager.componentsManager import Manager
from siblgui.globals.constants import Constants
from siblgui.globals.runtimeConstants import RuntimeConstants
from siblgui.globals.uiConstants import UiConstants
from siblgui.ui.widgets.active_QLabel import Active_QLabel
from siblgui.ui.widgets.delayed_QSplashScreen import Delayed_QSplashScreen

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

# Starting The Console Handler.
if not hasattr(sys, "frozen") or not (platform.system() == "Windows" or platform.system() == "Microsoft"):
	RuntimeConstants.loggingConsoleHandler = logging.StreamHandler(sys.__stdout__)
	RuntimeConstants.loggingConsoleHandler.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
	LOGGER.addHandler(RuntimeConstants.loggingConsoleHandler)

# Defining Logging Formatters.
RuntimeConstants.loggingFormatters = {"Default" :core.LOGGING_DEFAULT_FORMATTER,
									"Extended" : core.LOGGING_EXTENDED_FORMATTER,
									"Standard" : core.LOGGING_STANDARD_FORMATTER}

RuntimeConstants.uiFile = os.path.join(os.getcwd(), UiConstants.frameworkUiFile)
if os.path.exists(RuntimeConstants.uiFile):
	Ui_Setup, Ui_Type = uic.loadUiType(RuntimeConstants.uiFile)
else:
	siblgui.ui.common.uiStandaloneSystemExitExceptionHandler(OSError("'{0}' Ui File Is Not Available, {1} Will Now Close!".format(UiConstants.frameworkUiFile, Constants.applicationName)), Constants.applicationName)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Preferences():
	"""
	This Class Is The Preferences Class.
	"""

	@core.executionTrace
	def __init__(self, preferencesFile=None):
		"""
		This Method Initializes The Class.

		@param preferencesFile: Current Preferences File Path. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.__preferencesFile = None
		self.__preferencesFile = preferencesFile

		self.__settings = QSettings(self.preferencesFile, QSettings.IniFormat)

		# --- Initializing Preferences. ---
		self.__getDefaultLayoutsSettings()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def preferencesFile(self):
		"""
		This Method Is The Property For The _preferencesFile Attribute.

		@return: self.__preferencesFile. ( String )
		"""

		return self.__preferencesFile

	@preferencesFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def preferencesFile(self, value):
		"""
		This Method Is The Setter Method For The _preferencesFile Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("preferencesFile", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' File Doesn't Exists!".format("preferencesFile", value)
		self.__preferencesFile = value

	@preferencesFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesFile(self):
		"""
		This Method Is The Deleter Method For The _preferencesFile Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("preferencesFile"))

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

	@property
	def defaultLayoutsSettings(self):
		"""
		This Method Is The Property For The _defaultLayoutsSettings Attribute.

		@return: self.__defaultLayoutsSettings. ( QSettings )
		"""

		return self.__defaultLayoutsSettings

	@defaultLayoutsSettings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLayoutsSettings(self, value):
		"""
		This Method Is The Setter Method For The _defaultLayoutsSettings Attribute.
		
		@param value: Attribute Value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("defaultLayoutsSettings"))

	@defaultLayoutsSettings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLayoutsSettings(self):
		"""
		This Method Is The Deleter Method For The _defaultLayoutsSettings Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("defaultLayoutsSettings"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def setKey(self, section, key, value):
		"""
		This Method Stores Provided Key In Settings File.
	
		@param section: Current Section To Save The Key Into. ( String )
		@param key: Current Key To Save. ( String )
		@param value: Current Key Value To Save. ( Object )
		"""

		LOGGER.debug("> Saving '{0}' In '{1}' Section With Value: '{2}' In Settings File.".format(key, section, value))

		self.__settings.beginGroup(section)
		self.__settings.setValue(key , QVariant(value))
		self.__settings.endGroup()

	@core.executionTrace
	def getKey(self, section, key):
		"""
		This Method Gets Key Value From Settings File.
	
		@param section: Current Section To Retrieve Key From. ( String )
		@param key: Current Key To Retrieve. ( String )
		@return: Current Key Value. ( Object )
		"""

		LOGGER.debug("> Retrieving '{0}' In '{1}' Section.".format(key, section))

		self.__settings.beginGroup(section)
		value = self.__settings.value(key)
		LOGGER.debug("> Key Value: '{0}'.".format(value))
		self.__settings.endGroup()

		return value

	@core.executionTrace
	def __getDefaultLayoutsSettings(self):
		"""
		This Method Gets The Default Layouts Settings.
		"""

		LOGGER.debug("> Accessing '{0}' Layouts Settings File!".format(UiConstants.frameworkLayoutsFile))
		self.__defaultLayoutsSettings = QSettings(os.path.join(os.getcwd(), UiConstants.frameworkLayoutsFile), QSettings.IniFormat)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setDefaultPreferences(self):
		"""
		This Method Defines The Default Settings File Content.
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing Default Settings!")

		self.__settings.beginGroup("Settings")
		self.__settings.setValue("verbosityLevel", QVariant("3"))
		self.__settings.setValue("restoreGeometryOnLayoutChange", Qt.Unchecked)
		self.__settings.setValue("deactivatedComponents", QVariant(""))
		self.__settings.endGroup()
		self.__settings.beginGroup("Layouts")
		self.__settings.setValue("startupCentric_geometry", self.__defaultLayoutsSettings.value("startupCentric/geometry"))
		self.__settings.setValue("startupCentric_windowState", self.__defaultLayoutsSettings.value("startupCentric/windowState"))
		self.__settings.setValue("startupCentric_centralWidget", self.__defaultLayoutsSettings.value("startupCentric/centralWidget"))
		self.__settings.setValue("startupCentric_activeLabel", self.__defaultLayoutsSettings.value("startupCentric/activeLabel"))
		self.__settings.setValue("setsCentric_geometry", self.__defaultLayoutsSettings.value("setsCentric/geometry"))
		self.__settings.setValue("setsCentric_windowState", self.__defaultLayoutsSettings.value("setsCentric/windowState"))
		self.__settings.setValue("setsCentric_centralWidget", self.__defaultLayoutsSettings.value("setsCentric/centralWidget"))
		self.__settings.setValue("setsCentric_activeLabel", self.__defaultLayoutsSettings.value("setsCentric/activeLabel"))
		self.__settings.setValue("inspectCentric_geometry", self.__defaultLayoutsSettings.value("inspectCentric/geometry"))
		self.__settings.setValue("inspectCentric_windowState", self.__defaultLayoutsSettings.value("inspectCentric/windowState"))
		self.__settings.setValue("inspectCentric_centralWidget", self.__defaultLayoutsSettings.value("inspectCentric/centralWidget"))
		self.__settings.setValue("inspectCentric_activeLabel", self.__defaultLayoutsSettings.value("inspectCentric/activeLabel"))
		self.__settings.setValue("templatesCentric_geometry", self.__defaultLayoutsSettings.value("templatesCentric/geometry"))
		self.__settings.setValue("templatesCentric_windowState", self.__defaultLayoutsSettings.value("templatesCentric/windowState"))
		self.__settings.setValue("templatesCentric_centralWidget", self.__defaultLayoutsSettings.value("templatesCentric/centralWidget"))
		self.__settings.setValue("templatesCentric_activeLabel", self.__defaultLayoutsSettings.value("templatesCentric/activeLabel"))
		self.__settings.setValue("preferencesCentric_geometry", self.__defaultLayoutsSettings.value("preferencesCentric/geometry"))
		self.__settings.setValue("preferencesCentric_windowState", self.__defaultLayoutsSettings.value("preferencesCentric/windowState"))
		self.__settings.setValue("preferencesCentric_centralWidget", self.__defaultLayoutsSettings.value("preferencesCentric/centralWidget"))
		self.__settings.setValue("preferencesCentric_activeLabel", self.__defaultLayoutsSettings.value("preferencesCentric/activeLabel"))
		self.__settings.setValue("one_geometry", "")
		self.__settings.setValue("one_windowState", "")
		self.__settings.setValue("one_centralWidget", True)
		self.__settings.setValue("one_activeLabel", "")
		self.__settings.setValue("two_geometry", "")
		self.__settings.setValue("two_windowState", "")
		self.__settings.setValue("two_centralWidget", True)
		self.__settings.setValue("two_activeLabel", "")
		self.__settings.setValue("three_geometry", "")
		self.__settings.setValue("three_windowState", "")
		self.__settings.setValue("three_centralWidget", True)
		self.__settings.setValue("three_activeLabel", "")
		self.__settings.setValue("four_geometry", "")
		self.__settings.setValue("four_windowState", "")
		self.__settings.setValue("four_centralWidget", True)
		self.__settings.setValue("four_activeLabel", "")
		self.__settings.setValue("five_geometry", "")
		self.__settings.setValue("five_windowState", "")
		self.__settings.setValue("five_centralWidget", True)
		self.__settings.setValue("five_activeLabel", "")
		self.__settings.endGroup()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setDefaultLayouts(self):
		"""
		This Method Sets The Default Layouts In The Preferences File.
		
		@return: Method Success. ( Boolean )		
		"""

		for layout in ("setsCentric", "inspectCentric", "templatesCentric", "preferencesCentric"):
				for type in ("geometry", "windowState", "centralWidget", "activeLabel"):
					LOGGER.debug("> Updating Preferences File '{0}_{1}' Layout Attribute!".format(layout, type))
					self.setKey("Layouts", "{0}_{1}".format(layout, type), self.__defaultLayoutsSettings.value("{0}/{1}".format(layout, type)))
		return True

class LayoutActiveLabel(core.Structure):
	"""
	This Is The LayoutActiveLabel Class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This Method Initializes The Class.

		@param kwargs: name, object_, layout, shortcut. ( Key / Value Pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting Class Attributes. ---
		self.__dict__.update(kwargs)

class sIBL_GUI(Ui_Type, Ui_Setup):
	"""
	This Class Is The Main Class For sIBL_GUI.
	"""

	#***************************************************************************************
	#***	Initialization.
	#***************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(siblgui.ui.common.uiSystemExitExceptionHandler, False, foundations.exceptions.ProgrammingError, Exception)
	def __init__(self):
		"""
		This Method Initializes The Class.
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		Ui_Type.__init__(self)
		Ui_Setup.__init__(self)

		self.setupUi(self)

		self.closeEvent = self.__closeUi

		# --- Setting Class Attributes. ---
		self.__timer = None
		self.__componentsManager = None
		self.__coreComponentsManagerUi = None
		self.__corePreferencesManager = None
		self.__coreDb = None
		self.__coreDatabaseBrowser = None
		self.__coreCollectionsOutliner = None
		self.__coreTemplatesOutliner = None
		self.__coreInspector = None
		self.__lastBrowsedPath = os.getcwd()
		self.__userApplicationDatasDirectory = RuntimeConstants.userApplicationDatasDirectory
		self.__loggingSessionHandler = RuntimeConstants.loggingSessionHandler
		self.__loggingFileHandler = RuntimeConstants.loggingFileHandler
		self.__loggingConsoleHandler = RuntimeConstants.loggingConsoleHandler
		self.__loggingSessionHandlerStream = RuntimeConstants.loggingSessionHandlerStream
		self.__loggingActiveFormatter = RuntimeConstants.loggingActiveFormatter
		self.__settings = RuntimeConstants.settings
		self.__verbosityLevel = RuntimeConstants.verbosityLevel
		self.__parameters = RuntimeConstants.parameters
		self.__libraryActiveLabel = None
		self.__inspectActiveLabel = None
		self.__exportActiveLabel = None
		self.__preferencesActiveLabel = None
		self.__layoutsActiveLabels = None
		self.__layoutMenu = None
		self.__miscMenu = None
		self.__workerThreads = []

		# --- Initializing Timer. ---
		self.__timer = QTimer(self)
		self.__timer.start(Constants.defaultTimerCycle)

		# --- Initializing Application. ---
		RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Initializing Interface.".format(self.__class__.__name__, Constants.releaseVersion), textColor=Qt.white, waitTime=0.25)

		# Visual Style Initialisation.
		self.__setVisualStyle()
		siblgui.ui.common.setWindowDefaultIcon(self)

		# Setting Window Title And Toolbar.
		self.setWindowTitle("{0} - {1}".format(Constants.applicationName, Constants.releaseVersion))
		self.__initializeToolbar()

		# --- Initializing Component Manager. ---
		RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Initializing Components Manager.".format(self.__class__.__name__, Constants.releaseVersion), textColor=Qt.white, waitTime=0.25)

		self.__componentsManager = Manager({ "Core" : os.path.join(os.getcwd(), Constants.coreComponentsDirectory), "Addons" : os.path.join(os.getcwd(), Constants.addonsComponentsDirectory), "User" : os.path.join(self.__userApplicationDatasDirectory, Constants.userComponentsDirectory) })
		self.__componentsManager.gatherComponents()

		if not self.__componentsManager.components:
			raise foundations.exceptions.ProgrammingError, "'{0}' Manager Has No Components, {1} Will Now Close!".format(self.__componentsManager, Constants.applicationName)

		self.__componentsManager.instantiateComponents(self.__componentsInstantiationCallback)

		# --- Activating Component Manager Ui. ---
		self.__coreComponentsManagerUi = self.__componentsManager.getInterface("core.componentsManagerUi")
		if self.__coreComponentsManagerUi:
			RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, "core.componentsManagerUi"), textColor=Qt.white)
			self.__coreComponentsManagerUi.activate(self)
			self.__coreComponentsManagerUi.addWidget()
			self.__coreComponentsManagerUi.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close!".format("core.componentsManagerUi", Constants.applicationName)

		# --- Activating Preferences Manager Component. ---
		self.__corePreferencesManager = self.__componentsManager.getInterface("core.preferencesManager")
		if self.__corePreferencesManager:
			RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, "core.preferencesManager"), textColor=Qt.white)
			self.__corePreferencesManager.activate(self)
			self.__corePreferencesManager.addWidget()
			self.__corePreferencesManager.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close!".format("core.preferencesManager", Constants.applicationName)

		# --- Activating Database Component. ---
		self.__coreDb = self.__componentsManager.getInterface("core.db")
		if self.__coreDb:
			RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, "core.db"), textColor=Qt.white)
			self.__coreDb.activate(self)
			self.__coreDb.initialize()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close!".format("core.db", Constants.applicationName)

		# --- Activating Collections Outliner Component. ---
		self.__coreCollectionsOutliner = self.__componentsManager.getInterface("core.collectionsOutliner")
		if self.__coreCollectionsOutliner:
			RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, "core.collectionsOutliner"), textColor=Qt.white)
			self.__coreCollectionsOutliner.activate(self)
			self.__coreCollectionsOutliner.addWidget()
			self.__coreCollectionsOutliner.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close!".format("core.collectionsOutliner", Constants.applicationName)

		# --- Activating Database Browser Component. ---
		self.__coreDatabaseBrowser = self.__componentsManager.getInterface("core.databaseBrowser")
		if self.__coreDatabaseBrowser:
			RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, "core.databaseBrowser"), textColor=Qt.white)
			self.__coreDatabaseBrowser.activate(self)
			self.__coreDatabaseBrowser.addWidget()
			self.__coreDatabaseBrowser.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close!".format("core.databaseBrowser", Constants.applicationName)

		# --- Activating Inspector Component. ---
		self.__coreInspector = self.__componentsManager.getInterface("core.inspector")
		if self.__coreInspector:
			RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, "core.inspector"), textColor=Qt.white)
			self.__coreInspector.activate(self)
			self.__coreInspector.addWidget()
			self.__coreInspector.initializeUi()

		# --- Activating Templates Outliner Component. ---
		self.__coreTemplatesOutliner = self.__componentsManager.getInterface("core.templatesOutliner")
		if self.__coreTemplatesOutliner:
			RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, "core.templatesOutliner"), textColor=Qt.white)
			self.__coreTemplatesOutliner.activate(self)
			self.__coreTemplatesOutliner.addWidget()
			self.__coreTemplatesOutliner.initializeUi()
		else:
			raise foundations.exceptions.ProgrammingError, "'{0}' Component Is Not Available, {1} Will Now Close!".format("core.templatesOutliner", Constants.applicationName)

		# --- Activating Others Components. ---
		deactivatedComponents = self.__settings.getKey("Settings", "deactivatedComponents").toString().split(",")
		for component in self.__componentsManager.getComponents():
			if component not in deactivatedComponents:
				profile = self.__componentsManager.components[component]
				interface = self.__componentsManager.getInterface(component)
				if not interface.activated:
					RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, component), textColor=Qt.white)
					interface.activate(self)
					if profile.categorie == "default":
						interface.initialize()
					elif profile.categorie == "ui":
						interface.addWidget()
						interface.initializeUi()

		# Hiding Splashscreen.
		LOGGER.debug("> Hiding SplashScreen.")
		if RuntimeConstants.splashscreen:
			RuntimeConstants.splashscreen.setMessage("{0} - {1} | Initialization Done.".format(self.__class__.__name__, Constants.releaseVersion), textColor=Qt.white)
			RuntimeConstants.splashscreen.hide()

		# --- Running onStartup Components Methods. ---
		for component in self.__componentsManager.getComponents():
			interface = self.__componentsManager.getInterface(component)
			if interface.activated:
				hasattr(interface, "onStartup") and interface.onStartup()

		self.__setLayoutsActiveLabelsShortcuts()

		self.restoreStartupLayout()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def timer(self):
		"""
		This Method Is The Property For The _timer Attribute.

		@return: self.__timer. ( QTimer )
		"""

		return self.__timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		This Method Is The Setter Method For The _timer Attribute.

		@param value: Attribute Value. ( QTimer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("timer"))

	@timer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		This Method Is The Deleter Method For The _timer Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("timer"))

	@property
	def componentsManager(self):
		"""
		This Method Is The Property For The _componentsManager Attribute.

		@return: self.__componentsManager. ( Object )
		"""

		return self.__componentsManager

	@componentsManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsManager(self, value):
		"""
		This Method Is The Setter Method For The _componentsManager Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("componentsManager"))

	@componentsManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsManager(self):
		"""
		This Method Is The Deleter Method For The _componentsManager Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("componentsManager"))

	@property
	def coreComponentsManagerUi(self):
		"""
		This Method Is The Property For The _coreComponentsManagerUi Attribute.

		@return: self.__coreComponentsManagerUi. ( Object )
		"""

		return self.__coreComponentsManagerUi

	@coreComponentsManagerUi.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreComponentsManagerUi(self, value):
		"""
		This Method Is The Setter Method For The _coreComponentsManagerUi Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreComponentsManagerUi"))

	@coreComponentsManagerUi.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreComponentsManagerUi(self):
		"""
		This Method Is The Deleter Method For The _coreComponentsManagerUi Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreComponentsManagerUi"))

	@property
	def corePreferencesManager(self):
		"""
		This Method Is The Property For The _corePreferencesManager Attribute.

		@return: self.__corePreferencesManager. ( Object )
		"""

		return self.__corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self, value):
		"""
		This Method Is The Setter Method For The _corePreferencesManager Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("corePreferencesManager"))

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self):
		"""
		This Method Is The Deleter Method For The _corePreferencesManager Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("corePreferencesManager"))

	@property
	def coreDb(self):
		"""
		This Method Is The Property For The _coreDb Attribute.

		@return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This Method Is The Deleter Method For The _coreDb Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDb"))

	@property
	def coreCollectionsOutliner(self):
		"""
		This Method Is The Property For The _coreCollectionsOutliner Attribute.

		@return: self.__coreCollectionsOutliner. ( Object )
		"""

		return self.__coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		"""
		This Method Is The Setter Method For The _coreCollectionsOutliner Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This Method Is The Deleter Method For The _coreCollectionsOutliner Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreCollectionsOutliner"))

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
	def lastBrowsedPath(self):
		"""
		This Method Is The Property For The _lastBrowsedPath Attribute.

		@return: self.__lastBrowsedPath. ( String )
		"""

		return self.__lastBrowsedPath

	@lastBrowsedPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def lastBrowsedPath(self, value):
		"""
		This Method Is The Setter Method For The _lastBrowsedPath Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("lastBrowsedPath", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' Directory Doesn't Exists!".format("lastBrowsedPath", value)
		self.__lastBrowsedPath = value

	@lastBrowsedPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lastBrowsedPath(self):
		"""
		This Method Is The Deleter Method For The _lastBrowsedPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("lastBrowsedPath"))

	@property
	def userApplicationDatasDirectory(self):
		"""
		This Method Is The Property For The _userApplicationDatasDirectory Attribute.

		@return: self.__userApplicationDatasDirectory. ( String )
		"""

		return self.__userApplicationDatasDirectory

	@userApplicationDatasDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userApplicationDatasDirectory(self, value):
		"""
		This Method Is The Setter Method For The _userApplicationDatasDirectory Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("userApplicationDatasDirectory"))

	@userApplicationDatasDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userApplicationDatasDirectory(self):
		"""
		This Method Is The Deleter Method For The _userApplicationDatasDirectory Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("userApplicationDatasDirectory"))

	@property
	def loggingSessionHandler(self):
		"""
		This Method Is The Property For The _loggingSessionHandler Attribute.

		@return: self.__loggingSessionHandler. ( Handler )
		"""

		return self.__loggingSessionHandler

	@loggingSessionHandler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandler(self, value):
		"""
		This Method Is The Setter Method For The _loggingSessionHandler Attribute.

		@param value: Attribute Value. ( Handler )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("loggingSessionHandler"))

	@loggingSessionHandler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandler(self):
		"""
		This Method Is The Deleter Method For The _loggingSessionHandler Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("loggingSessionHandler"))

	@property
	def loggingFileHandler(self):
		"""
		This Method Is The Property For The _loggingFileHandler Attribute.

		@return: self.__loggingFileHandler. ( Handler )
		"""

		return self.__loggingFileHandler

	@loggingFileHandler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingFileHandler(self, value):
		"""
		This Method Is The Setter Method For The _loggingFileHandler Attribute.

		@param value: Attribute Value. ( Handler )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("loggingFileHandler"))

	@loggingFileHandler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingFileHandler(self):
		"""
		This Method Is The Deleter Method For The _loggingFileHandler Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("loggingFileHandler"))

	@property
	def loggingConsoleHandler(self):
		"""
		This Method Is The Property For The _loggingConsoleHandler Attribute.

		@return: self.__loggingConsoleHandler. ( Handler )
		"""

		return self.__loggingConsoleHandler

	@loggingConsoleHandler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingConsoleHandler(self, value):
		"""
		This Method Is The Setter Method For The _loggingConsoleHandler Attribute.

		@param value: Attribute Value. ( Handler )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("loggingConsoleHandler"))

	@loggingConsoleHandler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingConsoleHandler(self):
		"""
		This Method Is The Deleter Method For The _loggingConsoleHandler Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("loggingConsoleHandler"))

	@property
	def loggingSessionHandlerStream(self):
		"""
		This Method Is The Property For The _loggingSessionHandlerStream Attribute.

		@return: self.__loggingSessionHandlerStream. ( StreamObject )
		"""

		return self.__loggingSessionHandlerStream

	@loggingSessionHandlerStream.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandlerStream(self, value):
		"""
		This Method Is The Setter Method For The _loggingSessionHandlerStream Attribute.

		@param value: Attribute Value. ( StreamObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("loggingSessionHandlerStream"))

	@loggingSessionHandlerStream.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandlerStream(self):
		"""
		This Method Is The Deleter Method For The _loggingSessionHandlerStream Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("loggingSessionHandlerStream"))

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

	@property
	def verbosityLevel(self):
		"""
		This Method Is The Property For The _verbosityLevel Attribute.

		@return: self.__verbosityLevel. ( Integer )
		"""

		return self.__verbosityLevel

	@verbosityLevel.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def verbosityLevel(self, value):
		"""
		This Method Is The Setter Method For The _verbosityLevel Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' Attribute: '{1}' Type Is Not 'int'!".format("verbosityLevel", value)
			assert value >= 0 and value <= 4, "'{0}' Attribute: Value Need To Be Exactly Beetween 0 and 4!".format("verbosityLevel")
		self.__verbosityLevel = value

	@verbosityLevel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def verbosityLevel(self):
		"""
		This Method Is The Deleter Method For The _verbosityLevel Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("verbosityLevel"))

	@property
	def parameters(self):
		"""
		This Method Is The Property For The _parameters Attribute.

		@return: self.__parameters. ( Object )
		"""

		return self.__parameters

	@parameters.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parameters(self, value):
		"""
		This Method Is The Setter Method For The _parameters Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("parameters"))

	@parameters.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parameters(self):
		"""
		This Method Is The Deleter Method For The _parameters Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("parameters"))

	@property
	def libraryActiveLabel (self):
		"""
		This Method Is The Property For The _libraryActiveLabel  Attribute.

		@return: self.__libraryActiveLabel . ( Active_QLabel )
		"""

		return self.__libraryActiveLabel

	@libraryActiveLabel .setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryActiveLabel (self, value):
		"""
		This Method Is The Setter Method For The _libraryActiveLabel  Attribute.

		@param value: Attribute Value. ( Active_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("libraryActiveLabel "))

	@libraryActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryActiveLabel (self):
		"""
		This Method Is The Deleter Method For The _libraryActiveLabel  Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("libraryActiveLabel "))

	@property
	def inspectActiveLabel (self):
		"""
		This Method Is The Property For The _inspectActiveLabel  Attribute.

		@return: self.__inspectActiveLabel . ( Active_QLabel )
		"""

		return self.__inspectActiveLabel

	@inspectActiveLabel .setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectActiveLabel (self, value):
		"""
		This Method Is The Setter Method For The _inspectActiveLabel  Attribute.

		@param value: Attribute Value. ( Active_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("inspectActiveLabel "))

	@inspectActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectActiveLabel (self):
		"""
		This Method Is The Deleter Method For The _inspectActiveLabel  Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("inspectActiveLabel "))

	@property
	def exportActiveLabel (self):
		"""
		This Method Is The Property For The _exportActiveLabel  Attribute.

		@return: self.__exportActiveLabel . ( Active_QLabel )
		"""

		return self.__exportActiveLabel

	@exportActiveLabel .setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def exportActiveLabel (self, value):
		"""
		This Method Is The Setter Method For The _exportActiveLabel  Attribute.

		@param value: Attribute Value. ( Active_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("exportActiveLabel "))

	@exportActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def exportActiveLabel (self):
		"""
		This Method Is The Deleter Method For The _exportActiveLabel  Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("exportActiveLabel "))

	@property
	def preferencesActiveLabel (self):
		"""
		This Method Is The Property For The _preferencesActiveLabel  Attribute.

		@return: self.__preferencesActiveLabel . ( Active_QLabel )
		"""

		return self.__preferencesActiveLabel

	@preferencesActiveLabel .setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesActiveLabel (self, value):
		"""
		This Method Is The Setter Method For The _preferencesActiveLabel  Attribute.

		@param value: Attribute Value. ( Active_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("preferencesActiveLabel "))

	@preferencesActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesActiveLabel (self):
		"""
		This Method Is The Deleter Method For The _preferencesActiveLabel  Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("preferencesActiveLabel "))

	@property
	def layoutsActiveLabels(self):
		"""
		This Method Is The Property For The _layoutsActiveLabels Attribute.

		@return: self.__layoutsActiveLabels. ( Tuple )
		"""

		return self.__layoutsActiveLabels

	@layoutsActiveLabels.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutsActiveLabels(self, value):
		"""
		This Method Is The Setter Method For The _layoutsActiveLabels Attribute.

		@param value: Attribute Value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("layoutsActiveLabels"))

	@layoutsActiveLabels.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutsActiveLabels(self):
		"""
		This Method Is The Deleter Method For The _layoutsActiveLabels Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("layoutsActiveLabels"))

	@property
	def layoutMenu(self):
		"""
		This Method Is The Property For The _layoutMenu Attribute.

		@return: self.__layoutMenu. ( QMenu )
		"""

		return self.__layoutMenu

	@layoutMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutMenu(self, value):
		"""
		This Method Is The Setter Method For The _layoutMenu Attribute.

		@param value: Attribute Value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("layoutMenu"))

	@layoutMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutMenu(self):
		"""
		This Method Is The Deleter Method For The _layoutMenu Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("layoutMenu"))

	@property
	def miscMenu(self):
		"""
		This Method Is The Property For The _miscMenu Attribute.

		@return: self.__miscMenu. ( QMenu )
		"""

		return self.__miscMenu

	@miscMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def miscMenu(self, value):
		"""
		This Method Is The Setter Method For The _miscMenu Attribute.

		@param value: Attribute Value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("miscMenu"))

	@miscMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def miscMenu(self):
		"""
		This Method Is The Deleter Method For The _miscMenu Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("miscMenu"))

	@property
	def workerThreads(self):
		"""
		This Method Is The Property For The _workerThreads Attribute.

		@return: self.__workerThreads. ( List )
		"""

		return self.__workerThreads

	@workerThreads.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def workerThreads(self, value):
		"""
		This Method Is The Setter Method For The _workerThreads Attribute.

		@param value: Attribute Value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("workerThreads"))

	@workerThreads.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def workerThreads(self):
		"""
		This Method Is The Deleter Method For The _workerThreads Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("workerThreads"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def __closeUi(self, event):
		"""
		This Method Is Called When Close Event Is Fired.

		@param event: QEvent. ( QEvent )
		"""

		# --- Running onClose Components Methods. ---
		for component in self.__componentsManager.getComponents():
			interface = self.__componentsManager.getInterface(component)
			if interface.activated:
				hasattr(interface, "onClose") and interface.onClose()

		# Storing Current Layout.
		self.storeStartupLayout()
		self.__settings.settings.sync()

		# Stopping Worker Threads.
		for workerThread in self.__workerThreads:
			if not workerThread.isFinished():
				LOGGER.debug("> Stopping Worker Thread: '{0}'.".format(workerThread))
				workerThread.exit()

		foundations.common.closeHandler(LOGGER, self.__loggingFileHandler)
		foundations.common.closeHandler(LOGGER, self.__loggingSessionHandler)
		# foundations.common.closeHandler( LOGGER, self.__loggingConsoleHandler )

		# Stopping The Timer.
		self.__timer.stop()
		self.__timer = None

		self.deleteLater()
		event.accept()

		_exit()

	@core.executionTrace
	def __componentsInstantiationCallback(self, profile):
		"""
		This Method Is A Callback For The Components Instantiation.
		
		@param profile: Component Profile. ( Profile )	
		"""

		RuntimeConstants.splashscreen and RuntimeConstants.splashscreen.setMessage("{0} - {1} | Instantiating {2} Component.".format(self.__class__.__name__, Constants.releaseVersion, profile.name), textColor=Qt.white)

	@core.executionTrace
	def __initializeToolbar(self):
		"""
		This Method Initializes sIBL_GUI Toolbar.
		"""

		LOGGER.debug("> Initializing Application Toolbar.")

		self.toolBar.setIconSize(QSize(UiConstants.frameworkDefaultToolbarIconSize, UiConstants.frameworkDefaultToolbarIconSize))

		LOGGER.debug("> Adding Application Logo.")
		logoLabel = QLabel()
		logoLabel.setObjectName("Application_Logo_label")
		logoLabel.setPixmap(QPixmap(UiConstants.frameworkLogoPicture))
		self.toolBar.addWidget(logoLabel)

		spacer = QLabel()
		spacer.setObjectName("Logo_Spacer_label")
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolBar.addWidget(spacer)

		toolbarFont = QFont()
		toolbarFont.setPointSize(16)

		LOGGER.debug("> Adding Active Labels.")

		self.__libraryActiveLabel = Active_QLabel(QPixmap(UiConstants.frameworkLibraryIcon), QPixmap(UiConstants.frameworkLibraryHoverIcon), QPixmap(UiConstants.frameworkLibraryActiveIcon), True)
		self.__libraryActiveLabel.setObjectName("Library_activeLabel")
		self.toolBar.addWidget(self.__libraryActiveLabel)

		self.__inspectActiveLabel = Active_QLabel(QPixmap(UiConstants.frameworkInspectIcon), QPixmap(UiConstants.frameworkInspectHoverIcon), QPixmap(UiConstants.frameworkInspectActiveIcon), True)
		self.__inspectActiveLabel.setObjectName("Inspect_activeLabel")
		self.toolBar.addWidget(self.__inspectActiveLabel)

		self.__exportActiveLabel = Active_QLabel(QPixmap(UiConstants.frameworkExportIcon), QPixmap(UiConstants.frameworkExportHoverIcon), QPixmap(UiConstants.frameworkExportActiveIcon), True)
		self.__exportActiveLabel.setObjectName("Export_activeLabel")
		self.toolBar.addWidget(self.__exportActiveLabel)

		self.__preferencesActiveLabel = Active_QLabel(QPixmap(UiConstants.frameworkPreferencesIcon), QPixmap(UiConstants.frameworkPreferencesHoverIcon), QPixmap(UiConstants.frameworkPreferencesActiveIcon), True)
		self.__preferencesActiveLabel.setObjectName("Preferences_activeLabel")
		self.toolBar.addWidget(self.__preferencesActiveLabel)

		self.__layoutsActiveLabels = (LayoutActiveLabel(name="Library", object_=self.__libraryActiveLabel, layout="setsCentric", shortcut=Qt.Key_7),
									LayoutActiveLabel(name="Inspect", object_=self.__inspectActiveLabel, layout="inspectCentric", shortcut=Qt.Key_8),
									LayoutActiveLabel(name="Export", object_=self.__exportActiveLabel, layout="templatesCentric", shortcut=Qt.Key_9),
									LayoutActiveLabel(name="Preferences", object_=self.__preferencesActiveLabel, layout="preferencesCentric", shortcut=Qt.Key_0))

		# Signals / Slots.
		for layoutActiveLabel in self.__layoutsActiveLabels:
			layoutActiveLabel.object_.clicked.connect(functools.partial(self.__activeLabel__clicked, layoutActiveLabel.layout))

		LOGGER.debug("> Adding Central Widget Button.")
		centralWidgetButton = Active_QLabel(QPixmap(UiConstants.frameworCentralWidgetIcon), QPixmap(UiConstants.frameworCentralWidgetHoverIcon), QPixmap(UiConstants.frameworCentralWidgetActiveIcon))
		centralWidgetButton.setObjectName("Central_Widget_activeLabel")
		self.toolBar.addWidget(centralWidgetButton)

		centralWidgetButton.clicked.connect(self.__centralWidgetButton__clicked)

		LOGGER.debug("> Adding Layout Button.")
		layoutsButton = Active_QLabel(QPixmap(UiConstants.frameworLayoutIcon), QPixmap(UiConstants.frameworLayoutHoverIcon), QPixmap(UiConstants.frameworLayoutActiveIcon), parent=self)
		layoutsButton.setObjectName("Layouts_activeLabel")
		self.toolBar.addWidget(layoutsButton)

		self.__layoutMenu = QMenu("Layout", layoutsButton)

		userLayouts = (("1", Qt.Key_1, "one"), ("2", Qt.Key_2, "two"), ("3", Qt.Key_3, "three"), ("4", Qt.Key_4, "four"), ("5", Qt.Key_5, "five"))

		for layout in userLayouts:
			action = QAction("Restore Layout {0}".format(layout[0]), self)
			action.setShortcut(QKeySequence(layout[1]))
			self.__layoutMenu.addAction(action)

			# Signals / Slots.
			action.triggered.connect(functools.partial(self.restoreLayout, layout[2]))

		self.__layoutMenu.addSeparator()

		for layout in userLayouts:
			action = QAction("Store Layout {0}".format(layout[0]), self)
			action.setShortcut(QKeySequence(Qt.CTRL + layout[1]))
			self.__layoutMenu.addAction(action)

			# Signals / Slots.
			action.triggered.connect(functools.partial(self.storeLayout, layout[2]))

		layoutsButton.setMenu(self.__layoutMenu)

		LOGGER.debug("> Adding Miscellaneous Button.")
		miscellaneousButton = Active_QLabel(QPixmap(UiConstants.frameworMiscellaneousIcon), QPixmap(UiConstants.frameworMiscellaneousHoverIcon), QPixmap(UiConstants.frameworMiscellaneousActiveIcon), parent=self)
		miscellaneousButton.setObjectName("Miscellaneous_activeLabel")
		self.toolBar.addWidget(miscellaneousButton)

		helpDisplayMiscAction = QAction("Help Content ...", self)
		apiDisplayMiscAction = QAction("Api Content ...", self)

		self.__miscMenu = QMenu("Miscellaneous", miscellaneousButton)

		self.__miscMenu.addAction(helpDisplayMiscAction)
		self.__miscMenu.addAction(apiDisplayMiscAction)
		self.__miscMenu.addSeparator()

		# Signals / Slots.
		helpDisplayMiscAction.triggered.connect(self.__helpDisplayMiscAction__triggered)
		apiDisplayMiscAction.triggered.connect(self.__apiDisplayMiscAction__triggered)

		miscellaneousButton.setMenu(self.__miscMenu)

		spacer = QLabel()
		spacer.setObjectName("Closure_Spacer_activeLabel")
		spacer.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
		self.toolBar.addWidget(spacer)

	@core.executionTrace
	def __setLayoutsActiveLabelsShortcuts(self):
		"""
		This Method Sets The Layouts Active Labels Shortcuts.
		"""

		LOGGER.debug("> Setting Layouts Active Labels Shortcuts.")

		for layoutActiveLabel in self.__layoutsActiveLabels:
			action = QAction(layoutActiveLabel.name, self)
			action.setShortcut(QKeySequence(layoutActiveLabel.shortcut))
			self.addAction(action)
			action.triggered.connect(functools.partial(self.restoreLayout, layoutActiveLabel.layout))

	@core.executionTrace
	def __getLayoutsActiveLabel(self):
		"""
		This Method Returns The Current Layout Active Label Index.

		@return: Layouts Active Label Index. ( Integer )
		"""

		LOGGER.debug("> Retrieving Current Layout Active Label Index.")

		for index in range(len(self.__layoutsActiveLabels)):
			if self.__layoutsActiveLabels[index].object_.isChecked():
				LOGGER.debug("> Current Layout Active Label Index: '{0}'.".format(index))
				return index

	@core.executionTrace
	def __setLayoutsActiveLabel(self, index):
		"""
		This Method Sets The Layouts Active Label.

		@param index: Layouts Active Label. ( Integer )
		"""

		LOGGER.debug("> Setting Layouts Active Labels States.")

		for index_ in range(len(self.__layoutsActiveLabels)):
			self.__layoutsActiveLabels[index_].object_.setChecked(index == index_ and True or False)

	@core.executionTrace
	def __activeLabel__clicked(self, activeLabel):
		"""
		This Method Is Triggered When An Active Label Is Clicked.
		"""

		LOGGER.debug("> Clicked Active Label: '{0}'.".format(activeLabel))

		self.restoreLayout(activeLabel)
		for layoutActivelabel in self.__layoutsActiveLabels:
			layoutActivelabel.layout is not activeLabel and layoutActivelabel.object_.setChecked(False)

	@core.executionTrace
	def __centralWidgetButton__clicked(self):
		"""
		This Method Sets The Central Widget Visibility.
		"""

		LOGGER.debug("> Central Widget Button Clicked!")

		if self.centralwidget.isVisible():
			self.centralwidget.hide()
		else:
			self.centralwidget.show()

	@core.executionTrace
	def __helpDisplayMiscAction__triggered(self, checked):
		"""
		This Method Is Triggered By helpDisplayMiscAction Action.

		@param checked: Checked State. ( Boolean )
		"""

		LOGGER.debug("> Opening URL: '{0}'.".format(UiConstants.frameworkHelpFile))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.frameworkHelpFile)))

	@core.executionTrace
	def __apiDisplayMiscAction__triggered(self, checked):
		"""
		This Method Is Triggered By apiDisplayMiscAction Action.

		@param checked: Checked State. ( Boolean )
		"""

		LOGGER.debug("> Opening URL: '{0}'.".format(UiConstants.frameworkApiFile))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.frameworkApiFile)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def __setVisualStyle(self):
		"""
		This Method Sets The Application Visual Style.
		"""

		LOGGER.debug("> Setting Application Visual Style.")

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			RuntimeConstants.application.setStyle(UiConstants.frameworkWindowsStyle)
			styleSheetFile = io.File(UiConstants.frameworkWindowsStylesheetFile)
		elif platform.system() == "Darwin":
			RuntimeConstants.application.setStyle(UiConstants.frameworkDarwinStyle)
			styleSheetFile = io.File(UiConstants.frameworkDarwinStylesheetFile)
		elif platform.system() == "Linux":
			RuntimeConstants.application.setStyle(UiConstants.frameworkLinuxStyle)
			styleSheetFile = io.File(UiConstants.frameworkLinuxStylesheetFile)

		if os.path.exists(styleSheetFile.file):
			LOGGER.debug("> Reading Style Sheet File: '{0}'.".format(styleSheetFile.file))
			styleSheetFile.read()
			RuntimeConstants.application.setStyleSheet(QString("".join(styleSheetFile.content)))
		else:
			raise OSError, "{0} | '{1}' Stylesheet File Is Not Available, Visual Style Will Not Be Applied!".format(self.__class__.__name__, styleSheetFile.file)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeLayout(self, name, *args):
		"""
		This Method Is Called When Storing A Layout.

		@param name: Layout Name. ( String )
		@param *args: Arguments. ( * )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Storing Layout '{0}'.".format(name))

		self.__settings.setKey("Layouts", "{0}_geometry".format(name), self.saveGeometry())
		self.__settings.setKey("Layouts", "{0}_windowState".format(name), self.saveState())
		self.__settings.setKey("Layouts", "{0}_centralWidget".format(name), self.centralwidget.isVisible())
		self.__settings.setKey("Layouts", "{0}_activeLabel".format(name), self.__getLayoutsActiveLabel())
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreLayout(self, name, *args):
		"""
		This Method Is Called When Restoring A Layout.

		@param name: Layout Name. ( String )
		@param *args: Arguments. ( * )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Restoring Layout '{0}'.".format(name))

		visibleComponents = [ "core.databaseBrowser" ]
		for component, profile in self.__componentsManager.components.items():
			profile.categorie == "ui" and component not in visibleComponents and self.__componentsManager.getInterface(component).ui and self.__componentsManager.getInterface(component).ui.hide()

		self.centralwidget.setVisible(self.__settings.getKey("Layouts", "{0}_centralWidget".format(name)).toBool())
		self.restoreState(self.__settings.getKey("Layouts", "{0}_windowState".format(name)).toByteArray())
		self.__corePreferencesManager.ui.Restore_Geometry_On_Layout_Change_checkBox.isChecked() and self.restoreGeometry(self.__settings.getKey("Layouts", "{0}_geometry".format(name)).toByteArray())
		self.__setLayoutsActiveLabel(self.__settings.getKey("Layouts", "{0}_activeLabel".format(name)).toInt()[0])
		QApplication.focusWidget() and QApplication.focusWidget().clearFocus()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreStartupLayout(self):
		"""
		This Method Restores The Startup Layout.

		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Restoring Startup Layout.")

		if self.restoreLayout(UiConstants.frameworkStartupLayout):
			not self.__corePreferencesManager.ui.Restore_Geometry_On_Layout_Change_checkBox.isChecked() and self.restoreGeometry(self.__settings.getKey("Layouts", "{0}_geometry".format(UiConstants.frameworkStartupLayout)).toByteArray())
			return True
		else:
			raise Exception, "{0} | Exception Raised While Restoring Startup Layout!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeStartupLayout(self):
		"""
		This Method Stores The Startup Layout.

		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Storing Startup Layout.")

		return self.storeLayout(UiConstants.frameworkStartupLayout)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeLastBrowsedPath(self, path):
		"""
		This Method Is A Wrapper Method For Storing The Last Browser Path.
		
		@param path: Provided Path. ( QString )
		@return: Provided Path. ( QString )
		"""

		path = str(path)

		lastBrowserPath = os.path.normpath(os.path.join(os.path.isfile(path) and os.path.dirname(path) or path, ".."))
		LOGGER.debug("> Storing Last Browsed Path: '%s'.", lastBrowserPath)

		self.__lastBrowsedPath = lastBrowserPath

		return path

#***************************************************************************************
#***	Overall Definitions.
#***************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(siblgui.ui.common.uiStandaloneSystemExitExceptionHandler, False, OSError)
def _run():
	"""
	This Definition Is Called When sIBL_GUI Starts.
	"""

	# Command Line Parameters Handling.
	RuntimeConstants.parameters, RuntimeConstants.args = _getCommandLineParameters(sys.argv)

	if RuntimeConstants.parameters.about:
		for line in _getHeaderMessage():
			sys.stdout.write("{0}\n".format(line))
		foundations.common.exit(1, LOGGER, [])

	# Redirecting Standard Output And Error Messages.
	sys.stdout = core.StandardMessageHook(LOGGER)
	sys.stderr = core.StandardMessageHook(LOGGER)

	# Setting Application Verbose Level.
	LOGGER.setLevel(logging.DEBUG)

	# Setting User Application Datas Directory.
	if RuntimeConstants.parameters.userApplicationDatasDirectory:
		RuntimeConstants.userApplicationDatasDirectory = RuntimeConstants.parameters.userApplicationDatasDirectory
	else:
		RuntimeConstants.userApplicationDatasDirectory = foundations.common.getUserApplicationDatasDirectory()

	if not _setUserApplicationDatasDirectory(RuntimeConstants.userApplicationDatasDirectory):
		raise OSError, "'{0}' User Application Datas Directory Is Not Available, {1} Will Now Close!".format(RuntimeConstants.userApplicationDatasDirectory, Constants.applicationName)

	LOGGER.debug("> Application Python Interpreter: '{0}'".format(sys.executable))
	LOGGER.debug("> Application Startup Location: '{0}'".format(os.getcwd()))
	LOGGER.debug("> Session User Application Datas Directory: '{0}'".format(RuntimeConstants.userApplicationDatasDirectory))

	# Getting The Logging File Path.
	RuntimeConstants.loggingFile = os.path.join(RuntimeConstants.userApplicationDatasDirectory, Constants.loggingDirectory, Constants.loggingFile)

	try:
		os.path.exists(RuntimeConstants.loggingFile) and os.remove(RuntimeConstants.loggingFile)
	except:
		raise OSError, "{0} Logging File Is Currently Locked By Another Process, {1} Will Now Close!".format(RuntimeConstants.loggingFile, Constants.applicationName)

	try:
		RuntimeConstants.loggingFileHandler = logging.FileHandler(RuntimeConstants.loggingFile)
		RuntimeConstants.loggingFileHandler.setFormatter(RuntimeConstants.loggingFormatters[Constants.loggingDefaultFormatter])
		LOGGER.addHandler(RuntimeConstants.loggingFileHandler)
	except:
		raise OSError, "{0} Logging File Is Not Available, {1} Will Now Close!".format(RuntimeConstants.loggingFile, Constants.applicationName)

	# Retrieving Framework Verbose Level From Settings File.
	LOGGER.debug("> Initializing {0}!".format(Constants.applicationName))
	RuntimeConstants.settingsFile = os.path.join(RuntimeConstants.userApplicationDatasDirectory, Constants.settingsDirectory, Constants.settingsFile)

	RuntimeConstants.settings = Preferences(RuntimeConstants.settingsFile)

	LOGGER.debug("> Retrieving Default Layouts.")
	RuntimeConstants.settings.setDefaultLayouts()

	os.path.exists(RuntimeConstants.settingsFile) or RuntimeConstants.settings.setDefaultPreferences()

	LOGGER.debug("> Retrieving Stored Verbose Level.")
	RuntimeConstants.verbosityLevel = RuntimeConstants.parameters.verbosityLevel and RuntimeConstants.parameters.verbosityLevel or RuntimeConstants.settings.getKey("Settings", "verbosityLevel").toInt()[0]
	LOGGER.debug("> Setting Logger Verbosity Level To: '{0}'.".format(RuntimeConstants.verbosityLevel))
	core.setVerbosityLevel(RuntimeConstants.verbosityLevel)

	LOGGER.debug("> Retrieving Stored Logging Formatter.")
	loggingFormatter = RuntimeConstants.parameters.loggingFormater and RuntimeConstants.parameters.loggingFormater or str(RuntimeConstants.settings.getKey("Settings", "loggingFormatter").toString())
	loggingFormatter = loggingFormatter in RuntimeConstants.loggingFormatters.keys() and loggingFormatter or None
	RuntimeConstants.loggingActiveFormatter = loggingFormatter and loggingFormatter or Constants.loggingDefaultFormatter
	LOGGER.debug("> Setting Logging Formatter: '{0}'.".format(RuntimeConstants.loggingActiveFormatter))
	for handler in (RuntimeConstants.loggingConsoleHandler, RuntimeConstants.loggingFileHandler):
		handler and handler.setFormatter(RuntimeConstants.loggingFormatters[RuntimeConstants.loggingActiveFormatter])

	# Starting The Session Handler.
	RuntimeConstants.loggingSessionHandlerStream = StreamObject()
	RuntimeConstants.loggingSessionHandler = logging.StreamHandler(RuntimeConstants.loggingSessionHandlerStream)
	RuntimeConstants.loggingSessionHandler.setFormatter(RuntimeConstants.loggingFormatters[RuntimeConstants.loggingActiveFormatter])
	LOGGER.addHandler(RuntimeConstants.loggingSessionHandler)

	LOGGER.info(Constants.loggingSeparators)
	for line in _getHeaderMessage():
		LOGGER.info(line)
	LOGGER.info("{0} | Session Started At: {1}".format(Constants.applicationName, time.strftime('%X - %x')))
	LOGGER.info(Constants.loggingSeparators)
	LOGGER.info("{0} | Starting Interface!".format(Constants.applicationName))

	RuntimeConstants.application = QApplication(sys.argv)

	# Initializing SplashScreen.
	if RuntimeConstants.parameters.hideSplashScreen:
		LOGGER.debug("> SplashScreen Skipped By 'hideSplashScreen' Command Line Parameter.")
	else:
		LOGGER.debug("> Initializing SplashScreen.")

		RuntimeConstants.splashscreenPicture = QPixmap(UiConstants.frameworkSplashScreenPicture)
		RuntimeConstants.splashscreen = Delayed_QSplashScreen(RuntimeConstants.splashscreenPicture)
		RuntimeConstants.splashscreen.setMessage("{0} - {1} | Initializing {0}.".format(Constants.applicationName, Constants.releaseVersion), textColor=Qt.white)
		RuntimeConstants.splashscreen.show()

	RuntimeConstants.ui = sIBL_GUI()
	RuntimeConstants.ui.show()
	RuntimeConstants.ui.raise_()

	sys.exit(RuntimeConstants.application.exec_())

@core.executionTrace
def _exit():
	"""
	This Definition Is Called When sIBL_GUI Closes.
	"""

	LOGGER.info("{0} | Closing Interface! ".format(Constants.applicationName))
	LOGGER.info(Constants.loggingSeparators)
	LOGGER.info("{0} | Session Ended At: {1}".format(Constants.applicationName, time.strftime('%X - %x')))
	LOGGER.info(Constants.loggingSeparators)

	foundations.common.closeHandler(LOGGER, RuntimeConstants.loggingConsoleHandler)

	QApplication.exit()

@core.executionTrace
def _getHeaderMessage():
	"""
	This Definition Builds The Header Message.

	@return: Header Message ( List )
	"""

	message = {	"{0} | Copyright ( C ) 2008 - 2011 Thomas Mansencal - thomas.mansencal@gmail.com".format(Constants.applicationName),
				"{0} | This Software Is Released Under Terms Of GNU GPL V3 License.".format(Constants.applicationName),
				"{0} | http://www.gnu.org/licenses/ ".format(Constants.applicationName),
				"{0} | Version: {1}".format(Constants.applicationName, Constants.releaseVersion)}
	return message

@core.executionTrace
def _getCommandLineParameters(argv):
	"""
	This Definition Process Command Line Parameters.

	@param argv: Command Line Parameters. ( String )
	@return: Settings, Arguments ( Parser Instance )
	"""

	argv = argv or sys.argv[1:]

	parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter (indent_increment=2, max_help_position=8, width=128, short_first=1), add_help_option=None)

	parser.add_option("-h", "--help", action="help", help="'Display This Help Message And Exit.'")
	parser.add_option("-a", "--about", action="store_true", default=False, dest="about", help="'Display Application About Message.'")
	parser.add_option("-v", "--verbose", action="store", type="int", dest="verbosityLevel", help="'Application Verbosity Levels:  0 = Critical | 1 = Error | 2 = Warning | 3 = Info | 4 = Debug.'")
	parser.add_option("-f", "--loggingFormatter", action="store", type="string", dest="loggingFormater", help="'Application Logging Formatter: '{0}'.'".format(", ".join(sorted(RuntimeConstants.loggingFormatters.keys()))))
	parser.add_option("-u", "--userApplicationDatasDirectory", action="store", type="string", dest="userApplicationDatasDirectory", help="'User Application Datas Directory'.")

	parser.add_option("-t", "--deactivateWorkerThreads", action="store_true", default=False, dest="deactivateWorkerThreads", help="'Deactivate Worker Threads'.")

	parser.add_option("-d", "--databaseDirectory", action="store", type="string", dest="databaseDirectory", help="'Database Directory'.")
	parser.add_option("-r", "--databaseReadOnly", action="store_true", default=False, dest="databaseReadOnly", help="'Database Read Only'.")

	parser.add_option("-o", "--loaderScriptsOutputDirectory", action="store", type="string", dest="loaderScriptsOutputDirectory", help="'Loader Scripts Output Directory'.")

	parser.add_option("-s", "--hideSplashScreen", action="store_true", default=False, dest="hideSplashScreen", help="'Hide Splash Screen'.")

	parameters, args = parser.parse_args(argv)

	return parameters, args

@core.executionTrace
@foundations.exceptions.exceptionsHandler(siblgui.ui.common.uiStandaloneSystemExitExceptionHandler, False, OSError)
def _setUserApplicationDatasDirectory(path):
	"""
	This Definition Sets The Application Datas Directory.

	@param path: Starting Point For The Directories Tree Creation. ( String )
	@return: Definition Success. ( Boolean )		
	"""

	userApplicationDatasDirectory = RuntimeConstants.userApplicationDatasDirectory

	LOGGER.debug("> Current Application Datas Directory '{0}'.".format(userApplicationDatasDirectory))
	if io.setLocalDirectory(userApplicationDatasDirectory):
		for directory in Constants.preferencesDirectories:
			if not io.setLocalDirectory(os.path.join(userApplicationDatasDirectory, directory)):
				raise OSError, "'{0}' Directory Creation Failed , {1} Will Now Close!".format(os.path.join(userApplicationDatasDirectory, directory), Constants.applicationName)
		return True
	else:
		raise OSError, "'{0}' Directory Creation Failed , {1} Will Now Close!".format(userApplicationDatasDirectory, Constants.applicationName)

#***********************************************************************************************
#***	Launcher
#***********************************************************************************************
if __name__ == "__main__":
	_run()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
