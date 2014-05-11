#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`sibl_gui.components.addons.search_database.search_database.SearchDatabase`
    Component Interface class Views.

**Others:**

"""

from __future__ import unicode_literals

import foundations.verbose
import umbra.ui.views

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "TagsCloud_QListWidget"]

LOGGER = foundations.verbose.install_logger()


class TagsCloud_QListView(umbra.ui.views.Abstract_QListWidget):
    """
    Defines the view for Database Ibl Sets tags cloud.
    """

    pass
