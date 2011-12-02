from setuptools import setup

APP = ["../../src/sIBL_GUI.py"]
DATA_FILES = []
OPTIONS = {"argv_emulation": True, "iconfile": "../../src/sibl_gui/resources/images/Icon_Light_256.icns"}

setup(app=APP,
	data_files=DATA_FILES,
	options={"py2app": OPTIONS},
	setup_requires=["py2app"],)
