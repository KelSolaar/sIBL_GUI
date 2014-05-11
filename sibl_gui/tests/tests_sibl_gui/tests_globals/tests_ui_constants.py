#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsui_constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`sibl_gui.globals.ui_constants` module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import re
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from sibl_gui.globals.ui_constants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestUiConstants"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TestUiConstants(unittest.TestCase):
	"""
	Defines :class:`sibl_gui.globals.ui_constants.UiConstants` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("ui_file",
							"windows_stylesheet_file",
							"darwin_stylesheet_file",
							"linux_stylesheet_file",
							"windows_style",
							"darwin_style",
							"settings_file",
							"linux_style",
							"layouts_file",
							"application_windows_icon",
							"splash_screen_image",
							"logo_image",
							"default_toolbar_icon_size",
							"central_widget_icon",
							"central_widget_hover_icon",
							"central_widget_active_icon",
							"custom_layouts_icon",
							"custom_layouts_hover_icon",
							"custom_layouts_active_icon",
							"miscellaneous_icon",
							"miscellaneous_hover_icon",
							"miscellaneous_active_icon",
							"library_icon",
							"library_hover_icon",
							"library_active_icon",
							"inspect_icon",
							"inspect_hover_icon",
							"inspect_active_icon",
							"export_icon",
							"export_hover_icon",
							"export_active_icon",
							"edit_icon",
							"edit_hover_icon",
							"edit_active_icon",
							"preferences_icon",
							"preferences_hover_icon",
							"preferences_active_icon",
							"format_error_image",
							"missing_image",
							"loading_image",
							"startup_layout",
							"development_layout",
							"help_file",
							"api_file",
							"native_image_formats",
							"third_party_image_formats",
							"thumbnails_sizes",
							"thumbnails_cache_directory",
							"crittercism_id")

		for attribute in required_attributes:
			self.assertIn(attribute, UiConstants.__dict__)

	def test_ui_file_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.ui_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.ui_file, "\w+")

	def test_windows_stylesheet_file_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.windows_stylesheet_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windows_stylesheet_file, "\w+")

	def test_darwin_stylesheet_file_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.darwin_stylesheet_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwin_stylesheet_file, "\w+")

	def test_linux_stylesheet_file_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.linux_stylesheet_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linux_stylesheet_file, "\w+")

	def test_windows_style_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.windows_style` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windows_style, "\w+")

	def test_darwin_style_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.darwin_style` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwin_style, "\w+")

	def test_settings_file_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.settings_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.settings_file, "\w+")

	def test_linux_style_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.linux_style` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linux_style, "\w+")

	def test_layouts_file_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.layouts_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layouts_file, "\w+")

	def test_application_windows_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.application_windows_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.application_windows_icon, "\w+")
		self.assertRegexpMatches(UiConstants.application_windows_icon, "\.[pP][nN][gG]$")

	def test_splashscreem_image_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.splash_screen_image` attribute.
		"""

		self.assertRegexpMatches(UiConstants.splash_screen_image, "\w+")
		self.assertRegexpMatches(UiConstants.splash_screen_image,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def test_logo_image_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.logo_image` attribute.
		"""

		self.assertRegexpMatches(UiConstants.logo_image, "\w+")
		self.assertRegexpMatches(UiConstants.logo_image,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def test_default_toolbar_icon_size_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.default_toolbar_icon_size` attribute.
		"""

		self.assertIsInstance(UiConstants.default_toolbar_icon_size, int)
		self.assertGreaterEqual(UiConstants.default_toolbar_icon_size, 8)
		self.assertLessEqual(UiConstants.default_toolbar_icon_size, 128)

	def test_central_widget_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.central_widget_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.central_widget_icon, "\w+")

	def test_central_widget_hover_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.central_widget_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.central_widget_hover_icon, "\w+")

	def test_central_widget_active_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.central_widget_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.central_widget_active_icon, "\w+")

	def test_custom_layouts_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.custom_layouts_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.custom_layouts_icon, "\w+")

	def test_layout_hover_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.custom_layouts_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.custom_layouts_hover_icon, "\w+")

	def test_layout_active_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.custom_layouts_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.custom_layouts_active_icon, "\w+")

	def test_miscellaneous_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.miscellaneous_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneous_icon, "\w+")

	def test_miscellaneous_hover_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.miscellaneous_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneous_hover_icon, "\w+")

	def test_miscellaneous_active_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.miscellaneous_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneous_active_icon, "\w+")

	def test_library_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.library_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.library_icon, "\w+")

	def test_library_hover_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.library_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.library_hover_icon, "\w+")

	def test_library_active_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.library_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.library_active_icon, "\w+")

	def test_inspect_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.inspect_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.inspect_icon, "\w+")

	def test_inspect_hover_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.inspect_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.inspect_hover_icon, "\w+")

	def test_inspect_active_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.inspect_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.inspect_active_icon, "\w+")

	def test_export_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.export_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.export_icon, "\w+")

	def test_export_hover_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.export_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.export_hover_icon, "\w+")

	def test_export_active_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.export_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.export_active_icon, "\w+")

	def test_edit_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.edit_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.edit_icon, "\w+")

	def test_edit_hover_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.edit_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.edit_hover_icon, "\w+")

	def test_edit_active_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.edit_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.edit_active_icon, "\w+")

	def test_preferences_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.preferences_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferences_icon, "\w+")

	def test_preferences_hover_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.preferences_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferences_hover_icon, "\w+")

	def test_preferences_active_icon_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.preferences_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferences_active_icon, "\w+")

	def test_format_error_image_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.format_error_image` attribute.
		"""

		self.assertRegexpMatches(UiConstants.format_error_image, "\w+")
		self.assertRegexpMatches(UiConstants.format_error_image,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def test_missing_image_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.missing_image` attribute.
		"""

		self.assertRegexpMatches(UiConstants.missing_image, "\w+")
		self.assertRegexpMatches(UiConstants.missing_image,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def test_loading_image_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.loading_image` attribute.
		"""

		self.assertRegexpMatches(UiConstants.loading_image, "\w+")
		self.assertRegexpMatches(UiConstants.loading_image,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def test_startup_layout_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.startup_layout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.startup_layout, "\w+")

	def test_development_layout_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.development_layout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.development_layout, "\w+")

	def test_help_file_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.help_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.help_file, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def test_api_file_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.api_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.api_file, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def test_native_image_formats_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.native_image_formats` attribute.
		"""

		self.assertIsInstance(UiConstants.native_image_formats, dict)
		for key, value in UiConstants.native_image_formats.iteritems():
			self.assertIsInstance(key, unicode)
			self.assertIsInstance(value, unicode)
			self.assertTrue(re.compile(value))

	def test_third_party_image_formats_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.third_party_image_formats` attribute.
		"""

		self.assertIsInstance(UiConstants.third_party_image_formats, dict)
		for key, value in UiConstants.third_party_image_formats.iteritems():
			self.assertIsInstance(key, unicode)
			self.assertIsInstance(value, unicode)
			self.assertTrue(re.compile(value))

	def test_thumbnails_sizes_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.thumbnails_sizes` attribute.
		"""

		self.assertIsInstance(UiConstants.thumbnails_sizes, dict)
		for key, value in UiConstants.thumbnails_sizes.iteritems():
			self.assertIsInstance(key, unicode)
			self.assertIn(type(value), (type(None), int))

	def test_thumbnails_cache_directory_attribute(self):
		"""
		Tests :attr:`sibl_gui.globals.ui_constants.UiConstants.thumbnails_cache_directory` attribute.
		"""

		self.assertRegexpMatches(UiConstants.thumbnails_cache_directory, "\w+")

	def test_crittercism_id_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.crittercism_id` attribute.
		"""

		self.assertRegexpMatches(UiConstants.crittercism_id, "\w+")
		self.assertEqual(UiConstants.crittercism_id, "51290b3589ea7429250004fe")

if __name__ == "__main__":
	unittest.main()
