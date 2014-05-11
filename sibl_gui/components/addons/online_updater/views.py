#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`sibl_gui.components.addons.online_updater.online_updater.OnlineUpdater`
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

__all__ = ["LOGGER", "TemplatesReleases_QTableWidget"]

LOGGER = foundations.verbose.install_logger()

class TemplatesReleases_QTableWidget(umbra.ui.views.Abstract_QTableWidget):
	"""
	Defines the view for Templates releases.
	"""

	pass

