#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines
	the :class:`sibl_gui.components.core.collections_outliner.collections_outliner.CollectionsOutliner` Component
	Interface class Views.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtWebKit import QWebView

import foundations.verbose

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Map_QWebView"]

LOGGER = foundations.verbose.install_logger()

class Map_QWebView(QWebView):
	"""
	| Defines a `QWebView <http://doc.qt.nokia.com/qwebview.html>`_ subclass used for the GPS map.
	| It provides various methods to manipulate the `Microsoft Bing Maps <http://www.bing.com/maps/>`_ defined
		in the Component resources html file through Javascript evaluation.
	"""

	def __init__(self, parent=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		"""

		QWebView.__init__(self, parent)

	def __evaluate_javascript(self, javascript):
		"""
		Evaluates given javascript content in the View.

		:param javascript: Javascript.
		:type javascript: unicode
		"""

		self.page().mainFrame().evaluateJavaScript(javascript)

	def add_marker(self, coordinates, title, icon, content):
		"""
		Adds a marker to the GPS map.

		:param coordinates: Marker coordinates.
		:type coordinates: tuple
		:param title: Marker title.
		:type title: unicode
		:param icon: Marker icon.
		:type icon: unicode
		:param content: Marker popup window content.
		:type content: unicode
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' marker to gps map with '{1}' coordinates.".format(title, coordinates))

		latitude, longitude = coordinates
		self.__evaluate_javascript(
		"addMarker(new Microsoft.Maps.Location({0},{1}),\"{2}\",\"{3}\",\"{4}\")".format(latitude,
																						longitude,
																						title,
																						icon,
																						content))
		return True

	def remove_markers(self):
		"""
		Removes the GPS map markers.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing GPS map markers.")

		self.__evaluate_javascript("removeMarkers()")
		return True

	def set_center(self):
		"""
		Centers the GPS map.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Centering GPS map.")

		self.__evaluate_javascript("setCenter()")
		return True

	def set_map_type(self, mapTypeId):
		"""
		Sets the GPS map type.

		Available map types:

			- MapTypeId.auto
			- MapTypeId.aerial
			- MapTypeId.road

		:param mapTypeId: GPS map type.
		:type mapTypeId: unicode
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Setting GPS map type to '{0}'.".format(mapTypeId))

		self.__evaluate_javascript("setMapType(\"{0}\")".format(mapTypeId))
		return True

	def set_zoom(self, type):
		"""
		Sets the GPS map zoom.

		:param type: Zoom type.
		:type type: unicode
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Zooming '{0}' GPS map.".format(type))

		self.__evaluate_javascript("setZoom(\"{0}\")".format(type))
		return True
