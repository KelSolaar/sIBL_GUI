#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**10df7481424c_initial_revision.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Initial revision.

**Others:**
	Revises: None
	Creation date: 2014-04-26 21:22:45.831459
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sqlalchemy
from alembic import op

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["revision", "down_revision", "upgrade", "downgrade"]

revision = "10df7481424c"
down_revision = None

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def upgrade():
	"""
	Upgrade the database to current revision.
	"""

	pass

def downgrade():
	"""
	Downgrade the database to previous revision.
	"""

	pass
