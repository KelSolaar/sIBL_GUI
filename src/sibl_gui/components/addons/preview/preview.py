#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preview.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Preview` Component Interface class, the :class:`ImagesPreviewer` class and others images preview related objects.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import logging
import os
import platform
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from foundations.parsers import SectionsFileParser
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.addons.preview.imagesPreviewer import ImagesPreviewer
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Preview"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Preview.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Preview(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	This class is the **Preview** class.
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(Preview, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__uiResources = "resources"

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryPreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None

		self.__imagesPreviewers = None
		self.__maximumImagesPreviewersInstances = 5

		self.__inspectorButtons = {"Background" : {"object" : None, "text": "View Background Image", "row" : 1, "column" : 3},
									"Lighting" : {"object" : None, "text": "View Lighting Image", "row" : 1, "column" : 4},
									"Reflection" : {"object" : None, "text": "View Reflection Image", "row" : 1, "column" : 5},
									"Plates" : {"object" : None, "text": "View Plate(s)", "row" : 1, "column" : 6}}

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiResources(self):
		"""
		This method is the property for **self.__uiResources** attribute.

		:return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for **self.__uiResources** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for **self.__uiResources** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

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

	@property
	def imagesPreviewers(self):
		"""
		This method is the property for **self.__imagesPreviewers** attribute.

		:return: self.__imagesPreviewers. ( List )
		"""

		return self.__imagesPreviewers

	@imagesPreviewers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagesPreviewers(self, value):
		"""
		This method is the setter method for **self.__imagesPreviewers** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("imagesPreviewers"))

	@imagesPreviewers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagesPreviewers(self):
		"""
		This method is the deleter method for **self.__imagesPreviewers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("imagesPreviewers"))

	@property
	def maximumImagesPreviewersInstances(self):
		"""
		This method is the property for **self.__maximumImagesPreviewersInstances** attribute.

		:return: self.__maximumImagesPreviewersInstances. ( Integer )
		"""

		return self.__maximumImagesPreviewersInstances

	@maximumImagesPreviewersInstances.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumImagesPreviewersInstances(self, value):
		"""
		This method is the setter method for **self.__maximumImagesPreviewersInstances** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("maximumImagesPreviewersInstances"))

	@maximumImagesPreviewersInstances.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumImagesPreviewersInstances(self):
		"""
		This method is the deleter method for **self.__maximumImagesPreviewersInstances** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("maximumImagesPreviewersInstances"))

	@property
	def inspectorButtons(self):
		"""
		This method is the property for **self.__inspectorButtons** attribute.

		:return: self.__inspectorButtons. ( Dictionary )
		"""

		return self.__inspectorButtons

	@inspectorButtons.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorButtons(self, value):
		"""
		This method is the setter method for **self.__inspectorButtons** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("inspectorButtons"))

	@inspectorButtons.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorButtons(self):
		"""
		This method is the deleter method for **self.__inspectorButtons** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("inspectorButtons"))

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

		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__factoryPreferencesManager = self.__container.componentsManager.components["factory.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreInspector = self.__container.componentsManager.components["core.inspector"].interface

		self.__imagesPreviewers = []

		self.activated = True
		return True

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResources = os.path.basename(self.__uiResources)
		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryPreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreInspector = None

		for imagesPreviewer in self.__imagesPreviewers[:]:
			imagesPreviewer.ui.close()

		self.activated = False
		return True

	@core.executionTrace
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

		return True

	@core.executionTrace
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

		return True

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__factoryPreferencesManager.Others_Preferences_gridLayout.addWidget(self.Custom_Previewer_Path_groupBox)

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__factoryPreferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.Custom_Previewer_Path_groupBox.setParent(None)

		return True

	@core.executionTrace
	def __addActions(self):
		"""
		This method adds actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		separatorAction = QAction(self.__coreDatabaseBrowser.Database_Browser_listView)
		separatorAction.setSeparator(True)
		self.__coreDatabaseBrowser.Database_Browser_listView.addAction(separatorAction)

		self.__coreDatabaseBrowser.Database_Browser_listView.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|View Background Image ...", slot=self.__Database_Browser_listView_viewIblSetsBackgroundImagesAction__triggered))
		self.__coreDatabaseBrowser.Database_Browser_listView.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|View Lighting Image ...", slot=self.__Database_Browser_listView_viewIblSetsLightingImagesAction__triggered))
		self.__coreDatabaseBrowser.Database_Browser_listView.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|View Reflection Image ...", slot=self.__Database_Browser_listView_viewIblSetsReflectionImagesAction__triggered))
		self.__coreDatabaseBrowser.Database_Browser_listView.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|core.databaseBrowser|View Plate(s) ...", slot=self.__Database_Browser_listView_viewIblSetsPlatesAction__triggered))

		separatorAction = QAction(self.__coreInspector.Inspector_Overall_frame)
		separatorAction.setSeparator(True)
		self.__coreInspector.Inspector_Overall_frame.addAction(separatorAction)

		self.__coreInspector.Inspector_Overall_frame.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|core.inspector|View Background Image ...", slot=self.__Inspector_Overall_frame_viewInspectorIblSetBackgroundImageAction__triggered))
		self.__coreInspector.Inspector_Overall_frame.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|core.inspector|View Lighting Image ...", slot=self.__Inspector_Overall_frame_viewInspectorIblSetLightingImageAction__triggered))
		self.__coreInspector.Inspector_Overall_frame.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|core.inspector|View Reflection Image ...", slot=self.__Inspector_Overall_frame_viewInspectorIblSetReflectionImageAction__triggered))
		self.__coreInspector.Inspector_Overall_frame.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|core.inspector|View Plate(s) ...", slot=self.__Inspector_Overall_frame_viewInspectorIblSetPlatesAction__triggered))

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		viewIblSetsBackgroundImagesAction = "Actions|Umbra|Components|core.databaseBrowser|View Background Image ..."
		self.__coreDatabaseBrowser.Database_Browser_listView.removeAction(self.__container.actionsManager.getAction(viewIblSetsBackgroundImagesAction))
		self.__container.actionsManager.unregisterAction(viewIblSetsBackgroundImagesAction)
		viewIblSetsLightingImagesAction = "Actions|Umbra|Components|core.databaseBrowser|View Lighting Image ..."
		self.__coreDatabaseBrowser.Database_Browser_listView.removeAction(self.__container.actionsManager.getAction(viewIblSetsLightingImagesAction))
		self.__container.actionsManager.unregisterAction(viewIblSetsLightingImagesAction)
		viewIblSetsReflectionImagesAction = "Actions|Umbra|Components|core.databaseBrowser|View Reflection Image ..."
		self.__coreDatabaseBrowser.Database_Browser_listView.removeAction(self.__container.actionsManager.getAction(viewIblSetsReflectionImagesAction))
		self.__container.actionsManager.unregisterAction(viewIblSetsReflectionImagesAction)
		viewIblSetsPlatesAction = "Actions|Umbra|Components|core.databaseBrowser|View Plate(s) ..."
		self.__coreDatabaseBrowser.Database_Browser_listView.removeAction(self.__container.actionsManager.getAction(viewIblSetsPlatesAction))
		self.__container.actionsManager.unregisterAction(viewIblSetsPlatesAction)

		viewInspectorIblSetBackgroundImageAction = "Actions|Umbra|Components|core.inspector|View Background Image ..."
		self.__coreInspector.Inspector_Overall_frame.removeAction(self.__container.actionsManager.getAction(viewInspectorIblSetBackgroundImageAction))
		self.__container.actionsManager.unregisterAction(viewInspectorIblSetBackgroundImageAction)
		viewInspectorIblSetLightingImageAction = "Actions|Umbra|Components|core.inspector|View Lighting Image ..."
		self.__coreInspector.Inspector_Overall_frame.removeAction(self.__container.actionsManager.getAction(viewInspectorIblSetLightingImageAction))
		self.__container.actionsManager.unregisterAction(viewInspectorIblSetLightingImageAction)
		viewInspectorIblSetReflectionImageAction = "Actions|Umbra|Components|core.inspector|View Reflection Image ..."
		self.__coreInspector.Inspector_Overall_frame.removeAction(self.__container.actionsManager.getAction(viewInspectorIblSetReflectionImageAction))
		self.__container.actionsManager.unregisterAction(viewInspectorIblSetReflectionImageAction)
		viewInspectorIblSetPlatesAction = "Actions|Umbra|Components|core.inspector|View Plate(s) ..."
		self.__coreInspector.Inspector_Overall_frame.removeAction(self.__container.actionsManager.getAction(viewInspectorIblSetPlatesAction))
		self.__container.actionsManager.unregisterAction(viewInspectorIblSetPlatesAction)

	@core.executionTrace
	def __addInspectorButtons(self):
		"""
		This method adds buttons to the :mod:`umbra.components.core.inspector.inspector` Component.
		"""

		self.__coreInspector.Inspector_Options_groupBox.show()
		for key, value in self.__inspectorButtons.items():
			value["object"] = QPushButton(value["text"])
			self.__coreInspector.Inspector_Options_groupBox_gridLayout.addWidget(value["object"], value["row"], value["column"])
			value["object"].clicked.connect(functools.partial(self.viewIblSetsImages_ui, key))

	def __removeInspectorButtons(self):
		"""
		This method removes buttons from the :mod:`umbra.components.core.inspector.inspector` Component.
		"""

		for value in self.__inspectorButtons.values():
			value["object"].setParent(None)

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsBackgroundImagesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|View Background Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImages_ui("Background")

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsLightingImagesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|View Lighting Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImages_ui("Lighting")

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsReflectionImagesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|View Reflection Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImages_ui("Reflection")

	@core.executionTrace
	def __Database_Browser_listView_viewIblSetsPlatesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.databaseBrowser|View Plate(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImages_ui("Plates")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetBackgroundImageAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|View Background Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImages_ui("Background")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetLightingImageAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|View Lighting Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImages_ui("Lighting")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetReflectionImageAction__triggered(self, checked):
		"""
		This method is triggered by **'"Actions|Umbra|Components|core.inspector|View Reflection Image ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImages_ui("Reflection")

	@core.executionTrace
	def __Inspector_Overall_frame_viewInspectorIblSetPlatesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.inspector|View Plate(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.viewIblSetsImages_ui("Plates")

	@core.executionTrace
	def __Custom_Previewer_Path_lineEdit_setUi(self):
		"""
		This method fills **Custom_Previewer_Path_lineEdit** Widget.
		"""

		customPreviewer = self.__settings.getKey(self.__settingsSection, "customPreviewer")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Custom_Previewer_Path_lineEdit", customPreviewer.toString()))
		self.Custom_Previewer_Path_lineEdit.setText(customPreviewer.toString())

	@core.executionTrace
	def __Custom_Previewer_Path_toolButton__clicked(self, checked):
		"""
		This method is called when **Custom_Previewer_Path_toolButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		customPreviewerExecutable = umbra.ui.common.storeLastBrowsedPath(QFileDialog.getOpenFileName(self, "Custom previewer executable:", RuntimeGlobals.lastBrowsedPath))
		if customPreviewerExecutable != "":
			LOGGER.debug("> Chosen custom Images Previewer executable: '{0}'.".format(customPreviewerExecutable))
			self.Custom_Previewer_Path_lineEdit.setText(QString(customPreviewerExecutable))
			self.__settings.setKey(self.__settingsSection, "customPreviewer", self.Custom_Previewer_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __Custom_Previewer_Path_lineEdit__editFinished(self):
		"""
		This method is called when **Custom_Previewer_Path_lineEdit** Widget is edited and check that entered path is valid.
		"""

		if not os.path.exists(os.path.abspath(str(self.Custom_Previewer_Path_lineEdit.text()))) and str(self.Custom_Previewer_Path_lineEdit.text()) != "":
			LOGGER.debug("> Restoring preferences!")
			self.__Custom_Previewer_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError("{0} | Invalid custom Images Previewer executable file!".format(self.__class__.__name__))
		else:
			self.__settings.setKey(self.__settingsSection, "customPreviewer", self.Custom_Previewer_Path_lineEdit.text())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def viewIblSetsImages_ui(self, imageType, *args):
		"""
		This method launches selected Ibl Sets Images Previewer.

		:param imageType: Image type. ( String )
		:param \*args: Arguments. ( \* )

		:note: This method may require user interaction.
		"""

		success = True
		for iblSet in self.__coreDatabaseBrowser.getSelectedIblSets():
			if len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				messageBox.messageBox("Warning", "Warning", "{0} | You can only launch '{1}' images Previewer instances at same time!".format(self.__class__.__name__, self.__maximumImagesPreviewersInstances))
				break
			paths = self.getIblSetImagesPaths(iblSet, imageType)
			if paths:
				success *= self.viewImages(paths, str(self.Custom_Previewer_Path_lineEdit.text())) or False
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Ibl Set has no '{2}' image type and will be skipped!".format(self.__class__.__name__, iblSet.title, imageType))
		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while displaying '{1}' Ibl Set image(s)!".format(self.__class__.__name__, iblSet.title))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.FileExistsError, Exception)
	def viewInspectorIblSetImages_ui(self, imageType, *args):
		"""
		This method launches :mod:`umbra.components.core.inspector.inspector` Component Ibl Set Images Previewer.

		:param imageType: Image type. ( String )
		:param \*args: Arguments. ( \* )

		:note: This method may require user interaction.
		"""

		inspectorIblSet = self.__coreInspector.inspectorIblSet
		inspectorIblSet = inspectorIblSet and os.path.exists(inspectorIblSet.path) and inspectorIblSet or None
		if inspectorIblSet:
			if len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				messageBox.messageBox("Warning", "Warning", "{0} | You can only launch '{1}' images Previewer instances at same time!".format(self.__class__.__name__, self.__maximumImagesPreviewersInstances))
			paths = self.getIblSetImagesPaths(inspectorIblSet, imageType)
			if paths:
				if self.viewImages(paths, str(self.Custom_Previewer_Path_lineEdit.text())):
					return True
				else:
					raise Exception("{0} | Exception raised while displaying '{1}' inspector Ibl Set image(s)!".format(self.__class__.__name__, inspectorIblSet.title))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' inspector Ibl Set has no '{2}' image type!".format(self.__class__.__name__, inspectorIblSet.title, imageType))
		else:
			raise foundations.exceptions.FileExistsError("{0} | Exception raised while opening Inspector Ibl Set directory: '{1}' Ibl Set file doesn't exists!".format(self.__class__.__name__, inspectorIblSet.title))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
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
				LOGGER.info("{0} | Launching Previewer with '{1}' images paths.".format(self.__class__.__name__, ", ".join(paths)))
				editProcess = QProcess()
				editProcess.startDetached(previewCommand)
				return True
			else:
				raise Exception("{0} | Exception raised: No suitable process command provided!".format(self.__class__.__name__))
		else:
			if not len(self.__imagesPreviewers) >= self.__maximumImagesPreviewersInstances:
				return self.getImagesPreviewer(paths)
			else:
				LOGGER.warning("!> {0} | You can only launch '{1}' images Previewer instances at same time!".format(self.__class__.__name__, self.__maximumImagesPreviewersInstances))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addImagesPreviewer(self, imagesPreviewer):
		"""
		This method adds an Images Previewer.

		:param imagesPreviewer: Images Previewer. ( ImagesPreviewer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' Images Previewer.".format(imagesPreviewer))

		self.__imagesPreviewers.append(imagesPreviewer)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeImagesPreviewer(self, imagesPreviewer):
		"""
		This method removes an Images Previewer.

		:param imagesPreviewer: Images Previewer. ( ImagesPreviewer )
		"""

		LOGGER.debug("> Removing '{0}' Images Previewer.".format(imagesPreviewer))

		self.__imagesPreviewers.remove(imagesPreviewer)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getImagesPreviewer(self, paths):
		"""
		This method launches an Images Previewer.

		:param paths: Images paths. ( List )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Launching Images Previewer for '{0}' image.".format(paths))

		self.addImagesPreviewer(ImagesPreviewer(self, paths, Qt.Window))
		self.__imagesPreviewers[-1].show()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getIblSetImagesPaths(self, iblSet, imageType):
		"""
		This method gets Ibl Set images paths.

		:param iblSet: Ibl Set. ( DbIblSet )
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
		elif imageType == "Plates":
			if os.path.exists(iblSet.path):
				LOGGER.debug("> Parsing Inspector Ibl Set file: '{0}'.".format(iblSet))
				sectionsFileParser = SectionsFileParser(iblSet.path)
				sectionsFileParser.read() and sectionsFileParser.parse()
				for section in sectionsFileParser.sections:
					if re.search("Plate[0-9]+", section):
						imagePaths.append(os.path.normpath(os.path.join(os.path.dirname(iblSet.path), sectionsFileParser.getValue("PLATEfile", section))))

		for path in imagePaths[:]:
			if not os.path.exists(path):
				imagePaths.remove(path) and LOGGER.warning("!> {0} | '{1}' image file doesn't exists and will be skipped!".format(self.__class__.__name__, path))
		return imagePaths
