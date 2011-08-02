#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**locationsBrowser.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Locations Browser Component Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.components.core.db.dbUtilities.types as dbTypes
import umbra.ui.common
from foundations.environment import Environment
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants

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

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LocationsBrowser(UiComponent):
	"""
	This class is the **LocationsBrowser** class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		:param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__uiPath = "ui/Locations_Browser.ui"

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__coreComponentsManagerUi = None
		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None
		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

		self.__openIblSetsLocationsAction = None
		self.__openComponentsLocationsAction = None
		self.__openTemplatesLocationsAction = None

		self.__Open_Output_Directory_pushButton = None

		self.__linuxBrowsers = ("nautilus", "dolphin", "konqueror", "thunar")

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for **self.__uiPath** attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for **self.__uiPath** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for **self.__uiPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settingsSection"))

	@property
	def coreComponentsManagerUi(self):
		"""
		This method is the property for **self.__coreComponentsManagerUi** attribute.

		:return: self.__coreComponentsManagerUi. ( Object )
		"""

		return self.__coreComponentsManagerUi

	@coreComponentsManagerUi.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreComponentsManagerUi(self, value):
		"""
		This method is the setter method for **self.__coreComponentsManagerUi** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreComponentsManagerUi"))

	@coreComponentsManagerUi.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreComponentsManagerUi(self):
		"""
		This method is the deleter method for **self.__coreComponentsManagerUi** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreComponentsManagerUi"))

	@property
	def corePreferencesManager(self):
		"""
		This method is the property for **self.__corePreferencesManager** attribute.

		:return: self.__corePreferencesManager. ( Object )
		"""

		return self.__corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self, value):
		"""
		This method is the setter method for **self.__corePreferencesManager** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("corePreferencesManager"))

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self):
		"""
		This method is the deleter method for **self.__corePreferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("corePreferencesManager"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def coreTemplatesOutliner(self):
		"""
		This method is the property for **self.__coreTemplatesOutliner** attribute.

		:return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This method is the setter method for **self.__coreTemplatesOutliner** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This method is the deleter method for **self.__coreTemplatesOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreTemplatesOutliner"))

	@property
	def addonsLoaderScript(self):
		"""
		This method is the property for **self.__addonsLoaderScript** attribute.

		:return: self.__addonsLoaderScript. ( Object )
		"""

		return self.__addonsLoaderScript

	@addonsLoaderScript.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self, value):
		"""
		This method is the setter method for **self.__addonsLoaderScript** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("addonsLoaderScript"))

	@addonsLoaderScript.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self):
		"""
		This method is the deleter method for **self.__addonsLoaderScript** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("addonsLoaderScript"))

	@property
	def openIblSetsLocationsAction(self):
		"""
		This method is the property for **self.__openIblSetsLocationsAction** attribute.

		:return: self.__openIblSetsLocationsAction. ( QAction )
		"""

		return self.__openIblSetsLocationsAction

	@openIblSetsLocationsAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openIblSetsLocationsAction(self, value):
		"""
		This method is the setter method for **self.__openIblSetsLocationsAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("openIblSetsLocationsAction"))

	@openIblSetsLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openIblSetsLocationsAction(self):
		"""
		This method is the deleter method for **self.__openIblSetsLocationsAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("openIblSetsLocationsAction"))

	@property
	def openInspectorIblSetLocationsAction(self):
		"""
		This method is the property for **self.__openInspectorIblSetLocationsAction** attribute.

		:return: self.__openInspectorIblSetLocationsAction. ( QAction )
		"""

		return self.__openInspectorIblSetLocationsAction

	@openInspectorIblSetLocationsAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openInspectorIblSetLocationsAction(self, value):
		"""
		This method is the setter method for **self.__openInspectorIblSetLocationsAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("openInspectorIblSetLocationsAction"))

	@openInspectorIblSetLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openInspectorIblSetLocationsAction(self):
		"""
		This method is the deleter method for **self.__openInspectorIblSetLocationsAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("openInspectorIblSetLocationsAction"))

	@property
	def openComponentsLocationsAction(self):
		"""
		This method is the property for **self.__openComponentsLocationsAction** attribute.

		:return: self.__openComponentsLocationsAction. ( QAction )
		"""

		return self.__openComponentsLocationsAction

	@openComponentsLocationsAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openComponentsLocationsAction(self, value):
		"""
		This method is the setter method for **self.__openComponentsLocationsAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("openComponentsLocationsAction"))

	@openComponentsLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openComponentsLocationsAction(self):
		"""
		This method is the deleter method for **self.__openComponentsLocationsAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("openComponentsLocationsAction"))

	@property
	def openTemplatesLocationsAction(self):
		"""
		This method is the property for **self.__openTemplatesLocationsAction** attribute.

		:return: self.__openTemplatesLocationsAction. ( QAction )
		"""

		return self.__openTemplatesLocationsAction

	@openTemplatesLocationsAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openTemplatesLocationsAction(self, value):
		"""
		This method is the setter method for **self.__openTemplatesLocationsAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("openTemplatesLocationsAction"))

	@openTemplatesLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openTemplatesLocationsAction(self):
		"""
		This method is the deleter method for **self.__openTemplatesLocationsAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("openTemplatesLocationsAction"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("Open_Output_Directory_pushButton"))

	@Open_Output_Directory_pushButton.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Open_Output_Directory_pushButton(self):
		"""
		This method is the deleter method for **self.__Open_Output_Directory_pushButton** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("Open_Output_Directory_pushButton"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("linuxBrowsers"))

	@linuxBrowsers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self):
		"""
		This method is the deleter method for **self.__linuxBrowsers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("linuxBrowsers"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__coreComponentsManagerUi = self.__container.componentsManager.components["core.componentsManagerUi"].interface
		self.__corePreferencesManager = self.__container.componentsManager.components["core.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreInspector = self.__container.componentsManager.components["core.inspector"].interface
		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface
		self.__addonsLoaderScript = self.__container.componentsManager.components["addons.loaderScript"].interface

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__coreComponentsManagerUi = None
		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None
		self.__coreTemplatesOutliner = None
		self.__addonsLoaderScript = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__Custom_File_Browser_Path_lineEdit_setUi()

		self.__addActions()

		# Signals / Slots.
		self.ui.Custom_File_Browser_Path_toolButton.clicked.connect(self.__Custom_File_Browser_Path_toolButton__clicked)
		self.ui.Custom_File_Browser_Path_lineEdit.editingFinished.connect(self.__Custom_File_Browser_Path_lineEdit__editFinished)

		# LoaderScript addon component specific code.
		if self.__addonsLoaderScript.activated:
			self.__Open_Output_Directory_pushButton = QPushButton("Open output directory")
			self.__addonsLoaderScript.ui.Loader_Script_verticalLayout.addWidget(self.__Open_Output_Directory_pushButton)

			# Signals / Slots.
			self.__Open_Output_Directory_pushButton.clicked.connect(self.__Open_Output_Directory_pushButton__clicked)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Custom_File_Browser_Path_toolButton.clicked.disconnect(self.__Custom_File_Browser_Path_toolButton__clicked)
		self.ui.Custom_File_Browser_Path_lineEdit.editingFinished.disconnect(self.__Custom_File_Browser_Path_lineEdit__editFinished)

		# LoaderScript addon component specific code.
		if self.__addonsLoaderScript.activated:
			# Signals / Slots.
			self.__Open_Output_Directory_pushButton.clicked.disconnect(self.__Open_Output_Directory_pushButton__clicked)

			self.__Open_Output_Directory_pushButton.setParent(None)
			self.__Open_Output_Directory_pushButton = None

		self.__removeActions()

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Custom_File_Browser_Path_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.ui.Custom_File_Browser_Path_groupBox.setParent(None)

	@core.executionTrace
	def __addActions(self):
		"""
		This method adds actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		self.__openIblSetsLocationsAction = QAction("Open Ibl Set(s) Location(s) ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
		self.__openIblSetsLocationsAction.triggered.connect(self.__Database_Browser_listView_openIblSetsLocationsAction__triggered)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__openIblSetsLocationsAction)

		self.__openInspectorIblSetLocationsAction = QAction("Open Ibl Set location ...", self.__coreInspector.ui.Inspector_Overall_frame)
		self.__openInspectorIblSetLocationsAction.triggered.connect(self.__Inspector_Overall_frame_openInspectorIblSetLocationsAction__triggered)
		self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__openInspectorIblSetLocationsAction)

		self.__openComponentsLocationsAction = QAction("Open Component(s) Location(s) ...", self.__coreComponentsManagerUi.ui.Components_Manager_Ui_treeView)
		self.__openComponentsLocationsAction.triggered.connect(self.__Components_Manager_Ui_treeView_openComponentsLocationsAction__triggered)
		self.__coreComponentsManagerUi.ui.Components_Manager_Ui_treeView.addAction(self.__openComponentsLocationsAction)

		self.__openTemplatesLocationsAction = QAction("Open Template(s) Location(s) ...", self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView)
		self.__openTemplatesLocationsAction.triggered.connect(self.__Templates_Outliner_treeView_openTemplatesLocationsAction__triggered)
		self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.addAction(self.__openTemplatesLocationsAction)

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		self.__coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self.__openIblSetsLocationsAction)
		self.__coreInspector.ui.Inspector_Overall_frame.removeAction(self.__openInspectorIblSetLocationsAction)
		self.__coreComponentsManagerUi.ui.Components_Manager_Ui_treeView.removeAction(self.__openComponentsLocationsAction)
		self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.removeAction(self.__openTemplatesLocationsAction)

		self.__openIblSetsLocationsAction = None
		self.__openInspectorIblSetLocationsAction = None
		self.__openComponentsLocationsAction = None
		self.__openTemplatesLocationsAction = None

	@core.executionTrace
	def __Database_Browser_listView_openIblSetsLocationsAction__triggered(self, checked):
		"""
		This method is triggered by **openIblSetsLocationsAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.openIblSetsLocations__()

	@core.executionTrace
	def __Inspector_Overall_frame_openInspectorIblSetLocationsAction__triggered(self, checked):
		"""
		This method is triggered by **openInspectorIblSetLocationsAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.openInspectorIblSetLocations__()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_openComponentsLocationsAction__triggered(self, checked):
		"""
		This method is triggered by **openComponentsLocationsAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.openComponentsLocations__()

	@core.executionTrace
	def __Templates_Outliner_treeView_openTemplatesLocationsAction__triggered(self, checked):
		"""
		This method is triggered by **openTemplatesLocationsAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.openTemplatesLocations__()

	@core.executionTrace
	def __Custom_File_Browser_Path_lineEdit_setUi(self):
		"""
		This method fills **Custom_File_Browser_Path_lineEdit** Widget.
		"""

		customFileBrowser = self.__settings.getKey(self.__settingsSection, "customFileBrowser")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Custom_File_Browser_Path_lineEdit", customFileBrowser.toString()))
		self.ui.Custom_File_Browser_Path_lineEdit.setText(customFileBrowser.toString())

	@core.executionTrace
	def __Custom_File_Browser_Path_toolButton__clicked(self, checked):
		"""
		This method is called when **Custom_File_Browser_Path_toolButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		customFileBrowserExecutable = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom file browser executable:", self.__container.lastBrowsedPath))
		if customFileBrowserExecutable != "":
			LOGGER.debug("> Chosen custom file browser executable: '{0}'.".format(customFileBrowserExecutable))
			self.ui.Custom_File_Browser_Path_lineEdit.setText(QString(customFileBrowserExecutable))
			self.__settings.setKey(self.__settingsSection, "customFileBrowser", self.ui.Custom_File_Browser_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __Custom_File_Browser_Path_lineEdit__editFinished(self):
		"""
		This method is called when **Custom_File_Browser_Path_lineEdit** Widget is edited and check that entered path is valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.Custom_File_Browser_Path_lineEdit.text()))) and str(self.ui.Custom_File_Browser_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring preferences!")
			self.__Custom_File_Browser_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid custom file browser executable file!".format(self.__class__.__name__)
		else:
			self.__settings.setKey(self.__settingsSection, "customFileBrowser", self.ui.Custom_File_Browser_Path_lineEdit.text())

	@core.executionTrace
	def __Open_Output_Directory_pushButton__clicked(self, checked):
		"""
		This method is called when **Open_Output_Directory_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.openOutputDirectory__()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def openIblSetsLocations__(self):
		"""
		This method open selected Ibl Sets directories.

		:return: Method success. ( Boolean )
		"""

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()

		success = True
		for iblSet in selectedIblSets:
			path = iblSet.path and os.path.exists(iblSet.path) and os.path.dirname(iblSet.path)
			if path:
				success *= self.exploreDirectory(path, str(self.ui.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Ibl Set file doesn't exists and will be skipped!".format(self.__class__.__name__, iblSet.title))

		if success:
			return True
		else:
			raise Exception, "{0} | Exception raised while opening '{1}' Ibl Sets directories!".format(self.__class__.__name__, ", ".join(iblSet.title for iblSet in selectedIblSets))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, OSError)
	def openInspectorIblSetLocations__(self):
		"""
		This method opens **coreInspector** Ibl Set directory.

		:return: Method success. ( Boolean )
		"""

		inspectorIblSet = self.__coreInspector.inspectorIblSet
		inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
		if inspectorIblSet:
			return self.exploreDirectory(os.path.dirname(inspectorIblSet.path), str(self.ui.Custom_File_Browser_Path_lineEdit.text()))
		else:
			raise OSError, "{0} | Exception raised while opening Inspector Ibl Set directory: '{1}' Ibl Set file doesn't exists!".format(self.__class__.__name__, inspectorIblSet.title)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def openComponentsLocations__(self):
		"""
		This method opens selected Components directories.

		:return: Method success. ( Boolean )
		"""

		selectedComponents = self.__coreComponentsManagerUi.getSelectedComponents()

		success = True
		for component in selectedComponents:
			path = component.path and os.path.exists(component.path) and component.path
			if path:
				success *= self.exploreDirectory(path, str(self.ui.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Component file doesn't exists and will be skipped!".format(self.__class__.__name__, component.name))

		if success:
			return True
		else:
			raise Exception, "{0} | Exception raised while opening '{1}' Components directories!".format(self.__class__.__name__, ", ".join(component.name for component in selectedComponents))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def openTemplatesLocations__(self):
		"""
		This method opens selected Templates directories.

		:return: Method success. ( Boolean )
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()

		success = True
		for template in selectedTemplates:
			path = template.path and os.path.exists(template.path) and os.path.dirname(template.path)
			if path:
				success *= self.exploreDirectory(path, str(self.ui.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Template file doesn't exists and will be skipped!".format(self.__class__.__name__, template.name))

		if success:
			return True
		else:
			raise Exception, "{0} | Exception raised while opening '{1}' Templates directories!".format(self.__class__.__name__, ", ".join(template.name for template in selectedTemplates))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, OSError, Exception)
	def openOutputDirectory__(self):
		"""
		This method opens output directory.

		:return: Method success. ( Boolean )
		"""

		directory = self.__container.parameters.loaderScriptsOutputDirectory and self.__container.parameters.loaderScriptsOutputDirectory or self.__addonsLoaderScript.ioDirectory

		if not os.path.exists(directory):
			raise OSError, "{0} | '{1}' loader Script output directory doesn't exists!".format(self.__class__.__name__, directory)

		if self.exploreDirectory(directory, str(self.ui.Custom_File_Browser_Path_lineEdit.text())):
			return True
		else:
			raise Exception, "{0} | Exception raised while exploring '{1}' directory!".format(self.__class__.__name__, directory)

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
							if os.path.exists(os.path.join(path, browser)):
								processCommand = "\"{0}\" \"{1}\"".format(browser, directory)
								browserFound = True
								raise StopIteration
					except StopIteration:
						pass

				if not browserFound:
					raise Exception, "{0} | Exception raised: No suitable Linux browser found!".format(self.__class__.__name__)
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
			raise Exception, "{0} | Exception raised: No suitable process command provided!".format(self.__class__.__name__)

