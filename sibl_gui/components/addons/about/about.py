#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**about.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`About` Component Interface class.

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

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.ui.common
from manager.QWidget_component import QWidgetComponentFactory
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ABOUT_MESSAGE", "About"]

LOGGER = foundations.verbose.install_logger()

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
<br/><br/>Thanks to all folks at <b>HDRLabs.com</b> for providing Smart Ibl world!
<br/>
Special thanks to: Bob, Dschaga, Tischbein3, Andy, Volxen, Gwynne, Keksonja, Yuri, Rork, Jeff Hanna, Spedler,
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
This software uses Python, Qt, PyQt, FreeImage, SQLAlchemy, pyinstaller, Sphinx, Tidy and
Actual Installer.
<br/>
Coded with Aptana - Umbra - Sublime Text 2, Git and Github for Mac.
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
sIBL_GUI by Thomas Mansencal - 2008 - 2014
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
class About(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`sibl_gui.components.addons.about.about` Component Interface class.
	| It adds the **About sIBL_GUI ...** miscellaneous menu action and provides associated **sIBL_GUI - About** window.
	| The message displayed by the **sIBL_GUI - About** window is defined by the
		:attr:`sibl_gui.components.addons.about.about.ABOUT_MESSAGE` attribute.  
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

		super(About, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__ui_resources_directory = "resources"
		self.__ui_logo_image = "sIBL_GUI_Small_Logo.png"
		self.__ui_gpl3_image = "GPL_V3.png"

		self.__engine = None
		self.__miscellaneous_menu = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def ui_resources_directory(self):
		"""
		Property for **self.__ui_resources_directory** attribute.

		:return: self.__ui_resources_directory.
		:rtype: unicode
		"""

		return self.__ui_resources_directory

	@ui_resources_directory.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_resources_directory(self, value):
		"""
		Setter for **self.__ui_resources_directory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_resources_directory"))

	@ui_resources_directory.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_resources_directory(self):
		"""
		Deleter for **self.__ui_resources_directory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_resources_directory"))

	@property
	def ui_logo_image(self):
		"""
		Property for **self.__ui_logo_image** attribute.

		:return: self.__ui_logo_image.
		:rtype: unicode
		"""

		return self.__ui_logo_image

	@ui_logo_image.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_logo_image(self, value):
		"""
		Setter for **self.__ui_logo_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_logo_image"))

	@ui_logo_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_logo_image(self):
		"""
		Deleter for **self.__ui_logo_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_logo_image"))

	@property
	def ui_gpl3_image(self):
		"""
		Property for **self.__ui_gpl3_image** attribute.

		:return: self.__ui_gpl3_image.
		:rtype: unicode
		"""

		return self.__ui_gpl3_image

	@ui_gpl3_image.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_gpl3_image(self, value):
		"""
		Setter for **self.__ui_gpl3_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_gpl3_image"))

	@ui_gpl3_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_gpl3_image(self):
		"""
		Deleter for **self.__ui_gpl3_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_gpl3_image"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def miscellaneous_menu(self):
		"""
		Property for **self.__miscellaneous_menu** attribute.

		:return: self.__miscellaneous_menu.
		:rtype: QMenu
		"""

		return self.__miscellaneous_menu

	@miscellaneous_menu.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def miscellaneous_menu(self, value):
		"""
		Setter for **self.__miscellaneous_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "miscellaneous_menu"))

	@miscellaneous_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def miscellaneous_menu(self):
		"""
		Deleter for **self.__miscellaneous_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "miscellaneous_menu"))

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

		self.__ui_resources_directory = os.path.join(os.path.dirname(__file__), self.__ui_resources_directory)
		self.__engine = engine
		self.__miscellaneous_menu = self.__engine.toolBar.miscellaneous_menu

		self.__add_actions()

		self.activated = True
		return True

	def deactivate(self):
		"""
		Deactivates the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__remove_actions()

		self.__ui_resources_directory = os.path.basename(self.__ui_resources_directory)
		self.__engine = None
		self.__miscellaneous_menu = None

		self.activated = False
		return True

	def initialize_ui(self):
		"""
		Initializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.initialized_ui = True
		return True

	def uninitialize_ui(self):
		"""
		Uninitializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.initialized_ui = False
		return True

	def add_widget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		return True

	def remove_widget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		return True

	def __add_actions(self):
		"""
		Sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		self.__miscellaneous_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|ToolBar|Miscellaneous|About {0} ...".format(Constants.application_name),
																slot=self.__miscellaneous_menu_aboutAction__triggered))

	def __remove_actions(self):
		"""
		Removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		aboutAction = "Actions|Umbra|ToolBar|Miscellaneous|About {0} ...".format(Constants.application_name)
		self.__miscellaneous_menu.removeAction(self.__engine.actions_manager.get_action(aboutAction))
		self.__engine.actions_manager.unregister_action(aboutAction)

	def __miscellaneous_menu_aboutAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|ToolBar|Miscellaneous|About {0} ...'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' window.".format("About"))

		umbra.ui.common.set_window_default_icon(self)

		about_message = ABOUT_MESSAGE.format(os.path.join(self.__ui_resources_directory, self.__ui_logo_image),
						Constants.version.replace(".", " . "),
						os.path.join(self.__ui_resources_directory, self.__ui_gpl3_image))

		self.About_label.setText(about_message)

		self.show()
		return True
