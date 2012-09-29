#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**databaseOperations.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`DatabaseOperations` Component Interface class and others helper objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
from PyQt4.QtCore import QString
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QMessageBox

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import sibl_gui.components.core.db.utilities.common as dbCommon
import umbra.engine
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "DbType", "DatabaseOperations"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Database_Operations.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class DbType(foundations.dataStructures.Structure):
	"""
	| This class represents a storage object for manipulation methods associated to a given Database type.
	| See :mod:`sibl_gui.components.core.db.utilities.types` module for more informations
		about the available Database types.
	"""

	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: type, getMethod, updateContentMethod, removeMethod, modelContainer, updateLocationMethod ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class DatabaseOperations(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.addons.databaseOperations.databaseOperations` Component Interface class.
	| It provides various methods to operate on the Database.
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

		super(DatabaseOperations, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__db = None
		self.__preferencesManager = None
		self.__databaseBrowser = None
		self.__templatesOutliner = None

		self.__dbTypes = None

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
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settingsSection(self):
		"""
		This method is the property for **self.__settingsSection** attribute.

		:return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for **self.__settingsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def db(self):
		"""
		This method is the property for **self.__db** attribute.

		:return: self.__db. ( Object )
		"""

		return self.__db

	@db.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def db(self, value):
		"""
		This method is the setter method for **self.__db** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "db"))

	@db.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def db(self):
		"""
		This method is the deleter method for **self.__db** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "db"))

	@property
	def preferencesManager(self):
		"""
		This method is the property for **self.__preferencesManager** attribute.

		:return: self.__preferencesManager. ( QWidget )
		"""

		return self.__preferencesManager

	@preferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesManager(self, value):
		"""
		This method is the setter method for **self.__preferencesManager** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "preferencesManager"))

	@preferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesManager(self):
		"""
		This method is the deleter method for **self.__preferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preferencesManager"))

	@property
	def databaseBrowser(self):
		"""
		This method is the property for **self.__databaseBrowser** attribute.

		:return: self.__databaseBrowser. ( QWidget )
		"""

		return self.__databaseBrowser

	@databaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseBrowser(self, value):
		"""
		This method is the setter method for **self.__databaseBrowser** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseBrowser"))

	@databaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseBrowser(self):
		"""
		This method is the deleter method for **self.__databaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseBrowser"))

	@property
	def templatesOutliner(self):
		"""
		This method is the property for **self.__templatesOutliner** attribute.

		:return: self.__templatesOutliner. ( QWidget )
		"""

		return self.__templatesOutliner

	@templatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesOutliner(self, value):
		"""
		This method is the setter method for **self.__templatesOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesOutliner"))

	@templatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesOutliner(self):
		"""
		This method is the deleter method for **self.__templatesOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesOutliner"))

	@property
	def dbTypes(self):
		"""
		This method is the property for **self.__dbTypes** attribute.

		:return: self.__dbTypes. ( Tuple )
		"""

		return self.__dbTypes

	@dbTypes.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbTypes(self, value):
		"""
		This method is the setter method for **self.__dbTypes** attribute.

		:param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dbTypes"))

	@dbTypes.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbTypes(self):
		"""
		This method is the deleter method for **self.__dbTypes** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dbTypes"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__db = self.__engine.componentsManager["core.db"]
		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]
		self.__databaseBrowser = self.__engine.componentsManager["core.databaseBrowser"]
		self.__templatesOutliner = self.__engine.componentsManager["core.templatesOutliner"]

		self.__dbTypes = (DbType(type="Ibl Set",
						getMethod=dbCommon.getIblSets,
						updateContentMethod=dbCommon.updateIblSetContent,
						removeMethod=dbCommon.removeIblSet,
						modelContainer=self.__databaseBrowser,
						updateLocationMethod=self.__databaseBrowser.updateIblSetLocation),
						DbType(type="Template",
						getMethod=dbCommon.getTemplates,
						updateContentMethod=dbCommon.updateTemplateContent,
						removeMethod=dbCommon.removeTemplate,
						modelContainer=self.__templatesOutliner,
						updateLocationMethod=self.__templatesOutliner.updateTemplateLocation))

		self.activated = True
		return True

	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__preferencesManager = None
		self.__databaseBrowser = None
		self.__templatesOutliner = None

		self.activated = False
		return True

	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		if not self.__engine.parameters.databaseReadOnly:
			self.Synchronize_Database_pushButton.clicked.connect(self.__Synchronize_Database_pushButton__clicked)
			self.Remove_Invalid_Data_pushButton.clicked.connect(self.__Remove_Invalid_Data_pushButton__clicked)
		else:
			LOGGER.info(
			"{0} | Database Operations capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		self.initializedUi = True
		return True

	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		if not self.__engine.parameters.databaseReadOnly:
			self.Synchronize_Database_pushButton.clicked.disconnect(self.__Synchronize_Database_pushButton__clicked)
			self.Remove_Invalid_Data_pushButton.clicked.disconnect(self.__Remove_Invalid_Data_pushButton__clicked)

		self.initializedUi = False
		return True

	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.Database_Operations_groupBox)

		return True

	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.Database_Operations_groupBox.setParent(None)

		return True

	def __Synchronize_Database_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Synchronize_Database_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.synchronizeDatabase()

	def __Remove_Invalid_Data_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Remove_Invalid_Data_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.removeInvalidData()

	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	@umbra.engine.showProcessing("Synchronizing Database ...")
	def synchronizeDatabase(self):
		"""
		| This method synchronizes the Database.
		| Each type defined by :meth:`DatabaseOperations.dbTypes` attribute
			will have its instances checked and updated by their associated methods.

		:return: Method success. ( Boolean )
		"""

		for dbType in self.__dbTypes:
			for item in dbType.getMethod(self.__db.dbSession):
				if foundations.common.pathExists(item.path):
					if dbType.updateContentMethod(self.__db.dbSession, item):
						LOGGER.info("{0} | '{1}' {2} has been synchronized!".format(self.__class__.__name__,
																					item.name,
																					dbType.type))
				else:
					choice = messageBox.messageBox("Question", "Error",
					"{0} | '{1}' {2} file is missing, would you like to update it's location?".format(
					self.__class__.__name__, item.name, dbType.type),
					QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No,
					customButtons=((QString("No To All"), QMessageBox.RejectRole),))

					if choice == 0:
							break

					if choice == QMessageBox.Yes:
						dbType.updateLocationMethod(item)
				self.__engine.processEvents()
			dbType.modelContainer.modelRefresh.emit()
		self.__engine.stopProcessing()
		self.__engine.notificationsManager.notify("{0} | Database synchronization done!".format(self.__class__.__name__))
		return True

	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	@umbra.engine.showProcessing("Removing Invalid Data ...")
	def removeInvalidData(self):
		"""
		This method removes invalid data from the Database.

		:return: Method success. ( Boolean )
		"""

		if messageBox.messageBox("Question", "Question",
		"Are you sure you want to remove invalid data from the Database?",
		buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			for dbType in self.__dbTypes:
				for item in dbType.getMethod(self.__db.dbSession):
					if foundations.common.pathExists(item.path):
						continue

					LOGGER.info("{0} | Removing non existing '{1}' {2} from the Database!".format(self.__class__.__name__,
																								item.name,
																								dbType.type))
					dbType.removeMethod(self.__db.dbSession, item.id)

					self.__engine.processEvents()
				dbType.modelContainer.modelRefresh.emit()
			self.__engine.stopProcessing()
			self.__engine.notificationsManager.notify(
			"{0} | Invalid data removed from Database!".format(self.__class__.__name__))
		return True
