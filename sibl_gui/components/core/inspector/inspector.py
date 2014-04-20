#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**inspector.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Inspector` Component Interface class and others helpers objects.

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
import re
import sys

if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPen

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.cache
import foundations.common
import foundations.data_structures
import foundations.exceptions
import foundations.strings
import foundations.verbose
import sibl_gui.ui.common
import umbra.ui.nodes
from foundations.parsers import SectionsFileParser
from manager.QWidget_component import QWidgetComponentFactory
from sibl_gui.components.core.database.nodes import IblSetNode
from sibl_gui.components.core.inspector.models import PlatesModel
from sibl_gui.components.core.inspector.nodes import PlatesNode
from sibl_gui.components.core.inspector.views import Plates_QListView
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Plate", "Light", "Inspector"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Inspector.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Plate(foundations.data_structures.Structure):
	"""
	Defines a storage object for an Ibl Set Plate.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: name, icon, preview_image, image
		:type kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.data_structures.Structure.__init__(self, **kwargs)

class Light(foundations.data_structures.Structure):
	"""
	Defines a storage object for an Ibl Set light.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: name, color, u_coordinate, v_coordinate
		:type kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.data_structures.Structure.__init__(self, **kwargs)

class Inspector(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.core.inspector.inspector` Component Interface class.
	| It offers a large preview of the current inspected Ibl Set, and a way to navigate
		into the current selected Database Collection.
	"""

	# Custom signals definitions.
	refresh_nodes = pyqtSignal()
	"""
	This signal is emited by the :class:`Inspector` class when :obj:`Inspector.model` class property model
	nodes needs to be refreshed.
	"""

	ui_refresh = pyqtSignal()
	"""
	This signal is emited by the :class:`Inspector` class when the Ui needs to be refreshed.
	"""

	ui_clear = pyqtSignal()
	"""
	This signal is emited by the :class:`Inspector` class when the Ui needs to be cleared.
	"""

	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param name: Component name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(Inspector, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__ui_resources_directory = "resources"
		self.__ui_previous_image = "Previous.png"
		self.__ui_next_image = "Next.png"
		self.__ui_loading_image = "Loading.png"
		self.__dock_area = 2
		self.__list_view_icon_size = 30

		self.__engine = None
		self.__settings = None
		self.__settings_section = None

		self.__preferences_manager = None
		self.__ibl_sets_outliner = None

		self.__sections_file_parsers_cache = None

		self.__model = None
		self.__view = None

		self.__thumbnails_size = "Special1"

		self.__active_ibl_set = None
		self.__inspector_plates = None

		self.__no_preview_image_text = """
								<center>
								<table border="0" bordercolor="" cellpadding="0" cellspacing="16">
									<tr>
										<td>
											<img src="{0}">
										</td>
										<td>
											<p><b>Preview Image is unavailable!<b></p>
											What now?
											<ul>
												<li>Check For an updated set on <b>HDRLabs</b> at
												<a href="http://www.hdrlabs.com/sibl/archive.html">
												<span style="text-decoration: underline; color:#e0e0e0;">
												http://www.hdrlabs.com/sibl/archive.html</span></a>.</li>
												<li>Contact <b>{1}</b> for an updated Ibl Set: <a href="{2}">
												<span style="text-decoration: underline; color:#e0e0e0;">{2}</span>
												</a></li>
												<li>Resize the background image to 600x300 pixels.<br/>
												Save it as a jpeg in your set directory.<br/>
												Register it in the ."ibl" file header using the "PREVIEWfile" attribute.
												</li>
											</ul>
										</td>
									</tr>
								</table>
								</center>
								"""
		self.__no_active_ibl_set_text = """
								<center>
								<table border="0" bordercolor="" cellpadding="0" cellspacing="16">
									<tr>
										<td>
											<img src="{0}">
										</td>
										<td>
											<p><b>No Ibl Set to inspect!<b></p>
											Please add some Ibl Set to the Database or select a non empty Collection!
										</td>
									</tr>
								</table>
								</center>
								"""
		self.__active_ibl_set_tool_tip_text = """
								<p><b>{0}</b></p>
								<p><b>Author: </b>{1}<br>
								<b>Location: </b>{2}<br>
								<b>Shot Date: </b>{3}<br>
								<b>Comment: </b>{4}</p>
								"""

		self.__light_label_radius = 4
		self.__light_label_text_offset = 24
		self.__light_label_text_margin = 16
		self.__light_label_text_height = 14
		self.__light_label_text_font = "Helvetica"
		self.__unnamed_light_name = "Unnamed_Light"

		self.__pixmap_placeholder = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
	def ui_loading_image(self):
		"""
		Property for **self.__ui_loading_image** attribute.

		:return: self.__ui_loading_image.
		:rtype: unicode
		"""

		return self.__ui_loading_image

	@ui_loading_image.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_loading_image(self, value):
		"""
		Setter for **self.__ui_loading_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_loading_image"))

	@ui_loading_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_loading_image(self):
		"""
		Deleter for **self.__ui_loading_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_loading_image"))

	@property
	def dock_area(self):
		"""
		Property for **self.__dock_area** attribute.

		:return: self.__dock_area.
		:rtype: int
		"""

		return self.__dock_area

	@dock_area.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def dock_area(self, value):
		"""
		Setter for **self.__dock_area** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dock_area"))

	@dock_area.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def dock_area(self):
		"""
		Deleter for **self.__dock_area** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dock_area"))

	@property
	def list_view_icon_size(self):
		"""
		Property for **self.__list_view_icon_size** attribute.

		:return: self.__list_view_icon_size.
		:rtype: int
		"""

		return self.__list_view_icon_size

	@list_view_icon_size.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def list_view_icon_size(self, value):
		"""
		Setter for **self.__list_view_icon_size** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("list_view_icon_size", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("list_view_icon_size", value)
		self.__list_view_icon_size = value

	@list_view_icon_size.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def list_view_icon_size(self):
		"""
		Deleter for **self.__list_view_icon_size** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "list_view_icon_size"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def ibl_sets_outliner(self):
		"""
		Property for **self.__ibl_sets_outliner** attribute.

		:return: self.__ibl_sets_outliner.
		:rtype: QWidget
		"""

		return self.__ibl_sets_outliner

	@ibl_sets_outliner.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_outliner(self, value):
		"""
		Setter for **self.__ibl_sets_outliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ibl_sets_outliner"))

	@ibl_sets_outliner.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_outliner(self):
		"""
		Deleter for **self.__ibl_sets_outliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ibl_sets_outliner"))

	@property
	def sections_file_parsers_cache(self):
		"""
		Property for **self.__sections_file_parsers_cache** attribute.

		:return: self.__sections_file_parsers_cache.
		:rtype: Cache
		"""

		return self.__sections_file_parsers_cache

	@sections_file_parsers_cache.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def sections_file_parsers_cache(self, value):
		"""
		Setter for **self.__sections_file_parsers_cache** attribute.

		:param value: Attribute value.
		:type value: Cache
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "sections_file_parsers_cache"))

	@sections_file_parsers_cache.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def sections_file_parsers_cache(self):
		"""
		Deleter for **self.__sections_file_parsers_cache** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "sections_file_parsers_cache"))

	@property
	def model(self):
		"""
		Property for **self.__model** attribute.

		:return: self.__model.
		:rtype: PlatesModel
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		Setter for **self.__model** attribute.

		:param value: Attribute value.
		:type value: PlatesModel
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		Deleter for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def view(self):
		"""
		Property for **self.__view** attribute.

		:return: self.__view.
		:rtype: QWidget
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		Setter for **self.__view** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		Deleter for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def thumbnails_size(self):
		"""
		Property for **self.__thumbnails_size** attribute.

		:return: self.__thumbnails_size.
		:rtype: unicode
		"""

		return self.__thumbnails_size

	@thumbnails_size.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def thumbnails_size(self, value):
		"""
		Setter for **self.__thumbnails_size** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("thumbnails_size",
																								  value)
		self.__thumbnails_size = value

	@thumbnails_size.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def thumbnails_size(self):
		"""
		Deleter for **self.__thumbnails_size** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "thumbnails_size"))

	@property
	def active_ibl_set(self):
		"""
		Property for **self.__active_ibl_set** attribute.

		:return: self.__active_ibl_set.
		:rtype: IblSet
		"""

		return self.__active_ibl_set

	@active_ibl_set.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def active_ibl_set(self, value):
		"""
		Setter for **self.__active_ibl_set** attribute.

		:param value: Attribute value.
		:type value: IblSet
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "active_ibl_set"))

	@active_ibl_set.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def active_ibl_set(self):
		"""
		Deleter for **self.__active_ibl_set** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "active_ibl_set"))

	@property
	def inspector_plates(self):
		"""
		Property for **self.__inspector_plates** attribute.

		:return: self.__inspector_plates.
		:rtype: dict
		"""

		return self.__inspector_plates

	@inspector_plates.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def inspector_plates(self, value):
		"""
		Setter for **self.__inspector_plates** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspector_plates"))

	@inspector_plates.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def inspector_plates(self):
		"""
		Deleter for **self.__inspector_plates** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspector_plates"))

	@property
	def no_preview_image_text(self):
		"""
		Property for **self.__no_preview_image_text** attribute.

		:return: self.__no_preview_image_text.
		:rtype: unicode
		"""

		return self.__no_preview_image_text

	@no_preview_image_text.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def no_preview_image_text(self, value):
		"""
		Setter for **self.__no_preview_image_text** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "no_preview_image_text"))

	@no_preview_image_text.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def no_preview_image_text(self):
		"""
		Deleter for **self.__no_preview_image_text** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "no_preview_image_text"))

	@property
	def no_active_ibl_set_text(self):
		"""
		Property for **self.__no_active_ibl_set_text** attribute.

		:return: self.__no_active_ibl_set_text.
		:rtype: unicode
		"""

		return self.__no_active_ibl_set_text

	@no_active_ibl_set_text.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def no_active_ibl_set_text(self, value):
		"""
		Setter for **self.__no_active_ibl_set_text** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "no_active_ibl_set_text"))

	@no_active_ibl_set_text.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def no_active_ibl_set_text(self):
		"""
		Deleter for **self.__no_active_ibl_set_text** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "no_active_ibl_set_text"))

	@property
	def active_ibl_set_tool_tip_text(self):
		"""
		Property for **self.__active_ibl_set_tool_tip_text** attribute.

		:return: self.__active_ibl_set_tool_tip_text.
		:rtype: unicode
		"""

		return self.__active_ibl_set_tool_tip_text

	@active_ibl_set_tool_tip_text.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def active_ibl_set_tool_tip_text(self, value):
		"""
		Setter for **self.__active_ibl_set_tool_tip_text** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "active_ibl_set_tool_tip_text"))

	@active_ibl_set_tool_tip_text.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def active_ibl_set_tool_tip_text(self):
		"""
		Deleter for **self.__active_ibl_set_tool_tip_text** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "active_ibl_set_tool_tip_text"))

	@property
	def light_label_radius(self):
		"""
		Property for **self.__light_label_radius** attribute.

		:return: self.__light_label_radius.
		:rtype: int
		"""

		return self.__light_label_radius

	@light_label_radius.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_radius(self, value):
		"""
		Setter for **self.__light_label_radius** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "light_label_radius"))

	@light_label_radius.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_radius(self):
		"""
		Deleter for **self.__light_label_radius** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "light_label_radius"))

	@property
	def light_label_text_offset(self):
		"""
		Property for **self.__light_label_text_offset** attribute.

		:return: self.__light_label_text_offset.
		:rtype: int
		"""

		return self.__light_label_text_offset

	@light_label_text_offset.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_text_offset(self, value):
		"""
		Setter for **self.__light_label_text_offset** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "light_label_text_offset"))

	@light_label_text_offset.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_text_offset(self):
		"""
		Deleter for **self.__light_label_text_offset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "light_label_text_offset"))

	@property
	def light_label_text_margin(self):
		"""
		Property for **self.__light_label_text_margin** attribute.

		:return: self.__light_label_text_margin.
		:rtype: int
		"""

		return self.__light_label_text_margin

	@light_label_text_margin.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_text_margin(self, value):
		"""
		Setter for **self.__light_label_text_margin** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "light_label_text_margin"))

	@light_label_text_margin.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_text_margin(self):
		"""
		Deleter for **self.__light_label_text_margin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "light_label_text_margin"))

	@property
	def light_label_text_height(self):
		"""
		Property for **self.__light_label_text_height** attribute.

		:return: self.__light_label_text_height.
		:rtype: int
		"""

		return self.__light_label_text_height

	@light_label_text_height.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_text_height(self, value):
		"""
		Setter for **self.__light_label_text_height** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "light_label_text_height"))

	@light_label_text_height.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_text_height(self):
		"""
		Deleter for **self.__light_label_text_height** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "light_label_text_height"))

	@property
	def light_label_text_font(self):
		"""
		Property for **self.__light_label_text_font** attribute.

		:return: self.__light_label_text_font.
		:rtype: unicode
		"""

		return self.__light_label_text_font

	@light_label_text_font.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_text_font(self, value):
		"""
		Setter for **self.__light_label_text_font** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "light_label_text_font"))

	@light_label_text_font.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def light_label_text_font(self):
		"""
		Deleter for **self.__light_label_text_font** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "light_label_text_font"))

	@property
	def unnamed_light_name(self):
		"""
		Property for **self.__unnamed_light_name** attribute.

		:return: self.__unnamed_light_name.
		:rtype: unicode
		"""

		return self.__unnamed_light_name

	@unnamed_light_name.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def unnamed_light_name(self, value):
		"""
		Setter for **self.__unnamed_light_name** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"unnamed_light_name", value)
		self.__unnamed_light_name = value

	@unnamed_light_name.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def unnamed_light_name(self):
		"""
		Deleter for **self.__unnamed_light_name** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "unnamed_light_name"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Engine to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__ui_resources_directory = os.path.join(os.path.dirname(__file__), self.__ui_resources_directory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settings_section = self.name

		self.__preferences_manager = self.__engine.components_manager["factory.preferences_manager"]
		self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]

		self.activated = True
		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		Deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	def initialize_ui(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__pixmap_placeholder = \
			sibl_gui.ui.common.get_pixmap(os.path.join(self.__ui_resources_directory, self.__ui_loading_image),
										 asynchronous_loading=False)

		self.__sections_file_parsers_cache = foundations.cache.Cache()

		self.__model = PlatesModel()

		self.Plates_listView.setParent(None)
		self.Plates_listView = Plates_QListView(self, self.__model)
		self.Plates_listView.setObjectName("Plates_listView")
		self.Plates_frame_gridLayout.addWidget(self.Plates_listView, 0, 1)
		self.__view = self.Plates_listView
		self.__view.store_model_selection = self.__view.restore_model_selection = lambda: True

		self.Previous_Ibl_Set_pushButton.setIcon(
			QIcon(os.path.join(self.__ui_resources_directory, self.__ui_previous_image)))
		self.Next_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_next_image)))
		self.Previous_Plate_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_previous_image)))
		self.Next_Plate_pushButton.setIcon(QIcon(os.path.join(self.__ui_resources_directory, self.__ui_next_image)))

		self.Plates_frame.hide()
		self.Inspector_Options_groupBox.hide()

		self.__Inspector_DockWidget_set_ui()

		self.Inspector_Overall_frame.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Inspector_Overall_frame_add_actions()

		# Signals / Slots.
		self.__engine.images_caches.QIcon.content_added.connect(self.__view.viewport().update)
		self.__engine.images_caches.QPixmap.content_added.connect(self.__engine_images_caches_QPixmap__content_added)
		self.Plates_listView.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.__ibl_sets_outliner.model.modelReset.connect(self.__ibl_sets_outliner__modelReset)
		self.__engine.file_system_events_manager.file_changed.connect(self.__engine_file_system_events_manager__file_changed)
		for view in self.__ibl_sets_outliner.views:
			view.selectionModel().selectionChanged.connect(self.__ibl_sets_outliner_view_selectionModel__selectionChanged)
		self.Previous_Ibl_Set_pushButton.clicked.connect(self.__Previous_Ibl_Set_pushButton__clicked)
		self.Next_Ibl_Set_pushButton.clicked.connect(self.__Next_Ibl_Set_pushButton__clicked)
		self.Previous_Plate_pushButton.clicked.connect(self.__Previous_Plate_pushButton__clicked)
		self.Next_Plate_pushButton.clicked.connect(self.__Next_Plate_pushButton__clicked)
		self.Image_label.linkActivated.connect(self.__Image_label__linkActivated)
		self.refresh_nodes.connect(self.__model__refresh_nodes)
		self.ui_refresh.connect(self.__Inspector_DockWidget_refresh_ui)
		self.ui_clear.connect(self.__Inspector_DockWidget_clear_ui)

		self.initialized_ui = True
		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def uninitialize_ui(self):
		"""
		Uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def add_widget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dock_area), self)

		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def remove_widget(self):
		"""
		Removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	def __Inspector_DockWidget_set_ui(self):
		"""
		Sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		if self.__active_ibl_set:
			self.Title_label.setText("<center><b>{0}</b> - {1}</center>".format(self.__active_ibl_set.title,
																				self.__active_ibl_set.location))

			preview_available = False
			if foundations.common.path_exists(self.__active_ibl_set.preview_image):
				pixmap = sibl_gui.ui.common.get_pixmap(self.__active_ibl_set.preview_image)
				preview_available = True
			else:
				if foundations.common.path_exists(self.__active_ibl_set.background_image):
					pixmap = sibl_gui.ui.common.get_pixmap(self.__active_ibl_set.background_image,
														  size=self.__thumbnails_size,
														  placeholder=self.__pixmap_placeholder)
					preview_available = True

			if preview_available:
				self.Image_label.setPixmap(pixmap)
				self.__draw_active_ibl_set_overlay()
			else:
				self.Image_label.setText(self.__no_preview_image_text.format(
					sibl_gui.ui.common.filter_image_path(self.__active_ibl_set.icon),
					self.__active_ibl_set.author,
					self.__active_ibl_set.link))

			self.Image_label.setToolTip(self.__active_ibl_set_tool_tip_text.format(
				self.__active_ibl_set.title,
				self.__active_ibl_set.author or Constants.null_object,
				self.__active_ibl_set.location or Constants.null_object,
				sibl_gui.ui.common.get_formatted_shot_date(self.__active_ibl_set.date,
													   self.__active_ibl_set.time) or Constants.null_object,
				self.__active_ibl_set.comment or Constants.null_object))

			self.Details_label.setText("<center><b>Comment:</b> {0}</center>".format(self.__active_ibl_set.comment))

			self.Plates_frame.setVisible(bool(self.__inspector_plates))
		else:
			self.__Inspector_DockWidget_clear_ui()

	def __Inspector_DockWidget_refresh_ui(self):
		"""
		Sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		self.__Inspector_DockWidget_set_ui()

	def __Inspector_DockWidget_clear_ui(self):
		"""
		Clears the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		self.Title_label.setText(QString())
		self.Image_label.setText(self.__no_active_ibl_set_text.format(sibl_gui.ui.common.filter_image_path("")))
		self.Image_label.setToolTip(QString())
		self.Details_label.setText(QString())

		self.Plates_frame.hide()

	def __Inspector_Overall_frame_add_actions(self):
		"""
		Sets the **Inspector_Overall_frame** actions.
		"""

		pass

	def __model__refresh_nodes(self):
		"""
		Refreshes the **Plates_listView** Model nodes.
		"""

		self.set_plates()

	def __view_selectionModel__selectionChanged(self, selected_items, deselected_items):
		"""
		Defines the slot triggered by **Plates_listView** when Model selection has changed.

		:param selected_items: Selected items.
		:type selected_items: QItemSelection
		:param deselected_items: Deselected items.
		:type deselected_items: QItemSelection
		"""

		index = foundations.common.get_first_item(selected_items.indexes())
		node = index and self.__model.get_node(index) or None
		if not node:
			return

		if node.family == "Plate":
			self.Image_label.setPixmap(sibl_gui.ui.common.get_pixmap(node.plate.preview_image, asynchronous_loading=False))
		else:
			self.ui_refresh.emit()

	def __engine_file_system_events_manager__file_changed(self, file):
		"""
		Defines the slot triggered by the **file_system_events_manager** when a file is changed.

		:param file: File changed.
		:type file: unicode
		"""

		file = foundations.strings.to_string(file)
		if file in self.__sections_file_parsers_cache:
			LOGGER.debug("> Removing modified '{0}' file from cache.".format(file))
			self.__sections_file_parsers_cache.remove_content(file)

			if not self.__active_ibl_set:
				return

			if self.__active_ibl_set.path == file:
				self.__set_active_ibl_set()
				self.ui_refresh.emit()

	def __engine_images_caches_QPixmap__content_added(self, paths):
		"""
		Defines the slot triggered by the **QPixmap** images cache when content is added.

		:param paths: Added content.
		:type paths: list
		"""

		if not self.__active_ibl_set:
			return

		if foundations.common.get_first_item(paths) in (self.__active_ibl_set.preview_image,
													  self.__active_ibl_set.background_image):
			self.__Inspector_DockWidget_set_ui()

	def __ibl_sets_outliner__modelReset(self):
		"""
		Defines the slot triggered by :mod:`sibl_gui.components.core.ibl_sets_outliner.ibl_sets_outliner`
		Component Model when changed.
		"""

		self.__set_active_ibl_set()

	def __ibl_sets_outliner_view_selectionModel__selectionChanged(self, selected_items, deselected_items):
		"""
		Defines the slot triggered by :mod:`sibl_gui.components.core.ibl_sets_outliner.ibl_sets_outliner`
		Component Model selection when changed.

		:param selected_items: Selected items.
		:type selected_items: QItemSelection
		:param deselected_items: Deselected items.
		:type deselected_items: QItemSelection
		"""

		self.__set_active_ibl_set()

		self.__set_active_ibl_set_plates()
		self.refresh_nodes.emit()

		if self.__active_ibl_set:
			self.ui_refresh.emit()
		else:
			self.ui_clear.emit()

	def __Previous_Ibl_Set_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Previous_Ibl_Set_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loop_through_ibl_sets(True)

	def __Next_Ibl_Set_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Next_Ibl_Set_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loop_through_ibl_sets()

	def __Previous_Plate_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Previous_Plate_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loop_through_plates(True)

	def __Next_Plate_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Next_Plate_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loop_through_plates()

	def __Image_label__linkActivated(self, url):
		"""
		Defines the slot triggered by **Image_label** Widget when a link is clicked.

		:param url: Url to explore.
		:type url: QString
		"""

		QDesktopServices.openUrl(QUrl(url))

	def __set_active_ibl_set(self):
		"""
		Sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set.
		"""

		selected_ibl_sets = self.__ibl_sets_outliner.get_selected_ibl_sets()
		self.__active_ibl_set = foundations.common.get_first_item(selected_ibl_sets)
		if not self.__active_ibl_set:
			root_node = self.__ibl_sets_outliner.model.root_node
			childNode = foundations.common.get_first_item(root_node.children)
			self.__active_ibl_set = childNode.database_item if childNode is not None else None
		self.__active_ibl_set and self.__set_active_ibl_setParser()

	def __set_active_ibl_setParser(self):
		"""
		Sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set parser.
		"""

		if foundations.common.path_exists(self.__active_ibl_set.path):
			LOGGER.debug("> Parsing Inspector Ibl Set file: '{0}'.".format(self.__active_ibl_set))

			if not self.__sections_file_parsers_cache.get_content(self.__active_ibl_set.path):
				sections_file_parser = SectionsFileParser(self.__active_ibl_set.path)
				sections_file_parser.parse()
				self.__sections_file_parsers_cache.add_content(**{self.__active_ibl_set.path: sections_file_parser})

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
	def __set_active_ibl_set_plates(self):
		"""
		Sets the Plates from the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set.
		"""

		path = self.__active_ibl_set.path
		if not foundations.common.path_exists(path):
			raise foundations.exceptions.FileExistsError(
				"{0} | Exception raised while retrieving Plates: '{1}' Ibl Set file doesn't exists!".format(
					self.__class__.__name__, self.__active_ibl_set.title))

		sections_file_parser = self.__sections_file_parsers_cache.get_content(path)
		self.__inspector_plates = OrderedDict()
		for section in sections_file_parser.sections:
			if re.search(r"Plate\d+", section):
				self.__inspector_plates[section] = \
					Plate(
						name=foundations.strings.get_splitext_basename(sections_file_parser.get_value("PLATEfile", section)),
						icon=os.path.normpath(os.path.join(os.path.dirname(self.__active_ibl_set.path),
														   sections_file_parser.get_value("PLATEthumb", section))),
						preview_image=os.path.normpath(os.path.join(os.path.dirname(self.__active_ibl_set.path),
																   sections_file_parser.get_value("PLATEpreview",
																							   section))),
						image=os.path.normpath(os.path.join(os.path.dirname(self.__active_ibl_set.path),
															sections_file_parser.get_value("PLATEfile", section))))

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ExecutionError, ValueError)
	def __draw_active_ibl_set_overlay(self):
		"""
		Draws an overlay on :obj:`Inspector.Image_Label` Widget.
		"""

		painter = QPainter(self.Image_label.pixmap())
		painter.setRenderHints(QPainter.Antialiasing)

		ibl_set_path = self.__active_ibl_set.path
		sections_file_parser = self.__sections_file_parsers_cache.get_content(ibl_set_path)
		if sections_file_parser is None:
			raise foundations.exceptions.ExecutionError(
				"'{0}' Ibl Set file 'SectionsFileParser' instance not found!".format(ibl_set_path))

		for section in sections_file_parser.sections:
			if section == "Sun":
				self.__draw_light_label(painter,
									  Light(name="Sun",
											color=[int(value) for value in sections_file_parser.get_value(
												"SUNcolor", section).split(",")],
											u_coordinate=float(sections_file_parser.get_value("SUNu", section)),
											v_coordinate=float(sections_file_parser.get_value("SUNv", section))))

			elif re.search(r"Light\d+", section):
				self.__draw_light_label(painter, Light(name=sections_file_parser.get_value(
					"LIGHTname", section) or self.__unnamed_light_name,
													 color=[int(value) for value in sections_file_parser.get_value(
														 "LIGHTcolor", section).split(",")],
													 u_coordinate=float(
														 sections_file_parser.get_value("LIGHTu", section)),
													 v_coordinate=float(
														 sections_file_parser.get_value("LIGHTv", section))))

		painter.end()

	def __draw_light_label(self, painter, light):
		"""
		Draws a light label on given QPainter.

		:param painter: QPainter.
		:type painter: QPainter
		:param light: Light.
		:type light: Light
		"""

		width = painter.window().width()
		height = painter.window().height()

		light_color_red, light_color_green, light_color_blue = light.color

		painter.setBrush(QColor(light_color_red, light_color_green, light_color_blue, 200))
		painter.setPen(QPen(QBrush(QColor(light_color_red, light_color_green, light_color_blue, 200)), 2))
		font = QFont(self.__light_label_text_font, self.__light_label_text_height)
		font.setBold(True)
		painter.setFont(font)

		point_x = int(light.u_coordinate * width)
		point_y = int(light.v_coordinate * height)

		text_width = painter.fontMetrics().width(light.name.title())
		x_label_text_offset = -(self.__light_label_text_offset + text_width) if \
			point_x + text_width + self.__light_label_text_margin + self.__light_label_text_offset > width else \
			self.__light_label_text_offset
		y_label_text_offset = -(self.__light_label_text_offset + self.__light_label_text_height) if \
			point_y - (self.__light_label_text_height + self.__light_label_text_margin + self.__light_label_text_offset) < 0 else \
			self.__light_label_text_offset
		painter.drawText(point_x + x_label_text_offset, point_y - y_label_text_offset, light.name.title())

		painter.drawLine(point_x,
						 point_y,
						 point_x + (x_label_text_offset + text_width if x_label_text_offset < 0 else x_label_text_offset),
						 point_y - (y_label_text_offset + self.__light_label_text_height \
									   if y_label_text_offset < 0 else y_label_text_offset))

		painter.drawEllipse(QPoint(point_x, point_y), self.__light_label_radius, self.__light_label_radius)

		painter.setBrush(Qt.NoBrush)
		painter.setPen(QPen(QBrush(QColor(light_color_red, light_color_green, light_color_blue, 100)), 2))
		painter.drawEllipse(QPoint(point_x, point_y), self.__light_label_radius * 3, self.__light_label_radius * 3)
		painter.setPen(QPen(QBrush(QColor(light_color_red, light_color_green, light_color_blue, 50)), 2))
		painter.drawEllipse(QPoint(point_x, point_y), self.__light_label_radius * 4, self.__light_label_radius * 4)

	def set_plates(self):
		"""
		Sets the Plates Model nodes.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Setting up '{0}' Model!".format("Plates_listView"))

		node_flags = attributes_flags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
		root_node = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		ibl_set_node = IblSetNode(self.__active_ibl_set,
								name=self.__active_ibl_set.title,
								parent=root_node,
								node_flags=node_flags,
								attributes_flags=attributes_flags,
								icon_path=self.__active_ibl_set.icon)
		ibl_set_node.roles[Qt.DisplayRole] = ""

		if not self.__inspector_plates:
			return False

		for name, plate in self.__inspector_plates.iteritems():
			plate_node = PlatesNode(plate,
								   name=name,
								   parent=root_node,
								   node_flags=node_flags,
								   attributes_flags=attributes_flags)
			plate_node.roles[Qt.DisplayRole] = ""
			plate_node.roles[Qt.DecorationRole] = foundations.common.filter_path(plate.icon)

		self.__model.initialize_model(root_node)
		return True

	def loop_through_ibl_sets(self, backward=False):
		"""
		Loops through :mod:`sibl_gui.components.core.ibl_sets_outliner.ibl_sets_outliner` Component Ibl Sets.

		:param backward: Looping backward.
		:type backward: bool
		:return: Method success.
		:rtype: bool
		"""

		if self.__active_ibl_set:
			model = self.__ibl_sets_outliner.model

			active_ibl_set_node = [node for node in model.root_node.children if
								node.database_item.path == self.__active_ibl_set.path]
			active_ibl_set_node = foundations.common.get_first_item(active_ibl_set_node)
			if not active_ibl_set_node:
				return True

			row = active_ibl_set_node.row()

			step = not backward and 1 or -1
			idx = row + step
			if idx < 0:
				idx = model.root_node.children_count() - 1
			elif idx > model.root_node.children_count() - 1:
				idx = 0

			selection_model = self.__ibl_sets_outliner.get_active_view().selectionModel()
			selection_model.clear()
			selection_model.setCurrentIndex(model.index(idx), QItemSelectionModel.Select)
		else:
			self.ui_clear.emit()
		return True

	def loop_through_plates(self, backward=False):
		"""
		Loops through :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set Plates.

		:param backward: Looping backward.
		:type backward: bool
		:return: Method success.
		:rtype: bool
		"""

		index = foundations.common.get_first_item(self.Plates_listView.selectedIndexes())
		if index:
			step = not backward and 1 or -1
			idx = index.row() + step
			if idx < 0:
				idx = self.__model.rowCount() - 1
			elif idx > self.__model.rowCount() - 1:
				idx = 0

			selection_model = self.Plates_listView.selectionModel()
			selection_model.clear()
			selection_model.setCurrentIndex(self.__model.index(idx), QItemSelectionModel.Select)
		else:
			self.Plates_listView.setCurrentIndex(self.__model.index(0, 0))
		return True
