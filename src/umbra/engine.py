#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**engine.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| This module is the main **Umbra** package module.
	| It defines various classes, methods and definitions to run, maintain and exit the Application.
	| The main Application object is the :class:`Umbra` class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
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
#***	Path manipulations.
#***********************************************************************************************
def _setApplicationPackageDirectory():
	"""
	This definition sets the Application package directory in the path.

	:return: Definition success. ( Boolean )
	"""

	applicationPackageDirectory = os.path.normpath(os.path.join(sys.path[0], "../"))
	applicationPackageDirectory not in sys.path and sys.path.append(applicationPackageDirectory)
	return True

_setApplicationPackageDirectory()

#***********************************************************************************************
#***	Dependencies globals manipulation.
#***********************************************************************************************
import foundations.globals.constants
import manager.globals.constants
from umbra.globals.constants import Constants

def _overrideDependenciesGlobals():
	"""
	This definition overrides dependencies globals.

	:return: Definition success. ( Boolean )
	"""

	foundations.globals.constants.Constants.logger = manager.globals.constants.Constants.logger = Constants.logger
	foundations.globals.constants.Constants.applicationDirectory = manager.globals.constants.Constants.applicationDirectory = Constants.applicationDirectory
	return True

_overrideDependenciesGlobals()

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import umbra.ui.common
from foundations.streamObject import StreamObject
from manager.componentsManager import Manager
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants
from umbra.preferences import Preferences
from umbra.ui.widgets.active_QLabel import Active_QLabel
from umbra.ui.widgets.delayed_QSplashScreen import Delayed_QSplashScreen

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

# Starting the console handler.
if not hasattr(sys, "frozen") or not (platform.system() == "Windows" or platform.system() == "Microsoft"):
	RuntimeGlobals.loggingConsoleHandler = logging.StreamHandler(sys.__stdout__)
	RuntimeGlobals.loggingConsoleHandler.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
	LOGGER.addHandler(RuntimeGlobals.loggingConsoleHandler)

# Defining logging formatters.
RuntimeGlobals.loggingFormatters = {"Default" :core.LOGGING_DEFAULT_FORMATTER,
									"Extended" : core.LOGGING_EXTENDED_FORMATTER,
									"Standard" : core.LOGGING_STANDARD_FORMATTER}

class Ui_Setup():
	"""
	This class defines the Application ui setup methods.
	"""

	pass

class Ui_Type():
	"""
	This class defines the Application ui type base class ( `QMainWindow <http://doc.qt.nokia.com/4.7/qmainwindow.html>`_ ).
	"""

	pass

RuntimeGlobals.resourcesPaths.append(os.path.join(umbra.__path__[0], Constants.resourcesDirectory))
RuntimeGlobals.uiFile = umbra.ui.common.getResourcePath(UiConstants.uiFile)
if os.path.exists(RuntimeGlobals.uiFile):
	Ui_Setup, Ui_Type = uic.loadUiType(RuntimeGlobals.uiFile)
else:
	umbra.ui.common.uiStandaloneSystemExitExceptionHandler(OSError("'{0}' ui file is not available, {1} will now close!".format(UiConstants.uiFile, Constants.applicationName)), Constants.applicationName)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LayoutActiveLabel(core.Structure):
	"""
	This class represents a storage object for layout active labels attributes.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: name, object, layout, shortcut. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class Umbra(Ui_Type, Ui_Setup):
	"""
	This class is the main class of the Application.
	"""

	#***********************************************************************************************
	#***	Initialization..
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiSystemExitExceptionHandler, False, foundations.exceptions.ProgrammingError, Exception)
	def __init__(self, paths, components=None):
		"""
		This method initializes the class.

		:param paths: Components paths. ( QString )
		:param components: Mandatory components names. ( QString )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Ui_Type.__init__(self)
		Ui_Setup.__init__(self)

		self.setupUi(self)

		self.closeEvent = self.__closeUi

		# --- Setting class attributes. ---
		self.__timer = None
		self.__componentsManager = None
		self.__lastBrowsedPath = os.getcwd()
		self.__userApplicationDatasDirectory = RuntimeGlobals.userApplicationDatasDirectory
		self.__loggingSessionHandler = RuntimeGlobals.loggingSessionHandler
		self.__loggingFileHandler = RuntimeGlobals.loggingFileHandler
		self.__loggingConsoleHandler = RuntimeGlobals.loggingConsoleHandler
		self.__loggingSessionHandlerStream = RuntimeGlobals.loggingSessionHandlerStream
		self.__loggingActiveFormatter = RuntimeGlobals.loggingActiveFormatter
		self.__settings = RuntimeGlobals.settings
		self.__settings._datas = core.Structure(restoreGeometryOnLayoutChange=True)
		self.__verbosityLevel = RuntimeGlobals.verbosityLevel
		self.__parameters = RuntimeGlobals.parameters
		self.__developmentActiveLabel = None
		self.__preferencesActiveLabel = None
		self.__layoutsActiveLabels = None
		self.__layoutMenu = None
		self.__miscMenu = None
		self.__workerThreads = []

		# --- Initializing timer. ---
		self.__timer = QTimer(self)
		self.__timer.start(Constants.defaultTimerCycle)

		# --- Initializing application. ---
		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Initializing interface.".format(self.__class__.__name__, Constants.releaseVersion), textColor=Qt.white, waitTime=0.25)

		# Visual style initialization.
		self.__setVisualStyle()
		umbra.ui.common.setWindowDefaultIcon(self)

		# Setting window title and toolBar.
		self.setWindowTitle("{0} - {1}".format(Constants.applicationName, Constants.releaseVersion))
		self.__initializeToolBar()

		# --- Initializing Components Manager. ---
		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Initializing Components manager.".format(self.__class__.__name__, Constants.releaseVersion), textColor=Qt.white, waitTime=0.25)

		self.__componentsManager = Manager(paths)
		self.__componentsManager.registerComponents()

		if not self.__componentsManager.components:
			raise foundations.exceptions.ProgrammingError, "'{0}' Components Manager has no Components, {1} will now close!".format(self.__componentsManager, Constants.applicationName)

		self.__componentsManager.instantiateComponents(self.__componentsInstantiationCallback)

		# --- Activating mandatory Components. ---
		components = components or []
		for component in components:
			profile = self.__componentsManager.components[component]
			interface = self.__componentsManager.getInterface(component)
			setattr(self, "_{0}__{1}".format(self.__class__.__name__, Manager.getComponentAttributeName(component)), interface)
			RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, component), textColor=Qt.white)
			interface.activate(self)
			if profile.categorie == "default":
				interface.initialize()
			elif profile.categorie == "ui":
				interface.addWidget()
				interface.initializeUi()

		# --- Activating others Components. ---
		deactivatedComponents = self.__settings.getKey("Settings", "deactivatedComponents").toString().split(",")
		for component in self.__componentsManager.getComponents():
			if component in deactivatedComponents:
				continue

			profile = self.__componentsManager.components[component]
			interface = self.__componentsManager.getInterface(component)
			if interface.activated:
				continue

			RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, component), textColor=Qt.white)
			interface.activate(self)
			if profile.categorie == "default":
				interface.initialize()
			elif profile.categorie == "ui":
				interface.addWidget()
				interface.initializeUi()

		# Hiding splashscreen.
		LOGGER.debug("> Hiding splashscreen.")
		if RuntimeGlobals.splashscreen:
			RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Initialization done.".format(self.__class__.__name__, Constants.releaseVersion), textColor=Qt.white)
			RuntimeGlobals.splashscreen.hide()

		# --- Running onStartup components methods. ---
		for component in self.__componentsManager.getComponents():
			interface = self.__componentsManager.getInterface(component)
			if interface.activated:
				hasattr(interface, "onStartup") and interface.onStartup()

		self.__setLayoutsActiveLabelsShortcuts()

		self.restoreStartupLayout()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def timer(self):
		"""
		This method is the property for **self.__timer** attribute.

		:return: self.__timer. ( QTimer )
		"""

		return self.__timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		This method is the setter method for **self.__timer** attribute.

		:param value: Attribute value. ( QTimer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("timer"))

	@timer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		This method is the deleter method for **self.__timer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("timer"))

	@property
	def componentsManager(self):
		"""
		This method is the property for **self.__componentsManager** attribute.

		:return: self.__componentsManager. ( Object )
		"""

		return self.__componentsManager

	@componentsManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsManager(self, value):
		"""
		This method is the setter method for **self.__componentsManager** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("componentsManager"))

	@componentsManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsManager(self):
		"""
		This method is the deleter method for **self.__componentsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("componentsManager"))


	@property
	def lastBrowsedPath(self):
		"""
		This method is the property for **self.__lastBrowsedPath** attribute.

		:return: self.__lastBrowsedPath. ( String )
		"""

		return self.__lastBrowsedPath

	@lastBrowsedPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def lastBrowsedPath(self, value):
		"""
		This method is the setter method for **self.__lastBrowsedPath** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("lastBrowsedPath", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' directory doesn't exists!".format("lastBrowsedPath", value)
		self.__lastBrowsedPath = value

	@lastBrowsedPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lastBrowsedPath(self):
		"""
		This method is the deleter method for **self.__lastBrowsedPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("lastBrowsedPath"))

	@property
	def userApplicationDatasDirectory(self):
		"""
		This method is the property for **self.__userApplicationDatasDirectory** attribute.

		:return: self.__userApplicationDatasDirectory. ( String )
		"""

		return self.__userApplicationDatasDirectory

	@userApplicationDatasDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userApplicationDatasDirectory(self, value):
		"""
		This method is the setter method for **self.__userApplicationDatasDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("userApplicationDatasDirectory"))

	@userApplicationDatasDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userApplicationDatasDirectory(self):
		"""
		This method is the deleter method for **self.__userApplicationDatasDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("userApplicationDatasDirectory"))

	@property
	def loggingSessionHandler(self):
		"""
		This method is the property for **self.__loggingSessionHandler** attribute.

		:return: self.__loggingSessionHandler. ( Handler )
		"""

		return self.__loggingSessionHandler

	@loggingSessionHandler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandler(self, value):
		"""
		This method is the setter method for **self.__loggingSessionHandler** attribute.

		:param value: Attribute value. ( Handler )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("loggingSessionHandler"))

	@loggingSessionHandler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandler(self):
		"""
		This method is the deleter method for **self.__loggingSessionHandler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("loggingSessionHandler"))

	@property
	def loggingFileHandler(self):
		"""
		This method is the property for **self.__loggingFileHandler** attribute.

		:return: self.__loggingFileHandler. ( Handler )
		"""

		return self.__loggingFileHandler

	@loggingFileHandler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingFileHandler(self, value):
		"""
		This method is the setter method for **self.__loggingFileHandler** attribute.

		:param value: Attribute value. ( Handler )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("loggingFileHandler"))

	@loggingFileHandler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingFileHandler(self):
		"""
		This method is the deleter method for **self.__loggingFileHandler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("loggingFileHandler"))

	@property
	def loggingConsoleHandler(self):
		"""
		This method is the property for **self.__loggingConsoleHandler** attribute.

		:return: self.__loggingConsoleHandler. ( Handler )
		"""

		return self.__loggingConsoleHandler

	@loggingConsoleHandler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingConsoleHandler(self, value):
		"""
		This method is the setter method for **self.__loggingConsoleHandler** attribute.

		:param value: Attribute value. ( Handler )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("loggingConsoleHandler"))

	@loggingConsoleHandler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingConsoleHandler(self):
		"""
		This method is the deleter method for **self.__loggingConsoleHandler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("loggingConsoleHandler"))

	@property
	def loggingSessionHandlerStream(self):
		"""
		This method is the property for **self.__loggingSessionHandlerStream** attribute.

		:return: self.__loggingSessionHandlerStream. ( StreamObject )
		"""

		return self.__loggingSessionHandlerStream

	@loggingSessionHandlerStream.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandlerStream(self, value):
		"""
		This method is the setter method for **self.__loggingSessionHandlerStream** attribute.

		:param value: Attribute value. ( StreamObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("loggingSessionHandlerStream"))

	@loggingSessionHandlerStream.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandlerStream(self):
		"""
		This method is the deleter method for **self.__loggingSessionHandlerStream** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("loggingSessionHandlerStream"))

	@property
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))

	@property
	def verbosityLevel(self):
		"""
		This method is the property for **self.__verbosityLevel** attribute.

		:return: self.__verbosityLevel. ( Integer )
		"""

		return self.__verbosityLevel

	@verbosityLevel.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def verbosityLevel(self, value):
		"""
		This method is the setter method for **self.__verbosityLevel** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("verbosityLevel", value)
			assert value >= 0 and value <= 4, "'{0}' attribute: Value need to be exactly beetween 0 and 4!".format("verbosityLevel")
		self.__verbosityLevel = value

	@verbosityLevel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def verbosityLevel(self):
		"""
		This method is the deleter method for **self.__verbosityLevel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("verbosityLevel"))

	@property
	def parameters(self):
		"""
		This method is the property for **self.__parameters** attribute.

		:return: self.__parameters. ( Object )
		"""

		return self.__parameters

	@parameters.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parameters(self, value):
		"""
		This method is the setter method for **self.__parameters** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("parameters"))

	@parameters.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parameters(self):
		"""
		This method is the deleter method for **self.__parameters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("parameters"))

	@property
	def developmentActiveLabel (self):
		"""
		This method is the property for **self.__developmentActiveLabel** attribute.

		:return: self.__developmentActiveLabel . ( Active_QLabel )
		"""

		return self.__developmentActiveLabel

	@developmentActiveLabel .setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def developmentActiveLabel (self, value):
		"""
		This method is the setter method for **self.__developmentActiveLabel** attribute.

		:param value: Attribute value. ( Active_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("developmentActiveLabel "))

	@developmentActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def developmentActiveLabel (self):
		"""
		This method is the deleter method for **self.__developmentActiveLabel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("developmentActiveLabel "))

	@property
	def preferencesActiveLabel (self):
		"""
		This method is the property for **self.__preferencesActiveLabel** attribute.

		:return: self.__preferencesActiveLabel. ( Active_QLabel )
		"""

		return self.__preferencesActiveLabel

	@preferencesActiveLabel .setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesActiveLabel (self, value):
		"""
		This method is the setter method for **self.__preferencesActiveLabel** attribute.

		:param value: Attribute value. ( Active_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("preferencesActiveLabel "))

	@preferencesActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesActiveLabel (self):
		"""
		This method is the deleter method for **self.__preferencesActiveLabel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("preferencesActiveLabel "))

	@property
	def layoutsActiveLabels(self):
		"""
		This method is the property for **self.__layoutsActiveLabels** attribute.

		:return: self.__layoutsActiveLabels. ( Tuple )
		"""

		return self.__layoutsActiveLabels

	@layoutsActiveLabels.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutsActiveLabels(self, value):
		"""
		This method is the setter method for **self.__layoutsActiveLabels** attribute.

		:param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("layoutsActiveLabels"))

	@layoutsActiveLabels.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutsActiveLabels(self):
		"""
		This method is the deleter method for **self.__layoutsActiveLabels** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("layoutsActiveLabels"))

	@property
	def layoutMenu(self):
		"""
		This method is the property for **self.__layoutMenu** attribute.

		:return: self.__layoutMenu. ( QMenu )
		"""

		return self.__layoutMenu

	@layoutMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutMenu(self, value):
		"""
		This method is the setter method for **self.__layoutMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("layoutMenu"))

	@layoutMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutMenu(self):
		"""
		This method is the deleter method for **self.__layoutMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("layoutMenu"))

	@property
	def miscMenu(self):
		"""
		This method is the property for **self.__miscMenu** attribute.

		:return: self.__miscMenu. ( QMenu )
		"""

		return self.__miscMenu

	@miscMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def miscMenu(self, value):
		"""
		This method is the setter method for **self.__miscMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("miscMenu"))

	@miscMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def miscMenu(self):
		"""
		This method is the deleter method for **self.__miscMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("miscMenu"))

	@property
	def workerThreads(self):
		"""
		This method is the property for **self.__workerThreads** attribute.

		:return: self.__workerThreads. ( List )
		"""

		return self.__workerThreads

	@workerThreads.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def workerThreads(self, value):
		"""
		This method is the setter method for **self.__workerThreads** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("workerThreads"))

	@workerThreads.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def workerThreads(self):
		"""
		This method is the deleter method for **self.__workerThreads** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("workerThreads"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __closeUi(self, event):
		"""
		This method is called when close event is fired.

		:param event: QEvent. ( QEvent )
		"""

		# --- Running onClose components methods. ---
		for component in self.__componentsManager.getComponents():
			interface = self.__componentsManager.getInterface(component)
			if interface.activated:
				hasattr(interface, "onClose") and interface.onClose()

		# Storing current layout.
		self.storeStartupLayout()
		self.__settings.settings.sync()

		# Stopping worker threads.
		for workerThread in self.__workerThreads:
			if not workerThread.isFinished():
				LOGGER.debug("> Stopping worker thread: '{0}'.".format(workerThread))
				workerThread.exit()

		foundations.common.removeLoggingHandler(LOGGER, self.__loggingFileHandler)
		foundations.common.removeLoggingHandler(LOGGER, self.__loggingSessionHandler)
		# foundations.common.removeLoggingHandler(LOGGER, self.__loggingconsolehandler)

		# Stopping the timer.
		self.__timer.stop()
		self.__timer = None

		self.deleteLater()
		event.accept()

		_exit()

	@core.executionTrace
	def __componentsInstantiationCallback(self, profile):
		"""
		This method is a callback for the Components instantiation.

		:param profile: Component Profile. ( Profile )
		"""

		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Instantiating {2} Component.".format(self.__class__.__name__, Constants.releaseVersion, profile.name), textColor=Qt.white)

	@core.executionTrace
	def __initializeToolBar(self):
		"""
		This method initializes Application toolBar.
		"""

		LOGGER.debug("> Initializing Application toolBar.")

		self.toolBar.setIconSize(QSize(UiConstants.defaultToolbarIconSize, UiConstants.defaultToolbarIconSize))

		LOGGER.debug("> Adding Application logo.")
		logoLabel = QLabel()
		logoLabel.setObjectName("Application_Logo_label")
		logoLabel.setPixmap(QPixmap(umbra.ui.common.getResourcePath(UiConstants.logoImage)))
		self.toolBar.addWidget(logoLabel)

		spacer = QLabel()
		spacer.setObjectName("Logo_Spacer_label")
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolBar.addWidget(spacer)

		toolBarFont = QFont()
		toolBarFont.setPointSize(16)

		LOGGER.debug("> Adding Active_QLabels.")

		self.__developmentActiveLabel = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(UiConstants.developmentIcon)),
													QPixmap(umbra.ui.common.getResourcePath(UiConstants.developmentHoverIcon)),
													QPixmap(umbra.ui.common.getResourcePath(UiConstants.developmentActiveIcon)), True)
		self.__developmentActiveLabel.setObjectName("Development_activeLabel")
		self.toolBar.addWidget(self.__developmentActiveLabel)

		self.__preferencesActiveLabel = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(UiConstants.preferencesIcon)),
													QPixmap(umbra.ui.common.getResourcePath(UiConstants.preferencesHoverIcon)),
													QPixmap(umbra.ui.common.getResourcePath(UiConstants.preferencesActiveIcon)), True)
		self.__preferencesActiveLabel.setObjectName("Preferences_activeLabel")
		self.toolBar.addWidget(self.__preferencesActiveLabel)

		self.__layoutsActiveLabels = (LayoutActiveLabel(name="Development", object_=self.__developmentActiveLabel, layout="developmentCentric", shortcut=Qt.Key_9),
									LayoutActiveLabel(name="Preferences", object_=self.__preferencesActiveLabel, layout="preferencesCentric", shortcut=Qt.Key_0))

		# Signals / Slots.
		for layoutActiveLabel in self.__layoutsActiveLabels:
			layoutActiveLabel.object_.clicked.connect(functools.partial(self.__layoutActiveLabel__clicked, layoutActiveLabel.layout))

		LOGGER.debug("> Adding layout button.")
		layoutButton = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(UiConstants.layoutIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.layoutHoverIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.layoutActiveIcon)), parent=self)
		layoutButton.setObjectName("Layout_activeLabel")
		self.toolBar.addWidget(layoutButton)

		self.__layoutMenu = QMenu("Layout", layoutButton)

		userLayouts = (("1", Qt.Key_1, "one"), ("2", Qt.Key_2, "two"), ("3", Qt.Key_3, "three"), ("4", Qt.Key_4, "four"), ("5", Qt.Key_5, "five"))

		for layout in userLayouts:
			action = QAction("Restore layout {0}".format(layout[0]), self)
			action.setShortcut(QKeySequence(layout[1]))
			self.__layoutMenu.addAction(action)

			# Signals / Slots.
			action.triggered.connect(functools.partial(self.restoreLayout, layout[2]))

		self.__layoutMenu.addSeparator()

		for layout in userLayouts:
			action = QAction("Store layout {0}".format(layout[0]), self)
			action.setShortcut(QKeySequence(Qt.CTRL + layout[1]))
			self.__layoutMenu.addAction(action)

			# Signals / Slots.
			action.triggered.connect(functools.partial(self.storeLayout, layout[2]))

		layoutButton.setMenu(self.__layoutMenu)

		LOGGER.debug("> Adding miscellaneous button.")
		miscellaneousButton = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(UiConstants.miscellaneousIcon)),
										QPixmap(umbra.ui.common.getResourcePath(UiConstants.miscellaneousHoverIcon)),
										QPixmap(umbra.ui.common.getResourcePath(UiConstants.miscellaneousActiveIcon)), parent=self)
		miscellaneousButton.setObjectName("Miscellaneous_activeLabel")
		self.toolBar.addWidget(miscellaneousButton)

		helpDisplayMiscAction = QAction("Help content ...", self)
		apiDisplayMiscAction = QAction("Api content ...", self)

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
		This method sets the layouts **Active_QLabels** shortcuts.
		"""

		LOGGER.debug("> Setting layouts Active_QLabels shortcuts.")

		for layoutActiveLabel in self.__layoutsActiveLabels:
			action = QAction(layoutActiveLabel.name, self)
			action.setShortcut(QKeySequence(layoutActiveLabel.shortcut))
			self.addAction(action)
			action.triggered.connect(functools.partial(self.restoreLayout, layoutActiveLabel.layout))

	@core.executionTrace
	def __getLayoutsActiveLabel(self):
		"""
		This method returns the current layout **Active_QLabel** index.

		:return: Layouts Active_QLabel index. ( Integer )
		"""

		LOGGER.debug("> Retrieving current layout Active_QLabel index.")

		for index in range(len(self.__layoutsActiveLabels)):
			if self.__layoutsActiveLabels[index].object_.isChecked():
				LOGGER.debug("> Current layout Active_QLabel index: '{0}'.".format(index))
				return index

	@core.executionTrace
	def __setLayoutsActiveLabel(self, index):
		"""
		This method sets the layouts **Active_QLabel**.

		:param index: Layouts Active_QLabel. ( Integer )
		"""

		LOGGER.debug("> Setting layouts Active_QLabels states.")

		for index_ in range(len(self.__layoutsActiveLabels)):
			self.__layoutsActiveLabels[index_].object_.setChecked(index == index_ and True or False)

	@core.executionTrace
	def __layoutActiveLabel__clicked(self, activeLabel):
		"""
		This method is triggered when a layout **Active_QLabel** is clicked.
		"""

		LOGGER.debug("> Clicked Active_QLabel: '{0}'.".format(activeLabel))

		self.restoreLayout(activeLabel)
		for layoutActivelabel in self.__layoutsActiveLabels:
			layoutActivelabel.layout is not activeLabel and layoutActivelabel.object_.setChecked(False)

	@core.executionTrace
	def __helpDisplayMiscAction__triggered(self, checked):
		"""
		This method is triggered by **helpDisplayMiscAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.helpFile))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.helpFile)))

	@core.executionTrace
	def __apiDisplayMiscAction__triggered(self, checked):
		"""
		This method is triggered by **apiDisplayMiscAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.apiFile))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.apiFile)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def __setVisualStyle(self):
		"""
		This method sets the Application visual style.
		"""

		LOGGER.debug("> Setting Application visual style.")

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			RuntimeGlobals.application.setStyle(UiConstants.windowsStyle)
			styleSheetFile = io.File(umbra.ui.common.getResourcePath(UiConstants.windowsStylesheetFile))
		elif platform.system() == "Darwin":
			RuntimeGlobals.application.setStyle(UiConstants.darwinStyle)
			styleSheetFile = io.File(umbra.ui.common.getResourcePath(UiConstants.darwinStylesheetFile))
		elif platform.system() == "Linux":
			RuntimeGlobals.application.setStyle(UiConstants.linuxStyle)
			styleSheetFile = io.File(umbra.ui.common.getResourcePath(UiConstants.linuxStylesheetFile))

		if os.path.exists(styleSheetFile.file):
			LOGGER.debug("> Reading style sheet file: '{0}'.".format(styleSheetFile.file))
			styleSheetFile.read()
			RuntimeGlobals.application.setStyleSheet(QString("".join(styleSheetFile.content)))
		else:
			raise OSError, "{0} | '{1}' stylesheet file is not available, visual style will not be applied!".format(self.__class__.__name__, styleSheetFile.file)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeLayout(self, name, *args):
		"""
		This method is called when storing a layout.

		:param name: Layout name. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing layout '{0}'.".format(name))

		self.__settings.setKey("Layouts", "{0}_geometry".format(name), self.saveGeometry())
		self.__settings.setKey("Layouts", "{0}_windowState".format(name), self.saveState())
		self.__settings.setKey("Layouts", "{0}_centralWidget".format(name), self.centralwidget.isVisible())
		self.__settings.setKey("Layouts", "{0}_activeLabel".format(name), self.__getLayoutsActiveLabel())
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreLayout(self, name, *args):
		"""
		This method is called when restoring a layout.

		:param name: Layout name. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Restoring layout '{0}'.".format(name))

		visibleComponents = [ "core.databaseBrowser" ]
		for component, profile in self.__componentsManager.components.items():
			profile.categorie == "ui" and component not in visibleComponents and self.__componentsManager.getInterface(component).ui and self.__componentsManager.getInterface(component).ui.hide()

		self.centralwidget.setVisible(self.__settings.getKey("Layouts", "{0}_centralWidget".format(name)).toBool())
		self.restoreState(self.__settings.getKey("Layouts", "{0}_windowState".format(name)).toByteArray())
		self.__settings._datas.restoreGeometryOnLayoutChange and self.restoreGeometry(self.__settings.getKey("Layouts", "{0}_geometry".format(name)).toByteArray())
		self.__setLayoutsActiveLabel(self.__settings.getKey("Layouts", "{0}_activeLabel".format(name)).toInt()[0])
		QApplication.focusWidget() and QApplication.focusWidget().clearFocus()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreStartupLayout(self):
		"""
		This method restores the startup layout.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Restoring startup layout.")

		if self.restoreLayout(UiConstants.startupLayout):
			not self.__settings._datas.restoreGeometryOnLayoutChange and self.restoreGeometry(self.__settings.getKey("Layouts", "{0}_geometry".format(UiConstants.startupLayout)).toByteArray())
			return True
		else:
			raise Exception, "{0} | Exception raised while restoring startup layout!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeStartupLayout(self):
		"""
		This method stores the startup layout.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing startup layout.")

		return self.storeLayout(UiConstants.startupLayout)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeLastBrowsedPath(self, path):
		"""
		This method is a wrapper method for storing the last browser path.

		:param path: Provided path. ( QString )
		:return: Provided path. ( QString )
		"""

		path = str(path)

		lastBrowserPath = os.path.normpath(os.path.join(os.path.isfile(path) and os.path.dirname(path) or path, ".."))
		LOGGER.debug("> Storing last browsed path: '%s'.", lastBrowserPath)

		self.__lastBrowsedPath = lastBrowserPath

		return path

#***********************************************************************************************
#***	Overall definitions..
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiStandaloneSystemExitExceptionHandler, False, OSError)
def _run(engine, paths, components=None):
	"""
	This definition is called when **Umbra** starts.

	:param engine: Engine. ( QObject )
	:param paths: Components paths. ( QString )
	:param components: Mandatory components names. ( QString )
	:return: Definition success. ( Boolean )
	"""

	# Command line parameters handling.
	RuntimeGlobals.parameters, RuntimeGlobals.args = _getCommandLineParameters(sys.argv)

	if RuntimeGlobals.parameters.about:
		for line in _getHeaderMessage():
			sys.stdout.write("{0}\n".format(line))
		foundations.common.exit(1, LOGGER, [])

	# Redirecting standard output and error messages.
	sys.stdout = core.StandardMessageHook(LOGGER)
	sys.stderr = core.StandardMessageHook(LOGGER)

	# Setting application verbose level.
	LOGGER.setLevel(logging.DEBUG)

	# Setting user application datas directory.
	if RuntimeGlobals.parameters.userApplicationDatasDirectory:
		RuntimeGlobals.userApplicationDatasDirectory = RuntimeGlobals.parameters.userApplicationDatasDirectory
	else:
		RuntimeGlobals.userApplicationDatasDirectory = foundations.common.getUserApplicationDatasDirectory()

	if not _setUserApplicationDatasDirectory(RuntimeGlobals.userApplicationDatasDirectory):
		raise OSError, "'{0}' user Application datas directory is not available, {1} will now close!".format(RuntimeGlobals.userApplicationDatasDirectory, Constants.applicationName)

	LOGGER.debug("> Application python interpreter: '{0}'".format(sys.executable))
	LOGGER.debug("> Application startup location: '{0}'".format(os.getcwd()))
	LOGGER.debug("> Session user Application datas directory: '{0}'".format(RuntimeGlobals.userApplicationDatasDirectory))

	# Getting the logging file path.
	RuntimeGlobals.loggingFile = os.path.join(RuntimeGlobals.userApplicationDatasDirectory, Constants.loggingDirectory, Constants.loggingFile)

	try:
		os.path.exists(RuntimeGlobals.loggingFile) and os.remove(RuntimeGlobals.loggingFile)
	except:
		raise OSError, "{0} Logging file is currently locked by another process, {1} will now close!".format(RuntimeGlobals.loggingFile, Constants.applicationName)

	try:
		RuntimeGlobals.loggingFileHandler = logging.FileHandler(RuntimeGlobals.loggingFile)
		RuntimeGlobals.loggingFileHandler.setFormatter(RuntimeGlobals.loggingFormatters[Constants.loggingDefaultFormatter])
		LOGGER.addHandler(RuntimeGlobals.loggingFileHandler)
	except:
		raise OSError, "{0} Logging file is not available, {1} will now close!".format(RuntimeGlobals.loggingFile, Constants.applicationName)

	# Retrieving Framework verbose level from settings file.
	LOGGER.debug("> Initializing {0}!".format(Constants.applicationName))
	RuntimeGlobals.settingsFile = os.path.join(RuntimeGlobals.userApplicationDatasDirectory, Constants.settingsDirectory, Constants.settingsFile)

	RuntimeGlobals.settings = Preferences(RuntimeGlobals.settingsFile)

	LOGGER.debug("> Retrieving default layouts.")
	RuntimeGlobals.settings.setDefaultLayouts()

	os.path.exists(RuntimeGlobals.settingsFile) or RuntimeGlobals.settings.setDefaultPreferences()

	LOGGER.debug("> Retrieving stored verbose level.")
	RuntimeGlobals.verbosityLevel = RuntimeGlobals.parameters.verbosityLevel and RuntimeGlobals.parameters.verbosityLevel or RuntimeGlobals.settings.getKey("Settings", "verbosityLevel").toInt()[0]
	LOGGER.debug("> Setting logger verbosity level to: '{0}'.".format(RuntimeGlobals.verbosityLevel))
	core.setVerbosityLevel(RuntimeGlobals.verbosityLevel)

	LOGGER.debug("> Retrieving stored logging formatter.")
	loggingFormatter = RuntimeGlobals.parameters.loggingFormater and RuntimeGlobals.parameters.loggingFormater or str(RuntimeGlobals.settings.getKey("Settings", "loggingFormatter").toString())
	loggingFormatter = loggingFormatter in RuntimeGlobals.loggingFormatters.keys() and loggingFormatter or None
	RuntimeGlobals.loggingActiveFormatter = loggingFormatter and loggingFormatter or Constants.loggingDefaultFormatter
	LOGGER.debug("> Setting logging formatter: '{0}'.".format(RuntimeGlobals.loggingActiveFormatter))
	for handler in (RuntimeGlobals.loggingConsoleHandler, RuntimeGlobals.loggingFileHandler):
		handler and handler.setFormatter(RuntimeGlobals.loggingFormatters[RuntimeGlobals.loggingActiveFormatter])

	# Starting the session handler.
	RuntimeGlobals.loggingSessionHandlerStream = StreamObject()
	RuntimeGlobals.loggingSessionHandler = logging.StreamHandler(RuntimeGlobals.loggingSessionHandlerStream)
	RuntimeGlobals.loggingSessionHandler.setFormatter(RuntimeGlobals.loggingFormatters[RuntimeGlobals.loggingActiveFormatter])
	LOGGER.addHandler(RuntimeGlobals.loggingSessionHandler)

	LOGGER.info(Constants.loggingSeparators)
	for line in _getHeaderMessage():
		LOGGER.info(line)
	LOGGER.info("{0} | Session started at: {1}".format(Constants.applicationName, time.strftime('%X - %x')))
	LOGGER.info(Constants.loggingSeparators)
	LOGGER.info("{0} | Starting Interface!".format(Constants.applicationName))

	RuntimeGlobals.application = QApplication(sys.argv)

	# Initializing splashscreen.
	if RuntimeGlobals.parameters.hideSplashScreen:
		LOGGER.debug("> SplashScreen skipped by 'hideSplashScreen' command line parameter.")
	else:
		LOGGER.debug("> Initializing splashscreen.")

		RuntimeGlobals.splashscreenImage = QPixmap(umbra.ui.common.getResourcePath(UiConstants.splashScreenImage))
		RuntimeGlobals.splashscreen = Delayed_QSplashScreen(RuntimeGlobals.splashscreenImage)
		RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Initializing {0}.".format(Constants.applicationName, Constants.releaseVersion), textColor=Qt.white)
		RuntimeGlobals.splashscreen.show()

	RuntimeGlobals.ui = engine(paths, components)
	RuntimeGlobals.ui.show()
	RuntimeGlobals.ui.raise_()

	return sys.exit(RuntimeGlobals.application.exec_())

@core.executionTrace
def _exit():
	"""
	This definition is called when **Umbra** closes.
	"""

	LOGGER.info("{0} | Closing interface! ".format(Constants.applicationName))
	LOGGER.info(Constants.loggingSeparators)
	LOGGER.info("{0} | Session ended at: {1}".format(Constants.applicationName, time.strftime('%X - %x')))
	LOGGER.info(Constants.loggingSeparators)

	foundations.common.removeLoggingHandler(LOGGER, RuntimeGlobals.loggingConsoleHandler)

	QApplication.exit()

@core.executionTrace
def _getHeaderMessage():
	"""
	This definition builds the header message.

	:return: Header message ( Tuple )
	"""

	message = ("{0} | Copyright ( C ) 2008 - 2011 Thomas Mansencal - thomas.mansencal@gmail.com".format(Constants.applicationName),
				"{0} | This software is released under terms of GNU GPL V3 license.".format(Constants.applicationName),
				"{0} | http://www.gnu.org/licenses/ ".format(Constants.applicationName),
				"{0} | Version: {1}".format(Constants.applicationName, Constants.releaseVersion))
	return message

@core.executionTrace
def _getCommandLineParameters(argv):
	"""
	This definition process command line parameters.

	:param argv: Command line parameters. ( String )
	:return: Settings, arguments ( Parser instance )
	"""

	argv = argv or sys.argv[1:]

	parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter (indent_increment=2, max_help_position=8, width=128, short_first=1), add_help_option=None)

	parser.add_option("-h", "--help", action="help", help="'Display this help message and exit.'")
	parser.add_option("-a", "--about", action="store_true", default=False, dest="about", help="'Display Application about message.'")
	parser.add_option("-v", "--verbose", action="store", type="int", dest="verbosityLevel", help="'Application verbosity levels: 0 = Critical | 1 = Error | 2 = Warning | 3 = Info | 4 = Debug.'")
	parser.add_option("-f", "--loggingFormatter", action="store", type="string", dest="loggingFormater", help="'Application logging formatter: '{0}'.'".format(", ".join(sorted(RuntimeGlobals.loggingFormatters.keys()))))
	parser.add_option("-u", "--userApplicationDatasDirectory", action="store", type="string", dest="userApplicationDatasDirectory", help="'User Application datas directory'.")

	parser.add_option("-s", "--hideSplashScreen", action="store_true", default=False, dest="hideSplashScreen", help="'Hide splashscreen'.")

	parameters, args = parser.parse_args(argv)

	return parameters, args

@core.executionTrace
@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiStandaloneSystemExitExceptionHandler, False, OSError)
def _setUserApplicationDatasDirectory(path):
	"""
	This definition sets the Application datas directory.

	:param path: Starting point for the directories tree creation. ( String )
	:return: Definition success. ( Boolean )
	"""

	userApplicationDatasDirectory = RuntimeGlobals.userApplicationDatasDirectory

	LOGGER.debug("> Current Application datas directory '{0}'.".format(userApplicationDatasDirectory))
	if io.setDirectory(userApplicationDatasDirectory):
		for directory in Constants.preferencesDirectories:
			if not io.setDirectory(os.path.join(userApplicationDatasDirectory, directory)):
				raise OSError, "'{0}' directory creation failed , {1} will now close!".format(os.path.join(userApplicationDatasDirectory, directory), Constants.applicationName)
		return True
	else:
		raise OSError, "'{0}' directory creation failed , {1} will now close!".format(userApplicationDatasDirectory, Constants.applicationName)

#***********************************************************************************************
#***	Launcher.
#***********************************************************************************************
if __name__ == "__main__":
	_run(Umbra, (os.path.join(umbra.__path__[0], Constants.factoryComponentsDirectory),), ("factory.scriptEditor", "factory.preferencesManager", "factory.componentsManagerUi"))
