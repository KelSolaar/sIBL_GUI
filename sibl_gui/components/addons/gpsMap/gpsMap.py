#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**gpsMap.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`GpsMap` Component Interface class and the :class:`Map` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import sibl_gui.ui.common
import umbra.exceptions
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.addons.gpsMap.views import Map_QWebView
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_FILE", "GpsMap"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_FILE = os.path.join(os.path.dirname(__file__), "ui", "Gps_Map.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class GpsMap(QWidgetComponentFactory(uiFile=COMPONENT_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.addons.gpsMap.gpsMap` Component Interface class.
	| It displays the GPS map inside a `QDockWidget <http://doc.qt.nokia.com/qdockwidget.html>`_ window.
	"""

	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param name: Component name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
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

		self.__iblSetsOutliner = None

		self.__map = None
		self.__mapTypeIds = (("Auto", "MapTypeId.auto"), ("Aerial", "MapTypeId.aerial"), ("Road", "MapTypeId.road"))

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def uiResourcesDirectory(self):
		"""
		Property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory.
		:rtype: unicode
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		Setter for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		Deleter for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiZoomInImage(self):
		"""
		Property for **self.__uiZoomInImage** attribute.

		:return: self.__uiZoomInImage.
		:rtype: unicode
		"""

		return self.__uiZoomInImage

	@uiZoomInImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self, value):
		"""
		Setter for **self.__uiZoomInImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomInImage"))

	@uiZoomInImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self):
		"""
		Deleter for **self.__uiZoomInImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomInImage"))

	@property
	def uiZoomOutImage(self):
		"""
		Property for **self.__uiZoomOutImage** attribute.

		:return: self.__uiZoomOutImage.
		:rtype: unicode
		"""

		return self.__uiZoomOutImage

	@uiZoomOutImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self, value):
		"""
		Setter for **self.__uiZoomOutImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomOutImage"))

	@uiZoomOutImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self):
		"""
		Deleter for **self.__uiZoomOutImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomOutImage"))

	@property
	def gpsMapHtmlFile(self):
		"""
		Property for **self.__gpsMapHtmlFile** attribute.

		:return: self.__gpsMapHtmlFile.
		:rtype: unicode
		"""

		return self.__gpsMapHtmlFile

	@gpsMapHtmlFile.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def gpsMapHtmlFile(self, value):
		"""
		Setter for **self.__gpsMapHtmlFile** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "gpsMapHtmlFile"))

	@gpsMapHtmlFile.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def gpsMapHtmlFile(self):
		"""
		Deleter for **self.__gpsMapHtmlFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "gpsMapHtmlFile"))

	@property
	def gpsMapBaseSize(self):
		"""
		Property for **self.__gpsMapBaseSize** attribute.

		:return: self.__gpsMapBaseSize. ( QSize() )
		"""

		return self.__gpsMapBaseSize

	@gpsMapBaseSize.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def gpsMapBaseSize(self, value):
		"""
		Setter for **self.__gpsMapBaseSize** attribute.

		:param value: Attribute value. ( QSize() )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "gpsMapBaseSize"))

	@gpsMapBaseSize.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def gpsMapBaseSize(self):
		"""
		Deleter for **self.__gpsMapBaseSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "gpsMapBaseSize"))

	@property
	def dockArea(self):
		"""
		Property for **self.__dockArea** attribute.

		:return: self.__dockArea.
		:rtype: int
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		Setter for **self.__dockArea** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		Deleter for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def iblSetsOutliner(self):
		"""
		Property for **self.__iblSetsOutliner** attribute.

		:return: self.__iblSetsOutliner.
		:rtype: QWidget
		"""

		return self.__iblSetsOutliner

	@iblSetsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self, value):
		"""
		Setter for **self.__iblSetsOutliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsOutliner"))

	@iblSetsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self):
		"""
		Deleter for **self.__iblSetsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsOutliner"))

	@property
	def map(self):
		"""
		Property for **self.__map** attribute.

		:return: self.__map.
		:rtype: QObject
		"""

		return self.__map

	@map.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def map(self, value):
		"""
		Setter for **self.__map** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "map"))

	@map.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def map(self):
		"""
		Deleter for **self.__map** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "map"))

	@property
	def mapTypeIds(self):
		"""
		Property for **self.__mapTypeIds** attribute.

		:return: self.__mapTypeIds.
		:rtype: tuple
		"""

		return self.__mapTypeIds

	@mapTypeIds.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def mapTypeIds(self, value):
		"""
		Setter for **self.__mapTypeIds** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "mapTypeIds"))

	@mapTypeIds.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def mapTypeIds(self):
		"""
		Deleter for **self.__mapTypeIds** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "mapTypeIds"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Engine to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(__file__), self.__uiResourcesDirectory)

		self.__engine = engine

		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]

		self.activated = True
		return True

	def deactivate(self):
		"""
		Deactivates the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.basename(self.__uiResourcesDirectory)

		self.__engine = None

		self.__iblSetsOutliner = None

		self.activated = False
		return True

	def initializeUi(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiZoomInImage)))
		self.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiZoomOutImage)))

		self.Map_Type_comboBox.addItems([foundations.common.getFirstItem(mapType) for mapType in self.__mapTypeIds])

		self.__map = Map_QWebView()
		self.__map.setMinimumSize(self.__gpsMapBaseSize)
		self.__map.load(QUrl.fromLocalFile(os.path.normpath(os.path.join(self.__uiResourcesDirectory,
																		self.__gpsMapHtmlFile))))
		self.__map.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
		self.__map.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
		self.Map_scrollAreaWidgetContents_gridLayout.addWidget(self.__map)

		# Signals / Slots.
		for view in self.__iblSetsOutliner.views:
			view.selectionModel().selectionChanged.connect(
			self.__iblSetsOutliner_view_selectionModel__selectionChanged)
		self.__map.loadFinished.connect(self.__map__loadFinished)
		self.Map_Type_comboBox.activated.connect(self.__Map_Type_comboBox__activated)
		self.Zoom_In_pushButton.clicked.connect(self.__Zoom_In_pushButton__clicked)
		self.Zoom_Out_pushButton.clicked.connect(self.__Zoom_Out_pushButton__clicked)

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		Uninitializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		# Signals / Slots.
		for view in self.__iblSetsOutliner.views:
			view.selectionModel().selectionChanged.disconnect(
			self.__iblSetsOutliner_view_selectionModel__selectionChanged)
		self.__map.loadFinished.disconnect(self.__map__loadFinished)
		self.Map_Type_comboBox.activated.disconnect(self.__Map_Type_comboBox__activated)
		self.Zoom_In_pushButton.clicked.disconnect(self.__Zoom_In_pushButton__clicked)
		self.Zoom_Out_pushButton.clicked.disconnect(self.__Zoom_Out_pushButton__clicked)

		self.__map.setParent(None)
		self.__map = None

		self.initializedUi = True
		return True

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	def onClose(self):
		"""
		Defines the slot triggered on Framework close.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		self.__map.stop()
		return True

	def __iblSetsOutliner_view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		Defines the slot triggered by **Data** Model when selection changed

		:param selectedItems: Selected items.
		:type selectedItems: QItemSelection
		:param deselectedItems: Deselected items.
		:type deselectedItems: QItemSelection
		"""

		self.setMarkersUi()

	def __Map_Type_comboBox__activated(self, index):
		"""
		Defines the slot triggered by **Map_Type_comboBox** when activated.

		:param index: ComboBox activated item index.
		:type index: int
		"""

		self.__map.setMapType(self.__mapTypeIds[index][1])

	def __Zoom_In_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Zoom_In_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.__map.setZoom("In")

	def __Zoom_Out_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Zoom_Out_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.__map.setZoom("Out")

	def __map__loadFinished(self, state):
		"""
		Defines the slot triggered by the GPS map when load finished.

		:param state: Loading state.
		:type state: bool
		"""

		self.setMarkersUi()

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def setMarkersUi(self):
		"""
		Sets selected Ibl Sets markers.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		selectedIblSets = self.__iblSetsOutliner.getSelectedIblSets()
		self.__map.removeMarkers()
		success = True
		for iblSet in selectedIblSets:
			success *= self.setMarker(iblSet) or False
		self.__map.setCenter()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while setting '{1}' GPS markers!".format(
			self.__class__.__name__, ", ". join((iblSet.title for iblSet in selectedIblSets))))

	def setMarker(self, iblSet):
		"""
		Sets given Ibl Set marker.

		:param iblSet: Ibl Set to display marker.
		:type iblSet: IblSet
		:return: Method success.
		:rtype: bool
		"""

		if not iblSet.latitude and not iblSet.longitude:
			return True

		LOGGER.debug("> Ibl Set '{0}' provides GEO coordinates.".format(iblSet.name))
		shotDateString = "<b>Shot Date: </b>{0}".format(
		sibl_gui.ui.common.getFormattedShotDate(iblSet.date, iblSet.time) or Constants.nullObject)
		content = "<p><h3><b>{0}</b></h3></p><p><b>\
		Author: </b>{1}<br><b>\
		Location: </b>{2}<br>{3}<br><b>\
		Comment: </b>{4}</p>".format(iblSet.title, iblSet.author, iblSet.location, shotDateString, iblSet.comment)
		return self.__map.addMarker((iblSet.latitude, iblSet.longitude),
		 							iblSet.title,
		 							foundations.strings.toForwardSlashes(iblSet.icon), content)

	def removeMarkers(self):
		"""
		Removes the GPS map markers.

		:return: Method success.
		:rtype: bool
		"""

		self.__map.removeMarkers()
		return True
