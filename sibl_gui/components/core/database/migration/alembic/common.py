#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines common *Alembic* manipulation related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import copy
import sqlalchemy
from alembic import op

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose

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
		"rename_column"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def rename_column(table, column, name):
	"""
	Provides *Alembic* support for *SQLite* incomplete *ALTER* ddl statement, renames given table column with given name.
	
	:param table: Table name.
	:type table: unicode
	:param column: Column name.
	:type column: unicode
	:param name: New column name.
	:type name: unicode
	:return: Definition success.
	:rtype: bool
	"""

	engine = op.get_bind()
	metadata = sqlalchemy.MetaData(bind=engine)
	metadata.reflect()

	source_table = metadata.tables[table]
	source_table_name = source_table.name

	select = sqlalchemy.sql.select([source_column for source_column in source_table.columns])

	source_columns = [copy.copy(source_column) for source_column in source_table.columns]
	for source_column in source_columns:
		source_column.table = None
		if source_column.name == column:
			source_column.name = name

	target_table_name = "target_{0}".format(table)
	op.create_table(target_table_name, *source_columns)
	metadata.reflect()
	target_table = metadata.tables[target_table_name]

	insert = sqlalchemy.sql.insert(target_table).from_select([source_column.name for source_column in source_columns],
															select)
	engine.execute(insert)

	op.drop_table(source_table_name)
	op.rename_table(target_table_name, source_table_name)

	return True
