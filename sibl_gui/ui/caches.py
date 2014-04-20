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
from umbra.globals.ui_constants import UiConstants

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

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class CacheMetrics(foundations.data_structures.Structure):
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

		foundations.data_structures.Structure.__init__(self, **kwargs)

class AbstractResourcesCache(QObject):
	"""
	Defines a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass used as an abstract resources cache.
	"""

	content_added = pyqtSignal(list)
	"""
	This signal is emited by the :class:`AsynchronousGraphicsItemsCache` class
	whenever content has been added.
	
	:return: Content added to the cache.
	:rtype: list
	"""

	content_removed = pyqtSignal(list)
	"""
	This signal is emited by the :class:`AsynchronousGraphicsItemsCache` class
	whenever content has been removed.
	
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def mapping(self, value):
		"""
		Setter for **self.__mapping** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "mapping"))

	@mapping.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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

	def is_cached(self, key):
		"""
		Returns if given content is cached.

		:param key: Content to retrieve.
		:type key: object
		:return: Is content cached.
		:rtype: bool
		"""

		return key in self

	def list_content(self):
		"""
		Lists the cache content.

		:return: Cache content.
		:rtype: list
		"""

		return self.__mapping.keys()

	def add_content(self, **content):
		"""
		Adds given content to the cache.

		:param \*\*content: Content to add.
		:type \*\*content: \*\*
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' content to the cache.".format(self.__class__.__name__, content))

		self.__mapping.update(**content)
		self.content_added.emit(content.keys())
		return True

	def remove_content(self, *keys):
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
			self.content_removed.emit([key])
		return True

	def get_content(self, key):
		"""
		Gets given content from the cache.

		:param key: Content to retrieve.
		:type key: object
		:return: Content.
		:rtype: object
		"""

		LOGGER.debug("> Retrieving '{0}' content from the cache.".format(self.__class__.__name__, key))

		return self.__mapping.get(key)

	def flush_content(self):
		"""
		Flushes the cache content.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Flushing cache content.".format(self.__class__.__name__))

		content = self.__mapping.keys()
		self.__mapping.clear()
		self.content_removed.emit(content)
		return True

	def get_metrics(self):
		"""
		Returns the cache metrics.

		:return: Cache metrics.
		:rtype: dict
		"""

		cache_metrics = CacheMetrics()
		cache_metrics.type = None
		cache_metrics.content = dict.fromkeys(self.__mapping.keys())
		return cache_metrics

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

		self.__placeholder_graphics_item = None
		self.__worker = sibl_gui.ui.workers.GraphicsItem_worker()
		self.__worker.start()
		self.__worker.image_loaded.connect(self.__worker__image_loaded)

		self.__set_placeholder_graphics_item(placeholder)

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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def type(self, value):
		"""
		Setter for **self.__type** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "type"))

	@type.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def placeholder(self, value):
		"""
		Setter for **self.__placeholder** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "placeholder"))

	@placeholder.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def placeholder(self):
		"""
		Deleter for **self.__placeholder** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "placeholder"))

	@property
	def placeholder_graphics_item(self):
		"""
		Property for **self.__placeholder_graphics_item** attribute.

		:return: self.__placeholder_graphics_item.
		:rtype: QObject
		"""

		return self.__placeholder_graphics_item

	@placeholder_graphics_item.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def placeholder_graphics_item(self, value):
		"""
		Setter for **self.__placeholder_graphics_item** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "placeholder_graphics_item"))

	@placeholder_graphics_item.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def placeholder_graphics_item(self):
		"""
		Deleter for **self.__placeholder_graphics_item** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "placeholder_graphics_item"))

	@property
	def worker(self):
		"""
		Property for **self.__worker** attribute.

		:return: self.__worker.
		:rtype: QThread
		"""

		return self.__worker

	@worker.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def worker(self):
		"""
		Deleter for **self.__worker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "worker"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __worker__image_loaded(self, image, size):
		"""
		Defines the slot triggered by :obj:`AsynchronousGraphicsItemsCache.worker` method when an image has been loaded.
		
		:param image: Loaded image.
		:type image: QImage
		:param size: Image size.
		:type size: unicode
		"""

		graphics_item = sibl_gui.ui.common.convert_image(image, self.__type)
		graphics_item.data = image.data
		path = graphics_item.data.path
		if not self.is_cached(path):
			return

		self[path][foundations.strings.to_string(size)] = graphics_item
		self.content_added.emit([path])

	def __set_placeholder_graphics_item(self, path):
		"""
		Sets the placeholder_graphics_item graphics item.
		
		:param path: Placeholder image path.
		:type path: unicode
		"""

		if not foundations.common.path_exists(path):
			LOGGER.warning(
			"!> {0} | '{1}' placeholder graphics item file doesn't exists, unexpected behavior may occur!".format(
			self.__class__.__name__, self))
			return

		self.__placeholder_graphics_item = self.__type(path)
		self.__placeholder_graphics_item.data = sibl_gui.ui.common.get_image_informations_header(path, self.__placeholder_graphics_item)

	def get_content(self, key, size="Default"):
		"""
		Reimplements the :meth:`AbstractResourcesCache.get_content` method.

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

	def flush_content(self):
		"""
		Reimplements the :meth:`AbstractResourcesCache.flush_content` method.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Flushing cache content.".format(self.__class__.__name__))

		if self.__worker.flush_requests():
			content = self.mapping.keys()
			self.mapping.clear()
			self.content_removed.emit(content)
			return True
		return False

	def load_content(self, **content):
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

			if not foundations.common.path_exists(path):
				LOGGER.warning("!> {0} | '{1}' file doesn't exists and has been skipped!".format(
				self.__class__.__name__, path))
				continue

			if not self.is_cached(path):
				self[path] = dict.fromkeys(UiConstants.thumbnails_sizes.keys())

			image = sibl_gui.ui.common.load_graphics_item(path, type, size)
			image.data = sibl_gui.ui.common.get_image_informations_header(path, image)
			self[path][size] = image

			self.content_added.emit([path])
		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
	def load_asynchronous_content(self, **content):
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

			if not foundations.common.path_exists(path):
				raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
				self.__class__.__name__, path))

			if not self.is_cached(path):
				self[path] = dict.fromkeys(UiConstants.thumbnails_sizes.keys())

			image = self.get_content(path, size)
			if image is not None:
				if not hasattr(image, "data"):
					LOGGER.debug("> {0} | '{1}' object has not 'data' attribute and has been skipped!".format(
					self.__class__.__name__, image))
					continue

				if image.data.path != path:
					continue

				if image.data.os_stats.st_mtime == os.stat(path).st_mtime:
					continue
				else:
					LOGGER.info("{0} | '{1}' file has been modified and will be reloaded!".format(
					self.__class__.__name__, path))

			self[path][size] = placeholder if placeholder is not None else self.__placeholder_graphics_item
			self.content_added.emit([path])
			self.__worker.addRequest((path, size))
		return True

	def get_metrics(self):
		"""
		Reimplements the :meth:`AbstractResourcesCache.get_metrics` method.

		:return: Cache metrics.
		:rtype: dict
		"""

		cache_metrics = AbstractResourcesCache.get_metrics(self)
		cache_metrics.type = self.__type
		content = {}
		for path, data in self.mapping.iteritems():
			thumbnails = {}
			for size, thumbnail in data.iteritems():
				thumbnails[size] = None if thumbnail is None else (sibl_gui.ui.common.get_thumbnail_path(path, size),
																	thumbnail.data)
			content[path] = thumbnails
		cache_metrics.content = content
		return cache_metrics
