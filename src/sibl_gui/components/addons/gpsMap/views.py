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
import logging
from PyQt4.QtWebKit import QWebView

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Map_QWebView"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Map_QWebView(QWebView):
	"""
	| This class is a `QWebView <http://doc.qt.nokia.com/4.7/qwebview.html>`_ subclass used for the GPS map.
	| It provides various methods to manipulate the `Microsoft Bing Maps <http://www.bing.com/maps/>`_ defined
	in the Component resources html file through Javascript evaluation.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		QWebView.__init__(self, parent)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
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
		self.page().mainFrame().evaluateJavaScript(
		"addMarker( new Microsoft.Maps.Location({0},{1}),\"{2}\",\"{3}\",\"{4}\")".format(latitude,
																						longitude,
																						title,
																						icon,
																						content))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeMarkers(self):
		"""
		This method removes the map markers.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Removing GPS map markers.")

		self.page().mainFrame().evaluateJavaScript("removeMarkers()")
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setCenter(self):
		"""
		This method centers the map.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Centering GPS map.")

		self.page().mainFrame().evaluateJavaScript("setCenter()")
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
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
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setZoom(self, type):
		"""
		This method sets the map zoom.

		:param type: Zoom type. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Zooming '{0}' GPS map.".format(type))

		self.page().mainFrame().evaluateJavaScript("setZoom(\"{0}\")".format(type))
		return True
