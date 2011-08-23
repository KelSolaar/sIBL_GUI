#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**highlighters.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`PythonHighligher` class.

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
import foundations.exceptions
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
class Formats(core.Structure):
	"""
	This class represents a storage object for highlighters formats. 
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: name. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class PythonHighlighter(QSyntaxHighlighter):
	"""
	This class is a `QSyntaxHighlighter <http://doc.qt.nokia.com/4.7/qsyntaxhighlighter.html>`_ subclass providing syntax highlighting for Python documents.
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Syntax highlighter parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		self.__formats = None
		self.__rules = None
		self.__keywords = None
		self.__multiLineStringStart = None
		self.__multiLineStringEnd = None

		self.__setKeywords()
		self.__setFormats()
		self.__setRules()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def formats(self):
		"""
		This method is the property for **self.__formats** attribute.

		:return: self.__formats. ( Formats )
		"""

		return self.__formats

	@formats.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def formats(self, value):
		"""
		This method is the setter method for **self.__formats** attribute.

		:param value: Attribute value. ( Formats )
		"""

		if value:
			assert type(value) is Formats, "'{0}' attribute: '{1}' type is not 'Formats'!".format("formats", value)
		self.__formats = value

	@formats.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def formats(self):
		"""
		This method is the deleter method for **self.__formats** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("formats"))

	@property
	def rules(self):
		"""
		This method is the property for **self.__rules** attribute.

		:return: self.__rules. ( Tuple / List )
		"""

		return self.__rules

	@rules.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def rules(self, value):
		"""
		This method is the setter method for **self.__rules** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format("rules", value)
		self.__rules = value

	@rules.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rules(self):
		"""
		This method is the deleter method for **self.__rules** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("rules"))

	@property
	def keywords(self):
		"""
		This method is the property for **self.__keywords** attribute.

		:return: self.__keywords. ( Tuple / List )
		"""

		return self.__keywords

	@keywords.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def keywords(self, value):
		"""
		This method is the setter method for **self.__keywords** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format("keywords", value)
		self.__keywords = value

	@keywords.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def keywords(self):
		"""
		This method is the deleter method for **self.__keywords** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("keywords"))

	@property
	def multiLineStringStart(self):
		"""
		This method is the property for **self.__multiLineStringStart** attribute.

		:return: self.__multiLineStringStart. ( QRegExp )
		"""

		return self.__multiLineStringStart

	@multiLineStringStart.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def multiLineStringStart(self, value):
		"""
		This method is the setter method for **self.__multiLineStringStart** attribute.

		:param value: Attribute value. ( QRegExp )
		"""

		if value:
			assert type(value) is QRegExp, "'{0}' attribute: '{1}' type is not 'QRegExp'!".format("multiLineStringStart", value)
		self.__multiLineStringStart = value

	@multiLineStringStart.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def multiLineStringStart(self):
		"""
		This method is the deleter method for **self.__multiLineStringStart** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("multiLineStringStart"))

	@property
	def multiLineStringEnd(self):
		"""
		This method is the property for **self.__multiLineStringEnd** attribute.

		:return: self.__multiLineStringEnd. ( QRegExp )
		"""

		return self.__multiLineStringEnd

	@multiLineStringEnd.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def multiLineStringEnd(self, value):
		"""
		This method is the setter method for **self.__multiLineStringEnd** attribute.

		:param value: Attribute value. ( QRegExp )
		"""

		if value:
			assert type(value) is QRegExp, "'{0}' attribute: '{1}' type is not 'QRegExp'!".format("multiLineStringEnd", value)
		self.__multiLineStringEnd = value

	@multiLineStringEnd.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def multiLineStringEnd(self):
		"""
		This method is the deleter method for **self.__multiLineStringEnd** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("multiLineStringEnd"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __setKeywords(self):
		"""
		This method sets the highlighting keywords.
		"""

		self.__keywords = ("and", "as", "assert", "break", "class", "continue", "def", "del", "elif", "else", "except", "exec", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "not", "or", "pass", "print", "raise", "return", "try", "while", "with", "yield")

	@core.executionTrace
	def __setFormats(self):
		"""
		This method sets the highlighting formats.
		"""

		self.__formats = Formats(defaultFormat=QTextCharFormat())
		self.__formats.defaultFormat.setForeground(QColor(192, 192, 192))

		self.__formats.nullFormat = QTextCharFormat(self.__formats.defaultFormat)
		self.__formats.nullFormat.setFontPointSize(self.__formats.defaultFormat.font().pointSize() / 4.0)

		self.__formats.keywordFormat = QTextCharFormat(self.__formats.defaultFormat)
		self.__formats.keywordFormat.setForeground(QBrush(QColor(160, 96, 64)))
		self.__formats.keywordFormat.setFontWeight(QFont.Bold)

		self.__formats.objectFormat = QTextCharFormat(self.__formats.defaultFormat)

		self.__formats.specialObjectFormat = QTextCharFormat(self.__formats.defaultFormat)
		self.__formats.specialObjectFormat.setFontWeight(QFont.Bold)

		self.__formats.selfFormat = QTextCharFormat(self.__formats.defaultFormat)
		self.__formats.selfFormat.setForeground(Qt.red)
		self.__formats.selfFormat.setFontItalic(True)

		self.__formats.singleLineCommentFormat = QTextCharFormat(self.__formats.defaultFormat)
		self.__formats.singleLineCommentFormat.setForeground(QColor(128, 128, 128))

		self.__formats.multiLineStringFormat = QTextCharFormat(self.__formats.defaultFormat)
		self.__formats.multiLineStringFormat.setBackground(QBrush(QColor(127, 127, 255)))

		self.__formats.doubleQuotationFormat = QTextCharFormat(self.__formats.defaultFormat)
		self.__formats.doubleQuotationFormat.setForeground(Qt.blue)
		self.__formats.singleQuotationFormat = QTextCharFormat(self.__formats.defaultFormat)
		self.__formats.singleQuotationFormat.setForeground(Qt.blue)

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.
		"""

		self.__multiLineStringStart = QRegExp(r"\"\"\"|'''")
		self.__multiLineStringEnd = QRegExp(r"\"\"\"|'''")

		self.__rules = map(lambda i: (QRegExp(r"\b{0}\b".format(i)), self.__formats.keywordFormat), self.__keywords)

		self.__rules.append((QRegExp(r"\b[a-zA-Z0-9_]+\(.*\)"), self.__formats.objectFormat))
		self.__rules.append((QRegExp(r"\b__[a-zA-Z0-9]+__\b"), self.__formats.specialObjectFormat))
		self.__rules.append((QRegExp(r"\bself\b"), self.__formats.selfFormat))

		self.__rules.append((QRegExp(r"#[^\n]*"), self.__formats.singleLineCommentFormat))

		self.__rules.append((QRegExp(r"\"[^\n]*\""), self.__formats.doubleQuotationFormat))
		self.__rules.append((QRegExp(r"'[^\n]*'"), self.__formats.singleQuotationFormat))

	@core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights provided text block.

		:param block: Text block. ( QString )
		"""

		self.setCurrentBlockState(0)

		if block.trimmed().isEmpty():
			self.setFormat(0, len(block), self.__formats.nullFormat)
			return

		self.setFormat(0, len(block), self.__formats.defaultFormat)

		startIndex = 0
		if self.previousBlockState() != 1:
			startIndex = block.indexOf(self.__multiLineStringStart)

		if startIndex > -1:
			self.highlightText(block, 0, startIndex)
		else:
			self.highlightText(block, 0, len(block))

		while startIndex >= 0:
			endIndex = block.indexOf(self.__multiLineStringEnd, startIndex + len(self.__multiLineStringStart.pattern()))
			if endIndex == -1:
				self.setCurrentBlockState(1)
				commentLength = block.length() - startIndex
			else:
				commentLength = endIndex - startIndex + self.__multiLineStringEnd.matchedLength()
				self.highlightText(block, endIndex, len(block))

			self.setFormat(startIndex, commentLength, self.__formats.multiLineStringFormat)
			startIndex = block.indexOf(self.__multiLineStringStart, startIndex + commentLength)

	@core.executionTrace
	def highlightText(self, text, start, end):
		"""
		This method highlights provided text.

		:param text: Text. ( QString )
		:param start: Text start index. ( Integer )
		:param end: Text end index. ( Integer )
		:return: Method success. ( Boolean )
		"""

		for rule, format in self.__rules:
			index = rule.indexIn(text, start)
			while index >= start and index < end:
				length = rule.matchedLength()
				self.setFormat(index, min(length, end - index), format)
				index = rule.indexIn(text, index + length)
		return True

if __name__ == "__main__":

	import sys
	app = QApplication(sys.argv)
	widget = QTextEdit()
	widget.setStyleSheet("background-color: rgb(64, 64, 64);")
	widget.highlighter = PythonHighlighter(widget.document())
	widget.setText("""
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

'''
This module defines the :class:`PythonHighligher` class.
'''

# Starting the console handler.
if not hasattr(sys, "frozen") or not (platform.system() == "Windows" or platform.system() == "Microsoft"):
	RuntimeConstants.loggingConsoleHandler = logging.StreamHandler(sys.__stdout__)
	RuntimeConstants.loggingConsoleHandler.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
	LOGGER.addHandler(RuntimeConstants.loggingConsoleHandler)

# Defining logging formatters.
RuntimeConstants.loggingFormatters = {"Default" :core.LOGGING_DEFAULT_FORMATTER,
									"Extended" : core.LOGGING_EXTENDED_FORMATTER,
									"Standard" : core.LOGGING_STANDARD_FORMATTER}

class Preferences():
	
	@core.executionTrace
	def __init__(self, preferencesFile=None):
		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__preferencesFile = None
		self.__preferencesFile = preferencesFile

		self.__settings = QSettings(self.preferencesFile, QSettings.IniFormat)

		# --- Initializing preferences. ---
		self.__getDefaultLayoutsSettings()
		
	@core.executionTrace
	def highlightBlock(self, block):

		self.setCurrentBlockState(0)

		if block.trimmed().isEmpty():
			self.setFormat(0, len(block), self.__formats.nullFormat)
			return

		self.setFormat(0, len(block), self.__formats.defaultFormat)

		startIndex = 0
		if self.previousBlockState() != 1:
			startIndex = block.indexOf(self.__multiLineStringStart)

		if startIndex > -1:
			self.highlightText(block, 0, startIndex)
		else:
			self.highlightText(block, 0, len(block))

		while startIndex >= 0:
			endIndex = block.indexOf(self.__multiLineStringEnd, startIndex + len(self.__multiLineStringStart.pattern()))
			if endIndex == -1:
				self.setCurrentBlockState(1)
				commentLength = block.length() - startIndex
			else:
				commentLength = endIndex - startIndex + self.__multiLineStringEnd.matchedLength()
				self.highlightText(block, endIndex, len(block))

			self.setFormat(startIndex, commentLength, self.__formats.multiLineStringFormat)
			startIndex = block.indexOf(self.__multiLineStringStart, startIndex + commentLength)


""")
	widget.show()
	widget.raise_()
	sys.exit(app.exec_())
