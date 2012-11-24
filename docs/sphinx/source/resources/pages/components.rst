_`Components`
=============

**sIBL_GUI** has currently 3 categories of Components:

-  **Default Component** (Components inheriting from *Python Object*).
-  **QWidget Component** (Components inheriting from *Qt QWidget*).
-  **QObject Component** (Components inheriting from *Qt QObject*).

Those 2 types are split into 4 main families:

-  **Factory** (Factory required Components, not deactivable and not removable).
-  **Core** (Core required Components, not deactivable and not removable).
-  **Addons** (Factory optional Components, deactivable and removable).
-  **User** (User optional Components, deactivable and removable).

.. raw:: html

   <br/>

_`Factory`
----------

.. raw:: html

   <br/>

.. _factory.componentsManagerUi:

_`Components Manager Ui` (factory.componentsManagerUi)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ComponentsManagerUi.jpg            |
+---------------------------------------------------------------------+

The *Components Manager Ui* Component allows **sIBL_GUI** addons and user Components activation / deactivation (Factory and Core Components are required and not deactivable). Selected Components details are displayed in the bottom *Components Informations* widget.

Interactions:

-  **Right clic**: Displays a context menu described further.

Columns Descriptions:

-  **Components**: Components names (Components are sorted by families).
-  **Activated**: Components activations status.
-  **Category**: Components categories (Default or Ui).
-  **Dependencies**: Components dependencies on others Components.
-  **Version**: Components versions.

Context menu:

+--------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ComponentsManagerUiContextMenu.jpg            |
+--------------------------------------------------------------------------------+

-  **Activate Component(s)**: Activates selected Component(s).
-  **Dectivate Component(s)**: Deactivates selected Component(s).
-  **Reload Component(s)**: Reloads selected Component(s) (Deactivates the Component, reloads Component code, activates back the Component).

Addons Functionalities:

-  **Open Component(s) Location(s) ...**: Opens selected Component(s) directory(s).
-  **Edit Component(s) ...**: Edits selected Component(s) in *Script Editor* Component.

.. raw:: html

   <br/>

.. _factory.preferencesManager:

_`Preferences Manager` (factory.preferencesManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_PreferencesManager.jpg            |
+--------------------------------------------------------------------+

The *Preferences Manager* Component is used to configure **sIBL_GUI** behavior. There are 2 pages where settings can be changed:

-  **General**: Overall **sIBL_GUI** settings.
-  **Others**: Components settings.

General Page:

-  **Logging Formatter**: Adjusts **sIBL_GUI** logging formatter:

   -  Default: Default logging formatter: **Logging Level: Message**.
   -  Extended: Extended logging formatter: **Time - Thread - Logging Level: Message**.
   -  Standard: Simple standard logging formatter: **Message**.

-  **Verbose Level**: Adjusts **sIBL_GUI** verbose level between different modes (Debug being the most verbosing, Critical the less):

   -  Debug
   -  Info
   -  Warning
   -  Error
   -  Critical

-  **Restore Geometry On Layout Change**: **sIBL_GUI** window size and position will be restored when switching layouts.

Others Page:

Those settings are Components dependent and will be described per related Component.

.. raw:: html

   <br/>

.. _factory.scriptEditor:

_`Script Editor` (factory.scriptEditor)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditor.jpg            |
+--------------------------------------------------------------+

The *Script Editor* Component allows directly interaction with **sIBL_GUI** through scripting. It provides various code input acceleration mechanism like basic autocompletion, syntax highlighting, etc ... A status bar widget displays various informations about the currently edited document and allows language grammar change.

| Languages support is provided using custom grammars files but mechanism will be replaced by *Textmate* compliant system in the future.
| **sIBL_GUI** logging messages and commands execution results are displayed in the upper pane.
| By default the *Script Editor* Component is using tabs characters to indent lines, at the moment there are no exposed methods to use spaces instead.

Interactions:

-  **Language Combo Box**: Switches the current editor language.
-  **Drag’n’drop**:

   -  Drag’n’dropping an IBL Sets or Templates selection into the *Script Editor* Component will open their associated files.
   -  Drag’n’dropping any other type of file on **sIBL_GUI** will open it in the *Script Editor* Component.

Menus Bar:

File Menu:

+----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorFileMenu.jpg            |
+----------------------------------------------------------------------+

-  **New**: Adds a new editor.
-  **Load ...**: Loads user chosen file in a new editor.
-  **Source ...**: Loads user chosen file in a new editor and execute its content.
-  **Save**: Saves current editor content.
-  **Save As ...**: Saves current editor content as user chosen file.
-  **Save All**: Saves all editors content.
-  **Revert**: Reverts current editor content.
-  **Close**: Closes current editor.
-  **Close All**: Closes all editors.

Addons Functionalities:

-  **Add Project ...**: Adds user chosen Project.
-  **Remove Project**: Removes selected *Projects Explorer* Component Project.

Edit Menu:

+----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorEditMenu.jpg            |
+----------------------------------------------------------------------+

-  **Undo**: Undo current editor last changes.
-  **Redo**: Redo current editor reverted changes.
-  **Cut**: Cuts current editor selected content.
-  **Copy**: Copies current editor selected content.
-  **Paste**: Pastes clipboard content into current editor.
-  **Delete**: Deletes current editor selected content.
-  **Select All**: Selects all editor content.

Source Menu:

+------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorSourceMenu.jpg            |
+------------------------------------------------------------------------+

-  **Delete Line(s)**: Deletes current editor selected line(s).
-  **Duplicate Line(s)**: Duplicates current editor selected line(s).
-  **Move Up**: Move up current editor selected line(s).
-  **Move Down**: Move down current editor selected line(s).
-  **Indent Selection**: Indents current editor selected content.
-  **Unindent Selection**: Unindents current editor selected content.
-  **Convert Indentation To Tabs**: Converts current editor indentation to tabs.
-  **Convert Indentation To Spaces**: Converts current editor indentation to spaces.
-  **Remove Trailing Whitespaces**: Removes current editor trailing whitespaces.
-  **Toggle Comments**: Toggles comments on current editor selected content.

Navigate Menu:

+--------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorNavigateMenu.jpg            |
+--------------------------------------------------------------------------+

-  **Goto Line ...**: Scrolls current editor to user chosen line.

Search Menu:

+------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorSearchMenu.jpg            |
+------------------------------------------------------------------------+

-  **Search And Replace ...**: Launches the *Search And Replace* dialog described further below.
-  **Search In Files ...**: Launches the *Search In Files* dialog described further below.
-  **Search Next**: Searches next occurence of current editor selected text.
-  **Search Previous**: Searches previous occurence of current editor selected text.

Command Menu:

+-------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorCommandMenu.jpg            |
+-------------------------------------------------------------------------+

-  **Evaluate Selection**: Evaluates current editor selected text.
-  **Evaluate Script**: Evaluates current editor content.

Addons Functionalities:

-  **Send Selection To Server**: Sends current editor selected text to *TCP Client Ui* Component defined server.
-  **Send Current File To Server**: Sends current editor file to *TCP Client Ui* Component defined server.

View Menu:

+----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorViewMenu.jpg            |
+----------------------------------------------------------------------+

-  **Increase Font Size**: Increases current editor font size.
-  **Decrease Font Size**: Decreases current editor font size.
-  **Toggle Word Wrap**: Toggles word wrap on current editor.
-  **Toggle Whitespaces**: Toggles whitespaces display on current editor.
-  **Loop Through Editors**: Loops through editors.

Dialogs:

Search And Replace:

+------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorSearchAndReplace.jpg            |
+------------------------------------------------------------------------------+

-  **Search Combo Box**: Defines the search pattern.
-  **Replace With Combo Box**: Defines the replacement pattern.
-  **Case Sensitive Check Box**: Search will be performed case sensitively.
-  **Whole Word Check Box**: Search will be performed within words boundaries.
-  **Regular Expressions Check Box**: Search will be performed using Regular Expressions.
-  **Backward Search Check Box**: Search will be performed backward.
-  **Wrap Around Check Box**: Search will wrap around when reaching the editor end.
-  **Search Push Button**: Performs the search and highlight editor first matched occurence.
-  **Replace Push Button**: Performs the search and replace editor first matched occurence.
-  **Replace All Push Button**: Performs the search and replace all editor matched occurence.

Search In Files:

+---------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorSearchInFiles.jpg            |
+---------------------------------------------------------------------------+

-  **Search Combo Box**: Defines the search pattern.
-  **Replace With Combo Box**: Defines the replacement pattern.
-  **Where Line Edit**: Defines the search location (Clicking the magnifier brings a context menu).
-  **Case Sensitive Check Box**: Search will be performed case sensitively.
-  **Whole Word Check Box**: Search will be performed within words boundaries.
-  **Regular Expressions Check Box**: Search will be performed using Regular Expressions.
-  **Search Push Button**: Performs the search and highlight editor first matched occurence.

Magnifier Context menu:

+----------------------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorSearchInFilesLocationContextMenu.jpg            |
+----------------------------------------------------------------------------------------------+

-  **Add Directory ...**: Adds user chosen directory.
-  **Add File ...**: Adds user chosen file.
-  **Add Opened Files**: Adds opened files pattern.
-  **Add Include Filter**: Adds include glob files filter.
-  **Add Exclude Filter**: Adds exclude glob files filter.

Results View Context menu:

+--------------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ScriptEditorSearchInFilesContextMenu.jpg            |
+--------------------------------------------------------------------------------------+

-  **Replace All**: Replaces all search results with given replace pattern.
-  **Replace Selected**: Replaces selected search results with given replace pattern.
-  **Save All**: Saves all modified files.
-  **Save Selected**: Saves Selected modified files.

.. raw:: html

   <br/>

_`Core`
-------

.. raw:: html

   <br/>

.. _core.collectionsOutliner:

_`Collections Outliner` (core.collectionsOutliner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_CollectionsOutliner.jpg            |
+---------------------------------------------------------------------+

| The *Collections Outliner* Component is where the IBL Sets are organized into Collections for better management.
| There is a *Default Collection* where IBL Sets fall when they are added without a specific Collection container.

Interactions:

-  **Double clic**: Edits Collection name or comment.
-  **Right clic**: Displays a context menu described further.
-  **Drag’n’drop**:

   -  Drag’n’dropping an IBL Sets selection from the *Ibl Sets Outliner* Component to a Collections Outliner Component Collection changes given IBL Sets current Collection.
   -  Drag’n’dropping some IBL Sets files or directories from the Os will raise a message box asking confirmation for their addition into the database.

Columns Descriptions:

-  **Collections**: Collections names (Editable through double click).
-  **IBL Sets**: IBL Sets count per Collections.
-  **Comments**: Collections comments (Editable through double click).

Context menu:

+--------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_CollectionsOutlinerContextMenu.jpg            |
+--------------------------------------------------------------------------------+

-  **Add Content ...**: Adds a new Collection, then recursively adds chosen directory IBL Sets into the database, assigning them to the new Collection.
-  **Add Collection ...**: Adds a new Collection to the database.
-  **Remove Collection(s) ...**: Removes selected Collections from the database (Overall and Default Collections cannot be removed).

**Note**:

While adding a new Collection, a comment can be directly provided by using a comma separated name and comment.

+----------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_CollectionsOutlinerAddCollection.jpg            |
+----------------------------------------------------------------------------------+

.. raw:: html

   <br/>

_`Database` (core.database)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *Database* Component is the heart of **sIBL_GUI** data storage, it provides the database manipulation, read, write, migration and rotating backup methods.

.. raw:: html

   <br/>

.. _core.iblSetsOutliner:

_`Ibl Sets Outliner` (core.iblSetsOutliner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_IblSetsOutliner.jpg            |
+-----------------------------------------------------------------+

The *Ibl Sets Outliner* Component is the central Component where IBL Sets are viewed and chosen for export. The Component is tracking the IBL Sets files on the disk and reload them automatically when modified.

IBL Sets can be viewed using different views depending the user needs:

Columns View:

+----------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_IblSetsOutlinerColumnsView.jpg            |
+----------------------------------------------------------------------------+

Details View:

+----------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_IblSetsOutlinerDetailsView.jpg            |
+----------------------------------------------------------------------------+

Columns Descriptions:

-  **Ibl Set**: IBL Sets titles (Editable through double click).
-  **Author**: IBL Sets authors.
-  **Shot Location**: IBL Sets shot locations.
-  **Latitude**: IBL Sets shot locations latitudes.
-  **Longitude**: IBL Sets shot locations Longitudes.
-  **Shot Date**: IBL Sets shot days.
-  **Shot Time**: IBL Sets shot times.
-  **Comment**: IBL Sets comments.

Interactions:

-  **Double clic**: Opens the current Ibl Set in the *Inspector* Component.
-  **Right clic**: Displays a context menu described further.
-  **Drag’n’drop**:

   -  Drag’n’dropping an IBL Sets selection from the *Ibl Sets Outliner* Component to a *Collections Outliner* Component Collection change the selected sets Collection.
   -  Drag’n’dropping some IBL Sets files or directories from the Os will raise a message box asking confirmation for their addition into the database.

-  **Hovering**: Hovering an Ibl Set raises a popup with informations about the focused Ibl Set.
-  **Thumbnails View Push Button**: Switch the current view to *Thumbnails View*. 
-  **Columns View Push Button**: Switch the current view to *Columns View*.
-  **Details View Push Button**: Switch the current view to *Details View*.
-  **Case Sensitive Matching Push Button**: Search will be performed case sensitively if the button is checked.
-  **Search Database Line Edit**: It allows IBL Sets filtering. The string entered will be matched in the selected database field. Regular expressions are accepted. An autocompletion list will be raised once characters starts being typed. Clicking the magnifier glass raises a context menu pictured below allowing to choose the current database field.
-  **Thumbnails Size Horizontal Slider**: Adjusts IBL Sets icons size.

Context menu:

+----------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_IblSetsOutlinerContextMenu.jpg            |
+----------------------------------------------------------------------------+

-  **Add Content ...**: Recursively adds chosen directory IBL Sets into the database assigning them to the selected *Collections Outliner* Component Collection or the Default Collection if none is selected.
-  **Add Ibl Set ...**: Adds the selected Ibl Set file into the database assigning it to the selected *Collections Outliner* Component Collection or the Default Collection if none is selected.
-  **Remove Ibl Set(s) ...**: Removes selected IBL Sets from the database.
-  **Update Ibl Set(s) Location(s) ...**: Updates selected IBL Sets files paths.

Addons Functionalities:

-  **Edit In sIBLedit ...**: Sends selected IBL Sets to **sIBLedit**.
-  **Open Ibl Set(s) Location(s) ...**: Opens selected IBL Sets directories.
-  **Edit Ibl Set(s) File(s) ...**: Edits selected IBL Sets in the *Script Editor* Component or custom user defined text editor.
-  **View Background Image ...**: Views selected IBL Sets background images in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.
-  **View Lighting Image ...**: Views selected Ibls Set lighting images in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.
-  **View Reflection Image ...**: Views selected Ibls Set reflection images in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.
-  **View Plate(s) ...**: Views selected Ibls Set plates images in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.

Search widget context menu:

+----------------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_IblSetsOutlinerSearchWidgetContextMenu.jpg            |
+----------------------------------------------------------------------------------------+

.. raw:: html

   <br/>

.. _core.inspector:

_`Inspector` (core.inspector)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_Inspector.jpg            |
+-----------------------------------------------------------+

The *Inspector* Component allows Ibl Set inspection.

Interactions:

-  **Right clic**: Displays a context menu described further.
-  **Hovering**: Hovering Inspector Ibl Set raises a popup with informations about the Inspector Ibl Set.
-  **Previous Ibl Set Push Button**: Navigates to previous Ibl Set in the current selected Collection.
-  **Next Ibl Set Push Button**: Navigates to next Ibl Set in the current selected Collection.
-  **Previous Plate Push Button**: Navigates to previous Inspector Ibl Set plate.
-  **Next Plate Push Button**: Navigates to next Inspector Ibl Set plate.

Addons Functionalities:

-  **View Background Image Push Button**: Views Inspector Ibl Set background image in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.
-  **View Lighting Image Push Button**: Views Inspector Ibl Set lighting image in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.
-  **View Reflection Image Push Button**: Views Inspector Ibl Set reflection image in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.
-  **View Plate(s) Push Button**: Views Inspector Ibl Set plates images in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.

Context menu:

+----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_InspectorContextMenu.jpg            |
+----------------------------------------------------------------------+

Addons Functionalities:

-  **Edit In sIBLedit ...**: Sends Inspector Ibl Set to **sIBLedit**.
-  **Open Ibl Set Location ...**: Opens Inspector IBL Sets directory.
-  **Edit Ibl Set File ...**: Edits  Inspector Ibl Set in the *Script Editor* Component or custom user defined text editor.
-  **View Background Image ...**: Views the Inspector Ibl Set background image in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.
-  **View Lighting Image ...**: Views the Inspector Ibl Set lighting image in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.
-  **View Reflection Image ...**: Views the Inspector Ibl Set reflection image in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.
-  **View Plate(s) ...**: Views the Ibl Set Inspector plates images in either the Internal Images Previewer or the application defined in the *Preview* Component preferences.

.. raw:: html

   <br/>

.. _core.templatesOutliner:

_`Templates Outliner` (core.templatesOutliner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TemplatesOutliner.jpg            |
+-------------------------------------------------------------------+

The *Templates Outliner* Component is where Templates are organized and reviewed. Selected Templates details are displayed in the bottom *Templates Informations* widget. The Component is tracking the Templates files on the disk and reload them automatically when modified.

Templates are sorted into 2 main categories:

-  **Factory** (Templates from **sIBL_GUI** installation directory).
-  **User** (Templates not from **sIBL_GUI** installation directory).

In those categories, Templates are sorted by 3d packages.

Columns Descriptions:

-  **Templates**: Templates names.
-  **Release**: Templates versions numbers.
-  **Software Version**: 3d packages compatible version.

Interactions:

-  **Right clic**: Displays a context menu described further.
-  **Drag’n’drop**:

   -  Drag’n’dropping some Templates files or directories from the Os will raise a message box asking confirmation for their addition into the database.

Context menu:

+------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TemplatesOutlinerContextMenu.jpg            |
+------------------------------------------------------------------------------+

-  **Add Template ...**: Adds the selected Templates file to the database.
-  **Remove Templates(s) ...**: Removes selected Templates from the database.
-  **Import Default Templates**: **sIBL_GUI** will scan for Templates into it’s installation directory and the user preferences directories.
-  **Filter Templates Versions**: **sIBL_GUI** will filter the Templates keeping the highest version of multiple same Templates.
-  **Display Help File(s) ...**: Displays Templates associated help files.

Addons Functionalities:

-  **Open Templates(s) Location(s) ...**: Opens selected Templates directories.
-  **Edit Template(s) File(s) ...**: Edits selected Templates in the *Script Editor* Component or custom user defined text editor.

.. raw:: html

   <br/>

Addons
------

.. raw:: html

   <br/>

.. _addons.about:

_`About sIBL_GUI` (addons.about)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_About.jpg            |
+-------------------------------------------------------+

The *About* Component displays the *About* window.

.. raw:: html

   <br/>

.. _addons.databaseOperations:

_`Database Operations` (addons.databaseOperations)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_DatabaseOperations.jpg            |
+--------------------------------------------------------------------+

The *Database Operations* Component allows the user to launch some database maintenance operations.

Interactions:

-  **Synchronize Database Push Button**: Forces database synchronization by reparsing all registered files.
-  **Remove Invalid Data Push Button**: Removes invalid database entries ( Missing files, etc... ).

.. raw:: html

   <br/>

.. _addons.gpsMap:

_`Gps Map` (addons.gpsMap)
^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_GpsMap.jpg            |
+--------------------------------------------------------+

The *Gps Map* Component is embedding a Microsoft Bing Map into **sIBL_GUI**: Selecting some IBL Sets (Ibl Sets with GEO coordinates) in the *Ibl Sets Outliner* Component will display their markers onto the Gps Map.

Interactions:

-  **Zoom In Push Button**: Zooms into the Gps Map.
-  **Zoom Out Push Button**: Zooms out of the Gps Map.
-  **Map Type Combo Box**: Switches the Gps Map style.

   -  Auto: This map type automatically chooses between Aerial and Road mode.
   -  Aerial: This map type overlays satellite imagery onto the map and highlights roads and major landmarks to be easily identifiable amongst the satellite images.
   -  Road: This map type displays vector imagery of roads, buildings, and geography.

.. raw:: html

   <br/>

.. _addons.iblSetsScanner:

_`Ibl Sets Scanner` (addons.iblSetsScanner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *Ibl Sets Scanner* Component is a file scanning Component that will automatically register any new Ibl Sets to the Default Collection whenever it founds one in an already existing IBL Sets parent directory. This behavior can be stopped by deactivating the Component.

.. raw:: html

   <br/>

.. _addons.imagesCachesOperations:

_`Images Caches Operations` (addons.imagesCachesOperations)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ImagesCachesOperations.jpg            |
+------------------------------------------------------------------------+

The *Images Caches Operations* Component allows the user to manipulate **sIBL_GUI** images caches.

Interactions:

-  **Output Images Caches Metrics Push Button**: Outputs various images caches metrics: Images count, paths, sizes.
-  **Clear Images Caches Push Button**: Clears the various images caches, the Python interpreter may not release the memory immediately.

.. raw:: html

   <br/>

.. _addons.loaderScript:

_`Loader Script` (addons.loaderScript)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_LoaderScript.jpg            |
+--------------------------------------------------------------+

The *Loader Script* Component is providing the bridge between **sIBL_GUI** and the 3d packages. It parses the selected Ibl Set, extracts data from it, and feeds the selected Template with those data resulting in a loader script that can be executed by the 3d package.

Interactions:

-  **Output Loader Script Push Button**: Outputs the loader script to the output directory.
-  **Send To Software Push Button**: Sends a command to the 3d package that will execute the loader script.
-  **Convert To Posix Paths Check Box (Windows Only)**: Windows paths will be converted to Unix paths, drive letters will be trimmed.

Addons Functionalities:

-  **Open Output Folder Push Button**: Opens the output directory.

.. raw:: html

   <br/>

.. _addons.loaderScriptOptions:

_`Loader Script Options` (addons.loaderScriptOptions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_LoaderScriptOptions.jpg            |
+---------------------------------------------------------------------+

The *Loader Script Options* Component allows the user to tweak the way the loader script will behave in the 3d package. Templates attributes are exposed in 2 pages where they can be adjusted:

-  **Common Attributes**: Common Template attributes (Refer to the current Template help file for details about an attribute).
-  **Additional Attributes**: Additional Template attributes (Refer to the current Template help file for details about an attribute).

Templates settings are stored per version and restored each time one is selected in **sIBL_GUI** preferences directory.

.. raw:: html

   <br/>

.. _addons.locationsBrowser:

_`Locations Browser` (addons.locationsBrowser)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_LocationsBrowser.jpg            |
+------------------------------------------------------------------+

The *Locations Browser* Component provides browsing capability to **sIBL_GUI**, adding directory browsing at various entry points in **sIBL_GUI** Ui. The browsing is done either by the Os default file browser or an user defined file browser.

Default Supported File Browsers:

-  **Windows**:

   -  Explorer

-  **Mac Os X**:

   -  Finder

-  **Linux**:

   -  Nautilus
   -  Dolphin
   -  Konqueror
   -  Thunar

Interactions:

-  **Custom File Browser Path Line Edit**: User defined file browser executable path.

.. raw:: html

   <br/>

.. _addons.loggingNotifier:

_`Logging Notifier` (addons.loggingNotifier)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *Logging Notifier* Component displays logging messages in the status bar.

.. raw:: html

   <br/>

.. _addons.onlineUpdater:

_`Online Updater` (addons.onlineUpdater)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_RemoteUpdater.jpg            |
+---------------------------------------------------------------+

The *Online Updater* Component maintains **sIBL_GUI** and it’s Templates up to date by checking HDRLabs repository for new releases on startup or user request.

Interactions:

-  **Get sIBL_GUI Push Button**: Starts **sIBL_GUI** download.
-  **Get Lastest Templates**: Starts selected Templates download.
-  **Open Repository**: Opens HDRLabs repository.

When a download starts the *Download Manager* window will open:

+-----------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_DownloadManager.jpg            |
+-----------------------------------------------------------------+

The *Online Updater* Component is configurable in the *Preferences Manager* Component:

+---------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_OnlineUpdater.jpg            |
+---------------------------------------------------------------+

Interactions:

-  **Check For New Releases Push Button**: Checks for new releases on HDRLabs repository.
-  **Check For New Releases On Startup Check Box**: **sIBL_GUI** will check for new releases on startup.
-  **Ignore Non Existing Templates Check Box**: **sIBL_GUI** will ignore non existing Template when checking for new releases, meaning that if a Template for a new 3d package is available, it will be ignored.

.. raw:: html

   <br/>

.. _addons.projectsExplorer:

_`Projects Explorer` (addons.projectsExplorer)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ProjectsExplorer.jpg            |
+------------------------------------------------------------------+

The *Projects Explorer* Component displays **sIBL_GUI** opened files and projects. It offers a global overview on what is being edited in the *Script Editor* Component.

Interactions:

-  **Right clic**: Displays a context menu described further.

Context menu:

+-----------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ProjectsExplorerContextMenu.jpg            |
+-----------------------------------------------------------------------------+

-  **Add Project ...**: Adds a new Project.
-  **Remove Project**: Removes selected Project.
-  **Add New File ...**: Creates a new file under selected directory or next to selected file.
-  **Add New Directory ...**: Creates a new directory under selected directory or next to selected file.
-  **Rename ...**: Renames selected directory or file.
-  **Delete ...**: Deletes selected directory or file.
-  **Find In Files ...**: Search and replace in selected directory or file.
-  **Output Selected Path**: Print selected directory or file path in the *Script Editor*.

.. raw:: html

   <br/>

.. _addons.preview:

_`Preview` (addons.preview)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_Preview.jpg            |
+---------------------------------------------------------+

The *Preview* Component provides image viewing capability to **sIBL_GUI** through the use of the Internal Images Previewer or the application defined in the *Preview* Component preferences.

Interactions:

-  **Custom Previewer Path Line Edit**: User defined Image Viewer / Editor executable path.

The Internal Images Previewer window provides basic informations about the current Image:

+-----------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ImagesPreviewer.jpg            |
+-----------------------------------------------------------------+

Interactions:

-  **Clic’n’dragging**: Pans into the Image.
-  **Mouse Scrool Wheel**: Zooms into the Image.
-  **Shortcut Key “+”**: Zooms into the Image.
-  **Shortcut Key “-”**: Zooms out of the Image.
-  **Previous Image Push Button**: Navigate to the previous image.
-  **Next Image Push Button**: Navigate to the next image.
-  **Zoom In Push Button**: Zooms into the Image.
-  **Zoom Fit Push Button**: Zooms fit the Image.
-  **Zoom Out Push Button**: Zooms out of the Image.

.. raw:: html

   <br/>

.. _addons.rawEditingUtilities:

_`Raw Editing Utilities` (addons.rawEditingUtilities)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_RawEditingUtilities.jpg            |
+---------------------------------------------------------------------+

The *Raw Editing Utilities* Component provides text editing capability to **sIBL_GUI**, adding text edition at various entry points in **sIBL_GUI** Ui. The text edition is done either by the *Script Editor* Component or an user defined text editor.

Interactions:

-  **Custom Text Editor Path Line Edit**: User defined Text Editor executable path.

.. raw:: html

   <br/>

.. _addons.rewiringTool:

_`Rewiring Tool` (addons.rewiringTool)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_RewiringTool.jpg            |
+--------------------------------------------------------------+

The *Rewiring Tool* Component is available by right clicking the main toolbar. This Component allows rewiring / remapping of an Ibl Set file to another file of that set or an arbitrary image. This widget is powerful because it’s possible to dynamically generate IBL Sets and arbitrary loads whatever HDR you want and still benefit from **sIBL_GUI** one click lighting setup.

Interactions:

-  **Combo Boxes**: The current image will be remapped to the chosen entry.
-  **Path Line Edits**: The current image will be remapped to the chosen custom image.

.. raw:: html

   <br/>

.. _addons.searchDatabase:

_`Search Database` (addons.searchDatabase)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_SearchDatabaseSearchInTagsCloud.jpg            | ..  image:: ../pictures/sIBL_GUI_SearchDatabaseSearchInShotTime.jpg            |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------+

The *Search Database* Component enables search in the database. There are 2 pages providing different search options:

-  **Search In Tags Cloud**: Searches in database Ibl Sets comments tags cloud generated.
-  **Search In Shot Time**: Searches in shot time range.

Interactions:

-  **Search Database Line Edit**: The string entered will be matched in the selected database field. Regular expressions are accepted. An autocompletion list will raise once characters starts being typed.
-  **Case Insensitive Matching Check Box**: The string matching is done case insensitively.

Search In Shot Time:

-  **From Time Edit**: Time range search start.
-  **To Time Edit**: Time range search end.

.. raw:: html

   <br/>

.. _addons.sIBLeditUtilities:

_`sIBLedit Utilities` (addons.sIBLeditUtilities)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_sIBLeditUtilities.jpg            |
+-------------------------------------------------------------------+

The *sIBLedit Utilities* Component provides a bridge between **sIBL_GUI** and **sIBLedit**.

Interactions:

-  **sIBLedit Executable Path Line Edit**: **sIBLedit** executable path.

.. raw:: html

   <br/>

.. _addons.tcpClientUi:

_`TCP Client Ui` (addons.tcpClientUi)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TcpClientUi.jpg            |
+-------------------------------------------------------------+

The *TCP Client Ui* Component allows **sIBL_GUI** to connect to TCP servers. As a functionality test it's possible to connect **sIBL_GUI** to itself: ensure that both the *TCP Client Ui* and *TCP Server Ui* Components use the same address and port.

Interactions:

-  **Address Line Edit**: TCP server address.
-  **Port Spin Box**: TCP server port.
-  **File Command Line Edit**: File command the TCP server uses to execute a script.
-  **Connection End Line Edit**: TCP server connection end token.

.. raw:: html

   <br/>

.. _addons.tcpServerUi:

_`TCP Server Ui` (addons.tcpServerUi)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TcpServerUi.jpg            |
+-------------------------------------------------------------+

With the *TCP Server Ui* Component **sIBL_GUI** can be used as a TCP server and remote controlled.

Interactions:

-  **Port Spin Box**: TCP server port.
-  **Autostart TCP Server Check Box**: Starts the TCP server on **sIBL_GUI** startup.
-  **Start TCP Server Push Button**: Starts the TCP server.
-  **Stop TCP Server Push Button**: Stops the TCP server.

.. raw:: html

   <br/>

.. _addons.traceUi:

_`Trace Ui` (addons.traceUi)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TraceUi.jpg            |
+---------------------------------------------------------+

The *Trace Ui* Component is a development oriented Component allowing to trace execution of user defined modules. Tracing some modules doing intensive background work can stall **sIBL_GUI** and make it unresponsive.

Interactions:

-  **Objects Trace Filter Line Edit**: Filters objects to be traced using a regex pattern.

Context menu:

+--------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TraceUiContextMenu.jpg            |
+--------------------------------------------------------------------+

-  **Trace Module(s)**: Traces selected modules.
-  **Untrace Module(s)**: Untraces selected modules.

.. raw:: html

   <br/>

