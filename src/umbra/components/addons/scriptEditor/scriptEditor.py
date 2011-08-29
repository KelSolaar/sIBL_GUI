#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**scriptEditor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`ScriptEditor` Component Interface class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import code
import logging
import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants
from umbra.globals.runtimeConstants import RuntimeConstants
from umbra.globals.uiConstants import UiConstants
from umbra.ui.highlighters import LoggingHighlighter, PythonHighlighter

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
class ScriptEditor(UiComponent):
	"""
	| This class is the :mod:`umbra.components.addons.scriptEditor.scriptEditor` Component Interface class.
	"""

	# Custom signals definitions.
	datasChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		:param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__uiPath = "ui/Script_Editor.ui"
		self.__dockArea = 8

		self.__container = None

		self.__locals = None
		self.__memoryHandlerStackDepth = None
		self.__menuBar = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for **self.__uiPath** attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for **self.__uiPath** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for **self.__uiPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def dockArea(self):
		"""
		This method is the property for **self.__dockArea** attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def locals(self):
		"""
		This method is the property for **self.__locals** attribute.

		:return: self.__locals. ( Dictionary )
		"""

		return self.__locals

	@locals.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self, value):
		"""
		This method is the setter method for **self.__locals** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("locals"))

	@locals.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self):
		"""
		This method is the deleter method for **self.__locals** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("locals"))

	@property
	def memoryHandlerStackDepth(self):
		"""
		This method is the property for **self.__memoryHandlerStackDepth** attribute.

		:return: self.__memoryHandlerStackDepth. ( Integer )
		"""

		return self.__memoryHandlerStackDepth

	@memoryHandlerStackDepth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self, value):
		"""
		This method is the setter method for **self.__memoryHandlerStackDepth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("memoryHandlerStackDepth"))

	@memoryHandlerStackDepth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self):
		"""
		This method is the deleter method for **self.__memoryHandlerStackDepth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("memoryHandlerStackDepth"))

	@property
	def menuBar(self):
		"""
		This method is the property for **self.__menuBar** attribute.

		:return: self.__menuBar. ( QToolbar )
		"""

		return self.__menuBar

	@menuBar.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menuBar(self, value):
		"""
		This method is the setter method for **self.__menuBar** attribute.

		:param value: Attribute value. ( QToolbar )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("menuBar"))

	@menuBar.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menuBar(self):
		"""
		This method is the deleter method for **self.__menuBar** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("menuBar"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container

		self.__getsLocals()
		self.__console = code.InteractiveConsole(self.__locals)

		return UiComponent.activate(self)

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = None
		self.__container = None

		self.__console = None

		return UiComponent.deactivate(self)

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__menuBar = QMenuBar()
		self.__menuBar.setNativeMenuBar(False)
		self.ui.menuBar_frame_gridLayout.addWidget(self.__menuBar)
		self.__initializeMenuBar()

		self.ui.Script_Editor_Input_textEdit.highlighter = PythonHighlighter(self.ui.Script_Editor_Input_textEdit.document())
		self.ui.Script_Editor_Output_textEdit.highlighter = LoggingHighlighter(self.ui.Script_Editor_Output_textEdit.document())

		self.__Lines_Numbers_textEdit_setUi()

		# Signals / Slots.
		self.__container.timer.timeout.connect(self.__Script_Editor_Output_textEdit_refreshUi)
		self.ui.Evaluate_Script_pushButton.clicked.connect(self.__Evaluate_Script_pushButton__clicked)
		self.datasChanged.connect(self.__Script_Editor_Output_textEdit_refreshUi)
		self.ui.Script_Editor_Input_textEdit.textChanged.connect(self.__Script_Editor_Input_textEdit__textChanged)
		self.ui.Script_Editor_Input_textEdit.verticalScrollBar().valueChanged.connect(self.__Script_Editor_Input_textEdit_verticalScrollBar__valueChanged)

		return True

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__menuBar.setParent(None)
		self.__menuBar = None

		self.ui.Script_Editor_Input_textEdit.highlighter = None
		self.ui.Script_Editor_Output_textEdit.highlighter = None

		# Signals / Slots.
		self.__container.timer.timeout.disconnect(self.__Script_Editor_Output_textEdit_refreshUi)
		self.ui.Evaluate_Script_pushButton.clicked.disconnect(self.__Evaluate_Script_pushButton__clicked)
		self.datasChanged.disconnect(self.__Script_Editor_Output_textEdit_refreshUi)
		self.ui.Script_Editor_Input_textEdit.textChanged.disconnect(self.__Script_Editor_Input_textEdit__textChanged)
		self.ui.Script_Editor_Input_textEdit.verticalScrollBar().valueChanged.disconnect(self.__Script_Editor_Input_textEdit_verticalScrollBar__valueChanged)

		return True

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self.ui)
		self.ui.setParent(None)

		return True

	@core.executionTrace
	def __initializeMenuBar(self):
		"""
		This method initializes Component menuBar.
		"""

		self.__fileMenu = QMenu("&File")
		loadScriptAction = QAction("&Load script ...", self)
		loadScriptAction.setShortcut(QKeySequence(QKeySequence.Open))
		self.__fileMenu.addAction(loadScriptAction)
		sourceScriptAction = QAction("Source script ...", self)
		self.__fileMenu.addAction(sourceScriptAction)
		saveScriptAction = QAction("&Save script ...", self)
		saveScriptAction.setShortcut(QKeySequence(QKeySequence.Save))
		self.__fileMenu.addAction(saveScriptAction)
		self.__menuBar.addMenu(self.__fileMenu)

		# Signals / Slots.
		loadScriptAction.triggered.connect(self.__loadScriptAction__triggered)
		sourceScriptAction.triggered.connect(self.__sourceScriptAction__triggered)
		saveScriptAction.triggered.connect(self.__saveScriptAction__triggered)

		self.__editMenu = QMenu("&Edit")
		undoAction = QAction("&Undo", self)
		undoAction.setShortcut(QKeySequence(QKeySequence.Undo))
		self.__editMenu.addAction(undoAction)
		redoAction = QAction("&Redo", self)
		redoAction.setShortcut(QKeySequence(QKeySequence.Redo))
		self.__editMenu.addAction(redoAction)
		self.__editMenu.addSeparator()
		cutAction = QAction("Cu&t", self)
		cutAction.setShortcut(QKeySequence(QKeySequence.Cut))
		self.__editMenu.addAction(cutAction)
		copyAction = QAction("&Copy", self)
		copyAction.setShortcut(QKeySequence(QKeySequence.Copy))
		self.__editMenu.addAction(copyAction)
		pasteAction = QAction("&Paste", self)
		pasteAction.setShortcut(QKeySequence(QKeySequence.Paste))
		self.__editMenu.addAction(pasteAction)
		deleteAction = QAction("Delete", self)
		self.__editMenu.addAction(deleteAction)
		self.__editMenu.addSeparator()
		selectAllAction = QAction("Select All", self)
		selectAllAction.setShortcut(QKeySequence(QKeySequence.SelectAll))
		self.__editMenu.addAction(selectAllAction)
		self.__menuBar.addMenu(self.__editMenu)

		# Signals / Slots.
		undoAction.triggered.connect(self.__undoAction__triggered)
		redoAction.triggered.connect(self.__redoAction__triggered)
		cutAction.triggered.connect(self.__cutAction__triggered)
		copyAction.triggered.connect(self.__copyAction__triggered)
		pasteAction.triggered.connect(self.__pasteAction__triggered)
		deleteAction.triggered.connect(self.__deleteAction__triggered)
		selectAllAction.triggered.connect(self.__selectAllAction__triggered)

		self.__commandMenu = QMenu("&Command")
		evaluateSelectionAction = QAction("&Evaluate Selection", self)
		evaluateSelectionAction.setShortcut(QKeySequence(Qt.ControlModifier + Qt.Key_Return))
		self.__commandMenu.addAction(evaluateSelectionAction)
		evaluateScriptAction = QAction("Evaluate &Script", self)
		evaluateScriptAction.setShortcut(QKeySequence(Qt.SHIFT + Qt.CTRL + Qt.Key_Return))
		self.__commandMenu.addAction(evaluateScriptAction)
		self.__menuBar.addMenu(self.__commandMenu)

		# Signals / Slots.
		evaluateSelectionAction.triggered.connect(self.__evaluateSelectionAction__triggered)
		evaluateScriptAction.triggered.connect(self.__evaluateScriptAction__triggered)

	# @core.executionTrace
	def __Script_Editor_Output_textEdit_setUi(self):
		"""
		This method sets the **Script_Editor_Output_textEdit** Widget.
		"""

		for line in self.__container.loggingSessionHandlerStream.stream:
			self.ui.Script_Editor_Output_textEdit.moveCursor(QTextCursor.End)
			self.ui.Script_Editor_Output_textEdit.insertPlainText(line)
		self.__Script_Editor_Output_textEdit__setDefaultViewState()

	# @core.executionTrace
	def __Script_Editor_Output_textEdit__setDefaultViewState(self):
		"""
		This method sets the **Script_Editor_Output_textEdit** Widget.
		"""

		self.ui.Script_Editor_Output_textEdit.moveCursor(QTextCursor.End)
		self.ui.Script_Editor_Output_textEdit.ensureCursorVisible()

	# @core.executionTrace
	def __Script_Editor_Output_textEdit_refreshUi(self):
		"""
		This method updates the **Script_Editor_Output_textEdit** Widget.
		"""

		memoryHandlerStackDepth = len(self.__container.loggingSessionHandlerStream.stream)
		if memoryHandlerStackDepth != self.__memoryHandlerStackDepth:
			for line in self.__container.loggingSessionHandlerStream.stream[self.__memoryHandlerStackDepth:memoryHandlerStackDepth]:
				self.ui.Script_Editor_Output_textEdit.moveCursor(QTextCursor.End)
				self.ui.Script_Editor_Output_textEdit.insertPlainText(line)
			self.__Script_Editor_Output_textEdit__setDefaultViewState()
			self.__memoryHandlerStackDepth = memoryHandlerStackDepth

	@core.executionTrace
	def __Lines_Numbers_textEdit_setUi(self):
		"""
		This method sets the **Lines_Numbers_textEdit** Widget.
		"""

		self.ui.Lines_Numbers_textEdit.document().clear()
		for i in range(self.ui.Script_Editor_Input_textEdit.document().lineCount()):
				self.ui.Lines_Numbers_textEdit.setAlignment(Qt.AlignRight)
				self.ui.Lines_Numbers_textEdit.append(str(i + 1))
				self.ui.Lines_Numbers_textEdit.verticalScrollBar().setValue(self.ui.Script_Editor_Input_textEdit.verticalScrollBar().value())

	@core.executionTrace
	def __Lines_Numbers_textEdit_refreshUi(self):
		"""
		This method refreshes the **Lines_Numbers_textEdit** Widget.
		"""

		if self.ui.Script_Editor_Input_textEdit.document().lineCount() != self.ui.Lines_Numbers_textEdit.document().lineCount():
			self.__Lines_Numbers_textEdit_setUi()

	@core.executionTrace
	def __Script_Editor_Input_textEdit__textChanged(self):
		"""
		This method is triggered when **Script_Editor_Input_textEdit** widget text changed.
		"""

		self.__Lines_Numbers_textEdit_refreshUi()

	@core.executionTrace
	def __Script_Editor_Input_textEdit_verticalScrollBar__valueChanged(self, value):
		"""
		This method is triggered when **Script_Editor_Input_textEdit.verticalScrollbar** widget value changed.
		"""

		self.ui.Lines_Numbers_textEdit.verticalScrollBar().setValue(value)

	@core.executionTrace
	def __loadScriptAction__triggered(self, checked):
		"""
		This method is triggered by **loadScriptAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "loadScriptAction"

	@core.executionTrace
	def __sourceScriptAction__triggered(self, checked):
		"""
		This method is triggered by **sourceScriptAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "sourceScriptAction"

	@core.executionTrace
	def __saveScriptAction__triggered(self, checked):
		"""
		This method is triggered by **saveScriptAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "saveScriptAction"

	@core.executionTrace
	def __undoAction__triggered(self, checked):
		"""
		This method is triggered by **undoAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "undoAction"

	@core.executionTrace
	def __redoAction__triggered(self, checked):
		"""
		This method is triggered by **redoAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "redoAction"

	@core.executionTrace
	def __cutAction__triggered(self, checked):
		"""
		This method is triggered by **cutAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "cutAction"

	@core.executionTrace
	def __copyAction__triggered(self, checked):
		"""
		This method is triggered by **copyAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "copyAction"

	@core.executionTrace
	def __pasteAction__triggered(self, checked):
		"""
		This method is triggered by **pasteAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "pasteAction"

	@core.executionTrace
	def __deleteAction__triggered(self, checked):
		"""
		This method is triggered by **deleteAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "deleteAction"

	@core.executionTrace
	def __selectAllAction__triggered(self, checked):
		"""
		This method is triggered by **selectAllAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "selectAllAction"

	@core.executionTrace
	def __evaluateSelectionAction__triggered(self, checked):
		"""
		This method is triggered by **evaluateSelectionAction** action.

		:param checked: Checked state. ( Boolean )
		"""

		print "evaluateSelectionAction"

	@core.executionTrace
	def __evaluateScriptAction__triggered(self, checked):
		"""
		This method is triggered by **evaluateScript** action.

		:param checked: Checked state. ( Boolean )
		"""

		self.evaluateScript()

	@core.executionTrace
	def __Evaluate_Script_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Evaluate_Script_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.evaluateScript()

	@core.executionTrace
	def __getsLocals(self):
		"""
		This method gets the locals for the interactive console.

		:return: Method success. ( Boolean )
		"""

		self.__locals = {}

		for globals in (Constants, RuntimeConstants, UiConstants):
			self.__locals[globals.__name__] = globals

		self.__locals[Constants.applicationName] = self.__container
		self.__locals["componentsManager"] = self.__container.componentsManager

		return True

	@core.executionTrace
	def evaluateScript(self):
		"""
		This method evaluates **Script_Editor_Input_textEdit** widget content in the interactive console.

		:return: Method success. ( Boolean )
		"""

		if self.evaluateCode(str(self.ui.Script_Editor_Input_textEdit.toPlainText())):
			self.emit(SIGNAL("datasChanged()"))
			return True

	@core.executionTrace
	def evaluateCode(self, code):
		"""
		This method evaluates provided code in the interactive console.

		:param code: Code to evaluate. ( String )
		:return: Method success. ( Boolean )
		"""

		sys.stdout.write(code)
		self.__console.runcode(code)

		return True
