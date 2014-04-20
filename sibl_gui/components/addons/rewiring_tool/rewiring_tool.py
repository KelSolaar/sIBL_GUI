#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**rewiring_tool.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`RewiringTool` Component Interface class.

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
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFileDialog

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.parsers
import foundations.strings
import foundations.verbose
import umbra.ui.common
from manager.QWidget_component import QWidgetComponentFactory
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "RewiringTool"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Rewiring_Tool.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RewiringTool(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.addons.rewiring_tool.rewiring_tool` Component Interface class.
	| It provides override keys on request for the :mod:`sibl_gui.components.addons.loader_script.loader_script` Component.
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

		super(RewiringTool, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__dock_area = 2

		self.__engine = None

		self.__ibl_sets_outliner = None

		self.__rewire_frames_widgets = None
		self.__rewire_combo_boxes_widgets = None
		self.__rewire_line_edit_widgets = None

		self.__loader_script = None

		self.__rewiring_parameters = (("Background", "Background|BGfile", "background_image"),
									("Lighting", "Enviroment|EVfile", "lighting_image"),
									("Reflection", "Reflection|REFfile", "reflection_image"),
									("Custom image", None, None))

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
	def rewire_frames_widgets(self):
		"""
		Property for **self.__rewire_frames_widgets** attribute.

		:return: self.__rewire_frames_widgets.
		:rtype: tuple
		"""

		return self.__rewire_frames_widgets

	@rewire_frames_widgets.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def rewire_frames_widgets(self, value):
		"""
		Setter for **self.__rewire_frames_widgets** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "rewire_frames_widgets"))

	@rewire_frames_widgets.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def rewire_frames_widgets(self):
		"""
		Deleter for **self.__rewire_frames_widgets** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rewire_frames_widgets"))

	@property
	def rewire_combo_boxes_widgets(self):
		"""
		Property for **self.__rewire_combo_boxes_widgets** attribute.

		:return: self.__rewire_combo_boxes_widgets.
		:rtype: tuple
		"""

		return self.__rewire_combo_boxes_widgets

	@rewire_combo_boxes_widgets.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def rewire_combo_boxes_widgets(self, value):
		"""
		Setter for **self.__rewire_combo_boxes_widgets** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "rewire_combo_boxes_widgets"))

	@rewire_combo_boxes_widgets.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def rewire_combo_boxes_widgets(self):
		"""
		Deleter for **self.__rewire_combo_boxes_widgets** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rewire_combo_boxes_widgets"))

	@property
	def rewire_line_edit_widgets(self):
		"""
		Property for **self.__rewire_line_edit_widgets** attribute.

		:return: self.__rewire_line_edit_widgets.
		:rtype: tuple
		"""

		return self.__rewire_line_edit_widgets

	@rewire_line_edit_widgets.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def rewire_line_edit_widgets(self, value):
		"""
		Setter for **self.__rewire_line_edit_widgets** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "rewire_line_edit_widgets"))

	@rewire_line_edit_widgets.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def rewire_line_edit_widgets(self):
		"""
		Deleter for **self.__rewire_line_edit_widgets** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rewire_line_edit_widgets"))

	@property
	def rewiring_parameters(self):
		"""
		Property for **self.__rewiring_parameters** attribute.

		:return: self.__rewiring_parameters.
		:rtype: tuple
		"""

		return self.__rewiring_parameters

	@rewiring_parameters.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def rewiring_parameters(self, value):
		"""
		Setter for **self.__rewiring_parameters** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "rewiring_parameters"))

	@rewiring_parameters.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def rewiring_parameters(self):
		"""
		Deleter for **self.__rewiring_parameters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rewiring_parameters"))

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

		self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]
		self.__loader_script = self.__engine.components_manager["addons.loader_script"]

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

		self.__ibl_sets_outliner = None
		self.__loader_script = None

		self.activated = False
		return True

	def initialize_ui(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__rewire_frames_widgets = (self.Background_frame, self.Lighting_frame, self.Reflection_frame)
		self.__rewire_combo_boxes_widgets = (self.Background_comboBox, self.Lighting_comboBox, self.Reflection_comboBox)
		self.__rewire_line_edit_widgets = (self.Background_Path_lineEdit,
										self.Lighting_Path_lineEdit,
										self.Reflection_Path_lineEdit)

		for frame in self.__rewire_frames_widgets:
			LOGGER.debug("> Hiding '%s'.", frame)
			frame.hide()

		for index in range(len(self.__rewire_combo_boxes_widgets)):
			self.__rewire_combo_boxes_widgets[index].data = self.__rewiring_parameters[index][1]
			self.__rewire_combo_boxes_widgets[index].addItems([foundations.common.get_first_item(parameter) \
														 for parameter in self.__rewiring_parameters])
			self.__rewire_combo_boxes_widgets[index].setCurrentIndex(index)

		# Signals / Slots.
		self.Background_comboBox.activated.connect(self.__set_rewire_widget_frames_visibility)
		self.Lighting_comboBox.activated.connect(self.__set_rewire_widget_frames_visibility)
		self.Reflection_comboBox.activated.connect(self.__set_rewire_widget_frames_visibility)
		self.Background_Path_toolButton.clicked.connect(self.__Background_Path_toolButton__clicked)
		self.Lighting_Path_toolButton.clicked.connect(self.__Lighting_Path_toolButton__clicked)
		self.Reflection_Path_toolButton.clicked.connect(self.__Reflection_Path_toolButton__clicked)

		self.initialized_ui = True
		return True

	def uninitialize_ui(self):
		"""
		Uninitializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__rewire_frames_widgets = None
		self.__rewire_combo_boxes_widgets = None
		self.__rewire_line_edit_widgets = None

		# Signals / Slots.
		self.Background_comboBox.activated.disconnect(self.__set_rewire_widget_frames_visibility)
		self.Lighting_comboBox.activated.disconnect(self.__set_rewire_widget_frames_visibility)
		self.Reflection_comboBox.activated.disconnect(self.__set_rewire_widget_frames_visibility)
		self.Background_Path_toolButton.clicked.disconnect(self.__Background_Path_toolButton__clicked)
		self.Lighting_Path_toolButton.clicked.disconnect(self.__Lighting_Path_toolButton__clicked)
		self.Reflection_Path_toolButton.clicked.disconnect(self.__Reflection_Path_toolButton__clicked)

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

	def __Background_Path_toolButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Background_ToolButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.__set_rewire_custom_path("Background")

	def __Lighting_Path_toolButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Lighting_ToolButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.__set_rewire_custom_path("Lighting")

	def __Reflection_Path_toolButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Reflection_ToolButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.__set_rewire_custom_path("Reflection")

	def __set_rewire_widget_frames_visibility(self, index):
		"""
		Shows / hides rewire Widget frames.

		:param index: ComboBox index.
		:type index: tuple
		"""

		for index in range(len(self.__rewire_combo_boxes_widgets)):
			if self.__rewire_combo_boxes_widgets[index].currentText() == "Custom image":
				LOGGER.debug("> Showing rewire frame '{0}'.".format(self.__rewire_frames_widgets[index]))
				self.__rewire_frames_widgets[index].show()
			else:
				LOGGER.debug("> Hiding rewire frame '{0}'.".format(self.__rewire_frames_widgets[index]))
				self.__rewire_frames_widgets[index].hide()

	def __set_rewire_custom_path(self, component):
		"""
		Sets the :mod:`sibl_gui.components.addons.rewiring_tool.rewiring_tool` Component
		custom image QLineEdit Widgets.

		:param component: Target Component.
		:type component: unicode
		"""

		custom_file = umbra.ui.common.store_last_browsed_path(QFileDialog.getOpenFileName(self,
																					"Custom {0} File:".format(component),
																					RuntimeGlobals.last_browsed_path))
		LOGGER.debug("> Chosen custom '{0}': '{1}'.".format(component, custom_file))
		if custom_file != "":
			if component == "Background":
				self.Background_Path_lineEdit.setText(QString(custom_file))
			elif component == "Lighting":
				self.Lighting_Path_lineEdit.setText(QString(custom_file))
			elif component == "Reflection":
				self.Reflection_Path_lineEdit.setText(QString(custom_file))

	def get_override_keys(self):
		"""
		Gets override keys.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.info("{0} | Updating Loader Script override keys!".format(self.__class__.__name__))

		ibl_set = foundations.common.get_first_item(self.__ibl_sets_outliner.get_selected_ibl_sets())
		if not ibl_set:
			return False

		for index, combo_box in enumerate(self.__rewire_combo_boxes_widgets):
			parameter = self.__rewiring_parameters[combo_box.currentIndex()]
			if combo_box.currentText() == "Custom image":
				LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format(
				combo_box.data, foundations.strings.to_string(self.__rewire_line_edit_widgets[index].text())))
				self.__loader_script.override_keys[combo_box.data] = foundations.parsers.get_attribute_compound(
																		parameter[1],
																		foundations.strings.get_normalized_path(
																		foundations.strings.to_string(
																		self.__rewire_line_edit_widgets[index].text())))
			else:
				LOGGER.debug("> Adding '{0}' override key with value: '{1}'.".format(combo_box.data,
																					getattr(ibl_set, parameter[2])))
				self.__loader_script.override_keys[combo_box.data] = getattr(ibl_set, parameter[2]) and \
																foundations.parsers.get_attribute_compound(parameter[1],
																foundations.strings.get_normalized_path(getattr(ibl_set, parameter[2])))
		return True
