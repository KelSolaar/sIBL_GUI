#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**onlineUpdater.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`OnlineUpdater` Component Interface class and others online update related objects.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import sibl_gui.components.core.db.utilities.common as dbCommon
import sibl_gui.exceptions
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from foundations.parsers import SectionsFileParser
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.addons.onlineUpdater.remoteUpdater import RemoteUpdater, ReleaseObject
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "REPOSITORY_URL", "OnlineUpdater"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Online_Updater.ui")

REPOSITORY_URL = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Repository/"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class OnlineUpdater(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.addons.onlineUpdater.onlineUpdater` Component Interface class.
	| This Component provides online updating capabilities to the Application available through options exposed in the :mod:`umbra.components.core.preferencesManager.preferencesManager` Component ui.
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(OnlineUpdater, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryPreferencesManager = None
		self.__coreDb = None
		self.__coreTemplatesOutliner = None
		self.__addonsLocationsBrowser = None

		self.__ioDirectory = "remote/"

		self.__repositoryUrl = REPOSITORY_URL
		self.__releasesFileUrl = "sIBL_GUI_Releases.rc"

		self.__networkAccessManager = None
		self.__releaseReply = None

		self.__remoteUpdater = None
		self.__reportUpdateStatus = None

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

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settingsSection"))

	@property
	def factoryPreferencesManager(self):
		"""
		This method is the property for **self.__factoryPreferencesManager** attribute.

		:return: self.__factoryPreferencesManager. ( Object )
		"""

		return self.__factoryPreferencesManager

	@factoryPreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryPreferencesManager(self, value):
		"""
		This method is the setter method for **self.__factoryPreferencesManager** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("factoryPreferencesManager"))

	@factoryPreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryPreferencesManager(self):
		"""
		This method is the deleter method for **self.__factoryPreferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("factoryPreferencesManager"))

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
	def coreTemplatesOutliner(self):
		"""
		This method is the property for **self.__coreTemplatesOutliner** attribute.

		:return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This method is the setter method for **self.__coreTemplatesOutliner** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This method is the deleter method for **self.__coreTemplatesOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("coreTemplatesOutliner"))

	@property
	def addonsLocationsBrowser(self):
		"""
		This method is the property for **self.__addonsLocationsBrowser** attribute.

		:return: self.__addonsLocationsBrowser. ( Object )
		"""

		return self.__addonsLocationsBrowser

	@addonsLocationsBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLocationsBrowser(self, value):
		"""
		This method is the setter method for **self.__addonsLocationsBrowser** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("addonsLocationsBrowser"))

	@addonsLocationsBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def addonsLocationsBrowser(self):
		"""
		This method is the deleter method for **self.__addonsLocationsBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("addonsLocationsBrowser"))

	@property
	def ioDirectory(self):
		"""
		This method is the property for **self.__ioDirectory** attribute.

		:return: self.__ioDirectory. ( String )
		"""

		return self.__ioDirectory

	@ioDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self, value):
		"""
		This method is the setter method for **self.__ioDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("ioDirectory"))

	@ioDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ioDirectory(self):
		"""
		This method is the deleter method for **self.__ioDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("ioDirectory"))

	@property
	def repositoryUrl(self):
		"""
		This method is the property for **self.__repositoryUrl** attribute.

		:return: self.__repositoryUrl. ( String )
		"""

		return self.__repositoryUrl

	@repositoryUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self, value):
		"""
		This method is the setter method for **self.__repositoryUrl** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("repositoryUrl"))

	@repositoryUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def repositoryUrl(self):
		"""
		This method is the deleter method for **self.__repositoryUrl** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("repositoryUrl"))

	@property
	def releasesFileUrl(self):
		"""
		This method is the property for **self.__releasesFileUrl** attribute.

		:return: self.__releasesFileUrl. ( String )
		"""

		return self.__releasesFileUrl

	@releasesFileUrl.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releasesFileUrl(self, value):
		"""
		This method is the setter method for **self.__releasesFileUrl** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("releasesFileUrl"))

	@releasesFileUrl.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releasesFileUrl(self):
		"""
		This method is the deleter method for **self.__releasesFileUrl** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("releasesFileUrl"))

	@property
	def networkAccessManager(self):
		"""
		This method is the property for **self.__networkAccessManager** attribute.

		:return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This method is the setter method for **self.__networkAccessManager** attribute.

		:param value: Attribute value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This method is the deleter method for **self.__networkAccessManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("networkAccessManager"))

	@property
	def releaseReply(self):
		"""
		This method is the property for **self.__releaseReply** attribute.

		:return: self.__releaseReply. ( QNetworkReply )
		"""

		return self.__releaseReply

	@releaseReply.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releaseReply(self, value):
		"""
		This method is the setter method for **self.__releaseReply** attribute.

		:param value: Attribute value. ( QNetworkReply )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("releaseReply"))

	@releaseReply.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def releaseReply(self):
		"""
		This method is the deleter method for **self.__releaseReply** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("releaseReply"))

	@property
	def remoteUpdater(self):
		"""
		This method is the property for **self.__remoteUpdater** attribute.

		:return: self.__remoteUpdater. ( Object )
		"""

		return self.__remoteUpdater

	@remoteUpdater.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def remoteUpdater(self, value):
		"""
		This method is the setter method for **self.__remoteUpdater** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("remoteUpdater"))

	@remoteUpdater.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def remoteUpdater(self):
		"""
		This method is the deleter method for **self.__remoteUpdater** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("remoteUpdater"))

	@property
	def reportUpdateStatus(self):
		"""
		This method is the property for **self.__reportUpdateStatus** attribute.

		:return: self.__reportUpdateStatus. ( Boolean )
		"""

		return self.__reportUpdateStatus

	@reportUpdateStatus.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reportUpdateStatus(self, value):
		"""
		This method is the setter method for **self.__reportUpdateStatus** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("reportUpdateStatus"))

	@reportUpdateStatus.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def reportUpdateStatus(self):
		"""
		This method is the deleter method for **self.__reportUpdateStatus** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("reportUpdateStatus"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__factoryPreferencesManager = self.__container.componentsManager.components["factory.preferencesManager"].interface
		self.__coreDb = self.__container.componentsManager.components["core.db"].interface
		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface
		self.__addonsLocationsBrowser = self.__container.componentsManager.components["addons.locationsBrowser"].interface

		self.__ioDirectory = os.path.join(self.__container.userApplicationDatasDirectory, Constants.ioDirectory, self.__ioDirectory)
		not os.path.exists(self.__ioDirectory) and os.makedirs(self.__ioDirectory)

		self.__networkAccessManager = QNetworkAccessManager()

		self.__reportUpdateStatus = True

		self.activated = True
		return True

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryPreferencesManager = None
		self.__coreDb = None
		self.__coreTemplatesOutliner = None
		self.__addonsLocationsBrowser = None

		self.__ioDirectory = os.path.basename(os.path.abspath(self.__ioDirectory))

		self.__networkAccessManager = None

		self.__reportUpdateStatus = None

		self.activated = False
		return True

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__container.parameters.deactivateWorkerThreads and LOGGER.info("{0} | 'OnStartup' Online Updater worker thread deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "deactivateWorkerThreads"))

		self.__Check_For_New_Releases_On_Startup_checkBox_setUi()
		self.__Ignore_Non_Existing_Templates_checkBox_setUi()

		# Signals / Slots.
		self.Check_For_New_Releases_pushButton.clicked.connect(self.__Check_For_New_Releases_pushButton__clicked)
		self.Check_For_New_Releases_On_Startup_checkBox.stateChanged.connect(self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.Ignore_Non_Existing_Templates_checkBox.stateChanged.connect(self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

		return True

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.Check_For_New_Releases_pushButton.clicked.disconnect(self.__Check_For_New_Releases_pushButton__clicked)
		self.Check_For_New_Releases_On_Startup_checkBox.stateChanged.disconnect(self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.Ignore_Non_Existing_Templates_checkBox.stateChanged.disconnect(self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

		return True

	@core.executionTrace
	def onStartup(self):
		"""
		This method is called on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		self.__reportUpdateStatus = False
		not self.__container.parameters.deactivateWorkerThreads and self.Check_For_New_Releases_On_Startup_checkBox.isChecked() and self.checkForNewReleases()
		return True

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__factoryPreferencesManager.Others_Preferences_gridLayout.addWidget(self.Online_Updater_groupBox)

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.Online_Updater_groupBox.setParent(None)

	@core.executionTrace
	def __Check_For_New_Releases_On_Startup_checkBox_setUi(self):
		"""
		This method sets the **Check_For_New_Releases_On_Startup_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "checkForNewReleasesOnStartup").isNull() and self.__settings.setKey(self.__settingsSection, "checkForNewReleasesOnStartup", Qt.Checked)

		checkForNewReleasesOnStartup = self.__settings.getKey(self.__settingsSection, "checkForNewReleasesOnStartup")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Check_For_New_Releases_On_Startup_checkBox", checkForNewReleasesOnStartup.toInt()[0]))
		self.Check_For_New_Releases_On_Startup_checkBox.setCheckState(checkForNewReleasesOnStartup.toInt()[0])

	@core.executionTrace
	def __Check_For_New_Releases_On_Startup_checkBox__stateChanged(self, state):
		"""
		This method is called when **Check_For_New_Releases_On_Startup_checkBox** state changes.

		:param state: Checkbox state. ( Integer )
		"""

		LOGGER.debug("> Check for new releases on startup state: '{0}'.".format(self.Check_For_New_Releases_On_Startup_checkBox.checkState()))
		self.__settings.setKey(self.__settingsSection, "checkForNewReleasesOnStartup", self.Check_For_New_Releases_On_Startup_checkBox.checkState())

	@core.executionTrace
	def __Ignore_Non_Existing_Templates_checkBox_setUi(self):
		"""
		This method sets the **Ignore_Non_Existing_Templates_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "ignoreNonExistingTemplates").isNull() and self.__settings.setKey(self.__settingsSection, "ignoreNonExistingTemplates", Qt.Checked)

		ignoreNonExistingTemplates = self.__settings.getKey(self.__settingsSection, "ignoreNonExistingTemplates")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Ignore_Non_Existing_Templates_checkBox", ignoreNonExistingTemplates.toInt()[0]))
		self.Ignore_Non_Existing_Templates_checkBox.setCheckState(ignoreNonExistingTemplates.toInt()[0])

	@core.executionTrace
	def __Ignore_Non_Existing_Templates_checkBox__stateChanged(self, state):
		"""
		This method is called when **Ignore_Non_Existing_Templates_checkBox** state changes.

		:param state: Checkbox state. ( Integer )
		"""

		LOGGER.debug("> Ignore non existing Templates state: '{0}'.".format(self.Ignore_Non_Existing_Templates_checkBox.checkState()))
		self.__settings.setKey(self.__settingsSection, "ignoreNonExistingTemplates", self.Ignore_Non_Existing_Templates_checkBox.checkState())

	@core.executionTrace
	def __Check_For_New_Releases_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Check_For_New_Releases_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.checkForNewReleases_ui()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, sibl_gui.exceptions.NetworkError)
	def __releaseReply__finished(self):
		"""
		This method is triggered when the release reply finishes.
		"""

		if not self.__releaseReply.error():
			content = []
			while not self.__releaseReply.atEnd ():
				content.append(str(self.__releaseReply.readLine()))

			LOGGER.debug("> Parsing releases file content.")
			sectionsFileParser = SectionsFileParser()
			sectionsFileParser.content = content
			sectionsFileParser.parse()

			releases = {}
			for remoteObject in sectionsFileParser.sections:
				if remoteObject != Constants.applicationName:
						dbTemplates = dbCommon.filterTemplates(self.__coreDb.dbSession, "^{0}$".format(remoteObject), "name")
						dbTemplate = dbTemplates and [dbTemplate[0] for dbTemplate in sorted(((dbTemplate, dbTemplate.release) for dbTemplate in dbTemplates), reverse=True, key=lambda x:(strings.getVersionRank(x[1])))][0] or None
						if not self.__container.parameters.databaseReadOnly:
							if dbTemplate:
								if dbTemplate.release != sectionsFileParser.getValue("Release", remoteObject):
									releases[remoteObject] = ReleaseObject(name=remoteObject,
																		repositoryVersion=sectionsFileParser.getValue("Release", remoteObject),
																		localVersion=dbTemplate.release,
																		type=sectionsFileParser.getValue("Type", remoteObject),
																		url=sectionsFileParser.getValue("Url", remoteObject),
																		comment=sectionsFileParser.getValue("Comment", remoteObject))
							else:
								if not self.Ignore_Non_Existing_Templates_checkBox.isChecked():
									releases[remoteObject] = ReleaseObject(name=remoteObject,
																		repositoryVersion=sectionsFileParser.getValue("Release", remoteObject),
																		localVersion=None,
																		type=sectionsFileParser.getValue("Type", remoteObject),
																		url=sectionsFileParser.getValue("Url", remoteObject),
																		comment=sectionsFileParser.getValue("Comment", remoteObject))
						else:
							LOGGER.info("{0} | '{1}' repository remote object skipped by '{2}' command line parameter value!".format(self.__class__.__name__, remoteObject, "databaseReadOnly"))
				else:
					if Constants.releaseVersion != sectionsFileParser.getValue("Release", remoteObject):
						releases[remoteObject] = ReleaseObject(name=remoteObject,
															repositoryVersion=sectionsFileParser.getValue("Release", remoteObject),
															localVersion=Constants.releaseVersion,
															url=sectionsFileParser.getValue("Url", remoteObject),
															type=sectionsFileParser.getValue("Type", remoteObject),
															comment=None)
			if releases:
				LOGGER.debug("> Initializing Remote Updater.")
				self.__remoteUpdater = RemoteUpdater(self, releases, Qt.Window)
				self.__remoteUpdater.show()
			else:
				self.__reportUpdateStatus and messageBox.messageBox("Information", "Information", "{0} | '{1}' is up to date!".format(self.__class__.__name__, Constants.applicationName))
		else:
			raise sibl_gui.exceptions.NetworkError("QNetworkAccessManager error code: '{0}'.".format(self.__releaseReply.error()))

	@core.executionTrace
	def __getReleaseFile(self, url):
		"""
		This method gets the release file.
		"""

		LOGGER.debug("> Downloading '{0}' releases file.".format(url.path()))

		self.__releaseReply = self.__networkAccessManager.get(QNetworkRequest(url))
		self.__releaseReply.finished.connect(self.__releaseReply__finished)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, sibl_gui.exceptions.NetworkError, Exception)
	def checkForNewReleases_ui(self):
		"""
		This method checks for new releases.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		if not self.__networkAccessManager.networkAccessible():
			raise sibl_gui.exceptions.NetworkError("{0} | Network is not accessible!".format(self.__class__.__name__))

		self.__reportUpdateStatus = True
		if self.checkForNewReleases():
			return True
		else:
			raise Exception("{0} | Exception raised while checking for new releases!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, sibl_gui.exceptions.NetworkError, Exception)
	def checkForNewReleases(self):
		"""
		This method checks for new releases.

		:return: Method success. ( Boolean )
		"""

		if not self.__networkAccessManager.networkAccessible():
			raise sibl_gui.exceptions.NetworkError("{0} | Network is not accessible!".format(self.__class__.__name__))

		self.__getReleaseFile(QUrl(os.path.join(self.__repositoryUrl, self.__releasesFileUrl)))
		return True
