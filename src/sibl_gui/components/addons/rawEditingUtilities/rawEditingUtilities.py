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
import logging
import os
import platform
import re
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QGridLayout

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import sibl_gui.ui.highlighters
import umbra.engine
import umbra.ui.common
import umbra.ui.inputAccelerators
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.components.factory.scriptEditor.editor import Language
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "RawEditingUtilities"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Raw_Editing_Utilities.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RawEditingUtilities(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.addons.rawEditingUtilities.rawEditingUtilities` Component Interface class.
	| It provides methods to edit Application related text files.
	| By default the Component will use the **factory.scriptEditor** Component
	but the user can define a custom file editor through options exposed in
	the :mod:`umbra.components.core.preferencesManager.preferencesManager` Component ui.
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

		super(RawEditingUtilities, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__editLayout = "editCentric"

		self.__factoryScriptEditor = None
		self.__factoryPreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None
		self.__coreTemplatesOutliner = None

		self.__languages = (Language(name="Ibl Set",
							extension="\.ibl",
							highlighter=sibl_gui.ui.highlighters.IblSetHighlighter,
							completer=None,
							preInputAccelerators=(umbra.ui.inputAccelerators.symbolsExpandingPreEventInputAccelerators,),
							postInputAccelerators=(),
							indentMarker="\t",
							commentMarker=None),
							Language(name="JavaScript",
							extension="\.js",
							highlighter=sibl_gui.ui.highlighters.JavaScriptHighlighter,
							completer=None,
							preInputAccelerators=(umbra.ui.inputAccelerators.symbolsExpandingPreEventInputAccelerators,),
							postInputAccelerators=(),
							indentMarker="\t",
							commentMarker=None),
							Language(name="MelScript",
							extension="\.mel",
							highlighter=sibl_gui.ui.highlighters.MelScriptHighlighter,
							completer=None,
							preInputAccelerators=(umbra.ui.inputAccelerators.symbolsExpandingPreEventInputAccelerators,),
							postInputAccelerators=(),
							indentMarker="\t",
							commentMarker=None),
							Language(name="MaxScript",
							extension="\.mxs",
							highlighter=sibl_gui.ui.highlighters.MaxScriptHighlighter,
							completer=None,
							preInputAccelerators=(umbra.ui.inputAccelerators.symbolsExpandingPreEventInputAccelerators,),
							postInputAccelerators=(),
							indentMarker="\t",
							commentMarker=None),)

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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for **self.__settingsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def editLayout(self):
		"""
		This method is the property for **self.__editLayout** attribute.

		:return: self.__editLayout. ( String )
		"""

		return self.__editLayout

	@editLayout.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editLayout(self, value):
		"""
		This method is the setter method for **self.__editLayout** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "editLayout"))

	@editLayout.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editLayout(self):
		"""
		This method is the deleter method for **self.__editLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editLayout"))

	@property
	def factoryScriptEditor(self):
		"""
		This method is the property for **self.__factoryScriptEditor** attribute.

		:return: self.__factoryScriptEditor. ( Object )
		"""

		return self.__factoryScriptEditor

	@factoryScriptEditor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self, value):
		"""
		This method is the setter method for **self.__factoryScriptEditor** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryScriptEditor"))

	@factoryScriptEditor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self):
		"""
		This method is the deleter method for **self.__factoryScriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryScriptEditor"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryPreferencesManager"))

	@factoryPreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryPreferencesManager(self):
		"""
		This method is the deleter method for **self.__factoryPreferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryPreferencesManager"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDatabaseBrowser"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreInspector"))

	@coreInspector.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreInspector(self):
		"""
		This method is the deleter method for **self.__coreInspector** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreInspector"))

	@property
	def coreTemplatesOutliner(self):
		"""
		This method is the property for **self.__coreTemplatesOutliner** attribute.

		:return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This method is the setter method for **self.__coreTemplatesOutliner** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This method is the deleter method for **self.__coreTemplatesOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreTemplatesOutliner"))

	@property
	def languages(self):
		"""
		This method is the property for **self.__languages** attribute.

		:return: self.__languages. ( Dictionary )
		"""

		return self.__languages

	@languages.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def languages(self, value):
		"""
		This method is the setter method for **self.__languages** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "languages"))

	@languages.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def languages(self):
		"""
		This method is the deleter method for **self.__languages** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "languages"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

		self.__factoryScriptEditor = self.__engine.componentsManager.components["factory.scriptEditor"].interface
		self.__factoryPreferencesManager = self.__engine.componentsManager.components["factory.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__engine.componentsManager.components["core.databaseBrowser"].interface
		self.__coreInspector = self.__engine.componentsManager.components["core.inspector"].interface
		self.__coreTemplatesOutliner = self.__engine.componentsManager.components["core.templatesOutliner"].interface

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryScriptEditor = None
		self.__factoryPreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None
		self.__coreTemplatesOutliner = None

		self.activated = False
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__Custom_Text_Editor_Path_lineEdit_setUi()
		self.__addActions()
		self.__registerLanguages()

		# Signals / Slots.
		self.Custom_Text_Editor_Path_toolButton.clicked.connect(self.__Custom_Text_Editor_Path_toolButton__clicked)
		self.Custom_Text_Editor_Path_lineEdit.editingFinished.connect(
		self.__Custom_Text_Editor_Path_lineEdit__editFinished)
		self.__engine.contentDropped.connect(self.__application__contentDropped)
		self.__factoryScriptEditor.Script_Editor_tabWidget.contentDropped.connect(
		self.__factoryScriptEditor_Script_Editor_tabWidget__contentDropped)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
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
		self.__engine.contentDropped.disconnect(self.__application__contentDropped)
		self.__factoryScriptEditor.Script_Editor_tabWidget.contentDropped.disconnect(
		self.__factoryScriptEditor_Script_Editor_tabWidget__contentDropped)

		self.__removeActions()

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__factoryPreferencesManager.Others_Preferences_gridLayout.addWidget(self.Custom_Text_Editor_Path_groupBox)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__factoryPreferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.Custom_Text_Editor_Path_groupBox.setParent(None)

		return True

	@core.executionTrace
	def __addActions(self):
		"""
		This method adds actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			editIblSetsFilesAction = self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.databaseBrowser|Edit Ibl Set(s) File(s) ...",
			slot=self.__Database_Browser_listView_editIblSetsFilesAction__triggered)
			for view in self.__coreDatabaseBrowser.views:
				view.addAction(editIblSetsFilesAction)

			self.__coreInspector.Inspector_Overall_frame.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.inspector|Edit Ibl Set(s) File(s) ...",
			slot=self.__Inspector_Overall_frame_editInspectorIblSetsFilesAction__triggered))
			self.__coreTemplatesOutliner.view.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.templatesOutliner|Edit Template(s) File(s) ...",
			slot=self.__Templates_Outliner_treeView_editTemplatesFilesAction__triggered))
		else:
			LOGGER.info("{0} | Text editing capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			editIblSetsFilesAction = "Actions|Umbra|Components|core.databaseBrowser|Edit Ibl Set(s) File(s) ..."
			for view in self.__coreDatabaseBrowser.views:
				view.removeAction(self.__engine.actionsManager.getAction(editIblSetsFilesAction))
			self.__engine.actionsManager.unregisterAction(editIblSetsFilesAction)
			editInspectorIblSetsFilesAction = "Actions|Umbra|Components|core.inspector|Edit Ibl Set(s) File(s) ..."
			self.__coreInspector.Inspector_Overall_frame.removeAction(
			self.__engine.actionsManager.getAction(editInspectorIblSetsFilesAction))
			self.__engine.actionsManager.unregisterAction(editInspectorIblSetsFilesAction)
			editTemplatesFilesAction = "Actions|Umbra|Components|core.templatesOutliner|Edit Template(s) File(s) ..."
			self.__coreTemplatesOutliner.view.removeAction(
			self.__engine.actionsManager.getAction(editTemplatesFilesAction))
			self.__engine.actionsManager.unregisterAction(editTemplatesFilesAction)

	@core.executionTrace
	def __Database_Browser_listView_editIblSetsFilesAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|core.databaseBrowser|Edit Ibl Set(s) File(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editIblSetsFiles_ui()

	@core.executionTrace
	def __Inspector_Overall_frame_editInspectorIblSetsFilesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|Edit Ibl Set(s) File(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editInspectorIblSetFile_ui()

	@core.executionTrace
	def __Templates_Outliner_treeView_editTemplatesFilesAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|core.templatesOutliner|Edit Template(s) File(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.editTemplatesFiles_ui()

	@core.executionTrace
	def __Custom_Text_Editor_Path_lineEdit_setUi(self):
		"""
		This method fills **Custom_Text_Editor_Path_lineEdit** Widget.
		"""

		customTextEditor = self.__settings.getKey(self.__settingsSection, "customTextEditor")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Custom_Text_Editor_Path_lineEdit",
																customTextEditor.toString()))
		self.Custom_Text_Editor_Path_lineEdit.setText(customTextEditor.toString())

	@core.executionTrace
	def __Custom_Text_Editor_Path_toolButton__clicked(self, checked):
		"""
		This method is called when **Custom_Text_Editor_Path_toolButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		customTextEditorExecutable = umbra.ui.common.storeLastBrowsedPath(
		QFileDialog.getOpenFileName(self, "Custom text editor executable:", RuntimeGlobals.lastBrowsedPath))
		if customTextEditorExecutable != "":
			LOGGER.debug("> Chosen custom text editor executable: '{0}'.".format(customTextEditorExecutable))
			self.Custom_Text_Editor_Path_lineEdit.setText(QString(customTextEditorExecutable))
			self.__settings.setKey(self.__settingsSection,
									"customTextEditor",
									self.Custom_Text_Editor_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler,
											False,
											foundations.exceptions.UserError)
	def __Custom_Text_Editor_Path_lineEdit__editFinished(self):
		"""
		This method is called when **Custom_Text_Editor_Path_lineEdit** Widget
		is edited and check that entered path is valid.
		"""
		
		value = str(self.Custom_Text_Editor_Path_lineEdit.text())
		if not os.path.exists(os.path.abspath(value)) and value != "":
			LOGGER.debug("> Restoring preferences!")
			self.__Custom_Text_Editor_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError("{0} | Invalid custom text editor executable file!".format(
			self.__class__.__name__))
		else:
			self.__settings.setKey(self.__settingsSection,
									"customTextEditor",
									self.Custom_Text_Editor_Path_lineEdit.text())

	@core.executionTrace
	@umbra.engine.encapsulateProcessing
	def __application__contentDropped(self, event):
		"""
		This method is triggered when content is dropped in the Application.
		
		:param event: Event. ( QEvent )
		"""

		if not event.mimeData().hasUrls():
			return

		urls = event.mimeData().urls()

		LOGGER.debug("> Drag event urls list: '{0}'!".format(urls))

		self.__engine.startProcessing("Loading Files ...", len(urls))
		for url in event.mimeData().urls():
			path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
			re.search(r"^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
			if not re.search(r"\.{0}$".format(self.__coreDatabaseBrowser.extension), str(url.path())) and \
			not re.search(r"\.{0}$".format(self.coreTemplatesOutliner.extension), str(url.path())) and \
			not os.path.isdir(path):
				self.editFile(path, self.Custom_Text_Editor_Path_lineEdit.text())
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

	@core.executionTrace
	def __factoryScriptEditor_Script_Editor_tabWidget__contentDropped(self, event):
		"""
		This method is triggered when content is dropped in the **factoryScriptEditor.Script_Editor_tabWidget** Widget.
		
		:param event: Event. ( QEvent )
		"""

		if event.source() in self.__coreDatabaseBrowser.views:
			self.editIblSetsFiles_ui()
		elif event.source() is self.__coreTemplatesOutliner.view:
			self.editTemplatesFiles_ui()

	@core.executionTrace
	def __registerLanguages(self):
		"""
		This method registers Application related languages in **scriptEditor** component.
		"""

		for language in self.__languages:
			self.__factoryScriptEditor.languagesModel.registerLanguage(language)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def editIblSetsFiles_ui(self):
		"""
		This method edits selected Ibl Sets files.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()

		success = True
		for iblSet in selectedIblSets:
			path = iblSet.path and os.path.exists(iblSet.path) and iblSet.path
			if path:
				success *= self.editFile(path, self.Custom_Text_Editor_Path_lineEdit.text()) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Ibl Set file doesn't exists and will be skipped!".format(
				self.__class__.__name__, iblSet.title))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while editing '{1}' Ibl Sets!".format(self.__class__.__name__,
																", ".join(iblSet.title for iblSet in selectedIblSets)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler,
											False,
											foundations.exceptions.FileExistsError)
	def editInspectorIblSetFile_ui(self):
		"""
		This method edits :mod:`umbra.components.core.inspector.inspector` Component Ibl Set file.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		inspectorIblSet = self.__coreInspector.inspectorIblSet
		inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
		if inspectorIblSet:
			return self.editFile(inspectorIblSet.path, str(self.Custom_Text_Editor_Path_lineEdit.text()))
		else:
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while editing Inspector Ibl Set: '{1}' Ibl Set file doesn't exists!".format(
			self.__class__.__name__, inspectorIblSet.title))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def editTemplatesFiles_ui(self):
		"""
		This method edits selected Templates files.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedTemplates = self.__coreTemplatesOutliner.getSelectedTemplates()

		success = True
		for template in selectedTemplates:
			path = template.path and os.path.exists(template.path) and template.path
			if path:
				success *= self.editFile(path, self.Custom_Text_Editor_Path_lineEdit.text()) or False
			else:
				LOGGER.warning("!> {0} | '{1}' Template file doesn't exists and will be skipped!".format(
				self.__class__.__name__, template.name))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while editing '{1}' Templates!".format(self.__class__.__name__,
															", ".join(template.name for template in selectedTemplates)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProcessCommand(self, file, customTextEditor):
		"""
		This method gets process command.

		:param file: File to edit. ( String )
		:param customTextEditor: Custom text editor. ( String )
		:return: Process command. ( String )
		"""

		processCommand = None
		file = os.path.normpath(file)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			processCommand = "\"{0}\" \"{1}\"".format(customTextEditor, file)
		elif platform.system() == "Darwin":
			processCommand = "open -a \"{0}\" \"{1}\"".format(customTextEditor, file)
		elif platform.system() == "Linux":
			processCommand = "\"{0}\" \"{1}\"".format(customTextEditor, file)
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

		if customTextEditor:
			editCommand = self.getProcessCommand(file, customTextEditor)
			if editCommand:
				LOGGER.debug("> Current edit command: '{0}'.".format(editCommand))
				LOGGER.info("{0} | Launching text editor with '{1}' file.".format(self.__class__.__name__, file))
				editProcess = QProcess()
				editProcess.startDetached(editCommand)
				return True
			else:
				raise Exception("{0} | Exception raised: No suitable process command given!".format(
				self.__class__.__name__))
		else:
			self.__engine.currentLayout != self.__editLayout and self.__engine.restoreLayout(self.__editLayout)
			return self.__factoryScriptEditor.loadFile(file)
