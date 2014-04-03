#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **sIBL_GUI** package exceptions.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"AbstractNetworkError",
			"NetworkError",
			"SocketConnectionError",
			"Win32OLEServerConnectionError"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class AbstractNetworkError(foundations.exceptions.AbstractError):
	"""
	Defines the abstract base class for network related exceptions.
	"""

	pass

class NetworkError(AbstractNetworkError):
	"""
	Defines network exceptions.
	"""

	pass

class SocketConnectionError(AbstractNetworkError):
	"""
	Defines socket connection exception.
	"""

	pass

class Win32OLEServerConnectionError(AbstractNetworkError):
	"""
	Defines Win32OLE Server connection exception.
	"""

	pass

class AbstractCacheError(foundations.exceptions.AbstractError):
	"""
	Defines the abstract base class for caching related exception.
	"""

	pass

class CacheExistsError(foundations.exceptions.AbstractError):
	"""
	Defines non existing cache exception.
	"""

	pass

class CacheOperationError(foundations.exceptions.AbstractError):
	"""
	Defines cache operations exception.
	"""

	pass
