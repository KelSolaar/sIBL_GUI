#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**loggingNotifier.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`LoggingNotifier` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
from manager.component import Component

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LoggingNotifier"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LoggingNotifier(Component):
	"""
	| Defines the :mod:`sibl_gui.components.addons.loggingNotifier.loggingNotifier` Component Interface class.
	| It displays Application logging messages in the Application status bar.
	| The full Application logging history is available through
		the :mod:`sibl_gui.components.addons.loggingWindow.loggingWindow` Component.
	"""

	def __init__(self, name=None):
		"""
		Initializes the class.

		:param name: Component name.
		:type name: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Component.__init__(self, name=name)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None

		self.__memoryHandlerStackDepth = 0

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
	def memoryHandlerStackDepth(self):
		"""
		Property for **self.__memoryHandlerStackDepth** attribute.

		:return: self.__memoryHandlerStackDepth.
		:rtype: int
		"""

		return self.__memoryHandlerStackDepth

	@memoryHandlerStackDepth.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self, value):
		"""
		Setter for **self.__memoryHandlerStackDepth** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "memoryHandlerStackDepth"))

	@memoryHandlerStackDepth.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self):
		"""
		Deleter for **self.__memoryHandlerStackDepth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "memoryHandlerStackDepth"))

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

		self.__engine = engine

		self.activated = True
		return True

	def deactivate(self):
		"""
		Deactivates the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.activated = False
		return True

	def initialize(self):
		"""
		Initializes the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

		# Signals / Slots.
		self.__engine.timer.timeout.connect(self.__statusBar_showLoggingMessages)

		self.initialized = True
		return True

	def uninitialize(self):
		"""
		Uninitializes the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component.".format(self.__class__.__name__))

		# Signals / Slots.
		self.__engine.timer.timeout.disconnect(self.__statusBar_showLoggingMessages)

		self.initialized = False
		return True

	def __statusBar_showLoggingMessages(self):
		"""
		Updates the engine status bar with logging messages.
		"""

		memoryHandlerStackDepth = len(self.__engine.loggingSessionHandlerStream.stream)

		if memoryHandlerStackDepth != self.__memoryHandlerStackDepth:
			for index in range(self.__memoryHandlerStackDepth, memoryHandlerStackDepth):
				self.__engine.statusBar.showMessage(self.__engine.loggingSessionHandlerStream.stream[index])
			self.__memoryHandlerStackDepth = memoryHandlerStackDepth
