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
import sibl_gui.globals.runtimeGlobals
import umbra.globals.constants
import umbra.globals.uiConstants
import umbra.globals.runtimeGlobals

#***********************************************************************************************
#***	Dependencies globals manipulation.
#***********************************************************************************************
umbra.globals.constants.Constants.__dict__.update(sibl_gui.globals.constants.Constants.__dict__)
umbra.globals.uiConstants.UiConstants.__dict__.update(sibl_gui.globals.uiConstants.UiConstants.__dict__)
umbra.globals.runtimeGlobals.RuntimeGlobals.__dict__.update(sibl_gui.globals.runtimeGlobals.RuntimeGlobals.__dict__)

for path in (os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.resourcesDirectory), os.path.join(os.getcwd(), sibl_gui.__name__, sibl_gui.globals.constants.Constants.resourcesDirectory)):
	os.path.exists(path) and umbra.globals.runtimeGlobals.RuntimeGlobals.resourcesPaths.append(path)

import foundations.globals.constants
import manager.globals.constants

def _overrideDependenciesGlobals():
	"""
	This definition overrides dependencies globals.

	:return: Definition success. ( Boolean )
	"""

	foundations.globals.constants.Constants.logger = manager.globals.constants.Constants.logger = umbra.globals.constants.Constants.logger
	foundations.globals.constants.Constants.applicationDirectory = manager.globals.constants.Constants.applicationDirectory = umbra.globals.constants.Constants.applicationDirectory
	return True

_overrideDependenciesGlobals()

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
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

__all__ = ["LOGGER", "sIBL_GUI", "extendCommandLineParametersParser"]

LOGGER = logging.getLogger(umbra.globals.constants.Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class sIBL_GUI(umbra.engine.Umbra):
	"""
	This class is the main class of the **sIBL_GUI** package.
	"""

	@core.executionTrace
	def __init__(self, paths, components=None):
		"""
		This method initializes the class.

		:param paths: Components paths. ( QString )
		:param components: Mandatory components names. ( QString )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.engine.Umbra.__init__(self, paths, components)

		# --- Setting class attributes. ---

		self.__libraryActiveLabel = None
		self.__inspectActiveLabel = None
		self.__exportActiveLabel = None
		self.__preferencesActiveLabel = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def libraryActiveLabel (self):
		"""
		This method is the property for **self.__libraryActiveLabel** attribute.

		:return: self.__libraryActiveLabel . ( Active_QLabel )
		"""

		return self.__libraryActiveLabel

	@libraryActiveLabel .setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryActiveLabel (self, value):
		"""
		This method is the setter method for **self.__libraryActiveLabel** attribute.

		:param value: Attribute value. ( Active_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("libraryActiveLabel "))

	@libraryActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryActiveLabel (self):
		"""
		This method is the deleter method for **self.__libraryActiveLabel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("libraryActiveLabel "))

	@property
	def inspectActiveLabel (self):
		"""
		This method is the property for **self.__inspectActiveLabel** attribute.

		:return: self.__inspectActiveLabel . ( Active_QLabel )
		"""

		return self.__inspectActiveLabel

	@inspectActiveLabel .setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectActiveLabel (self, value):
		"""
		This method is the setter method for **self.__inspectActiveLabel** attribute.

		:param value: Attribute value. ( Active_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("inspectActiveLabel "))

	@inspectActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectActiveLabel (self):
		"""
		This method is the deleter method for **self.__inspectActiveLabel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("inspectActiveLabel "))

	@property
	def exportActiveLabel (self):
		"""
		This method is the property for **self.__exportActiveLabel** attribute.

		:return: self.__exportActiveLabel . ( Active_QLabel )
		"""

		return self.__exportActiveLabel

	@exportActiveLabel .setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def exportActiveLabel (self, value):
		"""
		This method is the setter method for **self.__exportActiveLabel** attribute.

		:param value: Attribute value. ( Active_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("exportActiveLabel "))

	@exportActiveLabel .deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def exportActiveLabel (self):
		"""
		This method is the deleter method for **self.__exportActiveLabel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("exportActiveLabel "))

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

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
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

		self.layoutsActiveLabels = (umbra.ui.common.LayoutActiveLabel(name="Library", object=self.__libraryActiveLabel, layout="setsCentric", shortcut=Qt.Key_7),
									umbra.ui.common.LayoutActiveLabel(name="Inspect", object=self.__inspectActiveLabel, layout="inspectCentric", shortcut=Qt.Key_8),
									umbra.ui.common.LayoutActiveLabel(name="Export", object=self.__exportActiveLabel, layout="templatesCentric", shortcut=Qt.Key_9),
									umbra.ui.common.LayoutActiveLabel(name="Preferences", object=self.__preferencesActiveLabel, layout="preferencesCentric", shortcut=Qt.Key_0))

		# Signals / Slots.
		for layoutActiveLabel in self.layoutsActiveLabels:
			layoutActiveLabel.object.clicked.connect(functools.partial(self.layoutActiveLabel__clicked, layoutActiveLabel.layout))

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

	@core.executionTrace
	def centralWidgetButton__clicked(self):
		"""
		This method sets the **Central** Widget visibility.
		"""

		LOGGER.debug("> Central Widget button clicked!")

		if self.centralwidget.isVisible():
			self.centralwidget.hide()
		else:
			self.centralwidget.show()

@core.executionTrace
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
	componentsPaths = []
	for path in (os.path.join(umbra.__path__[0], umbra.globals.constants.Constants.factoryComponentsDirectory),
					os.path.join(os.getcwd(), umbra.__name__, umbra.globals.constants.Constants.factoryComponentsDirectory),
					os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.coreComponentsDirectory),
					os.path.join(os.getcwd(), sibl_gui.__name__, sibl_gui.globals.constants.Constants.coreComponentsDirectory),
					os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.addonsComponentsDirectory),
					os.path.join(os.getcwd(), sibl_gui.__name__, sibl_gui.globals.constants.Constants.addonsComponentsDirectory)):
		os.path.exists(path) and componentsPaths.append(path)

	umbra.engine.run(sIBL_GUI, commandLineParametersParser.parse_args(sys.argv), componentsPaths, ("factory.scriptEditor", "factory.preferencesManager", "factory.componentsManagerUi", "core.db", "core.collectionsOutliner", "core.databaseBrowser", "core.inspector", "core.templatesOutliner"))
