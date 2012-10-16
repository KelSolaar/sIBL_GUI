#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**operations.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines Application Database operations objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import os
import re

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import sibl_gui.components.core.database.exceptions
from sibl_gui.components.core.database.types import DatabaseCollection
from sibl_gui.components.core.database.types import DatabaseIblSet
from sibl_gui.components.core.database.types import DatabaseTemplate

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "DATABASE_EXCEPTIONS"
			"commit",
			"addItem",
			"addStandardItem",
			"removeItem",
			"removeStandardItem",
			"updateItemContent",
			"updateItemLocation",
			"filterItems",
			"itemExists",
			"getIblSets",
			"filterIblSets",
			"iblSetExists",
			"addIblSet",
			"removeIblSet",
			"updateIblSetContent",
			"updateIblSetLocation",
			"checkIblSetsTableIntegrity",
			"getCollections",
			"filterCollections",
			"getCollectionsByType",
			"collectionExists",
			"addCollection",
			"removeCollection",
			"getCollectionsIblSets",
			"getTemplates",
			"filterTemplates",
			"templateExists",
			"addTemplate",
			"removeTemplate",
			"updateTemplateContent",
			"updateTemplateLocation",
			"checkTemplatesTableIntegrity"]

LOGGER = foundations.verbose.installLogger()

DATABASE_EXCEPTIONS = {
	sibl_gui.components.core.database.exceptions.MissingIblSetFileError : "Ibl Set's file is missing!",
	sibl_gui.components.core.database.exceptions.MissingIblSetIconError : "Ibl Set's icon is missing!",
	sibl_gui.components.core.database.exceptions.MissingIblSetPreviewImageError : "Ibl Set's preview image is missing!",
	sibl_gui.components.core.database.exceptions.MissingIblSetBackgroundImageError : "Ibl Set's background image is missing!",
	sibl_gui.components.core.database.exceptions.MissingIblSetLightingImageError : "Ibl Set's lighting image is missing!",
	sibl_gui.components.core.database.exceptions.MissingIblSetReflectionImageError : "Ibl Set's reflection image is missing!",
	sibl_gui.components.core.database.exceptions.MissingTemplateFileError : "Template file is missing!",
	sibl_gui.components.core.database.exceptions.MissingTemplateHelpFileError : "Template help file is missing!"}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@foundations.exceptions.handleExceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
def commit(session):
	"""
	This definition commits changes to the Database.

	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	try:
		session.commit()
		return True
	except Exception as error:
		session.rollback()
		raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
		"{0} | Database commit error: '{1}'".format(inspect.getmodulename(__file__), error))

def addItem(session, item):
	"""
	This definition adds an item to the Database.

	:param session: Database session. ( Session )
	:param item: Item to add. ( Database object )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' item to the Database.".format(item))

	session.add(item)

	return commit(session)

def addStandardItem(session, type, name, path, collection):
	"""
	This definition adds a new standard item to the Database.

	:param type: Item type. ( Object )
	:param session: Database session. ( Session )
	:param name: Item name. ( String )
	:param path: Item path. ( String )
	:param collection: Collection id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' '{1}' to the Database.".format(name, type.__name__))

	if not filterItems(session, session.query(type), "^{0}$".format(re.escape(path)), "path"):
		osStats = ",".join((foundations.strings.encode(stat) for stat in os.stat(path)))
		databaseItem = type(name=name, path=path, collection=collection, osStats=osStats)
		if databaseItem.setContent():
			return addItem(session, databaseItem)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' path already exists in Database!".format(
		inspect.getmodule(addStandardItem).__name__, path, type.__name__))
		return False

def removeItem(session, item):
	"""
	This definition removes an item from the Database.

	:param session: Database session. ( Session )
	:param item: Item to remove. ( Database object )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Removing: '{0}' item from the Database.".format(item))

	session.delete(item)

	return commit(session)

def removeStandardItem(session, type, identity):
	"""
	This definition removes a standard item from the Database.

	:param session: Database session. ( Session )
	:param type: Item type. ( Object )
	:param identity: Item id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Removing item type '{0}' with id '{1}' from the Database.".format(type.__name__, identity))

	item = session.query(type).filter_by(id=identity).one()
	return removeItem(session, item)

def updateItemContent(session, item):
	"""
	This definition update an item content.

	:param session: Database session. ( Session )
	:param item: Item to set content. ( DatabaseIblSet )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Updating '{0}' '{1}' content.".format(item.name, item.__class__.__name__))

	item.osStats = ",".join((foundations.strings.encode(stat) for stat in os.stat(item.path)))
	if item.setContent():
		return commit(session)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' content update failed!".format(inspect.getmodulename(updateItemContent),
		item.name, item.__class__.__name__))
		return False

def updateItemLocation(session, item, path):
	"""
	This definition updates an item location.

	:param session: Database session. ( Session )
	:param item: Item to update. ( Object )
	:param path: Item path. ( Path )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Updating '{0}' '{1}' location.".format(item, item.__class__.__name__))

	if not filterItems(session, session.query(item.__class__), "^{0}$".format(re.escape(path)), "path"):
		item.path = path
		return updateItemContent(session, item)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' path already exists in Database!".format(
		inspect.getmodulename(updateItemLocation), path, item.__class__.__name__))
		return False

def filterItems(session, items, pattern, field, flags=0):
	"""
	This definition filters items from the Database.

	:param session: Database session. ( Session )
	:param items: Database items. ( List )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered items. ( List )
	"""

	return [item for item in items if re.search(pattern, foundations.strings.encode(item.__dict__[field]), flags)]

def itemExists(session, items, pattern, field, flags=0):
	"""
	This definition returns if given item exists in the Database.

	:param session: Database session. ( Session )
	:param items: Database items. ( List )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered items. ( List )
	"""

	return filterItems(session, items, pattern, field, flags) and True or False

def getIblSets(session):
	"""
	This definition returns the Ibl Sets from the Database.

	:param session: Database session. ( Session )
	:return: Database Ibl Sets. ( List )
	"""

	return session.query(DatabaseIblSet)

def filterIblSets(session, pattern, field, flags=0):
	"""
	This definition filters the sets from the Database.

	:param session: Database session. ( Session )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered Ibl Sets. ( List )
	"""

	return filterItems(session, getIblSets(session), pattern, field, flags)

def iblSetExists(session, path):
	"""
	This method returns if given Ibl Set exists in the Database.

	:param name: Ibl Set path. ( String )
	:return: Ibl Set exists. ( Boolean )
	"""

	return filterIblSets(session, "^{0}$".format(re.escape(path)), "path") and True or False

def addIblSet(session, name, path, collection):
	"""
	This definition adds a new Ibl Set to the Database.

	:param session: Database session. ( Session )
	:param name: Ibl Set name. ( String )
	:param path: Ibl Set path. ( String )
	:param collection: Collection id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return addStandardItem(session, DatabaseIblSet, name, path, collection)

def removeIblSet(session, identity):
	"""
	This definition removes an Ibl Set from the Database.

	:param session: Database session. ( Session )
	:param identity: Ibl Set id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return removeStandardItem(session, DatabaseIblSet, identity)

def updateIblSetContent(session, iblSet):
	"""
	This definition update an Ibl Set content.

	:param session: Database session. ( Session )
	:param iblSet: Ibl Set to set content. ( DatabaseIblSet )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemContent(session, iblSet)

def updateIblSetLocation(session, iblSet, path):
	"""
	This definition updates an Ibl Set location.

	:param session: Database session. ( Session )
	:param iblSet: Ibl Set to update. ( DatabaseIblSet )
	:param path: Ibl Set path. ( Path )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemLocation(session, iblSet, path)

def checkIblSetsTableIntegrity(session):
	"""
	This definition checks sets table integrity.

	:param session: Database session. ( Session )
	:return: Ibl Sets table erroneous items. ( Dictionary )
	"""

	LOGGER.debug("> Checking 'Sets' Database table integrity.")

	erroneousIblSets = {}
	if getIblSets(session):
		for iblSet in getIblSets(session):
			exceptions = []
			if not foundations.common.pathExists(iblSet.path):
				exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetFileError)

			if not foundations.common.pathExists(iblSet.icon):
				exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetIconError)

			if iblSet.previewImage and not foundations.common.pathExists(os.path.join(os.path.dirname(iblSet.path),
																	iblSet.previewImage)):
				exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetPreviewImageError)
			if iblSet.backgroundImage and not foundations.common.pathExists(os.path.join(os.path.dirname(iblSet.path),
																		iblSet.backgroundImage)):
				exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetBackgroundImageError)
			if iblSet.lightingImage and not foundations.common.pathExists(os.path.join(os.path.dirname(iblSet.path),
																		iblSet.lightingImage)):
				exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetLightingImageError)
			if iblSet.reflectionImage and not foundations.common.pathExists(os.path.join(os.path.dirname(iblSet.path),
																		iblSet.reflectionImage)):
				exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetReflectionImageError)

			if exceptions:
				erroneousIblSets[iblSet] = exceptions

	return erroneousIblSets

def getCollections(session):
	"""
	This definition returns the Collections from the Database.

	:param session: Database session. ( Session )
	:return: Database Collections. ( List )
	"""

	return session.query(DatabaseCollection)

def filterCollections(session, pattern, field, flags=0):
	"""
	This definition filters the Collections from the Database.

	:param session: Database session. ( Session )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered Collections. ( List )
	"""

	return filterItems(session, getCollections(session), pattern, field, flags)

def getCollectionsByType(session, type):
	"""
	This method returns Collections of given type.

	:param session: Database session. ( Session )
	:param type: Type name. ( String )
	:return: Ibl Sets Collections. ( List )
	"""

	return [collection for collection in filterCollections(session, type, "type")]

def filterCollectionsByType(session, type, pattern, field, flags=0):
	"""
	This definition filters the Ibl Sets Collections from the Database.

	:param session: Database session. ( Session )
	:param type: Type name. ( String )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered Collections. ( List )
	"""

	return list(set(getCollectionsByType(session, type)).intersection(
	filterCollections(session, "{0}".format(pattern), field, flags)))

def filterIblSetsCollections(session, pattern, field, flags=0):
	"""
	This definition filters the Ibl Sets Collections from the Database.

	:param session: Database session. ( Session )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered Collections. ( List )
	"""

	return filterCollectionsByType(session, "IblSets", pattern, field, flags)

def filterTemplatesCollections(session, pattern, field, flags=0):
	"""
	This definition filters the Templates Collections from the Database.

	:param session: Database session. ( Session )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered Collections. ( List )
	"""

	return filterCollectionsByType(session, "Templates", pattern, field, flags)

def collectionExists(session, name):
	"""
	This method returns if the Collection exists in the Database.

	:param name: Collection name. ( String )
	:return: Collection exists. ( Boolean )
	"""

	return filterCollections(session, "^{0}$".format(name), "name") and True or False

def addCollection(session, collection, type, comment):
	"""
	This definition adds a Collection to the Database.

	:param session: Database session. ( Session )
	:param collection: Collection name. ( String )
	:param type: Collection type. ( String )
	:param comment: Collection comment. ( String )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' Collection of type '{1}' to the Database.".format(collection, type))

	if not filterCollections(session, "^{0}$".format(collection), "name"):
		databaseItem = DatabaseCollection(name=collection, type=type, comment=comment)
		return addItem(session, databaseItem)
	else:
		LOGGER.warning("!> {0} | '{1}' Collection already exists in Database!".format(
		inspect.getmodulename(addCollection), collection))
		return False

def removeCollection(session, identity):
	"""
	This definition removes a Collection from the Database.

	:param session: Database session. ( Session )
	:param identity: Collection id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return removeStandardItem(session, DatabaseCollection, identity)

def getCollectionsIblSets(session, identities):
	"""
	This definition returns Ibl Sets from Collections ids

	:param session: Database session. ( Session )
	:param identities: Collections ids. ( List )
	:return: Ibl Sets list. ( List )
	"""

	iblSets = []
	for identity in identities:
		collectionSets = filterIblSets(session, "^{0}$".format(identity), "collection")
		if collectionSets:
			for iblSet in collectionSets:
				iblSets.append(iblSet)
	return iblSets

def getTemplates(session):
	"""
	This definition returns the Templates from the Database.

	:param session: Database session. ( Session )
	:return: Database Templates. ( List )
	"""

	return session.query(DatabaseTemplate)

def filterTemplates(session, pattern, field, flags=0):
	"""
	This definition filters the Templates from the Database.

	:param session: Database session. ( Session )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered Templates. ( List )
	"""

	return filterItems(session, getTemplates(session), pattern, field, flags)

def templateExists(session, path):
	"""
	This method returns if given Template exists in the Database.

	:param name: Template path. ( String )
	:return: Template exists. ( Boolean )
	"""

	return filterTemplates(session, "^{0}$".format(re.escape(path)), "path") and True or False

def addTemplate(session, name, path, collection):
	"""
	This definition adds a new Template to the Database.

	:param session: Database session. ( Session )
	:param name: Template name. ( String )
	:param path: Template path. ( String )
	:param collection: Collection id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return addStandardItem(session, DatabaseTemplate, name, path, collection)

def removeTemplate(session, identity):
	"""
	This definition removes a Template from the Database.

	:param session: Database session. ( Session )
	:param identity: Template id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return removeStandardItem(session, DatabaseTemplate, identity)

def updateTemplateContent(session, template):
	"""
	This definition update a Template content.

	:param session: Database session. ( Session )
	:param template: Template to Template content. ( DatabaseTemplate )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemContent(session, template)

def updateTemplateLocation(session, template, path):
	"""
	This definition updates a Template location.

	:param session: Database session. ( Session )
	:param template: Template to update. ( DatabaseTemplate )
	:param path: Template path. ( Path )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemLocation(session, template, path)

def checkTemplatesTableIntegrity(session):
	"""
	This definition checks Templates table integrity.

	:param session: Database session. ( Session )
	:return: Templates table erroneous items. ( Dictionary )
	"""

	LOGGER.debug("> Checking 'Templates' Database table integrity.")

	erroneousTemplates = {}
	if getTemplates(session):
		for template in getTemplates(session):
			exceptions = []
			if not foundations.common.pathExists(template.path):
				exceptions.append(sibl_gui.components.core.database.exceptions.MissingTemplateFileError)

			if not foundations.common.pathExists(template.helpFile):
				exceptions.append(sibl_gui.components.core.database.exceptions.MissingTemplateHelpFileError)

			if exceptions:
				erroneousTemplates[template] = exceptions

	return erroneousTemplates
