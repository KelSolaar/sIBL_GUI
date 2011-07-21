#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**db.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Database Backup Component Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
import migrate.exceptions
import migrate.versioning.api
import sqlalchemy.orm
import shutil

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from foundations.rotatingBackup import RotatingBackup
from foundations.walker import Walker
from manager.component import Component
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Db(Component):
	"""
	This Class Is The Db Class.
	"""

	@core.executionTrace
	def __init__(self, name=None):
		"""
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		Component.__init__(self, name=name)

		# --- Setting Class Attributes. ---
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

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def dbName(self):
		"""
		This Method Is The Property For The _dbName Attribute.

		@return: self.__dbName. ( String )
		"""

		return self.__dbName

	@dbName.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbName(self, value):
		"""
		This Method Is The Setter Method For The _dbName Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbName"))

	@dbName.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbName(self):
		"""
		This Method Is The Deleter Method For The _dbName Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbName"))

	@property
	def dbEngine(self):
		"""
		This Method Is The Property For The _dbEngine Attribute.

		@return: self.__dbEngine. ( Object )
		"""

		return self.__dbEngine

	@dbEngine.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbEngine(self, value):
		"""
		This Method Is The Setter Method For The _dbEngine Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbEngine"))

	@dbEngine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbEngine(self):
		"""
		This Method Is The Deleter Method For The _dbEngine Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbEngine"))

	@property
	def dbCatalog(self):
		"""
		This Method Is The Property For The _dbCatalog Attribute.

		@return: self.__dbCatalog. ( Object )
		"""

		return self.__dbCatalog

	@dbCatalog.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbCatalog(self, value):
		"""
		This Method Is The Setter Method For The _dbCatalog Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbCatalog"))

	@dbCatalog.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbCatalog(self):
		"""
		This Method Is The Deleter Method For The _dbCatalog Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbCatalog"))

	@property
	def dbSession(self):
		"""
		This Method Is The Property For The _dbSession Attribute.

		@return: self.__dbSession. ( Object )
		"""

		return self.__dbSession

	@dbSession.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSession(self, value):
		"""
		This Method Is The Setter Method For The _dbSession Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbSession"))

	@dbSession.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSession(self):
		"""
		This Method Is The Deleter Method For The _dbSession Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbSession"))

	@property
	def dbSessionMaker(self):
		"""
		This Method Is The Property For The _dbSessionMaker Attribute.

		@return: self.__dbSessionMaker. ( Object )
		"""

		return self.__dbSessionMaker

	@dbSessionMaker.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSessionMaker(self, value):
		"""
		This Method Is The Setter Method For The _dbSessionMaker Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbSessionMaker"))

	@dbSessionMaker.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSessionMaker(self):
		"""
		This Method Is The Deleter Method For The _dbSessionMaker Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbSessionMaker"))

	@property
	def connectionString(self):
		"""
		This Method Is The Property For The _connectionString Attribute.

		@return: self.__connectionString. ( String )
		"""

		return self.__connectionString

	@connectionString.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def connectionString(self, value):
		"""
		This Method Is The Setter Method For The _connectionString Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("connectionString"))

	@connectionString.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def connectionString(self):
		"""
		This Method Is The Deleter Method For The _connectionString Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("connectionString"))

	@property
	def dbMigrationsRepositoryDirectory(self):
		"""
		This Method Is The Property For The _dbMigrationsRepositoryDirectory Attribute.

		@return: self.__dbMigrationsRepositoryDirectory. ( String )
		"""

		return self.__dbMigrationsRepositoryDirectory

	@dbMigrationsRepositoryDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbMigrationsRepositoryDirectory(self, value):
		"""
		This Method Is The Setter Method For The _dbMigrationsRepositoryDirectory Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbMigrationsRepositoryDirectory"))

	@dbMigrationsRepositoryDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbMigrationsRepositoryDirectory(self):
		"""
		This Method Is The Deleter Method For The _dbMigrationsRepositoryDirectory Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbMigrationsRepositoryDirectory"))

	@property
	def dbMigrationsTemplatesDirectory(self):
		"""
		This Method Is The Property For The _dbMigrationsTemplatesDirectory Attribute.

		@return: self.__dbMigrationsTemplatesDirectory. ( String )
		"""

		return self.__dbMigrationsTemplatesDirectory

	@dbMigrationsTemplatesDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbMigrationsTemplatesDirectory(self, value):
		"""
		This Method Is The Setter Method For The _dbMigrationsTemplatesDirectory Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbMigrationsTemplatesDirectory"))

	@dbMigrationsTemplatesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbMigrationsTemplatesDirectory(self):
		"""
		This Method Is The Deleter Method For The _dbMigrationsTemplatesDirectory Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbMigrationsTemplatesDirectory"))

	@property
	def dbBackupDirectory(self):
		"""
		This Method Is The Property For The _dbBackupDirectory Attribute.

		@return: self.__dbBackupDirectory. ( String )
		"""

		return self.__dbBackupDirectory

	@dbBackupDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbBackupDirectory(self, value):
		"""
		This Method Is The Setter Method For The _dbBackupDirectory Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbBackupDirectory"))

	@dbBackupDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbBackupDirectory(self):
		"""
		This Method Is The Deleter Method For The _dbBackupDirectory Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbBackupDirectory"))

	@property
	def dbBackupCount(self):
		"""
		This Method Is The Property For The _dbBackupCount Attribute.

		@return: self.__dbBackupCount. ( String )
		"""

		return self.__dbBackupCount

	@dbBackupCount.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbBackupCount(self, value):
		"""
		This Method Is The Setter Method For The _dbBackupCount Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbBackupCount"))

	@dbBackupCount.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbBackupCount(self):
		"""
		This Method Is The Deleter Method For The _dbBackupCount Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbBackupCount"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__container = container

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		messageBox.messageBox("Warning", "Warning", "{0} Component Cannot Be Deactivated!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiSystemExitExceptionHandler, False, OSError, Exception)
	def initialize(self):
		"""
		This Method Initializes The Component.
		"""

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

		LOGGER.debug("> Initializing '{0}' SQLite Database.".format(Constants.databaseFile))
		if self.__container.parameters.databaseDirectory:
			if os.path.exists(self.__container.parameters.databaseDirectory):
				self.__dbName = os.path.join(self.__container.parameters.databaseDirectory, Constants.databaseFile)
				self.__dbMigrationsRepositoryDirectory = os.path.join(self.__container.parameters.databaseDirectory, Constants.databaseMigrationsDirectory)
			else:
				raise OSError, "'{0}' Database Storing Directory Doesn't Exists, {1} Will Now Close!".format(self.__container.parameters.databaseDirectory, Constants.applicationName)
		else:
			self.__dbName = os.path.join(self.__container.userApplicationDatasDirectory , Constants.databaseDirectory, Constants.databaseFile)
			self.__dbMigrationsRepositoryDirectory = os.path.join(self.__container.userApplicationDatasDirectory , Constants.databaseDirectory, Constants.databaseMigrationsDirectory)

		LOGGER.info("{0} | Session Database Location: '{1}'.".format(self.__class__.__name__, self.__dbName))
		self.__connectionString = "sqlite:///{0}".format(self.__dbName)

		if os.path.exists(self.__dbName):
			if not self.__container.parameters.databaseReadOnly:
					backupDestination = os.path.join(os.path.dirname(self.dbName), self.__dbBackupDirectory)

					LOGGER.info("{0} | Backing Up '{1}' Database To '{2}'!".format(self.__class__.__name__, Constants.databaseFile, backupDestination))
					rotatingBackup = RotatingBackup(self.__dbName, backupDestination, self.__dbBackupCount)
					rotatingBackup.backup()
			else:
				LOGGER.info("{0} | Database Backup Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		if not self.__container.parameters.databaseReadOnly:
			LOGGER.info("{0} | SQLAlchemy Migrate Repository Location: '{1}'.".format(self.__class__.__name__, self.__dbMigrationsRepositoryDirectory))
			LOGGER.debug("> Creating SQLAlchemy Migrate Migrations Directory And Requisites.")
			try:
				repositoryTemplate = os.path.join(os.path.dirname(__file__), Constants.databaseMigrationsDirectory, Constants.databaseMigrationsTemplatesDirectory)
				migrate.versioning.api.create(self.__dbMigrationsRepositoryDirectory, "Migrations", version_table="Migrate", templates_path=repositoryTemplate)
			except migrate.exceptions.KnownError:
				LOGGER.debug("> SQLAlchemy Migrate Repository Directory Already Exists!")

			LOGGER.debug("> Copying Migrations Files To SQLAlchemy Migrate Repository.")
			walker = Walker(os.path.join(os.path.dirname(__file__), Constants.databaseMigrationsDirectory, Constants.databaseMigrationsFilesDirectory))
			walker.walk(filtersIn=(Constants.databaseMigrationsFilesExtension,))
			for file in walker.files.values():
				shutil.copy(file, os.path.join(self.__dbMigrationsRepositoryDirectory, Constants.databaseMigrationsFilesDirectory))

			if os.path.exists(self.__dbName):
				LOGGER.debug("> Placing Database Under SQLAlchemy Migrate Version Control.")
				try:
					migrate.versioning.api.version_control(self.__connectionString, self.__dbMigrationsRepositoryDirectory)
				except migrate.exceptions.DatabaseAlreadyControlledError:
					LOGGER.debug("> Database Is Already Under SQLAlchemy Migrate Version Control!")

				LOGGER.debug("> Upgrading Database.")
				migrate.versioning.api.upgrade(self.__connectionString, self.__dbMigrationsRepositoryDirectory)
		else:
			LOGGER.info("{0} | SQLAlchemy Migrate Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		LOGGER.debug("> Creating Database Engine.")
		self.__dbEngine = sqlalchemy.create_engine(self.__connectionString)

		LOGGER.debug("> Creating Database Metadatas.")
		self.__dbCatalog = dbUtilities.types.DbBase.metadata
		self.__dbCatalog.create_all(self.__dbEngine)

		LOGGER.debug("> Initializing Database Session.")
		self.__dbSessionMaker = sqlalchemy.orm.sessionmaker(bind=self.__dbEngine)

		self.__dbSession = self.__dbSessionMaker()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitialize(self):
		"""
		This Method Uninitializes The Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Cannot Be Uninitialized!".format(self.name))

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
