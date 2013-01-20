#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**darwinSetup.py**

**Platform:**
	Mac Os X.

**Description:**
	This module defines the py2app configuration file.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from setuptools import setup

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["MAJOR_VERSION", "APP", "DATA_FILES", "OPTIONS"]

APPLICATION_NAME = "sIBL_GUI"
MAJOR_VERSION = "4"

APP = ["../../sibl_gui/launcher.py"]
DATA_FILES = []
OPTIONS = {"argv_emulation": True, "iconfile": "../../sibl_gui/resources/images/Icon_Light_256.icns"}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
setup(name="{0} {1}".format(APPLICATION_NAME, MAJOR_VERSION),
	app=APP,
	data_files=DATA_FILES,
	options={"py2app": OPTIONS},
	setup_requires=["py2app"])
