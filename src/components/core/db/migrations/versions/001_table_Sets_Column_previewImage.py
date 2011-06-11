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
***    001_table_Sets_Column_previewImage.py
***
***    Platform:
***        Windows, Linux, Mac Os X
***
***    Description:
***          Database Migration Module.
***
***    Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***    Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***    External Imports
#***********************************************************************************************
from sqlalchemy import *
from migrate import *

#***********************************************************************************************
#***    Global Variables
#***********************************************************************************************
METADATA = MetaData()
TABLE = Table("Sets", METADATA)

#***********************************************************************************************
#***    Module Classes And Definitions
#***********************************************************************************************
def upgrade(dbEngine):
    """
    This Definition Upgrades The Database.

    @param dbEngine: Database Engine. ( Object )
    """
    
    METADATA.bind = dbEngine
    column = Column("previewImage", String)
    column.create(TABLE)

def downgrade(dbEngine):
    """
    This Definition Downgrades The Database.

    @param dbEngine: Database Engine. ( Object )
    """
    
    pass

#***********************************************************************************************
#***    Python End
#***********************************************************************************************