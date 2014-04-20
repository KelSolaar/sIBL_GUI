#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**${up_revision}_.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**

**Others:**
	Revises: ${down_revision}
	Creation date: ${create_date}
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sqlalchemy
from alembic import op
${imports if imports else ""}

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

revision = "${up_revision}"
down_revision = "${down_revision}"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def upgrade():
	"""
	Upgrade the database to current revision.
	"""

	${upgrades if upgrades else "pass"}

def downgrade():
	"""
	Downgrade the database to previous revision.
	"""

	${upgrades if upgrades else "pass"}