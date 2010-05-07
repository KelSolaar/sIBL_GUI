#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2010 - Thomas Mansencal - kelsolaar_fool@hotmail.com
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
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	about.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		About Component Module.
***
***	Others :
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import ui.common
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

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
		<br/><br/>Thanks To All Folks At <b>HDRLabs.com</b> To Provide Smart IBL World !
		<br/>
		Special Thanks To : Dschaga, Tischbein3, Andy, VolXen, Gwynne, keksonja, Yuri, Rork, Jeff Hanna, Spedler.
		<br/>
		Another Big Thanks To Emanuele Santos For Helping Me Out On The Mac Os X Bundle. 
		<br/>
		Thanks To Marienz From Irc #python For Optimisations Tips.
		<p>
		Very Special Thanks To Christian For Providing Me Some Space On His Server :]
		</p>
		<p>
		This Software Uses Python, Qt, PyQT, Py2App, PyInstaller And NSIS.
		<br/>
		Coded With Eclipse - Pydev - Aptana - TextMate - Jedit And Git.
		</p>
		<p>
		Light Bulb Icon Is Copyright Christian Bloch.
		</p>
		<p>
		If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
		<br/>
		Please Contact Us At HDRLabs :
		<br/>
		Christian Bloch - <a href="mailto:blochi@edenfx.com"><span style=" text-decoration: underline; color:#000000;">blochi@edenfx.com</span></a>
		<br/>
		Thomas Mansencal - <a href="mailto:kelsolaar_fool@hotmail.com"><span style=" text-decoration: underline; color:#000000;">kelsolaar_fool@hotmail.com</span></a>
		</p>
		<p>
		sIBL_GUI by Thomas Mansencal - 2008 - 2010
		<br/>
		This Software Is Released Under Terms Of GNU GPL V3 License : <a href="http://www.gnu.org/licenses/"><span style=" text-decoration: underline; color:#000000;">http://www.gnu.org/licenses/</span></a>
		<br/>
		<a href="http://my.opera.com/KelSolaar/"><span style=" text-decoration: underline; color:#000000;">http://my.opera.com/KelSolaar/</span></a>
		</p>
		<p>
		*
		</p>
		<p>
		<a href="http://www.hdrlabs.com/"><span style=" text-decoration: underline; color:#000000;">http://www.hdrlabs.com/</span></a>
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
class About( UiComponent ):
	'''
	This Class Is The About Class.
	'''

	@core.executionTrace
	def __init__( self, name = None, uiFile = None ):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		UiComponent.__init__( self, name = name, uiFile = uiFile )

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self._uiPath = "ui/About.ui"
		self._uiResources = "resources"
		self._uiLogoIcon = "sIBL_GUI_Small_Logo.png"
		self._uiGpl3Icon = "GPL_V3.png"

		self._container = None
		self._miscMenu = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath( self ):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self, value ):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiPath" ) )

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self ):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiPath" ) )

	@property
	def uiResources( self ):
		'''
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		'''

		return self._uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self, value ):
		'''
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiResources" ) )

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self ):
		'''
		This Method Is The Deleter Method For The _uiResources Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiResources" ) )

	@property
	def uiLogoIcon( self ):
		'''
		This Method Is The Property For The _uiLogoIcon Attribute.

		@return: self._uiLogoIcon. ( String )
		'''

		return self._uiLogoIcon

	@uiLogoIcon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLogoIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiLogoIcon Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiLogoIcon" ) )


	@uiLogoIcon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiLogoIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiLogoIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiLogoIcon" ) )

	@property
	def uiGpl3Icon( self ):
		'''
		This Method Is The Property For The _uiGpl3Icon Attribute.

		@return: self._uiGpl3Icon. ( String )
		'''

		return self._uiGpl3Icon

	@uiGpl3Icon.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiGpl3Icon( self, value ):
		'''
		This Method Is The Setter Method For The _uiGpl3Icon Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiGpl3Icon" ) )

	@uiGpl3Icon.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiGpl3Icon( self ):
		'''
		This Method Is The Deleter Method For The _uiGpl3Icon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiGpl3Icon" ) )

	@property
	def container( self ):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self, value ):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "container" ) )

	@container.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self ):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "container" ) )

	@property
	def miscMenu( self ):
		'''
		This Method Is The Property For The _miscMenu Attribute.

		@return: self._miscMenu. ( QMenu )
		'''

		return self._miscMenu

	@miscMenu.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def miscMenu( self, value ):
		'''
		This Method Is The Setter Method For The _miscMenu Attribute.

		@param value: Attribute Value. ( QMenu )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "miscMenu" ) )

	@miscMenu.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def miscMenu( self ):
		'''
		This Method Is The Deleter Method For The _miscMenu Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "miscMenu" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate( self, container ):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug( "> Activating '{0}' Component.".format( self.__class__.__name__ ) )

		self.uiFile = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiPath )
		self._uiResources = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiResources )
		self._container = container
		self._miscMenu = self._container.miscMenu

		self.addActions_()

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug( "> Deactivating '{0}' Component.".format( self.__class__.__name__ ) )

		self.removeActions_()

		self.uiFile = None
		self._uiResources = os.path.basename( self._uiResources )
		self._container = None
		self._miscMenu = None

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

	@core.executionTrace
	def addWidget( self ):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug( "> Adding '{0}' Component Widget.".format( self.__class__.__name__ ) )

	@core.executionTrace
	def removeWidget( self ):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug( "> Removing '{0}' Component Widget.".format( self.__class__.__name__ ) )

	@core.executionTrace
	def addActions_( self ):
		'''
		This Method Adds Actions.
		'''

		self._aboutMiscAction = QAction( "About {0} ...".format( Constants.applicationName ), self )
		self._aboutMiscAction.triggered.connect( self.miscMenu_aboutMiscAction )
		self._miscMenu.addAction( self._aboutMiscAction )

	@core.executionTrace
	def removeActions_( self ):
		'''
		This Method Removes Actions.
		'''

		self._miscMenu.removeAction( self._aboutMiscAction )

		self._aboutMiscAction = None

	@core.executionTrace
	def miscMenu_aboutMiscAction( self, checked ):
		'''
		This Method Is Triggered By aboutMiscAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		ui.common.setWindowDefaultIcon( self.ui )

		aboutMessage = ABOUT_MESSAGE.format( os.path.join( self._uiResources, self._uiLogoIcon ),
					Constants.releaseVersion.replace( ".", " . " ),
					os.path.join( self._uiResources, self._uiGpl3Icon )
					)

		self.ui.About_label.setText( aboutMessage )

		self.ui.show()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
