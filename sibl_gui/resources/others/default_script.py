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
verbosity_level = sIBL_GUI.verbosity_level
print("Verbosity level: '{0}'".format(verbosity_level))
# Setting verbosity level to 'Debug':
sIBL_GUI.set_verbosity_level(4)
# Setting verbosity level to 'Info':
sIBL_GUI.set_verbosity_level(3)

____()

"""
Preferences interactions:
"""
preferences = sIBL_GUI.settings
print("Preferences object: '{0}'".format(preferences))
preferences_file = preferences.file
print("Preferences file: '{0}'".format(preferences_file))
# Preferences value retrieval:
settings_verbosity_level = sIBL_GUI.settings.get_key("Settings", "verbosity_level").toString()
print("'Settings.verbosity_level': '{0}'".format(settings_verbosity_level))

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
sIBL_GUI.start_processing("Processing Example ...", steps)
for i in range(steps):
    foundations.core.wait(0.25)
    sIBL_GUI.step_processing()
sIBL_GUI.stop_processing()

____()

"""
Notifications interactions:
"""
sIBL_GUI.notifications_manager.notify("This is an 'Information' notification!")
sIBL_GUI.notifications_manager.warnify("This is a 'Warning' notification!")
sIBL_GUI.notifications_manager.exceptify("This is an 'Exception' notification!")

____()

"""
Layouts interactions:
"""
layouts = sIBL_GUI.layouts_manager.list_layouts()
print("Layouts: '{0}'".format(layouts))
current_layout = sIBL_GUI.layouts_manager.current_layout
print("Current layout: '{0}'".format(current_layout))
for layout in sIBL_GUI.layouts_manager.list_layouts():
    sIBL_GUI.process_events()
    sIBL_GUI.layouts_manager.restore_layout(layout)
sIBL_GUI.layouts_manager.restore_layout("edit_centric")

____()

"""
Fullscreen interactions:
"""
# sIBL_GUI.toggle_full_screen()

____()

"""
User application data directory:
"""
print("User application directory: '{0}'".format(sIBL_GUI.user_application_data_directory))

____()

"""
Components paths:
"""
components_paths = sIBL_GUI.components_paths
print("Components paths: '{0}'".format(components_paths))

____()

"""
Components list retrieval through various access points:
"""
components = sIBL_GUI.components_manager.list_components()
print("Components: '{0}'".format(components))
components = RuntimeGlobals.engine.components_manager.list_components()
print("Components: '{0}'".format(components))
components = components_manager.list_components()
print("Components: '{0}'".format(components))

____()

"""
Components interface access through various access points:
"""
script_editor = components_manager.get_interface("factory.script_editor")
ibl_sets_outliner = components_manager.components["core.ibl_sets_outliner"].interface
gps_map = components_manager["addons.gps_map"]
print(script_editor, ibl_sets_outliner, gps_map)

____()

"""
Actions Manager interactions:
"""
actions = actions_manager.list_actions()
print("Actions : {0}".format(actions))
action = actions_manager.get_action("Actions|Umbra|Components|factory.script_editor|&View|Toggle White Spaces")
action.trigger()

____()

"""
'factory.components_manager_ui' Component interactions:
"""
components_manager_ui = components_manager.get_interface("factory.components_manager_ui")
components = components_manager_ui.get_components()
print("Components: '{0}'".format(components))
names = components_manager_ui.list_components()
print("Components names: '{0}'".format(names))
# Component reload:
components_manager_ui.reload_component("addons.gps_map")
# Component deactivate:
components_manager_ui.deactivate_component("addons.gps_map")
# Component activate:
components_manager_ui.activate_component("addons.gps_map")

____()

"""
'core.collections_outliner' Component interactions:
"""
collections_outliner = components_manager.get_interface("core.collections_outliner")
collections = collections_outliner.get_collections()
print("Collections: '{0}'".format(collections))
collections_names = collections_outliner.list_collections()
print("Collections names: '{0}'".format(collections_names))
# Collections management:
collection = "Example Collection"
collections_outliner.add_collection(collection)
collection = collections_outliner.get_collection_by_name(collection)
collections_outliner.remove_collection(collection)

____()

"""
'core.ibl_sets_outliner' Component interactions:
"""
ibl_sets_outliner = components_manager.get_interface("core.ibl_sets_outliner")
example_ibl_set = umbra.ui.common.get_resource_path("others/Ditch_River_Example/Ditch-River_Example.ibl")
if example_ibl_set:
    ibl_sets_outliner.add_ibl_set("Example Ibl Set", example_ibl_set)
    ibl_sets = ibl_sets_outliner.get_ibl_sets()
    print("Ibl Sets: '{0}'".format(ibl_sets))
    ibl_sets_names = ibl_sets_outliner.list_ibl_sets()
    print("Ibl Sets names: '{0}'".format(ibl_sets_names))
    # Ibl Sets management:
    ibl_set = ibl_sets_outliner.get_ibl_set_by_name("Ditch River \( Example \)")
    ibl_sets_outliner.remove_ibl_set(ibl_set)
    ibl_sets_outliner.add_directory(os.path.dirname(example_ibl_set))
    ibl_sets_outliner.remove_ibl_set(ibl_sets_outliner.get_ibl_set_by_name("Ditch River \( Example \)"))

____()

"""
'core.templates_outliner' Component interactions:
"""
templates_outliner = components_manager.get_interface("core.templates_outliner")
templates_outliner.add_default_templates()
templates = templates_outliner.get_templates()
print("Templates: '{0}'".format(templates))
templates_names = templates_outliner.list_templates()
print("Templates names: '{0}'".format(templates_names))
if templates_names:
    template = templates_outliner.get_template_by_name(templates_names[0])
    name, path = template.name, template.path
    templates_outliner.remove_template(template)
    templates_outliner.add_template(name, path)

____()

"""
'addons.database_operations' Component interactions:
"""
database_operations = components_manager.get_interface("addons.database_operations")
database_operations.update_database()

____()

"""
'addons.gps_map' Component interactions:
"""
gps_map = components_manager.get_interface("addons.gps_map")
ibl_sets_outliner = components_manager.get_interface("core.ibl_sets_outliner")
ibl_sets = ibl_sets_outliner.get_ibl_sets()
if ibl_sets:
    gps_map.show()
    for ibl_set in ibl_sets:
        gps_map.set_marker(ibl_set)
    gps_map.remove_markers()
    gps_map.hide()

____()

"""
'addons.loader_script' Component interactions:
"""
loader_script = components_manager.get_interface("addons.loader_script")
ibl_sets_outliner = components_manager.get_interface("core.ibl_sets_outliner")
ibl_sets = ibl_sets_outliner.get_ibl_sets()
templates_outliner = components_manager.get_interface("core.templates_outliner")
templates_outliner.add_default_templates()
templates = templates_outliner.get_templates()

if ibl_sets and templates:
    output_script = loader_script.output_loader_script(templates[0], ibl_sets[0])
    script_editor = components_manager.get_interface("factory.script_editor")
    script_editor.load_file(output_script)

____()

"""
'addons.locations_browser' Component interactions:
"""
locations_browser = components_manager.get_interface("addons.locations_browser")
script_editor = components_manager.get_interface("factory.script_editor")
file = script_editor.get_current_editor().file
locations_browser.explore_directory(os.path.dirname(file))

____()

"""
'addons.online_updater' Component interactions:
"""
online_updater = components_manager.get_interface("addons.online_updater")
online_updater.check_for_new_releases()

____()

"""
'addons.preview' Component interactions:
"""
preview = components_manager.get_interface("addons.preview")
ibl_sets_outliner = components_manager.get_interface("core.ibl_sets_outliner")
ibl_sets = ibl_sets_outliner.get_ibl_sets()
if ibl_sets:
    preview.view_images(paths=(ibl_sets[0].lighting_image, ibl_sets[0].icon))

____()
