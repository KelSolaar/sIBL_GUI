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
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	sIBLeditUtilities.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		sIBLedit Utilities Component Module.
***
***	Others :
***
************************************************************************************************
'''

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
	'''
	This Class Is The LocationsBrowser Class.
	'''

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self._uiPath = "ui/sIBLedit_Utilities.ui"

		self._container = None
		self._settings = None
		self._settingsSection = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None

		self._editInSIBLEditAction = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("uiPath"))

	@property
	def container(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("container"))

	@property
	def settings(self):
		'''
		This Method Is The Property For The _settings Attribute.

		@return: self._settings. ( QSettings )
		'''

		return self._settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		'''
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		'''
		This Method Is The Deleter Method For The _settings Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("settings"))

	@property
	def settingsSection(self):
		'''
		This Method Is The Property For The _settingsSection Attribute.

		@return: self._settingsSection. ( String )
		'''

		return self._settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		'''
		This Method Is The Setter Method For The _settingsSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		'''
		This Method Is The Deleter Method For The _settingsSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("settingsSection"))

	@property
	def corePreferencesManager(self):
		'''
		This Method Is The Property For The _corePreferencesManager Attribute.

		@return: self._corePreferencesManager. ( Object )
		'''

		return self._corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self, value):
		'''
		This Method Is The Setter Method For The _corePreferencesManager Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("corePreferencesManager"))

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self):
		'''
		This Method Is The Deleter Method For The _corePreferencesManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("corePreferencesManager"))

	@property
	def coreDatabaseBrowser(self):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("coreDatabaseBrowser"))

	@property
	def editInSIBLEditAction(self):
		'''
		This Method Is The Property For The _editInSIBLEditAction Attribute.

		@return: self._editInSIBLEditAction. ( QAction )
		'''

		return self._editInSIBLEditAction

	@editInSIBLEditAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInSIBLEditAction(self, value):
		'''
		This Method Is The Setter Method For The _editInSIBLEditAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("editInSIBLEditAction"))

	@editInSIBLEditAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInSIBLEditAction(self):
		'''
		This Method Is The Deleter Method For The _editInSIBLEditAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("editInSIBLEditAction"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiPath)
		self._container = container
		self._settings = self._container.settings
		self._settingsSection = self.name

		self._corePreferencesManager = self._container.componentsManager.components["core.preferencesManager"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	def deactivate(self):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self._container = None
		self._settings = None
		self._settingsSection = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.sIBLedit_Path_lineEdit_setUi()

		self.addActions_()

		# Signals / Slots.
		self.ui.sIBLedit_Path_toolButton.clicked.connect(self.sIBLedit_Path_toolButton_OnClicked)
		self.ui.sIBLedit_Path_lineEdit.editingFinished.connect(self.sIBLedit_Path_lineEdit_OnEditFinished)

	@core.executionTrace
	def uninitializeUi(self):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.sIBLedit_Path_toolButton.clicked.disconnect(self.sIBLedit_Path_toolButton_OnClicked)
		self.ui.sIBLedit_Path_lineEdit.editingFinished.disconnect(self.sIBLedit_Path_lineEdit_OnEditFinished)

		self.removeActions_()

	@core.executionTrace
	def addWidget(self):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self._corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.sIBLedit_Path_groupBox)

	@core.executionTrace
	def removeWidget(self):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.ui.sIBLedit_Path_groupBox.setParent(None)

	@core.executionTrace
	def addActions_(self):
		'''
		This Method Adds Actions.
		'''

		LOGGER.debug("> Adding '{0}' Component Actions.".format(self.__class__.__name__))

		if not self._container.parameters.databaseReadOnly :
			self._editInSIBLEditAction = QAction("Edit In sIBLedit ...", self._coreDatabaseBrowser.ui.Database_Browser_listView)
			self._editInSIBLEditAction.triggered.connect(self.Database_Browser_listView_editInSIBLEditAction)
			self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self._editInSIBLEditAction)
		else :
			LOGGER.info("{0} | sIBLedit Link Deactivated By '{1}' Command Line Parameter Value !".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def removeActions_(self):
		'''
		This Method Removes Actions.
		'''

		LOGGER.debug("> Removing '{0}' Component Actions.".format(self.__class__.__name__))

		if not self._container.parameters.databaseReadOnly :
			self._coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self._editInSIBLEditAction)
			self._editInSIBLEditAction = None

	@core.executionTrace
	def Database_Browser_listView_editInSIBLEditAction(self, checked):
		'''
		This Method Is Triggered By editInSIBLEditAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		sIBLedit = str(self.ui.sIBLedit_Path_lineEdit.text())
		selectedIblSet = self._coreDatabaseBrowser.getSelectedItems()
		selectedIblSet = selectedIblSet and os.path.exists(selectedIblSet[0]._datas.path) and selectedIblSet[0] or None

		if sIBLedit :
			if selectedIblSet :
				LOGGER.info("{0} | Launching 'sIBLedit' With '{1}'.".format(self.__class__.__name__, selectedIblSet._datas.path))
				editCommand = "\"{0}\" \"{1}\"".format(sIBLedit, selectedIblSet._datas.path)

				LOGGER.debug("> Current Edit Command : '{0}'.".format(editCommand))
				editProcess = QProcess()
				editProcess.startDetached(editCommand)
		else :
			messageBox.messageBox("Warning", "Warning", "{0} | Please Define An 'sIBLedit' Executable In The Preferences !".format(self.__class__.__name__))

	@core.executionTrace
	def sIBLedit_Path_lineEdit_setUi(self) :
		'''
		This Method Fills The sIBLedit_Path_lineEdit.
		'''

		sIBLeditExecutable = self._settings.getKey(self._settingsSection, "sIBLeditExecutable")
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("sIBLedit_Path_lineEdit", sIBLeditExecutable.toString()))
		self.ui.sIBLedit_Path_lineEdit.setText(sIBLeditExecutable.toString())

	@core.executionTrace
	def sIBLedit_Path_toolButton_OnClicked(self, checked) :
		'''
		This Method Is Called When sIBLedit_Path_toolButton Is Clicked.
		
		@param checked : Checked State. ( Boolean )
		'''

		sIBLeditExecutable = self._container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "sIBLedit Executable :", self._container.lastBrowsedPath))
		if sIBLeditExecutable != "":
			LOGGER.debug("> Chosen sIBLedit Executable : '{0}'.".format(sIBLeditExecutable))
			self.ui.sIBLedit_Path_lineEdit.setText(QString(sIBLeditExecutable))
			self._settings.setKey(self._settingsSection, "sIBLeditExecutable", self.ui.sIBLedit_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def sIBLedit_Path_lineEdit_OnEditFinished(self) :
		'''
		This Method Is Called When sIBLedit_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists(os.path.abspath(str(self.ui.sIBLedit_Path_lineEdit.text()))) and str(self.ui.sIBLedit_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring Preferences !")
			self.sIBLedit_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid sIBLedit Executable File !".format(self.__class__.__name__)
		else :
			self._settings.setKey(self._settingsSection, "sIBLeditExecutable", self.ui.sIBLedit_Path_lineEdit.text())

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
