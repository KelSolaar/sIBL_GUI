#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**sIBL_GUI.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| This module defines various classes, methods and definitions to run, maintain and exit the Application.
	| The main Application object is the :class:`sIBL_GUI` class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import logging
import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import sibl_gui.globals.constants
import sibl_gui.globals.uiConstants
import umbra.globals.constants
import umbra.globals.uiConstants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#***********************************************************************************************
#***	Dependencies globals manipulation.
#***********************************************************************************************
umbra.globals.constants.Constants.__dict__.update(sibl_gui.globals.constants.Constants.__dict__)
umbra.globals.uiConstants.UiConstants.__dict__.update(sibl_gui.globals.uiConstants.UiConstants.__dict__)

RuntimeGlobals.resourcesPaths.append(os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.resourcesDirectory))

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import umbra.engine
import umbra.ui.common
from umbra.ui.widgets.active_QLabel import Active_QLabel

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(umbra.globals.constants.Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class sIBL_GUI(umbra.engine.Umbra):
	"""
	This class is the main class of the **sibl_gui** package.
	"""

	def __init__(self, paths, components=None):
		"""
		This method initializes the class.

		:param paths: Components paths. ( QString )
		:param components: Mandatory components names. ( QString )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.engine.Umbra.__init__(self, paths, components)

		# --- Setting class attributes. ---

	def initializeToolBar(self):
		"""
		This method initializes Application toolBar.
		"""

		LOGGER.debug("> Initializing Application toolBar.")

		self.toolBar.setIconSize(QSize(umbra.globals.uiConstants.UiConstants.defaultToolbarIconSize, umbra.globals.uiConstants.UiConstants.defaultToolbarIconSize))

		LOGGER.debug("> Adding Application logo.")
		logoLabel = QLabel()
		logoLabel.setObjectName("Application_Logo_label")
		logoLabel.setPixmap(QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.logoImage)))
		self.toolBar.addWidget(logoLabel)

		spacer = QLabel()
		spacer.setObjectName("Logo_Spacer_label")
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolBar.addWidget(spacer)

		toolBarFont = QFont()
		toolBarFont.setPointSize(16)

		LOGGER.debug("> Adding Active_QLabels.")

		self.__libraryActiveLabel = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.libraryIcon)),
													QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.libraryHoverIcon)),
													QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.libraryActiveIcon)), True)
		self.__libraryActiveLabel.setObjectName("Library_activeLabel")
		self.toolBar.addWidget(self.__libraryActiveLabel)

		self.__inspectActiveLabel = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.inspectIcon)),
														QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.inspectHoverIcon)),
														QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.inspectActiveIcon)), True)
		self.__inspectActiveLabel.setObjectName("Inspect_activeLabel")
		self.toolBar.addWidget(self.__inspectActiveLabel)

		self.__exportActiveLabel = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.exportIcon)),
												QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.exportHoverIcon)),
												QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.exportActiveIcon)), True)
		self.__exportActiveLabel.setObjectName("Export_activeLabel")
		self.toolBar.addWidget(self.__exportActiveLabel)

		self.__preferencesActiveLabel = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.preferencesIcon)),
													QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.preferencesHoverIcon)),
													QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.preferencesActiveIcon)), True)
		self.__preferencesActiveLabel.setObjectName("Preferences_activeLabel")
		self.toolBar.addWidget(self.__preferencesActiveLabel)

		self.layoutsActiveLabels = (umbra.ui.common.LayoutActiveLabel(name="Library", object_=self.__libraryActiveLabel, layout="setsCentric", shortcut=Qt.Key_7),
									umbra.ui.common.LayoutActiveLabel(name="Inspect", object_=self.__inspectActiveLabel, layout="inspectCentric", shortcut=Qt.Key_8),
									umbra.ui.common.LayoutActiveLabel(name="Export", object_=self.__exportActiveLabel, layout="templatesCentric", shortcut=Qt.Key_9),
									umbra.ui.common.LayoutActiveLabel(name="Preferences", object_=self.__preferencesActiveLabel, layout="preferencesCentric", shortcut=Qt.Key_0))

		# Signals / Slots.
		for layoutActiveLabel in self.layoutsActiveLabels:
			layoutActiveLabel.object_.clicked.connect(functools.partial(self.layoutActiveLabel__clicked, layoutActiveLabel.layout))

		LOGGER.debug("> Adding Central Widget button.")
		centralWidgetButton = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.centralWidgetIcon)),
											QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.centralWidgetHoverIcon)),
											QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.centralWidgetActiveIcon)))
		centralWidgetButton.setObjectName("Central_Widget_activeLabel")
		self.toolBar.addWidget(centralWidgetButton)

		centralWidgetButton.clicked.connect(self.centralWidgetButton__clicked)

		LOGGER.debug("> Adding layout button.")
		layoutButton = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.layoutIcon)),
									QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.layoutHoverIcon)),
									QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.layoutActiveIcon)), parent=self)
		layoutButton.setObjectName("Layout_activeLabel")
		self.toolBar.addWidget(layoutButton)

		self.layoutMenu = QMenu("Layout", layoutButton)

		userLayouts = (("1", Qt.Key_1, "one"), ("2", Qt.Key_2, "two"), ("3", Qt.Key_3, "three"), ("4", Qt.Key_4, "four"), ("5", Qt.Key_5, "five"))

		for layout in userLayouts:
			action = QAction("Restore layout {0}".format(layout[0]), self)
			action.setShortcut(QKeySequence(layout[1]))
			self.layoutMenu.addAction(action)

			# Signals / Slots.
			action.triggered.connect(functools.partial(self.restoreLayout, layout[2]))

		self.layoutMenu.addSeparator()

		for layout in userLayouts:
			action = QAction("Store layout {0}".format(layout[0]), self)
			action.setShortcut(QKeySequence(Qt.CTRL + layout[1]))
			self.layoutMenu.addAction(action)

			# Signals / Slots.
			action.triggered.connect(functools.partial(self.storeLayout, layout[2]))

		layoutButton.setMenu(self.layoutMenu)

		LOGGER.debug("> Adding miscellaneous button.")
		miscellaneousButton = Active_QLabel(QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.miscellaneousIcon)),
											QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.miscellaneousHoverIcon)),
											QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.miscellaneousActiveIcon)), parent=self)
		miscellaneousButton.setObjectName("Miscellaneous_activeLabel")
		self.toolBar.addWidget(miscellaneousButton)

		helpDisplayMiscAction = QAction("Help content ...", self)
		apiDisplayMiscAction = QAction("Api content ...", self)

		self.miscMenu = QMenu("Miscellaneous", miscellaneousButton)

		self.miscMenu.addAction(helpDisplayMiscAction)
		self.miscMenu.addAction(apiDisplayMiscAction)
		self.miscMenu.addSeparator()

		# Signals / Slots.
		helpDisplayMiscAction.triggered.connect(self.helpDisplayMiscAction__triggered)
		apiDisplayMiscAction.triggered.connect(self.apiDisplayMiscAction__triggered)

		miscellaneousButton.setMenu(self.miscMenu)

		spacer = QLabel()
		spacer.setObjectName("Closure_Spacer_activeLabel")
		spacer.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
		self.toolBar.addWidget(spacer)

	def centralWidgetButton__clicked(self):
		"""
		This method sets the **Central** Widget visibility.
		"""

		LOGGER.debug("> Central Widget button clicked!")

		if self.centralwidget.isVisible():
			self.centralwidget.hide()
		else:
			self.centralwidget.show()

# @core.executionTrace
def extendCommandLineParametersParser(parser):
	"""
	This definition returns the command line parameters parser.

	:param parser: Command line parameters parser. ( Parser )
	:return: Definition success. ( Boolean )
	"""

	parser.add_option("-t", "--deactivateWorkerThreads", action="store_true", default=False, dest="deactivateWorkerThreads", help="'Deactivate worker threads'.")
	parser.add_option("-d", "--databaseDirectory", action="store", type="string", dest="databaseDirectory", help="'Database directory'.")
	parser.add_option("-r", "--databaseReadOnly", action="store_true", default=False, dest="databaseReadOnly", help="'Database read only'.")
	parser.add_option("-o", "--loaderScriptsOutputDirectory", action="store", type="string", dest="loaderScriptsOutputDirectory", help="'Loader Scripts output directory'.")

	return True

#***********************************************************************************************
#***	Launcher.
#***********************************************************************************************
if __name__ == "__main__":
	commandLineParametersParser = umbra.engine.getCommandLineParametersParser()
	extendCommandLineParametersParser(commandLineParametersParser)
	umbra.engine._run(sIBL_GUI, commandLineParametersParser.parse_args(sys.argv), (os.path.join(umbra.__path__[0], umbra.globals.constants.Constants.factoryComponentsDirectory),
					os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.coreComponentsDirectory),
					os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.addonsComponentsDirectory)))

#***********************************************************************************************
#***	Path manipulations.
#***********************************************************************************************
#def _setApplicationPackageDirectory():
#	"""
#	This definition sets the Application package directory in the path.
#
#	:return: Definition success. ( Boolean )
#	"""
#
#	applicationPackageDirectory = os.path.normpath(os.path.join(sys.path[0], "../"))
#	applicationPackageDirectory not in sys.path and sys.path.append(applicationPackageDirectory)
#	return True
#
#_setApplicationPackageDirectory()

#***********************************************************************************************
#***	Dependencies globals manipulation.
#***********************************************************************************************
#import foundations.globals.constants
#import manager.globals.constants
#from umbra.globals.constants import Constants
#
#def _overrideDependenciesGlobals():
#	"""
#	This definition overrides dependencies globals.
#
#	:return: Definition success. ( Boolean )
#	"""
#
#	foundations.globals.constants.Constants.logger = manager.globals.constants.Constants.logger = Constants.logger
#	foundations.globals.constants.Constants.applicationDirectory = manager.globals.constants.Constants.applicationDirectory = Constants.applicationDirectory
#	return True
#
#_overrideDependenciesGlobals()

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
#import foundations.common
#import foundations.core as core
#import foundations.exceptions
#import foundations.io as io
#import umbra.ui.common
#from foundations.streamObject import StreamObject
#from manager.componentsManager import Manager
#from umbra.globals.runtimeGlobals import RuntimeGlobals
#from umbra.globals.uiConstants import UiConstants
#from umbra.ui.widgets.active_QLabel import Active_QLabel
#from umbra.ui.widgets.delayed_QSplashScreen import Delayed_QSplashScreen

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
#__author__ = "Thomas Mansencal"
#__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
#__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
#__maintainer__ = "Thomas Mansencal"
#__email__ = "thomas.mansencal@gmail.com"
#__status__ = "Production"
#
#LOGGER = logging.getLogger(Constants.logger)
#
## Starting the console handler.
#if not hasattr(sys, "frozen") or not (platform.system() == "Windows" or platform.system() == "Microsoft"):
#	RuntimeGlobals.loggingConsoleHandler = logging.StreamHandler(sys.__stdout__)
#	RuntimeGlobals.loggingConsoleHandler.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
#	LOGGER.addHandler(RuntimeGlobals.loggingConsoleHandler)
#
## Defining logging formatters.
#RuntimeGlobals.loggingFormatters = {"Default" :core.LOGGING_DEFAULT_FORMATTER,
#									"Extended" : core.LOGGING_EXTENDED_FORMATTER,
#									"Standard" : core.LOGGING_STANDARD_FORMATTER}
#
#class Ui_Setup():
#	"""
#	This class defines the Application ui setup methods.
#	"""
#
#	pass
#
#class Ui_Type():
#	"""
#	This class defines the Application ui type base class ( `QMainWindow <http://doc.qt.nokia.com/4.7/qmainwindow.html>`_ ).
#	"""
#
#	pass
#
#RuntimeGlobals.uiFile = umbra.ui.common.getResourcePath(UiConstants.uiFile)
#if os.path.exists(RuntimeGlobals.uiFile):
#	Ui_Setup, Ui_Type = uic.loadUiType(RuntimeGlobals.uiFile)
#else:
#	umbra.ui.common.uiStandaloneSystemExitExceptionHandler(OSError("'{0}' ui file is not available, {1} will now close!".format(UiConstants.uiFile, Constants.applicationName)), Constants.applicationName)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
#class Preferences():
#	"""
#	| This class provides methods to manipulate Application preferences / settings.
#	| Those are stored and retrieved using a `QSettings <http://doc.qt.nokia.com/4.7/qsettings.html>`_ class.
#	"""
#
#	@core.executionTrace
#	def __init__(self, preferencesFile=None):
#		"""
#		This method initializes the class.
#
#		:param preferencesFile: Current preferences file path. ( String )
#		"""
#
#		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))
#
#		# --- Setting class attributes. ---
#		self.__preferencesFile = None
#		self.__preferencesFile = preferencesFile
#
#		self.__settings = QSettings(self.preferencesFile, QSettings.IniFormat)
#
#		# --- Initializing preferences. ---
#		self.__getDefaultLayoutsSettings()
#
#	#***********************************************************************************************
#	#***	Attributes properties.
#	#***********************************************************************************************
#	@property
#	def preferencesFile(self):
#		"""
#		This method is the property for **self.__preferencesFile** attribute.
#
#		:return: self.__preferencesFile. ( String )
#		"""
#
#		return self.__preferencesFile
#
#	@preferencesFile.setter
#	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
#	def preferencesFile(self, value):
#		"""
#		This method is the setter method for **self.__preferencesFile** attribute.
#
#		:param value: Attribute value. ( String )
#		"""
#
#		if value:
#			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("preferencesFile", value)
#			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("preferencesFile", value)
#		self.__preferencesFile = value
#
#	@preferencesFile.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def preferencesFile(self):
#		"""
#		This method is the deleter method for **self.__preferencesFile** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("preferencesFile"))
#
#	@property
#	def settings(self):
#		"""
#		This method is the property for **self.__settings** attribute.
#
#		:return: self.__settings. ( QSettings )
#		"""
#
#		return self.__settings
#
#	@settings.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def settings(self, value):
#		"""
#		This method is the setter method for **self.__settings** attribute.
#
#		:param value: Attribute value. ( QSettings )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))
#
#	@settings.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def settings(self):
#		"""
#		This method is the deleter method for **self.__settings** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))
#
#	@property
#	def defaultLayoutsSettings(self):
#		"""
#		This method is the property for **self.__defaultLayoutsSettings** attribute.
#
#		:return: self.__defaultLayoutsSettings. ( QSettings )
#		"""
#
#		return self.__defaultLayoutsSettings
#
#	@defaultLayoutsSettings.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def defaultLayoutsSettings(self, value):
#		"""
#		This method is the setter method for **self.__defaultLayoutsSettings** attribute.
#
#		:param value: Attribute value. ( QSettings )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultLayoutsSettings"))
#
#	@defaultLayoutsSettings.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def defaultLayoutsSettings(self):
#		"""
#		This method is the deleter method for **self.__defaultLayoutsSettings** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultLayoutsSettings"))
#
#	#***********************************************************************************************
#	#***	Class methods.
#	#***********************************************************************************************
#	@core.executionTrace
#	def setKey(self, section, key, value):
#		"""
#		This method stores provided key in settings file.
#
#		:param section: Current section to save the key into. ( String )
#		:param key: Current key to save. ( String )
#		:param value: Current key value to save. ( Object )
#		"""
#
#		LOGGER.debug("> Saving '{0}' in '{1}' section with value: '{2}' in settings file.".format(key, section, value))
#
#		self.__settings.beginGroup(section)
#		self.__settings.setValue(key , QVariant(value))
#		self.__settings.endGroup()
#
#	@core.executionTrace
#	def getKey(self, section, key):
#		"""
#		This method gets key value from settings file.
#
#		:param section: Current section to retrieve key from. ( String )
#		:param key: Current key to retrieve. ( String )
#		:return: Current key value. ( Object )
#		"""
#
#		LOGGER.debug("> Retrieving '{0}' in '{1}' section.".format(key, section))
#
#		self.__settings.beginGroup(section)
#		value = self.__settings.value(key)
#		LOGGER.debug("> Key value: '{0}'.".format(value))
#		self.__settings.endGroup()
#
#		return value
#
#	@core.executionTrace
#	def __getDefaultLayoutsSettings(self):
#		"""
#		This method gets the default layouts settings.
#		"""
#
#		LOGGER.debug("> Accessing '{0}' layouts settings file!".format(UiConstants.layoutsFile))
#		self.__defaultLayoutsSettings = QSettings(umbra.ui.common.getResourcePath(UiConstants.layoutsFile), QSettings.IniFormat)
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def setDefaultPreferences(self):
#		"""
#		This method defines the default settings file content.
#		:return: Method success. ( Boolean )
#		"""
#
#		LOGGER.debug("> Initializing default settings!")
#
#		self.__settings.beginGroup("Settings")
#		self.__settings.setValue("verbosityLevel", QVariant("3"))
#		self.__settings.setValue("restoreGeometryOnLayoutChange", Qt.Unchecked)
#		self.__settings.setValue("deactivatedComponents", QVariant(""))
#		self.__settings.endGroup()
#		self.__settings.beginGroup("Layouts")
#		self.__settings.setValue("startupCentric_geometry", self.__defaultLayoutsSettings.value("startupCentric/geometry"))
#		self.__settings.setValue("startupCentric_windowState", self.__defaultLayoutsSettings.value("startupCentric/windowState"))
#		self.__settings.setValue("startupCentric_centralWidget", self.__defaultLayoutsSettings.value("startupCentric/centralWidget"))
#		self.__settings.setValue("startupCentric_activeLabel", self.__defaultLayoutsSettings.value("startupCentric/activeLabel"))
#		self.__settings.setValue("setsCentric_geometry", self.__defaultLayoutsSettings.value("setsCentric/geometry"))
#		self.__settings.setValue("setsCentric_windowState", self.__defaultLayoutsSettings.value("setsCentric/windowState"))
#		self.__settings.setValue("setsCentric_centralWidget", self.__defaultLayoutsSettings.value("setsCentric/centralWidget"))
#		self.__settings.setValue("setsCentric_activeLabel", self.__defaultLayoutsSettings.value("setsCentric/activeLabel"))
#		self.__settings.setValue("inspectCentric_geometry", self.__defaultLayoutsSettings.value("inspectCentric/geometry"))
#		self.__settings.setValue("inspectCentric_windowState", self.__defaultLayoutsSettings.value("inspectCentric/windowState"))
#		self.__settings.setValue("inspectCentric_centralWidget", self.__defaultLayoutsSettings.value("inspectCentric/centralWidget"))
#		self.__settings.setValue("inspectCentric_activeLabel", self.__defaultLayoutsSettings.value("inspectCentric/activeLabel"))
#		self.__settings.setValue("templatesCentric_geometry", self.__defaultLayoutsSettings.value("templatesCentric/geometry"))
#		self.__settings.setValue("templatesCentric_windowState", self.__defaultLayoutsSettings.value("templatesCentric/windowState"))
#		self.__settings.setValue("templatesCentric_centralWidget", self.__defaultLayoutsSettings.value("templatesCentric/centralWidget"))
#		self.__settings.setValue("templatesCentric_activeLabel", self.__defaultLayoutsSettings.value("templatesCentric/activeLabel"))
#		self.__settings.setValue("preferencesCentric_geometry", self.__defaultLayoutsSettings.value("preferencesCentric/geometry"))
#		self.__settings.setValue("preferencesCentric_windowState", self.__defaultLayoutsSettings.value("preferencesCentric/windowState"))
#		self.__settings.setValue("preferencesCentric_centralWidget", self.__defaultLayoutsSettings.value("preferencesCentric/centralWidget"))
#		self.__settings.setValue("preferencesCentric_activeLabel", self.__defaultLayoutsSettings.value("preferencesCentric/activeLabel"))
#		self.__settings.setValue("one_geometry", "")
#		self.__settings.setValue("one_windowState", "")
#		self.__settings.setValue("one_centralWidget", True)
#		self.__settings.setValue("one_activeLabel", "")
#		self.__settings.setValue("two_geometry", "")
#		self.__settings.setValue("two_windowState", "")
#		self.__settings.setValue("two_centralWidget", True)
#		self.__settings.setValue("two_activeLabel", "")
#		self.__settings.setValue("three_geometry", "")
#		self.__settings.setValue("three_windowState", "")
#		self.__settings.setValue("three_centralWidget", True)
#		self.__settings.setValue("three_activeLabel", "")
#		self.__settings.setValue("four_geometry", "")
#		self.__settings.setValue("four_windowState", "")
#		self.__settings.setValue("four_centralWidget", True)
#		self.__settings.setValue("four_activeLabel", "")
#		self.__settings.setValue("five_geometry", "")
#		self.__settings.setValue("five_windowState", "")
#		self.__settings.setValue("five_centralWidget", True)
#		self.__settings.setValue("five_activeLabel", "")
#		self.__settings.endGroup()
#		return True
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def setDefaultLayouts(self):
#		"""
#		This method sets the default layouts in the preferences file.
#
#		:return: Method success. ( Boolean )
#		"""
#
#		for layout in ("setsCentric", "inspectCentric", "templatesCentric", "preferencesCentric"):
#				for type in ("geometry", "windowState", "centralWidget", "activeLabel"):
#					LOGGER.debug("> Updating preferences file '{0}_{1}' layout attribute!".format(layout, type))
#					self.setKey("Layouts", "{0}_{1}".format(layout, type), self.__defaultLayoutsSettings.value("{0}/{1}".format(layout, type)))
#		return True
#
#class LayoutActiveLabel(core.Structure):
#	"""
#	This class represents a storage object for layout active labels attributes.
#	"""
#
#	@core.executionTrace
#	def __init__(self, **kwargs):
#		"""
#		This method initializes the class.
#
#		:param \*\*kwargs: name, object, layout, shortcut. ( Key / Value pairs )
#		"""
#
#		core.Structure.__init__(self, **kwargs)
#
#class sIBL_GUI(Ui_Type, Ui_Setup):
#	"""
#	This class is the main class of the Application.
#	"""
#
#	#***********************************************************************************************
#	#***	Initialization..
#	#***********************************************************************************************
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiSystemExitExceptionHandler, False, foundations.exceptions.ProgrammingError, Exception)
#	def __init__(self):
#		"""
#		This method initializes the class.
#		"""
#
#		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))
#
#		Ui_Type.__init__(self)
#		Ui_Setup.__init__(self)
#
#		self.setupUi(self)
#
#		self.closeEvent = self.__closeUi
#
#		# --- Setting class attributes. ---
#		self.__timer = None
#		self.__componentsManager = None
#		self.__coreComponentsManagerUi = None
#		self.__corePreferencesManager = None
#		self.__coreDb = None
#		self.__coreDatabaseBrowser = None
#		self.__coreCollectionsOutliner = None
#		self.__coreTemplatesOutliner = None
#		self.__coreInspector = None
#		self.__lastBrowsedPath = os.getcwd()
#		self.__userApplicationDatasDirectory = RuntimeGlobals.userApplicationDatasDirectory
#		self.__loggingSessionHandler = RuntimeGlobals.loggingSessionHandler
#		self.__loggingFileHandler = RuntimeGlobals.loggingFileHandler
#		self.__loggingConsoleHandler = RuntimeGlobals.loggingConsoleHandler
#		self.__loggingSessionHandlerStream = RuntimeGlobals.loggingSessionHandlerStream
#		self.__loggingActiveFormatter = RuntimeGlobals.loggingActiveFormatter
#		self.__settings = RuntimeGlobals.settings
#		self.__verbosityLevel = RuntimeGlobals.verbosityLevel
#		self.__parameters = RuntimeGlobals.parameters
#		self.__libraryActiveLabel = None
#		self.__inspectActiveLabel = None
#		self.__exportActiveLabel = None
#		self.__preferencesActiveLabel = None
#		self.layoutsActiveLabels = None
#		self.layoutMenu = None
#		self.miscMenu = None
#		self.__workerThreads = []
#
#		# --- Initializing timer. ---
#		self.__timer = QTimer(self)
#		self.__timer.start(Constants.defaultTimerCycle)
#
#		# --- Initializing application. ---
#		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Initializing interface.".format(self.__class__.__name__, Constants.releaseVersion), textColor=Qt.white, waitTime=0.25)
#
#		# Visual style initialization.
#		self.setVisualStyle()
#		umbra.ui.common.setWindowDefaultIcon(self)
#
#		# Setting window title and toolBar.
#		self.setWindowTitle("{0} - {1}".format(Constants.applicationName, Constants.releaseVersion))
#		self.initializeToolBar()
#
#		# --- Initializing Components Manager. ---
#		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Initializing Components manager.".format(self.__class__.__name__, Constants.releaseVersion), textColor=Qt.white, waitTime=0.25)
#
#		self.__componentsManager = Manager((os.path.join(os.getcwd(), Constants.coreComponentsDirectory), os.path.join(os.getcwd(), Constants.addonsComponentsDirectory), os.path.join(self.__userApplicationDatasDirectory, Constants.userComponentsDirectory)))
#		self.__componentsManager.registerComponents()
#
#		if not self.__componentsManager.components:
#			raise foundations.exceptions.ProgrammingError, "'{0}' Components Manager has no Components, {1} will now close!".format(self.__componentsManager, Constants.applicationName)
#
#		self.__componentsManager.instantiateComponents(self.__componentsInstantiationCallback)
#
#		# --- Activating mandatory Components. ---
#		for component in ("factory.componentsManagerUi", "factory.preferencesManager", "core.db", "core.collectionsOutliner", "core.databaseBrowser", "core.inspector", "core.templatesOutliner"):
#			profile = self.__componentsManager.components[component]
#			interface = self.__componentsManager.getInterface(component)
#			setattr(self, "_{0}__{1}".format(self.__class__.__name__, Manager.getComponentAttributeName(component)), interface)
#			RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, component), textColor=Qt.white)
#			interface.activate(self)
#			if profile.categorie == "default":
#				interface.initialize()
#			elif profile.categorie == "ui":
#				interface.addWidget()
#				interface.initializeUi()
#
#		# --- Activating others Components. ---
#		deactivatedComponents = self.__settings.getKey("Settings", "deactivatedComponents").toString().split(",")
#		for component in self.__componentsManager.getComponents():
#			if component in deactivatedComponents:
#				continue
#
#			profile = self.__componentsManager.components[component]
#			interface = self.__componentsManager.getInterface(component)
#			if interface.activated:
#				continue
#
#			RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, component), textColor=Qt.white)
#			interface.activate(self)
#			if profile.categorie == "default":
#				interface.initialize()
#			elif profile.categorie == "ui":
#				interface.addWidget()
#				interface.initializeUi()
#
#		# Hiding splashscreen.
#		LOGGER.debug("> Hiding splashscreen.")
#		if RuntimeGlobals.splashscreen:
#			RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Initialization done.".format(self.__class__.__name__, Constants.releaseVersion), textColor=Qt.white)
#			RuntimeGlobals.splashscreen.hide()
#
#		# --- Running onStartup components methods. ---
#		for component in self.__componentsManager.getComponents():
#			interface = self.__componentsManager.getInterface(component)
#			if interface.activated:
#				hasattr(interface, "onStartup") and interface.onStartup()
#
#		self.__setLayoutsActiveLabelsShortcuts()
#
#		self.restoreStartupLayout()
#
#	#***********************************************************************************************
#	#***	Attributes properties.
#	#***********************************************************************************************
#	@property
#	def timer(self):
#		"""
#		This method is the property for **self.__timer** attribute.
#
#		:return: self.__timer. ( QTimer )
#		"""
#
#		return self.__timer
#
#	@timer.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def timer(self, value):
#		"""
#		This method is the setter method for **self.__timer** attribute.
#
#		:param value: Attribute value. ( QTimer )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("timer"))
#
#	@timer.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def timer(self):
#		"""
#		This method is the deleter method for **self.__timer** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("timer"))
#
#	@property
#	def componentsManager(self):
#		"""
#		This method is the property for **self.__componentsManager** attribute.
#
#		:return: self.__componentsManager. ( Object )
#		"""
#
#		return self.__componentsManager
#
#	@componentsManager.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def componentsManager(self, value):
#		"""
#		This method is the setter method for **self.__componentsManager** attribute.
#
#		:param value: Attribute value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("componentsManager"))
#
#	@componentsManager.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def componentsManager(self):
#		"""
#		This method is the deleter method for **self.__componentsManager** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("componentsManager"))
#
#	@property
#	def coreComponentsManagerUi(self):
#		"""
#		This method is the property for **self.__coreComponentsManagerUi** attribute.
#
#		:return: self.__coreComponentsManagerUi. ( Object )
#		"""
#
#		return self.__coreComponentsManagerUi
#
#	@coreComponentsManagerUi.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreComponentsManagerUi(self, value):
#		"""
#		This method is the setter method for **self.__coreComponentsManagerUi** attribute.
#
#		:param value: Attribute value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreComponentsManagerUi"))
#
#	@coreComponentsManagerUi.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreComponentsManagerUi(self):
#		"""
#		This method is the deleter method for **self.__coreComponentsManagerUi** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreComponentsManagerUi"))
#
#	@property
#	def corePreferencesManager(self):
#		"""
#		This method is the property for **self.__corePreferencesManager** attribute.
#
#		:return: self.__corePreferencesManager. ( Object )
#		"""
#
#		return self.__corePreferencesManager
#
#	@corePreferencesManager.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def corePreferencesManager(self, value):
#		"""
#		This method is the setter method for **self.__corePreferencesManager** attribute.
#
#		:param value: Attribute value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("corePreferencesManager"))
#
#	@corePreferencesManager.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def corePreferencesManager(self):
#		"""
#		This method is the deleter method for **self.__corePreferencesManager** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("corePreferencesManager"))
#
#	@property
#	def coreDb(self):
#		"""
#		This method is the property for **self.__coreDb** attribute.
#
#		:return: self.__coreDb. ( Object )
#		"""
#
#		return self.__coreDb
#
#	@coreDb.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreDb(self, value):
#		"""
#		This method is the setter method for **self.__coreDb** attribute.
#
#		:param value: Attribute value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDb"))
#
#	@coreDb.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreDb(self):
#		"""
#		This method is the deleter method for **self.__coreDb** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDb"))
#
#	@property
#	def coreCollectionsOutliner(self):
#		"""
#		This method is the property for **self.__coreCollectionsOutliner** attribute.
#
#		:return: self.__coreCollectionsOutliner. ( Object )
#		"""
#
#		return self.__coreCollectionsOutliner
#
#	@coreCollectionsOutliner.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreCollectionsOutliner(self, value):
#		"""
#		This method is the setter method for **self.__coreCollectionsOutliner** attribute.
#
#		:param value: Attribute value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreCollectionsOutliner"))
#
#	@coreCollectionsOutliner.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreCollectionsOutliner(self):
#		"""
#		This method is the deleter method for **self.__coreCollectionsOutliner** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreCollectionsOutliner"))
#
#	@property
#	def coreDatabaseBrowser(self):
#		"""
#		This method is the property for **self.__coreDatabaseBrowser** attribute.
#
#		:return: self.__coreDatabaseBrowser. ( Object )
#		"""
#
#		return self.__coreDatabaseBrowser
#
#	@coreDatabaseBrowser.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreDatabaseBrowser(self, value):
#		"""
#		This method is the setter method for **self.__coreDatabaseBrowser** attribute.
#
#		:param value: Attribute value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))
#
#	@coreDatabaseBrowser.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreDatabaseBrowser(self):
#		"""
#		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))
#
#	@property
#	def coreTemplatesOutliner(self):
#		"""
#		This method is the property for **self.__coreTemplatesOutliner** attribute.
#
#		:return: self.__coreTemplatesOutliner. ( Object )
#		"""
#
#		return self.__coreTemplatesOutliner
#
#	@coreTemplatesOutliner.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreTemplatesOutliner(self, value):
#		"""
#		This method is the setter method for **self.__coreTemplatesOutliner** attribute.
#
#		:param value: Attribute value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreTemplatesOutliner"))
#
#	@coreTemplatesOutliner.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def coreTemplatesOutliner(self):
#		"""
#		This method is the deleter method for **self.__coreTemplatesOutliner** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreTemplatesOutliner"))
#
#	@property
#	def lastBrowsedPath(self):
#		"""
#		This method is the property for **self.__lastBrowsedPath** attribute.
#
#		:return: self.__lastBrowsedPath. ( String )
#		"""
#
#		return self.__lastBrowsedPath
#
#	@lastBrowsedPath.setter
#	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
#	def lastBrowsedPath(self, value):
#		"""
#		This method is the setter method for **self.__lastBrowsedPath** attribute.
#
#		:param value: Attribute value. ( String )
#		"""
#
#		if value:
#			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("lastBrowsedPath", value)
#			assert os.path.exists(value), "'{0}' attribute: '{1}' directory doesn't exists!".format("lastBrowsedPath", value)
#		self.__lastBrowsedPath = value
#
#	@lastBrowsedPath.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def lastBrowsedPath(self):
#		"""
#		This method is the deleter method for **self.__lastBrowsedPath** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("lastBrowsedPath"))
#
#	@property
#	def userApplicationDatasDirectory(self):
#		"""
#		This method is the property for **self.__userApplicationDatasDirectory** attribute.
#
#		:return: self.__userApplicationDatasDirectory. ( String )
#		"""
#
#		return self.__userApplicationDatasDirectory
#
#	@userApplicationDatasDirectory.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def userApplicationDatasDirectory(self, value):
#		"""
#		This method is the setter method for **self.__userApplicationDatasDirectory** attribute.
#
#		:param value: Attribute value. ( String )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("userApplicationDatasDirectory"))
#
#	@userApplicationDatasDirectory.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def userApplicationDatasDirectory(self):
#		"""
#		This method is the deleter method for **self.__userApplicationDatasDirectory** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("userApplicationDatasDirectory"))
#
#	@property
#	def loggingSessionHandler(self):
#		"""
#		This method is the property for **self.__loggingSessionHandler** attribute.
#
#		:return: self.__loggingSessionHandler. ( Handler )
#		"""
#
#		return self.__loggingSessionHandler
#
#	@loggingSessionHandler.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def loggingSessionHandler(self, value):
#		"""
#		This method is the setter method for **self.__loggingSessionHandler** attribute.
#
#		:param value: Attribute value. ( Handler )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("loggingSessionHandler"))
#
#	@loggingSessionHandler.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def loggingSessionHandler(self):
#		"""
#		This method is the deleter method for **self.__loggingSessionHandler** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("loggingSessionHandler"))
#
#	@property
#	def loggingFileHandler(self):
#		"""
#		This method is the property for **self.__loggingFileHandler** attribute.
#
#		:return: self.__loggingFileHandler. ( Handler )
#		"""
#
#		return self.__loggingFileHandler
#
#	@loggingFileHandler.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def loggingFileHandler(self, value):
#		"""
#		This method is the setter method for **self.__loggingFileHandler** attribute.
#
#		:param value: Attribute value. ( Handler )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("loggingFileHandler"))
#
#	@loggingFileHandler.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def loggingFileHandler(self):
#		"""
#		This method is the deleter method for **self.__loggingFileHandler** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("loggingFileHandler"))
#
#	@property
#	def loggingConsoleHandler(self):
#		"""
#		This method is the property for **self.__loggingConsoleHandler** attribute.
#
#		:return: self.__loggingConsoleHandler. ( Handler )
#		"""
#
#		return self.__loggingConsoleHandler
#
#	@loggingConsoleHandler.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def loggingConsoleHandler(self, value):
#		"""
#		This method is the setter method for **self.__loggingConsoleHandler** attribute.
#
#		:param value: Attribute value. ( Handler )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("loggingConsoleHandler"))
#
#	@loggingConsoleHandler.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def loggingConsoleHandler(self):
#		"""
#		This method is the deleter method for **self.__loggingConsoleHandler** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("loggingConsoleHandler"))
#
#	@property
#	def loggingSessionHandlerStream(self):
#		"""
#		This method is the property for **self.__loggingSessionHandlerStream** attribute.
#
#		:return: self.__loggingSessionHandlerStream. ( StreamObject )
#		"""
#
#		return self.__loggingSessionHandlerStream
#
#	@loggingSessionHandlerStream.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def loggingSessionHandlerStream(self, value):
#		"""
#		This method is the setter method for **self.__loggingSessionHandlerStream** attribute.
#
#		:param value: Attribute value. ( StreamObject )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("loggingSessionHandlerStream"))
#
#	@loggingSessionHandlerStream.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def loggingSessionHandlerStream(self):
#		"""
#		This method is the deleter method for **self.__loggingSessionHandlerStream** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("loggingSessionHandlerStream"))
#
#	@property
#	def settings(self):
#		"""
#		This method is the property for **self.__settings** attribute.
#
#		:return: self.__settings. ( QSettings )
#		"""
#
#		return self.__settings
#
#	@settings.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def settings(self, value):
#		"""
#		This method is the setter method for **self.__settings** attribute.
#
#		:param value: Attribute value. ( QSettings )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))
#
#	@settings.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def settings(self):
#		"""
#		This method is the deleter method for **self.__settings** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))
#
#	@property
#	def verbosityLevel(self):
#		"""
#		This method is the property for **self.__verbosityLevel** attribute.
#
#		:return: self.__verbosityLevel. ( Integer )
#		"""
#
#		return self.__verbosityLevel
#
#	@verbosityLevel.setter
#	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
#	def verbosityLevel(self, value):
#		"""
#		This method is the setter method for **self.__verbosityLevel** attribute.
#
#		:param value: Attribute value. ( Integer )
#		"""
#
#		if value:
#			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("verbosityLevel", value)
#			assert value >= 0 and value <= 4, "'{0}' attribute: Value need to be exactly beetween 0 and 4!".format("verbosityLevel")
#		self.__verbosityLevel = value
#
#	@verbosityLevel.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def verbosityLevel(self):
#		"""
#		This method is the deleter method for **self.__verbosityLevel** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("verbosityLevel"))
#
#	@property
#	def parameters(self):
#		"""
#		This method is the property for **self.__parameters** attribute.
#
#		:return: self.__parameters. ( Object )
#		"""
#
#		return self.__parameters
#
#	@parameters.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def parameters(self, value):
#		"""
#		This method is the setter method for **self.__parameters** attribute.
#
#		:param value: Attribute value. ( Object )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("parameters"))
#
#	@parameters.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def parameters(self):
#		"""
#		This method is the deleter method for **self.__parameters** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("parameters"))
#
#	@property
#	def libraryActiveLabel (self):
#		"""
#		This method is the property for **self.__libraryActiveLabel** attribute.
#
#		:return: self.__libraryActiveLabel . ( Active_QLabel )
#		"""
#
#		return self.__libraryActiveLabel
#
#	@libraryActiveLabel .setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def libraryActiveLabel (self, value):
#		"""
#		This method is the setter method for **self.__libraryActiveLabel** attribute.
#
#		:param value: Attribute value. ( Active_QLabel )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("libraryActiveLabel "))
#
#	@libraryActiveLabel .deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def libraryActiveLabel (self):
#		"""
#		This method is the deleter method for **self.__libraryActiveLabel** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("libraryActiveLabel "))
#
#	@property
#	def inspectActiveLabel (self):
#		"""
#		This method is the property for **self.__inspectActiveLabel** attribute.
#
#		:return: self.__inspectActiveLabel . ( Active_QLabel )
#		"""
#
#		return self.__inspectActiveLabel
#
#	@inspectActiveLabel .setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def inspectActiveLabel (self, value):
#		"""
#		This method is the setter method for **self.__inspectActiveLabel** attribute.
#
#		:param value: Attribute value. ( Active_QLabel )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("inspectActiveLabel "))
#
#	@inspectActiveLabel .deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def inspectActiveLabel (self):
#		"""
#		This method is the deleter method for **self.__inspectActiveLabel** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("inspectActiveLabel "))
#
#	@property
#	def exportActiveLabel (self):
#		"""
#		This method is the property for **self.__exportActiveLabel** attribute.
#
#		:return: self.__exportActiveLabel . ( Active_QLabel )
#		"""
#
#		return self.__exportActiveLabel
#
#	@exportActiveLabel .setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def exportActiveLabel (self, value):
#		"""
#		This method is the setter method for **self.__exportActiveLabel** attribute.
#
#		:param value: Attribute value. ( Active_QLabel )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("exportActiveLabel "))
#
#	@exportActiveLabel .deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def exportActiveLabel (self):
#		"""
#		This method is the deleter method for **self.__exportActiveLabel** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("exportActiveLabel "))
#
#	@property
#	def preferencesActiveLabel (self):
#		"""
#		This method is the property for **self.__preferencesActiveLabel** attribute.
#
#		:return: self.__preferencesActiveLabel. ( Active_QLabel )
#		"""
#
#		return self.__preferencesActiveLabel
#
#	@preferencesActiveLabel .setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def preferencesActiveLabel (self, value):
#		"""
#		This method is the setter method for **self.__preferencesActiveLabel** attribute.
#
#		:param value: Attribute value. ( Active_QLabel )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("preferencesActiveLabel "))
#
#	@preferencesActiveLabel .deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def preferencesActiveLabel (self):
#		"""
#		This method is the deleter method for **self.__preferencesActiveLabel** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("preferencesActiveLabel "))
#
#	@property
#	def layoutsActiveLabels(self):
#		"""
#		This method is the property for **self.layoutsActiveLabels** attribute.
#
#		:return: self.layoutsActiveLabels. ( Tuple )
#		"""
#
#		return self.layoutsActiveLabels
#
#	@layoutsActiveLabels.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def layoutsActiveLabels(self, value):
#		"""
#		This method is the setter method for **self.layoutsActiveLabels** attribute.
#
#		:param value: Attribute value. ( Tuple )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("layoutsActiveLabels"))
#
#	@layoutsActiveLabels.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def layoutsActiveLabels(self):
#		"""
#		This method is the deleter method for **self.layoutsActiveLabels** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("layoutsActiveLabels"))
#
#	@property
#	def layoutMenu(self):
#		"""
#		This method is the property for **self.layoutMenu** attribute.
#
#		:return: self.layoutMenu. ( QMenu )
#		"""
#
#		return self.layoutMenu
#
#	@layoutMenu.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def layoutMenu(self, value):
#		"""
#		This method is the setter method for **self.layoutMenu** attribute.
#
#		:param value: Attribute value. ( QMenu )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("layoutMenu"))
#
#	@layoutMenu.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def layoutMenu(self):
#		"""
#		This method is the deleter method for **self.layoutMenu** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("layoutMenu"))
#
#	@property
#	def miscMenu(self):
#		"""
#		This method is the property for **self.miscMenu** attribute.
#
#		:return: self.miscMenu. ( QMenu )
#		"""
#
#		return self.miscMenu
#
#	@miscMenu.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def miscMenu(self, value):
#		"""
#		This method is the setter method for **self.miscMenu** attribute.
#
#		:param value: Attribute value. ( QMenu )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("miscMenu"))
#
#	@miscMenu.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def miscMenu(self):
#		"""
#		This method is the deleter method for **self.miscMenu** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("miscMenu"))
#
#	@property
#	def workerThreads(self):
#		"""
#		This method is the property for **self.__workerThreads** attribute.
#
#		:return: self.__workerThreads. ( List )
#		"""
#
#		return self.__workerThreads
#
#	@workerThreads.setter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def workerThreads(self, value):
#		"""
#		This method is the setter method for **self.__workerThreads** attribute.
#
#		:param value: Attribute value. ( List )
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("workerThreads"))
#
#	@workerThreads.deleter
#	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
#	def workerThreads(self):
#		"""
#		This method is the deleter method for **self.__workerThreads** attribute.
#		"""
#
#		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("workerThreads"))
#
#	#***********************************************************************************************
#	#***	Class methods.
#	#***********************************************************************************************
#	@core.executionTrace
#	def __closeUi(self, event):
#		"""
#		This method is called when close event is fired.
#
#		:param event: QEvent. ( QEvent )
#		"""
#
#		# --- Running onClose components methods. ---
#		for component in self.__componentsManager.getComponents():
#			interface = self.__componentsManager.getInterface(component)
#			if interface.activated:
#				hasattr(interface, "onClose") and interface.onClose()
#
#		# Storing current layout.
#		self.storeStartupLayout()
#		self.__settings.settings.sync()
#
#		# Stopping worker threads.
#		for workerThread in self.__workerThreads:
#			if not workerThread.isFinished():
#				LOGGER.debug("> Stopping worker thread: '{0}'.".format(workerThread))
#				workerThread.exit()
#
#		foundations.common.removeLoggingHandler(LOGGER, self.__loggingFileHandler)
#		foundations.common.removeLoggingHandler(LOGGER, self.__loggingSessionHandler)
#		# foundations.common.removeLoggingHandler(LOGGER, self.__loggingconsolehandler)
#
#		# Stopping the timer.
#		self.__timer.stop()
#		self.__timer = None
#
#		self.deleteLater()
#		event.accept()
#
#		_exit()
#
#	@core.executionTrace
#	def __componentsInstantiationCallback(self, profile):
#		"""
#		This method is a callback for the Components instantiation.
#
#		:param profile: Component Profile. ( Profile )
#		"""
#
#		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Instantiating {2} Component.".format(self.__class__.__name__, Constants.releaseVersion, profile.name), textColor=Qt.white)
#
#	@core.executionTrace
#	def initializeToolBar(self):
#		"""
#		This method initializes Application toolBar.
#		"""
#
#		LOGGER.debug("> Initializing Application toolBar.")
#
#		self.toolBar.setIconSize(QSize(UiConstants.defaultToolbarIconSize, UiConstants.defaultToolbarIconSize))
#
#		LOGGER.debug("> Adding Application logo.")
#		logoLabel = QLabel()
#		logoLabel.setObjectName("Application_Logo_label")
#		logoLabel.setPixmap(QPixmap(UiConstants.logoImage))
#		self.toolBar.addWidget(logoLabel)
#
#		spacer = QLabel()
#		spacer.setObjectName("Logo_Spacer_label")
#		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#		self.toolBar.addWidget(spacer)
#
#		toolBarFont = QFont()
#		toolBarFont.setPointSize(16)
#
#		LOGGER.debug("> Adding Active_QLabels.")
#
#		self.__libraryActiveLabel = Active_QLabel(QPixmap(UiConstants.libraryIcon), QPixmap(UiConstants.libraryHoverIcon), QPixmap(UiConstants.libraryActiveIcon), True)
#		self.__libraryActiveLabel.setObjectName("Library_activeLabel")
#		self.toolBar.addWidget(self.__libraryActiveLabel)
#
#		self.__inspectActiveLabel = Active_QLabel(QPixmap(UiConstants.inspectIcon), QPixmap(UiConstants.inspectHoverIcon), QPixmap(UiConstants.inspectActiveIcon), True)
#		self.__inspectActiveLabel.setObjectName("Inspect_activeLabel")
#		self.toolBar.addWidget(self.__inspectActiveLabel)
#
#		self.__exportActiveLabel = Active_QLabel(QPixmap(UiConstants.exportIcon), QPixmap(UiConstants.exportHoverIcon), QPixmap(UiConstants.exportActiveIcon), True)
#		self.__exportActiveLabel.setObjectName("Export_activeLabel")
#		self.toolBar.addWidget(self.__exportActiveLabel)
#
#		self.__preferencesActiveLabel = Active_QLabel(QPixmap(UiConstants.preferencesIcon), QPixmap(UiConstants.preferencesHoverIcon), QPixmap(UiConstants.preferencesActiveIcon), True)
#		self.__preferencesActiveLabel.setObjectName("Preferences_activeLabel")
#		self.toolBar.addWidget(self.__preferencesActiveLabel)
#
#		self.layoutsActiveLabels = (LayoutActiveLabel(name="Library", object_=self.__libraryActiveLabel, layout="setsCentric", shortcut=Qt.Key_7),
#									LayoutActiveLabel(name="Inspect", object_=self.__inspectActiveLabel, layout="inspectCentric", shortcut=Qt.Key_8),
#									LayoutActiveLabel(name="Export", object_=self.__exportActiveLabel, layout="templatesCentric", shortcut=Qt.Key_9),
#									LayoutActiveLabel(name="Preferences", object_=self.__preferencesActiveLabel, layout="preferencesCentric", shortcut=Qt.Key_0))
#
#		# Signals / Slots.
#		for layoutActiveLabel in self.layoutsActiveLabels:
#			layoutActiveLabel.object_.clicked.connect(functools.partial(self.layoutActiveLabel__clicked, layoutActiveLabel.layout))
#
#		LOGGER.debug("> Adding Central Widget button.")
#		centralWidgetButton = Active_QLabel(QPixmap(UiConstants.centralWidgetIcon), QPixmap(UiConstants.centralWidgetHoverIcon), QPixmap(UiConstants.centralWidgetActiveIcon))
#		centralWidgetButton.setObjectName("Central_Widget_activeLabel")
#		self.toolBar.addWidget(centralWidgetButton)
#
#		centralWidgetButton.clicked.connect(self.centralWidgetButton__clicked)
#
#		LOGGER.debug("> Adding layout button.")
#		layoutButton = Active_QLabel(QPixmap(UiConstants.layoutIcon), QPixmap(UiConstants.layoutHoverIcon), QPixmap(UiConstants.layoutActiveIcon), parent=self)
#		layoutButton.setObjectName("Layout_activeLabel")
#		self.toolBar.addWidget(layoutButton)
#
#		self.layoutMenu = QMenu("Layout", layoutButton)
#
#		userLayouts = (("1", Qt.Key_1, "one"), ("2", Qt.Key_2, "two"), ("3", Qt.Key_3, "three"), ("4", Qt.Key_4, "four"), ("5", Qt.Key_5, "five"))
#
#		for layout in userLayouts:
#			action = QAction("Restore layout {0}".format(layout[0]), self)
#			action.setShortcut(QKeySequence(layout[1]))
#			self.layoutMenu.addAction(action)
#
#			# Signals / Slots.
#			action.triggered.connect(functools.partial(self.restoreLayout, layout[2]))
#
#		self.layoutMenu.addSeparator()
#
#		for layout in userLayouts:
#			action = QAction("Store layout {0}".format(layout[0]), self)
#			action.setShortcut(QKeySequence(Qt.CTRL + layout[1]))
#			self.layoutMenu.addAction(action)
#
#			# Signals / Slots.
#			action.triggered.connect(functools.partial(self.storeLayout, layout[2]))
#
#		layoutButton.setMenu(self.layoutMenu)
#
#		LOGGER.debug("> Adding miscellaneous button.")
#		miscellaneousButton = Active_QLabel(QPixmap(UiConstants.miscellaneousIcon), QPixmap(UiConstants.miscellaneousHoverIcon), QPixmap(UiConstants.miscellaneousActiveIcon), parent=self)
#		miscellaneousButton.setObjectName("Miscellaneous_activeLabel")
#		self.toolBar.addWidget(miscellaneousButton)
#
#		helpDisplayMiscAction = QAction("Help content ...", self)
#		apiDisplayMiscAction = QAction("Api content ...", self)
#
#		self.miscMenu = QMenu("Miscellaneous", miscellaneousButton)
#
#		self.miscMenu.addAction(helpDisplayMiscAction)
#		self.miscMenu.addAction(apiDisplayMiscAction)
#		self.miscMenu.addSeparator()
#
#		# Signals / Slots.
#		helpDisplayMiscAction.triggered.connect(self.helpDisplayMiscAction__triggered)
#		apiDisplayMiscAction.triggered.connect(self.apiDisplayMiscAction__triggered)
#
#		miscellaneousButton.setMenu(self.miscMenu)
#
#		spacer = QLabel()
#		spacer.setObjectName("Closure_Spacer_activeLabel")
#		spacer.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
#		self.toolBar.addWidget(spacer)
#
#	@core.executionTrace
#	def __setLayoutsActiveLabelsShortcuts(self):
#		"""
#		This method sets the layouts **Active_QLabels** shortcuts.
#		"""
#
#		LOGGER.debug("> Setting layouts Active_QLabels shortcuts.")
#
#		for layoutActiveLabel in self.layoutsActiveLabels:
#			action = QAction(layoutActiveLabel.name, self)
#			action.setShortcut(QKeySequence(layoutActiveLabel.shortcut))
#			self.addAction(action)
#			action.triggered.connect(functools.partial(self.restoreLayout, layoutActiveLabel.layout))
#
#	@core.executionTrace
#	def __getLayoutsActiveLabel(self):
#		"""
#		This method returns the current layout **Active_QLabel** index.
#
#		:return: Layouts Active_QLabel index. ( Integer )
#		"""
#
#		LOGGER.debug("> Retrieving current layout Active_QLabel index.")
#
#		for index in range(len(self.layoutsActiveLabels)):
#			if self.layoutsActiveLabels[index].object_.isChecked():
#				LOGGER.debug("> Current layout Active_QLabel index: '{0}'.".format(index))
#				return index
#
#	@core.executionTrace
#	def __setLayoutsActiveLabel(self, index):
#		"""
#		This method sets the layouts **Active_QLabel**.
#
#		:param index: Layouts Active_QLabel. ( Integer )
#		"""
#
#		LOGGER.debug("> Setting layouts Active_QLabels states.")
#
#		for index_ in range(len(self.layoutsActiveLabels)):
#			self.layoutsActiveLabels[index_].object_.setChecked(index == index_ and True or False)
#
#	@core.executionTrace
#	def layoutActiveLabel__clicked(self, activeLabel):
#		"""
#		This method is triggered when an **Active_QLabel** is clicked.
#		"""
#
#		LOGGER.debug("> Clicked Active_QLabel: '{0}'.".format(activeLabel))
#
#		self.restoreLayout(activeLabel)
#		for layoutActivelabel in self.layoutsActiveLabels:
#			layoutActivelabel.layout is not activeLabel and layoutActivelabel.object_.setChecked(False)
#
#	@core.executionTrace
#	def centralWidgetButton__clicked(self):
#		"""
#		This method sets the **Central** Widget visibility.
#		"""
#
#		LOGGER.debug("> Central Widget button clicked!")
#
#		if self.centralwidget.isVisible():
#			self.centralwidget.hide()
#		else:
#			self.centralwidget.show()
#
#	@core.executionTrace
#	def helpDisplayMiscAction__triggered(self, checked):
#		"""
#		This method is triggered by **helpDisplayMiscAction** action.
#
#		:param checked: Checked state. ( Boolean )
#		"""
#
#		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.helpFile))
#		QDesktopServices.openUrl(QUrl(QString(UiConstants.helpFile)))
#
#	@core.executionTrace
#	def apiDisplayMiscAction__triggered(self, checked):
#		"""
#		This method is triggered by **apiDisplayMiscAction** action.
#
#		:param checked: Checked state. ( Boolean )
#		"""
#
#		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.apiFile))
#		QDesktopServices.openUrl(QUrl(QString(UiConstants.apiFile)))
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, OSError)
#	def setVisualStyle(self):
#		"""
#		This method sets the Application visual style.
#		"""
#
#		LOGGER.debug("> Setting Application visual style.")
#
#		if platform.system() == "Windows" or platform.system() == "Microsoft":
#			RuntimeGlobals.application.setStyle(UiConstants.windowsStyle)
#			styleSheetFile = io.File(UiConstants.windowsStylesheetFile)
#		elif platform.system() == "Darwin":
#			RuntimeGlobals.application.setStyle(UiConstants.darwinStyle)
#			styleSheetFile = io.File(UiConstants.darwinStylesheetFile)
#		elif platform.system() == "Linux":
#			RuntimeGlobals.application.setStyle(UiConstants.linuxStyle)
#			styleSheetFile = io.File(UiConstants.linuxStylesheetFile)
#
#		if os.path.exists(styleSheetFile.file):
#			LOGGER.debug("> Reading style sheet file: '{0}'.".format(styleSheetFile.file))
#			styleSheetFile.read()
#			RuntimeGlobals.application.setStyleSheet(QString("".join(styleSheetFile.content)))
#		else:
#			raise OSError, "{0} | '{1}' stylesheet file is not available, visual style will not be applied!".format(self.__class__.__name__, styleSheetFile.file)
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def storeLayout(self, name, *args):
#		"""
#		This method is called when storing a layout.
#
#		:param name: Layout name. ( String )
#		:param \*args: Arguments. ( \* )
#		:return: Method success. ( Boolean )
#		"""
#
#		LOGGER.debug("> Storing layout '{0}'.".format(name))
#
#		self.__settings.setKey("Layouts", "{0}_geometry".format(name), self.saveGeometry())
#		self.__settings.setKey("Layouts", "{0}_windowState".format(name), self.saveState())
#		self.__settings.setKey("Layouts", "{0}_centralWidget".format(name), self.centralwidget.isVisible())
#		self.__settings.setKey("Layouts", "{0}_activeLabel".format(name), self.__getLayoutsActiveLabel())
#		return True
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def restoreLayout(self, name, *args):
#		"""
#		This method is called when restoring a layout.
#
#		:param name: Layout name. ( String )
#		:param \*args: Arguments. ( \* )
#		:return: Method success. ( Boolean )
#		"""
#
#		LOGGER.debug("> Restoring layout '{0}'.".format(name))
#
#		visibleComponents = [ "core.databaseBrowser" ]
#		for component, profile in self.__componentsManager.components.items():
#			profile.categorie == "ui" and component not in visibleComponents and self.__componentsManager.getInterface(component).ui and self.__componentsManager.getInterface(component).ui.hide()
#
#		self.centralwidget.setVisible(self.__settings.getKey("Layouts", "{0}_centralWidget".format(name)).toBool())
#		self.restoreState(self.__settings.getKey("Layouts", "{0}_windowState".format(name)).toByteArray())
#		self.__corePreferencesManager.ui.Restore_Geometry_On_Layout_Change_checkBox.isChecked() and self.restoreGeometry(self.__settings.getKey("Layouts", "{0}_geometry".format(name)).toByteArray())
#		self.__setLayoutsActiveLabel(self.__settings.getKey("Layouts", "{0}_activeLabel".format(name)).toInt()[0])
#		QApplication.focusWidget() and QApplication.focusWidget().clearFocus()
#		return True
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def restoreStartupLayout(self):
#		"""
#		This method restores the startup layout.
#
#		:return: Method success. ( Boolean )
#		"""
#
#		LOGGER.debug("> Restoring startup layout.")
#
#		if self.restoreLayout(UiConstants.startupLayout):
#			not self.__corePreferencesManager.ui.Restore_Geometry_On_Layout_Change_checkBox.isChecked() and self.restoreGeometry(self.__settings.getKey("Layouts", "{0}_geometry".format(UiConstants.startupLayout)).toByteArray())
#			return True
#		else:
#			raise Exception, "{0} | Exception raised while restoring startup layout!".format(self.__class__.__name__)
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def storeStartupLayout(self):
#		"""
#		This method stores the startup layout.
#
#		:return: Method success. ( Boolean )
#		"""
#
#		LOGGER.debug("> Storing startup layout.")
#
#		return self.storeLayout(UiConstants.startupLayout)
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def storeLastBrowsedPath(self, path):
#		"""
#		This method is a wrapper method for storing the last browser path.
#
#		:param path: Provided path. ( QString )
#		:return: Provided path. ( QString )
#		"""
#
#		path = str(path)
#
#		lastBrowserPath = os.path.normpath(os.path.join(os.path.isfile(path) and os.path.dirname(path) or path, ".."))
#		LOGGER.debug("> Storing last browsed path: '%s'.", lastBrowserPath)
#
#		self.__lastBrowsedPath = lastBrowserPath
#
#		return path
#
##***********************************************************************************************
##***	Overall definitions..
##***********************************************************************************************
#@core.executionTrace
#@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiStandaloneSystemExitExceptionHandler, False, OSError)
#def _run():
#	"""
#	This definition is called when sIBL_GUI starts.
#	"""
#
#	# Command line parameters handling.
#	RuntimeGlobals.parameters,  RuntimeGlobals.arguments = _getCommandLineParameters(sys.argv)
#
#	if RuntimeGlobals.parameters.about:
#		for line in _getHeaderMessage():
#			sys.stdout.write("{0}\n".format(line))
#		foundations.common.exit(1, LOGGER, [])
#
#	# Redirecting standard output and error messages.
#	sys.stdout = core.StandardMessageHook(LOGGER)
#	sys.stderr = core.StandardMessageHook(LOGGER)
#
#	# Setting application verbose level.
#	LOGGER.setLevel(logging.DEBUG)
#
#	# Setting user application datas directory.
#	if RuntimeGlobals.parameters.userApplicationDatasDirectory:
#		RuntimeGlobals.userApplicationDatasDirectory = RuntimeGlobals.parameters.userApplicationDatasDirectory
#	else:
#		RuntimeGlobals.userApplicationDatasDirectory = foundations.common.getUserApplicationDatasDirectory()
#
#	if not _setUserApplicationDatasDirectory(RuntimeGlobals.userApplicationDatasDirectory):
#		raise OSError, "'{0}' user Application datas directory is not available, {1} will now close!".format(RuntimeGlobals.userApplicationDatasDirectory, Constants.applicationName)
#
#	LOGGER.debug("> Application python interpreter: '{0}'".format(sys.executable))
#	LOGGER.debug("> Application startup location: '{0}'".format(os.getcwd()))
#	LOGGER.debug("> Session user Application datas directory: '{0}'".format(RuntimeGlobals.userApplicationDatasDirectory))
#
#	# Getting the logging file path.
#	RuntimeGlobals.loggingFile = os.path.join(RuntimeGlobals.userApplicationDatasDirectory, Constants.loggingDirectory, Constants.loggingFile)
#
#	try:
#		os.path.exists(RuntimeGlobals.loggingFile) and os.remove(RuntimeGlobals.loggingFile)
#	except:
#		raise OSError, "{0} Logging file is currently locked by another process, {1} will now close!".format(RuntimeGlobals.loggingFile, Constants.applicationName)
#
#	try:
#		RuntimeGlobals.loggingFileHandler = logging.FileHandler(RuntimeGlobals.loggingFile)
#		RuntimeGlobals.loggingFileHandler.setFormatter(RuntimeGlobals.loggingFormatters[Constants.loggingDefaultFormatter])
#		LOGGER.addHandler(RuntimeGlobals.loggingFileHandler)
#	except:
#		raise OSError, "{0} Logging file is not available, {1} will now close!".format(RuntimeGlobals.loggingFile, Constants.applicationName)
#
#	# Retrieving Framework verbose level from settings file.
#	LOGGER.debug("> Initializing {0}!".format(Constants.applicationName))
#	RuntimeGlobals.settingsFile = os.path.join(RuntimeGlobals.userApplicationDatasDirectory, Constants.settingsDirectory, Constants.settingsFile)
#
#	RuntimeGlobals.settings = Preferences(RuntimeGlobals.settingsFile)
#
#	LOGGER.debug("> Retrieving default layouts.")
#	RuntimeGlobals.settings.setDefaultLayouts()
#
#	os.path.exists(RuntimeGlobals.settingsFile) or RuntimeGlobals.settings.setDefaultPreferences()
#
#	LOGGER.debug("> Retrieving stored verbose level.")
#	RuntimeGlobals.verbosityLevel = RuntimeGlobals.parameters.verbosityLevel and RuntimeGlobals.parameters.verbosityLevel or RuntimeGlobals.settings.getKey("Settings", "verbosityLevel").toInt()[0]
#	LOGGER.debug("> Setting logger verbosity level to: '{0}'.".format(RuntimeGlobals.verbosityLevel))
#	core.setVerbosityLevel(RuntimeGlobals.verbosityLevel)
#
#	LOGGER.debug("> Retrieving stored logging formatter.")
#	loggingFormatter = RuntimeGlobals.parameters.loggingFormater and RuntimeGlobals.parameters.loggingFormater or str(RuntimeGlobals.settings.getKey("Settings", "loggingFormatter").toString())
#	loggingFormatter = loggingFormatter in RuntimeGlobals.loggingFormatters.keys() and loggingFormatter or None
#	RuntimeGlobals.loggingActiveFormatter = loggingFormatter and loggingFormatter or Constants.loggingDefaultFormatter
#	LOGGER.debug("> Setting logging formatter: '{0}'.".format(RuntimeGlobals.loggingActiveFormatter))
#	for handler in (RuntimeGlobals.loggingConsoleHandler, RuntimeGlobals.loggingFileHandler):
#		handler and handler.setFormatter(RuntimeGlobals.loggingFormatters[RuntimeGlobals.loggingActiveFormatter])
#
#	# Starting the session handler.
#	RuntimeGlobals.loggingSessionHandlerStream = StreamObject()
#	RuntimeGlobals.loggingSessionHandler = logging.StreamHandler(RuntimeGlobals.loggingSessionHandlerStream)
#	RuntimeGlobals.loggingSessionHandler.setFormatter(RuntimeGlobals.loggingFormatters[RuntimeGlobals.loggingActiveFormatter])
#	LOGGER.addHandler(RuntimeGlobals.loggingSessionHandler)
#
#	LOGGER.info(Constants.loggingSeparators)
#	for line in _getHeaderMessage():
#		LOGGER.info(line)
#	LOGGER.info("{0} | Session started at: {1}".format(Constants.applicationName, time.strftime('%X - %x')))
#	LOGGER.info(Constants.loggingSeparators)
#	LOGGER.info("{0} | Starting Interface!".format(Constants.applicationName))
#
#	RuntimeGlobals.application = QApplication(sys.argv)
#
#	# Initializing splashscreen.
#	if RuntimeGlobals.parameters.hideSplashScreen:
#		LOGGER.debug("> SplashScreen skipped by 'hideSplashScreen' command line parameter.")
#	else:
#		LOGGER.debug("> Initializing splashscreen.")
#
#		RuntimeGlobals.splashscreenImage = QPixmap(UiConstants.splashScreenImage)
#		RuntimeGlobals.splashscreen = Delayed_QSplashScreen(RuntimeGlobals.splashscreenImage)
#		RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Initializing {0}.".format(Constants.applicationName, Constants.releaseVersion), textColor=Qt.white)
#		RuntimeGlobals.splashscreen.show()
#
#	RuntimeGlobals.ui = sIBL_GUI()
#	RuntimeGlobals.ui.show()
#	RuntimeGlobals.ui.raise_()
#
#	sys.exit(RuntimeGlobals.application.exec_())
#
#@core.executionTrace
#def _exit():
#	"""
#	This definition is called when sIBL_GUI closes.
#	"""
#
#	LOGGER.info("{0} | Closing interface! ".format(Constants.applicationName))
#	LOGGER.info(Constants.loggingSeparators)
#	LOGGER.info("{0} | Session ended at: {1}".format(Constants.applicationName, time.strftime('%X - %x')))
#	LOGGER.info(Constants.loggingSeparators)
#
#	foundations.common.removeLoggingHandler(LOGGER, RuntimeGlobals.loggingConsoleHandler)
#
#	QApplication.exit()
#
#@core.executionTrace
#def _getHeaderMessage():
#	"""
#	This definition builds the header message.
#
#	:return: Header message ( Tuple )
#	"""
#
#	message = ("{0} | Copyright ( C ) 2008 - 2011 Thomas Mansencal - thomas.mansencal@gmail.com".format(Constants.applicationName),
#				"{0} | This software is released under terms of GNU GPL V3 license.".format(Constants.applicationName),
#				"{0} | http://www.gnu.org/licenses/ ".format(Constants.applicationName),
#				"{0} | Version: {1}".format(Constants.applicationName, Constants.releaseVersion))
#	return message
#
#@core.executionTrace
#def _getCommandLineParameters(argv):
#	"""
#	This definition process command line parameters.
#
#	:param argv: Command line parameters. ( String )
#	:return: Settings, arguments ( Parser instance )
#	"""
#
#	argv = argv or sys.argv[1:]
#
#	parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter (indent_increment=2, max_help_position=8, width=128, short_first=1), add_help_option=None)
#
#	parser.add_option("-h", "--help", action="help", help="'Display this help message and exit.'")
#	parser.add_option("-a", "--about", action="store_true", default=False, dest="about", help="'Display Application about message.'")
#	parser.add_option("-v", "--verbose", action="store", type="int", dest="verbosityLevel", help="'Application verbosity levels: 0 = Critical | 1 = Error | 2 = Warning | 3 = Info | 4 = Debug.'")
#	parser.add_option("-f", "--loggingFormatter", action="store", type="string", dest="loggingFormater", help="'Application logging formatter: '{0}'.'".format(", ".join(sorted(RuntimeGlobals.loggingFormatters.keys()))))
#	parser.add_option("-u", "--userApplicationDatasDirectory", action="store", type="string", dest="userApplicationDatasDirectory", help="'User Application datas directory'.")
#
#	parser.add_option("-t", "--deactivateWorkerThreads", action="store_true", default=False, dest="deactivateWorkerThreads", help="'Deactivate worker threads'.")
#
#	parser.add_option("-d", "--databaseDirectory", action="store", type="string", dest="databaseDirectory", help="'Database directory'.")
#	parser.add_option("-r", "--databaseReadOnly", action="store_true", default=False, dest="databaseReadOnly", help="'Database read only'.")
#
#	parser.add_option("-o", "--loaderScriptsOutputDirectory", action="store", type="string", dest="loaderScriptsOutputDirectory", help="'Loader Scripts output directory'.")
#
#	parser.add_option("-s", "--hideSplashScreen", action="store_true", default=False, dest="hideSplashScreen", help="'Hide splashscreen'.")
#
#	parameters, args = parser.parse_args(argv)
#
#	return parameters, args
#
#@core.executionTrace
#@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiStandaloneSystemExitExceptionHandler, False, OSError)
#def _setUserApplicationDatasDirectory(path):
#	"""
#	This definition sets the Application datas directory.
#
#	:param path: Starting point for the directories tree creation. ( String )
#	:return: Definition success. ( Boolean )
#	"""
#
#	userApplicationDatasDirectory = RuntimeGlobals.userApplicationDatasDirectory
#
#	LOGGER.debug("> Current Application datas directory '{0}'.".format(userApplicationDatasDirectory))
#	if io.setDirectory(userApplicationDatasDirectory):
#		for directory in Constants.preferencesDirectories:
#			if not io.setDirectory(os.path.join(userApplicationDatasDirectory, directory)):
#				raise OSError, "'{0}' directory creation failed , {1} will now close!".format(os.path.join(userApplicationDatasDirectory, directory), Constants.applicationName)
#		return True
#	else:
#		raise OSError, "'{0}' directory creation failed , {1} will now close!".format(userApplicationDatasDirectory, Constants.applicationName)
#
##***********************************************************************************************
##***	Launcher.
##***********************************************************************************************
#if __name__ == "__main__":
#	_run()
