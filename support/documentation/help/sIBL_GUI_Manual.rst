..  image:: resources/pictures/sIBL_GUI_Logo.png

Manual - Help File
==================

Table Of Content
=================

.. .tocTree

-  `Introduction`_

   -  `Donations`_

-  `Features`_
-  `Installation`_

   -  `Windows Platform`_
   -  `Mac Os X Platform`_
   -  `Linux Platform`_

-  `Usage`_

   -  `User Preferences`_
   -  `Command Line Parameters`_
   -  `Shared Database Configuration`_
   -  `IBL Sets Wizard`_
   -  `Interface`_

      -  `Toolbar`_
      -  `Library Layout`_
      -  `Inspect Layout`_
      -  `Export Layout`_
      -  `Preferences Layout`_

-  `Components`_

   -  `Factory`_

      -  `Components Manager Ui`_
      -  `Preferences Manager`_
      -  `Script Editor`_

   -  `Core`_

      -  `Collections Outliner`_
      -  `Database Browser`_
      -  `Db`_
      -  `Inspector`_
      -  `Templates Outliner`_

   -  `Addons`_

      -  `About sIBL_GUI`_
      -  `Database Operations`_
      -  `Gps Map`_
      -  `Ibl Sets Scanner`_
      -  `Loader Script`_
      -  `Loader Script Options`_
      -  `Locations Browser`_
      -  `Logging Notifier`_
      -  `Online Updater`_
      -  `Preview`_
      -  `Raw Editing Utilities`_
      -  `Rewiring Tool`_
      -  `Search Database`_
      -  `sIBLedit Utilities`_

-  `Api`_
-  `Faq`_
-  `Change Log`_
-  `About`_

.. .introduction

_`Introduction`
===============

| *sIBL_GUI* is an open source lighting assistant making the Image Based Lighting process easier and straight forward through the use of sIbl files (“.Ibl”).
| What is sIBL? It’s a short for “Smart IBL”, a standard describing all informations and files needed to provide a fast and easy Image Based Lighting Setup in the 3d package of your choice.

More detailed informations are available here: http://www.smartibl.com

_`Donations`
------------

With sIBL_GUI 4 release I decided to accept donations, so if you think the application is worth something you can use the following `Paypal <https://www.paypal.com/>`_ button:

.. raw:: html

	<form action="https://www.paypal.com/cgi-bin/webscr" method="post">
	<input type="hidden" name="cmd" value="_s-xclick">
	<input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----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-----END PKCS7-----">
	<input type="image" src="http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Pictures/Make_A_Donation.png" border="0" name="submit" alt="PayPal — The safer, easier way to pay online.">
	<img alt="" border="0" src="https://www.paypalobjects.com/fr_FR/i/scr/pixel.gif" width="1" height="1">
	</form>

.. .features

_`Features`
===========

Why an external application instead of directly using scripting possibilities of the 3d package itself? There are advantages and issues with both methods.

With an external application, “.Ibl” files format parsing, Collections management and database inspection are handled by that application, you write that Framework once and then you can reuse it for other 3d packages.

The bridge between *sIBL_GUI* and the 3d package is done through Templates that output simple loader scripts. That’s one of *sIBL_GUI* strength: It only tooks a few hours to convert the XSI Mental Ray Template into a Maya Mental Ray one. Scripting a native tool with a good interface offering same functionalities as *sIBL_GUI* would have taken days if not weeks.

*sIBL_GUI* is built around `Umbra <https://github.com/KelSolaar/Umbra>`_ Framework in `Python 2.7.1 <http://www.python.org/>`_ and uses some others major libraries / tools:

- `Nokia Qt Ui Framework <http://qt.nokia.com/>`_ is used for the Interface thanks to `PyQt <http://www.riverbankcomputing.co.uk/>`_ bindings.
- `SQLAlchemy <http://www.sqlalchemy.org/>`_ provides the database backbone.
- `SQLAlchemy-migrate <http://code.google.com/p/sqlalchemy-migrate/>`_ adds support for database migrations.
- `Sphinx <http://sphinx.pocoo.org/>`_ provides the documentation build system.
- `Tidy <http://tidy.sourceforge.net/>`_ is used to cleanup docutils documentation html files.

Some highlights:

-  Components Framework.
-  Configurable Ui Layout.
-  SQlite Database.
-  Online Updater.
-  Microsoft Bing Maps Gps map.
-  Internal Images Previewer.

and much more…

Additional informations about *sIBL_GUI* are available into this development thread: `sIBL_GUI Thread <http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371>`_

The source code is available on `github <http://github.com/>`_: http://github.com/KelSolaar

.. .installation

_`Installation`
===============

_`Windows Platform`
-------------------

Installation on Windows is pretty straightforward, just launch “sIBL_GUI.exe”.

_`Mac Os X Platform`
--------------------

Open “sIBL_GUI.dmg” and drag “sIBL_GUI.app” into the “Application” directory.

_`Linux Platform`
-----------------

| *sIBL_GUI 4*  is currently not built on Linux because of several issues.
| You can however grab the source code at Github.com: http://github.com/KelSolaar/sIBL_GUI and launch sIBL_GUI.py file from a shell.

You will need those dependencies:

-  **Python 2.7.1**: http://www.python.org/
-  **PyQt**: http://www.riverbankcomputing.co.uk/
-  **Qt**: http://qt.nokia.com/
-  **SQLAlchemy**: http://www.sqlalchemy.org/
-  **SQLAlchemy-migrate**: http://code.google.com/p/sqlalchemy-migrate/

If you want to build the documentation you will need:

-  **Sphinx**: http://sphinx.pocoo.org/
-  **Tidy** http://tidy.sourceforge.net/

.. .usage

_`Usage`
========

_`User Preferences`
-------------------

*sIBL_GUI* preferences are stored per user in their home directory:

-  C:\\Users\\$USER\\AppData\\Roaming\\HDRLabs\\sIBL_GUI on Windows 7
-  C:\\Documents and Settings\\$USER\\Application Data\\HDRLabs\\sIBL_GUI on Windows XP
-  /Users/$USER/Library/Preferences/HDRLabs/sIBL_GUI on Mac Os X
-  /home/$USER/.HDRLabs/sIBL_GUI on Linux

The typical *sIBL_GUI* preferences directory structure is the following:

+-------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_PreferencesFolder.jpg     |
+-------------------------------------------------------------------+

Structure Description:

-  **components**: Directory storing user components.
-  **database**: Directory storing the SQLite database.

   -  **backup**: Directory used by the *Db* component when it backups the database.
   -  **migrations**: Directory used by the *Db* migration mechanism responsible to migrate the database.

      -  **versions**: Directory used by to store the various migrations scripts.

-  **io**: Directory used for *sIBL_GUI* input / output operations.

   -  **loaderScripts**: Directory used as output directory by the *Loader Script* component.
   -  **remote**: Directory used by the *Online Updater* component when it downloads online files.
   -  **scriptEditor**: Directory containing the default scripts used by the *Script Editor* component.

-  **logging**: Directory storing *sIBL_GUI* logging file.
-  **settings**: Directory storing *sIBL_GUI* settings file.
-  **templates**: Directory storing user Templates (This directory is scanned by *sIBL_GUI* when importing default Templates).

_`Command Line Parameters`
--------------------------

*sIBL_GUI* accepts various command line parameters:

-  **-h, —help**: Display the command line parameters help message and exit. (Mac Os X and Linux only)
-  **-a, —about**: Display application “About” message. (Mac Os X and Linux only)
-  **-v VERBOSITYLEVEL, —verbose=VERBOSITYLEVEL**: Application verbosity levels: 0 = Critical \| 1 = Error \| 2 = Warning \| 3 = Info \| 4 = Debug.
-  **-f LOGGINGFORMATER, —loggingFormatter=LOGGINGFORMATER**: Application Logging Formatter: 'Default, Extended, Standard’.
-  **-u USERAPPLICATIONDATASDIRECTORY, —userApplicationDataDirectory=USERAPPLICATIONDATASDIRECTORY**: User application data directory (Preferences directory).
-  **-s, —hideSplashScreen**: The SplashScreen is not displayed during application startup.
-  **-x, —startupScript**: Execute provided startup script.
-  **-t, —deactivateWorkerThreads**: The Worker Threads are deactivated.
-  **-d DATABASEDIRECTORY, —databaseDirectory=DATABASEDIRECTORY**: Database directory.
-  **-r, —databaseReadOnly**: Database is read only, database write access methods are not exposed into the interface.
-  **-o LOADERSCRIPTSOUTPUTDIRECTORY, —loaderScriptsOutputDirectory=LOADERSCRIPTSOUTPUTDIRECTORY**: Loader scripts output directory.

Note: On Mac Os X, *sIBL_GUI* is launched from command line doing the following::

     cd sIBL_GUI.app
     ./Contents/MacOS/sIBL_GUI

_`Shared Database Configuration`
--------------------------------

If you want to share the same Database between multiple installed versions of *sIBL_GUI* there are 2 solutions:

**Dirty Method**

Copy the Database file **sIBL_Database.sqlite** on every machine that have *sIBL_GUI* installed.

The file is located in one of those directory depending your OS:

-  C:\\Users\\$USER\\AppData\\Roaming\\HDRLabs\\sIBL_GUI\\database\\ on Windows 7
-  C:\\Documents and Settings\\$USER\\Application Data\\HDRLabs\\sIBL_GUI\\database\\ on Windows XP
-  /Users/$USER/Library/Preferences/HDRLabs/sIBL_GUI/database/ on Mac Os X
-  /home/$USER/.HDRLabs/sIBL_GUI/database/ on Linux

**Recommended Method**

It’s possible to share one Database file between multiple *sIBL_GUI* install. In order to do that you need to start *sIBL_GUI* with some command line parameters:

-  **-d DATABASEDIRECTORY, —databaseDirectory=DATABASEDIRECTORY**: This one is mandatory for what you want to do, it will tell *sIBL_GUI* to store / use the database on the provided path.
-  **-r, —databaseReadOnly**: This one is optional, but HIGHLY recommended: It will hide / unexpose from the UI all methods that can write to the Database. That’s something important because the last thing you want is someone screwing the whole database by doing a mistake.

Example Command Line::

     C:\\HDRLabs\\sIBL_GUI\\sIBL_GUI.exe -d “Z:/sIBL_Database/” -r

When the Database is read only, the automatic scanner adding new IBL Sets is deactivated meaning that newly IBL Sets dropped into your library directory won’t be added automatically.

It’s a good idea to put the Database with a real file system write lock in case someone launch a *sIBL_GUI* instance without the command line arguments.

That way you can have artists using the Database a supervisor has defined, and even using different Databases depending on their current production.

_`IBL Sets Wizard`
------------------

The first time *sIBL_GUI* is started a wizard asks to add IBL Sets into the database:

+-----------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_EmptyDatabaseWizard_A.jpg     |
+-----------------------------------------------------------------------+

Choose a directory where are stored some IBL Sets and they will be added to the Default Ibl Sets Collection.

+-----------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_EmptyDatabaseWizard_B.jpg     |
+-----------------------------------------------------------------------+

_`Interface`
------------

*sIBL_GUI* Interface is customizable and comes with 3 main layouts directly available from the main toolbar:

-  `Library Layout`_
-  `Inspect Layout`_
-  `Export Layout`_
-  `Edit Layout`_
-  `Preferences Layout`_

_`Toolbar`
^^^^^^^^^^

+---------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_Toolbar.jpg     |
+---------------------------------------------------------+

Interactions:

**Right clic**: raises a context menu with the Ui Widgets list:

+--------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ToolbarContextMenu.jpg     |
+--------------------------------------------------------------------+

**Central Widget icon**: Shows / Hides the *Database Browser* component widget Ui.

**Layouts icon**: Raises a context menu where the user can store / restore up to 5 custom layouts and recall them whenever needed:

+--------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_LayoutsContextMenu.jpg     |
+--------------------------------------------------------------------+

**Miscellaneous icon**: Raises a context menu with some links and miscellaneous functionalities:

+--------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_MiscellaneousContextMenu.jpg     |
+--------------------------------------------------------------------------+

_`Library Layout`
^^^^^^^^^^^^^^^^^

The *Library layout* is where most of the IBL Sets management is done.

This layout is built around 4 components:

-  `Collections Outliner`_ (core.collectionsOutliner)
-  `Database Browser`_ (core.databaseBrowser)
-  `Search Database`_ (addons.searchDatabase)
-  `Gps Map`_ (addons.gpsMap)

+-------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_SetsCentricLayout.jpg     |
+-------------------------------------------------------------------+

_`Inspect Layout`
^^^^^^^^^^^^^^^^^

The *Inspect layout* is where Ibl Set inspection is done.

This layout is built around 3 components:

-  `Collections Outliner`_ (core.collectionsOutliner)
-  `Inspector`_ (core.inspector)
-  `Gps Map`_ (addons.gpsMap)

+----------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_InspectCentricLayout.jpg     |
+----------------------------------------------------------------------+

_`Export Layout`
^^^^^^^^^^^^^^^^

The *Export layout* is where the bridge between *sIBL_GUI* and the 3d packages is created.

This layout is built around 4 components:

-  `Templates Outliner`_ (core.templatesOutliner)
-  `Database Browser`_ (core.databaseBrowser)
-  `Loader Script`_ (addons.loaderScript)
-  `Loader Script Options`_ (addons.loaderScriptOptions)

An additional but extremely powerful export related component is available by right clicking the main toolbar:

-  `Rewiring Tool`_ (addons.rewiringTool)

+------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_TemplatesCentricLayout.jpg     |
+------------------------------------------------------------------------+

_`Edit Layout`
^^^^^^^^^^^^^^^^^

The *Edit layout* is where Ibl Set are edited.

This layout is built around 1 component:

-  `Script Editor`_ (factory.scriptEditor)

+-------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_EditCentricLayout.jpg     |
+-------------------------------------------------------------------+

_`Preferences Layout`
^^^^^^^^^^^^^^^^^^^^^

The *Preferences layout* is where *sIBL_GUI* behavior is configured.

This layout is built around 2 components:

-  `Components Manager Ui`_ (factory.componentsManagerUi)
-  `Preferences Manager`_ (factory.preferencesManager)

+--------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_PreferencesCentricLayout.jpg     |
+--------------------------------------------------------------------------+

.. .components

_`Components`
=============

*sIBL_GUI* has currently 3 categories of components:

-  **Default Component** (Components inheriting from *Python Object*).
-  **QWidget Component** (Components inheriting from *Qt QWidget*).
-  **QObject Component** (Components inheriting from *Qt QObject*).

Those 2 types are split into 4 main families:

-  **Factory** (Factory required components, not deactivable and not removable).
-  **Core** (Core required components, not deactivable and not removable).
-  **Addons** (Factory optional components, deactivable and removable).
-  **User** (User optional components, deactivable and removable).

_`Factory`
----------

.. _factory.componentsManagerUi:

_`Components Manager Ui` (factory.componentsManagerUi)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ComponentsManagerUi.jpg     |
+---------------------------------------------------------------------+

The *Components Manager Ui* component allows *sIBL_GUI* addons and user components activation / deactivation (Factory and Core components are required and not deactivable). Selected components details are displayed in the bottom *Components Informations* widget.

Interactions:

-  **Right clic**: Displays a context menu described further.

Columns Descriptions:

-  **Components**: Components names (Components are sorted by families).
-  **Activated**: Components activations status.
-  **Category**: Components categories (Default or Ui).
-  **Rank**: Components ranks (Components with a low rank will have a high instantiation priority).
-  **Version**: Components versions.

Context menu:

+--------------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ComponentsManagerUiContextMenu.jpg     |
+--------------------------------------------------------------------------------+

-  **Activate Component(s)**: Activates selected Component(s).
-  **Dectivate Component(s)**: Deactivates selected Component(s).
-  **Reload Component(s)**: Reloads selected Component(s) (Deactivates the component, reloads component code, activates back the component).

Addons Functionalities:

-  **Open Component(s) Location(s) ...**: Opens Component(s) directory(s).

**\*\*\***

.. _factory.preferencesManager:

_`Preferences Manager` (factory.preferencesManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_PreferencesManager.jpg     |
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

**\*\*\***

.. _factory.scriptEditor:

_`Script Editor` (factory.scriptEditor)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ScriptEditor.jpg     |
+--------------------------------------------------------------+

The *Script Editor* component allows directly interaction with *sIBL_GUI* through scripting. It provides various code input acceleration mechanism like basic autocompletion, syntax highlighting, etc ... A status bar widget displays various informations about the currently edited document and allows language grammar change.

| Languages support is provided using custom grammars files but mechanism will be replaced by *Textmate* compliant system in the future.
| *sIBL_GUI* logging messages and commands execution results are displayed in the upper pane.
| By default the *Script Editor* component is using tabs characters to indent lines, at the moment there are no exposed methods to use spaces instead.

Interactions:

-  **Language Combo Box**: Switches the current editor language.
-  **Drag’n’drop**:

   -  Drag’n’dropping an IBL Sets or Templates selection into the *Script Editor* component will open their associated files.
   -  Drag’n’dropping any other type of file on *sIBL_GUI* will open it in the *Script Editor* component.

Menus Bar:

File Menu:

+----------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ScriptEditorFileMenu.jpg     |
+----------------------------------------------------------------------+

-  **New**: Adds a new editor.
-  **Load ...**: Loads user chosen file in a new editor.
-  **Source ...**: Loads user chosen file in a new editor and execute its content.
-  **Save**: Saves current editor content.
-  **Save As ...**: Saves current editor content as user chosen file.
-  **Save All**: Saves all editors content.
-  **Close**: Closes current editor.
-  **Close All**: Closes all editors.

Edit Menu:

+----------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ScriptEditorEditMenu.jpg     |
+----------------------------------------------------------------------+

-  **Undo**: Reverts current editor last changes.
-  **Redo**: Repeats current editor reverted changes.
-  **Cut**: Cuts current editor selected content.
-  **Copy**: Copies current editor selected content.
-  **Paste**: Pastes clipboard content into current editor.
-  **Delete**: Deletes current editor selected content.
-  **Select All**: Selects all editor content.
-  **Goto Line ...**: Scrolls current editor to user chosen line.
-  **Indent Selection**: Indents current editor selected content.
-  **Unindent Selection**: Unindents current editor selected content.
-  **Convert Indentation To Tabs**: Converts current editor indentation to tabs.
-  **Convert Indentation To Spaces**: Converts current editor indentation to spaces.
-  **Remove Trailing Whitespaces**: Removes current editor trailing whitespaces.
-  **Toggle Comments**: Toggles comments on current editor selected content.

Search Menu:

+------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ScriptEditorSearchMenu.jpg     |
+------------------------------------------------------------------------+

-  **Search And Replace ...**: Launches the *Search And Replace* dialog described further below.
-  **Search Next**: Searches next occurence of current editor selected text.
-  **Search Previous**: Searches previous occurence of current editor selected text.

Command Menu:

+-------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ScriptEditorCommandMenu.jpg     |
+-------------------------------------------------------------------------+

-  **Evaluate Selection**: Evaluates current editor selected text.
-  **Evaluate Script**: Evaluates current editor content.

View Menu:

+----------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ScriptEditorViewMenu.jpg     |
+----------------------------------------------------------------------+

-  **Toggle Word Wrap**: Toggles word wrap on current editor.
-  **Toggle Whitespaces**: Toggles whitespaces display on current editor.

Dialogs:

Search And Replace:

+------------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ScriptEditorSearchAndReplace.jpg     |
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

_`Core`
-------

.. _core.collectionsOutliner:

_`Collections Outliner` (core.collectionsOutliner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_CollectionsOutliner.jpg     |
+---------------------------------------------------------------------+

| The *Collections Outliner* component is where the IBL Sets are organized into Collections for better management.
| There is a *Default Collection* where IBL Sets fall when they are added without a specific Collection container.

Interactions:

-  **Double clic**: Edits Collection name or comment.
-  **Right clic**: Displays a context menu described further.
-  **Drag’n’drop**:

   -  Drag’n’dropping an IBL Sets selection from the *Database Browser* component to a Collections Outliner component Collection changes given IBL Sets current Collection.
   -  Drag’n’dropping some IBL Sets files or directories from the Os will raise a message box asking confirmation for their addition into the database.

Columns Descriptions:

-  **Collections**: Collections names (Editable through double click).
-  **IBL Sets**: IBL Sets count per Collections.
-  **Comments**: Collections comments (Editable through double click).

Context menu:

+--------------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_CollectionsOutlinerContextMenu.jpg     |
+--------------------------------------------------------------------------------+

-  **Add Content ...**: Adds a new Collection, then recursively adds chosen directory IBL Sets into the database, assigning them to the new Collection.
-  **Add Collection ...**: Adds a new Collection to the database.
-  **Remove Collection(s) ...**: Removes selected Collections from the database (Overall and Default Collections cannot be removed).

**Note**:

While adding a new Collection, a comment can be directly provided by using a comma separated name and comment.

+----------------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_CollectionsOutlinerAddCollection.jpg     |
+----------------------------------------------------------------------------------+

**\*\*\***

.. _core.databaseBrowser:

_`Database Browser` (core.databaseBrowser)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_DatabaseBrowser.jpg     |
+-----------------------------------------------------------------+

The *Database Browser* component is the central component where IBL Sets are viewed and chosen for export. The component is tracking the IBL Sets files on the disk and reload them automatically when modified.

IBL Sets can be viewed using different views depending the user needs:

Columns View:

+----------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_DatabaseBrowserColumnsView.jpg     |
+----------------------------------------------------------------------------+

Details View:

+----------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_DatabaseBrowserDetailsView.jpg     |
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

-  **Double clic**: Edits selected Ibl Set title.
-  **Right clic**: Displays a context menu described further.
-  **Drag’n’drop**:

   -  Drag’n’dropping an IBL Sets selection from the *Database Browser* component to a *Collections Outliner* component Collection change the selected sets Collection.
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
| ..  image:: resources/pictures/sIBL_GUI_DatabaseBrowserContextMenu.jpg     |
+----------------------------------------------------------------------------+

-  **Add Content ...**: Recursively adds chosen directory IBL Sets into the database assigning them to the selected *Collections Outliner* component Collection or the Default Collection if none is selected.
-  **Add Ibl Set ...**: Adds the selected Ibl Set file into the database assigning it to the selected *Collections Outliner* component Collection or the Default Collection if none is selected.
-  **Remove Ibl Set(s) ...**: Removes selected IBL Sets from the database.
-  **Update Ibl Set(s) Location(s) ...**: Updates selected IBL Sets files paths.

Addons Functionalities:

-  **Edit In sIBLedit ...**: Sends selected IBL Sets to *sIBLedit*.
-  **Open Ibl Set(s) Location(s) ...**: Opens selected IBL Sets directories.
-  **Edit Ibl Set(s) File(s) ...**: Edits selected IBL Sets in the *Script Editor* component or custom user defined text editor.
-  **View Background Image ...**: Views selected IBL Sets background images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Lighting Image ...**: Views selected Ibls Set lighting images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Reflection Image ...**: Views selected Ibls Set reflection images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Plate(s) ...**: Views selected Ibls Set plates images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.

Search widget context menu:

+----------------------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_DatabaseBrowserSearchWidgetContextMenu.jpg     |
+----------------------------------------------------------------------------------------+

**\*\*\***

_`Db` (core.db)
^^^^^^^^^^^^^^^

The *Db* component is the heart of *sIBL_GUI* data storage, it provides the database manipulation, read, write, migration and rotating backup methods.

**\*\*\***

.. _core.inspector:

_`Inspector` (core.inspector)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_Inspector.jpg     |
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

Context menu:

+----------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_InspectorContextMenu.jpg     |
+----------------------------------------------------------------------+

Addons Functionalities:

-  **Edit In sIBLedit ...**: Sends Inspector Ibl Set to *sIBLedit*.
-  **Open Ibl Set Location ...**: Opens Inspector IBL Sets directory.
-  **Edit Ibl Set File ...**: Edits  Inspector Ibl Set in the *Script Editor* component or custom user defined text editor.
-  **View Background Image ...**: Views the Inspector Ibl Set background image in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Lighting Image ...**: Views the Inspector Ibl Set lighting image in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Reflection Image ...**: Views the Inspector Ibl Set reflection image in either the Internal Images Previewer or the application defined in the *Preview* component preferences.
-  **View Plate(s) ...**: Views the Ibl Set Inspector plates images in either the Internal Images Previewer or the application defined in the *Preview* component preferences.

**\*\*\***

.. _core.templatesOutliner:

_`Templates Outliner` (core.templatesOutliner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_TemplatesOutliner.jpg     |
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

Context menu:

+------------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_TemplatesOutlinerContextMenu.jpg     |
+------------------------------------------------------------------------------+

-  **Add Template ...**: Adds the selected Templates file to the database.
-  **Remove Templates(s) ...**: Removes selected Templates from the database.
-  **Import Default Templates**: *sIBL_GUI* will scan for Templates into it’s installation directory and the user preferences directories.
-  **Filter Templates Versions**: *sIBL_GUI* will filter the Templates keeping the highest version of multiple same Templates.
-  **Display Help File(s) ...**: Displays Templates associated help files.

Addons Functionalities:

-  **Open Templates(s) Location(s) ...**: Opens selected Templates directories.
-  **Edit Template(s) File(s) ...**: Edits selected Templates in the *Script Editor* component or custom user defined text editor.

Addons
------

.. _addons.about:

_`About sIBL_GUI` (addons.about)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_About.jpg     |
+-------------------------------------------------------+

The *About* component displays the *About* window.

**\*\*\***

.. _addons.databaseOperations:

_`Database Operations` (addons.databaseOperations)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_DatabaseOperations.jpg     |
+--------------------------------------------------------------------+

The *Database Operations* component allows the user to launch some database maintenance operations.

Interactions:

-  **Synchronize Database Push Button**: Forces database synchronization by reparsing all registered files.

**\*\*\***

.. _addons.gpsMap:

_`Gps Map` (addons.gpsMap)
^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_GpsMap.jpg     |
+--------------------------------------------------------+

The *Gps Map* component is embedding a Microsoft Bing Map into *sIBL_GUI*: Selecting some IBL Sets (Ibl Sets with GEO coordinates) in the *Database Browser* component will display their markers onto the Gps Map.

Interactions:

-  **Zoom In Push Button**: Zooms into the Gps Map.
-  **Zoom Out Push Button**: Zooms out of the Gps Map.
-  **Map Type Combo Box**: Switches the Gps Map style.

   -  Auto: This map type automatically chooses between Aerial and Road mode.
   -  Aerial: This map type overlays satellite imagery onto the map and highlights roads and major landmarks to be easily identifiable amongst the satellite images.
   -  Road: This map type displays vector imagery of roads, buildings, and geography.

**\*\*\***

.. _addons.iblSetsScanner:

_`Ibl Sets Scanner` (addons.iblSetsScanner)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *Ibl Sets Scanner* component is a file scanning component that will automatically register any new Ibl Sets to the Default Collection whenever it founds one in an already existing IBL Sets parent directory. This behavior can be stopped by deactivating the component.

**\*\*\***

.. _addons.loaderScript:

_`Loader Script` (addons.loaderScript)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_LoaderScript.jpg     |
+--------------------------------------------------------------+

The *Loader Script* component is providing the bridge between *sIBL_GUI* and the 3d packages. It parses the selected Ibl Set, extracts data from it, and feeds the selected Template with those data resulting in a loader script that can be executed by the 3d package.

Interactions:

-  **Output Loader Script Push Button**: Outputs the loader script to the output directory.
-  **Send To Software Push Button**: Sends a command to the 3d package that will execute the loader script.
-  **Software Port Spin Box**: Communication port of the host running the target 3d package.
-  **Ip Adress Line Edit**: Ip address of the host running the target 3d package.
-  **Convert To Posix Paths Check Box (Windows Only)**: Windows paths will be converted to Unix paths, drive letters will be trimmed.

Addons Functionalities:

-  **Open Output Folder Push Button**: Opens the output directory.

**\*\*\***

.. _addons.loaderScriptOptions:

_`Loader Script Options` (addons.loaderScriptOptions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_LoaderScriptOptions.jpg     |
+---------------------------------------------------------------------+

The *Loader Script Options* component allows the user to tweak the way the loader script will behave in the 3d package. Templates attributes are exposed in 2 pages where they can be adjusted:

-  **Common Attributes**: Common Template attributes (Refer to the current Template help file for details about an attribute).
-  **Additional Attributes**: Additional Template attributes (Refer to the current Template help file for details about an attribute).

Templates settings are stored per version and restored each time one is selected in *sIBL_GUI* preferences directory.

**\*\*\***

.. _addons.locationsBrowser:

_`Locations Browser` (addons.locationsBrowser)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_LocationsBrowser.jpg     |
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

**\*\*\***

.. _addons.loggingNotifier:

_`Logging Notifier` (addons.loggingNotifier)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *Logging Notifier* component displays logging messages in the status bar.

**\*\*\***

.. _addons.onlineUpdater:

_`Online Updater` (addons.onlineUpdater)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_OnlineUpdater.jpg     |
+---------------------------------------------------------------+

The *Online Updater* component maintains *sIBL_GUI* and it’s Templates up to date by checking HDRLabs repository for new releases on startup or user request.

Interactions:

-  **Get sIBL_GUI Push Button**: Starts *sIBL_GUI* download.
-  **Get Lastest Templates**: Starts selected Templates download.
-  **Open Repository**: Opens HDRLabs repository.

When a download starts the *Download Manager* window will open:

+-----------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_DownloadManager.jpg     |
+-----------------------------------------------------------------+

The *Online Updater* component is configurable in the *Preferences Manager* component:

+--------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_OnlineUpdaterPreferences.jpg     |
+--------------------------------------------------------------------------+

Interactions:

-  **Check For New Releases Push Button**: Checks for new releases on HDRLabs repository.
-  **Check For New Releases On Startup Check Box**: *sIBL_GUI* will check for new releases on startup.
-  **Ignore Non Existing Templates Check Box**: *sIBL_GUI* will ignore non existing Template when checking for new releases, meaning that if a Template for a new 3d package is available, it will be ignored.

**\*\*\***

.. _addons.preview:

_`Preview` (addons.preview)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_Preview.jpg     |
+---------------------------------------------------------+

The *Preview* component provides image viewing capability to *sIBL_GUI* through the use of the Internal Images Previewer or the application defined in the *Preview* component preferences.

Interactions:

-  **Custom Previewer Path Line Edit**: User defined Image Viewer / Editor executable path.

The Internal Images Previewer window provides basic informations about the current Image:

+-----------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_ImagesPreviewer.jpg     |
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

**\*\*\***

.. _addons.rawEditingUtilities:

_`Raw Editing Utilities` (addons.rawEditingUtilities)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_RawEditingUtilities.jpg     |
+---------------------------------------------------------------------+

The *Raw Editing Utilities* component provides text editing capability to *sIBL_GUI*, adding text edition at various entry points in *sIBL_GUI* Ui. The text edition is done either by the *Script Editor* component or an user defined text editor.

Interactions:

-  **Custom Text Editor Path Line Edit**: User defined Text Editor executable path.

**\*\*\***

.. _addons.rewiringTool:

_`Rewiring Tool` (addons.rewiringTool)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_RewiringTool.jpg     |
+--------------------------------------------------------------+

The *Rewiring Tool* component is available by right clicking the main toolbar. This component allows rewiring / remapping of an Ibl Set file to another file of that set or an arbitrary image. This widget is powerful because it’s possible to dynamically generate IBL Sets and arbitrary loads whatever HDR you want and still benefit from *sIBL_GUI* one click lighting setup.

Interactions:

-  **Combo Boxes**: The current image will be remapped to the chosen entry.
-  **Path Line Edits**: The current image will be remapped to the chosen custom image.

**\*\*\***

.. _addons.searchDatabase:

_`Search Database` (addons.searchDatabase)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_SearchDatabaseSearchInTagsCloud.jpg     | ..  image:: resources/pictures/sIBL_GUI_SearchDatabaseSearchInShotTime.jpg     |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------+

The *Search Database* component enables search in the database. There are 2 pages providing different search options:

-  **Search In Tags Cloud**: Searches in database Ibl Sets comments tags cloud generated.
-  **Search In Shot Time**: Searches in shot time range.

Interactions:

-  **Search Database Line Edit**: The string entered will be matched in the selected database field. Regular expressions are accepted. An autocompletion list will raise once characters starts being typed.
-  **Case Insensitive Matching Check Box**: The string matching is done case insensitively.

Search In Shot Time:

-  **From Time Edit**: Time range search start.
-  **To Time Edit**: Time range search end.

**\*\*\***

.. _addons.sIBLeditUtilities:

_`sIBLedit Utilities` (addons.sIBLeditUtilities)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------------------------+
| ..  image:: resources/pictures/sIBL_GUI_sIBLeditUtilities.jpg     |
+-------------------------------------------------------------------+

The *sIBLedit Utilities* component provides a bridge between *sIBL_GUI* and *sIBLedit*.

Interactions:

-  **sIBLedit Executable Path Line Edit**: *sIBLedit* executable path.

.. .api

Api
===

sIBL_GUI Api documentation is available here: `sIBL_GUI - Api <http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/index.html>`_

.. .faq

Faq
===

A “Frequently Asked Questions” thread is available on HDRLabs forum: `Smart Ibl Loaders - Faq <http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271612491>`_

.. .changeLog

Change Log
==========

**sIBL_GUI - Change Log**: http://kelsolaar.hdrlabs.com/sIBL_GUI/Change%20Log/Change%20Log.html

.. .about

About
=====

| *sIBL_GUI* by Thomas Mansencal - 2008 - 2011
| Copyright© 2008 - 2011 - Thomas Mansencal - `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This Software Is Released Under Terms Of GNU GPL V3 License: http://www.gnu.org/licenses/
| http://www.thomasmansencal.com/