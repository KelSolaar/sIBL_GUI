#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**RuntimeGlobals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **sIBL_GUI** package runtime globals through the :class:`RuntimeGlobals` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RuntimeGlobals"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RuntimeGlobals():
	"""
	Defines **sIBL_GUI** package runtime constants.
	"""

	templatesFactoryDirectory = None
	"""Templates factory directory."""
	templatesUserDirectory = None
	"""Templates user directory."""

	thumbnailsCacheDirectory = None
	"""Thumbnails cache directory."""

	imagesCaches = None
	"""Images cache."""

