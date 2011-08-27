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
from umbra.ui.widgets.menu_QLabel import Menu_QLabel

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
		self.__toolBar = None

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
	def toolBar(self):
		"""
		This method is the property for **self.__toolBar** attribute.

		:return: self.__toolBar. ( QToolbar )
		"""

		return self.__toolBar

	@toolBar.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolBar(self, value):
		"""
		This method is the setter method for **self.__toolBar** attribute.

		:param value: Attribute value. ( QToolbar )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("toolBar"))

	@toolBar.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolBar(self):
		"""
		This method is the deleter method for **self.__toolBar** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("toolBar"))

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

		self.__toolBar = QToolBar()
		self.ui.toolBar_frame_gridLayout.addWidget(self.__toolBar)
		self.__initializeToolbar()

		self.ui.Script_Editor_Input_textEdit.highlighter = PythonHighlighter(self.ui.Script_Editor_Input_textEdit.document())
		self.ui.Script_Editor_Output_textEdit.highlighter = LoggingHighlighter(self.ui.Script_Editor_Output_textEdit.document())

		# Signals / Slots.
		self.__container.timer.timeout.connect(self.__Script_Editor_Output_textEdit_refreshUi)
		self.ui.Evaluate_Script_pushButton.clicked.connect(self.__Evaluate_Script_pushButton__clicked)
		self.datasChanged.connect(self.__Script_Editor_Output_textEdit_refreshUi)

		return True

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__toolBar.setParent(None)
		self.__toolBar = None

		self.ui.Script_Editor_Input_textEdit.highlighter = None
		self.ui.Script_Editor_Output_textEdit.highlighter = None

		# Signals / Slots.
		self.__container.timer.timeout.disconnect(self.__Script_Editor_Output_textEdit_refreshUi)
		self.ui.Evaluate_Script_pushButton.clicked.disconnect(self.__Evaluate_Script_pushButton__clicked)
		self.datasChanged.disconnect(self.__Script_Editor_Output_textEdit_refreshUi)

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
	def __initializeToolbar(self):
		"""
		This method initializes Component toolBar.
		"""

		self.__fileLabel = Menu_QLabel("File", self)
		self.__fileMenu = QMenu()
		loadScriptAction = QAction("&Load script ...", self.__fileMenu)
		loadScriptAction.setShortcut(QKeySequence(QKeySequence.Open))
		self.__fileMenu.addAction(loadScriptAction)
		sourceScriptAction = QAction("&Source script ...", self.__fileMenu)
		self.__fileMenu.addAction(sourceScriptAction)
		saveScriptAction = QAction("&Save script ...", self.__fileMenu)
		saveScriptAction.setShortcut(QKeySequence(QKeySequence.Save))
		self.__fileMenu.addAction(saveScriptAction)
		# Signals / Slots.
		loadScriptAction.triggered.connect(self.__loadScriptAction__triggered)
		sourceScriptAction.triggered.connect(self.__sourceScriptAction__triggered)
		saveScriptAction.triggered.connect(self.__saveScriptAction__triggered)
		self.__fileLabel.setMenu(self.__fileMenu)
		self.__toolBar.addWidget(self.__fileLabel)

		self.__editLabel = Menu_QLabel("Edit", self)
		self.__editMenu = QMenu()
		undoAction = QAction("&Undo", self.__editMenu)
		undoAction.setShortcut(QKeySequence(QKeySequence.Undo))
		self.__editMenu.addAction(undoAction)
		redoAction = QAction("&Redo", self.__editMenu)
		redoAction.setShortcut(QKeySequence(QKeySequence.Redo))
		self.__editMenu.addAction(redoAction)
		self.__editMenu.addSeparator()
		cutAction = QAction("Cu&t", self.__editMenu)
		cutAction.setShortcut(QKeySequence(QKeySequence.Cut))
		self.__editMenu.addAction(cutAction)
		copyAction = QAction("&Copy", self.__editMenu)
		copyAction.setShortcut(QKeySequence(QKeySequence.Copy))
		self.__editMenu.addAction(copyAction)
		pasteAction = QAction("&Paste", self.__editMenu)
		pasteAction.setShortcut(QKeySequence(QKeySequence.Paste))
		self.__editMenu.addAction(pasteAction)
		deleteAction = QAction("Delete", self.__editMenu)
		self.__editMenu.addAction(deleteAction)
		self.__editMenu.addSeparator()
		selectAllAction = QAction("Select All", self.__editMenu)
		selectAllAction.setShortcut(QKeySequence(QKeySequence.SelectAll))
		self.__editMenu.addAction(selectAllAction)
		# Signals / Slots.
		undoAction.triggered.connect(self.__undoAction__triggered)
		redoAction.triggered.connect(self.__redoAction__triggered)
		cutAction.triggered.connect(self.__cutAction__triggered)
		copyAction.triggered.connect(self.__copyAction__triggered)
		pasteAction.triggered.connect(self.__pasteAction__triggered)
		deleteAction.triggered.connect(self.__deleteAction__triggered)
		selectAllAction.triggered.connect(self.__selectAllAction__triggered)
		self.__editLabel.setMenu(self.__editMenu)
		self.__toolBar.addWidget(self.__editLabel)

		self.__commandLabel = Menu_QLabel("Command", self)
		self.__commandMenu = QMenu()
		evaluateSelectionAction = QAction("&Evaluate Selection", self.__commandMenu)
		evaluateSelectionAction.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Enter))
		self.__commandMenu.addAction(evaluateSelectionAction)
		evaluateScriptAction = QAction("Evaluate &Script", self.__commandMenu)
		evaluateScriptAction.setShortcut(QKeySequence(Qt.SHIFT + Qt.CTRL + Qt.Key_Enter))
		self.__commandMenu.addAction(evaluateScriptAction)
		self.__commandLabel.setMenu(self.__commandMenu)
		self.__toolBar.addWidget(self.__commandLabel)

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
	def __Evaluate_Script_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Evaluate_Script_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		sys.stdout.write(str(self.ui.Script_Editor_Input_textEdit.toPlainText()))
		self.__console.runcode(str(self.ui.Script_Editor_Input_textEdit.toPlainText()))

		self.emit(SIGNAL("datasChanged()"))

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
