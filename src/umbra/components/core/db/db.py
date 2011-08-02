#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**db.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Database backup Component Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import migrate.exceptions
import migrate.versioning.api
import sqlalchemy.orm
import shutil

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
import umbra.components.core.db.dbUtilities.types as dbTypes
import umbra.ui.widgets.messageBox as messageBox
from foundations.rotatingBackup import RotatingBackup
from foundations.walker import Walker
from manager.component import Component
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Db(Component):
	"""
	This class is the **Db** class.
	"""

	@core.executionTrace
	def __init__(self, name=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Component.__init__(self, name=name)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__container = None

		self.__dbName = None
		self.__dbSession = None
		self.__dbEngine = None
		self.__dbCatalog = None

		self.__connectionString = None

		self.__dbMigrationsRepositoryDirectory = None
		self.__dbMigrationsTemplatesDirectory = None

		self.__dbBackupDirectory = "backup"
		self.__dbBackupCount = 6

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def dbName(self):
		"""
		This method is the property for **self.__dbName** attribute.

		:return: self.__dbName. ( String )
		"""

		return self.__dbName

	@dbName.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbName(self, value):
		"""
		This method is the setter method for **self.__dbName** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbName"))

	@dbName.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbName(self):
		"""
		This method is the deleter method for **self.__dbName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbName"))

	@property
	def dbEngine(self):
		"""
		This method is the property for **self.__dbEngine** attribute.

		:return: self.__dbEngine. ( Object )
		"""

		return self.__dbEngine

	@dbEngine.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbEngine(self, value):
		"""
		This method is the setter method for **self.__dbEngine** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbEngine"))

	@dbEngine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbEngine(self):
		"""
		This method is the deleter method for **self.__dbEngine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbEngine"))

	@property
	def dbCatalog(self):
		"""
		This method is the property for **self.__dbCatalog** attribute.

		:return: self.__dbCatalog. ( Object )
		"""

		return self.__dbCatalog

	@dbCatalog.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbCatalog(self, value):
		"""
		This method is the setter method for **self.__dbCatalog** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbCatalog"))

	@dbCatalog.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbCatalog(self):
		"""
		This method is the deleter method for **self.__dbCatalog** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbCatalog"))

	@property
	def dbSession(self):
		"""
		This method is the property for **self.__dbSession** attribute.

		:return: self.__dbSession. ( Object )
		"""

		return self.__dbSession

	@dbSession.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSession(self, value):
		"""
		This method is the setter method for **self.__dbSession** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbSession"))

	@dbSession.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSession(self):
		"""
		This method is the deleter method for **self.__dbSession** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbSession"))

	@property
	def dbSessionMaker(self):
		"""
		This method is the property for **self.__dbSessionMaker** attribute.

		:return: self.__dbSessionMaker. ( Object )
		"""

		return self.__dbSessionMaker

	@dbSessionMaker.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSessionMaker(self, value):
		"""
		This method is the setter method for **self.__dbSessionMaker** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbSessionMaker"))

	@dbSessionMaker.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSessionMaker(self):
		"""
		This method is the deleter method for **self.__dbSessionMaker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbSessionMaker"))

	@property
	def connectionString(self):
		"""
		This method is the property for **self.__connectionString** attribute.

		:return: self.__connectionString. ( String )
		"""

		return self.__connectionString

	@connectionString.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def connectionString(self, value):
		"""
		This method is the setter method for **self.__connectionString** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("connectionString"))

	@connectionString.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def connectionString(self):
		"""
		This method is the deleter method for **self.__connectionString** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("connectionString"))

	@property
	def dbMigrationsRepositoryDirectory(self):
		"""
		This method is the property for **self.__dbMigrationsRepositoryDirectory** attribute.

		:return: self.__dbMigrationsRepositoryDirectory. ( String )
		"""

		return self.__dbMigrationsRepositoryDirectory

	@dbMigrationsRepositoryDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbMigrationsRepositoryDirectory(self, value):
		"""
		This method is the setter method for **self.__dbMigrationsRepositoryDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbMigrationsRepositoryDirectory"))

	@dbMigrationsRepositoryDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbMigrationsRepositoryDirectory(self):
		"""
		This method is the deleter method for **self.__dbMigrationsRepositoryDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbMigrationsRepositoryDirectory"))

	@property
	def dbMigrationsTemplatesDirectory(self):
		"""
		This method is the property for **self.__dbMigrationsTemplatesDirectory** attribute.

		:return: self.__dbMigrationsTemplatesDirectory. ( String )
		"""

		return self.__dbMigrationsTemplatesDirectory

	@dbMigrationsTemplatesDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbMigrationsTemplatesDirectory(self, value):
		"""
		This method is the setter method for **self.__dbMigrationsTemplatesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbMigrationsTemplatesDirectory"))

	@dbMigrationsTemplatesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbMigrationsTemplatesDirectory(self):
		"""
		This method is the deleter method for **self.__dbMigrationsTemplatesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbMigrationsTemplatesDirectory"))

	@property
	def dbBackupDirectory(self):
		"""
		This method is the property for **self.__dbBackupDirectory** attribute.

		:return: self.__dbBackupDirectory. ( String )
		"""

		return self.__dbBackupDirectory

	@dbBackupDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbBackupDirectory(self, value):
		"""
		This method is the setter method for **self.__dbBackupDirectory** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbBackupDirectory"))

	@dbBackupDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbBackupDirectory(self):
		"""
		This method is the deleter method for **self.__dbBackupDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbBackupDirectory"))

	@property
	def dbBackupCount(self):
		"""
		This method is the property for **self.__dbBackupCount** attribute.

		:return: self.__dbBackupCount. ( String )
		"""

		return self.__dbBackupCount

	@dbBackupCount.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbBackupCount(self, value):
		"""
		This method is the setter method for **self.__dbBackupCount** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbBackupCount"))

	@dbBackupCount.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbBackupCount(self):
		"""
		This method is the deleter method for **self.__dbBackupCount** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbBackupCount"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__container = container

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		messageBox.messageBox("Warning", "Warning", "{0} Component cannot be deactivated!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiSystemExitExceptionHandler, False, OSError, Exception)
	def initialize(self):
		"""
		This method initializes the Component.
		"""

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

		LOGGER.debug("> Initializing '{0}' SQLiteDatabase.".format(Constants.databaseFile))
		if self.__container.parameters.databaseDirectory:
			if os.path.exists(self.__container.parameters.databaseDirectory):
				self.__dbName = os.path.join(self.__container.parameters.databaseDirectory, Constants.databaseFile)
				self.__dbMigrationsRepositoryDirectory = os.path.join(self.__container.parameters.databaseDirectory, Constants.databaseMigrationsDirectory)
			else:
				raise OSError, "'{0}' Database storing directory doesn't exists, {1} will now close!".format(self.__container.parameters.databaseDirectory, Constants.applicationName)
		else:
			self.__dbName = os.path.join(self.__container.userApplicationDatasDirectory , Constants.databaseDirectory, Constants.databaseFile)
			self.__dbMigrationsRepositoryDirectory = os.path.join(self.__container.userApplicationDatasDirectory , Constants.databaseDirectory, Constants.databaseMigrationsDirectory)

		LOGGER.info("{0} | Session Database location: '{1}'.".format(self.__class__.__name__, self.__dbName))
		self.__connectionString = "sqlite:///{0}".format(self.__dbName)

		if os.path.exists(self.__dbName):
			if not self.__container.parameters.databaseReadOnly:
					backupDestination = os.path.join(os.path.dirname(self.dbName), self.__dbBackupDirectory)

					LOGGER.info("{0} | Backing up '{1}' Database to '{2}'!".format(self.__class__.__name__, Constants.databaseFile, backupDestination))
					rotatingBackup = RotatingBackup(self.__dbName, backupDestination, self.__dbBackupCount)
					rotatingBackup.backup()
			else:
				LOGGER.info("{0} | Database backup deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		if not self.__container.parameters.databaseReadOnly:
			LOGGER.info("{0} | SQLAlchemy Migrate repository location: '{1}'.".format(self.__class__.__name__, self.__dbMigrationsRepositoryDirectory))
			LOGGER.debug("> Creating SQLAlchemy Migrate migrations directory and requisites.")
			try:
				repositoryTemplate = os.path.join(os.path.dirname(__file__), Constants.databaseMigrationsDirectory, Constants.databaseMigrationsTemplatesDirectory)
				migrate.versioning.api.create(self.__dbMigrationsRepositoryDirectory, "Migrations", version_table="Migrate", templates_path=repositoryTemplate)
			except migrate.exceptions.KnownError:
				LOGGER.debug("> SQLAlchemy Migrate repository directory already exists!")

			LOGGER.debug("> Copying migrations files to SQLAlchemy Migrate repository.")
			walker = Walker(os.path.join(os.path.dirname(__file__), Constants.databaseMigrationsDirectory, Constants.databaseMigrationsFilesDirectory))
			walker.walk(filtersIn=(Constants.databaseMigrationsFilesExtension,))
			for file in walker.files.values():
				shutil.copy(file, os.path.join(self.__dbMigrationsRepositoryDirectory, Constants.databaseMigrationsFilesDirectory))

			if os.path.exists(self.__dbName):
				LOGGER.debug("> Placing Database under SQLAlchemy Migrate version control.")
				try:
					migrate.versioning.api.version_control(self.__connectionString, self.__dbMigrationsRepositoryDirectory)
				except migrate.exceptions.DatabaseAlreadyControlledError:
					LOGGER.debug("> Database is already under SQLAlchemy Migrate version control!")

				LOGGER.debug("> Upgrading Database.")
				migrate.versioning.api.upgrade(self.__connectionString, self.__dbMigrationsRepositoryDirectory)
		else:
			LOGGER.info("{0} | SQLAlchemy Migrate deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		LOGGER.debug("> Creating Database engine.")
		self.__dbEngine = sqlalchemy.create_engine(self.__connectionString)

		LOGGER.debug("> Creating Database metadatas.")
		self.__dbCatalog = dbTypes.DbBase.metadata
		self.__dbCatalog.create_all(self.__dbEngine)

		LOGGER.debug("> Initializing Database session.")
		self.__dbSessionMaker = sqlalchemy.orm.sessionmaker(bind=self.__dbEngine)

		self.__dbSession = self.__dbSessionMaker()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitialize(self):
		"""
		This method uninitializes the Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component cannot be uninitialized!".format(self.name))

