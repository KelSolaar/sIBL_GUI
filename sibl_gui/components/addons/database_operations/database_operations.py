#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**database_operations.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`DatabaseOperations` Component Interface class and others helper objects.

**Others:**

"""

from __future__ import unicode_literals

import os
from PyQt4.QtCore import QString
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QMessageBox

import foundations.common
import foundations.data_structures
import foundations.exceptions
import foundations.verbose
import sibl_gui.components.core.database.operations
import umbra.engine
import umbra.ui.widgets.message_box as message_box
from manager.QWidget_component import QWidgetComponentFactory

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "DatabaseType", "DatabaseOperations"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Database_Operations.ui")

class DatabaseType(foundations.data_structures.Structure):
	"""
	| Defines a storage object for manipulation methods associated to a given Database type.
	| See :mod:`sibl_gui.components.core.database.types` module for more informations
		about the available Database types.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: type, get_method, update_content_method, remove_method, model_container, update_location_method
		:type kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.data_structures.Structure.__init__(self, **kwargs)

class DatabaseOperations(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.addons.database_operations.database_operations` Component Interface class.
	| It provides various methods to operate on the Database.
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

		super(DatabaseOperations, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settings_section = None

		self.__preferences_manager = None
		self.__ibl_sets_outliner = None
		self.__templates_outliner = None

		self.__types = None

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
	def types(self):
		"""
		Property for **self.__types** attribute.

		:return: self.__types.
		:rtype: tuple
		"""

		return self.__types

	@types.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def types(self, value):
		"""
		Setter for **self.__types** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "types"))

	@types.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def types(self):
		"""
		Deleter for **self.__types** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "types"))

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
		self.__templates_outliner = self.__engine.components_manager["core.templates_outliner"]

		self.__types = (DatabaseType(type="Ibl Set",
						get_method=sibl_gui.components.core.database.operations.get_ibl_sets,
						update_content_method=sibl_gui.components.core.database.operations.update_ibl_set_content,
						remove_method=sibl_gui.components.core.database.operations.remove_ibl_set,
						model_container=self.__ibl_sets_outliner,
						update_location_method=self.__ibl_sets_outliner.update_ibl_set_location_ui),
						DatabaseType(type="Template",
						get_method=sibl_gui.components.core.database.operations.get_templates,
						update_content_method=sibl_gui.components.core.database.operations.update_template_content,
						remove_method=sibl_gui.components.core.database.operations.remove_template,
						model_container=self.__templates_outliner,
						update_location_method=self.__templates_outliner.update_template_location_ui))

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
		self.__templates_outliner = None

		self.activated = False
		return True

	def initialize_ui(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		if not self.__engine.parameters.database_read_only:
			self.Update_Database_pushButton.clicked.connect(self.__Update_Database_pushButton__clicked)
			self.Remove_Invalid_Data_pushButton.clicked.connect(self.__Remove_Invalid_Data_pushButton__clicked)
		else:
			LOGGER.info(
			"{0} | Database Operations capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "database_read_only"))

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
		if not self.__engine.parameters.database_read_only:
			self.Update_Database_pushButton.clicked.disconnect(self.__Update_Database_pushButton__clicked)
			self.Remove_Invalid_Data_pushButton.clicked.disconnect(self.__Remove_Invalid_Data_pushButton__clicked)

		self.initialized_ui = False
		return True

	def add_widget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferences_manager.Others_Preferences_gridLayout.addWidget(self.Database_Operations_groupBox)

		return True

	def remove_widget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferences_manager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.Database_Operations_groupBox.setParent(None)

		return True

	def __Update_Database_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Update_Database_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.update_database()

	def __Remove_Invalid_Data_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Remove_Invalid_Data_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.remove_invalid_data()

	@umbra.engine.show_processing("Updating Database ...")
	def update_database(self):
		"""
		| Updates the Database.
		| Each type defined by :meth:`DatabaseOperations.sibl_gui.components.core.database.types` attribute
			will have its instances checked and updated by their associated methods.

		:return: Method success.
		:rtype: bool
		"""

		for type in self.__types:
			for item in type.get_method():
				if foundations.common.path_exists(item.path):
					if type.update_content_method(item):
						LOGGER.info("{0} | '{1}' {2} has been updated!".format(self.__class__.__name__,
																					item.name,
																					type.type))
				else:
					choice = message_box.message_box("Question", "Error",
					"{0} | '{1}' {2} file is missing, would you like to update it's location?".format(
					self.__class__.__name__, item.name, type.type),
					QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No,
					custom_buttons=((QString("No To All"), QMessageBox.RejectRole),))

					if choice == 0:
						break

					if choice == QMessageBox.Yes:
						type.update_location_method(item)
				self.__engine.process_events()
			type.model_container.refresh_nodes.emit()
		self.__engine.stop_processing()
		self.__engine.notifications_manager.notify("{0} | Database update done!".format(self.__class__.__name__))
		return True

	@umbra.engine.show_processing("Removing Invalid Data ...")
	def remove_invalid_data(self):
		"""
		Removes invalid data from the Database.

		:return: Method success.
		:rtype: bool
		"""

		if message_box.message_box("Question", "Question",
		"Are you sure you want to remove invalid data from the Database?",
		buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			for type in self.__types:
				for item in type.get_method():
					if foundations.common.path_exists(item.path):
						continue

					LOGGER.info("{0} | Removing non existing '{1}' {2} from the Database!".format(self.__class__.__name__,
																								item.name,
																								type.type))
					type.remove_method(item.id)

					self.__engine.process_events()
				type.model_container.refresh_nodes.emit()
			self.__engine.stop_processing()
			self.__engine.notifications_manager.notify(
			"{0} | Invalid data removed from Database!".format(self.__class__.__name__))
		return True
