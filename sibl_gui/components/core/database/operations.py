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

from __future__ import unicode_literals

import os
import re

import foundations.common
import foundations.exceptions
import foundations.strings
import sibl_gui.components.core.database.exceptions
from sibl_gui.components.core.database.types import Collection
from sibl_gui.components.core.database.types import IblSet
from sibl_gui.components.core.database.types import Template

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
           "create_session",
           "get_session",
           "commit",
           "add_item",
           "add_standard_item",
           "remove_item",
           "remove_standard_item",
           "update_item_content",
           "update_item_location",
           "filter_items",
           "item_exists",
           "get_ibl_sets",
           "filter_ibl_sets",
           "ibl_set_exists",
           "add_ibl_set",
           "remove_ibl_set",
           "update_ibl_set_content",
           "update_ibl_set_location",
           "check_ibl_sets_table_integrity",
           "get_collections",
           "filter_collections",
           "get_collections_by_type",
           "collection_exists",
           "add_collection",
           "remove_collection",
           "get_collections_ibl_sets",
           "getCollectionIblSetsCount",
           "get_collection_templates_count",
           "get_templates",
           "filter_templates",
           "template_exists",
           "add_template",
           "remove_template",
           "update_template_content",
           "update_template_location",
           "check_templates_table_integrity"]

LOGGER = foundations.verbose.install_logger()

DATABASE_EXCEPTIONS = {
    sibl_gui.components.core.database.exceptions.MissingIblSetFileError: "Ibl Set's file is missing!",
    sibl_gui.components.core.database.exceptions.MissingIblSetIconError: "Ibl Set's icon is missing!",
    sibl_gui.components.core.database.exceptions.MissingIblSetPreviewImageError: "Ibl Set's preview image is missing!",
    sibl_gui.components.core.database.exceptions.MissingIblSetBackgroundImageError: "Ibl Set's background image is missing!",
    sibl_gui.components.core.database.exceptions.MissingIblSetLightingImageError: "Ibl Set's lighting image is missing!",
    sibl_gui.components.core.database.exceptions.MissingIblSetReflectionImageError: "Ibl Set's reflection image is missing!",
    sibl_gui.components.core.database.exceptions.MissingTemplateFileError: "Template file is missing!",
    sibl_gui.components.core.database.exceptions.MissingTemplateHelpFileError: "Template help file is missing!"}

DEFAULT_SESSION_MAKER = None
DEFAULT_SESSION = None


def create_session():
    """
    Creates a default session.

    :return: Database session.
    :rtype: Session
    """

    return DEFAULT_SESSION_MAKER()


def get_session(session=None):
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

    return get_session(kwargs.get("session")).query(*args, **kwargs)


@foundations.exceptions.handle_exceptions(sibl_gui.components.core.database.exceptions.DatabaseOperationError)
def commit(session=None):
    """
    Commits changes to the Database.

    :param session: Database session.
    :type session: Session
    :return: Database commit success.
    :rtype: bool
    """

    session = get_session(session)

    try:
        session.commit()
        return True
    except Exception as error:
        session.rollback()
        raise sibl_gui.components.core.database.exceptions.DatabaseOperationError(
            "{0} | Database commit error: '{1}'".format(__name__, error))


def add_item(item, session=None):
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

    session = get_session(session)
    session.add(item)
    return commit(session)


def add_standard_item(type, name, path, collection, session=None):
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

    session = get_session(session)

    if not filter_items(query(type), "^{0}$".format(re.escape(path)), "path"):
        if not foundations.common.path_exists(path):
            LOGGER.warning("!> {0} | '{1}' file doesn't exists!".format(__name__, path))
            return False

        os_stats = ",".join((foundations.strings.to_string(stat) for stat in os.stat(path)))
        database_item = type(name=name, path=path, collection=collection, os_stats=os_stats)
        if database_item.set_content():
            return add_item(database_item, session)
    else:
        LOGGER.warning("!> {0} | '{1}' '{2}' path already exists in Database!".format(__name__, path, type.__name__))
        return False


def remove_item(item, session=None):
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

    session = get_session(session)
    session.delete(item)
    return commit(session)


def remove_standard_item(type, identity, session=None):
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
    return remove_item(item, get_session(session))


def update_item_content(item, session=None):
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

    if not foundations.common.path_exists(item.path):
        LOGGER.warning("!> {0} | '{1}' file doesn't exists!".format(__name__, item.path))
        return False

    item.os_stats = ",".join(map(foundations.strings.to_string, os.stat(item.path)))
    if item.set_content():
        return commit(get_session(session))
    else:
        LOGGER.warning("!> {0} | '{1}' '{2}' content update failed!".format(__name__,
                                                                            item.name,
                                                                            item.__class__.__name__))
        return False


def update_item_location(item, path, session=None):
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

    session = get_session(session)

    if not filter_items(query(item.__class__), "^{0}$".format(re.escape(path)), "path"):
        item.path = path
        return update_item_content(item, session)
    else:
        LOGGER.warning("!> {0} | '{1}' '{2}' path already exists in Database!".format(__name__,
                                                                                      path,
                                                                                      item.__class__.__name__))
        return False


def filter_items(items, pattern, field, flags=0):
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

    return [item for item in items if re.search(pattern, foundations.strings.to_string(item.__dict__[field]), flags)]


def item_exists(items, pattern, field, flags=0):
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

    return True if filter_items(items, pattern, field, flags) else False


def get_ibl_sets(session=None):
    """
    Returns the Ibl Sets from the Database.

    :param session: Database session.
    :type session: Session
    :return: Database Ibl Sets.
    :rtype: list
    """

    return get_session(session).query(IblSet)


def filter_ibl_sets(pattern, field, flags=0, session=None):
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

    return filter_items(get_ibl_sets(get_session(session)), pattern, field, flags)


def ibl_set_exists(path, session=None):
    """
    Returns if given Ibl Set exists in the Database.

    :param name: Ibl Set path.
    :type name: unicode
    :param session: Database session.
    :type session: Session
    :return: Ibl Set exists.
    :rtype: bool
    """

    return True if filter_ibl_sets("^{0}$".format(re.escape(path)), "path", session=get_session(session)) else False


def add_ibl_set(name, path, collection, session=None):
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

    return add_standard_item(IblSet, name, path, collection, get_session(session))


def remove_ibl_set(identity, session=None):
    """
    Removes an Ibl Set from the Database.

    :param identity: Ibl Set id.
    :type identity: unicode
    :param session: Database session.
    :type session: Session
    :return: Database commit success.
    :rtype: bool
    """

    return remove_standard_item(IblSet, identity, get_session(session))


def update_ibl_set_content(ibl_set, session=None):
    """
    Update an Ibl Set content.

    :param ibl_set: Ibl Set to set content.
    :type ibl_set: IblSet
    :param session: Database session.
    :type session: Session
    :return: Database commit success.
    :rtype: bool
    """

    return update_item_content(ibl_set, get_session(session))


def update_ibl_set_location(ibl_set, path, session=None):
    """
    Updates an Ibl Set location.

    :param ibl_set: Ibl Set to update.
    :type ibl_set: IblSet
    :param path: Ibl Set path.
    :type path: Path
    :param session: Database session.
    :type session: Session
    :return: Database commit success.
    :rtype: bool
    """

    return update_item_location(ibl_set, path, get_session(session))


def check_ibl_sets_table_integrity(session=None):
    """
    Checks sets table integrity.

    :param session: Database session.
    :type session: Session
    :return: Ibl Sets table erroneous items.
    :rtype: dict
    """

    LOGGER.debug("> Checking 'Sets' Database table integrity.")

    session = get_session(session)

    erroneous_ibl_sets = {}
    if get_ibl_sets(session):
        for ibl_set in get_ibl_sets(session):
            exceptions = []
            if not foundations.common.path_exists(ibl_set.path):
                exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetFileError)

            if not foundations.common.path_exists(ibl_set.icon):
                exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetIconError)

            if ibl_set.preview_image and not foundations.common.path_exists(os.path.join(os.path.dirname(ibl_set.path),
                                                                                         ibl_set.preview_image)):
                exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetPreviewImageError)
            if ibl_set.background_image and not foundations.common.path_exists(
                    os.path.join(os.path.dirname(ibl_set.path),
                                 ibl_set.background_image)):
                exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetBackgroundImageError)
            if ibl_set.lighting_image and not foundations.common.path_exists(os.path.join(os.path.dirname(ibl_set.path),
                                                                                          ibl_set.lighting_image)):
                exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetLightingImageError)
            if ibl_set.reflection_image and not foundations.common.path_exists(
                    os.path.join(os.path.dirname(ibl_set.path),
                                 ibl_set.reflection_image)):
                exceptions.append(sibl_gui.components.core.database.exceptions.MissingIblSetReflectionImageError)

            if exceptions:
                erroneous_ibl_sets[ibl_set] = exceptions

    return erroneous_ibl_sets


def get_collections(session=None):
    """
    Returns the Collections from the Database.

    :param session: Database session.
    :type session: Session
    :return: Database Collections.
    :rtype: list
    """

    return get_session(session).query(Collection)


def filter_collections(pattern, field, flags=0, session=None):
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

    return filter_items(get_collections(get_session(session)), pattern, field, flags)


def get_collections_by_type(type, session=None):
    """
    Returns Collections of given type.

    :param type: Type name.
    :type type: unicode
    :param session: Database session.
    :type session: Session
    :return: Ibl Sets Collections.
    :rtype: list
    """

    return [collection for collection in filter_collections(type, "type", session=get_session(session))]


def filter_collections_by_type(type, pattern, field, flags=0, session=None):
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

    return list(set(get_collections_by_type(type, session)).intersection(
        filter_collections("{0}".format(pattern), field, flags, get_session(session))))


def filter_ibl_sets_collections(pattern, field, flags=0, session=None):
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

    return filter_collections_by_type("ibl_sets", pattern, field, flags, get_session(session))


def filter_templates_collections(pattern, field, flags=0, session=None):
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

    return filter_collections_by_type("templates", pattern, field, flags, get_session(session))


def collection_exists(name, session=None):
    """
    Returns if the Collection exists in the Database.

    :param name: Collection name.
    :type name: unicode
    :param session: Database session.
    :type session: Session
    :return: Collection exists.
    :rtype: bool
    """

    return True if filter_collections("^{0}$".format(name), "name", session=get_session(session)) else False


def add_collection(collection, type, comment, session=None):
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

    session = get_session(session)

    if not filter_collections("^{0}$".format(collection), "name", session=session):
        database_item = Collection(name=collection, type=type, comment=comment)
        return add_item(database_item, session)
    else:
        LOGGER.warning("!> {0} | '{1}' Collection already exists in Database!".format(__name__, collection))
        return False


def remove_collection(identity, session=None):
    """
    Removes a Collection from the Database.

    :param identity: Collection id.
    :type identity: unicode
    :param session: Database session.
    :type session: Session
    :return: Database commit success.
    :rtype: bool
    """

    return remove_standard_item(Collection, identity, get_session(session))


def get_collections_ibl_sets(identities, session=None):
    """
    Returns Ibl Sets from Collections ids

    :param identities: Collections ids.
    :type identities: list
    :param session: Database session.
    :type session: Session
    :return: Ibl Sets list.
    :rtype: list
    """

    ibl_sets = []
    for identity in identities:
        collectionSets = filter_ibl_sets("^{0}$".format(identity), "collection", session=get_session(session))
        if collectionSets:
            for ibl_set in collectionSets:
                ibl_sets.append(ibl_set)
    return ibl_sets


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

    return get_session(session).query(IblSet).filter_by(collection=collection.id).count()


def get_collection_templates_count(collection, session=None):
    """
    Returns given Collection Tempates count.

    :param collection: Collection.
    :type collection: Collection
    :param session: Database session.
    :type session: Session
    :return: Collection Templates count.
    :rtype: int
    """

    return get_session(session).query(Template).filter_by(collection=collection.id).count()


def get_templates(session=None):
    """
    Returns the Templates from the Database.

    :param session: Database session.
    :type session: Session
    :return: Database Templates.
    :rtype: list
    """

    return get_session(session).query(Template)


def filter_templates(pattern, field, flags=0, session=None):
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

    return filter_items(get_templates(get_session(session)), pattern, field, flags)


def template_exists(path, session=None):
    """
    Returns if given Template exists in the Database.

    :param name: Template path.
    :type name: unicode
    :param session: Database session.
    :type session: Session
    :return: Template exists.
    :rtype: bool
    """

    return True if filter_templates("^{0}$".format(re.escape(path)), "path", session=get_session(session)) else False


def add_template(name, path, collection, session=None):
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

    return add_standard_item(Template, name, path, collection, get_session(session))


def remove_template(identity, session=None):
    """
    Removes a Template from the Database.

    :param identity: Template id.
    :type identity: unicode
    :param session: Database session.
    :type session: Session
    :return: Database commit success.
    :rtype: bool
    """

    return remove_standard_item(Template, identity, get_session(session))


def update_template_content(template, session=None):
    """
    Update a Template content.

    :param template: Template to Template content.
    :type template: Template
    :param session: Database session.
    :type session: Session
    :return: Database commit success.
    :rtype: bool
    """

    return update_item_content(template, get_session(session))


def update_template_location(template, path, session=None):
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

    return update_item_location(template, path, get_session(session))


def check_templates_table_integrity(session=None):
    """
    Checks Templates table integrity.

    :param session: Database session.
    :type session: Session
    :return: Templates table erroneous items.
    :rtype: dict
    """

    LOGGER.debug("> Checking 'templates' Database table integrity.")

    session = get_session(session)

    erroneous_templates = {}
    if get_templates(session):
        for template in get_templates(session):
            exceptions = []
            if not foundations.common.path_exists(template.path):
                exceptions.append(sibl_gui.components.core.database.exceptions.MissingTemplateFileError)

            if not foundations.common.path_exists(template.help_file):
                exceptions.append(sibl_gui.components.core.database.exceptions.MissingTemplateHelpFileError)

            if exceptions:
                erroneous_templates[template] = exceptions

    return erroneous_templates
