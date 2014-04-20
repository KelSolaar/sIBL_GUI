#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**001_migrate_3-x-x_to_4-0-0.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Migrates sIBL_GUI from 3.x.x to 4.0.0.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
# import os
# import shutil
# import sqlalchemy
# from PyQt4.QtGui import QMessageBox

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
# import foundations.common
# import foundations.core
import foundations.verbose
# import sibl_gui.components.core.database.operations
# import umbra.ui.widgets.message_box
# from umbra.globals.constants import Constants
# from umbra.globals.runtime_globals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UID", "apply"]

LOGGER = foundations.verbose.install_logger()

UID = "f23bedfa0def170bb6f70f24b4e1b047"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def apply():
	"""
	Triggers the patch execution.

	:return: Definition success.
	:rtype: bool
	"""

	deprecated = """
	if RuntimeGlobals.parameters.database_read_only:
		message = "sIBL_GUI is launched with '-r / --database_read_only' parameter preventing database migration!\n\n\
In order to complete the migration, you will need to relaunch sIBL_GUI without the '-r / --database_read_only' parameter!\n\n\
If you are using an already migrated shared database, you can ignore this message!\n\nWould like to continue?"
		if umbra.ui.widgets.message_box.message_box("Question",
													"sIBL_GUI | Question",
													message,
													buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
			foundations.core.exit(1)

	if RuntimeGlobals.parameters.database_read_only:
		LOGGER.warning(
		"!> {0} | Database has been set read only by '{1}' command line parameter value!".format(__name__,
																								"database_read_only"))
		return True

	if RuntimeGlobals.parameters.database_directory:
		database_directory = RuntimeGlobals.parameters.database_directory
		legacy_database_file = os.path.join(database_directory, "sIBL_Database.sqlite")
	else:
		database_directory = os.path.join(RuntimeGlobals.user_application_data_directory, Constants.database_directory)
		legacy_database_file = os.path.normpath(os.path.join(RuntimeGlobals.user_application_data_directory,
									"..",
									Constants.database_directory,
									"sIBL_Database.sqlite"))

	if foundations.common.path_exists(legacy_database_file):
		database_file = os.path.join(database_directory, Constants.database_file)
		message = "A previous sIBL_GUI database file has been found: '{0}'!\n\n\
Would you like to migrate it toward sIBL_GUI 4.0.0?".format(
				legacy_database_file)
		if umbra.ui.widgets.message_box.message_box("Question", "Question",
														message,
														buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			try:
				LOGGER.info("{0} | Copying '{1}' database file to '{2}' destination!".format(__name__,
																							legacy_database_file,
																							database_file))
				shutil.copyfile(legacy_database_file, database_file)
			except:
				message = "{0} | Critical exception raised while copying '{1}' database file to '{2}' destination!\n\n\
sIBL_GUI will now exit!".format(__name__, legacy_database_file, database_file)
				umbra.ui.widgets.message_box.message_box("Critical", "Critical", message)
				foundations.core.exit(1)

			if RuntimeGlobals.parameters.database_directory:
				deprecated_database_directory = os.path.join(database_directory, "backup", "deprecated")
				message = "The previous sIBL_GUI database file will be backuped into the following directory: '{0}'.".format(
				deprecated_database_directory)
				umbra.ui.widgets.message_box.message_box("Information", "Information", message)
				os.makedirs(deprecated_database_directory)
				shutil.move(legacy_database_file,
							os.path.join(deprecated_database_directory, os.path.basename(legacy_database_file)))

			database_engine = sqlalchemy.create_engine("sqlite:///{0}".format(database_file))
			database_session_maker = sqlalchemy.orm.sessionmaker(bind=database_engine)
			database_session = database_session_maker()
			for template in sibl_gui.components.core.database.operations.get_templates(database_session):
				id = template.id
				LOGGER.info("{0} | Removing deprecated Template with '{1}' id from database!".format(__name__, id))
				sibl_gui.components.core.database.operations.remove_template(id, database_session)
	"""

	return True
