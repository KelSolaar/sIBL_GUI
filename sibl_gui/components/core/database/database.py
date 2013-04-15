#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**database.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Database` Component Interface class.

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
import sqlalchemy.orm

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.verbose
import sibl_gui.components.core.database.operations
from foundations.rotatingBackup import RotatingBackup
from manager.component import Component
from sibl_gui.components.core.database.types import Base
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Database"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Database(Component):
	"""
	| This class is the :mod:`sibl_gui.components.core.database.database` Component Interface class.
	| It provides Application Database creation and session, proceeds to its backup using
		the :mod:`foundations.rotatingBackup`.
	"""

	def __init__(self, name=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Component.__init__(self, name=name)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__engine = None

		self.__databaseName = None
		self.__databaseSession = None
		self.__databaseSessionMaker = None
		self.__databaseEngine = None
		self.__databaseCatalog = None

		self.__databaseConnectionString = None

		self.__databaseBackupDirectory = "backup"
		self.__databaseBackupCount = 6

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def engine(self):
		"""
		This method is the property for **self.__engine** attribute.

		:return: self.__engine. ( QObject )
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def databaseName(self):
		"""
		This method is the property for **self.__databaseName** attribute.

		:return: self.__databaseName. ( String )
		"""

		return self.__databaseName

	@databaseName.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseName(self, value):
		"""
		This method is the setter method for **self.__databaseName** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseName"))

	@databaseName.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseName(self):
		"""
		This method is the deleter method for **self.__databaseName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseName"))

	@property
	def databaseEngine(self):
		"""
		This method is the property for **self.__databaseEngine** attribute.

		:return: self.__databaseEngine. ( Object )
		"""

		return self.__databaseEngine

	@databaseEngine.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseEngine(self, value):
		"""
		This method is the setter method for **self.__databaseEngine** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseEngine"))

	@databaseEngine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseEngine(self):
		"""
		This method is the deleter method for **self.__databaseEngine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseEngine"))

	@property
	def databaseCatalog(self):
		"""
		This method is the property for **self.__databaseCatalog** attribute.

		:return: self.__databaseCatalog. ( Object )
		"""

		return self.__databaseCatalog

	@databaseCatalog.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseCatalog(self, value):
		"""
		This method is the setter method for **self.__databaseCatalog** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseCatalog"))

	@databaseCatalog.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseCatalog(self):
		"""
		This method is the deleter method for **self.__databaseCatalog** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseCatalog"))

	@property
	def databaseSession(self):
		"""
		This method is the property for **self.__databaseSession** attribute.

		:return: self.__databaseSession. ( Object )
		"""

		return self.__databaseSession

	@databaseSession.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseSession(self, value):
		"""
		This method is the setter method for **self.__databaseSession** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseSession"))

	@databaseSession.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseSession(self):
		"""
		This method is the deleter method for **self.__databaseSession** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseSession"))

	@property
	def databaseSessionMaker(self):
		"""
		This method is the property for **self.__databaseSessionMaker** attribute.

		:return: self.__databaseSessionMaker. ( Object )
		"""

		return self.__databaseSessionMaker

	@databaseSessionMaker.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseSessionMaker(self, value):
		"""
		This method is the setter method for **self.__databaseSessionMaker** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseSessionMaker"))

	@databaseSessionMaker.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseSessionMaker(self):
		"""
		This method is the deleter method for **self.__databaseSessionMaker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseSessionMaker"))

	@property
	def databaseConnectionString(self):
		"""
		This method is the property for **self.__databaseConnectionString** attribute.

		:return: self.__databaseConnectionString. ( String )
		"""

		return self.__databaseConnectionString

	@databaseConnectionString.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseConnectionString(self, value):
		"""
		This method is the setter method for **self.__databaseConnectionString** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseConnectionString"))

	@databaseConnectionString.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseConnectionString(self):
		"""
		This method is the deleter method for **self.__databaseConnectionString** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseConnectionString"))

	@property
	def databaseBackupDirectory(self):
		"""
		This method is the property for **self.__databaseBackupDirectory** attribute.

		:return: self.__databaseBackupDirectory. ( String )
		"""

		return self.__databaseBackupDirectory

	@databaseBackupDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseBackupDirectory(self, value):
		"""
		This method is the setter method for **self.__databaseBackupDirectory** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseBackupDirectory"))

	@databaseBackupDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseBackupDirectory(self):
		"""
		This method is the deleter method for **self.__databaseBackupDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseBackupDirectory"))

	@property
	def databaseBackupCount(self):
		"""
		This method is the property for **self.__databaseBackupCount** attribute.

		:return: self.__databaseBackupCount. ( String )
		"""

		return self.__databaseBackupCount

	@databaseBackupCount.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseBackupCount(self, value):
		"""
		This method is the setter method for **self.__databaseBackupCount** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseBackupCount"))

	@databaseBackupCount.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def databaseBackupCount(self):
		"""
		This method is the deleter method for **self.__databaseBackupCount** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseBackupCount"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine

		self.activated = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	def initialize(self):
		"""
		This method initializes the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

		LOGGER.debug("> Initializing '{0}' SQLiteDatabase.".format(Constants.databaseFile))
		if self.__engine.parameters.databaseDirectory:
			if foundations.common.pathExists(self.__engine.parameters.databaseDirectory):
				self.__databaseName = os.path.join(self.__engine.parameters.databaseDirectory, Constants.databaseFile)
			else:
				raise foundations.exceptions.DirectoryExistsError(
				"{0} | '{1}' Database storing directory doesn't exists, {2} will now close!".format(
				self.__class__.__name__, self.__engine.parameters.databaseDirectory, Constants.applicationName))
		else:
			self.__databaseName = os.path.join(self.__engine.userApplicationDataDirectory,
										Constants.databaseDirectory,
										Constants.databaseFile)

		LOGGER.info("{0} | Session Database location: '{1}'.".format(self.__class__.__name__, self.__databaseName))
		self.__databaseConnectionString = "sqlite:///{0}".format(self.__databaseName)

		if foundations.common.pathExists(self.__databaseName):
			if not self.__engine.parameters.databaseReadOnly:
				backupDestination = os.path.join(os.path.dirname(self.databaseName), self.__databaseBackupDirectory)

				LOGGER.info("{0} | Backing up '{1}' Database to '{2}'!".format(self.__class__.__name__,
																				Constants.databaseFile,
																				backupDestination))
				rotatingBackup = RotatingBackup(self.__databaseName, backupDestination, self.__databaseBackupCount)
				rotatingBackup.backup()
			else:
				LOGGER.info("{0} | Database backup deactivated by '{1}' command line parameter value!".format(
				self.__class__.__name__, "databaseReadOnly"))

		LOGGER.debug("> Creating Database engine.")
		self.__databaseEngine = sqlalchemy.create_engine(self.__databaseConnectionString)

		LOGGER.debug("> Creating Database metadata.")
		self.__databaseCatalog = Base.metadata
		self.__databaseCatalog.create_all(self.__databaseEngine)

		LOGGER.debug("> Initializing Database session.")
		self.__databaseSessionMaker = sibl_gui.components.core.database.operations.DEFAULT_SESSION_MAKER = \
		sqlalchemy.orm.sessionmaker(bind=self.__databaseEngine)

		self.__databaseSession = sibl_gui.components.core.database.operations.DEFAULT_SESSION = \
		self.__databaseSessionMaker()

		self.initialized = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uninitialize(self):
		"""
		This method uninitializes the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def commit(self):
		"""
		This method commits pending changes in the Database.
	
		:return: Method success. ( Boolean )
		"""

		return sibl_gui.components.core.database.operations.commit(self.__databaseSession)
