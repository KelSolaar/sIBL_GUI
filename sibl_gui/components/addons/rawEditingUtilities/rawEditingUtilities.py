#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**rawEditingUtilities.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`RawEditingUtilities` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform
import re
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QGridLayout

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.engine
import umbra.exceptions
import umbra.ui.common
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "RawEditingUtilities"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Raw_Editing_Utilities.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RawEditingUtilities(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.addons.rawEditingUtilities.rawEditingUtilities` Component Interface class.
	| It provides methods to edit Application related text files.
	| By default the Component will use the **factory.scriptEditor** Component	but the user can define a custom file editor
		through options exposed in the :mod:`sibl_gui.components.core.preferencesManager.preferencesManager` Component ui.
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

		super(RawEditingUtilities, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__scriptEditor = None
		self.__preferencesManager = None
		self.__componentsManagerUi = None
		self.__iblSetsOutliner = None
		self.__inspector = None
		self.__templatesOutliner = None

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
	def scriptEditor(self):
		"""
		This method is the property for **self.__scriptEditor** attribute.

		:return: self.__scriptEditor. ( QWidget )
		"""

		return self.__scriptEditor

	@scriptEditor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self, value):
		"""
		This method is the setter method for **self.__scriptEditor** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "scriptEditor"))

	@scriptEditor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self):
		"""
		This method is the deleter method for **self.__scriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "scriptEditor"))

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
	def componentsManagerUi(self):
		"""
		This method is the property for **self.__componentsManagerUi** attribute.

		:return: self.__componentsManagerUi. ( QWidget )
		"""

		return self.__componentsManagerUi

	@componentsManagerUi.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def componentsManagerUi(self, value):
		"""
		This method is the setter method for **self.__componentsManagerUi** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "componentsManagerUi"))

	@componentsManagerUi.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def componentsManagerUi(self):
		"""
		This method is the deleter method for **self.__componentsManagerUi** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "componentsManagerUi"))

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

	@property
	def templatesOutliner(self):
		"""
		This method is the property for **self.__templatesOutliner** attribute.

		:return: self.__templatesOutliner. ( QWidget )
		"""

		return self.__templatesOutliner

	@templatesOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesOutliner(self, value):
		"""
		This method is the setter method for **self.__templatesOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesOutliner"))

	@templatesOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesOutliner(self):
		"""
		This method is the deleter method for **self.__templatesOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesOutliner"))

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

		self.__scriptEditor = self.__engine.componentsManager["factory.scriptEditor"]
		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]
		self.__componentsManagerUi = self.__engine.componentsManager["factory.componentsManagerUi"]
		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]
		self.__inspector = self.__engine.componentsManager["core.inspector"]
		self.__templatesOutliner = self.__engine.componentsManager["core.templatesOutliner"]

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

		self.__scriptEditor = None
		self.__preferencesManager = None
		self.__componentsManagerUi = None
		self.__iblSetsOutliner = None
		self.__inspector = None
		self.__templatesOutliner = None

		self.activated = False
		return True

	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__Custom_Text_Editor_Path_lineEdit_setUi()
		self.__addActions()

		# Signals / Slots.
		self.Custom_Text_Editor_Path_toolButton.clicked.connect(self.__Custom_Text_Editor_Path_toolButton__clicked)
		self.Custom_Text_Editor_Path_lineEdit.editingFinished.connect(
		self.__Custom_Text_Editor_Path_lineEdit__editFinished)
		self.__engine.contentDropped.connect(self.__engine__contentDropped)
		self.__scriptEditor.Script_Editor_tabWidget.contentDropped.connect(
		self.__scriptEditor_Script_Editor_tabWidget__contentDropped)

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.Custom_Text_Editor_Path_toolButton.clicked.disconnect(self.__Custom_Text_Editor_Path_toolButton__clicked)
		self.Custom_Text_Editor_Path_lineEdit.editingFinished.disconnect(
		self.__Custom_Text_Editor_Path_lineEdit__editFinished)
		self.__engine.contentDropped.disconnect(self.__engine__contentDropped)
		self.__scriptEditor.Script_Editor_tabWidget.contentDropped.disconnect(
		self.__scriptEditor_Script_Editor_tabWidget__contentDropped)

		self.__removeActions()

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.Custom_Text_Editor_Path_groupBox)

		return True

	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.Custom_Text_Editor_Path_groupBox.setParent(None)

		return True

	def __addActions(self):
		"""
		This method sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			editIblSetsFilesAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.iblSetsOutliner|Edit Ibl Set(s) File(s) ...",
			slot=self.__iblSetsOutliner_views_editIblSetsFilesAction__triggered)
			for view in self.__iblSetsOutliner.views:
				view.addAction(editIblSetsFilesAction)

			self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.inspector|Edit Ibl Set File ...",
			slot=self.__inspector_editActiveIblSetFileAction__triggered))
			self.__templatesOutliner.view.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.templatesOutliner|Edit Template(s) File(s) ...",
			slot=self.__templatesOutliner_view_editTemplatesFilesAction__triggered))
		else:
			LOGGER.info("{0} | Text editing capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		separatorAction = QAction(self.__componentsManagerUi.view)
		separatorAction.setSeparator(True)
		self.__componentsManagerUi.view.addAction(separatorAction)

		self.__componentsManagerUi.view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.componentsManagerUi|Edit Component(s) ...",
		slot=self.__componentsManagerUi_view_editComponentsAction__triggered))

	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			editIblSetsFilesAction = "Actions|Umbra|Components|core.iblSetsOutliner|Edit Ibl Set(s) File(s) ..."
			for view in self.__iblSetsOutliner.views:
				view.removeAction(self.__engine.actionsManager.getAction(editIblSetsFilesAction))
			self.__engine.actionsManager.unregisterAction(editIblSetsFilesAction)
			editActiveIblSetFileAction = "Actions|Umbra|Components|core.inspector|Edit Ibl Set File ..."
			self.__inspector.Inspector_Overall_frame.removeAction(
			self.__engine.actionsManager.getAction(editActiveIblSetFileAction))
			self.__engine.actionsManager.unregisterAction(editActiveIblSetFileAction)
			editTemplatesFilesAction = "Actions|Umbra|Components|core.templatesOutliner|Edit Template(s) File(s) ..."
			self.__templatesOutliner.view.removeAction(
			self.__engine.actionsManager.getAction(editTemplatesFilesAction))
			self.__engine.actionsManager.unregisterAction(editTemplatesFilesAction)
		editComponenetsAction = "Actions|Umbra|Components|factory.componentsManagerUi|Edit Component(s) ..."
		self.__componentsManagerUi.view.removeAction(
		self.__engine.actionsManager.getAction(editComponenetsAction))
		self.__engine.actionsManager.unregisterAction(editComponenetsAction)

	def __iblSetsOutliner_views_editIblSetsFilesAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|core.iblSetsOutliner|Edit Ibl Set(s) File(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editIblSetsFilesUi()

	def __inspector_editActiveIblSetFileAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|Edit Ibl Set File ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editActiveIblSetFileUi()

	def __templatesOutliner_view_editTemplatesFilesAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|core.templatesOutliner|Edit Template(s) File(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editTemplatesFilesUi()

	def __componentsManagerUi_view_editComponentsAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.componentsManagerUi|Edit Component(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editComponentsUi()

	def __Custom_Text_Editor_Path_lineEdit_setUi(self):
		"""
		This method fills **Custom_Text_Editor_Path_lineEdit** Widget.
		"""

		customTextEditor = self.__settings.getKey(self.__settingsSection, "customTextEditor")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Custom_Text_Editor_Path_lineEdit",
																customTextEditor.toString()))
		self.Custom_Text_Editor_Path_lineEdit.setText(customTextEditor.toString())

	def __Custom_Text_Editor_Path_toolButton__clicked(self, checked):
		"""
		This method is triggered when **Custom_Text_Editor_Path_toolButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		customTextEditorExecutable = umbra.ui.common.storeLastBrowsedPath(
		QFileDialog.getOpenFileName(self, "Custom Text Editor Executable:", RuntimeGlobals.lastBrowsedPath))
		if customTextEditorExecutable != "":
			LOGGER.debug("> Chosen custom text editor executable: '{0}'.".format(customTextEditorExecutable))
			self.Custom_Text_Editor_Path_lineEdit.setText(QString(customTextEditorExecutable))
			self.__settings.setKey(self.__settingsSection,
									"customTextEditor",
									self.Custom_Text_Editor_Path_lineEdit.text())

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError)
	def __Custom_Text_Editor_Path_lineEdit__editFinished(self):
		"""
		This method is triggered when **Custom_Text_Editor_Path_lineEdit** Widget
		is edited and check that entered path is valid.
		"""

		value = foundations.strings.encode(self.Custom_Text_Editor_Path_lineEdit.text())
		if not foundations.common.pathExists(os.path.abspath(value)) and value != unicode():
			LOGGER.debug("> Restoring preferences!")
			self.__Custom_Text_Editor_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError("{0} | Invalid custom text editor executable file!".format(
			self.__class__.__name__))
		else:
			self.__settings.setKey(self.__settingsSection,
									"customTextEditor",
									self.Custom_Text_Editor_Path_lineEdit.text())

	@umbra.engine.encapsulateProcessing
	def __engine__contentDropped(self, event):
		"""
		This method is triggered when content is dropped into the engine.
		
		:param event: Event. ( QEvent )
		"""

		if not event.mimeData().hasUrls():
			return

		urls = event.mimeData().urls()

		LOGGER.debug("> Drag event urls list: '{0}'!".format(urls))

		self.__engine.startProcessing("Loading Files ...", len(urls))
		for url in event.mimeData().urls():
			path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
			re.search(r"^\/[A-Z]:", foundations.strings.encode(url.path())) and foundations.strings.encode(url.path())[1:] or \
			foundations.strings.encode(url.path())
			if not re.search(r"\.{0}$".format(self.__iblSetsOutliner.extension), foundations.strings.encode(url.path())) and \
			not re.search(r"\.{0}$".format(self.templatesOutliner.extension), foundations.strings.encode(url.path())) and \
			not os.path.isdir(path):
				self.editPath(path, self.Custom_Text_Editor_Path_lineEdit.text())
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

	def __scriptEditor_Script_Editor_tabWidget__contentDropped(self, event):
		"""
		This method is triggered when content is dropped in the **scriptEditor.Script_Editor_tabWidget** Widget.
		
		:param event: Event. ( QEvent )
		"""

		if event.source() in self.__iblSetsOutliner.views:
			self.editIblSetsFilesUi()
		elif event.source() is self.__templatesOutliner.view:
			self.editTemplatesFilesUi()

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def editIblSetsFilesUi(self):
		"""
		This method edits selected Ibl Sets files.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedIblSets = self.__iblSetsOutliner.getSelectedIblSets()

		success = True
		for iblSet in selectedIblSets:
			path = iblSet.path and foundations.common.pathExists(iblSet.path) and iblSet.path
			if path:
				success *= self.editPath(path, self.Custom_Text_Editor_Path_lineEdit.text()) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Ibl Set file doesn't exists and will be skipped!".format(
				self.__class__.__name__, iblSet.title))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while editing '{1}' Ibl Sets!".format(self.__class__.__name__,
																", ".join(iblSet.title for iblSet in selectedIblSets)))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.FileExistsError)
	def editActiveIblSetFileUi(self):
		"""
		This method edits :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set file.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		activeIblSet = self.__inspector.activeIblSet
		if activeIblSet is None:
			return False

		if foundations.common.pathExists(activeIblSet.path):
			return self.editPath(activeIblSet.path, foundations.strings.encode(self.Custom_Text_Editor_Path_lineEdit.text()))
		else:
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while editing Inspector Ibl Set: '{1}' Ibl Set file doesn't exists!".format(
			self.__class__.__name__, activeIblSet.title))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def editTemplatesFilesUi(self):
		"""
		This method edits selected Templates files.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedTemplates = self.__templatesOutliner.getSelectedTemplates()

		success = True
		for template in selectedTemplates:
			path = template.path and foundations.common.pathExists(template.path) and template.path
			if path:
				success *= self.editPath(path, self.Custom_Text_Editor_Path_lineEdit.text()) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Template file doesn't exists and will be skipped!".format(
				self.__class__.__name__, template.name))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while editing '{1}' Templates!".format(self.__class__.__name__,
															", ".join(template.name for template in selectedTemplates)))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def editComponentsUi(self):
		"""
		This method edits selected Components packages.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedComponents = self.__componentsManagerUi.getSelectedComponents()

		success = True
		for component in selectedComponents:
			path = component.directory and foundations.common.pathExists(component.directory) and component.directory
			if path:
				success *= self.editPath(path, self.Custom_Text_Editor_Path_lineEdit.text()) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Component path doesn't exists and will be skipped!".format(
				self.__class__.__name__, component.name))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while editing '{1}' Components!".format(self.__class__.__name__,
															", ".join(component.name for component in selectedComponents)))

	def getProcessCommand(self, path, customTextEditor):
		"""
		This method gets process command.

		:param path: Path to edit. ( String )
		:param customTextEditor: Custom text editor. ( String )
		:return: Process command. ( String )
		"""

		processCommand = None
		path = os.path.normpath(path)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			processCommand = "\"{0}\" \"{1}\"".format(customTextEditor, path)
		elif platform.system() == "Darwin":
			processCommand = "open -a \"{0}\" \"{1}\"".format(customTextEditor, path)
		elif platform.system() == "Linux":
			processCommand = "\"{0}\" \"{1}\"".format(customTextEditor, path)
		return processCommand

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def editPath(self, path, customTextEditor=None):
		"""
		This method provides editing capability.

		:param path: Path to edit. ( String )
		:param customTextEditor: Custom text editor. ( String )
		:return: Method success. ( Boolean )
		"""

		if customTextEditor:
			editCommand = self.getProcessCommand(path, customTextEditor)
			if editCommand:
				LOGGER.debug("> Current edit command: '{0}'.".format(editCommand))
				LOGGER.info("{0} | Launching text editor with '{1}' path.".format(self.__class__.__name__, path))
				editProcess = QProcess()
				editProcess.startDetached(editCommand)
				return True
			else:
				raise Exception("{0} | Exception raised: No suitable process command given!".format(
				self.__class__.__name__))
		else:
			self.__scriptEditor.loadPath(path) and self.__scriptEditor.restoreDevelopmentLayout()
			return True
