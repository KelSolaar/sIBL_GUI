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
**componentsManagerUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Components Manager Ui Component Module.

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
import platform
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.strings as strings
import umbra.components.core.db.dbUtilities.common as dbCommon
import umbra.components.core.db.dbUtilities.types as dbTypes
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from manager.uiComponent import UiComponent
from foundations.walker import Walker
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class TemplatesOutliner_Worker(QThread):
	"""
	This Class Is The TemplatesOutliner_Worker Class.
	"""

	# Custom Signals Definitions.
	databaseChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, container):
		"""
		This Method Initializes The Class.
		
		@param container: Object Container. ( Object )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QThread.__init__(self, container)

		# --- Setting Class Attributes. ---
		self.__container = container

		self.__dbSession = self.__container.coreDb.dbSessionMaker()

		self.__timer = None
		self.__timerCycleMultiplier = 5

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
	def timer(self):
		"""
		This Method Is The Property For The _timer Attribute.

		@return: self.__timer. ( QTimer )
		"""

		return self.__timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		This Method Is The Setter Method For The _timer Attribute.

		@param value: Attribute Value. ( QTimer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("timer"))

	@timer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		This Method Is The Deleter Method For The _timer Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("timer"))

	@property
	def timerCycleMultiplier(self):
		"""
		This Method Is The Property For The _timerCycleMultiplier Attribute.

		@return: self.__timerCycleMultiplier. ( Float )
		"""

		return self.__timerCycleMultiplier

	@timerCycleMultiplier.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self, value):
		"""
		This Method Is The Setter Method For The _timerCycleMultiplier Attribute.

		@param value: Attribute Value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("timerCycleMultiplier"))

	@timerCycleMultiplier.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self):
		"""
		This Method Is The Deleter Method For The _timerCycleMultiplier Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("timerCycleMultiplier"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def run(self):
		"""
		This Method Starts The QThread.
		"""

		self.__timer = QTimer()
		self.__timer.moveToThread(self)
		self.__timer.start(Constants.defaultTimerCycle * self.__timerCycleMultiplier)

		self.__timer.timeout.connect(self.updateTemplates, Qt.DirectConnection)

		self.exec_()

	@core.executionTrace
	def updateTemplates(self):
		"""
		This Method Updates Database Templates If They Have Been Modified On Disk.
		"""

		needModelRefresh = False
		for template in dbCommon.getTemplates(self.__dbSession):
			if template.path:
				if os.path.exists(template.path):
					storedStats = template.osStats.split(",")
					osStats = os.stat(template.path)
					if str(osStats[8]) != str(storedStats[8]):
						LOGGER.info("{0} | '{1}' Template File Has Been Modified And Will Be Updated!".format(self.__class__.__name__, template.name))
						if dbCommon.updateTemplateContent(self.__dbSession, template):
							LOGGER.info("{0} | '{1}' Template Has Been Updated!".format(self.__class__.__name__, template.name))
							needModelRefresh = True

		needModelRefresh and self.emit(SIGNAL("databaseChanged()"))

class TemplatesOutliner_QTreeView(QTreeView):
	"""
	This Class Is The TemplatesOutliner_QTreeView Class.
	"""

	@core.executionTrace
	def __init__(self, container):
		"""
		This Method Initializes The Class.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QTreeView.__init__(self, container)

		self.setAcceptDrops(True)


		# --- Setting Class Attributes. ---
		self.__container = container

		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface

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
	def coreTemplatesOutliner(self):
		"""
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self.__coreTemplatesOutliner. ( Object )
		"""

		return self.__coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		"""
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		"""
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreTemplatesOutliner"))
	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def dragEnterEvent(self, event):
		"""
		This Method Defines The Drag Enter Event Behavior.
		
		@param event: QEvent. ( QEvent )
		"""

		if event.mimeData().hasFormat("text/uri-list"):
			LOGGER.debug("> '{0}' Drag Event Type Accepted!".format("text/uri-list"))
			event.accept()
		else:
			event.ignore()

	@core.executionTrace
	def dragMoveEvent(self, event):
		"""
		This Method Defines The Drag Move Event Behavior.
		
		@param event: QEvent. ( QEvent )
		"""

		pass

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, OSError, foundations.exceptions.UserError)
	def dropEvent(self, event):
		"""
		This Method Defines The Drop Event Behavior.
		
		@param event: QEvent. ( QEvent )		
		"""

		if not self.__container.parameters.databaseReadOnly:
			if event.mimeData().hasUrls():
				LOGGER.debug("> Drag Event Urls List: '{0}'!".format(event.mimeData().urls()))
				for url in event.mimeData().urls():
					path = (platform.system() == "Windows" or platform.system() == "Microsoft") and re.search("^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
					if re.search("\.{0}$".format(self.__coreTemplatesOutliner.extension), str(url.path())):
						name = strings.getSplitextBasename(path)
						if messageBox.messageBox("Question", "Question", "'{0}' Template Set File Has Been Dropped, Would You Like To Add It To The Database?".format(name), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
							self.__coreTemplatesOutliner.addTemplate(name, path)
					else:
						if os.path.isdir(path):
							if messageBox.messageBox("Question", "Question", "'{0}' Directory Has Been Dropped, Would You Like To Add Its Content To The Database?".format(path), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
								self.__coreTemplatesOutliner.addDirectory(path)
						else:
							raise OSError, "{0} | Exception Raised While Parsing '{1}' Path: Syntax Is Invalid!".format(self.__class__.__name__, path)
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only!".format(self.__class__.__name__)

class TemplatesOutliner(UiComponent):
	"""
	This Class Is The TemplatesOutliner Class.
	"""

	# Custom Signals Definitions.
	modelRefresh = pyqtSignal()
	modelChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
		self.deactivatable = False

		self.__uiPath = "ui/Templates_Outliner.ui"
		self.__uiResources = "resources"
		self.__uiSoftwareAffixe = "_Software.png"
		self.__uiUnknownSoftwareImage = "Unknown_Software.png"
		self.__dockArea = 1

		self.__container = None
		self.__settings = None
		self.__settingsSection = None
		self.__settingsSeparator = ","

		self.__coreDb = None

		self.__model = None
		self.__modelSelection = None

		self.__templatesOutlinerWorkerThread = None

		self.__extension = "sIBLT"

		self.__defaultCollections = None
		self.__factoryCollection = "Factory"
		self.__userCollection = "User"

		self.__modelHeaders = [ "Templates", "Release", "Software Version" ]
		self.__treeViewIndentation = 15
		self.__treeViewInnerMargins = QMargins(0, 0, 0, 12)
		self.__templatesInformationsDefaultText = "<center><h4>* * *</h4>Select A Template To Display Related Informations!<h4>* * *</h4></center>"
		self.__templatesInformationsText = """
											<h4><center>{0}</center></h4>
											<p>
											<b>Date:</b> {1}
											<br/>
											<b>Author:</b> {2}
											<br/>
											<b>Email:</b> <a href="mailto:{3}"><span style=" text-decoration: underline; color:#e0e0e0;">{3}</span></a>
											<br/>
											<b>Url:</b> <a href="{4}"><span style=" text-decoration: underline; color:#e0e0e0;">{4}</span></a>
											<br/>
											<b>Output Script:</b> {5}
											<p>
											<b>Comment:</b> {6}
											</p>
											<p>
											<b>Help File:</b> <a href="{7}"><span style=" text-decoration: underline; color:#e0e0e0;">Template Manual</span></a>
											</p>
											</p>
											"""

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This Method Is The Property For The _uiResources Attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This Method Is The Deleter Method For The _uiResources Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def uiSoftwareAffixe(self):
		"""
		This Method Is The Property For The _uiSoftwareAffixe Attribute.

		@return: self.__uiSoftwareAffixe. ( String )
		"""

		return self.__uiSoftwareAffixe

	@uiSoftwareAffixe.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSoftwareAffixe(self, value):
		"""
		This Method Is The Setter Method For The _uiSoftwareAffixe Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiSoftwareAffixe"))

	@uiSoftwareAffixe.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSoftwareAffixe(self):
		"""
		This Method Is The Deleter Method For The _uiSoftwareAffixe Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiSoftwareAffixe"))

	@property
	def uiUnknownSoftwareImage(self):
		"""
		This Method Is The Property For The _uiUnknownSoftwareImage Attribute.

		@return: self.__uiUnknownSoftwareImage. ( String )
		"""

		return self.__uiUnknownSoftwareImage

	@uiUnknownSoftwareImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUnknownSoftwareImage(self, value):
		"""
		This Method Is The Setter Method For The _uiUnknownSoftwareImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiUnknownSoftwareImage"))

	@uiUnknownSoftwareImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUnknownSoftwareImage(self):
		"""
		This Method Is The Deleter Method For The _uiUnknownSoftwareImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiUnknownSoftwareImage"))

	@property
	def dockArea(self):
		"""
		This Method Is The Property For The _dockArea Attribute.

		@return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This Method Is The Deleter Method For The _dockArea Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dockArea"))

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
	def settings(self):
		"""
		This Method Is The Property For The _settings Attribute.

		@return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This Method Is The Deleter Method For The _settings Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settings"))

	@property
	def settingsSection(self):
		"""
		This Method Is The Property For The _settingsSection Attribute.

		@return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This Method Is The Setter Method For The _settingsSection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This Method Is The Deleter Method For The _settingsSection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settingsSection"))

	@property
	def settingsSeparator(self):
		"""
		This Method Is The Property For The _settingsSeparator Attribute.

		@return: self.__settingsSeparator. ( String )
		"""

		return self.__settingsSeparator

	@settingsSeparator.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self, value):
		"""
		This Method Is The Setter Method For The _settingsSeparator Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self):
		"""
		This Method Is The Deleter Method For The _settingsSeparator Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("settingsSeparator"))

	@property
	def coreDb(self):
		"""
		This Method Is The Property For The _coreDb Attribute.

		@return: self.__coreDb. ( Object )
		"""

		return self.__coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		"""
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		"""
		This Method Is The Deleter Method For The _coreDb Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDb"))

	@property
	def model(self):
		"""
		This Method Is The Property For The _model Attribute.

		@return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This Method Is The Setter Method For The _model Attribute.

		@param value: Attribute Value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This Method Is The Deleter Method For The _model Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("model"))

	@property
	def modelSelection(self):
		"""
		This Method Is The Property For The _modelSelection Attribute.

		@return: self.__modelSelection. ( Dictionary )
		"""

		return self.__modelSelection

	@modelSelection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self, value):
		"""
		This Method Is The Setter Method For The _modelSelection Attribute.

		@param value: Attribute Value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("modelSelection"))

	@modelSelection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self):
		"""
		This Method Is The Deleter Method For The _modelSelection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("modelSelection"))

	@property
	def templatesOutlinerWorkerThread(self):
		"""
		This Method Is The Property For The _templatesOutlinerWorkerThread Attribute.

		@return: self.__templatesOutlinerWorkerThread. ( QThread )
		"""

		return self.__templatesOutlinerWorkerThread

	@templatesOutlinerWorkerThread.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesOutlinerWorkerThread(self, value):
		"""
		This Method Is The Setter Method For The _templatesOutlinerWorkerThread Attribute.

		@param value: Attribute Value. ( QThread )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templatesOutlinerWorkerThread"))

	@templatesOutlinerWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesOutlinerWorkerThread(self):
		"""
		This Method Is The Deleter Method For The _templatesOutlinerWorkerThread Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templatesOutlinerWorkerThread"))

	@property
	def extension(self):
		"""
		This Method Is The Property For The _extension Attribute.

		@return: self.__extension. ( String )
		"""

		return self.__extension

	@extension.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self, value):
		"""
		This Method Is The Setter Method For The _extension Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("extension"))

	@extension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		This Method Is The Deleter Method For The _extension Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("extension"))

	@property
	def defaultCollections(self):
		"""
		This Method Is The Property For The _defaultCollections Attribute.

		@return: self.__defaultCollections. ( Dictionary )
		"""

		return self.__defaultCollections

	@defaultCollections.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollections(self, value):
		"""
		This Method Is The Setter Method For The _defaultCollections Attribute.

		@param value: Attribute Value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("defaultCollections"))

	@defaultCollections.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollections(self):
		"""
		This Method Is The Deleter Method For The _defaultCollections Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("defaultCollections"))

	@property
	def factoryCollection(self):
		"""
		This Method Is The Property For The _factoryCollection Attribute.

		@return: self.__factoryCollection. ( String )
		"""

		return self.__factoryCollection

	@factoryCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryCollection(self, value):
		"""
		This Method Is The Setter Method For The _factoryCollection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("factoryCollection"))

	@factoryCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryCollection(self):
		"""
		This Method Is The Deleter Method For The _factoryCollection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("factoryCollection"))

	@property
	def userCollection(self):
		"""
		This Method Is The Property For The _userCollection Attribute.

		@return: self.__userCollection. ( String )
		"""

		return self.__userCollection

	@userCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userCollection(self, value):
		"""
		This Method Is The Setter Method For The _userCollection Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("userCollection"))

	@userCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userCollection(self):
		"""
		This Method Is The Deleter Method For The _userCollection Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("userCollection"))

	@property
	def modelHeaders(self):
		"""
		This Method Is The Property For The _modelHeaders Attribute.

		@return: self.__modelHeaders. ( List )
		"""

		return self.__modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self, value):
		"""
		This Method Is The Setter Method For The _modelHeaders Attribute.

		@param value: Attribute Value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("modelHeaders"))

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self):
		"""
		This Method Is The Deleter Method For The _modelHeaders Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("modelHeaders"))

	@property
	def treeViewIndentation(self):
		"""
		This Method Is The Property For The _treeViewIndentation Attribute.

		@return: self.__treeViewIndentation. ( Integer )
		"""

		return self.__treeViewIndentation

	@treeViewIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self, value):
		"""
		This Method Is The Setter Method For The _treeViewIndentation Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("treeViewIndentation"))

	@treeViewIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self):
		"""
		This Method Is The Deleter Method For The _treeViewIndentation Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("treeViewIndentation"))

	@property
	def treeViewInnerMargins(self):
		"""
		This Method Is The Property For The _treeViewInnerMargins Attribute.

		@return: self.__treeViewInnerMargins. ( Integer )
		"""

		return self.__treeViewInnerMargins

	@treeViewInnerMargins.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self, value):
		"""
		This Method Is The Setter Method For The _treeViewInnerMargins Attribute.

		@param value: Attribute Value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("treeViewInnerMargins"))

	@treeViewInnerMargins.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self):
		"""
		This Method Is The Deleter Method For The _treeViewInnerMargins Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("treeViewInnerMargins"))

	@property
	def templatesInformationsDefaultText(self):
		"""
		This Method Is The Property For The _templatesInformationsDefaultText Attribute.

		@return: self.__templatesInformationsDefaultText. ( String )
		"""

		return self.__templatesInformationsDefaultText

	@templatesInformationsDefaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsDefaultText(self, value):
		"""
		This Method Is The Setter Method For The _templatesInformationsDefaultText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templatesInformationsDefaultText"))

	@templatesInformationsDefaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsDefaultText(self):
		"""
		This Method Is The Deleter Method For The _templatesInformationsDefaultText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templatesInformationsDefaultText"))

	@property
	def templatesInformationsText(self):
		"""
		This Method Is The Property For The _templatesInformationsText Attribute.

		@return: self.__templatesInformationsText. ( String )
		"""

		return self.__templatesInformationsText

	@templatesInformationsText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsText(self, value):
		"""
		This Method Is The Setter Method For The _templatesInformationsText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templatesInformationsText"))

	@templatesInformationsText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsText(self):
		"""
		This Method Is The Deleter Method For The _templatesInformationsText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templatesInformationsText"))

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

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__coreDb = self.__container.componentsManager.components["core.db"].interface

		self.__defaultCollections = { self.__factoryCollection: os.path.join(os.getcwd(), Constants.templatesDirectory), self.__userCollection: os.path.join(self.__container.userApplicationDatasDirectory, Constants.templatesDirectory) }

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Cannot Be Deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self.__container.parameters.databaseReadOnly and	LOGGER.info("{0} | Templates_Outliner_treeView Model Edition Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))
		self.__model = QStandardItemModel()
		self.__Templates_Outliner_treeView_setModel()

		self.ui.Templates_Outliner_treeView = TemplatesOutliner_QTreeView(self.__container)
		self.ui.Templates_Outliner_gridLayout.setContentsMargins(self.__treeViewInnerMargins)
		self.ui.Templates_Outliner_gridLayout.addWidget(self.ui.Templates_Outliner_treeView, 0, 0)

		self.ui.Templates_Outliner_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Templates_Outliner_treeView_addActions()

		self.__Templates_Outliner_treeView_setView()

		self.ui.Template_Informations_textBrowser.setText(self.__templatesInformationsDefaultText)
		self.ui.Template_Informations_textBrowser.setOpenLinks(False)

		self.ui.Templates_Outliner_splitter.setSizes([16777215, 1])

		if not self.__container.parameters.databaseReadOnly:
			if not self.__container.parameters.deactivateWorkerThreads:
				self.__templatesOutlinerWorkerThread = TemplatesOutliner_Worker(self)
				self.__templatesOutlinerWorkerThread.start()
				self.__container.workerThreads.append(self.__templatesOutlinerWorkerThread)
			else:
				LOGGER.info("{0} | Templates Continuous Scanner Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Templates Continuous Scanner Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		# Signals / Slots.
		self.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.connect(self.__Templates_Outliner_treeView_selectionModel__selectionChanged)
		self.ui.Template_Informations_textBrowser.anchorClicked.connect(self.__Template_Informations_textBrowser__anchorClicked)
		self.modelChanged.connect(self.__Templates_Outliner_treeView_refreshView)
		self.modelRefresh.connect(self.__Templates_Outliner_treeView_refreshModel)
		not self.__container.parameters.databaseReadOnly and not self.__container.parameters.deactivateWorkerThreads and self.__templatesOutlinerWorkerThread.databaseChanged.connect(self.__coreDb_database__changed)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Ui Cannot Be Uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget Cannot Be Removed!".format(self.name))

	@core.executionTrace
	def onStartup(self):
		"""
		This Method Is Called On Framework Startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework Startup Method.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			# Adding Default Templates.			
			self.addDefaultTemplates()

			# Templates Table Integrity Checking.
			erroneousTemplates = dbCommon.checkTemplatesTableIntegrity(self.__coreDb.dbSession)
			if erroneousTemplates:
				for template in erroneousTemplates:
					if erroneousTemplates[template] == "INEXISTING_TEMPLATE_FILE_EXCEPTION":
						if messageBox.messageBox("Question", "Error", "{0} | '{1}' Template File Is Missing, Would You Like To Update It's Location?".format(self.__class__.__name__, template.name), QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No) == 16384:
							self.updateTemplateLocation(template)
					else:
						messageBox.messageBox("Warning", "Warning", "{0} | '{1}' {2}".format(self.__class__.__name__, template.name, dbCommon.DB_EXCEPTIONS[erroneousTemplates[template]]))
		else:
			LOGGER.info("{0} | Database Default Templates Wizard And Templates Integrity Checking Method Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeCollections = str(self.__settings.getKey(self.__settingsSection, "activeCollections").toString())
		LOGGER.debug("> Stored '{0}' Active Collections Selection: '{1}'.".format(self.__class__.__name__, activeCollections))
		if activeCollections:
			if self.__settingsSeparator in activeCollections:
				collections = activeCollections.split(self.__settingsSeparator)
			else:
				collections = [activeCollections]
			self.__modelSelection["Collections"] = collections

		activeSoftwares = str(self.__settings.getKey(self.__settingsSection, "activeSoftwares").toString())
		LOGGER.debug("> Stored '{0}' Active Softwares Selection: '{1}'.".format(self.__class__.__name__, activeSoftwares))
		if activeSoftwares:
			if self.__settingsSeparator in activeSoftwares:
				softwares = activeSoftwares.split(self.__settingsSeparator)
			else:
				softwares = [activeSoftwares]
			self.__modelSelection["Softwares"] = softwares

		activeTemplatesIds = str(self.__settings.getKey(self.__settingsSection, "activeTemplates").toString())
		LOGGER.debug("> Stored '{0}' Active Templates Ids Selection: '{1}'.".format(self.__class__.__name__, activeTemplatesIds))
		if activeTemplatesIds:
			if self.__settingsSeparator in activeTemplatesIds:
				ids = activeTemplatesIds.split(self.__settingsSeparator)
			else:
				ids = [activeTemplatesIds]
			self.__modelSelection["Templates"] = [int(id) for id in ids]

		self.__Templates_Outliner_treeView_restoreModelSelection()

	@core.executionTrace
	def onClose(self):
		"""
		This Method Is Called On Framework Close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework Close Method.".format(self.__class__.__name__))

		self.__Templates_Outliner_treeView_storeModelSelection()
		self.__settings.setKey(self.__settingsSection, "activeTemplates", self.__settingsSeparator.join(str(id) for id in self.__modelSelection["Templates"]))
		self.__settings.setKey(self.__settingsSection, "activeCollections", self.__settingsSeparator.join(str(id) for id in self.__modelSelection["Collections"]))
		self.__settings.setKey(self.__settingsSection, "activeSoftwares", self.__settingsSeparator.join(str(id) for id in self.__modelSelection["Softwares"]))

	@core.executionTrace
	def __Templates_Outliner_treeView_setModel(self):
		"""
		This Method Sets The Templates_Outliner_treeView Model.
		
		Columns:
		Templates | Release | Software Version
		
		Rows:
		* Collection: { _type: "Collection" }
		** Software: { _type: "Software" }
		***	Template: { _type: "Template", _datas: dbTypes.DbTemplate }
		"""

		LOGGER.debug("> Setting Up '{0}' Model!".format("Templates_Outliner_treeView"))

		self.__Templates_Outliner_treeView_storeModelSelection()

		self.__model.clear()

		self.__model.setHorizontalHeaderLabels(self.__modelHeaders)
		self.__model.setColumnCount(len(self.__modelHeaders))

		collections = dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type")

		for collection in collections:
			softwares = set((software[0] for software in self.__coreDb.dbSession.query(dbTypes.DbTemplate.software).filter(dbTypes.DbTemplate.collection == collection.id)))

			if softwares:
				LOGGER.debug("> Preparing '{0}' Collection For '{1}' Model.".format(collection.name, "Templates_Outliner_treeView"))

				collectionStandardItem = QStandardItem(QString(collection.name))
				collectionStandardItem._datas = collection
				collectionStandardItem._type = "Collection"

				LOGGER.debug("> Adding '{0}' Collection To '{1}' Model.".format(collection.name, "Templates_Outliner_treeView"))
				self.__model.appendRow(collectionStandardItem)

				for software in softwares:
					templates = set((template[0] for template in self.__coreDb.dbSession.query(dbTypes.DbTemplate.id).filter(dbTypes.DbTemplate.collection == collection.id).filter(dbTypes.DbTemplate.software == software)))

					if templates:
						LOGGER.debug("> Preparing '{0}' Software For '{1}' Model.".format(software, "Templates_Outliner_treeView"))

						softwareStandardItem = QStandardItem(QString(software))
						iconPath = os.path.join(self.__uiResources, "{0}{1}".format(software, self.__uiSoftwareAffixe))
						if os.path.exists(iconPath):
							softwareStandardItem.setIcon(QIcon(iconPath))
						else:
							softwareStandardItem.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiUnknownSoftwareImage)))

						softwareStandardItem._type = "Software"

						LOGGER.debug("> Adding '{0}' Software To '{1}' Model.".format(software, "Templates_Outliner_treeView"))
						collectionStandardItem.appendRow([softwareStandardItem, None, None])

						for template in templates:
							template = dbCommon.filterTemplates(self.__coreDb.dbSession, "^{0}$".format(template), "id")[0]

							LOGGER.debug("> Preparing '{0}' Template For '{1}' Model.".format(template.name, "Templates_Outliner_treeView"))

							try:
								templateStandardItem = QStandardItem(QString("{0} {1}".format(template.renderer, template.title)))

								templateReleaseStandardItem = QStandardItem(QString(template.release))
								templateReleaseStandardItem.setTextAlignment(Qt.AlignCenter)

								templateVersionStandardItem = QStandardItem(QString(template.version))
								templateVersionStandardItem.setTextAlignment(Qt.AlignCenter)

								templateStandardItem._datas = template
								templateStandardItem._type = "Template"

								LOGGER.debug("> Adding '{0}' Template To '{1}' Model.".format(template.name, "Templates_Outliner_treeView"))
								softwareStandardItem.appendRow([templateStandardItem, templateReleaseStandardItem, templateVersionStandardItem])

							except Exception as error:
								LOGGER.error("!>{0} | Exception Raised While Adding '{1}' Template To '{2}' Model!".format(self.__class__.__name__, template.name, "Templates_Outliner_treeView"))
								foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "__Templates_Outliner_treeView_setModel"))

		self.__Templates_Outliner_treeView_restoreModelSelection()

		self.emit(SIGNAL("modelChanged()"))

	@core.executionTrace
	def __Templates_Outliner_treeView_refreshModel(self):
		"""
		This Method Refreshes The Templates_Outliner_treeView Model.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Templates_Outliner_treeView"))

		self.__Templates_Outliner_treeView_setModel()

	@core.executionTrace
	def __Templates_Outliner_treeView_setView(self):
		"""
		This Method Sets The Templates_Outliner_treeView View.
		"""

		LOGGER.debug("> Initializing '{0}' Widget!".format("Templates_Outliner_treeView"))

		self.ui.Templates_Outliner_treeView.setAutoScroll(False)
		self.ui.Templates_Outliner_treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.ui.Templates_Outliner_treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.Templates_Outliner_treeView.setIndentation(self.__treeViewIndentation)
		self.ui.Templates_Outliner_treeView.setSortingEnabled(True)

		self.ui.Templates_Outliner_treeView.setModel(self.__model)

		self.__Templates_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def __Templates_Outliner_treeView_setDefaultViewState(self):
		"""
		This Method Sets Templates_Outliner_treeView Default View State.
		"""

		LOGGER.debug("> Setting '{0}' Default View State!".format("Templates_Outliner_treeView"))

		self.ui.Templates_Outliner_treeView.expandAll()
		for column in range(len(self.__modelHeaders)):
			self.ui.Templates_Outliner_treeView.resizeColumnToContents(column)

		self.ui.Templates_Outliner_treeView.sortByColumn(0, Qt.AscendingOrder)

	@core.executionTrace
	def __Templates_Outliner_treeView_refreshView(self):
		"""
		This Method Refreshes The Templates_Outliner_treeView View.
		"""

		self.__Templates_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def __Templates_Outliner_treeView_storeModelSelection(self):
		"""
		This Method Stores Templates_Outliner_treeView Model Selection.
		"""

		LOGGER.debug("> Storing '{0}' Model Selection!".format("Templates_Outliner_treeView"))

		self.__modelSelection = {"Collections":[], "Softwares":[], "Templates":[]}
		for item in self.getSelectedItems():
			if item._type == "Collection":
				self.__modelSelection["Collections"].append(item.text())
			elif item._type == "Software":
				self.__modelSelection["Softwares"].append(item.text())
			else:
				self.__modelSelection["Templates"].append(item._datas.id)

	@core.executionTrace
	def __Templates_Outliner_treeView_restoreModelSelection(self):
		"""
		This Method Restores Templates_Outliner_treeView Model Selection.
		"""

		LOGGER.debug("> Restoring '{0}' Model Selection!".format("Templates_Outliner_treeView"))

		indexes = []
		for i in range(self.__model.rowCount()):
			collectionStandardItem = self.__model.item(i)
			collectionStandardItem.text() in self.__modelSelection["Collections"] and indexes.append(self.__model.indexFromItem(collectionStandardItem))
			for j in range(collectionStandardItem.rowCount()):
				softwareStandardItem = collectionStandardItem.child(j, 0)
				softwareStandardItem.text() in self.__modelSelection["Softwares"] and indexes.append(self.__model.indexFromItem(softwareStandardItem))
				for k in range(softwareStandardItem.rowCount()):
					templateStandardItem = softwareStandardItem.child(k, 0)
					templateStandardItem._datas.id in self.__modelSelection["Templates"] and indexes.append(self.__model.indexFromItem(templateStandardItem))

		selectionModel = self.ui.Templates_Outliner_treeView.selectionModel()
		if selectionModel:
			selectionModel.clear()
			for index in indexes:
				selectionModel.setCurrentIndex(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

	@core.executionTrace
	def __Templates_Outliner_treeView_addActions(self):
		"""
		This Method Sets The Templates_Outliner_treeView Actions.
		"""

		if not self.__container.parameters.databaseReadOnly:
			addTemplateAction = QAction("Add Template ...", self.ui.Templates_Outliner_treeView)
			addTemplateAction.triggered.connect(self.__Templates_Outliner_treeView_addTemplateAction__triggered)
			self.ui.Templates_Outliner_treeView.addAction(addTemplateAction)

			removeTemplatesAction = QAction("Remove Template(s) ...", self.ui.Templates_Outliner_treeView)
			removeTemplatesAction.triggered.connect(self.__Templates_Outliner_treeView_removeTemplatesAction__triggered)
			self.ui.Templates_Outliner_treeView.addAction(removeTemplatesAction)

			separatorAction = QAction(self.ui.Templates_Outliner_treeView)
			separatorAction.setSeparator(True)
			self.ui.Templates_Outliner_treeView.addAction(separatorAction)

			importDefaultTemplatesAction = QAction("Import Default Templates", self.ui.Templates_Outliner_treeView)
			importDefaultTemplatesAction.triggered.connect(self.__Templates_Outliner_treeView_importDefaultTemplatesAction__triggered)
			self.ui.Templates_Outliner_treeView.addAction(importDefaultTemplatesAction)

			filterTemplatesVersionsAction = QAction("Filter Templates Versions", self.ui.Templates_Outliner_treeView)
			filterTemplatesVersionsAction.triggered.connect(self.__Templates_Outliner_treeView_filterTemplatesVersionsAction__triggered)
			self.ui.Templates_Outliner_treeView.addAction(filterTemplatesVersionsAction)

			separatorAction = QAction(self.ui.Templates_Outliner_treeView)
			separatorAction.setSeparator(True)
			self.ui.Templates_Outliner_treeView.addAction(separatorAction)
		else:
			LOGGER.info("{0} | Templates Database Alteration Capabilities Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		displayHelpFilesAction = QAction("Display Help File(s) ...", self.ui.Templates_Outliner_treeView)
		displayHelpFilesAction.triggered.connect(self.__Templates_Outliner_treeView_displayHelpFilesAction__triggered)
		self.ui.Templates_Outliner_treeView.addAction(displayHelpFilesAction)

		separatorAction = QAction(self.ui.Templates_Outliner_treeView)
		separatorAction.setSeparator(True)
		self.ui.Templates_Outliner_treeView.addAction(separatorAction)

	@core.executionTrace
	def __Templates_Outliner_treeView_addTemplateAction__triggered(self, checked):
		"""
		This Method Is Triggered By addTemplateAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.addTemplate__()

	@core.executionTrace
	def __Templates_Outliner_treeView_removeTemplatesAction__triggered(self, checked):
		"""
		This Method Is Triggered By removeTemplatesAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.removeTemplates__()

	@core.executionTrace
	def __Templates_Outliner_treeView_importDefaultTemplatesAction__triggered(self, checked):
		"""
		This Method Is Triggered By importDefaultTemplatesAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.importDefaultTemplates__()

	@core.executionTrace
	def __Templates_Outliner_treeView_displayHelpFilesAction__triggered(self, checked):
		"""
		This Method Is Triggered By displayHelpFilesAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.displayHelpFiles__()

	@core.executionTrace
	def __Templates_Outliner_treeView_filterTemplatesVersionsAction__triggered(self, checked):
		"""
		This Method Is Triggered By filterTemplatesVersionsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.filterTemplatesVersions__()

	@core.executionTrace
	def __Templates_Outliner_treeView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This Method Sets The Template_Informations_textEdit Widget.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		"""

		LOGGER.debug("> Initializing '{0}' Widget.".format("Template_Informations_textEdit"))

		selectedTemplates = self.getSelectedTemplates()
		content = []

		if selectedTemplates:
			for template in selectedTemplates:
				template and content.append(self.__templatesInformationsText.format("{0} {1} {2}".format(template.software, template.renderer, template.title),
												template.date,
												template.author,
												template.email,
												template.url,
												template.outputScript,
												template.comment,
												QUrl.fromLocalFile(template.helpFile).toString()))
		else:
			content.append(self.__templatesInformationsDefaultText)

		separator = len(content) == 1 and "" or "<p><center>* * *<center/></p>"

		self.ui.Template_Informations_textBrowser.setText(separator.join(content))

	@core.executionTrace
	def __Template_Informations_textBrowser__anchorClicked(self, url):
		"""
		This Method Is Triggered When A Link Is Clicked In The Template_Informations_textBrowser Widget.

		@param url: Url To Explore. ( QUrl )
		"""

		QDesktopServices.openUrl(url)

	@core.executionTrace
	def __coreDb_database__changed(self):
		"""
		This Method Is Triggered By The TemplatesOutliner_Worker When The Database Has Changed.
		"""

		# Ensure That Db Objects Modified By The Worker Thread Will Refresh Properly.
		self.__coreDb.dbSession.expire_all()
		self.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def addTemplate__(self):
		"""
		This Method Adds An User Defined Template To The Database.
		
		@return: Method Success. ( Boolean )		
		"""

		path = self.__container.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Add Template:", self.__container.lastBrowsedPath, "sIBLT Files (*.{0})".format(self.__extension))))
		if not path:
			return

		if not self.templateExists(path):
			LOGGER.debug("> Chosen Template Path: '{0}'.".format(path))
			if self.addTemplate(strings.getSplitextBasename(path), path):
				return True
			else:
				raise Exception, "{0} | Exception Raised While Adding '{1}' Template To The Database!".format(self.__class__.__name__, path)
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Template Already Exists In Database!".format(self.__class__.__name__, path))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def removeTemplates__(self):
		"""
		This Method Removes User Selected Templates From The Database.
		
		@return: Method Success. ( Boolean )		
		"""

		selectedItems = self.getSelectedItems()

		selectedCollections = []
		selectedSoftwares = []
		selectedTemplates = []

		for item in selectedItems:
			if item._type == "Collection":
				selectedCollections.append(str(item.text()))
			elif item._type == "Software":
				selectedSoftwares.append(str(item.text()))
			else:
				selectedTemplates.append(item._datas)

		selectedCollections and messageBox.messageBox("Warning", "Warning", "{0} | Cannot Remove '{1}' Collection(s)!".format(self.__class__.__name__, ", ".join(selectedCollections)))
		selectedSoftwares and messageBox.messageBox("Warning", "Warning", "{0} | Cannot Remove '{1}' Software(s)!".format(self.__class__.__name__, ", ".join(selectedSoftwares)))

		if not selectedTemplates:
			return

		if messageBox.messageBox("Question", "Question", "Are You Sure You Want To Remove '{0}' Template(s)?".format(", ".join([str(template.name) for template in selectedTemplates])), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
			success = True
			for template in selectedTemplates:
				success *= self.removeTemplate(template, emitSignal=False) or False

			self.emit(SIGNAL("modelRefresh()"))

			if success:
				return True
			else:
				raise Exception, "{0} | Exception Raised While Removing '{1}' Templates From The Database!".format(self.__class__.__name__, ", ". join((template.name for template in selectedTemplates)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def importDefaultTemplates__(self):
		"""
		This Method Imports Default Templates Into The Database.
		
		@return: Method Success. ( Boolean )		
		"""

		if self.addDefaultTemplates(forceImport=True):
			return True
		else:
			raise Exception, "{0} | Exception Raised While Importing Default Templates Into The Database!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def displayHelpFiles__(self):
		"""
		This Method Displays User Selected Templates Help Files.
		
		@return: Method Success. ( Boolean )		
		"""

		selectedTemplates = self.getSelectedTemplates()
		if not selectedTemplates:
			return

		success = True
		for template in selectedTemplates:
			success *= self.displayHelpFile(template) or False

		if success:
			return True
		else:
			raise Exception, "{0} | Exception Raised While Displaying Templates Help Files!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def filterTemplatesVersions__(self):
		"""
		This Method Filters Templates By Versions.
		
		@return: Method Success. ( Boolean )		
		"""

		templates = dbCommon.getTemplates(self.__coreDb.dbSession)
		for template in templates:
			matchingTemplates = dbCommon.filterTemplates(self.__coreDb.dbSession, "^{0}$".format(template.name), "name")
			if len(matchingTemplates) != 1:
				success = True
				for id in sorted([(dbTemplate.id, dbTemplate.release) for dbTemplate in matchingTemplates], reverse=True, key=lambda x:(strings.getVersionRank(x[1])))[1:]:
					success *= dbCommon.removeTemplate(self.__coreDb.dbSession, id[0]) or False

				self.emit(SIGNAL("modelRefresh()"))

				if success:
					return True
				else:
					raise Exception, "{0} | Exception Raised While Filtering Templates By Versions!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError, foundations.exceptions.DatabaseOperationError)
	def addTemplate(self, name, path, collectionId=None, emitSignal=True):
		"""
		This Method Adds A Template To The Database.
		
		@param name: Template Set Name. ( String )		
		@param path: Template Set Path. ( String )		
		@param collectionId: Target Collection Id. ( Integer )		
		@param emitSignal: Emit Signal. ( Boolean )
		@return: Method Success. ( Boolean )		
		"""

		if not dbCommon.filterTemplates(self.__coreDb.dbSession, "^{0}$".format(re.escape(path)), "path"):
			LOGGER.info("{0} | Adding '{1}' Template To The Database!".format(self.__class__.__name__, name))
			if dbCommon.addTemplate(self.__coreDb.dbSession, name, path, collectionId or self.getUniqueCollectionId(path)):
				emitSignal and self.emit(SIGNAL("modelRefresh()"))
				return True
			else:
				raise foundations.exceptions.DatabaseOperationError, "{0} | Exception Raised While Adding '{1}' Template To The Database!".format(self.__class__.__name__, name)
		else:
			raise foundations.exceptions.ProgrammingError, "{0} | '{1}' Template Already Exists In Database!".format(self.__class__.__name__, name)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addDirectory(self, directory, collectionId=None):
		"""
		This Method Adds Provided Directory Templates To The Database.
		
		@param directory: Templates Directory. ( String )
		@param collectionId: Collection Id. ( Integer )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing Directory '{0}' Walker.".format(directory))

		walker = Walker(directory)
		walker.walk(("\.{0}$".format(self.__extension),), ("\._",))

		success = True
		for template, path in walker.files.items():
			if not self.templateExists(path):
				success *= self.addTemplate(namespace.getNamespace(template, rootOnly=True), path, collectionId, emitSignal=False) or False

		self.emit(SIGNAL("modelRefresh()"))

		if success:
			return True
		else:
			raise Exception, "{0} | Exception Raised While Adding '{1}' Directory Content To The Database!".format(self.__class__.__name__, directory)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addDefaultTemplates(self, forceImport=False):
		"""
		This Method Adds Default Templates Collections / Templates To The Database.
		
		@param forceImport: Force Templates Import. ( Boolean )
		@return: Method Success. ( Boolean )		
		"""

		if not forceImport and self.getTemplates():
			return

		LOGGER.debug("> Adding Default Templates To The Database.")
		for collection, path in self.__defaultCollections.items():
			if not os.path.exists(path):
				continue

			if not set(dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(collection), "name")).intersection(dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type")):
				LOGGER.info("{0} | Adding '{1}' Collection To The Database!".format(self.__class__.__name__, collection))
				dbCommon.addCollection(self.__coreDb.dbSession, collection, "Templates", "Template {0} Collection".format(collection))
			if self.addDirectory(path, self.getCollection(collection).id):
				return True
			else:
				raise Exception, "{0} | Exception Raised While Adding Default Templates To The Database!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.DatabaseOperationError)
	def removeTemplate(self, template, emitSignal=True):
		"""
		This Method Removes Provided Template From The Database.

		@param templates: Template To Remove. ( List )
		@param emitSignal: Emit Signal. ( Boolean )
		@return: Method Success. ( Boolean )	
		"""

		LOGGER.info("{0} | Removing '{1}' Template From The Database!".format(self.__class__.__name__, template.name))
		if dbCommon.removeTemplate(self.__coreDb.dbSession, str(template.id)) :
			emitSignal and self.emit(SIGNAL("modelRefresh()"))
			return True
		else:
			raise foundations.exceptions.DatabaseOperationError, "{0} | Exception Raised While Removing '{1}' Template From The Database!".format(self.__class__.__name__, template.name)

	@core.executionTrace
	def templateExists(self, path):
		"""
		This Method Returns If Provided Template Path Exists In The Database.
		
		@param name: Template Path. ( String )
		@return: Template Exists. ( Boolean )
		"""

		return dbCommon.templateExists(self.__coreDb.dbSession, path)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.DatabaseOperationError)
	def updateTemplateLocation(self, template, emitSignal=True):
		"""
		This Method Updates Provided Template Location.
		
		@param template: Template To Update. ( DbTemplate )
		@param emitSignal: Emit Signal. ( Boolean )
		@return: Method Success. ( Boolean )	
		"""

		file = self.__container.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Updating '{0}' Template Location:".format(template.name), self.__container.lastBrowsedPath, "Template Files (*{0})".format(self.__extension))))
		if not file:
			return

		LOGGER.info("{0} | Updating '{1}' Template With New Location '{2}'!".format(self.__class__.__name__, template.name, file))
		if not dbCommon.updateTemplateLocation(self.__coreDb.dbSession, template, file):
			emitSignal and self.emit(SIGNAL("modelRefresh()"))
			return True
		else:
			raise foundations.exceptions.DatabaseOperationError, "{0} | Exception Raised While Updating '{1}' Template Location!".format(self.__class__.__name__, template.name)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def displayHelpFile(self, template):
		"""
		This Method Displays Provided Templates Help File.

		@param template: Template To Display Help File. ( DbTemplate )
		@return: Method Success. ( Boolean )	
		"""

		if os.path.exists(template.helpFile):
			LOGGER.info("{0} | Opening '{1}' Template Help File: '{2}'.".format(self.__class__.__name__, template.name, template.helpFile))
			QDesktopServices.openUrl(QUrl.fromLocalFile(template.helpFile))
			return True
		else:
			raise OSError, "{0} | Exception Raised While Displaying '{1}' Template Help File: '{2}' File Doesn't Exists!".format(self.__class__.__name__, template.name, template.helpFile)

	@core.executionTrace
	def getTemplates(self):
		"""
		This Method Returns Database Templates.
		
		@return: Database Templates Collections. ( List )
		"""

		return [template for template in dbCommon.getTemplates(self.__coreDb.dbSession)]

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This Method Returns The Templates_Outliner_treeView Selected Items.
		
		@param rowsRootOnly: Return Rows Roots Only. ( Boolean )
		@return: View Selected Items. ( List )
		"""

		selectedIndexes = self.ui.Templates_Outliner_treeView.selectedIndexes()
		return rowsRootOnly and [item for item in set([self.__model.itemFromIndex(self.__model.sibling(index.row(), 0, index)) for index in selectedIndexes])] or [self.__model.itemFromIndex(index) for index in selectedIndexes]

	@core.executionTrace
	def getSelectedTemplates(self):
		"""
		This Method Returns The Selected Templates.
		
		@return: View Selected Templates. ( List )
		"""

		selectedItems = self.getSelectedItems()
		return selectedItems and [item._datas for item in selectedItems if item._type == "Template"] or []

	@core.executionTrace
	def getCollection(self, collection):
		"""
		This Method Gets Template Collection From Provided Collection Name.
		
		@param collection: Collection Name. ( String )
		@return: Collection. ( DbCollection )
		"""

		return [collection for collection in set(dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(collection), "name")).intersection(dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type"))][0]

	@core.executionTrace
	def getUniqueCollectionId(self, path):
		"""
		This Method Gets An Unique Collection Id Using Provided Path.
		
		@param path: Template Path. ( String )
		@return: Unique Id. ( Integer )
		"""

		templatesCollections = dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type")
		return self.defaultCollections[self.__factoryCollection] in path and [collection for collection in set(dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(self.__factoryCollection), "name")).intersection(templatesCollections)][0].id or [collection for collection in set(dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(self.__userCollection), "name")).intersection(templatesCollections)][0].id

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
