#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**types.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines Application Database types: :class:`IblSet`, :class:`Template`
	and :class:`Collection` classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import sqlalchemy.ext.declarative
from sqlalchemy import ForeignKey

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.parsers
import foundations.verbose
from foundations.parsers import SectionsFileParser

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Base", "IblSet", "Template", "Collection"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
Base = sqlalchemy.ext.declarative.declarative_base()

class IblSet(Base):
	"""
	This class defines the Database IblSets type.
	"""

	__tablename__ = "IblSets"
	"""Table name. ( String )"""

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
		This method initializes the class.

		:param name: Ibl Set name. ( String )
		:param path: Ibl Set file path. ( String )
		:param osStats: Ibl Set file statistics. ( String )
		:param collection: Ibl Set collection. ( String )
		:param title: Ibl Set title. ( String )
		:param author: Ibl Set author. ( String )
		:param link: Ibl Set online link. ( String )
		:param icon: Ibl Set icon path. ( String )
		:param previewImage: Ibl Set preview image path. ( String )
		:param backgroundImage: Ibl Set background image path. ( String )
		:param lightingImage: Ibl Set lighting image path. ( String )
		:param reflectionImage: Ibl Set reflection image path. ( String )
		:param location: Ibl Set location. ( String )
		:param latitude: Ibl Set latitude. ( String ),
		:param longitude: Ibl Set longitude. ( String )
		:param date: Ibl Set shot date. ( String )
		:param time: Ibl Set shot time. ( String )
		:param comment: Ibl Set comment. ( String )	
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

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

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileStructureParsingError)
	def setContent(self):
		"""
		This method initializes the class attributes.

		:return: Method success. ( Boolean )
		"""

		sectionsFileParser = SectionsFileParser(self.path)
		sectionsFileParser.read() and sectionsFileParser.parse()

		if sectionsFileParser.sections:
			self.title = sectionsFileParser.getValue("Name", "Header", encode=True)
			self.author = sectionsFileParser.getValue("Author", "Header", encode=True)
			self.link = sectionsFileParser.getValue("Link", "Header", encode=True)
			self.icon = sectionsFileParser.getValue("ICOfile", "Header", encode=True) and \
						os.path.normpath(os.path.join(os.path.dirname(self.path),
													sectionsFileParser.getValue("ICOfile",
																				"Header",
																				encode=True))) or None
			self.previewImage = sectionsFileParser.getValue("PREVIEWfile", "Header", encode=True) and \
								os.path.normpath(os.path.join(os.path.dirname(self.path),
								 							sectionsFileParser.getValue("PREVIEWfile",
																						"Header",
																						encode=True))) or None
			self.backgroundImage = sectionsFileParser.getValue("BGfile", "Background", encode=True) and \
									os.path.normpath(os.path.join(os.path.dirname(self.path),
																sectionsFileParser.getValue("BGfile",
																							"Background",
																							encode=True))) or None
			self.lightingImage = sectionsFileParser.getValue("EVfile", "Enviroment", encode=True) and \
								os.path.normpath(os.path.join(os.path.dirname(self.path),
															sectionsFileParser.getValue("EVfile",
																						"Enviroment",
																						encode=True))) or None
			self.reflectionImage = sectionsFileParser.getValue("REFfile", "Reflection", encode=True) and \
									os.path.normpath(os.path.join(os.path.dirname(self.path),
																sectionsFileParser.getValue("REFfile",
																"Reflection",
																encode=True))) or None
			self.location = sectionsFileParser.getValue("Location", "Header", encode=True)
			self.latitude = sectionsFileParser.getValue("GEOlat", "Header", encode=True)
			self.longitude = sectionsFileParser.getValue("GEOlong", "Header", encode=True)
			self.date = sectionsFileParser.getValue("Date", "Header", encode=True)
			self.time = sectionsFileParser.getValue("Time", "Header", encode=True)
			self.comment = sectionsFileParser.getValue("Comment", "Header", encode=True)

			return True

		else:
			raise foundations.exceptions.FileStructureParsingError(
			"{0} | '{1}' no sections found, file structure seems invalid!".format(self.__class__.__name__, self.path))

class Template(Base):
	"""
	This class defines the Database Template type.
	"""

	__tablename__ = "Templates"
	"""Table name. ( String )"""

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
		This method initializes the class.

		:param name: Template name. ( String )
		:param path: Template file path. ( String )
		:param osStats: Template file statistics. ( String )
		:param collection: Template collection. ( String )
		:param helpFile: Template help file path. ( String )
		:param title: Template title. ( String )
		:param author: Template author. ( String )
		:param email: Template author email. ( String )
		:param url: Template online link. ( String )
		:param release: Template release version. ( String )
		:param date: Template release date. ( String )
		:param software: Template target software. ( String )
		:param version: Template target software version. ( String )
		:param renderer: Template target renderer. ( String )
		:param outputScript: Template loader script name. ( String )
		:param comment: Template comment. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

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

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileStructureParsingError)
	def setContent(self):
		"""
		This method initializes the class attributes.

		:return: Method success. ( Boolean )
		"""

		sectionsFileParser = SectionsFileParser(self.path)
		sectionsFileParser.read() and sectionsFileParser.parse(rawSections=("Script"))

		if sectionsFileParser.sections:
			self.helpFile = foundations.parsers.getAttributeCompound("HelpFile",
							sectionsFileParser.getValue("HelpFile",
														"Template",
														encode=True)).value and \
							os.path.join(os.path.dirname(self.path),
										foundations.parsers.getAttributeCompound("HelpFile",
										sectionsFileParser.getValue("HelpFile",
																	"Template",
																	encode=True)).value) or None
			self.title = foundations.parsers.getAttributeCompound("Name",
						sectionsFileParser.getValue("Name",
													"Template",
													encode=True)).value
			self.author = foundations.parsers.getAttributeCompound("Author",
						sectionsFileParser.getValue("Author",
													"Template",
													encode=True)).value
			self.email = foundations.parsers.getAttributeCompound("Email",
						sectionsFileParser.getValue("Email",
													"Template",
													encode=True)).value
			self.url = foundations.parsers.getAttributeCompound("Url",
						sectionsFileParser.getValue("Url",
													"Template",
													encode=True)).value
			self.release = foundations.parsers.getAttributeCompound("Release",
							sectionsFileParser.getValue("Release",
														"Template",
														encode=True)).value
			self.date = foundations.parsers.getAttributeCompound("Date",
						sectionsFileParser.getValue("Date",
													"Template",
													encode=True)).value
			self.software = foundations.parsers.getAttributeCompound("Software",
							sectionsFileParser.getValue("Software",
														"Template",
														encode=True)).value
			self.version = foundations.parsers.getAttributeCompound("Version",
							sectionsFileParser.getValue("Version",
														"Template",
														encode=True)).value
			self.renderer = foundations.parsers.getAttributeCompound("Renderer",
							sectionsFileParser.getValue("Renderer",
														"Template",
														encode=True)).value
			self.outputScript = foundations.parsers.getAttributeCompound("OutputScript",
								sectionsFileParser.getValue("OutputScript",
															"Template",
															encode=True)).value
			self.comment = foundations.parsers.getAttributeCompound("Comment",
							sectionsFileParser.getValue("Comment",
														"Template",
														encode=True)).value

			return True

		else:
			raise foundations.exceptions.FileStructureParsingError(
			"{0} | '{1}' no sections found, file structure seems invalid!".format(self.__class__.__name__, self.path))

class Collection(Base):
	"""
	This class defines the Database Collection type.
	"""

	__tablename__ = "Collections"
	"""Table name. ( String )"""

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	type = sqlalchemy.Column(sqlalchemy.String)
	comment = sqlalchemy.Column(sqlalchemy.String)

	def __init__(self, name=None, type=None, comment=None):
		"""
		This method initializes the class.

		:param name: Collection name. ( String )
		:param type: Collection type. ( String )
		:param comment: Collection comment. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.name = name
		self.type = type
		self.comment = comment
