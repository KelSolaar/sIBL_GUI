"""
Welcome to sIBL_GUI Default Script file!

The purpose of this file is to give a quick overview of some sIBL_GUI Api features.
"""

import os
import time

import foundations.common
import umbra.ui.common

def ____():
	print "-" * 120

____()

"""
Interactions with sIBL_GUI are done through locals exposed attributes:
"""
print(locals().keys())

____()

"""
Logging messages handling:
"""
LOGGER.critical("This is a 'Critical' logging message!")
LOGGER.error("This is an 'Error' logging message!")
LOGGER.warning("This is a 'Warning' logging message!")
LOGGER.info("This is an 'Info' logging message!")
LOGGER.debug("This is a 'Debug' logging message!")

____()


"""
Verbosity level interactions:
"""
verbosityLevel = sIBL_GUI.verbosityLevel
print("Verbosity level: '{0}'".format(verbosityLevel))
# Setting verbosity level to 'Debug':
sIBL_GUI.setVerbosityLevel(4)
# Setting verbosity level to 'Info':
sIBL_GUI.setVerbosityLevel(3)

____()

"""
Preferences interactions:
"""
preferences = sIBL_GUI.settings
print("Preferences object: '{0}'".format(preferences))
preferencesFile = preferences.file
print("Preferences file: '{0}'".format(preferencesFile))
# Preferences value retrieval:
settingsVerbosityLevel = sIBL_GUI.settings.getKey("Settings", "verbosityLevel").toString()
print("'Settings.verbosityLevel': '{0}'".format(settingsVerbosityLevel))

____()

"""
Command line parameters interactions:
"""
parameters = sIBL_GUI.parameters
print("Command line parameters: '{0}'".format(parameters))

____()

"""
Processing interactions:
"""
steps = 5
sIBL_GUI.startProcessing("Processing Example ...", steps)
for i in range(steps):
	foundations.common.wait(0.25)
	sIBL_GUI.stepProcessing()
sIBL_GUI.stopProcessing()

____()

"""
Layouts interactions:
"""
layouts = sIBL_GUI.listLayouts()
print("Layouts: '{0}'".format(layouts))
currentLayout = sIBL_GUI.currentLayout
print("Current layout: '{0}'".format(currentLayout))
for layout in sIBL_GUI.listLayouts(userLayouts=False):
	sIBL_GUI.processEvents()
	sIBL_GUI.restoreLayout(layout)
sIBL_GUI.restoreLayout("editCentric")

____()

"""
Fullscreen interactions:
"""
sIBL_GUI.toggleFullScreen()

____()

"""
User application data directory:
"""
print("User application directory: '{0}'".format(sIBL_GUI.userApplicationDataDirectory))

____()

"""
Components paths:
"""
componentsPaths = sIBL_GUI.componentsPaths
print("Components paths: '{0}'".format(componentsPaths))

____()

"""
Components list retrieval through various access points:
"""
components = sIBL_GUI.componentsManager.listComponents()
print("Components: '{0}'".format(components))
components = RuntimeGlobals.engine.componentsManager.listComponents()
print("Components: '{0}'".format(components))
components = componentsManager.listComponents()
print("Components: '{0}'".format(components))

____()

"""
Components interface access:
"""
scriptEditor = componentsManager.getInterface("factory.scriptEditor")
databaseBrowser = componentsManager.getInterface("core.databaseBrowser")
gpsMap = componentsManager.getInterface("addons.gpsMap")
print(scriptEditor, databaseBrowser, gpsMap)

____()

"""
Components Manager Ui interactions:
"""
componentsManagerUi = componentsManager.getInterface("factory.componentsManagerUi")
components = componentsManagerUi.getComponents()
print("Components: '{0}'".format(components))
names = componentsManagerUi.listComponents()
print("Components names: '{0}'".format(names))
# Component reload:
componentsManagerUi.reloadComponent("addons.gpsMap")
# Component deactivate:
componentsManagerUi.deactivateComponent("addons.gpsMap")
# Component activate:
componentsManagerUi.activateComponent("addons.gpsMap")

____()

"""
Collections Outliner interactions:
"""
collectionsOutliner = componentsManager.getInterface("core.collectionsOutliner")
collections = collectionsOutliner.getCollections()
print("Collections: '{0}'".format(collections))
names = collectionsOutliner.listCollections()
print("Collections names: '{0}'".format(names))
# Collections management:
collection = "Example Collection"
collectionsOutliner.addCollection(collection)
collection = collectionsOutliner.getCollectionByName(collection)
collectionsOutliner.removeCollection(collection)

____()

"""
Database Browser interactions:
"""
databaseBrowser = componentsManager.getInterface("core.databaseBrowser")
exampleIblSet = umbra.ui.common.getResourcePath("others/Ditch_River_Example/Ditch-River_Example.ibl")
if exampleIblSet:
	databaseBrowser.addIblSet("Example Ibl Set", exampleIblSet)
	iblSets = databaseBrowser.getIblSets()
	print("Ibl Sets: '{0}'".format(iblSets))
	names = databaseBrowser.listIblSets()
	print("Ibl Sets names: '{0}'".format(names))
	# Ibl Sets management:
	iblSet = databaseBrowser.getIblSetByName("Ditch River \( Example \)")
	databaseBrowser.removeIblSet(iblSet)
	databaseBrowser.addDirectory(os.path.dirname(exampleIblSet))
	databaseBrowser.removeIblSet(databaseBrowser.getIblSetByName("Ditch River \( Example \)"))

____()

"""
Templates Outliner interactions:
"""
templatesOutliner = componentsManager.getInterface("core.templatesOutliner")
templates = templatesOutliner.getTemplates()
print("Templates: '{0}'".format(templates))
names = templatesOutliner.listTemplates()
print("Templates names: '{0}'".format(names))

____()