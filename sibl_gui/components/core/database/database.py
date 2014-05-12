#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**database.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`Database` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import alembic.command
import os
import sqlalchemy.orm
from alembic.config import Config

import foundations.common
import foundations.exceptions
import foundations.verbose
import sibl_gui.components.core.database.operations
from foundations.rotating_backup import RotatingBackup
from manager.component import Component
from sibl_gui.components.core.database.types import Base
from umbra.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "ALEMBIC_CONFIGURATION_FILE",
           "ALEMBIC_SCRIPTS_DIRECTORY",
           "Database"]

LOGGER = foundations.verbose.install_logger()

ALEMBIC_CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), "migration", "alembic.ini")
ALEMBIC_SCRIPTS_DIRECTORY = os.path.join(os.path.dirname(__file__), "migration", "alembic")


class Database(Component):
    """
    | Defines the :mod:`sibl_gui.components.core.database.database` Component Interface class.
    | It provides Application Database creation and session, proceeds to its backup using
        the :mod:`foundations.rotating_backup`.
    """

    def __init__(self, name=None):
        """
        Initializes the class.

        :param name: Component name.
        :type name: unicode
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        Component.__init__(self, name=name)

        # --- Setting class attributes. ---
        self.deactivatable = False

        self.__engine = None

        self.__database_name = None
        self.__database_session = None
        self.__database_session_maker = None
        self.__database_engine = None
        self.__databaseCatalog = None

        self.__databaseConnectionString = None

        self.__databaseBackupDirectory = "backup"
        self.__databaseBackupCount = 6

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
    def database_name(self):
        """
        Property for **self.__database_name** attribute.

        :return: self.__database_name.
        :rtype: unicode
        """

        return self.__database_name

    @database_name.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_name(self, value):
        """
        Setter for **self.__database_name** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "database_name"))

    @database_name.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_name(self):
        """
        Deleter for **self.__database_name** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "database_name"))

    @property
    def database_engine(self):
        """
        Property for **self.__database_engine** attribute.

        :return: self.__database_engine.
        :rtype: object
        """

        return self.__database_engine

    @database_engine.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_engine(self, value):
        """
        Setter for **self.__database_engine** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "database_engine"))

    @database_engine.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_engine(self):
        """
        Deleter for **self.__database_engine** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "database_engine"))

    @property
    def databaseCatalog(self):
        """
        Property for **self.__databaseCatalog** attribute.

        :return: self.__databaseCatalog.
        :rtype: object
        """

        return self.__databaseCatalog

    @databaseCatalog.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def databaseCatalog(self, value):
        """
        Setter for **self.__databaseCatalog** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseCatalog"))

    @databaseCatalog.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def databaseCatalog(self):
        """
        Deleter for **self.__databaseCatalog** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseCatalog"))

    @property
    def database_session(self):
        """
        Property for **self.__database_session** attribute.

        :return: self.__database_session.
        :rtype: object
        """

        return self.__database_session

    @database_session.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_session(self, value):
        """
        Setter for **self.__database_session** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "database_session"))

    @database_session.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_session(self):
        """
        Deleter for **self.__database_session** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "database_session"))

    @property
    def database_session_maker(self):
        """
        Property for **self.__database_session_maker** attribute.

        :return: self.__database_session_maker.
        :rtype: object
        """

        return self.__database_session_maker

    @database_session_maker.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_session_maker(self, value):
        """
        Setter for **self.__database_session_maker** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "database_session_maker"))

    @database_session_maker.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_session_maker(self):
        """
        Deleter for **self.__database_session_maker** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "database_session_maker"))

    @property
    def databaseConnectionString(self):
        """
        Property for **self.__databaseConnectionString** attribute.

        :return: self.__databaseConnectionString.
        :rtype: unicode
        """

        return self.__databaseConnectionString

    @databaseConnectionString.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def databaseConnectionString(self, value):
        """
        Setter for **self.__databaseConnectionString** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseConnectionString"))

    @databaseConnectionString.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def databaseConnectionString(self):
        """
        Deleter for **self.__databaseConnectionString** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseConnectionString"))

    @property
    def databaseBackupDirectory(self):
        """
        Property for **self.__databaseBackupDirectory** attribute.

        :return: self.__databaseBackupDirectory.
        :rtype: unicode
        """

        return self.__databaseBackupDirectory

    @databaseBackupDirectory.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def databaseBackupDirectory(self, value):
        """
        Setter for **self.__databaseBackupDirectory** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseBackupDirectory"))

    @databaseBackupDirectory.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def databaseBackupDirectory(self):
        """
        Deleter for **self.__databaseBackupDirectory** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseBackupDirectory"))

    @property
    def databaseBackupCount(self):
        """
        Property for **self.__databaseBackupCount** attribute.

        :return: self.__databaseBackupCount.
        :rtype: unicode
        """

        return self.__databaseBackupCount

    @databaseBackupCount.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def databaseBackupCount(self, value):
        """
        Setter for **self.__databaseBackupCount** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseBackupCount"))

    @databaseBackupCount.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def databaseBackupCount(self):
        """
        Deleter for **self.__databaseBackupCount** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseBackupCount"))

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

        self.activated = True
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def deactivate(self):
        """
        Deactivates the Component.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

    def initialize(self):
        """
        Initializes the Component.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

        LOGGER.debug("> Initializing '{0}' SQLiteDatabase.".format(Constants.database_file))
        if self.__engine.parameters.database_directory:
            if foundations.common.path_exists(self.__engine.parameters.database_directory):
                self.__database_name = os.path.join(
                    self.__engine.parameters.database_directory, Constants.database_file)
            else:
                raise foundations.exceptions.DirectoryExistsError(
                    "{0} | '{1}' Database storing directory doesn't exists, {2} will now close!".format(
                        self.__class__.__name__, self.__engine.parameters.database_directory,
                        Constants.application_name))
        else:
            self.__database_name = os.path.join(self.__engine.user_application_data_directory,
                                                Constants.database_directory,
                                                Constants.database_file)

        LOGGER.info("{0} | Session Database location: '{1}'.".format(self.__class__.__name__, self.__database_name))
        self.__databaseConnectionString = "sqlite:///{0}".format(self.__database_name)

        if foundations.common.path_exists(self.__database_name):
            if not self.__engine.parameters.database_read_only:
                backupDestination = os.path.join(os.path.dirname(self.database_name), self.__databaseBackupDirectory)

                LOGGER.info("{0} | Backing up '{1}' Database to '{2}'!".format(self.__class__.__name__,
                                                                               Constants.database_file,
                                                                               backupDestination))
                rotating_backup = RotatingBackup(self.__database_name, backupDestination, self.__databaseBackupCount)
                rotating_backup.backup()
            else:
                LOGGER.info("{0} | Database backup deactivated by '{1}' command line parameter value!".format(
                    self.__class__.__name__, "database_read_only"))

        LOGGER.info("{0} | Migrating Database schema.".format(self.__class__.__name__))
        LOGGER.info("{0} | Alembic configuration file: '{1}'.".format(
            self.__class__.__name__, ALEMBIC_CONFIGURATION_FILE))
        LOGGER.info("{0} | Alembic scripts directory: '{1}'.".format(
            self.__class__.__name__, ALEMBIC_SCRIPTS_DIRECTORY))
        alembic_configuration = Config(ALEMBIC_CONFIGURATION_FILE)
        alembic_configuration.set_main_option("sqlalchemy.url", self.__databaseConnectionString)
        alembic_configuration.set_main_option("script_location", ALEMBIC_SCRIPTS_DIRECTORY)
        alembic.command.upgrade(alembic_configuration, "head")

        LOGGER.debug("> Creating Database engine.")
        self.__database_engine = sqlalchemy.create_engine(self.__databaseConnectionString)

        LOGGER.debug("> Creating Database metadata.")
        self.__databaseCatalog = Base.metadata
        self.__databaseCatalog.create_all(self.__database_engine)

        LOGGER.debug("> Initializing Database session.")
        self.__database_session_maker = sibl_gui.components.core.database.operations.DEFAULT_SESSION_MAKER = \
            sqlalchemy.orm.sessionmaker(bind=self.__database_engine)

        self.__database_session = sibl_gui.components.core.database.operations.DEFAULT_SESSION = \
            self.__database_session_maker()

        self.initialized = True
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def uninitialize(self):
        """
        Uninitializes the Component.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' Component cannot be uninitialized!".format(self.__class__.__name__, self.name))

    def commit(self):
        """
        Commits pending changes in the Database.

        :return: Method success.
        :rtype: bool
        """

        return sibl_gui.components.core.database.operations.commit(self.__database_session)
