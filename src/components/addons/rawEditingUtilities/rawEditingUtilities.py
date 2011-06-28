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
		self.__editInspectedIblSetInTextEditorAction = None
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
	def editInspectedIblSetInTextEditorAction(self):
		"""
		This Method Is The Property For The _editInspectedIblSetInTextEditorAction Attribute.

		@return: self.__editInspectedIblSetInTextEditorAction. ( QAction )
		"""

		return self.__editInspectedIblSetInTextEditorAction

	@editInspectedIblSetInTextEditorAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectedIblSetInTextEditorAction(self, value):
		"""
		This Method Is The Setter Method For The _editInspectedIblSetInTextEditorAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("editInspectedIblSetInTextEditorAction"))

	@editInspectedIblSetInTextEditorAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectedIblSetInTextEditorAction(self):
		"""
		This Method Is The Deleter Method For The _editInspectedIblSetInTextEditorAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("editInspectedIblSetInTextEditorAction"))

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

		self.Custom_Text_Editor_Path_lineEdit_setUi()

		self.addActions_()

		# Signals / Slots.
		self.ui.Custom_Text_Editor_Path_toolButton.clicked.connect(self.Custom_Text_Editor_Path_toolButton_OnClicked)
		self.ui.Custom_Text_Editor_Path_lineEdit.editingFinished.connect(self.Custom_Text_Editor_Path_lineEdit_OnEditFinished)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Custom_Text_Editor_Path_toolButton.clicked.disconnect(self.Custom_Text_Editor_Path_toolButton_OnClicked)
		self.ui.Custom_Text_Editor_Path_lineEdit.editingFinished.disconnect(self.Custom_Text_Editor_Path_lineEdit_OnEditFinished)

		self.removeActions_()

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
	def addActions_(self):
		"""
		This Method Adds Actions.
		"""

		LOGGER.debug("> Adding '{0}' Component Actions.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			self.__editIblSetsInTextEditorAction = QAction("Edit In Text Editor ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
			self.__editIblSetsInTextEditorAction.triggered.connect(self.Database_Browser_listView_editIblSetsInTextEditorAction_OnTriggered)
			self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__editIblSetsInTextEditorAction)

			self.__editInspectedIblSetInTextEditorAction = QAction("Edit In Text Editor ...", self.__coreInspector.ui.Inspector_Overall_frame)
			self.__editInspectedIblSetInTextEditorAction.triggered.connect(self.Inspector_Overall_frame_editInspectedIblSetInTextEditorAction_OnTriggered)
			self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__editInspectedIblSetInTextEditorAction)

			self.__editTemplateInTextEditorAction = QAction("Edit In Text Editor ...", self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView)
			self.__editTemplateInTextEditorAction.triggered.connect(self.Templates_Outliner_treeView_editTemplateInTextEditorAction_OnTriggered)
			self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.addAction(self.__editTemplateInTextEditorAction)

		else:
			LOGGER.info("{0} | Text Editing Capabilities Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def removeActions_(self):
		"""
		This Method Removes Actions.
		"""

		LOGGER.debug("> Removing '{0}' Component Actions.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			self.__coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self.__editIblSetsInTextEditorAction)
			self.__editIblSetsInTextEditorAction = None

			self.__coreInspector.ui.Inspector_Overall_frame.removeAction(self.__editInspectedIblSetInTextEditorAction)
			self.__editInspectedIblSetInTextEditorAction = None

			self.__coreTemplatesOutliner.ui.Templates_Outliner_treeView.removeAction(self.__editTemplateInTextEditorAction)
			self.__editTemplateInTextEditorAction = None

	@core.executionTrace
	def Database_Browser_listView_editIblSetsInTextEditorAction_OnTriggered(self, checked):
		"""
		This Method Is Triggered By editIblSetsInTextEditorAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedItems()
		for iblSet in selectedIblSets:
			iblSet._datas.path and os.path.exists(iblSet._datas.path) and self.editProvidedfile(iblSet._datas.path)

	@core.executionTrace
	def Inspector_Overall_frame_editInspectedIblSetInTextEditorAction_OnTriggered(self, checked):
		"""
		This Method Is Triggered By editInspectedIblSetInTextEditorAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedItems()
		selectedIblSet = selectedIblSets and os.path.exists(selectedIblSets[0]._datas.path) and selectedIblSets[0] or None
		selectedIblSet and self.editProvidedfile(selectedIblSet._datas.path)

	@core.executionTrace
	def Templates_Outliner_treeView_editTemplateInTextEditorAction_OnTriggered(self, checked):
		"""
		This Method Is Triggered By editTemplateInTextEditorAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()
		if selectedTemplates:
			for template in selectedTemplates:
				os.path.exists(template._datas.path) and self.editProvidedfile(template._datas.path)

	@core.executionTrace
	def Custom_Text_Editor_Path_lineEdit_setUi(self):
		"""
		This Method Fills The Custom_Text_Editor_Path_lineEdit.
		"""

		customTextEditor = self.__settings.getKey(self.__settingsSection, "customTextEditor")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("Custom_Text_Editor_Path_lineEdit", customTextEditor.toString()))
		self.ui.Custom_Text_Editor_Path_lineEdit.setText(customTextEditor.toString())

	@core.executionTrace
	def Custom_Text_Editor_Path_toolButton_OnClicked(self, checked):
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
	def Custom_Text_Editor_Path_lineEdit_OnEditFinished(self):
		"""
		This Method Is Called When Custom_Text_Editor_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.Custom_Text_Editor_Path_lineEdit.text()))) and str(self.ui.Custom_Text_Editor_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring Preferences!")
			self.Custom_Text_Editor_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid Custom Text Editor Executable File!".format(self.__class__.__name__)
		else:
			self.__settings.setKey(self.__settingsSection, "customTextEditor", self.ui.Custom_Text_Editor_Path_lineEdit.text())

	@core.executionTrace
	def editProvidedfile(self, file):
		"""
		This Method Provides Editing Capability.

		@param file: File To Edit. ( String )
		"""

		editCommand = None
		customTextEditor = str(self.ui.Custom_Text_Editor_Path_lineEdit.text())

		file = os.path.normpath(file)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			if customTextEditor:
				LOGGER.info("{0} | Launching '{1}' Custom Text Editor With '{2}'.".format(self.__class__.__name__, os.path.basename(customTextEditor), file))
				editCommand = "\"{0}\" \"{1}\"".format(customTextEditor, file)
			else:
				LOGGER.info("{0} | Launching 'notepad.exe' With '{1}'.".format(self.__class__.__name__, file))
				editCommand = "notepad.exe \"{0}\"".format(file)
		elif platform.system() == "Darwin":
			if customTextEditor:
				LOGGER.info("{0} | Launching '{1}' Custom Text Editor With '{2}'.".format(self.__class__.__name__, os.path.basename(customTextEditor), file))
				editCommand = "open -a \"{0}\" \"{1}\"".format(customTextEditor, file)
			else:
				LOGGER.info("{0} | Launching Default Text Editor With '{1}'.".format(self.__class__.__name__, file))
				editCommand = "open -e \"{0}\"".format(file)
		elif platform.system() == "Linux":
			if customTextEditor:
				LOGGER.info("{0} | Launching '{1}' Custom Text Editor With '{2}'.".format(self.__class__.__name__, os.path.basename(customTextEditor), file))
				editCommand = "\"{0}\" \"{1}\"".format(customTextEditor, file)
			else:
				environmentVariable = Environment("PATH")
				paths = environmentVariable.getPath().split(":")

				editorFound = False
				for editor in self.__linuxTextEditors:
					if not editorFound:
						try:
							for path in paths:
								if os.path.exists(os.path.join(path, editor)):
									LOGGER.info("{0} | Launching '{1}' Text Editor With '{2}'.".format(self.__class__.__name__, editor, file))
									editCommand = "\"{0}\" \"{1}\"".format(editor, file)
									editorFound = True
									raise StopIteration
						except StopIteration:
							pass
					else:
						break
		if editCommand:
			LOGGER.debug("> Current Edit Command: '{0}'.".format(editCommand))
			editProcess = QProcess()
			editProcess.startDetached(editCommand)
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | Please Define A Text Editor Executable In The Preferences!".format(self.__class__.__name__))

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
