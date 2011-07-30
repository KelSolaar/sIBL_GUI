#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**rawEditingUtilities.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Raw Editing Utilities Component Module.

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
class RawEditingUtilities(UiComponent):
	"""
	This class is the LocationsBrowser class.
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

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for the _uiPath attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for the _uiPath attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for the _uiPath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def settings(self):
		"""
		This method is the property for the _settings attribute.

		:return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for the _settings attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for the _settings attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))

	@property
	def settingsSection(self):
		"""
		This method is the property for the _settingsSection attribute.

		:return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for the _settingsSection attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for the _settingsSection attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settingsSection"))

	@property
	def corePreferencesManager(self):
		"""
		This method is the property for the _corePreferencesManager attribute.

		:return: self.__corePreferencesManager. ( Object )
		"""

		return self.__corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self, value):
		"""
		This method is the setter method for the _corePreferencesManager attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("corePreferencesManager"))

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self):
		"""
		This method is the deleter method for the _corePreferencesManager attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("corePreferencesManager"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for the _coreDatabaseBrowser attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for the _coreDatabaseBrowser attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for the _coreDatabaseBrowser attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def coreInspector(self):
		"""
		This method is the property for the _coreInspector attribute.

		:return: self.__coreInspector. ( Object )
		"""

		return self.__coreInspector

	@coreInspector.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self, value):
		"""
		This method is the setter method for the _coreInspector attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreInspector"))

	@coreInspector.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self):
		"""
		This method is the deleter method for the _coreInspector attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreInspector"))

	@property
	def coreTemplatesOutliner(self):
		"""
		This method is the property for the _coreTemplatesOutliner attribute.

		:return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This method is the setter method for the _coreTemplatesOutliner attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This method is the deleter method for the _coreTemplatesOutliner attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreTemplatesOutliner"))

	@property
	def editIblSetsInTextEditorAction(self):
		"""
		This method is the property for the _editIblSetsInTextEditorAction attribute.

		:return: self.__editIblSetsInTextEditorAction. ( QAction )
		"""

		return self.__editIblSetsInTextEditorAction

	@editIblSetsInTextEditorAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editIblSetsInTextEditorAction(self, value):
		"""
		This method is the setter method for the _editIblSetsInTextEditorAction attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("editIblSetsInTextEditorAction"))

	@editIblSetsInTextEditorAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editIblSetsInTextEditorAction(self):
		"""
		This method is the deleter method for the _editIblSetsInTextEditorAction attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("editIblSetsInTextEditorAction"))

	@property
	def editInspectorIblSetInTextEditorAction(self):
		"""
		This method is the property for the _editInspectorIblSetInTextEditorAction attribute.

		:return: self.__editInspectorIblSetInTextEditorAction. ( QAction )
		"""

		return self.__editInspectorIblSetInTextEditorAction

	@editInspectorIblSetInTextEditorAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectorIblSetInTextEditorAction(self, value):
		"""
		This method is the setter method for the _editInspectorIblSetInTextEditorAction attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("editInspectorIblSetInTextEditorAction"))

	@editInspectorIblSetInTextEditorAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editInspectorIblSetInTextEditorAction(self):
		"""
		This method is the deleter method for the _editInspectorIblSetInTextEditorAction attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("editInspectorIblSetInTextEditorAction"))

	@property
	def editTemplateInTextEditorAction(self):
		"""
		This method is the property for the _editTemplateInTextEditorAction attribute.

		:return: self.__editTemplateInTextEditorAction. ( QAction )
		"""

		return self.__editTemplateInTextEditorAction

	@editTemplateInTextEditorAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editTemplateInTextEditorAction(self, value):
		"""
		This method is the setter method for the _editTemplateInTextEditorAction attribute.

		:param value: Attribute value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("editTemplateInTextEditorAction"))

	@editTemplateInTextEditorAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editTemplateInTextEditorAction(self):
		"""
		This method is the deleter method for the _editTemplateInTextEditorAction attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("editTemplateInTextEditorAction"))

	@property
	def linuxTextEditors(self):
		"""
		This method is the property for the _linuxTextEditors attribute.

		:return: self.__linuxTextEditors. ( Tuple )
		"""

		return self.__linuxTextEditors

	@linuxTextEditors.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxTextEditors(self, value):
		"""
		This method is the setter method for the _linuxTextEditors attribute.

		:param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("linuxTextEditors"))

	@linuxTextEditors.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxTextEditors(self):
		"""
		This method is the deleter method for the _linuxTextEditors attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("linuxTextEditors"))

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

		self.__corePreferencesManager = self.__container.componentsManager.components["core.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreInspector = self.__container.componentsManager.components["core.inspector"].interface
		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface

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

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None
		self.__coreTemplatesOutliner = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__Custom_Text_Editor_Path_lineEdit_setUi()

		self.__addActions()

		# Signals / Slots.
		self.ui.Custom_Text_Editor_Path_toolButton.clicked.connect(self.__Custom_Text_Editor_Path_toolButton__clicked)
		self.ui.Custom_Text_Editor_Path_lineEdit.editingFinished.connect(self.__Custom_Text_Editor_Path_lineEdit__editFinished)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.ui.Custom_Text_Editor_Path_toolButton.clicked.disconnect(self.__Custom_Text_Editor_Path_toolButton__clicked)
		self.ui.Custom_Text_Editor_Path_lineEdit.editingFinished.disconnect(self.__Custom_Text_Editor_Path_lineEdit__editFinished)

		self.__removeActions()

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Custom_Text_Editor_Path_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self.ui)
		self.ui.Custom_Text_Editor_Path_groupBox.setParent(None)

	@core.executionTrace
	def __addActions(self):
		"""
		This method adds actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

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
			LOGGER.info("{0} | Text editing capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

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
		This method is triggered by editIblSetsInTextEditorAction action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.editIblSetsInTextEditor__()

	@core.executionTrace
	def __Inspector_Overall_frame_editInspectorIblSetInTextEditorAction__triggered(self, checked):
		"""
		This method is triggered by editInspectorIblSetInTextEditorAction action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.editInspectorIblSetInTextEditor__()

	@core.executionTrace
	def __Templates_Outliner_treeView_editTemplateInTextEditorAction__triggered(self, checked):
		"""
		This method is triggered by editTemplateInTextEditorAction action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.editTemplatesInTextEditor__()

	@core.executionTrace
	def __Custom_Text_Editor_Path_lineEdit_setUi(self):
		"""
		This method fills the Custom_Text_Editor_Path_lineEdit.
		"""

		customTextEditor = self.__settings.getKey(self.__settingsSection, "customTextEditor")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Custom_Text_Editor_Path_lineEdit", customTextEditor.toString()))
		self.ui.Custom_Text_Editor_Path_lineEdit.setText(customTextEditor.toString())

	@core.executionTrace
	def __Custom_Text_Editor_Path_toolButton__clicked(self, checked):
		"""
		This method is called when Custom_Text_Editor_Path_toolButton is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		customTextEditorExecutable = self.__container.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom text editor executable:", self.__container.lastBrowsedPath))
		if customTextEditorExecutable != "":
			LOGGER.debug("> Chosen custom text editor executable: '{0}'.".format(customTextEditorExecutable))
			self.ui.Custom_Text_Editor_Path_lineEdit.setText(QString(customTextEditorExecutable))
			self.__settings.setKey(self.__settingsSection, "customTextEditor", self.ui.Custom_Text_Editor_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __Custom_Text_Editor_Path_lineEdit__editFinished(self):
		"""
		This method is called when Custom_Text_Editor_Path_lineEdit is edited and check that entered path is valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.ui.Custom_Text_Editor_Path_lineEdit.text()))) and str(self.ui.Custom_Text_Editor_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring preferences!")
			self.__Custom_Text_Editor_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid custom text editor executable file!".format(self.__class__.__name__)
		else:
			self.__settings.setKey(self.__settingsSection, "customTextEditor", self.ui.Custom_Text_Editor_Path_lineEdit.text())

	@core.executionTrace
	def editIblSetsInTextEditor__(self):
		"""
		This method edits selected Ibl Sets.

		:return: Method success. ( Boolean )
		"""

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()

		success = True
		for iblSet in selectedIblSets:
			path = iblSet.path and os.path.exists(iblSet.path) and iblSet.path
			if path:
				success *= self.editFile(path, self.ui.Custom_Text_Editor_Path_lineEdit.text()) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Ibl Set file doesn't exists and will be skipped!".format(self.__class__.__name__, iblSet.title))

		if success:
			return True
		else:
			raise Exception, "{0} | Exception raised while editing '{1}' Ibl Sets!".format(self.__class__.__name__, ", ".join(iblSet.title for iblSet in selectedIblSets))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, OSError)
	def editInspectorIblSetInTextEditor__(self):
		"""
		This method edits Inspector Ibl Set.

		:return: Method success. ( Boolean )
		"""

		inspectorIblSet = self.__coreInspector.inspectorIblSet
		inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
		if inspectorIblSet:
			return self.editFile(inspectorIblSet.path, str(self.ui.Custom_Text_Editor_Path_lineEdit.text()))
		else:
			raise OSError, "{0} | Exception raised while editing Inspector Ibl Set: '{1}' Ibl Set file doesn't exists!".format(self.__class__.__name__, inspectorIblSet.title)

	@core.executionTrace
	def editTemplatesInTextEditor__(self):
		"""
		This method edits selected Templates.

		:return: Method success. ( Boolean )
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()

		success = True
		for template in selectedTemplates:
			path = template.path and os.path.exists(template.path) and template.path
			if path:
				success *= self.editFile(path, self.ui.Custom_Text_Editor_Path_lineEdit.text()) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Template file doesn't exists and will be skipped!".format(self.__class__.__name__, template.name))

		if success:
			return True
		else:
			raise Exception, "{0} | Exception raised while editing '{1}' Templates!".format(self.__class__.__name__, ", ".join(template.name for template in selectedTemplates))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProcessCommand(self, file, customTextEditor=None):
		"""
		This method gets process command.

		:param file: File to edit. ( String )
		:param customTextEditor: Custom text editor. ( String )
		:return: Process command. ( String )
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
					if editorFound:
						break

					try:
						for path in paths:
							if os.path.exists(os.path.join(path, editor)):
								processCommand = "\"{0}\" \"{1}\"".format(editor, file)
								editorFound = True
								raise StopIteration
					except StopIteration:
						pass

				if not editorFound:
					raise Exception, "{0} | Exception raised: No suitable Linux editor found!".format(self.__class__.__name__)
		return processCommand

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def editFile(self, file, customTextEditor=None):
		"""
		This method provides editing capability.

		:param file: File to edit. ( String )
		:param customTextEditor: Custom text editor. ( String )
		:return: Method success. ( Boolean )
		"""

		editCommand = self.getProcessCommand(file, customTextEditor)
		if editCommand:
			LOGGER.debug("> Current edit command: '{0}'.".format(editCommand))
			LOGGER.info("{0} | Launching text editor with '{1}' file.".format(self.__class__.__name__, file))
			editProcess = QProcess()
			editProcess.startDetached(editCommand)
			return True
		else:
			raise Exception, "{0} | Exception raised: No suitable process command provided!".format(self.__class__.__name__)

