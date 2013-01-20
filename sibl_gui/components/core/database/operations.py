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
import os
import re

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import sibl_gui.components.core.database.exceptions
from sibl_gui.components.core.database.types import Collection
from sibl_gui.components.core.database.types import IblSet
from sibl_gui.components.core.database.types import Template

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"DATABASE_EXCEPTIONS",
			"DEFAULT_SESSION_MAKER",
			"DEFAULT_SESSION",
			"createSession",
			"getSession",
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
			"getCollectionIblSetsCount",
			"getCollectionTemplatesCount",
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

DEFAULT_SESSION_MAKER = None
DEFAULT_SESSION = None

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def createSession():
	"""
	This definition creates a default session.

	:return: Database session. ( Session )
	"""

	return DEFAULT_SESSION_MAKER()

def getSession(session=None):
	"""
	This definition returns either given session or the default one.

	:param session: Database session. ( Session )
	:return: Database session. ( Session )
	"""

	if session is not None:
		return session

	if DEFAULT_SESSION is not None:
		return DEFAULT_SESSION
	else:
		LOGGER.warning("!> {0} | Default session is not set, creating one!".format(__name__))

def query(*args, **kwargs):
	"""
	This definition queries given session or the default one.

	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	:return: Query result. ( Object )
	"""

	return getSession(kwargs.get("session")).query(*args, **kwargs)

@foundations.exceptions.handleExceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
def commit(session=None):
	"""
	This definition commits changes to the Database.

	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	session = getSession(session)

	try:
		session.commit()
		return True
	except Exception as error:
		session.rollback()
		raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
		"{0} | Database commit error: '{1}'".format(__name__, error))

def addItem(item, session=None):
	"""
	This definition adds an item to the Database.

	:param item: Item to add. ( Database object )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' item to the Database.".format(item))

	session = getSession(session)
	session.add(item)
	return commit(session)

def addStandardItem(type, name, path, collection, session=None):
	"""
	This definition adds a new standard item to the Database.

	:param type: Item type. ( Object )
	:param name: Item name. ( String )
	:param path: Item path. ( String )
	:param collection: Collection id. ( String )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' '{1}' to the Database.".format(name, type.__name__))

	session = getSession(session)

	if not filterItems(query(type), "^{0}$".format(re.escape(path)), "path"):
		osStats = ",".join((foundations.strings.encode(stat) for stat in os.stat(path)))
		databaseItem = type(name=name, path=path, collection=collection, osStats=osStats)
		if databaseItem.setContent():
			return addItem(databaseItem, session)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' path already exists in Database!".format(__name__, path, type.__name__))
		return False

def removeItem(item, session=None):
	"""
	This definition removes an item from the Database.

	:param item: Item to remove. ( Database object )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Removing: '{0}' item from the Database.".format(item))

	session = getSession(session)
	session.delete(item)
	return commit(session)

def removeStandardItem(type, identity, session=None):
	"""
	This definition removes a standard item from the Database.

	:param type: Item type. ( Object )
	:param identity: Item id. ( String )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Removing item type '{0}' with id '{1}' from the Database.".format(type.__name__, identity))

	item = session.query(type).filter_by(id=identity).one()
	return removeItem(item, getSession(session))

def updateItemContent(item, session=None):
	"""
	This definition update an item content.

	:param item: Item to set content. ( IblSet )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Updating '{0}' '{1}' content.".format(item.name, item.__class__.__name__))

	item.osStats = ",".join(map(foundations.strings.encode, os.stat(item.path)))
	if item.setContent():
		return commit(getSession(session))
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' content update failed!".format(__name__,
																		item.name,
																		item.__class__.__name__))
		return False

def updateItemLocation(item, path, session=None):
	"""
	This definition updates an item location.

	:param item: Item to update. ( Object )
	:param path: Item path. ( Path )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Updating '{0}' '{1}' location.".format(item, item.__class__.__name__))

	session = getSession(session)

	if not filterItems(query(item.__class__), "^{0}$".format(re.escape(path)), "path"):
		item.path = path
		return updateItemContent(item, session)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' path already exists in Database!".format(__name__,
																					path,
																					item.__class__.__name__))
		return False

def filterItems(items, pattern, field, flags=0):
	"""
	This definition filters items from the Database.

	:param items: Database items. ( List )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered items. ( List )
	"""

	return [item for item in items if re.search(pattern, foundations.strings.encode(item.__dict__[field]), flags)]

def itemExists(items, pattern, field, flags=0):
	"""
	This definition returns if given item exists in the Database.

	:param items: Database items. ( List )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:return: Filtered items. ( List )
	"""

	return filterItems(items, pattern, field, flags) and True or False

def getIblSets(session=None):
	"""
	This definition returns the Ibl Sets from the Database.

	:param session: Database session. ( Session )
	:return: Database Ibl Sets. ( List )
	"""

	return getSession(session).query(IblSet)

def filterIblSets(pattern, field, flags=0, session=None):
	"""
	This definition filters the sets from the Database.

	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:param session: Database session. ( Session )
	:return: Filtered Ibl Sets. ( List )
	"""

	return filterItems(getIblSets(getSession(session)), pattern, field, flags)

def iblSetExists(path, session=None):
	"""
	This method returns if given Ibl Set exists in the Database.

	:param name: Ibl Set path. ( String )
	:param session: Database session. ( Session )
	:return: Ibl Set exists. ( Boolean )
	"""

	return filterIblSets("^{0}$".format(re.escape(path)), "path", session=getSession(session)) and True or False

def addIblSet(name, path, collection, session=None):
	"""
	This definition adds a new Ibl Set to the Database.

	:param name: Ibl Set name. ( String )
	:param path: Ibl Set path. ( String )
	:param collection: Collection id. ( String )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	return addStandardItem(IblSet, name, path, collection, getSession(session))

def removeIblSet(identity, session=None):
	"""
	This definition removes an Ibl Set from the Database.

	:param identity: Ibl Set id. ( String )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	return removeStandardItem(IblSet, identity, getSession(session))

def updateIblSetContent(iblSet, session=None):
	"""
	This definition update an Ibl Set content.

	:param iblSet: Ibl Set to set content. ( IblSet )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemContent(iblSet, getSession(session))

def updateIblSetLocation(iblSet, path, session=None):
	"""
	This definition updates an Ibl Set location.

	:param iblSet: Ibl Set to update. ( IblSet )
	:param path: Ibl Set path. ( Path )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemLocation(iblSet, path, getSession(session))

def checkIblSetsTableIntegrity(session=None):
	"""
	This definition checks sets table integrity.

	:param session: Database session. ( Session )
	:return: Ibl Sets table erroneous items. ( Dictionary )
	"""

	LOGGER.debug("> Checking 'Sets' Database table integrity.")

	session = getSession(session)

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

def getCollections(session=None):
	"""
	This definition returns the Collections from the Database.

	:param session: Database session. ( Session )
	:return: Database Collections. ( List )
	"""

	return getSession(session).query(Collection)

def filterCollections(pattern, field, flags=0, session=None):
	"""
	This definition filters the Collections from the Database.

	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:param session: Database session. ( Session )
	:return: Filtered Collections. ( List )
	"""

	return filterItems(getCollections(getSession(session)), pattern, field, flags)

def getCollectionsByType(type, session=None):
	"""
	This method returns Collections of given type.

	:param type: Type name. ( String )
	:param session: Database session. ( Session )
	:return: Ibl Sets Collections. ( List )
	"""

	return [collection for collection in filterCollections(type, "type", session=getSession(session))]

def filterCollectionsByType(type, pattern, field, flags=0, session=None):
	"""
	This definition filters the Ibl Sets Collections from the Database.

	:param type: Type name. ( String )
	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:param session: Database session. ( Session )
	:return: Filtered Collections. ( List )
	"""

	return list(set(getCollectionsByType(type, session)).intersection(
	filterCollections("{0}".format(pattern), field, flags, getSession(session))))

def filterIblSetsCollections(pattern, field, flags=0, session=None):
	"""
	This definition filters the Ibl Sets Collections from the Database.

	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:param session: Database session. ( Session )
	:return: Filtered Collections. ( List )
	"""

	return filterCollectionsByType("IblSets", pattern, field, flags, getSession(session))

def filterTemplatesCollections(pattern, field, flags=0, session=None):
	"""
	This definition filters the Templates Collections from the Database.

	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:param session: Database session. ( Session )
	:return: Filtered Collections. ( List )
	"""

	return filterCollectionsByType("Templates", pattern, field, flags, getSession(session))

def collectionExists(name, session=None):
	"""
	This method returns if the Collection exists in the Database.

	:param name: Collection name. ( String )
	:param session: Database session. ( Session )
	:return: Collection exists. ( Boolean )
	"""

	return filterCollections("^{0}$".format(name), "name", session=getSession(session)) and True or False

def addCollection(collection, type, comment, session=None):
	"""
	This definition adds a Collection to the Database.

	:param collection: Collection name. ( String )
	:param type: Collection type. ( String )
	:param comment: Collection comment. ( String )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' Collection of type '{1}' to the Database.".format(collection, type))

	session = getSession(session)

	if not filterCollections("^{0}$".format(collection), "name", session=session):
		databaseItem = Collection(name=collection, type=type, comment=comment)
		return addItem(databaseItem, session)
	else:
		LOGGER.warning("!> {0} | '{1}' Collection already exists in Database!".format(__name__, collection))
		return False

def removeCollection(identity, session=None):
	"""
	This definition removes a Collection from the Database.

	:param identity: Collection id. ( String )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	return removeStandardItem(Collection, identity, getSession(session))

def getCollectionsIblSets(identities, session=None):
	"""
	This definition returns Ibl Sets from Collections ids

	:param identities: Collections ids. ( List )
	:param session: Database session. ( Session )
	:return: Ibl Sets list. ( List )
	"""

	iblSets = []
	for identity in identities:
		collectionSets = filterIblSets("^{0}$".format(identity), "collection", session=getSession(session))
		if collectionSets:
			for iblSet in collectionSets:
				iblSets.append(iblSet)
	return iblSets

def getCollectionIblSetsCount(collection, session=None):
	"""
	This method returns given Collection Ibl Sets count.

	:param collection: Collection. ( Collection )
	:param session: Database session. ( Session )
	:return: Collection Ibl Sets count. ( Integer )
	"""

	return getSession(session).query(IblSet).filter_by(collection=collection.id).count()

def getCollectionTemplatesCount(collection, session=None):
	"""
	This method returns given Collection Tempates count.

	:param collection: Collection. ( Collection )
	:param session: Database session. ( Session )
	:return: Collection Templates count. ( Integer )
	"""

	return getSession(session).query(Template).filter_by(collection=collection.id).count()

def getTemplates(session=None):
	"""
	This definition returns the Templates from the Database.

	:param session: Database session. ( Session )
	:return: Database Templates. ( List )
	"""

	return getSession(session).query(Template)

def filterTemplates(pattern, field, flags=0, session=None):
	"""
	This definition filters the Templates from the Database.

	:param pattern: Filtering pattern. ( String )
	:param field: Database field to search into. ( String )
	:param flags: Flags passed to the regex engine. ( Integer )
	:param session: Database session. ( Session )
	:return: Filtered Templates. ( List )
	"""

	return filterItems(getTemplates(getSession(session)), pattern, field, flags)

def templateExists(path, session=None):
	"""
	This method returns if given Template exists in the Database.

	:param name: Template path. ( String )
	:param session: Database session. ( Session )
	:return: Template exists. ( Boolean )
	"""

	return filterTemplates("^{0}$".format(re.escape(path)), "path", session=getSession(session)) and True or False

def addTemplate(name, path, collection, session=None):
	"""
	This definition adds a new Template to the Database.

	:param name: Template name. ( String )
	:param path: Template path. ( String )
	:param collection: Collection id. ( String )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	return addStandardItem(Template, name, path, collection, getSession(session))

def removeTemplate(identity, session=None):
	"""
	This definition removes a Template from the Database.

	:param identity: Template id. ( String )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	return removeStandardItem(Template, identity, getSession(session))

def updateTemplateContent(template, session=None):
	"""
	This definition update a Template content.

	:param template: Template to Template content. ( Template )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemContent(template, getSession(session))

def updateTemplateLocation(template, path, session=None):
	"""
	This definition updates a Template location.

	:param template: Template to update. ( Template )
	:param path: Template path. ( Path )
	:param session: Database session. ( Session )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemLocation(template, path, getSession(session))

def checkTemplatesTableIntegrity(session=None):
	"""
	This definition checks Templates table integrity.

	:param session: Database session. ( Session )
	:return: Templates table erroneous items. ( Dictionary )
	"""

	LOGGER.debug("> Checking 'Templates' Database table integrity.")

	session = getSession(session)

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
