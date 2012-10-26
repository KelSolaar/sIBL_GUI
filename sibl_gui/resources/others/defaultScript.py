"""
Welcome to sIBL_GUI Default Script file!

The purpose of this file is to give a quick overview of some sIBL_GUI Api features.
"""

import os

import foundations.core
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
	foundations.core.wait(0.25)
	sIBL_GUI.stepProcessing()
sIBL_GUI.stopProcessing()

____()

"""
Notifications interactions:
"""
sIBL_GUI.notificationsManager.notify("This is an 'Information' notification!")
sIBL_GUI.notificationsManager.warnify("This is a 'Warning' notification!")
sIBL_GUI.notificationsManager.exceptify("This is an 'Exception' notification!")

____()

"""
Layouts interactions:
"""
layouts = sIBL_GUI.layoutsManager.listLayouts()
print("Layouts: '{0}'".format(layouts))
currentLayout = sIBL_GUI.layoutsManager.currentLayout
print("Current layout: '{0}'".format(currentLayout))
for layout in sIBL_GUI.layoutsManager.listLayouts():
	sIBL_GUI.processEvents()
	sIBL_GUI.layoutsManager.restoreLayout(layout)
sIBL_GUI.layoutsManager.restoreLayout("editCentric")

____()

"""
Fullscreen interactions:
"""
# sIBL_GUI.toggleFullScreen()

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
Components interface access through various access points:
"""
scriptEditor = componentsManager.getInterface("factory.scriptEditor")
iblSetsOutliner = componentsManager.components["core.iblSetsOutliner"].interface
gpsMap = componentsManager["addons.gpsMap"]
print(scriptEditor, iblSetsOutliner, gpsMap)

____()

"""
Actions Manager interactions:
"""
actions = actionsManager.listActions()
print("Actions : {0}".format(actions))
action = actionsManager.getAction("Actions|Umbra|Components|factory.scriptEditor|&View|Toggle White Spaces")
action.trigger()

____()

"""
'factory.componentsManagerUi' Component interactions:
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
'core.collectionsOutliner' Component interactions:
"""
collectionsOutliner = componentsManager.getInterface("core.collectionsOutliner")
collections = collectionsOutliner.getCollections()
print("Collections: '{0}'".format(collections))
collectionsNames = collectionsOutliner.listCollections()
print("Collections names: '{0}'".format(collectionsNames))
# Collections management:
collection = "Example Collection"
collectionsOutliner.addCollection(collection)
collection = collectionsOutliner.getCollectionByName(collection)
collectionsOutliner.removeCollection(collection)

____()

"""
'core.iblSetsOutliner' Component interactions:
"""
iblSetsOutliner = componentsManager.getInterface("core.iblSetsOutliner")
exampleIblSet = umbra.ui.common.getResourcePath("others/Ditch_River_Example/Ditch-River_Example.ibl")
if exampleIblSet:
	iblSetsOutliner.addIblSet("Example Ibl Set", exampleIblSet)
	iblSets = iblSetsOutliner.getIblSets()
	print("Ibl Sets: '{0}'".format(iblSets))
	iblSetsNames = iblSetsOutliner.listIblSets()
	print("Ibl Sets names: '{0}'".format(iblSetsNames))
	# Ibl Sets management:
	iblSet = iblSetsOutliner.getIblSetByName("Ditch River \( Example \)")
	iblSetsOutliner.removeIblSet(iblSet)
	iblSetsOutliner.addDirectory(os.path.dirname(exampleIblSet))
	iblSetsOutliner.removeIblSet(iblSetsOutliner.getIblSetByName("Ditch River \( Example \)"))

____()

"""
'core.templatesOutliner' Component interactions:
"""
templatesOutliner = componentsManager.getInterface("core.templatesOutliner")
templatesOutliner.addDefaultTemplates()
templates = templatesOutliner.getTemplates()
print("Templates: '{0}'".format(templates))
templatesNames = templatesOutliner.listTemplates()
print("Templates names: '{0}'".format(templatesNames))
if templatesNames:
	template = templatesOutliner.getTemplateByName(templatesNames[0])
	name, path = template.name, template.path
	templatesOutliner.removeTemplate(template)
	templatesOutliner.addTemplate(name, path)

____()

"""
'addons.databaseOperations' Component interactions:
"""
databaseOperations = componentsManager.getInterface("addons.databaseOperations")
databaseOperations.updateDatabase()

____()

"""
'addons.gpsMap' Component interactions:
"""
gpsMap = componentsManager.getInterface("addons.gpsMap")
iblSetsOutliner = componentsManager.getInterface("core.iblSetsOutliner")
iblSets = iblSetsOutliner.getIblSets()
if iblSets:
	gpsMap.show()
	for iblSet in iblSets:
		gpsMap.setMarker(iblSet)
	gpsMap.removeMarkers()
	gpsMap.hide()

____()

"""
'addons.loaderScript' Component interactions:
"""
loaderScript = componentsManager.getInterface("addons.loaderScript")
iblSetsOutliner = componentsManager.getInterface("core.iblSetsOutliner")
iblSets = iblSetsOutliner.getIblSets()
templatesOutliner = componentsManager.getInterface("core.templatesOutliner")
templatesOutliner.addDefaultTemplates()
templates = templatesOutliner.getTemplates()

if iblSets and templates:
	outputScript = loaderScript.outputLoaderScript(templates[0], iblSets[0])
	scriptEditor = componentsManager.getInterface("factory.scriptEditor")
	scriptEditor.loadFile(outputScript)

____()

"""
'addons.locationsBrowser' Component interactions:
"""
locationsBrowser = componentsManager.getInterface("addons.locationsBrowser")
scriptEditor = componentsManager.getInterface("factory.scriptEditor")
file = scriptEditor.getCurrentEditor().file
locationsBrowser.exploreDirectory(os.path.dirname(file))

____()

"""
'addons.onlineUpdater' Component interactions:
"""
onlineUpdater = componentsManager.getInterface("addons.onlineUpdater")
onlineUpdater.checkForNewReleases()

____()

"""
'addons.preview' Component interactions:
"""
preview = componentsManager.getInterface("addons.preview")
iblSetsOutliner = componentsManager.getInterface("core.iblSetsOutliner")
iblSets = iblSetsOutliner.getIblSets()
if iblSets:
	preview.viewImages(paths=(iblSets[0].lightingImage, iblSets[0].icon))

____()
