#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**getPackagePath.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Write given package path to stdout.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sys

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["getPackagePath"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getPackagePath(package):
	"""
	This writes given package path to stdout.
	"""

	package = __import__(package)
	sys.stdout.write(package.__path__[0])

if __name__ == "__main__":
	getPackagePath(sys.argv[1])
