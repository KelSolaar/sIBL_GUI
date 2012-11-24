_`Features`
===========

Why an external application instead of directly using scripting capabilities of the 3d package itself? There are advantages and inconvenient with both methods.

With an external application, *.Ibl* files format parsing, Collections management and database inspection are handled by that application, you write that Framework once and then you can reuse it for other 3d packages.

The bridge between **sIBL_GUI** and the 3d package is done through Templates that output simple loader scripts. That’s one of **sIBL_GUI** strength: It only took a few hours to convert the Autodesk Softimage Mental Ray Template into an Autodesk Maya Mental Ray one. Scripting a native tool with a good interface offering same functionalities as **sIBL_GUI** would have taken days if not weeks.

**sIBL_GUI** is built around `Umbra <https://github.com/KelSolaar/Umbra>`_ Framework in `Python <http://www.python.org/>`_ and uses some others major libraries / tools:

-  `Nokia Qt Ui Framework <http://qt.nokia.com/>`_ is used for the Interface thanks to `PyQt <http://www.riverbankcomputing.co.uk/>`_ bindings.
-  `SQLAlchemy <http://www.sqlalchemy.org/>`_ provides the database backbone.
-  `SQLAlchemy-migrate <http://code.google.com/p/sqlalchemy-migrate/>`_ adds support for database migrations.
-  `Sphinx <http://sphinx.pocoo.org/>`_ provides the documentation build system.
-  `Tidy <http://tidy.sourceforge.net/>`_ is used to cleanup docutils documentation html files.

The following softwares are used to generate the Windows and Mac Os X installers:

-  `Actual Installer <http://www.actualinstaller.com/>`_
-  `Drop DMG <http://c-command.com/dropdmg/>`_

Some highlights:

-  Components based Framework.
-  Configurable Ui Layout.
-  SQlite Database.
-  Online Updater.
-  Microsoft Bing Maps Gps map.
-  Internal Images Previewer.
-  Online Exceptions Reporter.

and much more…

Additional informations about **sIBL_GUI** are available into this development thread: `sIBL_GUI Thread <http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371>`_

.. raw:: html

   <br/>

