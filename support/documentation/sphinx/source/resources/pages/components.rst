_`Components`
=============

*sIBL_GUI* has currently 2 categories of components:

-  **Default Component** (Components without an associated Ui Widget).
-  **Ui Component** (Components with an associated Ui Widget).

Those 2 types are split into 3 main families:

-  **Core** (Factory required components, not deactivable and not removable)
-  **Addons** (Factory optional components, deactivable and removable)
-  **User** (User optional components, deactivable and removable)

_`Core`
-------

.. _core.collectionsOutliner:

_`Collections Outliner` (core.collectionsOutliner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_CollectionsOutliner.jpg            |
+---------------------------------------------------------------------+

| The *Collections Outliner* component is where the Ibl Sets are organized into Collections for better management.
| There is a *Default Collection* where Ibl Sets fall when they are added without a specific Collection container.

Interactions:

-  **Double clic**: Edits Collection name or comment.
-  **Right clic**: Displays a context menu described further.
-  **Drag’n’drop**:

   -  Drag’n’dropping an Ibl Sets selection from the *Database Browser* component to a Collections Outliner component Collection change sets current Collection.
   -  Drag’n’dropping some Ibl Sets files or directories from the Os will raise a message box asking confirmation for their addition into the database.

Columns Descriptions:

-  **Collections**: Collections names (Editable through double click).
-  **Sets**: Sets count per Collections.
-  **Comments**: Collections comments (Editable through double click).

Context Menu:

+--------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_CollectionsOutlinerContextMenu.jpg            |
+--------------------------------------------------------------------------------+

-  **Add Content …**: Adds a new Collection, then recursively adds chosen directory Ibl Sets into the database, assigning them to the new Collection.
-  **Add Collection …**: Adds a new Collection to the database.
-  **Remove Collection(s) ...**: Removes selected Collections from the database (Overall and Default Collections cannot be removed).

**Note**:

While adding a new Collection, a comment can be directly provided by using a comma separated name and comment.

+----------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_CollectionsOutlinerAddCollection.jpg            |
+----------------------------------------------------------------------------------+



.. _core.componentsManagerUi:

_`Components Manager` (core.componentsManagerUi)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ComponentsManager.jpg            |
+-------------------------------------------------------------------+

The *Components Manager* component allows *sIBL_GUI* addons and user components activation / deactivation (Core components are required and not deactivable). Selected components details are displayed in the bottom *Components Informations* widget.

Interactions:

-  **Right clic**: Displays a context menu described further.

Columns Descriptions:

-  **Components**: Components names (Components are sorted by families).
-  **Activated**: Components activations status.
-  **Categorie**: Components categories (Default or Ui).
-  **Rank**: Components ranks (Components with a low rank will have a high instantiation priority).

Context Menu:

+------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ComponentsManagerContextMenu.jpg            |
+------------------------------------------------------------------------------+

-  **Activate Component(s)**: Activates selected Component(s).
-  **Dectivate Component(s)**: Deactivates selected Component(s).
-  **Reload Component(s)**: Reloads selected Component(s) (Deactivates the component, reloads component code, activates back the component).

Addons Functionalities:

-  **Open Component(s) Location(s) ...**: Opens Component(s) directory(s).



.. _core.databaseBrowser:

_`Database Browser` (core.databaseBrowser)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_DatabaseBrowser.jpg            |
+-----------------------------------------------------------------+

The *Database Browser* component is the central component where Ibl Sets are viewed and chosen for export. The component is tracking the Ibl Sets files on the disk and reload them automatically when modified.

Interactions:

-  **Double clic**: Edits selected Ibl Set title.
-  **Right clic**: Displays a context menu described further.
-  **Drag’n’drop**:

   -  Drag’n’dropping an Ibl Sets selection from the *Database Browser* component to a *Collections Outliner* component Collection change the selected sets Collection.
   -  Drag’n’dropping some Ibl Sets files or directories from the Os will raise a message box asking confirmation for their addition into the database.

-  **Hovering**: Hovering an Ibl Set raises a popup with informations about the focused Ibl Set.
-  **Thumbnails Size Horizontal Slider**: Adjusts Ibl Sets icons size.

Context Menu:

+----------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_DatabaseBrowserContextMenu.jpg            |
+----------------------------------------------------------------------------+

-  **Add Content …**: Recursively adds chosen directory Ibl Sets into the database assigning them to the selected *Collections Outliner* component Collection or the Default Collection if none is selected.
-  **Add Ibl Set …**: Adds the selected Ibl Set file into the database assigning it to the selected *Collections Outliner* component Collection or the Default Collection if none is selected.
-  **Remove Ibl Set(s) ...**: Removes selected Ibl Sets from the database.
-  **Update Ibl Set(s) Location(s) ...**: Updates selected Ibl Sets files paths.

Addons Functionalities:

-  **Edit In sIBLedit …**: Sends selected Ibl Sets to *sIBLedit*.
-  **Edit In Text Editor …**: Edits selected Ibl Sets with system or custom user defined text editor.
-  **Open Ibl Set(s) Location(s) ...**: Opens selected Ibl Sets directories.
-  **View Background Image …**: Views selected Ibl Sets background images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Lighting Image …**: Views selected Ibls Set lighting images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Reflection Image …**: Views selected Ibls Set reflection images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Plate(s) …**: Views selected Ibls Set plates images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.



_`Db` (core.db)
^^^^^^^^^^^^^^^

The *Db* component is the heart of *sIBL_GUI* datas storage, it provides the database manipulation, read, write and rotating backup methods.



.. _core.inspector:

_`Inspector` (core.inspector)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_Inspector.jpg            |
+-----------------------------------------------------------+

The *Inspector* component allows Ibl Set inspection.

Interactions:

-  **Right clic**: Displays a context menu described further.
-  **Hovering**: Hovering Inspector Ibl Set raises a popup with informations about the Inspector Ibl Set.
-  **Previous Ibl Set Push Button**: Navigates to previous Ibl Set in the current selected Collection.
-  **Next Ibl Set Push Button**: Navigates to next Ibl Set in the current selected Collection.
-  **Previous Plate Push Button**: Navigates to previous Inspector Ibl Set plate.
-  **Next Plate Push Button**: Navigates to next Inspector Ibl Set plate.

Addons Functionalities:

-  **View Background Image Push Button**: Views Inspector Ibl Set background image in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Lighting Image Push Button**: Views Inspector Ibl Set lighting image in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Reflection Image Push Button**: Views Inspector Ibl Set reflection image in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Plate(s) Push Button**: Views Inspector Ibl Set plates images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.

Context Menu:

+----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_InspectorContextMenu.jpg            |
+----------------------------------------------------------------------+

Addons Functionalities:

-  **Edit In sIBLedit …**: Sends Inspector Ibl Set to *sIBLedit*.
-  **Edit In Text Editor …**: Edits Inspector Ibl Set with system or custom user defined text editor.
-  **Open Ibl Set(s) Location(s) ...**: Opens Inspector Ibl Sets directory.
-  **View Background Image …**: Views the Inspector Ibl Set background image in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Lighting Image …**: Views the Inspector Ibl Set lighting image in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Reflection Image …**: Views the Inspector Ibl Set reflection image in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Plate(s) …**: Views the Ibl Set Inspector plates images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.



.. _core.preferencesManager:

_`Preferences Manager` (core.preferencesManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_PreferencesManager.jpg            |
+--------------------------------------------------------------------+

The *Preferences Manager* component is used to configure *sIBL_GUI* behavior. There are 2 pages where settings can be changed:

-  **General**: Overall *sIBL_GUI* settings.
-  **Others**: Components settings.

General Page:

-  **Logging Formatter**: Adjusts *sIBL_GUI* logging formatter:

   -  Default: Default logging formatter: **Logging Level: Message**.
   -  Extended: Extended logging formatter: **Time - Thread - Logging Level: Message**.
   -  Standard: Simple standard logging formatter: **Message**.

-  **Verbose Level**: Adjusts *sIBL_GUI* verbose level between different modes (Debug being the most verbosing, Critical the less):

   -  Debug
   -  Info
   -  Warning
   -  Error
   -  Critical

-  **Restore Geometry On Layout Change**: *sIBL_GUI* window size and position will be restored when switching layouts.

Others Page:

Those settings are components dependent and will be described per related component.



.. _core.templatesOutliner:

_`Templates Outliner` (core.templatesOutliner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TemplatesOutliner.jpg            |
+-------------------------------------------------------------------+

The *Templates Outliner* component is where Templates are organized and reviewed. Selected Templates details are displayed in the bottom *Templates Informations* widget. The component is tracking the Templates files on the disk and reload them automatically when modified.

Templates are sorted into 2 main categories:

-  **Factory** (Templates from *sIBL_GUI* installation directory).
-  **User** (Templates not from *sIBL_GUI* installation directory).

In those categories, Templates are sorted by 3d packages.

Columns Descriptions:

-  **Templates**: Templates names.
-  **Release**: Templates versions numbers.
-  **Software Version**: 3d packages compatible version.

Interactions:

-  **Right clic**: Displays a context menu described further.
-  **Drag’n’drop**:

   -  Drag’n’dropping some Templates files or directories from the Os will raise a message box asking confirmation for their addition into the database.

Context Menu:

+------------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TemplatesOutlinerContextMenu.jpg            |
+------------------------------------------------------------------------------+

-  **Add Template …**: Adds the selected Templates file to the database.
-  **Remove Templates(s) ...**: Removes selected Templates from the database.
-  **Import Default Templates**: *sIBL_GUI* will scan for Templates into it’s installation directory and the user preferences directories.
-  **Filter Templates Versions**: *sIBL_GUI* will filter the Templates keeping the highest version of multiple same Templates.
-  **Display Help File(s) ...**: Displays Templates associated help files.

Addons Functionalities:

-  **Edit In Text Editor …**: Edits selected Templates with system or custom user defined text editor.
-  **Open Templates(s) Location(s) ...**: Opens selected Templates directories.

Addons
------

.. _addons.about:

_`About sIBL_GUI` (addons.about)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_About.jpg            |
+-------------------------------------------------------+

The *About* component displays the *About* window.



.. _addons.databaseOperations:

_`Database Operations` (addons.databaseOperations)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_DatabaseOperations.jpg            |
+--------------------------------------------------------------------+

The *Database Operations* component allows the user to launch some database maintenance operations.

Interactions:

-  **Synchronize Database Push Button**: Forces database synchronization by reparsing all registered files.



.. _addons.gpsMap:

_`Gps Map` (addons.gpsMap)
^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_GpsMap.jpg            |
+--------------------------------------------------------+

The *Gps Map* component is embedding a Microsoft Bing Map into *sIBL_GUI*: Selecting some Ibl Sets (Sets with GEO coordinates) in the *Database Browser* component will display their markers onto the Gps Map.

Interactions:

-  **Zoom In Push Button**: Zooms into the Gps Map.
-  **Zoom Out Push Button**: Zooms out of the Gps Map.
-  **Map Type Combo Box**: Switches the Gps Map style.

   -  Auto: This map type automatically chooses between Aerial and Road mode.
   -  Aerial: This map type overlays satellite imagery onto the map and highlights roads and major landmarks to be easily identifiable amongst the satellite images.
   -  Road: This map type displays vector imagery of roads, buildings, and geography.



.. _addons.loaderScript:

_`Loader Script` (addons.loaderScript)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_LoaderScript.jpg            |
+--------------------------------------------------------------+

The *Loader Script* component is providing the bridge between *sIBL_GUI* and the 3d packages. It parses the selected Ibl Set, extracts datas from it, and feeds the selected Template with those datas resulting in a loader script that can be executed by the 3d package.

Interactions:

-  **Output Loader Script Push Button**: Outputs the loader script to the output directory.
-  **Send To Software Push Button**: Sends a command to the 3d package that will execute the loader script.
-  **Software Port Spin Box**: Communication port of the host running the target 3d package.
-  **Ip Adress Line Edit**: Ip address of the host running the target 3d package.
-  **Convert To Posix Paths Check Box (Windows Only)**: Windows paths will be converted to Unix paths, drive letters will be trimmed.

Addons Functionalities:

-  **Open Output Folder Push Button**: Opens the output directory.



.. _addons.loaderScriptOptions:

_`Loader Script Options` (addons.loaderScriptOptions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_LoaderScriptOptions.jpg            |
+---------------------------------------------------------------------+

The *Loader Script Options* component allows the user to tweak the way the loader script will behave in the 3d package. Templates attributes are exposed in 2 pages where they can be adjusted:

-  **Common Attributes**: Common Template attributes (Refer to the current Template help file for details about an attribute).
-  **Additional Attributes**: Additional Template attributes (Refer to the current Template help file for details about an attribute).



.. _addons.locationsBrowser:

_`Locations Browser` (addons.locationsBrowser)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_LocationsBrowser.jpg            |
+------------------------------------------------------------------+

The *Locations Browser* component provides browsing capability to *sIBL_GUI*, adding directory browsing at various entry points in *sIBL_GUI* Ui. The browsing is done either by the Os default file browser or an user defined file browser.

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



.. _addons.loggingNotifier:

_`Logging Notifier` (addons.loggingNotifier)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *Logging Notifier* component displays logging messages in the status bar.



.. _addons.loggingWindow:

_`Logging Window` (addons.loggingWindow)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_LoggingWindow.jpg            |
+---------------------------------------------------------------+

The *Logging Window* component is available by right clicking the main toolbar and displays *sIBL_GUI* verbose messages.



.. _addons.onlineUpdater:

_`Online Updater` (addons.onlineUpdater)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_OnlineUpdater.jpg            |
+---------------------------------------------------------------+

The *Online Updater* component maintains *sIBL_GUI* and it’s Templates up to date by checking HDRLabs repository for new releases on startup or user request.

Interactions:

-  **Get sIBL_GUI Push Button**: Starts *sIBL_GUI* download.
-  **Get Lastest Templates**: Starts selected Templates download.
-  **Open Repository**: Opens HDRLabs repository.

When a download starts the *Download Manager* window will open:

+-----------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_DownloadManager.jpg            |
+-----------------------------------------------------------------+

The *Online Updater* component is configurable in the *Preferences Manager* component:

+--------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_OnlineUpdaterPreferences.jpg            |
+--------------------------------------------------------------------------+

Interactions:

-  **Check For New Releases Push Button**: Checks for new releases on HDRLabs repository.
-  **Check For New Releases On Startup Check Box**: *sIBL_GUI* will check for new releases on startup.
-  **Ignore Non Existing Templates Check Box**: *sIBL_GUI* will ignore non existing Template when checking for new releases, meaning that if a Template for a new 3d package is available, it will be ignored.



.. _addons.preview:

_`Preview` (addons.preview)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_Preview.jpg            |
+---------------------------------------------------------+

The *Preview* component provides image viewing capability to *sIBL_GUI* through the use of the Internal Images Previewer or the application defined in the *Preview* component preferences.

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



.. _addons.rawEditingUtilities:

_`Raw Editing Utilities` (addons.rawEditingUtilities)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_RawEditingUtilities.jpg            |
+---------------------------------------------------------------------+

The *Raw Editing Utilities* component provides text editing capability to *sIBL_GUI*, adding text edition at various entry points in *sIBL_GUI* Ui. The text edition is done either by the Os default text editor or an user defined text editor.

Default Supported Text Editors:

-  **Windows**:

   -  Notepad

-  **Mac Os X**:

   -  TextEdit

-  **Linux**:

   -  Gedit
   -  Kwrite
   -  Nedit
   -  Mousepad

Interactions:

-  **Custom Text Editor Path Line Edit**: User defined Text Editor executable path.



.. _addons.rewiringTool:

_`Rewiring Tool` (addons.rewiringTool)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_RewiringTool.jpg            |
+--------------------------------------------------------------+

The *Rewiring Tool* component is available by right clicking the main toolbar. This component allows rewiring / remapping of an Ibl Set file to another file of that set or an arbitrary image. This widget is powerful because it’s possible to dynamically generate IBL sets and arbitrary load whatever HDR you want and still benefit from *sIBL_GUI* one click lighting setup.

Interactions:

-  **Combo Boxes**: The current image will be remapped to the chosen entry.
-  **Path Line Edits**: The current image will be remapped to the chosen custom image.



.. _addons.searchDatabase:

_`Search Database` (addons.searchDatabase)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------------------------------------------------+------------------------------------------------------------------+------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_SearchDatabase_A.jpg            | ..  image:: ../pictures/sIBL_GUI_SearchDatabase_B.jpg            | ..  image:: ../pictures/sIBL_GUI_SearchDatabase_C.jpg            |
+------------------------------------------------------------------+------------------------------------------------------------------+------------------------------------------------------------------+

The *Search Database* component enables search in the database. There are 2 pages providing different search options:

-  **Search In Fields**: Searches in database fields.
-  **Search In Shot Time**: Searches in shot time range.

Interactions:

Search In Fields Page:

-  **Search Database Combo Box**: Field against which the search will be executed. There are 5 different fields types available:

   -  In Names
   -  In Authors
   -  In Links
   -  In Locations
   -  In Comments
   -  In Tags Cloud

-  **Search Database Line Edit**: The string entered will be matched in the selected database field. Regular expressions are accepted. An autocompletion list will raise once characters starts being typed.
-  **Case Insensitive Matching Check Box**: The string matching is done case insensitively.

Search In Shot Time:

-  **From Time Edit**: Time range search start.
-  **To Time Edit**: Time range search end.



.. _addons.setsScanner:

_`Sets Scanner` (addons.setsScanner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *Sets Scanner* component is a file scanning component that will automatically register any new sets to the Default Collection whenever it founds one in an already existing Ibl Sets parent directory. This behavior can be stopped by deactivating the component.



.. _addons.sIBLeditUtilities:

_`sIBLedit Utilities` (addons.sIBLeditUtilities)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_sIBLeditUtilities.jpg            |
+-------------------------------------------------------------------+

The *sIBLedit Utilities* component provides a bridge between *sIBL_GUI* and *sIBLedit*.

Interactions:

-  **sIBLedit Executable Path Line Edit**: *sIBLedit* executable path.

