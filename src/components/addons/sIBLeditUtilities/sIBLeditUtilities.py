#!/usr/bin/env python
# -*- coding: utf-8 -*-
import foundations

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
***	sIBLeditUtilities.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		sIBLedit Utilities Component Module.
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
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class sIBLeditUtilities(UiComponent):
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

		self.__uiPath = "ui/sIBLedit_Utilities.ui"

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None

		self.__editIblSetInSIBLEditAction = None
		self.__editInspectorIblSetInSIBLEditAction = None

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
	def editIblSetInSIBLEditAction(self):
		"""
		This Method Is The Property For The _editIblSetInSIBLEditAction Attribute.

		@return: self.__editIblSetInSIBLEditAction. ( QAction )
		"""

		return self.__editIblSetInSIBLEditAction

	@editIblSetInSIBLEditAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editIblSetInSIBLEditAction(self, value):
		"""
		This Method Is The Setter Method For The _editIblSetInSIBLEditAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("editIblSetInSIBLEditAction"))

	@editIblSetInSIBLEditAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editIblSetInSIBLEditAction(self):
		"""
		This Method Is The Deleter Method For The _editIblSetInSIBLEditAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("editIblSetInSIBLEditAction"))

	@property
	def editInspectorIblSetInSIBLEditAction(self):
		"""
		This Method Is The Property For The _editInspectorIblSetInSIBLEditAction Attribute.

		@return: self.__editInspectorIblSetInSIBLEditAction. ( QAction )
		"""

		return self.__editInspectorIblSetInSIBLEditAction

	@editInspectorIblSetInSIBLEditAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectorIblSetInSIBLEditAction(self, value):
		"""
		This Method Is The Setter Method For The _editInspectorIblSetInSIBLEditAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("editInspectorIblSetInSIBLEditAction"))

	@editInspectorIblSetInSIBLEditAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectorIblSetInSIBLEditAction(self):
		"""
		This Method Is The Deleter Method For The _editInspectorIblSetInSIBLEditAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("editInspectorIblSetInSIBLEditAction"))

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

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__sIBLedit_Path_lineEdit_setUi()

		self.__addActions()

		# Signals / Slots.
		self.ui.sIBLedit_Path_toolButton.clicked.connect(self.__sIBLedit_Path_toolButton__clicked)
		self.ui.sIBLedit_Path_lineEdit.editingFinished.connect(self.__sIBLedit_Path_lineEdit__editFinished)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.sIBLedit_Path_toolButton.clicked.disconnect(self.__sIBLedit_Path_toolButton__clicked)
		self.ui.sIBLedit_Path_lineEdit.editingFinished.disconnect(self.__sIBLedit_Path_lineEdit__editFinished)

		self.__removeActions()

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.sIBLedit_Path_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.ui.sIBLedit_Path_groupBox.setParent(None)

	@core.executionTrace
	def __addActions(self):
		"""
		This Method Adds Actions.
		"""

		LOGGER.debug("> Adding '{0}' Component Actions.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			self.__editIblSetInSIBLEditAction = QAction("Edit In sIBLedit ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
			self.__editIblSetInSIBLEditAction.triggered.connect(self.__Database_Browser_listView_editIblSetInSIBLEditAction__triggered)
			self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__editIblSetInSIBLEditAction)

			self.__editInspectorIblSetInSIBLEditAction = QAction("Edit In sIBLedit ...", self.__coreInspector.ui.Inspector_Overall_frame)
			self.__editInspectorIblSetInSIBLEditAction.triggered.connect(self.__Inspector_Overall_frame_editInspectorIblSetInSIBLEditAction__triggered)
			self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__editInspectorIblSetInSIBLEditAction)
		else:
			LOGGER.info("{0} | sIBLedit Editing Capabilities Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __removeActions(self):
		"""
		This Method Removes Actions.
		"""

		LOGGER.debug("> Removing '{0}' Component Actions.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			self.__coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self.__editIblSetInSIBLEditAction)
			self.__editIblSetInSIBLEditAction = None

			self.__coreInspector.ui.Inspector_Overall_frame.removeAction(self.__editInspectorIblSetInSIBLEditAction)
			self.__editInspectorIblSetInSIBLEditAction = None

	@core.executionTrace
	def __Database_Browser_listView_editIblSetInSIBLEditAction__triggered(self, checked):
		"""
		This Method Is Triggered By editIblSetInSIBLEditAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.editIblSetInSIBLEdit__()

	@core.executionTrace
	def __Inspector_Overall_frame_editInspectorIblSetInSIBLEditAction__triggered(self, checked):
		"""
		This Method Is Triggered By editInspectorIblSetInSIBLEditAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.editInspectorIblSetInSIBLEdit__()

	@core.executionTrace
	def __sIBLedit_Path_lineEdit_setUi(self):
		"""
		This Method Fills The sIBLedit_Path_lineEdit.
		"""

		sIBLeditExecutable = self.__settings.getKey(self.__settingsSection, "sIBLeditExecutable")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("sIBLedit_Path_lineEdit", sIBLeditExecutable.toString()))
		self.ui.sIBLedit_Path_lineEdit.setText(sIBLeditExecutable.toString())

	@core.executionTrace
	def __sIBLedit_Path_toolButton__clicked(self, checked):
		"""
		This Method Is Called When sIBLedit_Path_toolButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		sIBLeditExecutable = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "sIBLedit Executable:", self.__container.lastBrowsedPath))
		if sIBLeditExecutable != "":
			LOGGER.debug("> Chosen sIBLedit Executable: '{0}'.".format(sIBLeditExecutable))
			self.ui.sIBLedit_Path_lineEdit.setText(QString(sIBLeditExecutable))
			self.__settings.setKey(self.__settingsSection, "sIBLeditExecutable", self.ui.sIBLedit_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __sIBLedit_Path_lineEdit__editFinished(self):
		"""
		This Method Is Called When sIBLedit_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.sIBLedit_Path_lineEdit.text()))) and str(self.ui.sIBLedit_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring Preferences!")
			self.__sIBLedit_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid sIBLedit Executable File!".format(self.__class__.__name__)
		else:
			self.__settings.setKey(self.__settingsSection, "sIBLeditExecutable", self.ui.sIBLedit_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, OSError)
	def editIblSetInSIBLEdit__(self):
		"""
		This Method Edits Selected Ibl Set In sIBLedit.
		
		@return: Method Success. ( Boolean )		
		"""

		sIBLedit = str(self.ui.sIBLedit_Path_lineEdit.text())
		if sIBLedit:
			selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
			selectedIblSet = selectedIblSets and os.path.exists(selectedIblSets[0].path) and selectedIblSets[0] or None
			if selectedIblSet:
				return self.editIblSetInSIBLedit(selectedIblSet.path, str(self.ui.sIBLedit_Path_lineEdit.text()))
			else:
				raise OSError, "{0} | Exception Raised While Sending Ibl Set To sIBLedit: '{1}' Ibl Set File Doesn't Exists!".format(self.__class__.__name__, selectedIblSet.name)
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | Please Define An 'sIBLedit' Executable In The Preferences!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, OSError)
	def editInspectorIblSetInSIBLEdit__(self):
		"""
		This Method Edits Inspector Ibl Set In sIBLedit.
		
		@return: Method Success. ( Boolean )		
		"""

		sIBLedit = str(self.ui.sIBLedit_Path_lineEdit.text())
		if sIBLedit:
			inspectorIblSet = self.__coreInspector.inspectorIblSet
			inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
			if inspectorIblSet:
				return self.editIblSetInSIBLedit(inspectorIblSet.path, sIBLedit)
			else:
				raise OSError, "{0} | Exception Raised While Sending Inspector Ibl Set To sIBLedit: '{1}' Ibl Set File Doesn't Exists!".format(self.__class__.__name__, inspectorIblSet.name)
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | Please Define An 'sIBLedit' Executable In The Preferences!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProcessCommand(self, path, sIBLedit):
		"""
		This Method Gets Process Command.

		@param path: Path. ( String )
		@param sIBLedit: sIBLedit. ( String )
		@return: Process Command. ( String )		
		"""

		return "\"{0}\" \"{1}\"".format(sIBLedit, path)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def editIblSetInSIBLedit(self, path, sIBLedit):
		"""
		This Method Edits Provided Ibl Set In sIBLedit.
		
		@param path: Path. ( String )
		@param sIBLedit: sIBLedit. ( String )
		@return: Method Success. ( Boolean )		
		"""

		editCommand = self.getProcessCommand(path, sIBLedit)
		if editCommand:
			LOGGER.debug("> Current Edit Command: '{0}'.".format(editCommand))
			LOGGER.info("{0} | Launching 'sIBLedit' With '{1}'.".format(self.__class__.__name__, path))
			editProcess = QProcess()
			editProcess.startDetached(editCommand)
			return True
		else:
			raise Exception, "{0} | Exception Raised: No Suitable Process Command Provided!".format(self.__class__.__name__)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
