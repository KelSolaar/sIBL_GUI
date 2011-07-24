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
**sIBL_GUI_getSphinxDocumentationTocTree.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Gets Sphinx Documentation Toc Tree File.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************
#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import glob
import logging
import os
import re
import sys
from collections import OrderedDict

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.strings as strings
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

FILES_EXTENSION = ".rst"

TOCTREE_TEMPLATE_BEGIN = ["Welcome to sIBL_GUI |version|'s documentation!\n",
						"==============================================\n",
						"\n",
						"Contents:\n",
						"\n",
						".. toctree::\n",
						"   :maxdepth: 3\n",
						"   :numbered:\n"]
TOCTREE_TEMPLATE_END = ["Search:\n"
					"==================\n"
					"\n"
					"* :ref:`search`\n"]

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def getSphinxDocumentationTocTree(fileIn, fileOut, contentDirectory):
	"""
	This Definition Gets Sphinx Documentation Index File.
		
	@param fileIn: File To Convert. ( String )
	@param fileOut: Output File. ( String )
	@param contentDirectory: Content Directory. ( String )
	"""

	LOGGER.info("{0} | Building Sphinx Documentation Index '{1}' File!".format(getSphinxDocumentationTocTree.__name__, fileOut))
	file = File(fileIn)
	file.read()

	existingFiles = [strings.getSplitextBasename(item) for item in glob.glob("{0}/*{1}".format(contentDirectory, FILES_EXTENSION))]
	relativeDirectory = contentDirectory.replace("{0}/".format(os.path.dirname(fileOut)), "")

	tocTree = ["\n"]
	for line in file.content:
		search = re.search("`([a-zA-Z_ ]+)`_", line)
		if not search:
			continue

		item = search.groups()[0]
		code = "{0}{1}".format(item[0].lower(), item.replace(" ", "")[1:])
		if code in existingFiles:
			link = "{0}/{1}".format(relativeDirectory, code)
			datas = "{0}{1}{2} <{3}>\n".format("   ", " " * line.index("-"), item, link)
			LOGGER.info("{0} | Adding '{1}' Entry To Toc Tree!".format(getSphinxDocumentationTocTree.__name__, datas.replace("\n", "")))
			tocTree.append(datas)
	tocTree.append("\n")

	content = TOCTREE_TEMPLATE_BEGIN
	content.extend(tocTree)
	content.extend(TOCTREE_TEMPLATE_END)

	file = File(fileOut)
	file.content = content
	file.write()

if __name__ == "__main__":
	getSphinxDocumentationTocTree(sys.argv[1], sys.argv[2], sys.argv[3])

#***********************************************************************************************
#***	Python End
#***********************************************************************************************