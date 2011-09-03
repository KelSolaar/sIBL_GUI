#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preferences.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| This module is the main **Umbra** package module.
	| It defines various classes, methods and definitions to run, maintain and exit the Application.
	| The main Application object is the :class:`Umbra` class.

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
import umbra.ui.common
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants

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
class Preferences():
	"""
	| This class provides methods to manipulate Application preferences / settings.
	| Those are stored and retrieved using a `QSettings <http://doc.qt.nokia.com/4.7/qsettings.html>`_ class.
	"""

	@core.executionTrace
	def __init__(self, preferencesFile=None):
		"""
		This method initializes the class.

		:param preferencesFile: Current preferences file path. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__preferencesFile = None
		self.__preferencesFile = preferencesFile

		self.__settings = QSettings(self.__preferencesFile, QSettings.IniFormat)

		# --- Initializing preferences. ---
		self.__getDefaultSettings()
		self.__getDefaultLayoutsSettings()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def preferencesFile(self):
		"""
		This method is the property for **self.__preferencesFile** attribute.

		:return: self.__preferencesFile. ( String )
		"""

		return self.__preferencesFile

	@preferencesFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def preferencesFile(self, value):
		"""
		This method is the setter method for **self.__preferencesFile** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("preferencesFile", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("preferencesFile", value)
		self.__preferencesFile = value

	@preferencesFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesFile(self):
		"""
		This method is the deleter method for **self.__preferencesFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("preferencesFile"))

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
	def defaultSettings(self):
		"""
		This method is the property for **self.__defaultSettings** attribute.

		:return: self.__defaultSettings. ( QSettings )
		"""

		return self.__defaultSettings

	@defaultSettings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultSettings(self, value):
		"""
		This method is the setter method for **self.__defaultSettings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultSettings"))

	@defaultSettings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultSettings(self):
		"""
		This method is the deleter method for **self.__defaultSettings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultSettings"))

	@property
	def defaultLayoutsSettings(self):
		"""
		This method is the property for **self.__defaultLayoutsSettings** attribute.

		:return: self.__defaultLayoutsSettings. ( QSettings )
		"""

		return self.__defaultLayoutsSettings

	@defaultLayoutsSettings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLayoutsSettings(self, value):
		"""
		This method is the setter method for **self.__defaultLayoutsSettings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultLayoutsSettings"))

	@defaultLayoutsSettings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLayoutsSettings(self):
		"""
		This method is the deleter method for **self.__defaultLayoutsSettings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultLayoutsSettings"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def setKey(self, section, key, value):
		"""
		This method stores provided key in settings file.

		:param section: Current section to save the key into. ( String )
		:param key: Current key to save. ( String )
		:param value: Current key value to save. ( Object )
		"""

		LOGGER.debug("> Saving '{0}' in '{1}' section with value: '{2}' in settings file.".format(key, section, value))

		self.__settings.beginGroup(section)
		self.__settings.setValue(key , QVariant(value))
		self.__settings.endGroup()

	@core.executionTrace
	def getKey(self, section, key):
		"""
		This method gets key value from settings file.

		:param section: Current section to retrieve key from. ( String )
		:param key: Current key to retrieve. ( String )
		:return: Current key value. ( Object )
		"""

		LOGGER.debug("> Retrieving '{0}' in '{1}' section.".format(key, section))

		self.__settings.beginGroup(section)
		value = self.__settings.value(key)
		LOGGER.debug("> Key value: '{0}'.".format(value))
		self.__settings.endGroup()

		return value

	@core.executionTrace
	def __getDefaultSettings(self):
		"""
		This method gets the default settings.
		"""

		LOGGER.debug("> Accessing '{0}' default settings file!".format(UiConstants.settingsFile))
		self.__defaultSettings = QSettings(umbra.ui.common.getResourcePath(UiConstants.settingsFile), QSettings.IniFormat)

	@core.executionTrace
	def __getDefaultLayoutsSettings(self):
		"""
		This method gets the default layouts settings.
		"""

		LOGGER.debug("> Accessing '{0}' default layouts settings file!".format(UiConstants.layoutsFile))
		self.__defaultLayoutsSettings = QSettings(umbra.ui.common.getResourcePath(UiConstants.layoutsFile), QSettings.IniFormat)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setDefaultPreferences(self):
		"""
		This method defines the default settings file content.
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing default settings!")

		for key in self.__defaultSettings.allKeys():
			self.__settings.setValue(key, self.__defaultSettings.value(key))

		self.setDefaultLayouts()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setDefaultLayouts(self):
		"""
		This method sets the default layouts in the preferences file.

		:return: Method success. ( Boolean )
		"""

		for key in self.__defaultLayoutsSettings.allKeys():
			self.__settings.setValue(key, self.__defaultLayoutsSettings.value(key))
		return True
