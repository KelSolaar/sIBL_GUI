#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**__init__.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**

**Others:**

"""

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["DEFAULT_CODEC",
		   "CODEC_ERROR"]

DEFAULT_CODEC = "utf-8"
CODEC_ERROR = "ignore"

#**********************************************************************************************************************
#***	Encoding manipulations.
#**********************************************************************************************************************
def _setEncoding():
	"""
	Sets the Package encoding.
	"""

	import sys
	reload(sys)

	sys.setdefaultencoding(DEFAULT_CODEC)

_setEncoding()


