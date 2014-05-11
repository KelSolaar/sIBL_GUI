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

from __future__ import unicode_literals

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

import foundations.common
import foundations.exceptions
import foundations.ui.common
import foundations.verbose
import sibl_gui.ui.common

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Image_QGraphicsItem", "ImagesPreviewer"]

LOGGER = foundations.verbose.install_logger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Images_Previewer.ui")

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

    @property
    def image(self):
        """
        Property for **self.__image** attribute.

        :return: self.__image.
        :rtype: QImage
        """

        return self.__image

    @image.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
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
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
    @foundations.exceptions.handle_exceptions(AssertionError)
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
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
    @foundations.exceptions.handle_exceptions(AssertionError)
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
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def height(self):
        """
        Deleter for **self.__height** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "height"))

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

class ImagesPreviewer(foundations.ui.common.QWidget_factory(ui_file=UI_FILE)):
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

        self.__ui_resources_directory = "resources"
        self.__ui_resources_directory = os.path.join(os.path.dirname(__file__), self.__ui_resources_directory)
        self.__ui_previous_image = "Previous.png"
        self.__ui_next_image = "Next.png"
        self.__ui_zoom_out_image = "Zoom_Out.png"
        self.__ui_zoom_in_image = "Zoom_In.png"

        # Ensure the ui object is destroyed on close to avoid memory leaks.
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.__graphics_scene_background_color = QColor(32, 32, 32)
        self.__minimum_zoom_factor = 0.05
        self.__maximum_zoom_factor = 25
        self.__display_graphics_item_margin = 32
        self.__graphics_sceneWidth = QApplication.desktop().screenGeometry(
                                QApplication.desktop().primaryScreen()).width() * (1 / self.__minimum_zoom_factor * 1.75)
        self.__graphics_sceneHeight = QApplication.desktop().screenGeometry(
                                QApplication.desktop().primaryScreen()).height() * (1 / self.__minimum_zoom_factor * 1.75)
        self.__wheel_zoom_factor = 350.0
        self.__key_zoom_factor = 1.20

        self.__graphics_view = None
        self.__graphics_scene = None
        self.__display_graphics_item = None

        ImagesPreviewer.__initialize_ui(self)

        self.load_image()

    @property
    def container(self):
        """
        Property for **self.__container** attribute.

        :return: self.__container.
        :rtype: QObject
        """

        return self.__container

    @container.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def container(self, value):
        """
        Setter for **self.__container** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

    @container.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
    @foundations.exceptions.handle_exceptions(AssertionError)
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
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def paths(self):
        """
        Deleter for **self.__paths** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "paths"))

    @property
    def ui_resources_directory(self):
        """
        Property for **self.__ui_resources_directory** attribute.

        :return: self.__ui_resources_directory.
        :rtype: unicode
        """

        return self.__ui_resources_directory

    @ui_resources_directory.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_resources_directory(self, value):
        """
        Setter for **self.__ui_resources_directory** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_resources_directory"))

    @ui_resources_directory.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_resources_directory(self):
        """
        Deleter for **self.__ui_resources_directory** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_resources_directory"))

    @property
    def ui_previous_image(self):
        """
        Property for **self.__ui_previous_image** attribute.

        :return: self.__ui_previous_image.
        :rtype: unicode
        """

        return self.__ui_previous_image

    @ui_previous_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_previous_image(self, value):
        """
        Setter for **self.__ui_previous_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_previous_image"))

    @ui_previous_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_previous_image(self):
        """
        Deleter for **self.__ui_previous_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_previous_image"))

    @property
    def ui_next_image(self):
        """
        Property for **self.__ui_next_image** attribute.

        :return: self.__ui_next_image.
        :rtype: unicode
        """

        return self.__ui_next_image

    @ui_next_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_next_image(self, value):
        """
        Setter for **self.__ui_next_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_next_image"))

    @ui_next_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_next_image(self):
        """
        Deleter for **self.__ui_next_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_next_image"))

    @property
    def ui_zoom_out_image(self):
        """
        Property for **self.__ui_zoom_out_image** attribute.

        :return: self.__ui_zoom_out_image.
        :rtype: unicode
        """

        return self.__ui_zoom_out_image

    @ui_zoom_out_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_zoom_out_image(self, value):
        """
        Setter for **self.__ui_zoom_out_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_zoom_out_image"))

    @ui_zoom_out_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_zoom_out_image(self):
        """
        Deleter for **self.__ui_zoom_out_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_zoom_out_image"))

    @property
    def ui_zoom_in_image(self):
        """
        Property for **self.__ui_zoom_in_image** attribute.

        :return: self.__ui_zoom_in_image.
        :rtype: unicode
        """

        return self.__ui_zoom_in_image

    @ui_zoom_in_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_zoom_in_image(self, value):
        """
        Setter for **self.__ui_zoom_in_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_zoom_in_image"))

    @ui_zoom_in_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_zoom_in_image(self):
        """
        Deleter for **self.__ui_zoom_in_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_zoom_in_image"))

    @property
    def graphics_scene_background_color(self):
        """
        Property for **self.__graphics_scene_background_color** attribute.

        :return: self.__graphics_scene_background_color.
        :rtype: QColor
        """

        return self.__graphics_scene_background_color

    @graphics_scene_background_color.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_scene_background_color(self, value):
        """
        Setter for **self.__graphics_scene_background_color** attribute.

        :param value: Attribute value.
        :type value: QColor
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphics_scene_background_color"))

    @graphics_scene_background_color.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_scene_background_color(self):
        """
        Deleter for **self.__graphics_scene_background_color** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphics_scene_background_color"))

    @property
    def graphics_sceneWidth(self):
        """
        Property for **self.__graphics_sceneWidth** attribute.

        :return: self.__graphics_sceneWidth.
        :rtype: int
        """

        return self.__graphics_sceneWidth

    @graphics_sceneWidth.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_sceneWidth(self, value):
        """
        Setter for **self.__graphics_sceneWidth** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphics_sceneWidth"))

    @graphics_sceneWidth.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_sceneWidth(self):
        """
        Deleter for **self.__graphics_sceneWidth** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphics_sceneWidth"))

    @property
    def graphics_sceneHeight(self):
        """
        Property for **self.__graphics_sceneHeight** attribute.

        :return: self.__graphics_sceneHeight.
        :rtype: object
        """

        return self.__graphics_sceneHeight

    @graphics_sceneHeight.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_sceneHeight(self, value):
        """
        Setter for **self.__graphics_sceneHeight** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphics_sceneHeight"))

    @graphics_sceneHeight.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_sceneHeight(self):
        """
        Deleter for **self.__graphics_sceneHeight** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphics_sceneHeight"))

    @property
    def minimum_zoom_factor(self):
        """
        Property for **self.__minimum_zoom_factor** attribute.

        :return: self.__minimum_zoom_factor.
        :rtype: float
        """

        return self.__minimum_zoom_factor

    @minimum_zoom_factor.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def minimum_zoom_factor(self, value):
        """
        Setter for **self.__minimum_zoom_factor** attribute.

        :param value: Attribute value.
        :type value: float
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "minimum_zoom_factor"))

    @minimum_zoom_factor.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def minimum_zoom_factor(self):
        """
        Deleter for **self.__minimum_zoom_factor** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "minimum_zoom_factor"))

    @property
    def maximum_zoom_factor(self):
        """
        Property for **self.__maximum_zoom_factor** attribute.

        :return: self.__maximum_zoom_factor.
        :rtype: float
        """

        return self.__maximum_zoom_factor

    @maximum_zoom_factor.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def maximum_zoom_factor(self, value):
        """
        Setter for **self.__maximum_zoom_factor** attribute.

        :param value: Attribute value.
        :type value: float
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximum_zoom_factor"))

    @maximum_zoom_factor.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def maximum_zoom_factor(self):
        """
        Deleter for **self.__maximum_zoom_factor** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximum_zoom_factor"))

    @property
    def wheel_zoom_factor(self):
        """
        Property for **self.__wheel_zoom_factor** attribute.

        :return: self.__wheel_zoom_factor.
        :rtype: float
        """

        return self.__wheel_zoom_factor

    @wheel_zoom_factor.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def wheel_zoom_factor(self, value):
        """
        Setter for **self.__wheel_zoom_factor** attribute.

        :param value: Attribute value.
        :type value: float
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "wheel_zoom_factor"))

    @wheel_zoom_factor.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def wheel_zoom_factor(self):
        """
        Deleter for **self.__wheel_zoom_factor** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "wheel_zoom_factor"))

    @property
    def key_zoom_factor(self):
        """
        Property for **self.__key_zoom_factor** attribute.

        :return: self.__key_zoom_factor.
        :rtype: float
        """

        return self.__key_zoom_factor

    @key_zoom_factor.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def key_zoom_factor(self, value):
        """
        Setter for **self.__key_zoom_factor** attribute.

        :param value: Attribute value.
        :type value: float
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "key_zoom_factor"))

    @key_zoom_factor.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def key_zoom_factor(self):
        """
        Deleter for **self.__key_zoom_factor** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "key_zoom_factor"))

    @property
    def graphics_view(self):
        """
        Property for **self.__graphics_view** attribute.

        :return: self.__graphics_view.
        :rtype: QGraphicsView
        """

        return self.__graphics_view

    @graphics_view.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_view(self, value):
        """
        Setter for **self.__graphics_view** attribute.

        :param value: Attribute value.
        :type value: QGraphicsView
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphics_view"))

    @graphics_view.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_view(self):
        """
        Deleter for **self.__graphics_view** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphics_view"))

    @property
    def graphics_scene(self):
        """
        Property for **self.__graphics_scene** attribute.

        :return: self.__graphics_scene.
        :rtype: QGraphicsScene
        """

        return self.__graphics_scene

    @graphics_scene.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_scene(self, value):
        """
        Setter for **self.__graphics_scene** attribute.

        :param value: Attribute value.
        :type value: QGraphicsScene
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "graphics_scene"))

    @graphics_scene.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def graphics_scene(self):
        """
        Deleter for **self.__graphics_scene** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "graphics_scene"))

    @property
    def display_graphics_item(self):
        """
        Property for **self.__display_graphics_item** attribute.

        :return: self.__display_graphics_item.
        :rtype: QGraphicsItem
        """

        return self.__display_graphics_item

    @display_graphics_item.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def display_graphics_item(self, value):
        """
        Setter for **self.__display_graphics_item** attribute.

        :param value: Attribute value.
        :type value: QGraphicsItem
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "display_graphics_item"))

    @display_graphics_item.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def display_graphics_item(self):
        """
        Deleter for **self.__display_graphics_item** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "display_graphics_item"))

    def show(self):
        """
        Reimplements the :meth:`QWidget.show` method.
        """

        super(ImagesPreviewer, self).show()

        foundations.ui.common.center_widget_on_screen(self)

    def closeEvent(self, event):
        """
        Reimplements the :meth:`QWidget.closeEvent` method.

        :param event: QEvent
        :type event: QEvent
        """

        LOGGER.debug("> Removing '{0}' from Images Previewers list.".format(self))
        self.__container.images_previewers.remove(self)

        event.accept()

    def wheelEvent(self, event):
        """
        Reimplements the :meth:`QWidget.wheelEvent` method.

        :param event: QEvent
        :type event: QEvent
        """

        self.scale_view(pow(1.5, event.delta() / self.__wheel_zoom_factor))

    def keyPressEvent(self, event):
        """
        Reimplements the :meth:`QWidget.keyPressEvent` method.

        :param event: QEvent
        :type event: QEvent
        """

        key = event.key()
        if key == Qt.Key_Plus:
            self.scale_view(self.__key_zoom_factor)
        elif key == Qt.Key_Minus:
            self.scale_view(1 / self.__key_zoom_factor)
        elif key == Qt.Key_F:
            self.fit_image()
        else:
            super(ImagesPreviewer, self).keyPressEvent(event)

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        LOGGER.debug("> Initializing '{0}' ui.".format(self.__class__.__name__))

        self.Previous_Image_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_previous_image)))
        self.Next_Image_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_next_image)))
        self.Zoom_In_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_zoom_in_image)))
        self.Zoom_Out_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_zoom_out_image)))
        len(self.__paths) <= 1 and self.Navigation_frame.hide()

        LOGGER.debug("> Initializing graphics View.")
        self.__graphics_view = QGraphicsView()
        self.__graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__graphics_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.__graphics_view.setDragMode(QGraphicsView.ScrollHandDrag)
        # Reimplementing QGraphicsView wheelEvent method.
        self.__graphics_view.wheelEvent = self.wheelEvent

        LOGGER.debug("> Initializing graphics scene.")
        self.__graphics_scene = QGraphicsScene(self.__graphics_view)
        self.__graphics_scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.__graphics_scene.setSceneRect(-(float(self.__graphics_sceneWidth)) / 2,
                                        - (float(self.__graphics_sceneHeight)) / 2,
                                        float(self.__graphics_sceneWidth),
                                        float(self.__graphics_sceneHeight))

        self.__graphics_view.setScene(self.__graphics_scene)
        self.__graphics_view.setBackgroundBrush(QBrush(self.__graphics_scene_background_color))

        self.Images_Previewer_frame_gridLayout.addWidget(self.__graphics_view)

        # Signals / Slots.
        self.__container.engine.images_caches.QImage.content_added.connect(self.__engine_images_caches_QImage__content_added)
        self.Previous_Image_pushButton.clicked.connect(self.__Previous_Image_pushButton__clicked)
        self.Next_Image_pushButton.clicked.connect(self.__Next_Image_pushButton__clicked)
        self.Zoom_Out_pushButton.clicked.connect(self.__Zoom_Out_pushButton__clicked)
        self.Zoom_In_pushButton.clicked.connect(self.__Zoom_In_pushButton__clicked)
        self.Zoom_Fit_pushButton.clicked.connect(self.__Zoom_Fit_pushButton__clicked)

    def __Images_Informations_label_set_ui(self):
        """
        Sets the **Images_Informations_label** Widget ui.
        """

        if not self.__display_graphics_item:
            return

        image = self.__display_graphics_item.image
        self.Images_Informations_label.setText("{0} - {1}x{2} px - {3} bit".format(os.path.basename(image.data.path),
                                                                                image.data.width,
                                                                                image.data.height,
                                                                                image.data.bpp / 4))

    def __engine_images_caches_QImage__content_added(self, content):
        """
        Defines the slot triggered by Application **QImage** images cache when content has been added.

        :param content: Cache added content.
        :type content: list
        """

        if not self.__paths:
            return

        path = foundations.common.get_first_item(content)
        if not path in self.__paths:
            return

        image = self.__container.engine.images_caches.QImage.get_content(path)
        self.__set_display_graphics_item(image)

    def __Previous_Image_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Previous_Image_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.loop_through_images(True)

    def __Next_Image_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Next_Image_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.loop_through_images()

    def __Zoom_In_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Zoom_In_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.scale_view(self.__key_zoom_factor)

    def __Zoom_Out_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Zoom_Out_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.scale_view(1 / self.__key_zoom_factor)

    def __Zoom_Fit_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Zoom_Fit_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.fit_image()

    def __clear_graphics_scene(self):
        """
        Clears the View.
        """

        for graphics_item in self.__graphics_scene.items():
            self.__graphics_scene.removeItem(graphics_item)

    def __set_display_graphics_item(self, image):
        """
        Sets the View using given image.

        :param image: Image to display.
        :type image: QImage
        """

        self.__clear_graphics_scene()

        LOGGER.debug("> Initializing graphics item.")
        self.__display_graphics_item = Image_QGraphicsItem(image=image)
        self.__graphics_scene.addItem(self.__display_graphics_item)

        self.__Images_Informations_label_set_ui()

    def load_image(self, index=0):
        """
        Loads the display image in the View.

        :param index: Index to load.
        :type index: int
        :return: Method success.
        :rtype: bool
        """

        if not self.__paths:
            return False

        image = sibl_gui.ui.common.get_image(self.__paths[index])
        self.__set_display_graphics_item(image)

        return True

    def scale_view(self, scale_factor):
        """
        Scales the Previewer view.

        :param scale_factor: Float
        :type scale_factor: float
        :return: Method success.
        :rtype: bool
        """

        graphics_view = self.findChild(QGraphicsView)
        factor = graphics_view.matrix().scale(scale_factor, scale_factor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < self.__minimum_zoom_factor or factor > self.__maximum_zoom_factor:
            return False

        graphics_view.scale(scale_factor, scale_factor)
        return True

    def fit_window(self):
        """
        Fits the View window.

        :return: Method success.
        :rtype: bool
        """

        if not self.__display_graphics_item:
            return False

        desktop_width = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).width()
        desktop_height = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).height()
        width = min(desktop_width * 0.80, self.__display_graphics_item.width)
        height = min(desktop_height * 0.80, self.__display_graphics_item.height)
        self.resize(width, height)

        foundations.ui.common.center_widget_on_screen(self)

        return True

    def fit_image(self):
        """
        Fits the image to the View.

        :return: Method success.
        :rtype: bool
        """

        if not self.__display_graphics_item:
            return False

        self.__graphics_view.fitInView(
        QRectF(-(self.__display_graphics_item.width / 2) - (self.__display_graphics_item_margin / 2),
                - (self.__display_graphics_item.height / 2) - (self.__display_graphics_item_margin / 2),
                self.__display_graphics_item.width + self.__display_graphics_item_margin,
                self.__display_graphics_item.height + self.__display_graphics_item_margin),
                Qt.KeepAspectRatio)
        return True

    def loop_through_images(self, backward=False):
        """
        Loops through View images.

        :param backward: Looping backward.
        :type backward: bool
        :return: Method success.
        :rtype: bool
        """

        index = self.__paths.index(self.__display_graphics_item.image.data.path)
        index += not backward and 1 or -1
        if index < 0:
            index = len(self.__paths) - 1
        elif index > len(self.__paths) - 1:
            index = 0
        self.load_image(index)
        return True
