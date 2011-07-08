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
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
************************************************************************************************
***	componentsManagerUi.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Components Manager Ui Component Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import traceback

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
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
@core.executionTrace
def _componentActivationErrorHandler(exception, origin, *args, **kwargs):
	"""
	This Definition Provides An Exception Handler For Component Activation.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	"""

	ui.common.uiBasicExceptionHandler(Exception("{0} | An Exception Occurred While Activating '{1}' Component:\n{2}".format(core.getModule(_componentActivationErrorHandler).__name__, args[1].name, traceback.format_exc())), origin, *args, **kwargs)

@core.executionTrace
def _componentDeactivationErrorHandler(exception, origin, *args, **kwargs):
	"""
	This Definition Provides An Exception Handler For Component Deactivation.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	"""

	ui.common.uiBasicExceptionHandler(Exception("{0} | An Exception Occurred While Deactivating '{1}' Component:\n{2}".format(core.getModule(_componentDeactivationErrorHandler).__name__, args[1].name, traceback.format_exc())), origin, *args, **kwargs)

@core.executionTrace
def _componentReloadErrorHandler(exception, origin, *args, **kwargs):
	"""
	This Definition Provides An Exception Handler For Component Reload.
	
	@param exception: Exception. ( Exception )
	@param origin: Function / Method Raising The Exception. ( String )
	"""

	ui.common.uiBasicExceptionHandler(Exception("{0} | An Exception Occurred While Reloading '{1}' Component:\n{2}".format(core.getModule(_componentReloadErrorHandler).__name__, args[1].name, traceback.format_exc())), origin, *args, **kwargs)

class ComponentsManagerUi(UiComponent):
	"""
	This Class Is The ComponentsManagerUi Class.
	"""

	# Custom Signals Definitions.
	modelChanged = pyqtSignal()
	modelRefresh = pyqtSignal()
	modelPartialRefresh = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
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
		self.__componentsInformationsDefaultText = "<center><h4>* * *</h4>Select Some Components To Display Related Informations!<h4>* * *</h4></center>"
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

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This Method Is The Property For The _uiResources Attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This Method Is The Deleter Method For The _uiResources Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def uiActivatedImage(self):
		"""
		This Method Is The Property For The _uiActivatedImage Attribute.

		@return: self.__uiActivatedImage. ( String )
		"""

		return self.__uiActivatedImage

	@uiActivatedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiActivatedImage(self, value):
		"""
		This Method Is The Setter Method For The _uiActivatedImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiActivatedImage"))

	@uiActivatedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiActivatedImage(self):
		"""
		This Method Is The Deleter Method For The _uiActivatedImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiActivatedImage"))

	@property
	def uiDeactivatedImage(self):
		"""
		This Method Is The Property For The _uiDeactivatedImage Attribute.

		@return: self.__uiDeactivatedImage. ( String )
		"""

		return self.__uiDeactivatedImage

	@uiDeactivatedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDeactivatedImage(self, value):
		"""
		This Method Is The Setter Method For The _uiDeactivatedImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiDeactivatedImage"))

	@uiDeactivatedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDeactivatedImage(self):
		"""
		This Method Is The Deleter Method For The _uiDeactivatedImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiDeactivatedImage"))

	@property
	def uiCategorieAffixe(self):
		"""
		This Method Is The Property For The _uiCategorieAffixe Attribute.

		@return: self.__uiCategorieAffixe. ( String )
		"""

		return self.__uiCategorieAffixe

	@uiCategorieAffixe.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiCategorieAffixe(self, value):
		"""
		This Method Is The Setter Method For The _uiCategorieAffixe Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiCategorieAffixe"))

	@uiCategorieAffixe.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiCategorieAffixe(self):
		"""
		This Method Is The Deleter Method For The _uiCategorieAffixe Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiCategorieAffixe"))

	@property
	def dockArea(self):
		"""
		This Method Is The Property For The _dockArea Attribute.

		@return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This Method Is The Deleter Method For The _dockArea Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dockArea"))

	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def settings(self):
		"""
		This Method Is The Property For The _settings Attribute.

		@return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This Method Is The Deleter Method For The _settings Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settings"))

	@property
	def model(self):
		"""
		This Method Is The Property For The _model Attribute.

		@return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This Method Is The Setter Method For The _model Attribute.

		@param value: Attribute Value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This Method Is The Deleter Method For The _model Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("model"))

	@property
	def modelHeaders(self):
		"""
		This Method Is The Property For The _modelHeaders Attribute.

		@return: self.__modelHeaders. ( List )
		"""

		return self.__modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self, value):
		"""
		This Method Is The Setter Method For The _modelHeaders Attribute.

		@param value: Attribute Value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("modelHeaders"))

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self):
		"""
		This Method Is The Deleter Method For The _modelHeaders Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("modelHeaders"))

	@property
	def treeWidgetIndentation(self):
		"""
		This Method Is The Property For The _treeWidgetIndentation Attribute.

		@return: self.__treeWidgetIndentation. ( Integer )
		"""

		return self.__treeWidgetIndentation

	@treeWidgetIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeWidgetIndentation(self, value):
		"""
		This Method Is The Setter Method For The _treeWidgetIndentation Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("treeWidgetIndentation"))

	@treeWidgetIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeWidgetIndentation(self):
		"""
		This Method Is The Deleter Method For The _treeWidgetIndentation Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("treeWidgetIndentation"))

	@property
	def treeViewInnerMargins(self):
		"""
		This Method Is The Property For The _treeViewInnerMargins Attribute.

		@return: self.__treeViewInnerMargins. ( Integer )
		"""

		return self.__treeViewInnerMargins

	@treeViewInnerMargins.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self, value):
		"""
		This Method Is The Setter Method For The _treeViewInnerMargins Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("treeViewInnerMargins"))

	@treeViewInnerMargins.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self):
		"""
		This Method Is The Deleter Method For The _treeViewInnerMargins Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("treeViewInnerMargins"))

	@property
	def componentsInformationsDefaultText(self):
		"""
		This Method Is The Property For The _componentsInformationsDefaultText Attribute.

		@return: self.__componentsInformationsDefaultText. ( String )
		"""

		return self.__componentsInformationsDefaultText

	@componentsInformationsDefaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsDefaultText(self, value):
		"""
		This Method Is The Setter Method For The _componentsInformationsDefaultText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("componentsInformationsDefaultText"))

	@componentsInformationsDefaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsDefaultText(self):
		"""
		This Method Is The Deleter Method For The _componentsInformationsDefaultText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("componentsInformationsDefaultText"))

	@property
	def componentsInformationsText(self):
		"""
		This Method Is The Property For The _componentsInformationsText Attribute.

		@return: self.__componentsInformationsText. ( String )
		"""

		return self.__componentsInformationsText

	@componentsInformationsText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsText(self, value):
		"""
		This Method Is The Setter Method For The _componentsInformationsText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("componentsInformationsText"))

	@componentsInformationsText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsText(self):
		"""
		This Method Is The Deleter Method For The _componentsInformationsText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("componentsInformationsText"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
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
		This Method Deactivates The Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Cannot Be Deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

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
		This Method Uninitializes The Component Ui.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Ui Cannot Be Uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget Cannot Be Removed!".format(self.name))

	@core.executionTrace
	def onStartup(self):
		"""
		This Method Is Called On Framework Startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework Startup Method.".format(self.__class__.__name__))

		self.__Components_Manager_Ui_treeView_setActivationsStatus()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setModel(self):
		"""
		This Method Sets The Components_Manager_Ui_treeView Model.
		
		Columns:
		Collections | Activated | Categorie | Rank | Version
		
		Rows:
		* Path: { _type: "Path" }
		** Component: { _type: "Component", _datas: profile }
		"""

		LOGGER.debug("> Setting Up '{0}' Model!".format("Components_Manager_Ui_treeView"))

		self.__model.clear()

		self.__model.setHorizontalHeaderLabels(self.__modelHeaders)
		self.__model.setColumnCount(len(self.__modelHeaders))

		for path in self.__container.componentsManager.paths:
			components = [component for component in self.__container.componentsManager.components if os.path.normpath(self.__container.componentsManager.paths[path]) in os.path.normpath(self.__container.componentsManager.components[component].path)]

			if components:
				pathStandardItem = QStandardItem(QString(path))
				pathStandardItem._type = "Path"

				LOGGER.debug("> Adding '{0}' Path To '{1}' Model.".format(path, "Components_Manager_Ui_treeView"))
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

					LOGGER.debug("> Adding '{0}' Component To '{1}'.".format(component, "Components_Manager_Ui_treeView"))
					pathStandardItem.appendRow([componentStandardItem, componentActivationStandardItem, componentCategorieStandardItem, componentRankStandardItem, componentVersionStandardItem])

		self.emit(SIGNAL("modelChanged()"))

	@core.executionTrace
	def __Components_Manager_Ui_treeView_refreshModel(self):
		"""
		This Method Refreshes The Components_Manager_Ui_treeView Model.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Components_Manager_Ui_treeView"))

		self.__Components_Manager_Ui_treeView_setModel()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setView(self):
		"""
		This Method Sets The Components_Manager_Ui_treeView View.
		"""

		LOGGER.debug("> Refreshing '{0}' Ui!".format(self.__class__.__name__))

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
		This Method Sets Components_Manager_Ui_treeView Default View State.
		"""

		LOGGER.debug("> Setting '{0}' Default View State!".format("Components_Manager_Ui_treeView"))

		self.ui.Components_Manager_Ui_treeView.expandAll()
		for column in range(len(self.__modelHeaders)):
			self.ui.Components_Manager_Ui_treeView.resizeColumnToContents(column)

		self.ui.Components_Manager_Ui_treeView.sortByColumn(0, Qt.AscendingOrder)

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setActivationsStatus(self):
		"""
		This Method Sets The Components_Manager_Ui_treeView Activations Status.
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
		This Method Refreshes The Components_Manager_Ui_treeView View.
		"""

		self.__Components_Manager_Ui_treeView_setDefaultViewState()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_addActions(self):
		"""
		This Method Sets The Components_Manager_Ui_treeView Actions.
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
		This Method Is Triggered By activateComponentsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.activateComponents__()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_deactivateComponentsAction__triggered(self, checked):
		"""
		This Method Is Triggered By deactivateComponentsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.deactivateComponents__()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_reloadComponentsAction__triggered(self, checked):
		"""
		This Method Is Triggered By reloadComponentsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.reloadComponents__()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Sets The Additional_Informations_textEdit Widget.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
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
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, Exception)
	def __storeDeactivatedComponents(self):
		"""
		This Method Stores Deactivated Components In Settings File.

		@return: Method Success. ( Boolean )		
		"""

		deactivatedComponents = []
		for component in self.__model.findItems(".*", Qt.MatchRegExp | Qt.MatchRecursive, 0):
			if component._type == "Component":
				component._datas.interface.activated or deactivatedComponents.append(component._datas.name)

		LOGGER.debug("> Storing '{0}' Deactivated Components.".format(", ".join(deactivatedComponents)))
		self.__settings.setKey("Settings", "deactivatedComponents", ",".join(deactivatedComponents))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, Exception)
	def activateComponents__(self):
		"""
		This Method Activates User Selected Components.

		@return: Method Success. ( Boolean )		
		"""

		for component in self.getSelectedComponents():
			if not component.interface.activated:
				self.activateComponent(component)
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component Is Already Activated!".format(self.__class__.__name__, component.name))
		self.__storeDeactivatedComponents()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, Exception)
	def deactivateComponents__(self):
		"""
		This Method Deactivates User Selected Components.

		@return: Method Success. ( Boolean )		
		"""

		for component in self.getSelectedComponents():
			if component.interface.activated:
				if component.interface.deactivatable:
					self.deactivateComponent(component)
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component Cannot Be Deactivated!".format(self.__class__.__name__, component.name))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component Is Already Deactivated!".format(self.__class__.__name__, component.name))
		self.__storeDeactivatedComponents()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, Exception)
	def reloadComponents__(self):
		"""
		This Method Reloads User Selected Components.

		@return: Method Success. ( Boolean )		
		"""

		selectedComponents = self.getSelectedComponents()

		success = True
		for component in self.getSelectedComponents():
			success *= self.reloadComponent(component) or False

		if success: return True
		else: raise Exception, "{0} | Exception Raised While Reloading '{1}' Components!".format(self.__class__.__name__, ", ". join((component.name for component in selectedComponents)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(_componentActivationErrorHandler, False, foundations.exceptions.ComponentActivationError)
	def activateComponent(self, component):
		"""
		This Method Activates Provided Component.
		
		@param component: Component. ( Profile )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Attempting '{0}' Component Activation.".format(component.name))
		component.interface.activate(self.__container)
		if component.categorie == "default":
			component.interface.initialize()
		elif component.categorie == "ui":
			component.interface.addWidget()
			component.interface.initializeUi()
		LOGGER.info("{0} | '{1}' Component Has Been Activated!".format(self.__class__.__name__, component.name))
		self.emit(SIGNAL("modelPartialRefresh()"))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(_componentDeactivationErrorHandler, False, foundations.exceptions.ComponentDeactivationError)
	def deactivateComponent(self, component):
		"""
		This Method Deactivates Provided Component.
		
		@param component: Component. ( Profile )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Attempting '{0}' Component Deactivation.".format(component.name))
		if component.interface.deactivatable:
			if component.categorie == "default":
				component.interface.uninitialize()
			elif component.categorie == "ui":
				component.interface.uninitializeUi()
				component.interface.removeWidget()
			component.interface.deactivate()
			LOGGER.info("{0} | '{1}' Component Has Been Deactivated!".format(self.__class__.__name__, component.name))
			self.emit(SIGNAL("modelPartialRefresh()"))
			return True
		else:
			raise foundations.exceptions.ComponentDeactivationError, "{0} | '{1}' Component Cannot Be Deactivated!".format(self.__class__.__name__, component.name)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(_componentReloadErrorHandler, False, Exception)
	def reloadComponent(self, component):
		"""
		This Method Reloads Provided Component.

		@param component: Component. ( Profile )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Attempting '{0}' Component Reload.".format(component.name))
		if component.interface.activated:
			self.deactivateComponent(component)
		self.__container.componentsManager.reloadComponent(component.name)
		if not component.interface.activated:
			self.activateComponent(component)
		LOGGER.info("{0} | '{1}' Component Has Been Reloaded!".format(self.__class__.__name__, component.name))
		self.emit(SIGNAL("modelPartialRefresh()"))
		return True

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This Method Returns The Components_Manager_Ui_treeView Selected Items.
		
		@param rowsRootOnly: Return Rows Roots Only. ( Boolean )
		@return: View Selected Items. ( List )
		"""

		selectedIndexes = self.ui.Components_Manager_Ui_treeView.selectedIndexes()
		return rowsRootOnly and [item for item in set((self.__model.itemFromIndex(self.__model.sibling(index.row(), 0, index)) for index in selectedIndexes))] or [self.__model.itemFromIndex(index) for index in selectedIndexes]

	@core.executionTrace
	def getSelectedComponents(self):
		"""
		This Method Returns Selected Components.
		
		@return: View Selected Components. ( List )
		"""

		selectedComponents = [item._datas for item in self.getSelectedItems() if item._type == "Component"]
		return selectedComponents and selectedComponents or []

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
