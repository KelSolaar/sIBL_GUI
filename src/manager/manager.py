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
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	manager.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Manager Module.
***
***	Others:
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import inspect
import logging
import os
import sys
import re

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from component import Component
from uiComponent import UiComponent
from foundations.parser import Parser
from foundations.walker import Walker
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Profile(object):
	'''
	This Class Is The Profile Class.
	'''

	@core.executionTrace
	def __init__(self, name=None, path=None):
		'''
		This Method Initializes The Class.
		
		@param name: Name Of The Component. ( String )
		@param path: Path Of The Component. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self._name = None
		self.name = name
		self.path = None
		self._path = path

		self._object_ = None
		self._rank = None
		self._import = None
		self._interface = None
		self._categorie = None

		self._module = None
		self._version = None
		self._author = None
		self._email = None
		self._url = None
		self._description = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def name(self):
		'''
		This Method Is The Property For The _name Attribute.

		@return: self._name. ( String )
		'''

		return self._name

	@name.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def name(self, value):
		'''
		This Method Is The Setter Method For The _name Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("name", value)
		self._name = value

	@name.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def name(self):
		'''
		This Method Is The Deleter Method For The _name Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("name"))

	@property
	def path(self):
		'''
		This Method Is The Property For The _path Attribute.

		@return: self._path. ( String )
		'''

		return self._path

	@path.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def path(self, value):
		'''
		This Method Is The Setter Method For The _path Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("path", value)
			assert os.path.exists(value), "'{0}' Attribute : '{1}' Directory Doesn't Exists !".format("path", value)
		self._path = value

	@path.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def path(self):
		'''
		This Method Is The Deleter Method For The _path Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("path"))

	@property
	def object_(self):
		'''
		This Method Is The Property For The _object_ Attribute.

		@return: self._object_. ( String )
		'''

		return self._object_

	@object_.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def object_(self, value):
		'''
		This Method Is The Setter Method For The _object_ Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("object_", value)
		self._object_ = value

	@object_.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def object_(self):
		'''
		This Method Is The Deleter Method For The _object_ Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("object_"))

	@property
	def rank(self):
		'''
		This Method Is The Property For The _rank Attribute.

		@return: self._rank. ( String )
		'''

		return self._rank

	@rank.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def rank(self, value):
		'''
		This Method Is The Setter Method For The _rank Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("rank", value)
		self._rank = value

	@rank.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rank(self):
		'''
		This Method Is The Deleter Method For The _rank Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("rank"))

	@property
	def import_(self):
		'''
		This Method Is The Property For The _import_ Attribute.

		@return: self._import. ( Module )
		'''

		return self._import

	@import_.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def import_(self, value):
		'''
		This Method Is The Setter Method For The _import_ Attribute.
		
		@param value: Attribute Value. ( Module )
		'''

		if value:
			assert type(value) is type(sys), "'{0}' Attribute : '{1}' Type Is Not 'module' !".format("import", value)
		self._import = value

	@import_.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def import_(self):
		'''
		This Method Is The Deleter Method For The _import_ Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("import"))

	@property
	def interface(self):
		'''
		This Method Is The Property For The _interface Attribute.

		@return: self._interface. ( Object )
		'''

		return self._interface

	@interface.setter
	def interface(self, value):
		'''
		This Method Is The Setter Method For The _interface Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		self._interface = value

	@interface.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def interface(self):
		'''
		This Method Is The Deleter Method For The _interface Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("interface"))

	@property
	def categorie(self):
		'''
		This Method Is The Property For The _categorie Attribute.

		@return: self._categorie. ( String )
		'''

		return self._categorie

	@categorie.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def categorie(self, value):
		'''
		This Method Is The Setter Method For The _categorie Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("categorie", value)
		self._categorie = value

	@categorie.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def categorie(self):
		'''
		This Method Is The Deleter Method For The _categorie Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("categorie"))

	@property
	def module(self):
		'''
		This Method Is The Property For The _module Attribute.

		@return: self._module. ( String )
		'''

		return self._module

	@module.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def module(self, value):
		'''
		This Method Is The Setter Method For The _module Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("module", value)
		self._module = value

	@module.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def module(self):
		'''
		This Method Is The Deleter Method For The _module Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("module"))

	@property
	def version(self):
		'''
		This Method Is The Property For The _version Attribute.

		@return: self._version. ( String )
		'''

		return self._version

	@version.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def version(self, value):
		'''
		This Method Is The Setter Method For The _version Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("version", value)
		self._version = value

	@version.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def version(self):
		'''
		This Method Is The Deleter Method For The _version Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("version"))

	@property
	def author(self):
		'''
		This Method Is The Property For The _author Attribute.

		@return: self._author. ( String )
		'''

		return self._author

	@author.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def author(self, value):
		'''
		This Method Is The Setter Method For The _author Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("author", value)
		self._author = value

	@author.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def author(self):
		'''
		This Method Is The Deleter Method For The _author Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("author"))

	@property
	def email(self):
		'''
		This Method Is The Property For The _email Attribute.

		@return: self._email. ( String )
		'''

		return self._email

	@email.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def email(self, value):
		'''
		This Method Is The Setter Method For The _email Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("email", value)
		self._email = value

	@email.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def email(self):
		'''
		This Method Is The Deleter Method For The _email Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("email"))

	@property
	def url(self):
		'''
		This Method Is The Property For The _url Attribute.

		@return: self._url. ( String )
		'''

		return self._url

	@url.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def url(self, value):
		'''
		This Method Is The Setter Method For The _url Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("url", value)
		self._url = value

	@url.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def url(self):
		'''
		This Method Is The Deleter Method For The _url Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("url"))

	@property
	def description(self):
		'''
		This Method Is The Property For The _description Attribute.

		@return: self._description. ( String )
		'''

		return self._description

	@description.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def description(self, value):
		'''
		This Method Is The Setter Method For The _description Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("description", value)
		self._description = value

	@description.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def description(self):
		'''
		This Method Is The Deleter Method For The _description Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("description"))

class Manager(object):
	'''
	This Class Is The Manager Class.
	'''

	@core.executionTrace
	def __init__(self, paths=None, extension="rc", categories={ "default" : Component, "ui" : UiComponent }):
		'''
		This Method Initializes The Class.
		@param paths: Paths To Walk. ( Dictionary )
		@param extension: Extension To Look After. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self._paths = None
		self.paths = paths
		self._extension = None
		self.extension = extension
		self._categories = None
		self.categories = categories
		self._components = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def paths(self):
		'''
		This Method Is The Property For The _paths Attribute.

		@return: self._paths. ( Dictionary )
		'''

		return self._paths

	@paths.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def paths(self, value):
		'''
		This Method Is The Setter Method For The _paths Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		'''

		if value:
			assert type(value) is dict, "'{0}' Attribute : '{1}' Type Is Not 'dict' !".format("paths", value)
			for path in value.values() : assert os.path.exists(path), "'{0}' Attribute : '{1}' Directory Doesn't Exists !".format("paths", path)
		self._paths = value

	@paths.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def paths(self):
		'''
		This Method Is The Deleter Method For The _paths Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("paths"))

	@property
	def extension(self):
		'''
		This Method Is The Property For The _extension Attribute.

		@return: self._extension. ( String )
		'''

		return self._extension

	@extension.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def extension(self, value):
		'''
		This Method Is The Setter Method For The _extension Attribute.

		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format("extension", value)
		self._extension = value

	@extension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self):
		'''
		This Method Is The Deleter Method For The _extension Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("extension"))

	@property
	def categories(self):
		'''
		This Method Is The Property For The _categories Attribute.

		@return: self._categories. ( Dictionary )
		'''

		return self._categories

	@categories.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def categories(self, value):
		'''
		This Method Is The Setter Method For The _categories Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		'''

		if value:
			assert type(value) is dict, "'{0}' Attribute : '{1}' Type Is Not 'dict' !".format("categories", value)
		self._categories = value

	@categories.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def categories(self):
		'''
		This Method Is The Deleter Method For The _categories Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("categories"))

	@property
	def components(self):
		'''
		This Method Is The Property For The _components Attribute.

		@return: self._components. ( Dictionary )
		'''

		return self._components

	@components.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def components(self, value):
		'''
		This Method Is The Setter Method For The _components Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only !".format("components"))

	@components.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def components(self):
		'''
		This Method Is The Deleter Method For The _components Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable !".format("components"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileStructureError)
	def getProfile(self, file):
		'''
		This Method Gets Provided Component Profile.

		@param file: File Path. ( String )
		@return: Profile. ( Profile )
		'''

		LOGGER.debug("> Building '{0}' Profile.".format(file))

		parser = Parser(file)
		parser.read() and parser.parse()

		if parser.sections:
			profile = Profile()
			profile.path = os.path.dirname(file)
			profile.name = parser.attributeExists("Name", "Component") and parser.getValue("Name", "Component") or None
			if not profile.name:
				raise foundations.exceptions.FileStructureError("'{0}' No '{1}' Attribute Found, File Structure Seems Invalid !".format(file, "Name"))
			profile.path = os.path.dirname(file)
			profile.module = parser.attributeExists("Module", "Component") and parser.getValue("Module", "Component") or None
			if not profile.module:
				raise foundations.exceptions.FileStructureError("'{0}' No '{1}' Attribute Found, File Structure Seems Invalid !".format(file, "Module"))
			profile.object_ = parser.attributeExists("Object", "Component") and parser.getValue("Object", "Component") or None
			if not profile.object_:
				raise foundations.exceptions.FileStructureError("'{0}' No '{1}' Attribute Found, File Structure Seems Invalid !".format(file, "Object"))
			profile.rank = parser.attributeExists("Rank", "Component") and parser.getValue("Rank", "Component") or None
			if not profile.rank:
				raise foundations.exceptions.FileStructureError("'{0}' No '{1}' Attribute Found, File Structure Seems Invalid !".format(file, "Rank"))
			profile.version = parser.attributeExists("Version", "Component") and parser.getValue("Version", "Component") or None
			if not profile.version:
				raise foundations.exceptions.FileStructureError("'{0}' No '{1}' Attribute Found, File Structure Seems Invalid !".format(file, "Version"))
			profile.author = parser.attributeExists("Author", "Informations") and parser.getValue("Author", "Informations") or None
			profile.email = parser.attributeExists("Email", "Informations") and parser.getValue("Email", "Informations") or None
			profile.url = parser.attributeExists("Url", "Informations") and parser.getValue("Url", "Informations") or None
			profile.description = parser.attributeExists("Description", "Informations") and parser.getValue("Description", "Informations") or None

			return profile
		else:
			raise foundations.exceptions.FileStructureError("'{0}' No Sections Found, File Structure Seems Invalid !".format(file))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def gatherComponents(self):
		'''
		This Method Gather The Components.
		'''

		if self.paths:
			self._components = {}
			walker = Walker()
			for path in self.paths.keys():
				walker.root = self.paths[path]
				walker.walk(("\.{0}$".format(self._extension),), ("\._",))
				for component in walker.files.keys():
					LOGGER.debug("> Current Component : '{0}'.".format(component))
					profile = self.getProfile(walker.files[component])
					if profile:
						if os.path.isfile(os.path.join(profile.path, profile.module) + ".py"):
							self._components[profile.name] = profile
						else:
							LOGGER.warning("!> {0} | '{1}' Has No Associated Module And Has Been Rejected !".format(self.__class__.__name__, component))
							continue
					else:
						LOGGER.warning("!> {0} | '{1}' Is Not A Valid Component And Has Been Rejected !".format(self.__class__.__name__, component))
		else:
			raise foundations.exceptions.ProgrammingError("'{0}' Has No Components Paths Defined !".format(self))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError, ImportError)
	def instantiateComponents(self, callback=None):
		'''
		This Method Instantiates The Components.

		@param callback: Callback Object. ( Object )
		'''

		assert self._components, "'{0}' Manager Has No Components !".format(self)

		for component in self.getComponents():
			profile = self._components[component]
			callback and callback(profile)

			LOGGER.debug("> Current Component : '{0}'.".format(component))

			sys.path.append(profile.path)
			profile.import_ = __import__(profile.module)
			object_ = profile.object_ in profile._import.__dict__ and getattr(profile.import_, profile.object_) or None
			if object_ and inspect.isclass(object_):
				for categorie, type in self._categories.items():
					profile.categorie = categorie
					profile.interface = issubclass(object_, type) and object_ is not type and object_(name=profile.name) or None
					if profile.interface:
						LOGGER.info("{0} | '{1}' Component Has Been Instantiated !".format(self.__class__.__name__, profile.name))
						break
			else:
				LOGGER.error("{0} | '{1}' Component Has No Interface And Has Been Rejected !".format(self.__class__.__name__, profile.name))
				del(self._components[component])

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def deleteComponent(self, component):
		'''
		This Method Removes The Provided Component.

		@param component: Component To Remove. ( List )
		@return: Deletion Success. ( Boolean )
		'''

		del(self._components[component])
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def clearComponents(self):
		'''
		This Method Clears The Components.

		@return: Clearing Success. ( Boolean )
		'''

		self._components.clear()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, ImportError)
	def reloadComponent(self, component):
		'''
		This Method Reload The Provided Component.
		
		@param callback: Callback Object. ( Object )
		@return: Reload Success. ( Boolean )
		'''

		profile = self._components[component]
		import_ = __import__(profile.module)
		reload(import_)
		object_ = profile.object_ in dir(import_) and getattr(import_, profile.object_) or None
		if object_ and inspect.isclass(object_):
			interface = issubclass(object_, self._categories[profile.categorie]) and object_ is not self._categories[profile.categorie] and object_(name=profile.name) or None
			if interface:
				LOGGER.info("{0} | '{1}' Component Has Been Reloaded !".format(self.__class__.__name__, profile.name))
				profile.import_ = import_
				profile.interface = interface

				return True

	@core.executionTrace
	def getComponents(self):
		'''
		This Method Gets The Components By Ranking.
		'''

		return [component[0] for component in sorted([(component, profile.rank) for component, profile in self._components.items()], key=lambda x:(int(x[1])))]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def filterComponents(self, pattern, categorie=None):
		'''
		This Method Filters The Components Using The Provided Pattern.
		
		@param pattern: Regex Filtering Pattern. ( String )
		@param categorie: Categorie Filter. ( String )
		@return: Matching Items. ( List )
		'''

		assert self._components is not None, "'{0}' Manager Has No Components !".format(self)
		matchingItems = []
		for component, profile in self._components.items():
			if categorie:
				if profile.categorie != categorie : continue
			if re.search(pattern, component):
				matchingItems.append(component)
		return matchingItems

	@core.executionTrace
	def getInterface(self, component):
		'''
		This Method Gets The Component Interface.
		
		@param component: Component To Get The Interface.
		@return: Component Interface. ( Object )
		'''

		components = self.filterComponents("^" + component + "$")
		if components != [] : return self._components[components[0]].interface

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
