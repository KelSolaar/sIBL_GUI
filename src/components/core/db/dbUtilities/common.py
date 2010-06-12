#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2010 - Thomas Mansencal - kelsolaar_fool@hotmail.com
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
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	common.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Common Database Module.
***
***	Others :
***
************************************************************************************************
'''

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
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

DB_EXCEPTIONS = {
			"INEXISTING_IBL_SET_FILE_EXCEPTION" : "Set's Ibl File Is Missing !",
			"INEXISTING_IBL_SET_ICON_EXCEPTION" : "Set's Icon Is Missing !",
			"INEXISTING_IBL_SET_BACKGROUND_IMAGE_EXCEPTION" : "Set's Background Image Is Missing !",
			"INEXISTING_IBL_SET_LIGHTING_IMAGE_EXCEPTION" : "Set's Lighting Image Is Missing !",
			"INEXISTING_IBL_SET_REFLECTION_IMAGE_EXCEPTION" : "Set's Reflection Image Is Missing !",
			"INEXISTING_TEMPLATE_FILE_EXCEPTION" : "Template File Is Missing !",
			"INEXISTING_TEMPLATE_HELP_FILE_EXCEPTION" : "Template Help File Is Missing !"
		}

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@foundations.exceptions.exceptionsHandler( None, False, Exception )
@core.executionTrace
def commit( session ):
	'''
	This Definition Commits Changes To The Database.
	
	@param session: Database Session. ( Session )
	@return: Database Commit Success. ( Boolean )
	'''

	try :
		session.commit()
		return True
	except Exception as error:
		session.rollback()
		raise Exception( "Database Commit Error : '{0}'".format( error ) )

@core.executionTrace
@foundations.exceptions.exceptionsHandler( None, False, Exception )
def addItem( session, item ):
	'''
	This Definition Adds An Item To The Database.
	
	@param session: Database Session. ( Session )
	@param item: Item To Add. ( sIBL_DB Object )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Adding : '{0}' Item To Database.".format( item ) )

	session.add( item )

	return commit( session )

@core.executionTrace
@foundations.exceptions.exceptionsHandler( None, False, Exception )
def removeItem( session, item ):
	'''
	This Definition Removes An Item From The Database.
	
	@param session: Database Session. ( Session )
	@param item: Item To Remove. ( sIBL_DB Object )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Removing : '{0}' Item From Database.".format( item ) )

	session.delete( item )

	return commit( session )

@core.executionTrace
def getSets( session ):
	'''
	This Definition Gets The Sets From The Database.

	@param session: Database Session. ( Session )
	@return: Database Sets. ( List )
	'''

	return session.query( dbUtilities.types.DbSet )

@core.executionTrace
def filterSets( session, pattern, field, flags = 0 ):
	'''
	This Definition Filters The Sets From The Database.

	@param session: Database Session. ( Session )
	@param pattern: Filtering Pattern. ( String )
	@param field: Database Field To Search Into. ( String )
	@param flags: Flags Passed To The Regex Engine. ( Integer )
	@return: Filtered Sets. ( List )
	'''

	sets = getSets( session )
	if sets :
		filteredSets = [set for set in sets if re.search( pattern, str( set.__dict__[field] ), flags ) ]
		return filteredSets

@core.executionTrace
def addSet( session, name, path, collection ):
	'''
	This Definition Adds A New Set To The Database.

	@param session: Database Session. ( Session )
	@param name: Set Name. ( String )
	@param path: Set Path. ( String )
	@param collection: Collection Id. ( String )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Adding : '{0}' Set To Database.".format( name ) )

	if not filterSets( session, "^{0}$".format( re.escape( path ) ), "path" ) :
		osStats = ",".join( [str( stat ) for stat in os.stat( path )] )
		dbItem = dbUtilities.types.DbSet( name = name, path = path, collection = collection, osStats = osStats )
		if dbItem.setContent() :
			return addItem( session, dbItem )
	else:
		LOGGER.warning( "!> {0} | '{1}' Set Path Already Exists In Database !".format( core.getModule( addSet ).__name__, path ) )
		return False

@core.executionTrace
def removeSet( session, id ):
	'''
	This Definition Remove A Set From The Database.

	@param session: Database Session. ( Session )
	@param id: Set Id. ( String )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Removing Set With Id '{0}' From Database.".format( id ) )

	dbSet = session.query( dbUtilities.types.DbSet ).filter_by( id = id ).one()
	return removeItem( session, dbSet )

@core.executionTrace
def updateSetContent( session, set ):
	'''
	This Definition Update A Set Content.

	@param session: Database Session. ( Session )
	@param set: Set To Set Content. ( DbSet )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Updating '{0}' Set Content.".format( set ) )

	set.osStats = ",".join( [str( stat ) for stat in os.stat( set.path )] )
	if set.setContent() :
		return commit( session )
	else :
		LOGGER.warning( "!> {0} | '{1}' Set Content Update Failed !".format( core.getModule( updateSetContent ).__name__, set.name ) )
		return False

@core.executionTrace
def updateSetLocation( session, set, path ):
	'''
	This Definition Updates A Set Location.

	@param session: Database Session. ( Session )
	@param set: Set To Update. ( DbSet )
	@param path: Set Path. ( Path )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Updating '{0}' Set Location.".format( set ) )

	if not filterSets( session, "^{0}$".format( re.escape( path ) ), "path" ) :
		set.path = path
		return updateSetContent( session, set )
	else:
		LOGGER.warning( "!> {0} | '{1}' Set Path Already Exists In Database !".format( core.getModule( updateSetLocation ).__name__, path ) )
		return False

@core.executionTrace
def getCollections( session ):
	'''
	This Definition Gets The Collections From The Database.

	@param session: Database Session. ( Session )
	@return: Database Collections. ( List )
	'''

	return session.query( dbUtilities.types.DbCollection )

@core.executionTrace
def filterCollections( session, pattern, field, flags = 0 ):
	'''
	This Definition Filters The Collections From The Database.

	@param session: Database Session. ( Session )
	@param pattern: Filtering Pattern. ( String )
	@param field: Database Field To Search Into. ( String )
	@param flags: Flags Passed To The Regex Engine. ( Integer )
	@return: Filtered Collections. ( List )
	'''

	collections = getCollections( session )
	if collections :
		filteredCollections = [collection for collection in collections if re.search( pattern, str( collection.__dict__[field] ), flags ) ]
		return filteredCollections

@core.executionTrace
def addCollection( session, collection, type, comment ):
	'''
	This Definition Adds A Collection To The Database.

	@param session: Database Session. ( Session )
	@param collection: Collection Name. ( String )
	@param type: Collection Type. ( String )
	@param comment: Collection Comment. ( String )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Adding : '{0}' Collection Of Type '{1}' To Database.".format( collection, type ) )

	if not filterCollections( session, "^{0}$".format( collection ), "name" ) :
		dbItem = dbUtilities.types.DbCollection( name = collection, type = type, comment = comment )
		return addItem( session, dbItem )
	else:
		LOGGER.warning( "!> {0} | '{1}' Collection Already Exists In Database !".format( core.getModule( addCollection ).__name__, collection ) )
		return False

@core.executionTrace
def removeCollection( session, id ):
	'''
	This Definition Remove A Collection From The Database.

	@param session: Database Session. ( Session )
	@param id: Collection Id. ( String )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Removing Collection With Id '{0}' From Database.".format( id ) )

	dbCollection = session.query( dbUtilities.types.DbCollection ).filter_by( id = id ).one()
	return removeItem( session, dbCollection )

@core.executionTrace
def getCollectionsSets( session, ids ):
	'''
	This Definition Gets Sets From Collections Ids

	@param session: Database Session. ( Session )
	@param ids: Collections Ids. ( List )
	@return: Sets List. ( List )
	'''

	sets = []
	for id in ids :
		collectionSets = filterSets( session, str( id ), "collection" )
		if collectionSets :
			for set in filterSets( session, str( id ), "collection" ) :
				sets.append( set )
	return sets

@core.executionTrace
def checkSetsTableIntegrity( session ):
	'''
	This Definition Checks Sets Table Integrity.

	@param session: Database Session. ( Session )
	@return: Sets Table Erroneous Items. ( Dictionary )
	'''

	LOGGER.debug( "> Checking 'Sets' Database Table Integrity." )

	erroneousSets = {}
	if getSets( session ) :
		for set in getSets( session ) :
			if not os.path.exists( set.path ) :
				erroneousSets[set] = "INEXISTING_IBL_SET_FILE_EXCEPTION"
				continue
			if not os.path.exists( set.icon ) :
				erroneousSets[set] = "INEXISTING_IBL_SET_ICON_EXCEPTION"
			if set.backgroundImage and not os.path.exists( os.path.join( os.path.dirname( set.path ), set.backgroundImage ) ) :
				erroneousSets[set] = "INEXISTING_IBL_SET_BACKGROUND_IMAGE_EXCEPTION"
			if set.lightingImage and not os.path.exists( os.path.join( os.path.dirname( set.path ), set.lightingImage ) ) :
				erroneousSets[set] = "INEXISTING_IBL_SET_LIGHTING_IMAGE_EXCEPTION"
			if  set.reflectionImage and not os.path.exists( os.path.join( os.path.dirname( set.path ), set.reflectionImage ) ) :
				erroneousSets[set] = "INEXISTING_IBL_SET_REFLECTION_IMAGE_EXCEPTION"

	if erroneousSets : return erroneousSets

@core.executionTrace
def getTemplates( session ):
	'''
	This Definition Gets The Templates From The Database.

	@param session: Database Session. ( Session )
	@return: Database Templates. ( List )
	'''

	return session.query( dbUtilities.types.DbTemplate )

@core.executionTrace
def filterTemplates( session, pattern, field, flags = 0 ):
	'''
	This Definition Filters The Templates From The Database.

	@param session: Database Session. ( Session )
	@param pattern: Filtering Pattern. ( String )
	@param field: Database Field To Search Into. ( String )
	@param flags: Flags Passed To The Regex Engine. ( Integer )
	@return: Filtered Templates. ( List )
	'''

	templates = getTemplates( session )
	if templates :
		filteredTemplates = [template for template in templates if re.search( pattern, str( template.__dict__[field] ), flags ) ]
		return filteredTemplates

@core.executionTrace
def addTemplate( session, name, path, collection ):
	'''
	This Definition Adds A New Template To The Database.

	@param session: Database Session. ( Session )
	@param name: Template Name. ( String )
	@param path: Template Path. ( String )
	@param collection: Collection Id. ( String )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Adding : '{0}' Template To Database.".format( name ) )

	if not filterTemplates( session, "^{0}$".format( re.escape( path ) ), "path" ) :
		osStats = ",".join( [str( stat ) for stat in os.stat( path )] )
		dbItem = dbUtilities.types.DbTemplate( name = name, path = path, collection = collection, osStats = osStats )
		if dbItem.setContent() :
			return addItem( session, dbItem )
	else:
		LOGGER.warning( "!> {0} | '{1}' Template Path Already Exists In Database !".format( core.getModule( addTemplate ).__name__, path ) )
		return False

@core.executionTrace
def removeTemplate( session, id ):
	'''
	This Definition Remove A Template From The Database.

	@param session: Database Session. ( Session )
	@param id: Template Id. ( String )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Removing Template With Id '{0}' From Database.".format( id ) )

	dbTemplate = session.query( dbUtilities.types.DbTemplate ).filter_by( id = id ).one()
	return removeItem( session, dbTemplate )

@core.executionTrace
def updateTemplateContent( session, template ):
	'''
	This Definition Update A Template Content.

	@param session: Database Session. ( Session )
	@param template: Template To Template Content. ( DbTemplate )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Updating '{0}' Template Content.".format( template ) )

	template.osStats = ",".join( [str( stat ) for stat in os.stat( template.path )] )
	if template.setContent() :
		return commit( session )
	else :
		LOGGER.warning( "!> {0} | '{1}' Template Content Update Failed !".format( core.getModule( updateTemplateContent ).__name__, template.name ) )
		return False

@core.executionTrace
def updateTemplateLocation( session, template, path ):
	'''
	This Definition Updates A Template Location.

	@param session: Database Session. ( Session )
	@param template: Template To Update. ( DbTemplate )
	@param path: Template Path. ( Path )
	@return: Database Commit Success. ( Boolean )
	'''

	LOGGER.debug( "> Updating '{0}' Template Location.".format( template ) )

	if not filterTemplates( session, "^{0}$".format( re.escape( path ) ), "path" ) :
		template.path = path
		return updateTemplateContent( session, template )
	else:
		LOGGER.warning( "!> {0} | '{1}' Template Path Already Exists In Database !".format( core.getModule( updateTemplateLocation ).__name__, path ) )
		return False

@core.executionTrace
def checkTemplatesTableIntegrity( session ):
	'''
	This Definition Checks Templates Table Integrity.

	@param session: Database Session. ( Session )
	@return: Templates Table Erroneous Items. ( Dictionary )
	'''

	LOGGER.debug( "> Checking 'Templates' Database Table Integrity." )

	erroneousTemplates = {}
	if getTemplates( session ) :
		for template in getTemplates( session ) :
			if not os.path.exists( template.path ) :
				erroneousTemplates[template] = "INEXISTING_TEMPLATE_FILE_EXCEPTION"
				continue
			if not os.path.exists( template.helpFile ) :
				erroneousTemplates[template] = "INEXISTING_TEMPLATE_HELP_FILE_EXCEPTION"
	return erroneousTemplates

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
