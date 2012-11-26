sIBL_GUI
========

..  image:: https://secure.travis-ci.org/KelSolaar/sIBL_GUI.png?branch=master

Introduction
------------

| **sIBL_GUI** is an open source lighting assistant making the Image Based Lighting process easier and straight forward through the use of sIbl files (*.Ibl*).
| What is sIBL? It’s a short for *Smart IBL*, a standard describing all informations and files needed to provide a fast and easy Image Based Lighting Setup in the 3d package of your choice.

More detailed informations are available here: http://www.smartibl.com

..  image:: http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Help/resources/pictures/sIBL_GUI_SetsCentricLayout.jpg

Installation
------------

Windows Platform
^^^^^^^^^^^^^^^^

Installation on Windows is pretty straightforward, just launch *sIBL_GUI.exe*.
In order to support third party images formats through FreeImage you may need to install
`Microsoft Visual C++ 2010 Redistributable Package (x64) <http://download.microsoft.com/download/A/8/0/A80747C3-41BD-45DF-B505-E9710D2744E0/vcredist_x64.exe>`_.

Mac Os X Platform
^^^^^^^^^^^^^^^^^

Open *sIBL_GUI.dmg* and drag *sIBL_GUI 4.app* into the *Application* directory.


Linux Platform
^^^^^^^^^^^^^^

| *sIBL_GUI 4* is currently not built on Linux because of several issues.

The following dependencies are needed:

-  **Python 2.6.7** or **Python 2.7.3**: http://www.python.org/
-  **PyQt**: http://www.riverbankcomputing.co.uk/

To install **sIBL_GUI** from the `Python Package Index <http://pypi.python.org/pypi/sIBL_GUI>`_ you can issue this command in a shell::

      pip install sIBL_GUI

or this alternative command::

      easy install sIBL_GUI

Templates are not included by default and can be downloaded from `sIBL_GUI_Templates <https://github.com/KelSolaar/sIBL_GUI_Templates>`_ repository.

If you want to support third party images formats through FreeImage, you will need to recompile `FreeImage <https://github.com/KelSolaar/FreeImage>`_ with the following patch over it:

- **FreeImage_For_sIBL_GUI**: https://github.com/KelSolaar/FreeImage_For_sIBL_GUI

Alternatively, if you want to directly install from `Github <http://github.com/KelSolaar/sIBL_GUI>`_ source repository::

      git clone git://github.com/KelSolaar/sIBL_GUI.git
      cd sIBL_GUI
      python setup.py install

If you want to build the documentation you will also need:

-  **Tidy** http://tidy.sourceforge.net/

Usage
-----

Once installed, you can launch **sIBL_GUI** using this shell command::

      sIBL_GUI

About
-----

| **sIBL_GUI** by Thomas Mansencal – 2008 - 2012
| Copyright© 2008 - 2012 – Thomas Mansencal – `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This software is released under terms of GNU GPL V3 license: http://www.gnu.org/licenses/
| `http://www.thomasmansencal.com/ <http://www.thomasmansencal.com/>`_