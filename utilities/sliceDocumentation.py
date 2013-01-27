#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**sliceDocumentation.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Slices given documentation file.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
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
import foundations.verbose
from foundations.io import File

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"OUTPUT_FILES_EXTENSION",
		"SLICE_ATTRIBUTE_INDENT",
		"CONTENT_DELETION",
		"CONTENT_SUBSTITUTIONS",
		"sliceDocumentation"]

LOGGER = foundations.verbose.installLogger()

OUTPUT_FILES_EXTENSION = "rst"
SLICE_ATTRIBUTE_INDENT = 2
CONTENT_DELETION = ()
CONTENT_SUBSTITUTIONS = {"resources/": "../",
						"     \|":"            |" }

foundations.verbose.getLoggingConsoleHandler()
foundations.verbose.setVerbosityLevel(3)


#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def sliceDocumentation(fileIn, outputDirectory):
	"""
	This Definition slices given documentation file.

	:param fileIn: File to convert. ( String )
	:param outputDirectory: Output directory. ( String )
	"""

	LOGGER.info("{0} | Slicing '{1}' file!".format(sliceDocumentation.__name__, fileIn))
	file = File(fileIn)
	file.cache()

	slices = OrderedDict()
	for i, line in enumerate(file.content):
		search = re.search(r"^\.\. \.(\w+)", line)
		if search:
			slices[search.groups()[0]] = i + SLICE_ATTRIBUTE_INDENT

	index = 0
	for slice, sliceStart in slices.iteritems():
		sliceFile = File(os.path.join(outputDirectory, "{0}.{1}".format(slice, OUTPUT_FILES_EXTENSION)))
		LOGGER.info("{0} | Outputing '{1}' file!".format(sliceDocumentation.__name__, sliceFile.path))
		sliceEnd = index < (len(slices.values()) - 1) and slices.values()[index + 1] - SLICE_ATTRIBUTE_INDENT or \
		len(file.content)

		for i in range(sliceStart, sliceEnd):
			skipLine = False
			for item in CONTENT_DELETION:
				if re.search(item, file.content[i]):
					LOGGER.info("{0} | Skipping Line '{1}' with '{2}' content!".format(sliceDocumentation.__name__,
																						i,
																						item))
					skipLine = True
					break

			if skipLine:
				continue

			line = file.content[i]
			for pattern, value in CONTENT_SUBSTITUTIONS.iteritems():
				line = re.sub(pattern, value, line)

			search = re.search(r"-  `[\w ]+`_ \(([\w\.]+)\)", line)
			if search:
				LOGGER.info("{0} | Updating Line '{1}' link: '{2}'!".format(sliceDocumentation.__name__,
																			i,
																			search.groups()[0]))
				line = "-  :ref:`{0}`\n".format(search.groups()[0])
			sliceFile.content.append(line)

		sliceFile.write()
		index += 1

if __name__ == "__main__":
	sliceDocumentation(sys.argv[1], sys.argv[2])
