#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**setsScanner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Sets Scanner Component Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace
import umbra.components.core.db.dbUtilities.common as dbCommon
import umbra.components.core.db.dbUtilities.types as dbTypes
import umbra.ui.widgets.messageBox as messageBox
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
class SetsScanner_Worker(QThread):
	"""
	This class is the **SetsScanner_Worker** class.
	"""

	# Custom signals definitions.
	databaseChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, container):
		"""
		This method initializes the class.

		:param container: Object container. ( Object )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QThread.__init__(self)

		# --- Setting class attributes. ---
		self.__container = container

		self.__dbSession = self.__container.coreDb.dbSessionMaker()

		self.__extension = "ibl"

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
	def extension(self):
		"""
		This method is the property for **self.__extension** attribute.

		:return: self.__extension. ( String )
		"""

		return self.__extension

	@extension.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self, value):
		"""
		This method is the setter method for **self.__extension** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("extension"))

	@extension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		This method is the deleter method for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("extension"))

	@property
	def newIblSets(self):
		"""
		This method is the property for **self.__newIblSets** attribute.

		:return: self.__newIblSets. ( Dictionary )
		"""

		return self.__newIblSets

	@newIblSets.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def newIblSets(self, value):
		"""
		This method is the setter method for **self.__newIblSets** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("newIblSets"))

	@newIblSets.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def newIblSets(self):
		"""
		This method is the deleter method for **self.__newIblSets** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("newIblSets"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def run(self):
		"""
		This method starts the QThread.
		"""

		self.scanIblSetsDirectories()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def scanIblSetsDirectories(self):
		"""
		This method scans Ibl Sets directories.

		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Scanning Ibl Sets directories for new Ibl Sets!".format(self.__class__.__name__))

		self.__newIblSets = {}
		paths = [path[0] for path in self.__dbSession.query(dbTypes.DbIblSet.path).all()]
		directories = set((os.path.normpath(os.path.join(os.path.dirname(path), "..")) for path in paths))
		needModelRefresh = False
		for directory in directories:
			if os.path.exists(directory):
				walker = Walker(directory)
				walker.walk(("\.{0}$".format(self.__extension),), ("\._",))
				for iblSet, path in walker.files.items():
					if not dbCommon.filterIblSets(self.__dbSession, "^{0}$".format(re.escape(path)), "path"):
						needModelRefresh = True
						self.__newIblSets[iblSet] = path
			else:
				LOGGER.warning("!> '{0}' directory doesn't exists and won't be scanned for new Ibl Sets!".format(directory))

		self.__dbSession.close()

		LOGGER.info("{0} | Scanning done!".format(self.__class__.__name__))
		needModelRefresh and self.emit(SIGNAL("databaseChanged()"))
		return True

class SetsScanner(Component):
	"""
	This class is the **SetsScanner** class.
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
		self.deactivatable = True

		self.__container = None

		self.__coreDb = None
		self.__coreCollectionsOutliner = None

		self.__setsScannerWorkerThread = None

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
	def coreDb(self):
		"""
		This method is the property for **self.__coreDb** attribute.

		:return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This method is the setter method for **self.__coreDb** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for **self.__coreDb** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDb"))

	@property
	def coreCollectionsOutliner(self):
		"""
		This method is the property for **self.__coreCollectionsOutliner** attribute.

		:return: self.__coreCollectionsOutliner. ( Object )
		"""

		return self.__coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		"""
		This method is the setter method for **self.__coreCollectionsOutliner** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This method is the deleter method for **self.__coreCollectionsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreCollectionsOutliner"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def setsScannerWorkerThread(self):
		"""
		This method is the property for **self.__setsScannerWorkerThread** attribute.

		:return: self.__setsScannerWorkerThread. ( QThread )
		"""

		return self.__setsScannerWorkerThread

	@setsScannerWorkerThread.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setsScannerWorkerThread(self, value):
		"""
		This method is the setter method for **self.__setsScannerWorkerThread** attribute.

		:param value: Attribute value. ( QThread )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("setsScannerWorkerThread"))

	@setsScannerWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setsScannerWorkerThread(self):
		"""
		This method is the deleter method for **self.__setsScannerWorkerThread** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("setsScannerWorkerThread"))

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

		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__coreCollectionsOutliner = self.__container.componentsManager.components["core.collectionsOutliner"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__container = None

		self.__coreDb = None
		self.__coreCollectionsOutliner = None
		self.__coreDatabaseBrowser = None

		self._deactivate()

	@core.executionTrace
	def initialize(self):
		"""
		This method initializes the Component.
		"""

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			if not self.__container.parameters.deactivateWorkerThreads:
				self.__setsScannerWorkerThread = SetsScanner_Worker(self)
				self.__container.workerThreads.append(self.__setsScannerWorkerThread)

				# Signals / Slots.
				self.__setsScannerWorkerThread.databaseChanged.connect(self.__coreDb_database__changed)
			else:
				LOGGER.info("{0} | Ibl Sets scanning capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Ibl Sets scanning capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def uninitialize(self):
		"""
		This method uninitializes the Component.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			if not self.__container.parameters.deactivateWorkerThreads:
				# Signals / Slots.
				not self.__container.parameters.databaseReadOnly and self.__setsScannerWorkerThread.databaseChanged.disconnect(self.__coreDb_database__changed)

				self.__setsScannerWorkerThread = None

	@core.executionTrace
	def onStartup(self):
		"""
		This method is called on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework startup method.".format(self.__class__.__name__))

		not self.__container.parameters.databaseReadOnly and not self.__container.parameters.deactivateWorkerThreads and self.__setsScannerWorkerThread.start()

	@core.executionTrace
	def __coreDb_database__changed(self):
		"""
		This method is triggered by the **SetsScanner_Worker** when the Database has changed.
		"""

		if self.__setsScannerWorkerThread.newIblSets:
			if messageBox.messageBox("Question", "Question", "One or more neighbor Ibl Sets have been found! Would you like to add that content: '{0}' to the Database?".format(", ".join((foundations.namespace.getNamespace(iblSet, rootOnly=True) for iblSet in self.__setsScannerWorkerThread.newIblSets.keys()))), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
				for iblSet, path in self.__setsScannerWorkerThread.newIblSets.items():
					iblSet = foundations.namespace.getNamespace(iblSet, rootOnly=True)
					LOGGER.info("{0} | Adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, iblSet))
					if not dbCommon.addIblSet(self.__coreDb.dbSession, iblSet, path, self.__coreCollectionsOutliner.getCollectionId(self.__coreCollectionsOutliner.defaultCollection)):
						LOGGER.error("!>{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, iblSet))

				self.__coreDatabaseBrowser.emit(SIGNAL("modelRefresh()"))

		self.__setsScannerWorkerThread.exit()

