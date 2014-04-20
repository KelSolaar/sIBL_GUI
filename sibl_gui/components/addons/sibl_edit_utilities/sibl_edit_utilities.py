#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**sibl_edit_utilities.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_edit_utilities` Component Interface class.

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
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtGui import QFileDialog

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.exceptions
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "sibl_edit_utilities"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "sIBLedit_Utilities.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class sIBLeditUtilities(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.addons.sibl_edit_utilities.sIBLeditUtilities` Component Interface class.
	| It provides methods to link the Application to sibl_edit.
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

		super(sIBLeditUtilities, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settings_section = None

		self.__preferences_manager = None
		self.__ibl_sets_outliner = None
		self.__inspector = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: QSettings
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settings_section(self):
		"""
		Property for **self.__settings_section** attribute.

		:return: self.__settings_section.
		:rtype: unicode
		"""

		return self.__settings_section

	@settings_section.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_section(self, value):
		"""
		Setter for **self.__settings_section** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings_section"))

	@settings_section.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_section(self):
		"""
		Deleter for **self.__settings_section** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings_section"))

	@property
	def preferences_manager(self):
		"""
		Property for **self.__preferences_manager** attribute.

		:return: self.__preferences_manager.
		:rtype: QWidget
		"""

		return self.__preferences_manager

	@preferences_manager.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def preferences_manager(self, value):
		"""
		Setter for **self.__preferences_manager** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "preferences_manager"))

	@preferences_manager.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def preferences_manager(self):
		"""
		Deleter for **self.__preferences_manager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preferences_manager"))

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
	def inspector(self):
		"""
		Property for **self.__inspector** attribute.

		:return: self.__inspector.
		:rtype: QWidget
		"""

		return self.__inspector

	@inspector.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def inspector(self, value):
		"""
		Setter for **self.__inspector** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspector"))

	@inspector.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def inspector(self):
		"""
		Deleter for **self.__inspector** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspector"))

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
		self.__settings = self.__engine.settings
		self.__settings_section = self.name

		self.__preferences_manager = self.__engine.components_manager["factory.preferences_manager"]
		self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]
		self.__inspector = self.__engine.components_manager["core.inspector"]

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
		self.__settings = None
		self.__settings_section = None

		self.__preferences_manager = None
		self.__ibl_sets_outliner = None
		self.__inspector = None

		self.activated = False
		return True

	def initialize_ui(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__sIBLedit_Path_lineEdit_set_ui()

		self.__add_actions()

		# Signals / Slots.
		self.sIBLedit_Path_toolButton.clicked.connect(self.__sIBLedit_Path_toolButton__clicked)
		self.sIBLedit_Path_lineEdit.editingFinished.connect(self.__sIBLedit_Path_lineEdit__editFinished)

		self.initialized_ui = True
		return True

	def uninitialize_ui(self):
		"""
		Uninitializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.sIBLedit_Path_toolButton.clicked.disconnect(self.__sIBLedit_Path_toolButton__clicked)
		self.sIBLedit_Path_lineEdit.editingFinished.disconnect(self.__sIBLedit_Path_lineEdit__editFinished)

		self.__remove_actions()

		self.initialized_ui = False
		return True

	def add_widget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferences_manager.Others_Preferences_gridLayout.addWidget(self.sIBLedit_Path_groupBox)

		return True

	def remove_widget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.sIBLedit_Path_groupBox.setParent(None)

		return True

	def __add_actions(self):
		"""
		Sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.database_read_only:
			edit_ibl_set_in_sibl_edit_action = self.__engine.actions_manager.register_action(
			"Actions|Umbra|Components|core.ibl_sets_outliner|Edit In sIBLEdit ...",
			slot=self.__ibl_sets_outliner_views_edit_ibl_set_in_sibl_edit_action__triggered)
			for view in self.__ibl_sets_outliner.views:
				view.addAction(edit_ibl_set_in_sibl_edit_action)

			self.__inspector.Inspector_Overall_frame.addAction(self.__engine.actions_manager.register_action(
			"Actions|Umbra|Components|core.inspector|Edit In sIBLEdit ...",
			slot=self.__inspector_edit_active_ibl_set_in_sibl_edit_action__triggered))
		else:
			LOGGER.info("{0} | sIBLEdit editing capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "database_read_only"))

	def __remove_actions(self):
		"""
		Removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		if not self.__engine.parameters.database_read_only:
			edit_ibl_set_in_sibl_edit_action = "Actions|Umbra|Components|core.ibl_sets_outliner|Edit In sIBLEdit ..."
			for view in self.__ibl_sets_outliner.views:
				view.removeAction(self.__engine.actions_manager.get_action(edit_ibl_set_in_sibl_edit_action))
			self.__engine.actions_manager.unregister_action(edit_ibl_set_in_sibl_edit_action)
			edit_active_ibl_set_in_sibl_edit_action = "Actions|Umbra|Components|core.inspector|Edit In sIBLEdit ..."
			self.__inspector.Inspector_Overall_frame.removeAction(self.__engine.actions_manager.get_action(
			edit_active_ibl_set_in_sibl_edit_action))
			self.__engine.actions_manager.unregister_action(edit_active_ibl_set_in_sibl_edit_action)

	def __ibl_sets_outliner_views_edit_ibl_set_in_sibl_edit_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|core.ibl_sets_outliner|Edit In sIBLEdit ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.edit_ibl_set_in_sibl_edit_ui()

	def __inspector_edit_active_ibl_set_in_sibl_edit_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|core.inspector|Edit In sIBLEdit ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.edit_active_ibl_set_in_sibl_edit_ui()

	def __sIBLedit_Path_lineEdit_set_ui(self):
		"""
		Fills **sIBLedit_Path_lineEdit** Widget.
		"""

		sibl_edit_executable = self.__settings.get_key(self.__settings_section, "sibl_edit_executable")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("sIBLedit_Path_lineEdit", sibl_edit_executable.toString()))
		self.sIBLedit_Path_lineEdit.setText(sibl_edit_executable.toString())

	def __sIBLedit_Path_toolButton__clicked(self, checked):
		"""
		Defines the slot triggered by **sIBLedit_Path_toolButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		sibl_edit_executable = umbra.ui.common.store_last_browsed_path(QFileDialog.getOpenFileName(self,
																						"sibl_edit Executable:",
																						RuntimeGlobals.last_browsed_path))
		if sibl_edit_executable != "":
			LOGGER.debug("> Chosen sIBLEdit executable: '{0}'.".format(sibl_edit_executable))
			self.sIBLedit_Path_lineEdit.setText(QString(sibl_edit_executable))
			self.__settings.set_key(self.__settings_section, "sibl_edit_executable", self.sIBLedit_Path_lineEdit.text())

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
											foundations.exceptions.UserError)
	def __sIBLedit_Path_lineEdit__editFinished(self):
		"""
		Defines the slot triggered by **sIBLedit_Path_lineEdit** Widget when edited and check that entered path is valid.
		"""

		value = foundations.strings.to_string(self.sIBLedit_Path_lineEdit.text())
		if not foundations.common.path_exists(os.path.abspath(value)) and value != "":
			LOGGER.debug("> Restoring preferences!")
			self.__sIBLedit_Path_lineEdit_set_ui()

			raise foundations.exceptions.UserError("{0} | Invalid sIBLEdit executable file!".format(self.__class__.__name__))
		else:
			self.__settings.set_key(self.__settings_section, "sibl_edit_executable", self.sIBLedit_Path_lineEdit.text())

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
											foundations.exceptions.FileExistsError)
	def edit_ibl_set_in_sibl_edit_ui(self):
		"""
		Edits selected Ibl Set in sIBLEdit.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		sibl_edit = foundations.strings.to_string(self.sIBLedit_Path_lineEdit.text())
		if sibl_edit:
			selected_ibl_set = foundations.common.get_first_item(self.__ibl_sets_outliner.get_selected_ibl_sets())
			if selected_ibl_set is None:
				return False

			if foundations.common.path_exists(selected_ibl_set.path):
				return self.edit_ibl_set_in_sibl_edit(selected_ibl_set.path,
												foundations.strings.to_string(self.sIBLedit_Path_lineEdit.text()))
			else:
				raise foundations.exceptions.FileExistsError(
				"{0} | Exception raised while sending Ibl Set to sIBLEdit: '{1}' Ibl Set file doesn't exists!".format(
				self.__class__.__name__, selected_ibl_set.name))
		else:
			self.__engine.notifications_manager.warnify(
			"{0} | Please define an 'sIBLEdit' executable in the preferences!".format(self.__class__.__name__))

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
											foundations.exceptions.FileExistsError)
	def edit_active_ibl_set_in_sibl_edit_ui(self):
		"""
		Edits :mod:`sibl_gui.components.core.inspector.inspector` Component inspected Ibl Set in sIBLEdit.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		sibl_edit = foundations.strings.to_string(self.sIBLedit_Path_lineEdit.text())
		if sibl_edit:
			active_ibl_set = self.__inspector.active_ibl_set
			if active_ibl_set is None:
				return False

			if foundations.common.path_exists(active_ibl_set.path):
				return self.edit_ibl_set_in_sibl_edit(active_ibl_set.path, sibl_edit)
			else:
				raise foundations.exceptions.FileExistsError(
				"{0} | Exception raised while sending Inspector Ibl Set to sIBLEdit: '{1}' Ibl Set file doesn't exists!".format(
				self.__class__.__name__, active_ibl_set.title))
		else:
			self.__engine.notifications_manager.warnify(
			"{0} | Please define an 'sIBLEdit' executable in the preferences!".format(self.__class__.__name__))

	def get_process_command(self, path, sibl_edit):
		"""
		Gets process command.

		:param path: Path.
		:type path: unicode
		:param sibl_edit: sibl_edit.
		:type sibl_edit: unicode
		:return: Process command.
		:rtype: unicode
		"""

		return "\"{0}\" \"{1}\"".format(sibl_edit, path)

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler, Exception)
	def edit_ibl_set_in_sibl_edit(self, path, sibl_edit):
		"""
		Edits given Ibl Set in sIBLEdit.

		:param path: Path.
		:type path: unicode
		:param sibl_edit: sIBLEdit executable path.
		:type sibl_edit: unicode
		:return: Method success.
		:rtype: bool
		"""

		edit_command = self.get_process_command(path, sibl_edit)
		if edit_command:
			LOGGER.debug("> Current edit command: '{0}'.".format(edit_command))
			LOGGER.info("{0} | Launching 'sibl_edit' with '{1}'.".format(self.__class__.__name__, path))
			edit_process = QProcess()
			edit_process.startDetached(edit_command)
			return True
		else:
			raise Exception("{0} | Exception raised: No suitable process command given!".format(self.__class__.__name__))
