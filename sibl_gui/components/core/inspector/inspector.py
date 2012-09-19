#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**inspector.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Inspector` Component Interface class and others helpers objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import re
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPen

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.cache
import foundations.common
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import foundations.strings as strings
import sibl_gui.components.core.db.utilities.nodes as dbNodes
import sibl_gui.ui.common
import umbra.ui.common
import umbra.ui.nodes
from foundations.parsers import SectionsFileParser
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.core.inspector.models import PlatesModel
from sibl_gui.components.core.inspector.nodes import PlatesNode
from sibl_gui.components.core.inspector.views import Plates_QListView
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Plate", "Light", "Inspector"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Inspector.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Plate(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for an Ibl Set Plate.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: name, icon, previewImage, image ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class Light(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for an Ibl Set light.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: name, color, uCoordinate, vCoordinate ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class Inspector(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.core.inspector.inspector` Component Interface class.
	| It offers a large preview of the current inspected Ibl Set, and a way to navigate
		into the current selected Database Collection.
	"""

	# Custom signals definitions.
	modelRefresh = pyqtSignal()
	"""
	This signal is emited by the :class:`Inspector` class when :obj:`Inspector.model` class property model
	needs to be refreshed. ( pyqtSignal )
	"""

	uiRefresh = pyqtSignal()
	"""
	This signal is emited by the :class:`Inspector` class when the Ui needs to be refreshed. ( pyqtSignal )
	"""

	uiClear = pyqtSignal()
	"""
	This signal is emited by the :class:`Inspector` class when the Ui needs to be cleared. ( pyqtSignal )
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(Inspector, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiResourcesDirectory = "resources"
		self.__uiPreviousImage = "Previous.png"
		self.__uiNextImage = "Next.png"
		self.__dockArea = 2
		self.__listViewIconSize = 30

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__preferencesManager = None
		self.__databaseBrowser = None

		self.__sectionsFileParsersCache = None

		self.__model = None
		self.__view = None

		self.__inspectorIblSet = None
		self.__inspectorPlates = None

		self.__noPreviewImageText = """
								<center>
								<table border="0" bordercolor="" cellpadding="0" cellspacing="16">
									<tr>
										<td>
											<img src="{0}">
										</td>
										<td>
											<p><b>Preview Image is unavailable!<b></p>
											What now?
											<ul>
												<li>Check For an updated set on <b>HDRLabs</b> at
												<a href="http://www.hdrlabs.com/sibl/archive.html">
												<span style="text-decoration: underline; color:#e0e0e0;">
												http://www.hdrlabs.com/sibl/archive.html</span></a>.</li>
												<li>Contact <b>{1}</b> for an updated Ibl Set: <a href="{2}">
												<span style="text-decoration: underline; color:#e0e0e0;">{2}</span>
												</a></li>
												<li>Resize the background image to 600x300 pixels.<br/>
												Save it as a jpeg in your set directory.<br/>
												Register it in the ."ibl" file header using the "PREVIEWfile" attribute.
												</li>
											</ul>
										</td>
									</tr>
								</table>
								</center>
								"""
		self.__noInspectorIblSetText = """
								<center>
								<table border="0" bordercolor="" cellpadding="0" cellspacing="16">
									<tr>
										<td>
											<img src="{0}">
										</td>
										<td>
											<p><b>No Ibl Set to inspect!<b></p>
											Please add some Ibl Set to the Database or select a non empty Collection!
										</td>
									</tr>
								</table>
								</center>
								"""
		self.__inspectorIblSetToolTipText = """
								<p><b>{0}</b></p>
								<p><b>Author: </b>{1}<br>
								<b>Location: </b>{2}<br>
								<b>Shot Date: </b>{3}<br>
								<b>Comment: </b>{4}</p>
								"""

		self.__lightLabelRadius = 4
		self.__lightLabelTextOffset = 24
		self.__lightLabelTextMargin = 16
		self.__lightLabelTextHeight = 14
		self.__lightLabelTextFont = "Helvetica"
		self.__unnamedLightName = "Unnamed_Light"

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiPreviousImage(self):
		"""
		This method is the property for **self.__uiPreviousImage** attribute.

		:return: self.__uiPreviousImage. ( String )
		"""

		return self.__uiPreviousImage

	@uiPreviousImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self, value):
		"""
		This method is the setter method for **self.__uiPreviousImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self):
		"""
		This method is the deleter method for **self.__uiPreviousImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiPreviousImage"))

	@property
	def uiNextImage(self):
		"""
		This method is the property for **self.__uiNextImage** attribute.

		:return: self.__uiNextImage. ( String )
		"""

		return self.__uiNextImage

	@uiNextImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self, value):
		"""
		This method is the setter method for **self.__uiNextImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self):
		"""
		This method is the deleter method for **self.__uiNextImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiNextImage"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def listViewIconSize(self):
		"""
		This method is the property for **self.__listViewIconSize** attribute.

		:return: self.__listViewIconSize. ( Integer )
		"""

		return self.__listViewIconSize

	@listViewIconSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def listViewIconSize(self, value):
		"""
		This method is the setter method for **self.__listViewIconSize** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("listViewIconSize", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("listViewIconSize", value)
		self.__listViewIconSize = value

	@listViewIconSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def listViewIconSize(self):
		"""
		This method is the deleter method for **self.__listViewIconSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "listViewIconSize"))

	@property
	def engine(self):
		"""
		This method is the property for **self.__engine** attribute.

		:return: self.__engine. ( QObject )
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def databaseBrowser(self):
		"""
		This method is the property for **self.__databaseBrowser** attribute.

		:return: self.__databaseBrowser. ( QWidget )
		"""

		return self.__databaseBrowser

	@databaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseBrowser(self, value):
		"""
		This method is the setter method for **self.__databaseBrowser** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "databaseBrowser"))

	@databaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def databaseBrowser(self):
		"""
		This method is the deleter method for **self.__databaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "databaseBrowser"))

	@property
	def sectionsFileParsersCache(self):
		"""
		This method is the property for **self.__sectionsFileParsersCache** attribute.

		:return: self.__sectionsFileParsersCache. ( Cache )
		"""

		return self.__sectionsFileParsersCache

	@sectionsFileParsersCache.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def sectionsFileParsersCache(self, value):
		"""
		This method is the setter method for **self.__sectionsFileParsersCache** attribute.

		:param value: Attribute value. ( Cache )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "sectionsFileParsersCache"))

	@sectionsFileParsersCache.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def sectionsFileParsersCache(self):
		"""
		This method is the deleter method for **self.__sectionsFileParsersCache** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "sectionsFileParsersCache"))

	@property
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( PlatesModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( PlatesModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def view(self):
		"""
		This method is the property for **self.__view** attribute.

		:return: self.__view. ( QWidget )
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		This method is the setter method for **self.__view** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		This method is the deleter method for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def inspectorIblSet(self):
		"""
		This method is the property for **self.__inspectorIblSet** attribute.

		:return: self.__inspectorIblSet. ( QStandardItem )
		"""

		return self.__inspectorIblSet

	@inspectorIblSet.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSet(self, value):
		"""
		This method is the setter method for **self.__inspectorIblSet** attribute.

		:param value: Attribute value. ( QStandardItem )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorIblSet"))

	@inspectorIblSet.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSet(self):
		"""
		This method is the deleter method for **self.__inspectorIblSet** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorIblSet"))

	@property
	def inspectorPlates(self):
		"""
		This method is the property for **self.__inspectorPlates** attribute.

		:return: self.__inspectorPlates. ( Dictionary )
		"""

		return self.__inspectorPlates

	@inspectorPlates.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorPlates(self, value):
		"""
		This method is the setter method for **self.__inspectorPlates** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorPlates"))

	@inspectorPlates.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorPlates(self):
		"""
		This method is the deleter method for **self.__inspectorPlates** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorPlates"))

	@property
	def noPreviewImageText(self):
		"""
		This method is the property for **self.__noPreviewImageText** attribute.

		:return: self.__noPreviewImageText. ( String )
		"""

		return self.__noPreviewImageText

	@noPreviewImageText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noPreviewImageText(self, value):
		"""
		This method is the setter method for **self.__noPreviewImageText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "noPreviewImageText"))

	@noPreviewImageText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noPreviewImageText(self):
		"""
		This method is the deleter method for **self.__noPreviewImageText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "noPreviewImageText"))

	@property
	def noInspectorIblSetText(self):
		"""
		This method is the property for **self.__noInspectorIblSetText** attribute.

		:return: self.__noInspectorIblSetText. ( String )
		"""

		return self.__noInspectorIblSetText

	@noInspectorIblSetText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noInspectorIblSetText(self, value):
		"""
		This method is the setter method for **self.__noInspectorIblSetText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "noInspectorIblSetText"))

	@noInspectorIblSetText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noInspectorIblSetText(self):
		"""
		This method is the deleter method for **self.__noInspectorIblSetText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "noInspectorIblSetText"))

	@property
	def inspectorIblSetToolTipText(self):
		"""
		This method is the property for **self.__inspectorIblSetToolTipText** attribute.

		:return: self.__inspectorIblSetToolTipText. ( String )
		"""

		return self.__inspectorIblSetToolTipText

	@inspectorIblSetToolTipText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetToolTipText(self, value):
		"""
		This method is the setter method for **self.__inspectorIblSetToolTipText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorIblSetToolTipText"))

	@inspectorIblSetToolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetToolTipText(self):
		"""
		This method is the deleter method for **self.__inspectorIblSetToolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorIblSetToolTipText"))

	@property
	def lightLabelRadius(self):
		"""
		This method is the property for **self.__lightLabelRadius** attribute.

		:return: self.__lightLabelRadius. ( Integer )
		"""

		return self.__lightLabelRadius

	@lightLabelRadius.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelRadius(self, value):
		"""
		This method is the setter method for **self.__lightLabelRadius** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelRadius"))

	@lightLabelRadius.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelRadius(self):
		"""
		This method is the deleter method for **self.__lightLabelRadius** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelRadius"))

	@property
	def lightLabelTextOffset(self):
		"""
		This method is the property for **self.__lightLabelTextOffset** attribute.

		:return: self.__lightLabelTextOffset. ( Integer )
		"""

		return self.__lightLabelTextOffset

	@lightLabelTextOffset.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextOffset(self, value):
		"""
		This method is the setter method for **self.__lightLabelTextOffset** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextOffset"))

	@lightLabelTextOffset.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextOffset(self):
		"""
		This method is the deleter method for **self.__lightLabelTextOffset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextOffset"))

	@property
	def lightLabelTextMargin(self):
		"""
		This method is the property for **self.__lightLabelTextMargin** attribute.

		:return: self.__lightLabelTextMargin. ( Integer )
		"""

		return self.__lightLabelTextMargin

	@lightLabelTextMargin.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextMargin(self, value):
		"""
		This method is the setter method for **self.__lightLabelTextMargin** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextMargin"))

	@lightLabelTextMargin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextMargin(self):
		"""
		This method is the deleter method for **self.__lightLabelTextMargin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextMargin"))

	@property
	def lightLabelTextHeight(self):
		"""
		This method is the property for **self.__lightLabelTextHeight** attribute.

		:return: self.__lightLabelTextHeight. ( Integer )
		"""

		return self.__lightLabelTextHeight

	@lightLabelTextHeight.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextHeight(self, value):
		"""
		This method is the setter method for **self.__lightLabelTextHeight** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextHeight"))

	@lightLabelTextHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextHeight(self):
		"""
		This method is the deleter method for **self.__lightLabelTextHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextHeight"))

	@property
	def lightLabelTextFont(self):
		"""
		This method is the property for **self.__lightLabelTextFont** attribute.

		:return: self.__lightLabelTextFont. ( String )
		"""

		return self.__lightLabelTextFont

	@lightLabelTextFont.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextFont(self, value):
		"""
		This method is the setter method for **self.__lightLabelTextFont** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextFont"))

	@lightLabelTextFont.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextFont(self):
		"""
		This method is the deleter method for **self.__lightLabelTextFont** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextFont"))

	@property
	def unnamedLightName(self):
		"""
		This method is the property for **self.__unnamedLightName** attribute.

		:return: self.__unnamedLightName. ( String )
		"""

		return self.__unnamedLightName

	@unnamedLightName.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def unnamedLightName(self, value):
		"""
		This method is the setter method for **self.__unnamedLightName** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"unnamedLightName", value)
		self.__unnamedLightName = value

	@unnamedLightName.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def unnamedLightName(self):
		"""
		This method is the deleter method for **self.__unnamedLightName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "unnamedLightName"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__),
													self.__uiResourcesDirectory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]
		self.__databaseBrowser = self.__engine.componentsManager["core.databaseBrowser"]

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__sectionsFileParsersCache = foundations.cache.Cache()

		self.__model = PlatesModel()

		self.Plates_listView.setParent(None)
		self.Plates_listView = Plates_QListView(self, self.__model)
		self.Plates_listView.setObjectName("Plates_listView")
		self.Plates_frame_gridLayout.addWidget(self.Plates_listView, 0, 1)
		self.__view = self.Plates_listView
		self.__view.storeModelSelection = self.__view.restoreModelSelection = lambda:True

		self.Previous_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiPreviousImage)))
		self.Next_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiNextImage)))
		self.Previous_Plate_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiPreviousImage)))
		self.Next_Plate_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiNextImage)))

		self.Plates_frame.hide()
		self.Inspector_Options_groupBox.hide()

		self.__Inspector_DockWidget_setUi()

		self.Inspector_Overall_frame.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Inspector_Overall_frame_addActions()

		# Signals / Slots.
		self.__engine.imagesCaches.QIcon.contentAdded.connect(self.__view.viewport().update)
		self.Plates_listView.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.__databaseBrowser.model.modelReset.connect(self.__databaseBrowser__modelReset)
		self.__engine.fileSystemEventsManager.fileChanged.connect(self.__engine_fileSystemEventsManager__fileChanged)
		for view in self.__databaseBrowser.views:
			view.selectionModel().selectionChanged.connect(self.__databaseBrowser_view_selectionModel__selectionChanged)
		self.Previous_Ibl_Set_pushButton.clicked.connect(self.__Previous_Ibl_Set_pushButton__clicked)
		self.Next_Ibl_Set_pushButton.clicked.connect(self.__Next_Ibl_Set_pushButton__clicked)
		self.Previous_Plate_pushButton.clicked.connect(self.__Previous_Plate_pushButton__clicked)
		self.Next_Plate_pushButton.clicked.connect(self.__Next_Plate_pushButton__clicked)
		self.Image_label.linkActivated.connect(self.__Image_label__linkActivated)
		self.modelRefresh.connect(self.__inspector__modelRefresh)
		self.uiRefresh.connect(self.__Inspector_DockWidget_refreshUi)
		self.uiClear.connect(self.__Inspector_DockWidget_clearUi)

		self.initializedUi = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	def __Inspector_DockWidget_setUi(self):
		"""
		This method sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		if self.__inspectorIblSet:
			self.Title_label.setText("<center><b>{0}</b> - {1}</center>".format(self.__inspectorIblSet.title,
																				self.__inspectorIblSet.location))

			if foundations.common.pathExists(self.__inspectorIblSet.previewImage):
				self.Image_label.setPixmap(sibl_gui.ui.common.getPixmap(self.__inspectorIblSet.previewImage,
																		asynchronousLoading=False))
				self.__drawInspectorIblSetOverlay()
			else:
				self.Image_label.setText(self.__noPreviewImageText.format(
				sibl_gui.ui.common.filterImagePath(self.__inspectorIblSet.icon),
				self.__inspectorIblSet.author, self.__inspectorIblSet.link))

			self.Image_label.setToolTip(self.__inspectorIblSetToolTipText.format(
													self.__inspectorIblSet.title,
													self.__inspectorIblSet.author or Constants.nullObject,
													self.__inspectorIblSet.location or Constants.nullObject,
													sibl_gui.ui.common.getFormatedShotDate(self.__inspectorIblSet.date,
																self.__inspectorIblSet.time) or Constants.nullObject,
																self.__inspectorIblSet.comment or Constants.nullObject))

			self.Details_label.setText("<center><b>Comment:</b> {0}</center>".format(self.__inspectorIblSet.comment))

			self.Plates_frame.setVisible(bool(self.__inspectorPlates))
		else:
			self.__Inspector_DockWidget_clearUi()

	@core.executionTrace
	def __Inspector_DockWidget_refreshUi(self):
		"""
		This method sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		self.__Inspector_DockWidget_setUi()

	@core.executionTrace
	def __Inspector_DockWidget_clearUi(self):
		"""
		This method clears the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		self.Title_label.setText(QString())
		self.Image_label.setText(self.__noInspectorIblSetText.format(sibl_gui.ui.common.filterImagePath(unicode())))
		self.Image_label.setToolTip(QString())
		self.Details_label.setText(QString())

		self.Plates_frame.hide()

	@core.executionTrace
	def __Inspector_Overall_frame_addActions(self):
		"""
		This method sets the **Inspector_Overall_frame** actions.
		"""

		pass

	@core.executionTrace
	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when **Plates_listView** Model selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		index = foundations.common.getFirstItem(selectedItems.indexes())
		node = index and self.__model.getNode(index) or None
		if not node:
			return

		if node.family == "Plate":
			self.Image_label.setPixmap(sibl_gui.ui.common.getPixmap(node.plate.previewImage, asynchronousLoading=False))
		else:
			self.uiRefresh.emit()

	@core.executionTrace
	def __databaseBrowser__modelReset(self):
		"""
		This method is triggered when :mod:`sibl_gui.components.core.databaseBrowser.databaseBrowser`
		Component Model has changed.
		"""

		self.__setInspectorIblSet()

	@core.executionTrace
	def __engine_fileSystemEventsManager__fileChanged(self, file):
		"""
		This method is triggered by the **fileSystemEventsManager** when a file is changed.
		
		:param file: File changed. ( String )
		"""

		file = strings.encode(file)
		if file in self.__sectionsFileParsersCache:
			LOGGER.debug("> Removing modified '{0}' file from cache.".format(file))
			self.__sectionsFileParsersCache.removeContent(file)

			if not self.__inspectorIblSet:
				return

			if self.__inspectorIblSet.path == file:
				self.__setInspectorIblSet()
				self.uiRefresh.emit()

	@core.executionTrace
	def __databaseBrowser_view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when :mod:`sibl_gui.components.core.databaseBrowser.databaseBrowser`
		Component Model selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		self.__setInspectorIblSet()

		self.__setInspectorIblSetPlates()
		self.modelRefresh.emit()

		if self.__inspectorIblSet:
			self.uiRefresh.emit()
		else:
			self.uiClear.emit()

	@core.executionTrace
	def __Previous_Ibl_Set_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Previous_Ibl_Set_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughIblSets(True)

	@core.executionTrace
	def __Next_Ibl_Set_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Next_Ibl_Set_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughIblSets()

	@core.executionTrace
	def __Previous_Plate_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Previous_Plate_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughPlates(True)

	@core.executionTrace
	def __Next_Plate_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Next_Plate_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughPlates()

	@core.executionTrace
	def __inspector__modelRefresh(self):
		"""
		This method refreshes the **Plates_listView** Model.
		"""

		self.setPlates()

	@core.executionTrace
	def __Image_label__linkActivated(self, url):
		"""
		This method is triggered when a link is clicked in the **Image_label** Widget.

		:param url: Url to explore. ( QString )
		"""

		QDesktopServices.openUrl(QUrl(url))

	@core.executionTrace
	def __setInspectorIblSet(self):
		"""
		This method sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set.
		"""

		selectedIblSets = self.__databaseBrowser.getSelectedIblSets()
		self.__inspectorIblSet = foundations.common.getFirstItem(selectedIblSets)
		if not self.__inspectorIblSet:
			rootNode = self.__databaseBrowser.model.rootNode
			self.__inspectorIblSet = rootNode.children and foundations.common.getFirstItem(rootNode.children).dbItem
		self.__inspectorIblSet and self.__setInspectorIblSetParser()

	@core.executionTrace
	def __setInspectorIblSetParser(self):
		"""
		This method sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set parser.
		"""

		if foundations.common.pathExists(self.__inspectorIblSet.path):
			LOGGER.debug("> Parsing Inspector Ibl Set file: '{0}'.".format(self.__inspectorIblSet))

			if not self.__sectionsFileParsersCache.getContent(self.__inspectorIblSet.path):
				sectionsFileParser = SectionsFileParser(self.__inspectorIblSet.path)
				sectionsFileParser.read() and sectionsFileParser.parse()
				self.__sectionsFileParsersCache.addContent(**{self.__inspectorIblSet.path : sectionsFileParser})

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def __setInspectorIblSetPlates(self):
		"""
		This method sets the Plates from the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set.
		"""

		path = self.__inspectorIblSet.path
		if not foundations.common.pathExists(path):
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while retrieving Plates: '{1}' Ibl Set file doesn't exists!".format(
			self.__class__.__name__, self.__inspectorIblSet.title))

		sectionsFileParser = self.__sectionsFileParsersCache.getContent(path)
		self.__inspectorPlates = OrderedDict()
		for section in sectionsFileParser.sections:
			if re.search(r"Plate\d+", section):
				self.__inspectorPlates[section] = \
				Plate(name=strings.getSplitextBasename(sectionsFileParser.getValue("PLATEfile", section)),
					icon=os.path.normpath(os.path.join(os.path.dirname(self.__inspectorIblSet.path),
														sectionsFileParser.getValue("PLATEthumb", section))),
					previewImage=os.path.normpath(os.path.join(os.path.dirname(self.__inspectorIblSet.path),
															sectionsFileParser.getValue("PLATEpreview", section))),
					image=os.path.normpath(os.path.join(os.path.dirname(self.__inspectorIblSet.path),
														sectionsFileParser.getValue("PLATEfile", section))))

	@core.executionTrace
	def __drawInspectorIblSetOverlay(self):
		"""
		This method draws an overlay on :obj:`Inspector.Image_Label` Widget.
		"""

		painter = QPainter(self.Image_label.pixmap())
		painter.setRenderHints(QPainter.Antialiasing)
		sectionsFileParser = self.__sectionsFileParsersCache.getContent(self.__inspectorIblSet.path)
		for section in sectionsFileParser.sections:
			if section == "Sun":
				self.__drawLightLabel(painter, Light(name="Sun",
												color=[int(value) for value in sectionsFileParser.getValue(
												"SUNcolor", section).split(",")],
												uCoordinate=float(sectionsFileParser.getValue("SUNu", section)),
												vCoordinate=float(sectionsFileParser.getValue("SUNv", section))))
			elif re.search(r"Light\d+", section):
				self.__drawLightLabel(painter, Light(name=sectionsFileParser.getValue(
												"LIGHTname", section) or self.__unnamedLightName,
												color=[int(value) for value in sectionsFileParser.getValue(
												"LIGHTcolor", section).split(",")],
												uCoordinate=float(sectionsFileParser.getValue("LIGHTu", section)),
												vCoordinate=float(sectionsFileParser.getValue("LIGHTv", section))))
		painter.end()

	@core.executionTrace
	def __drawLightLabel(self, painter, light):
		"""
		This method draws a light label on given QPainter.

		:param painter: QPainter. ( QPainter )
		:param light: Light. ( Light )
		"""

		width = painter.window().width()
		height = painter.window().height()

		lightColorRed, lightColorGreen, lightColorBlue = light.color

		painter.setBrush(QColor(lightColorRed, lightColorGreen, lightColorBlue, 200))
		painter.setPen(QPen(QBrush(QColor(lightColorRed, lightColorGreen, lightColorBlue, 200)), 2))
		font = QFont(self.__lightLabelTextFont, self.__lightLabelTextHeight)
		font.setBold(True)
		painter.setFont(font)

		pointX = int(light.uCoordinate * width)
		pointY = int(light.vCoordinate * height)

		textWidth = painter.fontMetrics().width(light.name.title())
		xLabelTextOffset = pointX + textWidth + self.__lightLabelTextMargin + self.__lightLabelTextOffset > \
		width and -(self.__lightLabelTextOffset + textWidth) or self.__lightLabelTextOffset
		yLabelTextOffset = pointY - \
		(self.__lightLabelTextHeight + self.__lightLabelTextMargin + self.__lightLabelTextOffset) < 0 and \
		- (self.__lightLabelTextOffset + self.__lightLabelTextHeight) or self.__lightLabelTextOffset
		painter.drawText(pointX + xLabelTextOffset, pointY - yLabelTextOffset, light.name.title())

		painter.drawLine(pointX,
						pointY,
						pointX + (xLabelTextOffset < 0 and xLabelTextOffset + textWidth or xLabelTextOffset),
						pointY - (yLabelTextOffset < 0 and yLabelTextOffset + self.__lightLabelTextHeight or yLabelTextOffset))

		painter.drawEllipse(QPoint(pointX, pointY), self.__lightLabelRadius, self.__lightLabelRadius)

		painter.setBrush(Qt.NoBrush)
		painter.setPen(QPen(QBrush(QColor(lightColorRed, lightColorGreen, lightColorBlue, 100)), 2))
		painter.drawEllipse(QPoint(pointX, pointY), self.__lightLabelRadius * 3, self.__lightLabelRadius * 3)
		painter.setPen(QPen(QBrush(QColor(lightColorRed, lightColorGreen, lightColorBlue, 50)), 2))
		painter.drawEllipse(QPoint(pointX, pointY), self.__lightLabelRadius * 4, self.__lightLabelRadius * 4)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setPlates(self):
		"""
		This method sets the Plates Model nodes.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Setting up '{0}' Model!".format("Plates_listView"))

		nodeFlags = attributesFlags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		iblSetNode = dbNodes.IblSetNode(self.__inspectorIblSet,
										name=self.__inspectorIblSet.title,
										parent=rootNode,
										nodeFlags=nodeFlags,
										attributesFlags=attributesFlags)
		iblSetNode.roles[Qt.DisplayRole] = unicode()

		if not self.__inspectorPlates:
			return False

		for name, plate in self.__inspectorPlates.iteritems():
			plateNode = PlatesNode(plate, name=name, parent=rootNode, nodeFlags=nodeFlags, attributesFlags=attributesFlags)
			plateNode.roles[Qt.DisplayRole] = unicode()
			plateNode.roles[Qt.DecorationRole] = plate.icon

		self.__model.initializeModel(rootNode)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def loopThroughIblSets(self, backward=False):
		"""
		This method loops through :mod:`sibl_gui.components.core.databaseBrowser.databaseBrowser` Component Ibl Sets.

		:param backward: Looping backward. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if self.__inspectorIblSet:
			model = self.__databaseBrowser.model

			inspectorIblSetNode = [node for node in model.rootNode.children if node.dbItem.path == self.__inspectorIblSet.path]
			inspectorIblSetNode = foundations.common.getFirstItem(inspectorIblSetNode)
			if not inspectorIblSetNode:
				return True

			row = inspectorIblSetNode.row()

			step = not backward and 1 or -1
			idx = row + step
			if idx < 0:
				idx = model.rootNode.childrenCount() - 1
			elif idx > model.rootNode.childrenCount() - 1:
				idx = 0

			selectionModel = self.__databaseBrowser.getActiveView().selectionModel()
			selectionModel.clear()
			selectionModel.setCurrentIndex(model.index(idx), QItemSelectionModel.Select)
		else:
			self.uiClear.emit()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def loopThroughPlates(self, backward=False):
		"""
		This method loops through :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set Plates.

		:param backward: Looping backward. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		index = foundations.common.getFirstItem(self.Plates_listView.selectedIndexes())
		if index:
			step = not backward and 1 or -1
			idx = index.row() + step
			if idx < 0:
				idx = self.__model.rowCount() - 1
			elif idx > self.__model.rowCount() - 1:
				idx = 0

			selectionModel = self.Plates_listView.selectionModel()
			selectionModel.clear()
			selectionModel.setCurrentIndex(self.__model.index(idx), QItemSelectionModel.Select)
		else:
			self.Plates_listView.setCurrentIndex(self.__model.index(0, 0))
		return True
