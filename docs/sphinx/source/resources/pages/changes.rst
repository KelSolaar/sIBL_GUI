Changes
=======

.. raw:: html

    <div style="color: rgb(160, 96, 64);">
        <h2>Notes:</h2>
        <ul>
            <li>The following changes reflects the changes of <b>sIBL_GUI</b> package and also its dependencies.
            </li>
        </ul>
    </div>

4.0.5 - Stable
--------------

-  Implemented a better version rank calculation definition allowing to properly compare various version formats.
-  Ensured **Reporter** is not initialising the **Crittercism** Client API 2 times.
-  Handle Templates with no attributes sections.
-  Fixed **onlineUpdater** Component exception when trying to install the Templates in an user defined directory.
-  Fixed **templatesOutliner** Component exception when selected Template has no help file.
-  Fixed **Search And Replace** dialog patterns related exception.
-  Fixed **Softimage_MR_Standard** Template issue related to **mia_physicalsun** shader intensity being affected by **sIbl_Feedback** rotation.

4.0.4 - Stable
--------------

| **sIBL_GUI** 4.0.4 - Stable - Milestone: https://github.com/KelSolaar/sIBL_GUI/issues?milestone=5&state=closed
| **Umbra** 1.0.5 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=5&state=closed
| **Foundations** 2.0.5 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=3&state=closed

-  Fixed the encoding related issues preventing the application to work properly.
-  Fixed ui related exception in **Online Updater** component. 
-  Prevented exception in **TCP Server Ui** Component when requested address is not available.

4.0.3 - Stable
--------------

| **sIBL_GUI** 4.0.3 - Stable - Milestone: https://github.com/KelSolaar/sIBL_GUI/issues?milestone=4&state=closed
| **Umbra** 1.0.4 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=4&state=closed
| **Umbra** 1.0.3 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=3&state=closed
| **Umbra** 1.0.2 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=2&state=closed
| **Manager** 2.0.3 - Stable - https://github.com/KelSolaar/Manager/issues?milestone=2&state=closed
| **Manager** 2.0.2 - Stable - https://github.com/KelSolaar/Manager/issues?milestone=1&state=closed
| **Foundations** 2.0.4 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=2&state=closed
| **Foundations** 2.0.3 - Stable - https://github.com/KelSolaar/Foundations/issues?milestone=1&state=closed

-  Implemented an unhandled exceptions **Reporter** connected to https://www.crittercism.com/
-  Ensure that **sIBL_GUI** frozen version doesn't require administrator rights on Windows.
-  Overall Ui style update ( ScrollBars, Icons, etc... ).
-  Add wizard for case when no Templates were found.
-  **Loader Script** Component now uses **TCP Client Ui** Component interface.
-  Implemented mechanism to flush invalid / missing Database entries in **Database Operations** Component.
-  Implemented **Yes to All** / **No to All** buttons in relevant dialogs.
-  Implemented **Trace Ui** Component.
-  Reloading a Component will reload its dependencies in **Components Manager Ui** Component.
-  Implemented command line support for modules execution tracing through **-t, --traceModules** parameter.
-  Implemented support for per instance logging file.
-  Views display user friendly default message.
-  Rename **Db** Component to **Database**.
-  Rename **Database Browser** Component to **Ibl Sets Outliner**.
-  Add support for **Python 2.6**.
-  **sIBL_GUI** is now a distributable Python package: http://pypi.python.org/pypi/sIBL_GUI
-  Dropped support for **XSI_Arnold_Dome_Light**, **XSI_Arnold_Standard** and **XSI_MR_Standard** Templates.
-  Dropped support for **3dsmax** versions prior to **3dsmax 2010**.
-  Dropped support for **Maya** versions prior to **Maya 2011**.
-  Disable **mentalrayGlobals.passAlphaThrough** attribute in **Maya_MR_Standard** and **Maya_MR_Lightsmith** Templates.
-  Fixed various widgets classes, implemented small ui test cases.
-  Fixed inconsistent Ui startup verbose level.
-  Components are properly displayed in **Components Manager Ui** Component.
-  User Templates are properly imported into the user Collection.

4.0.2 - Stable
--------------

I would like to thanks **Jens Lindgren** for providing me a much needed stable PyQt installer. 

| **sIBL_GUI** 4.0.2 - Stable - Milestone: https://github.com/KelSolaar/sIBL_GUI/issues?milestone=3&state=closed
| **Umbra** 1.0.1 - Beta - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=1&state=closed

-  Implemented notifications manager code.
-  Implemented **Search In Files** in **Script Editor** Component.
-  Implemented matching symbols pairs highlighting in **Script Editor** Component.
-  Implemented occurences highlighting in **Script Editor** Component.
-  Implemented **Duplicate Line(s)** methods in **Script Editor** Component.
-  Implemented **Delete Line(s)** methods in **Script Editor** Component.
-  Implemented **Move Up / Down** methods in **Script Editor** Component.
-  Implemented **Font Size Increase / Decrease** methods in **Script Editor** Component.
-  The FAQ have been moved into the documentation: http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/../pages/faq.html
-  Added support for command line files arguments.
-  Refactored the layouts management code.
-  Optimized **Search Database** Component speed.
-  **Online Updater** Component now correctly reports networks errors.
-  Rolled back to Qt 4.7.x thanks to **Jens Lindgren**.
-  Fixed an exception in **Inspector** Component when an Ibl Set is modified and reloaded on Windows Os.
-  Fixed an exception related to drag'n'drop in **Collections Outliner** Component.
-  Ensured workers threads are properly closed on application exit.
-  Handled exception when **FreeImage** library cannot be loaded.

4.0.1 - Beta
------------

**sIBL_GUI** 4.0.1 - Beta - Milestone: https://github.com/KelSolaar/sIBL_GUI/issues?milestone=2&state=closed

-  Implemented asynchronous images loading in related **sIBL_GUI** Components for increased speed and responsiveness.
-  A new **Images Caches Operations** Component has been introduced to allow images caches operations.
-  Dropped **NSIS** installer for **Actual Installer** ( http://www.actualinstaller.com/ ) on Windows Os.
-  Double clicking an Ibl Set in the **Database Browser** Component now opens the **Inspect** layout.
-  Fixed a subtle memory leak related to a Python interpreter issue ( http://bugs.python.org/issue1469629 ), slightly reducing memory consumption. 
-  Fixed an exception in **Inspector** Component when a plate was selected and the view attempted to store the current nodes selection.
-  Fixed an exception in **Inspector** Component when current Ibl Set preview image doesn't exists.

4.0.0 - Alpha
--------------

**sIBL_GUI** 4.0.0 - Alpha - Milestone: https://github.com/KelSolaar/sIBL_GUI/issues?milestone=1&state=closed

-  **sIBL_GUI** is now built around **Umbra**: https://github.com/KelSolaar/Umbra
-  **sIBL_GUI** now features a refreshed new dark Ui theme with new logo, splashscreen and more!
-  x64 is the default new **sIBL_GUI** architecture, there won't be anymore support for x86.
-  **sIBL_GUI** 4.x.x preferences a now stored per version in **./HDRLabs/sIBL_GUI/$MAJOR_VERSION.$MINOR_VERSION** directory.
-  A new **Inspect** layout has been implemented, it makes use of the new **PREVIEWfile** attribute of .ibl files and allows you to browse your Collections using large preview images.
-  A new **Edit** layout has been implemented, it features **Umbra** **Script Editor** Component and allows you to directly edit Ibl Sets or Templates files and interact with **sIBL_GUI**. 
-  Support for Ibl Sets plates has been added (Templates don't create them in scenes yet).
-  Major parts of the underlying architecture have been rewrote for better evolutivity and feature a cleaner code base.
-  Startup speed has been dramaticaly increased (Non frozen application version is more than 4 times faster).
-  **sIBL_GUI** can be toggled to fullscreen using the related option in the **Custom_Layouts** menu.
-  A patches mechanism has been implemented to allow migrations between **sIBL_GUI** versions.
-  The **Logging Window** Component has been replaced by the **Script Editor** Component that allows direct interaction with **sIBL_GUI**.
-  The **Database Backup** Component has been integrated into the **Db** Component.
-  A database migration mechanism has been implemented using SQLAlchemy Migrate, it should allow database structure manipulation for future releases.
-  A new **Database Operations** Component has been introduced to allow manual database synchronization.
-  Adding / Renaming a Collection using an empty name was possible, this incorrect behavior has been fixed.
-  A **Logging Formatter** preferences option has been added, allowing to choose between different logging formatters.
-  Added support for Templates strings: **nodePrefix = @nodePrefix | __Prefix__ | String | Node Prefix**.
-  Added **-f / --loggingFormatter** command line parameter allowing logging formatter choice.
-  Added **-x / --startupScript** command line parameter allowing execution of an user script on startup.
-  Added **-t / --deactivateWorkerThreads** command line parameter allowing Worker Threads deactivation.
-  Renamed **-s / --noSplashScreen** command line parameter to **-s / --hideSplashScreen**.
-  Package directories structure has been deeply reorganized.
-  Documentation has been updated and converted from textile to reStructuredText and is available in different flavors:
   -  Sphinx documentation with chapters and API.
   -  Inline monolitic file for HDRLabs.com.
-  A **defaultScript.py** file is provided to showcase a few high level API features.
-  Templates settings are now stored / restored in preferences folder for each Template release. 
-  Most Maya Templates have been ported toward Python for better maintainability and performance.
-  3dsMax and Softimage / XSI Templates have been refactored for better maintainability.
-  Most Templates allows the user to define the prefix the setup will use for better customization.
-  The Maya, 3dsMax, Softimage / XSI helper scripts have been refactored to be inline with **sIBL_GUI** 4.0.0 release.
-  A donations page has been added and is available here: http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Donations/Make_A_Donation.html

3.5.0 - Stable
--------------

-  Implemented support for **Lightsmith Lights**: http://vimeo.com/20879389.
-  Most of the Templates have been refactored at different level.
-  Fixed an issue where Ibl Sets were displayed multiple times in the **Database Browser** Component.
-  Dropped support for Illuminate Labs Turtle Renderer.

3.1.3 - Stable
--------------

-  Templates have now options to define different light types: **Area**, **Directional**, **Point**, **Spot**, etc...
-  **Search Database** Component **In Tags Cloud** method is now case sensitive.
-  Fixed a remaining issue in **Search Database** Component and empty Ibl Set attributes in the **In Tags Cloud** method.
-  Fixed Windows building file to prevent incorrect Templates folder hierarchy.

3.1.2 - Stable
--------------

-  Fixed issues with the **Search Database** Component and empty Ibl Set attributes.
-  Added new **In Tags Cloud** method to the **Search Database** Component. It's now possible to search for multiples keywords in any order either by typing them in the **Search Database** widget or select them in the **Tags Cloud** widget.
-  **Search Database** widget now has a button to clear the current search.
-  Implemented units tests on **sIBL_GUI** **foundations**, **manager** and **globals** packages.
-  Extracted multiple packages to new repositories for better code reusability.

3.1.1 - Stable
--------------

-  Fixed **Add Content** broken context menu entry of **Collection Outliner** Component.
-  Fixed a code regression preventing export of Ibl Sets with comments.

3.1.0 - Stable
--------------

-  **sIBL_GUI** now uses Python 2.7.1, allowing usage of OrderedDict, Templates attributes are now displayed in correct order.
-  Replaced Google Maps by Bing Maps: Google Maps support is broken at the moment on Qt Webkit.
-  Added **-s / --noSplashScreen** command line parameter allowing user to deactivate the splashscreen.
-  Added support for Templates enums: **lightType = @lightType | Area;Directional;Spot | Enum | Light Type**.
-  Fixed an inconsistency related to the comments in the file parser.
-  Help files stored on network are now properly opened on Windows.
-  Modified Ibl Sets now refresh properly within the current session.
-  Added a new fancy splashscreen image thanks to Bob Groothuis.
-  Updated Windows icon.
-  Lots of code refactoring and updates.

3.0.9 - Stable
--------------

-  **sIBL_GUI** has now an Internal Images Previewer: You can quickly check your Ibl Sets images by right-clicking the **Database Browser** and use one of the new **Preview ...** context menu entry. It's also possible to use an External Viewer / Editor by assigning it in the Preferences. Picturenaut is obviously the way to go: http://www.hdrlabs.com/picturenaut/index.html.
-  Refactored the way Third Party Images formats are loaded by using direct memory access and custom FreeImage library build: Third Party Images loading is now 10 to 20 times faster.
-  Implemented Ibl Sets database display name edition: Double click an Ibl Set in the **Database Browser** Component to edit it's display name.
-  **-r / --databaseReadOnly** command line parameter properly disable **Database Browser**, **Collections Outliner** and **Templates Outliner** Components drag'n'drop capabilities and **Collections Outliner** Component editing capabilities.
-  Fixed a code regression preventing **Templates Informations** widget display.
-  Fixed a potential application crash when dragging multiples Ibl Sets from a Collection to another on Mac Os X.
-  Worker Threads are properly terminated on application exit.
-  Switched Darwin Installer to DropDmg application: Dmg icons are laid out correctly now.

3.0.8 - Stable
--------------

-  **sIBL_GUI** for Windows now is natively built on Windows 7, this should Fixed the slow startup issues reported on Windows Vista / 7.
-  Implemented drag'n'drop in various Components (Network paths are currently not supported on Windows Vista / 7):

   -  **Database Browser** Component: You can drag'n'drop Ibl Sets folders or Ibl Sets files directly from the Os.
   -  **Collections Outliner** Component: You can also drag'n'drop folders or Ibl Sets files directly from the Os.
   -  **Templates Outliner** Component: You can drag'n'drop Templates folders or Templates files directly from the Os.

-  Made the code stronger when **sIBL_GUI** deals with corrupted Ibl / Templates Files.
-  Refactored portions of the exceptions handling code.

3.0.7 - Stable
--------------

-  Standard Output and Standard Errors messages are redirected to the Logging Window.
-  **sIBL_GUI** creates one session per thread for SQLite database access thus increasing application stability.
-  Thumbnails size preference is restored on application start.
-  Each Component has its own section in the preferences file, resulting in a better and stronger file structure. (You will will need to reconfigure Components preferences).
-  Session geometry is always restored on application start ignoring the state of the **Restore Geometry On Layout Change** preferences option.
-  Fixed **Sets Scanner** Component regular expressions, it can now process paths with non alphanumerical characters (**C:/Program Files (x86)/**).
-  Fixed walkers arguments regular expressions so that they search for correct files extensions.
-  Added **-o / --loaderScriptsOutputDirectory** command line parameter allowing user to specify loader scripts output directory.
-  Added **-r / --databaseReadOnly** command line parameter that disable database edition methods.
-  Added **-d / --databaseDirectory** command line parameter allowing user to specify the database directory.
-  Added **-u / --userApplicationDataDirectory** command line parameter allowing user to specify application data directory (Preferences directory).

3.0.6 - Stable
--------------

-  Session layout state is now stored and restored on application start and exit. If you had a previous **sIBL_GUI** 3 installation, you may encounter two issues:

   -  The first time you launch **sIBL_GUI** 3.0.6, the application window will be empty, simply click one of the main toolbar layouts. This is happening because if not absolutely needed I would like to avoid Implementeding compatibility code.
   -  Your settings file will be a bit messy and missing some attributes. This will not prevent **sIBL_GUI** running properly. *It's however advised to remove it!* If you need to preserve some customs layouts, backup your original settings file, and merge them into the new one. Don't hesitate to contact me if you are encountering difficulties while doing the merge.

-  Moved Templates and Ibl Sets scanners to separate threads for increased performances.
-  Added support for command line parameters.
-  Fixed a regression with **Lights|DynamicLights** attribute export.
-  Binded FreeImage C/C++ imaging library, **sIBL_GUI** can now manipulate and access a lot more image formats.
-  Application walker is now skipping Mac Os X **._** files.

3.0.5 - Stable
--------------

-  Templates folders hierarchy has been updated. *It's strongly advised to uninstall any previous **sIBL_GUI** 3 version before installing this stable release.*
-  Database Browser is properly refreshing when a Collection is removed.
-  Database Browser items are again correctly laid out on **sIBL_GUI** resize.
-  Added **debug** verbose messages in a lot of methods.
-  Fixed wrong versions numbers calculations.

3.0.4 - Beta
------------

-  Templates paths are now provided to Loader Scripts.
-  **Database Browser** and **Templates Outliner** Components store / restore their selection when the Database is updated.
-  Changed **Components Manager Ui**, **Database Browser**, **Collections Outliner**, **Templates Outliner** Components to Qt Model / View framework.

3.0.3 - Alpha
-------------

-  Added application icon.
-  Regenerated Templates documentation help files.
-  Added application documentation help file.
-  Added Softimage 2011 Template.
-  Improved startup time.
-  Added callback for Components instantiation.
-  Online Updater skip extracting corrupted .zip files.
-  Changed the Toolbar Widgets.
-  Updated various Ui files / pictures.

3.0.2 - Alpha
-------------

-  Updated various Ui files / pictures.
-  Added Templates Versions filtering context menu option.
-  Merged **Database Browser** and **Thumbnails Size** Components.
-  Changed **Online Updater** Component IODevice to QFile, Windows 7 and Vista downloads are not corrupted anymore.
-  Various Ui tweaks.

3.0.1 - Alpha
-------------

-  Fixed slashes path issues on Windows preventing correct Sets loading in Maya.
-  Fixed Incorrect loaderScript path on Windows Socket Connections.
-  Fixed an error preventing the Templates Locations of being browsed.
-  Fixed drag'n'drop in the Templates Outliner Widget.

3.0.0 - Alpha
-------------

-  Full **sIBL_GUI** rewrite / refactoring.
-  First release in the new repository.

2.1.1 - Stable
--------------

-  Updated **sIBL_GUI** Help / Manual.
-  **sIBL_GUI**_FTP is now starting Download automatically when invoked, **Start Download** Button has been removed.
-  **sIBL_GUI** now restores the last visited folder.
-  Render Combo Box added in the Import Tab (Useful when you have multiple Templates for a Renderer).
-  Refinements in **sIBL_GUI** UI.

2.1.0 - Stable
--------------

-  New ReWire Widget in the Import Tab, you can now for example use the Lighting Image as Background or the Reflection one for the Lighting, it's even possible to load Custom Images so you can nearlly dynamically create your IBL on the fly.
-  Resorted **sIBL_GUI** Updater Columns.
-  Refinements in **sIBL_GUI** UI.
-  Corrected the incorrect Help / Manual Files Download Path on Frozen Executables.

2.0.8 - Stable
--------------

-  Updater / FTP Code Cleanup.
-  Fixed a Bug where more Templates than required were downloaded by **sIBL_GUI** Updater.
-  Debugging Code Cleanup.

2.0.7 - Stable
--------------

-  Refinements in **sIBL_GUI** UI.
-  Better Verbose when Remote Connection failed.
-  Manual / Help Files now load properly from a Windows Server Path.
-  Code Consolidation on Windows.

2.0.6 - Stable
--------------

-  Last Maya Templates are packaged.
-  Corrected a bug introduced during the Custom Text Editor / Browser Code refactoring.
-  Wait Cursor is properly released when Checking For New Releases.

2.0.5 - Release Candidate
-------------------------

-  Updated **sIBL_GUI** Help / Manual.
-  Refinements in **sIBL_GUI** UI.
-  Corrected a bug where user define Custom Editor / Browser weren't starting.
-  A default Picture is used when a Thumbnail is using an unsupported File Format (Tga / Tif are not supported yet for example).
-  Options Table Widgets are now properly reseted when there are no Templates available.
-  **sIBL_GUI** FTP is verbosing when Gathering Files List.
-  It's now possible to choose the Templates you want to download.
-  Custom Widgets code refactoring for better reusability.

2.0.2 - Beta
------------

-  Maya MR Template Help / Manual Files updated.
-  Maya Templates have been updated, VRay For Maya and Turtle For Maya are released as stable.
-  GPS Map is now a .jpg file for faster loading and XSI Addon Packaging Problem.

2.0.1 - Beta
------------

-  Corrected a Windows bug preventing download of Templates / Help.
-  Started Maya VRay and Maya Turtle Help / Manual Files.
-  Added Maya VRay and Maya Turtle Templates.
-  Refactored the Send/Edit sIBL code to something cleaner and stronger.
-  **Ignore Missing Templates** Option sets to False by default now on a fresh install.
-  Refinements in **sIBL_GUI** UI.

2.0.0 - Alpha
-------------

-  Updated **sIBL_GUI** Help / Manual.
-  Refinements in **sIBL_GUI** UI.
-  Trapped some errors if loader script failed.
-  Corrected an error in sIBL_Framework introduced while reorganizing Imports.
-  GPS Map Markers weren't properly resized while using the keyboard shortcuts to zoom in and out.
-  Cleaned a bit the Collection ListWidget ToolTips V2 Support Code.

1.9.2 - Alpha
-------------

-  Updated **sIBL_GUI** Help / Manual.
-  Improved Collection ListWidget ToolTips with Shot Time.
-  Refinements in **sIBL_GUI** UI.
-  Line Edits are not cropping their content anymore on Mac Os X.
-  Changed the About Tab with Links Support, etc.
-  An option is now available in Preferences to Ignore Missing Templates so you are not spammed with Templates you don't have locally.

1.9.1 - Alpha
-------------

-  Updated **sIBL_GUI** Help / Manual.
-  Tweaked the OsWalker so it correctly return files with multiple **.** in their name.
-  Splashscreen now stays on top of other windows.

1.9.0 - Alpha
-------------

-  Templates names have been changed.
-  A Splashscreen is now showing on initialization.
-  **sIBL_GUI** FTP Code has been slightly tweaked.
-  **sIBL_GUI_Updater** is now also checking for Templates releases. This release makes 1.4.X update mechanism obsolete.
-  Catched an exception when the Logging File is deleted while **sIBL_GUI** write into it.
-  Refinements in **sIBL_GUI** UI.
-  I wanted **sIBL_GUI** next stable release to be a 1.5, but since we are introducing the sIBL V2 File Format, I'm jumping the release numbers closer to 2.0.

1.4.3 - Alpha
-------------

-  GPS Map Zooming code has been tweaked, it should be smoother now.
-  Added OpenGL support to the GPS Map. There are some new related options in the preferences.
-  Tweaks in sIBL_Framework Dynamic Lights Handling to correct some problems with Maya Mel Script.
-  Improved sIBL_Parser, it uses now some Regex matching for stronger behavior and the Class is faster too.
-  Added GUI Support for sIBL V2 Format Parameters, Improved the Import Tab and some others minor Interface tweaks.
-  Removed some Remote Connection bugs.
-  Refactored Options Toolbox True/False Buttons to something cleaner and more in line with PyQt.
-  Removed a bug in the Search Function.
-  Cleaned some Functions Tracing related code.
-  Optimised Edit / Browser Code.
-  Exit Code is much cleaner, Logging Handlers are properly stopped and closed.

1.4.2 - Alpha
-------------

-  sIBL_Framework / sIBL_Parser have been refactored to deal with the new introduced parameters.
-  Refinements in **sIBL_GUI** UI.

1.4.1 - Alpha
-------------

-  Refactored some **sIBL_GUI** Methods and changed the GUI Messages code.
-  An Online Version Checker is now checking for **sIBL_GUI** Last Releases.
-  The Manual Browser has been changed to a more powerfull Widget (QWebView).

1.4.0 - Alpha
-------------

-  sIBL_IO Refactored to a more generic Class (sIBL_Parser).
-  Corrected one of the most nastier Bug I encountered since I'm working on **sIBL_GUI**. QSetting Class seems to affect Qt Dynamic Libraries (I'm using the Jpeg one) in a way that was making Qjpeg not working when reading settings.
-  FTP Code is now Threaded. Interface should be smooth while Downloading.
-  **sIBL_GUI** is now able to load multiple Help files (It will be possible to provide Help Files for the Templates now).
-  sIBL_Templates Class has been changed to a more generic and flexible Class (sIBL_Recursive_Walker).
-  Refinements in **sIBL_GUI** UI to include the new Help features.

1.3.0 - Alpha
-------------

-  Added Remote Templates / Help Download with the coding of **sIBL_GUI_FTP** Class. You can now download Templates and the Help directly from HDRLabs FTP. Notice the FTP Code is curently not multithreaded so the interface can be a bit laggy while downloading.
-  Added an Edit button for easier Collection Management.
-  Refinements in **sIBL_GUI** UI.
-  Corrected some Mac Os X related Logging issues.
-  Corrected some sIBL_Framework Logging issues.
-  Reworked the Exception Code.

1.2.6 - Alpha
-------------

-  Corrected a bug with Logging File not being found when opening a **sIBL_GUI** File / Directory Browser.
-  Logging Level is now correctly evaluated at **sIBL_GUI** startup.
-  Fixed the Code Syntax that was making the compiled **sIBL_GUI** Executable to crash on program exit (Console Verbose was disabled because of this in **sIBL_GUI** 1.2.5).
-  Refactored **sIBL_GUI** Settings Code using the QSettings Class.

1.2.5 - Alpha
-------------

-  Refactored **sIBL_GUI** Logging / Verbose: Now **sIBL_GUI** and sIBL_Framework use Python Standard Logging. Both are using a Log file: ****sIBL_GUI**_LogFile.log** for **sIBL_GUI** and **sIBL_Framework_LogFile.log** for sIBL_Framework. Those files are deleted then created each time the softwares start. One side effect is that if you launch two instances of **sIBL_GUI**, they will both output Log to ****sIBL_GUI**_LogFile.log** file, while it will not prevent **sIBL_GUI** from working, both Logging will be mixed.
-  Refactored **sIBL_GUI** Functions Call Trace: A Decorator is now used to trace whenever a function is called.
-  Added a brand new GPS Map under the Collection Browser. You can now see a Marker Cloud of sIBL Locations.
-  Interface Tweak to insert the new GPS Map.
-  Code Comment Improvements.

1.0.0 - Stable
--------------

-  Added **Edit In sIBLEdit** Linux Code though it seems there is maybe a bug with sIBLEdit preventing it to work.

0.9.9 - Release Candidate
-------------------------

-  Corrected introduced Bug in **Open Output Folder** button.
-  Code refactoring around Collections management.
-  Corrected Code execution when clicking Remove button and nothing was selected.
-  Clicking Remove Button when multiple items were selected on same row was throwing an error, this has been Fixed.

0.9.8 - Beta
------------

-  Code refinement for Mac Os X.
-  Mac Os X Release is now available as .dmg files (Thanx to Emanuele Santos and Volxen for their help).
-  Updated Windows NSIS Installer Script Code and corrected some Bugs related to Shortcuts creation.
-  Minor Code tweaks on sIBL_Framework.
-  Updated **sIBL_GUI** Help File - Manual.

0.9.7 - Beta
------------

-  **sIBL_GUI** behavior with corrupted Ibl Sets should be better.
-  Started Mac Os X Code (There is no **sIBL_GUI** packaged version for now).
-  Managed to half pack the Linux Release (You still need to download QT Libraries, refer to the Help File - Manual).
-  Updated **sIBL_GUI** Help File - Manual.

0.9.6 - Alpha
-------------

-  Bug introduced with Linux Code that prevented remote execution with Maya on Windows.
-  Corrected a dangerous behavior introduced with Eclipse NSIS Plugin: It adds this line to the setup script: **RmDir /r /REBOOTOK $INSTDIR**. That means that if you installed by mistake at the root of **Program Files/** and not in **Program Files/**sIBL_GUI****, everything in **Program Files/** will be deleted. **sIBL_GUI** - 0.9.6 For Windows and 12 October Nightly Releases are concerned!

0.9.6 - Alpha
-------------

-  Windows version now uses NSIS Installer for a better user experience.
-  Added Custom Browser Option in Preferences.
-  Added Custom Text Editor in Preferences.
-  Existence of paths from Preferences File is now checked.
-  Linux Code. (Notice that you will need a **TMPDIR** Environment Variable)
-  Documented the Code for Sources Release.

0.9.5 - Alpha
-------------

-  Corrected some erroneus Preferences File save state.
-  Template folder is now recursively scanned, so you can add as many folders you want in, try avoid using same Template names.
-  Refactored the way **sIBL_GUI** is verbosing, each method/definition now output something. Using the Debug Verbose Level will slow down performances.
-  Some Code optimisations/refactoring.
-  Infos in overlay if you keep your mouse over a Ibl Set in the ListView.
-  Search function available.
-  Improved filtering methods and behavior of **sIBL_GUI**.

0.9.4 - Alpha
-------------

-  Refined Socket Connection Code (**sIBL_GUI** can now directly connect to XSI too).
-  Added Custom IP Adress instead of the hardCoded **Localhost** one (**sIBL_GUI** should be able to connect through Network).
-  Connection Address and Port now take their Default Values from the Template.
-  Interface polishing.
-  Removed Collections Items reordering pop when triggering Filtering.
-  Corrected a bug related to the Nice Attribute Name feature and the sIBL Input/Output Class.

0.9.3 - Alpha
-------------

-  Wrote Socket and OLE Connection Code (**sIBL_GUI** can now directly connect To 3dsmax and Maya).
-  Added some eye candy buttons in the Templates Options.
-  Code cleaning and increased Verbose in Debug.

0.9.2 - Alpha
-------------

-  Corrected the Collection Filtering bug (Forget to pass a value to my verbose function!)

0.9.2 - Alpha
-------------

-  Improved Templates folder parsing.
-  Started Socket Connection Code.

0.9.1 - Alpha
-------------

-  Fixed refreshing Log Window bug.

0.9.0 - Alpha
-------------

-  Initial release of **sIBL_GUI** For Windows.

