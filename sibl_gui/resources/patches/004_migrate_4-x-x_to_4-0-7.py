#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**004_migrate_4-x-x_to_4-0-7.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Migrates sIBL_GUI from 4.x.x to 4.0.7.

**Others:**

"""

from __future__ import unicode_literals

import os
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.schema import DropTable
from sqlalchemy.schema import MetaData
from sqlalchemy.schema import Table

import foundations.common
import foundations.verbose
import sibl_gui.components.core.database.operations
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UID", "apply"]

LOGGER = foundations.verbose.install_logger()

UID = "ddfd9d292ea73aa3450989af7d7ee945"

def apply():
    """
    Triggers the patch execution.

    :return: Definition success.
    :rtype: bool
    """

    database_directory = os.path.join(RuntimeGlobals.user_application_data_directory, Constants.database_directory)

    migrations_directory = os.path.join(database_directory, "migrations")
    if foundations.common.path_exists(migrations_directory):
        foundations.io.remove(migrations_directory)

    database_file = os.path.join(database_directory, Constants.database_file)
    engine = create_engine("sqlite:///{0}".format(database_file))
    connection = engine.connect()
    transaction = connection.begin()
    inspector = reflection.Inspector.from_engine(engine)
    metadata = MetaData()
    for name in inspector.get_table_names():
        if name in ("Migrate", "{{ locals().pop('version_table') }}"):
            connection.execute(DropTable(Table(name, metadata)))
    transaction.commit()

    return True
