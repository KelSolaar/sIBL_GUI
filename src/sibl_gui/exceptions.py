#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **sIBL_GUI** package exceptions. 

**Others:**

"""

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.exceptions

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["AbstractNetworkError",
			"NetworkError",
			"SocketConnectionError"]

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class AbstractNetworkError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for network related exceptions.
	"""

	pass

class NetworkError(AbstractNetworkError):
	"""
	This class is used for network exceptions.
	"""

	pass

class SocketConnectionError(AbstractNetworkError):
	"""
	This class is used for socket connection exceptions.
	"""

	pass
