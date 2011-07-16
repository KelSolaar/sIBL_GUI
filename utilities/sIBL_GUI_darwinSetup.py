from setuptools import setup

APP = ["../../src/umbra/sIBL_GUI.py"]
DATA_FILES = []
OPTIONS = {"argv_emulation": True, "iconfile": "../../src/umbra/resources/Icon_Light_512.icns"}

setup(app=APP,
	data_files=DATA_FILES,
	options={"py2app": OPTIONS},
	setup_requires=["py2app"],)
