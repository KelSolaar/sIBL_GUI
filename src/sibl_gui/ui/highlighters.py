#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**highlighters.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application highlighters classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QSyntaxHighlighter

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import umbra.ui.highlighters
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "IblSetHighlighter", "JavaScriptHighlighter", "MelScriptHighlighter", "MaxScriptHighlighter"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class IblSetHighlighter(umbra.ui.highlighters.AbstractHighlighter):
	"""
	This class is a :class:`umbra.ui.higlighters.AbstractHighlighter` subclass providing syntax highlighting
	for Application Ibl Sets files.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		self.__setFormats()
		self.__setRules()

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setFormats(self):
		"""
		This method sets the highlighting formats.

		:return: Method success. ( Boolean )
		"""

		self.formats = umbra.ui.highlighters.Formats(
						default=umbra.ui.highlighters.getFormat(color=QColor(192, 192, 192)))

		self.formats.section = umbra.ui.highlighters.getFormat(format=self.formats.default,
																color=QColor(205, 170, 105), bold=True)
		self.formats.parameter = umbra.ui.highlighters.getFormat(format=self.formats.default)
		self.formats.storage = umbra.ui.highlighters.getFormat(format=self.formats.default,
																color=QColor(205, 170, 105))
		self.formats.numericConstant = umbra.ui.highlighters.getFormat(format=self.formats.default,
																		color=QColor(205, 105, 75))
		self.formats.numericConstant = umbra.ui.highlighters.getFormat(format=self.formats.default,
																		color=QColor(205, 105, 75))
		self.formats.string = umbra.ui.highlighters.getFormat(format=self.formats.default,
															color=QColor(145, 160, 105),
															italic=True)
		self.formats.lineComment = umbra.ui.highlighters.getFormat(format=self.formats.default,
																	color=QColor(96, 96, 96))

		return True

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.

		:return: Method success. ( Boolean )
		"""

		self.rules = umbra.ui.highlighters.Rules()

		self.rules.section = umbra.ui.highlighters.Rule(pattern=QRegExp(r"^\[.*\]"),
														format=self.formats.section)
		self.rules.parameter = umbra.ui.highlighters.Rule(pattern=QRegExp(r"\w+(?=\s*\=)"),
														format=self.formats.parameter)
		self.rules.storage = umbra.ui.highlighters.Rule(pattern=QRegExp(r"\="),
														format=self.formats.storage)
		self.rules.numericConstant = umbra.ui.highlighters.Rule(pattern=QRegExp(
																r"\b[-+]?[1-9]+\d*|0\b|[-+]?\d*\.?\d+([eE][-+]?\d+)?"),
																format=self.formats.numericConstant)
		self.rules.doubleQuotation = umbra.ui.highlighters.Rule(pattern=QRegExp(r"\"([^\"\\]|\\.)*\""),
																format=self.formats.string)
		self.rules.lineComment = umbra.ui.highlighters.Rule(pattern=QRegExp(r"[;#].*$"), format=self.formats.lineComment)

		return True

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights given text block.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))

class JavaScriptHighlighter(umbra.ui.highlighters.AbstractHighlighter):
	"""
	This class is a :class:`umbra.ui.higlighters.AbstractHighlighter` subclass providing syntax highlighting
	for Application Javascript Templates files.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		self.__setFormats()
		self.__setRules()

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setFormats(self):
		"""
		This method sets the highlighting formats.

		:return: Method success. ( Boolean )
		"""

		self.formats = umbra.ui.highlighters.Formats(default=umbra.ui.highlighters.getFormat(color=QColor(192, 192, 192)))

		return True

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.

		:return: Method success. ( Boolean )
		"""

		self.rules = umbra.ui.highlighters.Rules()

		return True

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights given text block.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))

class MelScriptHighlighter(umbra.ui.highlighters.AbstractHighlighter):
	"""
	This class is a :class:`umbra.ui.higlighters.AbstractHighlighter` subclass providing syntax highlighting
	for Application MelScript Templates files.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		self.__setFormats()
		self.__setRules()

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setFormats(self):
		"""
		This method sets the highlighting formats.

		:return: Method success. ( Boolean )
		"""

		self.formats = umbra.ui.highlighters.Formats(default=umbra.ui.highlighters.getFormat(color=QColor(192, 192, 192)))

		return True

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.

		:return: Method success. ( Boolean )
		"""

		self.rules = umbra.ui.highlighters.Rules()

		return True

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights given text block.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))

class MaxScriptHighlighter(umbra.ui.highlighters.AbstractHighlighter):
	"""
	This class is a :class:`umbra.ui.higlighters.AbstractHighlighter` subclass providing syntax highlighting
	for Application MaxScript Templates files.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		self.__setFormats()
		self.__setRules()

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setFormats(self):
		"""
		This method sets the highlighting formats.

		:return: Method success. ( Boolean )
		"""

		self.formats = umbra.ui.highlighters.Formats(default=umbra.ui.highlighters.getFormat(color=QColor(192, 192, 192)))

		return True

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.

		:return: Method success. ( Boolean )
		"""

		self.rules = umbra.ui.highlighters.Rules()

		return True

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights given text block.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))
