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
***	gpsMap.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		GPS Map Component Module.
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
from PyQt4.QtWebKit import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Map(QWebView):
	"""
	This Class Is The QWebView Class.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This Method Initializes The Class.
		
		@param parent: Widget Parent. ( QObject )
		"""

		QWebView.__init__(self, parent)

	@core.executionTrace
	def addMarker(self, coordinates, title, icon, content):
		"""
		This Method Adds A Marker To The Map.
		
		@param coordinates: Marker Coordinates. ( Tuple )
		@param title: Marker Title. ( String )
		@param icon: Marker Icon. ( String )
		@param content: Marker Popup Window Content. ( String )
		"""

		LOGGER.debug("> Adding '{0}' Marker To GPS Map With '{1}' Coordinates.".format(title, coordinates))

		self.page().mainFrame().evaluateJavaScript("addMarker( new Microsoft.Maps.Location({0},{1}),\"{2}\",\"{3}\",\"{4}\")".format(coordinates[0], coordinates[1], title, icon, content))

	@core.executionTrace
	def removeMarkers(self):
		"""
		This Method Removes The Map Markers.
		"""

		LOGGER.debug("> Removing GPS Map Markers.")

		self.page().mainFrame().evaluateJavaScript("removeMarkers()")

	@core.executionTrace
	def setCenter(self):
		"""
		This Method Center The Map.
		"""

		LOGGER.debug("> Centering GPS Map.")

		self.page().mainFrame().evaluateJavaScript("setCenter()")

	@core.executionTrace
	def setMapType(self, mapTypeId):
		"""
		This Method Sets The Map Type.
		
		@param mapTypeId: GPS Map Type. ( String )
		"""

		LOGGER.debug("> Setting GPS Map Type To '{0}'.".format(mapTypeId))

		self.page().mainFrame().evaluateJavaScript("setMapType(\"{0}\")".format(mapTypeId))

	@core.executionTrace
	def setZoom(self, type):
		"""
		This Method Sets The Map Zoom.
		
		@param type: Zoom Type. ( String )
		"""

		LOGGER.debug("> Zooming '{0}' GPS Map.".format(type))

		self.page().mainFrame().evaluateJavaScript("setZoom(\"{0}\")".format(type))

class GpsMap(UiComponent):
	"""
	This Class Is The GpsMap Class.
	"""

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
		self.deactivatable = True

		self.__uiPath = "ui/Gps_Map.ui"
		self.__uiResources = "resources"
		self.__uiZoomInImage = "Zoom_In.png"
		self.__uiZoomOutImage = "Zoom_Out.png"
		self.__gpsMapHtmlFile = "Bing_Maps.html"
		self.__gpsMapBaseSize = QSize(160, 100)
		self.__dockArea = 2

		self.__container = None

		self.__coreDatabaseBrowser = None

		self.__map = None
		self.__mapTypeIds = (("Auto", "MapTypeId.auto"), ("Aerial", "MapTypeId.aerial"), ("Road", "MapTypeId.road"))

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
	def uiZoomInImage(self):
		"""
		This Method Is The Property For The _uiZoomInImage Attribute.

		@return: self.__uiZoomInImage. ( String )
		"""

		return self.__uiZoomInImage

	@uiZoomInImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self, value):
		"""
		This Method Is The Setter Method For The _uiZoomInImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiZoomInImage"))

	@uiZoomInImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self):
		"""
		This Method Is The Deleter Method For The _uiZoomInImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiZoomInImage"))

	@property
	def uiZoomOutImage(self):
		"""
		This Method Is The Property For The _uiZoomOutImage Attribute.

		@return: self.__uiZoomOutImage. ( String )
		"""

		return self.__uiZoomOutImage

	@uiZoomOutImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self, value):
		"""
		This Method Is The Setter Method For The _uiZoomOutImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiZoomOutImage"))

	@uiZoomOutImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self):
		"""
		This Method Is The Deleter Method For The _uiZoomOutImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiZoomOutImage"))

	@property
	def gpsMapHtmlFile(self):
		"""
		This Method Is The Property For The _gpsMapHtmlFile Attribute.

		@return: self.__gpsMapHtmlFile. ( String )
		"""

		return self.__gpsMapHtmlFile

	@gpsMapHtmlFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def gpsMapHtmlFile(self, value):
		"""
		This Method Is The Setter Method For The _gpsMapHtmlFile Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("gpsMapHtmlFile"))

	@gpsMapHtmlFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def gpsMapHtmlFile(self):
		"""
		This Method Is The Deleter Method For The _gpsMapHtmlFile Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("gpsMapHtmlFile"))

	@property
	def gpsMapBaseSize(self):
		"""
		This Method Is The Property For The _gpsMapBaseSize Attribute.

		@return: self.__gpsMapBaseSize. ( QSize() )
		"""

		return self.__gpsMapBaseSize

	@gpsMapBaseSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def gpsMapBaseSize(self, value):
		"""
		This Method Is The Setter Method For The _gpsMapBaseSize Attribute.

		@param value: Attribute Value. ( QSize() )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("gpsMapBaseSize"))

	@gpsMapBaseSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def gpsMapBaseSize(self):
		"""
		This Method Is The Deleter Method For The _gpsMapBaseSize Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("gpsMapBaseSize"))

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
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDatabaseBrowser"))

	@property
	def map(self):
		"""
		This Method Is The Property For The _map Attribute.

		@return: self.__map. ( QObject )
		"""

		return self.__map

	@map.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def map(self, value):
		"""
		This Method Is The Setter Method For The _map Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("map"))

	@map.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def map(self):
		"""
		This Method Is The Deleter Method For The _map Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("map"))

	@property
	def mapTypeIds(self):
		"""
		This Method Is The Property For The _mapTypeIds Attribute.

		@return: self.__mapTypeIds. ( Tuple )
		"""

		return self.__mapTypeIds

	@mapTypeIds.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def mapTypeIds(self, value):
		"""
		This Method Is The Setter Method For The _mapTypeIds Attribute.

		@param value: Attribute Value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("mapTypeIds"))

	@mapTypeIds.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def mapTypeIds(self):
		"""
		This Method Is The Deleter Method For The _mapTypeIds Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("mapTypeIds"))

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

		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__uiResources = os.path.basename(self.__uiResources)

		self.__container = None

		self.__coreDatabaseBrowser = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.ui.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiZoomInImage)))
		self.ui.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiZoomOutImage)))

		self.ui.Map_Type_comboBox.addItems([mapType[0] for mapType in self.__mapTypeIds])

		self.__map = Map()
		self.__map.setMinimumSize(self.__gpsMapBaseSize)
		self.__map.load(QUrl.fromLocalFile(os.path.normpath(os.path.join(self.__uiResources, self.__gpsMapHtmlFile))))
		self.__map.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
		self.__map.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
		self.ui.Map_scrollAreaWidgetContents_gridLayout.addWidget(self.__map)

		# Signals / Slots.
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.selectionModel().selectionChanged.connect(self.__coreDatabaseBrowser_Database_Browser_listView_selectionModel__selectionChanged)
		self.__map.loadFinished.connect(self.__map__loadFinished)
		self.ui.Map_Type_comboBox.activated.connect(self.__Map_Type_comboBox__activated)
		self.ui.Zoom_In_pushButton.clicked.connect(self.__Zoom_In_pushButton__clicked)
		self.ui.Zoom_Out_pushButton.clicked.connect(self.__Zoom_Out_pushButton__clicked)

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		# Signals / Slots.
		self.__coreDatabaseBrowser.ui.Database_Browser_listView.selectionModel().selectionChanged.disconnect(self.__coreDatabaseBrowser_Database_Browser_listView_selectionModel__selectionChanged)
		self.__map.loadFinished.disconnect(self.__map__loadFinished)
		self.ui.Map_Type_comboBox.activated.disconnect(self.__Map_Type_comboBox__activated)
		self.ui.Zoom_In_pushButton.clicked.disconnect(self.__Zoom_In_pushButton__clicked)
		self.ui.Zoom_Out_pushButton.clicked.disconnect(self.__Zoom_Out_pushButton__clicked)

		self.__map = None

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self.ui)
		self.ui.setParent(None)

	@core.executionTrace
	def __coreDatabaseBrowser_Database_Browser_listView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Sets Is Triggered When coreDatabaseBrowser_Database_Browser_listView Selection Has Changed.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""

		self.setMarkers__()

	@core.executionTrace
	def __Map_Type_comboBox__activated(self, index):
		"""
		This Method Is Triggered When Map_Type_comboBox Index Changes.
		
		@param index: ComboBox Activated Item Index. ( Integer )
		"""

		self.__map.setMapType(self.__mapTypeIds[index][1])

	@core.executionTrace
	def __Zoom_In_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Zoom_In_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.__map.setZoom("In")

	@core.executionTrace
	def __Zoom_Out_pushButton__clicked(self, checked):
		"""
		This Method Is Triggered When Zoom_Out_pushButton Is Clicked.
		
		@param checked: Checked State. ( Boolean )
		"""

		self.__map.setZoom("Out")

	@core.executionTrace
	def __map__loadFinished(self, state):
		"""
		This Method Is Triggered When The GPS Map Finishes Loading.
		
		@param state: Loading State. ( Boolean )
		"""

		self.setMarkers__()

	@core.executionTrace
	def setMarkers__(self):
		"""
		This Method Sets Selected Ibl Sets Markers.
		"""

		selectedIblSets = [iblSet._datas for iblSet in self.__coreDatabaseBrowser.getSelectedIblSets()]
		selectedIblSets and	self.setMarkers(selectedIblSets)

	@core.executionTrace
	def setMarkers(self, iblSets):
		"""
		This Method Sets Ibl Sets Markers.

		@param iblSets: Ibl Sets To Display Markers. ( DbIblSet List )
		"""

		self.__map.removeMarkers()
		for iblSet in iblSets:
			LOGGER.debug("> Current Ibl Set: '{0}'.".format(iblSet.name))
			if iblSet.latitude and iblSet.longitude:
				LOGGER.debug("> Ibl Set '{0}' Provides GEO Coordinates.".format(iblSet.name))
				shotDateString = "<b>Shot Date: </b>{0}".format(self.__coreDatabaseBrowser.getFormatedShotDate(iblSet.date, iblSet.time) or Constants.nullObject)
				content = "<p><h3><b>{0}</b></h3></p><p><b>Author: </b>{1}<br><b>Location: </b>{2}<br>{3}<br><b>Comment: </b>{4}</p>".format(iblSet.title, iblSet.author, iblSet.location, shotDateString, iblSet.comment)
				self.__map.addMarker((iblSet.latitude, iblSet.longitude), iblSet.title, strings.toForwardSlashes(iblSet.icon), content)
		self.__map.setCenter()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
