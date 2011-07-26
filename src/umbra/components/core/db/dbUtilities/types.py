#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If you are a HDRI resources vendor and are interested in making your sets SmartIBL compliant:
# Please contact us at HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**types.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Database Types Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from sqlalchemy import ForeignKey

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.parser
from umbra.globals.constants import Constants
from foundations.parser import Parser

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
DbBase = sqlalchemy.ext.declarative.declarative_base()

class DbIblSet(DbBase):
	"""
	This Class Is The DbIblSet Class.
	"""

	__tablename__ = "Sets"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	path = sqlalchemy.Column(sqlalchemy.String)
	osStats = sqlalchemy.Column(sqlalchemy.String)
	collection = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("Collections.id"))
	title = sqlalchemy.Column(sqlalchemy.String)
	author = sqlalchemy.Column(sqlalchemy.String)
	link = sqlalchemy.Column(sqlalchemy.String)
	icon = sqlalchemy.Column(sqlalchemy.String)
	previewImage = sqlalchemy.Column(sqlalchemy.String)
	backgroundImage = sqlalchemy.Column(sqlalchemy.String)
	lightingImage = sqlalchemy.Column(sqlalchemy.String)
	reflectionImage = sqlalchemy.Column(sqlalchemy.String)
	location = sqlalchemy.Column(sqlalchemy.String)
	latitude = sqlalchemy.Column(sqlalchemy.String)
	longitude = sqlalchemy.Column(sqlalchemy.String)
	date = sqlalchemy.Column(sqlalchemy.String)
	time = sqlalchemy.Column(sqlalchemy.String)
	comment = sqlalchemy.Column(sqlalchemy.String)

	@core.executionTrace
	def __init__(self,
			name=None,
			path=None,
			osStats=None,
			collection=None,
			title=None,
			author=None,
			link=None,
			icon=None,
			previewImage=None,
			backgroundImage=None,
			lightingImage=None,
			reflectionImage=None,
			location=None,
			latitude=None,
			longitude=None,
			date=None,
			time=None,
			comment=None):
		"""
		This Method Initializes The Class.

		@param *:*. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.name = name
		self.path = path
		self.osStats = osStats
		self.collection = collection
		self.title = title
		self.author = author
		self.link = link
		self.icon = icon
		self.previewImage = previewImage
		self.backgroundImage = backgroundImage
		self.lightingImage = lightingImage
		self.reflectionImage = reflectionImage
		self.location = location
		self.latitude = latitude
		self.longitude = longitude
		self.date = date
		self.time = time
		self.comment = comment

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileStructureError)
	def setContent(self):
		"""
		This Method Initializes The DbIblSet Attributes.

		@return: DbIblSet Initialization Success. ( Boolean )
		"""

		parser = Parser(self.path)
		parser.read() and parser.parse()

		if parser.sections:
			self.title = parser.getValue("Name", "Header", encode=True)
			self.author = parser.getValue("Author", "Header", encode=True)
			self.link = parser.getValue("Link", "Header", encode=True)
			self.icon = parser.getValue("ICOfile", "Header", encode=True) and os.path.normpath(os.path.join(os.path.dirname(self.path), parser.getValue("ICOfile", "Header", encode=True))) or None
			self.previewImage = parser.getValue("PREVIEWfile", "Header", encode=True) and os.path.normpath(os.path.join(os.path.dirname(self.path), parser.getValue("PREVIEWfile", "Header", encode=True))) or None
			self.backgroundImage = parser.getValue("BGfile", "Background", encode=True) and os.path.normpath(os.path.join(os.path.dirname(self.path), parser.getValue("BGfile", "Background", encode=True))) or None
			self.lightingImage = parser.getValue("EVfile", "Enviroment", encode=True) and os.path.normpath(os.path.join(os.path.dirname(self.path), parser.getValue("EVfile", "Enviroment", encode=True))) or None
			self.reflectionImage = parser.getValue("REFfile", "Reflection", encode=True) and os.path.normpath(os.path.join(os.path.dirname(self.path), parser.getValue("REFfile", "Reflection", encode=True))) or None
			self.location = parser.getValue("Location", "Header", encode=True)
			self.latitude = parser.getValue("GEOlat", "Header", encode=True)
			self.longitude = parser.getValue("GEOlong", "Header", encode=True)
			self.date = parser.getValue("Date", "Header", encode=True)
			self.time = parser.getValue("Time", "Header", encode=True)
			self.comment = parser.getValue("Comment", "Header", encode=True)

			return True

		else:
			raise foundations.exceptions.FileStructureError("'{0}' No Sections Found, File Structure Seems Invalid!".format(self.path))

class DbTemplate(DbBase):
	"""
	This Class Is The DbTemplate Class.
	"""

	__tablename__ = "Templates"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	path = sqlalchemy.Column(sqlalchemy.String)
	osStats = sqlalchemy.Column(sqlalchemy.String)
	collection = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("Collections.id"))
	helpFile = sqlalchemy.Column(sqlalchemy.String)
	title = sqlalchemy.Column(sqlalchemy.String)
	author = sqlalchemy.Column(sqlalchemy.String)
	email = sqlalchemy.Column(sqlalchemy.String)
	url = sqlalchemy.Column(sqlalchemy.String)
	release = sqlalchemy.Column(sqlalchemy.String)
	date = sqlalchemy.Column(sqlalchemy.String)
	software = sqlalchemy.Column(sqlalchemy.String)
	version = sqlalchemy.Column(sqlalchemy.String)
	renderer = sqlalchemy.Column(sqlalchemy.String)
	outputScript = sqlalchemy.Column(sqlalchemy.String)
	comment = sqlalchemy.Column(sqlalchemy.String)

	@core.executionTrace
	def __init__(self,
			name=None,
			path=None,
			osStats=None,
			collection=None,
			helpFile=None,
			title=None,
			author=None,
			email=None,
			url=None,
			release=None,
			date=None,
			software=None,
			version=None,
			renderer=None,
			outputScript=None,
			comment=None):
		"""
		This Method Initializes The Class.

		@param *:*. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.name = name
		self.path = path
		self.osStats = osStats
		self.collection = collection
		self.helpFile = helpFile
		self.title = title
		self.author = author
		self.email = email
		self.url = url
		self.release = release
		self.date = date
		self.software = software
		self.version = version
		self.renderer = renderer
		self.outputScript = outputScript
		self.comment = comment

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileStructureError)
	def setContent(self):
		"""
		This Method Initializes The DbTemplate Attributes.

		@return: DbTemplate Initialization Success. ( Boolean )
		"""

		parser = Parser(self.path)
		parser.read() and parser.parse(rawSections=("Script"))

		if parser.sections:
			self.helpFile = foundations.parser.getAttributeCompound("HelpFile", parser.getValue("HelpFile", "Template", encode=True)).value and os.path.join(os.path.dirname(self.path), foundations.parser.getAttributeCompound("HelpFile", parser.getValue("HelpFile", "Template", encode=True)).value) or None
			self.title = foundations.parser.getAttributeCompound("Name", parser.getValue("Name", "Template", encode=True)).value
			self.author = foundations.parser.getAttributeCompound("Author", parser.getValue("Author", "Template", encode=True)).value
			self.email = foundations.parser.getAttributeCompound("Email", parser.getValue("Email", "Template", encode=True)).value
			self.url = foundations.parser.getAttributeCompound("Url", parser.getValue("Url", "Template", encode=True)).value
			self.release = foundations.parser.getAttributeCompound("Release", parser.getValue("Release", "Template", encode=True)).value
			self.date = foundations.parser.getAttributeCompound("Date", parser.getValue("Date", "Template", encode=True)).value
			self.software = foundations.parser.getAttributeCompound("Software", parser.getValue("Software", "Template", encode=True)).value
			self.version = foundations.parser.getAttributeCompound("Version", parser.getValue("Version", "Template", encode=True)).value
			self.renderer = foundations.parser.getAttributeCompound("Renderer", parser.getValue("Renderer", "Template", encode=True)).value
			self.outputScript = foundations.parser.getAttributeCompound("OutputScript", parser.getValue("OutputScript", "Template", encode=True)).value
			self.comment = foundations.parser.getAttributeCompound("Comment", parser.getValue("Comment", "Template", encode=True)).value

			return True

		else:
			raise foundations.exceptions.FileStructureError("'{0}' No Sections Found, File Structure Seems Invalid!".format(self.path))

class DbCollection(DbBase):
	"""
	This Class Is The DbCollection Class.
	"""

	__tablename__ = "Collections"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	type = sqlalchemy.Column(sqlalchemy.String)
	comment = sqlalchemy.Column(sqlalchemy.String)

	@core.executionTrace
	def __init__(self, name=None, type=None, comment=None):
		"""
		This Method Initializes The Class.

		@param *:*. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.name = name
		self.type = type
		self.comment = comment

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************
