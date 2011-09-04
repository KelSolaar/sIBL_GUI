#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**sIBLeditUtilities.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`sIBLeditUtilities` Component Interface class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
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

__all__ = ["LOGGER", "sIBLeditUtilities"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class sIBLeditUtilities(UiComponent):
	"""
	| This class is the :mod:`umbra.components.addons.sIBLeditUtilities.sIBLeditUtilities` Component Interface class.
	| It provides methods to link the Application to sIBLedit.
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

		self.__uiPath = "ui/sIBLedit_Utilities.ui"

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None

		self.__editIblSetInSIBLEditAction = None
		self.__editInspectorIblSetInSIBLEditAction = None

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
	def coreInspector(self):
		"""
		This method is the property for **self.__coreInspector** attribute.

		:return: self.__coreInspector. ( Object )
		"""

		return self.__coreInspector

	@coreInspector.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self, value):
		"""
		This method is the setter method for **self.__coreInspector** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreInspector"))

	@coreInspector.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self):
		"""
		This method is the deleter method for **self.__coreInspector** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreInspector"))

	@property
	def editIblSetInSIBLEditAction(self):
		"""
		This method is the property for **self.__editIblSetInSIBLEditAction** attribute.

		:return: self.__editIblSetInSIBLEditAction. ( QAction )
		"""

		return self.__editIblSetInSIBLEditAction

	@editIblSetInSIBLEditAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editIblSetInSIBLEditAction(self, value):
		"""
		This method is the setter method for **self.__editIblSetInSIBLEditAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("editIblSetInSIBLEditAction"))

	@editIblSetInSIBLEditAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editIblSetInSIBLEditAction(self):
		"""
		This method is the deleter method for **self.__editIblSetInSIBLEditAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("editIblSetInSIBLEditAction"))

	@property
	def editInspectorIblSetInSIBLEditAction(self):
		"""
		This method is the property for **self.__editInspectorIblSetInSIBLEditAction** attribute.

		:return: self.__editInspectorIblSetInSIBLEditAction. ( QAction )
		"""

		return self.__editInspectorIblSetInSIBLEditAction

	@editInspectorIblSetInSIBLEditAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectorIblSetInSIBLEditAction(self, value):
		"""
		This method is the setter method for **self.__editInspectorIblSetInSIBLEditAction** attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("editInspectorIblSetInSIBLEditAction"))

	@editInspectorIblSetInSIBLEditAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectorIblSetInSIBLEditAction(self):
		"""
		This method is the deleter method for **self.__editInspectorIblSetInSIBLEditAction** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("editInspectorIblSetInSIBLEditAction"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__corePreferencesManager = self.__container.componentsManager.components["factory.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreInspector = self.__container.componentsManager.components["core.inspector"].interface

		return UiComponent.activate(self)

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None

		return UiComponent.activate(self)

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__sIBLedit_Path_lineEdit_setUi()

		self.__addActions()

		# Signals / Slots.
		self.ui.sIBLedit_Path_toolButton.clicked.connect(self.__sIBLedit_Path_toolButton__clicked)
		self.ui.sIBLedit_Path_lineEdit.editingFinished.connect(self.__sIBLedit_Path_lineEdit__editFinished)

		return True

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.sIBLedit_Path_toolButton.clicked.disconnect(self.__sIBLedit_Path_toolButton__clicked)
		self.ui.sIBLedit_Path_lineEdit.editingFinished.disconnect(self.__sIBLedit_Path_lineEdit__editFinished)

		self.__removeActions()

		return True

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.sIBLedit_Path_groupBox)

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.ui.sIBLedit_Path_groupBox.setParent(None)

		return True

	@core.executionTrace
	def __addActions(self):
		"""
		This method adds actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			self.__editIblSetInSIBLEditAction = QAction("Edit In sIBLedit ...", self.__coreDatabaseBrowser.ui.Database_Browser_listView)
			self.__editIblSetInSIBLEditAction.triggered.connect(self.__Database_Browser_listView_editIblSetInSIBLEditAction__triggered)
			self.__coreDatabaseBrowser.ui.Database_Browser_listView.addAction(self.__editIblSetInSIBLEditAction)

			self.__editInspectorIblSetInSIBLEditAction = QAction("Edit In sIBLedit ...", self.__coreInspector.ui.Inspector_Overall_frame)
			self.__editInspectorIblSetInSIBLEditAction.triggered.connect(self.__Inspector_Overall_frame_editInspectorIblSetInSIBLEditAction__triggered)
			self.__coreInspector.ui.Inspector_Overall_frame.addAction(self.__editInspectorIblSetInSIBLEditAction)
		else:
			LOGGER.info("{0} | sIBLedit editing capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			self.__coreDatabaseBrowser.ui.Database_Browser_listView.removeAction(self.__editIblSetInSIBLEditAction)
			self.__editIblSetInSIBLEditAction = None

			self.__coreInspector.ui.Inspector_Overall_frame.removeAction(self.__editInspectorIblSetInSIBLEditAction)
			self.__editInspectorIblSetInSIBLEditAction = None

	@core.executionTrace
	def __Database_Browser_listView_editIblSetInSIBLEditAction__triggered(self, checked):
		"""
		This method is triggered by **editIblSetInSIBLEditAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.editIblSetInSIBLEdit_ui()

	@core.executionTrace
	def __Inspector_Overall_frame_editInspectorIblSetInSIBLEditAction__triggered(self, checked):
		"""
		This method is triggered by **editInspectorIblSetInSIBLEditAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.editInspectorIblSetInSIBLEdit_ui()

	@core.executionTrace
	def __sIBLedit_Path_lineEdit_setUi(self):
		"""
		This method fills **sIBLedit_Path_lineEdit** Widget.
		"""

		sIBLeditExecutable = self.__settings.getKey(self.__settingsSection, "sIBLeditExecutable")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("sIBLedit_Path_lineEdit", sIBLeditExecutable.toString()))
		self.ui.sIBLedit_Path_lineEdit.setText(sIBLeditExecutable.toString())

	@core.executionTrace
	def __sIBLedit_Path_toolButton__clicked(self, checked):
		"""
		This method is called when **sIBLedit_Path_toolButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		sIBLeditExecutable = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "sIBLedit executable:", self.__container.lastBrowsedPath))
		if sIBLeditExecutable != "":
			LOGGER.debug("> Chosen sIBLedit executable: '{0}'.".format(sIBLeditExecutable))
			self.ui.sIBLedit_Path_lineEdit.setText(QString(sIBLeditExecutable))
			self.__settings.setKey(self.__settingsSection, "sIBLeditExecutable", self.ui.sIBLedit_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __sIBLedit_Path_lineEdit__editFinished(self):
		"""
		This method is called when **sIBLedit_Path_lineEdit** Widget is edited and check that entered path is valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.sIBLedit_Path_lineEdit.text()))) and str(self.ui.sIBLedit_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring preferences!")
			self.__sIBLedit_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError("{0} | Invalid sIBLedit executable file!".format(self.__class__.__name__))
		else:
			self.__settings.setKey(self.__settingsSection, "sIBLeditExecutable", self.ui.sIBLedit_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.FileExistsError)
	def editIblSetInSIBLEdit_ui(self):
		"""
		This method edits selected Ibl Set in sIBLedit.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		sIBLedit = str(self.ui.sIBLedit_Path_lineEdit.text())
		if sIBLedit:
			selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
			selectedIblSet = selectedIblSets and os.path.exists(selectedIblSets[0].path) and selectedIblSets[0] or None
			if selectedIblSet:
				return self.editIblSetInSIBLedit(selectedIblSet.path, str(self.ui.sIBLedit_Path_lineEdit.text()))
			else:
				raise foundations.exceptions.FileExistsError("{0} | Exception raised while sending Ibl Set to sIBLedit: '{1}' Ibl Set file doesn't exists!".format(self.__class__.__name__, selectedIblSet.name))
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | Please define an 'sIBLedit' executable in the preferences!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.FileExistsError)
	def editInspectorIblSetInSIBLEdit_ui(self):
		"""
		This method edits :mod:`umbra.components.core.inspector.inspector` Component inspected Ibl Set in sIBLedit.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		sIBLedit = str(self.ui.sIBLedit_Path_lineEdit.text())
		if sIBLedit:
			inspectorIblSet = self.__coreInspector.inspectorIblSet
			inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
			if inspectorIblSet:
				return self.editIblSetInSIBLedit(inspectorIblSet.path, sIBLedit)
			else:
				raise foundations.exceptions.FileExistsError("{0} | Exception raised while sending Inspector Ibl Set to sIBLedit: '{1}' Ibl Set file doesn't exists!".format(self.__class__.__name__, inspectorIblSet.title))
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | Please define an 'sIBLedit' executable in the preferences!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProcessCommand(self, path, sIBLedit):
		"""
		This method gets process command.

		:param path: Path. ( String )
		:param sIBLedit: sIBLedit. ( String )
		:return: Process command. ( String )
		"""

		return "\"{0}\" \"{1}\"".format(sIBLedit, path)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def editIblSetInSIBLedit(self, path, sIBLedit):
		"""
		This method edits provided Ibl Set in sIBLedit.

		:param path: Path. ( String )
		:param sIBLedit: sIBLedit. ( String )
		:return: Method success. ( Boolean )
		"""

		editCommand = self.getProcessCommand(path, sIBLedit)
		if editCommand:
			LOGGER.debug("> Current edit command: '{0}'.".format(editCommand))
			LOGGER.info("{0} | Launching 'sIBLedit' with '{1}'.".format(self.__class__.__name__, path))
			editProcess = QProcess()
			editProcess.startDetached(editCommand)
			return True
		else:
			raise Exception("{0} | Exception raised: No suitable process command provided!".format(self.__class__.__name__))
