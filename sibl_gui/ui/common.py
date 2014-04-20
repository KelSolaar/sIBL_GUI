#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines common ui manipulation related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import hashlib
import itertools
import os
import re
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPen

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.verbose
import sibl_gui.exceptions
import umbra.ui.common
from sibl_gui.libraries.freeimage.freeimage import Image
from sibl_gui.libraries.freeimage.freeimage import ImageInformationsHeader
from umbra.globals.ui_constants import UiConstants
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals

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
		"convert_image",
		"get_thumbnail_path",
		"extract_thumbnail",
		"load_graphics_item",
		"get_graphics_item",
		"get_icon",
		"get_pixmap",
		"get_image",
		"create_pixmap",
		"get_image_informations_header",
		"filter_image_path",
		"get_formatted_shot_date"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def convert_image(image, type):
	"""
	Converts given image to given type.

	:param image: Image to convert.
	:type image: QImage
	:param type: Type to convert to.
	:type type: QImage or QPixmap or QIcon
	:return: Converted image.
	:rtype: QImage or QPixmap or QIcon
	"""

	graphics_item = image
	if type == QIcon:
		graphics_item = QIcon(QPixmap(image))
	elif type == QPixmap:
		graphics_item = QPixmap(image)

	return graphics_item

def get_thumbnail_path(path, size, cache_directory=None):
	"""
	Returns given image thumbnail cached path at given size.

	:param path: Image path.
	:type path: unicode
	:param size: Thumbnail size.
	:type size: unicode
	:param cache_directory: Thumbnails cache directory.
	:type cache_directory: unicode
	:return: Cached thumbnail path.
	:rtype: unicode
	"""

	cache_directory = cache_directory if cache_directory is not None else RuntimeGlobals.thumbnails_cache_directory
	return os.path.join(cache_directory,
					hashlib.md5("{0}_{1}.png".format(path, size).encode(Constants.default_codec)).hexdigest())

def extract_thumbnail(path,
					size="Default",
					image=None,
					format="PNG",
					quality= -1,
					cache_directory=None):
	"""
	Extract given image thumbnail at given size.

	:param path: Image path.
	:type path: unicode
	:param size: Thumbnail size.
	:type size: unicode
	:param image: Image to use instead of given path one.
	:type image: QImage
	:param format: Thumbnail format.
	:type format: unicode
	:param quality: Thumbnail quality, -1 to 100.
	:type quality: int
	:param cache_directory: Thumbnails cache directory.
	:type cache_directory: unicode
	:return: Thumbnail image.
	:rtype: QImage
	"""

	cache_directory = cache_directory if cache_directory is not None else RuntimeGlobals.thumbnails_cache_directory

	if not foundations.common.path_exists(cache_directory):
		foundations.io.set_directory(cache_directory)

	thumbnail_path = get_thumbnail_path(path, size, cache_directory)
	if not os.path.exists(thumbnail_path):
		thumbnail = QImage(path) if image is None else image
		thumbnail = thumbnail.scaled(UiConstants.thumbnails_sizes.get(size),
							UiConstants.thumbnails_sizes.get(size),
							Qt.KeepAspectRatio,
							Qt.SmoothTransformation)
		thumbnail.save(thumbnail_path, format, quality)
		return thumbnail
	else:
		return QImage(thumbnail_path)

def load_graphics_item(path, type, size="Default"):
	"""
	Loads a graphic item: `QIcon <http://doc.qt.nokia.com/qicon.html>`_,
	`QImage <http://doc.qt.nokia.com/qimage.html>`_, `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_.

	:param path: Image path.
	:type path: unicode
	:param type: QIcon or QImage or QPixmap
	:type type: QObject
	:param size: Image size.
	:type size: unicode
	:return: Image.
	:rtype: QIcon or QImage or QPixmap
	"""

	if not foundations.common.path_exists(path):
		graphics_item = type(umbra.ui.common.get_resource_path(UiConstants.missing_image))
	else:
		for extension in UiConstants.native_image_formats.itervalues():
			if re.search(extension, path, flags=re.IGNORECASE):
				graphics_item = convert_image(extract_thumbnail(path, size), type) if size != "Default" else type(path)
				break
		else:
			error_image = umbra.ui.common.get_resource_path(UiConstants.format_error_image)
			for extension in UiConstants.third_party_image_formats.itervalues():
				if re.search(extension, path, flags=re.IGNORECASE):
					try:
						image = Image(path)
						image = image.convert_to_QImage()
						graphics_item = \
						convert_image(extract_thumbnail(path, size, image), type) if size != "Default" else \
						convert_image(image, type)
						break
					except Exception as error:
						LOGGER.error("!> {0} | Exception raised while reading '{1}' image: '{2}'!".format(__name__,
																									path,
																									error))
						graphics_item = type(error_image)
						break
			else:
				graphics_item = type(error_image)
	return graphics_item

def get_graphics_item(path, type, size="Default", asynchronous_loading=True, placeholder=None, images_cache=None):
	"""
	Returns a display item: `QIcon <http://doc.qt.nokia.com/qicon.html>`_,
	`QImage <http://doc.qt.nokia.com/qimage.html>`_, `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_ instance.

	:param path: Image path.
	:type path: unicode
	:param type: QIcon or QImage or QPixmap
	:type type: QObject
	:param size: Image size.
	:type size: unicode
	:param asynchronous_loading: Images are loaded asynchronously.
	:type asynchronous_loading: bool
	:param placeholder: Placeholder to use while loading asynchronously. ( QIcon, QImage, QPixmap )
	:param images_cache: Image cache.
	:type images_cache: Dictionary or AsynchronousGraphicsItemsCache
	:return: Image.
	:rtype: QIcon or QImage or QPixmap
	"""

	if not foundations.common.path_exists(path):
		LOGGER.warning("!> {0} | '{1}' file doesn't exists!".format(__name__, path))
		return load_graphics_item(path, type, size)

	cache = images_cache if images_cache else RuntimeGlobals.images_caches.get(type.__name__)
	if cache is None:
		raise sibl_gui.exceptions.CacheExistsError("{0} | '{1}' cache doesn't exists!".format(__name__, type.__name__))

	graphics_item = cache.get_content(path, size)
	if graphics_item is None:
		if asynchronous_loading:
			cache.load_asynchronous_content(**{path : (type, size, placeholder)})
		else:
			cache.load_content(**{path : (type, size)})
		return cache.get_content(path, size)
	return graphics_item

def get_icon(path, size="Default", asynchronous_loading=True, placeholder=None, images_cache=None):
	"""
	Returns a `QIcon <http://doc.qt.nokia.com/qicon.html>`_ instance.

	:param path: Icon image path.
	:type path: unicode
	:param size: Image size.
	:type size: unicode
	:param asynchronous_loading: Images are loaded asynchronously.
	:type asynchronous_loading: bool
	:param placeholder: Placeholder to use while loading asynchronously.
	:type placeholder: QIcon
	:param images_cache: Image cache.
	:type images_cache: Dictionary or AsynchronousGraphicsItemsCache
	:return: QIcon.
	:rtype: QIcon
	"""

	cache = images_cache if images_cache else RuntimeGlobals.images_caches.get("QIcon")
	return get_graphics_item(path, QIcon, size, asynchronous_loading, placeholder, cache)

def get_pixmap(path, size="Default", asynchronous_loading=True, placeholder=None, images_cache=None):
	"""
	Returns a `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_ instance.

	:param path: Icon image path.
	:type path: unicode
	:param size: Image size.
	:type size: unicode
	:param asynchronous_loading: Images are loaded asynchronously.
	:type asynchronous_loading: bool
	:param placeholder: Placeholder to use while loading asynchronously.
	:type placeholder: QPixmap
	:param images_cache: Image cache.
	:type images_cache: Dictionary or AsynchronousGraphicsItemsCache
	:return: QPixmap.
	:rtype: QPixmap
	"""

	cache = images_cache if images_cache else RuntimeGlobals.images_caches.get("QPixmap")
	return get_graphics_item(path, QPixmap, size, asynchronous_loading, placeholder, cache)

def get_image(path, size="Default", asynchronous_loading=True, placeholder=None, images_cache=None):
	"""
	Returns a `QImage <http://doc.qt.nokia.com/qimage.html>`_ instance.

	:param path: Icon image path.
	:type path: unicode
	:param size: Image size.
	:type size: unicode
	:param asynchronous_loading: Images are loaded asynchronously.
	:type asynchronous_loading: bool
	:param placeholder: Placeholder to use while loading asynchronously.
	:type placeholder: QImage
	:param images_cache: Image cache.
	:type images_cache: Dictionary or AsynchronousGraphicsItemsCache
	:return: QImage.
	:rtype: QImage
	"""

	cache = images_cache if images_cache else RuntimeGlobals.images_caches.get("QImage")
	return get_graphics_item(path, QImage, size, asynchronous_loading, placeholder, cache)

def create_pixmap(width=128, height=128, text=None):
	"""
	Create a default `QPixmap <http://doc.qt.nokia.com/qpixmap.html>`_ instance.

	:param width: Pixmap width.
	:type width: int
	:param height: Pixmap height.
	:type height: int
	:param text: Pximap text.
	:type text: unicode
	:return: QPixmap.
	:rtype: QPixmap
	"""

	loading_pixmap = QPixmap(width, height)
	loading_pixmap.fill(QColor(96, 96, 96))
	painter = QPainter(loading_pixmap)
	if text:
		painter.setPen(QPen(QColor(192, 192, 192)))
		point_x = painter.fontMetrics().width(text) / 2
		point_y = width / 2
		painter.drawText(point_x, point_y, text)
	return loading_pixmap

@foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
def get_image_informations_header(path, graphics_item):
	"""
	Returns a :class:`sibl_gui.libraries.freeimage.freeimage.ImageInformationsHeader` class
	from given path and graphics item.

	:param path: Image path.
	:type path: unicode
	:param graphics_item: Image graphics item. ( QImage, QPixmap, QIcon )
	:return: Image informations header.
	:rtype: ImageInformationsHeader
	"""

	if not foundations.common.path_exists(path):
		raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(__name__, path))

	if type(graphics_item) is QIcon:
		graphics_item = QPixmap(path)

	return ImageInformationsHeader(path=path,
									width=graphics_item.width(),
									height=graphics_item.height(),
									bpp=graphics_item.depth(),
									os_stats=os.stat(path))

def filter_image_path(path):
	"""
	Filters the image path.

	:param path: Image path.
	:type path: unicode
	:return: Path.
	:rtype: unicode
	"""

	if foundations.common.path_exists(path):
		for extension in itertools.chain(UiConstants.native_image_formats.itervalues(),
										UiConstants.third_party_image_formats.itervalues()):
			if re.search(extension, path, flags=re.IGNORECASE):
				return path
		else:
			return umbra.ui.common.get_resource_path(UiConstants.format_error_image)
	else:
		return umbra.ui.common.get_resource_path(UiConstants.missing_image)

def get_formatted_shot_date(date, time):
	"""
	Returns a formatted shot date.

	:param date: Ibl Set date key value.
	:type date: unicode
	:param time: Ibl Set time key value.
	:type time: unicode
	:return: Current shot date.
	:rtype: unicode
	"""

	LOGGER.debug("> Formatting shot date with '{0}' date and '{1}' time.".format(date, time))

	if not Constants.null_object in (time, date):
		shot_time = "{0}H{1}".format(*foundations.common.unpack_default(time.split(":"), 2, "?"))
		shot_date = date.replace(":", "/")[2:] + " - " + shot_time

		LOGGER.debug("> Formatted shot date: '{0}'.".format(shot_date))
		return shot_date
	else:
		return Constants.null_object
