#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preview.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Preview` Component Interface class, the :class:`ImagesPreviewer` class and others images preview related objects.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.ui.common
import sibl_gui.libraries.freeImage.freeImage as freeImage
import sibl_gui.ui.common
import umbra.ui.common
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Image_QGraphicsItem", "ImagesPreviewer"]

LOGGER = logging.getLogger(Constants.logger)

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Images_Previewer.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Image_QGraphicsItem(QGraphicsItem):
	"""
	This class is a `QGraphicsItem <http://doc.qt.nokia.com/4.7/qgraphicsitem.html>`_ subclass used to display provided `QImage <http://doc.qt.nokia.com/4.7/qimage.html>`_.
	"""

	@core.executionTrace
	def __init__(self, parent=None, image=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param image: Image. ( QImage )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QGraphicsItem.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__image = None
		self.image = image or QImage()
		self.__width = image.width()
		self.__height = image.height()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def image(self):
		"""
		This method is the property for **self.__image** attribute.

		:return: self.__image. ( QImage )
		"""

		return self.__image

	@image.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def image(self, value):
		"""
		This method is the setter method for **self.__image** attribute.

		:param value: Attribute value. ( QImage )
		"""

		if value:
			assert type(value) is QImage, "'{0}' attribute: '{1}' type is not 'QImage'!".format("image", value)
		self.__image = value

	@image.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def image(self):
		"""
		This method is the deleter method for **self.__image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "image"))

	@property
	def width(self):
		"""
		This method is the property for **self.__width** attribute.

		:return: self.__width. ( Integer )
		"""

		return self.__width

	@width.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def width(self, value):
		"""
		This method is the setter method for **self.__width** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("width", value)
		self.__width = value

	@width.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def width(self):
		"""
		This method is the deleter method for **self.__width** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "width"))

	@property
	def height(self):
		"""
		This method is the property for **self.__height** attribute.

		:return: self.__height. ( Integer )
		"""

		return self.__height

	@height.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def height(self, value):
		"""
		This method is the setter method for **self.__height** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("height", value)
		self.__height = value

	@height.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def height(self):
		"""
		This method is the deleter method for **self.__height** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "height"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def boundingRect(self):
		"""
		This method sets the bounding rectangle.
		"""

		return QRectF(-(self.__image.width()) / 2, -(self.__image.height()) / 2, self.__image.width(), self.__image.height())

	@core.executionTrace
	def paint(self, painter, options, widget):
		"""
		This method paints the image.

		:param painter: QPainter ( QPainter )
		:param options: QStyleOptionGraphicsItem ( QStyleOptionGraphicsItem )
		:param widget: QWidget ( QWidget )
		"""

		painter.drawImage(-(self.__image.width() / 2), -(self.__image.height() / 2), self.__image)

class ImagesPreviewer(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	| This class provides the Application images previewer.
	| It defines methods to navigate through the list of provided images ( List of images paths ), zoom in / out and fit the displayed image, etc...
	"""

	@core.executionTrace
	def __init__(self, parent, paths=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param paths: Images paths. ( List )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(ImagesPreviewer, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__paths = None
		self.paths = paths

		self.__uiResourcesDirectory = "resources"
		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResourcesDirectory)
		self.__uiPreviousImage = "Previous.png"
		self.__uiNextImage = "Next.png"
		self.__uiZoomOutImage = "Zoom_Out.png"
		self.__uiZoomInImage = "Zoom_In.png"

		# Ensure the ui object is destroyed on close to avoid memory leaks.
		self.setAttribute(Qt.WA_DeleteOnClose)
		# Reimplementing widget close event method.
		self.closeEvent = self.closeUi

		self.__graphicsSceneBackgroundColor = QColor(48, 48, 48)
		self.__minimumZoomFactor = 0.05
		self.__maximumZoomFactor = 25
		self.__previewerMargin = 128
		self.__displayGraphicsItemMargin = 32
		self.__graphicsSceneWidth = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).width() * (1 / self.__minimumZoomFactor * 1.75)
		self.__graphicsSceneHeight = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).height() * (1 / self.__minimumZoomFactor * 1.75)
		self.__wheelZoomFactor = 350.0
		self.__keyZoomFactor = 1.20

		self.__graphicsView = None
		self.__graphicsScene = None
		self.__displayGraphicsItem = None

		ImagesPreviewer.__initializeUi(self)

		self.fitImage()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def paths(self):
		"""
		This method is the property for **self.__paths** attribute.

		:return: self.__paths. ( List )
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def paths(self, value):
		"""
		This method is the setter method for **self.__paths** attribute.

		:param value: Attribute value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("paths", value)
		self.__paths = value

	@paths.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		This method is the deleter method for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "paths"))

	@property
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiPreviousImage(self):
		"""
		This method is the property for **self.__uiPreviousImage** attribute.

		:return: self.__uiPreviousImage. ( String )
		"""

		return self.__uiPreviousImage

	@uiPreviousImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self, value):
		"""
		This method is the setter method for **self.__uiPreviousImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self):
		"""
		This method is the deleter method for **self.__uiPreviousImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiPreviousImage"))

	@property
	def uiNextImage(self):
		"""
		This method is the property for **self.__uiNextImage** attribute.

		:return: self.__uiNextImage. ( String )
		"""

		return self.__uiNextImage

	@uiNextImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self, value):
		"""
		This method is the setter method for **self.__uiNextImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self):
		"""
		This method is the deleter method for **self.__uiNextImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiNextImage"))

	@property
	def uiZoomOutImage(self):
		"""
		This method is the property for **self.__uiZoomOutImage** attribute.

		:return: self.__uiZoomOutImage. ( String )
		"""

		return self.__uiZoomOutImage

	@uiZoomOutImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self, value):
		"""
		This method is the setter method for **self.__uiZoomOutImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomOutImage"))

	@uiZoomOutImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self):
		"""
		This method is the deleter method for **self.__uiZoomOutImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomOutImage"))

	@property
	def uiZoomInImage(self):
		"""
		This method is the property for **self.__uiZoomInImage** attribute.

		:return: self.__uiZoomInImage. ( String )
		"""

		return self.__uiZoomInImage

	@uiZoomInImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self, value):
		"""
		This method is the setter method for **self.__uiZoomInImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomInImage"))

	@uiZoomInImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self):
		"""
		This method is the deleter method for **self.__uiZoomInImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomInImage"))

	@property
	def graphicsSceneBackgroundColor(self):
		"""
		This method is the property for **self.__graphicsSceneBackgroundColor** attribute.

		:return: self.__graphicsSceneBackgroundColor. ( QColors )
		"""

		return self.__graphicsSceneBackgroundColor

	@graphicsSceneBackgroundColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self, value):
		"""
		This method is the setter method for **self.__graphicsSceneBackgroundColor** attribute.

		:param value: Attribute value. ( QColors )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsSceneBackgroundColor"))

	@graphicsSceneBackgroundColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self):
		"""
		This method is the deleter method for **self.__graphicsSceneBackgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsSceneBackgroundColor"))

	@property
	def previewerMargin(self):
		"""
		This method is the property for **self.__previewerMargin** attribute.

		:return: self.__previewerMargin. ( Integer )
		"""

		return self.__previewerMargin

	@previewerMargin.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewerMargin(self, value):
		"""
		This method is the setter method for **self.__previewerMargin** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "previewerMargin"))

	@previewerMargin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def previewerMargin(self):
		"""
		This method is the deleter method for **self.__previewerMargin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "previewerMargin"))

	@property
	def graphicsSceneWidth(self):
		"""
		This method is the property for **self.__graphicsSceneWidth** attribute.

		:return: self.__graphicsSceneWidth. ( Integer )
		"""

		return self.__graphicsSceneWidth

	@graphicsSceneWidth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self, value):
		"""
		This method is the setter method for **self.__graphicsSceneWidth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsSceneWidth"))

	@graphicsSceneWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self):
		"""
		This method is the deleter method for **self.__graphicsSceneWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsSceneWidth"))

	@property
	def graphicsSceneHeight(self):
		"""
		This method is the property for **self.__graphicsSceneHeight** attribute.

		:return: self.__graphicsSceneHeight. ( Object )
		"""

		return self.__graphicsSceneHeight

	@graphicsSceneHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self, value):
		"""
		This method is the setter method for **self.__graphicsSceneHeight** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsSceneHeight"))

	@graphicsSceneHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self):
		"""
		This method is the deleter method for **self.__graphicsSceneHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsSceneHeight"))

	@property
	def minimumZoomFactor(self):
		"""
		This method is the property for **self.__minimumZoomFactor** attribute.

		:return: self.__minimumZoomFactor. ( Float )
		"""

		return self.__minimumZoomFactor

	@minimumZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self, value):
		"""
		This method is the setter method for **self.__minimumZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "minimumZoomFactor"))

	@minimumZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self):
		"""
		This method is the deleter method for **self.__minimumZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "minimumZoomFactor"))

	@property
	def maximumZoomFactor(self):
		"""
		This method is the property for **self.__maximumZoomFactor** attribute.

		:return: self.__maximumZoomFactor. ( Float )
		"""

		return self.__maximumZoomFactor

	@maximumZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self, value):
		"""
		This method is the setter method for **self.__maximumZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximumZoomFactor"))

	@maximumZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self):
		"""
		This method is the deleter method for **self.__maximumZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumZoomFactor"))

	@property
	def wheelZoomFactor(self):
		"""
		This method is the property for **self.__wheelZoomFactor** attribute.

		:return: self.__wheelZoomFactor. ( Float )
		"""

		return self.__wheelZoomFactor

	@wheelZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self, value):
		"""
		This method is the setter method for **self.__wheelZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "wheelZoomFactor"))

	@wheelZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self):
		"""
		This method is the deleter method for **self.__wheelZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "wheelZoomFactor"))

	@property
	def keyZoomFactor(self):
		"""
		This method is the property for **self.__keyZoomFactor** attribute.

		:return: self.__keyZoomFactor. ( Float )
		"""

		return self.__keyZoomFactor

	@keyZoomFactor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self, value):
		"""
		This method is the setter method for **self.__keyZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "keyZoomFactor"))

	@keyZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self):
		"""
		This method is the deleter method for **self.__keyZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "keyZoomFactor"))

	@property
	def graphicsView(self):
		"""
		This method is the property for **self.__graphicsView** attribute.

		:return: self.__graphicsView. ( QGraphicsView )
		"""

		return self.__graphicsView

	@graphicsView.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsView(self, value):
		"""
		This method is the setter method for **self.__graphicsView** attribute.

		:param value: Attribute value. ( QGraphicsView )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsView"))

	@graphicsView.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsView(self):
		"""
		This method is the deleter method for **self.__graphicsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsView"))

	@property
	def graphicsScene(self):
		"""
		This method is the property for **self.__graphicsScene** attribute.

		:return: self.__graphicsScene. ( QGraphicsScene )
		"""

		return self.__graphicsScene

	@graphicsScene.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsScene(self, value):
		"""
		This method is the setter method for **self.__graphicsScene** attribute.

		:param value: Attribute value. ( QGraphicsScene )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsScene"))

	@graphicsScene.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def graphicsScene(self):
		"""
		This method is the deleter method for **self.__graphicsScene** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsScene"))

	@property
	def displayGraphicsItem(self):
		"""
		This method is the property for **self.__displayGraphicsItem** attribute.

		:return: self.__displayGraphicsItem. ( QGraphicsItem )
		"""

		return self.__displayGraphicsItem

	@displayGraphicsItem.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self, value):
		"""
		This method is the setter method for **self.__displayGraphicsItem** attribute.

		:param value: Attribute value. ( QGraphicsItem )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "displayGraphicsItem"))

	@displayGraphicsItem.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self):
		"""
		This method is the deleter method for **self.__displayGraphicsItem** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "displayGraphicsItem"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def show(self):
		"""
		This method redefines the ui show method.
		"""

		super(ImagesPreviewer, self).show()
		self.fitImage()

	@core.executionTrace
	def closeUi(self, event):
		"""
		This method redefines the ui close event.

		:param event: QEvent ( QEvent )
		"""

		event.accept()

		LOGGER.debug("> Removing '{0}' from Images Previewers list.".format(self))
		self.__container.imagesPreviewers.remove(self)

	@core.executionTrace
	def wheelEvent(self, event):
		"""
		This method redefines wheelevent.

		:param event: QEvent ( QEvent )
		"""

		self.scaleView(pow(1.5, event.delta() / self.__wheelZoomFactor))

	@core.executionTrace
	def keyPressEvent(self, event):
		"""
		This method redefines keypressevent.

		:param event: QEvent ( QEvent )
		"""

		key = event.key()
		if key == Qt.Key_Plus:
			self.scaleView(self.__keyZoomFactor)
		elif key == Qt.Key_Minus:
			self.scaleView(1 / self.__keyZoomFactor)
		else:
			QGraphicsView.keyPressEvent(self, event)

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		LOGGER.debug("> Initializing '{0}' ui.".format(self.__class__.__name__))

		self.Previous_Image_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiPreviousImage)))
		self.Next_Image_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiNextImage)))
		self.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiZoomInImage)))
		self.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiZoomOutImage)))
		len(self.__paths) <= 1 and self.Navigation_groupBox.hide()

		LOGGER.debug("> Initializing graphics View.")
		self.__graphicsView = QGraphicsView()
		self.__graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.__graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.__graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		self.__graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
		# Reimplementing QGraphicsView wheelEvent method.
		self.__graphicsView.wheelEvent = self.wheelEvent

		LOGGER.debug("> Initializing graphics scene.")
		self.__graphicsScene = QGraphicsScene(self.__graphicsView)
		self.__graphicsScene.setItemIndexMethod(QGraphicsScene.NoIndex)
		self.__graphicsScene.setSceneRect(-(float(self.__graphicsSceneWidth)) / 2, -(float(self.__graphicsSceneHeight)) / 2, float(self.__graphicsSceneWidth), float(self.__graphicsSceneHeight))

		self.__graphicsView.setScene(self.__graphicsScene)
		self.__graphicsView.setBackgroundBrush(QBrush(self.__graphicsSceneBackgroundColor))

		self.setImage()
		self.fitPreviewer()

		self.Images_Previewer_frame_gridLayout.addWidget(self.__graphicsView)

		# Signals / Slots.
		self.Previous_Image_pushButton.clicked.connect(self.__Previous_Image_pushButton__clicked)
		self.Next_Image_pushButton.clicked.connect(self.__Next_Image_pushButton__clicked)
		self.Zoom_Out_pushButton.clicked.connect(self.__Zoom_Out_pushButton__clicked)
		self.Zoom_In_pushButton.clicked.connect(self.__Zoom_In_pushButton_clicked)
		self.Zoom_Fit_pushButton.clicked.connect(self.__Zoom_Fit_pushButton__clicked)

	@core.executionTrace
	def __Previous_Image_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Previous_Image_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughImages(True)

	@core.executionTrace
	def __Next_Image_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Next_Image_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughImages()

	@core.executionTrace
	def __Zoom_In_pushButton_clicked(self, checked):
		"""
		This method is triggered when **Zoom_In_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.scaleView(self.__keyZoomFactor)

	@core.executionTrace
	def __Zoom_Out_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Zoom_Out_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.scaleView(1 / self.__keyZoomFactor)

	@core.executionTrace
	def __Zoom_Fit_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Zoom_Fit_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.fitImage()

	@core.executionTrace
	def scaleView(self, scaleFactor):
		"""
		This method scales the QGraphicsView.

		:param scaleFactor: Float ( Float )
		"""

		graphicsView = self.findChild(QGraphicsView)
		factor = graphicsView.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
		if factor < self.__minimumZoomFactor or factor > self.__maximumZoomFactor:
			return

		graphicsView.scale(scaleFactor, scaleFactor)

	@core.executionTrace
	def fitPreviewer(self):
		"""
		This method fits the previewer window.
		"""

		if self.__displayGraphicsItem:
			desktopWidth = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).width()
			desktopHeight = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).height()
			width = self.__displayGraphicsItem.width > desktopWidth and desktopWidth / 1.5 + self.__previewerMargin or self.__displayGraphicsItem.width + self.__previewerMargin
			height = self.__displayGraphicsItem.height > desktopHeight and desktopHeight / 1.5 + self.__previewerMargin or self.__displayGraphicsItem.height + self.__previewerMargin

			self.resize(width, height)
			umbra.ui.common.centerWidgetOnScreen(self)

	@core.executionTrace
	def setImage(self, index=0):
		"""
		This method sets the display image.

		:param index: Index to display. ( Integer )
		"""

		if self.__paths:
			path = self.__paths[index]
			image = sibl_gui.ui.common.getImage(path)
			if not hasattr(image, "_datas"):
				image._datas = freeImage.ImageInformationsHeader(path=path, width=image.width(), height=image.height(), bpp=image.depth())

			LOGGER.debug("> Initializing graphics item.")
			self.__displayGraphicsItem = Image_QGraphicsItem(image=image)
			self.__graphicsScene.addItem(self.__displayGraphicsItem)

			self.Images_Informations_label.setText("{0} - {1} x {2} - {3} bpp".format(os.path.basename(image._datas.path), image._datas.width, image._datas.height, image._datas.bpp))

	@core.executionTrace
	def fitImage(self):
		"""
		This method fits the display image.
		"""

		if self.__displayGraphicsItem:
			self.__graphicsView.fitInView(QRectF(-(self.__displayGraphicsItem.width / 2) - (self.__displayGraphicsItemMargin / 2), -(self.__displayGraphicsItem.height / 2) - (self.__displayGraphicsItemMargin / 2), self.__displayGraphicsItem.width + self.__displayGraphicsItemMargin, self.__displayGraphicsItem.height + self.__displayGraphicsItemMargin), Qt.KeepAspectRatio)

	@core.executionTrace
	def loopThroughImages(self, backward=False):
		"""
		This method loops through Images Previewer images.

		:param backward: Looping backward. ( Boolean )
		"""

		index = self.__paths.index(self.__displayGraphicsItem.image._datas.path)
		index += not backward and 1 or -1
		if index < 0:
			index = len(self.__paths) - 1
		elif index > len(self.__paths) - 1:
			index = 0
		self.setImage(index)
		self.fitImage()
