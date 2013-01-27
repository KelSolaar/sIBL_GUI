#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preview.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Preview` Component Interface class, the :class:`ImagesPreviewer` class and
	others images preview related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import os
import platform
import re
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QPushButton

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
from foundations.parsers import SectionsFileParser
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.addons.preview.imagesPreviewer import ImagesPreviewer
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Preview"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Preview.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Preview(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.addons.preview.preview` Component Interface class.
	| It provides a basic image previewer.
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

		super(Preview, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__uiResourcesDirectory = "resources"

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__preferencesManager = None
		self.__iblSetsOutliner = None
		self.__inspector = None

		self.__imagesPreviewers = None
		self.__maximumImagesPreviewersInstances = 5

		self.__inspectorButtons = {"Background" : {"object" : None,
													"text": "View Background Image",
													"row" : 1,
													"column" : 3},
									"Lighting" : {"object" : None,
													"text": "View Lighting Image",
													"row" : 1,
													"column" : 4},
									"Reflection" : {"object" : None,
													"text": "View Reflection Image",
													"row" : 1,
													"column" : 5},
									"Plate" : {"object" : None,
													"text": "View Plate(s)",
													"row" : 1,
													"column" : 6}}

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

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

	@property
	def imagesPreviewers(self):
		"""
		This method is the property for **self.__imagesPreviewers** attribute.

		:return: self.__imagesPreviewers. ( List )
		"""

		return self.__imagesPreviewers

	@imagesPreviewers.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def imagesPreviewers(self, value):
		"""
		This method is the setter method for **self.__imagesPreviewers** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "imagesPreviewers"))

	@imagesPreviewers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def imagesPreviewers(self):
		"""
		This method is the deleter method for **self.__imagesPreviewers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "imagesPreviewers"))

	@property
	def maximumImagesPreviewersInstances(self):
		"""
		This method is the property for **self.__maximumImagesPreviewersInstances** attribute.

		:return: self.__maximumImagesPreviewersInstances. ( Integer )
		"""

		return self.__maximumImagesPreviewersInstances

	@maximumImagesPreviewersInstances.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumImagesPreviewersInstances(self, value):
		"""
		This method is the setter method for **self.__maximumImagesPreviewersInstances** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximumImagesPreviewersInstances"))

	@maximumImagesPreviewersInstances.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumImagesPreviewersInstances(self):
		"""
		This method is the deleter method for **self.__maximumImagesPreviewersInstances** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumImagesPreviewersInstances"))

	@property
	def inspectorButtons(self):
		"""
		This method is the property for **self.__inspectorButtons** attribute.

		:return: self.__inspectorButtons. ( Dictionary )
		"""

		return self.__inspectorButtons

	@inspectorButtons.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def inspectorButtons(self, value):
		"""
		This method is the setter method for **self.__inspectorButtons** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorButtons"))

	@inspectorButtons.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def inspectorButtons(self):
		"""
		This method is the deleter method for **self.__inspectorButtons** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorButtons"))

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

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(__file__), self.__uiResourcesDirectory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]
		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]
		self.__inspector = self.__engine.componentsManager["core.inspector"]

		self.__imagesPreviewers = []

		self.activated = True
		return True

	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.basename(self.__uiResourcesDirectory)
		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__preferencesManager = None
		self.__iblSetsOutliner = None
		self.__inspector = None

		for imagesPreviewer in self.__imagesPreviewers[:]:
			imagesPreviewer.ui.close()

		self.activated = False
		return True

	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__Custom_Previewer_Path_lineEdit_setUi()

		self.__addActions()
		self.__addInspectorButtons()

		# Signals / Slots.
		self.Custom_Previewer_Path_toolButton.clicked.connect(self.__Custom_Previewer_Path_toolButton__clicked)
		self.Custom_Previewer_Path_lineEdit.editingFinished.connect(self.__Custom_Previewer_Path_lineEdit__editFinished)

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__removeActions()
		self.__removeInspectorButtons()

		# Signals / Slots.
		self.Custom_Previewer_Path_toolButton.clicked.disconnect(self.__Custom_Previewer_Path_toolButton__clicked)
		self.Custom_Previewer_Path_lineEdit.editingFinished.disconnect(self.__Custom_Previewer_Path_lineEdit__editFinished)

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.Custom_Previewer_Path_groupBox)

		return True

	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.Custom_Previewer_Path_groupBox.setParent(None)

		return True

	def __addActions(self):
		"""
		This method sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))


		viewIblSetsBackgroundImagesAction = self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.iblSetsOutliner|View Background Image ...",
		slot=self.__iblSetsOutliner_views_viewIblSetsBackgroundImagesAction__triggered)
		viewIblSetsLightingImagesAction = self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.iblSetsOutliner|View Lighting Image ...",
		slot=self.__iblSetsOutliner_views_viewIblSetsLightingImagesAction__triggered)
		viewIblSetsReflectionImagesAction = self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.iblSetsOutliner|View Reflection Image ...",
		slot=self.__iblSetsOutliner_views_viewIblSetsReflectionImagesAction__triggered)
		viewIblSetsPlatesAction = self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.iblSetsOutliner|View Plate(s) ...",
		slot=self.__iblSetsOutliner_views_viewIblSetsPlatesAction__triggered)
		for view in self.__iblSetsOutliner.views:
			separatorAction = QAction(view)
			separatorAction.setSeparator(True)
			for action in (separatorAction,
							viewIblSetsBackgroundImagesAction,
							viewIblSetsLightingImagesAction,
							viewIblSetsReflectionImagesAction,
							viewIblSetsPlatesAction):
				view.addAction(action)

		separatorAction = QAction(self.__inspector.Inspector_Overall_frame)
		separatorAction.setSeparator(True)
		self.__inspector.Inspector_Overall_frame.addAction(separatorAction)

		self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.inspector|View Background Image ...",
		slot=self.__Inspector_Overall_frame_viewActiveIblSetBackgroundImageAction__triggered))
		self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.inspector|View Lighting Image ...",
		slot=self.__Inspector_Overall_frame_viewActiveIblSetLightingImageAction__triggered))
		self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.inspector|View Reflection Image ...",
		slot=self.__Inspector_Overall_frame_viewActiveIblSetReflectionImageAction__triggered))
		self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.inspector|View Plate(s) ...",
		slot=self.__Inspector_Overall_frame_viewActiveIblSetPlatesAction__triggered))

	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		viewIblSetsBackgroundImagesAction = "Actions|Umbra|Components|core.iblSetsOutliner|View Background Image ..."
		viewIblSetsLightingImagesAction = "Actions|Umbra|Components|core.iblSetsOutliner|View Lighting Image ..."
		viewIblSetsReflectionImagesAction = "Actions|Umbra|Components|core.iblSetsOutliner|View Reflection Image ..."
		viewIblSetsPlatesAction = "Actions|Umbra|Components|core.iblSetsOutliner|View Plate(s) ..."
		actions = (viewIblSetsBackgroundImagesAction,
					viewIblSetsLightingImagesAction,
					viewIblSetsReflectionImagesAction,
					viewIblSetsPlatesAction)
		for view in self.__iblSetsOutliner.views:
			for action in actions:
				view.removeAction(self.__engine.actionsManager.getAction(action))
		for action in actions:
			self.__engine.actionsManager.unregisterAction(action)

		viewActiveIblSetBackgroundImageAction = "Actions|Umbra|Components|core.inspector|View Background Image ..."
		viewActiveIblSetLightingImageAction = "Actions|Umbra|Components|core.inspector|View Lighting Image ..."
		viewActiveIblSetReflectionImageAction = "Actions|Umbra|Components|core.inspector|View Reflection Image ..."
		viewActiveIblSetPlatesAction = "Actions|Umbra|Components|core.inspector|View Plate(s) ..."
		actions = (viewActiveIblSetBackgroundImageAction,
					viewActiveIblSetLightingImageAction,
					viewActiveIblSetReflectionImageAction,
					viewActiveIblSetPlatesAction)
		for action in actions:
			self.__inspector.Inspector_Overall_frame.removeAction(self.__engine.actionsManager.getAction(action))
			self.__engine.actionsManager.unregisterAction(action)

	def __addInspectorButtons(self):
		"""
		This method adds buttons to the :mod:`sibl_gui.components.core.inspector.inspector` Component.
		"""

		self.__inspector.Inspector_Options_groupBox.show()
		for key, value in self.__inspectorButtons.iteritems():
			value["object"] = QPushButton(value["text"])
			self.__inspector.Inspector_Options_groupBox_gridLayout.addWidget(value["object"],
																				value["row"],
																				value["column"])
			value["object"].clicked.connect(functools.partial(self.viewActiveIblSetImagesUi, key))

	def __removeInspectorButtons(self):
		"""
		This method removes buttons from the :mod:`sibl_gui.components.core.inspector.inspector` Component.
		"""

		for value in self.__inspectorButtons.itervalues():
			value["object"].setParent(None)

	def __iblSetsOutliner_views_viewIblSetsBackgroundImagesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.iblSetsOutliner|View Background Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImagesUi("Background")

	def __iblSetsOutliner_views_viewIblSetsLightingImagesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.iblSetsOutliner|View Lighting Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImagesUi("Lighting")

	def __iblSetsOutliner_views_viewIblSetsReflectionImagesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.iblSetsOutliner|View Reflection Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImagesUi("Reflection")

	def __iblSetsOutliner_views_viewIblSetsPlatesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.iblSetsOutliner|View Plate(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImagesUi("Plate")

	def __Inspector_Overall_frame_viewActiveIblSetBackgroundImageAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|View Background Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewActiveIblSetImagesUi("Background")

	def __Inspector_Overall_frame_viewActiveIblSetLightingImageAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|View Lighting Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewActiveIblSetImagesUi("Lighting")

	def __Inspector_Overall_frame_viewActiveIblSetReflectionImageAction__triggered(self, checked):
		"""
		This method is triggered by **'"Actions|Umbra|Components|core.inspector|View Reflection Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewActiveIblSetImagesUi("Reflection")

	def __Inspector_Overall_frame_viewActiveIblSetPlatesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|View Plate(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewActiveIblSetImagesUi("Plate")

	def __Custom_Previewer_Path_lineEdit_setUi(self):
		"""
		This method fills **Custom_Previewer_Path_lineEdit** Widget.
		"""

		customPreviewer = self.__settings.getKey(self.__settingsSection, "customPreviewer")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format(
		"Custom_Previewer_Path_lineEdit", customPreviewer.toString()))
		self.Custom_Previewer_Path_lineEdit.setText(customPreviewer.toString())

	def __Custom_Previewer_Path_toolButton__clicked(self, checked):
		"""
		This method is triggered when **Custom_Previewer_Path_toolButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		customPreviewerExecutable = umbra.ui.common.storeLastBrowsedPath(
		QFileDialog.getOpenFileName(self, "Custom Previewer Executable:", RuntimeGlobals.lastBrowsedPath))
		if customPreviewerExecutable != "":
			LOGGER.debug("> Chosen custom Images Previewer executable: '{0}'.".format(customPreviewerExecutable))
			self.Custom_Previewer_Path_lineEdit.setText(QString(customPreviewerExecutable))
			self.__settings.setKey(self.__settingsSection,
									"customPreviewer",
									self.Custom_Previewer_Path_lineEdit.text())

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError)
	def __Custom_Previewer_Path_lineEdit__editFinished(self):
		"""
		This method is triggered when **Custom_Previewer_Path_lineEdit** Widget is edited and check that entered path is valid.
		"""

		value = foundations.strings.encode(self.Custom_Previewer_Path_lineEdit.text())
		if not foundations.common.pathExists(os.path.abspath(value)) and value != unicode():
			LOGGER.debug("> Restoring preferences!")
			self.__Custom_Previewer_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError("{0} | Invalid custom Images Previewer executable file!".format(
			self.__class__.__name__))
		else:
			self.__settings.setKey(self.__settingsSection, "customPreviewer", self.Custom_Previewer_Path_lineEdit.text())

	def __hasMaximumImagesPreviewersInstances(self):
		"""
		This method returns if the maximum Previewers instances allowed is reached.

		:return: Maximum instances reached. ( Boolean )
		"""

		if len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
			self.__engine.notificationsManager.warnify(
			"{0} | You can only launch '{1}' images Previewer instances at same time!".format(
			self.__class__.__name__, self.__maximumImagesPreviewersInstances))
			return True
		else:
			return False

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def viewIblSetsImagesUi(self, imageType, *args):
		"""
		This method launches selected Ibl Sets Images Previewer.

		:param imageType: Image type. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method success. ( Boolean )
		
		:note: This method may require user interaction.
		"""

		selectedIblSets = self.__iblSetsOutliner.getSelectedIblSets()
		success = True
		for iblSet in selectedIblSets:
			if self.__hasMaximumImagesPreviewersInstances():
				break

			paths = self.getIblSetImagesPaths(iblSet, imageType)
			if paths:
				success *= self.viewImages(paths, \
				foundations.strings.encode(self.Custom_Previewer_Path_lineEdit.text())) or False
			else:
				self.__engine.notificationsManager.warnify(
				"{0} | '{1}' Ibl Set has no '{2}' image type and will be skipped!".format(
				self.__class__.__name__, iblSet.title, imageType))

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while displaying '{1}' Ibl Set(s) image(s)!".format(
			self.__class__.__name__, ", ". join((iblSet.title for iblSet in selectedIblSets))))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.FileExistsError,
											Exception)
	def viewActiveIblSetImagesUi(self, imageType, *args):
		"""
		This method launches :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set Images Previewer.

		:param imageType: Image type. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method success. ( Boolean )
		
		:note: This method may require user interaction.
		"""

		activeIblSet = self.__inspector.activeIblSet
		if activeIblSet is None:
			return False

		if not foundations.common.pathExists(activeIblSet.path):
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while opening Inspector Ibl Set directory: '{1}' Ibl Set file doesn't exists!".format(
			self.__class__.__name__, activeIblSet.title))

		if self.__hasMaximumImagesPreviewersInstances():
			return False

		paths = self.getIblSetImagesPaths(activeIblSet, imageType)
		if paths:
			if self.viewImages(paths, \
			foundations.strings.encode(self.Custom_Previewer_Path_lineEdit.text())):
				return True
			else:
				raise Exception("{0} | Exception raised while displaying '{1}' inspector Ibl Set image(s)!".format(
				self.__class__.__name__, activeIblSet.title))
		else:
			self.__engine.notificationsManager.warnify(
			"{0} | '{1}' Inspector Ibl Set has no '{2}' image type!".format(self.__class__.__name__,
																		activeIblSet.title,
																		imageType))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def viewImages(self, paths, customPreviewer=None):
		"""
		This method launches an Ibl Set Images Previewer.

		:param paths: Image paths. ( List )
		:param customPreviewer: Custom previewer. ( String )
		"""

		if customPreviewer:
			previewCommand = self.getProcessCommand(paths, customPreviewer)
			if previewCommand:
				LOGGER.debug("> Current image preview command: '{0}'.".format(previewCommand))
				LOGGER.info("{0} | Launching Previewer with '{1}' images paths.".format(self.__class__.__name__,
																						", ".join(paths)))
				editProcess = QProcess()
				editProcess.startDetached(previewCommand)
				return True
			else:
				raise Exception("{0} | Exception raised: No suitable process command given!".format(
				self.__class__.__name__))
		else:
			if not len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				return self.getImagesPreviewer(paths)
			else:
				LOGGER.warning("!> {0} | You can only launch '{1}' images Previewer instances at same time!".format(
				self.__class__.__name__, self.__maximumImagesPreviewersInstances))

	def addImagesPreviewer(self, imagesPreviewer):
		"""
		This method adds an Images Previewer.

		:param imagesPreviewer: Images Previewer. ( ImagesPreviewer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' Images Previewer.".format(imagesPreviewer))

		self.__imagesPreviewers.append(imagesPreviewer)
		return True

	def removeImagesPreviewer(self, imagesPreviewer):
		"""
		This method removes an Images Previewer.

		:param imagesPreviewer: Images Previewer. ( ImagesPreviewer )
		"""

		LOGGER.debug("> Removing '{0}' Images Previewer.".format(imagesPreviewer))

		self.__imagesPreviewers.remove(imagesPreviewer)
		return True

	@umbra.ui.common.showWaitCursor
	@umbra.engine.showProcessing("Reading Images...")
	def getImagesPreviewer(self, paths):
		"""
		This method launches an Images Previewer.

		:param paths: Images paths. ( List )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Launching Images Previewer for '{0}' images.".format(", ".join(paths)))

		self.addImagesPreviewer(ImagesPreviewer(self, paths, Qt.Window))
		self.__imagesPreviewers[-1].show()
		return True

	def getProcessCommand(self, paths, customPreviewer):
		"""
		This method gets process command.

		:param paths: Paths to preview. ( String )
		:param customPreviewer: Custom browser. ( String )
		:return: Process command. ( String )
		"""

		processCommand = None
		imagesPaths = [os.path.normpath(path) for path in paths]
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			processCommand = "\"{0}\" \"{1}\"".format(customPreviewer, " ".join(imagesPaths))
		elif platform.system() == "Darwin":
			processCommand = "open -a \"{0}\" \"{1}\"".format(customPreviewer, " ".join(imagesPaths))
		elif platform.system() == "Linux":
			processCommand = "\"{0}\" \"{1}\"".format(customPreviewer, " ".join(imagesPaths))
		return processCommand

	def getIblSetImagesPaths(self, iblSet, imageType):
		"""
		This method gets Ibl Set images paths.

		:param iblSet: Ibl Set. ( IblSet )
		:param imageType: Image type. ( String )
		:return: Images paths. ( List )
		"""

		imagePaths = []
		if imageType == "Background":
			path = iblSet.backgroundImage
			path and imagePaths.append(path)
		elif imageType == "Lighting":
			path = iblSet.lightingImage
			path and imagePaths.append(path)
		elif imageType == "Reflection":
			path = iblSet.reflectionImage
			path and imagePaths.append(path)
		elif imageType == "Plate":
			if foundations.common.pathExists(iblSet.path):
				LOGGER.debug("> Parsing Inspector Ibl Set file: '{0}'.".format(iblSet))
				sectionsFileParser = SectionsFileParser(iblSet.path)
				sectionsFileParser.read() and sectionsFileParser.parse()
				for section in sectionsFileParser.sections:
					if re.search(r"Plate\d+", section):
						imagePaths.append(os.path.normpath(os.path.join(os.path.dirname(iblSet.path),
																	sectionsFileParser.getValue("PLATEfile", section))))

		for path in imagePaths[:]:
			if not foundations.common.pathExists(path):
				imagePaths.remove(path) and LOGGER.warning(
				"!> {0} | '{1}' image file doesn't exists and will be skipped!".format(self.__class__.__name__, path))
		return imagePaths
