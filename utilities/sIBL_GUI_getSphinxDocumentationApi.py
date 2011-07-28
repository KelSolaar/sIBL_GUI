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
# The following code is protected by GNU GPL V3 Licence.
#

"""
**sIBL_GUI_getSphinxDocumentationApi.py

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Gets Sphinx Documentation Toc Tree File.

**Others:**

"""

#***********************************************************************************************
#***    Python Begin.
#***********************************************************************************************
#***********************************************************************************************
#***    External Imports.
#***********************************************************************************************
import importlib
import logging
import os
import pyclbr
import re
import shutil
import sys
from collections import OrderedDict

#***********************************************************************************************
#***    Internal Imports.
#***********************************************************************************************
import foundations.core as core
import foundations.strings as strings
from foundations.io import File
from foundations.globals.constants import Constants
from foundations.walker import Walker

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries"))
import python.pyclbr as moduleBrowser

#***********************************************************************************************
#***    Global Variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

LOGGING_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
LOGGING_CONSOLE_HANDLER.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
LOGGER.addHandler(LOGGING_CONSOLE_HANDLER)

core.setVerbosityLevel(3)

FILES_EXTENSION = ".rst"

TOCTREE_TEMPLATE_BEGIN = ["Api\n",
                        "====\n",
                        "\n",
                        "Modules Summary:\n",
                        "\n",
                        ".. toctree::\n",
                        "\n"]

TOCTREE_TEMPLATE_END = []

STATEMENTS_UPDATE_MESSAGGE = "#***********************************************************************************************\n" \
                "#***\tStatements updated for auto-documentation purpose.\n" \
                "#***********************************************************************************************"

CONTENT_SUBSTITUTIONS = {"\tumbra\.ui\.common\.uiStandaloneSystemExitExceptionHandler": "{0}\n\tpass\n".format(STATEMENTS_UPDATE_MESSAGGE),
                        "APPLICATION \= QApplication\(sys.argv\)": "{0}".format(STATEMENTS_UPDATE_MESSAGGE)}

#***********************************************************************************************
#***    Main Python Code.
#***********************************************************************************************
def getSphinxDocumentationApi(sourceDirectory, cloneDirectory, outputDirectory, apiFile):
    """
    This Definition Gets Sphinx Documentation Api.

    @param sourceDirectory: Source Directory. ( String )
    @param cloneDirectory: Source Clone Directory. ( String )
    @param outputDirectory: Content Directory. ( String )
    @param apiFile: Api File. ( String )
    """

    LOGGER.info("{0} | Building Sphinx Documentation Api!".format(getSphinxDocumentationApi.__name__))

    not sourceDirectory in sys.path and sys.path.append(sourceDirectory)

    walker = Walker(sourceDirectory)
    walker.walk(filtersIn=("\.py$",))

    modules = []
    for file in sorted(walker.files.values()):
        LOGGER.info("{0} | Python File: '{1}'".format(getSphinxDocumentationApi.__name__, file))
        module = "{0}.{1}" .format((".".join(os.path.dirname(file).replace(sourceDirectory, "").split("/"))), strings.getSplitextBasename(file)).strip(".")
        LOGGER.info("{0} | Module Name: '{1}'".format(getSphinxDocumentationApi.__name__, module))
        directory = os.path.dirname(os.path.join(cloneDirectory, module.replace(".", "/")))
        if not os.path.exists(directory):
            os.makedirs(directory)
        source = os.path.join(directory, os.path.basename(file))
        shutil.copyfile(file, source)

        sourceFile = File(source)
        sourceFile.read()
        trimStartIndex = trimEndIndex = None
        for i, line in enumerate(sourceFile.content):
            if re.search("__name__ +\=\= +\"__main__\"", line):
                trimStartIndex = i
            if trimStartIndex and (line.startswith("\n") or line.startswith("    ") or line.startswith("\t")):
                trimEndIndex = i
            for pattern, value in CONTENT_SUBSTITUTIONS.items():
                if re.search(pattern, line):
                    sourceFile.content[i] = value

        if trimStartIndex and trimEndIndex:
            LOGGER.info("{0} | Trimming '__main__' Statements!".format(getSphinxDocumentationApi.__name__, module))
            content = [sourceFile.content[i] for i in range(trimStartIndex)]
            content.append("\n{0}\n".format(STATEMENTS_UPDATE_MESSAGGE))
            content.extend([sourceFile.content[i] for i in range(trimEndIndex, len(sourceFile.content))])
            sourceFile.content = content
            sourceFile.write()

        not directory in sys.path and sys.path.append(directory)

        if "__init__.py" in file:
            continue

        rstFilePath = "{0}{1}".format(module, FILES_EXTENSION)
        LOGGER.info("{0} | Building API File: '{1}'".format(getSphinxDocumentationApi.__name__, rstFilePath))
        rstFile = File(os.path.join(outputDirectory, rstFilePath))
        header = ["_`{0}`\n".format(module),
                "==={0}\n".format("="*len(module)),
                "\n",
                ".. automodule:: {0}\n".format(module),
                "\n"]
        rstFile.content.extend(header)

        functions = OrderedDict()
        classes = OrderedDict()
        for member, object in moduleBrowser._readmodule(module, [source, ]).items():
            if not "methods" in object.__dict__.keys():
                if not member.startswith("_"):
                    functions[member] = [".. autofunction:: {0}\n".format(member)]

            else:
                classes[member] = [".. autoclass:: {0}\n".format(member),
                                    "   :show-inheritance:\n",
                                    "   :members:\n"]

        functions and rstFile.content.append("Functions\n---------\n\n")
        for function in functions.values():
            rstFile.content.extend(function)
            rstFile.content.append("\n")

        classes and rstFile.content.append("Classes\n-------\n\n")
        for class_ in classes.values():
            rstFile.content.extend(class_)
            rstFile.content.append("\n")

        rstFile.write()
        modules.append(module)

    apiFile = File(apiFile)
    apiFile.content.extend(TOCTREE_TEMPLATE_BEGIN)
    for module in modules:
        apiFile.content.append("   {0} <{1}>\n".format(module, "api/{0}".format(module)))
    apiFile.content.extend(TOCTREE_TEMPLATE_END)
    apiFile.write()

if __name__ == "__main__":
    getSphinxDocumentationApi(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

#***********************************************************************************************
#***    Python End.
#***********************************************************************************************
