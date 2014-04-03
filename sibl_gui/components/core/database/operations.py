#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**operations.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines Application Database operations objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Creates a default session.

	:return: Database session.
	:rtype: Session
	"""

	return DEFAULT_SESSION_MAKER()

def getSession(session=None):
	"""
	Returns either given session or the default one.

	:param session: Database session.
	:type session: Session
	:return: Database session.
	:rtype: Session
	"""

	if session is not None:
		return session

	if DEFAULT_SESSION is not None:
		return DEFAULT_SESSION
	else:
		LOGGER.warning("!> {0} | Default session is not set, creating one!".format(__name__))

def query(*args, **kwargs):
	"""
	Queries given session or the default one.

	:param \*args: Arguments.
	:type \*args: \*
	:param \*\*kwargs: Keywords arguments.
	:type \*\*kwargs: \*\*
	:return: Query result.
	:rtype: object
	"""

	return getSession(kwargs.get("session")).query(*args, **kwargs)

@foundations.exceptions.handleExceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
def commit(session=None):
	"""
	Commits changes to the Database.

	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
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
	Adds an item to the Database.

	:param item: Item to add.
	:type item: Object
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	LOGGER.debug("> Adding: '{0}' item to the Database.".format(item))

	session = getSession(session)
	session.add(item)
	return commit(session)

def addStandardItem(type, name, path, collection, session=None):
	"""
	Adds a new standard item to the Database.

	:param type: Item type.
	:type type: object
	:param name: Item name.
	:type name: unicode
	:param path: Item path.
	:type path: unicode
	:param collection: Collection id.
	:type collection: unicode
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	LOGGER.debug("> Adding: '{0}' '{1}' to the Database.".format(name, type.__name__))

	session = getSession(session)

	if not filterItems(query(type), "^{0}$".format(re.escape(path)), "path"):
		if not foundations.common.pathExists(path):
			LOGGER.warning("!> {0} | '{1}' file doesn't exists!".format(__name__, path))
			return False

		osStats = ",".join((foundations.strings.toString(stat) for stat in os.stat(path)))
		databaseItem = type(name=name, path=path, collection=collection, osStats=osStats)
		if databaseItem.setContent():
			return addItem(databaseItem, session)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' path already exists in Database!".format(__name__, path, type.__name__))
		return False

def removeItem(item, session=None):
	"""
	Removes an item from the Database.

	:param item: Item to remove.
	:type item: Object
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	LOGGER.debug("> Removing: '{0}' item from the Database.".format(item))

	session = getSession(session)
	session.delete(item)
	return commit(session)

def removeStandardItem(type, identity, session=None):
	"""
	Removes a standard item from the Database.

	:param type: Item type.
	:type type: object
	:param identity: Item id.
	:type identity: unicode
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	LOGGER.debug("> Removing item type '{0}' with id '{1}' from the Database.".format(type.__name__, identity))

	item = session.query(type).filter_by(id=identity).one()
	return removeItem(item, getSession(session))

def updateItemContent(item, session=None):
	"""
	Update an item content.

	:param item: Item to set content.
	:type item: IblSet
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	LOGGER.debug("> Updating '{0}' '{1}' content.".format(item.name, item.__class__.__name__))

	if not foundations.common.pathExists(item.path):
		LOGGER.warning("!> {0} | '{1}' file doesn't exists!".format(__name__, item.path))
		return False

	item.osStats = ",".join(map(foundations.strings.toString, os.stat(item.path)))
	if item.setContent():
		return commit(getSession(session))
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' content update failed!".format(__name__,
																		item.name,
																		item.__class__.__name__))
		return False

def updateItemLocation(item, path, session=None):
	"""
	Updates an item location.

	:param item: Item to update.
	:type item: object
	:param path: Item path.
	:type path: Path
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
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
	Filters items from the Database.

	:param items: Database items.
	:type items: list
	:param pattern: Filtering pattern.
	:type pattern: unicode
	:param field: Database field to search into.
	:type field: unicode
	:param flags: Flags passed to the regex engine.
	:type flags: int
	:return: Filtered items.
	:rtype: list
	"""

	return [item for item in items if re.search(pattern, foundations.strings.toString(item.__dict__[field]), flags)]

def itemExists(items, pattern, field, flags=0):
	"""
	Returns if given item exists in the Database.

	:param items: Database items.
	:type items: list
	:param pattern: Filtering pattern.
	:type pattern: unicode
	:param field: Database field to search into.
	:type field: unicode
	:param flags: Flags passed to the regex engine.
	:type flags: int
	:return: Filtered items.
	:rtype: list
	"""

	return filterItems(items, pattern, field, flags) and True or False

def getIblSets(session=None):
	"""
	Returns the Ibl Sets from the Database.

	:param session: Database session.
	:type session: Session
	:return: Database Ibl Sets.
	:rtype: list
	"""

	return getSession(session).query(IblSet)

def filterIblSets(pattern, field, flags=0, session=None):
	"""
	Filters the sets from the Database.

	:param pattern: Filtering pattern.
	:type pattern: unicode
	:param field: Database field to search into.
	:type field: unicode
	:param flags: Flags passed to the regex engine.
	:type flags: int
	:param session: Database session.
	:type session: Session
	:return: Filtered Ibl Sets.
	:rtype: list
	"""

	return filterItems(getIblSets(getSession(session)), pattern, field, flags)

def iblSetExists(path, session=None):
	"""
	Returns if given Ibl Set exists in the Database.

	:param name: Ibl Set path.
	:type name: unicode
	:param session: Database session.
	:type session: Session
	:return: Ibl Set exists.
	:rtype: bool
	"""

	return filterIblSets("^{0}$".format(re.escape(path)), "path", session=getSession(session)) and True or False

def addIblSet(name, path, collection, session=None):
	"""
	Adds a new Ibl Set to the Database.

	:param name: Ibl Set name.
	:type name: unicode
	:param path: Ibl Set path.
	:type path: unicode
	:param collection: Collection id.
	:type collection: unicode
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	return addStandardItem(IblSet, name, path, collection, getSession(session))

def removeIblSet(identity, session=None):
	"""
	Removes an Ibl Set from the Database.

	:param identity: Ibl Set id.
	:type identity: unicode
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	return removeStandardItem(IblSet, identity, getSession(session))

def updateIblSetContent(iblSet, session=None):
	"""
	Update an Ibl Set content.

	:param iblSet: Ibl Set to set content.
	:type iblSet: IblSet
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	return updateItemContent(iblSet, getSession(session))

def updateIblSetLocation(iblSet, path, session=None):
	"""
	Updates an Ibl Set location.

	:param iblSet: Ibl Set to update.
	:type iblSet: IblSet
	:param path: Ibl Set path.
	:type path: Path
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	return updateItemLocation(iblSet, path, getSession(session))

def checkIblSetsTableIntegrity(session=None):
	"""
	Checks sets table integrity.

	:param session: Database session.
	:type session: Session
	:return: Ibl Sets table erroneous items.
	:rtype: dict
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
	Returns the Collections from the Database.

	:param session: Database session.
	:type session: Session
	:return: Database Collections.
	:rtype: list
	"""

	return getSession(session).query(Collection)

def filterCollections(pattern, field, flags=0, session=None):
	"""
	Filters the Collections from the Database.

	:param pattern: Filtering pattern.
	:type pattern: unicode
	:param field: Database field to search into.
	:type field: unicode
	:param flags: Flags passed to the regex engine.
	:type flags: int
	:param session: Database session.
	:type session: Session
	:return: Filtered Collections.
	:rtype: list
	"""

	return filterItems(getCollections(getSession(session)), pattern, field, flags)

def getCollectionsByType(type, session=None):
	"""
	Returns Collections of given type.

	:param type: Type name.
	:type type: unicode
	:param session: Database session.
	:type session: Session
	:return: Ibl Sets Collections.
	:rtype: list
	"""

	return [collection for collection in filterCollections(type, "type", session=getSession(session))]

def filterCollectionsByType(type, pattern, field, flags=0, session=None):
	"""
	Filters the Ibl Sets Collections from the Database.

	:param type: Type name.
	:type type: unicode
	:param pattern: Filtering pattern.
	:type pattern: unicode
	:param field: Database field to search into.
	:type field: unicode
	:param flags: Flags passed to the regex engine.
	:type flags: int
	:param session: Database session.
	:type session: Session
	:return: Filtered Collections.
	:rtype: list
	"""

	return list(set(getCollectionsByType(type, session)).intersection(
	filterCollections("{0}".format(pattern), field, flags, getSession(session))))

def filterIblSetsCollections(pattern, field, flags=0, session=None):
	"""
	Filters the Ibl Sets Collections from the Database.

	:param pattern: Filtering pattern.
	:type pattern: unicode
	:param field: Database field to search into.
	:type field: unicode
	:param flags: Flags passed to the regex engine.
	:type flags: int
	:param session: Database session.
	:type session: Session
	:return: Filtered Collections.
	:rtype: list
	"""

	return filterCollectionsByType("IblSets", pattern, field, flags, getSession(session))

def filterTemplatesCollections(pattern, field, flags=0, session=None):
	"""
	Filters the Templates Collections from the Database.

	:param pattern: Filtering pattern.
	:type pattern: unicode
	:param field: Database field to search into.
	:type field: unicode
	:param flags: Flags passed to the regex engine.
	:type flags: int
	:param session: Database session.
	:type session: Session
	:return: Filtered Collections.
	:rtype: list
	"""

	return filterCollectionsByType("Templates", pattern, field, flags, getSession(session))

def collectionExists(name, session=None):
	"""
	Returns if the Collection exists in the Database.

	:param name: Collection name.
	:type name: unicode
	:param session: Database session.
	:type session: Session
	:return: Collection exists.
	:rtype: bool
	"""

	return filterCollections("^{0}$".format(name), "name", session=getSession(session)) and True or False

def addCollection(collection, type, comment, session=None):
	"""
	Adds a Collection to the Database.

	:param collection: Collection name.
	:type collection: unicode
	:param type: Collection type.
	:type type: unicode
	:param comment: Collection comment.
	:type comment: unicode
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
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
	Removes a Collection from the Database.

	:param identity: Collection id.
	:type identity: unicode
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	return removeStandardItem(Collection, identity, getSession(session))

def getCollectionsIblSets(identities, session=None):
	"""
	Returns Ibl Sets from Collections ids

	:param identities: Collections ids.
	:type identities: list
	:param session: Database session.
	:type session: Session
	:return: Ibl Sets list.
	:rtype: list
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
	Returns given Collection Ibl Sets count.

	:param collection: Collection.
	:type collection: Collection
	:param session: Database session.
	:type session: Session
	:return: Collection Ibl Sets count.
	:rtype: int
	"""

	return getSession(session).query(IblSet).filter_by(collection=collection.id).count()

def getCollectionTemplatesCount(collection, session=None):
	"""
	Returns given Collection Tempates count.

	:param collection: Collection.
	:type collection: Collection
	:param session: Database session.
	:type session: Session
	:return: Collection Templates count.
	:rtype: int
	"""

	return getSession(session).query(Template).filter_by(collection=collection.id).count()

def getTemplates(session=None):
	"""
	Returns the Templates from the Database.

	:param session: Database session.
	:type session: Session
	:return: Database Templates.
	:rtype: list
	"""

	return getSession(session).query(Template)

def filterTemplates(pattern, field, flags=0, session=None):
	"""
	Filters the Templates from the Database.

	:param pattern: Filtering pattern.
	:type pattern: unicode
	:param field: Database field to search into.
	:type field: unicode
	:param flags: Flags passed to the regex engine.
	:type flags: int
	:param session: Database session.
	:type session: Session
	:return: Filtered Templates.
	:rtype: list
	"""

	return filterItems(getTemplates(getSession(session)), pattern, field, flags)

def templateExists(path, session=None):
	"""
	Returns if given Template exists in the Database.

	:param name: Template path.
	:type name: unicode
	:param session: Database session.
	:type session: Session
	:return: Template exists.
	:rtype: bool
	"""

	return filterTemplates("^{0}$".format(re.escape(path)), "path", session=getSession(session)) and True or False

def addTemplate(name, path, collection, session=None):
	"""
	Adds a new Template to the Database.

	:param name: Template name.
	:type name: unicode
	:param path: Template path.
	:type path: unicode
	:param collection: Collection id.
	:type collection: unicode
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	return addStandardItem(Template, name, path, collection, getSession(session))

def removeTemplate(identity, session=None):
	"""
	Removes a Template from the Database.

	:param identity: Template id.
	:type identity: unicode
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	return removeStandardItem(Template, identity, getSession(session))

def updateTemplateContent(template, session=None):
	"""
	Update a Template content.

	:param template: Template to Template content.
	:type template: Template
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	return updateItemContent(template, getSession(session))

def updateTemplateLocation(template, path, session=None):
	"""
	Updates a Template location.

	:param template: Template to update.
	:type template: Template
	:param path: Template path.
	:type path: Path
	:param session: Database session.
	:type session: Session
	:return: Database commit success.
	:rtype: bool
	"""

	return updateItemLocation(template, path, getSession(session))

def checkTemplatesTableIntegrity(session=None):
	"""
	Checks Templates table integrity.

	:param session: Database session.
	:type session: Session
	:return: Templates table erroneous items.
	:rtype: dict
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
