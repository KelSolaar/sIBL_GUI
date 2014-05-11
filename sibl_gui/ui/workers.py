#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**workers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application workers classes.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QImage
from Queue import Queue

import foundations.exceptions
import foundations.verbose
import sibl_gui.ui.common

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "GraphicsItem_worker"]

LOGGER = foundations.verbose.install_logger()

class GraphicsItem_worker(QThread):
	"""
	Defines a `QThread <http://doc.qt.nokia.com/qthread.html>`_ subclass used to load images.
	"""

	# If the signal uses **QImage** as signature instead of **object**, a copy gets passed to the slot instead
	# of the object itself, the issue is that the copy loses any defined extra attributes.
	image_loaded = pyqtSignal(object, unicode)
	"""
	This signal is emited by the :class:`GraphicsItem_worker` class when an image has been loaded.
	
	:return: Loaded image.
	:rtype: QImage
	"""

	def __init__(self, parent=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QThread.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__requests = Queue()
		self.__interrupt = False

	@property
	def requests(self):
		"""
		Property for **self.__requests** attribute.

		:return: self.__requests.
		:rtype: Queue
		"""

		return self.__requests

	@requests.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def requests(self, value):
		"""
		Setter for **self.__requests** attribute.

		:param value: Attribute value.
		:type value: Queue
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "requests"))

	@requests.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def requests(self):
		"""
		Deleter for **self.__requests** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requests"))

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
	def addRequest(self, request):
		"""
		Adds given request to the requests queue.

		:param request: Request.
		:type request: tuple or list
		:return: Method success.
		:rtype: bool
		"""

		path, size = request
		if not foundations.common.path_exists(path):
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while adding request: '{1}' file doesn't exists!".format(
			self.__class__.__name__, path))

		self.__requests.put(request)
		return True

	def flush_requests(self):
		"""
		Flushes the requests queue.

		:return: Method success.
		:rtype: bool
		"""

		with self.__requests.mutex:
			self.__requests.queue.clear()
		return True

	def run(self):
		"""
		Reimplements the :meth:`QThread.run` method.
		"""

		while True:
			request = self.__requests.get()

			if self.__interrupt:
				return

			path, size = request
			image = sibl_gui.ui.common.load_graphics_item(path, QImage, size)
			image.data = sibl_gui.ui.common.get_image_informations_header(path, image)
			self.image_loaded.emit(image, size)

	def quit(self):
		"""
		Reimplements the :meth:`QThread.quit` method.
		"""

		self.__interrupt = True
		self.__requests.put(None)

		QThread.quit(self)
