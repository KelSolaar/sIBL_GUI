#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines Application Database manipulations objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import logging
import os
import re

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import sibl_gui.components.core.db.exceptions
import sibl_gui.components.core.db.utilities.types as dbTypes
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"DB_EXCEPTIONS"
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

LOGGER = logging.getLogger(Constants.logger)

DB_EXCEPTIONS = {"INEXISTING_IBL_SET_FILE_EXCEPTION" : "Ibl Set's file is missing!",
				"INEXISTING_IBL_SET_ICON_EXCEPTION" : "Ibl Set's icon is missing!",
				"INEXISTING_IBL_SET_PREVIEW_IMAGE_EXCEPTION" : "Ibl Set's preview image is missing!",
				"INEXISTING_IBL_SET_BACKGROUND_IMAGE_EXCEPTION" : "Ibl Set's background image is missing!",
				"INEXISTING_IBL_SET_LIGHTING_IMAGE_EXCEPTION" : "Ibl Set's lighting image is missing!",
				"INEXISTING_IBL_SET_REFLECTION_IMAGE_EXCEPTION" : "Ibl Set's reflection image is missing!",
				"INEXISTING_TEMPLATE_FILE_EXCEPTION" : "Template file is missing!",
				"INEXISTING_TEMPLATE_HELP_FILE_EXCEPTION" : "Template help file is missing!"}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, sibl_gui.components.core.db.exceptions.DatabaseOperationError)
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
		raise sibl_gui.components.core.db.exceptions.DatabaseOperationError(
		"{0} | Database commit error: '{1}'".format(inspect.getmodulename(__file__), error))

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def addItem(session, item):
	"""
	This definition adds an item to the Database.

	:param session: Database session. ( Session )
	:param item: Item to add. ( Db object )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' item to the Database.".format(item))

	session.add(item)

	return commit(session)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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
		osStats = ",".join((str(stat) for stat in os.stat(path)))
		dbItem = type(name=name, path=path, collection=collection, osStats=osStats)
		if dbItem.setContent():
			return addItem(session, dbItem)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' path already exists in Database!".format(
		core.getModule(addStandardItem).__name__, path, type.__name__))
		return False

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def removeItem(session, item):
	"""
	This definition removes an item from the Database.

	:param session: Database session. ( Session )
	:param item: Item to remove. ( Db object )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Removing: '{0}' item from the Database.".format(item))

	session.delete(item)

	return commit(session)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def removeStandardItem(session, type, id):
	"""
	This definition removes a standard item from the Database.

	:param session: Database session. ( Session )
	:param type: Item type. ( Object )
	:param id: Item id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Removing item type '{0}' with id '{1}' from the Database.".format(type.__name__, id))

	item = session.query(type).filter_by(id=id).one()
	return removeItem(session, item)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def updateItemContent(session, item):
	"""
	This definition update an item content.

	:param session: Database session. ( Session )
	:param item: Item to set content. ( DbIblSet )
	:return: Database commit success. ( Boolean )
	"""

	LOGGER.debug("> Updating '{0}' '{1}' content.".format(item.name, item.__class__.__name__))

	item.osStats = ",".join((str(stat) for stat in os.stat(item.path)))
	if item.setContent():
		return commit(session)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' content update failed!".format(core.getModule(updateItemContent).__name__,
		item.name, item.__class__.__name__))
		return False

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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
		core.getModule(updateItemLocation).__name__, path, item.__class__.__name__))
		return False

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

	return [item for item in items if re.search(pattern, str(item.__dict__[field]), flags)]

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

@core.executionTrace
def getIblSets(session):
	"""
	This definition gets the Ibl Sets from the Database.

	:param session: Database session. ( Session )
	:return: Database Ibl Sets. ( List )
	"""

	return session.query(dbTypes.DbIblSet)

@core.executionTrace
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

@core.executionTrace
def iblSetExists(session, path):
	"""
	This method returns if given Ibl Set exists in the Database.

	:param name: Ibl Set path. ( String )
	:return: Ibl Set exists. ( Boolean )
	"""

	return filterIblSets(session, "^{0}$".format(re.escape(path)), "path") and True or False

@core.executionTrace
def addIblSet(session, name, path, collection):
	"""
	This definition adds a new Ibl Set to the Database.

	:param session: Database session. ( Session )
	:param name: Ibl Set name. ( String )
	:param path: Ibl Set path. ( String )
	:param collection: Collection id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return addStandardItem(session, dbTypes.DbIblSet, name, path, collection)

@core.executionTrace
def removeIblSet(session, id):
	"""
	This definition removes an Ibl Set from the Database.

	:param session: Database session. ( Session )
	:param id: Ibl Set id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return removeStandardItem(session, dbTypes.DbIblSet, id)

@core.executionTrace
def updateIblSetContent(session, iblSet):
	"""
	This definition update an Ibl Set content.

	:param session: Database session. ( Session )
	:param iblSet: Ibl Set to set content. ( DbIblSet )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemContent(session, iblSet)

@core.executionTrace
def updateIblSetLocation(session, iblSet, path):
	"""
	This definition updates an Ibl Set location.

	:param session: Database session. ( Session )
	:param iblSet: Ibl Set to update. ( DbIblSet )
	:param path: Ibl Set path. ( Path )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemLocation(session, iblSet, path)

@core.executionTrace
def checkIblSetsTableIntegrity(session):
	"""
	This definition checks sets table integrity.

	:param session: Database session. ( Session )
	:return: Ibl Sets table erroneous items. ( Dictionary )
	"""

	LOGGER.debug("> Checking 'Sets' Database table integrity.")

	erroneousSets = {}
	if getIblSets(session):
		for iblSet in getIblSets(session):
			if not foundations.common.pathExists(iblSet.path):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_FILE_EXCEPTION"
				continue

			if not foundations.common.pathExists(iblSet.icon):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_ICON_EXCEPTION"
			if iblSet.previewImage and not foundations.common.pathExists(os.path.join(os.path.dirname(iblSet.path),
																	iblSet.previewImage)):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_PREVIEW_IMAGE_EXCEPTION"
			if iblSet.backgroundImage and not foundations.common.pathExists(os.path.join(os.path.dirname(iblSet.path),
																		iblSet.backgroundImage)):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_BACKGROUND_IMAGE_EXCEPTION"
			if iblSet.lightingImage and not foundations.common.pathExists(os.path.join(os.path.dirname(iblSet.path),
																		iblSet.lightingImage)):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_LIGHTING_IMAGE_EXCEPTION"
			if iblSet.reflectionImage and not foundations.common.pathExists(os.path.join(os.path.dirname(iblSet.path),
																		iblSet.reflectionImage)):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_REFLECTION_IMAGE_EXCEPTION"

	if erroneousSets:
		return erroneousSets

@core.executionTrace
def getCollections(session):
	"""
	This definition gets the Collections from the Database.

	:param session: Database session. ( Session )
	:return: Database Collections. ( List )
	"""

	return session.query(dbTypes.DbCollection)

@core.executionTrace
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

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getCollectionsByType(session, type):
	"""
	This method returns Collections of given type.

	:param session: Database session. ( Session )
	:param type: Type name. ( String )
	:return: Ibl Sets Collections. ( List )
	"""

	return [collection for collection in filterCollections(session, type, "type")]

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

@core.executionTrace
def collectionExists(session, name):
	"""
	This method returns if the Collection exists in the Database.

	:param name: Collection name. ( String )
	:return: Collection exists. ( Boolean )
	"""

	return filterCollections(session, "^{0}$".format(name), "name") and True or False

@core.executionTrace
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
		dbItem = dbTypes.DbCollection(name=collection, type=type, comment=comment)
		return addItem(session, dbItem)
	else:
		LOGGER.warning("!> {0} | '{1}' Collection already exists in Database!".format(
		core.getModule(addCollection).__name__, collection))
		return False

@core.executionTrace
def removeCollection(session, id):
	"""
	This definition removes a Collection from the Database.

	:param session: Database session. ( Session )
	:param id: Collection id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return removeStandardItem(session, dbTypes.DbCollection, id)

@core.executionTrace
def getCollectionsIblSets(session, ids):
	"""
	This definition gets Ibl Sets from Collections ids

	:param session: Database session. ( Session )
	:param ids: Collections ids. ( List )
	:return: Ibl Sets list. ( List )
	"""

	iblSets = []
	for id in ids:
		collectionSets = filterIblSets(session, "^{0}$".format(id), "collection")
		if collectionSets:
			for iblSet in collectionSets:
				iblSets.append(iblSet)
	return iblSets

@core.executionTrace
def getTemplates(session):
	"""
	This definition gets the Templates from the Database.

	:param session: Database session. ( Session )
	:return: Database Templates. ( List )
	"""

	return session.query(dbTypes.DbTemplate)

@core.executionTrace
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

@core.executionTrace
def templateExists(session, path):
	"""
	This method returns if given Template exists in the Database.

	:param name: Template path. ( String )
	:return: Template exists. ( Boolean )
	"""

	return filterTemplates(session, "^{0}$".format(re.escape(path)), "path") and True or False

@core.executionTrace
def addTemplate(session, name, path, collection):
	"""
	This definition adds a new Template to the Database.

	:param session: Database session. ( Session )
	:param name: Template name. ( String )
	:param path: Template path. ( String )
	:param collection: Collection id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return addStandardItem(session, dbTypes.DbTemplate, name, path, collection)

@core.executionTrace
def removeTemplate(session, id):
	"""
	This definition removes a Template from the Database.

	:param session: Database session. ( Session )
	:param id: Template id. ( String )
	:return: Database commit success. ( Boolean )
	"""

	return removeStandardItem(session, dbTypes.DbTemplate, id)

@core.executionTrace
def updateTemplateContent(session, template):
	"""
	This definition update a Template content.

	:param session: Database session. ( Session )
	:param template: Template to Template content. ( DbTemplate )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemContent(session, template)

@core.executionTrace
def updateTemplateLocation(session, template, path):
	"""
	This definition updates a Template location.

	:param session: Database session. ( Session )
	:param template: Template to update. ( DbTemplate )
	:param path: Template path. ( Path )
	:return: Database commit success. ( Boolean )
	"""

	return updateItemLocation(session, template, path)

@core.executionTrace
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
			if not foundations.common.pathExists(template.path):
				erroneousTemplates[template] = "INEXISTING_TEMPLATE_FILE_EXCEPTION"
				continue

			if not foundations.common.pathExists(template.helpFile):
				erroneousTemplates[template] = "INEXISTING_TEMPLATE_HELP_FILE_EXCEPTION"
	return erroneousTemplates
