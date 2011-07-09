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
***	rawEditingUtilities.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Raw Editing Utilities Component Module.
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
import foundations.core as core
import foundations.exceptions
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
class RawEditingUtilities(UiComponent):
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

		self.__uiPath = "ui/Raw_Editing_Utilities.ui"

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None
		self.__coreTemplatesOutliner = None

		self.__editIblSetsInTextEditorAction = None
		self.__editInspectorIblSetInTextEditorAction = None
		self.__editTemplateInTextEditorAction = None

		self.__linuxTextEditors = ("gedit", "kwrite", "nedit", "mousepad")

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
	def coreInspector(self):
		"""
		This Method Is The Property For The _coreInspector Attribute.

		@return: self.__coreInspector. ( Object )
		"""

		return self.__coreInspector

	@coreInspector.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self, value):
		"""
		This Method Is The Setter Method For The _coreInspector Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreInspector"))

	@coreInspector.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self):
		"""
		This Method Is The Deleter Method For The _coreInspector Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreInspector"))

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
	def editIblSetsInTextEditorAction(self):
		"""
		This Method Is The Property For The _editIblSetsInTextEditorAction Attribute.

		@return: self.__editIblSetsInTextEditorAction. ( QAction )
		"""

		return self.__editIblSetsInTextEditorAction

	@editIblSetsInTextEditorAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editIblSetsInTextEditorAction(self, value):
		"""
		This Method Is The Setter Method For The _editIblSetsInTextEditorAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("editIblSetsInTextEditorAction"))

	@editIblSetsInTextEditorAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editIblSetsInTextEditorAction(self):
		"""
		This Method Is The Deleter Method For The _editIblSetsInTextEditorAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("editIblSetsInTextEditorAction"))

	@property
	def editInspectorIblSetInTextEditorAction(self):
		"""
		This Method Is The Property For The _editInspectorIblSetInTextEditorAction Attribute.

		@return: self.__editInspectorIblSetInTextEditorAction. ( QAction )
		"""

		return self.__editInspectorIblSetInTextEditorAction

	@editInspectorIblSetInTextEditorAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectorIblSetInTextEditorAction(self, value):
		"""
		This Method Is The Setter Method For The _editInspectorIblSetInTextEditorAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("editInspectorIblSetInTextEditorAction"))

	@editInspectorIblSetInTextEditorAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectorIblSetInTextEditorAction(self):
		"""
		This Method Is The Deleter Method For The _editInspectorIblSetInTextEditorAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("editInspectorIblSetInTextEditorAction"))

	@property
	def editTemplateInTextEditorAction(self):
		"""
		This Method Is The Property For The _editTemplateInTextEditorAction Attribute.

		@return: self.__editTemplateInTextEditorAction. ( QAction )
		"""

		return self.__editTemplateInTextEditorAction

	@editTemplateInTextEditorAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editTemplateInTextEditorAction(self, value):
		"""
		This Method Is The Setter Method For The _editTemplateInTextEditorAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("editTemplateInTextEditorAction"))

	@editTemplateInTextEditorAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editTemplateInTextEditorAction(self):
		"""
		This Method Is The Deleter Method For The _editTemplateInTextEditorAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("editTemplateInTextEditorAction"))

	@property
	def linuxTextEditors(self):
		"""
		This Method Is The Property For The _linuxTextEditors Attribute.

		@return: self.__linuxTextEditors. ( Tuple )
		"""

		return self.__linuxTextEditors

	@linuxTextEditors.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxTextEditors(self, value):
		"""
		This Method Is The Setter Method For The _linuxTextEditors Attribute.

		@param value: Attribute Value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("linuxTextEditors"))

	@linuxTextEditors.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxTextEditors(self):
		"""
		This Method Is The Deleter Method For The _linuxTextEditors Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("linuxTextEditors"))

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

		self.__corePreferencesManager = self.__container.componentsManager.components["core.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreInspector = self.__container.componentsManager.components["core.inspector"].interface
		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface

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

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None
		self.__coreTemplatesOutliner = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__Custom_Text_Editor_Path_lineEdit_setUi()

		self.__addActions()

		# Signals / Slots.
		self.ui.Custom_Text_Editor_Path_toolButton.clicked.connect(self.__Custom_Text_Editor_Path_toolButton__clicked)
		self.ui.Custom_Text_Editor_Path_lineEdit.editingFinished.connect(self.__Custom_Text_Editor_Path_lineEdit__editFinished)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Custom_Text_Editor_Path_toolButton.clicked.disconnect(self.__Custom_Text_Editor_Path_toolButton__clicked)
		self.ui.Custom_Text_Editor_Path_lineEdit.editingFinished.disconnect(self.__Custom_Text_Editor_Path_lineEdit__editFinished)

		self.__removeActions()

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Custom_Text_Editor_Path_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self.ui)
		self.ui.Custom_Text_Editor_Path_groupBox.setParent(None)

	@core.executionTrace
	def __addActions(self):
		"""
		This Method Adds Actions.
		"""

		LOGGER.debug("> Adding '{0}' Component Actions.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			self.__editIblSetsInTextEditorAction = QAction("Edit In Text Editor ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
			self.__editIblSetsInTextEditorAction.triggered.connect(self.__Database_Browser_listView_editIblSetsInTextEditorAction__triggered)
			self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__editIblSetsInTextEditorAction)

			self.__editInspectorIblSetInTextEditorAction = QAction("Edit In Text Editor ...", self.__coreInspector.ui.Inspector_Overall_frame)
			self.__editInspectorIblSetInTextEditorAction.triggered.connect(self.__Inspector_Overall_frame_editInspectorIblSetInTextEditorAction__triggered)
			self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__editInspectorIblSetInTextEditorAction)

			self.__editTemplateInTextEditorAction = QAction("Edit In Text Editor ...", self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView)
			self.__editTemplateInTextEditorAction.triggered.connect(self.__Templates_Outliner_treeView_editTemplateInTextEditorAction__triggered)
			self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.addAction(self.__editTemplateInTextEditorAction)

		else:
			LOGGER.info("{0} | Text Editing Capabilities Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __removeActions(self):
		"""
		This Method Removes Actions.
		"""

		LOGGER.debug("> Removing '{0}' Component Actions.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			self.__coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self.__editIblSetsInTextEditorAction)
			self.__editIblSetsInTextEditorAction = None

			self.__coreInspector.ui.Inspector_Overall_frame.removeAction(self.__editInspectorIblSetInTextEditorAction)
			self.__editInspectorIblSetInTextEditorAction = None

			self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.removeAction(self.__editTemplateInTextEditorAction)
			self.__editTemplateInTextEditorAction = None

	@core.executionTrace
	def __Database_Browser_listView_editIblSetsInTextEditorAction__triggered(self, checked):
		"""
		This Method Is Triggered By editIblSetsInTextEditorAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.editIblSetsInTextEditor__()

	@core.executionTrace
	def __Inspector_Overall_frame_editInspectorIblSetInTextEditorAction__triggered(self, checked):
		"""
		This Method Is Triggered By editInspectorIblSetInTextEditorAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.editInspectorIblSetInTextEditor__()

	@core.executionTrace
	def __Templates_Outliner_treeView_editTemplateInTextEditorAction__triggered(self, checked):
		"""
		This Method Is Triggered By editTemplateInTextEditorAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.editTemplatesInTextEditor__()

	@core.executionTrace
	def __Custom_Text_Editor_Path_lineEdit_setUi(self):
		"""
		This Method Fills The Custom_Text_Editor_Path_lineEdit.
		"""

		customTextEditor = self.__settings.getKey(self.__settingsSection, "customTextEditor")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("Custom_Text_Editor_Path_lineEdit", customTextEditor.toString()))
		self.ui.Custom_Text_Editor_Path_lineEdit.setText(customTextEditor.toString())

	@core.executionTrace
	def __Custom_Text_Editor_Path_toolButton__clicked(self, checked):
		"""
		This Method Is Called When Custom_Text_Editor_Path_toolButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		customTextEditorExecutable = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom Text Editor Executable:", self.__container.lastBrowsedPath))
		if customTextEditorExecutable != "":
			LOGGER.debug("> Chosen Custom Text Editor Executable: '{0}'.".format(customTextEditorExecutable))
			self.ui.Custom_Text_Editor_Path_lineEdit.setText(QString(customTextEditorExecutable))
			self.__settings.setKey(self.__settingsSection, "customTextEditor", self.ui.Custom_Text_Editor_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __Custom_Text_Editor_Path_lineEdit__editFinished(self):
		"""
		This Method Is Called When Custom_Text_Editor_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.Custom_Text_Editor_Path_lineEdit.text()))) and str(self.ui.Custom_Text_Editor_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring Preferences!")
			self.__Custom_Text_Editor_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid Custom Text Editor Executable File!".format(self.__class__.__name__)
		else:
			self.__settings.setKey(self.__settingsSection, "customTextEditor", self.ui.Custom_Text_Editor_Path_lineEdit.text())

	@core.executionTrace
	def editIblSetsInTextEditor__(self):
		"""
		This Method Edits Selected Ibl Sets.

		@return: Method Success. ( Boolean )		
		"""

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()

		success = True
		for iblSet in selectedIblSets:
			path = iblSet.path and os.path.exists(iblSet.path) and iblSet.path
			if path:
				success *= self.editFile(path, self.ui.Custom_Text_Editor_Path_lineEdit.text()) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Ibl Set File Doesn't Exists And Will Be Skipped!".format(self.__class__.__name__, iblSet.name))

		if success: return True
		else: raise Exception, "{0} | Exception Raised While Editing '{1}' Ibl Sets!".format(self.__class__.__name__, ", ".join(iblSet.name for iblSet in selectedIblSets))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, OSError)
	def editInspectorIblSetInTextEditor__(self):
		"""
		This Method Edits Inspector Ibl Set.

		@return: Method Success. ( Boolean )		
		"""

		inspectorIblSet = self.__coreInspector.inspectorIblSet
		inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
		if inspectorIblSet:
			return self.editFile(inspectorIblSet.path, str(self.ui.Custom_Text_Editor_Path_lineEdit.text()))
		else:
			raise OSError, "{0} | Exception Raised While Editing Inspector Ibl Set: '{1}' Ibl Set File Doesn't Exists!".format(self.__class__.__name__, inspectorIblSet.name)

	@core.executionTrace
	def editTemplatesInTextEditor__(self):
		"""
		This Method Edits Selected Templates.

		@return: Method Success. ( Boolean )		
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()

		success = True
		for template in selectedTemplates:
			path = template.path and os.path.exists(template.path) and template.path
			if path:
				success *= self.editFile(path, self.ui.Custom_Text_Editor_Path_lineEdit.text()) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Template File Doesn't Exists And Will Be Skipped!".format(self.__class__.__name__, template.name))

		if success: return True
		else: raise Exception, "{0} | Exception Raised While Editing '{1}' Templates!".format(self.__class__.__name__, ", ".join(template.name for template in selectedTemplates))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProcessCommand(self, file, customTextEditor=None):
		"""
		This Method Gets Process Command.

		@param file: File To Edit. ( String )
		@param customTextEditor: Custom Text Editor. ( String )
		@return: Process Command. ( String )		
		"""

		processCommand = None
		file = os.path.normpath(file)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			if customTextEditor:
				processCommand = "\"{0}\" \"{1}\"".format(customTextEditor, file)
			else:
				processCommand = "notepad.exe \"{0}\"".format(file)
		elif platform.system() == "Darwin":
			if customTextEditor:
				processCommand = "open -a \"{0}\" \"{1}\"".format(customTextEditor, file)
			else:
				processCommand = "open -e \"{0}\"".format(file)
		elif platform.system() == "Linux":
			if customTextEditor:
				processCommand = "\"{0}\" \"{1}\"".format(customTextEditor, file)
			else:
				environmentVariable = Environment("PATH")
				paths = environmentVariable.getPath().split(":")

				editorFound = False
				for editor in self.__linuxTextEditors:
					if editorFound: break

					try:
						for path in paths:
							if os.path.exists(os.path.join(path, editor)):
								processCommand = "\"{0}\" \"{1}\"".format(editor, file)
								editorFound = True
								raise StopIteration
					except StopIteration:
						pass

				if not editorFound:
					raise Exception, "{0} | Exception Raised: No Suitable Linux Editor Found!".format(self.__class__.__name__)
		return processCommand

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def editFile(self, file, customTextEditor=None):
		"""
		This Method Provides Editing Capability.

		@param file: File To Edit. ( String )
		@param customTextEditor: Custom Text Editor. ( String )
		@return: Method Success. ( Boolean )
		"""

		editCommand = self.getProcessCommand(file, customTextEditor)
		if editCommand:
			LOGGER.debug("> Current Edit Command: '{0}'.".format(editCommand))
			LOGGER.info("{0} | Launching Text Editor With '{1}' File.".format(self.__class__.__name__, file))
			editProcess = QProcess()
			editProcess.startDetached(editCommand)
			return True
		else:
			raise Exception, "{0} | Exception Raised: No Suitable Process Command Provided!".format(self.__class__.__name__)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
