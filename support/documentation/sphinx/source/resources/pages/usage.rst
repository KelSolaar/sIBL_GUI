_`Usage`
========

_`User Preferences`
-------------------

sIBL_GUI preferences are stored per user in their home directory:

-  C:\\Users\\$USER\\AppData\\Roaming\\HDRLabs\\sIBL_GUI on Windows 7
-  C:\\Documents and Settings\\$USER\\Application Data\\HDRLabs\\sIBL_GUI on Windows XP
-  /Users/$USER/Library/Preferences/HDRLabs/sIBL_GUI on Mac Os X
-  /home/$USER/.HDRLabs/sIBL_GUI on Linux

The typical sIBL_GUI preferences directory structure is the following:

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_PreferencesFolder.jpg            |
+-------------------------------------------------------------------+

Structure Description:

-  **Templates**: Directory storing user Templates (This directory is scanned by sIBL_GUI when importing default Templates).
-  **settings**: Directory storing sIBL_GUI settings file.
-  **logging**: Directory storing sIBL_GUI logging file.
-  **io**: Directory used for sIBL_GUI input / output operations.

   -  **remote**: Directory used by the Online Updater component when it downloads online files.
   -  **loaderScripts**: Directory used as output directory by the Loader Script component.

-  **database**: Directory storing the SQLite database.

   -  **backup**: Directory used by the Db component when it backups the database.

-  **components**: Directory storing user components.

_`Command Line Parameters`
--------------------------

sIBL_GUI accepts various command line parameters:

-  **-h, —help**: Display the command line parameters help message and exit. (Mac Os X and Linux only)
-  **-a, —about**: Display application “About” message. (Mac Os X and Linux only)
-  **-v VERBOSITYLEVEL, —verbose=VERBOSITYLEVEL**: Application verbosity levels: 0 = Critical \| 1 = Error \| 2 = Warning \| 3 = Info \| 4 = Debug.
-  **-f LOGGINGFORMATER, —loggingFormatter=LOGGINGFORMATER**: Application Logging Formatter: 'Default, Extended, Standard’.
-  **-u USERAPPLICATIONDATASDIRECTORY, —userApplicationDatasDirectory=USERAPPLICATIONDATASDIRECTORY**: User application datas directory (Preferences directory).
-  **-t, —deactivateWorkerThreads**: The Worker Threads are deactivated.
-  **-d DATABASEDIRECTORY, —databaseDirectory=DATABASEDIRECTORY**: Database directory.
-  **-r, —databaseReadOnly**: Database is read only, database write access methods are not exposed into the interface.
-  **-o LOADERSCRIPTSOUTPUTDIRECTORY, —loaderScriptsOutputDirectory=LOADERSCRIPTSOUTPUTDIRECTORY**: Loader scripts output directory.
-  **-s, —hideSplashScreen**: The SplashScreen is not displayed during application startup.

Note: On Mac Os X, sIBL_GUI is launched from command line doing the following: “cd” into “sIBL_GUI.app” directory and enter “./Contents/MacOS/sIBL_GUI” followed by the parameters.

_`Shared Database Configuration`
--------------------------------

If you want to share the same Database between multiple installed versions of sIBL_GUI there are 2 solutions:

**Dirty Method**

Copy the Database file **sIBL_Database.sqlite** on every machine that have sIBL_GUI installed.

The file is located in one of those directory depending your OS:

-  C:\\Users\\$USER\\AppData\\Roaming\\HDRLabs\\sIBL_GUI\\database\\ on Windows 7
-  C:\\Documents and Settings\\$USER\\Application Data\\HDRLabs\\sIBL_GUI\\database\\ on Windows XP
-  /Users/$USER/Library/Preferences/HDRLabs/sIBL_GUI/database/ on Mac Os X
-  /home/$USER/.HDRLabs/sIBL_GUI/database/ on Linux

**Recommended Method**

It’s possible to share one Database file between multiple sIBL_GUI install. In order to do that you need to start sIBL_GUI with some command line parameters:

-  **-d DATABASEDIRECTORY, —databaseDirectory=DATABASEDIRECTORY**: This one is mandatory for what you want to do, it will tell sIBL_GUI to store / use the database on the provided path.
-  **-r, —databaseReadOnly**: This one is optional, but HIGHLY recommended: It will hide / unexpose from the UI all methods that can write to the Database. That’s something important because the last thing you want is someone screwing the whole database by doing a mistake.

Example Command Line:

     C:\\HDRLabs\\sIBL_GUI\\sIBL_GUI.exe -d “Z:/sIBL_Database/” -r

When the Database is read only, the automatic scanner adding new Ibl Sets is deactivated meaning that newly Ibl Sets dropped into your library directory won’t be added automatically.

It’s a good idea to put the Database with a real file system write lock in case someone launch a sIBL_GUI instance without the command line arguments.

That way you can have artists using the Database a supervisor has defined, and even using different Databases depending on their current production.

_`Ibl Sets Wizard`
------------------

The first time sIBL_GUI is started a wizard asks to add Ibl Sets into the database:

+-----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_EmptyDatabaseWizard_A.jpg            |
+-----------------------------------------------------------------------+

Choose a directory where are stored some Ibl Sets and they will be added to the Default Sets Collection.

+-----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_EmptyDatabaseWizard_B.jpg            |
+-----------------------------------------------------------------------+

_`Interface`
------------

sIBL_GUI interface is customizable and comes with 3 main layouts directly available from the main toolbar:

-  `Library Layout`_
-  `Inspect Layout`_
-  `Export Layout`_
-  `Preferences Layout`_

_`Toolbar`
^^^^^^^^^^

+---------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_Toolbar.jpg            |
+---------------------------------------------------------+

Interactions:

**Right clic**: raises a context menu with the Ui Widgets list:

+--------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_ToolbarContextMenu.jpg            |
+--------------------------------------------------------------------+

**Central Widget icon**: Shows / hides the Database Browser component widget Ui.

**Layouts icon**: Raises a context menu where the user can store / restore up to 5 custom layouts and recall them whenever needed:

+--------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_LayoutsContextMenu.jpg            |
+--------------------------------------------------------------------+

**Miscellaneous icon**: Raises a context menu with some links and miscellaneous functionalities:

+--------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_MiscellaneousContextMenu.jpg            |
+--------------------------------------------------------------------------+

_`Library Layout`
^^^^^^^^^^^^^^^^^

The Library layout is where most of the Ibl Sets management is done.
This layout is built around 4 components:

-  `Collections Outliner`_ (core.collectionsOutliner)
-  `Database Browser`_ (core.databaseBrowser)
-  `Search Database`_ (addons.searchDatabase)
-  `Gps Map`_ (addons.gpsMap)

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_SetsCentricLayout.jpg            |
+-------------------------------------------------------------------+

_`Inspect Layout`
^^^^^^^^^^^^^^^^^

The Inspect layout is where Ibl Set inspection is done.
This layout is built around 3 components:

-  `Collections Outliner`_ (core.collectionsOutliner)
-  `Inspector`_ (core.databaseBrowser)
-  `Gps Map`_ (addons.gpsMap)

+----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_InspectCentricLayout.jpg            |
+----------------------------------------------------------------------+

_`Export Layout`
^^^^^^^^^^^^^^^^

The Export layout is where the bridge between sIBL_GUI and the 3d packages is created.
This layout is built around 4 components:

-  `Templates Outliner`_ (core.templatesOutliner)
-  `Database Browser`_ (core.databaseBrowser)
-  `Loader Script`_ (addons.loaderScript)
-  `Loader Script Options`_ (addons.loaderScriptOptions)

An additional but extremely powerful export related component is available by right clicking the main toolbar:

-  `Rewiring Tool`_ (addons.rewiringTool)

+------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TemplatesCentricLayout.jpg            |
+------------------------------------------------------------------------+

_`Preferences Layout`
^^^^^^^^^^^^^^^^^^^^^

The Preferences layout is where sIBL_GUI behavior is configured.
This layout is built around 2 components:

-  `Components Manager`_ (core.componentsManagerUi)
-  `Preferences Manager`_ (core.preferencesManager)

+--------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_PreferencesCentricLayout.jpg            |
+--------------------------------------------------------------------------+

