#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**imagesCachesOperations.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`ImagesCachesOperations` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtGui import QGridLayout

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import sibl_gui.exceptions
import umbra.exceptions
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ImagesCachesOperations"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Images_Caches_Operations.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ImagesCachesOperations(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.addons.imagesCachesOperations.imagesCachesOperations` Component Interface class.
	| It provides various methods to operate on the images caches.
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

		super(ImagesCachesOperations, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None

		self.__scriptEditor = None
		self.__preferencesManager = None

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
	def scriptEditor(self):
		"""
		This method is the property for **self.__scriptEditor** attribute.

		:return: self.__scriptEditor. ( QWidget )
		"""

		return self.__scriptEditor

	@scriptEditor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self, value):
		"""
		This method is the setter method for **self.__scriptEditor** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "scriptEditor"))

	@scriptEditor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self):
		"""
		This method is the deleter method for **self.__scriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "scriptEditor"))

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

		self.__scriptEditor = self.__engine.componentsManager["factory.scriptEditor"]
		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]

		self.activated = True
		return True

	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.__scriptEditor = None
		self.__preferencesManager = None

		self.activated = False
		return True

	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.Output_Images_Caches_Metrics_pushButton.clicked.connect(
		self.__Output_Images_Caches_Metrics_pushButton__clicked)
		self.Clear_Images_Caches_pushButton.clicked.connect(self.__Clear_Images_Caches_pushButton__clicked)

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.Output_Images_Caches_Metrics_pushButton.clicked.disconnect(
		self.__Output_Images_Caches_Metrics_pushButton__clicked)
		self.Clear_Images_Caches_pushButton.clicked.disconnect(self.__Clear_Images_Caches_pushButton__clicked)

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.Images_Caches_Operations_groupBox)

		return True

	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.Images_Caches_Operations_groupBox.setParent(None)

		return True

	def __Clear_Images_Caches_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Clear_Images_Caches_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.clearImagesCaches()

	def __Output_Images_Caches_Metrics_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Output_Images_Caches_Metrics_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.outputImagesCachesMetrics()
		self.__scriptEditor.restoreDevelopmentLayout()

	def outputImagesCachesMetrics(self):
		"""
		This method logs images caches metrics.

		:return: Method success. ( Boolean )
		"""

		separator = "{0}".format(Constants.loggingSeparators.replace("*", "-"))
		for type, cache in self.__engine.imagesCaches.iteritems():
			LOGGER.info(separator)
			LOGGER.info("{0} | Metrics for '{1}' '{2}' images cache:".format(self.__class__.__name__,
																			Constants.applicationName, type))
			cacheMetrics = cache.getMetrics().content
			LOGGER.info("{0} | \tCached graphics items count: '{1}'".format(self.__class__.__name__, len(cacheMetrics)))
			for path, data in sorted(cache.getMetrics().content.iteritems()):
				LOGGER.info("{0} | \t\t'{1}':".format(self.__class__.__name__, path))
				LOGGER.info("{0} | \t\t\tSize: {1}x{2} px".format(self.__class__.__name__, data.width, data.height))
				LOGGER.info("{0} | \t\t\tBpp: {1} bit".format(self.__class__.__name__, data.bpp / 4))
			LOGGER.info(separator)
		return True

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											sibl_gui.exceptions.CacheOperationError)
	def clearImagesCaches(self):
		"""
		This method clears the images caches.

		:return: Method success. ( Boolean )
		"""

		success = True
		for cache in self.__engine.imagesCaches.itervalues():
			success *= cache.flushContent()

		if success:
			self.__engine.notificationsManager.notify(
			"{0} | Images caches have been successfully cleared!".format(self.__class__.__name__))
			return True
		else:
			raise sibl_gui.exceptions.CacheOperationError(
				"{0} | Exception raised while attempting to clear images caches!".format(
				self.__class__.__name__))
