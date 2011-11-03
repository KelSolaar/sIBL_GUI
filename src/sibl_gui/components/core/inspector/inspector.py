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

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import re
from collections import OrderedDict
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import sibl_gui.ui.common
import sibl_gui.ui.common
import umbra.ui.common
from foundations.parsers import SectionsFileParser
from manager.qwidgetComponent import QWidgetComponentFactory
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "Plate", "Light", "Inspector"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Inspector.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Plate(core.Structure):
	"""
	This class represents a storage object for an Ibl Set plate.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: name, icon, previewImage, image ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class Light(core.Structure):
	"""
	This class represents a storage object for an Ibl Set light.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: name, color, uCoordinate, vCoordinate ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class Inspector(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.core.inspector.inspector` Component Interface class.
	| It offers a large preview of the current inspected Ibl Set, and a way to navigate into the current selected Database Collection.
	"""

	# Custom signals definitions.
	modelRefresh = pyqtSignal()
	uiRefresh = pyqtSignal()
	uiClear = pyqtSignal()

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
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

		self.__factoryPreferencesManager = None
		self.__coreDatabaseBrowser = None

		self.__model = None

		self.__inspectorIblSet = None
		self.__inspectorIblSetParser = None
		self.__inspectorPlates = None

		self.__noPreviewImageText = """
								<center>
								<table border="0" bordercolor="" cellpadding="0" cellspacing="16">
									<tr>
										<td>
											<img src="{0}">
										</td>
										<td>
											<p><b>Preview Image unavailable!<b></p>
											What now?
											<ul>
												<li>Check For an updated set on <b>HDRLabs</b> at <a href="http://www.hdrlabs.com/sibl/archive.html"><span style=" text-decoration: underline; color:#e0e0e0;">http://www.hdrlabs.com/sibl/archive.html</span></a>.</li>
												<li>Contact <b>{1}</b> At <a href="{2}"><span style=" text-decoration: underline; color:#e0e0e0;">{2}</span></a> for an updated set.</li>
												<li>Resize The background image to 600x300 pixels. Save it as a jpeg in your set directory.<br/>register it in the ."ibl" file header using the "PREVIEWfile" attribute.</li>
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
		self.__inspectorIblSetPlatesToolTipText = """
								<p><b>{0}</b></p>
								"""

		self.__lightLabelRadius = 4
		self.__lightLabelTextOffset = 24
		self.__lightLabelTextMargin = 16
		self.__lightLabelTextHeight = 14
		self.__lightLabelTextFont = "Helvetica"

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiPreviousImage"))

	@uiPreviousImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPreviousImage(self):
		"""
		This method is the deleter method for **self.__uiPreviousImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiPreviousImage"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiNextImage"))

	@uiNextImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiNextImage(self):
		"""
		This method is the deleter method for **self.__uiNextImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiNextImage"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

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

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("listViewIconSize", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("listViewIconSize", value)
		self.__listViewIconSize = value

	@listViewIconSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def listViewIconSize(self):
		"""
		This method is the deleter method for **self.__listViewIconSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "listViewIconSize"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def coreDatabaseBrowser(self):
		"""
		This method is the property for **self.__coreDatabaseBrowser** attribute.

		:return: self.__coreDatabaseBrowser. ( Object )
		"""

		return self.__coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self, value):
		"""
		This method is the setter method for **self.__coreDatabaseBrowser** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def coreDatabaseBrowser(self):
		"""
		This method is the deleter method for **self.__coreDatabaseBrowser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "coreDatabaseBrowser"))

	@property
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorIblSet"))

	@inspectorIblSet.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSet(self):
		"""
		This method is the deleter method for **self.__inspectorIblSet** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorIblSet"))

	@property
	def inspectorIblSetParser(self):
		"""
		This method is the property for **self.__inspectorIblSetParser** attribute.

		:return: self.__inspectorIblSetParser. ( SectionsFileParser )
		"""

		return self.__inspectorIblSetParser

	@inspectorIblSetParser.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetParser(self, value):
		"""
		This method is the setter method for **self.__inspectorIblSetParser** attribute.

		:param value: Attribute value. ( SectionsFileParser )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorIblSetParser"))

	@inspectorIblSetParser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetParser(self):
		"""
		This method is the deleter method for **self.__inspectorIblSetParser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorIblSetParser"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorPlates"))

	@inspectorPlates.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorPlates(self):
		"""
		This method is the deleter method for **self.__inspectorPlates** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorPlates"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "noPreviewImageText"))

	@noPreviewImageText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noPreviewImageText(self):
		"""
		This method is the deleter method for **self.__noPreviewImageText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "noPreviewImageText"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "noInspectorIblSetText"))

	@noInspectorIblSetText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def noInspectorIblSetText(self):
		"""
		This method is the deleter method for **self.__noInspectorIblSetText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "noInspectorIblSetText"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorIblSetToolTipText"))

	@inspectorIblSetToolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetToolTipText(self):
		"""
		This method is the deleter method for **self.__inspectorIblSetToolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorIblSetToolTipText"))

	@property
	def inspectorIblSetPlatesToolTipText(self):
		"""
		This method is the property for **self.__inspectorIblSetPlatesToolTipText** attribute.

		:return: self.__inspectorIblSetPlatesToolTipText. ( String )
		"""

		return self.__inspectorIblSetPlatesToolTipText

	@inspectorIblSetPlatesToolTipText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetPlatesToolTipText(self, value):
		"""
		This method is the setter method for **self.__inspectorIblSetPlatesToolTipText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "inspectorIblSetPlatesToolTipText"))

	@inspectorIblSetPlatesToolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def inspectorIblSetPlatesToolTipText(self):
		"""
		This method is the deleter method for **self.__inspectorIblSetPlatesToolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "inspectorIblSetPlatesToolTipText"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelRadius"))

	@lightLabelRadius.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelRadius(self):
		"""
		This method is the deleter method for **self.__lightLabelRadius** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelRadius"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextOffset"))

	@lightLabelTextOffset.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextOffset(self):
		"""
		This method is the deleter method for **self.__lightLabelTextOffset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextOffset"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextMargin"))

	@lightLabelTextMargin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextMargin(self):
		"""
		This method is the deleter method for **self.__lightLabelTextMargin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextMargin"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextHeight"))

	@lightLabelTextHeight.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextHeight(self):
		"""
		This method is the deleter method for **self.__lightLabelTextHeight** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextHeight"))

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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "lightLabelTextFont"))

	@lightLabelTextFont.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def lightLabelTextFont(self):
		"""
		This method is the deleter method for **self.__lightLabelTextFont** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "lightLabelTextFont"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResourcesDirectory)
		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__factoryPreferencesManager = self.__engine.componentsManager.components["factory.preferencesManager"].interface
		self.__coreDatabaseBrowser = self.__engine.componentsManager.components["core.databaseBrowser"].interface

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

#		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))
#
#		self.Previous_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiPreviousImage)))
#		self.Next_Ibl_Set_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiNextImage)))
#		self.Previous_Plate_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiPreviousImage)))
#		self.Next_Plate_pushButton.setIcon(QIcon(os.path.join(self.__uiResourcesDirectory, self.__uiNextImage)))
#
#		self.Plates_frame.hide()
#		self.Inspector_Options_groupBox.hide()
#
#		self.__model = QStandardItemModel()
#		self.__Plates_listView_setModel()
#		self.__Plates_listView_setView()
#
#		self.__Inspector_DockWidget_setUi()
#
#		self.Inspector_Overall_frame.setContextMenuPolicy(Qt.ActionsContextMenu)
#		self.__Inspector_Overall_frame_addActions()
#
#		# Signals / Slots.
#		self.Plates_listView.selectionModel().selectionChanged.connect(self.__Plates_listView_selectionModel__selectionChanged)
#		self.__coreDatabaseBrowser.model.changed.connect(self.__coreDatabaseBrowser__changed)
#		self.__coreDatabaseBrowser.view.selectionModel().selectionChanged.connect(self.__coreDatabaseBrowser_view_selectionModel__selectionChanged)
#		self.Previous_Ibl_Set_pushButton.clicked.connect(self.__Previous_Ibl_Set_pushButton__clicked)
#		self.Next_Ibl_Set_pushButton.clicked.connect(self.__Next_Ibl_Set_pushButton__clicked)
#		self.Previous_Plate_pushButton.clicked.connect(self.__Previous_Plate_pushButton__clicked)
#		self.Next_Plate_pushButton.clicked.connect(self.__Next_Plate_pushButton__clicked)
#		self.Image_label.linkActivated.connect(self.__Image_label__linkActivated)
#		self.modelRefresh.connect(self.__Plates_listView_refreshModel)
#		self.uiRefresh.connect(self.__Inspector_DockWidget_refreshUi)
#		self.uiClear.connect(self.__Inspector_DockWidget_clearUi)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	@core.executionTrace
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

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	def __Inspector_DockWidget_setUi(self):
		"""
		This method sets the :mod:`umbra.components.core.inspector.inspector` Component dockwidget ui.
		"""

		if self.__inspectorIblSet:

			self.Title_label.setText("<center><b>{0}</b> - {1}</center>".format(self.__inspectorIblSet.title, self.__inspectorIblSet.location))

			if self.__inspectorIblSet.previewImage:
				self.Image_label.setPixmap(sibl_gui.ui.common.getPixmap(self.__inspectorIblSet.previewImage))
				self.__drawInspectorIblSetOverlay()
			else:
				self.Image_label.setText(self.__noPreviewImageText.format(sibl_gui.ui.common.filterImagePath(self.__inspectorIblSet.icon), self.__inspectorIblSet.author, self.__inspectorIblSet.link))

			self.Image_label.setToolTip(self.__inspectorIblSetToolTipText.format(self.__inspectorIblSet.title, self.__inspectorIblSet.author or Constants.nullObject, self.__inspectorIblSet.location or Constants.nullObject, sibl_gui.ui.common.getFormatedShotDate(self.__inspectorIblSet.date, self.__inspectorIblSet.time) or Constants.nullObject, self.__inspectorIblSet.comment or Constants.nullObject))

			self.Details_label.setText("<center><b>Comment:</b> {0}</center>".format(self.__inspectorIblSet.comment))

			if self.__inspectorPlates:
				self.Plates_frame.show()
			else:
				self.Plates_frame.hide()
		else:
			self.__Inspector_DockWidget_clearUi()

	@core.executionTrace
	def __Inspector_DockWidget_refreshUi(self):
		"""
		This method sets the :mod:`umbra.components.core.inspector.inspector` Component dockwidget ui.
		"""

		self.__Inspector_DockWidget_setUi()

	@core.executionTrace
	def __Inspector_DockWidget_clearUi(self):
		"""
		This method clears the :mod:`umbra.components.core.inspector.inspector` Component dockwidget ui.
		"""

		self.Title_label.setText(QString())
		self.Image_label.setText(self.__noInspectorIblSetText.format(sibl_gui.ui.common.filterImagePath("")))
		self.Image_label.setToolTip(QString())
		self.Details_label.setText(QString())

		self.Plates_frame.hide()

	@core.executionTrace
	def __Plates_listView_setModel(self):
		"""
		This method sets the **Plates_listView** Model.
		"""

		LOGGER.debug("> Setting up '{0}' Model!".format("Plates_listView"))

		self.__model.clear()

		if self.__inspectorIblSet:
			LOGGER.debug("> Preparing '{0}' Ibl Set for '{1}' Model.".format(self.__inspectorIblSet.name, "Plates_listView"))
			inspectorIblSetStandardItem = QStandardItem()
			inspectorIblSetStandardItem.setIcon(sibl_gui.ui.common.getIcon(self.__inspectorIblSet.icon))
			inspectorIblSetStandardItem.setToolTip(self.__inspectorIblSetToolTipText.format(self.__inspectorIblSet.title, self.__inspectorIblSet.author or Constants.nullObject, self.__inspectorIblSet.location or Constants.nullObject, sibl_gui.ui.common.getFormatedShotDate(self.__inspectorIblSet.date, self.__inspectorIblSet.time) or Constants.nullObject, self.__inspectorIblSet.comment or Constants.nullObject))
			self.__model.appendRow(inspectorIblSetStandardItem)

			for name, plate in self.__inspectorPlates.items():
				LOGGER.debug("> Preparing '{0}' plate for '{1}' Model.".format(name, "Plates_listView"))
				try:
					plateStandardItem = QStandardItem()
					plateStandardItem.setIcon(sibl_gui.ui.common.getIcon(plate.icon))
					plateStandardItem.setToolTip(self.__inspectorIblSetPlatesToolTipText.format(plate.name))

					plateStandardItem._data = plate

					LOGGER.debug("> Adding '{0}' to '{1}' Model.".format(name, "Plates_listView"))
					self.__model.appendRow(plateStandardItem)

				except Exception as error:
					LOGGER.error("!>{0} | Exception raised while adding '{1}' plate to '{2}' Model!".format(self.__class__.__name__, name, "Plates_listView"))
					foundations.exceptions.defaultExceptionsHandler(error, "{0} | {1}.{2}()".format(core.getModule(self).__name__, self.__class__.__name__, "Plates_listView"))

	@core.executionTrace
	def __Plates_listView_refreshModel(self):
		"""
		This method refreshes the **Plates_listView** Model.
		"""

		self.__Plates_listView_setModel()

	@core.executionTrace
	def __Plates_listView_setView(self):
		"""
		This method sets the **Plates_listView** ui.
		"""

		LOGGER.debug("> Initializing '{0}' Widget!".format("Plates_listView"))

		self.Plates_listView.setAcceptDrops(False)
		self.Plates_listView.setAutoScroll(True)
		self.Plates_listView.setFlow(QListView.LeftToRight)
		self.Plates_listView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.Plates_listView.setMovement(QListView.Static)
		self.Plates_listView.setSelectionMode(QAbstractItemView.SingleSelection)
		self.Plates_listView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.Plates_listView.setViewMode(QListView.IconMode)
		self.Plates_listView.setWrapping(False)

		self.__Plates_listView_setDefaultViewState()

		self.Plates_listView.setModel(self.__model)

	@core.executionTrace
	def __Plates_listView_setDefaultViewState(self):
		"""
		This method scales the **Plates_listView** item size.
		"""

		LOGGER.debug("> Setting '{0}' view item size to: {1}.".format("Plates_listView", self.__listViewIconSize))

		self.Plates_listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.Plates_listView.setIconSize(QSize(self.__listViewIconSize, self.__listViewIconSize))

	@core.executionTrace
	def __Inspector_Overall_frame_addActions(self):
		"""
		This method sets the **Inspector_Overall_frame** actions.
		"""

		pass

	@core.executionTrace
	def __Plates_listView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when **Plates_listView** Model selection has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		index = selectedItems.indexes() and selectedItems.indexes()[0] or None
		item = index and self.__model.itemFromIndex(index) or None
		if item:
			if hasattr(item, "_data"):
				self.Image_label.setPixmap(sibl_gui.ui.common.getPixmap(item._data.previewImage))
			else:
				self.uiRefresh.emit()

	@core.executionTrace
	def __coreDatabaseBrowser__changed(self):
		"""
		This method is triggered when :mod:`umbra.components.core.databaseBrowser.databaseBrowser` Component Model has changed.
		"""

		self.__setInspectorIblSet()

	@core.executionTrace
	def __coreDatabaseBrowser_view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when **coreDatabaseBrowser.view** Model selection has changed.

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
	def __Image_label__linkActivated(self, url):
		"""
		This method is triggered when a link is clicked in the **Image_label** Widget.

		:param url: Url to explore. ( QString )
		"""

		QDesktopServices.openUrl(QUrl(url))

	@core.executionTrace
	def __setInspectorIblSet(self):
		"""
		This method sets the :mod:`umbra.components.core.inspector.inspector` Component Ibl Set.
		"""

		selectedIblSet = self.__coreDatabaseBrowser.getSelectedIblSets()
		self.__inspectorIblSet = selectedIblSet and selectedIblSet[0] or None
		if not self.__inspectorIblSet:
			model = self.__coreDatabaseBrowser.model
			self.__inspectorIblSet = model.rowCount() != 0 and model.item(0)._data or None
		self.__inspectorIblSet and self.__setInspectorIblSetParser()

	@core.executionTrace
	def __setInspectorIblSetParser(self):
		"""
		This method sets the :mod:`umbra.components.core.inspector.inspector` Component Ibl Set parser.
		"""

		if os.path.exists(self.__inspectorIblSet.path):
			LOGGER.debug("> Parsing Inspector Ibl Set file: '{0}'.".format(self.__inspectorIblSet))
			self.__inspectorIblSetParser = SectionsFileParser(self.__inspectorIblSet.path)
			self.__inspectorIblSetParser.read() and self.__inspectorIblSetParser.parse()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def __setInspectorIblSetPlates(self):
		"""
		This method sets the Plates from the :mod:`umbra.components.core.inspector.inspector` Component Ibl Set.
		"""

		if self.__inspectorIblSet:
			if os.path.exists(self.__inspectorIblSet.path):
				self.__inspectorPlates = OrderedDict()
				for section in self.__inspectorIblSetParser.sections:
					if re.search(r"Plate\d+", section):
						self.__inspectorPlates[section] = Plate(name=strings.getSplitextBasename(self.__inspectorIblSetParser.getValue("PLATEfile", section)),
																icon=os.path.normpath(os.path.join(os.path.dirname(self.__inspectorIblSet.path), self.__inspectorIblSetParser.getValue("PLATEthumb", section))),
																previewImage=os.path.normpath(os.path.join(os.path.dirname(self.__inspectorIblSet.path), self.__inspectorIblSetParser.getValue("PLATEpreview", section))),
																image=os.path.normpath(os.path.join(os.path.dirname(self.__inspectorIblSet.path), self.__inspectorIblSetParser.getValue("PLATEfile", section))))
			else:
				raise foundations.exceptions.FileExistsError("{0} | Exception raised while retrieving Plates: '{1}' Ibl Set file doesn't exists!".format(self.__class__.__name__, self.__inspectorIblSet.title))

	@core.executionTrace
	def __drawInspectorIblSetOverlay(self):
		"""
		This method draws an overlay on .
		"""

		painter = QPainter(self.Image_label.pixmap())
		painter.setRenderHints(QPainter.Antialiasing)
		for section in self.__inspectorIblSetParser.sections:
				if section == "Sun":
					self.__drawLightLabel(painter, Light(name="Sun",
													color=[int(value)for value in self.__inspectorIblSetParser.getValue("SUNcolor", section).split(",")],
													uCoordinate=float(self.__inspectorIblSetParser.getValue("SUNu", section)),
													vCoordinate=float(self.__inspectorIblSetParser.getValue("SUNv", section))))
				elif re.search(r"Light\d+", section):
					self.__drawLightLabel(painter, Light(name=self.__inspectorIblSetParser.getValue("LIGHTname", section),
													color=[int(value)for value in self.__inspectorIblSetParser.getValue("LIGHTcolor", section).split(",")],
													uCoordinate=float(self.__inspectorIblSetParser.getValue("LIGHTu", section)),
													vCoordinate=float(self.__inspectorIblSetParser.getValue("LIGHTv", section))))
		painter.end()

	@core.executionTrace
	def __drawLightLabel(self, painter, light):
		"""
		This method draws a light label on provided QPainter.

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

		x = int(light.uCoordinate * width)
		y = int(light.vCoordinate * height)

		textWidth = painter.fontMetrics().width(light.name.title())
		xLabelTextOffset = x + textWidth + self.__lightLabelTextMargin + self.__lightLabelTextOffset > width and -(self.__lightLabelTextOffset + textWidth) or self.__lightLabelTextOffset
		yLabelTextOffset = y - (self.__lightLabelTextHeight + self.__lightLabelTextMargin + self.__lightLabelTextOffset) < 0 and -(self.__lightLabelTextOffset + self.__lightLabelTextHeight) or self.__lightLabelTextOffset
		painter.drawText(x + xLabelTextOffset, y - yLabelTextOffset, light.name.title())

		painter.drawLine(x, y, x + (xLabelTextOffset < 0 and xLabelTextOffset + textWidth or xLabelTextOffset), y - (yLabelTextOffset < 0 and yLabelTextOffset + self.__lightLabelTextHeight or yLabelTextOffset))

		painter.drawEllipse(QPoint(x, y), self.__lightLabelRadius, self.__lightLabelRadius)

		painter.setBrush(Qt.NoBrush)
		painter.setPen(QPen(QBrush(QColor(lightColorRed, lightColorGreen, lightColorBlue, 100)), 2))
		painter.drawEllipse(QPoint(x, y), self.__lightLabelRadius * 3, self.__lightLabelRadius * 3)
		painter.setPen(QPen(QBrush(QColor(lightColorRed, lightColorGreen, lightColorBlue, 50)), 2))
		painter.drawEllipse(QPoint(x, y), self.__lightLabelRadius * 4, self.__lightLabelRadius * 4)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def loopThroughIblSets(self, backward=False):
		"""
		This method loops through Database Browser Ibl Sets.

		:param backward: Looping backward. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if self.__inspectorIblSet:
			iblSetStandardItems = [iblSetStandardItem for iblSetStandardItem in self.__coreDatabaseBrowser.model.findItems("*", Qt.MatchWildcard | Qt.MatchRecursive, 0) if iblSetStandardItem._data.path == self.__inspectorIblSet.path]
			inspectorIblSetStandardItem = iblSetStandardItems and iblSetStandardItems[0] or None
			if not inspectorIblSetStandardItem:
				return True

			model = self.__coreDatabaseBrowser.model
			index = model.indexFromItem(inspectorIblSetStandardItem)

			step = not backward and 1 or -1
			idx = index.row() + step
			if idx < 0:
				idx = model.rowCount() - 1
			elif idx > model.rowCount() - 1:
				idx = 0

			selectionModel = self.__coreDatabaseBrowser.view.selectionModel()
			selectionModel.clear()
			selectionModel.setCurrentIndex(index.sibling(idx, index.column()), QItemSelectionModel.Select)
		else:
			self.uiClear.emit()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def loopThroughPlates(self, backward=False):
		"""
		This method loops through :mod:`umbra.components.core.inspector.inspector` Component Ibl Set Plates.

		:param backward: Looping backward. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		index = self.Plates_listView.selectedIndexes() and self.Plates_listView.selectedIndexes()[0] or None
		if index:
			step = not backward and 1 or -1
			idx = index.row() + step
			if idx < 0:
				idx = self.__model.rowCount() - 1
			elif idx > self.__model.rowCount() - 1:
				idx = 0

			selectionModel = self.Plates_listView.selectionModel()
			selectionModel.clear()
			selectionModel.setCurrentIndex(index.sibling(idx, index.column()), QItemSelectionModel.Select)
		else:
			self.Plates_listView.setCurrentIndex(self.__model.index(0, 0))
		return True
