#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**loader_script_options.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`LoaderScriptOptions` Component Interface class.

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
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QDoubleSpinBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPalette

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.io
import foundations.parsers
import foundations.strings
import foundations.verbose
import umbra.exceptions
import umbra.ui.common
from foundations.parsers import SectionsFileParser
from manager.QWidget_component import QWidgetComponentFactory
from sibl_gui.components.addons.loader_script_options.views import TemplatesAttributes_QTableWidget
from umbra.globals.constants import Constants
from umbra.ui.widgets.variable_QPushButton import Variable_QPushButton

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "LoaderScriptOptions"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Loader_Script_Options.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LoaderScriptOptions(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	| Definesthe :mod:`sibl_gui.components.addons.loader_script_options.loader_script_options` Component Interface class.
	| It provides override keys on request for the :mod:`sibl_gui.components.addons.loader_script.loader_script` Component.
	| It exposes Templates files **Common Attributes** and **Additional Attributes** sections so that
		the user can configure the behavior of the Loader Script.
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

		super(LoaderScriptOptions, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__dock_area = 2

		self.__engine = None

		self.__templates_outliner = None
		self.__loader_script = None

		self.__views = None
		self.__common_view = None
		self.__additional_view = None

		self.__namespace_splitter = "|"

		self.__templates_settings_directory = "templates"
		self.__template_settings_file = None
		self.__template_common_attributes_section = "Common Attributes"
		self.__template_additional_attributes_section = "Additional Attributes"
		self.__template_script_section = "Script"
		self.__options_toolboxes_headers = ["Value"]

		self.__ui_light_gray_color = QColor(240, 240, 240)
		self.__ui_dark_gray_color = QColor(160, 160, 160)

		self.__enum_splitter = ";"

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
	def templates_outliner(self):
		"""
		Property for **self.__templates_outliner** attribute.

		:return: self.__templates_outliner.
		:rtype: QWidget
		"""

		return self.__templates_outliner

	@templates_outliner.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def templates_outliner(self, value):
		"""
		Setter for **self.__templates_outliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templates_outliner"))

	@templates_outliner.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def templates_outliner(self):
		"""
		Deleter for **self.__templates_outliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templates_outliner"))

	@property
	def loader_script(self):
		"""
		Property for **self.__loader_script** attribute.

		:return: self.__loader_script.
		:rtype: QWidget
		"""

		return self.__loader_script

	@loader_script.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def loader_script(self, value):
		"""
		Setter for **self.__loader_script** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loader_script"))

	@loader_script.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def loader_script(self):
		"""
		Deleter for **self.__loader_script** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loader_script"))

	@property
	def views(self):
		"""
		Property for **self.__views** attribute.

		:return: self.__views.
		:rtype: tuple
		"""

		return self.__views

	@views.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def views(self, value):
		"""
		Setter for **self.__views** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "views"))

	@views.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def views(self):
		"""
		Deleter for **self.__views** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "views"))

	@property
	def common_view(self):
		"""
		Property for **self.__common_view** attribute.

		:return: self.__common_view.
		:rtype: QListView
		"""

		return self.__common_view

	@common_view.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def common_view(self, value):
		"""
		Setter for **self.__common_view** attribute.

		:param value: Attribute value.
		:type value: QListView
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "common_view"))

	@common_view.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def common_view(self):
		"""
		Deleter for **self.__common_view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def additional_view(self):
		"""
		Property for **self.__additional_view** attribute.

		:return: self.__additional_view.
		:rtype: QListView
		"""

		return self.__additional_view

	@additional_view.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def additional_view(self, value):
		"""
		Setter for **self.__additional_view** attribute.

		:param value: Attribute value.
		:type value: QListView
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "additional_view"))

	@additional_view.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def additional_view(self):
		"""
		Deleter for **self.__additional_view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def namespace_splitter(self):
		"""
		Property for **self.__namespace_splitter** attribute.

		:return: self.__namespace_splitter.
		:rtype: unicode
		"""

		return self.__namespace_splitter

	@namespace_splitter.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def namespace_splitter(self, value):
		"""
		Setter for **self.__namespace_splitter** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"namespace_splitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format(
			"namespace_splitter", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
			"namespace_splitter", value)
		self.__namespace_splitter = value

	@namespace_splitter.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def namespace_splitter(self):
		"""
		Deleter for **self.__namespace_splitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "namespace_splitter"))

	@property
	def templates_settings_directory(self):
		"""
		Property for **self.__templates_settings_directory** attribute.

		:return: self.__templates_settings_directory.
		:rtype: unicode
		"""

		return self.__templates_settings_directory

	@templates_settings_directory.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def templates_settings_directory(self, value):
		"""
		Setter for **self.__templates_settings_directory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templates_settings_directory"))

	@templates_settings_directory.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def templates_settings_directory(self):
		"""
		Deleter for **self.__templates_settings_directory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templates_settings_directory"))

	@property
	def template_settings_file(self):
		"""
		Property for **self.__template_settings_file** attribute.

		:return: self.__template_settings_file.
		:rtype: unicode
		"""

		return self.__template_settings_file

	@template_settings_file.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def template_settings_file(self, value):
		"""
		Setter for **self.__template_settings_file** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "template_settings_file"))

	@template_settings_file.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def template_settings_file(self):
		"""
		Deleter for **self.__template_settings_file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "template_settings_file"))

	@property
	def template_common_attributes_section(self):
		"""
		Property for **self.__template_common_attributes_section** attribute.

		:return: self.__template_common_attributes_section.
		:rtype: unicode
		"""

		return self.__template_common_attributes_section

	@template_common_attributes_section.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def template_common_attributes_section(self, value):
		"""
		Setter for **self.__template_common_attributes_section** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "template_common_attributes_section"))

	@template_common_attributes_section.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def template_common_attributes_section(self):
		"""
		Deleter for **self.__template_common_attributes_section** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "template_common_attributes_section"))

	@property
	def template_additional_attributes_section(self):
		"""
		Property for **self.__template_additional_attributes_section** attribute.

		:return: self.__template_additional_attributes_section.
		:rtype: unicode
		"""

		return self.__template_additional_attributes_section

	@template_additional_attributes_section.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def template_additional_attributes_section(self, value):
		"""
		Setter for **self.__template_additional_attributes_section** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "template_additional_attributes_section"))

	@template_additional_attributes_section.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def template_additional_attributes_section(self):
		"""
		Deleter for **self.__template_additional_attributes_section** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(
		self.__class__.__name__, "template_additional_attributes_section"))

	@property
	def template_script_section(self):
		"""
		Property for **self.__template_script_section** attribute.

		:return: self.__template_script_section.
		:rtype: unicode
		"""

		return self.__template_script_section

	@template_script_section.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def template_script_section(self, value):
		"""
		Setter for **self.__template_script_section** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "template_script_section"))

	@template_script_section.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def template_script_section(self):
		"""
		Deleter for **self.__template_script_section** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "template_script_section"))

	@property
	def options_toolboxes_headers(self):
		"""
		Property for **self.__options_toolboxes_headers** attribute.

		:return: self.__options_toolboxes_headers.
		:rtype: list
		"""

		return self.__options_toolboxes_headers

	@options_toolboxes_headers.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def options_toolboxes_headers(self, value):
		"""
		Setter for **self.__options_toolboxes_headers** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "options_toolboxes_headers"))

	@options_toolboxes_headers.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def options_toolboxes_headers(self):
		"""
		Deleter for **self.__options_toolboxes_headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "options_toolboxes_headers"))

	@property
	def ui_light_gray_color(self):
		"""
		Property for **self.__ui_light_gray_color** attribute.

		:return: self.__ui_light_gray_color.
		:rtype: QColor
		"""

		return self.__ui_light_gray_color

	@ui_light_gray_color.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_light_gray_color(self, value):
		"""
		Setter for **self.__ui_light_gray_color** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_light_gray_color"))

	@ui_light_gray_color.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_light_gray_color(self):
		"""
		Deleter for **self.__ui_light_gray_color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_light_gray_color"))

	@property
	def ui_dark_gray_color(self):
		"""
		Property for **self.__ui_dark_gray_color** attribute.

		:return: self.__ui_dark_gray_color.
		:rtype: QColor
		"""

		return self.__ui_dark_gray_color

	@ui_dark_gray_color.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_dark_gray_color(self, value):
		"""
		Setter for **self.__ui_dark_gray_color** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_dark_gray_color"))

	@ui_dark_gray_color.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_dark_gray_color(self):
		"""
		Deleter for **self.__ui_dark_gray_color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_dark_gray_color"))

	@property
	def enum_splitter(self):
		"""
		Property for **self.__enum_splitter** attribute.

		:return: self.__enum_splitter.
		:rtype: unicode
		"""

		return self.__enum_splitter

	@enum_splitter.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def enum_splitter(self, value):
		"""
		Setter for **self.__enum_splitter** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"enum_splitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("enum_splitter", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
			"enum_splitter", value)
		self.__enum_splitter = value

	@enum_splitter.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def enum_splitter(self):
		"""
		Deleter for **self.__enum_splitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "enum_splitter"))

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

		self.__engine = engine

		self.__templates_outliner = self.__engine.components_manager["core.templates_outliner"]
		self.__loader_script = self.__engine.components_manager["addons.loader_script"]

		self.__templates_settings_directory = os.path.join(self.__engine.user_application_data_directory,
														Constants.settings_directory,
														self.__templates_settings_directory)
		not foundations.common.path_exists(self.__templates_settings_directory) and \
		os.makedirs(self.__templates_settings_directory)
		self.__template_settings_file = None

		self.activated = True
		return True

	def deactivate(self):
		"""
		Deactivates the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.__templates_outliner = None
		self.__loader_script = None

		self.__templates_settings_directory = os.path.basename(os.path.abspath(self.__templates_settings_directory))
		self.__template_settings_file = None

		self.activated = False
		return True

	def initialize_ui(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		umbra.ui.common.set_toolBox_height(self.Loader_Script_Options_toolBox)

		self.Common_Attributes_tableWidget.setParent(None)
		self.Common_Attributes_tableWidget = TemplatesAttributes_QTableWidget(self, message="No Attributes to view!")
		self.Common_Attributes_tableWidget.setObjectName("Common_Attributes_tableWidget")
		self.Common_Attributes_page_gridLayout.addWidget(self.Common_Attributes_tableWidget, 0, 0)
		self.__common_view = self.Common_Attributes_tableWidget

		self.Additional_Attributes_tableWidget.setParent(None)
		self.Additional_Attributes_tableWidget = TemplatesAttributes_QTableWidget(self, message="No Attributes to view!")
		self.Additional_Attributes_tableWidget.setObjectName("Additional_Attributes_tableWidget")
		self.Additional_Attributes_page_gridLayout.addWidget(self.Additional_Attributes_tableWidget, 0, 0)
		self.__additional_view = self.Additional_Attributes_tableWidget

		self.__views = (self.__common_view, self.__additional_view)

		# Signals / Slots.
		self.__templates_outliner.view.selectionModel().selectionChanged.connect(
		self.__templates_outliner_view_selectionModel__selectionChanged)

		self.initialized_ui = True
		return True

	def uninitialize_ui(self):
		"""
		Uninitializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__views = None
		self.__common_view = None
		self.__additional_view = None

		# Signals / Slots.
		self.__templates_outliner.view.selectionModel().selectionChanged.disconnect(
		self.__templates_outliner_view_selectionModel__selectionChanged)

		self.initialized_ui = False
		return True

	def add_widget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dock_area), self)

		return True

	def remove_widget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	@foundations.exceptions.handle_exceptions(ValueError)
	def __view_set_ui(self, section, view, overrides):
		"""
		Defines and sets the given View.

		:param section: Section attributes.
		:type section: dict
		:param view: Table Widget.
		:type view: QTableWidget
		:param overrides: Attributes overrides.
		:type overrides: dict
		"""

		LOGGER.debug("> Updating '{0}'.".format(view.objectName()))

		view.hide()

		self.__view_clear_ui(view)

		view.setRowCount(len(section))
		view.setColumnCount(len(self.__options_toolboxes_headers))
		view.horizontalHeader().setStretchLastSection(True)
		view.setHorizontalHeaderLabels(self.__options_toolboxes_headers)
		view.horizontalHeader().hide()

		palette = QPalette()
		palette.setColor(QPalette.Base, Qt.transparent)
		view.setPalette(palette)

		vertical_header_labels = []
		for row, attribute in enumerate(section):
			LOGGER.debug("> Current attribute: '{0}'.".format(attribute))

			overrides_value = overrides[attribute] if attribute in overrides else None
			LOGGER.debug("> Settings value: '{0}'.".format(overrides_value or Constants.null_object))

			attribute_compound = foundations.parsers.get_attribute_compound(attribute, section[attribute])
			if attribute_compound.name:
				vertical_header_labels.append(attribute_compound.alias)
			else:
				vertical_header_labels.append(foundations.strings.get_nice_name(attribute_compound.name))

			LOGGER.debug("> Attribute type: '{0}'.".format(attribute_compound.type))
			if attribute_compound.type == "Boolean":
				state = True if int(overrides_value if overrides_value is not None else attribute_compound.value) else False
				item = Variable_QPushButton(self,
						state,
						(self.__ui_light_gray_color, self.__ui_dark_gray_color),
						("True", "False"))
				item.setObjectName("Spread_Sheet_pushButton")
				item.setChecked(state)

				# Signals / Slots.
				item.clicked.connect(self.__view__valueChanged)
			elif attribute_compound.type == "Float":
				item = QDoubleSpinBox()
				item.setMinimum(0)
				item.setMaximum(65535)
				item.setValue(float(overrides_value if overrides_value is not None else attribute_compound.value))

				# Signals / Slots.
				item.valueChanged.connect(self.__view__valueChanged)
			elif attribute_compound.type == "Enum":
				item = QComboBox()
				combo_box_items = [enumItem.strip() for enumItem in attribute_compound.value.split(self.__enum_splitter)]
				item.addItems(combo_box_items)
				if overrides_value in combo_box_items:
					item.setCurrentIndex(combo_box_items.index(overrides_value))

				# Signals / Slots.
				item.currentIndexChanged.connect(self.__view__valueChanged)
			elif attribute_compound.type == "String":
				item = QLineEdit(QString(overrides_value if overrides_value is not None else attribute_compound.value))
				item.setAlignment(Qt.AlignCenter)

				# Signals / Slots.
				item.editingFinished.connect(self.__view__valueChanged)
			else:
				item = QLabel(QString("Attribute Type Error!"))
				item.setStyleSheet("QLabel {background-color: rgb(210, 64, 32);}")
				item.setAlignment(Qt.AlignCenter)

			item.data = attribute_compound
			view.setCellWidget(row, 0, item)

		view.setVerticalHeaderLabels(vertical_header_labels)
		view.show()

	def __view_clear_ui(self, view):
		"""
		Defines and sets the given View.

		:param view: Table Widget.
		:type view: QTableWidget
		"""

		LOGGER.debug("> Clearing '{0}'.".format(view.objectName()))

		view.clear()
		view.setRowCount(0)
		view.setColumnCount(0)

	def __views_set_ui(self):
		"""
		Sets the Views.
		"""

		selected_templates = self.__templates_outliner.get_selected_templates()
		template = foundations.common.get_first_item(selected_templates)
		if not (template and foundations.common.path_exists(template.path)):
			for view in self.__views:
				self.__view_clear_ui(view)
			return

		LOGGER.debug("> Attempting to read '{0}' Template settings file.".format(template.name))
		common_attributes_overrides = {}
		additional_attributes_overrides = {}
		template_settings_directory = os.path.join(self.__templates_settings_directory, template.software, template.name)
		current_template_settings_directory = os.path.join(template_settings_directory, template.release)
		self.__template_settings_file = os.path.join(template_settings_directory,
										template.release,
										os.path.basename(template.path))

		not foundations.common.path_exists(current_template_settings_directory) and \
		foundations.io.set_directory(current_template_settings_directory)

		template_settings_file = None
		if foundations.common.path_exists(self.__template_settings_file):
			template_settings_file = self.__template_settings_file
		else:
			for version in sorted((
							path for path in os.listdir(template_settings_directory)
							if re.search(r"\d\.\d\.\d", path)), reverse=True, key=lambda x:(foundations.strings.get_version_rank(x))):
				path = os.path.join(template_settings_directory, version, os.path.basename(template.path))
				if foundations.common.path_exists(path):
					template_settings_file = path
					break

		if template_settings_file:
			LOGGER.debug("> Accessing '{0}' Template settings file: '{1}'.".format(template.name, template_settings_file))
			template_settings_sections_file_parser = SectionsFileParser(template_settings_file)
			template_settings_sections_file_parser.parse()
			common_attributes_overrides.update(
			template_settings_sections_file_parser.sections[self.__template_common_attributes_section])
			additional_attributes_overrides.update(
			template_settings_sections_file_parser.sections[self.__template_additional_attributes_section])
		else:
			LOGGER.debug("> No Template settings file found for : '{0}'.".format(template.name))

		LOGGER.debug("> Parsing '{0}' Template for '{1}' and '{2}' section.".format(
		template.name, self.__template_common_attributes_section, self.__template_additional_attributes_section))
		template_sections_file_parser = SectionsFileParser(template.path)
		template_sections_file_parser.parse(raw_sections=(self.__template_script_section))

		self.__view_set_ui(template_sections_file_parser.sections.get(self.__template_common_attributes_section, {}),
								self.__common_view, common_attributes_overrides)
		self.__view_set_ui(template_sections_file_parser.sections.get(self.__template_additional_attributes_section, {}),
								self.__additional_view, additional_attributes_overrides)

	def __view__valueChanged(self, *args):
		"""
		Defines the slot triggered by a View when value changed.

		:param \*args: Arguments.
		:type \*args: \*
		"""

		LOGGER.debug("> Initializing '{0}' Template settings file content.".format(self.__template_settings_file))
		template_settings_sections_file_parser = SectionsFileParser(self.__template_settings_file)
		template_settings_sections_file_parser.sections = OrderedDict()
		for section, view in OrderedDict([(self.__template_common_attributes_section,
												self.Common_Attributes_tableWidget),
												(self.__template_additional_attributes_section,
												self.Additional_Attributes_tableWidget)]).iteritems():
			template_settings_sections_file_parser.sections[section] = OrderedDict()
			for row in range(view.rowCount()):
				widget = view.cellWidget(row, 0)
				if type(widget) is Variable_QPushButton:
					value = widget.text() == "True" and "1" or "0"
				elif type(widget) is QDoubleSpinBox:
					value = foundations.strings.to_string(widget.value())
				elif type(widget) is QComboBox:
					value = foundations.strings.to_string(widget.currentText())
				else:
					value = foundations.strings.to_string(widget.text())
				template_settings_sections_file_parser.sections[
				section][foundations.namespace.remove_namespace(widget.data.name)] = value
		template_settings_sections_file_parser.write()

	def __templates_outliner_view_selectionModel__selectionChanged(self, selected_items, deselected_items):
		"""
		Defines the slot triggered by **templates_outliner.view** Model when selection changed

		:param selected_items: Selected items.
		:type selected_items: QItemSelection
		:param deselected_items: Deselected items.
		:type deselected_items: QItemSelection
		"""

		self.__views_set_ui()

	def __update_override_keys(self, view):
		"""
		Updates the Loader Script Component override keys.

		:param view: Table Widget.
		:type view: QTableWidget
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Updating override keys with '{0}' attributes.".format(view.objectName()))

		for row in range(view.rowCount()):
			widget = view.cellWidget(row, 0)
			if type(widget) is Variable_QPushButton:
				value = widget.text() == "True" and "1" or "0"
			elif type(widget) is QDoubleSpinBox:
				value = foundations.strings.to_string(widget.value())
			elif type(widget) is QComboBox:
				value = foundations.strings.to_string(widget.currentText())
			else:
				value = foundations.strings.to_string(widget.text())
			widget.data.value = value

			LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format(widget.data.name, widget.data.value))
			self.__loader_script.override_keys[widget.data.name] = widget.data
		return True

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
	def get_override_keys(self):
		"""
		Gets override keys.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.info("{0} | Updating Loader Script override keys!".format(self.__class__.__name__))

		success = True
		success *= self.__update_override_keys(self.Common_Attributes_tableWidget) or False
		success *= self.__update_override_keys(self.Additional_Attributes_tableWidget) or False

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while retrieving override keys!".format(self.__class__.__name__))
