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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import QNetworkRequest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import sibl_gui.components.core.database.operations
import sibl_gui.exceptions
import umbra.exceptions
from foundations.parsers import SectionsFileParser
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.addons.onlineUpdater.remoteUpdater import ReleaseObject
from sibl_gui.components.addons.onlineUpdater.remoteUpdater import RemoteUpdater
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "REPOSITORY_URL", "OnlineUpdater"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Online_Updater.ui")

REPOSITORY_URL = "http://kelsolaar.hdrlabs.com/sIBL_GUI/Repository/"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class OnlineUpdater(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.addons.onlineUpdater.onlineUpdater` Component Interface class.
	| This Component provides online updating capabilities to the Application available through options exposed in
		the :mod:`sibl_gui.components.core.preferencesManager.preferencesManager` Component ui.
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

		super(OnlineUpdater, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__preferencesManager = None
		self.__templatesOutliner = None
		self.__locationsBrowser = None

		self.__ioDirectory = "remote/"

		self.__repositoryUrl = REPOSITORY_URL
		self.__releasesFileUrl = "sIBL_GUI_Releases.rc"

		self.__networkAccessManager = None
		self.__releasesFileReply = None

		self.__remoteUpdater = None
		self.__reportUpdateStatus = None

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
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for **self.__settingsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def preferencesManager(self):
		"""
		This method is the property for **self.__preferencesManager** attribute.

		:return: self.__preferencesManager. ( QWidget )
		"""

		return self.__preferencesManager

	@preferencesManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def preferencesManager(self, value):
		"""
		This method is the setter method for **self.__preferencesManager** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "preferencesManager"))

	@preferencesManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def preferencesManager(self):
		"""
		This method is the deleter method for **self.__preferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preferencesManager"))

	@property
	def templatesOutliner(self):
		"""
		This method is the property for **self.__templatesOutliner** attribute.

		:return: self.__templatesOutliner. ( QWidget )
		"""

		return self.__templatesOutliner

	@templatesOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesOutliner(self, value):
		"""
		This method is the setter method for **self.__templatesOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesOutliner"))

	@templatesOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesOutliner(self):
		"""
		This method is the deleter method for **self.__templatesOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesOutliner"))

	@property
	def locationsBrowser(self):
		"""
		This method is the property for **self.__locationsBrowser** attribute.

		:return: self.__locationsBrowser. ( QWidget )
		"""

		return self.__locationsBrowser

	@locationsBrowser.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def locationsBrowser(self, value):
		"""
		This method is the setter method for **self.__locationsBrowser** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locationsBrowser"))

	@locationsBrowser.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def locationsBrowser(self):
		"""
		This method is the deleter method for **self.__locationsBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locationsBrowser"))

	@property
	def ioDirectory(self):
		"""
		This method is the property for **self.__ioDirectory** attribute.

		:return: self.__ioDirectory. ( String )
		"""

		return self.__ioDirectory

	@ioDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def ioDirectory(self, value):
		"""
		This method is the setter method for **self.__ioDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ioDirectory"))

	@ioDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def ioDirectory(self):
		"""
		This method is the deleter method for **self.__ioDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ioDirectory"))

	@property
	def repositoryUrl(self):
		"""
		This method is the property for **self.__repositoryUrl** attribute.

		:return: self.__repositoryUrl. ( String )
		"""

		return self.__repositoryUrl

	@repositoryUrl.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def repositoryUrl(self, value):
		"""
		This method is the setter method for **self.__repositoryUrl** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "repositoryUrl"))

	@repositoryUrl.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def repositoryUrl(self):
		"""
		This method is the deleter method for **self.__repositoryUrl** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "repositoryUrl"))

	@property
	def releasesFileUrl(self):
		"""
		This method is the property for **self.__releasesFileUrl** attribute.

		:return: self.__releasesFileUrl. ( String )
		"""

		return self.__releasesFileUrl

	@releasesFileUrl.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def releasesFileUrl(self, value):
		"""
		This method is the setter method for **self.__releasesFileUrl** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "releasesFileUrl"))

	@releasesFileUrl.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def releasesFileUrl(self):
		"""
		This method is the deleter method for **self.__releasesFileUrl** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "releasesFileUrl"))

	@property
	def networkAccessManager(self):
		"""
		This method is the property for **self.__networkAccessManager** attribute.

		:return: self.__networkAccessManager. ( QNetworkAccessManager )
		"""

		return self.__networkAccessManager

	@networkAccessManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def networkAccessManager(self, value):
		"""
		This method is the setter method for **self.__networkAccessManager** attribute.

		:param value: Attribute value. ( QNetworkAccessManager )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "networkAccessManager"))

	@networkAccessManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def networkAccessManager(self):
		"""
		This method is the deleter method for **self.__networkAccessManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "networkAccessManager"))

	@property
	def releaseReply(self):
		"""
		This method is the property for **self.__releasesFileReply** attribute.

		:return: self.__releasesFileReply. ( QNetworkReply )
		"""

		return self.__releasesFileReply

	@releaseReply.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def releaseReply(self, value):
		"""
		This method is the setter method for **self.__releasesFileReply** attribute.

		:param value: Attribute value. ( QNetworkReply )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "releaseReply"))

	@releaseReply.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def releaseReply(self):
		"""
		This method is the deleter method for **self.__releasesFileReply** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "releaseReply"))

	@property
	def remoteUpdater(self):
		"""
		This method is the property for **self.__remoteUpdater** attribute.

		:return: self.__remoteUpdater. ( Object )
		"""

		return self.__remoteUpdater

	@remoteUpdater.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def remoteUpdater(self, value):
		"""
		This method is the setter method for **self.__remoteUpdater** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "remoteUpdater"))

	@remoteUpdater.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def remoteUpdater(self):
		"""
		This method is the deleter method for **self.__remoteUpdater** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "remoteUpdater"))

	@property
	def reportUpdateStatus(self):
		"""
		This method is the property for **self.__reportUpdateStatus** attribute.

		:return: self.__reportUpdateStatus. ( Boolean )
		"""

		return self.__reportUpdateStatus

	@reportUpdateStatus.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def reportUpdateStatus(self, value):
		"""
		This method is the setter method for **self.__reportUpdateStatus** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "reportUpdateStatus"))

	@reportUpdateStatus.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def reportUpdateStatus(self):
		"""
		This method is the deleter method for **self.__reportUpdateStatus** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "reportUpdateStatus"))

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
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]
		self.__templatesOutliner = self.__engine.componentsManager["core.templatesOutliner"]
		self.__locationsBrowser = self.__engine.componentsManager["addons.locationsBrowser"]

		self.__ioDirectory = os.path.join(self.__engine.userApplicationDataDirectory,
										Constants.ioDirectory, self.__ioDirectory)
		not foundations.common.pathExists(self.__ioDirectory) and os.makedirs(self.__ioDirectory)

		self.__networkAccessManager = QNetworkAccessManager()

		self.__reportUpdateStatus = True

		self.activated = True
		return True

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
		self.__templatesOutliner = None
		self.__locationsBrowser = None

		self.__ioDirectory = os.path.basename(os.path.abspath(self.__ioDirectory))

		self.__networkAccessManager = None

		self.__reportUpdateStatus = None

		self.activated = False
		return True

	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__engine.parameters.deactivateWorkerThreads and \
		LOGGER.info(
		"{0} | 'OnStartup' Online Updater worker thread deactivated by '{1}' command line parameter value!".format(
		self.__class__.__name__, "deactivateWorkerThreads"))

		self.__Check_For_New_Releases_On_Startup_checkBox_setUi()
		self.__Ignore_Non_Existing_Templates_checkBox_setUi()

		# Signals / Slots.
		self.Check_For_New_Releases_pushButton.clicked.connect(self.__Check_For_New_Releases_pushButton__clicked)
		self.Check_For_New_Releases_On_Startup_checkBox.stateChanged.connect(
		self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.Ignore_Non_Existing_Templates_checkBox.stateChanged.connect(
		self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.Check_For_New_Releases_pushButton.clicked.disconnect(self.__Check_For_New_Releases_pushButton__clicked)
		self.Check_For_New_Releases_On_Startup_checkBox.stateChanged.disconnect(
		self.__Check_For_New_Releases_On_Startup_checkBox__stateChanged)
		self.Ignore_Non_Existing_Templates_checkBox.stateChanged.disconnect(
		self.__Ignore_Non_Existing_Templates_checkBox__stateChanged)

		self.initializedUi = False
		return True

	def onStartup(self):
		"""
		This method is triggered on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		self.__reportUpdateStatus = False
		if not self.__engine.parameters.deactivateWorkerThreads and \
		self.Check_For_New_Releases_On_Startup_checkBox.isChecked():
			self.checkForNewReleases()
		return True

	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.Online_Updater_groupBox)

	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.Online_Updater_groupBox.setParent(None)

	def __Check_For_New_Releases_On_Startup_checkBox_setUi(self):
		"""
		This method sets the **Check_For_New_Releases_On_Startup_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "checkForNewReleasesOnStartup").isNull() and \
		self.__settings.setKey(self.__settingsSection, "checkForNewReleasesOnStartup", Qt.Checked)

		checkForNewReleasesOnStartup = self.__settings.getKey(self.__settingsSection, "checkForNewReleasesOnStartup")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Check_For_New_Releases_On_Startup_checkBox",
												foundations.common.getFirstItem(checkForNewReleasesOnStartup.toInt())))
		self.Check_For_New_Releases_On_Startup_checkBox.setCheckState(
		foundations.common.getFirstItem(checkForNewReleasesOnStartup.toInt()))

	def __Check_For_New_Releases_On_Startup_checkBox__stateChanged(self, state):
		"""
		This method is triggered when **Check_For_New_Releases_On_Startup_checkBox** Widget state changes.

		:param state: Checkbox state. ( Integer )
		"""

		LOGGER.debug("> Check for new releases on startup state: '{0}'.".format(state))
		self.__settings.setKey(self.__settingsSection, "checkForNewReleasesOnStartup", state)

	def __Ignore_Non_Existing_Templates_checkBox_setUi(self):
		"""
		This method sets the **Ignore_Non_Existing_Templates_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "ignoreNonExistingTemplates").isNull() and \
		self.__settings.setKey(self.__settingsSection, "ignoreNonExistingTemplates", Qt.Checked)

		ignoreNonExistingTemplates = self.__settings.getKey(self.__settingsSection, "ignoreNonExistingTemplates")
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Ignore_Non_Existing_Templates_checkBox",
													foundations.common.getFirstItem(ignoreNonExistingTemplates.toInt())))
		self.Ignore_Non_Existing_Templates_checkBox.setCheckState(
		foundations.common.getFirstItem(ignoreNonExistingTemplates.toInt()))

	def __Ignore_Non_Existing_Templates_checkBox__stateChanged(self, state):
		"""
		This method is triggered when **Ignore_Non_Existing_Templates_checkBox** Widget state changes.

		:param state: Checkbox state. ( Integer )
		"""

		LOGGER.debug("> Ignore non existing Templates state: '{0}'.".format(state))
		self.__settings.setKey(self.__settingsSection, "ignoreNonExistingTemplates", state)

	def __Check_For_New_Releases_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Check_For_New_Releases_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.checkForNewReleasesUi()

	@foundations.exceptions.handleExceptions(sibl_gui.exceptions.NetworkError)
	def __releasesFileReply__finished(self):
		"""
		This method is triggered when the releases file reply finishes.
		"""

		self.__engine.stopProcessing()

		if not self.__releasesFileReply.error():
			content = []
			while not self.__releasesFileReply.atEnd ():
				content.append(foundations.strings.encode(self.__releasesFileReply.readLine()))

			LOGGER.debug("> Parsing releases file content.")
			sectionsFileParser = SectionsFileParser()
			sectionsFileParser.content = content
			sectionsFileParser.parse()

			releases = {}
			for remoteObject in sectionsFileParser.sections:
				if remoteObject != Constants.applicationName:
					databaseTemplates = \
					sibl_gui.components.core.database.operations.filterTemplates("^{0}$".format(remoteObject), "name")
					databaseTemplate = foundations.common.getFirstItem([foundations.common.getFirstItem(databaseTemplate)
												for databaseTemplate in sorted(((databaseTemplate, databaseTemplate.release)
												for databaseTemplate in databaseTemplates),
												reverse=True,
												key=lambda x:(foundations.strings.getVersionRank(x[1])))])
					if not self.__engine.parameters.databaseReadOnly:
						if databaseTemplate:
							if databaseTemplate.release != sectionsFileParser.getValue("Release", remoteObject):
								releases[remoteObject] = ReleaseObject(name=remoteObject,
																	repositoryVersion=sectionsFileParser.getValue(
																	"Release", remoteObject),
																	localVersion=databaseTemplate.release,
																	type=sectionsFileParser.getValue("Type",
																									remoteObject),
																	url=sectionsFileParser.getValue("Url",
																									remoteObject),
																	comment=sectionsFileParser.getValue("Comment",
																									remoteObject))
						else:
							if not self.Ignore_Non_Existing_Templates_checkBox.isChecked():
								releases[remoteObject] = ReleaseObject(name=remoteObject,
																	repositoryVersion=sectionsFileParser.getValue(
																	"Release", remoteObject),
																	localVersion=None,
																	type=sectionsFileParser.getValue("Type",
																									remoteObject),
																	url=sectionsFileParser.getValue("Url",
																									remoteObject),
																	comment=sectionsFileParser.getValue("Comment",
																									remoteObject))
					else:
						LOGGER.info("{0} | '{1}' repository remote object skipped by '{2}' command line parameter value!".format(
						self.__class__.__name__, remoteObject, "databaseReadOnly"))
				else:
					if Constants.releaseVersion != sectionsFileParser.getValue("Release", remoteObject):
						releases[remoteObject] = ReleaseObject(name=remoteObject,
															repositoryVersion=sectionsFileParser.getValue("Release",
																										remoteObject),
															localVersion=Constants.releaseVersion,
															url=sectionsFileParser.getValue("Url", remoteObject),
															type=sectionsFileParser.getValue("Type", remoteObject),
															comment=None)
			if releases:
				LOGGER.debug("> Initializing Remote Updater.")
				self.__remoteUpdater = RemoteUpdater(self, releases, Qt.Window)
				self.__remoteUpdater.show()
			else:
				self.__reportUpdateStatus and self.__engine.notificationsManager.notify(
				"{0} | '{1}' is up to date!".format(self.__class__.__name__, Constants.applicationName))
		else:
			raise sibl_gui.exceptions.NetworkError("{0} | QNetworkAccessManager error code: '{1}'.".format(
			self.__class__.__name__, self.__releasesFileReply.error()))

	def __getReleasesFile(self, url):
		"""
		This method gets the releases file.
		"""

		LOGGER.debug("> Downloading '{0}' releases file.".format(url.path()))

		self.__engine.startProcessing("Retrieving Releases File ...")
		self.__releasesFileReply = self.__networkAccessManager.get(QNetworkRequest(url))
		self.__releasesFileReply.finished.connect(self.__releasesFileReply__finished)

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											sibl_gui.exceptions.NetworkError,
											Exception)
	def checkForNewReleasesUi(self):
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

	@foundations.exceptions.handleExceptions(sibl_gui.exceptions.NetworkError, Exception)
	def checkForNewReleases(self):
		"""
		This method checks for new releases.

		:return: Method success. ( Boolean )
		"""

		if not self.__networkAccessManager.networkAccessible():
			raise sibl_gui.exceptions.NetworkError("{0} | Network is not accessible!".format(self.__class__.__name__))

		self.__getReleasesFile(QUrl(os.path.join(self.__repositoryUrl, self.__releasesFileUrl)))
		return True
