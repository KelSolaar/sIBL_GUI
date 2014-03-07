#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preview.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Preview` Component Interface class, the :class:`ImagesPreviewer` class
	and others images preview related objects.

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines a `QGraphicsItem <http://doc.qt.nokia.com/qgraphicsitem.html>`_ subclass used
		to display given `QImage <http://doc.qt.nokia.com/qimage.html>`_.
	"""

	def __init__(self, parent=None, image=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param image: Image.
		:type image: QImage
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
		Property for **self.__image** attribute.

		:return: self.__image.
		:rtype: QImage
		"""

		return self.__image

	@image.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def image(self, value):
		"""
		Setter for **self.__image** attribute.

		:param value: Attribute value.
		:type value: QImage
		"""

		if value is not None:
			assert type(value) is QImage, "'{0}' attribute: '{1}' type is not 'QImage'!".format("image", value)
		self.__image = value

	@image.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def image(self):
		"""
		Deleter for **self.__image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "image"))

	@property
	def width(self):
		"""
		Property for **self.__width** attribute.

		:return: self.__width.
		:rtype: int
		"""

		return self.__width

	@width.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def width(self, value):
		"""
		Setter for **self.__width** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("width", value)
		self.__width = value

	@width.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def width(self):
		"""
		Deleter for **self.__width** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "width"))

	@property
	def height(self):
		"""
		Property for **self.__height** attribute.

		:return: self.__height.
		:rtype: int
		"""

		return self.__height

	@height.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def height(self, value):
		"""
		Setter for **self.__height** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("height", value)
		self.__height = value

	@height.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def height(self):
		"""
		Deleter for **self.__height** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "height"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def boundingRect(self):
		"""
		Reimplements the :meth:`QGraphicsItem.boundingRect` method.
		"""

		return QRectF(-(self.__image.width()) / 2,
					- (self.__image.height()) / 2,
					self.__image.width(),
					self.__image.height())

	def paint(self, painter, options, widget):
		"""
		Reimplements the :meth:`QGraphicsItem.paint` method.

		:param painter: QPainter
		:type painter: QPainter
		:param options: QStyleOptionGraphicsItem
		:type options: QStyleOptionGraphicsItem
		:param widget: QWidget
		:type widget: QWidget
		"""

		painter.drawImage(-(self.__image.width() / 2), -(self.__image.height() / 2), self.__image)

class ImagesPreviewer(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	| Defines the Application images previewer.
	| It defines methods to navigate through the list of given images ( List of images paths ),
		zoom in / out and fit the displayed image, etc...
	"""

	def __init__(self, parent, paths=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param paths: Images paths.
		:type paths: tuple or list
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
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
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def paths(self):
		"""
		Property for **self.__paths** attribute.

		:return: self.__paths.
		:rtype: tuple or list
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def paths(self, value):
		"""
		Setter for **self.__paths** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format("paths", value)
			for element in value:
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"paths", element)
		self.__paths = value

	@paths.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		Deleter for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "paths"))

	@property
	def uiResourcesDirectory(self):
		"""
		Property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory.
		:rtype: unicode
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		Setter for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		Deleter for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiPreviousImage(self):
		"""
		Property for **self.__uiPreviousImage** attribute.

		:return: self.__uiPreviousImage.
		:rtype: unicode
		"""

		return self.__uiPreviousImage

	@uiPreviousImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self, value):
		"""
		Setter for **self.__uiPreviousImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self):
		"""
		Deleter for **self.__uiPreviousImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiPreviousImage"))

	@property
	def uiNextImage(self):
		"""
		Property for **self.__uiNextImage** attribute.

		:return: self.__uiNextImage.
		:rtype: unicode
		"""

		return self.__uiNextImage

	@uiNextImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiNextImage(self, value):
		"""
		Setter for **self.__uiNextImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiNextImage(self):
		"""
		Deleter for **self.__uiNextImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiNextImage"))

	@property
	def uiZoomOutImage(self):
		"""
		Property for **self.__uiZoomOutImage** attribute.

		:return: self.__uiZoomOutImage.
		:rtype: unicode
		"""

		return self.__uiZoomOutImage

	@uiZoomOutImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self, value):
		"""
		Setter for **self.__uiZoomOutImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomOutImage"))

	@uiZoomOutImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomOutImage(self):
		"""
		Deleter for **self.__uiZoomOutImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomOutImage"))

	@property
	def uiZoomInImage(self):
		"""
		Property for **self.__uiZoomInImage** attribute.

		:return: self.__uiZoomInImage.
		:rtype: unicode
		"""

		return self.__uiZoomInImage

	@uiZoomInImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self, value):
		"""
		Setter for **self.__uiZoomInImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiZoomInImage"))

	@uiZoomInImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiZoomInImage(self):
		"""
		Deleter for **self.__uiZoomInImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiZoomInImage"))

	@property
	def graphicsSceneBackgroundColor(self):
		"""
		Property for **self.__graphicsSceneBackgroundColor** attribute.

		:return: self.__graphicsSceneBackgroundColor.
		:rtype: QColor
		"""

		return self.__graphicsSceneBackgroundColor

	@graphicsSceneBackgroundColor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self, value):
		"""
		Setter for **self.__graphicsSceneBackgroundColor** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsSceneBackgroundColor"))

	@graphicsSceneBackgroundColor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneBackgroundColor(self):
		"""
		Deleter for **self.__graphicsSceneBackgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsSceneBackgroundColor"))

	@property
	def graphicsSceneWidth(self):
		"""
		Property for **self.__graphicsSceneWidth** attribute.

		:return: self.__graphicsSceneWidth.
		:rtype: int
		"""

		return self.__graphicsSceneWidth

	@graphicsSceneWidth.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self, value):
		"""
		Setter for **self.__graphicsSceneWidth** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsSceneWidth"))

	@graphicsSceneWidth.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneWidth(self):
		"""
		Deleter for **self.__graphicsSceneWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsSceneWidth"))

	@property
	def graphicsSceneHeight(self):
		"""
		Property for **self.__graphicsSceneHeight** attribute.

		:return: self.__graphicsSceneHeight.
		:rtype: object
		"""

		return self.__graphicsSceneHeight

	@graphicsSceneHeight.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self, value):
		"""
		Setter for **self.__graphicsSceneHeight** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsSceneHeight"))

	@graphicsSceneHeight.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsSceneHeight(self):
		"""
		Deleter for **self.__graphicsSceneHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsSceneHeight"))

	@property
	def minimumZoomFactor(self):
		"""
		Property for **self.__minimumZoomFactor** attribute.

		:return: self.__minimumZoomFactor.
		:rtype: float
		"""

		return self.__minimumZoomFactor

	@minimumZoomFactor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self, value):
		"""
		Setter for **self.__minimumZoomFactor** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "minimumZoomFactor"))

	@minimumZoomFactor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def minimumZoomFactor(self):
		"""
		Deleter for **self.__minimumZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "minimumZoomFactor"))

	@property
	def maximumZoomFactor(self):
		"""
		Property for **self.__maximumZoomFactor** attribute.

		:return: self.__maximumZoomFactor.
		:rtype: float
		"""

		return self.__maximumZoomFactor

	@maximumZoomFactor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self, value):
		"""
		Setter for **self.__maximumZoomFactor** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximumZoomFactor"))

	@maximumZoomFactor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumZoomFactor(self):
		"""
		Deleter for **self.__maximumZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumZoomFactor"))

	@property
	def wheelZoomFactor(self):
		"""
		Property for **self.__wheelZoomFactor** attribute.

		:return: self.__wheelZoomFactor.
		:rtype: float
		"""

		return self.__wheelZoomFactor

	@wheelZoomFactor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self, value):
		"""
		Setter for **self.__wheelZoomFactor** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "wheelZoomFactor"))

	@wheelZoomFactor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def wheelZoomFactor(self):
		"""
		Deleter for **self.__wheelZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "wheelZoomFactor"))

	@property
	def keyZoomFactor(self):
		"""
		Property for **self.__keyZoomFactor** attribute.

		:return: self.__keyZoomFactor.
		:rtype: float
		"""

		return self.__keyZoomFactor

	@keyZoomFactor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self, value):
		"""
		Setter for **self.__keyZoomFactor** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "keyZoomFactor"))

	@keyZoomFactor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def keyZoomFactor(self):
		"""
		Deleter for **self.__keyZoomFactor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "keyZoomFactor"))

	@property
	def graphicsView(self):
		"""
		Property for **self.__graphicsView** attribute.

		:return: self.__graphicsView.
		:rtype: QGraphicsView
		"""

		return self.__graphicsView

	@graphicsView.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsView(self, value):
		"""
		Setter for **self.__graphicsView** attribute.

		:param value: Attribute value.
		:type value: QGraphicsView
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsView"))

	@graphicsView.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsView(self):
		"""
		Deleter for **self.__graphicsView** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsView"))

	@property
	def graphicsScene(self):
		"""
		Property for **self.__graphicsScene** attribute.

		:return: self.__graphicsScene.
		:rtype: QGraphicsScene
		"""

		return self.__graphicsScene

	@graphicsScene.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsScene(self, value):
		"""
		Setter for **self.__graphicsScene** attribute.

		:param value: Attribute value.
		:type value: QGraphicsScene
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphicsScene"))

	@graphicsScene.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def graphicsScene(self):
		"""
		Deleter for **self.__graphicsScene** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphicsScene"))

	@property
	def displayGraphicsItem(self):
		"""
		Property for **self.__displayGraphicsItem** attribute.

		:return: self.__displayGraphicsItem.
		:rtype: QGraphicsItem
		"""

		return self.__displayGraphicsItem

	@displayGraphicsItem.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self, value):
		"""
		Setter for **self.__displayGraphicsItem** attribute.

		:param value: Attribute value.
		:type value: QGraphicsItem
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "displayGraphicsItem"))

	@displayGraphicsItem.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def displayGraphicsItem(self):
		"""
		Deleter for **self.__displayGraphicsItem** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "displayGraphicsItem"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def show(self):
		"""
		Reimplements the :meth:`QWidget.show` method.
		"""

		super(ImagesPreviewer, self).show()

		foundations.ui.common.centerWidgetOnScreen(self)

	def closeEvent(self, event):
		"""
		Reimplements the :meth:`QWidget.closeEvent` method.

		:param event: QEvent
		:type event: QEvent
		"""

		LOGGER.debug("> Removing '{0}' from Images Previewers list.".format(self))
		self.__container.imagesPreviewers.remove(self)

		event.accept()

	def wheelEvent(self, event):
		"""
		Reimplements the :meth:`QWidget.wheelEvent` method.

		:param event: QEvent
		:type event: QEvent
		"""

		self.scaleView(pow(1.5, event.delta() / self.__wheelZoomFactor))

	def keyPressEvent(self, event):
		"""
		Reimplements the :meth:`QWidget.keyPressEvent` method.

		:param event: QEvent
		:type event: QEvent
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
		Initializes the Widget ui.
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
		Sets the **Images_Informations_label** Widget ui.
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
		Defines the slot triggered by Application **QImage** images cache when content has been added.

		:param content: Cache added content.
		:type content: list
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
		Defines the slot triggered by **Previous_Image_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loopThroughImages(True)

	def __Next_Image_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Next_Image_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loopThroughImages()

	def __Zoom_In_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Zoom_In_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.scaleView(self.__keyZoomFactor)

	def __Zoom_Out_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Zoom_Out_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.scaleView(1 / self.__keyZoomFactor)

	def __Zoom_Fit_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Zoom_Fit_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.fitImage()

	def __clearGraphicsScene(self):
		"""
		Clears the View.
		"""

		for graphicsItem in self.__graphicsScene.items():
			self.__graphicsScene.removeItem(graphicsItem)

	def __setDisplayGraphicsItem(self, image):
		"""
		Sets the View using given image.

		:param image: Image to display.
		:type image: QImage
		"""

		self.__clearGraphicsScene()

		LOGGER.debug("> Initializing graphics item.")
		self.__displayGraphicsItem = Image_QGraphicsItem(image=image)
		self.__graphicsScene.addItem(self.__displayGraphicsItem)

		self.__Images_Informations_label_setUi()

	def loadImage(self, index=0):
		"""
		Loads the display image in the View.

		:param index: Index to load.
		:type index: int
		:return: Method success.
		:rtype: bool
		"""

		if not self.__paths:
			return False

		image = sibl_gui.ui.common.getImage(self.__paths[index])
		self.__setDisplayGraphicsItem(image)

		return True

	def scaleView(self, scaleFactor):
		"""
		Scales the Previewer view.

		:param scaleFactor: Float
		:type scaleFactor: float
		:return: Method success.
		:rtype: bool
		"""

		graphicsView = self.findChild(QGraphicsView)
		factor = graphicsView.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
		if factor < self.__minimumZoomFactor or factor > self.__maximumZoomFactor:
			return False

		graphicsView.scale(scaleFactor, scaleFactor)
		return True

	def fitWindow(self):
		"""
		Fits the View window.
		
		:return: Method success.
		:rtype: bool
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
		Fits the image to the View.
		
		:return: Method success.
		:rtype: bool
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
		Loops through View images.

		:param backward: Looping backward.
		:type backward: bool
		:return: Method success.
		:rtype: bool
		"""

		index = self.__paths.index(self.__displayGraphicsItem.image.data.path)
		index += not backward and 1 or -1
		if index < 0:
			index = len(self.__paths) - 1
		elif index > len(self.__paths) - 1:
			index = 0
		self.loadImage(index)
		return True

