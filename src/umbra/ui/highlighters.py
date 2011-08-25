#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**highlighters.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the highlighters class.

**Others:**
	Portions of the code from Pyguin by Lee Harr: http://code.google.com/p/pynguin/.

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
class Rule(core.Structure):
	"""
	This class represents a storage object for highlighters rule. 
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: pattern, format. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

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

class Highlighter(QSyntaxHighlighter):
	"""
	This class is a `QSyntaxHighlighter <http://doc.qt.nokia.com/4.7/qsyntaxhighlighter.html>`_ subclass used as a base for highlighters classes.
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

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights provided text block.

		:param block: Text block. ( QString )
		"""
		pass

	# @core.executionTrace
	def highlightText(self, text, start, end):
		"""
		This method highlights provided text.

		:param text: Text. ( QString )
		:param start: Text start index. ( Integer )
		:param end: Text end index. ( Integer )
		:return: Method success. ( Boolean )
		"""

		for rule in self.__rules:
			index = rule.pattern.indexIn(text, start)
			while index >= start and index < end:
				length = rule.pattern.matchedLength()
				self.setFormat(index, min(length, end - index), rule.format)
				index = rule.pattern.indexIn(text, index + length)
		return True

class LoggingHighlighter(Highlighter):
	"""
	This class is a :class:`Highlighter` subclass subclass providing syntax highlighting for Application logging documents.
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Syntax highlighter parent. ( QObject )
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
		"""

		self.formats = Formats(default=QTextCharFormat())
		self.formats.default.setForeground(QColor(192, 192, 192))

		self.formats.null = QTextCharFormat(self.formats.default)
		self.formats.null.setFontPointSize(self.formats.default.font().pointSize() / 4.0)

		self.formats.loggingCritical = QTextCharFormat(self.formats.default)
		self.formats.loggingCritical.setForeground(QColor(48, 48, 48))
		self.formats.loggingCritical.setBackground(QColor(255, 64, 64))
		self.formats.loggingError = QTextCharFormat(self.formats.default)
		self.formats.loggingError.setForeground(QColor(255, 64, 64))
		self.formats.loggingWarning = QTextCharFormat(self.formats.default)
		self.formats.loggingWarning.setForeground(QColor(255, 128, 0))
		self.formats.loggingInfo = QTextCharFormat(self.formats.default)
		self.formats.loggingDebug = QTextCharFormat(self.formats.default)
		self.formats.loggingDebug.setFontItalic(True)

		self.formats.loggingDebugTraceIn = QTextCharFormat(self.formats.loggingDebug)
		self.formats.loggingDebugTraceIn.setForeground(QColor(128, 160, 192))
		self.formats.loggingDebugTraceOut = QTextCharFormat(self.formats.loggingDebug)
		self.formats.loggingDebugTraceOut.setForeground(QColor(192, 160, 128))

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.
		"""

		self.__multiLineStringStart = QRegExp(r"\"\"\"|'''")
		self.__multiLineStringEnd = QRegExp(r"\"\"\"|'''")

		self.rules = []

		self.rules.append(Rule(pattern=QRegExp(r"^CRITICAL\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*CRITICAL\s*:.*$"), format=self.formats.loggingCritical))
		self.rules.append(Rule(pattern=QRegExp(r"^ERROR\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*ERROR\s*:.*$"), format=self.formats.loggingError))
		self.rules.append(Rule(pattern=QRegExp(r"^WARNING\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*WARNING\s*:.*$"), format=self.formats.loggingWarning))
		self.rules.append(Rule(pattern=QRegExp(r"^INFO\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*INFO\s*:.*$"), format=self.formats.loggingInfo))
		self.rules.append(Rule(pattern=QRegExp(r"^DEBUG\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*DEBUG\s*:.*$"), format=self.formats.loggingDebug))

		self.rules.append(Rule(pattern=QRegExp(r"^DEBUG\s*:\s--->>>.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*DEBUG\s*:\s--->>>.*$"), format=self.formats.loggingDebugTraceIn))
		self.rules.append(Rule(pattern=QRegExp(r"^DEBUG\s*:\s---<<<.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*DEBUG\s*:\s---<<<.*$"), format=self.formats.loggingDebugTraceOut))

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights provided text block.

		:param block: Text block. ( QString )
		"""

		if block.trimmed().isEmpty():
			self.setFormat(0, len(block), self.formats.null)
			return

		self.highlightText(block, 0, len(block))

class PythonHighlighter(Highlighter):
	"""
	This class is a :class:`Highlighter` subclass providing syntax highlighting for Python documents.
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Syntax highlighter parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

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

		self.formats = Formats(default=QTextCharFormat())
		self.formats.default.setForeground(QColor(192, 192, 192))

		self.formats.null = QTextCharFormat(self.formats.default)
		self.formats.null.setFontPointSize(self.formats.default.font().pointSize() / 4.0)

		self.formats.keyword = QTextCharFormat(self.formats.default)
		self.formats.keyword.setForeground(QBrush(QColor(205, 170, 105)))
		self.formats.keyword.setFontWeight(QFont.Bold)

		self.formats.numericConstant = QTextCharFormat(self.formats.default)
		self.formats.numericConstant.setForeground(QColor(205, 105, 75))
		self.formats.numericIntegerDecimal = QTextCharFormat(self.formats.numericConstant)
		self.formats.numericIntegerLongDecimal = QTextCharFormat(self.formats.numericConstant)
		self.formats.numericIntegerHexadecimal = QTextCharFormat(self.formats.numericConstant)
		self.formats.numericIntegerLongHexadecimal = QTextCharFormat(self.formats.numericConstant)
		self.formats.numericIntegerOctal = QTextCharFormat(self.formats.numericConstant)
		self.formats.numericIntegerLongOctal = QTextCharFormat(self.formats.numericConstant)
		self.formats.numericFloat = QTextCharFormat(self.formats.numericConstant)
		self.formats.numericComplex = QTextCharFormat(self.formats.numericConstant)

		self.formats.modifierGlobal = QTextCharFormat(self.formats.default)
		self.formats.modifierGlobal.setForeground(QBrush(QColor(250, 240, 150)))
		self.formats.modifierSpecialGlobal = QTextCharFormat(self.formats.modifierGlobal)

		self.formats.operator = QTextCharFormat(self.formats.keyword)
		self.formats.operatorComparison = QTextCharFormat(self.formats.operator)
		self.formats.operatorAssignement = QTextCharFormat(self.formats.operator)
		self.formats.operatorAssignementAugmented = QTextCharFormat(self.formats.operator)
		self.formats.operatorArithmetic = QTextCharFormat(self.formats.operator)

		self.formats.entity = QTextCharFormat(self.formats.default)
		self.formats.entity.setForeground(QBrush(QColor(155, 110, 165)))
		self.formats.entityClass = QTextCharFormat(self.formats.entity)
		self.formats.entityFunction = QTextCharFormat(self.formats.entity)
		self.formats.entityDecorator = QTextCharFormat(self.formats.entity)

		self.formats.builtins = QTextCharFormat(self.formats.default)
		self.formats.builtins.setForeground(QBrush(QColor(115, 135, 175)))
		self.formats.builtinsExceptions = QTextCharFormat(self.formats.builtins)
		self.formats.builtinsFunctions = QTextCharFormat(self.formats.builtins)
		self.formats.builtinsMiscellaneous = QTextCharFormat(self.formats.builtins)
		self.formats.builtinsObjectMethods = QTextCharFormat(self.formats.builtins)
		self.formats.magicMethods = QTextCharFormat(self.formats.builtins)

		self.formats.magicObject = QTextCharFormat(self.formats.default)
		self.formats.magicObject.setFontWeight(QFont.Bold)

		self.formats.decoratorArgument = QTextCharFormat(self.formats.default)
		self.formats.decoratorArgument.setForeground(QColor(115, 135, 175))
		self.formats.decoratorArgument.setFontItalic(True)

		self.formats.singleLineComment = QTextCharFormat(self.formats.default)
		self.formats.singleLineComment.setForeground(QColor(128, 128, 128))

		self.formats.multiLineString = QTextCharFormat(self.formats.default)
		self.formats.multiLineString.setForeground(QColor(205, 105, 75))
		self.formats.multiLineString.setFontItalic(True)

		self.formats.quotation = QTextCharFormat(self.formats.default)
		self.formats.quotation.setForeground(QColor(145, 160, 105))
		self.formats.quotation.setFontItalic(True)
		self.formats.doubleQuotation = QTextCharFormat(self.formats.quotation)
		self.formats.singleQuotation = QTextCharFormat(self.formats.quotation)

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.
		"""

		self.__multiLineStringStart = QRegExp(r"\"\"\"|'''")
		self.__multiLineStringEnd = QRegExp(r"\"\"\"|'''")

		self.rules = map(lambda i: Rule(pattern=QRegExp(r"\b{0}\b".format(i)), format=self.formats.keyword), self.__keywords)

		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?[1-9]+\d*|0\b"), format=self.formats.numericIntegerDecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b([-+]?[1-9]+\d*|0)L\b"), format=self.formats.numericIntegerLongDecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0x[a-fA-F\d]+L\b"), format=self.formats.numericIntegerLongHexadecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0x[a-fA-F\d]+\b"), format=self.formats.numericIntegerHexadecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0x[a-fA-F\d]+L\b"), format=self.formats.numericIntegerLongHexadecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0[0-7]+\b"), format=self.formats.numericIntegerOctal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0[0-7]+L\b"), format=self.formats.numericIntegerLongOctal))
		self.rules.append(Rule(pattern=QRegExp(r"[-+]?\d*\.?\d+([eE][-+]?\d+)?"), format=self.formats.numericFloat))
		self.rules.append(Rule(pattern=QRegExp(r"[-+]?\d*\.?\d+([eE][-+]?\d+)?\s*\s*[-+]?\d*\.?\d+([eE][-+]?\d+)?[jJ]"), format=self.formats.numericComplex))

		self.rules.append(Rule(pattern=QRegExp(r"\b(global)\b"), format=self.formats.modifierGlobal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[A-Z_]+\b"), format=self.formats.modifierSpecialGlobal))

		self.rules.append(Rule(pattern=QRegExp(r"<\=|>\=|\=\=|<|>|\!\="), format=self.formats.operatorComparison))
		self.rules.append(Rule(pattern=QRegExp(r"\="), format=self.formats.operatorAssignement))
		self.rules.append(Rule(pattern=QRegExp(r"\+\=|-\=|\*\=|/\=|//\=|%\=|&\=|\|\=|\^\=|>>\=|<<\=|\*\*\="), format=self.formats.operatorAssignementAugmented))
		self.rules.append(Rule(pattern=QRegExp(r"\+|\-|\*|\*\*|/|//|%|<<|>>|&|\||\^|~"), format=self.formats.operatorArithmetic))

		# This rules don't work: QRegExp lacks of lookbehind support.		
		self.rules.append(Rule(pattern=QRegExp(r"(?<=class\s)\w+(?=\s?\(\)\s?:)"), format=self.formats.entityClass))
		self.rules.append(Rule(pattern=QRegExp(r"(?<=def\s)\w+(?=\s?\(\)\s?:)"), format=self.formats.entityFunction))

		self.rules.append(Rule(pattern=QRegExp(r"@[\w\.]+"), format=self.formats.entityDecorator))

		self.rules.append(Rule(pattern=QRegExp(r"\b(ArithmeticError|AssertionError|AttributeError|BufferError|BytesWarning|CodecRegistryError|DeprecationWarning|EOFError|EnvironmentError|FloatingPointError|FutureWarning|GetPassWarning|IOError|ImportError|ImportWarning|IndentationError|IndexError|ItimerError|KeyError|LookupError|MemoryError|NameError|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning|ReferenceError|RuntimeError|RuntimeWarning|StandardError|StopIteration|SyntaxError|SyntaxWarning|SystemError|TabError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|Warning|ZeroDivisionError|ZipImportError|_OptionError|error|error)\b"), format=self.formats.builtinsExceptions))
		self.rules.append(Rule(pattern=QRegExp(r"\b(abs|all|any|apply|basestring|bin|bool|buffer|bytearray|bytes|callable|chr|classmethod|cmp|coerce|compile|complex|copyright|credits|delattr|dict|dir|divmod|enumerate|eval|execfile|exit|file|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|intern|isinstance|issubclass|iter|len|license|list|locals|long|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|quit|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\b"), format=self.formats.builtinsFunctions))
		self.rules.append(Rule(pattern=QRegExp(r"\b(Ellipsis|False|None|True|__(debug|doc|import|name|package)__)\b"), format=self.formats.builtinsMiscellaneous))
		self.rules.append(Rule(pattern=QRegExp(r"\b(__(class|delattr|doc|format|getattribute|hash|init|new|reduce|reduce_ex|repr|setattr|sizeof|str|subclasshook)__)\b"), format=self.formats.builtinsObjectMethods))
		self.rules.append(Rule(pattern=QRegExp(r"\b__(abs|add|and|call|cmp|coerce|complex|contains|delattr|delete|delitem|delslice|del|divmod|div|enter|eq|exit|float|floordiv|getattribute|getattr|getitem|getslice|get|ge|gt|hash|hex|iadd|iand|idiv|ifloordiv|ilshift|imod|imul|index|init|int|invert|ior|ipow|irshift|isub|iter|itruediv|ixor|len|le|long|lshift|lt|mod|mul|neg|new|ne|nonzero|oct|or|pos|pow|radd|rand|rcmp|rdivmod|rdiv|repr|reversed|rfloordiv|rlshift|rmod|rmul|ror|rpow|rrshift|rshift|rsub|rtruediv|rxor|setattr|setitem|setslice|set|str|sub|truediv|unicode|xor)__\b"), format=self.formats.magicMethods))

		self.rules.append(Rule(pattern=QRegExp(r"\b(?:(?!__(debug|doc|import|name|package|class|delattr|doc|format|getattribute|hash|init|new|reduce|reduce_ex|repr|setattr|sizeof|str|subclasshook__|abs|add|and|call|cmp|coerce|complex|contains|delattr|delete|delitem|delslice|del|divmod|div|enter|eq|exit|float|floordiv|getattribute|getattr|getitem|getslice|get|ge|gt|hash|hex|iadd|iand|idiv|ifloordiv|ilshift|imod|imul|index|init|int|invert|ior|ipow|irshift|isub|iter|itruediv|ixor|len|le|long|lshift|lt|mod|mul|neg|new|ne|nonzero|oct|or|pos|pow|radd|rand|rcmp|rdivmod|rdiv|repr|reversed|rfloordiv|rlshift|rmod|rmul|ror|rpow|rrshift|rshift|rsub|rtruediv|rxor|setattr|setitem|setslice|set|str|sub|truediv|unicode|xor))__\w+__)\b"), format=self.formats.magicObject))

		self.rules.append(Rule(pattern=QRegExp(r"\bself\b"), format=self.formats.decoratorArgument))

		self.rules.append(Rule(pattern=QRegExp(r"#.*$\n?"), format=self.formats.singleLineComment))

		self.rules.append(Rule(pattern=QRegExp(r"\"[^\n\"]*\""), format=self.formats.doubleQuotation))
		self.rules.append(Rule(pattern=QRegExp(r"'[^\n']*'"), format=self.formats.singleQuotation))

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights provided text block.

		:param block: Text block. ( QString )
		"""

		self.setCurrentBlockState(0)

		if block.trimmed().isEmpty():
			self.setFormat(0, len(block), self.formats.null)
			return

		self.setFormat(0, len(block), self.formats.default)

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

			self.setFormat(startIndex, commentLength, self.formats.multiLineString)
			startIndex = block.indexOf(self.__multiLineStringStart, startIndex + commentLength)
