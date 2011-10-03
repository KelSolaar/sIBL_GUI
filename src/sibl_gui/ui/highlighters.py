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

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import umbra.ui.highlighters
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

__all__ = ["LOGGER", "IblSetHighlighter"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class IblSetHighlighter(umbra.ui.highlighters.Highlighter):
	"""
	This class is a :class:`umbra.ui.higlighters.Highlighter` subclass providing syntax highlighting for Application Ibl Sets files.
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

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __setFormats(self):
		"""
		This method sets the highlighting formats.

		:return: Method success. ( Boolean )
		"""

		self.formats = umbra.ui.highlighters.Formats(default=umbra.ui.highlighters.getFormat(color=QColor(192, 192, 192)))

		self.formats.section = umbra.ui.highlighters.getFormat(format=self.formats.default, bold=True)

		return True

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.

		:return: Method success. ( Boolean )
		"""

		self.rules = umbra.ui.highlighters.Rules()

		self.rules.section = umbra.ui.highlighters.Rule(pattern=QRegExp(r"^\[.*\]"), format=self.formats.section)

		return True

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights provided text block.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))
