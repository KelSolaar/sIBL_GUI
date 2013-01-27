#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **database** component exceptions. 

**Others:**

"""

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "AbstractDatabaseError",
			"DatabaseOperationError",
			"AbstractIblSetError",
			"MissingIblSetFileError",
			"MissingIblSetIconError",
			"MissingIblSetPreviewImageError",
			"MissingIblSetBackgroundImageError",
			"MissingIblSetLightingImageError",
			"MissingIblSetReflectionImageError",
			"AbstractTemplateError",
			"MissingTemplateFileError",
			"MissingTemplateHelpFileError"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class AbstractDatabaseError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for database related exceptions.
	"""

	pass

class DatabaseOperationError(AbstractDatabaseError):
	"""
	This class is used for Database operation exceptions.
	"""

	pass

class AbstractIblSetError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for Ibl Set related exceptions.
	"""

	pass

class MissingIblSetFileError(AbstractIblSetError):
	"""
	This class is used when an Ibl Set's file is missing.
	"""

	pass

class MissingIblSetIconError(AbstractIblSetError):
	"""
	This class is used when an Ibl Set's icon is missing.
	"""

	pass

class MissingIblSetPreviewImageError(AbstractIblSetError):
	"""
	This class is used when an Ibl Set's preview image is missing.
	"""

	pass

class MissingIblSetBackgroundImageError(AbstractIblSetError):
	"""
	This class is used when an Ibl Set's background image is missing.
	"""

	pass

class MissingIblSetLightingImageError(AbstractIblSetError):
	"""
	This class is used when an Ibl Set's lighting image is missing.
	"""

	pass

class MissingIblSetReflectionImageError(AbstractIblSetError):
	"""
	This class is used when an Ibl Set's reflection image is missing.
	"""

	pass

class AbstractTemplateError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for Template related exceptions.
	"""

	pass

class MissingTemplateFileError(AbstractTemplateError):
	"""
	This class is used when a Template file is missing.
	"""

	pass

class MissingTemplateHelpFileError(AbstractTemplateError):
	"""
	This class is used when a Template help file is missing.
	"""

	pass

