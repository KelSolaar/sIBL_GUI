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
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**componentsManagerUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Components Manager Ui Component Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import traceback

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
def _componentActivationErrorHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides an exception handler for Component activation.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	"""

	umbra.ui.common.uiBasicExceptionHandler(Exception("{0} | An exception occurred while activating '{1}' Component:\n{2}".format(core.getModule(_componentActivationErrorHandler).__name__, args[1].name, traceback.format_exc())), origin, *args, **kwargs)

@core.executionTrace
def _componentDeactivationErrorHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides an exception handler for Component deactivation.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	"""

	umbra.ui.common.uiBasicExceptionHandler(Exception("{0} | An exception occurred while deactivating '{1}' Component:\n{2}".format(core.getModule(_componentDeactivationErrorHandler).__name__, args[1].name, traceback.format_exc())), origin, *args, **kwargs)

@core.executionTrace
def _componentReloadErrorHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides an exception handler for Component reload.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	"""

	umbra.ui.common.uiBasicExceptionHandler(Exception("{0} | An exception occurred while reloading '{1}' Component:\n{2}".format(core.getModule(_componentReloadErrorHandler).__name__, args[1].name, traceback.format_exc())), origin, *args, **kwargs)

class ComponentsManagerUi(UiComponent):
	"""
	This class is the ComponentsManagerUi class.
	"""

	# Custom signals definitions.
	modelChanged = pyqtSignal()
	modelRefresh = pyqtSignal()
	modelPartialRefresh = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		@param name: Component name. ( String )
		@param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiPath = "ui/Components_Manager_Ui.ui"
		self.__uiResources = "resources"
		self.__uiActivatedImage = "Activated.png"
		self.__uiDeactivatedImage = "Deactivated.png"
		self.__uiCategorieAffixe = "_Categorie.png"
		self.__dockArea = 1

		self.__container = None
		self.__settings = None

		self.__model = None

		self.__modelHeaders = [ "Components", "Activated", "Categorie", "Rank", "Version" ]
		self.__treeWidgetIndentation = 15
		self.__treeViewInnerMargins = QMargins(0, 0, 0, 12)
		self.__componentsInformationsDefaultText = "<center><h4>* * *</h4>Select Some Components to display related informations!<h4>* * *</h4></center>"
		self.__componentsInformationsText = """
											<h4><center>{0}</center></h4>
											<p>
											<b>Categorie:</b> {1}
											<br/>
											<b>Author:</b> {2}
											<br/>
											<b>Email:</b> <a href="mailto:{3}"><span style=" text-decoration: underline; color:#e0e0e0;">{3}</span></a>
											<br/>
											<b>Url:</b> <a href="{4}"><span style=" text-decoration: underline; color:#e0e0e0;">{4}</span></a>
											<p>
											<b>Description:</b> {5}
											</p>
											</p>
											"""

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for the _uiPath attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for the _uiPath attribute.

		@param value: Attribute value. ( String )
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
	def uiResources(self):
		"""
		This method is the property for the _uiResources attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for the _uiResources attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for the _uiResources attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiActivatedImage(self):
		"""
		This method is the property for the _uiActivatedImage attribute.

		@return: self.__uiActivatedImage. ( String )
		"""

		return self.__uiActivatedImage

	@uiActivatedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiActivatedImage(self, value):
		"""
		This method is the setter method for the _uiActivatedImage attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiActivatedImage"))

	@uiActivatedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiActivatedImage(self):
		"""
		This method is the deleter method for the _uiActivatedImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiActivatedImage"))

	@property
	def uiDeactivatedImage(self):
		"""
		This method is the property for the _uiDeactivatedImage attribute.

		@return: self.__uiDeactivatedImage. ( String )
		"""

		return self.__uiDeactivatedImage

	@uiDeactivatedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDeactivatedImage(self, value):
		"""
		This method is the setter method for the _uiDeactivatedImage attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiDeactivatedImage"))

	@uiDeactivatedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDeactivatedImage(self):
		"""
		This method is the deleter method for the _uiDeactivatedImage attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiDeactivatedImage"))

	@property
	def uiCategorieAffixe(self):
		"""
		This method is the property for the _uiCategorieAffixe attribute.

		@return: self.__uiCategorieAffixe. ( String )
		"""

		return self.__uiCategorieAffixe

	@uiCategorieAffixe.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiCategorieAffixe(self, value):
		"""
		This method is the setter method for the _uiCategorieAffixe attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiCategorieAffixe"))

	@uiCategorieAffixe.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiCategorieAffixe(self):
		"""
		This method is the deleter method for the _uiCategorieAffixe attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiCategorieAffixe"))

	@property
	def dockArea(self):
		"""
		This method is the property for the _dockArea attribute.

		@return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for the _dockArea attribute.

		@param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for the _dockArea attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		@param value: Attribute value. ( QObject )
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

		@return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for the _settings attribute.

		@param value: Attribute value. ( QSettings )
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
	def model(self):
		"""
		This method is the property for the _model attribute.

		@return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for the _model attribute.

		@param value: Attribute value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for the _model attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("model"))

	@property
	def modelHeaders(self):
		"""
		This method is the property for the _modelHeaders attribute.

		@return: self.__modelHeaders. ( List )
		"""

		return self.__modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self, value):
		"""
		This method is the setter method for the _modelHeaders attribute.

		@param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("modelHeaders"))

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self):
		"""
		This method is the deleter method for the _modelHeaders attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("modelHeaders"))

	@property
	def treeWidgetIndentation(self):
		"""
		This method is the property for the _treeWidgetIndentation attribute.

		@return: self.__treeWidgetIndentation. ( Integer )
		"""

		return self.__treeWidgetIndentation

	@treeWidgetIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeWidgetIndentation(self, value):
		"""
		This method is the setter method for the _treeWidgetIndentation attribute.

		@param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("treeWidgetIndentation"))

	@treeWidgetIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeWidgetIndentation(self):
		"""
		This method is the deleter method for the _treeWidgetIndentation attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("treeWidgetIndentation"))

	@property
	def treeViewInnerMargins(self):
		"""
		This method is the property for the _treeViewInnerMargins attribute.

		@return: self.__treeViewInnerMargins. ( Integer )
		"""

		return self.__treeViewInnerMargins

	@treeViewInnerMargins.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self, value):
		"""
		This method is the setter method for the _treeViewInnerMargins attribute.

		@param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("treeViewInnerMargins"))

	@treeViewInnerMargins.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self):
		"""
		This method is the deleter method for the _treeViewInnerMargins attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("treeViewInnerMargins"))

	@property
	def componentsInformationsDefaultText(self):
		"""
		This method is the property for the _componentsInformationsDefaultText attribute.

		@return: self.__componentsInformationsDefaultText. ( String )
		"""

		return self.__componentsInformationsDefaultText

	@componentsInformationsDefaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsDefaultText(self, value):
		"""
		This method is the setter method for the _componentsInformationsDefaultText attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("componentsInformationsDefaultText"))

	@componentsInformationsDefaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsDefaultText(self):
		"""
		This method is the deleter method for the _componentsInformationsDefaultText attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("componentsInformationsDefaultText"))

	@property
	def componentsInformationsText(self):
		"""
		This method is the property for the _componentsInformationsText attribute.

		@return: self.__componentsInformationsText. ( String )
		"""

		return self.__componentsInformationsText

	@componentsInformationsText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsText(self, value):
		"""
		This method is the setter method for the _componentsInformationsText attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("componentsInformationsText"))

	@componentsInformationsText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsText(self):
		"""
		This method is the deleter method for the _componentsInformationsText attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("componentsInformationsText"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		@param container: Container to attach the Component to. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container

		self.__settings = self.__container.settings

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component cannot be deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__model = QStandardItemModel()
		self.__Components_Manager_Ui_treeView_setModel()

		self.ui.Components_Manager_Ui_gridLayout.setContentsMargins(self.__treeViewInnerMargins)

		self.ui.Components_Manager_Ui_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Components_Manager_Ui_treeView_addActions()

		self.__Components_Manager_Ui_treeView_setView()

		self.ui.Components_Informations_textBrowser.setText(self.__componentsInformationsDefaultText)

		self.ui.Components_Manager_Ui_splitter.setSizes([ 16777215, 1 ])

		# Signals / Slots.
		self.ui.Components_Manager_Ui_treeView.selectionModel().selectionChanged.connect(self.__Components_Manager_Ui_treeView_selectionModel__selectionChanged)
		self.modelChanged.connect(self.__Components_Manager_Ui_treeView_refreshView)
		self.modelRefresh.connect(self.__Components_Manager_Ui_treeView_refreshModel)
		self.modelPartialRefresh.connect(self.__Components_Manager_Ui_treeView_setActivationsStatus)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component ui cannot be uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget cannot be removed!".format(self.name))

	@core.executionTrace
	def onStartup(self):
		"""
		This method is called on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework startup method.".format(self.__class__.__name__))

		self.__Components_Manager_Ui_treeView_setActivationsStatus()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setModel(self):
		"""
		This method sets the Components_Manager_Ui_treeView Model.

		Columns:
		Collections | Activated | Categorie | Rank | Version

		Rows:
		* Path: { _type: "Path" }
		** Component: { _type: "Component", _datas: profile }
		"""

		LOGGER.debug("> Setting up '{0}' Model!".format("Components_Manager_Ui_treeView"))

		self.__model.clear()

		self.__model.setHorizontalHeaderLabels(self.__modelHeaders)
		self.__model.setColumnCount(len(self.__modelHeaders))

		for path in self.__container.componentsManager.paths:
			components = [component for component in self.__container.componentsManager.components if os.path.normpath(self.__container.componentsManager.paths[path]) in os.path.normpath(self.__container.componentsManager.components[component].path)]

			if components:
				pathStandardItem = QStandardItem(QString(path))
				pathStandardItem._type = "Path"

				LOGGER.debug("> Adding '{0}' path to '{1}' Model.".format(path, "Components_Manager_Ui_treeView"))
				self.__model.appendRow(pathStandardItem)

				for component in components:
					componentStandardItem = QStandardItem(QString(strings.getNiceName(self.__container.componentsManager.components[component].module)))
					iconPath = os.path.join(self.__uiResources, "{0}{1}".format(strings.getNiceName(self.__container.componentsManager.components[component].categorie), self.__uiCategorieAffixe))
					componentStandardItem.setIcon(QIcon(iconPath))

					componentActivationStandardItem = QStandardItem(QString(str(self.__container.componentsManager.components[component].interface.activated)))
					iconPath = self.__container.componentsManager.components[component].interface.activated and os.path.join(self.__uiResources, self.__uiActivatedImage) or os.path.join(self.__uiResources, self.__uiDeactivatedImage)
					componentActivationStandardItem.setIcon(QIcon(iconPath))

					componentCategorieStandardItem = QStandardItem(QString(self.__container.componentsManager.components[component].categorie and strings.getNiceName(self.__container.componentsManager.components[component].categorie) or ""))
					componentCategorieStandardItem.setTextAlignment(Qt.AlignCenter)

					componentRankStandardItem = QStandardItem(QString(self.__container.componentsManager.components[component].rank or ""))
					componentRankStandardItem.setTextAlignment(Qt.AlignCenter)

					componentVersionStandardItem = QStandardItem(QString(self.__container.componentsManager.components[component].version or ""))
					componentVersionStandardItem.setTextAlignment(Qt.AlignCenter)

					componentStandardItem._datas = self.__container.componentsManager.components[component]
					componentStandardItem._type = "Component"

					LOGGER.debug("> Adding '{0}' Component to '{1}'.".format(component, "Components_Manager_Ui_treeView"))
					pathStandardItem.appendRow([componentStandardItem, componentActivationStandardItem, componentCategorieStandardItem, componentRankStandardItem, componentVersionStandardItem])

		self.emit(SIGNAL("modelChanged()"))

	@core.executionTrace
	def __Components_Manager_Ui_treeView_refreshModel(self):
		"""
		This method refreshes the Components_Manager_Ui_treeView Model.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Components_Manager_Ui_treeView"))

		self.__Components_Manager_Ui_treeView_setModel()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setView(self):
		"""
		This method sets the Components_Manager_Ui_treeView View.
		"""

		LOGGER.debug("> Refreshing '{0}' ui!".format(self.__class__.__name__))

		self.ui.Components_Manager_Ui_treeView.setAutoScroll(False)
		self.ui.Components_Manager_Ui_treeView.setDragDropMode(QAbstractItemView.NoDragDrop)
		self.ui.Components_Manager_Ui_treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.ui.Components_Manager_Ui_treeView.setIndentation(self.__treeWidgetIndentation)
		self.ui.Components_Manager_Ui_treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.Components_Manager_Ui_treeView.setSortingEnabled(True)

		self.ui.Components_Manager_Ui_treeView.setModel(self.__model)

		self.__Components_Manager_Ui_treeView_setDefaultViewState()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setDefaultViewState(self):
		"""
		This method sets Components_Manager_Ui_treeView default View state.
		"""

		LOGGER.debug("> Setting '{0}' default View state!".format("Components_Manager_Ui_treeView"))

		self.ui.Components_Manager_Ui_treeView.expandAll()
		for column in range(len(self.__modelHeaders)):
			self.ui.Components_Manager_Ui_treeView.resizeColumnToContents(column)

		self.ui.Components_Manager_Ui_treeView.sortByColumn(0, Qt.AscendingOrder)

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setActivationsStatus(self):
		"""
		This method sets the Components_Manager_Ui_treeView activations status.
		"""

		for i in range(self.__model.rowCount()):
			for j in range(self.__model.item(i).rowCount()):
				componentStandardItem = self.__model.item(i).child(j, 0)
				componentActivationStandardItem = self.__model.item(i).child(j, 1)
				componentActivationStandardItem.setText(str(componentStandardItem._datas.interface.activated))
				iconPath = componentStandardItem._datas.interface.activated and os.path.join(self.__uiResources, self.__uiActivatedImage) or os.path.join(self.__uiResources, self.__uiDeactivatedImage)
				componentActivationStandardItem.setIcon(QIcon(iconPath))

	@core.executionTrace
	def __Components_Manager_Ui_treeView_refreshView(self):
		"""
		This method refreshes the Components_Manager_Ui_treeView View.
		"""

		self.__Components_Manager_Ui_treeView_setDefaultViewState()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_addActions(self):
		"""
		This method sets the Components_Manager_Ui_treeView actions.
		"""

		activateComponentsAction = QAction("Activate Component(s)", self.ui.Components_Manager_Ui_treeView)
		activateComponentsAction.triggered.connect(self.__Components_Manager_Ui_treeView_activateComponentsAction__triggered)
		self.ui.Components_Manager_Ui_treeView.addAction(activateComponentsAction)

		deactivateComponentsAction = QAction("Deactivate Component(s)", self.ui.Components_Manager_Ui_treeView)
		deactivateComponentsAction.triggered.connect(self.__Components_Manager_Ui_treeView_deactivateComponentsAction__triggered)
		self.ui.Components_Manager_Ui_treeView.addAction(deactivateComponentsAction)

		separatorAction = QAction(self.ui.Components_Manager_Ui_treeView)
		separatorAction.setSeparator(True)
		self.ui.Components_Manager_Ui_treeView.addAction(separatorAction)

		reloadComponentsAction = QAction("Reload Component(s)", self.ui.Components_Manager_Ui_treeView)
		reloadComponentsAction.triggered.connect(self.__Components_Manager_Ui_treeView_reloadComponentsAction__triggered)
		self.ui.Components_Manager_Ui_treeView.addAction(reloadComponentsAction)

		separatorAction = QAction(self.ui.Components_Manager_Ui_treeView)
		separatorAction.setSeparator(True)
		self.ui.Components_Manager_Ui_treeView.addAction(separatorAction)

	@core.executionTrace
	def __Components_Manager_Ui_treeView_activateComponentsAction__triggered(self, checked):
		"""
		This method is triggered by activateComponentsAction action.

		@param checked: Action checked state. ( Boolean )
		"""

		self.activateComponents__()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_deactivateComponentsAction__triggered(self, checked):
		"""
		This method is triggered by deactivateComponentsAction action.

		@param checked: Action checked state. ( Boolean )
		"""

		self.deactivateComponents__()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_reloadComponentsAction__triggered(self, checked):
		"""
		This method is triggered by reloadComponentsAction action.

		@param checked: Action checked state. ( Boolean )
		"""

		self.reloadComponents__()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method sets the Additional_Informations_textEdit Widget.

		@param selectedItems: Selected items. ( QItemSelection )
		@param deselectedItems: Deselected items. ( QItemSelection )
		"""

		LOGGER.debug("> Initializing '{0}' Widget.".format("Additional_Informations_textEdit"))

		selectedComponents = self.getSelectedComponents()
		content = []
		if selectedComponents:
			for item in selectedComponents:
				content.append(self.__componentsInformationsText.format(item.name,
																		strings.getNiceName(item.categorie),
																		item.author,
																		item.email,
																		item.url,
																		item.description))
		else:
			content.append(self.__componentsInformationsDefaultText)

		separator = len(content) == 1 and "" or "<p><center>* * *<center/></p>"
		self.ui.Components_Informations_textBrowser.setText(separator.join(content))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def __storeDeactivatedComponents(self):
		"""
		This method stores deactivated Components in settings file.

		@return: Method success. ( Boolean )
		"""

		deactivatedComponents = []
		for component in self.__model.findItems(".*", Qt.MatchRegExp | Qt.MatchRecursive, 0):
			if component._type == "Component":
				component._datas.interface.activated or deactivatedComponents.append(component._datas.name)

		LOGGER.debug("> Storing '{0}' deactivated Components.".format(", ".join(deactivatedComponents)))
		self.__settings.setKey("Settings", "deactivatedComponents", ",".join(deactivatedComponents))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def activateComponents__(self):
		"""
		This method activates user selected Components.

		@return: Method success. ( Boolean )
		"""

		for component in self.getSelectedComponents():
			if not component.interface.activated:
				self.activateComponent(component)
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component is already activated!".format(self.__class__.__name__, component.name))
		self.__storeDeactivatedComponents()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def deactivateComponents__(self):
		"""
		This method deactivates user selected Components.

		@return: Method success. ( Boolean )
		"""

		for component in self.getSelectedComponents():
			if component.interface.activated:
				if component.interface.deactivatable:
					self.deactivateComponent(component)
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, component.name))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component is already deactivated!".format(self.__class__.__name__, component.name))
		self.__storeDeactivatedComponents()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def reloadComponents__(self):
		"""
		This method reloads user selected Components.

		@return: Method success. ( Boolean )
		"""

		selectedComponents = self.getSelectedComponents()

		success = True
		for component in self.getSelectedComponents():
			success *= self.reloadComponent(component) or False

		if success:
			return True
		else:
			raise Exception, "{0} | Exception raised while reloading '{1}' Components!".format(self.__class__.__name__, ", ". join((component.name for component in selectedComponents)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(_componentActivationErrorHandler, False, foundations.exceptions.ComponentActivationError)
	def activateComponent(self, component):
		"""
		This method activates provided Component.

		@param component: Component. ( Profile )
		@return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Attempting '{0}' Component activation.".format(component.name))
		component.interface.activate(self.__container)
		if component.categorie == "default":
			component.interface.initialize()
		elif component.categorie == "ui":
			component.interface.addWidget()
			component.interface.initializeUi()
		LOGGER.info("{0} | '{1}' Component has been activated!".format(self.__class__.__name__, component.name))
		self.emit(SIGNAL("modelPartialRefresh()"))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(_componentDeactivationErrorHandler, False, foundations.exceptions.ComponentDeactivationError)
	def deactivateComponent(self, component):
		"""
		This method deactivates provided Component.

		@param component: Component. ( Profile )
		@return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Attempting '{0}' Component deactivation.".format(component.name))
		if component.interface.deactivatable:
			if component.categorie == "default":
				component.interface.uninitialize()
			elif component.categorie == "ui":
				component.interface.uninitializeUi()
				component.interface.removeWidget()
			component.interface.deactivate()
			LOGGER.info("{0} | '{1}' Component has been deactivated!".format(self.__class__.__name__, component.name))
			self.emit(SIGNAL("modelPartialRefresh()"))
			return True
		else:
			raise foundations.exceptions.ComponentDeactivationError, "{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, component.name)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(_componentReloadErrorHandler, False, Exception)
	def reloadComponent(self, component):
		"""
		This method reloads provided Component.

		@param component: Component. ( Profile )
		@return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Attempting '{0}' Component reload.".format(component.name))
		if component.interface.activated:
			self.deactivateComponent(component)
		self.__container.componentsManager.reloadComponent(component.name)
		if not component.interface.activated:
			self.activateComponent(component)
		LOGGER.info("{0} | '{1}' Component has been reloaded!".format(self.__class__.__name__, component.name))
		self.emit(SIGNAL("modelPartialRefresh()"))
		return True

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This method returns the Components_Manager_Ui_treeView selected items.

		@param rowsRootOnly: Return rows roots only. ( Boolean )
		@return: View selected items. ( List )
		"""

		selectedIndexes = self.ui.Components_Manager_Ui_treeView.selectedIndexes()
		return rowsRootOnly and [item for item in set((self.__model.itemFromIndex(self.__model.sibling(index.row(), 0, index)) for index in selectedIndexes))] or [self.__model.itemFromIndex(index) for index in selectedIndexes]

	@core.executionTrace
	def getSelectedComponents(self):
		"""
		This method returns selected Components.

		@return: View selected Components. ( List )
		"""

		selectedComponents = [item._datas for item in self.getSelectedItems() if item._type == "Component"]
		return selectedComponents and selectedComponents or []

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
