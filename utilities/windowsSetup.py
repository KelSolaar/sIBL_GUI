#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**windowsSetup.py**

**Platform:**
	Windows.

**Description:**
	This module defines the pyinstaller configuration file.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["a", "pyz", "exe", "coll", "app"]

a = Analysis([os.path.join(HOMEPATH, "support\\_mountzlib.py"),
			os.path.join(HOMEPATH, "support\\useUnicode.py"),
			"z:/Documents/Development/sIBL_GUI/sibl_gui/launcher.py"],
             pathex=["C:\\cygwin\\home\\KelSolaar"],
             excludes=["foundations", "manager", "umbra", "sibl_gui"])

pyz = PYZ(a.pure)

exe = EXE(pyz,
		a.scripts,
		exclude_binaries=1,
		name=os.path.join("build\\pyi.win32\\sIBL_GUI", "sIBL_GUI.exe"),
		debug=False,
		strip=False,
		upx=True,
		console=True if os.environ.get("CONSOLE_BUILD") else False,
		icon="z:\\Documents\\Development\\sIBL_GUI\\sibl_gui\\resources\\images\\Icon_Light.ico")

coll = COLLECT(exe,
			filter(lambda x: "API-MS-Win" not in x[0], a.binaries),
			a.zipfiles,
			a.datas,
			strip=False,
			upx=True,
			name=os.path.join("dist", "sIBL_GUI"))

app = BUNDLE(coll,
			name=os.path.join("dist", "sIBL_GUI.app"))
