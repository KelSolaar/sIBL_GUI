#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**completers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application completers classes.

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

PYTHON_TOKENS_FILE = os.path.join(os.getcwd(), UiConstants.pythonTokensFile)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class PythonCompleter(QCompleter):
	"""
	This class is a `QCompleter <http://doc.qt.nokia.com/4.7/qcompleter.html>`_ subclass used as a Python completion widget.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Completer parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__words = self.getPythonTokens()

		QCompleter.__init__(self, self.__words, parent)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def words(self):
		"""
		This method is the property for **self.__words** attribute.

		:return: self.__words. ( List / Tuple )
		"""

		return self.__words

	@words.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def words(self, value):
		"""
		This method is the setter method for **self.__words** attribute.

		:param value: Attribute value. ( List / Tuple )
		"""

		if value:
			assert type(value) in (list, tuple), "'{0}' attribute: '{1}' type is not 'list' or 'tuple'!".format("words", value)
		self.__words = value

	@words.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def words(self):
		"""
		This method is the deleter method for **self.__words** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("words"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getPythonTokens(self, splitter="|"):
		"""
		This method is the property for **self.__rules** attribute.

		:param splitters: Splitter character. ( String )
		:return: Python tokens. ( Dictionary )
		"""

		sections = umbra.ui.common.getTokensParser(PYTHON_TOKENS_FILE).sections
		return [token for section in sections["Tokens"].values() for token in section.split(splitter)]
