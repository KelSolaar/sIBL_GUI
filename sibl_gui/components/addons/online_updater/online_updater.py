#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**online_updater.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`OnlineUpdater` Component Interface class and others online update related objects.

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
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import QNetworkRequest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import sibl_gui.components.core.database.operations
import sibl_gui.exceptions
import umbra.exceptions
from foundations.parsers import SectionsFileParser
from manager.QWidget_component import QWidgetComponentFactory
from sibl_gui.components.addons.online_updater.remote_updater import ReleaseObject
from sibl_gui.components.addons.online_updater.remote_updater import RemoteUpdater
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "REPOSITORY_URL", "OnlineUpdater"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Online_Updater.ui")

REPOSITORY_URL = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Repository/"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class OnlineUpdater(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.addons.online_updater.online_updater` Component Interface class.
	| This Component provides online updating capabilities to the Application available through options exposed in
		the :mod:`sibl_gui.components.core.preferences_manager.preferences_manager` Component ui.
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

		super(OnlineUpdater, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settings_section = None

		self.__preferences_manager = None
		self.__templates_outliner = None
		self.__locations_browser = None

		self.__io_directory = "remote"

		self.__repository_url = REPOSITORY_URL
		self.__releases_file_url = "sIBL_GUI_Releases.rc"

		self.__release_reply = None
		self.__network_access_manager = None
		self.__releases_file_reply = None

		self.__remote_updater = None
		self.__report_update_status = None

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
	def locations_browser(self):
		"""
		Property for **self.__locations_browser** attribute.

		:return: self.__locations_browser.
		:rtype: QWidget
		"""

		return self.__locations_browser

	@locations_browser.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def locations_browser(self, value):
		"""
		Setter for **self.__locations_browser** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locations_browser"))

	@locations_browser.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def locations_browser(self):
		"""
		Deleter for **self.__locations_browser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locations_browser"))

	@property
	def io_directory(self):
		"""
		Property for **self.__io_directory** attribute.

		:return: self.__io_directory.
		:rtype: unicode
		"""

		return self.__io_directory

	@io_directory.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def io_directory(self, value):
		"""
		Setter for **self.__io_directory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "io_directory"))

	@io_directory.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def io_directory(self):
		"""
		Deleter for **self.__io_directory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "io_directory"))

	@property
	def repository_url(self):
		"""
		Property for **self.__repository_url** attribute.

		:return: self.__repository_url.
		:rtype: unicode
		"""

		return self.__repository_url

	@repository_url.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def repository_url(self, value):
		"""
		Setter for **self.__repository_url** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "repository_url"))

	@repository_url.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def repository_url(self):
		"""
		Deleter for **self.__repository_url** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "repository_url"))

	@property
	def releases_file_url(self):
		"""
		Property for **self.__releases_file_url** attribute.

		:return: self.__releases_file_url.
		:rtype: unicode
		"""

		return self.__releases_file_url

	@releases_file_url.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def releases_file_url(self, value):
		"""
		Setter for **self.__releases_file_url** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "releases_file_url"))

	@releases_file_url.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def releases_file_url(self):
		"""
		Deleter for **self.__releases_file_url** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "releases_file_url"))

	@property
	def network_access_manager(self):
		"""
		Property for **self.__network_access_manager** attribute.

		:return: self.__network_access_manager.
		:rtype: QNetworkAccessManager
		"""

		return self.__network_access_manager

	@network_access_manager.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def network_access_manager(self, value):
		"""
		Setter for **self.__network_access_manager** attribute.

		:param value: Attribute value.
		:type value: QNetworkAccessManager
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "network_access_manager"))

	@network_access_manager.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def network_access_manager(self):
		"""
		Deleter for **self.__network_access_manager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "network_access_manager"))

	@property
	def release_reply(self):
		"""
		Property for **self.__releases_file_reply** attribute.

		:return: self.__releases_file_reply.
		:rtype: QNetworkReply
		"""

		return self.__releases_file_reply

	@release_reply.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def release_reply(self, value):
		"""
		Setter for **self.__releases_file_reply** attribute.

		:param value: Attribute value.
		:type value: QNetworkReply
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "release_reply"))

	@release_reply.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def release_reply(self):
		"""
		Deleter for **self.__releases_file_reply** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "release_reply"))

	@property
	def remote_updater(self):
		"""
		Property for **self.__remote_updater** attribute.

		:return: self.__remote_updater.
		:rtype: object
		"""

		return self.__remote_updater

	@remote_updater.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def remote_updater(self, value):
		"""
		Setter for **self.__remote_updater** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "remote_updater"))

	@remote_updater.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def remote_updater(self):
		"""
		Deleter for **self.__remote_updater** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "remote_updater"))

	@property
	def report_update_status(self):
		"""
		Property for **self.__report_update_status** attribute.

		:return: self.__report_update_status.
		:rtype: bool
		"""

		return self.__report_update_status

	@report_update_status.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def report_update_status(self, value):
		"""
		Setter for **self.__report_update_status** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "report_update_status"))

	@report_update_status.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def report_update_status(self):
		"""
		Deleter for **self.__report_update_status** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "report_update_status"))

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
		self.__templates_outliner = self.__engine.components_manager["core.templates_outliner"]
		self.__locations_browser = self.__engine.components_manager["addons.locations_browser"]

		self.__io_directory = os.path.join(self.__engine.user_application_data_directory,
										Constants.io_directory, self.__io_directory)
		not foundations.common.path_exists(self.__io_directory) and os.makedirs(self.__io_directory)

		self.__network_access_manager = QNetworkAccessManager()

		self.__report_update_status = True

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
		self.__templates_outliner = None
		self.__locations_browser = None

		self.__io_directory = os.path.basename(os.path.abspath(self.__io_directory))

		self.__network_access_manager = None

		self.__report_update_status = None

		self.activated = False
		return True

	def initialize_ui(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__engine.parameters.deactivate_worker_threads and \
		LOGGER.info(
		"{0} | 'OnStartup' Online Updater worker thread deactivated by '{1}' command line parameter value!".format(
		self.__class__.__name__, "deactivate_worker_threads"))

		self.__Check_For_New_Releases_On_Startup_checkBox_set_ui()
		self.__Ignore_Non_Existing_Templates_checkBox_set_ui()

		# Signals / Slots.
		self.Check_For_New_Releases_pushButton.clicked.connect(self.__Check_For_New_Releases_pushButton__clicked)
		self.Check_For_New_Releases_On_Startup_checkBox.stateChanged.connect(
		self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.Ignore_Non_Existing_Templates_checkBox.stateChanged.connect(
		self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

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
		self.Check_For_New_Releases_pushButton.clicked.disconnect(self.__Check_For_New_Releases_pushButton__clicked)
		self.Check_For_New_Releases_On_Startup_checkBox.stateChanged.disconnect(
		self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.Ignore_Non_Existing_Templates_checkBox.stateChanged.disconnect(
		self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

		self.initialized_ui = False
		return True

	def on_startup(self):
		"""
		Defines the slot triggered on Framework startup.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'on_startup' method.".format(self.__class__.__name__))

		self.__report_update_status = False
		if not self.__engine.parameters.deactivate_worker_threads and \
		self.Check_For_New_Releases_On_Startup_checkBox.isChecked():
			self.check_for_new_releases()
		return True

	def add_widget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferences_manager.Others_Preferences_gridLayout.addWidget(self.Online_Updater_groupBox)

	def remove_widget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.Online_Updater_groupBox.setParent(None)

	def __Check_For_New_Releases_On_Startup_checkBox_set_ui(self):
		"""
		Sets the **Check_For_New_Releases_On_Startup_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.get_key(self.__settings_section, "check_for_new_releases_on_startup").isNull() and \
		self.__settings.set_key(self.__settings_section, "check_for_new_releases_on_startup", Qt.Checked)

		check_for_new_releases_on_startup = self.__settings.get_key(self.__settings_section, "check_for_new_releases_on_startup")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Check_For_New_Releases_On_Startup_checkBox",
												foundations.common.get_first_item(check_for_new_releases_on_startup.toInt())))
		self.Check_For_New_Releases_On_Startup_checkBox.setCheckState(
		foundations.common.get_first_item(check_for_new_releases_on_startup.toInt()))

	def __Check_For_New_Releases_On_Startup_checkBox__stateChanged(self, state):
		"""
		Defines the slot triggered by **Check_For_New_Releases_On_Startup_checkBox** Widget when state changed.

		:param state: Checkbox state.
		:type state: int
		"""

		LOGGER.debug("> Check for new releases on startup state: '{0}'.".format(state))
		self.__settings.set_key(self.__settings_section, "check_for_new_releases_on_startup", state)

	def __Ignore_Non_Existing_Templates_checkBox_set_ui(self):
		"""
		Sets the **Ignore_Non_Existing_Templates_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.get_key(self.__settings_section, "ignore_non_existing_templates").isNull() and \
		self.__settings.set_key(self.__settings_section, "ignore_non_existing_templates", Qt.Checked)

		ignore_non_existing_templates = self.__settings.get_key(self.__settings_section, "ignore_non_existing_templates")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Ignore_Non_Existing_Templates_checkBox",
													foundations.common.get_first_item(ignore_non_existing_templates.toInt())))
		self.Ignore_Non_Existing_Templates_checkBox.setCheckState(
		foundations.common.get_first_item(ignore_non_existing_templates.toInt()))

	def __Ignore_Non_Existing_Templates_checkBox__stateChanged(self, state):
		"""
		Defines the slot triggered by **Ignore_Non_Existing_Templates_checkBox** Widget when state changed.

		:param state: Checkbox state.
		:type state: int
		"""

		LOGGER.debug("> Ignore non existing Templates state: '{0}'.".format(state))
		self.__settings.set_key(self.__settings_section, "ignore_non_existing_templates", state)

	def __Check_For_New_Releases_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Check_For_New_Releases_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.check_for_new_releases_ui()

	@foundations.exceptions.handle_exceptions(sibl_gui.exceptions.NetworkError)
	def __releases_file_reply__finished(self):
		"""
		Defines the slot triggered by the releases file reply when finished.
		"""

		self.__engine.stop_processing()

		if not self.__releases_file_reply.error():
			content = []
			while not self.__releases_file_reply.atEnd ():
				content.append(foundations.strings.to_string(self.__releases_file_reply.readLine()))

			LOGGER.debug("> Parsing releases file content.")
			sections_file_parser = SectionsFileParser()
			sections_file_parser.content = content
			sections_file_parser.parse()

			releases = {}
			for remote_object in sections_file_parser.sections:
				if remote_object != Constants.application_name:
					database_templates = \
					sibl_gui.components.core.database.operations.filter_templates("^{0}$".format(remote_object), "name")
					database_template = foundations.common.get_first_item([foundations.common.get_first_item(database_template)
												for database_template in sorted(((database_template, database_template.release)
												for database_template in database_templates),
												reverse=True,
												key=lambda x:(foundations.strings.get_version_rank(x[1])))])
					if not self.__engine.parameters.database_read_only:
						if database_template:
							if database_template.release != sections_file_parser.get_value("Release", remote_object):
								releases[remote_object] = ReleaseObject(name=remote_object,
																	repository_version=sections_file_parser.get_value(
																	"Release", remote_object),
																	local_version=database_template.release,
																	type=sections_file_parser.get_value("Type",
																									remote_object),
																	url=sections_file_parser.get_value("Url",
																									remote_object),
																	comment=sections_file_parser.get_value("Comment",
																									remote_object))
						else:
							if not self.Ignore_Non_Existing_Templates_checkBox.isChecked():
								releases[remote_object] = ReleaseObject(name=remote_object,
																	repository_version=sections_file_parser.get_value(
																	"Release", remote_object),
																	local_version=None,
																	type=sections_file_parser.get_value("Type",
																									remote_object),
																	url=sections_file_parser.get_value("Url",
																									remote_object),
																	comment=sections_file_parser.get_value("Comment",
																									remote_object))
					else:
						LOGGER.info("{0} | '{1}' repository remote object skipped by '{2}' command line parameter value!".format(
						self.__class__.__name__, remote_object, "database_read_only"))
				else:
					if Constants.version != sections_file_parser.get_value("Release", remote_object):
						releases[remote_object] = ReleaseObject(name=remote_object,
															repository_version=sections_file_parser.get_value("Release",
																										remote_object),
															local_version=Constants.version,
															url=sections_file_parser.get_value("Url", remote_object),
															type=sections_file_parser.get_value("Type", remote_object),
															comment=None)
			if releases:
				LOGGER.debug("> Initializing Remote Updater.")
				self.__remote_updater = RemoteUpdater(self, releases, Qt.Window)
				self.__remote_updater.show()
			else:
				self.__report_update_status and self.__engine.notifications_manager.notify(
				"{0} | '{1}' is up to date!".format(self.__class__.__name__, Constants.application_name))
		else:
			raise sibl_gui.exceptions.NetworkError("{0} | QNetworkAccessManager error code: '{1}'.".format(
			self.__class__.__name__, self.__releases_file_reply.error()))

	def __get_releases_file(self, url):
		"""
		Gets the releases file.
		"""

		LOGGER.debug("> Downloading '{0}' releases file.".format(url.path()))

		self.__engine.start_processing("Retrieving Releases File ...")
		self.__releases_file_reply = self.__network_access_manager.get(QNetworkRequest(url))
		self.__releases_file_reply.finished.connect(self.__releases_file_reply__finished)

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
											sibl_gui.exceptions.NetworkError,
											Exception)
	def check_for_new_releases_ui(self):
		"""
		Checks for new releases.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		if not self.__network_access_manager.networkAccessible():
			raise sibl_gui.exceptions.NetworkError("{0} | Network is not accessible!".format(self.__class__.__name__))

		self.__report_update_status = True
		if self.check_for_new_releases():
			return True
		else:
			raise Exception("{0} | Exception raised while checking for new releases!".format(self.__class__.__name__))

	@foundations.exceptions.handle_exceptions(sibl_gui.exceptions.NetworkError, Exception)
	def check_for_new_releases(self):
		"""
		Checks for new releases.

		:return: Method success.
		:rtype: bool
		"""

		if not self.__network_access_manager.networkAccessible():
			raise sibl_gui.exceptions.NetworkError("{0} | Network is not accessible!".format(self.__class__.__name__))

		self.__get_releases_file(QUrl(os.path.join(self.__repository_url, self.__releases_file_url)))
		return True
