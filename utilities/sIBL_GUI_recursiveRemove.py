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

'''
************************************************************************************************
***	sIBL_GUI_recursiveRemove.py
***
***	Platform:
***		Windows
***
***	Description:
***		Recursion Delete.
***
***	Others:
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import os
import sys

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def recursiveRemove(rootDirectory, pattern):
	'''
	This Definition Recursively Deletes The Matching Items.
		
	@param rootDirectory: Directory To Recurse. ( String )
	@param pattern: Pattern To Match. ( String )
	'''

	if os.path.exists(rootDirectory):
		for root, dirs, files in os.walk(rootDirectory):
			for item in files:
				itemPath = os.path.join(root, item).replace("\\", "/")
				if pattern in str(item):
					remove(itemPath)

def remove(item):
	'''
	This Definition Deletes Provided Item.
	@param item: Item To Delete. ( String )
	'''

	print("remove | Removing: '%s'" % item)
	try:
		os.remove(item)
	except:
		print("remove | '%s' Remove Failed!" % item)

if __name__ == "__main__":
	recursiveRemove(sys.argv[1], sys.argv[2])

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
