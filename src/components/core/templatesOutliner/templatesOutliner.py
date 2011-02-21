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

'''
************************************************************************************************
***	componentsManagerUi.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Components Manager Ui Component Module.
***
***	Others:
***
************************************************************************************************
'''

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
import dbUtilities.common
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.strings as strings
import ui.common
import ui.widgets.messageBox as messageBox
from globals.constants import Constants
from manager.uiComponent import UiComponent
from foundations.walker import Walker

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class TemplatesOutliner_Worker(QThread):
	'''
	This Class Is The TemplatesOutliner_Worker Class.
	'''

	# Custom Signals Definitions.
	databaseChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, container):
		'''
		This Method Initializes The Class.
		
		@param container: Object Container. ( Object )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QThread.__init__(self, container)

		# --- Setting Class Attributes. ---
		self._container = container

		self._dbSession = self._container.coreDb.dbSessionMaker()

		self._timer = None
		self._timerCycleMultiplier = 5

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def dbSession(self):
		'''
		This Method Is The Property For The _dbSession Attribute.

		@return: self._dbSession. ( Object )
		'''

		return self._dbSession

	@dbSession.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSession(self, value):
		'''
		This Method Is The Setter Method For The _dbSession Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dbSession"))

	@dbSession.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dbSession(self):
		'''
		This Method Is The Deleter Method For The _dbSession Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dbSession"))


	@property
	def timer(self):
		'''
		This Method Is The Property For The _timer Attribute.

		@return: self._timer. ( QTimer )
		'''

		return self._timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self, value):
		'''
		This Method Is The Setter Method For The _timer Attribute.

		@param value: Attribute Value. ( QTimer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("timer"))

	@timer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self):
		'''
		This Method Is The Deleter Method For The _timer Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("timer"))

	@property
	def timerCycleMultiplier(self):
		'''
		This Method Is The Property For The _timerCycleMultiplier Attribute.

		@return: self._timerCycleMultiplier. ( Float )
		'''

		return self._timerCycleMultiplier

	@timerCycleMultiplier.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self, value):
		'''
		This Method Is The Setter Method For The _timerCycleMultiplier Attribute.

		@param value: Attribute Value. ( Float )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("timerCycleMultiplier"))

	@timerCycleMultiplier.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self):
		'''
		This Method Is The Deleter Method For The _timerCycleMultiplier Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("timerCycleMultiplier"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def run(self):
		'''
		This Method Starts The QThread.
		'''

		self._timer = QTimer()
		self._timer.moveToThread(self)
		self._timer.start(Constants.defaultTimerCycle * self._timerCycleMultiplier)

		self._timer.timeout.connect(self.updateTemplates, Qt.DirectConnection)

		self.exec_()

	@core.executionTrace
	def updateTemplates(self):
		'''
		This Method Updates Database Templates If They Have Been Modified On Disk.
		'''

		needModelRefresh = False
		for template in dbUtilities.common.getTemplates(self._dbSession):
			if template.path:
				if os.path.exists(template.path):
					storedStats = template.osStats.split(",")
					osStats = os.stat(template.path)
					if str(osStats[8]) != str(storedStats[8]):
						LOGGER.info("{0} | '{1}' Template File Has Been Modified And Will Be Updated!".format(self.__class__.__name__, template.name))
						if dbUtilities.common.updateTemplateContent(self._dbSession, template):
							LOGGER.info("{0} | '{1}' Template Has Been Updated!".format(self.__class__.__name__, template.name))
							needModelRefresh = True

		needModelRefresh and self.emit(SIGNAL("databaseChanged()"))

class TemplatesOutliner_QTreeView(QTreeView):
	'''
	This Class Is The TemplatesOutliner_QTreeView Class.
	'''

	@core.executionTrace
	def __init__(self, container):
		'''
		This Method Initializes The Class.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QTreeView.__init__(self, container)

		self.setAcceptDrops(True)


		# --- Setting Class Attributes. ---
		self._container = container

		self._coreTemplatesOutliner = self._container.componentsManager.components["core.templatesOutliner"].interface

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def coreTemplatesOutliner(self):
		'''
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self._coreTemplatesOutliner. ( Object )
		'''

		return self._coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self, value):
		'''
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreTemplatesOutliner"))

	@coreTemplatesOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreTemplatesOutliner(self):
		'''
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreTemplatesOutliner"))
	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def dragEnterEvent(self, event):
		'''
		This Method Defines The Drag Enter Event Behavior.
		
		@param event: QEvent. ( QEvent )
		'''

		if event.mimeData().hasFormat("text/uri-list"):
			LOGGER.debug("> '{0}' Drag Event Type Accepted!".format("text/uri-list"))
			event.accept()
		else:
			event.ignore()

	@core.executionTrace
	def dragMoveEvent(self, event):
		'''
		This Method Defines The Drag Move Event Behavior.
		
		@param event: QEvent. ( QEvent )
		'''

		pass

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, OSError, foundations.exceptions.UserError)
	def dropEvent(self, event):
		'''
		This Method Defines The Drop Event Behavior.
		
		@param event: QEvent. ( QEvent )		
		'''

		if not self._container.parameters.databaseReadOnly:
			if event.mimeData().hasUrls():
				LOGGER.debug("> Drag Event Urls List: '{0}'!".format(event.mimeData().urls()))
				for url in event.mimeData().urls():
					path = (platform.system() == "Windows" or platform.system() == "Microsoft") and re.search("^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
					if re.search("\.{0}$".format(self._coreTemplatesOutliner.extension), str(url.path())):
						name = strings.getSplitextBasename(path)
						if messageBox.messageBox("Question", "Question", "'{0}' Template Set File Has Been Dropped, Would You Like To Add It To The Database?".format(name), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
							self._coreTemplatesOutliner.addTemplate(name, path) and self._coreTemplatesOutliner.Templates_Outliner_treeView_refreshModel()
					else:
						if os.path.isdir(path):
							if messageBox.messageBox("Question", "Question", "'{0}' Directory Has Been Dropped, Would You Like To Add Its Content To The Database?".format(path), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
								self._coreTemplatesOutliner.addDirectory(path)
								self._coreTemplatesOutliner.Templates_Outliner_treeView_refreshModel()
						else:
							raise OSError, "{0} | Exception Raised While Parsing '{1}' Path: Syntax Is Invalid!".format(self.__class__.__name__, path)
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only!".format(self.__class__.__name__)

class TemplatesOutliner(UiComponent):
	'''
	This Class Is The TemplatesOutliner Class.
	'''

	# Custom Signals Definitions.
	modelChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
		self.deactivatable = False

		self._uiPath = "ui/Templates_Outliner.ui"
		self._uiResources = "resources"
		self._uiSoftwareAffixe = "_Software.png"
		self._uiUnknownSoftwareIcon = "Unknown_Software.png"
		self._dockArea = 1

		self._container = None

		self._coreDb = None

		self._model = None
		self._modelSelection = None

		self._templatesOutlinerWorkerThread = None

		self._extension = "sIBLT"

		self._defaultCollections = None
		self._factoryCollection = "Factory"
		self._userCollection = "User"

		self._modelHeaders = [ "Templates", "Release", "Software Version" ]
		self._treeViewIndentation = 15
		self._treeViewInnerMargins = QMargins(0, 0, 0, 12)
		self._Template_Informations_textBrowser_defaultText = "<center><h4>* * *</h4>Select A Template To Display Related Informations!<h4>* * *</h4></center>"

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		'''
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		'''

		return self._uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		'''
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		'''
		This Method Is The Deleter Method For The _uiResources Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def uiSoftwareAffixe(self):
		'''
		This Method Is The Property For The _uiSoftwareAffixe Attribute.

		@return: self._uiSoftwareAffixe. ( String )
		'''

		return self._uiSoftwareAffixe

	@uiSoftwareAffixe.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSoftwareAffixe(self, value):
		'''
		This Method Is The Setter Method For The _uiSoftwareAffixe Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiSoftwareAffixe"))

	@uiSoftwareAffixe.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSoftwareAffixe(self):
		'''
		This Method Is The Deleter Method For The _uiSoftwareAffixe Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiSoftwareAffixe"))

	@property
	def uiUnknownSoftwareIcon(self):
		'''
		This Method Is The Property For The _uiUnknownSoftwareIcon Attribute.

		@return: self._uiUnknownSoftwareIcon. ( String )
		'''

		return self._uiUnknownSoftwareIcon

	@uiUnknownSoftwareIcon.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUnknownSoftwareIcon(self, value):
		'''
		This Method Is The Setter Method For The _uiUnknownSoftwareIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiUnknownSoftwareIcon"))

	@uiUnknownSoftwareIcon.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUnknownSoftwareIcon(self):
		'''
		This Method Is The Deleter Method For The _uiUnknownSoftwareIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiUnknownSoftwareIcon"))

	@property
	def dockArea(self):
		'''
		This Method Is The Property For The _dockArea Attribute.

		@return: self._dockArea. ( Integer )
		'''

		return self._dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		'''
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		'''
		This Method Is The Deleter Method For The _dockArea Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("dockArea"))

	@property
	def container(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def coreDb(self):
		'''
		This Method Is The Property For The _coreDb Attribute.

		@return: self._coreDb. ( Object )
		'''

		return self._coreDb

	@coreDb.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self, value):
		'''
		This Method Is The Setter Method For The _coreDb Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDb"))

	@coreDb.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDb(self):
		'''
		This Method Is The Deleter Method For The _coreDb Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDb"))

	@property
	def model(self):
		'''
		This Method Is The Property For The _model Attribute.

		@return: self._model. ( QStandardItemModel )
		'''

		return self._model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		'''
		This Method Is The Setter Method For The _model Attribute.

		@param value: Attribute Value. ( QStandardItemModel )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		'''
		This Method Is The Deleter Method For The _model Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("model"))

	@property
	def modelSelection(self):
		'''
		This Method Is The Property For The _modelSelection Attribute.

		@return: self._modelSelection. ( Dictionary )
		'''

		return self._modelSelection

	@modelSelection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self, value):
		'''
		This Method Is The Setter Method For The _modelSelection Attribute.

		@param value: Attribute Value. ( Dictionary )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("modelSelection"))

	@modelSelection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self):
		'''
		This Method Is The Deleter Method For The _modelSelection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("modelSelection"))

	@property
	def templatesOutlinerWorkerThread(self):
		'''
		This Method Is The Property For The _templatesOutlinerWorkerThread Attribute.

		@return: self._templatesOutlinerWorkerThread. ( QThread )
		'''

		return self._templatesOutlinerWorkerThread

	@templatesOutlinerWorkerThread.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesOutlinerWorkerThread(self, value):
		'''
		This Method Is The Setter Method For The _templatesOutlinerWorkerThread Attribute.

		@param value: Attribute Value. ( QThread )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("templatesOutlinerWorkerThread"))

	@templatesOutlinerWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesOutlinerWorkerThread(self):
		'''
		This Method Is The Deleter Method For The _templatesOutlinerWorkerThread Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("templatesOutlinerWorkerThread"))

	@property
	def extension(self):
		'''
		This Method Is The Property For The _extension Attribute.

		@return: self._extension. ( String )
		'''

		return self._extension

	@extension.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self, value):
		'''
		This Method Is The Setter Method For The _extension Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("extension"))

	@extension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self):
		'''
		This Method Is The Deleter Method For The _extension Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("extension"))

	@property
	def defaultCollections(self):
		'''
		This Method Is The Property For The _defaultCollections Attribute.

		@return: self._defaultCollections. ( Dictionary )
		'''

		return self._defaultCollections

	@defaultCollections.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollections(self, value):
		'''
		This Method Is The Setter Method For The _defaultCollections Attribute.

		@param value: Attribute Value. ( Dictionary )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("defaultCollections"))

	@defaultCollections.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollections(self):
		'''
		This Method Is The Deleter Method For The _defaultCollections Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("defaultCollections"))

	@property
	def factoryCollection(self):
		'''
		This Method Is The Property For The _factoryCollection Attribute.

		@return: self._factoryCollection. ( String )
		'''

		return self._factoryCollection

	@factoryCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryCollection(self, value):
		'''
		This Method Is The Setter Method For The _factoryCollection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("factoryCollection"))

	@factoryCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryCollection(self):
		'''
		This Method Is The Deleter Method For The _factoryCollection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("factoryCollection"))

	@property
	def userCollection(self):
		'''
		This Method Is The Property For The _userCollection Attribute.

		@return: self._userCollection. ( String )
		'''

		return self._userCollection

	@userCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userCollection(self, value):
		'''
		This Method Is The Setter Method For The _userCollection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("userCollection"))

	@userCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userCollection(self):
		'''
		This Method Is The Deleter Method For The _userCollection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("userCollection"))

	@property
	def modelHeaders(self):
		'''
		This Method Is The Property For The _modelHeaders Attribute.

		@return: self._modelHeaders. ( List )
		'''

		return self._modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self, value):
		'''
		This Method Is The Setter Method For The _modelHeaders Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("modelHeaders"))

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self):
		'''
		This Method Is The Deleter Method For The _modelHeaders Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("modelHeaders"))

	@property
	def treeViewIndentation(self):
		'''
		This Method Is The Property For The _treeViewIndentation Attribute.

		@return: self._treeViewIndentation. ( Integer )
		'''

		return self._treeViewIndentation

	@treeViewIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self, value):
		'''
		This Method Is The Setter Method For The _treeViewIndentation Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("treeViewIndentation"))

	@treeViewIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self):
		'''
		This Method Is The Deleter Method For The _treeViewIndentation Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("treeViewIndentation"))

	@property
	def treeViewInnerMargins(self):
		'''
		This Method Is The Property For The _treeViewInnerMargins Attribute.

		@return: self._treeViewInnerMargins. ( Integer )
		'''

		return self._treeViewInnerMargins

	@treeViewInnerMargins.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self, value):
		'''
		This Method Is The Setter Method For The _treeViewInnerMargins Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("treeViewInnerMargins"))

	@treeViewInnerMargins.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self):
		'''
		This Method Is The Deleter Method For The _treeViewInnerMargins Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("treeViewInnerMargins"))

	@property
	def Template_Informations_textBrowser_defaultText(self):
		'''
		This Method Is The Property For The _Template_Informations_textBrowser_defaultText Attribute.

		@return: self._Template_Informations_textBrowser_defaultText. ( String )
		'''

		return self._Template_Informations_textBrowser_defaultText

	@Template_Informations_textBrowser_defaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Template_Informations_textBrowser_defaultText(self, value):
		'''
		This Method Is The Setter Method For The _Template_Informations_textBrowser_defaultText Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("Template_Informations_textBrowser_defaultText"))

	@Template_Informations_textBrowser_defaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Template_Informations_textBrowser_defaultText(self):
		'''
		This Method Is The Deleter Method For The _Template_Informations_textBrowser_defaultText Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("Template_Informations_textBrowser_defaultText"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiPath)
		self._uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self._uiResources)
		self._container = container

		self._coreDb = self._container.componentsManager.components["core.db"].interface

		self._defaultCollections = { self._factoryCollection: os.path.join(os.getcwd(), Constants.templatesDirectory), self._userCollection: os.path.join(self._container.userApplicationDatasDirectory, Constants.templatesDirectory) }

		self._activate()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		'''
		This Method Deactivates The Component.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Component Cannot Be Deactivated!".format(self._name))

	@core.executionTrace
	def initializeUi(self):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

		self._model = QStandardItemModel()
		self.Templates_Outliner_treeView_setModel()

		self.ui.Templates_Outliner_treeView = TemplatesOutliner_QTreeView(self._container)
		self.ui.Templates_Outliner_gridLayout.setContentsMargins(self._treeViewInnerMargins)
		self.ui.Templates_Outliner_gridLayout.addWidget(self.ui.Templates_Outliner_treeView, 0, 0)

		self.ui.Templates_Outliner_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.Templates_Outliner_treeView_setActions()

		self.Templates_Outliner_treeView_setView()

		self.ui.Template_Informations_textBrowser.setText(self._Template_Informations_textBrowser_defaultText)
		self.ui.Template_Informations_textBrowser.setOpenLinks(False)

		self.ui.Templates_Outliner_splitter.setSizes([ 16777215, 1 ])

		if not self._container.parameters.databaseReadOnly:
			self._templatesOutlinerWorkerThread = TemplatesOutliner_Worker(self)
			self._templatesOutlinerWorkerThread.start()
			self._container.workerThreads.append(self._templatesOutlinerWorkerThread)
		else:
			LOGGER.info("{0} | Templates Continuous Scanner Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		# Signals / Slots.
		self.ui.Templates_Outliner_treeView.selectionModel().selectionChanged.connect(self.Templates_Outliner_treeView_OnSelectionChanged)
		self.ui.Template_Informations_textBrowser.anchorClicked.connect(self.Template_Informations_textBrowser_OnAnchorClicked)
		self.modelChanged.connect(self.Templates_Outliner_treeView_refreshView)
		not self._container.parameters.databaseReadOnly and self._templatesOutlinerWorkerThread.databaseChanged.connect(self.databaseChanged)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		'''
		This Method Uninitializes The Component Ui.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Component Ui Cannot Be Uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self._container.addDockWidget(Qt.DockWidgetArea(self._dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget Cannot Be Removed!".format(self.name))

	@core.executionTrace
	def onStartup(self):
		'''
		This Method Is Called On Framework Startup.
		'''

		LOGGER.debug("> Calling '{0}' Component Framework Startup Method.".format(self.__class__.__name__))

		if not self._container.parameters.databaseReadOnly:
			# Adding Default Templates.			
			self.addDefaultTemplates()

			# Templates Table Integrity Checking.
			erroneousTemplates = dbUtilities.common.checkTemplatesTableIntegrity(self._coreDb.dbSession)
			if erroneousTemplates:
				for template in erroneousTemplates:
					if erroneousTemplates[template] == "INEXISTING_TEMPLATE_FILE_EXCEPTION":
						if messageBox.messageBox("Question", "Error", "{0} | '{1}' Template File Is Missing, Would You Like To Update It's Location?".format(self.__class__.__name__, template.name), QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No) == 16384:
							self.updateTemplateLocation(template)
					else:
						messageBox.messageBox("Warning", "Warning", "{0} | '{1}' {2}".format(self.__class__.__name__, template.name, dbUtilities.common.DB_EXCEPTIONS[erroneousTemplates[template]]))
				self.Templates_Outliner_treeView_refreshModel()
		else:
			LOGGER.info("{0} | Database Default Templates Wizard And Templates Integrity Checking Method Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def Templates_Outliner_treeView_setModel(self):
		'''
		This Method Sets The Templates_Outliner_treeView Model.
		
		Columns:
		Templates | Release | Software Version
		
		Rows:
		* Collection: { _type: "Collection" }
		** Software: { _type: "Software" }
		***	Template: { _type: "Template", _datas: dbUtilities.types.DbTemplate }
		'''

		LOGGER.debug("> Setting Up '{0}' Model!".format("Templates_Outliner_treeView"))

		self.Templates_Outliner_treeView_storeModelSelection()

		self._model.clear()

		self._model.setHorizontalHeaderLabels(self._modelHeaders)
		self._model.setColumnCount(len(self._modelHeaders))

		collections = dbUtilities.common.filterCollections(self._coreDb.dbSession, "Templates", "type")

		for collection in collections:
			softwares = set((software[0] for software in self._coreDb.dbSession.query(dbUtilities.types.DbTemplate.software).filter(dbUtilities.types.DbTemplate.collection == collection.id)))

			if softwares:
				LOGGER.debug("> Preparing '{0}' Collection For '{1}' Model.".format(collection.name, "Templates_Outliner_treeView"))

				collectionStandardItem = QStandardItem(QString(collection.name))
				collectionStandardItem._datas = collection
				collectionStandardItem._type = "Collection"

				LOGGER.debug("> Adding '{0}' Collection To '{1}' Model.".format(collection.name, "Templates_Outliner_treeView"))
				self._model.appendRow(collectionStandardItem)

				for software in softwares:
					templates = set((template[0] for template in self._coreDb.dbSession.query(dbUtilities.types.DbTemplate.id).filter(dbUtilities.types.DbTemplate.collection == collection.id).filter(dbUtilities.types.DbTemplate.software == software)))

					if templates:
						LOGGER.debug("> Preparing '{0}' Software For '{1}' Model.".format(software, "Templates_Outliner_treeView"))

						softwareStandardItem = QStandardItem(QString(software))
						iconPath = os.path.join(self._uiResources, "{0}{1}".format(software, self._uiSoftwareAffixe))
						if os.path.exists(iconPath):
							softwareStandardItem.setIcon(QIcon(iconPath))
						else:
							softwareStandardItem.setIcon(QIcon(os.path.join(self._uiResources, self._uiUnknownSoftwareIcon)))

						softwareStandardItem._type = "Software"

						LOGGER.debug("> Adding '{0}' Software To '{1}' Model.".format(software, "Templates_Outliner_treeView"))
						collectionStandardItem.appendRow([softwareStandardItem, None, None])

						for template in templates:
							template = dbUtilities.common.filterTemplates(self._coreDb.dbSession, "^{0}$".format(template), "id")[0]

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
								foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "Templates_Outliner_treeView_setModel"))

		self.Templates_Outliner_treeView_restoreModelSelection()

		self.emit(SIGNAL("modelChanged()"))

	@core.executionTrace
	def Templates_Outliner_treeView_refreshModel(self):
		'''
		This Method Refreshes The Templates_Outliner_treeView Model.
		'''

		LOGGER.debug("> Refreshing '{0}' Model!".format("Templates_Outliner_treeView"))

		self.Templates_Outliner_treeView_setModel()

	@core.executionTrace
	def Templates_Outliner_treeView_setView(self):
		'''
		This Method Sets The Templates_Outliner_treeView View.
		'''

		LOGGER.debug("> Initializing '{0}' Widget!".format("Templates_Outliner_treeView"))

		self.ui.Templates_Outliner_treeView.setAutoScroll(False)
		self.ui.Templates_Outliner_treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.ui.Templates_Outliner_treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.Templates_Outliner_treeView.setIndentation(self._treeViewIndentation)
		self.ui.Templates_Outliner_treeView.setSortingEnabled(True)

		self.ui.Templates_Outliner_treeView.setModel(self._model)

		self.Templates_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def Templates_Outliner_treeView_refreshView(self):
		'''
		This Method Refreshes The Templates_Outliner_treeView View.
		'''

		self.Templates_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def Templates_Outliner_treeView_setDefaultViewState(self):
		'''
		This Method Sets Templates_Outliner_treeView Default View State.
		'''

		LOGGER.debug("> Setting '{0}' Default View State!".format("Templates_Outliner_treeView"))

		self.ui.Templates_Outliner_treeView.expandAll()
		for column in range(len(self._modelHeaders)):
			self.ui.Templates_Outliner_treeView.resizeColumnToContents(column)

		self.ui.Templates_Outliner_treeView.sortByColumn(0, Qt.AscendingOrder)

	@core.executionTrace
	def Templates_Outliner_treeView_storeModelSelection(self):
		'''
		This Method Stores Templates_Outliner_treeView Model Selection.
		'''

		LOGGER.debug("> Storing '{0}' Model Selection!".format("Templates_Outliner_treeView"))

		self._modelSelection = {"Collections":[], "Softwares":[], "Templates":[]}
		for item in self.getSelectedItems():
			if item._type == "Collection":
				self._modelSelection["Collections"].append(item.text())
			elif item._type == "Software":
				self._modelSelection["Softwares"].append(item.text())
			else:
				self._modelSelection["Templates"].append(item._datas.id)

	@core.executionTrace
	def Templates_Outliner_treeView_restoreModelSelection(self):
		'''
		This Method Restores Templates_Outliner_treeView Model Selection.
		'''

		LOGGER.debug("> Restoring '{0}' Model Selection!".format("Templates_Outliner_treeView"))

		indexes = []
		for i in range(self._model.rowCount()):
			collectionStandardItem = self._model.item(i)
			collectionStandardItem.text() in self._modelSelection["Collections"] and indexes.append(self._model.indexFromItem(collectionStandardItem))
			for j in range(collectionStandardItem.rowCount()):
				softwareStandardItem = collectionStandardItem.child(j, 0)
				softwareStandardItem.text() in self._modelSelection["Softwares"] and indexes.append(self._model.indexFromItem(softwareStandardItem))
				for k in range(softwareStandardItem.rowCount()):
					templateStandardItem = softwareStandardItem.child(k, 0)
					templateStandardItem._datas.id in self._modelSelection["Templates"] and indexes.append(self._model.indexFromItem(templateStandardItem))

		selectionModel = self.ui.Templates_Outliner_treeView.selectionModel()
		if selectionModel:
			selectionModel.reset()
			for index in indexes:
				selectionModel.setCurrentIndex(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

	@core.executionTrace
	def Templates_Outliner_treeView_setActions(self):
		'''
		This Method Sets The Templates_Outliner_treeView Actions.
		'''

		if not self._container.parameters.databaseReadOnly:
			addTemplateAction = QAction("Add Template ...", self.ui.Templates_Outliner_treeView)
			addTemplateAction.triggered.connect(self.Templates_Outliner_treeView_addTemplateAction)
			self.ui.Templates_Outliner_treeView.addAction(addTemplateAction)

			removeTemplatesAction = QAction("Remove Template(s) ...", self.ui.Templates_Outliner_treeView)
			removeTemplatesAction.triggered.connect(self.Templates_Outliner_treeView_removeTemplatesAction)
			self.ui.Templates_Outliner_treeView.addAction(removeTemplatesAction)

			separatorAction = QAction(self.ui.Templates_Outliner_treeView)
			separatorAction.setSeparator(True)
			self.ui.Templates_Outliner_treeView.addAction(separatorAction)

			importDefaultTemplatesAction = QAction("Import Default Templates", self.ui.Templates_Outliner_treeView)
			importDefaultTemplatesAction.triggered.connect(self.Templates_Outliner_treeView_importDefaultTemplatesAction)
			self.ui.Templates_Outliner_treeView.addAction(importDefaultTemplatesAction)

			filterTemplatesVersionsAction = QAction("Filter Templates Versions", self.ui.Templates_Outliner_treeView)
			filterTemplatesVersionsAction.triggered.connect(self.Templates_Outliner_treeView_filterTemplatesVersionsAction)
			self.ui.Templates_Outliner_treeView.addAction(filterTemplatesVersionsAction)

			separatorAction = QAction(self.ui.Templates_Outliner_treeView)
			separatorAction.setSeparator(True)
			self.ui.Templates_Outliner_treeView.addAction(separatorAction)
		else:
			LOGGER.info("{0} | Templates Database Alteration Capabilities Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		displayHelpFilesAction = QAction("Display Help File(s) ...", self.ui.Templates_Outliner_treeView)
		displayHelpFilesAction.triggered.connect(self.Templates_Outliner_treeView_displayHelpFilesAction)
		self.ui.Templates_Outliner_treeView.addAction(displayHelpFilesAction)

		separatorAction = QAction(self.ui.Templates_Outliner_treeView)
		separatorAction.setSeparator(True)
		self.ui.Templates_Outliner_treeView.addAction(separatorAction)


	@core.executionTrace
	def Templates_Outliner_treeView_addTemplateAction(self, checked):
		'''
		This Method Is Triggered By addTemplateAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		templatePath = self._container.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Add Template:", self._container.lastBrowsedPath, "Ibls Files (*.{0})".format(self._extension))))
		if templatePath:
			LOGGER.debug("> Chosen Template Path: '{0}'.".format(templatePath))
			self.addTemplate(strings.getSplitextBasename(templatePath), templatePath) and self.Templates_Outliner_treeView_refreshModel()

	@core.executionTrace
	def Templates_Outliner_treeView_removeTemplatesAction(self, checked):
		'''
		This Method Is Triggered By removeTemplatesAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		self.removeTemplates()
		self.Templates_Outliner_treeView_refreshModel()

	@core.executionTrace
	def Templates_Outliner_treeView_importDefaultTemplatesAction(self, checked):
		'''
		This Method Is Triggered By importDefaultTemplatesAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		for collection, path in self._defaultCollections.items():
			os.path.exists(path) and self.addDirectory(path, self.getCollection(collection).id, noWarning=True)
		self.Templates_Outliner_treeView_refreshModel()

	@core.executionTrace
	def Templates_Outliner_treeView_displayHelpFilesAction(self, checked):
		'''
		This Method Is Triggered By displayHelpFilesAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedTemplates = self.getSelectedTemplates()
		if selectedTemplates:
			for template in selectedTemplates:
				LOGGER.info("{0} | Opening '{1}' Template Help File: '{2}'.".format(self.__class__.__name__, template._datas.name, template._datas.helpFile))
				QDesktopServices.openUrl(QUrl.fromLocalFile(template._datas.helpFile))

	@core.executionTrace
	def Templates_Outliner_treeView_filterTemplatesVersionsAction(self, checked):
		'''
		This Method Is Triggered By filterTemplatesVersionsAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		templates = dbUtilities.common.getTemplates(self._coreDb.dbSession)
		needModelRefresh = False
		for template in templates:
			matchingTemplates = dbUtilities.common.filterTemplates(self._coreDb.dbSession, "^{0}$".format(template.name), "name")
			if len(matchingTemplates) != 1:
				needModelRefresh = True
				for id in sorted([(dbTemplate.id, dbTemplate.release) for dbTemplate in matchingTemplates], reverse=True, key=lambda x:(strings.getVersionRank(x[1])))[1:]:
					dbUtilities.common.removeTemplate(self._coreDb.dbSession, id[0])

		needModelRefresh and self.Templates_Outliner_treeView_refreshModel()

	@core.executionTrace
	def Templates_Outliner_treeView_OnSelectionChanged(self, selectedItems, deselectedItems):
		'''
		This Method Sets The Template_Informations_textEdit Widget.
		
		@param selectedItems: Selected Items. ( QItemSelection )
		@param deselectedItems: Deselected Items. ( QItemSelection )
		'''

		LOGGER.debug("> Initializing '{0}' Widget.".format("Template_Informations_textEdit"))

		content = []
		subContent = """
					<h4><center>{0}</center></h4>
					<p>
					<b>Date:</b> {1}
					<br/>
					<b>Author:</b> {2}
					<br/>
					<b>Email:</b> <a href="mailto:{3}"><span style=" text-decoration: underline; color:#000000;">{3}</span></a>
					<br/>
					<b>Url:</b> <a href="{4}"><span style=" text-decoration: underline; color:#000000;">{4}</span></a>
					<br/>
					<b>Output Script:</b> {5}
					<p>
					<b>Comment:</b> {6}
					</p>
					<p>
					<b>Help File:</b> <a href="{7}"><span style=" text-decoration: underline; color:#000000;">Template Manual</span></a>
					</p>
					</p>
					"""

		selectedTemplates = self.getSelectedTemplates()

		if selectedTemplates:
			for template in selectedTemplates:
				template and content.append(subContent.format("{0} {1} {2}".format(template._datas.software, template._datas.renderer, template._datas.title),
									template._datas.date,
									template._datas.author,
									template._datas.email,
									template._datas.url,
									template._datas.outputScript,
									template._datas.comment,
									QUrl.fromLocalFile(template._datas.helpFile).toString()
									))
		else:
			content.append(self._Template_Informations_textBrowser_defaultText)

		separator = len(content) == 1 and "" or "<p><center>* * *<center/></p>"

		self.ui.Template_Informations_textBrowser.setText(separator.join(content))

	@core.executionTrace
	def Template_Informations_textBrowser_OnAnchorClicked(self, url):
		'''
		This Method Is Triggered When A Link Is Clicked In The Template_Informations_textBrowser Widget.

		@param url: Url To Explore. ( QUrl )
		'''

		QDesktopServices.openUrl(url)

	@core.executionTrace
	def databaseChanged(self):
		'''
		This Method Is Triggered By The TemplatesOutliner_Worker When The Database Has Changed.
		'''

		# Ensure That DB Objects Modified By The Worker Thread Will Refresh Properly.
		self._coreDb.dbSession.expire_all()
		self.Templates_Outliner_treeView_refreshModel()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.DatabaseOperationError)
	def addTemplate(self, name, path, collectionId=None, noWarning=False):
		'''
		This Method Adds A Template To The Database.
		
		@param name: Template Set Name. ( String )		
		@param path: Template Set Path. ( String )		
		@param collectionId: Target Collection Id. ( Integer )		
		@param noWarning: No Warning Message. ( Boolean )
		@return: Template Database Addition Success. ( Boolean )		
		'''

		if not dbUtilities.common.filterTemplates(self._coreDb.dbSession, "^{0}$".format(re.escape(path)), "path"):
			LOGGER.info("{0} | Adding '{1}' Template To Database!".format(self.__class__.__name__, name))
			if dbUtilities.common.addTemplate(self._coreDb.dbSession, name, path, collectionId or self.getUniqueCollectionId(path)):
				return True
			else:
				raise foundations.exceptions.DatabaseOperationError, "{0} | Exception Raised While Adding '{1}' Template To Database!".format(self.__class__.__name__, name)
		else:
			noWarning or messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Template Path Already Exists In Database!".format(self.__class__.__name__, path))

	@core.executionTrace
	def addDirectory(self, directory, collectionId=None, noWarning=False):
		'''
		This Method Imports Provided Directory Templates Into Provided Collection.
		
		@param directory: Templates Directory. ( String )
		@param collectionId: Collection Id. ( Integer )
		@param noWarning: No Warning Message. ( Boolean )
		'''

		LOGGER.debug("> Initializing Directory '{0}' Walker.".format(directory))

		walker = Walker(directory)
		walker.walk(("\.{0}$".format(self._extension),), ("\._",))
		for template, path in walker.files.items():
			self.addTemplate(namespace.getNamespace(template, rootOnly=True), path, collectionId, noWarning)

	@core.executionTrace
	def removeTemplates(self):
		'''
		This Method Removes Templates From The Database.
		'''

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
				selectedTemplates.append(item)

		selectedCollections and messageBox.messageBox("Warning", "Warning", "{0} | Cannot Remove '{1}' Collection(s)!".format(self.__class__.__name__, ", ".join(selectedCollections)))
		selectedSoftwares and messageBox.messageBox("Warning", "Warning", "{0} | Cannot Remove '{1}' Software(s)!".format(self.__class__.__name__, ", ".join(selectedSoftwares)))

		if selectedTemplates:
			if messageBox.messageBox("Question", "Question", "Are You Sure You Want To Remove '{0}' Template(s)?".format(", ".join([str(template.text()) for template in selectedTemplates])), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
				for template in selectedTemplates:
					LOGGER.info("{0} | Removing '{1}' Template From Database!".format(self.__class__.__name__, template.text()))
					dbUtilities.common.removeTemplate(self._coreDb.dbSession, str(template._datas.id))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.DatabaseOperationError)
	def updateTemplateLocation(self, template):
		'''
		This Method Updates A Template Location.
		
		@param template: Template To Update. ( DbTemplate )
		@return: Update Success. ( Boolean )
		'''

		templatePath = self._container.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Updating '{0}' Template Location:".format(template.name), self._container.lastBrowsedPath, "Template Files (*{0})".format(self._extension))))
		if templatePath:
			LOGGER.info("{0} | Updating '{1}' Template With New Location '{2}'!".format(self.__class__.__name__, template.name, file))
			if not dbUtilities.common.updateTemplateLocation(self._coreDb.dbSession, template, templatePath):
				raise foundations.exceptions.DatabaseOperationError, "{0} | Exception Raised While Updating '{1}' Template!".format(self.__class__.__name__, template.name)
			else:
				return True

	@core.executionTrace
	def addDefaultTemplates(self):
		'''
		This Method Adds Default Templates Collections / Templates To The Database.
		'''

		LOGGER.debug("> Adding Default Templates To Database.")

		if not dbUtilities.common.getTemplates(self._coreDb.dbSession).count():
			needModelRefresh = False
			for collection, path in self._defaultCollections.items():
				if os.path.exists(path):
					if not set(dbUtilities.common.filterCollections(self._coreDb.dbSession, "^{0}$".format(collection), "name")).intersection(dbUtilities.common.filterCollections(self._coreDb.dbSession, "Templates", "type")):
						LOGGER.info("{0} | Adding '{1}' Collection To Database!".format(self.__class__.__name__, collection))
						dbUtilities.common.addCollection(self._coreDb.dbSession, collection, "Templates", "Template {0} Collection".format(collection))
					needModelRefresh = True
					self.addDirectory(path, self.getCollection(collection).id)

			needModelRefresh and self.Templates_Outliner_treeView_refreshModel()

	@core.executionTrace
	def getCollection(self, collection):
		'''
		This Method Gets Template Collection From Provided Collection Name.
		
		@param collection: Collection Name. ( String )
		@return: Collection. ( dbCollection )
		'''

		return [collection for collection in set(dbUtilities.common.filterCollections(self._coreDb.dbSession, "^{0}$".format(collection), "name")).intersection(dbUtilities.common.filterCollections(self._coreDb.dbSession, "Templates", "type"))][0]

	@core.executionTrace
	def getUniqueCollectionId(self, path):
		'''
		This Method Gets A Unique Collection Id Using Provided Path.
		
		@param path: Template Path. ( String )
		@return: Collection. ( Integer )
		'''

		templatesCollections = dbUtilities.common.filterCollections(self._coreDb.dbSession, "Templates", "type")
		return self.defaultCollections[self._factoryCollection] in path and [collection for collection in set(dbUtilities.common.filterCollections(self._coreDb.dbSession, "^{0}$".format(self._factoryCollection), "name")).intersection(templatesCollections)][0].id or [collection for collection in set(dbUtilities.common.filterCollections(self._coreDb.dbSession, "^{0}$".format(self._userCollection), "name")).intersection(templatesCollections)][0].id

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		'''
		This Method Returns The Templates_Outliner_treeView Selected Items.
		
		@param rowsRootOnly: Return Rows Roots Only. ( Boolean )
		@return: View Selected Items. ( List )
		'''

		selectedIndexes = self.ui.Templates_Outliner_treeView.selectedIndexes()

		return rowsRootOnly and [item for item in set([self._model.itemFromIndex(self._model.sibling(index.row(), 0, index)) for index in selectedIndexes])] or [self._model.itemFromIndex(index) for index in selectedIndexes]

	@core.executionTrace
	def getSelectedTemplates(self):
		'''
		This Method Returns The Selected Templates.
		
		@return: Selected Template. ( QTreeWidgetItem )
		'''

		selectedItems = self.getSelectedItems()
		return selectedItems and [item for item in selectedItems if item._type == "Template"] or None

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
