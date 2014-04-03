#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**caches.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application caches classes.

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
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import sibl_gui.ui.common
import sibl_gui.ui.workers
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"CacheMetrics",
		"AbstractResourcesCache",
		"AsynchronousGraphicsItemsCache"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class CacheMetrics(foundations.dataStructures.Structure):
	"""
	Defines a storage object for cache metrics.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: type, content.
		:type kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class AbstractResourcesCache(QObject):
	"""
	Defines a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass used as an abstract resources cache.
	"""

	contentAdded = pyqtSignal(list)
	"""
	This signal is emited by the :class:`AsynchronousGraphicsItemsCache` class
	whenever content has been added. ( pyqtSignal )
	
	:return: Content added to the cache.
	:rtype: list
	"""

	contentRemoved = pyqtSignal(list)
	"""
	This signal is emited by the :class:`AsynchronousGraphicsItemsCache` class
	whenever content has been removed. ( pyqtSignal )
	
	:return: Content removed from the cache.
	:rtype: list
	"""

	def __init__(self, parent=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		"""

		QObject.__init__(self, parent)

		self.__mapping = {}

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def mapping(self):
		"""
		Property for **self.__mapping** attribute.

		:return: self.__mapping.
		:rtype: dict
		"""

		return self.__mapping

	@mapping.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def mapping(self, value):
		"""
		Setter for **self.__mapping** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "mapping"))

	@mapping.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def mapping(self):
		"""
		Deleter for **self.__mapping** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "mapping"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __getitem__(self, item):
		"""
		Reimplements the :meth:`object.__getitem__` method.

		:param item: Item name.
		:type item: unicode
		:return: Item.
		:rtype: object
		"""

		return self.__mapping.__getitem__(item)

	def __setitem__(self, key, value):
		"""
		Reimplements the :meth:`object.__setitem__` method.

		:param key: Key.
		:type key: unicode
		:param value: Value.
		:type value: object
		"""

		self.__mapping.__setitem__(key, value)

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Paths iterator.
		:rtype: object
		"""

		return self.__mapping.iteritems()

	def __contains__(self, item):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param item: Item name.
		:type item: unicode
		:return: Item existence.
		:rtype: bool
		"""

		return item in self.__mapping.keys()

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Paths count.
		:rtype: int
		"""

		return len(self.__mapping.keys())

	def isCached(self, key):
		"""
		Returns if given content is cached.

		:param key: Content to retrieve.
		:type key: object
		:return: Is content cached.
		:rtype: bool
		"""

		return key in self

	def listContent(self):
		"""
		Lists the cache content.

		:return: Cache content.
		:rtype: list
		"""

		return self.__mapping.keys()

	def addContent(self, **content):
		"""
		Adds given content to the cache.

		:param \*\*content: Content to add.
		:type \*\*content: \*\*
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' content to the cache.".format(self.__class__.__name__, content))

		self.__mapping.update(**content)
		self.contentAdded.emit(content.keys())
		return True

	def removeContent(self, *keys):
		"""
		Removes given content from the cache.

		:param \*keys: Content to remove.
		:type \*keys: \*
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' content from the cache.".format(self.__class__.__name__, keys))

		for key in keys:
			if not key in self:
				raise KeyError("{0} | '{1}' key doesn't exists in cache content!".format(self.__class__.__name__, key))

			del(self.__mapping[key])
			self.contentRemoved.emit([key])
		return True

	def getContent(self, key):
		"""
		Gets given content from the cache.

		:param key: Content to retrieve.
		:type key: object
		:return: Content.
		:rtype: object
		"""

		LOGGER.debug("> Retrieving '{0}' content from the cache.".format(self.__class__.__name__, key))

		return self.__mapping.get(key)

	def flushContent(self):
		"""
		Flushes the cache content.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Flushing cache content.".format(self.__class__.__name__))

		content = self.__mapping.keys()
		self.__mapping.clear()
		self.contentRemoved.emit(content)
		return True

	def getMetrics(self):
		"""
		Returns the cache metrics.

		:return: Cache metrics.
		:rtype: dict
		"""

		cacheMetrics = CacheMetrics()
		cacheMetrics.type = None
		cacheMetrics.content = dict.fromkeys(self.__mapping.keys())
		return cacheMetrics

class AsynchronousGraphicsItemsCache(AbstractResourcesCache):
	"""
	Defines an asynchronous graphics items cache.
	"""

	def __init__(self, parent=None, type=None, placeholder=None):
		"""
		Initializes the class.
		
		:param parent: Object parent.
		:type parent: QObject
		:param type: Cache type.
		:type type: QImage or QPixmap or QIcon
		:param placeholder: Placeholder image.
		:type placeholder: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractResourcesCache.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__type = type
		self.__placeholder = placeholder

		self.__placeholderGraphicsItem = None
		self.__worker = sibl_gui.ui.workers.GraphicsItem_worker()
		self.__worker.start()
		self.__worker.imageLoaded.connect(self.__worker__imageLoaded)

		self.__setPlaceholderGraphicsItem(placeholder)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def type(self):
		"""
		Property for **self.__type** attribute.

		:return: self.__type.
		:rtype: QObject
		"""

		return self.__type

	@type.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def type(self, value):
		"""
		Setter for **self.__type** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "type"))

	@type.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def type(self):
		"""
		Deleter for **self.__type** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "type"))

	@property
	def placeholder(self):
		"""
		Property for **self.__placeholder** attribute.

		:return: self.__placeholder.
		:rtype: unicode
		"""

		return self.__placeholder

	@placeholder.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def placeholder(self, value):
		"""
		Setter for **self.__placeholder** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "placeholder"))

	@placeholder.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def placeholder(self):
		"""
		Deleter for **self.__placeholder** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "placeholder"))

	@property
	def placeholderGraphicsItem(self):
		"""
		Property for **self.__placeholderGraphicsItem** attribute.

		:return: self.__placeholderGraphicsItem.
		:rtype: QObject
		"""

		return self.__placeholderGraphicsItem

	@placeholderGraphicsItem.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def placeholderGraphicsItem(self, value):
		"""
		Setter for **self.__placeholderGraphicsItem** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "placeholderGraphicsItem"))

	@placeholderGraphicsItem.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def placeholderGraphicsItem(self):
		"""
		Deleter for **self.__placeholderGraphicsItem** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "placeholderGraphicsItem"))

	@property
	def worker(self):
		"""
		Property for **self.__worker** attribute.

		:return: self.__worker.
		:rtype: QThread
		"""

		return self.__worker

	@worker.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def worker(self, value):
		"""
		Setter for **self.__worker** attribute.

		:param value: Attribute value.
		:type value: QThread
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"worker", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("worker", value)
		self.__worker = value

	@worker.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def worker(self):
		"""
		Deleter for **self.__worker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "worker"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __worker__imageLoaded(self, image, size):
		"""
		Defines the slot triggered by :obj:`AsynchronousGraphicsItemsCache.worker` method when an image has been loaded.
		
		:param image: Loaded image.
		:type image: QImage
		:param size: Image size.
		:type size: unicode
		"""

		graphicsItem = sibl_gui.ui.common.convertImage(image, self.__type)
		graphicsItem.data = image.data
		path = graphicsItem.data.path
		if not self.isCached(path):
			return

		self[path][foundations.strings.toString(size)] = graphicsItem
		self.contentAdded.emit([path])

	def __setPlaceholderGraphicsItem(self, path):
		"""
		Sets the placeholderGraphicsItem graphics item.
		
		:param path: Placeholder image path.
		:type path: unicode
		"""

		if not foundations.common.pathExists(path):
			LOGGER.warning(
			"!> {0} | '{1}' placeholder graphics item file doesn't exists, unexpected behavior may occur!".format(
			self.__class__.__name__, self))
			return

		self.__placeholderGraphicsItem = self.__type(path)
		self.__placeholderGraphicsItem.data = sibl_gui.ui.common.getImageInformationsHeader(path, self.__placeholderGraphicsItem)

	def getContent(self, key, size="Default"):
		"""
		Reimplements the :meth:`AbstractResourcesCache.getContent` method.

		:param key: Content to retrieve.
		:type key: object
		:param size: Size to retrieve.
		:type size: unicode
		:return: Content.
		:rtype: object
		"""

		LOGGER.debug("> Retrieving '{0}' content from the cache.".format(self.__class__.__name__, key))

		content = self.mapping.get(key)
		if content is not None:
			return content.get(size)

	def flushContent(self):
		"""
		Reimplements the :meth:`AbstractResourcesCache.flushContent` method.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Flushing cache content.".format(self.__class__.__name__))

		if self.__worker.flushRequests():
			content = self.mapping.keys()
			self.mapping.clear()
			self.contentRemoved.emit(content)
			return True
		return False

	def loadContent(self, **content):
		"""
		Loads given content into the cache.
		
		:param \*\*content: Content to add.
		:type \*\*content: \*\*
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' content to the cache.".format(self.__class__.__name__, content))

		for path, data in content.iteritems():
			type, size = data

			if not foundations.common.pathExists(path):
				LOGGER.warning("!> {0} | '{1}' file doesn't exists and has been skipped!".format(
				self.__class__.__name__, path))
				continue

			if not self.isCached(path):
				self[path] = dict.fromkeys(UiConstants.thumbnailsSizes.keys())

			image = sibl_gui.ui.common.loadGraphicsItem(path, type, size)
			image.data = sibl_gui.ui.common.getImageInformationsHeader(path, image)
			self[path][size] = image

			self.contentAdded.emit([path])
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def loadAsynchronousContent(self, **content):
		"""
		Loads given content asynchronously into the cache.

		:param \*\*content: Content to add.
		:type \*\*content: \*\*
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' content to the cache.".format(self.__class__.__name__, content))

		for path, data in content.iteritems():
			type, size, placeholder = data

			if not foundations.common.pathExists(path):
				raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
				self.__class__.__name__, path))

			if not self.isCached(path):
				self[path] = dict.fromkeys(UiConstants.thumbnailsSizes.keys())

			image = self.getContent(path, size)
			if image is not None:
				if not hasattr(image, "data"):
					LOGGER.debug("> {0} | '{1}' object has not 'data' attribute and has been skipped!".format(
					self.__class__.__name__, image))
					continue

				if image.data.path != path:
					continue

				if image.data.osStats.st_mtime == os.stat(path).st_mtime:
					continue
				else:
					LOGGER.info("{0} | '{1}' file has been modified and will be reloaded!".format(
					self.__class__.__name__, path))

			self[path][size] = placeholder if placeholder is not None else self.__placeholderGraphicsItem
			self.contentAdded.emit([path])
			self.__worker.addRequest((path, size))
		return True

	def getMetrics(self):
		"""
		Reimplements the :meth:`AbstractResourcesCache.getMetrics` method.

		:return: Cache metrics.
		:rtype: dict
		"""

		cacheMetrics = AbstractResourcesCache.getMetrics(self)
		cacheMetrics.type = self.__type
		content = {}
		for path, data in self.mapping.iteritems():
			thumbnails = {}
			for size, thumbnail in data.iteritems():
				thumbnails[size] = None if thumbnail is None else (sibl_gui.ui.common.getThumbnailPath(path, size),
																	thumbnail.data)
			content[path] = thumbnails
		cacheMetrics.content = content
		return cacheMetrics
