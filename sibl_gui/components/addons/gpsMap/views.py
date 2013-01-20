#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines
	the :class:`sibl_gui.components.core.collectionsOutliner.collectionsOutliner.CollectionsOutliner` Component
	Interface class Views.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtWebKit import QWebView

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Map_QWebView"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Map_QWebView(QWebView):
	"""
	| This class is a `QWebView <http://doc.qt.nokia.com/qwebview.html>`_ subclass used for the GPS map.
	| It provides various methods to manipulate the `Microsoft Bing Maps <http://www.bing.com/maps/>`_ defined
		in the Component resources html file through Javascript evaluation.
	"""

	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		QWebView.__init__(self, parent)

	def __evaluateJavascript(self, javascript):
		"""
		This method evaluates given javascript content in the View.

		:param javascript: Javascript. ( String )
		"""

		self.page().mainFrame().evaluateJavaScript(javascript)

	def addMarker(self, coordinates, title, icon, content):
		"""
		This method adds a marker to the GPS map.

		:param coordinates: Marker coordinates. ( Tuple )
		:param title: Marker title. ( String )
		:param icon: Marker icon. ( String )
		:param content: Marker popup window content. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' marker to gps map with '{1}' coordinates.".format(title, coordinates))

		latitude, longitude = coordinates
		self.__evaluateJavascript(
		"addMarker( new Microsoft.Maps.Location({0},{1}),\"{2}\",\"{3}\",\"{4}\")".format(latitude,
																						longitude,
																						title,
																						icon,
																						content))
		return True

	def removeMarkers(self):
		"""
		This method removes the GPS map markers.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Removing GPS map markers.")

		self.__evaluateJavascript("removeMarkers()")
		return True

	def setCenter(self):
		"""
		This method centers the GPS map.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Centering GPS map.")

		self.__evaluateJavascript("setCenter()")
		return True

	def setMapType(self, mapTypeId):
		"""
		This method sets the GPS map type.
		
		Available map types:
			
			- MapTypeId.auto
			- MapTypeId.aerial
			- MapTypeId.road
			
		:param mapTypeId: GPS map type. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Setting GPS map type to '{0}'.".format(mapTypeId))

		self.__evaluateJavascript("setMapType(\"{0}\")".format(mapTypeId))
		return True

	def setZoom(self, type):
		"""
		This method sets the GPS map zoom.

		:param type: Zoom type. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Zooming '{0}' GPS map.".format(type))

		self.__evaluateJavascript("setZoom(\"{0}\")".format(type))
		return True
