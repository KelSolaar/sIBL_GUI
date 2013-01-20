#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**workers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application workers classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QImage
from Queue import Queue

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import sibl_gui.ui.common
from sibl_gui.libraries.freeImage.freeImage import ImageInformationsHeader

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "GraphicsItem_worker"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class GraphicsItem_worker(QThread):
	"""
	This class is a `QThread <http://doc.qt.nokia.com/qthread.html>`_ subclass used to load images.
	"""

	# If the signal uses **QImage** as signature instead of **object**, a copy gets passed to the slot instead
	# of the object itself, the issue is that the copy loses any defined extra attributes.
	imageLoaded = pyqtSignal(object)
	"""
	This signal is emited by the :class:`GraphicsItem_worker` class when an image has been loaded. ( pyqtSignal )
	
	:return: Loaded image. ( QImage )		
	"""

	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QThread.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__requests = Queue()
		self.__interrupt = False

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def requests(self):
		"""
		This method is the property for **self.__requests** attribute.

		:return: self.__requests. ( Queue )
		"""

		return self.__requests

	@requests.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def requests(self, value):
		"""
		This method is the setter method for **self.__requests** attribute.

		:param value: Attribute value. ( Queue )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "requests"))

	@requests.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def requests(self):
		"""
		This method is the deleter method for **self.__requests** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requests"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def addRequest(self, path):
		"""
		This method adds given image path to the requests queue.

		:param path: Image path. ( String )
		:return: Method success. ( Boolean )
		"""

		if not foundations.common.pathExists(path):
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while adding request: '{1}' file doesn't exists!".format(
			self.__class__.__name__, path))

		self.__requests.put(path)
		return True

	def run(self):
		"""
		This method reimplements the :meth:`QThread.run` method.
		"""

		while True:
			path = self.__requests.get()

			if self.__interrupt:
				return

			image = sibl_gui.ui.common.loadGraphicsItem(path, QImage)
			image.data = sibl_gui.ui.common.getImageInformationsHeader(path, image)
			self.imageLoaded.emit(image)

	def quit(self):
		"""
		This method reimplements the :meth:`QThread.quit` method.
		"""

		self.__interrupt = True
		self.__requests.put(None)

		QThread.quit(self)
