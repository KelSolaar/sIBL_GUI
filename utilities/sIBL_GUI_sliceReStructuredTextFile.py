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

"""
************************************************************************************************
***	sIBL_GUI_sliceReStructuredTextFile.py
***
***	Platform:
***		Windows
***
***	Description:
***		Slices Provided reStructuredText File.
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
import sys
from collections import OrderedDict

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
from foundations.io import File
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

LOGGING_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
LOGGING_CONSOLE_HANDLER.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
LOGGER.addHandler(LOGGING_CONSOLE_HANDLER)

core.setVerbosityLevel(3)

FILES_EXTENSION = "rst"
SLICE_ATTRIBUTE_INDENT = 2

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def sliceReStructuredTextFile(fileIn, outputDirectory):
	"""
	This Definition Slices Slices Provided reStructuredText File.
		
	@param fileIn: File To Convert. ( String )
	@param outputDirectory: Output Directory. ( String )
	"""

	LOGGER.info("{0} | Slicing '{1}' File!".format(sliceReStructuredTextFile.__name__, fileIn))
	file = File(fileIn)
	file.read()

	slices = OrderedDict()
	for i, line in enumerate(file.content):
		search = re.search("^\.\. \.(\w+)", line)
		if search:
			slices[search.groups()[0]] = i + SLICE_ATTRIBUTE_INDENT

	index = 0
	for slice, sliceStart in slices.items():
		sliceFile = File(os.path.join(outputDirectory, "{0}.{1}".format(slice, FILES_EXTENSION)))
		LOGGER.info("{0} | Outputing '{1}' File!".format(sliceReStructuredTextFile.__name__, sliceFile.file))
		sliceEnd = index < (len(slices.values()) - 1) and slices.values()[index + 1] - SLICE_ATTRIBUTE_INDENT or len(file.content)
		sliceFile.content = [file.content[i] for i in range(sliceStart, sliceEnd)]
		sliceFile.write()
		index += 1

if __name__ == "__main__":
	sliceReStructuredTextFile(sys.argv[1], sys.argv[2])

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
