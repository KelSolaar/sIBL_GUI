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
import foundations.dataStructures
import foundations.exceptions
import foundations.strings
import foundations.verbose
import sibl_gui.ui.common
import umbra.ui.nodes
from foundations.parsers import SectionsFileParser
from manager.qwidgetComponent import QWidgetComponentFactory
from sibl_gui.components.core.database.nodes import IblSetNode
from sibl_gui.components.core.inspector.models import PlatesModel
from sibl_gui.components.core.inspector.nodes import PlatesNode
from sibl_gui.components.core.inspector.views import Plates_QListView
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Plate", "Light", "Inspector"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Inspector.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Plate(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for an Ibl Set Plate.
	"""

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
	refreshNodes = pyqtSignal()
	"""
	This signal is emited by the :class:`Inspector` class when :obj:`Inspector.model` class property model
	nodes needs to be refreshed. ( pyqtSignal )
	"""

	uiRefresh = pyqtSignal()
	"""
	This signal is emited by the :class:`Inspector` class when the Ui needs to be refreshed. ( pyqtSignal )
	"""

	uiClear = pyqtSignal()
	"""
	This signal is emited by the :class:`Inspector` class when the Ui needs to be cleared. ( pyqtSignal )
	"""

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
		self.__iblSetsOutliner = None

		self.__sectionsFileParsersCache = None

		self.__model = None
		self.__view = None

		self.__activeIblSet = None
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
		self.__noActiveIblSetText = """
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
		self.__activeIblSetToolTipText = """
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self, value):
		"""
		This method is the setter method for **self.__uiPreviousImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiNextImage(self, value):
		"""
		This method is the setter method for **self.__uiNextImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(AssertionError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def iblSetsOutliner(self):
		"""
		This method is the property for **self.__iblSetsOutliner** attribute.

		:return: self.__iblSetsOutliner. ( QWidget )
		"""

		return self.__iblSetsOutliner

	@iblSetsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self, value):
		"""
		This method is the setter method for **self.__iblSetsOutliner** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsOutliner"))

	@iblSetsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self):
		"""
		This method is the deleter method for **self.__iblSetsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsOutliner"))

	@property
	def sectionsFileParsersCache(self):
		"""
		This method is the property for **self.__sectionsFileParsersCache** attribute.

		:return: self.__sectionsFileParsersCache. ( Cache )
		"""

		return self.__sectionsFileParsersCache

	@sectionsFileParsersCache.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def sectionsFileParsersCache(self, value):
		"""
		This method is the setter method for **self.__sectionsFileParsersCache** attribute.

		:param value: Attribute value. ( Cache )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "sectionsFileParsersCache"))

	@sectionsFileParsersCache.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( PlatesModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		This method is the setter method for **self.__view** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		This method is the deleter method for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def activeIblSet(self):
		"""
		This method is the property for **self.__activeIblSet** attribute.

		:return: self.__activeIblSet. ( IblSet )
		"""

		return self.__activeIblSet

	@activeIblSet.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeIblSet(self, value):
		"""
		This method is the setter method for **self.__activeIblSet** attribute.

		:param value: Attribute value. ( IblSet )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "activeIblSet"))

	@activeIblSet.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeIblSet(self):
		"""
		This method is the deleter method for **self.__activeIblSet** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activeIblSet"))

	@property
	def inspectorPlates(self):
		"""
		This method is the property for **self.__inspectorPlates** attribute.

		:return: self.__inspectorPlates. ( Dictionary )
		"""

		return self.__inspectorPlates

	@inspectorPlates.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def inspectorPlates(self, value):
		"""
		This method is the setter method for **self.__inspectorPlates** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorPlates"))

	@inspectorPlates.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def noPreviewImageText(self, value):
		"""
		This method is the setter method for **self.__noPreviewImageText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "noPreviewImageText"))

	@noPreviewImageText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def noPreviewImageText(self):
		"""
		This method is the deleter method for **self.__noPreviewImageText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "noPreviewImageText"))

	@property
	def noActiveIblSetText(self):
		"""
		This method is the property for **self.__noActiveIblSetText** attribute.

		:return: self.__noActiveIblSetText. ( String )
		"""

		return self.__noActiveIblSetText

	@noActiveIblSetText.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def noActiveIblSetText(self, value):
		"""
		This method is the setter method for **self.__noActiveIblSetText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "noActiveIblSetText"))

	@noActiveIblSetText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def noActiveIblSetText(self):
		"""
		This method is the deleter method for **self.__noActiveIblSetText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "noActiveIblSetText"))

	@property
	def activeIblSetToolTipText(self):
		"""
		This method is the property for **self.__activeIblSetToolTipText** attribute.

		:return: self.__activeIblSetToolTipText. ( String )
		"""

		return self.__activeIblSetToolTipText

	@activeIblSetToolTipText.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeIblSetToolTipText(self, value):
		"""
		This method is the setter method for **self.__activeIblSetToolTipText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "activeIblSetToolTipText"))

	@activeIblSetToolTipText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeIblSetToolTipText(self):
		"""
		This method is the deleter method for **self.__activeIblSetToolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activeIblSetToolTipText"))

	@property
	def lightLabelRadius(self):
		"""
		This method is the property for **self.__lightLabelRadius** attribute.

		:return: self.__lightLabelRadius. ( Integer )
		"""

		return self.__lightLabelRadius

	@lightLabelRadius.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelRadius(self, value):
		"""
		This method is the setter method for **self.__lightLabelRadius** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelRadius"))

	@lightLabelRadius.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextOffset(self, value):
		"""
		This method is the setter method for **self.__lightLabelTextOffset** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextOffset"))

	@lightLabelTextOffset.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextMargin(self, value):
		"""
		This method is the setter method for **self.__lightLabelTextMargin** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextMargin"))

	@lightLabelTextMargin.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextHeight(self, value):
		"""
		This method is the setter method for **self.__lightLabelTextHeight** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextHeight"))

	@lightLabelTextHeight.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextFont(self, value):
		"""
		This method is the setter method for **self.__lightLabelTextFont** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextFont"))

	@lightLabelTextFont.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(AssertionError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unnamedLightName(self):
		"""
		This method is the deleter method for **self.__unnamedLightName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "unnamedLightName"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(__file__), self.__uiResourcesDirectory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]
		self.__iblSetsOutliner = self.__engine.componentsManager["core.iblSetsOutliner"]

		self.activated = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

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
		self.__iblSetsOutliner.model.modelReset.connect(self.__iblSetsOutliner__modelReset)
		self.__engine.fileSystemEventsManager.fileChanged.connect(self.__engine_fileSystemEventsManager__fileChanged)
		for view in self.__iblSetsOutliner.views:
			view.selectionModel().selectionChanged.connect(self.__iblSetsOutliner_view_selectionModel__selectionChanged)
		self.Previous_Ibl_Set_pushButton.clicked.connect(self.__Previous_Ibl_Set_pushButton__clicked)
		self.Next_Ibl_Set_pushButton.clicked.connect(self.__Next_Ibl_Set_pushButton__clicked)
		self.Previous_Plate_pushButton.clicked.connect(self.__Previous_Plate_pushButton__clicked)
		self.Next_Plate_pushButton.clicked.connect(self.__Next_Plate_pushButton__clicked)
		self.Image_label.linkActivated.connect(self.__Image_label__linkActivated)
		self.refreshNodes.connect(self.__model__refreshNodes)
		self.uiRefresh.connect(self.__Inspector_DockWidget_refreshUi)
		self.uiClear.connect(self.__Inspector_DockWidget_clearUi)

		self.initializedUi = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	def __Inspector_DockWidget_setUi(self):
		"""
		This method sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		if self.__activeIblSet:
			self.Title_label.setText("<center><b>{0}</b> - {1}</center>".format(self.__activeIblSet.title,
																				self.__activeIblSet.location))

			if foundations.common.pathExists(self.__activeIblSet.previewImage):
				self.Image_label.setPixmap(sibl_gui.ui.common.getPixmap(self.__activeIblSet.previewImage,
																		asynchronousLoading=False))
				self.__drawActiveIblSetOverlay()
			else:
				self.Image_label.setText(self.__noPreviewImageText.format(
				sibl_gui.ui.common.filterImagePath(self.__activeIblSet.icon),
				self.__activeIblSet.author, self.__activeIblSet.link))

			self.Image_label.setToolTip(self.__activeIblSetToolTipText.format(
													self.__activeIblSet.title,
													self.__activeIblSet.author or Constants.nullObject,
													self.__activeIblSet.location or Constants.nullObject,
													sibl_gui.ui.common.getFormatedShotDate(self.__activeIblSet.date,
																self.__activeIblSet.time) or Constants.nullObject,
																self.__activeIblSet.comment or Constants.nullObject))

			self.Details_label.setText("<center><b>Comment:</b> {0}</center>".format(self.__activeIblSet.comment))

			self.Plates_frame.setVisible(bool(self.__inspectorPlates))
		else:
			self.__Inspector_DockWidget_clearUi()

	def __Inspector_DockWidget_refreshUi(self):
		"""
		This method sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		self.__Inspector_DockWidget_setUi()

	def __Inspector_DockWidget_clearUi(self):
		"""
		This method clears the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		self.Title_label.setText(QString())
		self.Image_label.setText(self.__noActiveIblSetText.format(sibl_gui.ui.common.filterImagePath(unicode())))
		self.Image_label.setToolTip(QString())
		self.Details_label.setText(QString())

		self.Plates_frame.hide()

	def __Inspector_Overall_frame_addActions(self):
		"""
		This method sets the **Inspector_Overall_frame** actions.
		"""

		pass

	def __model__refreshNodes(self):
		"""
		This method refreshes the **Plates_listView** Model nodes.
		"""

		self.setPlates()

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

	def __engine_fileSystemEventsManager__fileChanged(self, file):
		"""
		This method is triggered by the **fileSystemEventsManager** when a file is changed.
		
		:param file: File changed. ( String )
		"""

		file = foundations.strings.encode(file)
		if file in self.__sectionsFileParsersCache:
			LOGGER.debug("> Removing modified '{0}' file from cache.".format(file))
			self.__sectionsFileParsersCache.removeContent(file)

			if not self.__activeIblSet:
				return

			if self.__activeIblSet.path == file:
				self.__setActiveIblSet()
				self.uiRefresh.emit()

	def __iblSetsOutliner__modelReset(self):
		"""
		This method is triggered when :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner`
		Component Model has changed.
		"""

		self.__setActiveIblSet()

	def __iblSetsOutliner_view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner`
		Component Model selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		self.__setActiveIblSet()

		self.__setActiveIblSetPlates()
		self.refreshNodes.emit()

		if self.__activeIblSet:
			self.uiRefresh.emit()
		else:
			self.uiClear.emit()

	def __Previous_Ibl_Set_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Previous_Ibl_Set_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughIblSets(True)

	def __Next_Ibl_Set_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Next_Ibl_Set_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughIblSets()

	def __Previous_Plate_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Previous_Plate_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughPlates(True)

	def __Next_Plate_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Next_Plate_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.loopThroughPlates()

	def __Image_label__linkActivated(self, url):
		"""
		This method is triggered when a link is clicked in the **Image_label** Widget.

		:param url: Url to explore. ( QString )
		"""

		QDesktopServices.openUrl(QUrl(url))

	def __setActiveIblSet(self):
		"""
		This method sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set.
		"""

		selectedIblSets = self.__iblSetsOutliner.getSelectedIblSets()
		self.__activeIblSet = foundations.common.getFirstItem(selectedIblSets)
		if not self.__activeIblSet:
			rootNode = self.__iblSetsOutliner.model.rootNode
			self.__activeIblSet = rootNode.children and foundations.common.getFirstItem(rootNode.children).databaseItem
		self.__activeIblSet and self.__setActiveIblSetParser()

	def __setActiveIblSetParser(self):
		"""
		This method sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set parser.
		"""

		if foundations.common.pathExists(self.__activeIblSet.path):
			LOGGER.debug("> Parsing Inspector Ibl Set file: '{0}'.".format(self.__activeIblSet))

			if not self.__sectionsFileParsersCache.getContent(self.__activeIblSet.path):
				sectionsFileParser = SectionsFileParser(self.__activeIblSet.path)
				sectionsFileParser.read() and sectionsFileParser.parse()
				self.__sectionsFileParsersCache.addContent(**{str(self.__activeIblSet.path) : sectionsFileParser})

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def __setActiveIblSetPlates(self):
		"""
		This method sets the Plates from the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set.
		"""

		path = self.__activeIblSet.path
		if not foundations.common.pathExists(path):
			raise foundations.exceptions.FileExistsError(
			"{0} | Exception raised while retrieving Plates: '{1}' Ibl Set file doesn't exists!".format(
			self.__class__.__name__, self.__activeIblSet.title))

		sectionsFileParser = self.__sectionsFileParsersCache.getContent(path)
		self.__inspectorPlates = OrderedDict()
		for section in sectionsFileParser.sections:
			if re.search(r"Plate\d+", section):
				self.__inspectorPlates[section] = \
				Plate(name=foundations.strings.getSplitextBasename(sectionsFileParser.getValue("PLATEfile", section)),
					icon=os.path.normpath(os.path.join(os.path.dirname(self.__activeIblSet.path),
														sectionsFileParser.getValue("PLATEthumb", section))),
					previewImage=os.path.normpath(os.path.join(os.path.dirname(self.__activeIblSet.path),
															sectionsFileParser.getValue("PLATEpreview", section))),
					image=os.path.normpath(os.path.join(os.path.dirname(self.__activeIblSet.path),
														sectionsFileParser.getValue("PLATEfile", section))))

	@foundations.exceptions.handleExceptions(foundations.exceptions.ExecutionError)
	def __drawActiveIblSetOverlay(self):
		"""
		This method draws an overlay on :obj:`Inspector.Image_Label` Widget.
		"""

		painter = QPainter(self.Image_label.pixmap())
		painter.setRenderHints(QPainter.Antialiasing)

		iblSetPath = self.__activeIblSet.path
		sectionsFileParser = self.__sectionsFileParsersCache.getContent(iblSetPath)
		if sectionsFileParser is None:
			raise foundations.exceptions.ExecutionError(
			"'{1}' Ibl Set file 'SectionsFileParser' instance not found!".format(iblSetPath))

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
		xLabelTextOffset = -(self.__lightLabelTextOffset + textWidth) if \
						pointX + textWidth + self.__lightLabelTextMargin + self.__lightLabelTextOffset > width else \
						self.__lightLabelTextOffset
		yLabelTextOffset = -(self.__lightLabelTextOffset + self.__lightLabelTextHeight) if \
						pointY - (self.__lightLabelTextHeight + self.__lightLabelTextMargin + self.__lightLabelTextOffset) < 0 else \
						self.__lightLabelTextOffset
		painter.drawText(pointX + xLabelTextOffset, pointY - yLabelTextOffset, light.name.title())

		painter.drawLine(pointX,
						pointY,
						pointX + (xLabelTextOffset + textWidth if xLabelTextOffset < 0 else xLabelTextOffset),
						pointY - (yLabelTextOffset + self.__lightLabelTextHeight \
								if yLabelTextOffset < 0 else yLabelTextOffset))

		painter.drawEllipse(QPoint(pointX, pointY), self.__lightLabelRadius, self.__lightLabelRadius)

		painter.setBrush(Qt.NoBrush)
		painter.setPen(QPen(QBrush(QColor(lightColorRed, lightColorGreen, lightColorBlue, 100)), 2))
		painter.drawEllipse(QPoint(pointX, pointY), self.__lightLabelRadius * 3, self.__lightLabelRadius * 3)
		painter.setPen(QPen(QBrush(QColor(lightColorRed, lightColorGreen, lightColorBlue, 50)), 2))
		painter.drawEllipse(QPoint(pointX, pointY), self.__lightLabelRadius * 4, self.__lightLabelRadius * 4)

	def setPlates(self):
		"""
		This method sets the Plates Model nodes.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Setting up '{0}' Model!".format("Plates_listView"))

		nodeFlags = attributesFlags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		iblSetNode = IblSetNode(self.__activeIblSet,
								name=self.__activeIblSet.title,
								parent=rootNode,
								nodeFlags=nodeFlags,
								attributesFlags=attributesFlags)
		iblSetNode.roles[Qt.DisplayRole] = unicode()

		if not self.__inspectorPlates:
			return False

		for name, plate in self.__inspectorPlates.iteritems():
			plateNode = PlatesNode(plate,
								name=name,
								parent=rootNode,
								nodeFlags=nodeFlags,
								attributesFlags=attributesFlags)
			plateNode.roles[Qt.DisplayRole] = unicode()
			plateNode.roles[Qt.DecorationRole] = plate.icon

		self.__model.initializeModel(rootNode)
		return True

	def loopThroughIblSets(self, backward=False):
		"""
		This method loops through :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner` Component Ibl Sets.

		:param backward: Looping backward. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if self.__activeIblSet:
			model = self.__iblSetsOutliner.model

			activeIblSetNode = [node for node in model.rootNode.children if node.databaseItem.path == self.__activeIblSet.path]
			activeIblSetNode = foundations.common.getFirstItem(activeIblSetNode)
			if not activeIblSetNode:
				return True

			row = activeIblSetNode.row()

			step = not backward and 1 or -1
			idx = row + step
			if idx < 0:
				idx = model.rootNode.childrenCount() - 1
			elif idx > model.rootNode.childrenCount() - 1:
				idx = 0

			selectionModel = self.__iblSetsOutliner.getActiveView().selectionModel()
			selectionModel.clear()
			selectionModel.setCurrentIndex(model.index(idx), QItemSelectionModel.Select)
		else:
			self.uiClear.emit()
		return True

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
