#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
************************************************************************************************
***	about.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		About Component Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
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
		<br/><br/>Thanks To All Folks At <b>HDRLabs.com</b> For Providing Smart IBL World!
		<br/>
		Special Thanks To: Dschaga, Tischbein3, Andy, VolXen, Gwynne, keksonja, Yuri, Rork, Jeff Hanna, Spedler, Lee And Brett.
		<br/>
		Another Big Thanks To Emanuele Santos For Helping Me Out On The Mac Os X Bundle. 
		<br/>
		Thanks To Marienz From Irc #python For Optimisations Tips.
		<p>
		Thanks To All Cool Guys From CGFeedback, XSIBase And CGTalk.
		</p>
		<p>
		Very Special Thanks To Christian For Providing Me Some Space On His Server!
		</p>
		<p>
		This Software Uses Python, Qt, PyQT, FreeImage, SQLAlchemy, SQLAlchemy-migrate, Py2App, PyInstaller And NSIS.
		<br/>
		Coded With Eclipse - Pydev - Aptana - TextMate And Git.
		</p>
		<p>
		Light Bulb Icon Is Copyright Christian Bloch.
		</p>
		<p>
		If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets Smart IBL Compliant:
		<br/>
		Please Contact Us At HDRLabs:
		<br/>
		Christian Bloch - <a href="mailto:blochi@edenfx.com"><span style=" text-decoration: underline; color:#e0e0e0;">blochi@edenfx.com</span></a>
		<br/>
		Thomas Mansencal - <a href="mailto:thomas.mansencal@gmail.com"><span style=" text-decoration: underline; color:#e0e0e0;">thomas.mansencal@gmail.com</span></a>
		</p>
		<p>
		sIBL_GUI by Thomas Mansencal - 2008 - 2011
		<br/>
		This Software Is Released Under Terms Of GNU GPL V3 License: <a href="http://www.gnu.org/licenses/"><span style=" text-decoration: underline; color:#e0e0e0;">http://www.gnu.org/licenses/</span></a>
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
#***	Module Classes And Definitions
#***********************************************************************************************
class About(UiComponent):
	"""
	This Class Is The About Class.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self.__uiPath = "ui/About.ui"
		self.__uiResources = "resources"
		self.__uiLogoImage = "sIBL_GUI_Small_Logo.png"
		self.__uiGpl3Image = "GPL_V3.png"

		self.__container = None
		self.__miscMenu = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath(self):
		"""
		This Method Is The Property For The _uiPath Attribute.

		@return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This Method Is The Deleter Method For The _uiPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiPath"))

	@property
	def uiResources(self):
		"""
		This Method Is The Property For The _uiResources Attribute.

		@return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This Method Is The Deleter Method For The _uiResources Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiResources"))

	@property
	def uiLogoImage(self):
		"""
		This Method Is The Property For The _uiLogoImage Attribute.

		@return: self.__uiLogoImage. ( String )
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This Method Is The Setter Method For The _uiLogoImage Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This Method Is The Deleter Method For The _uiLogoImage Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiLogoImage"))

	@property
	def uiGpl3Image(self):
		"""
		This Method Is The Property For The _uiGpl3Image Attribute.

		@return: self.__uiGpl3Image. ( String )
		"""

		return self.__uiGpl3Image

	@uiGpl3Image.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiGpl3Image(self, value):
		"""
		This Method Is The Setter Method For The _uiGpl3Image Attribute.

		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("uiGpl3Image"))

	@uiGpl3Image.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiGpl3Image(self):
		"""
		This Method Is The Deleter Method For The _uiGpl3Image Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("uiGpl3Image"))

	@property
	def container(self):
		"""
		This Method Is The Property For The _container Attribute.

		@return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This Method Is The Deleter Method For The _container Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def miscMenu(self):
		"""
		This Method Is The Property For The _miscMenu Attribute.

		@return: self.__miscMenu. ( QMenu )
		"""

		return self.__miscMenu

	@miscMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def miscMenu(self, value):
		"""
		This Method Is The Setter Method For The _miscMenu Attribute.

		@param value: Attribute Value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("miscMenu"))

	@miscMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def miscMenu(self):
		"""
		This Method Is The Deleter Method For The _miscMenu Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("miscMenu"))

	@property
	def aboutMiscAction(self):
		"""
		This Method Is The Property For The _aboutMiscAction Attribute.

		@return: self.__aboutMiscAction. ( QAction )
		"""

		return self.__aboutMiscAction

	@aboutMiscAction.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def aboutMiscAction(self, value):
		"""
		This Method Is The Setter Method For The _aboutMiscAction Attribute.

		@param value: Attribute Value. ( QAction )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("aboutMiscAction"))

	@aboutMiscAction.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def aboutMiscAction(self):
		"""
		This Method Is The Deleter Method For The _aboutMiscAction Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("aboutMiscAction"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container
		self.__miscMenu = self.__container.miscMenu

		self.__addActions()

		self._activate()

	@core.executionTrace
	def deactivate(self):
		"""
		This Method Deactivates The Component.
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__removeActions()

		self.uiFile = None
		self.__uiResources = os.path.basename(self.__uiResources)
		self.__container = None
		self.__miscMenu = None

		self._deactivate()

	@core.executionTrace
	def initializeUi(self):
		"""
		This Method Initializes The Component Ui.
		"""

		LOGGER.debug("> Initializing '{0}' Component Ui.".format(self.__class__.__name__))

	@core.executionTrace
	def uninitializeUi(self):
		"""
		This Method Uninitializes The Component Ui.
		"""

		LOGGER.debug("> Uninitializing '{0}' Component Ui.".format(self.__class__.__name__))

	@core.executionTrace
	def addWidget(self):
		"""
		This Method Adds The Component Widget To The Container.
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

	@core.executionTrace
	def removeWidget(self):
		"""
		This Method Removes The Component Widget From The Container.
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

	@core.executionTrace
	def __addActions(self):
		"""
		This Method Adds Actions.
		"""

		LOGGER.debug("> Adding '{0}' Component Actions.".format(self.__class__.__name__))

		self.__aboutMiscAction = QAction("About {0} ...".format(Constants.applicationName), self)
		self.__aboutMiscAction.triggered.connect(self.__miscMenu_aboutMiscAction__triggered)
		self.__miscMenu.addAction(self.__aboutMiscAction)

	@core.executionTrace
	def __removeActions(self):
		"""
		This Method Removes Actions.
		"""

		LOGGER.debug("> Removing '{0}' Component Actions.".format(self.__class__.__name__))

		self.__miscMenu.removeAction(self.__aboutMiscAction)

		self.__aboutMiscAction = None

	@core.executionTrace
	def __miscMenu_aboutMiscAction__triggered(self, checked):
		"""
		This Method Is Triggered By aboutMiscAction Action.

		@param checked: Action Checked State. ( Boolean )
		"""


		LOGGER.debug("> Initializing '{0}' Window.".format("About"))

		umbra.ui.common.setWindowDefaultIcon(self.ui)

		aboutMessage = ABOUT_MESSAGE.format(os.path.join(self.__uiResources, self.__uiLogoImage),
					Constants.releaseVersion.replace(".", " . "),
					os.path.join(self.__uiResources, self.__uiGpl3Image)
					)

		self.ui.About_label.setText(aboutMessage)

		self.ui.show()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
