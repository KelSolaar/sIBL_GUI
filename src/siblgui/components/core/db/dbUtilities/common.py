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

"""
************************************************************************************************
***	common.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Common Database Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
import re
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
from siblgui.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

DB_EXCEPTIONS = {
			"INEXISTING_IBL_SET_FILE_EXCEPTION" : "Ibl Set's Ibl File Is Missing!",
			"INEXISTING_IBL_SET_ICON_EXCEPTION" : "Ibl Set's Icon Is Missing!",
			"INEXISTING_IBL_SET_PREVIEW_IMAGE_EXCEPTION" : "Ibl Set's Preview Image Is Missing!",
			"INEXISTING_IBL_SET_BACKGROUND_IMAGE_EXCEPTION" : "Ibl Set's Background Image Is Missing!",
			"INEXISTING_IBL_SET_LIGHTING_IMAGE_EXCEPTION" : "Ibl Set's Lighting Image Is Missing!",
			"INEXISTING_IBL_SET_REFLECTION_IMAGE_EXCEPTION" : "Ibl Set's Reflection Image Is Missing!",
			"INEXISTING_TEMPLATE_FILE_EXCEPTION" : "Template File Is Missing!",
			"INEXISTING_TEMPLATE_HELP_FILE_EXCEPTION" : "Template Help File Is Missing!"
		}

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def commit(session):
	"""
	This Definition Commits Changes To The Database.
	
	@param session: Database Session. ( Session )
	@return: Database Commit Success. ( Boolean )
	"""

	try:
		session.commit()
		return True
	except Exception as error:
		session.rollback()
		raise Exception("Database Commit Error: '{0}'".format(error))

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def addItem(session, item):
	"""
	This Definition Adds An Item To The Database.
	
	@param session: Database Session. ( Session )
	@param item: Item To Add. ( Db Object )
	@return: Database Commit Success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' Item To The Database.".format(item))

	session.add(item)

	return commit(session)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def addStandardItem(session, type, name, path, collection):
	"""
	This Definition Adds A New Standard Item To The Database.

	@param type: Item Type. ( Object )
	@param session: Database Session. ( Session )
	@param name: Item Name. ( String )
	@param path: Item Path. ( String )
	@param collection: Collection Id. ( String )
	@return: Database Commit Success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' '{1}' To The Database.".format(name, type.__name__))

	if not filterItems(session, session.query(type), "^{0}$".format(re.escape(path)), "path"):
		osStats = ",".join((str(stat) for stat in os.stat(path)))
		dbItem = type(name=name, path=path, collection=collection, osStats=osStats)
		if dbItem.setContent():
			return addItem(session, dbItem)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' Path Already Exists In Database!".format(core.getModule(addStandardItem).__name__, path, type.__name__))
		return False

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def removeItem(session, item):
	"""
	This Definition Removes An Item From The Database.
	
	@param session: Database Session. ( Session )
	@param item: Item To Remove. ( Db Object )
	@return: Database Commit Success. ( Boolean )
	"""

	LOGGER.debug("> Removing: '{0}' Item From The Database.".format(item))

	session.delete(item)

	return commit(session)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def removeStandardItem(session, type, id):
	"""
	This Definition Removes A Standard Item From The Database.

	@param session: Database Session. ( Session )
	@param type: Item Type. ( Object )
	@param id: Item Id. ( String )
	@return: Database Commit Success. ( Boolean )
	"""

	LOGGER.debug("> Removing Item Type '{0}' With Id '{1}' From The Database.".format(type.__name__, id))

	item = session.query(type).filter_by(id=id).one()
	return removeItem(session, item)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def updateItemContent(session, item):
	"""
	This Definition Update An Item Content.

	@param session: Database Session. ( Session )
	@param item: Item To Set Content. ( DbIblSet )
	@return: Database Commit Success. ( Boolean )
	"""

	LOGGER.debug("> Updating '{0}' '{1}' Content.".format(item.name, item.__class__.__name__))

	item.osStats = ",".join((str(stat) for stat in os.stat(item.path)))
	if item.setContent():
		return commit(session)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' Content Update Failed!".format(core.getModule(updateItemContent).__name__, item.name, item.__class__.__name__))
		return False

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def updateItemLocation(session, item, path):
	"""
	This Definition Updates An Item Location.

	@param session: Database Session. ( Session )
	@param item: Item To Update. ( Object )
	@param path: Item Path. ( Path )
	@return: Database Commit Success. ( Boolean )
	"""

	LOGGER.debug("> Updating '{0}' '{1}' Location.".format(item, item.__class__.__name__))

	if not filterItems(session, session.query(item.__class__), "^{0}$".format(re.escape(path)), "path"):
		item.path = path
		return updateItemContent(session, item)
	else:
		LOGGER.warning("!> {0} | '{1}' '{2}' Path Already Exists In Database!".format(core.getModule(updateItemLocation).__name__, path, item.__class__.__name__))
		return False

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def filterItems(session, items, pattern, field, flags=0):
	"""
	This Definition Filters Items From The Database.

	@param session: Database Session. ( Session )
	@param items: Database Items. ( List )
	@param pattern: Filtering Pattern. ( String )
	@param field: Database Field To Search Into. ( String )
	@param flags: Flags Passed To The Regex Engine. ( Integer )
	@return: Filtered Items. ( List )
	"""

	return [item for item in items if re.search(pattern, str(item.__dict__[field]), flags)]

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def itemExists(session, items, pattern, field, flags=0):
	"""
	This Definition Returns If Item Exists In The Database.

	@param session: Database Session. ( Session )
	@param items: Database Items. ( List )
	@param pattern: Filtering Pattern. ( String )
	@param field: Database Field To Search Into. ( String )
	@param flags: Flags Passed To The Regex Engine. ( Integer )
	@return: Filtered Items. ( List )
	"""

	return filterItems(session, items, pattern, field, flags) and True or False

@core.executionTrace
def getIblSets(session):
	"""
	This Definition Gets The Ibl Sets From The Database.

	@param session: Database Session. ( Session )
	@return: Database Ibl Sets. ( List )
	"""

	return session.query(dbUtilities.types.DbIblSet)

@core.executionTrace
def filterIblSets(session, pattern, field, flags=0):
	"""
	This Definition Filters The Sets From The Database.

	@param session: Database Session. ( Session )
	@param pattern: Filtering Pattern. ( String )
	@param field: Database Field To Search Into. ( String )
	@param flags: Flags Passed To The Regex Engine. ( Integer )
	@return: Filtered Ibl Sets. ( List )
	"""

	return filterItems(session, getIblSets(session), pattern, field, flags)

@core.executionTrace
def iblSetExists(session, path):
	"""
	This Method Returns If Ibl Set Exists In The Database.
	
	@param name: Ibl Set path. ( String )
	@return: Ibl Set Exists. ( Boolean )
	"""

	return filterIblSets(session, "^{0}$".format(re.escape(path)), "path") and True or False

@core.executionTrace
def addIblSet(session, name, path, collection):
	"""
	This Definition Adds A New Ibl Set To The Database.

	@param session: Database Session. ( Session )
	@param name: Ibl Set Name. ( String )
	@param path: Ibl Set Path. ( String )
	@param collection: Collection Id. ( String )
	@return: Database Commit Success. ( Boolean )
	"""

	return addStandardItem(session, dbUtilities.types.DbIblSet, name, path, collection)

@core.executionTrace
def removeIblSet(session, id):
	"""
	This Definition Removes An Ibl Set From The Database.

	@param session: Database Session. ( Session )
	@param id: Ibl Set Id. ( String )
	@return: Database Commit Success. ( Boolean )
	"""

	return removeStandardItem(session, dbUtilities.types.DbIblSet, id)

@core.executionTrace
def updateIblSetContent(session, iblSet):
	"""
	This Definition Update An Ibl Set Content.

	@param session: Database Session. ( Session )
	@param iblSet: Ibl Set To Set Content. ( DbIblSet )
	@return: Database Commit Success. ( Boolean )
	"""

	return updateItemContent(session, iblSet)

@core.executionTrace
def updateIblSetLocation(session, iblSet, path):
	"""
	This Definition Updates An Ibl Set Location.

	@param session: Database Session. ( Session )
	@param iblSet: Ibl Set To Update. ( DbIblSet )
	@param path: Ibl Set Path. ( Path )
	@return: Database Commit Success. ( Boolean )
	"""

	return updateItemLocation(session, iblSet, path)

@core.executionTrace
def checkIblSetsTableIntegrity(session):
	"""
	This Definition Checks Sets Table Integrity.

	@param session: Database Session. ( Session )
	@return: Ibl Sets Table Erroneous Items. ( Dictionary )
	"""

	LOGGER.debug("> Checking 'Sets' Database Table Integrity.")

	erroneousSets = {}
	if getIblSets(session):
		for iblSet in getIblSets(session):
			if not os.path.exists(iblSet.path):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_FILE_EXCEPTION"
				continue
			if not os.path.exists(iblSet.icon):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_ICON_EXCEPTION"
			if iblSet.previewImage and not os.path.exists(os.path.join(os.path.dirname(iblSet.path), iblSet.previewImage)):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_PREVIEW_IMAGE_EXCEPTION"
			if iblSet.backgroundImage and not os.path.exists(os.path.join(os.path.dirname(iblSet.path), iblSet.backgroundImage)):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_BACKGROUND_IMAGE_EXCEPTION"
			if iblSet.lightingImage and not os.path.exists(os.path.join(os.path.dirname(iblSet.path), iblSet.lightingImage)):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_LIGHTING_IMAGE_EXCEPTION"
			if  iblSet.reflectionImage and not os.path.exists(os.path.join(os.path.dirname(iblSet.path), iblSet.reflectionImage)):
				erroneousSets[iblSet] = "INEXISTING_IBL_SET_REFLECTION_IMAGE_EXCEPTION"

	if erroneousSets:
		return erroneousSets

@core.executionTrace
def getCollections(session):
	"""
	This Definition Gets The Collections From The Database.

	@param session: Database Session. ( Session )
	@return: Database Collections. ( List )
	"""

	return session.query(dbUtilities.types.DbCollection)

@core.executionTrace
def filterCollections(session, pattern, field, flags=0):
	"""
	This Definition Filters The Collections From The Database.

	@param session: Database Session. ( Session )
	@param pattern: Filtering Pattern. ( String )
	@param field: Database Field To Search Into. ( String )
	@param flags: Flags Passed To The Regex Engine. ( Integer )
	@return: Filtered Collections. ( List )
	"""

	return filterItems(session, getCollections(session), pattern, field, flags)

@core.executionTrace
def collectionExists(session, name):
	"""
	This Method Returns If The Collection Exists In The Database.
	
	@param name: Collection Name. ( String )
	@return: Collection Exists. ( Boolean )
	"""

	return filterCollections(session, "^{0}$".format(name), "name") and True or False

@core.executionTrace
def addCollection(session, collection, type, comment):
	"""
	This Definition Adds A Collection To The Database.

	@param session: Database Session. ( Session )
	@param collection: Collection Name. ( String )
	@param type: Collection Type. ( String )
	@param comment: Collection Comment. ( String )
	@return: Database Commit Success. ( Boolean )
	"""

	LOGGER.debug("> Adding: '{0}' Collection Of Type '{1}' To The Database.".format(collection, type))

	if not filterCollections(session, "^{0}$".format(collection), "name"):
		dbItem = dbUtilities.types.DbCollection(name=collection, type=type, comment=comment)
		return addItem(session, dbItem)
	else:
		LOGGER.warning("!> {0} | '{1}' Collection Already Exists In Database!".format(core.getModule(addCollection).__name__, collection))
		return False

@core.executionTrace
def removeCollection(session, id):
	"""
	This Definition Removes A Collection From The Database.

	@param session: Database Session. ( Session )
	@param id: Collection Id. ( String )
	@return: Database Commit Success. ( Boolean )
	"""

	return removeStandardItem(session, dbUtilities.types.DbCollection, id)

@core.executionTrace
def getCollectionsIblSets(session, ids):
	"""
	This Definition Gets Ibl Sets From Collections Ids

	@param session: Database Session. ( Session )
	@param ids: Collections Ids. ( List )
	@return: Ibl Sets List. ( List )
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
	This Definition Gets The Templates From The Database.

	@param session: Database Session. ( Session )
	@return: Database Templates. ( List )
	"""

	return session.query(dbUtilities.types.DbTemplate)

@core.executionTrace
def filterTemplates(session, pattern, field, flags=0):
	"""
	This Definition Filters The Templates From The Database.

	@param session: Database Session. ( Session )
	@param pattern: Filtering Pattern. ( String )
	@param field: Database Field To Search Into. ( String )
	@param flags: Flags Passed To The Regex Engine. ( Integer )
	@return: Filtered Templates. ( List )
	"""

	return filterItems(session, getTemplates(session), pattern, field, flags)

@core.executionTrace
def templateExists(session, path):
	"""
	This Method Returns If Template Exists In The Database.
	
	@param name: Template path. ( String )
	@return: Template Exists. ( Boolean )
	"""

	return filterTemplates(session, "^{0}$".format(re.escape(path)), "path") and True or False

@core.executionTrace
def addTemplate(session, name, path, collection):
	"""
	This Definition Adds A New Template To The Database.

	@param session: Database Session. ( Session )
	@param name: Template Name. ( String )
	@param path: Template Path. ( String )
	@param collection: Collection Id. ( String )
	@return: Database Commit Success. ( Boolean )
	"""

	return addStandardItem(session, dbUtilities.types.DbTemplate, name, path, collection)

@core.executionTrace
def removeTemplate(session, id):
	"""
	This Definition Removes A Template From The Database.

	@param session: Database Session. ( Session )
	@param id: Template Id. ( String )
	@return: Database Commit Success. ( Boolean )
	"""

	return removeStandardItem(session, dbUtilities.types.DbTemplate, id)

@core.executionTrace
def updateTemplateContent(session, template):
	"""
	This Definition Update A Template Content.

	@param session: Database Session. ( Session )
	@param template: Template To Template Content. ( DbTemplate )
	@return: Database Commit Success. ( Boolean )
	"""

	return updateItemContent(session, template)

@core.executionTrace
def updateTemplateLocation(session, template, path):
	"""
	This Definition Updates A Template Location.

	@param session: Database Session. ( Session )
	@param template: Template To Update. ( DbTemplate )
	@param path: Template Path. ( Path )
	@return: Database Commit Success. ( Boolean )
	"""

	return updateItemLocation(session, template, path)

@core.executionTrace
def checkTemplatesTableIntegrity(session):
	"""
	This Definition Checks Templates Table Integrity.

	@param session: Database Session. ( Session )
	@return: Templates Table Erroneous Items. ( Dictionary )
	"""

	LOGGER.debug("> Checking 'Templates' Database Table Integrity.")

	erroneousTemplates = {}
	if getTemplates(session):
		for template in getTemplates(session):
			if not os.path.exists(template.path):
				erroneousTemplates[template] = "INEXISTING_TEMPLATE_FILE_EXCEPTION"
				continue
			if not os.path.exists(template.helpFile):
				erroneousTemplates[template] = "INEXISTING_TEMPLATE_HELP_FILE_EXCEPTION"
	return erroneousTemplates

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
