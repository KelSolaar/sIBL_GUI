#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**templatesOutliner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`TemplatesOutliner` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import platform
import re
from collections import OrderedDict
from PyQt4.QtCore import QMargins
from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QMessageBox

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.strings as strings
import sibl_gui.components.core.db.exceptions as dbExceptions
import sibl_gui.components.core.db.utilities.common as dbCommon
import sibl_gui.components.core.db.utilities.nodes as dbNodes
import sibl_gui.components.core.db.utilities.types as dbTypes
import umbra.engine
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from manager.qwidgetComponent import QWidgetComponentFactory
from foundations.walkers import OsWalker
from sibl_gui.components.core.templatesOutliner.models import SoftwareNode
from sibl_gui.components.core.templatesOutliner.models import TemplatesModel
from sibl_gui.components.core.templatesOutliner.views import Templates_QTreeView
from sibl_gui.components.core.templatesOutliner.workers import TemplatesOutliner_Worker
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "TemplatesOutliner"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Templates_Outliner.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TemplatesOutliner(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.core.templatesOutliner.templatesOutliner` Component Interface class.
	| It defines methods for Database Templates management.
	"""

	# Custom signals definitions.
	modelRefresh = pyqtSignal()
	"""
	This signal is emited by the :class:`TemplatesOutliner` class when :obj:`TemplatesOutliner.model` class property
	model needs to be refreshed. ( pyqtSignal )
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(TemplatesOutliner, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiResourcesDirectory = "resources"
		self.__uiSoftwareAffixe = "_Software.png"
		self.__uiUnknownSoftwareImage = "Unknown_Software.png"
		self.__dockArea = 1

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None
		self.__settingsSeparator = ","

		self.__editLayout = "editCentric"

		self.__factoryScriptEditor = None
		self.__coreDb = None

		self.__model = None
		self.__view = None
		self.__headers = OrderedDict([("Templates", "name"),
										("Release", "release"),
										("Software Version", "version")])

		self.__templatesOutlinerWorkerThread = None

		self.__extension = "sIBLT"

		self.__defaultCollections = None
		self.__factoryCollection = "Factory"
		self.__userCollection = "User"

		self.__treeViewInnerMargins = QMargins(0, 0, 0, 12)

		self.__templatesInformationsDefaultText = \
					"<center><h4>* * *</h4>Select a Template to display related informations!<h4>* * *</h4></center>"
		self.__templatesInformationsText = """
											<h4><center>{0}</center></h4>
											<p>
											<b>Date:</b> {1}
											<br/>
											<b>Author:</b> {2}
											<br/>
											<b>Email:</b> <a href="mailto:{3}">
											<span style=" text-decoration: underline; color:#e0e0e0;">{3}</span></a>
											<br/>
											<b>Url:</b> <a href="{4}">
											<span style=" text-decoration: underline; color:#e0e0e0;">{4}</span></a>
											<br/>
											<b>Output script:</b> {5}
											<p>
											<b>Comment:</b> {6}
											</p>
											<p>
											<b>Help file:</b> <a href="{7}">
											<span style=" text-decoration: underline; color:#e0e0e0;">
											template manual</span></a>
											</p>
											</p>
											"""

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiSoftwareAffixe"))

	@uiSoftwareAffixe.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSoftwareAffixe(self):
		"""
		This method is the deleter method for **self.__uiSoftwareAffixe** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSoftwareAffixe"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiUnknownSoftwareImage"))

	@uiUnknownSoftwareImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiUnknownSoftwareImage(self):
		"""
		This method is the deleter method for **self.__uiUnknownSoftwareImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiUnknownSoftwareImage"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSeparator(self):
		"""
		This method is the deleter method for **self.__settingsSeparator** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSeparator"))

	@property
	def editLayout(self):
		"""
		This method is the property for **self.__editLayout** attribute.

		:return: self.__editLayout. ( String )
		"""

		return self.__editLayout

	@editLayout.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editLayout(self, value):
		"""
		This method is the setter method for **self.__editLayout** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "editLayout"))

	@editLayout.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editLayout(self):
		"""
		This method is the deleter method for **self.__editLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editLayout"))

	@property
	def factoryScriptEditor(self):
		"""
		This method is the property for **self.__factoryScriptEditor** attribute.

		:return: self.__factoryScriptEditor. ( Object )
		"""

		return self.__factoryScriptEditor

	@factoryScriptEditor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self, value):
		"""
		This method is the setter method for **self.__factoryScriptEditor** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryScriptEditor"))

	@factoryScriptEditor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self):
		"""
		This method is the deleter method for **self.__factoryScriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryScriptEditor"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def view(self):
		"""
		This method is the property for **self.__view** attribute.

		:return: self.__view. ( QWidget )
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		This method is the setter method for **self.__view** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		This method is the deleter method for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def headers(self):
		"""
		This method is the property for **self.__headers** attribute.

		:return: self.__headers. ( OrderedDict )
		"""

		return self.__headers

	@headers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		This method is the setter method for **self.__headers** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

	@headers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def headers(self):
		"""
		This method is the deleter method for **self.__headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesOutlinerWorkerThread"))

	@templatesOutlinerWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesOutlinerWorkerThread(self):
		"""
		This method is the deleter method for **self.__templatesOutlinerWorkerThread** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesOutlinerWorkerThread"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "extension"))

	@extension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		This method is the deleter method for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultCollections"))

	@defaultCollections.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultCollections(self):
		"""
		This method is the deleter method for **self.__defaultCollections** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultCollections"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryCollection"))

	@factoryCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryCollection(self):
		"""
		This method is the deleter method for **self.__factoryCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryCollection"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "userCollection"))

	@userCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userCollection(self):
		"""
		This method is the deleter method for **self.__userCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "userCollection"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesInformationsDefaultText"))

	@templatesInformationsDefaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsDefaultText(self):
		"""
		This method is the deleter method for **self.__templatesInformationsDefaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesInformationsDefaultText"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "treeViewInnerMargins"))

	@treeViewInnerMargins.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self):
		"""
		This method is the deleter method for **self.__treeViewInnerMargins** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "treeViewInnerMargins"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesInformationsText"))

	@templatesInformationsText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def templatesInformationsText(self):
		"""
		This method is the deleter method for **self.__templatesInformationsText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesInformationsText"))

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

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__),
													self.__uiResourcesDirectory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__factoryScriptEditor = self.__engine.componentsManager.components["factory.scriptEditor"].interface
		self.__coreDb = self.__engine.componentsManager.components["core.db"].interface

		RuntimeGlobals.templatesFactoryDirectory = umbra.ui.common.getResourcePath(Constants.templatesDirectory)
		RuntimeGlobals.templatesUserDirectory = os.path.join(self.__engine.userApplicationDataDirectory,
															Constants.templatesDirectory)

		self.__defaultCollections = {self.__factoryCollection : RuntimeGlobals.templatesFactoryDirectory,
									self.__userCollection : RuntimeGlobals.templatesUserDirectory}

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__engine.parameters.databaseReadOnly and \
		LOGGER.info("{0} | Model edition deactivated by '{1}' command line parameter value!".format(
		self.__class__.__name__, "databaseReadOnly"))
		self.__model = TemplatesModel(self, horizontalHeaders=self.__headers)
		self.setTemplates()

		self.Templates_Outliner_treeView.setParent(None)
		self.Templates_Outliner_treeView = Templates_QTreeView(self, self.__model, self.__engine.parameters.databaseReadOnly)
		self.Templates_Outliner_treeView.setObjectName("Templates_Outliner_treeView")
		self.Templates_Outliner_gridLayout.setContentsMargins(self.__treeViewInnerMargins)
		self.Templates_Outliner_gridLayout.addWidget(self.Templates_Outliner_treeView, 0, 0)
		self.__view = self.Templates_Outliner_treeView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__view_addActions()

		self.Template_Informations_textBrowser.setText(self.__templatesInformationsDefaultText)
		self.Template_Informations_textBrowser.setOpenLinks(False)

		self.Templates_Outliner_splitter.setSizes([16777215, 1])

		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				self.__templatesOutlinerWorkerThread = TemplatesOutliner_Worker(self)
				self.__templatesOutlinerWorkerThread.start()
				self.__engine.workerThreads.append(self.__templatesOutlinerWorkerThread)
			else:
				LOGGER.info("{0} | Templates continuous scanner deactivated by '{1}' command line parameter value!".format(
				self.__class__.__name__, "deactivateWorkerThreads"))
		else:
			LOGGER.info("{0} | Templates continuous scanner deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		# Signals / Slots.
		self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.Template_Informations_textBrowser.anchorClicked.connect(self.__Template_Informations_textBrowser__anchorClicked)
		self.modelRefresh.connect(self.__templatesOutliner__modelRefresh)
		if not self.__engine.parameters.databaseReadOnly:
			if not self.__engine.parameters.deactivateWorkerThreads:
				self.__templatesOutlinerWorkerThread.databaseChanged.connect(self.__coreDb_database__databaseChanged)
			self.__engine.contentDropped.connect(self.__application__contentDropped)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def onStartup(self):
		"""
		This method is called on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			# Adding default templates.
			self.addDefaultTemplates()

			# Templates table integrity checking.
			erroneousTemplates = dbCommon.checkTemplatesTableIntegrity(self.__coreDb.dbSession)
			if erroneousTemplates:
				for template in erroneousTemplates:
					if erroneousTemplates[template] == "INEXISTING_TEMPLATE_FILE_EXCEPTION":
						if messageBox.messageBox("Question", "Error",
						"{0} | '{1}' Template file is missing, would you like to update it's location?".format(
						self.__class__.__name__, template.name),
						QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
							self.updateTemplateLocation(template)
					else:
						messageBox.messageBox("Warning", "Warning",
						"{0} | '{1}' {2}".format(self.__class__.__name__,
												template.name,
												dbCommon.DB_EXCEPTIONS[erroneousTemplates[template]]))
		else:
			LOGGER.info("{0} | Database default Templates wizard and Templates integrity checking method deactivated by \
			'{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeCollectionsIdentities = str(self.__settings.getKey(self.__settingsSection, "activeCollections").toString())
		LOGGER.debug("> Stored '{0}' active Collections selection: '{1}'.".format(self.__class__.__name__,
																				activeCollectionsIdentities))
		self.__view.modelSelection["Collections"] = activeCollectionsIdentities and [int(identity)
																		for identity in activeCollectionsIdentities.split(
																		self.__settingsSeparator)] or []

		activeSoftwares = str(self.__settings.getKey(self.__settingsSection, "activeSoftwares").toString())
		LOGGER.debug("> Stored '{0}' active softwares selection: '{1}'.".format(self.__class__.__name__, activeSoftwares))
		self.__view.modelSelection["Softwares"] = activeSoftwares and activeSoftwares.split(self.__settingsSeparator) or []

		activeTemplatesIdentities = str(self.__settings.getKey(self.__settingsSection, "activeTemplates").toString())
		LOGGER.debug("> '{0}' View stored selected Templates identities '{1}'.".format(self.__class__.__name__,
																						activeTemplatesIdentities))
		self.__view.modelSelection["Templates"] = activeTemplatesIdentities and [int(identity)
																		for identity in activeTemplatesIdentities.split(
																		self.__settingsSeparator)] or []

		self.__view.restoreModelSelection()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def onClose(self):
		"""
		This method is called on Framework close.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		self.__view.storeModelSelection()
		self.__settings.setKey(self.__settingsSection,
								"activeTemplates",
								self.__settingsSeparator.join(str(identity)
															for identity in self.__view.modelSelection["Templates"]))
		self.__settings.setKey(self.__settingsSection,
								"activeCollections",
								self.__settingsSeparator.join(str(identity)
															for identity in self.__view.modelSelection["Collections"]))
		self.__settings.setKey(self.__settingsSection,
								"activeSoftwares",
								self.__settingsSeparator.join(str(name)
															for name in self.__view.modelSelection["Softwares"]))
		return True

	@core.executionTrace
	def __view_addActions(self):
		"""
		This method sets the View actions.
		"""

		if not self.__engine.parameters.databaseReadOnly:
			self.__view.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.templatesOutliner|Add Template ...",
			slot=self.__view_addTemplateAction__triggered))
			self.__view.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.templatesOutliner|Remove Template(s) ...",
			slot=self.__view_removeTemplatesAction__triggered))

			separatorAction = QAction(self.__view)
			separatorAction.setSeparator(True)
			self.__view.addAction(separatorAction)

			self.__view.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.templatesOutliner|Import Default Templates",
			slot=self.__view_importDefaultTemplatesAction__triggered))
			self.__view.addAction(self.__engine.actionsManager.registerAction(
			"Actions|Umbra|Components|core.templatesOutliner|Filter Templates Versions",
			slot=self.__view_filterTemplatesVersionsAction__triggered))

			separatorAction = QAction(self.__view)
			separatorAction.setSeparator(True)
			self.__view.addAction(separatorAction)
		else:
			LOGGER.info("{0} | Templates Database alteration capabilities deactivated by \
			'{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.templatesOutliner|Display Help File(s) ...",
		slot=self.__view_displayHelpFilesAction__triggered))

		separatorAction = QAction(self.__view)
		separatorAction.setSeparator(True)
		self.__view.addAction(separatorAction)

	@core.executionTrace
	def __view_addTemplateAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.templatesOutliner|Add Template ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.addTemplate_ui()

	@core.executionTrace
	def __view_removeTemplatesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.templatesOutliner|Remove Template(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.removeTemplates_ui()

	@core.executionTrace
	def __view_importDefaultTemplatesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.templatesOutliner|Import Default Templates'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.importDefaultTemplates_ui()

	@core.executionTrace
	def __view_displayHelpFilesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.templatesOutliner|Display Help File(s) ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.displayHelpFiles_ui()

	@core.executionTrace
	def __view_filterTemplatesVersionsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|core.templatesOutliner|Filter Templates Versions'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.filterTemplatesVersions_ui()

	@core.executionTrace
	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
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
				template and content.append(self.__templatesInformationsText.format("{0} {1} {2}".format(template.software,
																										template.renderer,
																										template.title),
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

		self.Template_Informations_textBrowser.setText(separator.join(content))

	@core.executionTrace
	def __Template_Informations_textBrowser__anchorClicked(self, url):
		"""
		This method is triggered when a link is clicked in the **Template_Informations_textBrowser** Widget.

		:param url: Url to explore. ( QUrl )
		"""

		QDesktopServices.openUrl(url)

	@core.executionTrace
	def __templatesOutliner__modelRefresh(self):
		"""
		This method is triggered when the Model data need refresh.
		"""

		self.setTemplates()

	@core.executionTrace
	def __coreDb_database__databaseChanged(self, templates):
		"""
		This method is triggered by the
		:class:`umbra.components.core.templatesOutliner.workers.TemplatesOutliner_Worker`class
		when the Database has changed.

		:param templates: Modified Templates. ( List )
		"""

		# Ensure that db objects modified by the worker thread will refresh properly.
		self.__coreDb.dbSession.expire_all()
		self.modelRefresh.emit()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler,
											False,
											foundations.exceptions.UserError)
	@umbra.engine.showProcessing("Retrieving Templates ...")
	def __application__contentDropped(self, event):
		"""
		This method is triggered when content is dropped in the Application.
		
		:param event: Event. ( QEvent )
		"""

		if not event.mimeData().hasUrls():
			return

		LOGGER.debug("> Drag event urls list: '{0}'!".format(event.mimeData().urls()))

		if not self.__engine.parameters.databaseReadOnly:
			for url in event.mimeData().urls():
				path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
				re.search(r"^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
				if re.search(r"\.{0}$".format(self.__extension), str(url.path())):
					name = strings.getSplitextBasename(path)
					choice = messageBox.messageBox("Question", "Question",
					"'{0}' Template file has been dropped, would you like \
					to 'Add' it to the Database or 'Edit' it in the Script Editor?".format(name),
					buttons=QMessageBox.Cancel,
					customButtons=((QString("Add"), QMessageBox.AcceptRole), (QString("Edit"), QMessageBox.AcceptRole)))
					if choice == 0:
						self.addTemplate(name, path)
					elif choice == 1:
						self.__factoryScriptEditor.loadFile(path)
						self.__engine.currentLayout != self.__editLayout and self.__engine.restoreLayout(self.__editLayout)
				else:
					if not os.path.isdir(path):
						return

					osWalker = OsWalker(path)
					osWalker.walk(("\.{0}$".format(self.__extension),), ("\._",))

					if not osWalker.files:
						return

					if messageBox.messageBox("Question", "Question",
					"Would you like to add '{0}' directory Template(s) file(s) to the Database?".format(path),
					buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
						self.addDirectory(path)
				self.__engine.processEvents()
		else:
			raise foundations.exceptions.UserError(
			"{0} | Cannot perform action, Database has been set read only!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.showProcessing("Adding Template ...")
	def addTemplate_ui(self):
		"""
		This method adds an user defined Template to the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		path = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																		"Add Template:",
																		RuntimeGlobals.lastBrowsedPath,
																		"sIBLT files (*.{0})".format(self.__extension))))
		if not path:
			return

		if not self.templateExists(path):
			LOGGER.debug("> Chosen Template path: '{0}'.".format(path))
			if self.addTemplate(strings.getSplitextBasename(path), path):
				return True
			else:
				raise Exception("{0} | Exception raised while adding '{1}' Template to the Database!".format(
				self.__class__.__name__, path))
		else:
			messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Template already exists in Database!".format(
			self.__class__.__name__, path))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.encapsulateProcessing
	def removeTemplates_ui(self):
		"""
		This method removes user selected Templates from the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedNodes = self.getSelectedNodes()

		selectedCollections = []
		selectedSoftwares = []
		for item in selectedNodes:
			if item.family == "Collection":
				selectedCollections.append(item.name)
			elif item.family == "Software":
				selectedSoftwares.append(item.name)
		selectedCollections and messageBox.messageBox("Warning", "Warning",
		"{0} | Cannot remove '{1}' Collection(s)!".format(self.__class__.__name__, ", ".join(selectedCollections)))
		selectedSoftwares and messageBox.messageBox("Warning", "Warning",
		"{0} | Cannot remove '{1}' software(s)!".format(self.__class__.__name__, ", ".join(selectedSoftwares)))

		selectedTemplates = self.getSelectedTemplates()
		if not selectedTemplates:
			return

		if messageBox.messageBox("Question", "Question",
		"Are you sure you want to remove '{0}' Template(s)?".format(
		", ".join([str(template.name) for template in selectedTemplates])),
		buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.startProcessing("Removing Templates ...", len(selectedTemplates))
			success = True
			for template in selectedTemplates:
				success *= self.removeTemplate(template, emitSignal=False) or False
				self.__engine.stepProcessing()
			self.__engine.stopProcessing()

			self.modelRefresh.emit()

			if success:
				return True
			else:
				raise Exception("{0} | Exception raised while removing '{1}' Templates from the Database!".format(
				self.__class__.__name__, ", ". join((template.name for template in selectedTemplates))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.showProcessing("Importing Default Templates ...")
	def importDefaultTemplates_ui(self):
		"""
		This method imports default Templates into the Database.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		if self.addDefaultTemplates(forceImport=True):
			return True
		else:
			raise Exception("{0} | Exception raised while importing default Templates into the Database!".format(
			self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.encapsulateProcessing
	def displayHelpFiles_ui(self):
		"""
		This method displays user selected Templates help files.

		:return: Method success. ( Boolean )
		"""

		selectedTemplates = self.getSelectedTemplates()
		if not selectedTemplates:
			return

		self.__engine.startProcessing("Displaying Templates Help Files ...", len(selectedTemplates))
		success = True
		for template in selectedTemplates:
			success *= self.displayHelpFile(template) or False
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while displaying Templates help files!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	@umbra.engine.encapsulateProcessing
	def filterTemplatesVersions_ui(self):
		"""
		This method filters Templates by versions.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		templates = dbCommon.getTemplates(self.__coreDb.dbSession)
		self.__engine.startProcessing("Filtering Templates ...", len(templates.all()))
		success = True
		for template in templates:
			matchingTemplates = dbCommon.filterTemplates(self.__coreDb.dbSession, "^{0}$".format(template.name), "name")
			if len(matchingTemplates) != 1:
				for id in sorted([(dbTemplate.id, dbTemplate.release) for dbTemplate in matchingTemplates],
								reverse=True,
								key=lambda x:(strings.getVersionRank(x[1])))[1:]:
					success *= dbCommon.removeTemplate(self.__coreDb.dbSession, id[0]) or False
				self.modelRefresh.emit()
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while filtering Templates by versions!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None,
											False,
											foundations.exceptions.ProgrammingError,
											dbExceptions.DatabaseOperationError)
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
				emitSignal and self.modelRefresh.emit()
				return True
			else:
				raise dbExceptions.DatabaseOperationError(
				"{0} | Exception raised while adding '{1}' Template to the Database!".format(self.__class__.__name__, name))
		else:
			raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Template already exists in Database!".format(self.__class__.__name__, name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@umbra.engine.encapsulateProcessing
	def addDirectory(self, directory, collectionId=None):
		"""
		This method adds given directory Templates to the Database.

		:param directory: Templates directory. ( String )
		:param collectionId: Collection id. ( Integer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing directory '{0}' osWalker.".format(directory))

		osWalker = OsWalker(directory)
		osWalker.walk(("\.{0}$".format(self.__extension),), ("\._",))

		self.__engine.startProcessing("Adding Directory Templates ...", len(osWalker.files.keys()))
		success = True
		for template, path in osWalker.files.items():
			if not self.templateExists(path):
				success *= self.addTemplate(namespace.getNamespace(template, rootOnly=True),
											path,
											collectionId,
											emitSignal=False) or False
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.modelRefresh.emit()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
			self.__class__.__name__, directory))

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

		success = True
		for collection, path in ((collection, path) for (collection, path) in self.__defaultCollections.items() if path):
			if not os.path.exists(path):
				continue

			if not set(dbCommon.filterCollections(self.__coreDb.dbSession,
												"^{0}$".format(collection), "name")).intersection(
												dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type")):
				LOGGER.info("{0} | Adding '{1}' Collection to the Database!".format(self.__class__.__name__, collection))
				dbCommon.addCollection(self.__coreDb.dbSession,
										collection,
										"Templates", "Template {0} Collection".format(collection))
			success *= self.addDirectory(path, self.getCollection(collection).id)

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while adding default Templates to the Database!".format(
			self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, dbExceptions.DatabaseOperationError)
	def removeTemplate(self, template, emitSignal=True):
		"""
		This method removes given Template from the Database.

		:param templates: Template to remove. ( List )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Removing '{1}' Template from the Database!".format(self.__class__.__name__, template.name))
		if dbCommon.removeTemplate(self.__coreDb.dbSession, str(template.id)) :
			emitSignal and self.modelRefresh.emit()
			return True
		else:
			raise dbExceptions.DatabaseOperationError(
			"{0} | Exception raised while removing '{1}' Template from the Database!".format(self.__class__.__name__,
																							template.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def templateExists(self, path):
		"""
		This method returns if given Template path exists in the Database.

		:param name: Template path. ( String )
		:return: Template exists. ( Boolean )
		"""

		return dbCommon.templateExists(self.__coreDb.dbSession, path)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, dbExceptions.DatabaseOperationError)
	def updateTemplateLocation(self, template, emitSignal=True):
		"""
		This method updates given Template location.

		:param template: Template to update. ( DbTemplate )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		file = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																"Updating '{0}' Template location:".format(template.name),
																RuntimeGlobals.lastBrowsedPath,
																"Template files (*{0})".format(self.__extension))))
		if not file:
			return

		LOGGER.info("{0} | Updating '{1}' Template with new location '{2}'!".format(self.__class__.__name__,
																					template.name, file))
		if not dbCommon.updateTemplateLocation(self.__coreDb.dbSession, template, file):
			emitSignal and self.modelRefresh.emit()
			return True
		else:
			raise dbExceptions.DatabaseOperationError(
			"{0} | Exception raised while updating '{1}' Template location!".format(self.__class__.__name__, template.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def displayHelpFile(self, template):
		"""
		This method displays given Templates help file.

		:param template: Template to display help file. ( DbTemplate )
		:return: Method success. ( Boolean )
		"""

		if os.path.exists(template.helpFile):
			LOGGER.info("{0} | Opening '{1}' Template help file: '{2}'.".format(self.__class__.__name__,
																				template.name,
																				template.helpFile))
			QDesktopServices.openUrl(QUrl.fromLocalFile(template.helpFile))
			return True
		else:
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while displaying '{1}' Template help file: '{2}' file doesn't exists!".format(
			self.__class__.__name__, template.name, template.helpFile))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getTemplates(self):
		"""
		This method returns Database Templates.

		:return: Database Templates Collections. ( List )
		"""

		return [template for template in dbCommon.getTemplates(self.__coreDb.dbSession)]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setTemplates(self):
		"""
		This method sets the Templates Model nodes.
		"""

		nodeFlags = attributesFlags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)

		rootNode = umbra.ui.models.DefaultNode(name="InvisibleRootNode")

		collections = dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type")
		for collection in collections:
			softwares = set((software[0] for software in self.__coreDb.dbSession.query(
						dbTypes.DbTemplate.software).filter(dbTypes.DbTemplate.collection == collection.id)))
			if not softwares:
				continue

			collectionNode = dbNodes.CollectionNode(collection,
													name=collection.name,
													parent=rootNode,
													nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
													attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
													release=umbra.ui.models.GraphModelAttribute(name="release",
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)),
													version=umbra.ui.models.GraphModelAttribute(name="version",
															flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)))

			for software in softwares:
				templates = set((template for template in self.__coreDb.dbSession.query(dbTypes.DbTemplate).filter(
				dbTypes.DbTemplate.collection == collection.id).filter(dbTypes.DbTemplate.software == software)))

				if not templates:
					continue

				softwareNode = SoftwareNode(name=software,
											parent=collectionNode,
											nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
											attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
				iconPath = os.path.join(self.__uiResourcesDirectory, "{0}{1}".format(software, self.__uiSoftwareAffixe))
				softwareNode.roles[Qt.DecorationRole] = os.path.exists(iconPath) and iconPath or \
												os.path.join(self.__uiResourcesDirectory, self.__uiUnknownSoftwareImage)

				for template in templates:
					templateNode = dbNodes.TemplateNode(template,
														name="{0} {1}".format(template.renderer, template.title),
														parent=softwareNode,
														nodeFlags=nodeFlags,
														attributesFlags=attributesFlags)

		rootNode.sortChildren(attribute="title")

		self.__model.initializeModel(rootNode)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedNodes(self):
		"""
		This method returns the View selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return self.__view.getSelectedNodes()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedTemplatesNodes(self):
		"""
		This method returns the View selected Templates nodes.

		:return: View selected Templates nodes. ( List )
		"""

		return [node for node in self.getSelectedNodes().keys() if node.family == "Template"]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedTemplates(self):
		"""
		This method gets the View selected Templates.

		:return: View selected Templates. ( List )
		"""

		return [node.dbItem for node in self.getSelectedTemplatesNodes()]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getCollection(self, collection):
		"""
		This method gets Template Collection from given Collection name.

		:param collection: Collection name. ( String )
		:return: Collection. ( DbCollection )
		"""

		return [collection for collection in set(dbCommon.filterCollections(
		self.__coreDb.dbSession, "^{0}$".format(collection), "name")).intersection(
		dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type"))][0]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getUniqueCollectionId(self, path):
		"""
		This method gets an unique Collection id using given path.

		:param path: Template path. ( String )
		:return: Unique id. ( Integer )
		"""

		templatesCollections = dbCommon.filterCollections(self.__coreDb.dbSession, "Templates", "type")
		id = [collection for collection in set(dbCommon.filterCollections(
			self.__coreDb.dbSession, "^{0}$".format(self.__userCollection), "name")).intersection(
			templatesCollections)][0].id
		if self.__defaultCollections[self.__factoryCollection]:
			if path in self.__defaultCollections[self.__factoryCollection]:
				id = [collection for collection in set(dbCommon.filterCollections(
					self.__coreDb.dbSession, "^{0}$".format(self.__factoryCollection), "name")).intersection(
					templatesCollections)][0].id
		return id
