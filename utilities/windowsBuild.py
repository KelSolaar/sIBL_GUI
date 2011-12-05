# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH, "support\\_mountzlib.py"),
			os.path.join(HOMEPATH, "support\\useUnicode.py"),
			"z:/Documents/Developement/sIBL_GUI/src/sIBL_GUI.py"],
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
		console=False,
		icon="z:\\Documents\\Developement\\sIBL_GUI\\src\\sibl_gui\\resources\\images\\Icon_Light.ico")
coll = COLLECT(exe,
			a.binaries,
			a.zipfiles,
			a.datas,
			strip=False,
			upx=True,
			name=os.path.join("dist", "sIBL_GUI"))
app = BUNDLE(coll,
			name=os.path.join("dist", "sIBL_GUI.app"))
