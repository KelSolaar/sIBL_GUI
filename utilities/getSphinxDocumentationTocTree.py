#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**getSphinxDocumentationTocTree.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Gets Sphinx documentation Toc Tree file.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import glob
import os
import re
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.strings as strings
import foundations.verbose
from foundations.io import File

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"FILES_EXTENSION",
		"TOCTREE_TEMPLATE_BEGIN",
		"TOCTREE_TEMPLATE_END",
		"getSphinxDocumentationTocTree"]

LOGGER = foundations.verbose.installLogger()

FILES_EXTENSION = ".rst"

TOCTREE_TEMPLATE_BEGIN = ["Welcome to {0} |version|'s documentation!\n",
						"{0}\n",
						"\n",
						"Contents:\n",
						"\n",
						".. toctree::\n",
						" :maxdepth: 2\n",
						" :numbered:\n"]
TOCTREE_TEMPLATE_END = ["Search:\n",
					"==================\n",
					"\n",
					"* :ref:`genindex`\n",
					"* :ref:`modindex`\n",
					"* :ref:`search`\n", ]

foundations.verbose.getLoggingConsoleHandler()
foundations.verbose.setVerbosityLevel(3)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getSphinxDocumentationTocTree(title, fileIn, fileOut, contentDirectory):
	"""
	This definition gets Sphinx documentation index file.

	:param title: Package title. ( String )
	:param fileIn: File to convert. ( String )
	:param fileOut: Output file. ( String )
	:param contentDirectory: Content directory. ( String )
	"""

	LOGGER.info("{0} | Building Sphinx documentation index '{1}' file!".format(getSphinxDocumentationTocTree.__name__,
																				fileOut))
	file = File(fileIn)
	file.read()

	existingFiles = [strings.getSplitextBasename(item)
					for item in glob.glob("{0}/*{1}".format(contentDirectory, FILES_EXTENSION))]
	relativeDirectory = contentDirectory.replace("{0}/".format(os.path.dirname(fileOut)), "")

	tocTree = ["\n"]
	for line in file.content:
		search = re.search(r"`([a-zA-Z_ ]+)`_", line)
		if not search:
			continue

		item = search.groups()[0]
		code = "{0}{1}".format(item[0].lower(), item.replace(" ", "")[1:])
		if code in existingFiles:
			link = "{0}/{1}".format(relativeDirectory, code)
			data = "{0}{1}{2} <{3}>\n".format(" ", " " * line.index("-"), item, link)
			LOGGER.info("{0} | Adding '{1}' entry to Toc Tree!".format(getSphinxDocumentationTocTree.__name__,
																		data.replace("\n", "")))
			tocTree.append(data)
	tocTree.append("\n")

	TOCTREE_TEMPLATE_BEGIN[0] = TOCTREE_TEMPLATE_BEGIN[0].format(title)
	TOCTREE_TEMPLATE_BEGIN[1] = TOCTREE_TEMPLATE_BEGIN[1].format("=" * len(TOCTREE_TEMPLATE_BEGIN[0]))
	content = TOCTREE_TEMPLATE_BEGIN
	content.extend(tocTree)
	content.extend(TOCTREE_TEMPLATE_END)

	file = File(fileOut)
	file.content = content
	file.write()

if __name__ == "__main__":
	getSphinxDocumentationTocTree(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
