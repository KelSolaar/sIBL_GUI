#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**templatesOutliner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`TemplatesOutliner` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform
import re
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
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
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import foundations.walkers
import sibl_gui.components.core.database.exceptions
import sibl_gui.components.core.database.operations
import umbra.engine
import umbra.exceptions
import umbra.ui.common
import umbra.ui.nodes
import umbra.ui.widgets.messageBox as messageBox
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.core.database.nodes import CollectionNode
from sibl_gui.components.core.database.nodes import TemplateNode
from sibl_gui.components.core.templatesOutliner.models import TemplatesModel
from sibl_gui.components.core.templatesOutliner.nodes import SoftwareNode
from sibl_gui.components.core.templatesOutliner.views import Templates_QTreeView
from sibl_gui.components.core.database.types import Template
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "TemplatesOutliner"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Templates_Outliner.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TemplatesOutliner(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.core.templatesOutliner.templatesOutliner` Component Interface class.
	| It defines methods for Database Templates management.
	"""

	# Custom signals definitions.
	refreshNodes = pyqtSignal()
	"""
	This signal is emited by the :class:`TemplatesOutliner` class when :obj:`TemplatesOutliner.model` class property
	model Nodes needs to be refreshed. ( pyqtSignal )
	"""

	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param name: Component name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
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

		self.__scriptEditor = None
		self.__database = None

		self.__model = None
		self.__view = None
		self.__headers = OrderedDict([("Templates", "name"),
										("Release", "release"),
										("Software Version", "version")])

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
											Template Manual</span></a>
											</p>
											</p>
											"""

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def uiResourcesDirectory(self):
		"""
		Property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory.
		:rtype: unicode
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		Setter for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		Deleter for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiSoftwareAffixe(self):
		"""
		Property for **self.__uiSoftwareAffixe** attribute.

		:return: self.__uiSoftwareAffixe.
		:rtype: unicode
		"""

		return self.__uiSoftwareAffixe

	@uiSoftwareAffixe.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiSoftwareAffixe(self, value):
		"""
		Setter for **self.__uiSoftwareAffixe** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiSoftwareAffixe"))

	@uiSoftwareAffixe.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiSoftwareAffixe(self):
		"""
		Deleter for **self.__uiSoftwareAffixe** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSoftwareAffixe"))

	@property
	def uiUnknownSoftwareImage(self):
		"""
		Property for **self.__uiUnknownSoftwareImage** attribute.

		:return: self.__uiUnknownSoftwareImage.
		:rtype: unicode
		"""

		return self.__uiUnknownSoftwareImage

	@uiUnknownSoftwareImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiUnknownSoftwareImage(self, value):
		"""
		Setter for **self.__uiUnknownSoftwareImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiUnknownSoftwareImage"))

	@uiUnknownSoftwareImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiUnknownSoftwareImage(self):
		"""
		Deleter for **self.__uiUnknownSoftwareImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiUnknownSoftwareImage"))

	@property
	def dockArea(self):
		"""
		Property for **self.__dockArea** attribute.

		:return: self.__dockArea.
		:rtype: int
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		Setter for **self.__dockArea** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		Deleter for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: QSettings
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settingsSection(self):
		"""
		Property for **self.__settingsSection** attribute.

		:return: self.__settingsSection.
		:rtype: unicode
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		Setter for **self.__settingsSection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		Deleter for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def settingsSeparator(self):
		"""
		Property for **self.__settingsSeparator** attribute.

		:return: self.__settingsSeparator.
		:rtype: unicode
		"""

		return self.__settingsSeparator

	@settingsSeparator.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSeparator(self, value):
		"""
		Setter for **self.__settingsSeparator** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSeparator"))

	@settingsSeparator.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSeparator(self):
		"""
		Deleter for **self.__settingsSeparator** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSeparator"))

	@property
	def scriptEditor(self):
		"""
		Property for **self.__scriptEditor** attribute.

		:return: self.__scriptEditor.
		:rtype: QWidget
		"""

		return self.__scriptEditor

	@scriptEditor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self, value):
		"""
		Setter for **self.__scriptEditor** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "scriptEditor"))

	@scriptEditor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self):
		"""
		Deleter for **self.__scriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "scriptEditor"))

	@property
	def database(self):
		"""
		Property for **self.__database** attribute.

		:return: self.__database.
		:rtype: object
		"""

		return self.__database

	@database.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def database(self, value):
		"""
		Setter for **self.__database** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "database"))

	@database.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def database(self):
		"""
		Deleter for **self.__database** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "database"))

	@property
	def model(self):
		"""
		Property for **self.__model** attribute.

		:return: self.__model.
		:rtype: TemplatesModel
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		Setter for **self.__model** attribute.

		:param value: Attribute value.
		:type value: TemplatesModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		Deleter for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def view(self):
		"""
		Property for **self.__view** attribute.

		:return: self.__view.
		:rtype: QWidget
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		Setter for **self.__view** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		Deleter for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def headers(self):
		"""
		Property for **self.__headers** attribute.

		:return: self.__headers.
		:rtype: OrderedDict
		"""

		return self.__headers

	@headers.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		Setter for **self.__headers** attribute.

		:param value: Attribute value.
		:type value: OrderedDict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

	@headers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def headers(self):
		"""
		Deleter for **self.__headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

	@property
	def extension(self):
		"""
		Property for **self.__extension** attribute.

		:return: self.__extension.
		:rtype: unicode
		"""

		return self.__extension

	@extension.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def extension(self, value):
		"""
		Setter for **self.__extension** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "extension"))

	@extension.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		Deleter for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

	@property
	def defaultCollections(self):
		"""
		Property for **self.__defaultCollections** attribute.

		:return: self.__defaultCollections.
		:rtype: dict
		"""

		return self.__defaultCollections

	@defaultCollections.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultCollections(self, value):
		"""
		Setter for **self.__defaultCollections** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultCollections"))

	@defaultCollections.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultCollections(self):
		"""
		Deleter for **self.__defaultCollections** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultCollections"))

	@property
	def factoryCollection(self):
		"""
		Property for **self.__factoryCollection** attribute.

		:return: self.__factoryCollection.
		:rtype: unicode
		"""

		return self.__factoryCollection

	@factoryCollection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def factoryCollection(self, value):
		"""
		Setter for **self.__factoryCollection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryCollection"))

	@factoryCollection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def factoryCollection(self):
		"""
		Deleter for **self.__factoryCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryCollection"))

	@property
	def userCollection(self):
		"""
		Property for **self.__userCollection** attribute.

		:return: self.__userCollection.
		:rtype: unicode
		"""

		return self.__userCollection

	@userCollection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def userCollection(self, value):
		"""
		Setter for **self.__userCollection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "userCollection"))

	@userCollection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def userCollection(self):
		"""
		Deleter for **self.__userCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "userCollection"))

	@property
	def templatesInformationsDefaultText(self):
		"""
		Property for **self.__templatesInformationsDefaultText** attribute.

		:return: self.__templatesInformationsDefaultText.
		:rtype: unicode
		"""

		return self.__templatesInformationsDefaultText

	@templatesInformationsDefaultText.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesInformationsDefaultText(self, value):
		"""
		Setter for **self.__templatesInformationsDefaultText** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesInformationsDefaultText"))

	@templatesInformationsDefaultText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesInformationsDefaultText(self):
		"""
		Deleter for **self.__templatesInformationsDefaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesInformationsDefaultText"))

	@property
	def treeViewInnerMargins(self):
		"""
		Property for **self.__treeViewInnerMargins** attribute.

		:return: self.__treeViewInnerMargins.
		:rtype: int
		"""

		return self.__treeViewInnerMargins

	@treeViewInnerMargins.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self, value):
		"""
		Setter for **self.__treeViewInnerMargins** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "treeViewInnerMargins"))

	@treeViewInnerMargins.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self):
		"""
		Deleter for **self.__treeViewInnerMargins** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "treeViewInnerMargins"))

	@property
	def templatesInformationsText(self):
		"""
		Property for **self.__templatesInformationsText** attribute.

		:return: self.__templatesInformationsText.
		:rtype: unicode
		"""

		return self.__templatesInformationsText

	@templatesInformationsText.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesInformationsText(self, value):
		"""
		Setter for **self.__templatesInformationsText** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "templatesInformationsText"))

	@templatesInformationsText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def templatesInformationsText(self):
		"""
		Deleter for **self.__templatesInformationsText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "templatesInformationsText"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Engine to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(__file__), self.__uiResourcesDirectory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__scriptEditor = self.__engine.componentsManager["factory.scriptEditor"]
		self.__database = self.__engine.componentsManager["core.database"]

		RuntimeGlobals.templatesFactoryDirectory = umbra.ui.common.getResourcePath(Constants.templatesDirectory)
		RuntimeGlobals.templatesUserDirectory = os.path.join(self.__engine.userApplicationDataDirectory,
															Constants.templatesDirectory)

		self.__defaultCollections = {self.__factoryCollection : RuntimeGlobals.templatesFactoryDirectory,
									self.__userCollection : RuntimeGlobals.templatesUserDirectory}

		self.activated = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		Deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	def initializeUi(self):
		"""
		Initializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__engine.parameters.databaseReadOnly and \
		LOGGER.info("{0} | Model edition deactivated by '{1}' command line parameter value!".format(
		self.__class__.__name__, "databaseReadOnly"))
		self.__model = TemplatesModel(self, horizontalHeaders=self.__headers)
		self.setTemplates()

		self.Templates_Outliner_treeView.setParent(None)
		self.Templates_Outliner_treeView = Templates_QTreeView(self,
															self.__model,
															self.__engine.parameters.databaseReadOnly,
															"No Template to view!")
		self.Templates_Outliner_treeView.setObjectName("Templates_Outliner_treeView")
		self.Templates_Outliner_gridLayout.setContentsMargins(self.__treeViewInnerMargins)
		self.Templates_Outliner_gridLayout.addWidget(self.Templates_Outliner_treeView, 0, 0)
		self.__view = self.Templates_Outliner_treeView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__view_addActions()

		self.Template_Informations_textBrowser.setText(self.__templatesInformationsDefaultText)
		self.Template_Informations_textBrowser.setOpenLinks(False)

		self.Templates_Outliner_splitter.setSizes([16777215, 1])

		# Signals / Slots.
		self.__engine.imagesCaches.QIcon.contentAdded.connect(self.__view.viewport().update)
		self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.Template_Informations_textBrowser.anchorClicked.connect(self.__Template_Informations_textBrowser__anchorClicked)
		self.refreshNodes.connect(self.__model__refreshNodes)
		if not self.__engine.parameters.databaseReadOnly:
			self.__engine.fileSystemEventsManager.fileChanged.connect(self.__engine_fileSystemEventsManager__fileChanged)
			self.__engine.contentDropped.connect(self.__engine__contentDropped)
		else:
			LOGGER.info("{0} | Templates file system events ignored by '{1}' command line parameter value!".format(
			self.__class__.__name__, "databaseReadOnly"))

		self.initializedUi = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		Uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	def onStartup(self):
		"""
		Defines the slot triggered by Framework startup.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if not self.__engine.parameters.databaseReadOnly:
			# Adding default templates.
			self.addDefaultTemplates()

			# Wizard if Templates table is empty.
			if not self.getTemplates():
				if messageBox.messageBox("Question", "Question",
				"The Database has no Templates, would you like to add some?",
				buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
					directory = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self,
																						 "Add Content:",
																						RuntimeGlobals.lastBrowsedPath)))
					if directory:
						if not self.addDirectory(directory):
							raise Exception(
							"{0} | Exception raised while adding '{1}' directory content to the Database!".format(
							self.__class__.__name__, directory))

			# Templates table integrity checking.
			erroneousTemplates = sibl_gui.components.core.database.operations.checkTemplatesTableIntegrity()
			for template, exceptions in erroneousTemplates.iteritems():
				if sibl_gui.components.core.database.exceptions.MissingTemplateFileError in exceptions:
					choice = messageBox.messageBox("Question", "Error",
					"{0} | '{1}' Template file is missing, would you like to update it's location?".format(
					self.__class__.__name__, template.name),
					QMessageBox.Critical, QMessageBox.Yes | QMessageBox.No,
					customButtons=((QString("No To All"), QMessageBox.RejectRole),))

					if choice == 0:
						break

					if choice == QMessageBox.Yes:
						if self.updateTemplateLocationUi(template):
							# TODO: Check updated Template file integrity.
							continue

				for exception in exceptions:
					self.__engine.notificationsManager.warnify(
					"{0} | '{1}' {2}".format(self.__class__.__name__,
									template.name,
									sibl_gui.components.core.database.operations.DATABASE_EXCEPTIONS[exception]))
		else:
			LOGGER.info("{0} | Database default Templates wizard and Templates integrity checking method deactivated\
by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		activeCollectionsIdentities = foundations.strings.toString(self.__settings.getKey(
		self.__settingsSection, "activeCollections").toString())
		LOGGER.debug("> Stored '{0}' active Collections selection: '{1}'.".format(self.__class__.__name__,
																				activeCollectionsIdentities))
		self.__view.modelSelection["Collections"] = activeCollectionsIdentities and [int(identity)
																		for identity in activeCollectionsIdentities.split(
																		self.__settingsSeparator)] or []

		activeSoftwares = foundations.strings.toString(
		self.__settings.getKey(self.__settingsSection, "activeSoftwares").toString())
		LOGGER.debug("> Stored '{0}' active softwares selection: '{1}'.".format(self.__class__.__name__, activeSoftwares))
		self.__view.modelSelection["Softwares"] = activeSoftwares and activeSoftwares.split(self.__settingsSeparator) or []

		activeTemplatesIdentities = foundations.strings.toString(
		self.__settings.getKey(self.__settingsSection, "activeTemplates").toString())
		LOGGER.debug("> '{0}' View stored selected Templates identities '{1}'.".format(self.__class__.__name__,
																						activeTemplatesIdentities))
		self.__view.modelSelection["Templates"] = activeTemplatesIdentities and [int(identity)
																		for identity in activeTemplatesIdentities.split(
																		self.__settingsSeparator)] or []

		self.__view.restoreModelSelection()
		return True

	def onClose(self):
		"""
		Defines the slot triggered by Framework close.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		self.__view.storeModelSelection()
		self.__settings.setKey(self.__settingsSection,
								"activeTemplates",
								self.__settingsSeparator.join(foundations.strings.toString(identity)
															for identity in self.__view.modelSelection["Templates"]))
		self.__settings.setKey(self.__settingsSection,
								"activeCollections",
								self.__settingsSeparator.join(foundations.strings.toString(identity)
															for identity in self.__view.modelSelection["Collections"]))
		self.__settings.setKey(self.__settingsSection,
								"activeSoftwares",
								self.__settingsSeparator.join(foundations.strings.toString(name)
															for name in self.__view.modelSelection["Softwares"]))
		return True

	def __model__refreshNodes(self):
		"""
		Defines the slot triggered by the Model when nodes need refresh.
		"""

		self.setTemplates()

	def __view_addActions(self):
		"""
		Sets the View actions.
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
			LOGGER.info("{0} | Templates Database alteration capabilities deactivated\
by '{1}' command line parameter value!".format(self.__class__.__name__, "databaseReadOnly"))

		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|core.templatesOutliner|Display Help File(s) ...",
		slot=self.__view_displayHelpFilesAction__triggered))

		separatorAction = QAction(self.__view)
		separatorAction.setSeparator(True)
		self.__view.addAction(separatorAction)

	def __view_addTemplateAction__triggered(self, checked):
		"""
		Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templatesOutliner|Add Template ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.addTemplateUi()

	def __view_removeTemplatesAction__triggered(self, checked):
		"""
		Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templatesOutliner|Remove Template(s) ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.removeTemplatesUi()

	def __view_importDefaultTemplatesAction__triggered(self, checked):
		"""
		Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templatesOutliner|Import Default Templates'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.importDefaultTemplatesUi()

	def __view_displayHelpFilesAction__triggered(self, checked):
		"""
		Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templatesOutliner|Display Help File(s) ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.displayHelpFilesUi()

	def __view_filterTemplatesVersionsAction__triggered(self, checked):
		"""
		Defines the slot triggered by \*\*'Actions|Umbra|Components|core.templatesOutliner|Filter Templates Versions'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.filterTemplatesVersionsUi()

	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		Sets the **Template_Informations_textEdit** Widget.

		:param selectedItems: Selected items.
		:type selectedItems: QItemSelection
		:param deselectedItems: Deselected items.
		:type deselectedItems: QItemSelection
		"""

		LOGGER.debug("> Initializing '{0}' Widget.".format("Template_Informations_textEdit"))

		selectedTemplates = self.getSelectedTemplates()
		content = []

		if selectedTemplates:
			for template in selectedTemplates:
				helpFile = template.helpFile or umbra.ui.common.getResourcePath(UiConstants.invalidLinkHtmlFile)
				content.append(self.__templatesInformationsText.format(template.title,
																	template.date,
																	template.author,
																	template.email,
																	template.url,
																	template.outputScript,
																	template.comment,
																	QUrl.fromLocalFile(helpFile).toString()))
		else:
			content.append(self.__templatesInformationsDefaultText)

		separator = "" if len(content) == 1 else "<p><center>* * *<center/></p>"

		self.Template_Informations_textBrowser.setText(separator.join(content))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError)
	@umbra.engine.showProcessing("Retrieving Templates ...")
	def __engine__contentDropped(self, event):
		"""
		Defines the slot triggered when content is dropped into the engine.
		
		:param event: Event.
		:type event: QEvent
		"""

		if not event.mimeData().hasUrls():
			return

		LOGGER.debug("> Drag event urls list: '{0}'!".format(event.mimeData().urls()))

		if not self.__engine.parameters.databaseReadOnly:
			for url in event.mimeData().urls():
				path = foundations.strings.toString(url.path())
				LOGGER.debug("> Handling dropped '{0}' file.".format(path))
				path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
				re.search(r"^\/[A-Z]:", path) and path[1:] or path
				if re.search(r"\.{0}$".format(self.__extension), path):
					name = foundations.strings.getSplitextBasename(path)
					choice = messageBox.messageBox("Question", "Question",
					"'{0}' Template file has been dropped, would you like to 'Add' it to the Database or \
'Edit' it in the Script Editor?".format(name),
					buttons=QMessageBox.Cancel,
					customButtons=((QString("Add"), QMessageBox.AcceptRole), (QString("Edit"), QMessageBox.AcceptRole)))
					if choice == 0:
						self.addTemplate(name, path)
					elif choice == 1:
						self.__scriptEditor.loadFile(path) and self.__scriptEditor.restoreDevelopmentLayout()
				else:
					if not os.path.isdir(path):
						return

					if not list(foundations.walkers.filesWalker(path, ("\.{0}$".format(self.__extension),), ("\._",))):
						return

					if messageBox.messageBox("Question", "Question",
					"Would you like to add '{0}' directory Template(s) file(s) to the Database?".format(path),
					buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
						self.addDirectory(path)
				self.__engine.processEvents()
		else:
			raise foundations.exceptions.UserError(
			"{0} | Cannot perform action, Database has been set read only!".format(self.__class__.__name__))

	def __engine_fileSystemEventsManager__fileChanged(self, file):
		"""
		Defines the slot triggered by the **fileSystemEventsManager** when a file is changed.
		
		:param file: File changed.
		:type file: unicode
		"""

		template = foundations.common.getFirstItem(filter(lambda x: x.path == file, self.getTemplates()))
		if not template:
			return

		if sibl_gui.components.core.database.operations.updateTemplateContent(template):
			self.__engine.notificationsManager.notify(
			"{0} | '{1}' Template file has been reparsed and associated database object updated!".format(
			self.__class__.__name__, template.title))
			self.refreshNodes.emit()

	def __Template_Informations_textBrowser__anchorClicked(self, url):
		"""
		Defines the slot triggered by **Template_Informations_textBrowser** Widget when a link is clicked.

		:param url: Url to explore.
		:type url: QUrl
		"""

		QDesktopServices.openUrl(url)

	def __getCandidateCollectionId(self, path=None):
		"""
		Returns a Collection id.

		:param path: Template path.
		:type path: unicode
		:return: Collection id.
		:rtype: int
		"""

		collection = self.getCollectionByName(self.__userCollection)
		identity = collection and collection.id or None

		factoryCollectionPath = self.__defaultCollections[self.__factoryCollection]
		if path and factoryCollectionPath:
			if os.path.normpath(factoryCollectionPath) in os.path.normpath(path):
				collection = self.getCollectionByName(self.__factoryCollection)
				identity = collection and collection.id or None
		return identity

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.showProcessing("Adding Template ...")
	def addTemplateUi(self):
		"""
		Adds an user defined Template to the Database.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		path = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																		"Add Template:",
																		RuntimeGlobals.lastBrowsedPath,
																		"sIBLT files (*.{0})".format(self.__extension))))
		if not path:
			return

		if not self.templateExists(path):
			LOGGER.debug("> Chosen Template path: '{0}'.".format(path))
			if self.addTemplate(foundations.strings.getSplitextBasename(path), path):
				return True
			else:
				raise Exception("{0} | Exception raised while adding '{1}' Template to the Database!".format(
				self.__class__.__name__, path))
		else:
			self.__engine.notificationsManager.warnify(
			"{0} | '{1}' Template already exists in Database!".format(self.__class__.__name__, path))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.encapsulateProcessing
	def removeTemplatesUi(self):
		"""
		Removes user selected Templates from the Database.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		selectedNodes = self.getSelectedNodes()

		selectedCollections = []
		selectedSoftwares = []
		for item in selectedNodes:
			if item.family == "Collection":
				selectedCollections.append(item.name)
			elif item.family == "Software":
				selectedSoftwares.append(item.name)
		selectedCollections and self.__engine.notificationsManager.warnify(
		"{0} | '{1}' Collection(s) cannot be removed!".format(self.__class__.__name__, ", ".join(selectedCollections)))
		selectedSoftwares and self.__engine.notificationsManager.warnify(
		"{0} | '{1}' software(s) cannot be removed!".format(self.__class__.__name__, ", ".join(selectedSoftwares)))

		selectedTemplates = self.getSelectedTemplates()
		if not selectedTemplates:
			return False

		if messageBox.messageBox("Question", "Question",
		"Are you sure you want to remove '{0}' Template(s)?".format(
		", ".join([foundations.strings.toString(template.name) for template in selectedTemplates])),
		buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.startProcessing("Removing Templates ...", len(selectedTemplates))
			success = True
			for template in selectedTemplates:
				success *= umbra.ui.common.signalsBlocker(self, self.removeTemplate, template) or False
				self.__engine.stepProcessing()
			self.__engine.stopProcessing()

			self.refreshNodes.emit()

			if success:
				return True
			else:
				raise Exception("{0} | Exception raised while removing '{1}' Templates from the Database!".format(
				self.__class__.__name__, ", ". join((template.name for template in selectedTemplates))))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def updateTemplateLocationUi(self, template):
		"""
		Updates given Template location.

		:param template: Template to update.
		:type template: Template
		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		file = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																"Updating '{0}' Template Location:".format(template.name),
																RuntimeGlobals.lastBrowsedPath,
																"Template files (*{0})".format(self.__extension))))
		if not file:
			return False

		LOGGER.info("{0} | Updating '{1}' Template with new location '{2}'!".format(self.__class__.__name__,
																					template.name, file))
		if sibl_gui.components.core.database.operations.updateTemplateLocation(template, file):
			self.refreshNodes.emit()
			return True
		else:
			raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
			"{0} | Exception raised while updating '{1}' Template location!".format(self.__class__.__name__, template.name))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.showProcessing("Importing Default Templates ...")
	def importDefaultTemplatesUi(self):
		"""
		Imports default Templates into the Database.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		if self.addDefaultTemplates(forceImport=True):
			return True
		else:
			raise Exception("{0} | Exception raised while importing default Templates into the Database!".format(
			self.__class__.__name__))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.encapsulateProcessing
	def displayHelpFilesUi(self):
		"""
		Displays user selected Templates help files.

		:return: Method success.
		:rtype: bool
		"""

		selectedTemplates = self.getSelectedTemplates()
		if not selectedTemplates:
			return False

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

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.encapsulateProcessing
	def filterTemplatesVersionsUi(self):
		"""
		Filters Templates by versions.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		templates = sibl_gui.components.core.database.operations.getTemplates()
		self.__engine.startProcessing("Filtering Templates ...", len(templates.all()))
		success = True
		for template in templates:
			matchingTemplates = sibl_gui.components.core.database.operations.filterTemplates(
								 "^{0}$".format(template.name), "name")
			if len(matchingTemplates) != 1:
				for identity in sorted([(databaseTemplate.id, databaseTemplate.release) for databaseTemplate in matchingTemplates],
								reverse=True,
								key=lambda x:(foundations.strings.getVersionRank(x[1])))[1:]:
					success *= 	sibl_gui.components.core.database.operations.removeTemplate(
								foundations.common.getFirstItem(identity)) or False
				self.refreshNodes.emit()
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while filtering Templates by versions!".format(self.__class__.__name__))

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError,
											sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def addTemplate(self, name, path, collectionId=None):
		"""
		Adds a Template to the Database.

		:param name: Template set name.
		:type name: unicode
		:param path: Template set path.
		:type path: unicode
		:param collectionId: Target Collection id.
		:type collectionId: int
		:return: Method success.
		:rtype: bool
		"""

		if not sibl_gui.components.core.database.operations.filterTemplates("^{0}$".format(re.escape(path)), "path"):
			LOGGER.info("{0} | Adding '{1}' Template to the Database!".format(self.__class__.__name__, name))
			if sibl_gui.components.core.database.operations.addTemplate(
			name, path, collectionId or self.__getCandidateCollectionId(path)):
				self.refreshNodes.emit()
				return True
			else:
				raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
				"{0} | Exception raised while adding '{1}' Template to the Database!".format(self.__class__.__name__, name))
		else:
			raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Template already exists in Database!".format(self.__class__.__name__, name))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	@umbra.engine.encapsulateProcessing
	def addDirectory(self, directory, collectionId=None):
		"""
		Adds given directory Templates to the Database.

		:param directory: Templates directory.
		:type directory: unicode
		:param collectionId: Collection id.
		:type collectionId: int
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing directory '{0}' filesWalker.".format(directory))

		files = list(foundations.walkers.filesWalker(directory, ("\.{0}$".format(self.__extension),), ("\._",)))

		self.__engine.startProcessing("Adding Directory Templates ...", len(files))
		success = True
		for path in files:
			if not self.templateExists(path):
				success *= umbra.ui.common.signalsBlocker(self,
														self.addTemplate,
														foundations.strings.getSplitextBasename(path),
														path,
														collectionId) or False
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.refreshNodes.emit()

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while adding '{1}' directory content to the Database!".format(
			self.__class__.__name__, directory))

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler, Exception)
	def addDefaultTemplates(self, forceImport=False):
		"""
		Adds default Templates Collections / Templates to the Database.

		:param forceImport: Force Templates import.
		:type forceImport: bool
		:return: Method success.
		:rtype: bool
		"""

		if not forceImport and self.getTemplates():
			return False

		LOGGER.debug("> Adding default Templates to the Database.")

		success = True
		for collection, path in ((collection, path) for (collection, path) in self.__defaultCollections.iteritems() if path):
			if not foundations.common.pathExists(path):
				continue

			if not set(sibl_gui.components.core.database.operations.filterCollections(
									"^{0}$".format(collection), "name")).intersection(
									sibl_gui.components.core.database.operations.filterCollections("Templates", "type")):
				LOGGER.info("{0} | Adding '{1}' Collection to the Database!".format(self.__class__.__name__, collection))
				sibl_gui.components.core.database.operations.addCollection(
				collection, "Templates", "Template {0} Collection".format(collection))
			success *= self.addDirectory(path, self.getCollectionByName(collection).id)

		if success:
			return True
		else:
			raise Exception("{0} | Exception raised while adding default Templates to the Database!".format(
			self.__class__.__name__))

	@foundations.exceptions.handleExceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
	def removeTemplate(self, template):
		"""
		Removes given Template from the Database.

		:param templates: Template to remove.
		:type templates: list
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.info("{0} | Removing '{1}' Template from the Database!".format(self.__class__.__name__, template.name))
		if sibl_gui.components.core.database.operations.removeTemplate(foundations.strings.toString(template.id)):
			self.refreshNodes.emit()
			return True
		else:
			raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
			"{0} | Exception raised while removing '{1}' Template from the Database!".format(self.__class__.__name__,
																							template.name))

	def templateExists(self, path):
		"""
		Returns if given Template path exists in the Database.

		:param name: Template path.
		:type name: unicode
		:return: Template exists.
		:rtype: bool
		"""

		return sibl_gui.components.core.database.operations.templateExists(path)

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def displayHelpFile(self, template):
		"""
		Displays given Templates help file.

		:param template: Template to display help file.
		:type template: Template
		:return: Method success.
		:rtype: bool
		"""

		helpFile = template.helpFile or umbra.ui.common.getResourcePath(UiConstants.invalidLinkHtmlFile)
		if foundations.common.pathExists(helpFile):
			LOGGER.info("{0} | Opening '{1}' Template help file: '{2}'.".format(self.__class__.__name__,
																				template.name,
																				helpFile))
			QDesktopServices.openUrl(QUrl.fromLocalFile(helpFile))
			return True
		else:
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while displaying '{1}' Template help file: '{2}' file doesn't exists!".format(
			self.__class__.__name__, template.name, helpFile))

	def getCollections(self):
		"""
		Returns Database Templates Collections.

		:return: Database Templates Collections.
		:rtype: list
		"""

		return sibl_gui.components.core.database.operations.getCollectionsByType("Templates")

	def filterCollections(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		Filters the Database Templates Collections on given attribute using given pattern.
		
		:param pattern: Filter pattern.
		:type pattern: unicode
		:param attribute: Attribute to filter on.
		:type attribute: unicode
		:param flags: Regex filtering flags.
		:type flags: int

		:return: Filtered Database Templates Collections.
		:rtype: list
		"""

		try:
			pattern = re.compile(pattern, flags)
		except Exception:
			return list()

		return sibl_gui.components.core.database.operations.filterTemplatesCollections(
		"{0}".format(foundations.strings.toString(pattern.pattern)), attribute, flags)

	def getTemplates(self):
		"""
		Returns Database Templates.

		:return: Database Templates.
		:rtype: list
		"""

		return [template for template in sibl_gui.components.core.database.operations.getTemplates()]

	def filterTemplates(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		Filters the Database Templates on given attribute using given pattern.
		
		:param pattern: Filter pattern.
		:type pattern: unicode
		:param attribute: Attribute to filter on.
		:type attribute: unicode
		:param flags: Regex filtering flags.
		:type flags: int

		:return: Filtered Database Templates.
		:rtype: list
		"""

		try:
			pattern = re.compile(pattern, flags)
		except Exception:
			return list()

		return list(set(self.getTemplates()).intersection(
		sibl_gui.components.core.database.operations.filterTemplates(
		"{0}".format(foundations.strings.toString(pattern.pattern)), attribute, flags)))

	def listTemplates(self):
		"""
		Lists Database Templates names.

		:return: Database Templates names.
		:rtype: list
		"""

		return [template.title for template in self.getTemplates()]

	def setTemplates(self):
		"""
		Sets the Templates Model nodes.
		"""

		nodeFlags = attributesFlags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)

		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")

		collections = sibl_gui.components.core.database.operations.filterCollections("Templates", "type")
		for collection in collections:
			softwares = set((foundations.common.getFirstItem(software) for software in \
						sibl_gui.components.core.database.operations.query(Template.software).filter(
						Template.collection == collection.id)))
			if not softwares:
				continue

			collectionNode = CollectionNode(collection,
											name=collection.name,
											parent=rootNode,
											nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
											attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
			collectionNode["release"] = sibl_gui.ui.nodes.GraphModelAttribute(name="release",
																flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
			collectionNode["version"] = sibl_gui.ui.nodes.GraphModelAttribute(name="version",
																flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
			for software in softwares:
				templates = set((template for template in sibl_gui.components.core.database.operations.query(
							Template).filter(Template.collection == collection.id).filter(
							Template.software == software)))

				if not templates:
					continue

				softwareNode = SoftwareNode(name=software,
											parent=collectionNode,
											nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
											attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
				iconPath = os.path.join(self.__uiResourcesDirectory, "{0}{1}".format(software, self.__uiSoftwareAffixe))
				softwareNode.roles[Qt.DecorationRole] = iconPath if foundations.common.pathExists(iconPath) else \
												os.path.join(self.__uiResourcesDirectory, self.__uiUnknownSoftwareImage)

				for template in templates:
					templateNode = TemplateNode(template,
												name=foundations.strings.removeStrip(template.title, template.software),
												parent=softwareNode,
												nodeFlags=nodeFlags,
												attributesFlags=attributesFlags)

					path = foundations.strings.toString(template.path)
					if not foundations.common.pathExists(path):
						continue

					not self.__engine.fileSystemEventsManager.isPathRegistered(path) and \
					self.__engine.fileSystemEventsManager.registerPath(path, modifiedTime=float(template.osStats.split(",")[8]))

		rootNode.sortChildren(attribute="title")

		self.__model.initializeModel(rootNode)
		return True

	def getTemplateByName(self, name):
		"""
		Returns Database Template with given name.

		:param name: Template name.
		:type name: unicode
		:return: Database Template.
		:rtype: Template
		
		:note: The filtering is actually performed on 'title' attributes instead of 'name' attributes.
		"""

		templates = self.filterTemplates(r"^{0}$".format(name), "title")
		return foundations.common.getFirstItem(templates)

	def getCollectionByName(self, name):
		"""
		Returns Templates Collection from given Collection name.

		:param collection: Collection name.
		:type collection: unicode
		:return: Collection.
		:rtype: Collection
		"""

		collections = self.filterCollections(r"^{0}$".format(name), "name")
		return foundations.common.getFirstItem(collections)

	def getCollectionId(self, collection):
		"""
		Returns given Collection id.

		:param collection: Collection to get the id from.
		:type collection: unicode
		:return: Provided Collection id.
		:rtype: int
		"""

		children = self.__model.findChildren(r"^{0}$".format(collection))
		child = foundations.common.getFirstItem(children)
		return child and child.databaseItem.id or None

	def getSelectedNodes(self):
		"""
		Returns the View selected nodes.

		:return: View selected nodes.
		:rtype: dict
		"""

		return self.__view.getSelectedNodes()

	def getSelectedTemplatesNodes(self):
		"""
		Returns the View selected Templates nodes.

		:return: View selected Templates nodes.
		:rtype: list
		"""

		return [node for node in self.getSelectedNodes() if node.family == "Template"]

	def getSelectedTemplates(self):
		"""
		Returns the View selected Templates.

		:return: View selected Templates.
		:rtype: list
		"""

		return [node.databaseItem for node in self.getSelectedTemplatesNodes()]
