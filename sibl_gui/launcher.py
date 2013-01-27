#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**launcher.py**

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
import os
import sys
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QPixmap

#**********************************************************************************************************************
#***	Encoding manipulations.
#**********************************************************************************************************************
def _setEncoding():
	"""
	This definition sets the Application encoding.
	"""

	reload(sys)
	sys.setdefaultencoding("utf-8")

_setEncoding()

#**********************************************************************************************************************
#***	Path manipulations.
#**********************************************************************************************************************
def _setPackageDirectory():
	"""
	This definition sets the Application package directory in the path.
	"""

	if hasattr(sys, "frozen"):
		packageDirectory = os.path.dirname(__file__)
	else:
		packageDirectory = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
	packageDirectory not in sys.path and sys.path.append(packageDirectory)

_setPackageDirectory()

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
	path = os.path.normpath(path)
	if os.path.exists(path):
		path not in umbra.globals.runtimeGlobals.RuntimeGlobals.resourcesDirectories and \
		umbra.globals.runtimeGlobals.RuntimeGlobals.resourcesDirectories.append(path)

import foundations.globals.constants
import manager.globals.constants

def _overrideDependenciesGlobals():
	"""
	This definition overrides dependencies globals.
	"""

	foundations.globals.constants.Constants.logger = \
	manager.globals.constants.Constants.logger = umbra.globals.constants.Constants.logger

	foundations.globals.constants.Constants.applicationDirectory = \
	manager.globals.constants.Constants.applicationDirectory = umbra.globals.constants.Constants.applicationDirectory

_overrideDependenciesGlobals()

import umbra.ui.widgets.application_QToolBar
import sibl_gui.ui.widgets.application_QToolBar

def _overrideApplicationToolbar():
	"""
	This definition overrides Application toolbar.
	"""

	umbra.ui.widgets.application_QToolBar.Application_QToolBar = \
	sibl_gui.ui.widgets.application_QToolBar.Application_QToolBar

_overrideApplicationToolbar()

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.verbose
import sibl_gui.ui.cache
import sibl_gui.ui.models
import umbra.engine
import umbra.ui.common
import umbra.ui.models

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "sIBL_GUI", "extendCommandLineParametersParser"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def _setImagesCaches():
	"""
	This definition sets the Application images caches.
	"""

	loadingImage = umbra.ui.common.getResourcePath(umbra.globals.uiConstants.UiConstants.loadingImage)
	umbra.globals.runtimeGlobals.RuntimeGlobals.imagesCaches = foundations.dataStructures.Structure(**{
								"QImage":sibl_gui.ui.cache.AsynchronousGraphicsItemsCache(type=QImage, default=loadingImage),
								"QPixmap":sibl_gui.ui.cache.AsynchronousGraphicsItemsCache(type=QPixmap, default=loadingImage),
								"QIcon":sibl_gui.ui.cache.AsynchronousGraphicsItemsCache(type=QIcon, default=loadingImage)})

	# Override "umbra.ui.models.GraphModel.data" method to use "sibl_gui.ui.models.GraphModel.data" method
	# with asynchronous images loading.
	setattr(umbra.ui.models.GraphModel, "data", umbra.ui.models.GraphModel.data)

_setImagesCaches()

class sIBL_GUI(umbra.engine.Umbra):
	"""
	This class is the main class of the **sIBL_GUI** package.
	"""

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

		self.__imagesCaches = None

		umbra.engine.Umbra.__init__(self,
									parent,
									componentsPaths,
									requisiteComponents,
									visibleComponents,
									*args,
									**kwargs)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def imagesCaches(self):
		"""
		This method is the property for **self.__imagesCaches** attribute.

		:return: self.__imagesCaches. ( Cache )
		"""

		return self.__imagesCaches

	@imagesCaches.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def imagesCaches(self, value):
		"""
		This method is the setter method for **self.__imagesCaches** attribute.

		:param value: Attribute value. ( Cache )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "imagesCaches"))

	@imagesCaches.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def imagesCaches(self):
		"""
		This method is the deleter method for **self.__imagesCaches** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "imagesCaches"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def onPreInitialisation(self):
		"""
		This method is called by the :class:`umbra.engine.Umbra` class before Application main class initialisation.
		"""

		# Binding Application images caches.
		self.__imagesCaches = umbra.globals.runtimeGlobals.RuntimeGlobals.imagesCaches

	def onPostInitialisation(self):
		"""
		This method is called by the :class:`umbra.engine.Umbra` class after Application main class initialisation.
		"""

		for cache in self.__imagesCaches.itervalues():
			self.workerThreads.append(cache.worker)

		componentsManagerUi = self.componentsManager.getInterface("factory.componentsManagerUi")
		self.imagesCaches.QIcon.contentAdded.connect(componentsManagerUi.view.viewport().update)

		scriptEditor = self.componentsManager.getInterface("factory.scriptEditor")
		self.contentDropped.disconnect(scriptEditor._ScriptEditor__engine__contentDropped)

def extendCommandLineParametersParser(parser):
	"""
	This definition returns the command line parameters parser.

	:param parser: Command line parameters parser. ( Parser )
	:return: Definition success. ( Boolean )
	"""

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
def main():
	"""
	This definition starts the Application.

	:return: Definition success. ( Boolean )
	"""

	commandLineParametersParser = umbra.engine.getCommandLineParametersParser()
	extendCommandLineParametersParser(commandLineParametersParser)
	componentsPaths = []
	for path in (os.path.join(umbra.__path__[0], umbra.globals.constants.Constants.factoryComponentsDirectory),
		os.path.join(os.getcwd(), umbra.__name__, umbra.globals.constants.Constants.factoryComponentsDirectory),
		os.path.join(umbra.__path__[0], umbra.globals.constants.Constants.factoryAddonsComponentsDirectory),
		os.path.join(os.getcwd(), umbra.__name__, umbra.globals.constants.Constants.factoryAddonsComponentsDirectory),
		os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.coreComponentsDirectory),
		os.path.join(os.getcwd(), sibl_gui.__name__, sibl_gui.globals.constants.Constants.coreComponentsDirectory),
		os.path.join(sibl_gui.__path__[0], sibl_gui.globals.constants.Constants.addonsComponentsDirectory),
		os.path.join(os.getcwd(), sibl_gui.__name__, sibl_gui.globals.constants.Constants.addonsComponentsDirectory)):
		(foundations.common.pathExists(path) and not path in componentsPaths) and componentsPaths.append(path)

	return umbra.engine.run(sIBL_GUI,
						commandLineParametersParser.parse_args(sys.argv),
						componentsPaths,
						("factory.scriptEditor",
						"factory.preferencesManager",
						"factory.componentsManagerUi",
						"core.database",
						"core.collectionsOutliner",
						"core.iblSetsOutliner",
						"core.inspector",
						"core.templatesOutliner"),
						("core.iblSetsOutliner",))

if __name__ == "__main__":
	main()
