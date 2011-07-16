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
***	sIBL_GUI_textileToHtml.py
***
***	Platform:
***		Windows
***
***	Description:
***		Converts A Textile File To HTML.
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
import sys
import textile

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

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def textileToHtml(fileIn, fileOut, title):
	"""
	This Definition Outputs A Textile File To HTML.
		
	@param fileIn: File To Convert. ( String )
	@param fileOut: Output File. ( String )
	@param title: HTML File Title. ( String )
	"""

	LOGGER.info("{0} | Converting '{1}' Textile File To HTML!".format(textileToHtml.__name__, fileIn))
	file = File(fileIn)
	file.read()

	output = []
	output.append("<html>\n\t<head>\n")
	output.append("\t\t<title>{0}</title>\n".format(title))
	output.append(
			"""\t\t<style type="text/css">
	            body {
	                text-align: justify;
	                font-size: 10pt;
	                margin: 10px 10px 10px 10px;
	                background-color: rgb(48, 48, 48);
	                color: rgb(192, 192, 192);
	            }
	            A:link {
	                text-decoration: none;
	                color: rgb(160, 96, 64);
	            }
	            A:visited {
	                text-decoration: none;
	                color: rgb(160, 96, 64);
	            }
	            A:active {
	                text-decoration: none;
	                color: rgb(160, 96, 64);
	            }
	            A:hover {
	                text-decoration: underline;
	                color: rgb(160, 96, 64);
	            }
	        </style>\n""")
	output.append("\t</head>\n\t<body>\n\t")
	output.append("\n\t".join(line for line in textile.textile("".join(file.content)).split("\n") if line))
	output.append("\t\t</span>\n")
	output.append("\t</body>\n</html>")

	file = File(fileOut)
	file.content = output
	file.write()

	LOGGER.info("{0} | Formatting HTML File!".format(textileToHtml.__name__))
	os.system("tidy -config {0} -m '{1}'".format(os.path.join(os.path.dirname(__file__), "tidy/tidySettings.rc"), file.file))

	file.read()
	file.content = [line.replace(" " * 4, "\t") for line in file.content]
	file.write()

if __name__ == "__main__":
	textileToHtml(sys.argv[1], sys.argv[2], sys.argv[3])

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
