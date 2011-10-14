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
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "sIBLeditUtilities"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "sIBLedit_Utilities.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class sIBLeditUtilities(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.addons.sIBLeditUtilities.sIBLeditUtilities` Component Interface class.
	| It provides methods to link the Application to sIBLedit.
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(sIBLeditUtilities, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryPreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("engine"))

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
	def factoryPreferencesManager(self):
		"""
		This method is the property for **self.__factoryPreferencesManager** attribute.

		:return: self.__factoryPreferencesManager. ( Object )
		"""

		return self.__factoryPreferencesManager

	@factoryPreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryPreferencesManager(self, value):
		"""
		This method is the setter method for **self.__factoryPreferencesManager** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("factoryPreferencesManager"))

	@factoryPreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryPreferencesManager(self):
		"""
		This method is the deleter method for **self.__factoryPreferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("factoryPreferencesManager"))

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

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__factoryPreferencesManager = self.__engine.componentsManager.components["factory.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__engine.componentsManager.components["core.databaseBrowser"].interface
		self.__coreInspector = self.__engine.componentsManager.components["core.inspector"].interface

		self.activated = True
		return True

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryPreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None

		self.activated = False
		return True

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
		self.sIBLedit_Path_toolButton.clicked.connect(self.__sIBLedit_Path_toolButton__clicked)
		self.sIBLedit_Path_lineEdit.editingFinished.connect(self.__sIBLedit_Path_lineEdit__editFinished)

		return True

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.sIBLedit_Path_toolButton.clicked.disconnect(self.__sIBLedit_Path_toolButton__clicked)
		self.sIBLedit_Path_lineEdit.editingFinished.disconnect(self.__sIBLedit_Path_lineEdit__editFinished)

		self.__removeActions()

		return True

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__factoryPreferencesManager.Others_Preferences_gridLayout.addWidget(self.sIBLedit_Path_groupBox)

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.sIBLedit_Path_groupBox.setParent(None)

		return True

	@core.executionTrace
	def __addActions(self):
		"""
		This method adds actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			self.__coreDatabaseBrowser.Database_Browser_listView.addAction(self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|Edit In sIBLedit ...", slot=self.__Database_Browser_listView_editIblSetInSIBLEditAction__triggered))
			self.__coreInspector.Inspector_Overall_frame.addAction(self.__engine.actionsManager.registerAction("Actions|Umbra|Components|core.inspector|Edit In sIBLedit ...", slot=self.__Inspector_Overall_frame_editInspectorIblSetInSIBLEditAction__triggered))
		else:
			LOGGER.info("{0} | sIBLedit editing capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			editIblSetInSIBLEditAction = "Actions|Umbra|Components|core.databaseBrowser|Edit In sIBLedit ..."
			self.__coreDatabaseBrowser.Database_Browser_listView.removeAction(self.__engine.actionsManager.getAction(editIblSetInSIBLEditAction))
			self.__engine.actionsManager.unregisterAction(editIblSetInSIBLEditAction)
			editInspectorIblSetInSIBLEditAction = "Actions|Umbra|Components|core.inspector|Edit In sIBLedit ..."
			self.__coreInspector.Inspector_Overall_frame.removeAction(self.__engine.actionsManager.getAction(editInspectorIblSetInSIBLEditAction))
			self.__engine.actionsManager.unregisterAction(editInspectorIblSetInSIBLEditAction)

	@core.executionTrace
	def __Database_Browser_listView_editIblSetInSIBLEditAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|Edit In sIBLedit ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editIblSetInSIBLEdit_ui()

	@core.executionTrace
	def __Inspector_Overall_frame_editInspectorIblSetInSIBLEditAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|Edit In sIBLedit ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editInspectorIblSetInSIBLEdit_ui()

	@core.executionTrace
	def __sIBLedit_Path_lineEdit_setUi(self):
		"""
		This method fills **sIBLedit_Path_lineEdit** Widget.
		"""

		sIBLeditExecutable = self.__settings.getKey(self.__settingsSection, "sIBLeditExecutable")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("sIBLedit_Path_lineEdit", sIBLeditExecutable.toString()))
		self.sIBLedit_Path_lineEdit.setText(sIBLeditExecutable.toString())

	@core.executionTrace
	def __sIBLedit_Path_toolButton__clicked(self, checked):
		"""
		This method is called when **sIBLedit_Path_toolButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		sIBLeditExecutable = umbra.ui.common.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "sIBLedit executable:", RuntimeGlobals.lastBrowsedPath))
		if sIBLeditExecutable != "":
			LOGGER.debug("> Chosen sIBLedit executable: '{0}'.".format(sIBLeditExecutable))
			self.sIBLedit_Path_lineEdit.setText(QString(sIBLeditExecutable))
			self.__settings.setKey(self.__settingsSection, "sIBLeditExecutable", self.sIBLedit_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __sIBLedit_Path_lineEdit__editFinished(self):
		"""
		This method is called when **sIBLedit_Path_lineEdit** Widget is edited and check that entered path is valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.sIBLedit_Path_lineEdit.text()))) and str(self.sIBLedit_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring preferences!")
			self.__sIBLedit_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError("{0} | Invalid sIBLedit executable file!".format(self.__class__.__name__))
		else:
			self.__settings.setKey(self.__settingsSection, "sIBLeditExecutable", self.sIBLedit_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.FileExistsError)
	def editIblSetInSIBLEdit_ui(self):
		"""
		This method edits selected Ibl Set in sIBLedit.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		sIBLedit = str(self.sIBLedit_Path_lineEdit.text())
		if sIBLedit:
			selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
			selectedIblSet = selectedIblSets and os.path.exists(selectedIblSets[0].path) and selectedIblSets[0] or None
			if selectedIblSet:
				return self.editIblSetInSIBLedit(selectedIblSet.path, str(self.sIBLedit_Path_lineEdit.text()))
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

		sIBLedit = str(self.sIBLedit_Path_lineEdit.text())
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
