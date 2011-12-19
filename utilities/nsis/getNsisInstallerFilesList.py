#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**getNsisInstallerFilesList.py**

**Platform:**
	Windows.

**Description:**
	This module defines generates 2 lists of NSIS commands (install & uninstall) for all files in a given directory.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import glob
import os
import sys

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["INSTALLED_DIRECTORY_TEMPLATE",
		"INSTALLED_FILE_TEMPLATE",
		"UNINSTALLED_DIRECTORY_TEMPLATE",
		"UNINSTALLED_FILE_TEMPLATE",
		"Data",
		"visitor",
		"getNsisDependencies"]

INSTALLED_DIRECTORY_TEMPLATE = ' SetOutPath "$instdir%s"'
INSTALLED_FILE_TEMPLATE = ' File "%s"'
UNINSTALLED_DIRECTORY_TEMPLATE = ' RMDir "$instdir%s"'
UNINSTALLED_FILE_TEMPLATE = ' Delete "$instdir%s"'

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Data(dict):
	"""
	This class creates an object similar to C/C++ structured type.
	"""

	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		kwargs.update(self.__dict__)

		dict.__init__(self, **kwargs)
		self.__dict__ = self

def visitor(data, currentDirectory, items):
	"""
	This definition handles the directories walking interactions.

	:param data: Data. ( Data )
	:param currentDirectory: Directory being walked. ( String )
	:param items: Directory items. ( List )
	"""

	data.directoriesCounter += 1

	files = [item for item in items if os.path.isfile(os.path.join(currentDirectory, item))]
	directory = currentDirectory[len(data.sourceDirectory):]

	data.visitedItems.append((files, directory))

	if len(files):
		print >> data.installedItemsFileHandler, INSTALLED_DIRECTORY_TEMPLATE % (directory)
		for item in files:
			print >> data.installedItemsFileHandler, INSTALLED_FILE_TEMPLATE % (os.path.join(os.path.abspath(currentDirectory), item))
			data.filesCounter += 1
		print >> data.installedItemsFileHandler, " "

def getNsisDependencies(sourceDirectory, installedItemsFile, uninstalledItemsFile):
	"""
	This definition gets NSIS dependencies.

	:param sourceDirectory: Source directory. ( String )
	:param installedItemsFile: Installed files file name. ( String )
	:param uninstalledItemsFile: Uninstalled files file name. ( String )
	"""

	installedItemsFileHandler = file(installedItemsFile, "w")
	uninstalledItemsFileHandler = file(uninstalledItemsFile, "w")

	data = Data(**{"visitedItems" : [],
			"installedItemsFileHandler" : installedItemsFileHandler,
			"uninstalledItemsFileHandler" : uninstalledItemsFileHandler,
			"sourceDirectory" : sourceDirectory,
			"filesCounter" : 0,
			"directoriesCounter" : 0})

	print "Generating install & uninstall list of files"
	print " For directory", sourceDirectory
	print >> installedItemsFileHandler, " ; Files to install\n"
	print >> uninstalledItemsFileHandler, " ; Files and directories to remove\n"

	os.path.walk(sourceDirectory, visitor, data)
	installedItemsFileHandler.close()

	print "Install list done!"
	print " ", data.filesCounter, "Files in", data.directoriesCounter, "Directories"

	data.visitedItems.reverse()
	for (files, directory) in data.visitedItems:
			for item in files:
				print >> uninstalledItemsFileHandler, UNINSTALLED_FILE_TEMPLATE % (os.sep.join((directory, item)))
			if directory:
				print >> uninstalledItemsFileHandler, UNINSTALLED_DIRECTORY_TEMPLATE % directory
				print >> uninstalledItemsFileHandler, " "

	print >> uninstalledItemsFileHandler, " "
	print >> uninstalledItemsFileHandler, " RMDir /r \"$instdir\\support\\\""
	print >> uninstalledItemsFileHandler, " RMDir \"$instdir\\\""

	uninstalledItemsFileHandler.close()
	print "Uninstall list done!\n"

if __name__ == "__main__":
	getNsisDependencies(sys.argv[1], sys.argv[2], sys.argv[3])
