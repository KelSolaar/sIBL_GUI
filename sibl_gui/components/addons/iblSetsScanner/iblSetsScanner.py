#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**iblSetsScanner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`IblSetsScanner` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtGui import QMessageBox

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.namespace
import foundations.verbose
import sibl_gui.components.core.database.operations
import umbra.engine
import umbra.ui.widgets.messageBox as messageBox
from manager.qobjectComponent import QObjectComponent
from sibl_gui.components.addons.iblSetsScanner.workers import IblSetsScanner_worker

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "IblSetsScanner"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class IblSetsScanner(QObjectComponent):
	"""
	| This class is the :mod:`sibl_gui.components.addons.iblSetsScanner.iblSetsScanner` Component Interface class.
	| It instantiates the :class:`IblSetsScanner` class on Application startup which will gather new Ibl Sets
		from Database registered directories parents.
	"""

	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObjectComponent.__init__(self, parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None

		self.__collectionsOutliner = None
		self.__iblSetsOutliner = None

		self.__iblSetsScannerWorkerThread = None

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
	def collectionsOutliner(self):
		"""
		This method is the property for **self.__collectionsOutliner** attribute.

		:return: self.__collectionsOutliner. ( QWidget )
		"""

		return self.__collectionsOutliner

	@collectionsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def collectionsOutliner(self, value):
		"""
		This method is the setter method for **self.__collectionsOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "collectionsOutliner"))

	@collectionsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def collectionsOutliner(self):
		"""
		This method is the deleter method for **self.__collectionsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "collectionsOutliner"))

	@property
	def iblSetsOutliner(self):
		"""
		This method is the property for **self.__iblSetsOutliner** attribute.

		:return: self.__iblSetsOutliner. ( QWidget )
		"""

		return self.__iblSetsOutliner

	@iblSetsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self, value):
		"""
		This method is the setter method for **self.__iblSetsOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsOutliner"))

	@iblSetsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self):
		"""
		This method is the deleter method for **self.__iblSetsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsOutliner"))

	@property
	def iblSetsScannerWorkerThread(self):
		"""
		This method is the property for **self.__iblSetsScannerWorkerThread** attribute.

		:return: self.__iblSetsScannerWorkerThread. ( QThread )
		"""

		return self.__iblSetsScannerWorkerThread

	@iblSetsScannerWorkerThread.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsScannerWorkerThread(self, value):
		"""
		This method is the setter method for **self.__iblSetsScannerWorkerThread** attribute.

		:param value: Attribute value. ( QThread )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsScannerWorkerThread"))

	@iblSetsScannerWorkerThread.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsScannerWorkerThread(self):
		"""
		This method is the deleter method for **self.__iblSetsScannerWorkerThread** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsScannerWorkerThread"))

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

		self.__collectionsOutliner = self.__engine.componentsManager["core.collectionsOutliner"]
		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]

		self.activated = True
		return True

	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.__collectionsOutliner = None
		self.__iblSetsOutliner = None

		self.activated = False
		return True

	def initialize(self):
		"""
		This method initializes the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

		self.__iblSetsScannerWorkerThread = IblSetsScanner_worker(self)
		self.__engine.workerThreads.append(self.__iblSetsScannerWorkerThread)

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				# Signals / Slots.
				self.__iblSetsScannerWorkerThread.iblSetsRetrieved.connect(self.__iblSetsScannerWorkerThread__iblSetsRetrieved)
			else:
				LOGGER.info("{0} | Ibl Sets scanning capabilities deactivated by '{1}' command line parameter value!".format(
				self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Ibl Sets scanning capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		self.initialized = True
		return True

	def uninitialize(self):
		"""
		This method uninitializes the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Uninitializing '{0}' Component.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				# Signals / Slots.
				not self.__engine.parameters.databaseReadOnly and \
				self.__iblSetsScannerWorkerThread.iblSetsRetrieved.disconnect(
				self.__iblSetsScannerWorkerThread__iblSetsRetrieved)

		self.__engine.workerThreads.remove(self.__iblSetsScannerWorkerThread)
		self.__iblSetsScannerWorkerThread = None

		self.initialized = False
		return True

	def onStartup(self):
		"""
		This method is triggered on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		not self.__engine.parameters.databaseReadOnly and \
		not self.__engine.parameters.deactivateWorkerThreads and self.__iblSetsScannerWorkerThread.start()
		return True

	@umbra.engine.encapsulateProcessing
	def __iblSetsScannerWorkerThread__iblSetsRetrieved(self, iblSets):
		"""
		This method is triggered by the **IblSetsScanner_worker** when the Database has changed.

		:param iblSets: Retrieve Ibl Sets. ( Dictionary )
		"""

		if messageBox.messageBox("Question", "Question",
		"One or more neighbor Ibl Sets have been found! Would you like to add that content: '{0}' to the Database?".format(
		", ".join(map(foundations.strings.getSplitextBasename, iblSets))),
		 buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.startProcessing("Adding Retrieved Ibl Sets ...", len(iblSets))
			for path in iblSets:
				iblSet = foundations.strings.getSplitextBasename(path)
				LOGGER.info("{0} | Adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, iblSet))
				if not sibl_gui.components.core.database.operations.addIblSet(
				iblSet, path, self.__collectionsOutliner.getCollectionId(self.__collectionsOutliner.defaultCollection)):
					LOGGER.error("!> {0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(
					self.__class__.__name__, iblSet))
				self.__engine.stepProcessing()
			self.__engine.stopProcessing()

			self.__iblSetsOutliner.refreshNodes.emit()
