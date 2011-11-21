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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import logging
import os
import sys
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPixmap

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import sibl_gui.globals.constants
import sibl_gui.globals.uiConstants
import sibl_gui.globals.runtimeGlobals
import umbra.globals.constants
import umbra.globals.uiConstants
import umbra.globals.runtimeGlobals

#**********************************************************************************************************************
#***	Dependencies globals manipulation.
#**********************************************************************************************************************
umbra.globals.constants.Constants.__dict__.update(sibl_gui.globals.constants.Constants.__dict__)
umbra.globals.uiConstants.UiConstants.__dict__.update(sibl_gui.globals.uiConstants.UiConstants.__dict__)
umbra.globals.runtimeGlobals.RuntimeGlobals.__dict__.update(sibl_gui.globals.runtimeGlobals.RuntimeGlobals.__dict__)

for path in (os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.resourcesDirectory),
			os.path.join(os.getcwd(), sibl_gui.__name__, sibl_gui.globals.constants.Constants.resourcesDirectory)):
	((os.path.exists(path) and not path in umbra.globals.runtimeGlobals.RuntimeGlobals.resourcesDirectories) and
	umbra.globals.runtimeGlobals.RuntimeGlobals.resourcesDirectories.append(path))

import foundations.globals.constants
import manager.globals.constants

def _overrideDependenciesGlobals():
	"""
	This definition overrides dependencies globals.

	:return: Definition success. ( Boolean )
	"""

	foundations.globals.constants.Constants.logger = \
	manager.globals.constants.Constants.logger = umbra.globals.constants.Constants.logger

	foundations.globals.constants.Constants.applicationDirectory = \
	manager.globals.constants.Constants.applicationDirectory = umbra.globals.constants.Constants.applicationDirectory
	return True

_overrideDependenciesGlobals()

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import umbra.engine
import umbra.ui.common
from umbra.ui.widgets.active_QLabel import Active_QLabel

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "sIBL_GUI", "extendCommandLineParametersParser"]

LOGGER = logging.getLogger(umbra.globals.constants.Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class sIBL_GUI(umbra.engine.Umbra):
	"""
	This class is the main class of the **sIBL_GUI** package.
	"""

	@core.executionTrace
	def __init__(self,
				parent=None,
				componentsPaths=None,
				requisiteComponents=None,
				visibleComponents=None,
				*args,
				**kwargs):
		"""
		This method initializes the class.

		:param componentsPaths: Components componentsPaths. ( Tuple / List )
		:param requisiteComponents: Requisite components names. ( Tuple / List )
		:param visibleComponents: Visible components names. ( Tuple / List )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.engine.Umbra.__init__(self,
									parent,
									componentsPaths,
									requisiteComponents,
									visibleComponents,
									*args,
									**kwargs)

		self.__setOverrides()

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setOverrides(self):
		"""
		This method sets Application overrides.
		"""

		factoryScriptEditor = self.componentsManager.getInterface("factory.scriptEditor")
		factoryScriptEditor._ScriptEditor__developmentLayout = "editCentric"
		self.contentDropped.disconnect(factoryScriptEditor._ScriptEditor__application__contentDropped)

	@core.executionTrace
	def __centralWidgetButton__clicked(self):
		"""
		This method sets the **Central** Widget visibility.
		"""

		LOGGER.debug("> Central Widget button clicked!")

		if self.centralwidget.isVisible():
			self.centralwidget.hide()
		else:
			self.centralwidget.show()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getLayoutsActiveLabels(self):
		"""
		This method returns the default layouts active labels widgets.

		:return: Method success. ( Boolean )
		"""

		libraryActiveLabel = Active_QLabel(self,
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.libraryIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.libraryHoverIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.libraryActiveIcon)), True)
		libraryActiveLabel.setObjectName("Library_activeLabel")

		inspectActiveLabel = Active_QLabel(self,
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.inspectIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.inspectHoverIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.inspectActiveIcon)), True)
		inspectActiveLabel.setObjectName("Inspect_activeLabel")

		exportActiveLabel = Active_QLabel(self,
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.exportIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.exportHoverIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.exportActiveIcon)), True)
		exportActiveLabel.setObjectName("Export_activeLabel")

		editActiveLabel = Active_QLabel(self,
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.editIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.editHoverIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.editActiveIcon)), True)
		editActiveLabel.setObjectName("Edit_activeLabel")

		preferencesActiveLabel = Active_QLabel(self,
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.preferencesIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.preferencesHoverIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.preferencesActiveIcon)), True)
		preferencesActiveLabel.setObjectName("Preferences_activeLabel")

		self.layoutsActiveLabels = (umbra.ui.common.LayoutActiveLabel(name="Library",
																	object=libraryActiveLabel,
																	layout="setsCentric",
																	shortcut=Qt.Key_6),
									umbra.ui.common.LayoutActiveLabel(name="Inspect",
																	object=inspectActiveLabel,
																	layout="inspectCentric",
																	shortcut=Qt.Key_7),
									umbra.ui.common.LayoutActiveLabel(name="Export",
																	object=exportActiveLabel,
																	layout="templatesCentric",
																	shortcut=Qt.Key_8),
									umbra.ui.common.LayoutActiveLabel(name="Edit",
																	object=editActiveLabel,
																	layout="editCentric",
																	shortcut=Qt.Key_9),
									umbra.ui.common.LayoutActiveLabel(name="Preferences",
																	object=preferencesActiveLabel,
																	layout="preferencesCentric",
																	shortcut=Qt.Key_0))

		# Signals / Slots.
		for layoutActiveLabel in self.layoutsActiveLabels:
			layoutActiveLabel.object.clicked.connect(functools.partial(self._Umbra__layoutActiveLabel__clicked,
																		layoutActiveLabel.layout))

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getCentralWidgetActiveLabel(self):
		"""
		This method provides the default **Central_Widget_activeLabel** widget.

		:return: Central Widget active label. ( Active_QLabel )
		"""

		centralWidgetButton = Active_QLabel(self,
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.centralWidgetIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.centralWidgetHoverIcon)),
		QPixmap(umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.centralWidgetActiveIcon)))
		centralWidgetButton.setObjectName("Central_Widget_activeLabel")

		# Signals / Slots.
		centralWidgetButton.clicked.connect(self.__centralWidgetButton__clicked)
		return centralWidgetButton

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeToolBar(self):
		"""
		This method initializes Application toolBar.
		"""

		LOGGER.debug("> Initializing Application toolBar!")
		self.toolBar.setIconSize(QSize(umbra.globals.uiConstants.UiConstants.defaultToolbarIconSize,
										umbra.globals.uiConstants.UiConstants.defaultToolbarIconSize))

		LOGGER.debug("> Adding 'Application_Logo_label' widget!")
		self.toolBar.addWidget(self.getApplicationLogoLabel())

		LOGGER.debug("> Adding 'Logo_Spacer_label' widget!")
		self.toolBar.addWidget(self.getLogoSpacerLabel())

		LOGGER.debug("> Adding 'Library_activeLabel', \
					'Inspect_activeLabel', \
					'Export_activeLabel', \
					'Edit_activeLabel', \
					'Preferences_activeLabel' \
					widgets!")

		self.getLayoutsActiveLabels()
		for activeLabel in self.layoutsActiveLabels:
			self.toolBar.addWidget(activeLabel.object)

		LOGGER.debug("> Adding 'Central_Widget_activeLabel' widget!")
		self.toolBar.addWidget(self.getCentralWidgetActiveLabel())

		LOGGER.debug("> Adding 'Custom_Layouts_activeLabel' widget!")
		self.toolBar.addWidget(self.getCustomLayoutsActiveLabel())

		LOGGER.debug("> Adding 'Miscellaneous_activeLabel' widget!")
		self.toolBar.addWidget(self.getMiscellaneousActiveLabel())

		LOGGER.debug("> Adding 'Closure_Spacer_label' widget!")
		self.toolBar.addWidget(self.getClosureSpacerLabel())
		return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def extendCommandLineParametersParser(parser):
	"""
	This definition returns the command line parameters parser.

	:param parser: Command line parameters parser. ( Parser )
	:return: Definition success. ( Boolean )
	"""

	parser.add_option("-t",
					"--deactivateWorkerThreads",
					action="store_true",
					default=False,
					dest="deactivateWorkerThreads",
					help="'Deactivate worker threads'.")
	parser.add_option("-d",
					"--databaseDirectory",
					action="store",
					type="string",
					dest="databaseDirectory",
					help="'Database directory'.")
	parser.add_option("-r",
					"--databaseReadOnly",
					action="store_true",
					default=False,
					dest="databaseReadOnly",
					help="'Database read only'.")
	parser.add_option("-o",
					"--loaderScriptsOutputDirectory",
					action="store",
					type="string",
					dest="loaderScriptsOutputDirectory",
					help="'Loader Scripts output directory'.")

	return True

#**********************************************************************************************************************
#***	Launcher.
#**********************************************************************************************************************
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
		(os.path.exists(path) and not path in componentsPaths) and componentsPaths.append(path)

	umbra.engine.run(sIBL_GUI,
					commandLineParametersParser.parse_args(sys.argv),
					componentsPaths,
					("factory.scriptEditor",
					"factory.preferencesManager",
					"factory.componentsManagerUi",
					"core.db",
					"core.collectionsOutliner",
					"core.databaseBrowser",
					"core.inspector",
					"core.templatesOutliner"),
					("core.databaseBrowser",))
