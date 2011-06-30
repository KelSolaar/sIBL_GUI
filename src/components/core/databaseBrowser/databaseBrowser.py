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
************************************************************************************************
***	databaseBrowser.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Database Browser Component Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import functools
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
from foundations.walker import Walker
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class DatabaseBrowser_Worker(QThread):
	"""
	This Class Is The DatabaseBrowser_Worker Class.
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

		self.__timer.timeout.connect(self.__updateSets, Qt.DirectConnection)

		self.exec_()

	@core.executionTrace
	def __updateSets(self):
		"""
		This Method Updates Database Sets If They Have Been Modified On Disk.
		"""

		needModelRefresh = False
		for iblSet in dbUtilities.common.getIblSets(self.__dbSession):
			if iblSet.path:
				if os.path.exists(iblSet.path):
					storedStats = iblSet.osStats.split(",")
					osStats = os.stat(iblSet.path)
					if str(osStats[8]) != str(storedStats[8]):
						LOGGER.info("{0} | '{1}' Ibl Set File Has Been Modified And Will Be Updated!".format(self.__class__.__name__, iblSet.name))
						if dbUtilities.common.updateIblSetContent(self.__dbSession, iblSet):
							LOGGER.info("{0} | '{1}' Ibl Set Has Been Updated!".format(self.__class__.__name__, iblSet.name))
							needModelRefresh = True

		needModelRefresh and self.emit(SIGNAL("databaseChanged()"))

class DatabaseBrowser_QListView(QListView):
	"""
	This Class Is The DatabaseBrowser_QListView Class.
	"""

	@core.executionTrace
	def __init__(self, container):
		"""
		This Method Initializes The Class.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		QListView.__init__(self, container)

		self.setAcceptDrops(True)


		# --- Setting Class Attributes. ---
		self.__container = container

		self.__coreDatabaseBrowser = self.__container.componentsManager.components["core.databaseBrowser"].interface

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
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreDatabaseBrowser"))
	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def dragEnterEvent(self, event):
		"""
		This Method Defines The Drag Enter Event Behavior.
		
		@param event: QEvent. ( QEvent )
		"""

		if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
			LOGGER.debug("> '{0}' Drag Event Type Accepted!".format("application/x-qabstractitemmodeldatalist"))
			event.accept()
		elif event.mimeData().hasFormat("text/uri-list"):
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
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, OSError, foundations.exceptions.UserError)
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
					if re.search("\.{0}$".format(self.__coreDatabaseBrowser.extension), str(url.path())):
						name = strings.getSplitextBasename(path)
						if messageBox.messageBox("Question", "Question", "'{0}' Ibl Set File Has Been Dropped, Would You Like To Add It To The Database?".format(name), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
							self.__coreDatabaseBrowser.addIblSet(name, path)
					else:
						if os.path.isdir(path):
							if messageBox.messageBox("Question", "Question", "'{0}' Directory Has Been Dropped, Would You Like To Add Its Content To The Database?".format(path), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
								self.__coreDatabaseBrowser.addDirectory(path)
						else:
							raise OSError, "{0} | Exception Raised While Parsing '{1}' Path: Syntax Is Invalid!".format(self.__class__.__name__, path)
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __QListView__doubleClicked(self, index):
		"""
		This Method Defines The Behavior When A QStandardItem Is Double Clicked.
		
		@param index: Clicked Model Item Index. ( QModelIndex )
		"""

		if not self.__container.parameters.databaseReadOnly:
			pass
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot Perform Action, Database Has Been Set Read Only!".format(self.__class__.__name__)

class DatabaseBrowser(UiComponent):
	"""
	This Class Is The DatabaseBrowser Class.
	"""

	# Custom Signals Definitions.
	modelDatasRefresh = pyqtSignal()
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

		self.__uiPath = "ui/Database_Browser.ui"
		self.__uiResources = "resources"
		self.__uiLargestSizeImage = "Largest_Size.png"
		self.__uiSmallestSizeImage = "Smallest_Size.png"
		self.__dockArea = 8
		self.__listViewSpacing = 24
		self.__listViewMargin = 32
		self.__listViewIconSize = 128

		self.__container = None
		self.__settings = None
		self.__settingsSection = None
		self.__settingsSeparator = ","

		self.__extension = "ibl"

		self.__coreDb = None
		self.__coreCollectionsOutliner = None

		self.__model = None
		self.__modelSelection = None

		self.__databaseBrowserWorkerThread = None

		self.__modelContent = None

		self.__toolTipText = """
								<p><b>{0}</b></p>
								<p><b>Author: </b>{1}<br>
								<b>Location: </b>{2}<br>
								<b>Shot Date: </b>{3}<br>
								<b>Comment: </b>{4}</p>
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
	def uiLargestSizeImage(self):
		"""
		This Method Is The Property For The _uiLargestSizeImage Attribute.

		@return: self.__uiLargestSizeImage. ( String )
		"""

		return self.__uiLargestSizeImage

	@uiLargestSizeImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLargestSizeImage(self, value):
		"""
		This Method Is The Setter Method For The _uiLargestSizeImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiLargestSizeImage"))

	@uiLargestSizeImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLargestSizeImage(self):
		"""
		This Method Is The Deleter Method For The _uiLargestSizeImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiLargestSizeImage"))

	@property
	def uiSmallestSizeImage(self):
		"""
		This Method Is The Property For The _uiSmallestSizeImage Attribute.

		@return: self.__uiSmallestSizeImage. ( String )
		"""

		return self.__uiSmallestSizeImage

	@uiSmallestSizeImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSmallestSizeImage(self, value):
		"""
		This Method Is The Setter Method For The _uiSmallestSizeImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiSmallestSizeImage"))

	@uiSmallestSizeImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSmallestSizeImage(self):
		"""
		This Method Is The Deleter Method For The _uiSmallestSizeImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiSmallestSizeImage"))

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
	def listViewSpacing(self):
		"""
		This Method Is The Property For The _listViewSpacing Attribute.

		@return: self.__listViewSpacing. ( Integer )
		"""

		return self.__listViewSpacing

	@listViewSpacing.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def listViewSpacing(self, value):
		"""
		This Method Is The Setter Method For The _listViewSpacing Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' Attribute: '{1}' Type Is Not 'int'!".format("listViewSpacing", value)
			assert value > 0, "'{0}' Attribute: '{1}' Need To Be Exactly Positive!".format("listViewSpacing", value)
		self.__listViewSpacing = value

	@listViewSpacing.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def listViewSpacing(self):
		"""
		This Method Is The Deleter Method For The _listViewSpacing Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("listViewSpacing"))

	@property
	def listViewMargin(self):
		"""
		This Method Is The Property For The _listViewMargin Attribute.

		@return: self.__listViewMargin. ( Integer )
		"""

		return self.__listViewMargin

	@listViewMargin.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def listViewMargin(self, value):
		"""
		This Method Is The Setter Method For The _listViewMargin Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' Attribute: '{1}' Type Is Not 'int'!".format("listViewMargin", value)
			assert value > 0, "'{0}' Attribute: '{1}' Need To Be Exactly Positive!".format("listViewMargin", value)
		self.__listViewMargin = value

	@listViewMargin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def listViewMargin(self):
		"""
		This Method Is The Deleter Method For The _listViewMargin Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("listViewMargin"))

	@property
	def listViewIconSize(self):
		"""
		This Method Is The Property For The _listViewIconSize Attribute.

		@return: self.__listViewIconSize. ( Integer )
		"""

		return self.__listViewIconSize

	@listViewIconSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def listViewIconSize(self, value):
		"""
		This Method Is The Setter Method For The _listViewIconSize Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' Attribute: '{1}' Type Is Not 'int'!".format("listViewIconSize", value)
			assert value > 0, "'{0}' Attribute: '{1}' Need To Be Exactly Positive!".format("listViewIconSize", value)
		self.__listViewIconSize = value

	@listViewIconSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def listViewIconSize(self):
		"""
		This Method Is The Deleter Method For The _listViewIconSize Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("listViewIconSize"))

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
	def coreCollectionsOutliner(self):
		"""
		This Method Is The Property For The _coreCollectionsOutliner Attribute.

		@return: self.__coreCollectionsOutliner. ( Object )
		"""

		return self.__coreCollectionsOutliner

	@coreCollectionsOutliner.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self, value):
		"""
		This Method Is The Setter Method For The _coreCollectionsOutliner Attribute.

		@param value: Attribute Value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("coreCollectionsOutliner"))

	@coreCollectionsOutliner.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreCollectionsOutliner(self):
		"""
		This Method Is The Deleter Method For The _coreCollectionsOutliner Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("coreCollectionsOutliner"))


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
	def databaseBrowserWorkerThread(self):
		"""
		This Method Is The Property For The _databaseBrowserWorkerThread Attribute.

		@return: self.__databaseBrowserWorkerThread. ( QThread )
		"""

		return self.__databaseBrowserWorkerThread

	@databaseBrowserWorkerThread.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseBrowserWorkerThread(self, value):
		"""
		This Method Is The Setter Method For The _databaseBrowserWorkerThread Attribute.

		@param value: Attribute Value. ( QThread )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("databaseBrowserWorkerThread"))

	@databaseBrowserWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseBrowserWorkerThread(self):
		"""
		This Method Is The Deleter Method For The _databaseBrowserWorkerThread Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("databaseBrowserWorkerThread"))

	@property
	def modelContent(self):
		"""
		This Method Is The Property For The _modelContent Attribute.

		@return: self.__modelContent. ( List )
		"""

		return self.__modelContent

	@modelContent.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def modelContent(self, value):
		"""
		This Method Is The Setter Method For The _modelContent Attribute.

		@param value: Attribute Value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' Attribute: '{1}' Type Is Not 'list'!".format("content", value)
		self.__modelContent = value

	@modelContent.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelContent(self):
		"""
		This Method Is The Deleter Method For The _modelContent Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("modelContent"))

	@property
	def toolTipText(self):
		"""
		This Method Is The Property For The _toolTipText Attribute.

		@return: self.__toolTipText. ( String )
		"""

		return self.__toolTipText

	@toolTipText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolTipText(self, value):
		"""
		This Method Is The Setter Method For The _toolTipText Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("toolTipText"))

	@toolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolTipText(self):
		"""
		This Method Is The Deleter Method For The _toolTipText Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("toolTipText"))

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
		self.__coreCollectionsOutliner = self.__container.componentsManager.components["core.collectionsOutliner"].interface

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

		self.ui.Database_Browser_listView = DatabaseBrowser_QListView(self.__container)
		self.ui.Database_Browser_Widget_gridLayout.addWidget(self.ui.Database_Browser_listView, 0, 0)

		self.__modelContent = dbUtilities.common.getIblSets(self.__coreDb.dbSession)

		listViewIconSize = self.__settings.getKey(self.__settingsSection, "listViewIconSize")
		self.__listViewIconSize = listViewIconSize.toInt()[1] and listViewIconSize.toInt()[0] or self.__listViewIconSize

		self.__container.parameters.databaseReadOnly and LOGGER.info("{0} | Database_Browser_listView Model Edition Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))
		self.__model = QStandardItemModel()
		self.__Database_Browser_listView_setModel()

		self.ui.Database_Browser_listView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Database_Browser_listView_addActions()

		self.__Database_Browser_listView_setView()

		if not self.__container.parameters.databaseReadOnly:
			if not self.__container.parameters.deactivateWorkerThreads:
				self.__databaseBrowserWorkerThread = DatabaseBrowser_Worker(self)
				self.__databaseBrowserWorkerThread.start()
				self.__container.workerThreads.append(self.__databaseBrowserWorkerThread)
			else:
				LOGGER.info("{0} | Ibl Sets Continuous Scanner Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Ibl Sets Continuous Scanner Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		self.ui.Thumbnails_Size_horizontalSlider.setValue(self.__listViewIconSize)
		self.ui.Largest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResources, self.__uiLargestSizeImage)))
		self.ui.Smallest_Size_label.setPixmap(QPixmap(os.path.join(self.__uiResources, self.__uiSmallestSizeImage)))

		# Signals / Slots.
		self.ui.Thumbnails_Size_horizontalSlider.valueChanged.connect(self.__Thumbnails_Size_horizontalSlider__changed)
		self.ui.Database_Browser_listView.doubleClicked.connect(self.ui.Database_Browser_listView._DatabaseBrowser_QListView__QListView__doubleClicked)
		self.modelDatasRefresh.connect(self.__Database_Browser_listView_setModelContent)
		self.modelChanged.connect(self.__Database_Browser_listView_refreshView)
		self.modelChanged.connect(functools.partial(self.__coreCollectionsOutliner.emit, SIGNAL("modelPartialRefresh()")))
		self.modelRefresh.connect(self.__Database_Browser_listView_refreshModel)

		if not self.__container.parameters.databaseReadOnly:
			if not self.__container.parameters.deactivateWorkerThreads:
				self.__databaseBrowserWorkerThread.databaseChanged.connect(self.__coreDb_database__changed)
			self.__model.dataChanged.connect(self.__Database_Browser_listView_model__dataChanged)

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

		self.__container.centralwidget_gridLayout.addWidget(self.ui)

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
			# Wizard If Sets Table Is Empty.
			if not dbUtilities.common.getIblSets(self.__coreDb.dbSession).count():
				if messageBox.messageBox("Question", "Question", "The Database Is Empty, Would You Like To Add Some Sets?", buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
					directory = self.__container.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self, "Add Content:", self.__container.lastBrowsedPath)))
					if directory:
						self.addDirectory(directory)

			# Ibl Sets Table Integrity Checking.
			erroneousIblSets = dbUtilities.common.checkIblSetsTableIntegrity(self.__coreDb.dbSession)
			if erroneousIblSets:
				for iblSet in erroneousIblSets:
					if erroneousIblSets[iblSet] == "INEXISTING_IBL_SET_FILE_EXCEPTION":
						if messageBox.messageBox("Question", "Error", "{0} | '{1}' Ibl Set File Is Missing, Would You Like To Update It's Location?".format(self.__class__.__name__, iblSet.name), QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No) == 16384:
							self.updateIblSetLocation(iblSet)
					else:
						messageBox.messageBox("Warning", "Warning", "{0} | '{1}' {2}".format(self.__class__.__name__, iblSet.name, dbUtilities.common.DB_EXCEPTIONS[erroneousIblSets[iblSet]]))
		else:
			LOGGER.info("{0} | Database Ibl Sets Wizard And Ibl Sets Integrity Checking Method Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeIblSetsIds = str(self.__settings.getKey(self.__settingsSection, "activeIblSets").toString())
		LOGGER.debug("> Stored '{0}' Active Ibl Sets Ids Selection: '{1}'.".format(self.__class__.__name__, activeIblSetsIds))
		if activeIblSetsIds:
			if self.__settingsSeparator in activeIblSetsIds:
				ids = activeIblSetsIds.split(self.__settingsSeparator)
			else:
				ids = [activeIblSetsIds]
			self.__modelSelection = [int(id) for id in ids]

		self.__Database_Browser_listView_restoreModelSelection()

	@core.executionTrace
	def onClose(self):
		"""
		This Method Is Called On Framework Close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework Close Method.".format(self.__class__.__name__))

		self.__Database_Browser_listView_storeModelSelection()
		self.__settings.setKey(self.__settingsSection, "activeIblSets", self.__settingsSeparator.join(str(id) for id in self.__modelSelection))

	@core.executionTrace
	def __Database_Browser_listView_setModelContent(self):
		"""
		This Method Sets Database_Browser_listView Model Content.
		"""

		self.__modelContent = self.__coreCollectionsOutliner.getSelectedCollectionsIblSets()

	@core.executionTrace
	def __Database_Browser_listView_setModel(self):
		"""
		This Method Sets The Database_Browser_listView Model.
		"""

		LOGGER.debug("> Setting Up '{0}' Model!".format("Database_Browser_listView"))

		self.__Database_Browser_listView_storeModelSelection()

		self.__model.clear()

		for iblSet in [iblSet[0] for iblSet in sorted(((displaySet, displaySet.title) for displaySet in self.__modelContent), key=lambda x:(x[1]))]:
			LOGGER.debug("> Preparing '{0}' Ibl Set For '{1}' Model.".format(iblSet.name, "Database_Browser_listView"))

			try:
				iblSetStandardItem = QStandardItem()
				iblSetStandardItem.setData(iblSet.title, Qt.DisplayRole)
				iblSetStandardItem.setToolTip(self.__toolTipText.format(iblSet.title, iblSet.author or Constants.nullObject, iblSet.location or Constants.nullObject, self.getFormatedShotDate(iblSet.date, iblSet.time) or Constants.nullObject, iblSet.comment or Constants.nullObject))

				iblSetStandardItem.setIcon(ui.common.getIcon(iblSet.icon))

				self.__container.parameters.databaseReadOnly and iblSetStandardItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsDragEnabled)

				iblSetStandardItem._datas = iblSet

				LOGGER.debug("> Adding '{0}' To '{1}' Model.".format(iblSet.name, "Database_Browser_listView"))
				self.__model.appendRow(iblSetStandardItem)

			except Exception as error:
				LOGGER.error("!>{0} | Exception Raised While Adding '{1}' Ibl Set To '{2}' Model!".format(self.__class__.__name__, iblSet.name, "Database_Browser_listView"))
				foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "__Database_Browser_listView_setModel"))

		self.__Database_Browser_listView_restoreModelSelection()

		self.emit(SIGNAL("modelChanged()"))

	@core.executionTrace
	def __Database_Browser_listView_refreshModel(self):
		"""
		This Method Refreshes The Database_Browser_listView Model.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Database_Browser_listView"))

		self.__Database_Browser_listView_setModel()

	@core.executionTrace
	def __Database_Browser_listView_setView(self):
		"""
		This Method Sets The Database_Browser_listView Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Widget!".format("Database_Browser_listView"))

		self.ui.Database_Browser_listView.setAutoScroll(True)
		self.ui.Database_Browser_listView.setResizeMode(QListView.Adjust)
		self.ui.Database_Browser_listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.Database_Browser_listView.setViewMode(QListView.IconMode)

		self.__Database_Browser_listView_setDefaultViewState()

		self.ui.Database_Browser_listView.setModel(self.__model)

	@core.executionTrace
	def __Database_Browser_listView_setDefaultViewState(self):
		"""
		This Method Scales The Database_Browser_listView Item Size.
		"""

		LOGGER.debug("> Setting '{0}' View Item Size To: {1}.".format("Database_Browser_listView", self.__listViewIconSize))

		self.ui.Database_Browser_listView.setIconSize(QSize(self.__listViewIconSize, self.__listViewIconSize))
		self.ui.Database_Browser_listView.setGridSize(QSize(self.__listViewIconSize + self.__listViewSpacing, self.__listViewIconSize + self.__listViewMargin))

	@core.executionTrace
	def __Database_Browser_listView_refreshView(self):
		"""
		This Method Refreshes The Database_Browser_listView View.
		"""

		self.__Database_Browser_listView_setDefaultViewState()

	@core.executionTrace
	def __Database_Browser_listView_storeModelSelection(self):
			"""
			This Method Stores Database_Browser_listView Model Selection.
			"""

			# Crash Preventing Code.
			# if self.__modelSelectionState:

			LOGGER.debug("> Storing '{0}' Model Selection!".format("Database_Browser_listView"))

			self.__modelSelection = []
			for item in self.getSelectedItems():
				self.__modelSelection.append(item._datas.id)

	@core.executionTrace
	def __Database_Browser_listView_restoreModelSelection(self):
			"""
			This Method Restores Database_Browser_listView Model Selection.
			"""

			# Crash Preventing Code.
			# if self.__modelSelectionState:

			LOGGER.debug("> Restoring '{0}' Model Selection!".format("Database_Browser_listView"))

			indexes = []
			for i in range(self.__model.rowCount()):
				iblSetStandardItem = self.__model.item(i)
				iblSetStandardItem._datas.id in self.__modelSelection and indexes.append(self.__model.indexFromItem(iblSetStandardItem))

			selectionModel = self.ui.Database_Browser_listView.selectionModel()
			if selectionModel:
				selectionModel.clear()
				for index in indexes:
					selectionModel.setCurrentIndex(index, QItemSelectionModel.Select)

	@core.executionTrace
	def __Database_Browser_listView_addActions(self):
		"""
		This Method Sets The Database Browser Actions.
		"""

		if not self.__container.parameters.databaseReadOnly:
			addContentAction = QAction("Add Content ...", self.ui.Database_Browser_listView)
			addContentAction.triggered.connect(self.__Database_Browser_listView_addContentAction__triggered)
			self.ui.Database_Browser_listView.addAction(addContentAction)

			addIblSetAction = QAction("Add Ibl Set ...", self.ui.Database_Browser_listView)
			addIblSetAction.triggered.connect(self.__Database_Browser_listView_addIblSetAction__triggered)
			self.ui.Database_Browser_listView.addAction(addIblSetAction)

			removeIblSetsAction = QAction("Remove Ibl Set(s) ...", self.ui.Database_Browser_listView)
			removeIblSetsAction.triggered.connect(self.__Database_Browser_listView_removeIblSetsAction__triggered)
			self.ui.Database_Browser_listView.addAction(removeIblSetsAction)

			updateIblSetsLocationsAction = QAction("Update Ibl Set(s) Location(s) ...", self.ui.Database_Browser_listView)
			updateIblSetsLocationsAction.triggered.connect(self.__Database_Browser_listView_updateIblSetsLocationsAction__triggered)
			self.ui.Database_Browser_listView.addAction(updateIblSetsLocationsAction)

			separatorAction = QAction(self.ui.Database_Browser_listView)
			separatorAction.setSeparator(True)
			self.ui.Database_Browser_listView.addAction(separatorAction)
		else:
			LOGGER.info("{0} | Ibl Sets Database Alteration Capabilities Deactivated By '{1}' Command Line Parameter Value!".format(self.__class__.__name__, "databaseReadOnly"))

	@core.executionTrace
	def __Database_Browser_listView_addContentAction__triggered(self, checked):
		"""
		This Method Is Triggered By addContentAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.addUserContent()

	@core.executionTrace
	def __Database_Browser_listView_addIblSetAction__triggered(self, checked):
		"""
		This Method Is Triggered By addIblSetAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.addUserIblSet()

	@core.executionTrace
	def __Database_Browser_listView_removeIblSetsAction__triggered(self, checked):
		"""
		This Method Is Triggered By removeIblSetsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.removeUserIblSets()

	@core.executionTrace
	def __Database_Browser_listView_updateIblSetsLocationsAction__triggered(self, checked):
		"""
		This Method Is Triggered By updateIblSetsLocationsAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""

		self.updateUserIblSetsLocation()

	@core.executionTrace
	def __Database_Browser_listView_model__dataChanged(self, startIndex, endIndex):
		"""
		This Method Defines The Behavior When The Database_Browser_listView Model Data Changes.
		
		@param startIndex: Edited Item Starting QModelIndex. ( QModelIndex )
		@param endIndex: Edited Item Ending QModelIndex. ( QModelIndex )
		"""

		standardItem = self.__model.itemFromIndex(startIndex)
		currentTitle = standardItem.text()

		LOGGER.debug("> Updating Ibl Set '{0}' Title To '{1}'.".format(standardItem._datas.title, currentTitle))
		iblSet = dbUtilities.common.filterIblSets(self.__coreDb.dbSession, "^{0}$".format(standardItem._datas.id), "id")[0]
		iblSet.title = str(currentTitle)
		dbUtilities.common.commit(self.__coreDb.dbSession)

		self.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	def __Thumbnails_Size_horizontalSlider__changed(self, value):
		"""
		This Method Scales The Database_Browser_listView Icons.
		
		@param value: Thumbnails Size. ( Integer )
		"""

		self.__listViewIconSize = value

		self.__Database_Browser_listView_setDefaultViewState()

		# Storing Settings Key.
		LOGGER.debug("> Setting '{0}' With Value '{1}'.".format("listViewIconSize", value))
		self.__settings.setKey(self.__settingsSection, "listViewIconSize", value)

	@core.executionTrace
	def __coreDb_database__changed(self):
		"""
		This Method Is Triggered By The DatabaseBrowser_Worker When The Database Has Changed.
		"""

		# Ensure That DB Objects Modified By The Worker Thread Will Refresh Properly.
		self.__coreDb.dbSession.expire_all()
		self.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	def getSelectedItems(self):
		"""
		This Method Returns The Database_Browser_listView Selected Items.
		
		@return: View Selected Items. ( List )
		"""

		return [self.__model.itemFromIndex(index) for index in self.ui.Database_Browser_listView.selectedIndexes()]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getFormatedShotDate(self, date, time):
		"""
		This Method Returns A Formated Shot Date.

		@param date: sIBL Set Date Key Value. ( String )
		@param time: sIBL Set Time Key Value. ( String )
		@return: Current Shot Date. ( String )
		"""

		LOGGER.debug("> Formatting Shot Date With '{0}' Date and '{1}' Time.".format(date, time))

		if date and time and date != Constants.nullObject and time != Constants.nullObject:
			shotTime = time.split(":")
			shotTime = shotTime[0] + "H" + shotTime[1]
			shotDate = date.replace(":", "/")[2:] + " - " + shotTime

			LOGGER.debug("> Formatted Shot Date: '{0}'.".format(shotDate))
			return shotDate
		else:
			return Constants.nullObject

	@core.executionTrace
	def addUserContent(self):
		"""
		This Method Adds User Content To The Database.
		"""

		directory = self.__container.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self, "Add Content:", self.__container.lastBrowsedPath)))
		if directory:
			LOGGER.debug("> Chosen Directory Path: '{0}'.".format(directory))
			self.addDirectory(directory)

	@core.executionTrace
	def addUserIblSet(self):
		"""
		This Method Adds User Ibl Set To The Database.
		"""
		iblSetPath = self.__container.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Add Ibl Set:", self.__container.lastBrowsedPath, "Ibls Files (*{0})".format(self.__extension))))
		if iblSetPath:
			LOGGER.debug("> Chosen Ibl Set Path: '{0}'.".format(iblSetPath))
			self.addIblSet(strings.getSplitextBasename(iblSetPath), iblSetPath)

	@core.executionTrace
	def removeUserIblSets(self):
		"""
		This Method Remove User Ibl Sets From The Database.
		"""

		selectedIblSets = [iblSet._datas for iblSet in self.getSelectedItems()]
		if selectedIblSets:
			if messageBox.messageBox("Question", "Question", "Are You Sure You Want To Remove '{0}' Sets(s)?".format(", ".join((str(iblSet.name) for iblSet in selectedIblSets))), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
				self.removeIblSets(selectedIblSets)

	@core.executionTrace
	def updateUserIblSetsLocation(self):
		"""
		This Method Updates User Ibl Sets Location.
		"""

		selectedIblSets = self.getSelectedItems()
		if selectedIblSets:
			for iblSet in selectedIblSets:
				file = self.__container.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Updating '{0}' Ibl Set Location:".format(iblSet._datas.name), self.__container.lastBrowsedPath, "Ibls Files (*.{0})".format(self.__extension))))
				self.updateIblSetLocation(iblSet._datas, file)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.DatabaseOperationError)
	def addIblSet(self, name, path, collectionId=None, noWarning=False):
		"""
		This Method Adds An Ibl Set To The Database.
		
		@param name: Ibl Set Name. ( String )		
		@param path: Ibl Set Path. ( String )		
		@param collectionId: Target Collection Id. ( Integer )		
		@param noWarning: No Warning Message. ( Boolean )
		"""

		if not dbUtilities.common.filterIblSets(self.__coreDb.dbSession, "^{0}$".format(re.escape(path)), "path"):
			LOGGER.info("{0} | Adding '{1}' Ibl Set To Database!".format(self.__class__.__name__, name))
			if dbUtilities.common.addIblSet(self.__coreDb.dbSession, name, path, collectionId or self.__coreCollectionsOutliner.getUniqueCollectionId()):
				self.emit(SIGNAL("modelDatasRefresh()"))
				self.emit(SIGNAL("modelRefresh()"))
			else:
				raise foundations.exceptions.DatabaseOperationError, "{0} | Exception Raised While Adding '{1}' Ibl Set To Database!".format(self.__class__.__name__, name)
		else:
			noWarning or messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Ibl Set Path Already Exists In Database!".format(self.__class__.__name__, name))

	@core.executionTrace
	def addDirectory(self, directory, collectionId=None, noWarning=False):
		"""
		This Method Adds A Sets Directory Content To The Database.
		
		@param directory: Directory To Add. ( String )		
		@param collectionId: Target Collection Id. ( Integer )		
		@param noWarning: No Warning Message. ( Boolean )
		"""

		LOGGER.debug("> Initializing Directory '{0}' Walker.".format(directory))

		walker = Walker(directory)
		walker.walk(("\.{0}$".format(self.__extension),), ("\._",))
		for iblSet, path in walker.files.items():
			self.addIblSet(namespace.getNamespace(iblSet, rootOnly=True), path, collectionId or self.__coreCollectionsOutliner.getUniqueCollectionId())
		self.emit(SIGNAL("modelDatasRefresh()"))
		self.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	def removeIblSets(self, iblSets):
		"""
		This Method Remove Ibl Sets From The Database.
		
		@param iblSets: Ibl Sets To Remove ( DbIblSet List )
		"""

		for iblSet in iblSets:
			LOGGER.info("{0} | Removing '{1}' Ibl Set From Database!".format(self.__class__.__name__, iblSet.name))
			dbUtilities.common.removeIblSet(self.__coreDb.dbSession, iblSet.id)
		self.emit(SIGNAL("modelDatasRefresh()"))
		self.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(ui.common.uiBasicExceptionHandler, False, foundations.exceptions.DatabaseOperationError)
	def updateIblSetLocation(self, iblSet, file):
		"""
		This Method Updates An Ibl Set Location.
		
		@param iblSet: Ibl Set To Update. ( DbIblSet )
		@param iblSet: New Ibl Set File. ( String )
		"""

		LOGGER.info("{0} | Updating '{1}' Ibl Set With New Location: '{2}'!".format(self.__class__.__name__, iblSet.name, file))
		if not dbUtilities.common.updateIblSetLocation(self.__coreDb.dbSession, iblSet, file):
			raise foundations.exceptions.DatabaseOperationError, "{0} | Exception Raised While Updating '{1}' Ibl Set!".format(self.__class__.__name__, iblSet.name)
		else:
			self.emit(SIGNAL("modelDatasRefresh()"))
			self.emit(SIGNAL("modelRefresh()"))

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
