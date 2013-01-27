import re
from setuptools import setup
from setuptools import find_packages

import sibl_gui.globals.constants

def getLongDescription():
	"""
	This definition returns the Package long description.

	:return: Package long description. ( String )
	"""

	description = []
	with open("README.rst") as file:
		for line in file:
			if ".. code:: python" in line and len(description) >= 2:
				blockLine = description[-2]
				if re.search(r":$", blockLine) and not re.search(r"::$", blockLine):
					description[-2] = "::".join(blockLine.rsplit(":", 1))
				continue

			description.append(line)
	return str().join(description)

setup(name=sibl_gui.globals.constants.Constants.applicationName,
	version=sibl_gui.globals.constants.Constants.releaseVersion,
	author=sibl_gui.globals.constants.__author__,
	author_email=sibl_gui.globals.constants.__email__,
	include_package_data=True,
	packages=find_packages(),
	scripts=["bin/sIBL_GUI"],
	url="https://github.com/KelSolaar/sIBL_GUI",
	license="GPLv3",
	description="sIBL_GUI is an open source lighting assistant making the Image Based Lighting process easier and straight forward through the use of \"Smart Ibl\" files.",
	long_description=getLongDescription(),
	install_requires=["SQLAlchemy>=0.7.8", "Umbra>=1.0.7", "Counter>=1.0.0", "sqlalchemy-migrate>=0.7.2"],
	classifiers=["Development Status :: 5 - Production/Stable",
				"Environment :: Console",
				"Environment :: MacOS X",
				"Environment :: Win32 (MS Windows)",
				"Environment :: X11 Applications :: Qt",
				"Intended Audience :: Developers",
				"Intended Audience :: Other Audience",
				"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
				"Natural Language :: English",
				"Operating System :: OS Independent",
				"Programming Language :: Python :: 2.7",
				"Topic :: Utilities"])
