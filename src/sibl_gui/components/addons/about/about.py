#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**about.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`About` Component Interface class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
from manager.uiComponent import UiComponent
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

__all__ = ["LOGGER", "ABOUT_MESSAGE", "About"]

LOGGER = logging.getLogger(Constants.logger)

ABOUT_MESSAGE = """
		<center>
		*
		<p>
		<img src="{0}">
		</p>
		<p>
		s I B L _ G U I - {1}
		</p>
		*
		<br/><br/>Thanks To all folks at <b>HDRLabs.com</b> for providing Smart Ibl world!
		<br/>
		Special thanks to: Dschaga, Tischbein3, Andy, Volxen, Gwynne, Keksonja, Yuri, Rork, Jeff Hanna, Spedler, Lee and Brett.
		<br/>
		Another big thanks to Emanuele Santos for helping me out on the Mac Os X bundle.
		<br/>
		Thanks to Marienz from irc #python for optimisations tips.
		<p>
		Thanks to all cool guys from CGFeedback, XSIBase and CGTalk.
		</p>
		<p>
		Very special thanks to Christian for providing me some space on his server!
		</p>
		<p>
		This software uses Python, Qt, PyQt, FreeImage, SQLAlchemy, SQLAlchemy-migrate, py2app, pyinstaller and NSIS.
		<br/>
		Coded with Eclipse - Pydev - Aptana - Textmate and Git.
		</p>
		<p>
		Light bulb icon is copyright Christian Bloch.
		</p>
		<p>
		If you are a HDRI resources vendor and are interested in making your sets Smart Ibl compliant:
		<br/>
		Please contact us at HDRLabs:
		<br/>
		Christian Bloch - <a href="mailto:blochi@edenfx.com"><span style=" text-decoration: underline; color:#e0e0e0;">blochi@edenfx.com</span></a>
		<br/>
		Thomas Mansencal - <a href="mailto:thomas.mansencal@gmail.com"><span style=" text-decoration: underline; color:#e0e0e0;">thomas.mansencal@gmail.com</span></a>
		</p>
		<p>
		sIBL_GUI by Thomas Mansencal - 2008 - 2011
		<br/>
		This software is released under terms of GNU GPL v3 license: <a href="http://www.gnu.org/licenses/"><span style=" text-decoration: underline; color:#e0e0e0;">http://www.gnu.org/licenses/</span></a>
		<br/>
		<a href="http://www.thomasmansencal.com/"><span style=" text-decoration: underline; color:#e0e0e0;">http://www.thomasmansencal.com/</span></a>
		</p>
		<p>
		*
		</p>
		<p>
		<a href="http://www.hdrlabs.com/"><span style=" text-decoration: underline; color:#e0e0e0;">http://www.hdrlabs.com/</span></a>
		</p>
		*
		<p>
		<img src="{2}">
		</p>
		*
		</center>
		"""

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class About(UiComponent):
	"""
	| This class is the :mod:`umbra.components.addons.about.about` Component Interface class.
	| It adds the **About sIBL_GUI ...** miscellaneous menu action and provides associated **sIBL_GUI - About** window.
	| The message displayed by the **sIBL_GUI - About** window is defined by the :attr:`umbra.components.addons.about.about.ABOUT_MESSAGE` attribute.  
	"""

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

		self.__uiPath = "ui/About.ui"
		self.__uiResources = "resources"
		self.__uiLogoImage = "sIBL_GUI_Small_Logo.png"
		self.__uiGpl3Image = "GPL_V3.png"

		self.__container = None
		self.__miscellaneousMenu = None

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
	def uiResources(self):
		"""
		This method is the property for **self.__uiResources** attribute.

		:return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for **self.__uiResources** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for **self.__uiResources** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiLogoImage(self):
		"""
		This method is the property for **self.__uiLogoImage** attribute.

		:return: self.__uiLogoImage. ( String )
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This method is the setter method for **self.__uiLogoImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This method is the deleter method for **self.__uiLogoImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiLogoImage"))

	@property
	def uiGpl3Image(self):
		"""
		This method is the property for **self.__uiGpl3Image** attribute.

		:return: self.__uiGpl3Image. ( String )
		"""

		return self.__uiGpl3Image

	@uiGpl3Image.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiGpl3Image(self, value):
		"""
		This method is the setter method for **self.__uiGpl3Image** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiGpl3Image"))

	@uiGpl3Image.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiGpl3Image(self):
		"""
		This method is the deleter method for **self.__uiGpl3Image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiGpl3Image"))

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
	def miscellaneousMenu(self):
		"""
		This method is the property for **self.__miscellaneousMenu** attribute.

		:return: self.__miscellaneousMenu. ( QMenu )
		"""

		return self.__miscellaneousMenu

	@miscellaneousMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def miscellaneousMenu(self, value):
		"""
		This method is the setter method for **self.__miscellaneousMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("miscellaneousMenu"))

	@miscellaneousMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def miscellaneousMenu(self):
		"""
		This method is the deleter method for **self.__miscellaneousMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("miscellaneousMenu"))

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
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container
		self.__miscellaneousMenu = self.__container.miscellaneousMenu

		self.__addActions()

		return UiComponent.activate(self)

	@core.executionTrace
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__removeActions()

		self.uiFile = None
		self.__uiResources = os.path.basename(self.__uiResources)
		self.__container = None
		self.__miscellaneousMenu = None

		return UiComponent.deactivate(self)

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		return True

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		return True

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		return True

	@core.executionTrace
	def __addActions(self):
		"""
		This method adds actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		self.__miscellaneousMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|ToolBar|Miscellaneous|About {0} ...".format(Constants.applicationName), slot=self.__miscellaneousMenu_aboutAction__triggered))

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		aboutAction = "Actions|Umbra|ToolBar|Miscellaneous|About {0} ...".format(Constants.applicationName)
		self.__miscellaneousMenu.removeAction(self.__container.actionsManager.getAction(aboutAction))
		self.__container.actionsManager.unregisterAction(aboutAction)

	@core.executionTrace
	def __miscellaneousMenu_aboutAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|ToolBar|Miscellaneous|About {0} ...'** action.

		:param checked: Action checked state. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}' window.".format("About"))

		umbra.ui.common.setWindowDefaultIcon(self.ui)

		aboutMessage = ABOUT_MESSAGE.format(os.path.join(self.__uiResources, self.__uiLogoImage),
					Constants.releaseVersion.replace(".", " . "),
					os.path.join(self.__uiResources, self.__uiGpl3Image))

		self.ui.About_label.setText(aboutMessage)

		self.ui.show()
