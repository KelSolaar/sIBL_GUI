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
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.common
from foundations.environment import Environment
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "LocationsBrowser"]

LOGGER = foundations.verbose.installLogger()

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

		self.__componentsManagerUi = None
		self.__preferencesManager = None
		self.__iblSetsOutliner = None
		self.__inspector = None
		self.__templatesOutliner = None
		self.__loaderScript = None

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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for **self.__settingsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def componentsManagerUi(self):
		"""
		This method is the property for **self.__componentsManagerUi** attribute.

		:return: self.__componentsManagerUi. ( QWidget )
		"""

		return self.__componentsManagerUi

	@componentsManagerUi.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def componentsManagerUi(self, value):
		"""
		This method is the setter method for **self.__componentsManagerUi** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "componentsManagerUi"))

	@componentsManagerUi.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def componentsManagerUi(self):
		"""
		This method is the deleter method for **self.__componentsManagerUi** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "componentsManagerUi"))

	@property
	def preferencesManager(self):
		"""
		This method is the property for **self.__preferencesManager** attribute.

		:return: self.__preferencesManager. ( QWidget )
		"""

		return self.__preferencesManager

	@preferencesManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def preferencesManager(self, value):
		"""
		This method is the setter method for **self.__preferencesManager** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "preferencesManager"))

	@preferencesManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def preferencesManager(self):
		"""
		This method is the deleter method for **self.__preferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preferencesManager"))

	@property
	def iblSetsOutliner(self):
		"""
		This method is the property for **self.__iblSetsOutliner** attribute.

		:return: self.__iblSetsOutliner. ( QWidget )
		"""

		return self.__iblSetsOutliner

	@iblSetsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self, value):
		"""
		This method is the setter method for **self.__iblSetsOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsOutliner"))

	@iblSetsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self):
		"""
		This method is the deleter method for **self.__iblSetsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsOutliner"))

	@property
	def templatesOutliner(self):
		"""
		This method is the property for **self.__templatesOutliner** attribute.

		:return: self.__templatesOutliner. ( QWidget )
		"""

		return self.__templatesOutliner

	@templatesOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesOutliner(self, value):
		"""
		This method is the setter method for **self.__templatesOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesOutliner"))

	@templatesOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesOutliner(self):
		"""
		This method is the deleter method for **self.__templatesOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesOutliner"))

	@property
	def loaderScript(self):
		"""
		This method is the property for **self.__loaderScript** attribute.

		:return: self.__loaderScript. ( QWidget )
		"""

		return self.__loaderScript

	@loaderScript.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loaderScript(self, value):
		"""
		This method is the setter method for **self.__loaderScript** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loaderScript"))

	@loaderScript.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loaderScript(self):
		"""
		This method is the deleter method for **self.__loaderScript** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loaderScript"))

	@property
	def Open_Output_Directory_pushButton(self):
		"""
		This method is the property for **self.__Open_Output_Directory_pushButton** attribute.

		:return: self.__Open_Output_Directory_pushButton. ( QPushButton )
		"""

		return self.__Open_Output_Directory_pushButton

	@Open_Output_Directory_pushButton.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def Open_Output_Directory_pushButton(self, value):
		"""
		This method is the setter method for **self.__Open_Output_Directory_pushButton** attribute.

		:param value: Attribute value. ( QPushButton )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "Open_Output_Directory_pushButton"))

	@Open_Output_Directory_pushButton.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self, value):
		"""
		This method is the setter method for **self.__linuxBrowsers** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "linuxBrowsers"))

	@linuxBrowsers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self):
		"""
		This method is the deleter method for **self.__linuxBrowsers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "linuxBrowsers"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
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

		self.__componentsManagerUi = self.__engine.componentsManager["factory.componentsManagerUi"]
		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]
		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]
		self.__inspector = self.__engine.componentsManager["core.inspector"]
		self.__templatesOutliner = self.__engine.componentsManager["core.templatesOutliner"]
		self.__loaderScript = self.__engine.componentsManager["addons.loaderScript"]

		self.activated = True
		return True

	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__componentsManagerUi = None
		self.__preferencesManager = None
		self.__iblSetsOutliner = None
		self.__inspector = None
		self.__templatesOutliner = None
		self.__loaderScript = None

		self.activated = False
		return True

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
		if self.__loaderScript.activated:
			self.__Open_Output_Directory_pushButton = QPushButton("Open Output Directory ...")
			self.__loaderScript.Loader_Script_verticalLayout.addWidget(self.__Open_Output_Directory_pushButton)

			# Signals / Slots.
			self.__Open_Output_Directory_pushButton.clicked.connect(self.__Open_Output_Directory_pushButton__clicked)

		self.initializedUi = True
		return True

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
		if self.__loaderScript.activated:
			# Signals / Slots.
			self.__Open_Output_Directory_pushButton.clicked.disconnect(self.__Open_Output_Directory_pushButton__clicked)

			self.__Open_Output_Directory_pushButton.setParent(None)
			self.__Open_Output_Directory_pushButton = None

		self.__removeActions()

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.Custom_File_Browser_Path_groupBox)

		return True

	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.Custom_File_Browser_Path_groupBox.setParent(None)

		return True

	def __addActions(self):
		"""
		This method sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		openIblSetsLocationsAction = self.__engine.actionsManager.registerAction(
									"Actions|Umbra|Components|core.iblSetsOutliner|Open Ibl Set(s) Location(s) ...",
									slot=self.__iblSetsOutliner_views_openIblSetsLocationsAction__triggered)
		for view in self.__iblSetsOutliner.views:
			view.addAction(openIblSetsLocationsAction)

		self.__inspector.Inspector_Overall_frame.addAction(
		self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.inspector|Open Ibl Set location ...",
		slot=self.__inspector_openActiveIblSetLocationsAction__triggered))
		self.__componentsManagerUi.view.addAction(
		self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.ComponentsManagerUi|Open Component(s) Location(s) ...",
		slot=self.__componentsManagerUi_view_openComponentsLocationsAction__triggered))
		self.__templatesOutliner.view.addAction(
		self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.templatesOutliner|Open Template(s) Location(s) ...",
		slot=self.__templatesOutliner_view_openTemplatesLocationsAction__triggered))

	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		openIblSetsLocationsAction = "Actions|Umbra|Components|core.iblSetsOutliner|Open Ibl Set(s) Location(s) ..."
		for view in self.__iblSetsOutliner.views:
			view.removeAction(self.__engine.actionsManager.getAction(openIblSetsLocationsAction))
		self.__engine.actionsManager.unregisterAction(openIblSetsLocationsAction)
		openActiveIblSetLocationsAction = "Actions|Umbra|Components|core.inspector|Open Ibl Set location ..."
		self.__inspector.Inspector_Overall_frame.removeAction(
		self.__engine.actionsManager.getAction(openActiveIblSetLocationsAction))
		self.__engine.actionsManager.unregisterAction(openActiveIblSetLocationsAction)
		openComponentsLocationsAction = \
		"Actions|Umbra|Components|factory.ComponentsManagerUi|Open Component(s) Location(s) ..."
		self.__componentsManagerUi.view.removeAction(
		self.__engine.actionsManager.getAction(openComponentsLocationsAction))
		self.__engine.actionsManager.unregisterAction(openComponentsLocationsAction)
		openTemplatesLocationsAction = \
		"Actions|Umbra|Components|core.templatesOutliner|Open Template(s) Location(s) ..."
		self.__templatesOutliner.view.removeAction(
		self.__engine.actionsManager.getAction(openTemplatesLocationsAction))
		self.__engine.actionsManager.unregisterAction(openTemplatesLocationsAction)

	def __iblSetsOutliner_views_openIblSetsLocationsAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|core.iblSetsOutliner|Open Ibl Set(s) Location(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.openIblSetsLocationsUi()

	def __inspector_openActiveIblSetLocationsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|Open Ibl Set location ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.openActiveIblSetLocationsUi()

	def __componentsManagerUi_view_openComponentsLocationsAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.ComponentsManagerUi|Open Component(s) Location(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.openComponentsLocationsUi()

	def __templatesOutliner_view_openTemplatesLocationsAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|core.templatesOutliner|Open Template(s) Location(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.openTemplatesLocationsUi()

	def __Custom_File_Browser_Path_lineEdit_setUi(self):
		"""
		This method fills **Custom_File_Browser_Path_lineEdit** Widget.
		"""

		customFileBrowser = self.__settings.getKey(self.__settingsSection, "customFileBrowser")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format(
		"Custom_File_Browser_Path_lineEdit", customFileBrowser.toString()))
		self.Custom_File_Browser_Path_lineEdit.setText(customFileBrowser.toString())

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

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError)
	def __Custom_File_Browser_Path_lineEdit__editFinished(self):
		"""
		This method is triggered when **Custom_File_Browser_Path_lineEdit** Widget
		is edited and check that entered path is valid.
		"""

		value = foundations.strings.encode(self.Custom_File_Browser_Path_lineEdit.text())
		if not foundations.common.pathExists(os.path.abspath(value)) and value != unicode():
			LOGGER.debug("> Restoring preferences!")
			self.__Custom_File_Browser_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError(
			"{0} | Invalid custom file browser executable file!".format(self.__class__.__name__))
		else:
			self.__settings.setKey(self.__settingsSection,
									"customFileBrowser",
									self.Custom_File_Browser_Path_lineEdit.text())

	def __Open_Output_Directory_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Open_Output_Directory_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.openOutputDirectoryUi()

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def openIblSetsLocationsUi(self):
		"""
		This method open selected Ibl Sets directories.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedIblSets = self.__iblSetsOutliner.getSelectedIblSets()

		success = True
		for iblSet in selectedIblSets:
			path = iblSet.path and foundations.common.pathExists(iblSet.path) and os.path.dirname(iblSet.path)
			if path:
				success *= self.exploreDirectory(path, \
				foundations.strings.encode(self.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Ibl Set file doesn't exists and will be skipped!".format(
				self.__class__.__name__, iblSet.title))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while opening '{1}' Ibl Sets directories!".format(
			self.__class__.__name__, ", ".join(iblSet.title for iblSet in selectedIblSets)))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.FileExistsError)
	def openActiveIblSetLocationsUi(self):
		"""
		This method opens :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set directory.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		activeIblSet = self.__inspector.activeIblSet
		if activeIblSet is None:
			return False

		if foundations.common.pathExists(activeIblSet.path):
			return self.exploreDirectory(os.path.dirname(activeIblSet.path),
										foundations.strings.encode(self.Custom_File_Browser_Path_lineEdit.text()))
		else:
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while opening Inspector Ibl Set directory: '{1}' Ibl Set file doesn't exists!".format(
			self.__class__.__name__, activeIblSet.title))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def openComponentsLocationsUi(self):
		"""
		This method opens selected Components directories.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedComponents = self.__componentsManagerUi.getSelectedComponents()

		success = True
		for component in selectedComponents:
			path = component.directory and foundations.common.pathExists(component.directory) and component.directory
			if path:
				success *= self.exploreDirectory(path, \
				foundations.strings.encode(self.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Component file doesn't exists and will be skipped!".format(
				self.__class__.__name__, component.name))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while opening '{1}' Components directories!".format(
			self.__class__.__name__, ", ".join(component.name for component in selectedComponents)))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def openTemplatesLocationsUi(self):
		"""
		This method opens selected Templates directories.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedTemplates = self.__templatesOutliner.getSelectedTemplates()

		success = True
		for template in selectedTemplates:
			path = template.path and foundations.common.pathExists(template.path) and os.path.dirname(template.path)
			if path:
				success *= self.exploreDirectory(path, \
				foundations.strings.encode(self.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Template file doesn't exists and will be skipped!".format(
				self.__class__.__name__, template.name))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while opening '{1}' Templates directories!".format(
			self.__class__.__name__, ", ".join(template.name for template in selectedTemplates)))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.DirectoryExistsError,
											Exception)
	def openOutputDirectoryUi(self):
		"""
		This method opens output directory.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		directory = self.__engine.parameters.loaderScriptsOutputDirectory and \
					self.__engine.parameters.loaderScriptsOutputDirectory or self.__loaderScript.ioDirectory

		if not foundations.common.pathExists(directory):
			raise foundations.exceptions.DirectoryExistsError(
			"{0} | '{1}' loader Script output directory doesn't exists!".format(self.__class__.__name__, directory))

		if self.exploreDirectory(directory, foundations.strings.encode(self.Custom_File_Browser_Path_lineEdit.text())):
			return True
		else:
			raise Exception("{0} | Exception raised while exploring '{1}' directory!".format(
			self.__class__.__name__, directory))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
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
