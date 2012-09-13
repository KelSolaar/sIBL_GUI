_`Installation`
===============

.. raw:: html

   <br/>


_`Windows Platform`
-------------------

Installation on Windows is pretty straightforward, just launch *sIBL_GUI.exe*.
In order to support third party images formats through FreeImage you may need to install
`Microsoft Visual C++ 2010 Redistributable Package (x64) <http://download.microsoft.com/download/A/8/0/A80747C3-41BD-45DF-B505-E9710D2744E0/vcredist_x64.exe>`_.

.. raw:: html

   <br/>

_`Mac Os X Platform`
--------------------

Open *sIBL_GUI.dmg* and drag *sIBL_GUI.app* into the *Application* directory.

.. raw:: html

   <br/>

_`Linux Platform`
-----------------

| *sIBL_GUI 4* is currently not built on Linux because of several issues.
| You can however grab the source code at Github.com: http://github.com/KelSolaar/sIBL_GUI and launch sIBL_GUI.py file from a shell.

You will need those dependencies:

- **Foundations**: https://github.com/KelSolaar/Foundations
- **Manager**: https://github.com/KelSolaar/Manager
- **Umbra**: https://github.com/KelSolaar/Umbra
- **sIBL_GUI_Templates**: https://github.com/KelSolaar/sIBL_GUI_Templates

If you want to support third party images formats through FreeImage, you will need to recompile `FreeImage <3.15.1 http://downloads.sourceforge.net/freeimage/FreeImage3151.zip>`_ with the following patch over it:

- **FreeImage_For_sIBL_GUI**: https://github.com/KelSolaar/FreeImage_For_sIBL_GUI

The following third party dependencies are also needed:

-  **Python 2.7.1**: http://www.python.org/
-  **PyQt**: http://www.riverbankcomputing.co.uk/
-  **Qt**: http://qt.nokia.com/
-  **SQLAlchemy**: http://www.sqlalchemy.org/
-  **SQLAlchemy-migrate**: http://code.google.com/p/sqlalchemy-migrate/

If you want to build the documentation you will need:

-  **Sphinx**: http://sphinx.pocoo.org/
-  **Tidy** http://tidy.sourceforge.net/

.. raw:: html

   <br/>

