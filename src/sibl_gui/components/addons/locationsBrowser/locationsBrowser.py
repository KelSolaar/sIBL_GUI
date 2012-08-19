#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**locationsBrowser.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`LocationsBrowser` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import platform
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QPushButton

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import umbra.ui.common
from foundations.environment import Environment
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "LocationsBrowser"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Locations_Browser.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LocationsBrowser(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.addons.locationsBrowser.locationsBrowser` Component Interface class.
	| It provides methods to explore operating system directories.
	| By default the Component will use current operating system file browsers but 
		the user can define a custom file browser through options exposed
		in the :mod:`sibl_gui.components.core.preferencesManager.preferencesManager` Component ui.

	Defaults file browsers:

		- Windows:

			- Explorer

		- Mac Os X:

			- Finder

		- Linux:

			- Nautilus
			- Dolphin
			- Konqueror
			- Thunar
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

		super(LocationsBrowser, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryComponentsManagerUi = None
		self.__factoryPreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None
		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

		self.__Open_Output_Directory_pushButton = None

		self.__linuxBrowsers = ("nautilus", "dolphin", "konqueror", "thunar")

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settingsSection(self):
		"""
		This method is the property for **self.__settingsSection** attribute.

		:return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for **self.__settingsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def factoryComponentsManagerUi(self):
		"""
		This method is the property for **self.__factoryComponentsManagerUi** attribute.

		:return: self.__factoryComponentsManagerUi. ( QWidget )
		"""

		return self.__factoryComponentsManagerUi

	@factoryComponentsManagerUi.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryComponentsManagerUi(self, value):
		"""
		This method is the setter method for **self.__factoryComponentsManagerUi** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryComponentsManagerUi"))

	@factoryComponentsManagerUi.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryComponentsManagerUi(self):
		"""
		This method is the deleter method for **self.__factoryComponentsManagerUi** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryComponentsManagerUi"))

	@property
	def factoryPreferencesManager(self):
		"""
		This method is the property for **self.__factoryPreferencesManager** attribute.

		:return: self.__factoryPreferencesManager. ( QWidget )
		"""

		return self.__factoryPreferencesManager

	@factoryPreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryPreferencesManager(self, value):
		"""
		This method is the setter method for **self.__factoryPreferencesManager** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryPreferencesManager"))

	@factoryPreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryPreferencesManager(self):
		"""
		This method is the deleter method for **self.__factoryPreferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryPreferencesManager"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( QWidget )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDatabaseBrowser"))

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
	def Open_Output_Directory_pushButton(self):
		"""
		This method is the property for **self.__Open_Output_Directory_pushButton** attribute.

		:return: self.__Open_Output_Directory_pushButton. ( QPushButton )
		"""

		return self.__Open_Output_Directory_pushButton

	@Open_Output_Directory_pushButton.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Open_Output_Directory_pushButton(self, value):
		"""
		This method is the setter method for **self.__Open_Output_Directory_pushButton** attribute.

		:param value: Attribute value. ( QPushButton )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "Open_Output_Directory_pushButton"))

	@Open_Output_Directory_pushButton.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Open_Output_Directory_pushButton(self):
		"""
		This method is the deleter method for **self.__Open_Output_Directory_pushButton** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "Open_Output_Directory_pushButton"))

	@property
	def linuxBrowsers(self):
		"""
		This method is the property for **self.__linuxBrowsers** attribute.

		:return: self.__linuxBrowsers. ( QObject )
		"""

		return self.__linuxBrowsers

	@linuxBrowsers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self, value):
		"""
		This method is the setter method for **self.__linuxBrowsers** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "linuxBrowsers"))

	@linuxBrowsers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self):
		"""
		This method is the deleter method for **self.__linuxBrowsers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "linuxBrowsers"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def activate(self, engine):
		"""
		This method Engine the Component.

		:param engine: Container to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__factoryComponentsManagerUi = self.__engine.componentsManager.components[
											"factory.componentsManagerUi"].interface
		self.__factoryPreferencesManager = self.__engine.componentsManager.components[
											"factory.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__engine.componentsManager.components["core.databaseBrowser"].interface
		self.__coreInspector = self.__engine.componentsManager.components["core.inspector"].interface
		self.__coreTemplatesOutliner = self.__engine.componentsManager.components["core.templatesOutliner"].interface
		self.__addonsLoaderScript = self.__engine.componentsManager.components["addons.loaderScript"].interface

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
		self.__settings = None
		self.__settingsSection = None

		self.__factoryComponentsManagerUi = None
		self.__factoryPreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None
		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

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

		self.__Custom_File_Browser_Path_lineEdit_setUi()

		self.__addActions()

		# Signals / Slots.
		self.Custom_File_Browser_Path_toolButton.clicked.connect(self.__Custom_File_Browser_Path_toolButton__clicked)
		self.Custom_File_Browser_Path_lineEdit.editingFinished.connect(
		self.__Custom_File_Browser_Path_lineEdit__editFinished)

		# LoaderScript addon component specific code.
		if self.__addonsLoaderScript.activated:
			self.__Open_Output_Directory_pushButton = QPushButton("Open Output Directory ...")
			self.__addonsLoaderScript.Loader_Script_verticalLayout.addWidget(self.__Open_Output_Directory_pushButton)

			# Signals / Slots.
			self.__Open_Output_Directory_pushButton.clicked.connect(self.__Open_Output_Directory_pushButton__clicked)

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
		self.Custom_File_Browser_Path_toolButton.clicked.disconnect(self.__Custom_File_Browser_Path_toolButton__clicked)
		self.Custom_File_Browser_Path_lineEdit.editingFinished.disconnect(
		self.__Custom_File_Browser_Path_lineEdit__editFinished)

		# LoaderScript addon component specific code.
		if self.__addonsLoaderScript.activated:
			# Signals / Slots.
			self.__Open_Output_Directory_pushButton.clicked.disconnect(self.__Open_Output_Directory_pushButton__clicked)

			self.__Open_Output_Directory_pushButton.setParent(None)
			self.__Open_Output_Directory_pushButton = None

		self.__removeActions()

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__factoryPreferencesManager.Others_Preferences_gridLayout.addWidget(self.Custom_File_Browser_Path_groupBox)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.Custom_File_Browser_Path_groupBox.setParent(None)

		return True

	@core.executionTrace
	def __addActions(self):
		"""
		This method sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		openIblSetsLocationsAction = self.__engine.actionsManager.registerAction(
									"Actions|Umbra|Components|core.databaseBrowser|Open Ibl Set(s) Location(s) ...",
									slot=self.__Database_Browser_listView_openIblSetsLocationsAction__triggered)
		for view in self.__coreDatabaseBrowser.views:
			view.addAction(openIblSetsLocationsAction)

		self.__coreInspector.Inspector_Overall_frame.addAction(
		self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.inspector|Open Ibl Set location ...",
		slot=self.__Inspector_Overall_frame_openInspectorIblSetLocationsAction__triggered))
		self.__factoryComponentsManagerUi.Components_Manager_Ui_treeView.addAction(
		self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.ComponentsManagerUi|Open Component(s) Location(s) ...",
		slot=self.__Components_Manager_Ui_treeView_openComponentsLocationsAction__triggered))
		self.__coreTemplatesOutliner.view.addAction(
		self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.templatesOutliner|Open Template(s) Location(s) ...",
		slot=self.__Templates_Outliner_treeView_openTemplatesLocationsAction__triggered))

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		openIblSetsLocationsAction = "Actions|Umbra|Components|core.databaseBrowser|Open Ibl Set(s) Location(s) ..."
		for view in self.__coreDatabaseBrowser.views:
			view.removeAction(self.__engine.actionsManager.getAction(openIblSetsLocationsAction))
		self.__engine.actionsManager.unregisterAction(openIblSetsLocationsAction)
		openInspectorIblSetLocationsAction = "Actions|Umbra|Components|core.inspector|Open Ibl Set location ..."
		self.__coreInspector.Inspector_Overall_frame.removeAction(
		self.__engine.actionsManager.getAction(openInspectorIblSetLocationsAction))
		self.__engine.actionsManager.unregisterAction(openInspectorIblSetLocationsAction)
		openComponentsLocationsAction = \
		"Actions|Umbra|Components|factory.ComponentsManagerUi|Open Component(s) Location(s) ..."
		self.__factoryComponentsManagerUi.Components_Manager_Ui_treeView.removeAction(
		self.__engine.actionsManager.getAction(openComponentsLocationsAction))
		self.__engine.actionsManager.unregisterAction(openComponentsLocationsAction)
		openTemplatesLocationsAction = \
		"Actions|Umbra|Components|core.templatesOutliner|Open Template(s) Location(s) ..."
		self.__coreTemplatesOutliner.view.removeAction(
		self.__engine.actionsManager.getAction(openTemplatesLocationsAction))
		self.__engine.actionsManager.unregisterAction(openTemplatesLocationsAction)

	@core.executionTrace
	def __Database_Browser_listView_openIblSetsLocationsAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|core.databaseBrowser|Open Ibl Set(s) Location(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.openIblSetsLocationsUi()

	@core.executionTrace
	def __Inspector_Overall_frame_openInspectorIblSetLocationsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|Open Ibl Set location ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.openInspectorIblSetLocationsUi()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_openComponentsLocationsAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.ComponentsManagerUi|Open Component(s) Location(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.openComponentsLocationsUi()

	@core.executionTrace
	def __Templates_Outliner_treeView_openTemplatesLocationsAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|core.templatesOutliner|Open Template(s) Location(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.openTemplatesLocationsUi()

	@core.executionTrace
	def __Custom_File_Browser_Path_lineEdit_setUi(self):
		"""
		This method fills **Custom_File_Browser_Path_lineEdit** Widget.
		"""

		customFileBrowser = self.__settings.getKey(self.__settingsSection, "customFileBrowser")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format(
		"Custom_File_Browser_Path_lineEdit", customFileBrowser.toString()))
		self.Custom_File_Browser_Path_lineEdit.setText(customFileBrowser.toString())

	@core.executionTrace
	def __Custom_File_Browser_Path_toolButton__clicked(self, checked):
		"""
		This method is triggered when **Custom_File_Browser_Path_toolButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		customFileBrowserExecutable = umbra.ui.common.storeLastBrowsedPath(
		QFileDialog.getOpenFileName(self, "Custom File Browser Executable:", RuntimeGlobals.lastBrowsedPath))
		if customFileBrowserExecutable != "":
			LOGGER.debug("> Chosen custom file browser executable: '{0}'.".format(customFileBrowserExecutable))
			self.Custom_File_Browser_Path_lineEdit.setText(QString(customFileBrowserExecutable))
			self.__settings.setKey(self.__settingsSection,
									"customFileBrowser",
									self.Custom_File_Browser_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler,
											False,
											foundations.exceptions.UserError)
	def __Custom_File_Browser_Path_lineEdit__editFinished(self):
		"""
		This method is triggered when **Custom_File_Browser_Path_lineEdit** Widget
		is edited and check that entered path is valid.
		"""

		value = strings.encode(self.Custom_File_Browser_Path_lineEdit.text())
		if not foundations.common.pathExists(os.path.abspath(value)) and value != unicode():
			LOGGER.debug("> Restoring preferences!")
			self.__Custom_File_Browser_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError(
			"{0} | Invalid custom file browser executable file!".format(self.__class__.__name__))
		else:
			self.__settings.setKey(self.__settingsSection,
									"customFileBrowser",
									self.Custom_File_Browser_Path_lineEdit.text())

	@core.executionTrace
	def __Open_Output_Directory_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Open_Output_Directory_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.openOutputDirectoryUi()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def openIblSetsLocationsUi(self):
		"""
		This method open selected Ibl Sets directories.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()

		success = True
		for iblSet in selectedIblSets:
			path = iblSet.path and foundations.common.pathExists(iblSet.path) and os.path.dirname(iblSet.path)
			if path:
				success *= self.exploreDirectory(path, \
				strings.encode(self.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Ibl Set file doesn't exists and will be skipped!".format(
				self.__class__.__name__, iblSet.title))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while opening '{1}' Ibl Sets directories!".format(
			self.__class__.__name__, ", ".join(iblSet.title for iblSet in selectedIblSets)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler,
											False,
											foundations.exceptions.FileExistsError)
	def openInspectorIblSetLocationsUi(self):
		"""
		This method opens :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set directory.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		inspectorIblSet = self.__coreInspector.inspectorIblSet
		inspectorIblSet = inspectorIblSet and foundations.common.pathExists(inspectorIblSet.path) and \
						inspectorIblSet or None
		if inspectorIblSet:
			return self.exploreDirectory(os.path.dirname(inspectorIblSet.path),
										strings.encode(self.Custom_File_Browser_Path_lineEdit.text()))
		else:
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while opening Inspector Ibl Set directory: '{1}' Ibl Set file doesn't exists!".format(
			self.__class__.__name__, inspectorIblSet.title))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def openComponentsLocationsUi(self):
		"""
		This method opens selected Components directories.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedComponents = self.__factoryComponentsManagerUi.getSelectedComponents()

		success = True
		for component in selectedComponents:
			path = component.directory and foundations.common.pathExists(component.directory) and component.directory
			if path:
				success *= self.exploreDirectory(path, \
				strings.encode(self.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Component file doesn't exists and will be skipped!".format(
				self.__class__.__name__, component.name))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while opening '{1}' Components directories!".format(
			self.__class__.__name__, ", ".join(component.name for component in selectedComponents)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def openTemplatesLocationsUi(self):
		"""
		This method opens selected Templates directories.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()

		success = True
		for template in selectedTemplates:
			path = template.path and foundations.common.pathExists(template.path) and os.path.dirname(template.path)
			if path:
				success *= self.exploreDirectory(path, \
				strings.encode(self.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Template file doesn't exists and will be skipped!".format(
				self.__class__.__name__, template.name))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while opening '{1}' Templates directories!".format(
			self.__class__.__name__, ", ".join(template.name for template in selectedTemplates)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler,
											False,
											foundations.exceptions.DirectoryExistsError,
											Exception)
	def openOutputDirectoryUi(self):
		"""
		This method opens output directory.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		directory = self.__engine.parameters.loaderScriptsOutputDirectory and \
					self.__engine.parameters.loaderScriptsOutputDirectory or self.__addonsLoaderScript.ioDirectory

		if not foundations.common.pathExists(directory):
			raise foundations.exceptions.DirectoryExistsError(
			"{0} | '{1}' loader Script output directory doesn't exists!".format(self.__class__.__name__, directory))

		if self.exploreDirectory(directory, strings.encode(self.Custom_File_Browser_Path_lineEdit.text())):
			return True
		else:
			raise Exception("{0} | Exception raised while exploring '{1}' directory!".format(
			self.__class__.__name__, directory))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProcessCommand(self, directory, customBrowser=None):
		"""
		This method gets process command.

		:param directory: Directory to explore. ( String )
		:param customBrowser: Custom browser. ( String )
		:return: Process command. ( String )
		"""

		processCommand = None
		directory = os.path.normpath(directory)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			if customBrowser:
				processCommand = "\"{0}\" \"{1}\"".format(customBrowser, directory)
			else:
				processCommand = "explorer.exe \"{0}\"".format(directory)
		elif platform.system() == "Darwin":
			if customBrowser:
				processCommand = "open -a \"{0}\" \"{1}\"".format(customBrowser, directory)
			else:
				processCommand = "open \"{0}\"".format(directory)
		elif platform.system() == "Linux":
			if customBrowser:
				processCommand = "\"{0}\" \"{1}\"".format(customBrowser, directory)
			else:
				environmentVariable = Environment("PATH")
				paths = environmentVariable.getValue().split(":")

				browserFound = False
				for browser in self.__linuxBrowsers:
					if browserFound:
						break

					try:
						for path in paths:
							if foundations.common.pathExists(os.path.join(path, browser)):
								processCommand = "\"{0}\" \"{1}\"".format(browser, directory)
								browserFound = True
								raise StopIteration
					except StopIteration:
						pass

				if not browserFound:
					raise Exception("{0} | Exception raised: No suitable Linux browser found!".format(
					self.__class__.__name__))
		return processCommand

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def exploreDirectory(self, directory, customBrowser=None):
		"""
		This method provides directory exploring capability.

		:param directory: Directory to explore. ( String )
		:param customBrowser: Custom browser. ( String )
		:return: Method success. ( Boolean )
		"""

		browserCommand = self.getProcessCommand(directory, customBrowser)
		if browserCommand:
			LOGGER.debug("> Current browser command: '{0}'.".format(browserCommand))
			LOGGER.info("{0} | Launching file browser with '{1}' directory.".format(self.__class__.__name__, directory))
			browserProcess = QProcess()
			browserProcess.startDetached(browserCommand)
			return True
		else:
			raise Exception("{0} | Exception raised: No suitable process command given!".format(self.__class__.__name__))
