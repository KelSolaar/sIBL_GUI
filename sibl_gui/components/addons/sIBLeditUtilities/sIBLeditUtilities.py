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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtGui import QFileDialog

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.exceptions
import umbra.ui.common
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "sIBLeditUtilities"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "sIBLedit_Utilities.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class sIBLeditUtilities(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.addons.sIBLeditUtilities.sIBLeditUtilities` Component Interface class.
	| It provides methods to link the Application to sIBLedit.
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

		super(sIBLeditUtilities, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__preferencesManager = None
		self.__iblSetsOutliner = None
		self.__inspector = None

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
	def inspector(self):
		"""
		This method is the property for **self.__inspector** attribute.

		:return: self.__inspector. ( QWidget )
		"""

		return self.__inspector

	@inspector.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def inspector(self, value):
		"""
		This method is the setter method for **self.__inspector** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspector"))

	@inspector.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def inspector(self):
		"""
		This method is the deleter method for **self.__inspector** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspector"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
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

		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]
		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]
		self.__inspector = self.__engine.componentsManager["core.inspector"]

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

		self.__preferencesManager = None
		self.__iblSetsOutliner = None
		self.__inspector = None

		self.activated = False
		return True

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

		self.initializedUi = True
		return True

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

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.sIBLedit_Path_groupBox)

		return True

	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.sIBLedit_Path_groupBox.setParent(None)

		return True

	def __addActions(self):
		"""
		This method sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			editIblSetInSIBLEditAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.iblSetsOutliner|Edit In sIBLedit ...",
			slot=self.__iblSetsOutliner_views_editIblSetInSIBLEditAction__triggered)
			for view in self.__iblSetsOutliner.views:
				view.addAction(editIblSetInSIBLEditAction)

			self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.inspector|Edit In sIBLedit ...",
			slot=self.__inspector_editActiveIblSetInSIBLEditAction__triggered))
		else:
			LOGGER.info("{0} | sIBLedit editing capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			editIblSetInSIBLEditAction = "Actions|Umbra|Components|core.iblSetsOutliner|Edit In sIBLedit ..."
			for view in self.__iblSetsOutliner.views:
				view.removeAction(self.__engine.actionsManager.getAction(editIblSetInSIBLEditAction))
			self.__engine.actionsManager.unregisterAction(editIblSetInSIBLEditAction)
			editActiveIblSetInSIBLEditAction = "Actions|Umbra|Components|core.inspector|Edit In sIBLedit ..."
			self.__inspector.Inspector_Overall_frame.removeAction(self.__engine.actionsManager.getAction(
			editActiveIblSetInSIBLEditAction))
			self.__engine.actionsManager.unregisterAction(editActiveIblSetInSIBLEditAction)

	def __iblSetsOutliner_views_editIblSetInSIBLEditAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.iblSetsOutliner|Edit In sIBLedit ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editIblSetInSIBLEditUi()

	def __inspector_editActiveIblSetInSIBLEditAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|Edit In sIBLedit ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editActiveIblSetInSIBLEditUi()

	def __sIBLedit_Path_lineEdit_setUi(self):
		"""
		This method fills **sIBLedit_Path_lineEdit** Widget.
		"""

		sIBLeditExecutable = self.__settings.getKey(self.__settingsSection, "sIBLeditExecutable")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("sIBLedit_Path_lineEdit", sIBLeditExecutable.toString()))
		self.sIBLedit_Path_lineEdit.setText(sIBLeditExecutable.toString())

	def __sIBLedit_Path_toolButton__clicked(self, checked):
		"""
		This method is triggered when **sIBLedit_Path_toolButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		sIBLeditExecutable = umbra.ui.common.storeLastBrowsedPath(QFileDialog.getOpenFileName(self,
																						"sIBLedit Executable:",
																						RuntimeGlobals.lastBrowsedPath))
		if sIBLeditExecutable != "":
			LOGGER.debug("> Chosen sIBLedit executable: '{0}'.".format(sIBLeditExecutable))
			self.sIBLedit_Path_lineEdit.setText(QString(sIBLeditExecutable))
			self.__settings.setKey(self.__settingsSection, "sIBLeditExecutable", self.sIBLedit_Path_lineEdit.text())

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError)
	def __sIBLedit_Path_lineEdit__editFinished(self):
		"""
		This method is triggered when **sIBLedit_Path_lineEdit** Widget is edited and check that entered path is valid.
		"""

		value = foundations.strings.encode(self.sIBLedit_Path_lineEdit.text())
		if not foundations.common.pathExists(os.path.abspath(value)) and value != unicode():
			LOGGER.debug("> Restoring preferences!")
			self.__sIBLedit_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError("{0} | Invalid sIBLedit executable file!".format(self.__class__.__name__))
		else:
			self.__settings.setKey(self.__settingsSection, "sIBLeditExecutable", self.sIBLedit_Path_lineEdit.text())

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.FileExistsError)
	def editIblSetInSIBLEditUi(self):
		"""
		This method edits selected Ibl Set in sIBLedit.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		sIBLedit = foundations.strings.encode(self.sIBLedit_Path_lineEdit.text())
		if sIBLedit:
			selectedIblSet = foundations.common.getFirstItem(self.__iblSetsOutliner.getSelectedIblSets())
			if selectedIblSet is None:
				return False

			if foundations.common.pathExists(selectedIblSet.path):
				return self.editIblSetInSIBLedit(selectedIblSet.path,
												foundations.strings.encode(self.sIBLedit_Path_lineEdit.text()))
			else:
				raise foundations.exceptions.FileExistsError(
				"{0} | Exception raised while sending Ibl Set to sIBLedit: '{1}' Ibl Set file doesn't exists!".format(
				self.__class__.__name__, selectedIblSet.name))
		else:
			self.__engine.notificationsManager.warnify(
			"{0} | Please define an 'sIBLedit' executable in the preferences!".format(self.__class__.__name__))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.FileExistsError)
	def editActiveIblSetInSIBLEditUi(self):
		"""
		This method edits :mod:`sibl_gui.components.core.inspector.inspector` Component inspected Ibl Set in sIBLedit.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		sIBLedit = foundations.strings.encode(self.sIBLedit_Path_lineEdit.text())
		if sIBLedit:
			activeIblSet = self.__inspector.activeIblSet
			if activeIblSet is None:
				return False

			if foundations.common.pathExists(activeIblSet.path):
				return self.editIblSetInSIBLedit(activeIblSet.path, sIBLedit)
			else:
				raise foundations.exceptions.FileExistsError(
				"{0} | Exception raised while sending Inspector Ibl Set to sIBLedit: '{1}' Ibl Set file doesn't exists!".format(
				self.__class__.__name__, activeIblSet.title))
		else:
			self.__engine.notificationsManager.warnify(
			"{0} | Please define an 'sIBLedit' executable in the preferences!".format(self.__class__.__name__))

	def getProcessCommand(self, path, sIBLedit):
		"""
		This method gets process command.

		:param path: Path. ( String )
		:param sIBLedit: sIBLedit. ( String )
		:return: Process command. ( String )
		"""

		return "\"{0}\" \"{1}\"".format(sIBLedit, path)

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def editIblSetInSIBLedit(self, path, sIBLedit):
		"""
		This method edits given Ibl Set in sIBLedit.

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
			raise Exception("{0} | Exception raised: No suitable process command given!".format(self.__class__.__name__))
