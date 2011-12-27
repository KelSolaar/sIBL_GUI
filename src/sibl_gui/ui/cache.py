#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**cache.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application cache classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import sibl_gui.ui.common
import sibl_gui.ui.workers
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

__all__ = ["LOGGER",
			"AbstractResourcesCache",
			"AsynchronousGraphicsCache"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class AbstractResourcesCache(QObject):
	"""
	This class is a `QObject <http://doc.qt.nokia.com/4.7/qobject.html>`_ subclass used as an abstract resources cache.
	"""

	contentAdded = pyqtSignal(list)
	"""
	This signal is emited by the :class:`AsynchronousGraphicsCache` class
	whenever content has been added. ( pyqtSignal )
	
	:return: Content added to the cache. ( List )	
	"""

	contentRemoved = pyqtSignal(list)
	"""
	This signal is emited by the :class:`AsynchronousGraphicsCache` class
	whenever content has been removed. ( pyqtSignal )
	
	:return: Content removed from the cache. ( List )	
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		QObject.__init__(self, parent)

		self.__mapping = {}

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def mapping(self):
		"""
		This method is the property for **self.__mapping** attribute.

		:return: self.__mapping. ( Dictionary )
		"""

		return self.__mapping

	@mapping.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def mapping(self, value):
		"""
		This method is the setter method for **self.__mapping** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "mapping"))

	@mapping.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def mapping(self):
		"""
		This method is the deleter method for **self.__mapping** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "mapping"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isCached(self, key):
		"""
		This method returns if given content is cached.

		:param key: Content to retrieve. ( Object )
		:return: Is content cached. ( Boolean )
		"""

		return key in self.__mapping

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addContent(self, **content):
		"""
		This method adds given content to the cache.

		:param \*\*content: Content to add. ( \*\* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' content to the cache.".format(self.__class__.__name__, content))

		self.__mapping.update(**content)
		self.contentAdded.emit(content.keys())
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeContent(self, *keys):
		"""
		This method removes given content from the cache.

		:param \*keys: Content to remove. ( \* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Removing '{0}' content from the cache.".format(self.__class__.__name__, keys))

		for key in keys:
			if not key in self.__mapping:
				raise KeyError("{0} | '{1}' key doesn't exists in cache content!".format(self.__class__.__name__, key))

			del self.__mapping[key]
			self.contentRemoved.emit([key])
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getContent(self, key):
		"""
		This method gets given content from the cache.

		:param key: Content to retrieve. ( Object )
		:return: Content. ( Object )
		"""

		LOGGER.debug("> Retrieving '{0}' content from the cache.".format(self.__class__.__name__, key))

		return self.__mapping.get(key)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def flushContent(self):
		"""
		This method flushes the cache content.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Flushing cache content.".format(self.__class__.__name__))

		content = self.__mapping.keys()
		self.__mapping.clear()
		self.contentRemoved.emit(content)
		return True

class AsynchronousGraphicsCache(AbstractResourcesCache):
	"""
	This class provides an asynchronous graphics resources cache.
	"""

	@core.executionTrace
	def __init__(self, parent=None, type=None, default=None):
		"""
		This method initializes the class.
		
		:param parent: Object parent. ( QObject )
		:param type: Cache type. ( QImage / QPixmap / QIcon )
		:param default: Default cache object. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractResourcesCache.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__type = type
		self.__default = default
		self.__worker = sibl_gui.ui.workers.GraphicsItem_worker()
		self.__worker.start()
		self.__worker.imageLoaded.connect(self.__worker__imageLoaded)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def type(self):
		"""
		This method is the property for **self.__type** attribute.

		:return: self.__type. ( QObject )
		"""

		return self.__type

	@type.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def type(self, value):
		"""
		This method is the setter method for **self.__type** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "type"))

	@type.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def type(self):
		"""
		This method is the deleter method for **self.__type** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "type"))

	@property
	def default(self):
		"""
		This method is the property for **self.__default** attribute.

		:return: self.__default. ( String )
		"""

		return self.__default

	@default.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def default(self, value):
		"""
		This method is the setter method for **self.__default** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default"))

	@default.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def default(self):
		"""
		This method is the deleter method for **self.__default** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default"))

	@property
	def worker(self):
		"""
		This method is the property for **self.__worker** attribute.

		:return: self.__worker. ( QThread )
		"""

		return self.__worker

	@worker.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def worker(self, value):
		"""
		This method is the setter method for **self.__worker** attribute.

		:param value: Attribute value. ( QThread )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"worker", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("worker", value)
		self.__worker = value

	@worker.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def worker(self):
		"""
		This method is the deleter method for **self.__worker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "worker"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __worker__imageLoaded(self, image):
		"""
		This method is triggered by the :obj:`AsynchronousGraphicsCache.worker` method when an image has been loaded.
		
		:param image: Loaded image. ( QImage )
		"""
		graphicsItem = sibl_gui.ui.common.convertImage(image, self.__type)
		graphicsItem.data = image.data
		path = graphicsItem.data.path
		self.mapping[path] = graphicsItem
		self.contentAdded.emit([path])

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addContent(self, **content):
		"""
		This method reimplements the :meth:`AbstractResourcesCache.addContent` method.
		
		:param \*\*content: Content to add. ( \*\* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' content to the cache.".format(self.__class__.__name__, content))

		for path, item in content.items():
			if type(item) is not self.__type:
				LOGGER.warning("!> {0} | '{1}' item type is not '{2}' type and has been skipped!".format(
				self.__class__.__name__, item, self.__type))
				del(content[path])

		self.mapping.update(**content)
		self.contentAdded.emit(content.keys())
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def addDeferredContent(self, *content):
		"""
		This method adds given content to the cache.

		:param \*content: Comantent to add. ( \* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' content to the cache.".format(self.__class__.__name__, content))

		for path in content:
			if not foundations.common.pathExists(path):
				raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
				self.__class__.__name__, path))

			if path in self.mapping:
				image = self.mapping.get(path)
				if hasattr(image, "data"):
					if image.data.osStats.st_mtime == os.stat(path).st_mtime:
						continue
					else:
						LOGGER.info("{0} | '{1}' file has been modified and will be reloaded!".format(
						self.__class__.__name__, path))

			self.mapping[path] = self.__type(self.default)
			self.contentAdded.emit([path])
			self.__worker.addRequest(path)
		return True
