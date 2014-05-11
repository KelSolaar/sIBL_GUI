#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**003_migrate_4-x-x_to_4-0-3.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Migrates sIBL_GUI from 4.x.x to 4.0.3.

**Others:**

"""

from __future__ import unicode_literals

import os

import foundations.common
import foundations.core
import foundations.verbose
import umbra.ui.widgets.message_box
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UID", "apply"]

LOGGER = foundations.verbose.install_logger()

UID = "97DD5A8BEA1E9CA5F849754730C4EEB3"

def apply():
    """
    Triggers the patch execution.

    :return: Definition success.
    :rtype: bool
    """

    umbra.ui.widgets.message_box.message_box("Information",
    "Message",
    "Hello!\n\nUpon startup and from now on, sIBL_GUI will attempt to connect to \
https://www.crittercism.com/ to report unhandled exceptions whenever they occur!\n\nThis message will only display once!")

    default_script_editor_directory = os.path.join(RuntimeGlobals.user_application_data_directory,
                                                        Constants.io_directory,
                                                        "script_editor")
    default_script_editor_file = os.path.join(default_script_editor_directory, "default_script.py")

    if foundations.common.path_exists(default_script_editor_file):
        LOGGER.info("{0} | Removing deprecated '{1}' default script file!".format(__name__, default_script_editor_file))
        os.remove(default_script_editor_file)
    return True
