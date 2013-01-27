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
import os
import re
import shutil
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.strings
import foundations.verbose
import foundations.walkers
from foundations.io import File

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries"))
import python.pyclbr as moduleBrowser

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
		"FILES_EXTENSION",
		"TOCTREE_TEMPLATE_BEGIN",
		"TOCTREE_TEMPLATE_END",
		"EXCLUDED_PYTHON_MODULES",
		"STATEMENTS_UPDATE_MESSAGGE",
		"DECORATORS_COMMENT_MESSAGE",
		"CONTENT_SUBSTITUTIONS",
		"getSphinxDocumentationApi"]

LOGGER = foundations.verbose.installLogger()

FILES_EXTENSION = ".rst"

TOCTREE_TEMPLATE_BEGIN = ["Api\n",
						"====\n",
						"\n",
						"Modules Summary:\n",
						"\n",
						".. toctree::\n",
						"   :maxdepth: 1\n",
						"\n"]

TOCTREE_TEMPLATE_END = []

EXCLUDED_PYTHON_MODULES = ("tests",
                        "defaultScript\.py",
						"001_migrate_3-x-x_to_4-0-0\.py",
						"002_migrate_4-x-x_to_4-0-2\.py",
						"003_migrate_4-x-x_to_4-0-3\.py",
						"001_dummy\.py")

STATEMENTS_UPDATE_MESSAGGE = "#**********************************************************************************************************************\n" \
							"#***\tSphinx: Statements updated for auto-documentation purpose.\n" \
							"#**********************************************************************************************************************"

DECORATORS_COMMENT_MESSAGE = "#***\tSphinx: Decorator commented for auto-documentation purpose."

CONTENT_SUBSTITUTIONS = {"^_initializeApplication\(\)$" : "{0}".format(STATEMENTS_UPDATE_MESSAGGE),
						"This method initializes the class.\n" :
						".. Sphinx: Statements updated for auto-documentation purpose.\n",
						"PYTHON_LANGUAGE \= getPythonLanguage\(\)" :
						"{0}\n{1}".format(STATEMENTS_UPDATE_MESSAGGE, "PYTHON_LANGUAGE = None"),
						"LOGGING_LANGUAGE \= getLoggingLanguage\(\)" :
						"{0}\n{1}".format(STATEMENTS_UPDATE_MESSAGGE, "LOGGING_LANGUAGE = None"),
						"TEXT_LANGUAGE \= getTextLanguage\(\)" :
						"{0}\n{1}".format(STATEMENTS_UPDATE_MESSAGGE, "TEXT_LANGUAGE = None")}

foundations.verbose.getLoggingConsoleHandler()
foundations.verbose.setVerbosityLevel(3)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getSphinxDocumentationApi(packages, cloneDirectory, outputDirectory, apiFile):
	"""
	This definition gets Sphinx documentation API.

	:param packages: Packages. ( String )
	:param cloneDirectory: Source clone directory. ( String )
	:param outputDirectory: Content directory. ( String )
	:param apiFile: API file. ( String )
	"""

	LOGGER.info("{0} | Building Sphinx documentation API!".format(getSphinxDocumentationApi.__name__))

	if os.path.exists(cloneDirectory):
		shutil.rmtree(cloneDirectory)
		os.makedirs(cloneDirectory)

	packagesModules = {"apiModules" : [],
					"testsModules" : []}
	for package in packages.split(","):
		package = __import__(package)
		path = foundations.common.getFirstItem(package.__path__)
		sourceDirectory = os.path.dirname(path)

		for file in sorted(list(foundations.walkers.filesWalker(sourceDirectory, filtersIn=("{0}.*\.ui$".format(path),)))):
			LOGGER.info("{0} | Ui file: '{1}'".format(getSphinxDocumentationApi.__name__, file))
			targetDirectory = os.path.dirname(file).replace(sourceDirectory, "")
			directory = "{0}{1}".format(cloneDirectory, targetDirectory)
			if not foundations.common.pathExists(directory):
				os.makedirs(directory)
			source = os.path.join(directory, os.path.basename(file))
			shutil.copyfile(file, source)

		modules = []
		for file in sorted(list(foundations.walkers.filesWalker(sourceDirectory, filtersIn=("{0}.*\.py$".format(path),),
		filtersOut=EXCLUDED_PYTHON_MODULES))):
			LOGGER.info("{0} | Python file: '{1}'".format(getSphinxDocumentationApi.__name__, file))
			module = "{0}.{1}" .format((".".join(os.path.dirname(file).replace(sourceDirectory, "").split("/"))),
												foundations.strings.getSplitextBasename(file)).strip(".")
			LOGGER.info("{0} | Module name: '{1}'".format(getSphinxDocumentationApi.__name__, module))
			directory = os.path.dirname(os.path.join(cloneDirectory, module.replace(".", "/")))
			if not foundations.common.pathExists(directory):
				os.makedirs(directory)
			source = os.path.join(directory, os.path.basename(file))
			shutil.copyfile(file, source)

			sourceFile = File(source)
			sourceFile.cache()
			trimFromIndex = trimEndIndex = None
			inMultilineString = inDecorator = False
			for i, line in enumerate(sourceFile.content):
				if re.search(r"__name__ +\=\= +\"__main__\"", line):
					trimFromIndex = i
				for pattern, value in CONTENT_SUBSTITUTIONS.iteritems():
					if re.search(pattern, line):
						sourceFile.content[i] = re.sub(pattern, value, line)

				strippedLine = line.strip()
				if re.search(r"^\"\"\"", strippedLine):
					inMultilineString = not inMultilineString

				if inMultilineString:
					continue

				if re.search(r"^@\w+", strippedLine) and \
				not re.search(r"@property", strippedLine) and \
				not re.search(r"^@\w+\.setter", strippedLine) and \
				not re.search(r"^@\w+\.deleter", strippedLine):
					inDecorator = True
					indent = re.search(r"^([ \t]*)", line)

				if re.search(r"^[ \t]*def \w+", sourceFile.content[i]) or \
					re.search(r"^[ \t]*class \w+", sourceFile.content[i]):
					inDecorator = False

				if not inDecorator:
					continue

				sourceFile.content[i] = "{0}{1} {2}".format(indent.groups()[0], DECORATORS_COMMENT_MESSAGE, line)

			if trimFromIndex:
				LOGGER.info("{0} | Trimming '__main__' statements!".format(getSphinxDocumentationApi.__name__))
				content = [sourceFile.content[i] for i in range(trimFromIndex)]
				content.append("{0}\n".format(STATEMENTS_UPDATE_MESSAGGE))
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
			for member, object in moduleBrowser._readmodule(module, [source, ]).iteritems():
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
			for moduleAttribute in moduleAttributes.itervalues():
				rstFile.content.extend(moduleAttribute)
				rstFile.content.append("\n")

			functions and rstFile.content.append("Functions\n---------\n\n")
			for function in functions.itervalues():
				rstFile.content.extend(function)
				rstFile.content.append("\n")

			classes and rstFile.content.append("Classes\n-------\n\n")
			for class_ in classes.itervalues():
				rstFile.content.extend(class_)
				rstFile.content.append("\n")

			rstFile.write()
			modules.append(module)

		packagesModules["apiModules"].extend([module for module in modules if not "tests" in module])
		packagesModules["testsModules"].extend([module for module in modules if "tests" in module])

	apiFile = File(apiFile)
	apiFile.content.extend(TOCTREE_TEMPLATE_BEGIN)
	for module in packagesModules["apiModules"]:
		apiFile.content.append("   {0} <{1}>\n".format(module, "api/{0}".format(module)))
	for module in packagesModules["testsModules"]:
		apiFile.content.append("   {0} <{1}>\n".format(module, "api/{0}".format(module)))
	apiFile.content.extend(TOCTREE_TEMPLATE_END)
	apiFile.write()

if __name__ == "__main__":
	getSphinxDocumentationApi(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
