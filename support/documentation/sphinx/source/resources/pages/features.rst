_`Features`
-----------

Why an external application instead of directly using scripting possibilities of the 3d package itself? There are advantages and issues with both methods.
With an external application, “.Ibl” files format parsing, Collections management and database inspection are handled by that application, you write that framework once and then you can reuse it for other 3d packages.
The bridge between sIBL_GUI and the 3d package is done through Templates that output simple loader scripts. That’s one of sIBL_GUI strength: It only took a few hours to convert the XSI Mental Ray Template into a Maya Mental Ray one. Scripting a native tool with a good interface offering same functionalities as sIBL_GUI would have taken days if not weeks.

sIBL_GUI is built in Python:

- `http://www.python.org/ <http://www.python.org/>`_.
- Nokia Qt Ui Framework: `http://qt.nokia.com/ <http://qt.nokia.com/>`_ is used for the Interface thanks to PyQt bindings:
- `http://www.riverbankcomputing.co.uk/ <http://www.riverbankcomputing.co.uk/>`_
- SQLAlchemy: `http://www.sqlalchemy.org/ <http://www.sqlalchemy.org/>`_ provides the database backbone.

Some highlights:

-  Components Framework.
-  Configurable Ui Layout.
-  SQlite Database.
-  Online Updater.
-  Microsoft Bing Maps Gps map.
-  Internal Image Previewer.

and much more…

Additional informations about sIBL_GUI are available into this development thread: `sIBL_GUI Thread <http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371>`_
The source code is available on `github <http://github.com/>`_: `http://github.com/KelSolaar <http://github.com/KelSolaar>`_

