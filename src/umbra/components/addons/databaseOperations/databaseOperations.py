#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**databaseOperations.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Database Operations Component Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.components.core.db.dbUtilities.common as dbCommon
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from manager.uiComponent import UiComponent
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
class DbType(core.Structure):
	"""
	This is the DbType class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		@param kwargs: type, getmethod, updatecontentmethod, modelcontainer, updatelocationmethod ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__dict__.update(kwargs)

class DatabaseOperations(UiComponent):
	"""
	This class is the DatabaseOperations class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		@param name: Component name. ( String )
		@param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__uiPath = "ui/Database_Operations.ui"

		self.__container = None

		self.__coreDb = None
		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreTemplatesOutliner = None

		self.__dbTypes = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for the _uiPath attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for the _uiPath attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for the _uiPath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def container(self):
		"""
		This method is the property for the _container attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for the _container attribute.

		@param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for the _container attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def coreDb(self):
		"""
		This method is the property for the _coreDb attribute.

		@return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This method is the setter method for the _coreDb attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This method is the deleter method for the _coreDb attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDb"))

	@property
	def corePreferencesManager(self):
		"""
		This method is the property for the _corePreferencesManager attribute.

		@return: self.__corePreferencesManager. ( Object )
		"""

		return self.__corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self, value):
		"""
		This method is the setter method for the _corePreferencesManager attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("corePreferencesManager"))

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def corePreferencesManager(self):
		"""
		This method is the deleter method for the _corePreferencesManager attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("corePreferencesManager"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for the _coreDatabaseBrowser attribute.

		@return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for the _coreDatabaseBrowser attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for the _coreDatabaseBrowser attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreDatabaseBrowser"))

	@property
	def coreTemplatesOutliner(self):
		"""
		This method is the property for the _coreTemplatesOutliner attribute.

		@return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This method is the setter method for the _coreTemplatesOutliner attribute.

		@param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This method is the deleter method for the _coreTemplatesOutliner attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreTemplatesOutliner"))

	@property
	def dbTypes(self):
		"""
		This method is the property for the _dbTypes attribute.

		@return: self.__dbTypes. ( Tuple )
		"""

		return self.__dbTypes

	@dbTypes.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbTypes(self, value):
		"""
		This method is the setter method for the _dbTypes attribute.

		@param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dbTypes"))

	@dbTypes.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbTypes(self):
		"""
		This method is the deleter method for the _dbTypes attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dbTypes"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		@param container: Container to attach the Component to. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__corePreferencesManager = self.__container.componentsManager.components["core.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface
		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface

		self.__dbTypes = (DbType(type="Ibl Set", getMethod=dbCommon.getIblSets, updateContentMethod=dbCommon.updateIblSetContent, modelContainer=self.__coreDatabaseBrowser, updateLocationMethod=self.__coreDatabaseBrowser.updateIblSetLocation),
						DbType(type="Template", getMethod=dbCommon.getTemplates, updateContentMethod=dbCommon.updateTemplateContent, modelContainer=self.__coreTemplatesOutliner, updateLocationMethod=self.__coreTemplatesOutliner.updateTemplateLocation))

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__corePreferencesManager = None
		self.__coreDatabaseBrowser = None
		self.__coreTemplatesOutliner = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		if not self.__container.parameters.databaseReadOnly:
			self.ui.Synchronize_Database_pushButton.clicked.connect(self.__synchronize_Database_pushButton_clicked)
		else:
			LOGGER.info("{0} | Database Operations capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		not self.__container.parameters.databaseReadOnly and	self.ui.Synchronize_Database_pushButton.clicked.disconnect(self.__synchronize_Database_pushButton_clicked)

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget(self.ui.Database_Operations_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__corePreferencesManager.ui.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self.ui)
		self.ui.Database_Operations_groupBox.setParent(None)

	@core.executionTrace
	def __synchronize_Database_pushButton_clicked(self, checked):
		"""
		This method is triggered when Synchronize_Database_pushButton is clicked.

		@param checked: Checked state. ( Boolean )
		"""

		self.synchronizeDatabase()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def synchronizeDatabase(self):
		"""
		This method synchronizes the Database.

		@return: Method success. ( Boolean )
		"""

		for dbType in self.__dbTypes:
			for item in dbType.getMethod(self.__coreDb.dbSession):
				if not item.path:
					continue

				if os.path.exists(item.path):
					if dbType.updateContentMethod(self.__coreDb.dbSession, item):
						LOGGER.info("{0} | '{1}' {2} has been synchronized!".format(self.__class__.__name__, item.name, dbType.type))
				else:
					if messageBox.messageBox("Question", "Error", "{0} | '{1}' {2} file is missing, would you like to update it's location?".format(self.__class__.__name__, item.name, dbType.type), QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No) == 16384:
						dbType.updateLocationMethod(item)
			dbType.modelContainer.emit(SIGNAL("modelRefresh"))
		messageBox.messageBox("Information", "Information", "{0} | Database synchronization done!".format(self.__class__.__name__), QMessageBox.Information, QMessageBox.Ok)
		return True

