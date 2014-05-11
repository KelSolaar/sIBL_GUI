#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**runtime_globals.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines **sIBL_GUI** package runtime globals through the :class:`RuntimeGlobals` class.

**Others:**

"""

from __future__ import unicode_literals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RuntimeGlobals"]


class RuntimeGlobals():
    """
    Defines **sIBL_GUI** package runtime constants.
    """

    templates_factory_directory = None
    """Templates factory directory."""
    templates_user_directory = None
    """Templates user directory."""

    thumbnails_cache_directory = None
    """Thumbnails cache directory."""

    images_caches = None
    """Images cache."""
