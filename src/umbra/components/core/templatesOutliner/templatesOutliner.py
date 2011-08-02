#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**componentsManagerUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Templates Outliner Component Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import platform
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
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
class TemplatesOutliner_Worker(QThread):
	"""
	This class is the **TemplatesOutliner_Worker** class.
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

		QThread.__init__(self, container)

		# --- Setting class attributes. ---
		self.__container = container

		self.__dbSession = self.__container.coreDb.dbSessionMaker()

		self.__timer = None
		self.__timerCycleMultiplier = 5

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
	def timer(self):
		"""
		This method is the property for **self.__timer** attribute.

		:return: self.__timer. ( QTimer )
		"""

		return self.__timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		This method is the setter method for **self.__timer** attribute.

		:param value: Attribute value. ( QTimer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("timer"))

	@timer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		This method is the deleter method for **self.__timer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("timer"))

	@property
	def timerCycleMultiplier(self):
		"""
		This method is the property for **self.__timerCycleMultiplier** attribute.

		:return: self.__timerCycleMultiplier. ( Float )
		"""

		return self.__timerCycleMultiplier

	@timerCycleMultiplier.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self, value):
		"""
		This method is the setter method for **self.__timerCycleMultiplier** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("timerCycleMultiplier"))

	@timerCycleMultiplier.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self):
		"""
		This method is the deleter method for **self.__timerCycleMultiplier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("timerCycleMultiplier"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def run(self):
		"""
		This method starts the QThread.
		"""

		self.__timer = QTimer()
		self.__timer.moveToThread(self)
		self.__timer.start(Constants.defaultTimerCycle * self.__timerCycleMultiplier)

		self.__timer.timeout.connect(self.updateTemplates, Qt.DirectConnection)

		self.exec_()

	@core.executionTrace
	def updateTemplates(self):
		"""
		This method updates Database Templates if they have been modified on disk.
		"""

		needModelRefresh = False
		for template in dbCommon.getTemplates(self.__dbSession):
			if template.path:
				if os.path.exists(template.path):
					storedStats = template.osStats.split(",")
					osStats = os.stat(template.path)
					if str(osStats[8]) != str(storedStats[8]):
						LOGGER.info("{0} | '{1}' Template file has been modified and will be updated!".format(self.__class__.__name__, template.name))
						if dbCommon.updateTemplateContent(self.__dbSession, template):
							LOGGER.info("{0} | '{1}' Template has been updated!".format(self.__class__.__name__, template.name))
							needModelRefresh = True

		needModelRefresh and self.emit(SIGNAL("databaseChanged()"))

class TemplatesOutliner_QTreeView(QTreeView):
	"""
	This class is the **TemplatesOutliner_QTreeView** class.
	"""

	@core.executionTrace
	def __init__(self, container):
		"""
		This method initializes the class.

		:param container: Container to attach the Component to. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTreeView.__init__(self, container)

		self.setAcceptDrops(True)

		# --- Setting class attributes. ---
		self.__container = container

		self.__coreTemplatesOutliner = self.__container.componentsManager.components["core.templatesOutliner"].interface

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
	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def dragEnterEvent(self, event):
		"""
		This method defines the drag enter event behavior.

		:param event: QEvent. ( QEvent )
		"""

		if event.mimeData().hasFormat("text/uri-list"):
			LOGGER.debug("> '{0}' drag event type accepted!".format("text/uri-list"))
			event.accept()
		else:
			event.ignore()

	@core.executionTrace
	def dragMoveEvent(self, event):
		"""
		This method defines the drag move event behavior.

		:param event: QEvent. ( QEvent )
		"""

		pass

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, OSError, foundations.exceptions.UserError)
	def dropEvent(self, event):
		"""
		This method defines the drop event behavior.

		:param event: QEvent. ( QEvent )
		"""

		if not self.__container.parameters.databaseReadOnly:
			if event.mimeData().hasUrls():
				LOGGER.debug("> Drag event urls list: '{0}'!".format(event.mimeData().urls()))
				for url in event.mimeData().urls():
					path = (platform.system() == "Windows" or platform.system() == "Microsoft") and re.search("^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
					if re.search("\.{0}$".format(self.__coreTemplatesOutliner.extension), str(url.path())):
						name = strings.getSplitextBasename(path)
						if messageBox.messageBox("Question", "Question", "'{0}' Template set file has been dropped, would you like to add it to the Database?".format(name), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
							self.__coreTemplatesOutliner.addTemplate(name, path)
					else:
						if os.path.isdir(path):
							if messageBox.messageBox("Question", "Question", "'{0}' directory has been dropped, would you like to add its content to the Database?".format(path), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
								self.__coreTemplatesOutliner.addDirectory(path)
						else:
							raise OSError, "{0} | Exception raised while parsing '{1}' path: Syntax is invalid!".format(self.__class__.__name__, path)
		else:
			raise foundations.exceptions.UserError, "{0} | Cannot perform action, Database has been set read only!".format(self.__class__.__name__)

class TemplatesOutliner(UiComponent):
	"""
	This class is the **TemplatesOutliner** class.
	"""

	# Custom signals definitions.
	modelRefresh = pyqtSignal()
	modelChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		:param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
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

		self.__modelHeaders = [ "Templates", "Release", "Software version" ]
		self.__treeViewIndentation = 15
		self.__treeViewInnerMargins = QMargins(0, 0, 0, 12)
		self.__templatesInformationsDefaultText = "<center><h4>* * *</h4>Select a Template to display related informations!<h4>* * *</h4></center>"
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
											<b>Output script:</b> {5}
											<p>
											<b>Comment:</b> {6}
											</p>
											<p>
											<b>Help file:</b> <a href="{7}"><span style=" text-decoration: underline; color:#e0e0e0;">template manual</span></a>
											</p>
											</p>
											"""

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for **self.__uiPath** attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for **self.__uiPath** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for **self.__uiPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This method is the property for **self.__uiResources** attribute.

		:return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for **self.__uiResources** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for **self.__uiResources** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiSoftwareAffixe(self):
		"""
		This method is the property for **self.__uiSoftwareAffixe** attribute.

		:return: self.__uiSoftwareAffixe. ( String )
		"""

		return self.__uiSoftwareAffixe

	@uiSoftwareAffixe.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSoftwareAffixe(self, value):
		"""
		This method is the setter method for **self.__uiSoftwareAffixe** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiSoftwareAffixe"))

	@uiSoftwareAffixe.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSoftwareAffixe(self):
		"""
		This method is the deleter method for **self.__uiSoftwareAffixe** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiSoftwareAffixe"))

	@property
	def uiUnknownSoftwareImage(self):
		"""
		This method is the property for **self.__uiUnknownSoftwareImage** attribute.

		:return: self.__uiUnknownSoftwareImage. ( String )
		"""

		return self.__uiUnknownSoftwareImage

	@uiUnknownSoftwareImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUnknownSoftwareImage(self, value):
		"""
		This method is the setter method for **self.__uiUnknownSoftwareImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiUnknownSoftwareImage"))

	@uiUnknownSoftwareImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUnknownSoftwareImage(self):
		"""
		This method is the deleter method for **self.__uiUnknownSoftwareImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiUnknownSoftwareImage"))

	@property
	def dockArea(self):
		"""
		This method is the property for **self.__dockArea** attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

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
	def settingsSeparator(self):
		"""
		This method is the property for **self.__settingsSeparator** attribute.

		:return: self.__settingsSeparator. ( String )
		"""

		return self.__settingsSeparator

	@settingsSeparator.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self, value):
		"""
		This method is the setter method for **self.__settingsSeparator** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self):
		"""
		This method is the deleter method for **self.__settingsSeparator** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settingsSeparator"))

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
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("model"))

	@property
	def modelSelection(self):
		"""
		This method is the property for **self.__modelSelection** attribute.

		:return: self.__modelSelection. ( Dictionary )
		"""

		return self.__modelSelection

	@modelSelection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self, value):
		"""
		This method is the setter method for **self.__modelSelection** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("modelSelection"))

	@modelSelection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelSelection(self):
		"""
		This method is the deleter method for **self.__modelSelection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("modelSelection"))

	@property
	def templatesOutlinerWorkerThread(self):
		"""
		This method is the property for **self.__templatesOutlinerWorkerThread** attribute.

		:return: self.__templatesOutlinerWorkerThread. ( QThread )
		"""

		return self.__templatesOutlinerWorkerThread

	@templatesOutlinerWorkerThread.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesOutlinerWorkerThread(self, value):
		"""
		This method is the setter method for **self.__templatesOutlinerWorkerThread** attribute.

		:param value: Attribute value. ( QThread )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templatesOutlinerWorkerThread"))

	@templatesOutlinerWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesOutlinerWorkerThread(self):
		"""
		This method is the deleter method for **self.__templatesOutlinerWorkerThread** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templatesOutlinerWorkerThread"))

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
	def defaultCollections(self):
		"""
		This method is the property for **self.__defaultCollections** attribute.

		:return: self.__defaultCollections. ( Dictionary )
		"""

		return self.__defaultCollections

	@defaultCollections.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollections(self, value):
		"""
		This method is the setter method for **self.__defaultCollections** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultCollections"))

	@defaultCollections.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollections(self):
		"""
		This method is the deleter method for **self.__defaultCollections** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultCollections"))

	@property
	def factoryCollection(self):
		"""
		This method is the property for **self.__factoryCollection** attribute.

		:return: self.__factoryCollection. ( String )
		"""

		return self.__factoryCollection

	@factoryCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryCollection(self, value):
		"""
		This method is the setter method for **self.__factoryCollection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("factoryCollection"))

	@factoryCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryCollection(self):
		"""
		This method is the deleter method for **self.__factoryCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("factoryCollection"))

	@property
	def userCollection(self):
		"""
		This method is the property for **self.__userCollection** attribute.

		:return: self.__userCollection. ( String )
		"""

		return self.__userCollection

	@userCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userCollection(self, value):
		"""
		This method is the setter method for **self.__userCollection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("userCollection"))

	@userCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userCollection(self):
		"""
		This method is the deleter method for **self.__userCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("userCollection"))

	@property
	def modelHeaders(self):
		"""
		This method is the property for **self.__modelHeaders** attribute.

		:return: self.__modelHeaders. ( List )
		"""

		return self.__modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self, value):
		"""
		This method is the setter method for **self.__modelHeaders** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("modelHeaders"))

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self):
		"""
		This method is the deleter method for **self.__modelHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("modelHeaders"))

	@property
	def treeViewIndentation(self):
		"""
		This method is the property for **self.__treeViewIndentation** attribute.

		:return: self.__treeViewIndentation. ( Integer )
		"""

		return self.__treeViewIndentation

	@treeViewIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self, value):
		"""
		This method is the setter method for **self.__treeViewIndentation** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("treeViewIndentation"))

	@treeViewIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self):
		"""
		This method is the deleter method for **self.__treeViewIndentation** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("treeViewIndentation"))

	@property
	def treeViewInnerMargins(self):
		"""
		This method is the property for **self.__treeViewInnerMargins** attribute.

		:return: self.__treeViewInnerMargins. ( Integer )
		"""

		return self.__treeViewInnerMargins

	@treeViewInnerMargins.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self, value):
		"""
		This method is the setter method for **self.__treeViewInnerMargins** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("treeViewInnerMargins"))

	@treeViewInnerMargins.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self):
		"""
		This method is the deleter method for **self.__treeViewInnerMargins** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("treeViewInnerMargins"))

	@property
	def templatesInformationsDefaultText(self):
		"""
		This method is the property for **self.__templatesInformationsDefaultText** attribute.

		:return: self.__templatesInformationsDefaultText. ( String )
		"""

		return self.__templatesInformationsDefaultText

	@templatesInformationsDefaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsDefaultText(self, value):
		"""
		This method is the setter method for **self.__templatesInformationsDefaultText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templatesInformationsDefaultText"))

	@templatesInformationsDefaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsDefaultText(self):
		"""
		This method is the deleter method for **self.__templatesInformationsDefaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templatesInformationsDefaultText"))

	@property
	def templatesInformationsText(self):
		"""
		This method is the property for **self.__templatesInformationsText** attribute.

		:return: self.__templatesInformationsText. ( String )
		"""

		return self.__templatesInformationsText

	@templatesInformationsText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsText(self, value):
		"""
		This method is the setter method for **self.__templatesInformationsText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("templatesInformationsText"))

	@templatesInformationsText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsText(self):
		"""
		This method is the deleter method for **self.__templatesInformationsText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("templatesInformationsText"))

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
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component cannot be deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__container.parameters.databaseReadOnly and	LOGGER.info("{0} | Templates_Outliner_treeView Model edition deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))
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
				LOGGER.info("{0} | Templates continuous scanner deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Templates continuous scanner deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

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
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component ui cannot be uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget cannot be removed!".format(self.name))

	@core.executionTrace
	def onStartup(self):
		"""
		This method is called on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework startup method.".format(self.__class__.__name__))

		if not self.__container.parameters.databaseReadOnly:
			# Adding default templates.
			self.addDefaultTemplates()

			# Templates table integrity checking.
			erroneousTemplates = dbCommon.checkTemplatesTableIntegrity(self.__coreDb.dbSession)
			if erroneousTemplates:
				for template in erroneousTemplates:
					if erroneousTemplates[template] == "INEXISTING_TEMPLATE_FILE_EXCEPTION":
						if messageBox.messageBox("Question", "Error", "{0} | '{1}' Template file is missing, would you like to update it's location?".format(self.__class__.__name__, template.name), QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No) == 16384:
							self.updateTemplateLocation(template)
					else:
						messageBox.messageBox("Warning", "Warning", "{0} | '{1}' {2}".format(self.__class__.__name__, template.name, dbCommon.DB_EXCEPTIONS[erroneousTemplates[template]]))
		else:
			LOGGER.info("{0} | Database default Templates wizard and Templates integrity checking method deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeCollections = str(self.__settings.getKey(self.__settingsSection, "activeCollections").toString())
		LOGGER.debug("> Stored '{0}' active Collections selection: '{1}'.".format(self.__class__.__name__, activeCollections))
		if activeCollections:
			if self.__settingsSeparator in activeCollections:
				collections = activeCollections.split(self.__settingsSeparator)
			else:
				collections = [activeCollections]
			self.__modelSelection["Collections"] = collections

		activeSoftwares = str(self.__settings.getKey(self.__settingsSection, "activeSoftwares").toString())
		LOGGER.debug("> Stored '{0}' active softwares selection: '{1}'.".format(self.__class__.__name__, activeSoftwares))
		if activeSoftwares:
			if self.__settingsSeparator in activeSoftwares:
				softwares = activeSoftwares.split(self.__settingsSeparator)
			else:
				softwares = [activeSoftwares]
			self.__modelSelection["Softwares"] = softwares

		activeTemplatesIds = str(self.__settings.getKey(self.__settingsSection, "activeTemplates").toString())
		LOGGER.debug("> Stored '{0}' active Templates ids selection: '{1}'.".format(self.__class__.__name__, activeTemplatesIds))
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
		This method is called on Framework close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework close method.".format(self.__class__.__name__))

		self.__Templates_Outliner_treeView_storeModelSelection()
		self.__settings.setKey(self.__settingsSection, "activeTemplates", self.__settingsSeparator.join(str(id) for id in self.__modelSelection["Templates"]))
		self.__settings.setKey(self.__settingsSection, "activeCollections", self.__settingsSeparator.join(str(id) for id in self.__modelSelection["Collections"]))
		self.__settings.setKey(self.__settingsSection, "activeSoftwares", self.__settingsSeparator.join(str(id) for id in self.__modelSelection["Softwares"]))

	@core.executionTrace
	def __Templates_Outliner_treeView_setModel(self):
		"""
		This method sets the **Templates_Outliner_treeView** Model.

		Columns:
		Templates | Release | Software version

		Rows:
		* Collection: { _type: "Collection" }
		** Software: { _type: "Software" }
		*** Template: { _type: "Template", _datas: dbTypes.DbTemplate }
		"""

		LOGGER.debug("> Setting up '{0}' Model!".format("Templates_Outliner_treeView"))

		self.__Templates_Outliner_treeView_storeModelSelection()

		self.__model.clear()

		self.__model.setHorizontalHeaderLabels(self.__modelHeaders)
		self.__model.setColumnCount(len(self.__modelHeaders))

		collections = dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type")

		for collection in collections:
			softwares = set((software[0] for software in self.__coreDb.dbSession.query(dbTypes.DbTemplate.software).filter(dbTypes.DbTemplate.collection == collection.id)))

			if softwares:
				LOGGER.debug("> Preparing '{0}' Collection for '{1}' Model.".format(collection.name, "Templates_Outliner_treeView"))

				collectionStandardItem = QStandardItem(QString(collection.name))
				collectionStandardItem._datas = collection
				collectionStandardItem._type = "Collection"

				LOGGER.debug("> Adding '{0}' Collection to '{1}' Model.".format(collection.name, "Templates_Outliner_treeView"))
				self.__model.appendRow(collectionStandardItem)

				for software in softwares:
					templates = set((template[0] for template in self.__coreDb.dbSession.query(dbTypes.DbTemplate.id).filter(dbTypes.DbTemplate.collection == collection.id).filter(dbTypes.DbTemplate.software == software)))

					if templates:
						LOGGER.debug("> Preparing '{0}' software for '{1}' Model.".format(software, "Templates_Outliner_treeView"))

						softwareStandardItem = QStandardItem(QString(software))
						iconPath = os.path.join(self.__uiResources, "{0}{1}".format(software, self.__uiSoftwareAffixe))
						if os.path.exists(iconPath):
							softwareStandardItem.setIcon(QIcon(iconPath))
						else:
							softwareStandardItem.setIcon(QIcon(os.path.join(self.__uiResources, self.__uiUnknownSoftwareImage)))

						softwareStandardItem._type = "Software"

						LOGGER.debug("> Adding '{0}' software to '{1}' Model.".format(software, "Templates_Outliner_treeView"))
						collectionStandardItem.appendRow([softwareStandardItem, None, None])

						for template in templates:
							template = dbCommon.filterTemplates(self.__coreDb.dbSession, "^{0}$".format(template), "id")[0]

							LOGGER.debug("> Preparing '{0}' Template for '{1}' Model.".format(template.name, "Templates_Outliner_treeView"))

							try:
								templateStandardItem = QStandardItem(QString("{0} {1}".format(template.renderer, template.title)))

								templateReleaseStandardItem = QStandardItem(QString(template.release))
								templateReleaseStandardItem.setTextAlignment(Qt.AlignCenter)

								templateVersionStandardItem = QStandardItem(QString(template.version))
								templateVersionStandardItem.setTextAlignment(Qt.AlignCenter)

								templateStandardItem._datas = template
								templateStandardItem._type = "Template"

								LOGGER.debug("> Adding '{0}' Template to '{1}' Model.".format(template.name, "Templates_Outliner_treeView"))
								softwareStandardItem.appendRow([templateStandardItem, templateReleaseStandardItem, templateVersionStandardItem])

							except Exception as error:
								LOGGER.error("!>{0} | Exception raised while adding '{1}' Template to '{2}' Model!".format(self.__class__.__name__, template.name, "Templates_Outliner_treeView"))
								foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "__Templates_Outliner_treeView_setModel"))

		self.__Templates_Outliner_treeView_restoreModelSelection()

		self.emit(SIGNAL("modelChanged()"))

	@core.executionTrace
	def __Templates_Outliner_treeView_refreshModel(self):
		"""
		This method refreshes the **Templates_Outliner_treeView** Model.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Templates_Outliner_treeView"))

		self.__Templates_Outliner_treeView_setModel()

	@core.executionTrace
	def __Templates_Outliner_treeView_setView(self):
		"""
		This method sets the **Templates_Outliner_treeView** View.
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
		This method sets **Templates_Outliner_treeView** default View state.
		"""

		LOGGER.debug("> Setting '{0}' default View state!".format("Templates_Outliner_treeView"))

		self.ui.Templates_Outliner_treeView.expandAll()
		for column in range(len(self.__modelHeaders)):
			self.ui.Templates_Outliner_treeView.resizeColumnToContents(column)

		self.ui.Templates_Outliner_treeView.sortByColumn(0, Qt.AscendingOrder)

	@core.executionTrace
	def __Templates_Outliner_treeView_refreshView(self):
		"""
		This method refreshes the **Templates_Outliner_treeView** View.
		"""

		self.__Templates_Outliner_treeView_setDefaultViewState()

	@core.executionTrace
	def __Templates_Outliner_treeView_storeModelSelection(self):
		"""
		This method stores **Templates_Outliner_treeView** Model selection.
		"""

		LOGGER.debug("> Storing '{0}' Model selection!".format("Templates_Outliner_treeView"))

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
		This method restores **Templates_Outliner_treeView** Model selection.
		"""

		LOGGER.debug("> Restoring '{0}' Model selection!".format("Templates_Outliner_treeView"))

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
		This method sets the **Templates_Outliner_treeView** actions.
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
			LOGGER.info("{0} | Templates Database alteration capabilities deactivated by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		displayHelpFilesAction = QAction("Display Help File(s) ...", self.ui.Templates_Outliner_treeView)
		displayHelpFilesAction.triggered.connect(self.__Templates_Outliner_treeView_displayHelpFilesAction__triggered)
		self.ui.Templates_Outliner_treeView.addAction(displayHelpFilesAction)

		separatorAction = QAction(self.ui.Templates_Outliner_treeView)
		separatorAction.setSeparator(True)
		self.ui.Templates_Outliner_treeView.addAction(separatorAction)

	@core.executionTrace
	def __Templates_Outliner_treeView_addTemplateAction__triggered(self, checked):
		"""
		This method is triggered by **addTemplateAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.addTemplate__()

	@core.executionTrace
	def __Templates_Outliner_treeView_removeTemplatesAction__triggered(self, checked):
		"""
		This method is triggered by **removeTemplatesAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.removeTemplates__()

	@core.executionTrace
	def __Templates_Outliner_treeView_importDefaultTemplatesAction__triggered(self, checked):
		"""
		This method is triggered by **importDefaultTemplatesAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.importDefaultTemplates__()

	@core.executionTrace
	def __Templates_Outliner_treeView_displayHelpFilesAction__triggered(self, checked):
		"""
		This method is triggered by **displayHelpFilesAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.displayHelpFiles__()

	@core.executionTrace
	def __Templates_Outliner_treeView_filterTemplatesVersionsAction__triggered(self, checked):
		"""
		This method is triggered by **filterTemplatesVersionsAction** action.

		:param checked: Action checked state. ( Boolean )
		"""

		self.filterTemplatesVersions__()

	@core.executionTrace
	def __Templates_Outliner_treeView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method sets the **Template_Informations_textEdit** Widget.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
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
		This method is triggered when a link is clicked in the **Template_Informations_textBrowser** Widget.

		:param url: Url to explore. ( QUrl )
		"""

		QDesktopServices.openUrl(url)

	@core.executionTrace
	def __coreDb_database__changed(self):
		"""
		This method is triggered by the **TemplatesOutliner_Worker** when the Database has changed.
		"""

		# Ensure that db objects modified by the worker thread will refresh properly.
		self.__coreDb.dbSession.expire_all()
		self.emit(SIGNAL("modelRefresh()"))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def addTemplate__(self):
		"""
		This method adds an user defined Template to the Database.

		:return: Method success. ( Boolean )
		"""

		path = self.__container.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Add Template:", self.__container.lastBrowsedPath, "sIBLT files (*.{0})".format(self.__extension))))
		if not path:
			return

		if not self.templateExists(path):
			LOGGER.debug("> Chosen Template path: '{0}'.".format(path))
			if self.addTemplate(strings.getSplitextBasename(path), path):
				return True
			else:
				raise Exception, "{0} | Exception raised while adding '{1}' Template to the Database!".format(self.__class__.__name__, path)
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Template already exists in Database!".format(self.__class__.__name__, path))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def removeTemplates__(self):
		"""
		This method removes user selected Templates from the Database.

		:return: Method success. ( Boolean )
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

		selectedCollections and messageBox.messageBox("Warning", "Warning", "{0} | Cannot remove '{1}' Collection(s)!".format(self.__class__.__name__, ", ".join(selectedCollections)))
		selectedSoftwares and messageBox.messageBox("Warning", "Warning", "{0} | Cannot remove '{1}' software(s)!".format(self.__class__.__name__, ", ".join(selectedSoftwares)))

		if not selectedTemplates:
			return

		if messageBox.messageBox("Question", "Question", "Are you sure you want to remove '{0}' Template(s)?".format(", ".join([str(template.name) for template in selectedTemplates])), buttons=QMessageBox.Yes | QMessageBox.No) == 16384:
			success = True
			for template in selectedTemplates:
				success *= self.removeTemplate(template, emitSignal=False) or False

			self.emit(SIGNAL("modelRefresh()"))

			if success:
				return True
			else:
				raise Exception, "{0} | Exception raised while removing '{1}' Templates from the Database!".format(self.__class__.__name__, ", ". join((template.name for template in selectedTemplates)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def importDefaultTemplates__(self):
		"""
		This method imports default Templates into the Database.

		:return: Method success. ( Boolean )
		"""

		if self.addDefaultTemplates(forceImport=True):
			return True
		else:
			raise Exception, "{0} | Exception raised while importing default Templates into the Database!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def displayHelpFiles__(self):
		"""
		This method displays user selected Templates help files.

		:return: Method success. ( Boolean )
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
			raise Exception, "{0} | Exception raised while displaying Templates help files!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def filterTemplatesVersions__(self):
		"""
		This method filters Templates by versions.

		:return: Method success. ( Boolean )
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
					raise Exception, "{0} | Exception raised while filtering Templates by versions!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError, foundations.exceptions.DatabaseOperationError)
	def addTemplate(self, name, path, collectionId=None, emitSignal=True):
		"""
		This method adds a Template to the Database.

		:param name: Template set name. ( String )
		:param path: Template set path. ( String )
		:param collectionId: Target Collection id. ( Integer )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not dbCommon.filterTemplates(self.__coreDb.dbSession, "^{0}$".format(re.escape(path)), "path"):
			LOGGER.info("{0} | Adding '{1}' Template to the Database!".format(self.__class__.__name__, name))
			if dbCommon.addTemplate(self.__coreDb.dbSession, name, path, collectionId or self.getUniqueCollectionId(path)):
				emitSignal and self.emit(SIGNAL("modelRefresh()"))
				return True
			else:
				raise foundations.exceptions.DatabaseOperationError, "{0} | Exception raised while adding '{1}' Template to the Database!".format(self.__class__.__name__, name)
		else:
			raise foundations.exceptions.ProgrammingError, "{0} | '{1}' Template already exists in Database!".format(self.__class__.__name__, name)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addDirectory(self, directory, collectionId=None):
		"""
		This method adds provided directory Templates to the Database.

		:param directory: Templates directory. ( String )
		:param collectionId: Collection id. ( Integer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing directory '{0}' walker.".format(directory))

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
			raise Exception, "{0} | Exception raised while adding '{1}' directory content to the Database!".format(self.__class__.__name__, directory)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addDefaultTemplates(self, forceImport=False):
		"""
		This method adds default Templates Collections / Templates to the Database.

		:param forceImport: Force Templates import. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not forceImport and self.getTemplates():
			return

		LOGGER.debug("> Adding default Templates to the Database.")
		for collection, path in self.__defaultCollections.items():
			if not os.path.exists(path):
				continue

			if not set(dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(collection), "name")).intersection(dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type")):
				LOGGER.info("{0} | Adding '{1}' Collection to the Database!".format(self.__class__.__name__, collection))
				dbCommon.addCollection(self.__coreDb.dbSession, collection, "Templates", "Template {0} Collection".format(collection))
			if self.addDirectory(path, self.getCollection(collection).id):
				return True
			else:
				raise Exception, "{0} | Exception raised while adding default Templates to the Database!".format(self.__class__.__name__)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.DatabaseOperationError)
	def removeTemplate(self, template, emitSignal=True):
		"""
		This method removes provided Template from the Database.

		:param templates: Template to remove. ( List )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Removing '{1}' Template from the Database!".format(self.__class__.__name__, template.name))
		if dbCommon.removeTemplate(self.__coreDb.dbSession, str(template.id)) :
			emitSignal and self.emit(SIGNAL("modelRefresh()"))
			return True
		else:
			raise foundations.exceptions.DatabaseOperationError, "{0} | Exception raised while removing '{1}' Template from the Database!".format(self.__class__.__name__, template.name)

	@core.executionTrace
	def templateExists(self, path):
		"""
		This method returns if provided Template path exists in the Database.

		:param name: Template path. ( String )
		:return: Template exists. ( Boolean )
		"""

		return dbCommon.templateExists(self.__coreDb.dbSession, path)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.DatabaseOperationError)
	def updateTemplateLocation(self, template, emitSignal=True):
		"""
		This method updates provided Template location.

		:param template: Template to update. ( DbTemplate )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		file = self.__container.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Updating '{0}' Template location:".format(template.name), self.__container.lastBrowsedPath, "Template files (*{0})".format(self.__extension))))
		if not file:
			return

		LOGGER.info("{0} | Updating '{1}' Template with new location '{2}'!".format(self.__class__.__name__, template.name, file))
		if not dbCommon.updateTemplateLocation(self.__coreDb.dbSession, template, file):
			emitSignal and self.emit(SIGNAL("modelRefresh()"))
			return True
		else:
			raise foundations.exceptions.DatabaseOperationError, "{0} | Exception raised while updating '{1}' Template location!".format(self.__class__.__name__, template.name)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def displayHelpFile(self, template):
		"""
		This method displays provided Templates help file.

		:param template: Template to display help file. ( DbTemplate )
		:return: Method success. ( Boolean )
		"""

		if os.path.exists(template.helpFile):
			LOGGER.info("{0} | Opening '{1}' Template help file: '{2}'.".format(self.__class__.__name__, template.name, template.helpFile))
			QDesktopServices.openUrl(QUrl.fromLocalFile(template.helpFile))
			return True
		else:
			raise OSError, "{0} | Exception raised while displaying '{1}' Template help file: '{2}' file doesn't exists!".format(self.__class__.__name__, template.name, template.helpFile)

	@core.executionTrace
	def getTemplates(self):
		"""
		This method returns Database Templates.

		:return: Database Templates Collections. ( List )
		"""

		return [template for template in dbCommon.getTemplates(self.__coreDb.dbSession)]

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This method returns the **Templates_Outliner_treeView** selected items.

		:param rowsRootOnly: Return rows roots only. ( Boolean )
		:return: View selected items. ( List )
		"""

		selectedIndexes = self.ui.Templates_Outliner_treeView.selectedIndexes()
		return rowsRootOnly and [item for item in set([self.__model.itemFromIndex(self.__model.sibling(index.row(), 0, index)) for index in selectedIndexes])] or [self.__model.itemFromIndex(index) for index in selectedIndexes]

	@core.executionTrace
	def getSelectedTemplates(self):
		"""
		This method returns the selected Templates.

		:return: View selected Templates. ( List )
		"""

		selectedItems = self.getSelectedItems()
		return selectedItems and [item._datas for item in selectedItems if item._type == "Template"] or []

	@core.executionTrace
	def getCollection(self, collection):
		"""
		This method gets Template Collection from provided Collection name.

		:param collection: Collection name. ( String )
		:return: Collection. ( DbCollection )
		"""

		return [collection for collection in set(dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(collection), "name")).intersection(dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type"))][0]

	@core.executionTrace
	def getUniqueCollectionId(self, path):
		"""
		This method gets an unique Collection id using provided path.

		:param path: Template path. ( String )
		:return: Unique id. ( Integer )
		"""

		templatesCollections = dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type")
		return self.defaultCollections[self.__factoryCollection] in path and [collection for collection in set(dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(self.__factoryCollection), "name")).intersection(templatesCollections)][0].id or [collection for collection in set(dbCommon.filterCollections(self.__coreDb.dbSession, "^{0}$".format(self.__userCollection), "name")).intersection(templatesCollections)][0].id

