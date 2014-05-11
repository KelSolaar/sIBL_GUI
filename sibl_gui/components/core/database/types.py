#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**types.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines Application Database types: :class:`IblSet`, :class:`Template`
	and :class:`Collection` classes.

**Others:**

"""

from __future__ import unicode_literals

import os
import sqlalchemy.ext.declarative
from sqlalchemy import ForeignKey

import foundations.exceptions
import foundations.parsers
import foundations.verbose
from foundations.parsers import SectionsFileParser

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Base", "IblSet", "Template", "Collection"]

LOGGER = foundations.verbose.install_logger()

Base = sqlalchemy.ext.declarative.declarative_base()

class IblSet(Base):
	"""
	Defines the Database ibl_sets type.
	"""

	__tablename__ = "ibl_sets"
	"""
	:param __tablename__: Table name.
	:type __tablename__: unicode
	"""

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	path = sqlalchemy.Column(sqlalchemy.String)
	os_stats = sqlalchemy.Column(sqlalchemy.String)
	collection = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("collections.id"))
	title = sqlalchemy.Column(sqlalchemy.String)
	author = sqlalchemy.Column(sqlalchemy.String)
	link = sqlalchemy.Column(sqlalchemy.String)
	icon = sqlalchemy.Column(sqlalchemy.String)
	preview_image = sqlalchemy.Column(sqlalchemy.String)
	background_image = sqlalchemy.Column(sqlalchemy.String)
	lighting_image = sqlalchemy.Column(sqlalchemy.String)
	reflection_image = sqlalchemy.Column(sqlalchemy.String)
	location = sqlalchemy.Column(sqlalchemy.String)
	latitude = sqlalchemy.Column(sqlalchemy.String)
	longitude = sqlalchemy.Column(sqlalchemy.String)
	date = sqlalchemy.Column(sqlalchemy.String)
	time = sqlalchemy.Column(sqlalchemy.String)
	comment = sqlalchemy.Column(sqlalchemy.String)

	def __init__(self,
			name=None,
			path=None,
			os_stats=None,
			collection=None,
			title=None,
			author=None,
			link=None,
			icon=None,
			preview_image=None,
			background_image=None,
			lighting_image=None,
			reflection_image=None,
			location=None,
			latitude=None,
			longitude=None,
			date=None,
			time=None,
			comment=None):
		"""
		Initializes the class.

		:param name: Ibl Set name.
		:type name: unicode
		:param path: Ibl Set file path.
		:type path: unicode
		:param os_stats: Ibl Set file statistics.
		:type os_stats: unicode
		:param collection: Ibl Set collection.
		:type collection: unicode
		:param title: Ibl Set title.
		:type title: unicode
		:param author: Ibl Set author.
		:type author: unicode
		:param link: Ibl Set online link.
		:type link: unicode
		:param icon: Ibl Set icon path.
		:type icon: unicode
		:param preview_image: Ibl Set preview image path.
		:type preview_image: unicode
		:param background_image: Ibl Set background image path.
		:type background_image: unicode
		:param lighting_image: Ibl Set lighting image path.
		:type lighting_image: unicode
		:param reflection_image: Ibl Set reflection image path.
		:type reflection_image: unicode
		:param location: Ibl Set location.
		:type location: unicode
		:param latitude: Ibl Set latitude.
		:type latitude: unicode
		:param longitude: Ibl Set longitude.
		:type longitude: unicode
		:param date: Ibl Set shot date.
		:type date: unicode
		:param time: Ibl Set shot time.
		:type time: unicode
		:param comment: Ibl Set comment.
		:type comment: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.name = name
		self.path = path
		self.os_stats = os_stats
		self.collection = collection
		self.title = title
		self.author = author
		self.link = link
		self.icon = icon
		self.preview_image = preview_image
		self.background_image = background_image
		self.lighting_image = lighting_image
		self.reflection_image = reflection_image
		self.location = location
		self.latitude = latitude
		self.longitude = longitude
		self.date = date
		self.time = time
		self.comment = comment

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileStructureParsingError)
	def set_content(self):
		"""
		Initializes the class attributes.

		:return: Method success.
		:rtype: bool
		"""

		sections_file_parser = SectionsFileParser(self.path)
		sections_file_parser.parse()

		if sections_file_parser.sections:
			self.title = sections_file_parser.get_value("Name", "Header")
			self.author = sections_file_parser.get_value("Author", "Header")
			self.link = sections_file_parser.get_value("Link", "Header")
			self.icon = os.path.normpath(os.path.join(os.path.dirname(self.path),
										sections_file_parser.get_value("ICOfile", "Header"))) \
										if sections_file_parser.get_value("ICOfile", "Header") else None
			self.preview_image = os.path.normpath(os.path.join(os.path.dirname(self.path),
								 				sections_file_parser.get_value("PREVIEWfile", "Header"))) \
								 				if sections_file_parser.get_value("PREVIEWfile", "Header") else None
			self.background_image = os.path.normpath(os.path.join(os.path.dirname(self.path),
													sections_file_parser.get_value("BGfile", "Background"))) \
													if sections_file_parser.get_value("BGfile", "Background") else None
			self.lighting_image = os.path.normpath(os.path.join(os.path.dirname(self.path),
												sections_file_parser.get_value("EVfile", "Enviroment"))) \
												if sections_file_parser.get_value("EVfile", "Enviroment") else None
			self.reflection_image = os.path.normpath(os.path.join(os.path.dirname(self.path),
													sections_file_parser.get_value("REFfile", "Reflection"))) \
													if sections_file_parser.get_value("REFfile", "Reflection") else None
			self.location = sections_file_parser.get_value("Location", "Header")
			self.latitude = sections_file_parser.get_value("GEOlat", "Header")
			self.longitude = sections_file_parser.get_value("GEOlong", "Header")
			self.date = sections_file_parser.get_value("Date", "Header")
			self.time = sections_file_parser.get_value("Time", "Header")
			self.comment = sections_file_parser.get_value("Comment", "Header")

			return True
		else:
			raise foundations.exceptions.FileStructureParsingError(
			"{0} | '{1}' no sections found, file structure seems invalid!".format(self.__class__.__name__, self.path))

class Template(Base):
	"""
	Defines the Database Template type.
	"""

	__tablename__ = "templates"
	"""
	:param __tablename__: Table name.
	:type __tablename__: unicode
	"""

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	path = sqlalchemy.Column(sqlalchemy.String)
	os_stats = sqlalchemy.Column(sqlalchemy.String)
	collection = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("collections.id"))
	help_file = sqlalchemy.Column(sqlalchemy.String)
	title = sqlalchemy.Column(sqlalchemy.String)
	author = sqlalchemy.Column(sqlalchemy.String)
	email = sqlalchemy.Column(sqlalchemy.String)
	url = sqlalchemy.Column(sqlalchemy.String)
	release = sqlalchemy.Column(sqlalchemy.String)
	date = sqlalchemy.Column(sqlalchemy.String)
	software = sqlalchemy.Column(sqlalchemy.String)
	version = sqlalchemy.Column(sqlalchemy.String)
	renderer = sqlalchemy.Column(sqlalchemy.String)
	output_script = sqlalchemy.Column(sqlalchemy.String)
	comment = sqlalchemy.Column(sqlalchemy.String)

	def __init__(self,
			name=None,
			path=None,
			os_stats=None,
			collection=None,
			help_file=None,
			title=None,
			author=None,
			email=None,
			url=None,
			release=None,
			date=None,
			software=None,
			version=None,
			renderer=None,
			output_script=None,
			comment=None):
		"""
		Initializes the class.

		:param name: Template name.
		:type name: unicode
		:param path: Template file path.
		:type path: unicode
		:param os_stats: Template file statistics.
		:type os_stats: unicode
		:param collection: Template collection.
		:type collection: unicode
		:param help_file: Template help file path.
		:type help_file: unicode
		:param title: Template title.
		:type title: unicode
		:param author: Template author.
		:type author: unicode
		:param email: Template author email.
		:type email: unicode
		:param url: Template online link.
		:type url: unicode
		:param release: Template release version.
		:type release: unicode
		:param date: Template release date.
		:type date: unicode
		:param software: Template target software.
		:type software: unicode
		:param version: Template target software version.
		:type version: unicode
		:param renderer: Template target renderer.
		:type renderer: unicode
		:param output_script: Template loader script name.
		:type output_script: unicode
		:param comment: Template comment.
		:type comment: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.name = name
		self.path = path
		self.os_stats = os_stats
		self.collection = collection
		self.help_file = help_file
		self.title = title
		self.author = author
		self.email = email
		self.url = url
		self.release = release
		self.date = date
		self.software = software
		self.version = version
		self.renderer = renderer
		self.output_script = output_script
		self.comment = comment

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileStructureParsingError)
	def set_content(self):
		"""
		Initializes the class attributes.

		:return: Method success.
		:rtype: bool
		"""

		sections_file_parser = SectionsFileParser(self.path)
		sections_file_parser.parse(raw_sections=("Script"))

		if sections_file_parser.sections:
			self.help_file = foundations.parsers.get_attribute_compound("HelpFile",
							sections_file_parser.get_value("HelpFile", "Template")).value and \
							os.path.join(os.path.dirname(self.path),
										foundations.parsers.get_attribute_compound("HelpFile",
										sections_file_parser.get_value("HelpFile", 	"Template")).value) or None
			self.title = foundations.parsers.get_attribute_compound("Name",
						sections_file_parser.get_value("Name", 	"Template")).value
			self.author = foundations.parsers.get_attribute_compound("Author",
						sections_file_parser.get_value("Author", "Template")).value
			self.email = foundations.parsers.get_attribute_compound("Email",
						sections_file_parser.get_value("Email", "Template")).value
			self.url = foundations.parsers.get_attribute_compound("Url",
						sections_file_parser.get_value("Url", "Template")).value
			self.release = foundations.parsers.get_attribute_compound("Release",
							sections_file_parser.get_value("Release", "Template")).value
			self.date = foundations.parsers.get_attribute_compound("Date",
						sections_file_parser.get_value("Date", "Template")).value
			self.software = foundations.parsers.get_attribute_compound("Software",
							sections_file_parser.get_value("Software", "Template")).value
			self.version = foundations.parsers.get_attribute_compound("Version",
							sections_file_parser.get_value("Version", "Template")).value
			self.renderer = foundations.parsers.get_attribute_compound("Renderer",
							sections_file_parser.get_value("Renderer", "Template")).value
			self.output_script = foundations.parsers.get_attribute_compound("OutputScript",
								sections_file_parser.get_value("OutputScript", "Template")).value
			self.comment = foundations.parsers.get_attribute_compound("Comment",
							sections_file_parser.get_value("Comment", "Template")).value

			return True

		else:
			raise foundations.exceptions.FileStructureParsingError(
			"{0} | '{1}' no sections found, file structure seems invalid!".format(self.__class__.__name__, self.path))

class Collection(Base):
	"""
	Defines the Database Collection type.
	"""

	__tablename__ = "collections"
	"""
	:param __tablename__: Table name.
	:type __tablename__: unicode
	"""

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	type = sqlalchemy.Column(sqlalchemy.String)
	comment = sqlalchemy.Column(sqlalchemy.String)

	def __init__(self, name=None, type=None, comment=None):
		"""
		Initializes the class.

		:param name: Collection name.
		:type name: unicode
		:param type: Collection type.
		:type type: unicode
		:param comment: Collection comment.
		:type comment: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.name = name
		self.type = type
		self.comment = comment
