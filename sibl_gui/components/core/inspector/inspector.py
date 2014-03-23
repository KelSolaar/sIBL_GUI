#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**inspector.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Inspector` Component Interface class and others helpers objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines a storage object for an Ibl Set Plate.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: name, icon, previewImage, image
		:type kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class Light(foundations.dataStructures.Structure):
	"""
	Defines a storage object for an Ibl Set light.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: name, color, uCoordinate, vCoordinate
		:type kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class Inspector(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.core.inspector.inspector` Component Interface class.
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
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param name: Component name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(Inspector, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiResourcesDirectory = "resources"
		self.__uiPreviousImage = "Previous.png"
		self.__uiNextImage = "Next.png"
		self.__uiLoadingImage = "Loading.png"
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

		self.__thumbnailsSize = "Special1"

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

		self.__pixmapPlaceholder = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def uiResourcesDirectory(self):
		"""
		Property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory.
		:rtype: unicode
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		Setter for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		Deleter for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@property
	def uiPreviousImage(self):
		"""
		Property for **self.__uiPreviousImage** attribute.

		:return: self.__uiPreviousImage.
		:rtype: unicode
		"""

		return self.__uiPreviousImage

	@uiPreviousImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self, value):
		"""
		Setter for **self.__uiPreviousImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self):
		"""
		Deleter for **self.__uiPreviousImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiPreviousImage"))

	@property
	def uiNextImage(self):
		"""
		Property for **self.__uiNextImage** attribute.

		:return: self.__uiNextImage.
		:rtype: unicode
		"""

		return self.__uiNextImage

	@uiNextImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiNextImage(self, value):
		"""
		Setter for **self.__uiNextImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiNextImage(self):
		"""
		Deleter for **self.__uiNextImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiNextImage"))

	@property
	def uiLoadingImage(self):
		"""
		Property for **self.__uiLoadingImage** attribute.

		:return: self.__uiLoadingImage.
		:rtype: unicode
		"""

		return self.__uiLoadingImage

	@uiLoadingImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiLoadingImage(self, value):
		"""
		Setter for **self.__uiLoadingImage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLoadingImage"))

	@uiLoadingImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiLoadingImage(self):
		"""
		Deleter for **self.__uiLoadingImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiLoadingImage"))

	@property
	def dockArea(self):
		"""
		Property for **self.__dockArea** attribute.

		:return: self.__dockArea.
		:rtype: int
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		Setter for **self.__dockArea** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		Deleter for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def listViewIconSize(self):
		"""
		Property for **self.__listViewIconSize** attribute.

		:return: self.__listViewIconSize.
		:rtype: int
		"""

		return self.__listViewIconSize

	@listViewIconSize.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def listViewIconSize(self, value):
		"""
		Setter for **self.__listViewIconSize** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("listViewIconSize", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("listViewIconSize", value)
		self.__listViewIconSize = value

	@listViewIconSize.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def listViewIconSize(self):
		"""
		Deleter for **self.__listViewIconSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "listViewIconSize"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def iblSetsOutliner(self):
		"""
		Property for **self.__iblSetsOutliner** attribute.

		:return: self.__iblSetsOutliner.
		:rtype: QWidget
		"""

		return self.__iblSetsOutliner

	@iblSetsOutliner.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self, value):
		"""
		Setter for **self.__iblSetsOutliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "iblSetsOutliner"))

	@iblSetsOutliner.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def iblSetsOutliner(self):
		"""
		Deleter for **self.__iblSetsOutliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "iblSetsOutliner"))

	@property
	def sectionsFileParsersCache(self):
		"""
		Property for **self.__sectionsFileParsersCache** attribute.

		:return: self.__sectionsFileParsersCache.
		:rtype: Cache
		"""

		return self.__sectionsFileParsersCache

	@sectionsFileParsersCache.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def sectionsFileParsersCache(self, value):
		"""
		Setter for **self.__sectionsFileParsersCache** attribute.

		:param value: Attribute value.
		:type value: Cache
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "sectionsFileParsersCache"))

	@sectionsFileParsersCache.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def sectionsFileParsersCache(self):
		"""
		Deleter for **self.__sectionsFileParsersCache** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "sectionsFileParsersCache"))

	@property
	def model(self):
		"""
		Property for **self.__model** attribute.

		:return: self.__model.
		:rtype: PlatesModel
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		Setter for **self.__model** attribute.

		:param value: Attribute value.
		:type value: PlatesModel
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		Deleter for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def view(self):
		"""
		Property for **self.__view** attribute.

		:return: self.__view.
		:rtype: QWidget
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		Setter for **self.__view** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		Deleter for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def thumbnailsSize(self):
		"""
		Property for **self.__thumbnailsSize** attribute.

		:return: self.__thumbnailsSize.
		:rtype: unicode
		"""

		return self.__thumbnailsSize

	@thumbnailsSize.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def thumbnailsSize(self, value):
		"""
		Setter for **self.__thumbnailsSize** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("thumbnailsSize",
																								  value)
		self.__thumbnailsSize = value

	@thumbnailsSize.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def thumbnailsSize(self):
		"""
		Deleter for **self.__thumbnailsSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "thumbnailsSize"))

	@property
	def activeIblSet(self):
		"""
		Property for **self.__activeIblSet** attribute.

		:return: self.__activeIblSet.
		:rtype: IblSet
		"""

		return self.__activeIblSet

	@activeIblSet.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeIblSet(self, value):
		"""
		Setter for **self.__activeIblSet** attribute.

		:param value: Attribute value.
		:type value: IblSet
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "activeIblSet"))

	@activeIblSet.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeIblSet(self):
		"""
		Deleter for **self.__activeIblSet** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activeIblSet"))

	@property
	def inspectorPlates(self):
		"""
		Property for **self.__inspectorPlates** attribute.

		:return: self.__inspectorPlates.
		:rtype: dict
		"""

		return self.__inspectorPlates

	@inspectorPlates.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def inspectorPlates(self, value):
		"""
		Setter for **self.__inspectorPlates** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorPlates"))

	@inspectorPlates.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def inspectorPlates(self):
		"""
		Deleter for **self.__inspectorPlates** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorPlates"))

	@property
	def noPreviewImageText(self):
		"""
		Property for **self.__noPreviewImageText** attribute.

		:return: self.__noPreviewImageText.
		:rtype: unicode
		"""

		return self.__noPreviewImageText

	@noPreviewImageText.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def noPreviewImageText(self, value):
		"""
		Setter for **self.__noPreviewImageText** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "noPreviewImageText"))

	@noPreviewImageText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def noPreviewImageText(self):
		"""
		Deleter for **self.__noPreviewImageText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "noPreviewImageText"))

	@property
	def noActiveIblSetText(self):
		"""
		Property for **self.__noActiveIblSetText** attribute.

		:return: self.__noActiveIblSetText.
		:rtype: unicode
		"""

		return self.__noActiveIblSetText

	@noActiveIblSetText.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def noActiveIblSetText(self, value):
		"""
		Setter for **self.__noActiveIblSetText** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "noActiveIblSetText"))

	@noActiveIblSetText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def noActiveIblSetText(self):
		"""
		Deleter for **self.__noActiveIblSetText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "noActiveIblSetText"))

	@property
	def activeIblSetToolTipText(self):
		"""
		Property for **self.__activeIblSetToolTipText** attribute.

		:return: self.__activeIblSetToolTipText.
		:rtype: unicode
		"""

		return self.__activeIblSetToolTipText

	@activeIblSetToolTipText.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeIblSetToolTipText(self, value):
		"""
		Setter for **self.__activeIblSetToolTipText** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "activeIblSetToolTipText"))

	@activeIblSetToolTipText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeIblSetToolTipText(self):
		"""
		Deleter for **self.__activeIblSetToolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activeIblSetToolTipText"))

	@property
	def lightLabelRadius(self):
		"""
		Property for **self.__lightLabelRadius** attribute.

		:return: self.__lightLabelRadius.
		:rtype: int
		"""

		return self.__lightLabelRadius

	@lightLabelRadius.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelRadius(self, value):
		"""
		Setter for **self.__lightLabelRadius** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelRadius"))

	@lightLabelRadius.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelRadius(self):
		"""
		Deleter for **self.__lightLabelRadius** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelRadius"))

	@property
	def lightLabelTextOffset(self):
		"""
		Property for **self.__lightLabelTextOffset** attribute.

		:return: self.__lightLabelTextOffset.
		:rtype: int
		"""

		return self.__lightLabelTextOffset

	@lightLabelTextOffset.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextOffset(self, value):
		"""
		Setter for **self.__lightLabelTextOffset** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextOffset"))

	@lightLabelTextOffset.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextOffset(self):
		"""
		Deleter for **self.__lightLabelTextOffset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextOffset"))

	@property
	def lightLabelTextMargin(self):
		"""
		Property for **self.__lightLabelTextMargin** attribute.

		:return: self.__lightLabelTextMargin.
		:rtype: int
		"""

		return self.__lightLabelTextMargin

	@lightLabelTextMargin.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextMargin(self, value):
		"""
		Setter for **self.__lightLabelTextMargin** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextMargin"))

	@lightLabelTextMargin.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextMargin(self):
		"""
		Deleter for **self.__lightLabelTextMargin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextMargin"))

	@property
	def lightLabelTextHeight(self):
		"""
		Property for **self.__lightLabelTextHeight** attribute.

		:return: self.__lightLabelTextHeight.
		:rtype: int
		"""

		return self.__lightLabelTextHeight

	@lightLabelTextHeight.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextHeight(self, value):
		"""
		Setter for **self.__lightLabelTextHeight** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextHeight"))

	@lightLabelTextHeight.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextHeight(self):
		"""
		Deleter for **self.__lightLabelTextHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextHeight"))

	@property
	def lightLabelTextFont(self):
		"""
		Property for **self.__lightLabelTextFont** attribute.

		:return: self.__lightLabelTextFont.
		:rtype: unicode
		"""

		return self.__lightLabelTextFont

	@lightLabelTextFont.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextFont(self, value):
		"""
		Setter for **self.__lightLabelTextFont** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextFont"))

	@lightLabelTextFont.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def lightLabelTextFont(self):
		"""
		Deleter for **self.__lightLabelTextFont** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextFont"))

	@property
	def unnamedLightName(self):
		"""
		Property for **self.__unnamedLightName** attribute.

		:return: self.__unnamedLightName.
		:rtype: unicode
		"""

		return self.__unnamedLightName

	@unnamedLightName.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def unnamedLightName(self, value):
		"""
		Setter for **self.__unnamedLightName** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"unnamedLightName", value)
		self.__unnamedLightName = value

	@unnamedLightName.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unnamedLightName(self):
		"""
		Deleter for **self.__unnamedLightName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "unnamedLightName"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Engine to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
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
		Deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	def initializeUi(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__pixmapPlaceholder = \
			sibl_gui.ui.common.getPixmap(os.path.join(self.__uiResourcesDirectory, self.__uiLoadingImage),
										 asynchronousLoading=False)

		self.__sectionsFileParsersCache = foundations.cache.Cache()

		self.__model = PlatesModel()

		self.Plates_listView.setParent(None)
		self.Plates_listView = Plates_QListView(self, self.__model)
		self.Plates_listView.setObjectName("Plates_listView")
		self.Plates_frame_gridLayout.addWidget(self.Plates_listView, 0, 1)
		self.__view = self.Plates_listView
		self.__view.storeModelSelection = self.__view.restoreModelSelection = lambda: True

		self.Previous_Ibl_Set_pushButton.setIcon(
			QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiPreviousImage)))
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
		self.__engine.imagesCaches.QPixmap.contentAdded.connect(self.__engine_imagesCaches_QPixmap__contentAdded)
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
		Uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	def __Inspector_DockWidget_setUi(self):
		"""
		Sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		if self.__activeIblSet:
			self.Title_label.setText("<center><b>{0}</b> - {1}</center>".format(self.__activeIblSet.title,
																				self.__activeIblSet.location))

			previewAvailable = False
			if foundations.common.pathExists(self.__activeIblSet.previewImage):
				pixmap = sibl_gui.ui.common.getPixmap(self.__activeIblSet.previewImage)
				previewAvailable = True
			else:
				if foundations.common.pathExists(self.__activeIblSet.backgroundImage):
					pixmap = sibl_gui.ui.common.getPixmap(self.__activeIblSet.backgroundImage,
														  size=self.__thumbnailsSize,
														  placeholder=self.__pixmapPlaceholder)
					previewAvailable = True

			if previewAvailable:
				self.Image_label.setPixmap(pixmap)
				self.__drawActiveIblSetOverlay()
			else:
				self.Image_label.setText(self.__noPreviewImageText.format(
					sibl_gui.ui.common.filterImagePath(self.__activeIblSet.icon),
					self.__activeIblSet.author,
					self.__activeIblSet.link))

			self.Image_label.setToolTip(self.__activeIblSetToolTipText.format(
				self.__activeIblSet.title,
				self.__activeIblSet.author or Constants.nullObject,
				self.__activeIblSet.location or Constants.nullObject,
				sibl_gui.ui.common.getFormattedShotDate(self.__activeIblSet.date,
													   self.__activeIblSet.time) or Constants.nullObject,
				self.__activeIblSet.comment or Constants.nullObject))

			self.Details_label.setText("<center><b>Comment:</b> {0}</center>".format(self.__activeIblSet.comment))

			self.Plates_frame.setVisible(bool(self.__inspectorPlates))
		else:
			self.__Inspector_DockWidget_clearUi()

	def __Inspector_DockWidget_refreshUi(self):
		"""
		Sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		self.__Inspector_DockWidget_setUi()

	def __Inspector_DockWidget_clearUi(self):
		"""
		Clears the :mod:`sibl_gui.components.core.inspector.inspector` Component Widget ui.
		"""

		self.Title_label.setText(QString())
		self.Image_label.setText(self.__noActiveIblSetText.format(sibl_gui.ui.common.filterImagePath("")))
		self.Image_label.setToolTip(QString())
		self.Details_label.setText(QString())

		self.Plates_frame.hide()

	def __Inspector_Overall_frame_addActions(self):
		"""
		Sets the **Inspector_Overall_frame** actions.
		"""

		pass

	def __model__refreshNodes(self):
		"""
		Refreshes the **Plates_listView** Model nodes.
		"""

		self.setPlates()

	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		Defines the slot triggered by **Plates_listView** when Model selection has changed.

		:param selectedItems: Selected items.
		:type selectedItems: QItemSelection
		:param deselectedItems: Deselected items.
		:type deselectedItems: QItemSelection
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
		Defines the slot triggered by the **fileSystemEventsManager** when a file is changed.

		:param file: File changed.
		:type file: unicode
		"""

		file = foundations.strings.toString(file)
		if file in self.__sectionsFileParsersCache:
			LOGGER.debug("> Removing modified '{0}' file from cache.".format(file))
			self.__sectionsFileParsersCache.removeContent(file)

			if not self.__activeIblSet:
				return

			if self.__activeIblSet.path == file:
				self.__setActiveIblSet()
				self.uiRefresh.emit()

	def __engine_imagesCaches_QPixmap__contentAdded(self, paths):
		"""
		Defines the slot triggered by the **QPixmap** images cache when content is added.

		:param paths: Added content.
		:type paths: list
		"""

		if not self.__activeIblSet:
			return

		if foundations.common.getFirstItem(paths) in (self.__activeIblSet.previewImage,
													  self.__activeIblSet.backgroundImage):
			self.__Inspector_DockWidget_setUi()

	def __iblSetsOutliner__modelReset(self):
		"""
		Defines the slot triggered by :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner`
		Component Model when changed.
		"""

		self.__setActiveIblSet()

	def __iblSetsOutliner_view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		Defines the slot triggered by :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner`
		Component Model selection when changed.

		:param selectedItems: Selected items.
		:type selectedItems: QItemSelection
		:param deselectedItems: Deselected items.
		:type deselectedItems: QItemSelection
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
		Defines the slot triggered by **Previous_Ibl_Set_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loopThroughIblSets(True)

	def __Next_Ibl_Set_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Next_Ibl_Set_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loopThroughIblSets()

	def __Previous_Plate_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Previous_Plate_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loopThroughPlates(True)

	def __Next_Plate_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Next_Plate_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.loopThroughPlates()

	def __Image_label__linkActivated(self, url):
		"""
		Defines the slot triggered by **Image_label** Widget when a link is clicked.

		:param url: Url to explore.
		:type url: QString
		"""

		QDesktopServices.openUrl(QUrl(url))

	def __setActiveIblSet(self):
		"""
		Sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set.
		"""

		selectedIblSets = self.__iblSetsOutliner.getSelectedIblSets()
		self.__activeIblSet = foundations.common.getFirstItem(selectedIblSets)
		if not self.__activeIblSet:
			rootNode = self.__iblSetsOutliner.model.rootNode
			childNode = foundations.common.getFirstItem(rootNode.children)
			self.__activeIblSet = childNode.databaseItem if childNode is not None else None
		self.__activeIblSet and self.__setActiveIblSetParser()

	def __setActiveIblSetParser(self):
		"""
		Sets the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set parser.
		"""

		if foundations.common.pathExists(self.__activeIblSet.path):
			LOGGER.debug("> Parsing Inspector Ibl Set file: '{0}'.".format(self.__activeIblSet))

			if not self.__sectionsFileParsersCache.getContent(self.__activeIblSet.path):
				sectionsFileParser = SectionsFileParser(self.__activeIblSet.path)
				sectionsFileParser.parse()
				self.__sectionsFileParsersCache.addContent(**{self.__activeIblSet.path: sectionsFileParser})

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def __setActiveIblSetPlates(self):
		"""
		Sets the Plates from the :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set.
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
					Plate(
						name=foundations.strings.getSplitextBasename(sectionsFileParser.getValue("PLATEfile", section)),
						icon=os.path.normpath(os.path.join(os.path.dirname(self.__activeIblSet.path),
														   sectionsFileParser.getValue("PLATEthumb", section))),
						previewImage=os.path.normpath(os.path.join(os.path.dirname(self.__activeIblSet.path),
																   sectionsFileParser.getValue("PLATEpreview",
																							   section))),
						image=os.path.normpath(os.path.join(os.path.dirname(self.__activeIblSet.path),
															sectionsFileParser.getValue("PLATEfile", section))))

	@foundations.exceptions.handleExceptions(foundations.exceptions.ExecutionError, ValueError)
	def __drawActiveIblSetOverlay(self):
		"""
		Draws an overlay on :obj:`Inspector.Image_Label` Widget.
		"""

		painter = QPainter(self.Image_label.pixmap())
		painter.setRenderHints(QPainter.Antialiasing)

		iblSetPath = self.__activeIblSet.path
		sectionsFileParser = self.__sectionsFileParsersCache.getContent(iblSetPath)
		if sectionsFileParser is None:
			raise foundations.exceptions.ExecutionError(
				"'{0}' Ibl Set file 'SectionsFileParser' instance not found!".format(iblSetPath))

		for section in sectionsFileParser.sections:
			if section == "Sun":
				self.__drawLightLabel(painter,
									  Light(name="Sun",
											color=[int(value) for value in sectionsFileParser.getValue(
												"SUNcolor", section).split(",")],
											uCoordinate=float(sectionsFileParser.getValue("SUNu", section)),
											vCoordinate=float(sectionsFileParser.getValue("SUNv", section))))

			elif re.search(r"Light\d+", section):
				self.__drawLightLabel(painter, Light(name=sectionsFileParser.getValue(
					"LIGHTname", section) or self.__unnamedLightName,
													 color=[int(value) for value in sectionsFileParser.getValue(
														 "LIGHTcolor", section).split(",")],
													 uCoordinate=float(
														 sectionsFileParser.getValue("LIGHTu", section)),
													 vCoordinate=float(
														 sectionsFileParser.getValue("LIGHTv", section))))

		painter.end()

	def __drawLightLabel(self, painter, light):
		"""
		Draws a light label on given QPainter.

		:param painter: QPainter.
		:type painter: QPainter
		:param light: Light.
		:type light: Light
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
		Sets the Plates Model nodes.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Setting up '{0}' Model!".format("Plates_listView"))

		nodeFlags = attributesFlags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		iblSetNode = IblSetNode(self.__activeIblSet,
								name=self.__activeIblSet.title,
								parent=rootNode,
								nodeFlags=nodeFlags,
								attributesFlags=attributesFlags,
								iconPath = self.__activeIblSet.icon)
		iblSetNode.roles[Qt.DisplayRole] = ""

		if not self.__inspectorPlates:
			return False

		for name, plate in self.__inspectorPlates.iteritems():
			plateNode = PlatesNode(plate,
								   name=name,
								   parent=rootNode,
								   nodeFlags=nodeFlags,
								   attributesFlags=attributesFlags)
			plateNode.roles[Qt.DisplayRole] = ""
			plateNode.roles[Qt.DecorationRole] = foundations.common.filterPath(plate.icon)

		self.__model.initializeModel(rootNode)
		return True

	def loopThroughIblSets(self, backward=False):
		"""
		Loops through :mod:`sibl_gui.components.core.iblSetsOutliner.iblSetsOutliner` Component Ibl Sets.

		:param backward: Looping backward.
		:type backward: bool
		:return: Method success.
		:rtype: bool
		"""

		if self.__activeIblSet:
			model = self.__iblSetsOutliner.model

			activeIblSetNode = [node for node in model.rootNode.children if
								node.databaseItem.path == self.__activeIblSet.path]
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
		Loops through :mod:`sibl_gui.components.core.inspector.inspector` Component Ibl Set Plates.

		:param backward: Looping backward.
		:type backward: bool
		:return: Method success.
		:rtype: bool
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
