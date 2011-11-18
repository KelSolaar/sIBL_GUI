#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**setsScanner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`SetsScanner` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtGui import QMessageBox

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace
import sibl_gui.components.core.db.utilities.common as dbCommon
import umbra.engine
import umbra.ui.widgets.messageBox as messageBox
from manager.qobjectComponent import QObjectComponent
from sibl_gui.components.addons.setsScanner.workers import SetsScanner_Worker
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "SetsScanner"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class SetsScanner(QObjectComponent):
	"""
	| This class is the :mod:`umbra.components.addons.setsScanner.setsScanner` Component Interface class.
	| It instantiates the :class:`SetsScanner` class on Application startup which will gather new Ibl Sets
	from Database registered directories parents.
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObjectComponent.__init__(self, parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None

		self.__coreDb = None
		self.__coreCollectionsOutliner = None

		self.__setsScannerWorkerThread = None

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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for **self.__coreDb** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDb"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This method is the deleter method for **self.__coreCollectionsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreCollectionsOutliner"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDatabaseBrowser"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "setsScannerWorkerThread"))

	@setsScannerWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setsScannerWorkerThread(self):
		"""
		This method is the deleter method for **self.__setsScannerWorkerThread** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "setsScannerWorkerThread"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine

		self.__coreDb = self.__engine.componentsManager.components["core.db"].interface
		self.__coreCollectionsOutliner = self.__engine.componentsManager.components["core.collectionsOutliner"].interface
		self.__coreDatabaseBrowser = self.__engine.componentsManager.components["core.databaseBrowser"].interface

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.__coreDb = None
		self.__coreCollectionsOutliner = None
		self.__coreDatabaseBrowser = None

		self.activated = False
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initialize(self):
		"""
		This method initializes the Component.
		"""

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				self.__setsScannerWorkerThread = SetsScanner_Worker(self)
				self.__engine.workerThreads.append(self.__setsScannerWorkerThread)

				# Signals / Slots.
				self.__setsScannerWorkerThread.iblSetsRetrieved.connect(self.__setsScannerWorkerThread__iblSetsRetrieved)
			else:
				LOGGER.info("{0} | Ibl Sets scanning capabilities deactivated by '{1}' command line parameter value!".format(
				self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Ibl Sets scanning capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def uninitialize(self):
		"""
		This method uninitializes the Component.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				# Signals / Slots.
				not self.__engine.parameters.databaseReadOnly and \
				self.__setsScannerWorkerThread.iblSetsRetrieved.disconnect(
				self.__setsScannerWorkerThread__iblSetsRetrieved)

				self.__setsScannerWorkerThread = None

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def onStartup(self):
		"""
		This method is called on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		not self.__engine.parameters.databaseReadOnly and \
		not self.__engine.parameters.deactivateWorkerThreads and self.__setsScannerWorkerThread.start()
		return True

	@core.executionTrace
	@umbra.engine.encapsulateProcessing
	def __setsScannerWorkerThread__iblSetsRetrieved(self, iblSets):
		"""
		This method is triggered by the **SetsScanner_Worker** when the Database has changed.

		:param iblSets: Retrieve Ibl Sets. ( Dictionary )
		"""

		if messageBox.messageBox("Question", "Question",
		"One or more neighbor Ibl Sets have been found! Would you like to add that content: '{0}' to the Database?".format(
		", ".join((foundations.namespace.getNamespace(iblSet, rootOnly=True) for iblSet in iblSets.keys()))),
		 buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.startProcessing("Adding Retrieved Ibl Sets ...", len(iblSets.keys()))
			for iblSet, path in iblSets.items():
				iblSet = foundations.namespace.getNamespace(iblSet, rootOnly=True)
				LOGGER.info("{0} | Adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, iblSet))
				if not dbCommon.addIblSet(self.__coreDb.dbSession,
				 						iblSet,
										path,
										self.__coreCollectionsOutliner.getCollectionId(
										self.__coreCollectionsOutliner.defaultCollection)):
					LOGGER.error("!>{0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(
					self.__class__.__name__, iblSet))
				self.__engine.stepProcessing()
			self.__engine.stopProcessing()

			self.__coreDatabaseBrowser.modelRefresh.emit()
