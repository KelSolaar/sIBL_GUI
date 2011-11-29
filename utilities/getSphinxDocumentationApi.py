#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**getSphinxDocumentationApi.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Gets Sphinx documentation Api files.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import importlib
import logging
import os
import pyclbr
import re
import shutil
import sys
from collections import OrderedDict

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.strings as strings
from foundations.io import File
from foundations.globals.constants import Constants
from foundations.walkers import OsWalker

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries"))
import python.pyclbr as moduleBrowser

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

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
						"   :maxdepth: 1\n",
						"\n"]

EXCLUDED_PYTHON_MODULES = ("defaultScript\.py",)

TOCTREE_TEMPLATE_END = []

STATEMENTS_UPDATE_MESSAGGE = "#**********************************************************************************************************************\n" \
							"#***\tSphinx: Statements updated for auto-documentation purpose.\n" \
							"#**********************************************************************************************************************"

DECORATORS_COMMENT_MESSAGE = "#***\tSphinx: Decorator commented for auto-documentation purpose."

CONTENT_SUBSTITUTIONS = {"APPLICATION \= QApplication\(sys.argv\)": "{0}".format(STATEMENTS_UPDATE_MESSAGGE),
						"This method initializes the class.\n" :
						".. Sphinx: Statements updated for auto-documentation purpose.\n",
						"PYTHON_LANGUAGE \= getPythonLanguage\(\)" :
						"{0}\n{1}".format(STATEMENTS_UPDATE_MESSAGGE, "PYTHON_LANGUAGE = None"),
						"LOGGING_LANGUAGE \= getLoggingLanguage\(\)" :
						"{0}\n{1}".format(STATEMENTS_UPDATE_MESSAGGE, "LOGGING_LANGUAGE = None"),
						"TEXT_LANGUAGE \= getTextLanguage\(\)" :
						"{0}\n{1}".format(STATEMENTS_UPDATE_MESSAGGE, "TEXT_LANGUAGE = None")}

#**********************************************************************************************************************
#***	Main Python code.
#**********************************************************************************************************************
def getSphinxDocumentationApi(sourceDirectory, cloneDirectory, outputDirectory, apiFile):
	"""
	This definition gets Sphinx documentation API.

	:param sourceDirectory: Source directory. ( String )
	:param cloneDirectory: Source clone directory. ( String )
	:param outputDirectory: Content directory. ( String )
	:param apiFile: API file. ( String )
	"""

	LOGGER.info("{0} | Building Sphinx documentation API!".format(getSphinxDocumentationApi.__name__))

	not cloneDirectory in sys.path and sys.path.append(sourceDirectory)

	osWalker = OsWalker(sourceDirectory)
	osWalker.walk(filtersIn=("\.ui$",))
	for file in sorted(osWalker.files.values()):
		LOGGER.info("{0} | Ui file: '{1}'".format(getSphinxDocumentationApi.__name__, file))
		targetDirectory = os.path.dirname(file).replace(sourceDirectory, "")
		directory = "{0}{1}".format(cloneDirectory, targetDirectory)
		if not os.path.exists(directory):
			os.makedirs(directory)
		source = os.path.join(directory, os.path.basename(file))
		shutil.copyfile(file, source)

	osWalker = OsWalker(sourceDirectory)
	osWalker.walk(filtersIn=("\.py$",), filtersOut=EXCLUDED_PYTHON_MODULES)
	modules = []
	for file in sorted(osWalker.files.values()):
		LOGGER.info("{0} | Python file: '{1}'".format(getSphinxDocumentationApi.__name__, file))
		module = "{0}.{1}" .format((".".join(os.path.dirname(file).replace(sourceDirectory, "").split("/"))),
											strings.getSplitextBasename(file)).strip(".")
		LOGGER.info("{0} | Module name: '{1}'".format(getSphinxDocumentationApi.__name__, module))
		directory = os.path.dirname(os.path.join(cloneDirectory, module.replace(".", "/")))
		if not os.path.exists(directory):
			os.makedirs(directory)
		source = os.path.join(directory, os.path.basename(file))
		shutil.copyfile(file, source)

		sourceFile = File(source)
		sourceFile.read()
		trimStartIndex = trimEndIndex = None
		for i, line in enumerate(sourceFile.content):
			if re.search(r"__name__ +\=\= +\"__main__\"", line):
				trimStartIndex = i
			if trimStartIndex and re.search(r"^\s*$", line):
				trimEndIndex = i
			for pattern, value in CONTENT_SUBSTITUTIONS.items():
				if re.search(pattern, line):
					sourceFile.content[i] = re.sub(pattern, value, line)
			if i < len(sourceFile.content):
				if re.search(r"^[ \t]*@\w+", line) and (re.search(r"^[ \t]*def \w+", sourceFile.content[i + 1]) or \
				re.search(r"^[ \t]*class \w+", sourceFile.content[i + 1]) or \
				re.search(r"^[ \t]*@\w+", sourceFile.content[i + 1])):
					if not re.search(r"^[ \t]*@property", line) and \
						not re.search(r"^[ \t]*@\w+\.setter", line) and \
						not re.search(r"^[ \t]*@\w+\.deleter", line) and \
						not re.search(r"^[ \t]*@exceptionsHandler", line):
						indent = re.search(r"^([ \t]*)", line)
						sourceFile.content[i] = "{0}{1} {2}".format(indent.groups()[0], DECORATORS_COMMENT_MESSAGE, line)

		if trimStartIndex and trimEndIndex:
			LOGGER.info("{0} | Trimming '__main__' statements!".format(getSphinxDocumentationApi.__name__))
			content = [sourceFile.content[i] for i in range(trimStartIndex)]
			content.append("\n{0}\n".format(STATEMENTS_UPDATE_MESSAGGE))
			content.extend([sourceFile.content[i] for i in range(trimEndIndex, len(sourceFile.content))])
			sourceFile.content = content
		sourceFile.write()

		if "__init__.py" in file:
			continue

		rstFilePath = "{0}{1}".format(module, FILES_EXTENSION)
		LOGGER.info("{0} | Building API file: '{1}'".format(getSphinxDocumentationApi.__name__, rstFilePath))
		rstFile = File(os.path.join(outputDirectory, rstFilePath))
		header = ["_`{0}`\n".format(module),
				"==={0}\n".format("="*len(module)),
				"\n",
				".. automodule:: {0}\n".format(module),
				"\n"]
		rstFile.content.extend(header)

		functions = OrderedDict()
		classes = OrderedDict()
		moduleAttributes = OrderedDict()
		for member, object in moduleBrowser._readmodule(module, [source, ]).items():
			if object.__class__ == moduleBrowser.Function:
				if not member.startswith("_"):
					functions[member] = [".. autofunction:: {0}\n".format(member)]
			elif object.__class__ == moduleBrowser.Class:
				classes[member] = [".. autoclass:: {0}\n".format(member),
									"	:show-inheritance:\n",
									"	:members:\n"]
			elif object.__class__ == moduleBrowser.Global:
				if not member.startswith("_"):
					moduleAttributes[member] = [".. attribute:: {0}.{1}\n".format(module, member)]

		moduleAttributes and rstFile.content.append("Module Attributes\n-----------------\n\n")
		for moduleAttribute in moduleAttributes.values():
			rstFile.content.extend(moduleAttribute)
			rstFile.content.append("\n")

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

	testsModules = [module for module in modules if "tests" in module]
	modules = [module for module in modules if not "tests" in module]

	apiFile = File(apiFile)
	apiFile.content.extend(TOCTREE_TEMPLATE_BEGIN)
	for module in modules:
		apiFile.content.append("   {0} <{1}>\n".format(module, "api/{0}".format(module)))
	for module in testsModules:
		apiFile.content.append("   {0} <{1}>\n".format(module, "api/{0}".format(module)))
	apiFile.content.extend(TOCTREE_TEMPLATE_END)
	apiFile.write()

if __name__ == "__main__":
	getSphinxDocumentationApi(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
