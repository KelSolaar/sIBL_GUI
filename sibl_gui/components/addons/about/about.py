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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.ui.common
from manager.qwidgetComponent import QWidgetComponentFactory
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ABOUT_MESSAGE", "About"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "About.ui")

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
Special thanks to: Dschaga, Tischbein3, Andy, Volxen, Gwynne, Keksonja, Yuri, Rork, Jeff Hanna, Spedler,
Lee and Brett.
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
This software uses Python, Qt, PyQt, FreeImage, SQLAlchemy, SQLAlchemy-migrate, py2app, pyinstaller, Sphinx, Tidy, \
Actual Installer.
<br/>
Coded with Aptana - Pydev - Textmate - Sublime Text 2, Git and Github for Mac.
</p>
<p>
If you are a HDRI resources vendor and are interested in making your sets Smart Ibl compliant:
<br/>
Please contact us at HDRLabs:
<br/>
Christian Bloch - <a href="mailto:blochi@edenfx.com">
<span style=" text-decoration: underline; color:#e0e0e0;">blochi@edenfx.com</span></a>
<br/>
Thomas Mansencal - <a href="mailto:thomas.mansencal@gmail.com">
<span style=" text-decoration: underline; color:#e0e0e0;">thomas.mansencal@gmail.com</span></a>
</p>
<p>
sIBL_GUI by Thomas Mansencal - 2008 - 2013
<br/>
This software is released under terms of GNU GPL v3 license: <a href="http://www.gnu.org/licenses/">
<span style=" text-decoration: underline; color:#e0e0e0;">http://www.gnu.org/licenses/</span></a>
<br/>
<a href="http://www.thomasmansencal.com/">
<span style=" text-decoration: underline; color:#e0e0e0;">http://www.thomasmansencal.com/</span></a>
</p>
<p>
*
</p>
<p>
<a href="http://www.hdrlabs.com/">
<span style=" text-decoration: underline; color:#e0e0e0;">http://www.hdrlabs.com/</span></a>
</p>
*
<p>
<img src="{2}">
</p>
*
</center>
"""

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class About(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`sibl_gui.components.addons.about.about` Component Interface class.
	| It adds the **About sIBL_GUI ...** miscellaneous menu action and provides associated **sIBL_GUI - About** window.
	| The message displayed by the **sIBL_GUI - About** window is defined by the
		:attr:`sibl_gui.components.addons.about.about.ABOUT_MESSAGE` attribute.  
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

		super(About, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__uiResourcesDirectory = "resources"
		self.__uiLogoImage = "sIBL_GUI_Small_Logo.png"
		self.__uiGpl3Image = "GPL_V3.png"

		self.__engine = None
		self.__miscellaneousMenu = None

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
	def uiLogoImage(self):
		"""
		This method is the property for **self.__uiLogoImage** attribute.

		:return: self.__uiLogoImage. ( String )
		"""

		return self.__uiLogoImage

	@uiLogoImage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiLogoImage(self, value):
		"""
		This method is the setter method for **self.__uiLogoImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiLogoImage"))

	@uiLogoImage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiLogoImage(self):
		"""
		This method is the deleter method for **self.__uiLogoImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiLogoImage"))

	@property
	def uiGpl3Image(self):
		"""
		This method is the property for **self.__uiGpl3Image** attribute.

		:return: self.__uiGpl3Image. ( String )
		"""

		return self.__uiGpl3Image

	@uiGpl3Image.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiGpl3Image(self, value):
		"""
		This method is the setter method for **self.__uiGpl3Image** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiGpl3Image"))

	@uiGpl3Image.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uiGpl3Image(self):
		"""
		This method is the deleter method for **self.__uiGpl3Image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiGpl3Image"))

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
	def miscellaneousMenu(self):
		"""
		This method is the property for **self.__miscellaneousMenu** attribute.

		:return: self.__miscellaneousMenu. ( QMenu )
		"""

		return self.__miscellaneousMenu

	@miscellaneousMenu.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def miscellaneousMenu(self, value):
		"""
		This method is the setter method for **self.__miscellaneousMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "miscellaneousMenu"))

	@miscellaneousMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def miscellaneousMenu(self):
		"""
		This method is the deleter method for **self.__miscellaneousMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "miscellaneousMenu"))

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
		self.__miscellaneousMenu = self.__engine.toolBar.miscellaneousMenu

		self.__addActions()

		self.activated = True
		return True

	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__removeActions()

		self.__uiResourcesDirectory = os.path.basename(self.__uiResourcesDirectory)
		self.__engine = None
		self.__miscellaneousMenu = None

		self.activated = False
		return True

	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		return True

	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		return True

	def __addActions(self):
		"""
		This method sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		self.__miscellaneousMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|ToolBar|Miscellaneous|About {0} ...".format(Constants.applicationName),
																slot=self.__miscellaneousMenu_aboutAction__triggered))

	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		aboutAction = "Actions|Umbra|ToolBar|Miscellaneous|About {0} ...".format(Constants.applicationName)
		self.__miscellaneousMenu.removeAction(self.__engine.actionsManager.getAction(aboutAction))
		self.__engine.actionsManager.unregisterAction(aboutAction)

	def __miscellaneousMenu_aboutAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|ToolBar|Miscellaneous|About {0} ...'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}' window.".format("About"))

		umbra.ui.common.setWindowDefaultIcon(self)

		aboutMessage = ABOUT_MESSAGE.format(os.path.join(self.__uiResourcesDirectory, self.__uiLogoImage),
						Constants.releaseVersion.replace(".", " . "),
						os.path.join(self.__uiResourcesDirectory, self.__uiGpl3Image))

		self.About_label.setText(aboutMessage)

		self.show()
		return True
