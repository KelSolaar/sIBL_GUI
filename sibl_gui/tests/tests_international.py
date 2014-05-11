#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Runs the international tests suite.

**Others:**

"""

from __future__ import unicode_literals

import os
import shutil
import subprocess
import tempfile

import sibl_gui

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
           "INTERNATIONAL_TEST_SCRIPT_FILE",
           "USER_APPLICATION_DIRECTORY_PREFIX",
           "tests_international"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
INTERNATIONAL_TEST_SCRIPT_FILE = os.path.join(RESOURCES_DIRECTORY, "international_script.py")
USER_APPLICATION_DIRECTORY_PREFIX = "标准"


def tests_international():
    """
    Runs the international tests suite.

    :return: Definition success.
    :rtype: bool
    """

    user_application_directory = tempfile.mkdtemp(prefix=USER_APPLICATION_DIRECTORY_PREFIX)
    command = [os.path.join(sibl_gui.__path__[0], "..", "bin", "sIBL_GUI"),
               "-u", user_application_directory,
               "-x", unicode(INTERNATIONAL_TEST_SCRIPT_FILE)]
    if subprocess.check_call(command) == 0:
        shutil.rmtree(user_application_directory)


if __name__ == "__main__":
    tests_international()
