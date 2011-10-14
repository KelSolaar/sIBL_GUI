#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**gpsMap.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`GpsMap` Component Interface class and the :class:`Map` class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import umbra.ui.common
from manager.qwidgetComponent import QWidgetComponentFactory
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

__all__ = ["LOGGER", "COMPONENT_FILE", "Map", "GpsMap"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_FILE = os.path.join(os.path.dirname(__file__), "ui", "Gps_Map.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Map(QWebView):
	"""
	| This class is a `QWebView <http://doc.qt.nokia.com/4.7/qwebview.html>`_ subclass used for the GPS map.
	| It provides various methods to manipulate the `Microsoft Bing Maps <http://www.bing.com/maps/>`_ defined in the Component resources html file through Javascript evaluation.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		QWebView.__init__(self, parent)

	@core.executionTrace
	def addMarker(self, coordinates, title, icon, content):
		"""
		This method adds a marker to the map.

		:param coordinates: Marker coordinates. ( Tuple )
		:param title: Marker title. ( String )
		:param icon: Marker icon. ( String )
		:param content: Marker popup window content. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' marker to gps map with '{1}' coordinates.".format(title, coordinates))

		latitude, longitude = coordinates
		self.page().mainFrame().evaluateJavaScript("addMarker( new Microsoft.Maps.Location({0},{1}),\"{2}\",\"{3}\",\"{4}\")".format(latitude, longitude, title, icon, content))
		return True

	@core.executionTrace
	def removeMarkers(self):
		"""
		This method removes the map markers.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Removing GPS map markers.")

		self.page().mainFrame().evaluateJavaScript("removeMarkers()")
		return True

	@core.executionTrace
	def setCenter(self):
		"""
		This method centers the map.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Centering GPS map.")

		self.page().mainFrame().evaluateJavaScript("setCenter()")
		return True

	@core.executionTrace
	def setMapType(self, mapTypeId):
		"""
		This method sets the map type.
		
		Available map types:
			
			- MapTypeId.auto
			- MapTypeId.aerial
			- MapTypeId.road
			
		:param mapTypeId: GPS map type. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Setting GPS map type to '{0}'.".format(mapTypeId))

		self.page().mainFrame().evaluateJavaScript("setMapType(\"{0}\")".format(mapTypeId))
		return True

	@core.executionTrace
	def setZoom(self, type):
		"""
		This method sets the map zoom.

		:param type: Zoom type. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Zooming '{0}' GPS map.".format(type))

		self.page().mainFrame().evaluateJavaScript("setZoom(\"{0}\")".format(type))
		return True

class GpsMap(QWidgetComponentFactory(uiFile=COMPONENT_FILE)):
	"""
	| This class is the :mod:`umbra.components.addons.gpsMap.gpsMap` Component Interface class.
	| It displays the GPS map inside a `QDockWidget <http://doc.qt.nokia.com/4.7/qdockwidget.html>`_ window.
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

		super(GpsMap, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__uiResourcesDirectory = "resources"
		self.__uiZoomInImage = "Zoom_In.png"
		self.__uiZoomOutImage = "Zoom_Out.png"
		self.__gpsMapHtmlFile = "Bing_Maps.html"
		self.__gpsMapBaseSize = QSize(160, 100)
		self.__dockArea = 2

		self.__engine = None

		self.__coreDatabaseBrowser = None

		self.__map = None
		self.__mapTypeIds = (("Auto", "MapTypeId.auto"), ("Aerial", "MapTypeId.aerial"), ("Road", "MapTypeId.road"))

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiZoomInImage(self):
		"""
		This method is the property for **self.__uiZoomInImage** attribute.

		:return: self.__uiZoomInImage. ( String )
		"""

		return self.__uiZoomInImage

	@uiZoomInImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self, value):
		"""
		This method is the setter method for **self.__uiZoomInImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomInImage"))

	@uiZoomInImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self):
		"""
		This method is the deleter method for **self.__uiZoomInImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomInImage"))

	@property
	def uiZoomOutImage(self):
		"""
		This method is the property for **self.__uiZoomOutImage** attribute.

		:return: self.__uiZoomOutImage. ( String )
		"""

		return self.__uiZoomOutImage

	@uiZoomOutImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self, value):
		"""
		This method is the setter method for **self.__uiZoomOutImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomOutImage"))

	@uiZoomOutImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self):
		"""
		This method is the deleter method for **self.__uiZoomOutImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomOutImage"))

	@property
	def gpsMapHtmlFile(self):
		"""
		This method is the property for **self.__gpsMapHtmlFile** attribute.

		:return: self.__gpsMapHtmlFile. ( String )
		"""

		return self.__gpsMapHtmlFile

	@gpsMapHtmlFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def gpsMapHtmlFile(self, value):
		"""
		This method is the setter method for **self.__gpsMapHtmlFile** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "gpsMapHtmlFile"))

	@gpsMapHtmlFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def gpsMapHtmlFile(self):
		"""
		This method is the deleter method for **self.__gpsMapHtmlFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "gpsMapHtmlFile"))

	@property
	def gpsMapBaseSize(self):
		"""
		This method is the property for **self.__gpsMapBaseSize** attribute.

		:return: self.__gpsMapBaseSize. ( QSize() )
		"""

		return self.__gpsMapBaseSize

	@gpsMapBaseSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def gpsMapBaseSize(self, value):
		"""
		This method is the setter method for **self.__gpsMapBaseSize** attribute.

		:param value: Attribute value. ( QSize() )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "gpsMapBaseSize"))

	@gpsMapBaseSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def gpsMapBaseSize(self):
		"""
		This method is the deleter method for **self.__gpsMapBaseSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "gpsMapBaseSize"))

	@property
	def dockArea(self):
		"""
		This method is the property for **self.__dockArea** attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@property
	def map(self):
		"""
		This method is the property for **self.__map** attribute.

		:return: self.__map. ( QObject )
		"""

		return self.__map

	@map.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def map(self, value):
		"""
		This method is the setter method for **self.__map** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "map"))

	@map.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def map(self):
		"""
		This method is the deleter method for **self.__map** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "map"))

	@property
	def mapTypeIds(self):
		"""
		This method is the property for **self.__mapTypeIds** attribute.

		:return: self.__mapTypeIds. ( Tuple )
		"""

		return self.__mapTypeIds

	@mapTypeIds.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def mapTypeIds(self, value):
		"""
		This method is the setter method for **self.__mapTypeIds** attribute.

		:param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "mapTypeIds"))

	@mapTypeIds.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def mapTypeIds(self):
		"""
		This method is the deleter method for **self.__mapTypeIds** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "mapTypeIds"))

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

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResourcesDirectory)

		self.__engine = engine

		self.__coreDatabaseBrowser = self.__engine.componentsManager.components["core.databaseBrowser"].interface

		self.activated = True
		return True

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.basename(self.__uiResourcesDirectory)

		self.__engine = None

		self.__coreDatabaseBrowser = None

		self.activated = False
		return True

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiZoomInImage)))
		self.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiZoomOutImage)))

		self.Map_Type_comboBox.addItems([mapType[0] for mapType in self.__mapTypeIds])

		self.__map = Map()
		self.__map.setMinimumSize(self.__gpsMapBaseSize)
		self.__map.load(QUrl.fromLocalFile(os.path.normpath(os.path.join(self.__uiResourcesDirectory, self.__gpsMapHtmlFile))))
		self.__map.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
		self.__map.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
		self.Map_scrollAreaWidgetContents_gridLayout.addWidget(self.__map)

		# Signals / Slots.
		self.__coreDatabaseBrowser.Database_Browser_listView.selectionModel().selectionChanged.connect(self.__coreDatabaseBrowser_Database_Browser_listView_selectionModel__selectionChanged)
		self.__map.loadFinished.connect(self.__map__loadFinished)
		self.Map_Type_comboBox.activated.connect(self.__Map_Type_comboBox__activated)
		self.Zoom_In_pushButton.clicked.connect(self.__Zoom_In_pushButton__clicked)
		self.Zoom_Out_pushButton.clicked.connect(self.__Zoom_Out_pushButton__clicked)

		return True

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		# Signals / Slots.
		self.__coreDatabaseBrowser.Database_Browser_listView.selectionModel().selectionChanged.disconnect(self.__coreDatabaseBrowser_Database_Browser_listView_selectionModel__selectionChanged)
		self.__map.loadFinished.disconnect(self.__map__loadFinished)
		self.Map_Type_comboBox.activated.disconnect(self.__Map_Type_comboBox__activated)
		self.Zoom_In_pushButton.clicked.disconnect(self.__Zoom_In_pushButton__clicked)
		self.Zoom_Out_pushButton.clicked.disconnect(self.__Zoom_Out_pushButton__clicked)

		self.__map = None

		return True

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	@core.executionTrace
	def onClose(self):
		"""
		This method is called on Framework close.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		self.__map.stop()
		return True

	@core.executionTrace
	def __coreDatabaseBrowser_Database_Browser_listView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when **coreDatabaseBrowser.Database_Browser_listView** Model selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		self.setMarkers_ui()

	@core.executionTrace
	def __Map_Type_comboBox__activated(self, index):
		"""
		This method is triggered when **Map_Type_comboBox** index changes.

		:param index: ComboBox activated item index. ( Integer )
		"""

		self.__map.setMapType(self.__mapTypeIds[index][1])

	@core.executionTrace
	def __Zoom_In_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Zoom_In_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.__map.setZoom("In")

	@core.executionTrace
	def __Zoom_Out_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Zoom_Out_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.__map.setZoom("Out")

	@core.executionTrace
	def __map__loadFinished(self, state):
		"""
		This method is triggered when the GPS map finishes loading.

		:param state: Loading state. ( Boolean )
		"""

		self.setMarkers_ui()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def setMarkers_ui(self):
		"""
		This method sets selected Ibl Sets markers.

		:return: Method success. ( Boolean )
		
		:note: This method may require user interaction.
		"""

		selectedIblSets = self.__coreDatabaseBrowser.getSelectedIblSets()
		self.__map.removeMarkers()
		success = True
		for iblSet in selectedIblSets:
			success *= self.setMarker(iblSet) or False
		self.__map.setCenter()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while setting '{1}' GPS markers!".format(self.__class__.__name__, ", ". join((iblSet.title for iblSet in selectedIblSets))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setMarker(self, iblSet):
		"""
		This method sets provided Ibl Set marker.

		:param iblSet: Ibl Set to display marker. ( DbIblSet )
		:return: Method success. ( Boolean )
		"""

		if not iblSet.latitude and not iblSet.longitude:
			return True

		LOGGER.debug("> Ibl Set '{0}' provides GEO coordinates.".format(iblSet.name))
		shotDateString = "<b>Shot Date: </b>{0}".format(self.__coreDatabaseBrowser.getFormatedShotDate(iblSet.date, iblSet.time) or Constants.nullObject)
		content = "<p><h3><b>{0}</b></h3></p><p><b>Author: </b>{1}<br><b>Location: </b>{2}<br>{3}<br><b>Comment: </b>{4}</p>".format(iblSet.title, iblSet.author, iblSet.location, shotDateString, iblSet.comment)
		return self.__map.addMarker((iblSet.latitude, iblSet.longitude), iblSet.title, strings.toForwardSlashes(iblSet.icon), content)
