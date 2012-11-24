_`Usage`
========

.. raw:: html

   <br/>

Once installed, you can launch **sIBL_GUI** using this shell command::

      sIBL_GUI

_`User Preferences`
-------------------

**sIBL_GUI** preferences are stored per user in their home directory:

-  C:\\Users\\$USER\\AppData\\Roaming\\HDRLabs\\sIBL_GUI on Windows 7
-  C:\\Documents and Settings\\$USER\\Application Data\\HDRLabs\\sIBL_GUI on Windows XP
-  /Users/$USER/Library/Preferences/HDRLabs/sIBL_GUI on Mac Os X
-  /home/$USER/.HDRLabs/sIBL_GUI on Linux

The typical **sIBL_GUI** preferences directory structure is the following:

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_PreferencesFolder.jpg            |
+-------------------------------------------------------------------+

Structure Description:

-  **$MAJOR_VERSION.$MINOR_VERSION**: Current **sIBL_GUI** version.

   -  **components**: Directory storing user Components.
   -  **database**: Directory storing the SQLite database.

      -  **backup**: Directory used by the *Database* Component when it backups the database.
      -  **migrations**: Directory used by the *Database* migration mechanism responsible to migrate the database.

         -  **versions**: Directory used by to store the various migrations scripts.

   -  **io**: Directory used for **sIBL_GUI** input / output operations.

      -  **loaderScripts**: Directory used as output directory by the *Loader Script* Component.
      -  **remote**: Directory used by the *Online Updater* Component when it downloads online files.
      -  **scriptEditor**: Directory containing the default scripts used by the *Script Editor* Component.

   -  **logging**: Directory storing **sIBL_GUI** logging file.
   -  **patches**: Directory storing **sIBL_GUI** patches file.
   -  **settings**: Directory storing **sIBL_GUI** settings file.

      -  **templates**: Directory storing Templates settings.

   -  **templates**: Directory storing user Templates (This directory is scanned by **sIBL_GUI** when importing default Templates).

.. raw:: html

   <br/>

_`Command Line Parameters`
--------------------------

**sIBL_GUI** accepts various command line parameters:

-  **-h, —help**: Display the command line parameters help message and exit. (Mac Os X and Linux only)
-  **-a, —about**: Display application *About* message. (Mac Os X and Linux only)
-  **-v VERBOSITYLEVEL, —verbose=VERBOSITYLEVEL**: Application verbosity levels: 0 = Critical \| 1 = Error \| 2 = Warning \| 3 = Info \| 4 = Debug.
-  **-f LOGGINGFORMATER, —loggingFormatter=LOGGINGFORMATER**: Application Logging Formatter: 'Default, Extended, Standard’.
-  **-u USERAPPLICATIONDATASDIRECTORY, —userApplicationDataDirectory=USERAPPLICATIONDATASDIRECTORY**: User application data directory (Preferences directory).
-  **-s, —hideSplashScreen**: The SplashScreen is not displayed during application startup.
-  **-w, —deactivateWorkerThreads**: The Worker Threads are deactivated.
-  **-x STARTUPSCRIPT, --startupScript=STARTUPSCRIPT**: Execute given startup script.
-  **-t TRACEMODULES, --traceModules=TRACEMODULES**: Trace given modules.
-  **-d DATABASEDIRECTORY, —databaseDirectory=DATABASEDIRECTORY**: Database directory.
-  **-r, —databaseReadOnly**: Database is read only, database write access methods are not exposed into the interface.
-  **-o LOADERSCRIPTSOUTPUTDIRECTORY, —loaderScriptsOutputDirectory=LOADERSCRIPTSOUTPUTDIRECTORY**: Loader scripts output directory.

Note: On Mac Os X, **sIBL_GUI** is launched from command line doing the following::

      cd sIBL_GUI.app
      ./Contents/MacOS/sIBL_GUI

.. raw:: html

   <br/>

_`Shared Database Configuration`
--------------------------------

If you want to share the same Database between multiple installed versions of **sIBL_GUI** there are 2 solutions:

**Dirty Method**

Copy the Database file **sIBL_Database.sqlite** on every machine that have **sIBL_GUI** installed.

The file is located in one of those directory depending your OS:

-  C:\\Users\\$USER\\AppData\\Roaming\\HDRLabs\\sIBL_GUI\\$MAJOR_VERSION.$MINOR_VERSION\\database\\ on Windows 7
-  C:\\Documents and Settings\\$USER\\Application Data\\HDRLabs\\sIBL_GUI\\$MAJOR_VERSION.$MINOR_VERSION\\database\\ on Windows XP
-  /Users/$USER/Library/Preferences/HDRLabs/sIBL_GUI/$MAJOR_VERSION.$MINOR_VERSION/database/ on Mac Os X
-  /home/$USER/.HDRLabs/sIBL_GUI/$MAJOR_VERSION.$MINOR_VERSION/database/ on Linux

**Recommended Method**

It’s possible to share one Database file between multiple **sIBL_GUI** install. In order to do that you need to start **sIBL_GUI** with some command line parameters:

-  **-d DATABASEDIRECTORY, —databaseDirectory=DATABASEDIRECTORY**: This one is mandatory for what you want to do, it will tell **sIBL_GUI** to store / use the database on the provided path.
-  **-r, —databaseReadOnly**: This one is optional, but HIGHLY recommended: It will hide / unexpose from the UI all methods that can write to the Database. That’s something important because the last thing you want is someone screwing the whole database by doing a mistake.

Example Command Line::

      C:\\HDRLabs\\sIBL_GUI\\sIBL_GUI.exe -d “Z:/sIBL_Database/” -r

When the Database is read only, the automatic scanner adding new IBL Sets is deactivated meaning that newly IBL Sets dropped into your library directory won’t be added automatically.

It’s a good idea to put the Database with a real file system write lock in case someone launch a **sIBL_GUI** instance without the command line arguments.

That way you can have artists using the Database a supervisor has defined, and even using different Databases depending on their current production.

.. raw:: html

   <br/>

_`IBL Sets Wizard`
------------------

The first time **sIBL_GUI** is started a wizard asks to add IBL Sets into the database:

+-----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_EmptyDatabaseWizard_A.jpg            |
+-----------------------------------------------------------------------+

Choose a directory where are stored some IBL Sets and they will be added to the Default Ibl Sets Collection.

+-----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_EmptyDatabaseWizard_B.jpg            |
+-----------------------------------------------------------------------+

.. raw:: html

   <br/>

_`Interface`
------------

**sIBL_GUI** Interface is customizable and comes with 3 main layouts directly available from the main toolbar:

-  `Library Layout`_
-  `Inspect Layout`_
-  `Export Layout`_
-  `Edit Layout`_
-  `Preferences Layout`_

.. raw:: html

   <br/>

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

**Central Widget icon**: Shows / Hides the *Ibl Sets Outliner* Component widget Ui.

**Layouts icon**: Raises a context menu where the user can store / restore up to 5 custom layouts and recall them whenever needed:

+--------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_LayoutsContextMenu.jpg            |
+--------------------------------------------------------------------+

**Miscellaneous icon**: Raises a context menu with some links and miscellaneous functionalities:

+--------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_MiscellaneousContextMenu.jpg            |
+--------------------------------------------------------------------------+

.. raw:: html

   <br/>

_`Library Layout`
^^^^^^^^^^^^^^^^^

The *Library layout* is where most of the IBL Sets management is done.

This layout is built around 4 Components:

-  :ref:`core.collectionsOutliner`
-  :ref:`core.iblSetsOutliner`
-  :ref:`addons.searchDatabase`
-  :ref:`addons.gpsMap`

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_SetsCentricLayout.jpg            |
+-------------------------------------------------------------------+

.. raw:: html

   <br/>

_`Inspect Layout`
^^^^^^^^^^^^^^^^^

The *Inspect layout* is where Ibl Set inspection is done.

This layout is built around 3 Components:

-  :ref:`core.collectionsOutliner`
-  :ref:`core.inspector`
-  :ref:`addons.gpsMap`

+----------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_InspectCentricLayout.jpg            |
+----------------------------------------------------------------------+

.. raw:: html

   <br/>

_`Export Layout`
^^^^^^^^^^^^^^^^

The *Export layout* is where the bridge between **sIBL_GUI** and the 3d packages is created.

This layout is built around 4 Components:

-  :ref:`core.templatesOutliner`
-  :ref:`core.iblSetsOutliner`
-  :ref:`addons.loaderScript`
-  :ref:`addons.loaderScriptOptions`

An additional but extremely powerful export related Component is available by right clicking the main toolbar:

-  :ref:`addons.rewiringTool`

+------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_TemplatesCentricLayout.jpg            |
+------------------------------------------------------------------------+

.. raw:: html

   <br/>

_`Edit Layout`
^^^^^^^^^^^^^^^^^

The *Edit layout* is where Ibl Set are edited.

This layout is built around 2 Component:

-  :ref:`addons.projectsExplorer`
-  :ref:`factory.scriptEditor`

+-------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_EditCentricLayout.jpg            |
+-------------------------------------------------------------------+

.. raw:: html

   <br/>

_`Preferences Layout`
^^^^^^^^^^^^^^^^^^^^^

The *Preferences layout* is where **sIBL_GUI** behavior is configured.

This layout is built around 2 Components:

-  :ref:`factory.componentsManagerUi`
-  :ref:`factory.preferencesManager`

+--------------------------------------------------------------------------+
| ..  image:: ../pictures/sIBL_GUI_PreferencesCentricLayout.jpg            |
+--------------------------------------------------------------------------+

.. raw:: html

   <br/>

