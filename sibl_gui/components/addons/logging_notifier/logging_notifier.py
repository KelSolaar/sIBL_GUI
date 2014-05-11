#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**logging_notifier.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`LoggingNotifier` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import foundations.exceptions
import foundations.verbose
from manager.component import Component

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LoggingNotifier"]

LOGGER = foundations.verbose.install_logger()

class LoggingNotifier(Component):
    """
    | Defines the :mod:`sibl_gui.components.addons.logging_notifier.logging_notifier` Component Interface class.
    | It displays Application logging messages in the Application status bar.
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

        self.__memory_handler_stack_depth = 0

    @property
    def engine(self):
        """
        Property for **self.__engine** attribute.

        :return: self.__engine.
        :rtype: QObject
        """

        return self.__engine

    @engine.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def engine(self, value):
        """
        Setter for **self.__engine** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

    @engine.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def engine(self):
        """
        Deleter for **self.__engine** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

    @property
    def memory_handler_stack_depth(self):
        """
        Property for **self.__memory_handler_stack_depth** attribute.

        :return: self.__memory_handler_stack_depth.
        :rtype: int
        """

        return self.__memory_handler_stack_depth

    @memory_handler_stack_depth.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def memory_handler_stack_depth(self, value):
        """
        Setter for **self.__memory_handler_stack_depth** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "memory_handler_stack_depth"))

    @memory_handler_stack_depth.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def memory_handler_stack_depth(self):
        """
        Deleter for **self.__memory_handler_stack_depth** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "memory_handler_stack_depth"))

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
        self.__engine.timer.timeout.connect(self.__statusBar_show_logging_messages)

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
        self.__engine.timer.timeout.disconnect(self.__statusBar_show_logging_messages)

        self.initialized = False
        return True

    def __statusBar_show_logging_messages(self):
        """
        Updates the engine status bar with logging messages.
        """

        memory_handler_stack_depth = len(self.__engine.logging_session_handler_stream.stream)

        if memory_handler_stack_depth != self.__memory_handler_stack_depth:
            for index in range(self.__memory_handler_stack_depth, memory_handler_stack_depth):
                self.__engine.statusBar.showMessage(self.__engine.logging_session_handler_stream.stream[index])
            self.__memory_handler_stack_depth = memory_handler_stack_depth
