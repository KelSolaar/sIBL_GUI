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
***	locationsBrowser.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Locations Browser Component Module.
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
import logging
import os
import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import ui.common
import ui.widgets.messageBox as messageBox
from foundations.environment import Environment
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class LocationsBrowser(UiComponent):
	"""
	This Class Is The LocationsBrowser Class.
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

		# --- Setting Class Attributes. ---
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

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
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

	@property
	def settingsSection(self):
		"""
		This Method Is The Property For The _settingsSection Attribute.

		@return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This Method Is The Setter Method For The _settingsSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This Method Is The Deleter Method For The _settingsSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settingsSection"))

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
	def addonsLoaderScript(self):
		"""
		This Method Is The Property For The _addonsLoaderScript Attribute.

		@return: self.__addonsLoaderScript. ( Object )
		"""

		return self.__addonsLoaderScript

	@addonsLoaderScript.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self, value):
		"""
		This Method Is The Setter Method For The _addonsLoaderScript Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("addonsLoaderScript"))

	@addonsLoaderScript.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLoaderScript(self):
		"""
		This Method Is The Deleter Method For The _addonsLoaderScript Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("addonsLoaderScript"))

	@property
	def openIblSetsLocationsAction(self):
		"""
		This Method Is The Property For The _openIblSetsLocationsAction Attribute.

		@return: self.__openIblSetsLocationsAction. ( QAction )
		"""

		return self.__openIblSetsLocationsAction

	@openIblSetsLocationsAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openIblSetsLocationsAction(self, value):
		"""
		This Method Is The Setter Method For The _openIblSetsLocationsAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("openIblSetsLocationsAction"))

	@openIblSetsLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openIblSetsLocationsAction(self):
		"""
		This Method Is The Deleter Method For The _openIblSetsLocationsAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("openIblSetsLocationsAction"))

	@property
	def openInspectorIblSetLocationsAction(self):
		"""
		This Method Is The Property For The _openInspectorIblSetLocationsAction Attribute.

		@return: self.__openInspectorIblSetLocationsAction. ( QAction )
		"""

		return self.__openInspectorIblSetLocationsAction

	@openInspectorIblSetLocationsAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openInspectorIblSetLocationsAction(self, value):
		"""
		This Method Is The Setter Method For The _openInspectorIblSetLocationsAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("openInspectorIblSetLocationsAction"))

	@openInspectorIblSetLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openInspectorIblSetLocationsAction(self):
		"""
		This Method Is The Deleter Method For The _openInspectorIblSetLocationsAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("openInspectorIblSetLocationsAction"))

	@property
	def openComponentsLocationsAction(self):
		"""
		This Method Is The Property For The _openComponentsLocationsAction Attribute.

		@return: self.__openComponentsLocationsAction. ( QAction )
		"""

		return self.__openComponentsLocationsAction

	@openComponentsLocationsAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openComponentsLocationsAction(self, value):
		"""
		This Method Is The Setter Method For The _openComponentsLocationsAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("openComponentsLocationsAction"))

	@openComponentsLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openComponentsLocationsAction(self):
		"""
		This Method Is The Deleter Method For The _openComponentsLocationsAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("openComponentsLocationsAction"))

	@property
	def openTemplatesLocationsAction(self):
		"""
		This Method Is The Property For The _openTemplatesLocationsAction Attribute.

		@return: self.__openTemplatesLocationsAction. ( QAction )
		"""

		return self.__openTemplatesLocationsAction

	@openTemplatesLocationsAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openTemplatesLocationsAction(self, value):
		"""
		This Method Is The Setter Method For The _openTemplatesLocationsAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("openTemplatesLocationsAction"))

	@openTemplatesLocationsAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def openTemplatesLocationsAction(self):
		"""
		This Method Is The Deleter Method For The _openTemplatesLocationsAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("openTemplatesLocationsAction"))

	@property
	def Open_Output_Directory_pushButton(self):
		"""
		This Method Is The Property For The _Open_Output_Directory_pushButton Attribute.

		@return: self.__Open_Output_Directory_pushButton. ( QPushButton )
		"""

		return self.__Open_Output_Directory_pushButton

	@Open_Output_Directory_pushButton.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Open_Output_Directory_pushButton(self, value):
		"""
		This Method Is The Setter Method For The _Open_Output_Directory_pushButton Attribute.

		@param value: Attribute Value. ( QPushButton )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("Open_Output_Directory_pushButton"))

	@Open_Output_Directory_pushButton.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Open_Output_Directory_pushButton(self):
		"""
		This Method Is The Deleter Method For The _Open_Output_Directory_pushButton Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("Open_Output_Directory_pushButton"))

	@property
	def linuxBrowsers(self):
		"""
		This Method Is The Property For The _linuxBrowsers Attribute.

		@return: self.__linuxBrowsers. ( QObject )
		"""

		return self.__linuxBrowsers

	@linuxBrowsers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self, value):
		"""
		This Method Is The Setter Method For The _linuxBrowsers Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("linuxBrowsers"))

	@linuxBrowsers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self):
		"""
		This Method Is The Deleter Method For The _linuxBrowsers Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("linuxBrowsers"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
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
		This Method Deactivates The Component.
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
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))


		self.__Custom_File_Browser_Path_lineEdit_setUi()

		self.__addActions()

		# Signals / Slots.
		self.ui.Custom_File_Browser_Path_toolButton.clicked.connect(self.__Custom_File_Browser_Path_toolButton__clicked)
		self.ui.Custom_File_Browser_Path_lineEdit.editingFinished.connect(self.__Custom_File_Browser_Path_lineEdit__editFinished)

		# LoaderScript Addon Component Specific Code.
		if self.__addonsLoaderScript.activated:
			self.__Open_Output_Directory_pushButton = QPushButton("Open Output Directory")
			self.__addonsLoaderScript.ui.Loader_Script_verticalLayout.addWidget(self.__Open_Output_Directory_pushButton)

			# Signals / Slots.
			self.__Open_Output_Directory_pushButton.clicked.connect(self.__Open_Output_Directory_pushButton__clicked)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Custom_File_Browser_Path_toolButton.clicked.disconnect(self.__Custom_File_Browser_Path_toolButton__clicked)
		self.ui.Custom_File_Browser_Path_lineEdit.editingFinished.disconnect(self.__Custom_File_Browser_Path_lineEdit__editFinished)

		# LoaderScript Addon Component Specific Code.
		if self.__addonsLoaderScript.activated:
			# Signals / Slots.
			self.__Open_Output_Directory_pushButton.clicked.disconnect(self.__Open_Output_Directory_pushButton__clicked)

			self.__Open_Output_Directory_pushButton.setParent(None)
			self.__Open_Output_Directory_pushButton = None

		self.__removeActions()

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Custom_File_Browser_Path_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.ui.Custom_File_Browser_Path_groupBox.setParent(None)

	@core.executionTrace
	def __addActions(self):
		"""
		This Method Adds Actions.
		"""

		LOGGER.debug("> Adding '{0}' Component Actions.".format(self.__class__.__name__))

		self.__openIblSetsLocationsAction = QAction("Open Ibl Set(s) Location(s) ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
		self.__openIblSetsLocationsAction.triggered.connect(self.__Database_Browser_listView_openIblSetsLocationsAction__triggered)
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__openIblSetsLocationsAction)

		self.__openInspectorIblSetLocationsAction = QAction("Open Ibl Set Location ...", self.__coreInspector.ui.Inspector_Overall_frame)
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
		This Method Removes Actions.
		"""

		LOGGER.debug("> Removing '{0}' Component Actions.".format(self.__class__.__name__))

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
		This Method Is Triggered By openIblSetsLocationsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.openIblSetsLocations__()

	@core.executionTrace
	def __Inspector_Overall_frame_openInspectorIblSetLocationsAction__triggered(self, checked):
		"""
		This Method Is Triggered By openInspectorIblSetLocationsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.openInspectorIblSetLocations__()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_openComponentsLocationsAction__triggered(self, checked):
		"""
		This Method Is Triggered By openComponentsLocationsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.openComponentsLocations__()

	@core.executionTrace
	def __Templates_Outliner_treeView_openTemplatesLocationsAction__triggered(self, checked):
		"""
		This Method Is Triggered By openTemplatesLocationsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.openTemplatesLocations__()

	@core.executionTrace
	def __Custom_File_Browser_Path_lineEdit_setUi(self):
		"""
		This Method Fills The Custom_File_Browser_Path_lineEdit.
		"""

		customFileBrowser = self.__settings.getKey(self.__settingsSection, "customFileBrowser")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("Custom_File_Browser_Path_lineEdit", customFileBrowser.toString()))
		self.ui.Custom_File_Browser_Path_lineEdit.setText(customFileBrowser.toString())

	@core.executionTrace
	def __Custom_File_Browser_Path_toolButton__clicked(self, checked):
		"""
		This Method Is Called When Custom_File_Browser_Path_toolButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		customFileBrowserExecutable = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom File Browser Executable:", self.__container.lastBrowsedPath))
		if customFileBrowserExecutable != "":
			LOGGER.debug("> Chosen Custom File Browser Executable: '{0}'.".format(customFileBrowserExecutable))
			self.ui.Custom_File_Browser_Path_lineEdit.setText(QString(customFileBrowserExecutable))
			self.__settings.setKey(self.__settingsSection, "customFileBrowser", self.ui.Custom_File_Browser_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __Custom_File_Browser_Path_lineEdit__editFinished(self):
		"""
		This Method Is Called When Custom_File_Browser_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.Custom_File_Browser_Path_lineEdit.text()))) and str(self.ui.Custom_File_Browser_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring Preferences!")
			self.__Custom_File_Browser_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid Custom File Browser Executable File!".format(self.__class__.__name__)
		else:
			self.__settings.setKey(self.__settingsSection, "customFileBrowser", self.ui.Custom_File_Browser_Path_lineEdit.text())

	@core.executionTrace
	def __Open_Output_Directory_pushButton__clicked(self, checked):
		"""
		This Method Is Called When Open_Output_Directory_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.openOutputDirectory__()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, Exception)
	def openIblSetsLocations__(self):
		"""
		This Method Open Selected Ibl Sets Directories.

		@return: Method Success. ( Boolean )		
		"""

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()

		success = True
		for iblSet in selectedIblSets:
			path = iblSet.path and os.path.exists(iblSet.path) and os.path.dirname(iblSet.path)
			if path:
				success *= self.exploreDirectory(path, str(self.ui.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Ibl Set File Doesn't Exists And Will Be Skipped!".format(self.__class__.__name__, iblSet.name))

		if success: return True
		else: raise Exception, "{0} | Exception Raised While Opening '{1}' Ibl Sets Directories!".format(self.__class__.__name__, ", ".join(iblSet.name for iblSet in selectedIblSets))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, OSError)
	def openInspectorIblSetLocations__(self):
		"""
		This Method Opens Inspector Ibl Set Directory.

		@return: Method Success. ( Boolean )		
		"""

		inspectorIblSet = self.__coreInspector.inspectorIblSet
		inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
		if inspectorIblSet:
			return self.exploreDirectory(os.path.dirname(inspectorIblSet.path), str(self.ui.Custom_File_Browser_Path_lineEdit.text()))
		else:
			raise OSError, "{0} | Exception Raised While Opening Inspector Ibl Set Directory: '{1}' Ibl Set File Doesn't Exists!".format(self.__class__.__name__, inspectorIblSet.name)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, Exception)
	def openComponentsLocations__(self):
		"""
		This Method Opens Selected Components Directories.

		@return: Method Success. ( Boolean )		
		"""

		selectedComponents = self.__coreComponentsManagerUi.getSelectedComponents()

		success = True
		for component in selectedComponents:
			path = component.path and os.path.exists(component.path) and component.path
			if path:
				success *= self.exploreDirectory(path, str(self.ui.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Component File Doesn't Exists And Will Be Skipped!".format(self.__class__.__name__, component.name))

		if success: return True
		else: raise Exception, "{0} | Exception Raised While Opening '{1}' Components Directories!".format(self.__class__.__name__, ", ".join(component.name for component in selectedComponents))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, Exception)
	def openTemplatesLocations__(self):
		"""
		This Method Opens Selected Templates Directories.

		@return: Method Success. ( Boolean )		
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()

		success = True
		for template in selectedTemplates:
			path = template.path and os.path.exists(template.path) and os.path.dirname(template.path)
			if path:
				success *= self.exploreDirectory(path, str(self.ui.Custom_File_Browser_Path_lineEdit.text())) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Template File Doesn't Exists And Will Be Skipped!".format(self.__class__.__name__, template.name))

		if success: return True
		else: raise Exception, "{0} | Exception Raised While Opening '{1}' Templates Directories!".format(self.__class__.__name__, ", ".join(template.name for template in selectedTemplates))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, OSError, Exception)
	def openOutputDirectory__(self):
		"""
		This Method Opens Output Directory.

		@return: Method Success. ( Boolean )		
		"""

		directory = self.__container.parameters.loaderScriptsOutputDirectory and self.__container.parameters.loaderScriptsOutputDirectory or self.__addonsLoaderScript.ioDirectory

		if not os.path.exists(directory):
			raise OSError, "{0} | '{1}' Loader Script Output Directory Doesn't Exists!".format(self.__class__.__name__, directory)

		if self.exploreDirectory(directory, str(self.ui.Custom_File_Browser_Path_lineEdit.text())): return True
		else: raise Exception, "{0} | Exception Raised While Exploring '{1}' Directory!".format(self.__class__.__name__, directory)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProcessCommand(self, directory, customBrowser=None):
		"""
		This Method Gets Process Command.

		@param directory: Directory To Explore. ( String )
		@param customBrowser: Custom Browser. ( String )
		@return: Process Command. ( String )		
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
				paths = environmentVariable.getPath().split(":")

				browserFound = False
				for browser in self.__linuxBrowsers:
					if browserFound: break

					try:
						for path in paths:
							if os.path.exists(os.path.join(path, browser)):
								processCommand = "\"{0}\" \"{1}\"".format(browser, directory)
								browserFound = True
								raise StopIteration
					except StopIteration:
						pass

				if not browserFound:
					raise Exception, "{0} | Exception Raised: No Suitable Linux Browser Found!".format(self.__class__.__name__)
		return processCommand

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def exploreDirectory(self, directory, customBrowser=None):
		"""
		This Method Provides Directory Exploring Capability.

		@param directory: Directory To Explore. ( String )
		@param customBrowser: Custom Browser. ( String )
		@return: Method Success. ( Boolean )		
		"""

		browserCommand = self.getProcessCommand(directory, customBrowser)
		if browserCommand:
			LOGGER.debug("> Current Browser Command: '{0}'.".format(browserCommand))
			LOGGER.info("{0} | Launching File Browser With '{1}' Directory.".format(self.__class__.__name__, directory))
			browserProcess = QProcess()
			browserProcess.startDetached(browserCommand)
			return True
		else:
			raise Exception, "{0} | Exception Raised: No Suitable Process Command Provided!".format(self.__class__.__name__)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
