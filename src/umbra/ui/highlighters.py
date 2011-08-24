#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**highlighters.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`PythonHighligher` class.

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

		self.__formats = Formats(default=QTextCharFormat())
		self.__formats.default.setForeground(QColor(192, 192, 192))

		self.__formats.null = QTextCharFormat(self.__formats.default)
		self.__formats.null.setFontPointSize(self.__formats.default.font().pointSize() / 4.0)

		self.__formats.keyword = QTextCharFormat(self.__formats.default)
		self.__formats.keyword.setForeground(QBrush(QColor(205, 170, 105)))
		self.__formats.keyword.setFontWeight(QFont.Bold)

		self.__formats.numericConstant = QTextCharFormat(self.__formats.default)
		self.__formats.numericConstant.setForeground(QColor(205, 105, 75))
		self.__formats.numericIntegerDecimal = QTextCharFormat(self.__formats.numericConstant)
		self.__formats.numericIntegerLongDecimal = QTextCharFormat(self.__formats.numericConstant)
		self.__formats.numericIntegerHexadecimal = QTextCharFormat(self.__formats.numericConstant)
		self.__formats.numericIntegerLongHexadecimal = QTextCharFormat(self.__formats.numericConstant)
		self.__formats.numericIntegerOctal = QTextCharFormat(self.__formats.numericConstant)
		self.__formats.numericIntegerLongOctal = QTextCharFormat(self.__formats.numericConstant)
		self.__formats.numericFloat = QTextCharFormat(self.__formats.numericConstant)
		self.__formats.numericComplex = QTextCharFormat(self.__formats.numericConstant)

		self.__formats.modifierGlobal = QTextCharFormat(self.__formats.default)
		self.__formats.modifierGlobal.setForeground(QBrush(QColor(250, 240, 150)))
		self.__formats.modifierSpecialGlobal = QTextCharFormat(self.__formats.modifierGlobal)

		self.__formats.operator = QTextCharFormat(self.__formats.keyword)
		self.__formats.operatorComparison = QTextCharFormat(self.__formats.operator)
		self.__formats.operatorAssignement = QTextCharFormat(self.__formats.operator)
		self.__formats.operatorAssignementAugmented = QTextCharFormat(self.__formats.operator)
		self.__formats.operatorArithmetic = QTextCharFormat(self.__formats.operator)

		self.__formats.entity = QTextCharFormat(self.__formats.default)
		self.__formats.entity.setForeground(QBrush(QColor(155, 110, 165)))
		self.__formats.entityClass = QTextCharFormat(self.__formats.entity)
		self.__formats.entityFunction = QTextCharFormat(self.__formats.entity)
		self.__formats.entityDecorator = QTextCharFormat(self.__formats.entity)

		self.__formats.builtins = QTextCharFormat(self.__formats.default)
		self.__formats.builtins.setForeground(QBrush(QColor(115, 135, 175)))
		self.__formats.builtinsExceptions = QTextCharFormat(self.__formats.builtins)
		self.__formats.builtinsFunctions = QTextCharFormat(self.__formats.builtins)
		self.__formats.builtinsMiscellaneous = QTextCharFormat(self.__formats.builtins)
		self.__formats.builtinsObjectMethods = QTextCharFormat(self.__formats.builtins)
		self.__formats.magicMethods = QTextCharFormat(self.__formats.builtins)

		self.__formats.magicObject = QTextCharFormat(self.__formats.default)
		self.__formats.magicObject.setFontWeight(QFont.Bold)

		self.__formats.decoratorArgument = QTextCharFormat(self.__formats.default)
		self.__formats.decoratorArgument.setForeground(QColor(115, 135, 175))
		self.__formats.decoratorArgument.setFontItalic(True)

		self.__formats.singleLineComment = QTextCharFormat(self.__formats.default)
		self.__formats.singleLineComment.setForeground(QColor(128, 128, 128))

		self.__formats.multiLineString = QTextCharFormat(self.__formats.default)
		self.__formats.multiLineString.setForeground(QColor(205, 105, 75))
		self.__formats.multiLineString.setFontItalic(True)

		self.__formats.quotation = QTextCharFormat(self.__formats.default)
		self.__formats.quotation.setForeground(QColor(145, 160, 105))
		self.__formats.quotation.setFontItalic(True)
		self.__formats.doubleQuotation = QTextCharFormat(self.__formats.quotation)
		self.__formats.singleQuotation = QTextCharFormat(self.__formats.quotation)

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.
		"""

		self.__multiLineStringStart = QRegExp(r"\"\"\"|'''")
		self.__multiLineStringEnd = QRegExp(r"\"\"\"|'''")

		self.__rules = map(lambda i: Rule(pattern=QRegExp(r"\b{0}\b".format(i)), format=self.__formats.keyword), self.__keywords)

		self.__rules.append(Rule(pattern=QRegExp(r"\b[-+]?[1-9]+\d*|0\b"), format=self.__formats.numericIntegerDecimal))
		self.__rules.append(Rule(pattern=QRegExp(r"\b([-+]?[1-9]+\d*|0)L\b"), format=self.__formats.numericIntegerLongDecimal))
		self.__rules.append(Rule(pattern=QRegExp(r"\b[-+]?0x[a-fA-F\d]+L\b"), format=self.__formats.numericIntegerLongHexadecimal))
		self.__rules.append(Rule(pattern=QRegExp(r"\b[-+]?0x[a-fA-F\d]+\b"), format=self.__formats.numericIntegerHexadecimal))
		self.__rules.append(Rule(pattern=QRegExp(r"\b[-+]?0x[a-fA-F\d]+L\b"), format=self.__formats.numericIntegerLongHexadecimal))
		self.__rules.append(Rule(pattern=QRegExp(r"\b[-+]?0[0-7]+\b"), format=self.__formats.numericIntegerOctal))
		self.__rules.append(Rule(pattern=QRegExp(r"\b[-+]?0[0-7]+L\b"), format=self.__formats.numericIntegerLongOctal))
		self.__rules.append(Rule(pattern=QRegExp(r"[-+]?\d*\.?\d+([eE][-+]?\d+)?"), format=self.__formats.numericFloat))
		self.__rules.append(Rule(pattern=QRegExp(r"[-+]?\d*\.?\d+([eE][-+]?\d+)?\s*\s*[-+]?\d*\.?\d+([eE][-+]?\d+)?[jJ]"), format=self.__formats.numericComplex))

		self.__rules.append(Rule(pattern=QRegExp(r"\b(global)\b"), format=self.__formats.modifierGlobal))
		self.__rules.append(Rule(pattern=QRegExp(r"\b[A-Z_]+\b"), format=self.__formats.modifierSpecialGlobal))

		self.__rules.append(Rule(pattern=QRegExp(r"<\=|>\=|\=\=|<|>|\!\="), format=self.__formats.operatorComparison))
		self.__rules.append(Rule(pattern=QRegExp(r"\="), format=self.__formats.operatorAssignement))
		self.__rules.append(Rule(pattern=QRegExp(r"\+\=|-\=|\*\=|/\=|//\=|%\=|&\=|\|\=|\^\=|>>\=|<<\=|\*\*\="), format=self.__formats.operatorAssignementAugmented))
		self.__rules.append(Rule(pattern=QRegExp(r"\+|\-|\*|\*\*|/|//|%|<<|>>|&|\||\^|~"), format=self.__formats.operatorArithmetic))

		# This rules don't work: QRegExp lacks of lookbehind support.		
		self.__rules.append(Rule(pattern=QRegExp(r"(?<=class\s)\w+(?=\s?\(\)\s?:)"), format=self.__formats.entityClass))
		self.__rules.append(Rule(pattern=QRegExp(r"(?<=def\s)\w+(?=\s?\(\)\s?:)"), format=self.__formats.entityFunction))

		self.__rules.append(Rule(pattern=QRegExp(r"@[\w\.]+"), format=self.__formats.entityDecorator))

		self.__rules.append(Rule(pattern=QRegExp(r"\b(ArithmeticError|AssertionError|AttributeError|BufferError|BytesWarning|CodecRegistryError|DeprecationWarning|EOFError|EnvironmentError|FloatingPointError|FutureWarning|GetPassWarning|IOError|ImportError|ImportWarning|IndentationError|IndexError|ItimerError|KeyError|LookupError|MemoryError|NameError|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning|ReferenceError|RuntimeError|RuntimeWarning|StandardError|StopIteration|SyntaxError|SyntaxWarning|SystemError|TabError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|Warning|ZeroDivisionError|ZipImportError|_OptionError|error|error)\b"), format=self.__formats.builtinsExceptions))
		self.__rules.append(Rule(pattern=QRegExp(r"\b(abs|all|any|apply|basestring|bin|bool|buffer|bytearray|bytes|callable|chr|classmethod|cmp|coerce|compile|complex|copyright|credits|delattr|dict|dir|divmod|enumerate|eval|execfile|exit|file|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|intern|isinstance|issubclass|iter|len|license|list|locals|long|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|quit|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\b"), format=self.__formats.builtinsFunctions))
		self.__rules.append(Rule(pattern=QRegExp(r"\b(Ellipsis|False|None|True|__(debug|doc|import|name|package)__)\b"), format=self.__formats.builtinsMiscellaneous))
		self.__rules.append(Rule(pattern=QRegExp(r"\b(__(class|delattr|doc|format|getattribute|hash|init|new|reduce|reduce_ex|repr|setattr|sizeof|str|subclasshook)__)\b"), format=self.__formats.builtinsObjectMethods))
		self.__rules.append(Rule(pattern=QRegExp(r"\b__(abs|add|and|call|cmp|coerce|complex|contains|delattr|delete|delitem|delslice|del|divmod|div|enter|eq|exit|float|floordiv|getattribute|getattr|getitem|getslice|get|ge|gt|hash|hex|iadd|iand|idiv|ifloordiv|ilshift|imod|imul|index|init|int|invert|ior|ipow|irshift|isub|iter|itruediv|ixor|len|le|long|lshift|lt|mod|mul|neg|new|ne|nonzero|oct|or|pos|pow|radd|rand|rcmp|rdivmod|rdiv|repr|reversed|rfloordiv|rlshift|rmod|rmul|ror|rpow|rrshift|rshift|rsub|rtruediv|rxor|setattr|setitem|setslice|set|str|sub|truediv|unicode|xor)__\b"), format=self.__formats.magicMethods))

		self.__rules.append(Rule(pattern=QRegExp(r"\b(?:(?!__(debug|doc|import|name|package|class|delattr|doc|format|getattribute|hash|init|new|reduce|reduce_ex|repr|setattr|sizeof|str|subclasshook__|abs|add|and|call|cmp|coerce|complex|contains|delattr|delete|delitem|delslice|del|divmod|div|enter|eq|exit|float|floordiv|getattribute|getattr|getitem|getslice|get|ge|gt|hash|hex|iadd|iand|idiv|ifloordiv|ilshift|imod|imul|index|init|int|invert|ior|ipow|irshift|isub|iter|itruediv|ixor|len|le|long|lshift|lt|mod|mul|neg|new|ne|nonzero|oct|or|pos|pow|radd|rand|rcmp|rdivmod|rdiv|repr|reversed|rfloordiv|rlshift|rmod|rmul|ror|rpow|rrshift|rshift|rsub|rtruediv|rxor|setattr|setitem|setslice|set|str|sub|truediv|unicode|xor))__\w+__)\b"), format=self.__formats.magicObject))

		self.__rules.append(Rule(pattern=QRegExp(r"\bself\b"), format=self.__formats.decoratorArgument))

		self.__rules.append(Rule(pattern=QRegExp(r"#.*$\n?"), format=self.__formats.singleLineComment))

		self.__rules.append(Rule(pattern=QRegExp(r"\"[^\n\"]*\""), format=self.__formats.doubleQuotation))
		self.__rules.append(Rule(pattern=QRegExp(r"'[^\n']*'"), format=self.__formats.singleQuotation))

	@core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights provided text block.

		:param block: Text block. ( QString )
		"""

		self.setCurrentBlockState(0)

		if block.trimmed().isEmpty():
			self.setFormat(0, len(block), self.__formats.null)
			return

		self.setFormat(0, len(block), self.__formats.default)

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

			self.setFormat(startIndex, commentLength, self.__formats.multiLineString)
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

		for rule in self.__rules:
			index = rule.pattern.indexIn(text, start)
			while index >= start and index < end:
				length = rule.pattern.matchedLength()
				self.setFormat(index, min(length, end - index), rule.format)
				index = rule.pattern.indexIn(text, index + length)
		return True

