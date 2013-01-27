#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preview.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Preview` Component Interface class, the :class:`ImagesPreviewer` class
	and others images preview related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtCore import QRectF
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QGraphicsItem
from PyQt4.QtGui import QGraphicsScene
from PyQt4.QtGui import QGraphicsView
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QImage

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.ui.common
import foundations.verbose
import sibl_gui.ui.common

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Image_QGraphicsItem", "ImagesPreviewer"]

LOGGER = foundations.verbose.installLogger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Images_Previewer.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Image_QGraphicsItem(QGraphicsItem):
	"""
	This class is a `QGraphicsItem <http://doc.qt.nokia.com/qgraphicsitem.html>`_ subclass used
		to display given `QImage <http://doc.qt.nokia.com/qimage.html>`_.
	"""

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

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def image(self):
		"""
		This method is the property for **self.__image** attribute.

		:return: self.__image. ( QImage )
		"""

		return self.__image

	@image.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def image(self, value):
		"""
		This method is the setter method for **self.__image** attribute.

		:param value: Attribute value. ( QImage )
		"""

		if value is not None:
			assert type(value) is QImage, "'{0}' attribute: '{1}' type is not 'QImage'!".format("image", value)
		self.__image = value

	@image.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def image(self):
		"""
		This method is the deleter method for **self.__image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "image"))

	@property
	def width(self):
		"""
		This method is the property for **self.__width** attribute.

		:return: self.__width. ( Integer )
		"""

		return self.__width

	@width.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def width(self, value):
		"""
		This method is the setter method for **self.__width** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("width", value)
		self.__width = value

	@width.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def width(self):
		"""
		This method is the deleter method for **self.__width** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "width"))

	@property
	def height(self):
		"""
		This method is the property for **self.__height** attribute.

		:return: self.__height. ( Integer )
		"""

		return self.__height

	@height.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def height(self, value):
		"""
		This method is the setter method for **self.__height** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("height", value)
		self.__height = value

	@height.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def height(self):
		"""
		This method is the deleter method for **self.__height** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "height"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def boundingRect(self):
		"""
		This method reimplements the :meth:`QGraphicsItem.boundingRect` method.
		"""

		return QRectF(-(self.__image.width()) / 2,
					- (self.__image.height()) / 2,
					self.__image.width(),
					self.__image.height())

	def paint(self, painter, options, widget):
		"""
		This method reimplements the :meth:`QGraphicsItem.paint` method.

		:param painter: QPainter ( QPainter )
		:param options: QStyleOptionGraphicsItem ( QStyleOptionGraphicsItem )
		:param widget: QWidget ( QWidget )
		"""

		painter.drawImage(-(self.__image.width() / 2), -(self.__image.height() / 2), self.__image)

class ImagesPreviewer(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	| This class provides the Application images previewer.
	| It defines methods to navigate through the list of given images ( List of images paths ),
		zoom in / out and fit the displayed image, etc...
	"""

	def __init__(self, parent, paths=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param paths: Images paths. ( Tuple / List )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(ImagesPreviewer, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__paths = None
		self.paths = paths

		self.__uiResourcesDirectory = "resources"
		self.__uiResourcesDirectory = os.path.join(os.path.dirname(__file__), self.__uiResourcesDirectory)
		self.__uiPreviousImage = "Previous.png"
		self.__uiNextImage = "Next.png"
		self.__uiZoomOutImage = "Zoom_Out.png"
		self.__uiZoomInImage = "Zoom_In.png"

		# Ensure the ui object is destroyed on close to avoid memory leaks.
		self.setAttribute(Qt.WA_DeleteOnClose)

		self.__graphicsSceneBackgroundColor = QColor(32, 32, 32)
		self.__minimumZoomFactor = 0.05
		self.__maximumZoomFactor = 25
		self.__displayGraphicsItemMargin = 32
		self.__graphicsSceneWidth = QApplication.desktop().screenGeometry(
								QApplication.desktop().primaryScreen()).width() * (1 / self.__minimumZoomFactor * 1.75)
		self.__graphicsSceneHeight = QApplication.desktop().screenGeometry(
								QApplication.desktop().primaryScreen()).height() * (1 / self.__minimumZoomFactor * 1.75)
		self.__wheelZoomFactor = 350.0
		self.__keyZoomFactor = 1.20

		self.__graphicsView = None
		self.__graphicsScene = None
		self.__displayGraphicsItem = None

		ImagesPreviewer.__initializeUi(self)

		self.loadImage()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def paths(self):
		"""
		This method is the property for **self.__paths** attribute.

		:return: self.__paths. ( Tuple / List )
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def paths(self, value):
		"""
		This method is the setter method for **self.__paths** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format("paths", value)
			for element in value:
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"paths", element)
		self.__paths = value

	@paths.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		This method is the deleter method for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "paths"))

	@property
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiPreviousImage(self):
		"""
		This method is the property for **self.__uiPreviousImage** attribute.

		:return: self.__uiPreviousImage. ( String )
		"""

		return self.__uiPreviousImage

	@uiPreviousImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self, value):
		"""
		This method is the setter method for **self.__uiPreviousImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self):
		"""
		This method is the deleter method for **self.__uiPreviousImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiPreviousImage"))

	@property
	def uiNextImage(self):
		"""
		This method is the property for **self.__uiNextImage** attribute.

		:return: self.__uiNextImage. ( String )
		"""

		return self.__uiNextImage

	@uiNextImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiNextImage(self, value):
		"""
		This method is the setter method for **self.__uiNextImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiNextImage(self):
		"""
		This method is the deleter method for **self.__uiNextImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiNextImage"))

	@property
	def uiZoomOutImage(self):
		"""
		This method is the property for **self.__uiZoomOutImage** attribute.

		:return: self.__uiZoomOutImage. ( String )
		"""

		return self.__uiZoomOutImage

	@uiZoomOutImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self, value):
		"""
		This method is the setter method for **self.__uiZoomOutImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomOutImage"))

	@uiZoomOutImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self):
		"""
		This method is the deleter method for **self.__uiZoomOutImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomOutImage"))

	@property
	def uiZoomInImage(self):
		"""
		This method is the property for **self.__uiZoomInImage** attribute.

		:return: self.__uiZoomInImage. ( String )
		"""

		return self.__uiZoomInImage

	@uiZoomInImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self, value):
		"""
		This method is the setter method for **self.__uiZoomInImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomInImage"))

	@uiZoomInImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self):
		"""
		This method is the deleter method for **self.__uiZoomInImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomInImage"))

	@property
	def graphicsSceneBackgroundColor(self):
		"""
		This method is the property for **self.__graphicsSceneBackgroundColor** attribute.

		:return: self.__graphicsSceneBackgroundColor. ( QColors )
		"""

		return self.__graphicsSceneBackgroundColor

	@graphicsSceneBackgroundColor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self, value):
		"""
		This method is the setter method for **self.__graphicsSceneBackgroundColor** attribute.

		:param value: Attribute value. ( QColors )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsSceneBackgroundColor"))

	@graphicsSceneBackgroundColor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self):
		"""
		This method is the deleter method for **self.__graphicsSceneBackgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsSceneBackgroundColor"))

	@property
	def graphicsSceneWidth(self):
		"""
		This method is the property for **self.__graphicsSceneWidth** attribute.

		:return: self.__graphicsSceneWidth. ( Integer )
		"""

		return self.__graphicsSceneWidth

	@graphicsSceneWidth.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self, value):
		"""
		This method is the setter method for **self.__graphicsSceneWidth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsSceneWidth"))

	@graphicsSceneWidth.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self):
		"""
		This method is the deleter method for **self.__graphicsSceneWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsSceneWidth"))

	@property
	def graphicsSceneHeight(self):
		"""
		This method is the property for **self.__graphicsSceneHeight** attribute.

		:return: self.__graphicsSceneHeight. ( Object )
		"""

		return self.__graphicsSceneHeight

	@graphicsSceneHeight.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self, value):
		"""
		This method is the setter method for **self.__graphicsSceneHeight** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsSceneHeight"))

	@graphicsSceneHeight.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self):
		"""
		This method is the deleter method for **self.__graphicsSceneHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsSceneHeight"))

	@property
	def minimumZoomFactor(self):
		"""
		This method is the property for **self.__minimumZoomFactor** attribute.

		:return: self.__minimumZoomFactor. ( Float )
		"""

		return self.__minimumZoomFactor

	@minimumZoomFactor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self, value):
		"""
		This method is the setter method for **self.__minimumZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "minimumZoomFactor"))

	@minimumZoomFactor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self):
		"""
		This method is the deleter method for **self.__minimumZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "minimumZoomFactor"))

	@property
	def maximumZoomFactor(self):
		"""
		This method is the property for **self.__maximumZoomFactor** attribute.

		:return: self.__maximumZoomFactor. ( Float )
		"""

		return self.__maximumZoomFactor

	@maximumZoomFactor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self, value):
		"""
		This method is the setter method for **self.__maximumZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximumZoomFactor"))

	@maximumZoomFactor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self):
		"""
		This method is the deleter method for **self.__maximumZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumZoomFactor"))

	@property
	def wheelZoomFactor(self):
		"""
		This method is the property for **self.__wheelZoomFactor** attribute.

		:return: self.__wheelZoomFactor. ( Float )
		"""

		return self.__wheelZoomFactor

	@wheelZoomFactor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self, value):
		"""
		This method is the setter method for **self.__wheelZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "wheelZoomFactor"))

	@wheelZoomFactor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self):
		"""
		This method is the deleter method for **self.__wheelZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "wheelZoomFactor"))

	@property
	def keyZoomFactor(self):
		"""
		This method is the property for **self.__keyZoomFactor** attribute.

		:return: self.__keyZoomFactor. ( Float )
		"""

		return self.__keyZoomFactor

	@keyZoomFactor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self, value):
		"""
		This method is the setter method for **self.__keyZoomFactor** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "keyZoomFactor"))

	@keyZoomFactor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self):
		"""
		This method is the deleter method for **self.__keyZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "keyZoomFactor"))

	@property
	def graphicsView(self):
		"""
		This method is the property for **self.__graphicsView** attribute.

		:return: self.__graphicsView. ( QGraphicsView )
		"""

		return self.__graphicsView

	@graphicsView.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsView(self, value):
		"""
		This method is the setter method for **self.__graphicsView** attribute.

		:param value: Attribute value. ( QGraphicsView )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsView"))

	@graphicsView.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsView(self):
		"""
		This method is the deleter method for **self.__graphicsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsView"))

	@property
	def graphicsScene(self):
		"""
		This method is the property for **self.__graphicsScene** attribute.

		:return: self.__graphicsScene. ( QGraphicsScene )
		"""

		return self.__graphicsScene

	@graphicsScene.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsScene(self, value):
		"""
		This method is the setter method for **self.__graphicsScene** attribute.

		:param value: Attribute value. ( QGraphicsScene )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsScene"))

	@graphicsScene.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsScene(self):
		"""
		This method is the deleter method for **self.__graphicsScene** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsScene"))

	@property
	def displayGraphicsItem(self):
		"""
		This method is the property for **self.__displayGraphicsItem** attribute.

		:return: self.__displayGraphicsItem. ( QGraphicsItem )
		"""

		return self.__displayGraphicsItem

	@displayGraphicsItem.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self, value):
		"""
		This method is the setter method for **self.__displayGraphicsItem** attribute.

		:param value: Attribute value. ( QGraphicsItem )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "displayGraphicsItem"))

	@displayGraphicsItem.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self):
		"""
		This method is the deleter method for **self.__displayGraphicsItem** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "displayGraphicsItem"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def show(self):
		"""
		This method reimplements the :meth:`QWidget.show` method.
		"""

		super(ImagesPreviewer, self).show()

		foundations.ui.common.centerWidgetOnScreen(self)

	def closeEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.closeEvent` method.

		:param event: QEvent ( QEvent )
		"""

		LOGGER.debug("> Removing '{0}' from Images Previewers list.".format(self))
		self.__container.imagesPreviewers.remove(self)

		event.accept()

	def wheelEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.wheelEvent` method.

		:param event: QEvent ( QEvent )
		"""

		self.scaleView(pow(1.5, event.delta() / self.__wheelZoomFactor))

	def keyPressEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.keyPressEvent` method.

		:param event: QEvent ( QEvent )
		"""

		key = event.key()
		if key == Qt.Key_Plus:
			self.scaleView(self.__keyZoomFactor)
		elif key == Qt.Key_Minus:
			self.scaleView(1 / self.__keyZoomFactor)
		else:
			super(ImagesPreviewer, self).keyPressEvent(event)

	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		LOGGER.debug("> Initializing '{0}' ui.".format(self.__class__.__name__))

		self.Previous_Image_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiPreviousImage)))
		self.Next_Image_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiNextImage)))
		self.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiZoomInImage)))
		self.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiZoomOutImage)))
		len(self.__paths) <= 1 and self.Navigation_frame.hide()

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
		self.__graphicsScene.setSceneRect(-(float(self.__graphicsSceneWidth)) / 2,
										- (float(self.__graphicsSceneHeight)) / 2,
										float(self.__graphicsSceneWidth),
										float(self.__graphicsSceneHeight))

		self.__graphicsView.setScene(self.__graphicsScene)
		self.__graphicsView.setBackgroundBrush(QBrush(self.__graphicsSceneBackgroundColor))

		self.Images_Previewer_frame_gridLayout.addWidget(self.__graphicsView)

		# Signals / Slots.
		self.__container.engine.imagesCaches.QImage.contentAdded.connect(self.__engine_imagesCaches_QImage__contentAdded)
		self.Previous_Image_pushButton.clicked.connect(self.__Previous_Image_pushButton__clicked)
		self.Next_Image_pushButton.clicked.connect(self.__Next_Image_pushButton__clicked)
		self.Zoom_Out_pushButton.clicked.connect(self.__Zoom_Out_pushButton__clicked)
		self.Zoom_In_pushButton.clicked.connect(self.__Zoom_In_pushButton__clicked)
		self.Zoom_Fit_pushButton.clicked.connect(self.__Zoom_Fit_pushButton__clicked)

	def __Images_Informations_label_setUi(self):
		"""
		This method sets the **Images_Informations_label** Widget ui.
		"""

		if not self.__displayGraphicsItem:
			return

		image = self.__displayGraphicsItem.image
		self.Images_Informations_label.setText("{0} - {1}x{2} px - {3} bit".format(os.path.basename(image.data.path),
		 																		image.data.width,
																				image.data.height,
																				image.data.bpp / 4))

	def __engine_imagesCaches_QImage__contentAdded(self, content):
		"""
		This method is triggered by the Application **QImage** images cache when content has been added.

		:param content: Cache added content. ( List )
		"""

		if not self.__paths:
			return

		path = foundations.common.getFirstItem(content)
		if not path in self.__paths:
			return

		image = self.__container.engine.imagesCaches.QImage.getContent(path)
		self.__setDisplayGraphicsItem(image)

	def __Previous_Image_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Previous_Image_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughImages(True)

	def __Next_Image_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Next_Image_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughImages()

	def __Zoom_In_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Zoom_In_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.scaleView(self.__keyZoomFactor)

	def __Zoom_Out_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Zoom_Out_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.scaleView(1 / self.__keyZoomFactor)

	def __Zoom_Fit_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Zoom_Fit_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.fitImage()

	def __clearGraphicsScene(self):
		"""
		This method clears the View.
		"""

		for graphicsItem in self.__graphicsScene.items():
			self.__graphicsScene.removeItem(graphicsItem)

	def __setDisplayGraphicsItem(self, image):
		"""
		This method sets the View using given image.

		:param image: Image to display. ( Qimage )
		"""

		self.__clearGraphicsScene()

		LOGGER.debug("> Initializing graphics item.")
		self.__displayGraphicsItem = Image_QGraphicsItem(image=image)
		self.__graphicsScene.addItem(self.__displayGraphicsItem)

		self.__Images_Informations_label_setUi()

	def loadImage(self, index=0):
		"""
		This method loads the display image in the View.

		:param index: Index to load. ( Integer )
		:return: Method success. ( Boolean )
		"""

		if not self.__paths:
			return False

		image = sibl_gui.ui.common.getImage(self.__paths[index])
		self.__setDisplayGraphicsItem(image)

		return True

	def scaleView(self, scaleFactor):
		"""
		This method scales the Previewer view.

		:param scaleFactor: Float ( Float )
		:return: Method success. ( Boolean )
		"""

		graphicsView = self.findChild(QGraphicsView)
		factor = graphicsView.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
		if factor < self.__minimumZoomFactor or factor > self.__maximumZoomFactor:
			return False

		graphicsView.scale(scaleFactor, scaleFactor)
		return True

	def fitWindow(self):
		"""
		This method fits the View window.
		
		:return: Method success. ( Boolean )
		"""

		if not self.__displayGraphicsItem:
			return False

		desktopWidth = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).width()
		desktopHeight = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).height()
		width = min(desktopWidth * 0.80, self.__displayGraphicsItem.width)
		height = min(desktopHeight * 0.80, self.__displayGraphicsItem.height)
		self.resize(width, height)

		foundations.ui.common.centerWidgetOnScreen(self)

		return True

	def fitImage(self):
		"""
		This method fits the image to the View.
		
		:return: Method success. ( Boolean )
		"""

		if not self.__displayGraphicsItem:
			return False

		self.__graphicsView.fitInView(
		QRectF(-(self.__displayGraphicsItem.width / 2) - (self.__displayGraphicsItemMargin / 2),
				- (self.__displayGraphicsItem.height / 2) - (self.__displayGraphicsItemMargin / 2),
				self.__displayGraphicsItem.width + self.__displayGraphicsItemMargin,
				self.__displayGraphicsItem.height + self.__displayGraphicsItemMargin),
				Qt.KeepAspectRatio)
		return True

	def loopThroughImages(self, backward=False):
		"""
		This method loops through View images.

		:param backward: Looping backward. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		index = self.__paths.index(self.__displayGraphicsItem.image.data.path)
		index += not backward and 1 or -1
		if index < 0:
			index = len(self.__paths) - 1
		elif index > len(self.__paths) - 1:
			index = 0
		self.loadImage(index)
		return True

